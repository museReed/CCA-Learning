# Sending Tool Results — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) / D1 — Agentic Architecture (22%) |
| Task Statements | 2.4 (tool_result block format), 2.2 (content block handling), 1.2 (closing the tool-use loop) |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 37 |

---

## One-Liner

Tool results are delivered back to Claude as `tool_result` content blocks wrapped inside a **user** message, each keyed by a `tool_use_id` that must exactly match the preceding `ToolUseBlock.id`.

---

## From Tool Request to Execution

After Claude returns a `ToolUseBlock`, you invoke your local function using the block's `input` dict. Python's `**` unpacking turns the dict into keyword arguments:

```python
tool_block = response.content[1]  # Example: [TextBlock, ToolUseBlock]
result = get_current_datetime(**tool_block.input)
# Equivalent to: get_current_datetime(format="HH:MM:SS")
```

The `input` dict is guaranteed to match the tool's `input_schema` (assuming Claude complied with it), so unpacking is the idiomatic bridge between JSON Schema and your function signature.

---

## Anatomy of a `tool_result` Block

A `tool_result` block is a user-role content block with exactly these fields:

| Field | Type | Purpose |
|-------|------|---------|
| `type` | Literal `"tool_result"` | Tells the API this block is a tool return |
| `tool_use_id` | String | Must match the `id` from the earlier `ToolUseBlock` |
| `content` | String or list of blocks | Your tool's output, serialized |
| `is_error` | Boolean | `True` if the tool failed; Claude will handle the error accordingly |

```python
messages.append({
    "role": "user",
    "content": [{
        "type": "tool_result",
        "tool_use_id": response.content[1].id,
        "content": "15:04:22",
        "is_error": False
    }]
})
```

The critical invariant: **every `ToolUseBlock` in the prior assistant message must be answered by a matching `tool_result` in the next user message**. The API validates this pairing and will 400 on mismatches.

---

## Content Serialization Rules

The `content` field accepts either a plain string or a list of content blocks. For anything non-trivial, serialize to JSON:

```python
import json

tool_output = {"time": "15:04:22", "timezone": "UTC", "epoch": 1762978180}
result_block = {
    "type": "tool_result",
    "tool_use_id": tool_block.id,
    "content": json.dumps(tool_output),
    "is_error": False
}
```

Claude is trained to parse stringified JSON in tool results, so `json.dumps` is the canonical pattern for structured data. Binary data (images, files) must use the list-of-blocks form with image blocks inside.

---

## Handling Multiple Tool Calls in One Turn

If Claude requests more than one tool in a single response (e.g., "What's 10+10 and 30+30?" produces two `ToolUseBlocks`), you must return **all** corresponding `tool_result` blocks in a single user message:

```python
tool_use_blocks = [b for b in response.content if b.type == "tool_use"]

tool_results = []
for tub in tool_use_blocks:
    output = run_tool(tub.name, tub.input)
    tool_results.append({
        "type": "tool_result",
        "tool_use_id": tub.id,
        "content": json.dumps(output),
        "is_error": False
    })

messages.append({"role": "user", "content": tool_results})
```

Ordering of results within the content list does not matter — the `tool_use_id` is what pairs request and response. But **you cannot skip any**: missing even one result block produces a 400.

---

## Error Handling with `is_error`

When your tool raises, do not omit the result block. Instead, send `is_error: True` and put the error message in `content`:

```python
try:
    output = run_tool(tub.name, tub.input)
    block = {
        "type": "tool_result",
        "tool_use_id": tub.id,
        "content": json.dumps(output),
        "is_error": False
    }
except Exception as e:
    block = {
        "type": "tool_result",
        "tool_use_id": tub.id,
        "content": f"Error: {e}",
        "is_error": True
    }
```

Claude will read the error message and either retry with different arguments, report the failure to the user, or choose a different strategy. Silently dropping a failed tool breaks the ID pairing invariant and causes a 400.

---

## The Follow-Up API Call

The follow-up request must:

1. Include the **full conversation history** (original user message + assistant tool-use message + new user tool-result message)
2. Still pass `tools=[...]` — Claude needs the schema to resolve tool references
3. Use the same `model` and `max_tokens` configuration

```python
client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,  # now has 3+ messages including tool-result
    tools=[get_current_datetime_schema]
)
```

Claude's next response integrates the tool output into natural language. If it needs another tool, you repeat the loop.

---

## Common Mistakes

1. **Putting `tool_result` in an assistant message** — it must be in a **user** role message. The API rejects assistant-role tool results.
2. **Omitting `tool_use_id`** or using a wrong value — causes 400 "mismatched tool_use_id".
3. **Sending a dict/object as `content`** without serializing — `content` must be a string (or list of blocks); pass `json.dumps(data)` for structured output.
4. **Dropping `is_error`** — defaults to `False`, so forgetting it after a failure tells Claude the tool succeeded, leading to hallucinations.
5. **Returning only one result when Claude requested multiple tools** — every `ToolUseBlock` needs a matching `tool_result` block in the same user turn.
6. **Forgetting to pass `tools=[...]` on the follow-up** — Claude rejects history that references tools whose schemas are not present.

---

> **Key Insight**
>
> The `tool_use_id` is a contract between your code and Claude. Every `ToolUseBlock` the assistant emits must be answered by exactly one `tool_result` block in the next **user** message, keyed by the same ID. Think of it like a request/response pairing at the content-block level, not the message level — and remember that even errors must come back as `tool_result` blocks with `is_error: True`, not as missing blocks.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: Know the four fields of a `tool_result` block and which role (`user`) it lives in.
- **D1 (Agentic Architecture)**: Understand the request/result pairing as the fundamental unit of the agentic loop.
- Expect questions presenting malformed `tool_result` blocks (wrong role, missing ID, dict content) and asking which error occurs.

---

## Flashcards

| Front | Back |
|-------|------|
| In which role's message does a `tool_result` block live? | The `user` role — Claude sees tool results as user-provided context |
| Which field on a `tool_result` block pairs it with a prior tool-use request? | `tool_use_id` — must exactly match the `ToolUseBlock.id` |
| What type must the `content` field of a `tool_result` be? | A string (or a list of blocks for images/files) — use `json.dumps` for structured data |
| What should you set `is_error` to when a tool raises? | `True` — and put the error message in `content`, do not drop the block |
| What Python syntax unpacks `ToolUseBlock.input` into keyword arguments? | `my_function(**tool_block.input)` |
| What happens if Claude requests two tools and you only return one result? | The API rejects the follow-up request with a 400 about missing `tool_use_id` pairing |
| Must the follow-up API call still include `tools=[...]`? | Yes — Claude needs the schema to resolve references in conversation history |
| How do you handle multiple tool calls in one turn? | Execute all tools, collect every `tool_result` block, and send them together in a single user message |
