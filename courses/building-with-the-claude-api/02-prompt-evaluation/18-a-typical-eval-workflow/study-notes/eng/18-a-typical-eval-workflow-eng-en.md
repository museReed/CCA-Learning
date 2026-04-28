# A Typical Eval Workflow — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation & Iteration (20%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 3.1 (eval design), 3.2 (test datasets), 3.3 (eval execution) |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 18 |

---

## One-Liner

A prompt evaluation workflow is a five-step loop — draft, dataset, run, grade, iterate — that turns subjective prompt engineering into a measurable, reproducible process you can actually put under CI.

---

## The Five-Step Workflow

The lesson defines the minimal viable eval workflow. Every open-source and paid eval tool on the market is essentially a more sophisticated implementation of these same five steps.

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ 1. Draft     │ → │ 2. Dataset   │ → │ 3. Run       │ → │ 4. Grade     │ → │ 5. Iterate   │
│   a prompt   │   │              │   │  through     │   │  outputs     │   │  prompt      │
│              │   │              │   │  Claude      │   │              │   │              │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
        ▲                                                                             │
        └─────────────────────────────────────────────────────────────────────────────┘
                                   loop until score plateaus
```

---

## Step 1: Draft a Prompt

Start with whatever prompt you would have written anyway. The lesson uses a deliberately minimal baseline:

```python
prompt = f"""
Please answer the user's question:

{question}
"""
```

The value of the baseline is not that it is good — it is that it is *measurable*. A baseline lets you prove that your later iterations are actually improvements.

---

## Step 2: Create an Eval Dataset

Your dataset is a collection of sample inputs that represent the kinds of questions or requests your prompt will handle in production. Each entry is a slot that will be interpolated into the prompt template.

The lesson uses three questions:

- "What's 2+2?"
- "How do I make oatmeal?"
- "How far away is the Moon?"

In production you may have tens, hundreds, or thousands of records. You can either:
- assemble them by hand (high-fidelity, low-throughput), or
- use Claude itself to generate them (lower-fidelity, high-throughput — covered in Lesson 19).

The important property is that the dataset **reflects the real input distribution** your prompt will see, not just the happy path.

---

## Step 3: Feed Through Claude

For each dataset entry, interpolate it into the template and send the fully-formed prompt to Claude. Example for the first question:

```
Please answer the user's question:
What's 2+2?
```

Claude produces a response — something like "2 + 2 = 4" for the math question, cooking instructions for oatmeal, and a distance figure for the Moon. This is the raw output that the grader will score.

The implementation in Lesson 20 will wrap this in a `run_prompt(test_case)` function.

---

## Step 4: Feed Through a Grader

The grader is the critical component that makes this loop an engineering process rather than an opinion. It inspects both the original input and Claude's output and emits a numeric score — the lesson uses a **1-to-10 scale** where 10 is a perfect answer.

Example scores from the lesson:

| Test case | Grader score |
|-----------|--------------|
| Math: "What's 2+2?" | 10 (perfect) |
| Oatmeal: "How do I make oatmeal?" | 4 (needs improvement) |
| Moon: "How far away is the Moon?" | 9 (very good) |

Aggregate score: `(10 + 4 + 9) / 3 = 7.66`.

The grader itself can be code-based (regex, JSON schema check, etc.) or model-based (another LLM judging the output). Both are covered later in the chapter.

---

## Step 5: Change Prompt and Repeat

Now that you have a baseline score (7.66), you change something about the prompt and re-run the entire pipeline. The lesson demonstrates a simple improvement — adding a guidance line:

```python
prompt = f"""
Please answer the user's question:

{question}

Answer the question with ample detail
"""
```

Running the same dataset through this v2 prompt yields a new average: **8.7**. Because the delta is numeric, there is no debate — v2 is objectively better on this dataset.

You keep iterating until the score plateaus, or until it is good enough for production.

---

## Why This Workflow Matters

The workflow delivers three capabilities that ad-hoc testing cannot:

1. **Numeric comparison of prompt versions** — you pick the higher score, not the one that "feels" better.
2. **Best-version selection** — you can ship the objectively highest-scoring prompt, not a lucky one.
3. **Continuous iteration** — every new change is measured against the same dataset, creating a regression safety net.

The workflow "removes guesswork from prompt engineering" and gives you confidence that changes are actually improvements rather than just different variations.

---

## Scaling Considerations (Beyond the Lesson)

The five steps are minimal. Real production eval pipelines layer on:

- **Versioned datasets** — each dataset revision is checkpointed so you can reproduce old scores.
- **Parallel execution** — datasets of thousands of entries benefit from concurrent API calls.
- **CI integration** — the pipeline runs on every PR that touches a prompt, blocking regressions.
- **Multiple graders** — a single score hides dimensional trade-offs; production uses several rubrics (correctness, format, tone).
- **Stratified sampling** — the dataset contains weighted buckets so rare categories are not drowned by common ones.

None of this changes the core loop — it just operationalizes it at scale.

---

## Common Mistakes

1. **No baseline score** — iterating without a baseline means you never know if a change is actually an improvement.
2. **Dataset that only contains happy-path examples** — the whole point of the dataset is to surface failure modes, not validate the easy wins.
3. **Eyeballing the outputs and skipping the grader** — without a numeric scorer, "iteration" is just opinion laundering.
4. **Changing prompt and dataset at the same time** — you will not know whether a score change came from the prompt or the dataset.
5. **Stopping as soon as the score ticks up** — the first improvement is rarely the best improvement; keep iterating until the score plateaus.

---

> **Key Insight**
>
> The whole power of the five-step workflow is that the dataset stays fixed while the prompt varies. This isolates the prompt as the independent variable, so every change in score can be attributed to a change in prompt. If you mutate the dataset between runs, you destroy the experiment. For the CCA exam, the canonical ordering — draft → dataset → run → grade → iterate — is the single most testable sequence in D3.

---

## CCA Exam Relevance

- **D3 (Evaluation & Iteration)**: memorize the five-step sequence; know that the baseline score exists to enable numeric comparison; understand that "feed through grader" outputs a 1-10 score.
- **D5 (Enterprise Deployment)**: recognize that this workflow is the production-readiness gate — no eval loop, no deployment.
- Exam trigger: any question that asks "what is the process for improving a prompt with objective data" is answered by this five-step loop.

---

## Flashcards

| Front | Back |
|-------|------|
| What are the five steps of a typical eval workflow? | 1) Draft a prompt, 2) Create an eval dataset, 3) Feed through Claude, 4) Feed through a grader, 5) Change prompt and repeat. |
| What scale does the lesson use for grader scores? | 1 to 10, where 10 is a perfect answer and lower scores indicate room for improvement. |
| What baseline prompt does the lesson use? | `Please answer the user's question: {question}` interpolated into an f-string. |
| How does the lesson demonstrate iteration? | By adding "Answer the question with ample detail" to the prompt, the average score rose from 7.66 to 8.7. |
| Why is the dataset held constant across iterations? | So that score differences can be attributed to the prompt change, not to a change in inputs. |
| What happens in Step 3 of the workflow? | Each dataset entry is interpolated into the prompt template and sent to Claude; the full responses become the raw material for grading. |
| What three benefits does the workflow unlock? | Numeric comparison of versions, objective best-version selection, continuous measurable iteration. |
| What are two ways to assemble an eval dataset? | By hand, or generated automatically by Claude (covered in Lesson 19). |
