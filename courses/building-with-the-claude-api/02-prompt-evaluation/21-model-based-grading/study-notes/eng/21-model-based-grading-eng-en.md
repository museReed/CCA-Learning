# Model-Based Grading — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation (20%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 3.4 (LLM-as-judge grading), 3.3 (test case execution), 5.4 (eval-driven iteration) |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 21 |

---

## One-Liner

Model-based grading uses a second Claude call as a "judge" that returns a structured quality score (1-10) plus reasoning — turning subjective output quality into an objective, trackable metric you can iterate against.

---

## The Grading Problem

When you build a prompt evaluation workflow, you need an **objective signal** about output quality. The source frames a grader as a function that takes model output and returns measurable feedback — typically a number between 1 and 10, where 10 is high quality and 1 is poor quality.

Three grader families exist:

| Grader Type | What It Does | Best For |
|-------------|--------------|----------|
| **Code grader** | Programmatic checks (length, keywords, syntax, readability) | Objective, rule-based properties |
| **Model grader** | Another AI model assesses quality via an API call | Subjective quality, instruction following, helpfulness |
| **Human grader** | People manually review and score | Nuanced judgement — but slow and tedious |

Model graders are the bridge: more flexible than code, faster and cheaper than humans.

---

## When Model Graders Shine

The source lists the subjective dimensions model graders handle well:

- Response quality
- Quality of instruction following
- Completeness
- Helpfulness
- Safety

These are all things code cannot check with a regex — they require judgement about meaning.

---

## Evaluation Criteria Come First

Before writing any grader, you must define clear criteria. The source gives a code-generation prompt example with three criteria:

- **Format** — response should return only Python, JSON, or Regex without explanation
- **Valid Syntax** — produced code should parse correctly
- **Task Following** — response should directly and accurately address the user's task

The first two map to **code graders** (cheap, deterministic). The third — Task Following — is better suited for a **model grader** because it requires understanding whether the output actually solves the user's problem.

---

## The Model Grader Function

From the source, nearly verbatim:

```python
def grade_by_model(test_case, output):
    # Create evaluation prompt
    eval_prompt = """
    You are an expert code reviewer. Evaluate this AI-generated solution.

    Task: {task}
    Solution: {solution}

    Provide your evaluation as a structured JSON object with:
    - "strengths": An array of 1-3 key strengths
    - "weaknesses": An array of 1-3 key areas for improvement
    - "reasoning": A concise explanation of your assessment
    - "score": A number between 1-10
    """

    messages = []
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")

    eval_text = chat(messages, stop_sequences=["```"])
    return json.loads(eval_text)
```

Three engineering details worth highlighting:

1. **Assistant prefill with `` ```json ``** — forces Claude to begin emitting JSON immediately, skipping any preamble.
2. **`stop_sequences=["```"]`** — cuts Claude off the moment it closes the JSON code fence, giving a clean, parseable string.
3. **Structured output** — requesting `strengths`, `weaknesses`, `reasoning` alongside `score` forces the model to justify itself. Without that context, the source notes models "tend to default to middling scores around 6."

---

## Why Strengths + Weaknesses + Reasoning Matter

This is the single most important insight from the lesson. If you ask only for a score, model graders regress to the mean (score ≈ 6). Forcing the grader to write out strengths and weaknesses *before* committing to a number acts like a mini chain-of-thought: the model has to build a case, then pick a score consistent with that case. You get:

- **Less regression to 6** — scores spread across the full range
- **Auditable grades** — when a score surprises you, the reasoning tells you why
- **Actionable signal** — weaknesses become your backlog of prompt-engineering fixes

---

## Integrating Into the Test Runner

```python
def run_test_case(test_case):
    output = run_prompt(test_case)

    # Grade the output
    model_grade = grade_by_model(test_case, output)
    score = model_grade["score"]
    reasoning = model_grade["reasoning"]

    return {
        "output": output,
        "test_case": test_case,
        "score": score,
        "reasoning": reasoning
    }
```

Each test case now returns both the raw output and an objective score-plus-justification. The reasoning field is critical — it lets a human quickly sanity-check whether the grader is trustworthy for this task.

---

## Averaging Across a Dataset

```python
from statistics import mean

def run_eval(dataset):
    results = []

    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    average_score = mean([result["score"] for result in results])
    print(f"Average score: {average_score}")

    return results
```

The average becomes the prompt's "quality metric." You change the prompt, re-run, and compare averages. The source is explicit that model graders are "somewhat capricious" — but capricious in a consistent way, so *deltas* are trustworthy even if absolute scores wobble.

---

## Common Mistakes

1. **Asking only for a score** — the grader regresses to 6. Always require strengths, weaknesses, and reasoning first.
2. **Forgetting the assistant prefill** — without `` ```json `` and a `stop_sequences=["```"]` pairing, you must parse arbitrary prose.
3. **Treating the absolute score as ground truth** — model graders are capricious. Trust *deltas* across prompt versions, not absolute numbers.
4. **Using a model grader for deterministic checks** — wasteful and slower than a code grader. Use code graders for syntax, length, and keyword checks.
5. **Not logging the reasoning field** — when a surprising score appears, you need the justification to debug.

> **Key Insight**
>
> Model graders work best when they must *argue their case* before picking a number. Force the grader to emit strengths, weaknesses, and reasoning — the score becomes a consequence of the argument, not an arbitrary guess. This single technique turns an unreliable 6-everywhere judge into an iteration-ready quality metric.

---

## CCA Exam Relevance

- **D3 (Evaluation)**: Model-based grading is the canonical LLM-as-judge pattern. Expect questions on when to use model vs. code vs. human graders and how to structure the grader prompt.
- **D5 (Enterprise Deployment)**: Automated grading underpins eval-driven prompt iteration and CI for prompts in production.
- Watch for scenarios like: "You need to measure instruction-following quality" → answer is model grader, not code grader.

---

## Flashcards

| Front | Back |
|-------|------|
| What are the three types of graders? | Code graders, model graders, and human graders. |
| What score range do graders typically return? | A number between 1 and 10, where 10 is high quality and 1 is poor quality. |
| Why request strengths/weaknesses/reasoning alongside the score? | Without this context, model graders tend to default to middling scores around 6. |
| Which grading criterion is best suited for a model grader in the code-gen example? | Task Following — because it requires flexible judgement about whether the output actually solves the user's task. |
| What two tricks clean up the grader's JSON output? | Assistant prefill with `` ```json `` and `stop_sequences=["```"]`. |
| What dimensions do model graders evaluate well? | Response quality, instruction following, completeness, helpfulness, and safety. |
| How do you turn per-test-case scores into a prompt-level metric? | Take the mean of all test case scores across the dataset. |
| Why are model graders considered "capricious but useful"? | Absolute scores wobble, but deltas across prompt versions remain a consistent baseline for tracking improvement. |
