# Implementing Multiple Turns — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) / D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 1.2 (agentic loop implementation), 2.4 (multi-turn tool loops), 1.3 (multi-turn conversation management) |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 39 |

---

## One-Liner

The agentic loop is a `while True` that calls Claude, checks `response.stop_reason != "tool_use"` to break, otherwise executes every `tool_use` block, wraps each result as a `tool_result` block, and loops again.

---

## The Canonical Agentic Loop

This is the pattern that the entire rest of the agentic ecosystem builds on:

```python
def run_conversation(messages):
    while True:
        response = chat(messages, tools=[get_current_datetime_schema])
        add_assistant_message(messages, response)
        print(text_from_message(response))

        if response.stop_reason != "tool_use":
            break

        tool_results = run_tools(response)
        add_user_message(messages, tool_results)

    return messages
```

**Five steps per iteration:**

1. Call Claude with current history and tool schemas
2. Append the full assistant message to history
3. Surface any text blocks to the user (progress indication)
4. Check `stop_reason` — if it is not `"tool_use"`, break
5. Execute all tool-use blocks and append the results as a user message

The loop terminates only when `stop_reason` is something other than `"tool_use"` — typically `"end_turn"`, but could also be `"max_tokens"` or `"stop_sequence"`.

---

## `stop_reason` as the Authoritative Signal

The `stop_reason` field on the response is the **only** reliable way to know whether Claude wants more tools:

| `stop_reason` value | Meaning | Loop action |
|---------------------|---------|-------------|
| `"tool_use"` | Claude wants to run one or more tools | Execute and loop again |
| `"end_turn"` | Claude has completed its answer | Break, return final response |
| `"max_tokens"` | Hit output length limit | Break, warn user, maybe retry with more tokens |
| `"stop_sequence"` | Matched a stop sequence | Break |

Do not try to infer from block contents. Claude can emit a text block **and** a tool-use block in the same turn; relying on "the response contains text, so we are done" is a classic bug.

---

## `run_tools` — Filter Then Execute

`run_tools` walks the response content, picks out `tool_use` blocks, executes each, and returns a list of `tool_result` blocks:

```python
import json

def run_tools(message):
    tool_requests = [
        block for block in message.content if block.type == "tool_use"
    ]
    tool_result_blocks = []

    for tool_request in tool_requests:
        try:
            tool_output = run_tool(tool_request.name, tool_request.input)
            tool_result_blocks.append({
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": json.dumps(tool_output),
                "is_error": False
            })
        except Exception as e:
            tool_result_blocks.append({
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": f"Error: {e}",
                "is_error": True
            })

    return tool_result_blocks
```

Two invariants this function preserves:

1. **Every tool-use block gets a matching result block** (even on failure)
2. **`tool_use_id` is echoed exactly**, so the API can pair requests and responses

---

## `run_tool` — Scalable Tool Routing

`run_tool` maps tool name → concrete function. The naive version is a chain of `if/elif`, but any production system uses a dict-based registry:

```python
TOOL_REGISTRY = {
    "get_current_datetime": get_current_datetime,
    "add_duration_to_datetime": add_duration_to_datetime,
    # register more tools here
}

def run_tool(tool_name, tool_input):
    if tool_name not in TOOL_REGISTRY:
        raise ValueError(f"Unknown tool: {tool_name}")
    return TOOL_REGISTRY[tool_name](**tool_input)
```

The registry pattern makes adding new tools a pure data change — no edits to the loop logic itself. Combined with `run_tools`, this gives you an agent that scales to dozens of tools without structural rewrites.

---

## Error Handling Inside the Loop

The lesson emphasizes **robust error handling at the tool layer**, not the loop layer. When a tool raises:

1. Catch the exception inside `run_tools`
2. Create a `tool_result` block with `is_error=True` and the stringified error in `content`
3. Continue the loop — let Claude decide what to do next

