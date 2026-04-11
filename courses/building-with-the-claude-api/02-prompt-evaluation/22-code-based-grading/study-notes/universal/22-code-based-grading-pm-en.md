# Code-Based Grading — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation (20%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 3.4 (deterministic scoring), 3.3 (test runner integration), 5.4 (combined eval metrics) |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 22 |

---

## One-Liner

Code-based grading is the cheap, deterministic floor of your AI quality metric — it automatically rejects broken outputs in microseconds so your team stops shipping regressions that a quick demo would have caught.

---

## Why PMs Should Care

Imagine shipping a code-generation feature and learning from a user tweet that half the outputs have syntax errors. That should never happen. Code-based grading makes this class of regression **impossible to ship** — every test case is parsed automatically before your prompt change goes live.

The three things code graders catch that model graders cannot reliably catch:

- "Is this actually parseable JSON / Python / Regex?"
- "Did the model sneak in commentary when I asked for raw code only?"
- "Did we accidentally regress on format discipline this week?"

These are quality regressions that a human demo might miss but a CI pipeline running on every prompt PR will catch every time.

---

## Mental Model: The Spell-Checker Before the Editor

Think of code graders and model graders as a two-stage editing pipeline:

| Stage | Role | Cost | Catches |
|-------|------|------|---------|
| **Spell-checker** (code grader) | Auto-reject syntactically broken output | Microseconds, free | JSON parse errors, Python syntax errors, regex errors |
| **Editor** (model grader) | Judge clarity, helpfulness, instruction following | API call per case | Subjective quality issues |

Every piece of writing goes through spell-check before a human editor even sees it. The same logic applies to AI output — the cheap deterministic check runs first, and only output that passes gets the expensive judgement call.

---

## Product Use Cases

### When to Use Code Graders

| Scenario | Why Code Graders Work |
|----------|-----------------------|
| Shipping a JSON API where the AI must return valid JSON | Parseability is non-negotiable and free to check |
| Code-generation features (SQL, Python, regex) | Invalid syntax breaks the product immediately |
| "Raw output only, no commentary" instructions | Easy to verify with a strict parser |
| Length or format constraints | Boolean checks, not judgement calls |
| CI/CD eval gates on every prompt PR | Microsecond latency makes it cheap to run everywhere |

### When NOT to Use Code Graders

| Scenario | Better Alternative |
|----------|--------------------|
| "Is the response helpful?" | Use a model grader — this is subjective |
| "Does the output follow brand voice?" | Use a model grader |
| "Is the answer correct?" | Use a model grader unless you have a ground-truth string to compare |

---

## The Hybrid Score Is the Feature

The source's final move is to average the model grader score and the code grader score:

```
score = (model_score + syntax_score) / 2
```

This composite metric is what PMs should actually chart. It rewards prompts that are both correct in form (syntax) and good in substance (quality), and it penalizes prompts that cheat on either axis.

A critical PM decision: **the weighting**. An equal 50/50 is the default. For a pure code-generation product, you might push syntax to 70%. For a customer-service tone feature, you might push quality to 80% and only use the code grader as a hard floor. This weighting is a product decision, not an engineering one — own it explicitly in your PRD.

---

## PM Decision Framework

| Question | If Yes | Action |
|----------|--------|--------|
| Does the output have a deterministic structure (JSON, code, regex)? | Yes | Add a code grader — it's free and deterministic |
| Do we have a test-case format field (`format: "python"`)? | Yes | Great — the runner can route automatically |
| Is the eval pipeline gated in CI? | Yes | Code graders are the cheapest gate to run on every PR |
| Do we care about content quality too? | Yes | Combine with a model grader via averaged score |
| Does one dimension matter much more than the other? | Yes | Tune the combination weights in the PRD — don't default to 50/50 |

---

## Common PM Mistakes

1. **Skipping code graders because "model graders can do everything"** — you waste tokens on deterministic checks and introduce variance where none should exist.
2. **Not gating CI on the code grader** — a broken JSON regression will ship because nothing catches it before review.
3. **Defaulting to 50/50 weighting forever** — not every product values syntax and quality equally. Tune deliberately.
4. **Owning the test case format in engineering alone** — the `format` field is a product decision (what do we promise the user?) and belongs in the PRD.
5. **Treating the score as a goal** — the source is clear: the score itself isn't inherently good or bad. What matters is whether prompt iterations move it in the right direction.

> **Key Insight**
>
> Code graders exist because some quality properties are binary: the JSON parses or it doesn't, the Python compiles or it doesn't. Paying a model grader for those is like paying a book editor to spell-check. Put the cheap deterministic check first, then spend your model grader tokens only on the things that actually require judgement.

---

## CCA Exam Relevance

- **D3 (Evaluation)**: Code graders are the deterministic half of a hybrid eval pipeline. Know which tasks belong to code graders (format, syntax, length) vs. model graders (quality, helpfulness).
- **D5 (Enterprise Deployment)**: Deterministic scoring is what makes eval automation cheap enough to gate CI.
- Watch for: "You need to validate AI-generated JSON / Python / Regex" → the answer is always a code grader.

---

## Flashcards

| Front | Back |
|-------|------|
| What product problem do code graders solve that model graders cannot reliably? | Catching broken deterministic output (invalid JSON, unparseable Python, bad regex) before it ships. |
| What are the two main advantages of code graders? | Deterministic (same input → same score) and extremely cheap (microseconds, no API cost). |
| What is the mental model for code grader + model grader? | Spell-checker (code grader) runs first, human editor (model grader) runs second. |
| What is the default way to combine model and code grader scores? | Unweighted average: `(model_score + syntax_score) / 2`. |
| Who should own the weighting between model and code grader scores? | The PM — it's a product decision about what matters more for this feature. |
| What field must test cases include for the runner to route to the right validator? | `format` — with values like `"python"`, `"json"`, or `"regex"`. |
| Why is the absolute score not inherently good or bad? | Because what matters is whether prompt iterations can move it — the delta, not the level. |
| When should you skip code graders entirely? | When the output has no deterministic structure to validate (e.g., free-form helpful responses). |
