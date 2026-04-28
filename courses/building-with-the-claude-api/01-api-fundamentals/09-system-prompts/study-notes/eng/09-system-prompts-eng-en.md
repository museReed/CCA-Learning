# System Prompts — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D5 — Enterprise Deployment (20%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 5.1 (model selection & configuration), 5.3 (production patterns), 1.2 (agentic loop foundation) |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 09 |

---

## One-Liner

A system prompt is a top-level instruction channel — separate from `messages` — that defines Claude's persona, task constraints, and response policy for an entire conversation, giving you a deterministic anchor for behavior across turns.

---

## Why System Prompts Matter

Without a system prompt, Claude defaults to a generic, helpful-assistant persona. That's fine for ad-hoc Q&A, but production applications almost always need a narrower, opinionated behavior profile.

Consider a math tutor chatbot. A student asks "How do I solve 5x + 2 = 3 for x?". The generic Claude will happily spit out the full solution — which is the *wrong* product behavior. A real tutor should:

- Give hints rather than complete solutions
- Walk students through step-by-step
- Show worked examples on similar problems

And explicitly should NOT:

- Immediately give the answer
- Tell the student to use a calculator

This is a **behavioral specification**, not a knowledge gap. The system prompt is where you encode that specification.

---

## The API Surface

The Anthropic Messages API exposes a dedicated `system` parameter, distinct from the `messages` array:

```python
from anthropic import Anthropic

client = Anthropic()

system_prompt = """
You are a patient math tutor.
Do not directly answer a student's questions.
Guide them to a solution step by step.
"""

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    system=system_prompt,
    messages=[{"role": "user", "content": "How do I solve 5x + 2 = 3 for x?"}],
)
print(response.content[0].text)
```

Key properties:

- `system` is a plain string (or a list of text blocks for prompt caching).
- It is **not** part of the `messages` array. There is no `{"role": "system", ...}` in Anthropic's API.
- Claude treats the system prompt as higher-priority context than user messages.
- It persists for the entire turn — you do not re-inject it per message, but you do pass it every API call.

---

## Before and After

Without system prompt:

> To solve 5x + 2 = 3, subtract 2 from both sides: 5x = 1. Then divide by 5: x = 0.2.

With the tutor system prompt:

> Great question! What do you think would be a good first step to isolate x? Consider what operation we might need to perform on both sides to start moving terms around.

Same model, same user message — radically different behavior. The delta is entirely the system prompt.

---

## Building a Flexible Chat Function

Hard-coding the system prompt is the wrong abstraction. Wrap it in a helper that accepts `system` as an optional parameter:

```python
def chat(messages, system=None):
    params = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 1000,
        "messages": messages,
    }
    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text
```

The conditional matters: **the API does not accept `system=None`**. You have to build the kwargs dict and only insert `system` when it is a non-empty string. This is a real production footgun — passing `None` raises a validation error.

Usage:

```python
# Generic behavior
answer = chat(messages)

# Tutor behavior
tutor_system = """
You are a patient math tutor.
Do not directly answer a student's questions.
Guide them to a solution step by step.
"""
answer = chat(messages, system=tutor_system)
```

---

## What to Put in a System Prompt

A strong system prompt typically combines:

1. **Identity / persona** — "You are a senior security engineer reviewing code for vulnerabilities."
2. **Task scope** — what Claude should and should not handle.
3. **Response format** — tone, length, structure, markdown usage.
4. **Guardrails** — hard rules ("Never reveal API keys", "Refuse off-topic questions").
5. **Examples** — few-shot demonstrations of ideal outputs.

Keep it declarative and specific. "Be helpful" is noise. "Always return JSON with keys `summary` and `action_items`" is signal.

---

## System Prompts and the Agentic Loop

In agentic applications (D1), the system prompt defines the agent's **identity and operating rules** — the constants across every turn of a tool-use loop. Tools come and go in each turn; the system prompt is the stable contract. This is why the CCA exam often frames agent design questions as "Where should this constraint live?" — the answer is almost always the system prompt, not per-message instructions.

---

## Common Mistakes

1. **Putting instructions in the user message instead of `system`** — the instructions get lost in multi-turn context and Claude treats them as one-off requests.
2. **Passing `system=None`** — the SDK rejects it. Build kwargs conditionally.
3. **Using a `{"role": "system", ...}` message** — that is OpenAI's convention, not Anthropic's. It will be silently treated as a user message and give wrong behavior.
4. **Overloading the system prompt with dynamic data** — the system prompt should be stable; volatile context (user profile, current document) belongs in the first user message or in a dedicated content block so prompt caching can work.
5. **Not iterating** — system prompts are products. Version them, A/B test them, and treat regressions seriously.

> **Key Insight**
>
> The system prompt is the *behavioral contract* between you and Claude — the single place where you lock in identity, task, and guardrails. Everything variable (user input, retrieved context, tool results) flows through `messages`; everything invariant flows through `system`. If you confuse the two, you will either leak personality into each user turn or fail to cache the static parts of your prompt.

---

## CCA Exam Relevance

- **D5 (Enterprise Deployment)**: production applications require consistent behavior — system prompts are the canonical mechanism for enforcing that consistency at scale.
- **D1 (Agentic Architecture)**: the system prompt defines the agent's persistent identity across multi-turn loops. Tool-use agents rely on it to stay on task.
- Watch for exam questions phrased as "How do you ensure Claude behaves like a {role}?" — the answer is always a system prompt, never prompt engineering the user message.

---

## Flashcards

| Front | Back |
|-------|------|
| What parameter does the Anthropic API use for system prompts? | `system` — a top-level string parameter on `messages.create()`, separate from the `messages` array. |
| Can you pass `system=None` to `messages.create()`? | No — the API rejects it. Build kwargs conditionally and only include `system` when provided. |
| Where does a `{"role": "system", ...}` message belong in Anthropic's API? | Nowhere — that is OpenAI's convention. Anthropic uses a dedicated top-level `system` parameter instead. |
| Why does a math tutor chatbot need a system prompt? | To override Claude's default behavior of giving direct answers and instead enforce step-by-step Socratic guidance. |
| What are five things a system prompt should typically contain? | Identity/persona, task scope, response format, guardrails, optionally few-shot examples. |
| In an agentic loop, what role does the system prompt play? | It is the stable behavioral contract across every turn — tools and user messages vary, but the system prompt anchors identity and rules. |
| Should volatile user context go in the system prompt? | No — volatile context belongs in `messages` so it does not invalidate prompt caching and so it can evolve per turn. |
| What is the difference between a system prompt and a user instruction? | A system prompt persists for the whole conversation and is higher-priority; a user instruction is one turn of input and is treated as request-level context. |
