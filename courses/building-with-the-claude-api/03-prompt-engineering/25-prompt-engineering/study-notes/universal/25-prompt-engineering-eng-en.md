# Prompt Engineering — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation & Iteration (20%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 3.1 (prompt design & iteration), 1.1 (instruction following) |
| Source | building-with-the-claude-api / 03-prompt-engineering / Lesson 25 |

---

## One-Liner

Prompt engineering is a measurable, iterative loop — write a baseline, score it with an evaluator, apply one technique at a time, and re-score — not a guessing game of clever wording.

---

## The Iterative Improvement Loop

The lesson frames prompt engineering as a disciplined cycle you repeat until the score crosses your quality bar:

1. **Set a goal** — define what the prompt must accomplish.
2. **Write an initial prompt** — a deliberately naive baseline.
3. **Evaluate the prompt** — run it against a dataset and criteria.
4. **Apply a technique** — clarity, specificity, examples, XML tags, etc.
5. **Re-evaluate** — confirm the change actually improved the score.

Steps 4 and 5 repeat. The discipline is: **one change per iteration**, so you can attribute the score delta to the technique, not to a mix of edits.

This is the same scientific-method loop used for ML model development — the prompt is the hypothesis, the eval dataset is the test set, and the score is the objective function.

---

## The Running Example: Athlete Meal Planner

The lesson uses one concrete task all the way through: generate a one-day meal plan for an athlete given height, weight, goal, and dietary restrictions. Using a single task across iterations is deliberate — it lets you compare scores meaningfully.

---

## The Evaluation Harness

A `PromptEvaluator` class drives the loop. You instantiate it with a concurrency cap:

```python
evaluator = PromptEvaluator(max_concurrent_tasks=5)
```

The course explicitly warns to start low (around 3) to avoid rate-limit errors, and raise it only if your API quota permits faster parallelism. Concurrency is an orthogonal knob to prompt quality — it affects wall-clock time, not scores.

---

## Generating the Test Dataset

Instead of hand-writing test cases, the evaluator can synthesize them from a task description and an input spec:

```python
dataset = evaluator.generate_dataset(
    task_description="Write a compact, concise 1 day meal plan for a single athlete",
    prompt_inputs_spec={
        "height": "Athlete's height in cm",
        "weight": "Athlete's weight in kg",
        "goal": "Goal of the athlete",
        "restrictions": "Dietary restrictions of the athlete"
    },
    output_file="dataset.json",
    num_cases=3
)
```

Critical guidance from the lesson: **keep `num_cases` small (2-3) during iteration**. You are optimizing iteration speed, not statistical rigor. Bump the count only for a final validation run.

---

## The Baseline Prompt

A deliberately weak baseline is the whole point — you need something bad to measure improvement against:

```python
def run_prompt(prompt_inputs):
    prompt = f"""
What should this person eat?

- Height: {prompt_inputs["height"]}
- Weight: {prompt_inputs["weight"]}
- Goal: {prompt_inputs["goal"]}
- Dietary restrictions: {prompt_inputs["restrictions"]}
"""
    messages = []
    add_user_message(messages, prompt)
    return chat(messages)
```

"What should this person eat?" is a question, not an instruction. It gives Claude no target for length, format, nutritional detail, or timing. A typical first score is around **2.3 / 10**, which the lesson explicitly calls normal.

---

## Running the Evaluation with Extra Criteria

Beyond the dataset, you can inject domain-specific grading criteria so the judge model scores against what actually matters:

```python
results = evaluator.run_evaluation(
    run_prompt_function=run_prompt,
    dataset_file="dataset.json",
    extra_criteria="""
The output should include:
- Daily caloric total
- Macronutrient breakdown
- Meals with exact foods, portions, and timing
"""
)
```

`extra_criteria` is your rubric. Without it, the judge invents a generic "is this a reasonable meal plan?" scale. With it, the score reflects whether your prompt hits the business requirements.

---

## Reading the Results

The evaluator returns two artifacts: a numerical score and a detailed HTML report. The report shows per-case model output plus the grader's reasoning — this is where you learn *why* a case failed, not just *that* it did. That "why" is the raw material for the next iteration.

---

## Why One Change Per Iteration

If you apply clarity + specificity + examples + XML structure in a single edit and the score jumps from 2.3 to 6.8, you cannot attribute the gain. Next time you face a new prompt you will not know which technique to reach for. Single-technique iterations build a personal playbook of which moves matter for which tasks.

---

## Common Mistakes

1. **No baseline** — jumping straight to a "good" prompt leaves you with no score to improve against.
2. **Multi-change iterations** — changing several things at once obscures which technique drove the improvement.
3. **Too many test cases too early** — slows iteration and burns API quota before the prompt is worth validating at scale.
4. **Ignoring the judge's reasoning** — looking only at the numeric score wastes the most valuable signal in the report.
5. **Missing `extra_criteria`** — the default rubric often doesn't reflect your actual requirements, so the score is noise.

> **Key Insight**
>
> Prompt engineering is not "write a better prompt." It is **instrument a loop**: baseline, score, change one thing, re-score. The evaluator is the microscope; without it you're guessing. A 2.3/10 first attempt is normal — the metric to watch is the delta per iteration, not the absolute starting score.

---

## CCA Exam Relevance

- **D3 (Evaluation & Iteration)**: recognize the baseline → eval → iterate cycle as the canonical prompt improvement pattern.
- **D1 (Agentic Architecture)**: prompts are how you steer agent behavior; the iteration loop applies identically when tuning an agent's system prompt.
- Expect questions framed as: "The team has a prompt scoring 2.3/10, what do they do next?" → answer is never "rewrite from scratch," it is "apply one technique and re-evaluate."
- Know that `max_concurrent_tasks` is a rate-limit knob, not a quality knob.

---

## Flashcards

| Front | Back |
|-------|------|
| What are the five steps of the prompt engineering loop? | 1) Set goal, 2) Write initial prompt, 3) Evaluate, 4) Apply technique, 5) Re-evaluate. Repeat 4-5 until satisfied. |
| Why change only one thing per iteration? | So the score delta is attributable to that specific technique, building a reliable mental model of what works. |
| What is a typical score for a first-attempt prompt? | Around 2.3/10 — the lesson says low initial scores are normal and not a reason to be discouraged. |
| Why keep the test dataset small (2-3 cases) during iteration? | Iteration speed. Small datasets let you test many techniques quickly; you scale up only for final validation. |
| What does `max_concurrent_tasks` control? | Parallelism of API calls in the evaluator. Start low (around 3) to avoid rate-limit errors; raise only if quota allows. |
| What is the purpose of `extra_criteria` in `run_evaluation`? | It tells the grading model which domain-specific qualities to score against, aligning the score with actual requirements. |
| What two artifacts does an evaluation run produce? | A numerical score and a detailed HTML report showing per-case outputs and the grader's reasoning. |
| Why use a deliberately weak baseline prompt? | Because you need a measurable starting point — improvement is only visible as a delta from the baseline. |
