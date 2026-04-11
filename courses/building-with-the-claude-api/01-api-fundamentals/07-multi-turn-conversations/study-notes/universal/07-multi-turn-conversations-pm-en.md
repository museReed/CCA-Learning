# Multi-Turn Conversations — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Architecture (22%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 1.2 (agentic loop foundation), 1.1 (conversation state management), 5.3 (production patterns) |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 07 |

---

## One-Liner

Claude has no memory between calls — your product must supply the conversation history on every turn — which makes "what does the user feel is remembered" a product decision you can't delegate to engineering.

---

## Mental Model: The Goldfish Consultant

Imagine hiring a brilliant consultant who is also a goldfish: every time you walk into the room, they have no memory of the last meeting. To have a continuous conversation you must hand them a printed transcript of every prior meeting at the start of every new one.

| Goldfish consultant | Claude API |
|---------------------|-----------|
| Forgets between meetings | Stateless between API calls |
| Reads transcript to catch up | Reads the `messages` list on every call |
| Transcript grows each meeting | `messages` list grows each turn |
| Thick transcripts take longer to read | Longer histories cost more input tokens |

The PM job is deciding: what goes into that transcript, how long it stays, and how much you're willing to pay for each meeting.

---

## Why PMs Should Care About Statelessness

This one technical detail has outsized product implications:

| Product concern | Impact of statelessness |
|-----------------|------------------------|
| Chat feel | Memory must be designed; it doesn't happen for free |
| Cost curve | Long chats get expensive quickly (linear token growth) |
| Privacy | You decide what to keep and what to drop from history |
| Session timeouts | You choose when a conversation "ends" (not the API) |
| Multi-device continuity | History must live somewhere durable, not just in-memory |
| Per-user isolation | You must never mix one user's history into another's |

Every one of these is a product decision. Engineering can implement any of them, but they need PM direction on *which* behavior the product should have.

---

## Product Use Cases

### When You Need Multi-Turn

| Feature | Why multi-turn is required |
|---------|---------------------------|
| Customer support chat | Users refer back to earlier parts of the same conversation |
| Tutoring / coaching agent | Learning progress depends on context from previous turns |
| Long-running writing assistant | Drafts are iterated across multiple prompts |
| Research agent | Findings from one step inform the next |

### When Single-Turn Is Fine

| Feature | Why single-turn works |
|---------|----------------------|
| "Summarize this email" button | Each click is independent |
| Document classifier | No conversation needed |
| Translation | Stateless transformation |
| Autocomplete suggestion | Fire-and-forget |

PM rule of thumb: if the user would expect the AI to "remember earlier," you're in multi-turn territory and you must design for it explicitly.

---

## The Cost Curve: A Graph PMs Must Understand

Because history is replayed on every turn, input tokens grow linearly:

```
   Input tokens
        │
20,000  │                                    ●
        │                               ●
        │                          ●
10,000  │                     ●
        │                ●
        │           ●
 5,000  │      ●
        │  ●
        └──────────────────────────────────────── Turns
          1    5    10   20   30    40    50
```

This has three product consequences:

1. **Your unit economics change with chat length.** A 50-turn chat costs roughly 25x a 10-turn chat in input tokens.
2. **You will hit the context window.** Every model has a max history it can read; long chats need a strategy (summarize, truncate, or prompt-cache) before that wall.
3. **Cost forecasting is hard without a distribution of chat length.** You need real data from instrumentation, not a gut estimate.

---

## PM Decision Framework: Memory Strategy

Before launch, pick a memory strategy per feature:

| Strategy | How it works | When to use |
|----------|-------------|-------------|
| **Full history** | Keep every turn forever in the messages list | Short chats (< 20 turns) where context matters |
| **Sliding window** | Keep only the last N turns | Long chats where recent context is enough |
| **Summarization** | Compress older turns into a rolling summary | Long chats where early context still matters |
| **Session reset** | Explicitly end and clear on idle or action | Task-based chats with clear completion |
| **Prompt caching** | Pay once for unchanged prefixes | Long, stable system prompts with changing tails |

The PRD should specify which strategy applies and what the user-visible behavior looks like. "How many turns will the user remember?" is a PM-answerable question, not an engineering detail.

---

## Common PM Mistakes

1. **Assuming Claude remembers by default** — it doesn't; if you skip this lesson, your first chat feature will feel "dumb" to users.
2. **Not capping chat length or budget** — a power user with a 200-turn conversation can cost you real money; set limits.
3. **Mixing sessions across users** — a backend bug where two users share a `messages` list is a privacy incident; PM acceptance criteria must require isolation.
4. **Forgetting about reset flows** — users need a "new chat" button; without it, cost climbs and context becomes stale.
5. **Not instrumenting chat length distributions** — you can't plan budgets or eval prompts without knowing how long real chats actually run.

> **Key Insight**
>
> Statelessness is a product decision in disguise. The API gives you a blank slate; your product defines what "memory" means. Chat products that feel magical do this deliberately — they decide which turns matter, how long sessions last, how cost scales, and what the user sees when a chat is "reset." Products that ignore this ship chats that feel slow, expensive, and forgetful, and then blame the model. Own the memory strategy in your PRD and you'll ship features that feel smart and predictable.

---

## CCA Exam Relevance

- **D1 (Agentic Architecture)**: multi-turn IS the foundation of the agent loop. Scenario: "How does Claude remember earlier messages?" → the client resends them every turn.
- **D5 (Enterprise Deployment)**: cost and scale implications of linear token growth.
- Scenario trigger: "Users report the chatbot forgets" → check whether the app is appending assistant replies and sending full history, not a prompt tweak.

---

## Flashcards

| Front | Back |
|-------|------|
| Does Claude remember prior exchanges in the same chat automatically? | No — the API is stateless; your app must replay history on every turn |
| What is the "goldfish consultant" analogy? | Claude forgets between calls, so you hand it a fresh transcript of every prior meeting at the start of each new one |
| Why do long chats cost disproportionately more? | Input tokens grow linearly as history is replayed; a 50-turn chat has ~25x the input tokens of a 10-turn chat |
| What memory strategies can PMs choose from? | Full history, sliding window, summarization, session reset, prompt caching |
| What product concern does statelessness raise for multi-user apps? | Per-user isolation — one user's history must never leak into another's |
| When is single-turn sufficient? | When each interaction is independent (summary, translation, classification) and users don't expect "memory" |
| What's the first thing to check when a chatbot "forgets"? | Whether the app is appending assistant replies and sending full history on each call |
| What should the PRD specify about memory? | Which memory strategy applies, the turn/cost cap, and how "new chat" / session reset works |
