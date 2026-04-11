# Running the Eval — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation & Iteration (20%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 3.3 (eval execution), 3.1 (eval design), 3.2 (test datasets) |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 20 |

---

## One-Liner

The core eval pipeline is three small functions — `run_prompt`, `run_test_case`, `run_eval` — that take a dataset, push every entry through Claude, and emit a structured result list ready for grading.

---

## Three-Function Architecture

The lesson organizes the eval runner as three composable functions with clear separation of responsibilities:

```
┌─────────────────────┐
│     run_eval        │  ← loads dataset, loops over cases
│  (dataset)          │
└──────────┬──────────┘
           │ for each test_case
           ▼
┌─────────────────────┐
│   run_test_case     │  ← orchestrates prompt + grader
│  (test_case)        │
└──────────┬──────────┘
           │ calls
           ▼
┌─────────────────────┐
│    run_prompt       │  ← merges template and input, calls Claude
│  (test_case)        │
└─────────────────────┘
```

Each function does exactly one thing. This is deliberate — as the eval grows more sophisticated (parallel execution, retries, model-based grading), you modify one function at a time without rewriting the whole pipeline.

---

## Function 1: `run_prompt`

The lowest-level function handles a single prompt execution:

```python
def run_prompt(test_case):
    """Merges the prompt and test case input, then returns the result"""
    prompt = f"""
Please solve the following task:

{test_case["task"]}
"""

    messages = []
    add_user_message(messages, prompt)
    output = chat(messages)
    return output
```

Note the current state of the prompt — it is deliberately minimal. No formatting instructions, no output constraints. The lesson says: *"Right now, we're keeping the prompt extremely simple. We're not including any formatting instructions, so Claude will likely return more verbose output than we need. We'll refine this later as we iterate on our prompt design."*

That verbose-output baseline is the entire point — it is what you will measure against as you add structure in later lessons.

---

## Function 2: `run_test_case`

The middle layer orchestrates running a single test case and grading its result:

```python
def run_test_case(test_case):
    """Calls run_prompt, then grades the result"""
    output = run_prompt(test_case)

    # TODO - Grading
    score = 10

    return {
        "output": output,
        "test_case": test_case,
        "score": score
    }
```

Two important observations:

1. **Score is hardcoded to 10.** This is a deliberate placeholder. The grading logic ships in lessons 21 (model-based grading) and 22 (code-based grading). Hardcoding 10 lets you run the end-to-end pipeline before the grader is ready — a classic "walking skeleton" technique.
2. **The return shape is a tight contract.** Every result carries `output`, `test_case`, and `score`. Downstream consumers (report generation, regression detection, dashboards) rely on this shape.

---

## Function 3: `run_eval`

The top-level function drives the whole loop:

```python
def run_eval(dataset):
    """Loads the dataset and calls run_test_case with each case"""
    results = []

    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    return results
```

This is intentionally trivial. It loops, calls `run_test_case`, collects results. Later chapters will upgrade it for parallel execution, but the synchronous version is enough to demonstrate the pattern.

---

## Driving the Pipeline

Loading and running the full eval is a five-line script:

```python
with open("dataset.json", "r") as f:
    dataset = json.load(f)

results = run_eval(dataset)
```

The dataset you persisted in Lesson 19 is picked up by `json.load`, handed to `run_eval`, and comes back as a list of result dicts.

**Timing note:** the lesson warns that even with Haiku, a full dataset can take around 30 seconds the first time you run it. At production scale (hundreds or thousands of entries), this becomes the first bottleneck and motivates parallelization.

---

## Result Shape

Each result dict contains three keys:

| Key | Contents | Purpose |
|-----|----------|---------|
| `output` | The complete text response from Claude | What you are scoring |
| `test_case` | The original test case (the `task` dict) | Context for graders and reports |
| `score` | Numeric score (hardcoded 10 for now) | The quality metric |

To inspect results:

```python
print(json.dumps(results, indent=2))
```

The lesson notes that outputs are "quite verbose" because the prompt has no formatting instructions — this is the baseline condition the rest of the chapter improves against.

