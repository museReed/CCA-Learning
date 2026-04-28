# Temperature — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D5 — Enterprise Deployment (20%) |
| Task Statements | 5.1 (model configuration), 5.3 (production patterns), 5.4 (evaluation & reliability) |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 11 |

---

## One-Liner

Temperature is the "creativity dial" on Claude — it controls how much variance the user sees in responses. As a PM, choosing the right temperature per feature is how you align output behavior with user expectations: predictable for factual tasks, varied for creative ones.

---

## Mental Model: The Chef Analogy

Imagine ordering from a restaurant:

| Temperature | Chef behavior | Diner expectation |
|-------------|---------------|-------------------|
| 0.0 | Makes the exact same dish from the recipe every time | "I want the signature steak — exactly as it was last time." |
| 0.5 | Follows the recipe but adds small, tasteful variations | "Do your thing, chef, but keep it on-brand." |
| 1.0 | Improvises freely — each plate is a new creation | "Surprise me — chef's choice, never the same twice." |

If a diner orders a medical prescription and gets "chef's choice" behavior, that's a disaster. If a diner orders a tasting menu and gets the same dish every night, that's boring. Temperature is the product decision about which experience this feature delivers.

---

## Why PMs Should Care

Temperature is one of the few Claude parameters that **directly shapes the user experience**. It is not a technical detail — it is a product policy.

- **Low temperature** = product promise of *consistency and reliability*
- **High temperature** = product promise of *variety and surprise*
- **Medium** = product promise of *quality with a human touch*

If your data-extraction feature returns different JSON shapes each time, users lose trust. If your brainstorming tool returns the same three ideas each visit, users stop opening it. Temperature is the simplest lever to fix both.

---

## Product Use Cases

### Low Temperature (0.0 – 0.3)

| Product | Why low? |
|---------|----------|
| Support ticket classifier | Same input must get same label |
| Invoice data extractor | Downstream systems expect deterministic fields |
| Medical / legal explainers | Variance in wording can be legally dangerous |
| Code assistant | Users expect the same fix for the same bug |
| Content moderation | Consistency is a fairness requirement |

### Medium Temperature (0.4 – 0.7)

| Product | Why medium? |
|---------|-------------|
| Meeting summarizer | Coherent structure + natural phrasing |
| Tutoring explanations | Consistent pedagogy with a human voice |
| Email draft assistant | Grounded in facts but not robotic |
| Knowledge-base answers | Reliable facts with readable variation |

### High Temperature (0.8 – 1.0)

| Product | Why high? |
|---------|-----------|
| Brainstorming / ideation tool | Users want many different ideas |
| Marketing copy generator | Novelty is the whole point |
| Name / slogan generator | Diversity > precision |
| Fiction / game dialog | Surprise drives engagement |

---

## The PM Decision Framework

Ask four questions when you specify an AI feature:

1. **Does the same input need to produce the same output?** → Low temperature. No exceptions.
2. **Does a downstream parser or automation consume the output?** → Low temperature. Variance breaks pipelines.
3. **Will users compare two runs side-by-side?** → Low or medium. Inconsistency reads as a bug.
4. **Is variety part of the value proposition?** → High. Lock it in.

Write the answer into the PRD as part of acceptance criteria. "Temperature: 0.2, fixed" is a real product requirement, not a tuning detail.

---

## What Temperature Cannot Fix

Temperature is a sampling knob, not a quality fix. Do not reach for it when the real problem is:

- **Bad prompts** → improve the prompt first; temperature is second-order.
- **Missing context** → add retrieved data or tools; temperature cannot invent facts.
- **Wrong model size** → upgrade the model tier if outputs are simply not smart enough.
- **Inconsistent persona** → that is a system-prompt job, not a temperature job.

A common failure mode: PM sees "hallucinations" in production, lowers temperature to 0, ships it. The hallucinations were caused by a bad prompt, not temperature. The fix does nothing.

---

## Common PM Mistakes

1. **Leaving temperature at the default (1.0) for everything** — great for chat, terrible for extraction. Pick per feature.
2. **Confusing low temperature with high accuracy** — it only means low variance. A consistent wrong answer is still wrong.
3. **Not specifying temperature in the PRD** — engineers pick whatever they feel, and you inherit the inconsistency at launch.
4. **A/B testing high vs. low temperature without changing the prompt** — you may be testing the wrong variable.
5. **Using high temperature on legally sensitive copy** — the one day it generates something off-brand, you will be in a meeting about it.

> **Key Insight**
>
> Temperature is a product-policy decision, not an engineering tuning knob. It encodes the contract you make with users about how much variance they should expect. Decide it deliberately, write it into the PRD, and lock it per feature. The worst outcome is an inconsistent product because temperature was set by whoever wrote the code first.

---

## CCA Exam Relevance

- **D5 (Enterprise Deployment)**: temperature is a standard production configuration parameter. Expect scenario questions asking which range fits a given product.
- Watch for phrasing like "How do you ensure consistent classification output?" — the answer is low temperature.
- Watch for phrasing like "How do you generate diverse marketing copy variants?" — the answer is high temperature.

---

## Flashcards

| Front | Back |
|-------|------|
| What does temperature control in product terms? | The variance the user sees in responses — low = consistent, high = varied. |
| Which temperature band fits a data-extraction tool? | Low (0.0–0.3) — determinism is a product requirement. |
| Which temperature band fits a brainstorming tool? | High (0.8–1.0) — variety is the value proposition. |
| Which temperature band fits a meeting summarizer? | Medium (0.4–0.7) — coherent but natural. |
| Is low temperature the same as high accuracy? | No — it means low variance. A repeatably wrong answer is still wrong. |
| Should temperature be specified in the PRD? | Yes — it is a product policy, not an engineering tuning detail. |
| What is the chef analogy for temperature 0 vs 1? | 0 = signature dish exact every time; 1 = chef's choice, never the same twice. |
| What product problem does temperature NOT fix? | Bad prompts, missing context, wrong model, persona drift. Temperature is second-order. |
| Why is temperature 1.0 dangerous for legal / medical copy? | A rare unusual phrasing can be legally problematic; you need consistency, not creativity. |
