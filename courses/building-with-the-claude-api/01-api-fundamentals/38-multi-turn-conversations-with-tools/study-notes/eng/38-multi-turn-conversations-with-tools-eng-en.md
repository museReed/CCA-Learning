# Multi-Turn Conversations with Tools — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) / D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 1.3 (multi-turn conversation management), 1.2 (agentic loop implementation), 2.4 (multi-turn tool loops) |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 38 |

---

## One-Liner

Multi-turn tool conversations emerge whenever Claude needs to chain multiple tool calls to answer a single user question, and the only way to support this is a **loop** that keeps round-tripping the API until Claude stops asking for tools.

---

## Why Multi-Turn Is Necessary

Some questions cannot be answered in one tool call. "What day is 103 days from today?" decomposes into:

1. `get_current_datetime()` → today's date
2. `add_duration_to_datetime(date, +103 days)` → target date

Claude cannot pre-bake both calls because the second depends on the first's output. Each call becomes a separate turn, and the server (your code) is responsible for driving the loop.

```
User question
  ↓
Claude → tool_use: get_current_datetime
  ↓
Server executes tool → tool_result
  ↓
Claude → tool_use: add_duration_to_datetime(date=..., days=103)
  ↓
Server executes tool → tool_result
  ↓
Claude → final text answer (stop_reason="end_turn")
```

---

## The Conversation Loop Skeleton

The canonical pattern is a `while True` loop that breaks when Claude stops requesting tools:

```python
def run_conversation(messages):
    while True:
        response = chat(messages)
        add_assistant_message(messages, response)

        # Pseudo-code until we see the real stop_reason check in Lesson 39
        if not response_is_asking_for_a_tool(response):
            break

        tool_result_blocks = run_tools(response)
        add_user_message(messages, tool_result_blocks)

    return messages
```

Three key points:

1. **`add_assistant_message` preserves the full block list** (text + tool-use blocks)
2. **`run_tools` executes every tool-use block** and returns all results together
3. **`add_user_message` with tool results** feeds the results back as a single user-role message

---

## Refactoring Helper Functions for Multi-Block Content

The lesson emphasizes that before implementing the loop, your helpers must be upgraded to accept `Message` objects, not just strings.

### `add_user_message` — accept strings, block lists, or Messages

```python
from anthropic.types import Message

def add_user_message(messages, message):
    content = message.content if isinstance(message, Message) else message
    messages.append({"role": "user", "content": content})
```

This polymorphism lets you call it with:
- a plain string (`"What time is it?"`)
- a list of content blocks (tool result blocks)
- a full `Message` object returned from the API

### `add_assistant_message` — same polymorphism

```python
def add_assistant_message(messages, message):
    content = message.content if isinstance(message, Message) else message
    messages.append({"role": "assistant", "content": content})
```

### `chat` — accept tools, return the full Message object

```python
def chat(messages, system=None, temperature=1.0, stop_sequences=[], tools=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }
    if tools:
        params["tools"] = tools
    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message
```

Returning the whole `Message` (not just `.content[0].text`) is non-negotiable once tools are involved — you need the block list, `stop_reason`, and usage data.

### `text_from_message` — extract display text when you need it

```python
def text_from_message(message):
    return "\n".join(
        [block.text for block in message.content if block.type == "text"]
    )
```

Filtering on `block.type == "text"` is the idiomatic way to pull user-visible narration out of a mixed-block response.

---

## Conversation Accumulation Semantics

Every turn adds at least one message to the history:

| Turn | Added to `messages` |
|------|---------------------|
| 0 | User question |
| 1 | Assistant message with `text + tool_use_1` |
| 2 | User message with `tool_result_1` |
| 3 | Assistant message with `text + tool_use_2` |
| 4 | User message with `tool_result_2` |
| 5 | Assistant message with final text (`stop_reason=end_turn`) |

Note how assistant and user messages **alternate strictly** — tool results always come back as user messages, never as assistant messages. This preserves the alternation invariant the API enforces.

---

## Context Window Considerations

Each loop iteration grows `messages` by one (sometimes two) messages. For long tool chains, you can blow through the context window. Mitigation strategies:

1. **Cap the loop** with a `max_iterations` counter to guard against runaway agents
2. **Summarize intermediate tool results** if they contain verbose data that is no longer needed
3. **Use prompt caching** (covered later in the course) to amortize the cost of the growing history
4. **Use shorter tool responses** — tools that return concise JSON beat tools that return entire web pages

---

## Common Mistakes

1. **Appending only `.content[0].text` to history** — drops the tool-use block, breaking the next turn's `tool_use_id` pairing
2. **Forgetting to pass `tools=[...]` on every loop iteration** — Claude needs the schema every time, even when replying to tool results
3. **Using `add_user_message` with a string instead of blocks for tool results** — tool results must be a content-block list
4. **No loop cap** — a misbehaving tool or a confused Claude can produce infinite tool-use loops, burning tokens
5. **Breaking on text content heuristics** — "if response has text, stop" is wrong because Claude can emit text AND a tool_use in the same turn; always check `stop_reason`

---

> **Key Insight**
>
> Multi-turn conversations with tools are not a special case — they are the general case. Single-turn tool use is just "the loop terminated after one iteration." Writing your first tool-use feature as a proper loop (even for single-tool features) saves you a full rewrite when the product evolves to need tool chaining. The upfront investment in helper function polymorphism is what makes the loop trivial to implement.

---

## CCA Exam Relevance

- **D1 (Agentic Architecture)**: This is a core agentic loop pattern question. Expect prompts asking "what signals the loop to continue" or "how does Claude know to chain tool calls."
- **D2 (Tool Design & MCP Integration)**: Understand how the tool schema must be passed on every loop iteration.
- Exam tip: questions about "multi-turn tool conversations" almost always test the loop structure — know the `while` pattern cold.

---

## Flashcards

| Front | Back |
|-------|------|
| Why do some user questions require multi-turn tool conversations? | Because the second tool call depends on the output of the first (e.g., "103 days from today" needs current date first) |
| What control structure implements multi-turn tool conversations? | A `while` loop that keeps calling the API until Claude stops requesting tools |
| What must `add_assistant_message` accept, beyond plain strings? | Full `Message` objects — so it preserves the complete block list including tool-use blocks |
| Why must `chat` return the whole `Message` object, not just `text`? | Because you need `content` (block list), `stop_reason`, and usage data to drive the loop |
| What helper extracts user-visible text from a mixed-block message? | `text_from_message` — filters `block.type == "text"` and joins them |
| Why should you cap the loop with `max_iterations`? | To guard against runaway agents or misbehaving tools producing infinite loops |
| What is the alternation invariant in multi-turn tool conversations? | Assistant and user messages must strictly alternate; tool results always come back in a user message |
| What is wrong with "break when response has text"? | Claude can emit text AND a tool_use in the same turn — always check `stop_reason` instead |
