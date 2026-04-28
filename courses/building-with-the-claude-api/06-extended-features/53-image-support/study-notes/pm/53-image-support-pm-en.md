# Image Support — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 2.2 (content blocks), 2.1 (multimodal input), 5.2 (token accounting) |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 53 |

---

## One-Liner

Image support turns the same Claude API into a multimodal endpoint, opening up entire product categories — insurance inspections, medical triage, retail analytics, field-ops automation — that were previously locked behind human-in-the-loop vision work.

---

## Mental Model: Handing the Analyst a Photo

Imagine your company's best analyst. If you ask them "what's going on in this office?" they can answer questions, spot anomalies, and summarize patterns. But today you have to verbally describe the scene to them. Image support is handing the analyst the actual photograph.

The questions you can ask do not change. What changes is that now they are grounded in real visual evidence instead of your description of it. And because Claude reads the photo directly, the analyst never misses something that was "not in the description."

This is the single biggest unlock for any product where the answer depends on seeing, not just reading.

---

## Why PMs Should Care

Product categories that were historically impossible or expensive to automate become viable:

- **Insurance inspections**: satellite or drone imagery fed into a rubric-based prompt replaces a field inspector.
- **Medical triage**: a dermatology app asking Claude to categorize a visible condition (under clinician supervision).
- **E-commerce**: automatic categorization of seller-uploaded product photos.
- **Accessibility**: generating rich alt-text from images on the fly.
- **Content moderation**: flagging sensitive material across a large image feed.
- **Retail analytics**: counting shelves, detecting out-of-stock, or auditing planograms from store photos.

The same Messages API handles all of these. No separate vision product, no separate pricing page, no separate SDK — just a new content block inside the request you already make.

---

## Product Use Cases

### When Image Support Fits

| Need | Why It Works |
|------|-------------|
| Answer questions grounded in a real image (what is in this photo?) | Core capability — Claude sees the image directly |
| Structured extraction from visual content (table counts, category tags) | Works with a well-prompted rubric |
| Quality control or visual audits against written criteria | Rubric + step-by-step prompt gives reliable, consistent scoring |
| Side-by-side comparison of multiple images | Up to 100 images per request, useful for before/after or batch comparisons |

### When Image Support Is Not the Answer

| Need | Better Alternative |
|------|--------------------|
| Real-time video analysis | Vision APIs are single-shot on images, not video pipelines |
| Pixel-perfect measurements or OCR on tiny text | Specialized OCR or CV tools, possibly combined with Claude for reasoning |
| Medical diagnosis (as the sole decision-maker) | Always pair with a clinician; do not ship autonomous diagnosis |
| Very high-throughput batch processing on a tight cost budget | Cost per image grows with resolution; spec the token math early |

---

## PM Decision Framework

| Question | If Yes | Implication |
|----------|--------|-------------|
| Does the user workflow genuinely depend on interpreting an image? | Yes | Image support is a real candidate. |
| Is the answer derivable from a single still frame? | Yes | You are in Claude's sweet spot. |
| Will we be sending more than 100 images per request? | Yes | Batch your workflow — 100 is a hard cap. |
| Can we downsize images to the smallest useful dimensions? | Yes | Do it. Tokens are `(width × height) / 750`, so size matters directly. |
| Do we need pixel-perfect measurements or OCR on tiny text? | Yes | Consider a specialized pre-processor; Claude is for reasoning about the image, not measuring it. |
| Can we write a rubric or methodology the model should follow? | Yes | Accuracy will jump. Naive prompts usually under-deliver. |

---

## Cost, Accuracy, and UX Trade-offs

The token formula matters more than it looks. `(width × height) / 750` is linear in pixel count, which means doubling resolution quadruples token cost. A mobile screenshot at 1170×2532 costs ~3950 tokens per call. At 100k calls a day, that is a visible line item.

Three PM playbooks:

1. **Pre-process aggressively.** Resize to the smallest dimensions that still let Claude see what matters. Test the accuracy floor before shipping.
2. **Bring the same prompt discipline you use for text.** A naive "what's in this image?" prompt will under-perform. Give Claude a rubric, a methodology, and ideally a one-shot reference.
3. **Budget for the 100-image cap.** If your workflow handles hundreds of images per user session, design the batching layer explicitly.

---

## The Prompt Engineering Parallel

One thing to hammer into any spec: **the prompt engineering techniques you use with text apply to images**. This is in the lesson and it is where most naive integrations lose points:

- Simple questions lead to unreliable answers ("how many marbles?" → wrong count).
- Detailed methodology + one-shot example + step decomposition lead to reliable answers.
- Categorical rubrics (define what 1, 2, 3, 4 mean) stabilize quantitative output.

The fire-risk assessment example in the lesson is a PM template: name the steps, list what to look for in each, and define the output categories explicitly. Any vision PRD should read like that.

---

## Common PM Mistakes

1. **Specifying "analyze the image" without a methodology.** The model will do something, but it will not be reliable. Write the rubric into the PRD.
2. **Ignoring the token math.** A full-resolution phone screenshot can cost as much as several pages of text. Model this before picking the feature.
3. **Skipping the image cap review.** Some workflows silently need more than 100 images per request and only discover it in production.
4. **Treating image support as a separate product.** It is a content block inside the same Messages API, which means your existing retries, logging, and auth already work.
5. **Shipping image features without an accuracy eval set.** You do not know if the feature is good until you have labeled a representative sample.
6. **Forgetting safety review on user-uploaded images.** When users can upload arbitrary images, your content-moderation and privacy posture has to level up.

---

> **Key Insight**
>
> Image support is the biggest multimodal product unlock in the Claude API and it costs almost no engineering effort — it is just a new block inside an existing request. The PM work is all in the **prompt rubric** (detailed methodology, one-shot examples, categorical outputs) and the **token math** (size images down, batch around the 100-image cap). Get those two right and entire categories of previously-manual vision work become automatable.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: recognize image blocks as a content-block variant in the same Messages API; no separate endpoint.
- **D5 (Enterprise Deployment)**: remember quotas (100 images, 5 MB, 8000 px single / 2000 px multi) and the `(w × h) / 750` token formula.
- Exam scenario pattern: "image analysis is returning inconsistent answers — what do you recommend?" The intended answer is to apply text-grade prompt discipline (methodology, one-shot, decomposition) and to right-size the image.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the analyst analogy for image support? | Before, you had to describe a photo to your analyst. Now you can hand them the actual photo — the questions are the same, but the grounding is real. |
| What product categories does image support unlock? | Insurance inspections, medical triage (with clinician), e-commerce tagging, accessibility alt-text, content moderation, retail analytics. |
| What is the hard per-request cap on image count? | 100 images total across all messages in a single request. |
| What is the max per-image file size? | 5 MB. |
| What is the token formula for an image? | `tokens = (width × height) / 750`. Doubling resolution quadruples token cost. |
| Why do naive prompts underperform on image tasks? | Because image tasks need the same prompt discipline as text — methodology, rubrics, one-shot examples, step decomposition. |
| What belongs in a PRD for a vision feature? | A rubric / methodology, a token-cost model, a batching plan for the 100-image cap, an accuracy eval set, and a safety review for uploads. |
| When is image support the wrong choice? | Real-time video, pixel-perfect measurement, sole-decision medical diagnosis, or very high-throughput batch processing on tight cost budgets. |
