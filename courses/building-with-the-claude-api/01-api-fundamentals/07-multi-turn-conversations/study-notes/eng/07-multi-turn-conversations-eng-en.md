# Multi-Turn Conversations — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Architecture (22%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 1.2 (agentic loop foundation), 1.1 (conversation state management), 5.3 (production patterns for statefulness) |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 07 |

---

## One-Liner

The Anthropic API is **stateless** — Claude has no memory between calls — so the client is fully responsible for maintaining conversation history and replaying it with every request, which is the mechanical foundation of every agent and chat feature you will ever build.

---

## The Core Principle: Statelessness

Claude the model does not store your conversation. Each `messages.create()` call is a fresh request with no memory of prior exchanges. If you call:

```python
client.messages.create(model=model, max_tokens=1000, messages=[
    {"role": "user", "content": "What is quantum computing?"}
])
# → great answer

client.messages.create(model=model, max_tokens=1000, messages=[
    {"role": "user", "content": "Write another sentence"}
])
# → Claude has NO IDEA what "another sentence" refers to; generates something random
```

The second call has zero context. Claude will write a sentence about something completely unrelated because it never saw the first exchange. This is not a bug — it's the fundamental design.

| Property | Anthropic API |
|----------|---------------|
| Server-side memory of your conversations | None |
| Conversation IDs | None (at the API layer) |
| Who owns the history | Your application |
| How is history replayed | Your code sends the full `messages` list each call |

---

## The Fix: Client-Side History

To get multi-turn conversations, you must:

1. **Maintain a list of all messages in your application code.**
2. **Send the complete message history with every request.**

The flow:

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  Turn 1:                                        │
│   messages = [user: "Define quantum computing"] │
│   response = create(messages)                   │
│   messages.append(assistant: response.text)     │
│                                                 │
│  Turn 2:                                        │
│   messages.append(user: "Write another          │
│                         sentence")              │
│   response = create(messages)   ← sends ALL     │
│   messages.append(assistant: response.text)     │
│                                                 │
│  Turn N:                                        │
│   messages grows unboundedly; the whole list    │
│   is replayed on every call.                    │
│                                                 │
└─────────────────────────────────────────────────┘
```

Every turn appends two entries: the previous assistant response and the new user question.

---

## Helper Functions: The Minimal Chat Skeleton

The lesson recommends three one-line helpers:

```python
def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
    )
    return message.content[0].text
```

These three functions are the cleanest way to keep call sites readable and the history mutation rules consistent.

---

## Putting It Together

```python
from dotenv import load_dotenv
load_dotenv()

from anthropic import Anthropic

client = Anthropic()
model = "claude-sonnet-4-5"

def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
    )
    return message.content[0].text

# Start with an empty message list
messages = []

# Turn 1
add_user_message(messages, "Define quantum computing in one sentence")
answer = chat(messages)
add_assistant_message(messages, answer)

# Turn 2 — Claude now has the full context of turn 1
add_user_message(messages, "Write another sentence")
final_answer = chat(messages)
add_assistant_message(messages, final_answer)

print(final_answer)
```

Now "Write another sentence" works as expected — Claude sees the entire conversation and understands the anaphoric reference to quantum computing.

---

## The Hidden Cost: Linear Token Growth

Because the full history is replayed every turn, **input tokens grow linearly with conversation length**. On turn N, you pay to send turns 1 through N-1 all over again.

| Turn | Input tokens (approx) | Cumulative input cost |
|------|----------------------|----------------------|
| 1 | 50 | 50 |
| 2 | 150 | 200 |
| 3 | 300 | 500 |
| 10 | 2,000 | ~10,000 |
| 50 | 20,000 | ~500,000 |

Two practical consequences:

1. **Input tokens dominate the bill for long chats.** Output may stay steady at a few hundred tokens per turn; input balloons.
2. **You will eventually hit the context window.** Every model has a max context length; long conversations must be truncated or summarized before that wall.

Mitigation strategies (beyond the scope of Lesson 07 but worth knowing):

- **Sliding window** — keep only the last N turns.
- **Summarization** — compress older turns into a rolling summary.
- **Prompt caching** — Anthropic's caching feature lets you reuse unchanged prefixes cheaply (covered later in the course).

---

## Why This Matters for Agents

Lesson 07 teaches single-responsibility multi-turn chat, but the exact same pattern is the foundation of every agent:

```python
# Agent loop — just multi-turn chat with branching on stop_reason
while True:
    response = client.messages.create(model=model, max_tokens=1024, messages=messages, tools=tools)
    messages.append({"role": "assistant", "content": response.content})

    if response.stop_reason == "end_turn":
        break

    if response.stop_reason == "tool_use":
        tool_result = execute_tool(response)
        messages.append({"role": "user", "content": [tool_result]})
        continue
```

The structural similarity is the whole point: **multi-turn chat + a branch on stop_reason = an agent**. If you understand Lesson 07, you understand the skeleton of every agent in D1.

---

## Common Mistakes

1. **Forgetting to append the assistant response** — the next turn arrives without context and Claude appears to have amnesia.
2. **Appending only user messages** — the API rejects two consecutive user turns; you must interleave.
3. **Treating the API as stateful** — there are no server-side conversation IDs; all state is on your side.
4. **Ignoring token growth** — conversations that work fine in testing blow up on long sessions in production.
5. **Mutating `messages` in parallel** — multi-user chat servers must keep each conversation isolated; sharing a single list across users corrupts history.

> **Key Insight**
>
> The API's statelessness is not a limitation — it's a **deliberate design** that puts you in full control of memory. You decide what to keep, what to drop, what to summarize, and how to isolate per-user state. Every fancy feature (agents, tool use, streaming, caching) sits on top of "maintain a list, replay it every turn." Master this lesson and you have the mental model for every higher-level pattern in the CCA curriculum.

---

## CCA Exam Relevance

- **D1 (Agentic Architecture)**: the multi-turn loop IS the agent loop. Expect questions framing "how does Claude remember context?" — the answer is always "the client replays history; the API is stateless."
- **D5 (Enterprise Deployment)**: implications for cost (linear token growth) and scale (per-user isolation).
- Scenario trigger: "Claude forgot what we were talking about" → the app failed to append the prior exchange; the fix is on the client, not in a prompt tweak.

---

## Flashcards

| Front | Back |
|-------|------|
| Does Claude store conversation history between API calls? | No — the API is fully stateless; your application owns history |
| What two actions must you perform on every turn to keep context? | Append the previous assistant reply and the new user message to the `messages` list, then send the whole list |
| Why does input token usage grow linearly with conversation length? | The full history is replayed on every request, so each call includes all prior turns as input |
| What are the three helper functions Lesson 07 recommends? | `add_user_message`, `add_assistant_message`, `chat` |
| What happens if you only append user messages (no assistant)? | The API rejects consecutive user turns; the conversation must alternate |
| How does multi-turn chat relate to an agent loop? | An agent is multi-turn chat plus branching on `stop_reason` (tool_use vs end_turn) |
| What mitigations exist for the linear token growth problem? | Sliding windows, summarization of older turns, and prompt caching |
| Where does conversation state live in a production chat app? | In the server-side session for the specific user — never shared across users |
