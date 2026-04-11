# Accessing the API — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D5 — Enterprise Deployment (20%) — primary; D3 — Claude Code Configuration (20%) — secondary; D1 — Agentic Architecture (22%) |
| Task Statements | 5.1 (model selection), 5.3 (production patterns), 3.1 (API key management), 1.2 (agentic loop foundation) |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 04 |

---

## One-Liner

Every Claude feature in your product is really a five-hop journey through client, server, API, model, and back — and PMs who understand the hops make smarter trade-offs around latency, cost, security, and failure UX.

---

## Mental Model: The Airport Connection

Think of a Claude request as a passenger flying from their phone to the model and back:

| Hop | Airport Analogy | PM Stake |
|-----|-----------------|----------|
| 1. Client → Your Server | Passenger boards local flight | UX latency budget starts ticking |
| 2. Your Server → Anthropic | International transfer (with passport = API key) | Security, rate limiting, logging |
| 3. Inside Claude | Customs / baggage handling | You can't see inside, but it costs time & money |
| 4. Anthropic → Your Server | Plane lands, bags unload | You get `stop_reason` + `usage` metadata |
| 5. Server → Client | Passenger catches taxi home | Render streaming, show cost to user if needed |

Every hop adds latency. Every hop is a place something can go wrong. The PM job is to design around the reality that none of this is instant or free.

---

## Why a Server Is a Non-Negotiable Product Requirement

PMs often get asked "can we just call the API from the mobile app?" The answer is always no, and the reason is a business one, not just a technical one:

| Risk of client-side calls | Business Impact |
|---------------------------|-----------------|
| API key extracted from app binary | Credits drained overnight, unexpected invoice |
| Key committed to a public repo | Auto-revoked, feature broken, embarrassing incident |
| No rate limiting on client | Abusive users cost you more than they pay |
| No audit logs | Can't satisfy enterprise compliance asks (SOC2, HIPAA) |

The server is where you enforce all the things legal, finance, and security will eventually demand. Build it on day one, not after the breach.

---

## Product Use Cases

### When the Five-Step Flow Matters Most

| Scenario | Why PMs Care About the Flow |
|----------|----------------------------|
| Chatbot for enterprise customers | Audit logs, PII redaction must happen at server hop |
| Mobile app with AI feature | API key cannot ship in binary; you need a BFF |
| Cost-sensitive free tier | `usage` in response lets you meter per-user without extra calls |
| Regulated industries (health, finance) | Server hop is the only place you can enforce data residency |
| Long-form generation feature | `stop_reason == max_tokens` needs a "continue" UX pattern |

### When It Matters Less (But Still Matters)

| Scenario | Why |
|----------|-----|
| Internal tool for 10 engineers | Security still matters, but cost/latency tuning can wait |
| One-shot experiments | The flow is the same; you just skip the production hardening |

---

## PM Decision Framework

When scoping a Claude-powered feature, walk these questions:

| Question | Why It Matters |
|----------|---------------|
| Where does the API key live? | Answer must be server. If engineering says "client," flag it. |
| What is our `max_tokens` budget per feature? | Drives cost ceiling and UX (truncation handling). |
| How do we handle `stop_reason == max_tokens`? | Do we auto-continue? Show "see more"? Silent truncate? |
| How do we meter usage per user? | `response.usage` is free; a separate billing system is not. |
| Where do we log prompts? | Must be server, with PII redaction. |
| What do we show while waiting? | The five hops take seconds; streaming UX or loaders required. |

---

## The Cost-Transparency Advantage

Every response Anthropic sends back includes `usage.input_tokens` and `usage.output_tokens`. This is a quiet superpower for PMs:

- You can show cost to enterprise users per interaction.
- You can enforce per-user quotas without asking engineering to instrument everything.
- You can A/B test prompt changes and measure cost delta immediately.
- You can build dashboards showing which features are most expensive.

In other SaaS products, you'd need a separate billing pipeline for this. With Anthropic, it's a field on every response.

---

## Common PM Mistakes

1. **Treating AI features as instant** — the five hops take real time; design loading states, streaming, or optimistic UI from day one.
2. **Scoping without a `max_tokens` decision** — leaves engineering to pick a number, which quietly caps your feature's quality.
3. **Forgetting the truncation UX** — `stop_reason == max_tokens` will happen in production; the PRD must describe what users see.
4. **Not requiring cost metering in v1** — retrofitting per-user cost tracking later is 10x harder than using `usage` from the start.
5. **Assuming the client can call Anthropic directly** — blocks your mobile and web launches until security reviews the BFF.

> **Key Insight**
>
> As a PM, the five-step flow is your map for every incident, cost review, and security audit you will ever face on a Claude feature. When an engineer says "the AI is slow" or "the AI broke," your first question should always be "which hop?" That single question forces the team to isolate client vs server vs Anthropic vs model, and it unblocks every post-mortem faster than any other framing.

---

## CCA Exam Relevance

- **D5 (Enterprise Deployment)**: expect scenario questions about where the key lives, how to size `max_tokens`, and how production code handles `stop_reason`.
- **D3 (Claude Code Configuration)**: API key management patterns — the answer is always server-side storage.
- **D1 (Agentic Architecture)**: every agent loop is a for-loop over this five-step envelope.
- Scenario trigger: "A developer puts the key in the mobile app" → the correct answer is always "move it to a backend service."

---

## Flashcards

| Front | Back |
|-------|------|
| What is the five-step Claude request flow, in PM terms? | Client → Server → Anthropic API → Model → back through Server → Client |
| Why can't a mobile app call Anthropic directly? | The API key would be extractable from the app binary, letting anyone drain your credits |
| Which hop is the only place PII redaction can happen? | The server hop (before data leaves your perimeter) |
| What PM-relevant metadata does every response include? | `usage.input_tokens`, `usage.output_tokens`, `stop_reason` |
| What does `stop_reason == max_tokens` mean for UX? | Claude was cut off mid-answer; PRD must describe the truncation UI (e.g. "Continue" button) |
| Why is `usage` in the response a PM superpower? | It enables per-user cost metering and A/B cost comparisons without extra infrastructure |
| When scoping an AI feature, what's the first security question to ask? | "Where does the API key live?" — the only correct answer is a server |
| What do PMs lose by assuming AI responses are instant? | They skip loading / streaming UX, and users perceive the feature as broken during the 2–5 second round trip |
