# Structured Data — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D5 — Enterprise Deployment (20%) — primary; D2 — Tool Design & MCP Integration (18%) — secondary |
| Task Statements | 5.3 (production patterns), 1.3 (prompt engineering), 2.1 (structured output for tools) |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 14 |

---

## One-Liner

When you need Claude to return raw JSON, code, or other structured data without the chatty commentary it naturally wraps around output, you combine **assistant message prefilling** with **stop sequences** to force Claude into the exact format you need.

---

## The Problem: Claude Wants to Be Helpful

Ask Claude for JSON and you will typically get something like:

````
```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["running"]
  }
}
```

This rule captures EC2 instance state changes when instances start running.
````

The JSON is correct, but it is wrapped in markdown code fences *and* followed by an English explanation. For an AWS EventBridge rule generator where users expect to click "copy" and paste directly into the AWS console, this is terrible UX. Users have to manually select the JSON, strip the fences, and remember not to include the explanation.

This is not a bug in Claude — it is Claude's default helpful behavior leaking into a context where you need raw data. You cannot fix it with `temperature` or a better system prompt alone; Claude will still want to explain itself.

---

## The Solution: Prefill + Stop Sequences

The trick is to give Claude an **assistant message that is already started** — as if Claude had begun its response with the exact opening you want. Then you use a **stop sequence** to cut generation off before Claude can add any trailing text.

```python
messages = []

add_user_message(messages, "Generate a very short event bridge rule as json")
add_assistant_message(messages, "```json")

text = chat(messages, stop_sequences=["```"])
```

The flow:

1. **User message** — tells Claude what to generate
2. **Prefilled assistant message** — `` ```json `` makes Claude think it has already started a markdown code block. The next tokens it generates must continue that block.
3. **Claude generates JSON content** — constrained by the prefill to emit JSON (not prose).
4. **Stop sequence** — when Claude tries to close the code block with `` ``` ``, the API immediately stops generation. No trailing explanation ever appears.

The result is clean JSON with no markdown fences, no commentary, nothing to strip:

```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["running"]
  }
}
```

---

## Why Prefilling Works

Claude is a next-token predictor. When you hand it an assistant message, it treats that message as "what I already said" and continues from there. If the prefill is `` ```json `` then statistically the next tokens are overwhelmingly likely to be valid JSON — because that is what follows an opening markdown fence in the training distribution.

Prefilling is a form of prompt engineering that bypasses the "helpful preamble" instinct. Claude cannot apologize or introduce its answer because from its perspective it has already started writing the JSON. There is no "before the code block" to go back to.

---

## Why Stop Sequences Matter

Without a stop sequence, Claude will happily finish the code block and then continue with its explanation. The prefill solves the start of the output; the stop sequence solves the end.

`stop_sequences` is a list of strings that, when Claude emits them, cause the API to immediately terminate generation. The emitted stop sequence itself is **not** included in the output. So if you pass `stop_sequences=["```"]` and Claude tries to close the fence, generation halts before those backticks appear in the returned text.

You can pass up to (a small number of) stop sequences, and any of them will trigger termination. Common uses:

- `"```"` to stop at a closing markdown fence
- `"\n\n"` to stop at a paragraph break
- Custom delimiters you inject via prefill

---

## Wiring It Into the chat() Helper

Building on the chat function from Lessons 09 and 11, add `stop_sequences`:

```python
from anthropic import Anthropic

client = Anthropic()

def chat(messages, system=None, temperature=1.0, stop_sequences=None):
    params = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
    }
    if system:
        params["system"] = system
    if stop_sequences:
        params["stop_sequences"] = stop_sequences

    message = client.messages.create(**params)
    return message.content[0].text

def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})
```

Same conditional pattern as `system`: only insert `stop_sequences` when provided.

---

## Parsing the Result

Because Claude generates JSON content right after the opening fence, the raw returned text usually contains leading whitespace or newlines. Strip it before parsing:

