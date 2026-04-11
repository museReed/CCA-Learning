# Using Multiple Tools — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%), D1 — Agentic Architecture (22%) |
| Task Statements | 2.1 (tool schema & selection), 1.2 (tool orchestration), 2.4 (multi-turn tool loops) |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 40 |

---

## One-Liner

Claude can select and chain multiple tools within a single conversation; once you have a core tool-handling infrastructure (schemas list + router function), adding new tools is a simple four-step pattern that scales linearly.

---

## The Core Pattern

Extending Claude from one tool to many requires only four steps per new tool:

1. Implement the Python function
2. Define the JSON schema
3. Add the schema to the `tools=[...]` list
4. Add an `elif` branch in the tool router

No changes to the outer agentic loop. The existing `stop_reason == "tool_use"` check and message accumulation logic all continue to work.

---

## Example: Reminder Agent With Three Tools

```python
tools = [
    get_current_datetime_schema,
    add_duration_to_datetime_schema,
    set_reminder_schema,
]

def run_tool(tool_name: str, tool_input: dict):
    if tool_name == "get_current_datetime":
        return get_current_datetime(**tool_input)
    elif tool_name == "add_duration_to_datetime":
        return add_duration_to_datetime(**tool_input)
    elif tool_name == "set_reminder":
        return set_reminder(**tool_input)
    else:
        raise ValueError(f"Unknown tool: {tool_name}")

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    messages=messages,
)
```

The router is effectively a dispatch table; many teams migrate it to a dict registry once the number of tools exceeds ~5:

```python
TOOL_REGISTRY = {
    "get_current_datetime": get_current_datetime,
    "add_duration_to_datetime": add_duration_to_datetime,
    "set_reminder": set_reminder,
}

def run_tool(tool_name, tool_input):
    return TOOL_REGISTRY[tool_name](**tool_input)
```

---

## How Claude Selects Tools

With multiple tools in the list, Claude reads each schema's `name` + `description` and uses the surrounding conversation context to decide which tool (if any) to call. Selection factors include:

- **Description quality** — a crisp, action-oriented description wins over a vague one
- **Input parameter names** — clearly named params reduce ambiguity
- **User request phrasing** — "remind me" maps obviously to `set_reminder`
- **Chain dependencies** — if a tool needs data it does not have, Claude may first call another tool to acquire it

This is why tool descriptions matter as much as the implementation.

---

## Chained Tool Calls and the Agentic Loop

Example prompt: *"Set a reminder for my doctor's appointment. It is 177 days after Jan 1st, 2050."*

Claude typically handles this as a sequence of tool_use blocks across multiple turns:

1. **Turn 1** — Claude emits a `tool_use` block for `add_duration_to_datetime(start="2050-01-01", days=177)`
2. **Your code** runs the function, returns `"2050-06-27"` as a `tool_result`
3. **Turn 2** — Claude receives the result and emits a `tool_use` block for `set_reminder(date="2050-06-27", description="doctor appointment")`
4. **Your code** runs the function, returns the confirmation
5. **Turn 3** — Claude emits a final `text` block summarizing what it did

Your agent loop keeps calling the API until `stop_reason != "tool_use"`.

---

## Parallel vs. Sequential Tool Calls

A single assistant message can contain **multiple tool_use blocks in parallel** when the tools are independent. For instance, if the user asks "What is the weather in Tokyo AND the current price of AAPL?", Claude may emit both `get_weather` and `get_stock_price` tool_use blocks in the same response. You must execute each and return **all** the `tool_result` blocks in one user message before continuing.

```python
# Collect all tool_use blocks from the assistant turn
tool_uses = [b for b in response.content if b.type == "tool_use"]

# Execute them and build tool_result blocks
tool_results = [
    {
        "type": "tool_result",
        "tool_use_id": tu.id,
        "content": str(run_tool(tu.name, tu.input)),
    }
    for tu in tool_uses
]

# Send all results in a single user message
messages.append({"role": "user", "content": tool_results})
```

Sequential chaining (Tool A result feeds Tool B) requires multiple round-trips to the API and accumulates in `messages` as separate turns.

---

## Message Structure When Multiple Tools Fire

The conversation history for a multi-tool request looks like:

```
user:      "Set a reminder 177 days after Jan 1, 2050"
assistant: [text "I need to calculate the date first"] + [tool_use add_duration_to_datetime]
user:      [tool_result "2050-06-27"]
assistant: [text "Now setting the reminder"] + [tool_use set_reminder]
user:      [tool_result "Reminder set"]
assistant: [text "Done. Reminder scheduled for June 27, 2050."]
```

Notice that assistant messages can mix text blocks and tool_use blocks. Do not strip the text blocks when replaying history — Claude uses them as reasoning context.

---

## Common Mistakes

1. **Forgetting to register the schema** — implementing the Python function and router case, but not adding it to the `tools=[...]` list. Claude never learns the tool exists.
2. **Router silently ignores unknown tools** — always raise on unknown names so typos in the schema surface immediately, instead of silently returning `None`.
3. **Only returning one tool_result when Claude sent multiple tool_uses in parallel** — the API returns an error if the tool_use_id set does not match.
4. **Dropping text blocks from assistant messages** — assistant content can be a list of blocks; when appending to history, keep all blocks intact.
5. **Ambiguous tool descriptions** — "helper tool" or "utility" descriptions confuse Claude. Write imperative, action-first descriptions: "Adds a duration in days to a starting datetime."

> **Key Insight**
>
> The agentic loop for N tools is identical to the loop for one tool. Once `stop_reason == "tool_use"` handling is correct, scaling is purely a matter of registering more schemas and dispatch cases. The architectural cost is constant; the only variable cost is writing high-quality tool descriptions.

---

## CCA Exam Relevance

- **D2 (Tool Design)**: Know how Claude selects among multiple tools based on schema + description. Expect questions on tool dispatch patterns.
- **D1 (Agentic Architecture)**: Recognize parallel tool_use emission and the requirement to return all tool_results in a single user turn.
- **Task 2.4 (multi-turn tool loops)**: Tracing a chained tool-use sequence and identifying where the loop terminates is a frequent question type.

---

## Flashcards

| Front | Back |
|-------|------|
| What are the four steps to add a new tool to a multi-tool agent? | 1) Implement function 2) Define schema 3) Add to tools list 4) Add router case |
| How does Claude choose between multiple tools? | Based on each tool's name, description, parameter names, and the current conversation context |
| Can a single assistant message contain multiple tool_use blocks? | Yes — parallel tool calls appear as multiple tool_use blocks in one response and must all be answered in one user message |
| What must accompany every tool_result you send back? | The matching `tool_use_id` from the assistant's tool_use block |
| When does the agentic loop terminate? | When `stop_reason` is no longer `"tool_use"` (typically `"end_turn"`) |
| Why keep text blocks from assistant turns in history? | Claude uses them as reasoning context; dropping them degrades subsequent turns |
| What is a scalable replacement for a large `if/elif` router? | A dict-based tool registry mapping name to callable |
| What is the risk of an overly generic tool description? | Claude may fail to select the right tool or mis-apply it, leading to bad tool calls |
