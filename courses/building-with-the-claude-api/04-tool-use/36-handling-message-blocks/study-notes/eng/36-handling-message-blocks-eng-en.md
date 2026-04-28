# Handling Message Blocks — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) / D1 — Agentic Architecture (22%) |
| Task Statements | 2.2 (content block handling), 2.1 (tool schema integration), 1.2 (agentic loop foundation) |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 36 |

---

## One-Liner

When tools are enabled, Claude returns a list of typed content blocks (`TextBlock`, `ToolUseBlock`) instead of a single text string, and your code must iterate over them, preserve the full structure in conversation history, and dispatch on block type.

---

## The Shift From Text-Only to Multi-Block Responses

Without tools, `response.content` is functionally a single `TextBlock`. With `tools=[...]` in the request, Claude can decide to call a function, and the assistant message becomes a **heterogeneous list**:

```python
response = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    tools=[get_current_datetime_schema],
)

# response.content is now a list of blocks:
# [TextBlock(text="I can help you find the current time..."),
#  ToolUseBlock(id="toolu_01...", name="get_current_datetime", input={})]
```

The fundamental change: `response.content` is **always a list of blocks**, and any given turn may mix narration text with one or more tool-use requests.

---

## Anatomy of a `ToolUseBlock`

Each tool-use block carries four fields your code must handle:

| Field | Purpose |
|-------|---------|
| `type` | Always `"tool_use"` — use this to filter blocks by type |
| `id` | Unique per-call ID (e.g., `toolu_01A09q90qw...`). You must echo this back in the matching `tool_result` |
| `name` | Function name the model chose (must match a schema you registered) |
| `input` | Dict of arguments conforming to the tool's `input_schema` |

```python
for block in response.content:
    if block.type == "tool_use":
        tool_id = block.id
        tool_name = block.name
        tool_args = block.input  # dict, unpack with **
```

---

## Preserving Content in Conversation History

Claude is stateless — **you** manage history. When the assistant returns multi-block content, you must append the **entire `response.content` list**, not just the text:

```python
messages.append({
    "role": "assistant",
    "content": response.content   # keep ALL blocks, including ToolUseBlock
})
```

If you flatten this to a string or drop the tool-use block, the next API call will fail because the subsequent `tool_result` block (in a user message) will reference a `tool_use_id` that no longer exists in history. The API enforces this pairing strictly.

---

## `stop_reason` as the Loop Signal

Alongside the content list, each response has a `stop_reason`. When Claude emits a tool-use block, `stop_reason == "tool_use"`. This is the canonical signal that your code must execute a tool and send results back before getting a final answer. Other common values: `"end_turn"` (Claude is done), `"max_tokens"`, `"stop_sequence"`.

---

## Updating Helper Functions for Multi-Block Content

If you previously wrote helpers that assumed text-only content:

```python
# Old (text-only) — BREAKS with tools
def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})
```

Upgrade them to accept either a string or a full `Message` object:

```python
from anthropic.types import Message

def add_assistant_message(messages, message):
    content = message.content if isinstance(message, Message) else message
    messages.append({"role": "assistant", "content": content})
```

This polymorphism is essential once you introduce tools — every call site that used to pass a string now needs to handle typed block lists.

---

## The Complete Tool-Use Flow (Single Turn)

1. Send user message + `tools=[...]` schema list
2. Receive assistant message with `content = [TextBlock, ToolUseBlock]` and `stop_reason="tool_use"`
3. Iterate `response.content`, find `ToolUseBlock`, extract `id`, `name`, `input`
4. Execute the real function locally
5. Append a user message containing a `tool_result` block referencing the same `id`
6. Re-call the API (still passing `tools=[...]`) to get the final natural-language answer

Each step depends on preserving the full block structure — skipping any part breaks the chain.

---

## Common Mistakes

1. **Treating `response.content` as a string** — it is a list of typed blocks when tools are enabled. Use `response.content[0].text` or iterate.
2. **Dropping the `ToolUseBlock` when storing history** — the next turn's `tool_result` will reference an `id` the API cannot find, causing a 400 error.
3. **Assuming exactly one block per response** — Claude may emit narration text plus one or more tool-use blocks in the same turn.
4. **Forgetting to pass `tools=[...]` on the follow-up call** — even after you have the tool result, Claude needs the schema to resolve the tool references in history.
5. **Using block index (`content[1]`) instead of filtering by `type`** — Claude may omit the text block or change block order; always filter on `block.type == "tool_use"`.

---

> **Key Insight**
>
> The moment you add `tools=[...]` to a request, you cross a contract boundary: responses become heterogeneous block lists and history must preserve exact block identity (especially `tool_use_id`). Code that assumed "assistant content is a string" will silently break, and the failures surface as cryptic 400s on subsequent turns. Write helpers that accept `Message` objects from day one.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: Understand the `TextBlock` vs `ToolUseBlock` distinction and how `input_schema` maps to the `input` field on a `ToolUseBlock`.
- **D1 (Agentic Architecture)**: This lesson is the foundation for the agentic loop — `stop_reason == "tool_use"` is the canonical continuation signal.
- Expect questions that show a code snippet assigning `response.content` to a string and ask what goes wrong.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the type of `response.content` when tools are enabled? | A list of typed content blocks (e.g., `TextBlock`, `ToolUseBlock`) |
| Which four fields appear on a `ToolUseBlock`? | `type`, `id`, `name`, `input` |
| What `stop_reason` value signals Claude wants to call a tool? | `"tool_use"` |
| Why must you append the full `response.content` (not just text) to history? | Because the next `tool_result` block references the `ToolUseBlock.id`, which must exist in conversation history |
| How do you safely identify tool-use blocks in a response? | Filter by `block.type == "tool_use"` — never rely on block index |
| Must you still pass `tools=[...]` on the follow-up API call after sending a tool result? | Yes — Claude needs the schema to resolve tool references in prior history |
| What Python idiom unpacks the `ToolUseBlock.input` dict into keyword arguments for your function? | `my_function(**block.input)` |
| What happens if your helper flattens `response.content` to a string? | Subsequent turns fail because the `tool_use_id` referenced in `tool_result` is no longer in history |
