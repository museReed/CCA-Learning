# Tool Choice Parameter — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.1 (tool schema design), 2.2 (content blocks), 1.2 (agentic loop control) |
| Source | Supplementary — fills curriculum gap in building-with-the-claude-api / 04-tool-use |

---

## One-Liner

`tool_choice` is the steering wheel for Claude's tool-calling behavior — it lets you declare whether Claude *may*, *must*, or *must not* call a tool on this turn, and optionally which specific tool.

---

## The Four Modes

| Mode | Syntax | Behavior | `stop_reason` |
|------|--------|----------|---------------|
| `auto` | `{"type": "auto"}` | **Default.** Claude decides whether to call a tool. Response can be a TextBlock (chat) or a ToolUseBlock. | `end_turn` OR `tool_use` |
| `any` | `{"type": "any"}` | Claude MUST call one of the provided tools. It picks which. Response is always a ToolUseBlock. | `tool_use` |
| `tool` | `{"type": "tool", "name": "get_weather"}` | Force Claude to call a SPECIFIC named tool. | `tool_use` |
| `none` | `{"type": "none"}` | Tools disabled for this turn; Claude replies with text only. | `end_turn` |

### `auto` — Claude Decides

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "auto"},  # same as omitting tool_choice
    messages=messages,
)
```

Best for general-purpose agents and chat interfaces. Claude produces natural chain-of-thought text before a tool call when it decides one is needed, giving you reasoning transparency.

### `any` — Claude Must Call Some Tool

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "any"},
    messages=messages,
)
# response.content[0].type == "tool_use" — guaranteed
```

Best for workflows where every turn must yield a structured action. Claude still picks which tool based on the message, but cannot escape into free text.

### `tool` — Force a Specific Tool

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "tool", "name": "extract_invoice"},
    messages=messages,
)
```

Best for structured data extraction — the tool's `input_schema` acts as a typed output contract. This is the idiomatic "JSON mode" equivalent in the Claude API.

### `none` — Tools Disabled This Turn

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,  # still declared
    tool_choice={"type": "none"},
    messages=messages,
)
```

Useful inside an agent loop when you want Claude to summarize, reflect, or "think out loud" without triggering more tool calls — for example, producing the final user-facing message after all tool results have been gathered.

---

## Interaction with `stop_reason`

The tool_choice mode directly constrains which `stop_reason` values you must handle:

| Mode | Possible `stop_reason` | Branches you must code |
|------|------------------------|------------------------|
| `auto` | `end_turn`, `tool_use`, `max_tokens`, `stop_sequence` | Two main branches: text reply vs tool call |
| `any` | `tool_use` (plus `max_tokens` edge case) | Single branch: always execute a tool |
| `tool` | `tool_use` (plus `max_tokens` edge case) | Single branch: always execute the forced tool |
| `none` | `end_turn`, `max_tokens`, `stop_sequence` | Single branch: text reply only |

This matters for loop control. When using `auto`, your agent loop exits on `end_turn`. When using `any`, the loop can only be broken by switching `tool_choice` to `auto` or `none`, or by the tool results reaching a terminal state your code recognizes.

---

## `disable_parallel_tool_use`

```python
tool_choice={"type": "any", "disable_parallel_tool_use": True}
```

By default, Claude may emit multiple `tool_use` blocks in a single response (parallel tool use). Setting `disable_parallel_tool_use: true` forces **at most one** `tool_use` block per turn.

- Pairs naturally with `any` or `tool` when you need strict single-action enforcement (e.g., state machines, transactional workflows).
- Also valid with `auto` when your executor cannot safely run tools in parallel.
- Trade-off: you lose the latency benefit of parallel calls.

---

## When to Use Each Mode — Decision Guide

```
Need live data sometimes, chat other times?         → auto
Every turn MUST produce a structured action?         → any
Extracting typed data from unstructured input?       → tool (specific)
Summary / reflection turn inside an agent loop?      → none
Strict one-action-at-a-time state machine?           → any + disable_parallel_tool_use
```

---

## Common Mistakes

1. **Using `any` for a chat agent** — forces a tool call on every turn, including "hello" and "thanks", which produces nonsensical tool_use blocks.
2. **Expecting chain-of-thought with `tool` or `any`** — when Claude is forced, it does not emit reasoning text before the tool_use block. You lose transparency. Only `auto` permits natural CoT.
3. **Forgetting that `none` still requires `tools=` to be declared** — the tools list stays; `none` only disables calling them on this specific turn.
4. **Assuming `auto` always calls a tool when one is available** — `auto` means Claude may *choose not to*. If your use case requires a tool call, use `any` or `tool`.
5. **Not setting `disable_parallel_tool_use` when your executor is not parallel-safe** — Claude may emit two tool_use blocks simultaneously and your serial executor will either deadlock or double-apply state.

---

> **Key Insight**
>
> `tool_choice` is how you convert Claude from a conversational assistant into a deterministic component. `auto` keeps Claude in the driver's seat (flexible, transparent reasoning). `any`/`tool` put your code in the driver's seat (structured, guaranteed action, but opaque reasoning). Choosing the right mode is a trade-off between flexibility and control — and this trade-off is at the heart of CCA D1 (agent design) and D2 (tool design).

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: knowing all four modes, their syntax, and when each is appropriate is directly testable. Expect questions framed as "Which `tool_choice` setting guarantees Claude will call a tool?".
- **D1 (Agentic Architecture)**: `tool_choice` controls loop termination and structure. Using `none` for summary turns and `any` for action turns is a core agent pattern.
- **Trap to watch for**: exam questions may describe a "JSON extraction" use case — the correct answer is `{"type": "tool", "name": "..."}`, not `any` and not a prompt trick.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the default value of `tool_choice`? | `{"type": "auto"}` — Claude decides whether to call a tool. |
| Which `tool_choice` mode guarantees Claude calls some tool? | `{"type": "any"}` — Claude must pick one of the provided tools. |
| How do you force Claude to call a specific named tool? | `{"type": "tool", "name": "<tool_name>"}` |
| What does `{"type": "none"}` do? | Disables tool calling for this turn; Claude replies with text only and `stop_reason` is `end_turn`. |
| Which mode preserves Claude's chain-of-thought reasoning before a tool call? | Only `auto`. `any` and `tool` suppress reasoning text and emit the tool_use block directly. |
| Which `stop_reason` values are possible under `tool_choice: auto`? | `end_turn` (text reply) or `tool_use` (tool call). |
| What does `disable_parallel_tool_use: true` enforce? | At most one `tool_use` block per turn, even when Claude could call multiple tools in parallel. |
| When would you use `tool_choice: none` inside an agent loop? | On a summary/reflection turn after all tool results have been collected, to force a final text answer. |
| Why is `any` a bad choice for a general chat agent? | It forces a tool call on every turn, including small talk, producing nonsensical tool_use blocks. |
| Which `tool_choice` mode is the idiomatic "JSON mode" equivalent in the Claude API? | `{"type": "tool", "name": "..."}` — the tool's `input_schema` acts as the typed output contract. |