---

## What You Have Built vs. What Is Missing

The lesson is explicit: *"you've just built the majority of what an eval pipeline actually does."* The skeleton works — dataset in, results out. What remains is three layers of sophistication:

| Dimension | Current state | Coming later |
|-----------|---------------|--------------|
| Grading | Hardcoded 10 | Lessons 21 (model-based) and 22 (code-based) |
| Prompt quality | Verbose baseline | Iterated against eval scores |
| Performance | Sequential, ~30s | Parallel batching |

The key insight is that the *pipeline* is simple — the complexity lives in the details of each stage, not in how the stages connect.

---

## Why This Minimal Pipeline Is the Right Starting Point

A "walking skeleton" has three properties that a fully-featured runner does not:

1. **End-to-end proof** — you can demonstrate the whole loop works before any grader is implemented, catching integration bugs early.
2. **Isolated upgrades** — you can replace the hardcoded grader with a real one without touching `run_prompt` or `run_eval`.
3. **Stable contract** — downstream tooling (dashboards, regression CI, report generation) can rely on the result shape from day one.

This is exactly the pattern you want for production AI systems: ship the trivial pipeline first, then replace each function with its sophisticated version as the product matures.

---

## Common Mistakes

1. **Skipping the walking skeleton** — trying to build grader, parallelism, and dashboards in one pass leads to debugging hell.
2. **Mixing grading into `run_prompt`** — the separation of concerns is what lets you upgrade the grader independently.
3. **Not persisting `results`** — in production you want the results saved to disk so you can diff them across runs.
4. **Synchronous loops at production scale** — fine for 3 entries, fatal for 3,000; plan for `asyncio` or thread pools early.
5. **Forgetting to fix the grader placeholder** — shipping `score = 10` to CI would make the eval meaningless; this is for learning only.

---

> **Key Insight**
>
> The power of the three-function architecture is not complexity — it is the separation of concerns. `run_prompt` owns Claude calls, `run_test_case` owns scoring, `run_eval` owns iteration. Each function is independently replaceable, which is exactly what you need as you move from a notebook demo to a production eval pipeline. For the CCA exam, the structured result shape (`output` / `test_case` / `score`) is a testable detail of D3 task 3.3.

---

## CCA Exam Relevance

- **D3 (Evaluation & Iteration)**: know the three-function decomposition and the fixed result shape; understand that a hardcoded grader is a stepping stone, not an endpoint.
- **D5 (Enterprise Deployment)**: this pipeline is the operational substrate for every production prompt eval; recognize that the walking-skeleton pattern scales to real systems by replacing functions one at a time.
- Exam trigger: any question about "how do you actually run an eval over a dataset" points at the `run_eval → run_test_case → run_prompt` layering.

---

## Flashcards

| Front | Back |
|-------|------|
| What are the three functions in the eval runner, from outer to inner? | `run_eval` (loops over dataset) → `run_test_case` (orchestrates prompt + grader) → `run_prompt` (calls Claude). |
| What does `run_prompt` do? | Merges the prompt template with a test case's `task` input, sends it to Claude via `chat()`, and returns the output text. |
| What does `run_test_case` return? | A dict with three keys: `output` (Claude's response), `test_case` (the original input), and `score` (numeric score, hardcoded 10 for now). |
| Why is the grading score hardcoded to 10 in this lesson? | To keep the walking-skeleton pipeline runnable before the real grader (lessons 21–22) is implemented. |
| How is the dataset loaded at runtime? | `with open("dataset.json", "r") as f: dataset = json.load(f)` — the file produced in Lesson 19. |
| What is the approximate runtime of the first eval run with Haiku? | Around 30 seconds for a full (small) dataset, per the lesson. |
| Why does the baseline prompt produce verbose outputs? | Because it has no formatting instructions — this is intentional so that prompt iteration can later demonstrate measurable improvement. |
| What is the "walking skeleton" pattern this lesson demonstrates? | Build the full pipeline with placeholder implementations first, then replace each function with its production version without changing the contract. |
