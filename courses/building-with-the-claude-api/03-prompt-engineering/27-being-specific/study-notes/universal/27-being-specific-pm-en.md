# Being Specific — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation & Iteration (20%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 3.1 (prompt design & iteration), 1.1 (instruction following) |
| Source | building-with-the-claude-api / 03-prompt-engineering / Lesson 27 |

---

## One-Liner

Specificity is an acceptance criteria list — bullet by bullet, you tell Claude exactly what "done" looks like, turning a vague ask into a testable contract.

---

## Why PMs Should Care

Every PM has written a vague ticket and watched it come back wrong, not because the engineer was bad but because "done" wasn't defined. Prompts fail the same way. A prompt without specificity is a feature ticket without acceptance criteria — you'll get *something*, but you can't predict what, and you can't prove it's correct.

The lesson's measured impact is dramatic: adding a specificity bullet list to a clear+direct prompt jumped the eval score from **3.92 to 7.86** — more than doubling quality from one edit. That's the single largest quality jump in the entire prompt engineering chapter. For PMs it's the highest ROI lever available.

---

## Mental Model: Acceptance Criteria

| PM Artifact | Prompt Equivalent |
|-------------|-------------------|
| User story | The clear+direct first line |
| Acceptance criteria | Output quality guidelines |
| Test plan / checklist | The eval rubric (`extra_criteria`) |
| Process doc / SOP | Process steps |

When you read the lesson's meal-plan guidelines ("Include accurate daily calorie amount, show protein/fat/carb amounts, specify when to eat each meal...") you are reading acceptance criteria for an AI feature. Every bullet is testable. Every bullet closes one source of ambiguity.

---

## The Two Levers

### Output Quality Guidelines — The "What"

Tell Claude what the finished artifact must contain:

- Length
- Structure and format
- Specific elements or attributes
- Tone or style

The lesson recommends using these in **almost every prompt**. They are the consistency safety net.

### Process Steps — The "How"

Tell Claude how to think through the problem before answering:

1. Brainstorm options
2. Pick the best one
3. Outline the detail
4. Consider supporting factors

Use these when the task is complex enough that Claude might fixate on one angle when it should consider many. The lesson's canonical example is "analyze why a sales team's performance dropped" — a task where jumping to a single cause gives a shallow answer.

---

## Product Use Cases

### Always Add Output Guidelines

| Feature | Guidelines Example |
|---------|--------------------|
| Meeting summarizer | "Include attendees, decisions, action items with owners, and next meeting date in under 200 words." |
| Support ticket classifier | "Return only: category (one of: billing/bug/feature/other), priority (P0-P3), and a one-sentence summary." |
| Weekly newsletter generator | "Include a 2-sentence intro, 3 highlighted stories, a stats table, and a CTA link. Max 400 words." |

### Add Process Steps for Multi-Angle Analysis

| Feature | Process Steps Example |
|---------|-----------------------|
| Root-cause analysis assistant | "1) List possible causes 2) Rank by likelihood 3) Identify data needed to confirm each 4) Propose top 2 hypotheses." |
| Design critique tool | "1) Identify the primary user goal 2) Evaluate against it 3) Note strengths 4) Note weaknesses 5) Propose one fix." |
| Deal review for sales ops | "1) Check pipeline stage 2) Review recent activity 3) Flag risk signals 4) Recommend next action." |

### Don't Over-Engineer

Simple extraction or formatting tasks ("extract the email from this signature") don't need process steps. Adding them just costs latency without quality gain.

---

## PM Decision Framework

When designing an AI feature's prompt, ask:

| Question | Action |
|----------|--------|
| Can I list the exact elements the output must contain? | Write output guidelines as a numbered list |
| Is there a "right answer" that requires considering multiple factors? | Add process steps |
| Is there a risk Claude will ignore an important angle? | Add a process step for that angle |
| Can my eval rubric score each guideline independently? | Yes — keep guidelines and rubric aligned |
| Are all my guidelines testable? | Replace fuzzy ones with measurable versions |

If a PM can't write acceptance criteria for a feature, the prompt is going to fail. The exercise of listing output guidelines often uncovers the PRD gaps.

---

## The Compounding Effect

Specificity pays off twice:

1. **Directly** — the eval score goes up because the output is closer to what you asked for.
2. **Indirectly** — because each bullet is testable, your eval rubric can be tighter, which means future iterations improve faster.

This is the same compounding you see in strong PRDs: clearer acceptance criteria make QA faster, bugs more specific, and regressions easier to prevent. Prompts benefit from the same discipline.

---

## Common PM Mistakes

1. **Vague quality bullets** — "should be professional" is not a guideline, "avoid contractions, use third-person voice, max 300 words" is.
2. **Skipping specificity because clear+direct "worked"** — 3.92/10 is not shipping quality. Specificity is the lever that gets you to 7.86+.
3. **Confusing process steps with output structure** — process steps control *how Claude thinks*, not *how the answer is formatted*. Those are separate levers.
4. **Cramming everything into one bullet** — each guideline should be independently testable. Split overloaded bullets.
5. **Misaligning guidelines with the eval rubric** — if the prompt asks for X but the rubric scores Y, you'll never ship improvements reliably.

> **Key Insight**
>
> Specificity is where prompt engineering stops being "word choice" and starts being **product spec writing**. Output guidelines are acceptance criteria, process steps are SOPs, and together they turn a prompt from a request into a contract. The lesson's 3.92 → 7.86 jump is the strongest evidence in the chapter that this is the highest-ROI move a PM can make on AI features.

---

## CCA Exam Relevance

- **D3 (Evaluation & Iteration)**: recognize specificity as the highest-leverage technique after clarity/directness, and know the distinction between output guidelines and process steps.
- **D1 (Agentic Architecture)**: agent system prompts use the same two levers to control what the agent produces and how it reasons.
- Exam scenarios may describe a prompt missing one lever and ask what to add. Watch for clues: "inconsistent format" → output guidelines; "jumping to conclusions" → process steps.

---

## Flashcards

| Front | Back |
|-------|------|
| What PM artifact is directly analogous to specificity output guidelines? | Acceptance criteria — a testable, bullet-point list of what "done" looks like. |
| What score delta did specificity deliver in the lesson? | 3.92 → 7.86 — more than doubling the eval score from adding output guidelines. |
| When should a PM reach for process steps instead of just output guidelines? | When the task requires considering multiple angles, like root-cause analysis or decision-making — where Claude might fixate on one cause. |
| What's the test for a good output guideline? | Each bullet is independently testable by the eval rubric — vague bullets like "be professional" fail this test. |
| Should output guidelines be in almost every prompt? | Yes — the lesson calls them the "safety net" for consistent results; they should be a default, not an optimization. |
| Give an example of a process step sequence for a deal-review feature. | 1) Check pipeline stage 2) Review recent activity 3) Flag risk signals 4) Recommend next action. |
| What happens when the prompt guidelines and eval rubric are misaligned? | The score does not measure what the prompt is trying to optimize, so iterations don't translate into shipping improvements. |
| What's the two-part compounding benefit of specificity? | Direct (higher score from closer-to-spec output) and indirect (tighter rubric enables faster future iterations). |
