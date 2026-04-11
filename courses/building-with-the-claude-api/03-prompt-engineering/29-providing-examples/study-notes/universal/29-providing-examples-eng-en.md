# Providing Examples — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation & Iteration (20%) — primary; D2 — Tool Design (18%) — secondary |
| Task Statements | 3.1 (prompt design for reliability), 2.2 (structured content blocks) |
| Source | building-with-the-claude-api / 03-prompt-engineering / Lesson 29 |

---

## One-Liner

Few-shot prompting (one-shot / multi-shot) shows Claude input/output pairs instead of describing the desired behavior — the single most effective prompt engineering technique for corner cases, formats, and tone.

---

## Why Examples Beat Instructions

Instructions tell; examples show. When a task has subtleties that are hard to pin down in words — sarcasm, a specific JSON shape, a house style — demonstrating the expected behavior is more reliable than trying to describe it. The source lesson calls few-shot prompting "one of the most effective prompt engineering techniques you'll use."

The canonical failure case in the lesson is sentiment analysis with sarcasm. The tweet:

> "Yeah, sure, that was the best movie I've seen since 'Plan 9 from Outer Space'"

reads positive on the surface (best, since, sure) but is sarcastic and actually negative. No short instruction like "detect sarcasm" reliably fixes this. Showing a sarcastic example does.

---

## The Sarcasm Example, Structured

The improved prompt from the lesson contains:

- A clear positive example: `"Great game tonight!"` → `"Positive"`
- A sarcastic example: `"Oh yeah, I really needed a flight delay tonight! Excellent!"` → `"Negative"`
- Context explaining why sarcasm should be treated carefully

Critically, these examples are wrapped in XML tags: `<sample_input>` and `<ideal_output>`. This chains directly to Lesson 28 — XML tags delimit what is an example input vs. an example output vs. the real task. Few-shot without structure is a recipe for Claude guessing which piece of text is supposed to be "the answer."

```
<example>
  <sample_input>Great game tonight!</sample_input>
  <ideal_output>Positive</ideal_output>
</example>

<example>
  <sample_input>Oh yeah, I really needed a flight delay tonight! Excellent!</sample_input>
  <ideal_output>Negative</ideal_output>
</example>

Classify the following tweet. Sarcasm should be treated as negative.

<tweet>
{user_tweet}
</tweet>
```

---

## One-Shot vs Multi-Shot

Straight from the source:

- **One-shot** — a single example, enough to establish the pattern
- **Multi-shot** — multiple examples, covering different scenarios and edge cases

Use multi-shot when you need to handle various corner cases or demonstrate different types of valid responses. Rule of thumb: each example you add should "pay for itself" by covering a failure mode that the prior examples did not.

---

## When Examples Are the Right Tool

From the source, examples are particularly useful for:

- Capturing corner cases or edge scenarios (sarcasm, ambiguous inputs)
- Defining complex output formats (e.g., specific JSON structures)
- Showing the exact style or tone you want
- Demonstrating how to handle ambiguous inputs

Notice the theme: anything where "show me" is faster than "describe exactly what I want."

---

## Harvesting Examples from Evaluations

One of the most important practical points: when you run prompt evals, look at your **highest-scoring outputs** and promote them into the prompt as examples. The lesson is explicit — "Find responses that scored 10 (or your highest available score) and use those input/output pairs as examples in your prompt."

This closes a virtuous loop:

1. Run eval with current prompt
2. Find the cases where Claude already produced ideal output
3. Copy those (input, output) pairs into the prompt as few-shot examples
4. Re-run eval — scores on the hard cases should rise

This is why Lesson 29 sits inside the "prompt engineering → evaluation" flow of the chapter: examples and evals are the same iterative loop.

---

## Don't Just Show — Explain

The source emphasizes that an ideal example is paired with a reason. From the lesson:

