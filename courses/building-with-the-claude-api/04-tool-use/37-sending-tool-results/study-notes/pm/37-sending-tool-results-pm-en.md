# Sending Tool Results — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) / D1 — Agentic Architecture (22%) |
| Task Statements | 2.4 (tool_result block format), 2.2 (content block handling), 1.2 (closing the tool-use loop) |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 37 |

---

## One-Liner

Sending tool results back to Claude is the "return receipt" step — a strictly-formatted packet that closes the loop between "Claude asked for something" and "Claude has the information to answer the user."

---

## Mental Model: The Order Ticket System

Think of a busy restaurant kitchen:

| Kitchen Step | Claude Tool-Use Step |
|--------------|---------------------|
| Waiter writes ticket #47: "burger, medium" | Claude emits `ToolUseBlock(id="toolu_47", name="cook", input={"item":"burger"})` |
| Cook prepares burger | Your code runs the function |
| Cook attaches ticket #47 to the plate | You return a `tool_result` block with `tool_use_id="toolu_47"` |
| Plate goes back to ticket #47's table | Claude uses the result to answer the user |

The ticket number (`tool_use_id`) is sacred. If the cook forgets to attach it, nobody knows which table gets the burger. If the cook returns two burgers for one ticket, or one burger for two tickets, the whole service breaks down. That is exactly how the Anthropic API treats tool results.

---

## Why PMs Should Care

Tool results are the failure surface where most tool-use features break in production:

| Failure Mode | User-Visible Symptom |
|--------------|---------------------|
| Backend crashes mid-tool and drops the result | Claude hangs or replies with "I'm sorry, I can't help with that" |
| Backend forgets to mark errors as `is_error: True` | Claude hallucinates success and gives a confident wrong answer |
| Multiple tool calls, backend only returns one result | 400 error shown to user, conversation unrecoverable |
| Backend returns raw dict instead of JSON string | Conversation breaks with cryptic validation error |

Every one of these is a product quality issue. A PM who understands the tool-result contract can write better acceptance criteria and catch these in staging instead of on launch day.

---

## Product Use Cases: Error Visibility

Tool failures are not just engineering concerns — they are UX decisions:

| Strategy | When to Use | UX Impact |
|----------|-------------|-----------|
| Pass error to Claude via `is_error: True` | Most cases | Claude explains the problem naturally ("I couldn't fetch the stock price because the API is down. Would you like to try again?") |
| Catch error before Claude sees it | Rate limits, security errors | Show a custom UI toast; bypass Claude entirely |
| Retry silently with exponential backoff | Transient network errors | User never sees a blip, but increases latency |

The default pattern — `is_error: True` — gives Claude the information to recover gracefully. Skipping this lets Claude hallucinate success, which is the worst possible user experience.

---

## PM Decision Framework

For any feature that uses tools, your PRD should answer:

| Question | Why It Matters |
|----------|---------------|
| What is the timeout budget for each tool? | Long tools produce dead UX; you need progress events |
| How do we communicate tool errors to the user? | Via Claude (`is_error: True`) or via our own UI? |
| What happens if Claude calls the same tool twice? | Caching? Idempotency? Permission escalation? |
| Can Claude see sensitive error details? | Stripping before sending avoids leaking internal stack traces |
| How do we log tool_use_id pairs for observability? | Essential for debugging production conversations |

---

## Common PM Mistakes

1. **Not specifying error handling in the PRD** — engineers default to "log and drop," which silently breaks conversations
2. **Assuming tool results are "just function returns"** — they have a strict format (role=user, content blocks with specific fields) that constrains engineering
3. **Ignoring the multi-tool case** — "what if Claude calls two tools at once" is a real design question, not an edge case
4. **Not budgeting for observability** — tool_use_id tracing is crucial for diagnosing production issues, but rarely in initial scope
5. **Treating `is_error` as an engineering detail** — it is a product decision: do you want Claude to explain failures, or hide them behind a custom UI?

---

> **Key Insight**
>
> Every `tool_result` is a return receipt keyed by `tool_use_id`. The PM lesson: tool failures are product features in disguise. The choice between "Claude sees the error and explains it" (use `is_error: True`) versus "we bypass Claude and show a custom error" is a UX decision with direct impact on user trust and recovery rates. Ship neither by accident — design it deliberately.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: Know the `tool_result` block fields and that it lives in a user-role message.
- **D1 (Agentic Architecture)**: Understand tool_result as the closing half of the agentic request/response pair.
- Exam questions often describe scenarios where a tool fails and ask how to inform Claude — the answer is almost always "send a `tool_result` block with `is_error: True`."

---

## Flashcards

| Front | Back |
|-------|------|
| What analogy captures the `tool_use_id` / `tool_result` pairing? | Restaurant order tickets — each ticket number must round-trip from waiter to cook to table |
| Why is `is_error: True` a PM concern, not just an engineering flag? | It decides whether Claude explains failures to users or the UI hides them — a UX decision with real user-trust impact |
| What is the worst failure mode of tool results? | Silent success — forgetting `is_error: True`, causing Claude to hallucinate a successful result |
| What must the PRD specify for any tool-using feature? | Timeout budgets, error-handling strategy, multi-tool behavior, observability for tool_use_ids |
| Why does sending a raw dict as `content` break? | The API requires the `content` field to be a string (or list of blocks); dicts must be JSON-serialized |
| When Claude calls two tools at once, how many results should you return? | Exactly two — every `ToolUseBlock` needs a matching `tool_result` in the same user turn |
| Where in the message structure does a `tool_result` block live? | Inside a user-role message's `content` array |
| What happens in production if the backend drops a tool result? | The next API call returns 400; the conversation becomes unrecoverable and the user sees an error |
