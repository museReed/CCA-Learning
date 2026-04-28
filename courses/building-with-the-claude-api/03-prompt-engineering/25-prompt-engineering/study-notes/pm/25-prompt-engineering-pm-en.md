# Prompt Engineering — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation & Iteration (20%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 3.1 (prompt design & iteration), 1.1 (instruction following) |
| Source | building-with-the-claude-api / 03-prompt-engineering / Lesson 25 |

---

## One-Liner

Prompt engineering is product iteration with a measurable scoreboard — you build a baseline, score it, improve one thing, and re-score, so every release ships on data instead of vibes.

---

## Why PMs Should Care

Most AI features ship a prompt and never measure it again. That is the equivalent of shipping a landing page and never looking at conversion. This lesson frames prompts as **a core product artifact that deserves its own CI, its own regression tests, and its own KPIs** — the evaluator is literally a score out of 10.

Without an eval loop, you get:

- Drift — a model update silently degrades output quality.
- Disagreement — engineering says "it works," CS says "users complain," no one can point to a number.
- Fear of change — no one wants to touch the prompt because no one can prove the change is safe.

With an eval loop, prompt changes behave like any other product change: you see the delta, you ship the winner, you roll back the regression.

---

## Mental Model: The Fitness Tracker

Think of prompt engineering like training with a fitness tracker:

| Activity | Without Tracker | With Tracker |
|----------|----------------|--------------|
| Start a routine | "I think I'm getting stronger" | Baseline bench press = 60 kg |
| Try a new technique | "Feels harder, must be working" | Technique A → 62 kg (+2) |
| Try another technique | "Which one was better?" | Technique B → 70 kg (+10), ship it |

The evaluator is the fitness tracker. The prompt is your training plan. Techniques are exercises. You cannot know which exercise paid off until you weigh yourself after each one, in isolation.

---

## The Five-Step Loop (in PM language)

| Step | What | PM Translation |
|------|------|----------------|
| 1 | Set a goal | What does "good" look like? Define acceptance criteria. |
| 2 | Write an initial prompt | Ship a v0, even if you know it's bad. |
| 3 | Evaluate | Run the test and get a number. |
| 4 | Apply a technique | Make one change. One. |
| 5 | Re-evaluate | Did the number go up? Keep it. Down? Roll back. |

This is literally the build-measure-learn loop from Lean Startup applied at prompt granularity.

---

## Product Use Cases

### When an Eval Loop Is Worth Building

| Scenario | Why It Matters |
|----------|----------------|
| A user-facing feature where quality is subjective (summaries, recommendations) | Humans disagree on quality; you need a shared scoreboard |
| A regulated or high-stakes domain (health, finance, legal) | You must be able to prove the prompt behaves consistently |
| A prompt that will be touched by multiple engineers over months | Regression safety — changes must be provably non-destructive |
| A prompt feeding a downstream pipeline (prompt → tool call → DB write) | Upstream degradation is hard to detect without scored outputs |

### When It's Probably Overkill

| Scenario | Better Alternative |
|----------|--------------------|
| A one-off internal script | Just spot-check the output manually |
| A throwaway prototype before product-market fit | Optimize for learning speed, not prompt quality |
| A prompt that ships to five internal users | The users are the eval |

---

## The Scorecard Mindset

The lesson gives you concrete numbers: baseline 2.3/10 is normal. A PM should internalize a few anchors:

| Score (/10) | What It Means | Ship? |
|-------------|---------------|-------|
| 2-3 | First-draft baseline | Never |
| 5-6 | Clarity + specificity applied | Internal dogfood |
| 7-8 | Examples + structure added | Beta |
| 9+ | Edge-cases hardened | GA |

This is opinionated — the course shows 2.3 → 3.92 → 7.86 across two technique applications. The point for PMs is: **attach a score threshold to each release gate**, not a vague "it looks good."

---

## PM Decision Framework

When you're about to ship an AI feature, ask:

| Question | If Yes, You Need |
|----------|------------------|
| Will this prompt be changed more than once after launch? | An eval loop with regression tracking |
| Do different stakeholders disagree about quality? | A rubric encoded as `extra_criteria` |
| Is quality subjective (tone, format, completeness)? | A model-graded evaluator, not just unit tests |
| Will model upgrades affect this feature? | Pinned baseline scores so upgrades prove themselves |
| Do we care about p95 quality, not just average? | Larger dataset for final validation runs |

---

## Common PM Mistakes

1. **"It works on my example"** — one happy-path test case is not an eval, it is a demo.
2. **Skipping the baseline** — launching with a "good" prompt and no score means you can never prove the next version is better.
3. **Moving the rubric** — changing `extra_criteria` between iterations invalidates score comparisons. Freeze the rubric, iterate the prompt.
4. **Over-investing too early** — building a 500-case eval harness before you've shipped a baseline burns runway. Start with 2-3 cases.
5. **Ignoring the report** — PMs who only look at the score miss the grader's reasoning, which is where the product insights live.

> **Key Insight**
>
> Prompt engineering turns a subjective product artifact into a measurable one. For a PM this is the difference between "launching on vibes" and "launching on data." Once you have a score you can own it, defend it, regress against it, and improve it — and that transforms the AI feature from magic to engineering.

---

## CCA Exam Relevance

- **D3 (Evaluation & Iteration)**: recognize that the eval-driven loop is the canonical answer for "how do you improve a prompt?"
- **D1 (Agentic Architecture)**: the same loop tunes agent system prompts. Questions may frame agent misbehavior as a prompt tuning problem.
- Expect questions asking "the team's prompt scores 2.3/10, what's next?" → always "apply one technique and re-evaluate," never "rewrite from scratch."
- Know that small datasets (2-3 cases) are a feature of early iteration, not a flaw.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the core idea of prompt engineering per this lesson? | It is an iterative loop: baseline → evaluate → apply technique → re-evaluate. It is measurable, not vibes-based. |
| Why should PMs attach a score to every prompt release? | Because without a score you cannot tell if a change improved or regressed the feature; it turns prompts into a managed product artifact. |
| What is a typical baseline score, and how should a PM react? | Around 2.3/10 — treat it as normal and a starting line, not a reason to panic. |
| Why apply only one technique per iteration? | So score deltas are attributable, giving you a reliable playbook for future prompts. |
| What is `extra_criteria` in PM language? | A rubric — the list of must-haves the grader should score against. It is how you encode business requirements into the eval. |
| What's the "fitness tracker" analogy? | The evaluator is the scale/tracker, the prompt is your training plan, each technique is one exercise. You weigh in after each. |
| When is building an eval loop overkill? | One-off scripts, throwaway prototypes, or prompts that only ship to a handful of internal users. |
| What release-gate pattern does this lesson support? | Tie each release stage (internal, beta, GA) to a minimum eval score threshold. |
