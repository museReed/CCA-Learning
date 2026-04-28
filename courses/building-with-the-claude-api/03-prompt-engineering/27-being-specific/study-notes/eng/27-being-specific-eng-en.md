# Being Specific — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation & Iteration (20%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 3.1 (prompt design & iteration), 1.1 (instruction following) |
| Source | building-with-the-claude-api / 03-prompt-engineering / Lesson 27 |

---

## One-Liner

Specificity narrows Claude's search space — output guidelines pin down *what* the result must look like, and process steps pin down *how* Claude should think about it.

---

## The Core Problem: Unbounded Interpretation

A clear and direct prompt is not enough by itself. Consider "Write a short story about a character who discovers a hidden talent." That prompt is clear, direct, and imperative — yet it still leaves Claude free to choose:

- Length (200 words or 2,000)
- Cast size (one character or five)
- Genre and setting
- Which "hidden talent" and how it's revealed

Every axis of freedom is an axis where output quality can drift across runs. Specificity is how you close those axes.

---

## Two Kinds of Specificity

The lesson identifies two complementary levers. In production prompts you will usually combine them.

### 1. Output Quality Guidelines

A list of qualities the output must have. These control the artifact itself:

- **Length** of the response
- **Structure** and format
- **Specific attributes or elements** to include
- **Tone** or style requirements

For the short-story example: "should be under 1,000 words, include a clear action that reveals the character's talent, and feature at least one supporting character." Each bullet removes one axis of freedom.

### 2. Process Steps

A numbered sequence of actions Claude should follow before producing its final answer. This controls the reasoning path:

1. Brainstorm three talents that would create dramatic tension.
2. Pick the most interesting talent.
3. Outline a pivotal scene that reveals the talent.
4. Brainstorm supporting character types that could increase the impact.

Process steps are especially valuable when the task benefits from considering multiple angles before committing, rather than generating a single pass.

---

## The Running Example: Meal Planner Guidelines

Layered onto the clear+direct prompt from Lesson 26, the lesson shows these output guidelines:

```
Guidelines:
1. Include accurate daily calorie amount
2. Show protein, fat, and carb amounts
3. Specify when to eat each meal
4. Use only foods that fit restrictions
5. List all portion sizes in grams
6. Keep budget-friendly if mentioned
```

Each bullet is testable. Each bullet closes a specific quality axis that the earlier prompt left open.

---

## Measured Impact

The course reports evaluator scores across the iterative prompt improvements:

| Version | Score (/10) |
|---------|-------------|
| Baseline ("What should this person eat?") | 2.32 |
| Clear and direct ("Generate a one-day meal plan...") | 3.92 |
| **+ Specificity guidelines** | **7.86** |

Adding specificity **doubled the score** from 3.92 to 7.86 — a larger jump than the clarity/directness rewrite delivered, and in the lesson's framing this is why specificity earns "always use" status in the playbook.

---

## When to Use Each Approach

| Technique | When to Apply |
|-----------|--------------|
| **Output Quality Guidelines** | Almost every prompt. This is your consistency safety net. |
| **Process Steps** | Complex problems — troubleshooting, decision-making, critical thinking, or anywhere you want Claude to consider multiple angles before answering. |

The lesson's example for process steps: asking Claude to analyze why a sales team's performance dropped. Without process steps, Claude might fixate on one cause. With process steps guiding it through market metrics → industry changes → individual performance → organizational changes → customer feedback, the analysis becomes exhaustive and balanced.

---

## Combining Both Approaches

In professional prompts, you will typically see both levers applied together:

- **Process steps** at the top, telling Claude how to think through the problem.
- **Output guidelines** at the bottom, telling Claude what the final artifact must contain.

This combination gives you *both* consistency in the output and confidence that Claude considered all the important factors before producing it.

---

## Why Specificity Compounds

Each bullet in a guidelines list acts like a unit test for the output. The grader (whether a human or a model-based evaluator) can check each item independently, which is exactly how your eval's `extra_criteria` scores the response. The closer the prompt's guidelines map to the evaluator's rubric, the more directly every eval iteration translates into prompt improvement.

This is why seasoned prompt engineers often write the rubric and the guidelines at the same time — they are two views of the same contract.

---

## Common Mistakes

1. **Stopping at clear + direct** — leaving Claude to guess length, structure, and included elements. You cap the eval score unnecessarily.
2. **Specifying too little, too vaguely** — "include details" is not a guideline; "list all portion sizes in grams" is.
3. **Using process steps on trivial tasks** — for simple extraction or formatting, steps just add latency without quality gain.
4. **Mismatch between prompt guidelines and eval rubric** — the prompt asks for X, the evaluator scores Y. Align them.
5. **Stacking too many process steps** — beyond about 5 steps, Claude may drop or merge them. Keep process sequences focused.

> **Key Insight**
>
> Specificity is the single largest-impact technique in the lesson's playbook — doubling the eval score from 3.92 to 7.86. Every bullet in your guidelines closes one axis of output drift, and each closed axis makes the prompt measurably more reliable. Output guidelines should be in almost every prompt; process steps join them whenever the task requires multi-angle reasoning.

---

## CCA Exam Relevance

- **D3 (Evaluation & Iteration)**: recognize specificity as the highest-leverage technique after clarity/directness, and know the two flavors (output guidelines vs process steps).
- **D1 (Agentic Architecture)**: agent system prompts rely on the same two levers — guidelines constrain the agent's outputs, process steps constrain its reasoning.
- Expect questions about which technique to apply to which task type. "Multi-angle analysis" → process steps. "Consistent artifact format" → output guidelines. "Both" → combine them.

---

## Flashcards

| Front | Back |
|-------|------|
| What are the two types of specificity guidelines? | Output quality guidelines (what the result must look like) and process steps (how Claude should think through the problem). |
| What does "output quality guidelines" control? | Length, structure, format, specific attributes/elements to include, and tone or style. |
| When should you use process steps? | For complex problems — troubleshooting, decision-making, critical thinking, or any task where Claude should consider multiple angles before answering. |
| What score improvement did specificity produce in the meal-planner example? | 3.92 → 7.86 — the eval score more than doubled just from adding specific guidelines. |
| Should output guidelines be in every prompt? | Almost always — the lesson calls them a "safety net" for consistent results. |
| Give an example process-step sequence from the lesson. | 1) Brainstorm three talents that create tension 2) Pick the most interesting 3) Outline a pivotal scene 4) Brainstorm supporting characters. |
| What happens if your prompt's guidelines don't match the evaluator's rubric? | The score will not reflect what the prompt is actually optimizing for — the two must stay aligned. |
| What's the professional pattern for combining both approaches? | Process steps at the top (how to think), output guidelines at the bottom (what the final artifact must contain). |
