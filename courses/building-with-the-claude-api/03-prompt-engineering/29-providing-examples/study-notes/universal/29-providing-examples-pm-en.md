# Providing Examples — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation & Iteration (20%) — primary; D2 — Tool Design (18%) — secondary |
| Task Statements | 3.1 (prompt design for reliability), 2.2 (structured content blocks) |
| Source | building-with-the-claude-api / 03-prompt-engineering / Lesson 29 |

---

## One-Liner

Showing Claude a few examples of the outcome you want is the closest thing to "training" you can do from a PM seat — it turns vague quality bars into reproducible behavior, and it directly consumes your eval data as fuel.

---

## Why PMs Should Care About Examples

Every PM has had this conversation: "The output is kind of right but it's not quite our voice," or "It handles the easy cases but fails on the tricky ones." Describing "our voice" or "the tricky cases" in words is genuinely hard. Showing the AI 2–4 examples is often faster and more reliable than iterating on prose instructions for a week.

The course lesson is explicit: few-shot prompting is "one of the most effective prompt engineering techniques you'll use." It is also the technique with the tightest feedback loop to evals — your best eval outputs literally become the next prompt's examples.

---

## Mental Model: The Style Guide with Worked Examples

Think of how a design system or brand voice doc actually works. The text rules matter (tone: confident but warm; use active voice), but the worked examples are what the team actually copies:

| Without examples | With examples |
|------------------|---------------|
| "Be concise" | "Not this: 'We are pleased to announce…' — this: 'New today:'" |
| "Be empathetic" | Shows a refund email side-by-side with a bad version |
| "Follow our format" | Ships a filled-in template next to a blank one |

Few-shot prompts do the same thing for Claude. Instead of arguing over the definition of "concise" in a PRD, you put the good example and the bad example inside the prompt. The AI reads them every time.

---

## Product Use Cases

### When Examples Are the Right Move

| Scenario | Why Examples Work |
|----------|------------------|
| Sentiment analysis with sarcasm | Sarcasm is too context-dependent to describe in prose — one example makes it obvious |
| Specific JSON or schema output | Showing a filled-in example beats listing field rules |
| Matching brand voice | A single on-brand example beats a paragraph of style guidance |
| Extracting structured info from messy text | Examples make the output shape unambiguous |
| Any task where you already have "gold" outputs from eval | Promote those outputs into the prompt as examples |

### When Examples Are Overkill

| Scenario | Better Alternative |
|----------|--------------------|
| Very simple transformations | A clear instruction is enough |
| Highly variable creative output | Examples can over-constrain the model |
| Tasks with no "right answer" | Examples suggest a single correct path that may not exist |

---

## The Four Product Benefits

1. **Consistency on edge cases** — the places where your feature is most likely to embarrass you (sarcasm, corner cases, ambiguous inputs) are exactly where examples shine.
2. **Tighter quality bar** — instead of writing "be high quality" in the prompt, you show Claude three high-quality outputs. The bar becomes concrete.
3. **Eval-driven improvement** — your eval harness produces the raw material for the next prompt version. Shipping high-scoring eval outputs back into the prompt is a free quality upgrade.
4. **Fewer prose instructions** — complex rules that were hard to describe in English can be replaced by a handful of examples, which are easier to review and revise.

---

## The Eval-to-Example Loop

This is the single most important PM takeaway from Lesson 29:

1. Run the current prompt through your eval set
2. Identify the outputs that scored highest (perfect or near-perfect)
3. Paste those input/output pairs into the prompt as few-shot examples
4. Re-run the eval — the hard cases should improve because Claude now has "gold" reference behavior

This is why Chapter 03 (Prompt Engineering) and the evaluation chapter are tied together. PMs who think of prompts as static strings miss the loop; PMs who treat evals as the feedstock for prompt updates get compounding improvements.

---

## PM Decision Framework

When reviewing a prompt template, ask:

| Question | If Yes | Action |
|----------|--------|--------|
| Does the task have corner cases that are hard to describe? | Yes | Add examples covering those cases |
| Does the task require a specific output shape? | Yes | Show at least one fully-formed example |
| Do you already have high-scoring eval outputs for this task? | Yes | Promote them into the prompt |
| Is the style / tone / voice hard to pin down in writing? | Yes | Show an ideal example, not a rule |
| Is the task simple and succeeding without examples? | Yes | Don't add them |

---

## Common PM Mistakes

1. **Treating examples as "engineer's business"** — examples encode product decisions (tone, edge-case handling). PMs should own which examples go into the prompt.
2. **Cherry-picking only pretty examples** — the whole value of few-shot is covering your failure modes. Don't just show cases where Claude already wins.
3. **Letting examples go stale** — the eval set evolves; the few-shot examples should evolve with it. Build the update into the feature's maintenance rhythm.
4. **Missing the "why this is good" annotation** — a one-line rationale after each ideal output helps Claude generalize. PMs often forget this because it looks like documentation, not prompt.
5. **Not using XML tags to wrap examples** — without structure, Claude may confuse example inputs with the real task. PMs should insist on `<sample_input>` / `<ideal_output>` framing.

> **Key Insight**
>
> For PMs, few-shot prompting is the shortest path from "we have an eval that measures quality" to "we have a prompt that hits that quality bar." Your highest-scoring eval outputs become the next prompt's examples. This is the loop the CCA exam is testing when it asks about iterating on prompt reliability — and it is the loop PMs can drive without writing code.

---

## CCA Exam Relevance

- **D3 (Evaluation & Iteration)**: few-shot is the canonical move when evals show failures on specific cases. The "promote high-scoring outputs into the prompt" pattern is directly testable.
- **D2 (Tool Design)**: examples work hand-in-hand with XML-tagged content blocks and strict output formats.
- Watch for exam scenarios like "Claude fails on sarcasm," "output format varies between calls," or "we have eval scores but the prompt is not improving" — all point to few-shot examples.

---

## Flashcards

| Front | Back |
|-------|------|
| In one sentence, what is few-shot prompting? | Showing Claude sample input/output pairs in the prompt to guide its responses. |
| What is the PM-level benefit of showing examples instead of writing rules? | It replaces hard-to-describe quality bars (tone, edge cases) with concrete demonstrations Claude can copy and generalize from. |
| Where should a PM source good examples for a prompt? | From the highest-scoring outputs in the feature's eval set. |
| What is the eval-to-example loop? | Run eval → find highest-scoring outputs → paste them into the prompt as examples → re-run eval. |
| Why should each ideal example include a short "why this is good" note? | So Claude learns the criteria, not just the surface form — helps with generalization. |
| When should a PM NOT push for more examples? | When the task is simple and already passing evals, or when creativity would be over-constrained. |
| What XML tags does the lesson recommend for examples? | `<sample_input>` and `<ideal_output>`. |
| Which lesson does Lesson 29 directly build on? | Lesson 28 (XML tags) — examples live inside XML-tagged structures. |
