# Chaining Workflows — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) — PRIMARY |
| Task Statements | 1.2 (agentic patterns — chaining), 5.2 (production workflow deployment) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 79 |

---

## One-Liner

Chaining is the "one thing at a time" workflow: any time Claude struggles to satisfy multiple constraints in a single prompt, or when a task has natural sequential stages, split it into focused steps with outputs flowing from one to the next.

---

## Mental Model: The Newsroom

A magazine article is not written by one person doing everything at once:

| Role | Job | Analogy to Chaining |
|------|-----|---------------------|
| **Reporter** | Gathers raw material | Step 1: research LLM call |
| **Writer** | Turns material into draft | Step 2: drafting LLM call |
| **Copy editor** | Enforces house style, removes clichés | Step 3: revision LLM call |
| **Fact checker** | Validates claims | Step 4: validation (can be non-LLM) |
| **Publisher** | Distributes the finished piece | Step 5: publishing API call |

Each role focuses on what they do best, and work flows from one desk to the next. Chaining workflows are the same idea applied to Claude: instead of one prompt playing all five roles badly, five focused calls each play one role well.

---

## Product Use Cases

### When Chaining Fits

| Scenario | Why Chaining |
|----------|-------------|
| Marketing copy generator with brand voice rules | Step 1 drafts, step 2 enforces voice, step 3 shortens |
| Auto-reply system with tone calibration | Classify intent → draft reply → tone-correct → send |
| Document translation preserving structure | Extract structure → translate text → reassemble |
| Data-to-report pipelines | Fetch data → summarize → format → add visualizations |
| Video content pipeline (lesson example) | Trending topics → research → script → video → post |
| Legal contract review | Section-by-section analysis feeding a final recommendation |

### When Chaining Does Not Fit

| Scenario | Better Alternative |
|----------|-------------------|
| Simple one-shot task | Just one Claude call |
| Independent sub-analyses | Parallelization (lesson 78) |
| Open-ended exploration | Agent (lesson 77) |
| Latency-critical real-time feature | Single call — chaining sums latencies |

---

## The "Long Prompt Problem" PMs Recognize

This is the most common PM pain point chaining solves. You write a PRD saying "the AI should generate content that is X, Y, Z, avoiding A, B, C" — engineering builds a big prompt with all those rules — and the output still violates rules inconsistently.

**Diagnosis**: You're asking Claude to *create* quality content *and* enforce six constraints simultaneously. Split the job:

1. **First call** — focus only on creating good content
2. **Second call** — focus only on enforcing constraints ("remove X, replace Y, adjust tone Z")

The second call succeeds because Claude is no longer balancing creativity against compliance — it is just editing.

This pattern scales to any feature with "the output should be X *and* avoid Y" requirements.

---

## PM Decision Framework

Ask these questions:

| Question | If Yes | Action |
|----------|--------|--------|
| Does the task have natural sequential stages? | Yes | Chaining candidate |
| Is Claude ignoring some rules in a single prompt? | Yes | Chaining (split create/enforce) |
| Do later steps need earlier step outputs? | Yes | Chaining, not parallelization |
| Can I validate output between steps? | Yes | Chaining (adds quality gates) |
| Is a single prompt working reliably? | Yes | Do not chain — keep it simple |

---

## Business Value Framing

When advocating for chaining vs a single big prompt, translate to business-speak:

- **Quality** — "Each step does one thing well instead of several things poorly"
- **Reliability** — "Constraints are enforced by a dedicated revision step, not left to chance"
- **Testability** — "Each step has clear inputs and outputs, so we can unit-test and eval them independently"
- **Observability** — "Failures show up in a specific step, not hidden in a monolithic prompt"
- **Latency trade-off** — "Total time is the sum of step times, so we budget for ~2× the single-prompt time"

---

## Hidden Costs PMs Should Budget For

1. **Latency sums up.** Chains are slower than single prompts. If step 1 is 2s, step 2 is 2s, step 3 is 2s, total is 6s. Users feel this. Mitigate with streaming intermediate outputs if appropriate.
2. **Token cost sums up.** Each step pays its own prompt tokens + output tokens. Model the total cost early.
3. **Error propagation.** A bad step 2 output makes step 3 worse. Require engineering to add validation between steps.
4. **Debugging complexity.** Multi-step failures require trace logs — make sure observability is in the spec.
5. **Eval work multiplies.** Each step needs its own eval dataset *plus* end-to-end evals.

---

## Common PM Mistakes

1. **Chaining when one prompt is enough.** Over-engineering is real. Start with the simplest solution; chain only when the single prompt genuinely fails.
2. **Chain too long.** 3–5 steps is sweet spot. 10+ step chains become fragile and slow. If you need 10+ steps, you probably want multiple smaller chains with checkpoints.
3. **Missing the non-LLM hooks.** Chains let you interleave code between LLM calls — PMs forget this and ask for "AI everything", missing opportunities for deterministic validation.
4. **Not budgeting for eval.** Each chain step needs evals. The eval budget is often bigger than the initial build budget.
5. **Not specifying error handling in the PRD.** When step 3 fails, what happens? Retry? Fallback? Degrade? Fail the whole request? Specify it upfront.

---

> **Key Insight**
>
> Chaining is the "one focused responsibility per call" pattern. When your product requires Claude to balance multiple goals (create + enforce, extract + reformat, classify + respond), split the work into sequential, single-purpose LLM calls. The "long prompt problem" is the #1 PM pain point this solves. For the exam, remember: **chaining has sequential dependencies; parallelization does not.**

---

## CCA Exam Relevance

- **D1 (22%) PRIMARY**: Chaining is one of the four core workflow patterns. Expect scenario questions distinguishing chaining from parallelization and routing.
- **D5 (20%) SECONDARY**: Production patterns — error handling, checkpointing, between-step validation.
- Signal words for chaining: "sequential", "output feeds next step", "break into steps", "focus on one aspect".
- The clearest tell: a scenario describing "Claude writes X, then we ask Claude to revise X" — that is chaining.

---

## Flashcards

| Front | Back |
|-------|------|
| What is chaining in product terms? | Break a task into sequential, focused LLM calls where each step's output feeds the next |
| What is the newsroom analogy for chaining? | Reporter → writer → copy editor → fact checker → publisher; each role focused, work flows between desks |
| What is "the long prompt problem" that chaining solves? | Claude ignores constraints when a single prompt tries to create content AND enforce rules simultaneously |
| How does chaining differ from parallelization? | Chaining has sequential dependencies; parallelization runs independent sub-tasks at the same time |
| When should a PM avoid chaining? | When a single prompt works reliably or latency is the top constraint |
| Name three PM mistakes with chaining. | Chaining when unnecessary, chains too long, forgetting error handling in the PRD |
| What hidden costs should PMs budget for chaining features? | Latency sum, token cost sum, eval per step, error handling, debug complexity |
| Is chaining a workflow or an agent? | A workflow — code owns the sequence, Claude does not decide the next step |
