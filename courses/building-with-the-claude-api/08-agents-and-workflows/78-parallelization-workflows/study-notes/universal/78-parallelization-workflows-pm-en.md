# Parallelization Workflows — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) — PRIMARY |
| Task Statements | 1.2 (agentic patterns — parallelization), 5.2 (production workflow deployment) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 78 |

---

## One-Liner

Parallelization workflows are the product move when quality depends on depth per criterion: instead of asking Claude to juggle 10 criteria in one prompt, you run 10 focused sub-analyses in parallel and aggregate the verdict — better answers, similar latency, at the cost of more API spend.

---

## Mental Model: The Tasting Panel

Imagine choosing a wine for a restaurant menu.

| Approach | What It Looks Like | Result |
|----------|-------------------|--------|
| One generalist taster | "Is this wine good?" — answers everything at once | Average, wobbly judgment |
| **Specialist panel (parallelization)** | One taster for acidity, one for tannins, one for finish, one for value, one for food pairing, one head judge to aggregate | Focused depth + integrated final verdict |

Parallelization workflows are the specialist panel. Each expert concentrates on *one* axis; a head judge reads all expert notes and makes the final call. Better decisions, faster than running them sequentially, at the cost of paying every expert.

---

## Product Use Cases

### When to Use Parallelization

| Scenario | Why Parallelization Helps |
|----------|---------------------------|
| Material recommender (lesson example) | Each material needs deep, specialized evaluation |
| Resume screening (pro/con per dimension) | Evaluate candidates on skills, experience, culture fit independently |
| Content moderation voting | Run N safety checks and take majority vote for high-stakes decisions |
| Code review across multiple rubrics | Security reviewer + style reviewer + performance reviewer + maintainability reviewer |
| Multi-lens customer feedback analysis | Sentiment, urgency, topic, action-required — each as its own sub-task |
| Document comparison across multiple criteria | Legal, financial, technical analysis in parallel |

### When NOT to Use Parallelization

| Scenario | Better Alternative |
|----------|--------------------|
| Task with sequential dependencies | Use **chaining** (lesson 79) |
| Simple single-answer question | Just one Claude call |
| Cost is the top constraint | Single prompt with well-engineered criteria |
| Sub-tasks cannot be truly independent | Chaining or agent |

---

## The Two Flavors

| Flavor | Product Use | Example |
|--------|-------------|---------|
| **Sectioning** | Break a decision into multiple dimensions | Material recommender (one LLM per material) |
| **Voting** | Run the same evaluation N times for reliability | Moderation: "is this safe?" × 5 voters, majority wins |

Sectioning improves *quality* by giving each dimension focused attention. Voting improves *reliability* by averaging out noise. Some features benefit from both (e.g., "5 safety votes for each of 3 risk categories").

---

## PM Decision Framework

Ask these questions:

| Question | If Yes | Action |
|----------|--------|--------|
| Does the decision depend on multiple independent criteria? | Yes | Sectioning candidate |
| Do sub-tasks need each other's outputs? | Yes | NOT parallelization — use chaining |
| Is quality > cost for this feature? | Yes | Parallelization is a fit |
| Is latency a key metric? | Yes | Parallel N calls ≈ slowest single call (good!) |
| Do you need high reliability on a binary decision? | Yes | Voting variant |

---

## Business Value Translation

When pitching this architecture to engineering or finance, translate it into business-speak:

- **Quality** — "We get specialist-level analysis per criterion instead of generalist analysis across all criteria"
- **Latency** — "The user waits for the slowest sub-task, not the sum of all sub-tasks — roughly the same perceived speed"
- **Cost** — "API bill multiplies by N, but each sub-task is typically smaller and faster than a monolithic prompt; real cost varies"
- **Scalability** — "Adding a new criterion = adding a prompt file. No regression on existing criteria."
- **A/B testing** — "We can iterate on one sub-task's prompt without re-testing the others"

---

## Production Guardrails PMs Must Request

When shipping a parallelization workflow, ask engineering to build:

1. **Per-task timeouts** — one slow call should not stall the whole request
2. **Partial-result handling** — if 5 of 6 sub-tasks finish and one fails, can you still produce a useful aggregate?
3. **Fan-out cap** — never let N grow unbounded based on user input
4. **Cost alerts** — parallelization multiplies token spend; watch for anomalies
5. **Aggregator fallback** — if the aggregator LLM fails, do you have a rule-based fallback?

---

## Common PM Mistakes

1. **Confusing parallelization with agents.** Parallelization runs multiple *predetermined* sub-tasks. The code still owns the flow. It is still a workflow.
2. **Missing the aggregator step.** Shipping "here are 6 analyses" to the user is a failure — users want one answer, not a jury. Always budget time for the aggregator prompt.
3. **Under-budgeting API spend.** Parallelization is the easiest way to 5–10× your token bill without realizing it. Model the unit economics upfront.
4. **Using voting when sectioning would do.** Voting is expensive — use it only for high-stakes binary decisions where reliability matters more than depth.
5. **Forgetting partial-failure semantics.** If one sub-task errors, does the feature degrade gracefully or crash the whole request? Specify in the PRD.

---

> **Key Insight**
>
> Parallelization is the "specialist panel" workflow — each Claude call gets a single narrow job, then a head judge aggregates the results. It is the standard product move whenever a decision depends on multiple independent criteria, each deserving focused analysis. Trade quality and latency wins for higher API spend, and always include an aggregator step. For the exam, remember both flavors: **sectioning** (different sub-tasks) for depth, **voting** (same task N times) for reliability.

---

## CCA Exam Relevance

- **D1 (22%) PRIMARY**: Parallelization is one of the four core workflow patterns from "Building Effective Agents". Expect a scenario question.
- **D5 (20%) SECONDARY**: Production deployment — latency, cost, partial failure.
- Exam signal words: "split into independent evaluations", "run simultaneously", "aggregate", "fan out / fan in".
- Memorize both variants (sectioning and voting) and one example of each.

---

## Flashcards

| Front | Back |
|-------|------|
| What is a parallelization workflow in product terms? | Run multiple focused sub-analyses in parallel and aggregate them into one answer |
| What is the "tasting panel" analogy? | Specialists each evaluate one criterion, a head judge combines their notes into a final verdict |
| Name the two flavors of parallelization. | Sectioning (different sub-tasks for depth) and voting (same task repeated for reliability) |
| When should a PM avoid parallelization? | When sub-tasks depend on each other's outputs, or when cost is the top constraint |
| What is the key latency benefit? | Total time ≈ slowest sub-task, not sum of sub-tasks |
| What is the key cost cost? | N× API spend vs one call — token bill multiplies |
| What production guardrail is critical for parallelization? | Per-task timeouts and partial-failure handling |
| Is parallelization a workflow or an agent? | A workflow — the code owns the fan-out/fan-in structure, Claude does not decide |
