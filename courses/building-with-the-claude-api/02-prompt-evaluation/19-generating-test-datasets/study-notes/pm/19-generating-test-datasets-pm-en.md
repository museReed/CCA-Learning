# Generating Test Datasets — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation & Iteration (20%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 3.2 (test datasets), 3.1 (eval design), 3.3 (eval execution) |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 19 |

---

## One-Liner

Your eval dataset encodes what "good" means for your AI feature — and the fastest way to get a usable first version is to have Claude draft it for you, then treat that draft as a living PM artifact you own and iterate on.

---

## Mental Model: The Survey Questionnaire

Think of an eval dataset like a customer survey. A PM doesn't start user research from a blank page — they draft a questionnaire, test it on a few people, and refine. Same here:

| Survey concept | Eval dataset concept |
|----------------|---------------------|
| Draft survey questions | Generate initial dataset with Haiku |
| Pilot with a few users | Run pilot eval on generated dataset |
| Refine questions based on signal | Edit dataset to strengthen weak spots |
| Lock the final version | Save `dataset.json` and version-control it |
| Re-field the survey each quarter | Re-run eval on every prompt change |

The dataset is the questionnaire. Every line in it is a decision about what your product should handle well.

---

## The AWS Code Assistant Example

The lesson's running example is a prompt that helps users write AWS-specific **Python, JSON, or regex**. The requirement is clean output — no prose wrapping, no "here is your code" preamble. For a PM, three things are worth noticing about this setup:

1. **The output format is a product requirement, not a technical detail.** Clean code is what makes the feature usable in a copy-paste workflow; messy code breaks the use case.
2. **The dataset exists to prove the prompt honors that product requirement on inputs the team did not hand-pick.**
3. **The generation step creates a dataset that can surface formatting failures cheaply, before a customer ever sees them.**

---

## Two Ways to Build a Dataset

| Approach | Speed | Fidelity | When to use |
|----------|-------|----------|-------------|
| Hand-built | Slow | High — you control every case | Specialized domains, regulated verticals, high-stakes features |
| Claude-generated | Fast | Medium — coverage depends on prompt | Bootstrapping, generic tasks, early-stage features |

The lesson picks Claude-generated for good reason: the initial cost is trivial, and you can always go back and edit the dataset by hand once you see what Claude produced. Hand-editing a generated dataset is much faster than writing one from scratch.

**Cost lever:** the lesson tells engineers to use **Haiku** (not Sonnet) for generation. For a PM, this maps directly to operating cost — bulk dataset work should never use your most expensive model.

---

## PM Decision Framework

When your team tells you they generated an eval dataset, walk through these questions:

| Question | What a good answer looks like |
|----------|------------------------------|
| Who generated it — human, or Claude? | Either is fine, but the answer shapes the next questions |
| If Claude: was it Haiku or Sonnet? | Haiku — anything else is wasted spend on bulk work |
| How many entries? | Small (e.g., 3) to start; plan for tens/hundreds at production |
| Does it cover the failure modes we're worried about? | Explicit yes, with examples |
| Is it committed to version control? | Yes — the dataset is a PM artifact, not a notebook cell |
| When a prompt change is proposed, will we re-run against THIS dataset? | Yes — same dataset, different prompt |

---

## Product Use Cases

### When to Generate with Claude

| Scenario | Why generation wins |
|----------|---------------------|
| New AI feature, no prior dataset | Fastest path from zero to something measurable |
| Exploring a new output format | Claude suggests task varieties a PM might not think of |
| Bootstrapping a dataset before hand-curating | Saves hours of hand-writing |

### When to Hand-Build

| Scenario | Why hand-building wins |
|----------|------------------------|
| Legal, medical, financial features | Mistakes in the dataset become mistakes in the product |
| Real-customer edge cases from support tickets | Those are already the best test cases |
| Production regression suite | Each entry should correspond to a known failure mode |

---

## The Growing Dataset Pattern

A PM-friendly mental model for dataset evolution:

1. **Bootstrap** — generate ~3 entries with Haiku to prove the eval pipeline runs.
2. **Expand** — ask Haiku for 30 more to cover breadth; review and keep the good ones.
3. **Curate** — add hand-written cases from real customer complaints and edge cases.
4. **Lock** — version-control the dataset; every new prompt version runs against it.
5. **Grow** — whenever a production incident happens, add the failing case to the dataset so it can never regress again.

Step 5 is how the dataset becomes a living quality contract between product and engineering.

---

## Common PM Mistakes

1. **Thinking the dataset is an engineering artifact** — it encodes product definition-of-good, so it is a PM deliverable.
2. **Accepting a dataset you have never read** — if you cannot skim the cases and say "yes, these reflect real usage," the eval is not measuring the right thing.
3. **Not adding production incidents to the dataset** — every customer-visible failure should become a permanent test case.
4. **Letting engineers regenerate the dataset between runs** — this destroys comparability and hides regressions.
5. **Under-budgeting for Haiku spend on dataset refresh** — cheap, but not free; include it in the feature's operating cost.

---

> **Key Insight**
>
> The eval dataset is the clearest PM-owned answer to "what does quality mean for this feature?" Every case you include is an explicit promise that the product will handle inputs like this well. Because the CCA exam frames dataset work under D3, any question about "how should a team bootstrap test data for a new prompt" points at Haiku-generated datasets with prefilling, saved to disk for reuse.

---

## CCA Exam Relevance

- **D3 (Evaluation & Iteration)**: know the two dataset-building approaches, when to use each, and why Haiku is the default for generation.
- **D5 (Enterprise Deployment)**: the versioned dataset on disk is a production artifact — it is what makes prompt regression detectable.
- Exam trigger: "bootstrap an eval dataset" → Haiku + prefilling + stop sequence + `json.loads` + save to disk.

---

## Flashcards

| Front | Back |
|-------|------|
| Why should a PM consider the eval dataset a PM artifact, not an engineering one? | It encodes what "good" means for the feature — that is a product judgment, not an implementation detail. |
| What is the survey analogy for an eval dataset? | A customer questionnaire — it is drafted, piloted, refined, locked, and re-fielded each time the product changes. |
| What two approaches to dataset building does the lesson describe? | Hand-built (slow, high fidelity) and Claude-generated (fast, medium fidelity). |
| Which model should bulk dataset generation use? | Haiku — it is the faster, cheaper choice for bulk creative work. |
| What should a PM do when a production incident surfaces a new failure mode? | Add the failing case to the eval dataset so the regression is caught on the next iteration. |
| Why must the dataset stay fixed across prompt iterations? | So that score differences between prompt versions can be attributed to the prompt change, not to a change in inputs. |
| What is the minimum viable first dataset the lesson builds? | Three Claude-generated tasks (one each for Python, JSON config, regex) for the AWS code-assistant prompt. |
| Which CCA domain covers dataset generation? | Primary: D3 Evaluation & Iteration; the persisted dataset also touches D5 Enterprise Deployment as a production artifact. |