```
<ideal_output>
[Your example output here]
</ideal_output>

This example is well-structured, provides detailed information
on food choices and quantities, and aligns with the athlete's
goals and restrictions.
```

The short annotation after the example tells Claude what makes it good, not just what it looks like. This helps generalization — Claude is learning the criteria, not just copying the surface form.

---

## Python Pattern

```python
from anthropic import Anthropic

client = Anthropic()

few_shot = """<example>
  <sample_input>Great game tonight!</sample_input>
  <ideal_output>Positive</ideal_output>
</example>

<example>
  <sample_input>Oh yeah, I really needed a flight delay tonight! Excellent!</sample_input>
  <ideal_output>Negative</ideal_output>
</example>

Sarcasm should be treated as negative."""

tweet = "Yeah, sure, that was the best movie I've seen since 'Plan 9 from Outer Space'"

prompt = f"""{few_shot}

Classify the following tweet as Positive or Negative.

<tweet>
{tweet}
</tweet>"""

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=64,
    messages=[{"role": "user", "content": prompt}],
)
```

Two things to notice: the examples live above the real task, and both the examples and the real input use XML tags.

---

## Best Practices from the Source

- Always use XML tags to structure your examples clearly
- Be explicit about what you are showing ("Here is an example input with an ideal response")
- Include examples that address your most common failure cases
- Explain why your example outputs are considered ideal
- Keep examples relevant to your specific task

---

## Common Mistakes

1. **No XML structure around examples** — Claude has to guess which string is input, which is output, and which is the real question.
2. **Cherry-picked easy examples** — demonstrating cases Claude already handles well while ignoring your real failure modes.
3. **Examples drift from the task** — using examples that are close to, but not exactly, the shape of the real input.
4. **Showing without explaining** — an ideal output without an annotation tells Claude "copy this" instead of "reason like this."
5. **Not re-harvesting after evals** — leaving examples static while the eval set evolves, so the prompt stops matching the hard cases.

> **Key Insight**
>
> Few-shot prompting is the bridge between Lesson 28 (XML structure) and Chapter 04 (tool use). On the CCA exam, expect scenario questions like "the prompt handles normal cases but fails on sarcasm / JSON formatting / a specific tone." The answer is almost always: add XML-tagged examples that cover those failure modes, ideally sourced from your highest-scoring eval outputs.

---

## CCA Exam Relevance

- **D3 (Evaluation & Iteration)**: few-shot is the primary iteration lever when evals expose a systematic failure mode. The "promote high-scoring eval outputs into examples" loop is exam-relevant.
- **D2 (Tool Design)**: when designing prompts that define strict output shapes (including JSON for tool-like behavior), examples are more reliable than prose schemas.
- Watch for exam phrases like "sarcasm," "specific format," "corner case," "style or tone" — all point to few-shot examples.

---

## Flashcards

| Front | Back |
|-------|------|
| What is few-shot prompting? | Providing sample input/output pairs in the prompt to guide Claude's responses (one-shot = 1 example, multi-shot = multiple). |
| Why do examples beat instructions for sarcasm detection? | Sarcasm is hard to describe in prose; showing a sarcastic example is more reliable than telling Claude "watch for sarcasm." |
| What XML tags does the lesson use for examples? | `<sample_input>` and `<ideal_output>` (wrapped inside an `<example>` container in practice). |
| When should you use multi-shot instead of one-shot? | When you need to cover multiple edge cases or different valid response types. |
| How do you source good examples from evaluations? | Find responses that scored highest (e.g., 10/10) and promote those input/output pairs into the prompt. |
| Why should you explain why an example is ideal? | It helps Claude learn the underlying criteria instead of only copying the surface form. |
| Name four situations where examples are especially useful. | Corner cases, complex output formats, specific style/tone, ambiguous inputs. |
| What is the relationship between Lesson 28 and Lesson 29? | XML tags (28) provide the structure; examples (29) fill that structure with demonstrations — they are designed to be used together. |