Claude is surprisingly good at recovering from errors: it may retry with corrected arguments, try a different tool, or report the failure to the user. Your code's job is just to faithfully communicate what happened.

**Do not** try to hide errors or skip the failed block — that would break the `tool_use_id` pairing invariant and cause a 400.

---

## The Complete Workflow

```
┌────────────────────────────────┐
│ User sends question            │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│ chat(messages, tools=[...])    │◀───────────┐
└──────────────┬─────────────────┘            │
               ▼                              │
┌────────────────────────────────┐            │
│ add_assistant_message          │            │
│ print text_from_message        │            │
└──────────────┬─────────────────┘            │
               ▼                              │
         stop_reason                          │
        == "tool_use"?                        │
        /           \                         │
       No            Yes                      │
       ▼              ▼                       │
   ┌───────┐   ┌───────────────┐              │
   │ break │   │ run_tools     │              │
   └───────┘   │ (exec + wrap) │              │
               └──────┬────────┘              │
                      ▼                       │
               ┌──────────────────┐           │
               │ add_user_message │           │
               │ (tool_results)   │───────────┘
               └──────────────────┘
```

Each iteration strictly alternates assistant/user messages. Conversation history grows until Claude converges on a final answer.

---

## Common Mistakes

1. **Using `block.type == "tool_use"` checks instead of `stop_reason`** — works for the common case but fails if Claude emits tool_use blocks that you do not want to execute
2. **Forgetting to append the assistant message before running tools** — breaks the history ordering; the next API call will reject it
3. **Returning the wrong number of `tool_result` blocks** — every `tool_use` must get a result, even on error
4. **Not passing `tools=[...]` on every loop iteration** — Claude needs the schema to resolve tool references in history
5. **Running tools sequentially when they could be parallel** — for IO-bound tools, `asyncio.gather` or thread pools dramatically reduce latency
6. **No max iterations** — a misbehaving Claude can loop forever, burning tokens; always cap the loop

---

> **Key Insight**
>
> The agentic loop is astonishingly small — maybe 15 lines of Python — but it is the atomic unit of every agent framework (LangChain, AutoGPT, Claude Code, MCP clients). Master this pattern and you understand how every tool-using agent works. The signal is always `stop_reason != "tool_use"`; the action is always "execute tools and loop." Everything else is production hardening: parallelism, caching, observability, iteration caps.

---

## CCA Exam Relevance

- **D1 (Agentic Architecture)**: This is THE agentic loop. Expect multiple questions on the `stop_reason` check and the loop structure.
- **D2 (Tool Design & MCP Integration)**: Know how `run_tools` filters blocks and constructs `tool_result` blocks.
- Prime exam scenarios: "how do you know when to stop the loop," "what happens if a tool fails mid-loop," "how do you handle multiple tool calls in one response."

---

## Flashcards

| Front | Back |
|-------|------|
| What is the exact condition for exiting the agentic loop? | `response.stop_reason != "tool_use"` — break on any stop_reason that is not tool_use |
| What does `run_tools` do? | Filters content for `tool_use` blocks, executes each via `run_tool`, and returns a list of `tool_result` blocks |
| How should `run_tools` handle exceptions? | Catch them, create a `tool_result` block with `is_error=True` and the error message in `content`, continue the loop |
| Why use a `TOOL_REGISTRY` dict instead of if/elif? | Scalable routing — adding a new tool becomes a data change, not a logic change |
| What Python call unpacks a `tool_input` dict into a function's keyword arguments? | `tool_function(**tool_input)` |
| What happens if you return fewer `tool_result` blocks than `tool_use` blocks received? | The API rejects the next call with a 400 about missing `tool_use_id` pairings |
| Why must `add_assistant_message` come before running tools? | To preserve history order — the assistant message must exist before the user tool-result message that references it |
| What is the minimum safety feature you must add to a production agentic loop? | A `max_iterations` cap to prevent infinite loops from runaway Claude responses |
