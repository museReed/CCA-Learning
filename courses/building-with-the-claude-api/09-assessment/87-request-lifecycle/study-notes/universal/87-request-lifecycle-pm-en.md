# Request Lifecycle — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 1.1 (API request flow), 5.1 (secure architecture), 5.3 (stop reasons and token limits) |
| Source | building-with-the-claude-api / 09-assessment / Lesson 87 |

---

## One-Liner

The Claude request lifecycle is the anatomy of every AI interaction in your product — understanding it lets PMs make sound decisions on security, latency budget, cost, and incident response before the first line of code is written.

---

## Why PMs Should Care

PMs do not need to write the `ast.parse` call or implement tokenization — but PMs *do* need to decide architecture, review security, set token budgets, and own incident response. Every one of those decisions lives inside this five-step lifecycle:

| PM Decision | Which Lifecycle Step Informs It |
|-------------|--------------------------------|
| "Where does our API key live?" | Steps 1-2 (never in the client) |
| "What is our worst-case latency?" | Step 3 (model) + network on 1-2, 4-5 |
| "What is our per-request cost ceiling?" | Step 2 (max_tokens) + Step 4 (usage) |
| "How do we handle a truncated answer?" | Step 4 (stop_reason) |
| "What's our incident triage flow?" | Every step — the lifecycle is the map |

Skip this knowledge and your team will make these decisions without you, usually badly.

---

## Mental Model: The Restaurant Order

Think of every Claude request as ordering food at a restaurant with a kitchen that speaks a different language:

| Step | Restaurant Analogy | Lifecycle Step |
|------|-------------------|----------------|
| Customer tells waiter what they want | User talks to your app | Request to server |
| Waiter writes the order in the kitchen's language | Your server calls the Anthropic API | Request to API |
| Kitchen prepares the dish | Claude tokenizes, embeds, contextualizes, generates | Model processing |
| Waiter carries the plate back | API returns message, usage, stop_reason | Response to server |
| Plate placed in front of customer | Your server forwards text to the UI | Response to client |

The waiter (your server) is non-negotiable. You would never let the customer walk into the kitchen themselves — and you never let the client call the Anthropic API directly, for the same reason: it breaks the kitchen's safety and speed guarantees.

---

## Product Use Cases: Where Each Step Matters

### Security (Steps 1-2)

The source is categorical: **never call the Anthropic API from client-side code**. API keys in client code can be extracted and used for unauthorized requests. For a PM, this translates into non-negotiable security requirements in every PRD for an AI feature:

- API key lives on the server in secure storage
- Client only talks to your server, never to Anthropic
- Server adds authentication, rate limiting, and audit logging

### Cost & Latency (Steps 2-3)

Every request must include a `max_tokens` value. This is the single most important cost lever a PM owns. Set it too high and runaway generations blow your unit economics. Set it too low and Claude gets cut off mid-sentence, frustrating users. A common PM move is to tier it by feature: short replies get 256, long explanations get 2048, document drafts get 8192.

### Response Handling (Step 4)

The API response contains three fields the PM cares about:

| Field | PM Concern |
|-------|-----------|
| Message | The actual content the user sees |
| Usage | Drives billing, budget tracking, per-user quotas |
| Stop Reason | Determines whether the feature worked or silently truncated |

The stop_reason is the sneakiest of the three. If your app ignores it, a `max_tokens` truncation looks exactly like a complete answer — except half the paragraph is missing. Always handle stop reasons explicitly in the UX (e.g., "Response was cut off — continue?").

---

## The Four Internal Stages — Why PMs Should Care

Claude's internal processing has four stages: **tokenization, embedding, contextualization, generation**. A PM does not need to implement these, but understanding them at a conceptual level unlocks better product intuition:

| Stage | PM Insight |
|-------|-----------|
| **Tokenization** | Cost and length are measured in tokens, not words. Inputs with lots of code or non-English text cost more than you'd guess. |
| **Embedding** | Every token carries *all* its meanings at first — which is why short, ambiguous inputs produce unreliable outputs. |
| **Contextualization** | Surrounding words disambiguate meaning — which is why well-framed prompts beat bare instructions. |
| **Generation** | Claude uses controlled randomness, not pure max probability — which is why identical requests sometimes produce different answers, and why "deterministic" is not the default. |

---

## PM Decision Framework

| Question | If Yes | Action |
|----------|--------|--------|
| Does our architecture have a server between client and Anthropic? | Yes | Pass security review |
| Does every request have a sensible `max_tokens`? | Yes | Pass cost review |
| Does the app differentiate `end_turn` from `max_tokens` stop reasons? | Yes | Pass UX review |
| Is per-user token usage logged and budgeted? | Yes | Pass financial review |
| Does the team know which lifecycle step failed when an incident hits? | Yes | Pass incident review |

---

## Common PM Mistakes

1. **Letting engineering ship client-direct API calls** — instant security incident waiting to happen. This should fail every security review.
2. **Not owning max_tokens** — leaving it at engineering defaults means costs scale linearly with usage with no product input.
3. **Ignoring stop_reason in UX spec** — the answer silently truncates and users blame the AI for being dumb.
4. **Confusing words with tokens in the PRD** — a "200-word limit" is not the same as `max_tokens=200`; tokens can be sub-word.
5. **Expecting deterministic output** — the generation step uses controlled randomness; identical inputs can produce different outputs, and your acceptance tests must account for that.

> **Key Insight**
>
> Every sophisticated Claude pattern — tool use, streaming, caching, agents — is a variation on the same five-step lifecycle. A PM who holds this model in their head can read any proposal for an AI feature and instantly ask the right questions about security, cost, latency, and failure handling. A PM who skips it has to guess, and usually guesses wrong on the expensive ones.

---

## CCA Exam Relevance

- **D1 (Agentic Architecture)**: The lifecycle is the foundation of every agentic pattern. Questions will often be framed as "where does X happen in the request flow?"
- **D5 (Enterprise Deployment)**: Secure architecture, token budgeting, and stop-reason handling are production deployment essentials.
- Watch for: "Why do you need a server between the client and Anthropic?" → API key security, always.

---

## Flashcards

| Front | Back |
|-------|------|
| What are the five steps of the Claude request lifecycle? | Client to server → server to API → model processing → API to server → server to client. |
| Why must a PM require a server between client and Anthropic API? | To protect the API key — client-side keys can be extracted and used for unauthorized requests. |
| What is the restaurant analogy for the server's role? | The waiter — the non-negotiable intermediary between the customer and the kitchen. |
| What are the four required fields in every API request? | API Key, Model, Messages, Max Tokens. |
| What are the four internal processing stages inside Claude? | Tokenization, embedding, contextualization, generation. |
| Which response field tells you whether the answer was silently truncated? | `stop_reason` — if it is `max_tokens` the answer was cut off. |
| What cost lever does a PM own at the request level? | `max_tokens` — it directly caps per-request cost and latency. |
| Why are identical Claude requests not always deterministic? | The generation step uses a mix of probability and controlled randomness. |
| What does the `usage` field enable for PMs? | Billing, budget tracking, and per-user quotas. |
| Why should a PM distinguish words from tokens in a PRD? | Tokens can be sub-word, whitespace, or symbols — "200 words" is not the same as `max_tokens=200`. |
