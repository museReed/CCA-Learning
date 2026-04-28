# Making a Request — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D5 — Enterprise Deployment (20%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 5.1 (model selection), 5.3 (production patterns), 1.2 (agentic loop foundation) |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 06 |

---

## One-Liner

A single Claude request is the smallest unit of product value in any AI feature — three parameters decide the feature's quality, cost, and failure modes, so PMs need to sign off on `model`, `max_tokens`, and `messages` just like they sign off on copy and UX.

---

## Mental Model: The Vending Machine Transaction

Think of `client.messages.create()` as a vending machine:

| Vending Machine | Claude Request |
|-----------------|---------------|
| Pick the machine (coffee vs soda) | Pick the `model` (Sonnet, Haiku, Opus) |
| Insert correct change | Provide API key |
| Press a button (which product) | Send `messages` (the prompt) |
| Machine dispenses up to one item | Claude responds up to `max_tokens` |
| Receipt with price | `response.usage` with input/output token counts |

Every feature in your product is a thousands-of-these-transactions system. Quality, cost, and latency are emergent properties of the three parameters you pick.

---

## The Three Parameters As Product Decisions

### Model

Choosing the model is a product decision disguised as a technical one. It trades off speed, capability, and cost.

| Model tier | Good for | PM considerations |
|------------|----------|-------------------|
| Sonnet (balanced) | Default for most features | Good baseline; start here |
| Haiku (fast, cheap) | Summaries, classification, high-volume | Cheaper per call, might miss nuance on hard prompts |
| Opus (most capable) | Reasoning-heavy features, complex drafting | Higher cost per call; reserve for high-value flows |

Note: model names in the course are examples; always confirm the current generation (e.g. `claude-sonnet-4-5`) with engineering.

### `max_tokens`

This is your per-call cost ceiling. PMs who don't have an opinion on `max_tokens` are letting engineering silently decide feature quality.

| Feature type | Suggested max_tokens | Reasoning |
|--------------|---------------------|-----------|
| Chat reply | 500–1000 | Short responses; room for nuance |
| Summary of a document | 1000–2000 | Summaries are bounded but need breathing room |
| Long-form draft (email, blog) | 2000–4000 | Worth paying for unless feature needs to be fast |
| Classification / routing | 50–100 | Single token answers; wasted tokens = wasted money |

**Critical clarification**: `max_tokens` is a ceiling, not a target. If you want longer outputs, you need to ask for them in the prompt itself, not bump the ceiling.

### `messages`

The messages list is your "conversation state." For single-turn features (Q&A, summarize), it has one entry. For multi-turn features (chat, agent), it grows. Lesson 07 covers the multi-turn case in detail.

---

## Product Use Cases

### When a Single Request Is Enough

| Feature | Why single-turn works |
|---------|----------------------|
| "Summarize this document" | One question, one answer |
| "Translate this text" | Stateless transformation |
| "Classify this ticket" | Routing decision, no follow-up |
| "Rewrite this email in a friendlier tone" | Fire-and-forget transformation |

### When You Need More Than One Call

| Feature | Why single-turn is not enough |
|---------|-------------------------------|
| Chat with history | Needs `messages` growing over time (Lesson 07) |
| Tool-using agent | Needs a loop that branches on `stop_reason` (Lesson 32+) |
| Streaming output | Same call with `stream=True` flag |

---

## PM Decision Framework: The Pre-Launch Questionnaire

Before shipping any feature that calls Claude, answer these in the PRD:

| Question | Default |
|----------|---------|
| Which model are we calling? | Start with Sonnet unless there's a reason |
| What is `max_tokens` set to? | The max length of a valid response × 1.5 |
| Is this single-turn or multi-turn? | Single-turn unless user needs follow-ups |
| How much does a typical call cost? | Compute: (avg input + output tokens) × pricing |
| What do we show during the call? | Loading state, streaming, or optimistic UI |
| What if `stop_reason == "max_tokens"`? | Define truncation UX |
| How do we test prompt quality? | Eval harness or human review loop |

---

## Cost Economics in Plain English

Every call has two cost components:

- **Input tokens** — the length of everything you send (system prompt + messages)
- **Output tokens** — the length of Claude's response

You pay per-million tokens per direction. The PM implications:

| Lever | Effect on cost |
|-------|---------------|
| Shorter prompts | Linearly cheaper inputs |
| Tighter `max_tokens` | Caps worst-case output cost |
| Smaller model | Significantly cheaper but may reduce quality |
| Batching multiple questions into one call | Saves per-call overhead but couples failures |
| Using tool use vs huge context windows | Fewer input tokens per call (Lesson 32+) |

Rule of thumb: for most features, input tokens dominate the bill because you keep resending context. Lesson 07 (multi-turn) will make this dramatic.

---

## Common PM Mistakes

1. **Not having an opinion on `max_tokens`** — lets engineering pick silently, which caps feature quality you didn't know you were capping.
2. **Assuming a bigger model is always better** — Haiku beats Sonnet on cost for classification and routing, and the user never notices.
3. **Skipping prompt iteration in the PRD** — prompts are product copy; they deserve the same review as UI text.
4. **Not budgeting for prompt eval infrastructure** — you need some way to measure quality, or you can't A/B prompts safely.
5. **Thinking single-turn is always cheaper** — for long-running chats, forced single-turn patterns often waste tokens by re-sending context in a worse format than multi-turn.

> **Key Insight**
>
> The three parameters of `messages.create()` are not technical trivia — they are the three biggest product decisions in any Claude feature: capability (model), cost ceiling (max_tokens), and conversation design (messages). A PM who signs off on all three explicitly in the PRD ships features that hit cost and quality targets. A PM who delegates all three to engineering ships features that quietly miss their targets and get blamed on "the AI."

---

## CCA Exam Relevance

- **D5 (Enterprise Deployment)**: scenario questions about model selection, sizing `max_tokens`, and cost tradeoffs.
- **D1 (Agentic Architecture)**: every agent is a loop over this single call; knowing the atomic unit is a prerequisite.
- Scenario trigger: "The AI feature is too slow / too expensive / too short" → the answer usually lives in one of the three parameters.

---

## Flashcards

| Front | Back |
|-------|------|
| What are the three product-relevant parameters on `messages.create()`? | `model` (capability), `max_tokens` (cost ceiling), `messages` (conversation design) |
| Does `max_tokens` set a target or a ceiling? | A ceiling — if you want longer output, ask for it in the prompt, not by bumping the ceiling |
| Why should a PM have an opinion on model choice? | It trades off cost, speed, and capability; engineering will default to one without PM input |
| When is a smaller model (Haiku) the right call? | Classification, routing, high-volume summarization — places where the user never sees the difference |
| What are the two cost components of every call? | Input tokens (what you send) and output tokens (what Claude writes) |
| What vending machine analogy fits a Claude call? | Pick machine (model), insert coins (API key), press button (messages), get item up to one serving (max_tokens), receipt (usage) |
| Why is prompt quality a PM concern? | Prompts are product copy — they determine output quality and deserve PRD-level attention |
| What do you need before you can A/B test prompts? | A prompt evaluation infrastructure to measure quality changes |
