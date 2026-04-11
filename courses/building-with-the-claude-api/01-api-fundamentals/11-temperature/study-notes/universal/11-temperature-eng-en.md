# Temperature — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D5 — Enterprise Deployment (20%) |
| Task Statements | 5.1 (model configuration), 5.3 (production patterns), 5.4 (evaluation & reliability) |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 11 |

---

## One-Liner

Temperature is a sampling parameter (0.0–1.0) that controls how sharply or softly Claude's next-token probability distribution is sampled — low values make output deterministic and factual, high values make it varied and creative.

---

## How Claude Actually Generates Text

Before temperature makes sense, you need the three-step generation loop:

1. **Tokenization** — the input is split into tokens (subword units).
2. **Prediction** — the model computes a probability distribution over every possible next token.
3. **Sampling** — one token is drawn from that distribution and appended to the output. Repeat until the model emits a stop token or hits `max_tokens`.

For a prompt ending in "What do you think?", the distribution might look like:

| Candidate next token | Probability |
|---------------------|-------------|
| " about" | 30% |
| " would" | 20% |
| " of" | 10% |
| ... | ... |

The model picks one, appends it, and runs the whole loop again for the next token. Temperature is the knob that reshapes step 3.

---

## What Temperature Does Mathematically

Temperature rescales the logits (pre-softmax scores) before the distribution is sampled.

- **Temperature = 0** → the distribution collapses to argmax. The highest-probability token is always picked. Output is deterministic (in practice — tie-breaking aside).
- **Temperature = 1** → the distribution is used as-is. Claude samples from the full probability mass, producing varied outputs.
- **Between 0 and 1** → intermediate sharpening. Higher-probability tokens are still favored, but lower-probability ones get a realistic chance.

Think of it as a "confidence dial". At 0 you trust only the single best guess; at 1 you let diversity in.

---

## The Three Temperature Bands

Different product behaviors need different bands. The course defines three:

### Low (0.0 – 0.3) — Deterministic Tasks

Use when the right answer is narrow and facts matter.

- Factual Q&A
- Coding assistance
- Data extraction / classification
- Content moderation
- Anything that feeds a downstream parser

### Medium (0.4 – 0.7) — Structured Creativity

Use when you want coherent, useful output with some natural variation.

- Summarization
- Educational content
- Problem-solving
- Creative writing with constraints

### High (0.8 – 1.0) — Divergent Generation

Use when the goal is variety and novelty.

- Brainstorming
- Marketing copy
- Fiction / joke generation
- Ideation sessions

Match the band to the task. A content moderation system at temperature 1.0 is a bug. A brainstorming tool at temperature 0.0 is boring.

---

## Adding Temperature to a Chat Function

Building on the `chat()` helper from Lesson 09, add `temperature` as a first-class parameter:

```python
from anthropic import Anthropic

client = Anthropic()

def chat(messages, system=None, temperature=1.0):
    params = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
    }
    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text
```

The only changes from the Lesson 09 version are the new `temperature=1.0` kwarg and the corresponding entry in `params`. Note that `temperature` is **always** passed — unlike `system`, it does not need conditional handling because the API accepts float values directly.

---

## Observing the Effect

Generate movie ideas at two extremes:

```python
messages = [{"role": "user", "content": "Give me a one-sentence movie idea."}]

print(chat(messages, temperature=0.0))
# "A time-traveling archaeologist must prevent ancient artifacts from being stolen."

print(chat(messages, temperature=1.0))
# Varies wildly run-to-run — new themes, characters, and plots each call.
```

At `0.0` you tend to get the same answer every time. At `1.0` you get meaningfully different answers on each call. This is why integration tests for non-deterministic flows must pin `temperature=0` or use LLM-as-judge evals rather than exact-match assertions.

---

## Temperature Is Not a Guarantee

Two critical caveats:

1. **Temperature 0 is not strictly deterministic across API versions or infrastructure.** Tie-breaking, KV-cache effects, and backend routing can produce rare variations. If you need exact determinism, pair low temperature with deterministic evaluation (exact-match over many samples, not a single call).
2. **High temperature does not guarantee novelty.** Even at 1.0, Claude might repeat common phrasings because those tokens still dominate the distribution. Temperature changes probabilities; it does not invent new tokens.

---

## Temperature vs. Other Sampling Params

Temperature is one of several sampling controls. Anthropic's API also supports `top_p` (nucleus sampling), which caps the distribution at a cumulative probability threshold. The course focuses on temperature because it is the most intuitive lever; in practice, production systems usually leave `top_p` at default and tune only temperature.

**Rule of thumb**: tune one sampling parameter at a time. Jointly tuning `temperature` and `top_p` makes it very hard to reason about outputs.

---

## Common Mistakes

1. **Using high temperature in extraction pipelines** — if downstream code expects structured JSON, temperature 1.0 is a recipe for parse errors.
2. **Using temperature 0 for creative tasks** — outputs become repetitive and boring; users notice immediately.
3. **Assuming temperature 0 is bit-exact reproducible** — it is not; rare variation is possible due to infrastructure-level nondeterminism.
4. **Tuning temperature before tuning the prompt** — the biggest quality lever is prompt + system prompt; temperature is a fine-tune knob, not a first-order fix.
5. **Forgetting to set temperature at all** — defaulting to 1.0 everywhere leads to flaky tests and inconsistent production behavior for structured tasks.

> **Key Insight**
>
> Temperature is a policy decision, not a performance one. It encodes how much variance is acceptable in your product. Pick the band based on user expectations: do users want *the* answer (low), *a good* answer (medium), or *many different* answers (high)? Then lock it in per endpoint or per feature — do not let it float.

---

## CCA Exam Relevance

- **D5 (Enterprise Deployment)**: temperature is a core production configuration parameter. Expect questions asking which temperature range to use for a given scenario (extraction vs. brainstorming).
- **D5.3 (evaluation & reliability)**: deterministic evaluation pipelines require pinning temperature — the exam may ask about reproducibility.
- Watch for scenarios asking "How do you make Claude's outputs consistent for a data-extraction task?" — the answer is low temperature (plus structured prompting), not retries.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the valid range for Claude's `temperature` parameter? | 0.0 to 1.0, inclusive. |
| What does temperature 0 mean mechanically? | Claude picks the highest-probability next token at every step — effectively argmax, producing near-deterministic output. |
| What does temperature 1 mean mechanically? | The full probability distribution is sampled directly, producing varied and creative output. |
| Which temperature band should you use for data extraction? | Low (0.0–0.3) — determinism and fact-fidelity matter. |
| Which temperature band should you use for brainstorming? | High (0.8–1.0) — variety and novelty are the goal. |
| Which temperature band should you use for summarization? | Medium (0.4–0.7) — structured but with natural variation. |
| Is temperature 0 bit-exact reproducible? | No — rare variations can occur due to infrastructure-level nondeterminism; it is approximately deterministic, not guaranteed. |
| What are the three steps of text generation? | Tokenization → Prediction (probability distribution) → Sampling (pick next token). |
| Why shouldn't you tune temperature before tuning the prompt? | The prompt is the first-order quality lever; temperature is a fine-tune knob that can't fix a bad prompt. |
