# Fine-Grained Tool Calling — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%), D5 — Enterprise Deployment (20%) |
| Task Statements | 2.1 (tool schema & selection), 2.4 (multi-turn tool loops), 5.2 (streaming & responsiveness) |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 41 |

---

## One-Liner

Fine-grained tool calling is an opt-in streaming mode that disables server-side JSON validation of tool arguments, letting you receive partial tool_use JSON chunks in real time at the cost of having to handle invalid JSON yourself.

---

## Background: Tool Use + Streaming

When you enable streaming on a messages request with tools, Claude emits events as the response is generated:

- `ContentBlockStart` / `ContentBlockStop`
- `ContentBlockDelta` — for regular text generation
- `InputJsonEvent` — specific to tool_use blocks, delivering partial JSON

Each `InputJsonEvent` carries two key properties:

| Property | Meaning |
|----------|---------|
| `partial_json` | A chunk of JSON representing part of the tool arguments |
| `snapshot` | The cumulative JSON built up from all chunks received so far |

```python
for chunk in stream:
    if chunk.type == "input_json":
        print(chunk.partial_json)     # incremental piece
        current_args = chunk.snapshot # accumulated so far
```

---

## Default Behavior: Buffered Validation

By default, the Anthropic API does **not** forward every token of tool JSON the moment Claude generates it. Instead, the server buffers chunks and validates them against your tool schema before flushing them to the client. The unit of validation is the **top-level key-value pair**.

Given a tool schema that expects:

```json
{
  "abstract": "This paper presents a novel...",
  "meta": {
    "word_count": 847,
    "review": "This paper introduces QuanNet..."
  }
}
```

The API will:

1. Wait until the entire `abstract` value is complete
2. Validate that key-value pair against the schema
3. Send all buffered chunks for `abstract` at once
4. Repeat for the `meta` object

This is why tool-use streaming feels like **delays followed by bursts**, not a smooth token-by-token stream. Validation is protecting you from emitting invalid or unusable partial arguments to your downstream code.

---

## Enabling Fine-Grained Tool Calling

Fine-grained tool calling turns **off** this server-side validation:

```python
run_conversation(
    messages,
    tools=[save_article_schema],
    fine_grained=True,
)
```

The effect:

| Aspect | Default | Fine-Grained |
|--------|---------|--------------|
| JSON validation | On (per top-level key-value) | Off |
| Chunk delivery | Buffered bursts after each valid key | Immediate, token-by-token |
| UX responsiveness | Delayed feel | Real-time feel |
| Invalid JSON possible? | No (rejected/coerced server-side) | **Yes — client must handle** |

With fine-grained enabled, you may receive a `word_count` value well before the rest of the `meta` object is complete, unlocking early UI updates or pre-processing.

---

## Handling Invalid JSON

Because validation is disabled, Claude might emit values that are not yet legal JSON, for example `"word_count": undefined` rather than a number. Your snapshot parser must tolerate this:

```python
import json

for chunk in stream:
    if chunk.type != "input_json":
        continue
    try:
        parsed_args = json.loads(chunk.snapshot)
    except json.JSONDecodeError:
        # Partial / invalid JSON — keep accumulating, do not crash
        continue
    # Once parseable, you can safely act on parsed_args
```

Typical defensive patterns:

1. **Accumulate and retry** — try to parse the snapshot; on failure, wait for more chunks
2. **Per-field extraction** — parse out completed keys with a lenient regex or incremental JSON parser
3. **Final validation** — when `ContentBlockStop` arrives for the tool_use block, perform one last strict parse and schema-check

---

## When to Use Fine-Grained Tool Calling

Enable it when any of these apply:

- You need to **show users real-time progress** on tool argument generation (e.g., streaming a draft article into a preview pane)
- You want to **start processing partial tool results** to reduce end-to-end latency
- The default buffering delays negatively impact your UX
- You can invest in **robust JSON error handling** throughout the streaming pipeline

For most applications, the default (validated) behavior is adequate. Only reach for fine-grained when the buffering pauses are visibly harmful to the user experience.

---

## Comparison With Non-Streaming Tool Use

| Mode | Latency Profile | Validation | Complexity |
|------|----------------|------------|------------|
| Non-streaming | One response at the end | Full schema validation | Simplest |
| Streaming (default) | Bursts between top-level keys | Per-key validation | Medium |
| Streaming (fine-grained) | Smooth token-by-token | None (client's responsibility) | Highest |

Use the simplest mode that meets your UX needs. The added complexity of fine-grained is only justified when buffering delays are actually causing user-visible pauses.

---

## Common Mistakes

1. **Enabling fine-grained without adding JSON error handling** — your stream consumer will crash on the first partial snapshot that fails `json.loads`.
2. **Parsing `partial_json` directly as a standalone JSON document** — `partial_json` is a fragment; parse the `snapshot` instead.
3. **Treating the first parseable snapshot as final** — the snapshot keeps growing; only treat it as final when `ContentBlockStop` fires for that tool_use block.
4. **Using fine-grained for tools that depend on fully validated inputs** — if your downstream code cannot tolerate malformed arguments, stay with the default.
5. **Not final-validating against the schema** — fine-grained skips server validation entirely, so you must validate before executing the tool.

> **Key Insight**
>
> Fine-grained tool calling is a latency/correctness tradeoff: you trade server-side JSON validation for faster, smoother streaming. The default mode is safer; fine-grained is for cases where visible streaming progress is worth the cost of implementing robust JSON error handling on the client.

---

## CCA Exam Relevance

- **D2 (Tool Design)**: Understand that tool argument streaming is buffered by default and validated per top-level key. Know how to opt out.
- **D5 (Enterprise Deployment)**: Latency optimization for production UX — streaming tool_use is a concrete lever.
- Watch for questions that describe "delayed bursts" in tool argument streaming — the answer is that per-key validation is causing the buffering.

---

## Flashcards

| Front | Back |
|-------|------|
| What event type delivers partial tool arguments during streaming? | `InputJsonEvent`, with `partial_json` (chunk) and `snapshot` (cumulative) |
| What does the default streaming mode validate? | Each top-level key-value pair of the tool arguments against the schema |
| What does `fine_grained=True` disable? | Server-side JSON validation of tool arguments during streaming |
| Why does default tool-use streaming feel "bursty"? | The API buffers chunks until a complete, valid top-level key-value pair is ready |
| What is the main risk of fine-grained tool calling? | Claude may emit invalid JSON; the client must handle `json.JSONDecodeError` gracefully |
| When should you enable fine-grained tool calling? | When real-time streaming progress matters and you can implement robust JSON error handling |
| What property gives the accumulated JSON so far? | `snapshot` on the `InputJsonEvent` |
| What must you still do after fine-grained streaming finishes? | Perform a final strict parse and schema check before executing the tool |
