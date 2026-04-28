# System Prompts — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D5 — Enterprise Deployment (20%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 5.1 (model selection & configuration), 5.3 (production patterns), 1.2 (agentic loop foundation) |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 09 |

---

## One-Liner

A system prompt is the "job description" you hand Claude at the start of every conversation — it turns a generic AI into your product's specific persona, and it is the single biggest lever PMs have over output quality and on-brand behavior.

---

## Why PMs Should Care

Without a system prompt, every user of your product talks to the same generic, vanilla Claude that anyone else can get from the consumer Claude.ai app. That is not a product — that is a thin wrapper. The system prompt is where your differentiation lives.

| Without system prompt | With a well-crafted system prompt |
|----------------------|------------------------------------|
| Generic, helpful-but-unspecific replies | On-brand voice, consistent tone |
| Direct answers that skip the user journey | Experience designed around your user's goal |
| Same behavior as every other Claude integration | Differentiated product behavior |
| No guardrails — off-topic questions answered | Bounded scope, graceful refusals |
| Unpredictable formatting | Reliable, parseable structure |

The math tutor example is instructive. Without guidance, Claude answers "5x + 2 = 3" by giving the solution. A real tutoring product doesn't want that — it wants the **pedagogical experience**, not the answer. The system prompt is how you encode "this is a tutor, not a calculator."

---

## Mental Model: The Onboarding Briefing

Imagine you hire a world-class consultant. They are brilliant, but on day one they know nothing about your company, your customers, or your brand voice. What do you do? You give them an onboarding briefing:

- "You are the lead customer success manager for an enterprise SaaS company."
- "Our tone is friendly but professional — never use emojis, always sign off with the customer's name."
- "Never promise timelines you cannot verify."
- "Here are three example emails from our best CSM — match this style."

That briefing is the system prompt. Every user query Claude receives is a new customer email — the briefing shapes how every reply lands.

---

## Product Use Cases

### When System Prompts Are Critical

| Scenario | Why the system prompt matters |
|----------|-------------------------------|
| Customer support chatbot | Brand voice, escalation rules, knowledge boundaries |
| Math / language tutor | Pedagogical stance (guide, don't solve) |
| Legal / medical assistant | Hard guardrails, disclaimers, scope limits |
| Code review tool | Technical persona, severity rubric, output schema |
| Internal HR bot | Company policy as source of truth, privacy rules |

### When System Prompts Are Less Important

| Scenario | Why |
|----------|-----|
| Generic ChatGPT-style playground | Users expect vanilla assistant behavior |
| One-off research query | No repeatable workflow to encode |
| Prototype before product-market fit | Iteration speed beats persona polish |

---

## The Five Things Every Production System Prompt Needs

1. **Identity** — "You are ..." Who is Claude pretending to be?
2. **Task scope** — What is in scope? What is out of scope?
3. **Voice & format** — Tone, length, structure, whether to use markdown.
4. **Guardrails** — Hard rules for safety, privacy, legal, brand.
5. **Examples** — One or two gold-standard outputs to anchor style.

If your system prompt is missing any of these five, you have a quality bug waiting to happen.

---

## PM Decision Framework

When specifying a new AI feature, ask these questions:

| Question | If "Yes" | Implication |
|----------|----------|-------------|
| Does the feature have a specific persona or role? | Yes | System prompt — define it explicitly |
| Are there topics Claude should refuse? | Yes | System prompt — encode refusal rules |
| Is there a required output format (JSON, markdown, bullets)? | Yes | System prompt — specify the structure |
| Do we need brand voice consistency? | Yes | System prompt — lock the tone |
| Should behavior stay stable across multi-turn conversations? | Yes | System prompt — persistent context |
| Is context unique per user / per query? | Yes | **Not** system prompt — put in `messages` |

The last row is the trap most PMs fall into: shoving per-user data into the system prompt because "that's where instructions go." Dynamic context belongs in `messages`, not `system` — otherwise you break prompt caching and waste money.

---

## Common PM Mistakes

1. **Treating system prompts as one-and-done** — they are products. Version them, A/B test them, measure regressions. When quality degrades, the system prompt is where you look first.
2. **Writing vague instructions** — "Be helpful and friendly" is useless. "Always respond in three bullets, never more than 40 words total, never use exclamation marks" is actionable.
3. **Stuffing dynamic data into the system prompt** — per-user context belongs in messages so caching works.
4. **Not specifying the system prompt in the PRD** — engineers will write a default one, and it will not match your vision. Include the system prompt as an acceptance criterion.
5. **Copying the user's request into a "system message"** — system prompts are ambient rules, not the current task. If you mix them up, behavior becomes unpredictable.

> **Key Insight**
>
> The system prompt is the only place where you can guarantee Claude behaves like *your* product instead of a generic assistant. It is the highest-leverage artifact a PM can own in an AI feature — more leverage than model choice, temperature, or even tool selection. If you outsource writing it to an engineer with no product context, your feature will feel like a wrapper around Claude, not a product.

---

## CCA Exam Relevance

- **D5 (Enterprise Deployment)**: system prompts are the canonical production mechanism for enforcing consistent behavior across an enterprise deployment.
- **D1 (Agentic Architecture)**: the system prompt is the stable identity layer of every agent, persisting across tool-use loops.
- Watch for scenarios phrased as "How do you enforce brand voice / refusal rules / output format?" — the answer on the exam is always system prompt, not per-message engineering.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the PM-level definition of a system prompt? | The "job description" or onboarding briefing you give Claude — it defines persona, scope, voice, and guardrails for an entire conversation. |
| What are the five essential elements of a production system prompt? | Identity, task scope, voice & format, guardrails, examples. |
| Why shouldn't per-user data go in the system prompt? | Because the system prompt should be stable and cacheable; per-user data belongs in `messages` so prompt caching works and context can evolve per turn. |
| What is the biggest product risk of not writing a system prompt? | Your feature becomes a thin wrapper around generic Claude — no differentiation, inconsistent voice, no guardrails. |
| In a math tutor product, what does the system prompt prevent? | It prevents Claude from giving direct answers and enforces step-by-step Socratic guidance. |
| Should "Be helpful" be part of a system prompt? | No — it is vague and provides no real constraint. Specific, testable rules ("Always respond in 3 bullets max") are what move quality. |
| Who in the team should own the system prompt? | PM — it encodes product intent. Engineers implement; PM defines the contract, versions it, and A/B tests it. |
| What CCA domain does system-prompt design map to most directly? | D5 Enterprise Deployment — it is how you enforce production-grade consistency at scale. |
