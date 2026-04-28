# Model-Based Grading — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation (20%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 3.4 (LLM-as-judge grading), 3.3 (test case execution), 5.4 (eval-driven iteration) |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 21 |

---

## One-Liner

Model-based grading is how you turn "does this AI output feel good?" into a number on a dashboard — so prompt engineering stops being vibes and starts being a measurable product workflow.

---

## Why PMs Should Care

Without graded evals, every prompt change is a leap of faith. Someone tweaks the system prompt, eyeballs ten outputs, and ships. There is no way to answer basic product questions:

- Did this week's prompt change actually improve helpfulness?
- Did our new instructions break completeness?
- Are we regressing on safety without knowing it?

Model-based grading gives you a **quality metric per prompt version** — a single number you can chart over time, just like DAU or conversion rate. It converts prompt engineering from craft into engineering.

---

## Mental Model: The Restaurant Critic

Think of the three grader types as three different restaurant review systems:

| Grader Type | Restaurant Analogy | Strength | Weakness |
|-------------|-------------------|----------|----------|
| **Code grader** | Health inspector with a checklist | Fast, cheap, 100% consistent | Can only check rules, not taste |
| **Model grader** | Freelance food critic working by email | Judges taste, scales cheaply | Slightly different opinion each visit |
| **Human grader** | Michelin inspector visiting in person | Deepest, most nuanced verdict | Slow and expensive |

A real restaurant chain uses all three. A PM building an AI feature should too: code graders for rule compliance, model graders for quality of experience, human graders when the stakes are high (safety, legal, brand).

---

## Product Use Cases

### When to Use Model Graders

| Scenario | Why Model Graders Work |
|----------|-----------------------|
| "Is this customer service response helpful?" | Helpfulness is a judgement call code cannot make |
| "Did the AI follow the instructions we gave it?" | Instruction-following is a semantic question |
| "Is this summary complete?" | Completeness depends on meaning, not word count |
| "Does this response feel safe and on-brand?" | Tone and safety need a model's judgement |

### When NOT to Use Model Graders

| Scenario | Better Alternative |
|----------|--------------------|
| "Is the output valid JSON?" | Use a code grader — deterministic and free |
| "Is the response under 200 words?" | Use a code grader — trivial |
| "Does the answer match a known correct answer?" | Use a code grader with string comparison |
| "Does this violate our most sensitive policies?" | Use human graders for the hard cases |

---

## The One Trick Every PM Should Push For

In the source, the grader prompt asks the model for four things in order:

1. Strengths (1-3 items)
2. Weaknesses (1-3 items)
3. Reasoning (a short explanation)
4. Score (1-10)

This is the **most important design decision in the whole lesson**. Without strengths and weaknesses, the source notes, model graders default to middling scores around 6 — useless for tracking improvement.

PMs should push engineers to keep this structure even under pressure to "simplify" the grader. The strengths and weaknesses are also directly usable as PM artifacts: they become a backlog of prompt fixes, and the reasoning gives customer success and QA auditable explanations when something regresses.

---

## PM Decision Framework

When a team proposes adding model-based grading, ask:

| Question | If Yes | Action |
|----------|--------|--------|
| Do we have clear evaluation criteria written down? | Yes | Proceed — graders need criteria first |
| Is the quality dimension subjective (helpfulness, completeness)? | Yes | Model grader is the right choice |
| Is the quality dimension deterministic (valid JSON, length)? | Yes | Push for a code grader instead |
| Do we care about *absolute* scores? | No | Good — trust the *deltas*, not the absolute numbers |
| Is the reasoning field logged and reviewable? | Yes | Proceed — this is what makes grades auditable |

---

## Common PM Mistakes

1. **Treating grader scores as ground truth** — model graders are capricious. Trust deltas between prompt versions, not absolute numbers.
2. **Skipping criteria definition** — telling engineers "just grade it" produces a grader that scores everything 6. You must define the rubric first.
3. **Not budgeting for grader iteration** — the grader itself is a prompt that needs tuning. Plan cycles for it.
4. **Using model graders where code graders work** — wastes tokens and slows iteration. For rule-based checks, always prefer code graders.
5. **Not logging reasoning** — when a surprising score appears, you need the justification to debug with engineering or QA.

> **Key Insight**
>
> Model-based grading turns prompt engineering from a craft into a product workflow. The grader is not the feature — the grader is the **measurement instrument** that lets you improve the real feature with confidence. PMs who understand this ship quality improvements in weeks; PMs who skip it ship vibes and hope.

---

## CCA Exam Relevance

- **D3 (Evaluation)**: Model-based grading is the canonical LLM-as-judge pattern. Know when to pick model vs code vs human, and what the grader prompt must contain (strengths, weaknesses, reasoning, score).
- **D5 (Enterprise Deployment)**: Graders underpin eval-driven iteration — expect questions framed around measuring prompt improvements in production.
- Watch for: "You need to measure helpfulness / instruction following / completeness" → model grader.

---

## Flashcards

| Front | Back |
|-------|------|
| What product problem does model-based grading solve? | Turning subjective AI output quality into a number PMs can chart and iterate against. |
| What are the three grader types? | Code graders, model graders, human graders. |
| When should a PM choose a model grader over a code grader? | When the quality dimension is subjective — helpfulness, completeness, instruction following, safety. |
| Why must a model grader return strengths and weaknesses, not just a score? | Without them, the model regresses to middling scores around 6 and the metric becomes useless. |
| What is the restaurant analogy for the three grader types? | Health inspector (code), freelance food critic (model), Michelin inspector (human). |
| Which score should PMs trust — absolute or delta? | Deltas between prompt versions — model graders are capricious on absolutes. |
| What dimensions do model graders handle well? | Response quality, instruction following, completeness, helpfulness, safety. |
| What is the grader actually — a feature or a measurement instrument? | A measurement instrument — it exists to help you improve the real feature with confidence. |
