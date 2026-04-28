# Overview of Claude Models — PM Quick-Scan

| Item | Detail |
|------|--------|
| Exam Domain | D5 — Enterprise Deployment (20%) — primary |
| Task Statements | 5.1 (model selection for production workloads) |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 03 |

---

## One-Liner

Claude offers three model tiers — Opus (smartest), Sonnet (balanced), Haiku (fastest/cheapest) — and choosing the right model per feature is the single biggest lever PMs have over AI cost and user experience.

---

## Mental Model: The Consulting Firm

Think of the three models as three tiers of consultants:

| Model | Consultant Analogy | When to Hire |
|-------|-------------------|-------------|
| Opus | Senior partner — deep expertise, expensive, takes time | Complex strategy work, high-stakes decisions |
| Sonnet | Mid-level associate — capable, reasonably priced, solid speed | Most day-to-day client work |
| Haiku | Junior analyst — fast, cheap, good for routine tasks | High-volume grunt work, quick turnaround |

You would never assign a senior partner to answer routine emails. Likewise, you should not route simple classification tasks to Opus.

---

## The Three Models at a Glance

| Dimension | Opus | Sonnet | Haiku |
|-----------|------|--------|-------|
| Intelligence | Highest | High | Moderate |
| Speed | Slower | Moderate | Fastest |
| Cost | Highest | Moderate | Lowest |
| Extended thinking | Yes | Yes | No |
| Best for | Complex reasoning, multi-hour autonomous tasks | General-purpose, coding, most features | Real-time chat, classification, high-volume |

---

## Why Model Selection Is a PM Decision

Model selection is not purely technical. It directly controls:

| Business Lever | Impact |
|---------------|--------|
| Cost per interaction | Opus can cost 5-10x more than Haiku for the same conversation |
| User-perceived latency | Haiku responds in under a second; Opus may take several seconds |
| Feature quality ceiling | Haiku cannot do extended thinking; some features are impossible without Opus/Sonnet |
| Scalability budget | High-volume features on Opus can blow through budget in hours |

**The PM job**: define which features need which quality tier, then work with engineering to route accordingly.

---

## Product Use Cases

| Scenario | Recommended Model | Why |
|----------|------------------|-----|
| Customer support chatbot (high volume) | Haiku | Speed + cost; most support queries are routine |
| Document analysis for legal review | Opus | Complex reasoning over long documents |
| In-app writing assistant | Sonnet | Good quality, acceptable latency |
| Real-time autocomplete suggestions | Haiku | Sub-second latency is non-negotiable |
| Multi-step research agent | Opus | Needs extended thinking and autonomy |
| Code review tool | Sonnet | Strong coding ability, precise edits |

---

## PM Decision Framework

| Question | Answer Drives |
|----------|--------------|
| How complex is the reasoning our feature needs? | Opus vs Sonnet vs Haiku |
| How fast must the response feel to users? | Haiku for real-time, Sonnet/Opus for async |
| What is our cost ceiling per user per month? | Model mix ratio |
| Can we use different models for different features? | Almost always yes — this is the recommended pattern |
| Does any feature need extended thinking? | If yes, Haiku is ruled out for that feature |

---

## The Multi-Model Architecture

The most cost-effective production pattern is to use multiple models:

| Application Layer | Model | PM Rationale |
|-------------------|-------|-------------|
| Greeting / routing / classification | Haiku | Instant, cheap; users don't need intelligence here |
| Main feature logic | Sonnet | Quality matters but so does response time |
| Escalation / complex edge cases | Opus | Reserve the expensive model for high-value moments |

This pattern can reduce AI costs by 60-80% compared to using a single high-end model for everything.

---

## Common PM Mistakes

1. **Defaulting to the "best" model** — Opus everywhere is like hiring senior partners for filing. Most features don't need maximum intelligence.
2. **Ignoring the cost-per-interaction math** — run the numbers before committing. A feature serving 100K users/day on Opus costs very differently than on Haiku.
3. **Not specifying model per feature in the PRD** — if you leave model selection to engineering without context, they will either over-spend (Opus for safety) or under-deliver (Haiku for budget).
4. **Forgetting Haiku's limitation** — it cannot do extended thinking. If your feature spec says "the AI should reason step by step," Haiku is out.
5. **Treating model selection as permanent** — you can change models per feature as quality or budget needs evolve. Build the routing flexibility from day one.

> **Key Insight**
>
> Model selection is the highest-leverage cost decision a PM makes on a Claude-powered product. It is not a technical detail to delegate — it is a business architecture choice that determines your unit economics and user experience simultaneously. The right answer is almost always "use multiple models, routed by task complexity."

---

## CCA Exam Relevance

- **D5 (Enterprise Deployment)**: model selection questions are a near-certainty. Expect scenarios describing a workload and asking which model fits.
- Know the three-way trade-off: intelligence vs speed vs cost.
- Remember: Haiku does NOT support extended thinking. This is the most testable differentiator.

---

## Flashcards

| Front | Back |
|-------|------|
| What are Claude's three model families? | Opus (smartest), Sonnet (balanced), Haiku (fastest/cheapest) |
| Which model is best for real-time user-facing features? | Haiku — lowest latency and cost |
| Why is model selection a PM decision, not just engineering? | It directly controls cost per interaction, perceived latency, and feature quality ceiling |
| What is the recommended production pattern for model selection? | Use multiple models — Haiku for simple tasks, Sonnet for core logic, Opus for complex reasoning |
| Which model lacks extended thinking support? | Haiku — it cannot do step-by-step reasoning |
| How much can multi-model routing reduce costs? | 60-80% compared to using a single high-end model for everything |
| When should a PM insist on Opus? | When the feature requires deep reasoning, multi-step planning, or long autonomous operation |
| What model does this course use as its default? | Sonnet — best balance of quality, speed, and cost |
