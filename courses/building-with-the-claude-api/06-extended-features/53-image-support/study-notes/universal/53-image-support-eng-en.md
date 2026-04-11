# Image Support — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 2.2 (content blocks), 2.1 (multimodal input structure), 5.2 (token accounting) |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 53 |

---

## One-Liner

Claude's image support lets you drop image content blocks into user messages alongside text, turning the same Messages API into a multimodal endpoint — with concrete quotas, token accounting, and the same prompt engineering discipline that text tasks require.

---

## Multimodal Messages, Same API

There is no separate "vision" endpoint. You call `/v1/messages` the way you always do; the difference is that a user message's `content` becomes a list that can mix **image blocks** and **text blocks**. Claude reads the full multimodal payload and replies with a normal text block.

This design is deliberate: existing message-handling code mostly works, and the only new thing is knowing how to construct an image block and account for its token cost.

---

## Hard Limits to Remember

The course calls out a specific set of limits that every production deployment has to respect:

- **Up to 100 images** across all messages in a single request.
- **Max 5 MB per image.**
- **Single image**: max height and max width of **8000 px**.
- **Multiple images**: max height and max width of **2000 px** per image.
- Images can be sent **base64-encoded** or as a **URL** to the image.
- Token cost formula: `tokens = (width_px × height_px) / 750`.

The token formula is important for cost modeling. A 1920×1080 image costs about `2,764` tokens just to include — before any text or response tokens. Resize aggressively: a 1024×1024 image is ~1400 tokens; a 512×512 is ~350. If you do not need full resolution, do not send full resolution.

---

## Image Block Structure

The image block lives inside a user message's content list, next to any text blocks:

```python
import base64

with open("image.png", "rb") as f:
    image_bytes = base64.standard_b64encode(f.read()).decode("utf-8")

add_user_message(messages, [
    # Image Block
    {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/png",
            "data": image_bytes,
        }
    },
    # Text Block
    {
        "type": "text",
        "text": "What do you see in this image?"
    }
])
```

Key details:

- `type: "image"` — not `"image_url"` or anything else.
- `source.type: "base64"` — the other option is URL.
- `source.media_type` — must match the actual file (`image/png`, `image/jpeg`, etc.).
- `source.data` — the base64 string, not raw bytes.

Note the pattern: image block first, then text block. The course's example puts the question *after* the image, which reads like "look at this, now answer this." You can order them either way, but in practice putting the image first and the question right after it is cleanest.

---

## Message Flow Is Unchanged

The request/response cycle works exactly like a text-only conversation. Your server sends a user message with mixed blocks; Claude replies with a text block containing its analysis. Multi-turn conversations, tool use, system prompts — all work the same way on top of image input. Nothing about the loop changes just because one turn included an image.

This is one of the hidden wins of content-block-oriented APIs: adding a new modality does not force new endpoints or new handlers.

---

## Prompting Techniques: The Same Rules Apply

The single biggest takeaway from the lesson: **the prompt engineering techniques you use with text apply just as strongly to images**. A naive question like "How many marbles are in this image?" will often return an incorrect count. A well-engineered prompt will not.

The three techniques the lesson demonstrates:

1. **Detailed guidelines and analysis steps.** Tell Claude the methodology it should use, not just the question.
2. **One-shot or multi-shot examples.** Include a reference image whose answer you know, state the correct answer, then ask about the target image. Claude calibrates off the example.
3. **Breaking complex tasks into smaller steps.** Instead of asking for a final answer, ask for intermediate observations first, then the final judgement.

### Step-by-step counting example from the lesson

```
Analyze this image of marbles and determine the exact count using this methodology:
1. Begin by identifying each unique marble one at a time. Assign each a number as you identify it.
2. Verify your result by counting with a different method. Start from the bottom-left corner and work row by row, from left to right.

What is the exact, verified number of marbles in this image?
```

This simple transformation — from "how many?" to "count with this methodology, then verify with a second pass" — dramatically improves accuracy without changing the model or the image.

---

## Real-World Example: Fire Risk Assessment

The lesson walks through automating fire-risk assessments for home insurance from satellite imagery. Instead of sending a field inspector, an insurance company sends satellite images to Claude with a structured prompt.

The prompt decomposes the task into five explicit steps: residence identification, tree-overhang analysis, fire-risk assessment, defensible-space identification, and a final numerical rating from 1 to 4. Each step tells Claude exactly what to look for.

