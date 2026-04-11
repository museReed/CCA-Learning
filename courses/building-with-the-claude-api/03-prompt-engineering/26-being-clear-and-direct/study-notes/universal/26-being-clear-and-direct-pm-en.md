# Being Clear and Direct — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation & Iteration (20%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 3.1 (prompt design & iteration), 1.1 (instruction following) |
| Source | building-with-the-claude-api / 03-prompt-engineering / Lesson 26 |

---

## One-Liner

Write prompts the way you write a design brief — start with an imperative verb and a concrete deliverable, not a polite question.

---

## Why PMs Should Care

The first line of a prompt is like the first line of a PRD or a design brief. If the engineer or designer can't tell from sentence one what they're supposed to produce, the rest of the document is damage control. The same is true for Claude. This lesson shows that the single most leveraged prompt edit — rewriting the first line from question to imperative — delivered a measurable score jump (2.32 → 3.92 on a 10-point eval). That is a larger product quality delta than most A/B tests will ever show, and it comes from editing one sentence.

---

## Mental Model: The Design Brief

Compare how a weak vs strong brief lands with a designer:

| Brief Style | Designer Reaction | Claude Reaction |
|-------------|-------------------|-----------------|
| "We were thinking about maybe revisiting the onboarding flow, it feels off?" | "OK... what do you actually want?" | Produces a vague response asking for clarification or guessing scope |
| "Redesign the onboarding flow to reduce drop-off at step 2. Deliverable: 3 Figma frames by Friday." | "Got it, starting now." | Produces a structured artifact matching the ask |

Prompts are briefs. Claude is the collaborator. Briefs that open with a verb and a deliverable always outperform briefs that open with context or a question.

---

## The Two Principles in Product Language

| Principle | Definition | PM Translation |
|-----------|------------|----------------|
| **Clarity** | Simple language, no ambiguity about what you want | The user story — "As a X, I want Y so that Z" — no one has to guess |
| **Directness** | Instructions not questions, start with action verbs | The acceptance criteria — "Given / When / Then" — imperative, testable |

If a PM is used to writing Jira tickets well, they already know how to write clear and direct prompts. The skills transfer.

---

## Product Use Cases

### Where Clarity + Directness Is the First Fix

| Feature | Symptom | Fix |
|---------|---------|-----|
| AI summarizer produces inconsistent lengths | The prompt asks "Can you summarize this?" | Rewrite: "Write a 3-sentence summary covering the main argument, supporting evidence, and conclusion." |
| AI writing assistant is too chatty | Prompt opens with a question | Rewrite as an imperative: "Draft a professional email declining the meeting." |
| Internal doc extractor misses fields | Prompt says "Tell me about the contract" | Rewrite: "Extract the effective date, party names, and total value from the contract." |

### Where It's Not Enough

Clarity and directness alone cap out — the lesson only reaches 3.92/10. To go further you need specificity (Lesson 27), examples, and structure. Think of clear+direct as the **minimum viable prompt**, not the final product.

---

## PM Decision Framework

When reviewing a team's AI prompt during a PRD review, ask:

| Question | If No, Flag It |
|----------|---------------|
| Does the first line start with a verb? | Flag — rewrite as imperative |
| Can I tell what Claude will produce from just the first sentence? | Flag — the brief is unclear |
| Are there any hedge words ("maybe," "if possible," "could you")? | Flag — remove them |
| Does the prompt specify the output format or length? | Flag — add constraints |
| Would a new team member understand the first line without context? | Flag — simplify the wording |

This is essentially a PRD lint pass applied to prompts.

---

## The Hidden Product Win

Clear + direct prompts don't just score higher — they fail more predictably. A vague prompt can fail in a hundred different ways (too long, too short, wrong topic, wrong format, chatty, off-brand). An imperative prompt fails in one: the requested artifact is wrong in a specific, debuggable way.

Predictable failure is a product asset. It means your QA can write targeted tests, your on-call can recognize the shape of the bug, and your eval rubric can keep pace.

---

## Common PM Mistakes

1. **Polite prompts** — "Could you please kindly..." PMs often write AI prompts like emails to strangers. Claude doesn't need politeness; it needs clarity.
2. **Front-loading context** — burying the instruction behind three sentences of background information. Instruction first, context second.
3. **Asking instead of telling** — treating Claude as if it might refuse. It won't; give it an imperative.
4. **Skipping this fix because it "feels too simple"** — the lesson's measured win is +1.6 on a 10-point scale from a one-line edit. Do not skip simple wins.
5. **Calling "clear + direct" done** — it's the floor, not the ceiling. You still need specificity and examples on top.

> **Key Insight**
>
> The cheapest product quality win in AI features is rewriting the first line of every prompt as a verb-led imperative. It costs zero engineering hours, produces a measurable score improvement, and transforms how predictably the feature fails. Every PM reviewing an AI prompt should audit the first line first.

---

## CCA Exam Relevance

- **D3 (Evaluation & Iteration)**: know "convert question → imperative" as the cheapest first step in the prompt-improvement loop.
- **D1 (Agentic Architecture)**: the same rule applies to agent system prompts — lead with the imperative, not the preamble.
- Exam scenarios that show a weak prompt will usually have a rewritten imperative version as the correct answer.

---

## Flashcards

| Front | Back |
|-------|------|
| What part of a prompt should PMs audit first? | The first line — it sets the stage and determines response quality more than any other part. |
| What PM artifact is analogous to a clear-and-direct prompt? | A good design brief or Jira ticket — starts with a verb and a concrete deliverable, no hedging. |
| What score improvement did the lesson measure from clarity + directness alone? | 2.32 → 3.92 on the meal-planner eval — a +1.6 point absolute gain from one rewrite. |
| Why is a vague prompt a product risk beyond quality? | Because it fails unpredictably — failures can't be debugged, tested against, or anticipated. |
| What's the "design brief" analogy? | A vague brief leaves the designer guessing; a verb-led brief with a deliverable enables immediate execution. Claude behaves the same. |
| List three hedge words PMs should strip from prompts. | "Maybe," "if possible," "could you" — any word that makes the instruction feel optional. |
| Is "clear and direct" sufficient on its own? | No — it's the floor. You still need specificity, examples, and structure to reach high eval scores. |
