# Prompt Evaluation — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation & Iteration (20%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 3.1 (eval design), 3.2 (test datasets), 3.3 (eval execution) |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 17 |

---

## One-Liner

Prompt evaluation is the product-quality equivalent of A/B testing for AI features — it lets your team ship prompt changes with measured confidence instead of hoping the last tweak didn't break anything for real users.

---

## Why PMs Should Care

Every AI feature your team ships depends on a prompt. Without an evaluation pipeline, "is this prompt good?" is an opinion your engineer has, not a fact your product has. That gap has direct business consequences.

| Symptom | Root cause | Business impact |
|---------|------------|----------------|
| Support tickets about "AI gave wrong answer" | Prompt was never tested on realistic traffic | Customer churn, brand trust erosion |
| Engineers arguing about which prompt version is "better" | No objective metric to end the debate | Slow iteration, political decisions |
| Fear of changing an existing prompt | No safety net to catch regressions | Feature stagnation, tech debt on prompts |
| Inability to quote a quality number to execs | No eval score to point at | No AI quality OKR is possible |

Prompt evaluation turns every one of those "opinions" and "fears" into a number. Numbers are how PMs run products.

---

## Mental Model: The Restaurant Kitchen

Think of a prompt as a recipe, and prompt evaluation as the tasting panel.

| Kitchen concept | Prompt concept |
|-----------------|----------------|
| Recipe card | Prompt template |
| Chef tweaks the recipe | Prompt engineer tweaks the prompt |
| Chef tastes once, ships the dish | Option 1 — test once and ship |
| Chef tastes five times, patches seasoning | Option 2 — test a few times, patch corner cases |
| Tasting panel scores 20 dishes on a rubric, chef iterates | Option 3 — run through an eval pipeline |

Option 3 is the only path that gives you a Michelin-grade kitchen. Options 1 and 2 feel fast but produce inconsistent dinners.

---

## The Three Paths — PM Framing

| Option | What engineers actually do | PM-visible risk |
|--------|----------------------------|----------------|
| 1. Test once | Run the prompt on one example, looks fine, ship | High: every unusual user input is a potential incident |
| 2. Test and patch | Run a handful of edge cases they thought of | Medium: human imagination misses real tail behavior |
| 3. Eval pipeline | Run hundreds/thousands of cases through an automated scorer | Low: regressions are caught on dev machine, not in customer tickets |

When an engineer says "the prompt is ready," the PM's next question should always be: *which of these three paths did you take?*

---

## Product Use Cases

### When Evaluation is Non-Negotiable

| Scenario | Why |
|----------|-----|
| Customer-facing AI feature | Failures are visible to users; cost of incidents is high |
| Prompt that handles money, health, legal, or safety decisions | Accuracy is a compliance and liability issue |
| Any feature you plan to iterate monthly | Without eval, every iteration is a regression risk |
| Feature where you want to compare two models (Haiku vs. Sonnet) | Eval gives the objective comparison needed for the cost/quality trade-off |

### When You Can Defer (Briefly)

| Scenario | Caveat |
|----------|--------|
| Internal prototype for a demo next week | Defer, but do not ship to users without eval |
| Single-use throwaway script | Defer, but recognize you are creating tech debt if it sticks |

---

## PM Decision Framework

Before approving any AI feature for GA, ask:

| Question | If "No" |
|----------|---------|
| Do we have a documented eval dataset that reflects real user inputs? | Block the launch — you cannot measure quality |
| Can we produce an objective score for the current prompt version? | Block the launch — you have no baseline |
| If we change the prompt next month, will CI tell us whether quality went up or down? | Block the launch — you have no regression safety |
| Can I cite a number in the quality section of the launch doc? | Block the launch — your quality story is vibes |

---

## Common PM Mistakes

1. **Accepting "it looks good" as a quality signal** — you should require a number, not a vibe, before any prompt-backed feature goes to GA.
2. **Letting engineers skip eval because of timeline pressure** — every skipped eval becomes a production incident you will pay for later.
3. **Not budgeting API spend for evals** — eval runs cost money; include them in the feature's cost model from day one.
4. **Conflating one good demo with production readiness** — a demo is Option 1; Option 1 is a trap.
5. **Not owning the eval dataset as a PM artifact** — the dataset encodes what "good" means for your product. That is a PM decision, not a junior eng decision.

---

> **Key Insight**
>
> As a PM, your job is to make "quality" a number. Prompt evaluation is the mechanism that turns AI quality from a subjective argument into an objective metric you can put in an OKR, a launch doc, and an incident postmortem. On the CCA exam, questions framed around "how do we know this prompt is ready for production?" are D3 questions, and the answer is always: run it through an eval pipeline.

---

## CCA Exam Relevance

- **D3 (Evaluation & Iteration)**: distinguish prompt engineering (how you write prompts) from prompt evaluation (how you measure prompts). The three-paths framing and why Option 3 wins.
- **D5 (Enterprise Deployment)**: prompt eval is a prerequisite for production rollout — no eval, no launch.
- Watch for exam prompts framed as "how do we compare prompt versions," "how do we catch regressions," "how do we report quality" — all D3/D5 and all point at an eval pipeline.

---

## Flashcards

| Front | Back |
|-------|------|
| What PM problem does prompt evaluation solve? | It converts subjective "is this prompt good?" into an objective score you can put in launch docs, OKRs, and incident reviews. |
| What is the restaurant analogy for prompt evaluation? | A tasting panel scoring dishes on a rubric so the chef can iterate with confidence instead of trusting one taste test. |
| What are the three paths a PM should ask about after a prompt is drafted? | 1) Test once, 2) Test a few corner cases, 3) Run through an eval pipeline — only #3 is safe for GA. |
| What should a PM require before approving GA for an AI feature? | A dataset, an objective score, regression safety, and a number they can cite in the launch doc. |
| Why is "it looks good on the demo" insufficient? | Demos are Option 1 — one example is not a random sample of production traffic and hides failure modes. |
| When is deferring an eval pipeline acceptable? | Only for internal prototypes or throwaway scripts — never for customer-facing features. |
| Who owns the eval dataset? | It is a PM-level artifact because it encodes what "good" means for the product, not just an engineering decision. |
| Which CCA domain handles prompt evaluation? | D3 Evaluation & Iteration (primary), D5 Enterprise Deployment (secondary as a production gate). |
