# Introducing Tool Use — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 1.2 (agentic loop foundation), 2.1 (tool schema design), 2.4 (multi-turn tool loops) |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 32 |

---

## One-Liner

Tool use is a structured request/response protocol that lets Claude ask your application to fetch external data or perform actions, bridging the gap between static training knowledge and live, real-world information.

---

## The Problem: Static Knowledge Horizon

Without tools, Claude is bounded by its training cutoff. A user asking "What's the weather in San Francisco?" will get:

> "I'm sorry, but I don't have access to up-to-date weather information."

This is a capability wall, not a prompt problem. No amount of prompt engineering can conjure real-time data that was never in the training set. The same wall appears for:

- Current stock prices, sports scores, news headlines
- Internal company databases and CRM records
- User-specific state (their calendar, their files, their preferences)
- Any side effect in the real world (sending emails, writing files, triggering workflows)

Tools are the architectural answer: instead of trying to prompt around the limitation, you **extend** Claude's capabilities by giving it a structured way to request help from your code.

---

## The Four-Step Tool Use Flow

```
┌──────────┐   1. user question + tool definitions    ┌─────────┐
│  Client  │ ─────────────────────────────────────▶ │ Claude  │
│  (app)   │                                           │   API   │
│          │ ◀───────────────────────────────────────  │         │
│          │   2. tool_use request (name + args)      └─────────┘
│          │
│          │   3. execute function locally
│          │
│          │   4. tool_result with fetched data       ┌─────────┐
│          │ ─────────────────────────────────────▶ │ Claude  │
│          │ ◀───────────────────────────────────────  │   API   │
│          │   5. final natural-language answer       └─────────┘
└──────────┘
```

1. **Initial Request** — You POST the user's question plus a list of available tools (name, description, input_schema) to `/v1/messages`.
2. **Tool Request** — Claude's `stop_reason` returns `"tool_use"` and the response `content` contains a `tool_use` block with `id`, `name`, and `input` (the JSON arguments).
3. **Local Execution** — Your server reads the tool_use block, dispatches to the matching Python function, and captures the result.
4. **Final Response** — You append the `assistant` message and a new `user` message containing a `tool_result` block (matched by `tool_use_id`), then call the API again. Claude synthesizes the final answer.

---

## Minimal Python Example

```python
from anthropic import Anthropic

client = Anthropic()

tools = [{
    "name": "get_weather",
    "description": "Returns the current weather for a given city.",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name, e.g. San Francisco"}
        },
        "required": ["city"]
    }
}]

messages = [{"role": "user", "content": "What's the weather in San Francisco?"}]

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    messages=messages,
)

if response.stop_reason == "tool_use":
    tool_use = next(b for b in response.content if b.type == "tool_use")
    result = fetch_weather(tool_use.input["city"])  # your function

    messages.append({"role": "assistant", "content": response.content})
    messages.append({
        "role": "user",
        "content": [{
            "type": "tool_result",
            "tool_use_id": tool_use.id,
            "content": result,
        }],
    })

    final = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )
    print(final.content[0].text)
```

The critical insight: **tool use is multi-turn**. One user question can span two (or more) API calls.

---

## Why Tools Beat Fine-Tuning for Live Data

| Approach | Freshness | Cost | Maintenance |
|----------|-----------|------|-------------|
| Fine-tune on fresh data | Hours-to-days stale | High (retrain cycle) | Constant retraining |
| RAG (vector search) | Depends on index refresh | Medium (embedding + storage) | Index pipeline |
| **Tool use** | Real-time — hits live source | Pay-per-call | Zero — source of truth is upstream |

Tools are the only pattern where Claude reads directly from the system of record. Nothing is cached, nothing is stale.

---

## Key Benefits

- **Real-time information** — current data that was not in training
- **External system integration** — databases, SaaS APIs, internal services
- **Dynamic responses** — each answer grounded in live state
- **Structured interaction** — Claude declares exactly what it needs via `input_schema`
- **Actionability** — tools can have side effects (not just reads), turning Claude into an agent

---

## Common Mistakes

1. **Forgetting the second API call** — returning the `tool_use` block to the user instead of executing it and calling the API again with the `tool_result`.
2. **Mismatched `tool_use_id`** — the `tool_result` must reference the exact `id` from the `tool_use` block; otherwise Claude loses the thread.
3. **Sending a string when a tool_use is expected** — the assistant message must preserve the full `content` array, not a flattened text string.
4. **Treating tool use as optional** — if your use case needs live data, there is no prompt-engineering workaround; you must use tools.
5. **Not handling `stop_reason`** — you must branch on `stop_reason == "tool_use"` to know whether to continue the loop or emit the final answer.

> **Key Insight**
>
> Tool use is not a single API call — it is a **loop**. Each turn, you inspect `stop_reason`, and if it is `tool_use`, you execute locally, append a `tool_result`, and call the API again. This loop is the foundation of every agentic pattern in the CCA curriculum. Understanding it well unlocks D1 (agents) and D2 (tool design).

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: tool_use request/response flow, `tool_use` and `tool_result` block types, `input_schema` as JSON Schema.
- **D1 (Agentic Architecture)**: the tool use loop IS the minimal agentic loop. Multi-turn tool calls form the basis of more complex agent patterns.
- Watch for exam questions framed as: "Claude needs real-time weather" → answer is always tools, never prompt engineering.

---

## Flashcards

| Front | Back |
|-------|------|
| What problem does tool use solve? | Claude's static training cutoff — it lets Claude access real-time data and external systems it could not otherwise reach. |
| What `stop_reason` indicates Claude wants to call a tool? | `"tool_use"` |
| What content block does Claude emit when requesting a tool? | A `tool_use` block containing `id`, `name`, and `input` (JSON arguments). |
| How does your app return a tool's output to Claude? | By sending a new user message with a `tool_result` block that references the original `tool_use_id`. |
| How many API calls does a single tool use round trip require? | At least two — one to receive the tool_use request, one to submit the tool_result and get the final answer. |
| What are the four steps of the tool use flow? | 1) Initial request with tools, 2) Claude returns tool_use, 3) App executes locally, 4) App returns tool_result and Claude emits final response. |
| Why can't prompt engineering replace tools for real-time data? | The data was never in training — no amount of prompting can generate facts the model does not know. |
| Can tools have side effects? | Yes — tools can both read (e.g., weather API) and write (e.g., send email, create record), which is what turns Claude into an agent. |
