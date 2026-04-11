# Running the Eval — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation & Iteration (20%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 3.3 (eval execution), 3.1 (eval design), 3.2 (test datasets) |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 20 |

---

## One-Liner

The eval runner is the AI team's "assembly line" — the minimal three-step machine that takes a dataset and emits structured quality data, turning what used to be opinion into something you can dashboard, diff, and ship against.

---

## Mental Model: The Assembly Line

Think of the eval runner as a small factory floor with three stations:

| Station | Engineering name | What it does |
|---------|-----------------|--------------|
| Workbench | `run_prompt` | Assembles the full prompt from a template + one test case, sends it to Claude, collects the raw output |
| Quality check | `run_test_case` | Takes the output, runs it past the scorer, attaches a quality score |
| Conveyor belt | `run_eval` | Feeds every test case through the line, collects a tidy report at the end |

A PM does not need to write the code, but should know the three stations exist — because the three stations are what separate "we ran some tests" from "we have an eval pipeline."

---

## The "Walking Skeleton" Pattern

The most important PM concept in this lesson is the walking skeleton: a pipeline where every function exists but some have placeholder implementations. In this lesson, the grader is temporarily hardcoded to `score = 10` so the rest of the pipeline can be validated end-to-end before any real grading logic is built.

Why PMs should care:

- **Integration risk is de-risked early** — you can demo the pipeline to stakeholders before grading is ready.
- **Scope is protected** — each later phase (real grader, parallel execution, dashboards) plugs in without touching the skeleton.
- **Timeline is honest** — "we have a walking skeleton" is a real milestone; "we have something that looks like eval" is not.

When an engineer says "we built an eval pipeline," ask: is it a walking skeleton, or is it production-ready? The two are months apart and should be tracked separately.

---

## The Result Shape Is a PM Contract

Every result dict the pipeline produces has three keys:

| Key | What's inside | Why a PM cares |
|-----|---------------|----------------|
| `output` | The complete text response from Claude | This is what a customer would have seen |
| `test_case` | The original input | Context for reviewing why a case failed |
| `score` | Numeric quality score | The headline metric for launch/OKR |

The PM value is that once the result shape is locked, you can layer on dashboards, regression tracking, and launch reports without asking engineering to re-instrument anything. The shape is a product-quality contract.

---

## Product Use Cases

### When the Walking-Skeleton Runner Is Enough

| Scenario | Why |
|----------|-----|
| Internal demo of "we have an eval" to execs | Pipeline works end-to-end, score is placeholder — fine for storytelling |
| Early scoping of a new AI feature | Shows the team can iterate even before the grader is real |
| Regression-free refactor of the runner itself | The contract is stable; swapping internals is safe |

### When You Need the Real Grader (Lessons 21–22)

| Scenario | Why |
|----------|-----|
| Any customer-facing release | Hardcoded 10 means no quality signal; you cannot ship on it |
| Comparing two prompt versions | Placeholder grader always gives a tie — useless for iteration |
| Regression CI for prompt changes | You need a real number to detect when a change makes things worse |

---

## PM Decision Framework

When the team reports "the eval ran successfully," ask:

| Question | Good answer | Bad answer |
|----------|-------------|------------|
| Is the grader real or placeholder? | Real (lessons 21/22) | "Hardcoded 10 for now" (fine for dev, not launch) |
| Are the results persisted somewhere we can diff between runs? | Yes, saved to disk or a DB | "Only printed to the notebook" |
| How long does one eval run take? | Acceptable for iteration cadence | Too slow to run on every prompt change |
| Can I see the three-key result format? | Yes, shown in a dashboard | "It's just a list of outputs" |
| If I rerun with the same inputs, do I get the same outputs? | Mostly yes (reproducibility for comparisons) | "Results vary randomly" → needs `temperature` discussion |

---

## Performance Reality Check

The lesson notes that a full eval run on Haiku can take around **30 seconds** even on a small dataset. For a PM, this is an early warning:

- **30 seconds × 1,000 test cases = 8 hours.** Production-scale eval will need parallelization.
- **Rerun cost matters.** If every prompt PR triggers an 8-hour eval, engineers will stop running it. Design the pipeline so it fits the iteration cadence.
- **Cost budget.** Each run is money, especially at scale. Build that into the feature's operating cost from day one.

---

## Common PM Mistakes

1. **Celebrating the walking skeleton as "eval is done"** — it is the foundation, not the shipped feature; lessons 21–22 add the real grader.
2. **Not persisting `results`** — if every run disappears after the notebook closes, there is no history, no diff, no regression signal.
3. **Ignoring runtime** — at scale, sequential loops become unusable; push for parallelization before the dataset grows.
4. **Forgetting the result shape is a contract** — when downstream tools depend on `output / test_case / score`, changing that shape silently breaks dashboards.
5. **Confusing "walking skeleton" with "production pipeline"** — they are months apart; track them as separate milestones.

---

> **Key Insight**
>
> A walking-skeleton eval runner is the cheapest way to turn prompt quality into a dashboard-ready metric, even before the grader is real. The minute you have the three-function pipeline and a stable result shape, you can layer observability, CI, and regression tracking on top without further engineering changes. CCA exam questions about "how do you actually execute an eval against a dataset" are D3 task 3.3 — the answer is always the `run_eval → run_test_case → run_prompt` layering with a structured result dict.

---

## CCA Exam Relevance

- **D3 (Evaluation & Iteration)**: understand the three-function decomposition; know that the result dict has `output`, `test_case`, and `score`; recognize the walking-skeleton pattern.
- **D5 (Enterprise Deployment)**: the pipeline is the substrate for production eval; stable contracts enable dashboards, CI, and regression gates.
- Exam trigger: any question about the *mechanics* of running an eval maps to this lesson's three functions.

---

## Flashcards

| Front | Back |
|-------|------|
| What are the three functions in the eval runner, and what does each do? | `run_eval` loops over the dataset, `run_test_case` orchestrates prompt + grader, `run_prompt` merges template with input and calls Claude. |
| What is a "walking skeleton" in this lesson? | A full pipeline with placeholder implementations (e.g., `score = 10`) so integration can be validated end-to-end before each stage is production-ready. |
| What three keys does every result dict contain? | `output` (Claude's response), `test_case` (the original input), `score` (numeric quality score). |
| Why is the stable result shape valuable for PMs? | It is a contract — dashboards, regression tracking, and launch reports can be built on top without asking engineering to re-instrument. |
| How long does one eval run roughly take on Haiku (per the lesson)? | Around 30 seconds for a full small dataset. |
| Why should a PM care about parallelization? | Because sequential loops scale linearly with dataset size, and at production scale they become too slow to run on every prompt change. |
| When is the walking-skeleton runner NOT enough for launch? | When you need a real quality signal — i.e., any customer-facing release where the placeholder score would make the eval meaningless. |
| What PM-level risk does "results printed but not persisted" create? | No historical diff, no regression detection, and no way to attribute quality changes to specific prompt versions. |
