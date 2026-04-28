# A Typical Eval Workflow — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation & Iteration (20%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 3.1 (eval design), 3.2 (test datasets), 3.3 (eval execution) |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 18 |

---

## One-Liner

A prompt eval workflow is the AI team's equivalent of a product launch checklist — a repeatable five-step process that produces a single quality number every PM can use in launch docs, OKRs, and prioritization decisions.

---

## Mental Model: The Recipe Testing Kitchen

A professional test kitchen doesn't ship a new cereal recipe based on one taste. They have a fixed panel of tasters, a fixed scoring rubric, and they re-score every variant until the average crosses a bar. That is exactly what prompt evaluation does for prompts.

| Test kitchen | Prompt eval |
|--------------|-------------|
| Initial recipe | Draft prompt |
| Panel of tasters | Eval dataset |
| Tasters try each spoonful | Feed through Claude |
| Tasters score 1–10 on rubric | Feed through grader |
| Chef tweaks recipe, re-scores | Iterate prompt and repeat |

The dataset is the panel. The grader is the rubric. The prompt is the recipe. Keep the panel and rubric fixed; only change the recipe. That's how you isolate "what worked."

---

## The Five Steps — PM Cheat Sheet

| Step | What it produces | PM value |
|------|------------------|---------|
| 1. Draft a prompt | A baseline version | Something measurable to improve |
| 2. Create a dataset | N realistic inputs | Defines what "quality" means for this feature |
| 3. Feed through Claude | N raw outputs | Evidence of current behavior |
| 4. Feed through grader | A numeric score (1–10 per case; averaged) | The quality metric you can put in launch doc |
| 5. Iterate | A new prompt + new score | Proof the team is actually improving the product |

The number the grader spits out is the thing you will argue with finance, marketing, and execs about. Without step 4, there is no number, so there is no argument, so there is no prioritization.

---

## The Lesson's Worked Example (Why It Matters)

The lesson uses a toy dataset of three questions and shows that changing one line of the prompt moved the average score from **7.66 to 8.7**. That's the entire point in miniature:

- Before: "is this better?" → opinion.
- After: "the average score went from 7.66 to 8.7" → fact.

You can now update the launch doc, the OKR dashboard, and the engineering roadmap with a real delta. That number is what makes prompt work legible to the rest of the org.

---

## Product Use Cases

### When to Run the Full Workflow

| Scenario | Why the full loop is non-negotiable |
|----------|------------------------------------|
| Evaluating whether to ship a new prompt version to GA | You need a before/after number for the launch review |
| Comparing two competing prompts from different engineers | The score breaks the tie objectively |
| Deciding whether to downgrade from Sonnet to Haiku for cost savings | The score tells you how much quality you're giving up |
| CI regression check on a prompt-backed feature | The number is the regression signal |

### When a Lighter Approach Is OK

| Scenario | Caveat |
|----------|--------|
| Exploratory prototyping before product is greenlit | Still a trap — document any "it looks fine" decisions |
| Quick internal demo to leadership | OK, but do not promote to customers on this basis |

---

## PM Decision Framework

When the engineering team tells you a new prompt version is ready, walk through these four questions:

| Question | What a good answer looks like |
|----------|------------------------------|
| What's the baseline score for the current prompt? | A number, on a 1–10 scale, from a fixed dataset |
| What's the new score for the proposed prompt? | A number, from the **same** dataset, same grader |
| Did the dataset change since the last run? | No — if yes, the comparison is invalid |
| Is the lift big enough to justify the launch? | Subjective, but at least the conversation is about a number |

If any answer is "we didn't do that," push back. The team is asking you to ship opinion, not measured improvement.

---

## Common PM Mistakes

1. **Accepting "we tested it and it's better"** — always ask for the baseline number and the new number.
2. **Letting the team change the dataset silently between runs** — this destroys comparability and invalidates any claimed improvement.
3. **Treating the grader as "too technical to care about"** — the grader *is* your quality definition; a PM who doesn't own it is handing off product judgment.
4. **Celebrating a small score bump as "shipped"** — the first improvement is rarely the best; push for continued iteration until the score plateaus.
5. **Forgetting to put the score in the launch doc** — if you don't write the number down, the org forgets what "good" meant.

---

> **Key Insight**
>
> The five-step workflow converts prompt engineering from "trust us" into "look at the number." For the CCA exam, any question about process, reproducibility, or iteration in D3 is answered by naming the five steps in order and emphasizing that the dataset is held constant. For PMs, this is the mechanism that lets you hold engineering accountable for AI quality without having to be a prompt engineer yourself.

---

## CCA Exam Relevance

- **D3 (Evaluation & Iteration)**: the five-step loop is THE canonical workflow. Expect exam questions that list steps out of order and ask for the correct sequence.
- **D5 (Enterprise Deployment)**: the loop is the gate between "engineering thinks it's ready" and "launch."
- Watch for exam scenarios where the dataset changes mid-experiment — the correct answer is always that the dataset must remain fixed.

---

## Flashcards

| Front | Back |
|-------|------|
| What are the five steps of a typical prompt eval workflow, in order? | Draft prompt → create dataset → feed through Claude → feed through grader → iterate. |
| What does the grader produce? | A numeric score, typically on a 1-10 scale, where 10 is a perfect answer. |
| Why must the dataset stay fixed across iterations? | So that score differences can be attributed to the prompt change, not to a change in inputs. |
| What concrete delta does the lesson demonstrate? | Average score rose from 7.66 to 8.7 after adding "Answer the question with ample detail" to the prompt. |
| What is the PM-level test kitchen analogy for the dataset? | The panel of tasters — kept constant so that changes in score only reflect changes in the recipe (prompt). |
| What should a PM ask before approving a new prompt version? | Baseline score, new score, dataset unchanged, and whether the lift justifies the launch. |
| What is the risk of changing the dataset between two eval runs? | Comparability is destroyed — you cannot tell if the score change came from the prompt or from the inputs. |
| Which CCA domain tests this workflow most directly? | D3 Evaluation & Iteration — the five-step sequence is the most testable concept in this chapter. |