```python
import json

text = chat(messages, stop_sequences=["```"])
clean_json = json.loads(text.strip())
```

Alternatively, you can be more aggressive and use a regex to extract the first `{...}` or `[...]` block, but `text.strip() + json.loads()` covers the common case.

---

## Beyond JSON

The technique is format-agnostic. Use it anywhere you need clean structured output:

| Target format | Prefill | Stop sequence |
|---------------|---------|---------------|
| JSON | `` ```json `` | `` ``` `` |
| Python code | `` ```python `` | `` ``` `` |
| YAML | `` ```yaml `` | `` ``` `` |
| CSV | `` ```csv `` | `` ``` `` |
| Bulleted list | `- ` | `\n\n` |
| Custom XML | `<output>` | `</output>` |

The pattern is: identify what Claude naturally wraps around the content, use the opening as the prefill, and use the closing as the stop sequence.

---

## Prefill + Stop Sequences vs. Tool Use

For JSON specifically, there is a second (often better) approach: use **tool use** to force Claude to return structured data as a tool input. That gives you a schema-validated JSON object without prefill tricks — Claude treats the JSON as a tool call and the SDK parses it for you.

When should you use which?

| Approach | Best for |
|----------|---------|
| Prefill + stop sequence | Quick, schema-less structured output; simple scripts; non-JSON formats like Python or CSV |
| Tool use (input schema) | Production JSON generation where you want schema validation, type guarantees, and agent-style integration |

Lesson 14 covers the prefill technique because it is the foundation — it works for any format and does not require learning the tool use protocol. Tool use is introduced later in the course.

---

## Common Mistakes

1. **Forgetting the stop sequence** — the prefill solves the start but without `stop_sequences` Claude will close the fence and add explanatory text.
2. **Mismatched fence in prefill and stop sequence** — if you prefill with `` ```json `` but stop on `"\n\n"`, you will capture the closing fence in the output.
3. **Not stripping whitespace before parsing** — `json.loads(text)` will fail on leading newlines; always `text.strip()` first.
4. **Expecting 100% valid JSON without a retry loop** — Claude can still emit malformed JSON occasionally; production code should catch `json.JSONDecodeError` and retry with a lower temperature.
5. **Using prefill when tool use is available** — for production JSON, tool use with `input_schema` gives you validation for free.

> **Key Insight**
>
> Prefilling is the oldest and simplest way to constrain Claude's output format. It works because Claude is a sequence predictor — if you put words in its mouth, it will continue from those words rather than restart with its usual preamble. Combined with `stop_sequences` to cut off trailing explanation, it gives you precise control over output structure without needing tool use or JSON mode. Every CCA candidate should know this pattern cold.

---

## CCA Exam Relevance

- **D5.3 (production patterns)**: prefill + stop sequences is a canonical pattern for extracting clean structured output from Claude.
- **D2 (Tool Design)**: the lesson foreshadows tool use as the next-level approach for JSON generation; the exam may contrast the two.
- **D1.3 (prompt engineering for structured output)**: expect questions about how to force a specific output format without adding explanatory text.

---

## Flashcards

| Front | Back |
|-------|------|
| What two techniques combine to force Claude into a specific output format? | Assistant message prefilling and stop sequences. |
| What does assistant message prefilling do? | It adds an assistant message with a partial response (e.g., `` ```json ``) so Claude continues from that point instead of starting fresh with a preamble. |
| What does `stop_sequences` do? | It lists strings that, when emitted by Claude, immediately terminate generation — the stop sequence itself is not included in the output. |
| What is the typical prefill + stop sequence for extracting pure JSON? | Prefill with `` ```json ``, stop on `` ``` ``. |
| Why does prefilling work mechanically? | Claude is a next-token predictor; given a partial assistant message, it continues from there rather than re-introducing itself. |
| What do you need to do to the result before calling `json.loads()`? | Strip leading/trailing whitespace — `text.strip()` — to remove the newlines Claude emits after the opening fence. |
| When is tool use a better choice than prefill + stop sequences? | For production JSON generation where schema validation and type guarantees are important. |
| Can this technique work for non-JSON formats? | Yes — Python, YAML, CSV, bulleted lists, custom XML. The pattern is prefill the opener, stop on the closer. |
| What is the main risk of relying only on prefill without a stop sequence? | Claude will close the code block and then add an English explanation, defeating the point of the prefill. |