```
Analyze the attached satellite image of a property with these specific steps:

1. Residence identification: Locate the primary residence on the property by looking for:
   - The largest roofed structure
   - Typical residential features (driveway connection, regular geometry)
   - Distinction from other structures (garages, sheds, pools)

2. Tree overhang analysis: Examine all trees near the primary residence:
   - Identify any trees whose canopy extends directly over any portion of the roof
   - Estimate the percentage of roof covered by overhanging branches (0-25%, 25-50%, 50-75%, 75%+)
   - Note particularly dense areas of overhang

3. Fire risk assessment: For any overhanging trees, evaluate:
   - Potential wildfire vulnerability (ember catch points, continuous fuel paths to structure)
   - Proximity to chimneys, vents, or other roof openings if visible
   - Areas where branches create a "bridge" between wildland vegetation and the structure

4. Defensible space identification: Assess the property's overall vegetative structure:
   - Identify if trees connect to form a continuous canopy over or near the home
   - Note any obvious fuel ladders (vegetation that can carry fire from ground to tree to roof)

5. Fire risk rating: Based on your analysis, assign a Fire Risk Rating from 1-4:
   - Rating 1 (Low Risk): No tree branches overhanging the roof, good defensible space around the home
   - Rating 2 (Moderate Risk): Minimal overhang (<25% of roof), some separation between tree canopies
   - Rating 3 (High Risk): Significant overhang (25-50% of roof), connected tree canopies, multiple vulnerability points
   - Rating 4 (Severe Risk): Extensive overhang (>50% of roof), dense vegetation against structure

For each item above (1-5), write one sentence summarizing your findings, with your final response being the numerical rating.
```

Two patterns to internalize from this prompt:

1. **Named steps with explicit sub-questions.** Not "assess the property" but "look for largest roofed structure; regular geometry; driveway connection."
2. **Categorical bands for quantitative output.** Instead of asking for a single score, define what 1, 2, 3, and 4 mean. This is equivalent to providing a rubric and dramatically stabilizes outputs.

---

## Common Mistakes

1. **Using simple questions on hard visual tasks.** "How many marbles?" without a methodology produces unreliable counts. Always bring text-prompting discipline to image tasks.
2. **Ignoring the token formula.** `tokens = (w × h) / 750` means full-resolution images silently burn token budgets. Resize before encoding.
3. **Exceeding per-image size limits.** 5 MB and 8000 px for single-image / 2000 px for multi-image are hard stops; the API will reject violations.
4. **Forgetting the 100-image cap per request.** Bulk visual workflows must batch by 100.
5. **Mismatching `media_type` and actual file.** Declaring `image/png` for a JPEG will confuse decoding. Inspect the file, don't guess.
6. **Treating the image block as a URL field.** It is a structured content block with `type`, `source.type`, `source.media_type`, and `source.data`. A flat URL string will not work.

---

> **Key Insight**
>
> Claude's image support is not a separate product — it is a new block type inside the same Messages API. The API surface is easy; what matters for production is **token accounting** (the width × height / 750 formula) and **prompt discipline** (step-by-step methodologies, rubrics, and one-shot examples are as important for images as they are for text).

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: image blocks are a content-block variant — know the `type: "image"` shape, `source.type: "base64"`, and `media_type` fields.
- **D5 (Enterprise Deployment)**: remember the quotas (100 images, 5 MB, 8000 px / 2000 px) and the token formula `(w × h) / 750` for cost planning.
- Watch for questions framed as "why is accuracy low on my image task?" — the intended answer is usually "apply the same prompt engineering you use for text: methodology, one-shot examples, step decomposition."

---

## Flashcards

| Front | Back |
|-------|------|
| What is the max number of images in a single Claude API request? | 100 images total across all messages. |
| What is the per-image size limit? | 5 MB. |
| What is the max dimension for a single-image request vs multi-image? | 8000 px for a single image, 2000 px when sending multiple images. |
| What is the formula for image token cost? | `tokens = (width_px × height_px) / 750`. |
| What are the two ways to send an image to Claude? | Base64-encoded inline, or as a URL to the image. |
| What block type do you use for an image, and what field inside holds the data? | `type: "image"`, with `source.type: "base64"` and `source.data` holding the base64 string (plus `source.media_type`). |
| Why does "How many marbles?" often fail on an image? | It is a naive prompt. Image tasks need the same methodology, step-by-step instructions, and one-shot examples that text tasks need. |
| What three prompting techniques does the lesson recommend for image tasks? | 1) Detailed guidelines and methodology, 2) one-shot or multi-shot examples, 3) decomposition into smaller steps. |
| Does adding an image change the message-flow loop? | No — it is still a user message sent to `/v1/messages`, replied to with a text block. The loop is unchanged. |
