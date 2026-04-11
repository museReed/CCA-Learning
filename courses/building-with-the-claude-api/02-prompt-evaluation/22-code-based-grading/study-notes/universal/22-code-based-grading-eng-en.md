# Code-Based Grading — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation (20%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 3.4 (deterministic scoring), 3.3 (test runner integration), 5.4 (combined eval metrics) |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 22 |

---

## One-Liner

Code-based grading runs your model's output through deterministic parsers — JSON, Python AST, regex — and returns a 10 or a 0 per test case, giving you a cheap, reliable floor for eval quality that complements the fuzzier model grader.

---

## Why Code Graders Exist

When evaluating AI models that generate code, you need more than "does the answer look right?" You need to verify that the generated code **actually has valid syntax and follows the correct format**. A model grader is too slow and too expensive for that — and it doesn't need a judgement call, it needs a parser.

Code grading validates two aspects of AI-generated responses:

| Aspect | Check |
|--------|-------|
| **Format** | The response should return only the requested code type (Python, JSON, or Regex) without explanations |
| **Valid Syntax** | The generated code should actually parse correctly as the intended language |
| **Task Following** | (handled by the model grader — not by code grading) |

The split is intentional: cheap/deterministic things go to code graders, subjective things go to model graders. Together they give a comprehensive evaluation.

---

## The Three Validators

From the source, the three syntax validators each follow the same pattern — try to parse, return 10 on success, return 0 on failure:

```python
def validate_json(text):
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
        return 0

def validate_python(text):
    try:
        ast.parse(text.strip())
        return 10
    except SyntaxError:
        return 0

def validate_regex(text):
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0
```

Three engineering points:

1. **`.strip()` first** — leading/trailing whitespace would otherwise cause false negatives on valid payloads.
2. **Binary 10-or-0 output** — keeps the scoring scale consistent with the model grader so they can be averaged later.
3. **Catch-specific exceptions** — `json.JSONDecodeError`, `SyntaxError`, `re.error`. A bare `except:` would mask bugs in the grader itself.

All three validators use the standard library — no external dependencies, no API costs, latency measured in microseconds.

---

## Dataset Format Requirement

For the code grader to know *which* validator to run, each test case must declare its expected format:

```python
{
    "task": "Create a Python function to validate an AWS IAM username",
    "format": "python"
}
```

The source recommends updating your dataset generation prompt to automatically include this `format` field in its example output structure, so new test cases always carry the hint needed for routing.

---

## Improving Prompt Clarity

Code graders also push your underlying prompt engineering to be more disciplined. To increase pass rates, the source suggests two prompt-level moves:

```
* Respond only with Python, JSON, or a plain Regex
* Do not add any comments or commentary or explanation
```

And a clever pre-fill trick — start the assistant message with a generic code fence opener that doesn't commit to a specific language:

```python
add_assistant_message(messages, "```code")
```

This tells Claude to start generating code content without forcing the runner to know in advance whether the output is Python, JSON, or Regex. The validator called later depends on the `format` field in the test case, not on an a-priori fence choice.

---

## Combining Model + Code Scores

The final step is merging the model grader score with the code grader score. The source's simple default is an unweighted average:

```python
model_grade = grade_by_model(test_case, output)
model_score = model_grade["score"]
syntax_score = grade_syntax(output, test_case)

score = (model_score + syntax_score) / 2
```

This gives equal weight to content quality (model grader) and technical correctness (code grader). The source explicitly notes you might adjust the weights based on what matters more for your specific use case — e.g., for a code-generation product, syntax correctness might carry 70% weight.

---

## The Real Value of Code Graders

The source closes with the crucial framing: the score itself isn't inherently good or bad — **what matters is whether you can improve it by refining your prompts.** Code graders give you a quantitative way to measure prompt engineering progress rather than relying on subjective assessment. They are the quantitative spine of prompt iteration.

Two practical properties to internalize:

- **Deterministic** — same input produces the same score every time. No capriciousness like model graders.
- **Cheap** — microsecond latency, no API cost. You can re-run the whole dataset on every prompt tweak.

Together these mean code graders are the first line of defense in any eval pipeline. Fail the code grader? Don't even bother calling the model grader.

---

## Common Mistakes

1. **Using only a model grader for syntax** — wastes tokens, introduces variance on a question that should be deterministic.
2. **Not calling `.strip()`** — valid payloads with surrounding whitespace fail, false negatives pollute the metric.
3. **Missing the `format` field in test cases** — the runner cannot route to the correct validator.
4. **Catching bare `Exception`** — hides bugs in the grader code itself; always catch the specific parser exception.
5. **Not averaging with the model grader** — code correctness alone is necessary but not sufficient; you also need content quality.
6. **Using the same weights forever** — different products value syntax vs. quality differently; tune the weighting.

> **Key Insight**
>
> Code graders are the cheap, deterministic spine of prompt evaluation. They cannot judge taste, but they catch every broken payload for free and in microseconds. Pair them with a model grader (for taste) and average the two — you now have a composite metric you can run on every prompt change without breaking the bank.

---

## CCA Exam Relevance

- **D3 (Evaluation)**: Code graders are the deterministic half of a hybrid eval pipeline. Expect questions on when to use code vs. model graders and how to combine their scores.
- **D5 (Enterprise Deployment)**: Deterministic scoring fits into CI/CD for prompts — cheap, fast, and reliable enough to run on every PR.
- Watch for: "You need to validate AI-generated JSON / Python / Regex" → always a code grader, never a model grader.

---

## Flashcards

| Front | Back |
|-------|------|
| What two aspects does code grading validate? | Format (only the requested code type) and Valid Syntax (actually parses). |
| What score does a successful `validate_json` return? | 10 |
| What score does a failed `validate_python` return? | 0 |
| Which Python module parses Python code for the validator? | `ast` — specifically `ast.parse(text.strip())`. |
| Which exception does `validate_regex` catch? | `re.error` |
| What field must the dataset include so the runner knows which validator to use? | `format` — with values like `"python"`, `"json"`, or `"regex"`. |
| What assistant prefill trick encourages raw-code output without committing to a language? | `` add_assistant_message(messages, "```code") `` |
| How does the source combine model grader and code grader scores? | An unweighted average: `(model_score + syntax_score) / 2`. |
| Why is the absolute code-grader score not inherently good or bad? | Because what matters is whether you can improve it by refining your prompts — it's the direction that matters, not the level. |
| What are the two main advantages of code graders over model graders? | Deterministic (same input → same score) and extremely cheap (microseconds, no API cost). |
