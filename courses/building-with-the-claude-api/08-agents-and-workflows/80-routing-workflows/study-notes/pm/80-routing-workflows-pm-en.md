# Routing Workflows — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) — PRIMARY |
| Task Statements | 1.2 (agentic patterns — routing), 5.2 (production workflow deployment) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 80 |

---

## One-Liner

Routing is the "triage desk" workflow — before doing the work, a quick classifier decides which specialized pipeline should handle the request. It's the right architecture when your product handles distinctly different request types that each deserve different treatment.

---

## Mental Model: The Hospital Triage Desk

When you walk into an emergency room, the first person you meet is the triage nurse. They ask a few questions and decide where you go:

| Triage result | Pipeline |
|---------------|----------|
| Chest pain | Cardiology unit |
| Broken bone | Orthopedics |
| Fever and cough | General medicine |
| Psychiatric concern | Mental health unit |

The triage nurse is not a cardiologist or an orthopedic surgeon — they are a classifier. They route patients to the specialist who can actually treat them. Each specialist unit is optimized for its case load, not for "everything".

Routing workflows are the triage desk. A small classifier LLM call decides which specialized prompt (or sub-pipeline) handles the request. Each specialist does one thing really well.

---

## Product Use Cases

### When Routing Fits

| Scenario | Why Routing |
|----------|-------------|
| Customer support bot (billing / technical / refund) | Each type needs different tools, KB, and tone |
| Content generation (educational / entertainment / review) — lesson example | Each genre needs a different style |
| Multi-domain assistant (coding / writing / math) | Each domain needs different context and prompts |
| Intent-based routing (question / task / small talk) | Different response types, different latency budgets |
| Multi-tier model selection | Route simple requests to Haiku, complex ones to Opus |
| Localized pipelines (English / Chinese / Japanese) | Different prompts, locale-specific tools |

### When Routing Does Not Fit

| Scenario | Better Alternative |
|----------|--------------------|
| Single request type with narrow scope | Just one prompt |
| Overlapping categories the classifier cannot distinguish | Chaining or agent |
| Latency ultra-sensitive (every ms matters) | Skip the classification call, use one good prompt |
| Categories constantly change | Routing is brittle — consider an agent |

---

## The Two-Step Shape

```
user input ──→ [triage LLM call] ──→ category ──→ [specialist pipeline] ──→ output
```

1. **Triage call** — fast, cheap, structured output (one category label)
2. **Specialist call** — slower, expensive, optimized for that category

PMs must be explicit about both calls in the PRD. Each has its own latency budget, model choice, prompt, eval, and fallback behavior.

---

## The `tool_choice` Trick PMs Must Understand

Engineering should implement the classifier using Claude's tool use with `tool_choice` set to force a specific tool. PMs do not need to write the code, but must understand why it matters:

- **Reliability** — forcing a structured tool call guarantees the classifier returns a valid category, not a free-form "maybe educational?"
- **Safety** — an `enum` list prevents Claude from inventing new categories your pipeline cannot handle
- **Debugging** — structured outputs are trivial to log and inspect

If engineering says "we'll ask Claude and parse the response", push back: that is fragile. Ask for `tool_choice={"type": "tool", "name": "..."}` with an enum schema.

---

## PM Decision Framework

| Question | If Yes | Action |
|----------|--------|--------|
| Does your product handle distinctly different request types? | Yes | Routing candidate |
| Can you list the categories on one page? | Yes | Categories are clear enough |
| Does each category benefit from a specialized prompt or tool set? | Yes | Routing |
| Can Claude (or a cheaper classifier) reliably categorize? | Yes | Routing is viable |
| Is one extra LLM call acceptable in latency and cost? | Yes | Ship it |
| Do categories overlap a lot? | No | Routing is reliable |

If you answer yes to all, routing is the right move. One "no" usually kills the case.

---

## Production Requirements PMs Must Ask For

1. **Enum-constrained tool classifier** — use `tool_choice` with a predefined enum, not free-form text
2. **Low-confidence fallback** — when the classifier is uncertain, route to a default/generic pipeline or human review
3. **Per-category observability** — log category distribution, conversion by category, failure rate by category
4. **Cheap classifier model** — use a smaller model (e.g., Haiku) for classification to keep costs low
5. **Eval per branch** — each specialist pipeline needs its own eval dataset; generic evals miss per-category quality drops
6. **Abuse protection** — malicious inputs could try to trigger the wrong branch; sanity-check category selections

---

## Business Value Framing

- **Quality** — "Each request type gets a dedicated, optimized handler instead of a one-size-fits-all prompt"
- **Scalability** — "Adding a new request type = adding a new branch; no regression on existing types"
- **Cost** — "We can send simple requests to cheaper models and complex ones to the top-tier model"
- **Latency** — "Cheap classification + focused specialist is often faster than a slow generic prompt"
- **Observability** — "We can see exactly which request types our users send and which ones perform poorly"

---

## Common PM Mistakes

1. **Too many categories.** PMs love taxonomies; classifiers hate them. Keep categories to 10 or fewer. If you need more, chain or sub-classify.
2. **Overlapping categories.** If a request can belong to two categories, the classifier will flip-flop. Define categories so each request has one obvious home.
3. **No fallback pipeline.** Never assume the classifier is always right. Ship a default "general" pipeline for low-confidence cases.
4. **Confusing routing with agents.** A routing workflow is still a workflow — the code picks the pipeline after classification. An agent would let Claude pick tools autonomously. PMs sometimes mix these up in design docs.
5. **Forgetting per-category metrics.** A product with routing needs a dashboard per category — otherwise you cannot see which branch is degrading.

---

> **Key Insight**
>
> Routing is the "triage desk" workflow — classify first, then dispatch to a specialist. It is the standard product move when your app handles diverse request types that each deserve focused handling. The production-critical detail is the classifier implementation: use forced tool use with an enum input schema to guarantee a valid category label. For the exam, remember: **routing is a workflow (code dispatches), not an agent (Claude decides).**

---

## CCA Exam Relevance

- **D1 (22%) PRIMARY**: Routing is one of four core workflow patterns. Expect scenario questions.
- **D2 (18%) SECONDARY**: `tool_choice="tool"` forced tool use is explicitly tested.
- **D5 (20%) SECONDARY**: Production patterns — cheap classifier model, per-branch eval, fallback pipeline.
- Signal words: "categorize", "classifier", "dispatch", "different types of requests", "specialized pipeline".
- Trap: routing ≠ agent. Routing is a predetermined dispatch after one classification call.

---

## Flashcards

| Front | Back |
|-------|------|
| What is routing in product terms? | A triage step classifies the request, then code dispatches to a specialized pipeline |
| What is the triage desk analogy? | A nurse asks a few questions and sends the patient to cardiology, orthopedics, or general medicine |
| Why use forced tool use for the classifier? | Guarantees a structured category label from an enum, no free-form parsing required |
| What is a key PM mistake when designing routing features? | Too many or overlapping categories — classifiers become unreliable |
| What production guardrail is essential for routing? | A fallback/default pipeline for low-confidence classifier output |
| Is routing a workflow or an agent? | A workflow — code owns the dispatch decision after classification |
| What is one cost optimization PMs should ask for? | Use a smaller/cheaper model for the classifier step (classification is simpler than generation) |
| What metric does a routing product need beyond overall quality? | Per-category metrics — category distribution and failure rate by branch |
