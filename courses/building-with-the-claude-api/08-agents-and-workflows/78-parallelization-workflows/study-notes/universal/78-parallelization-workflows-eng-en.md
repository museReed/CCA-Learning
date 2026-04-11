# Parallelization Workflows — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) — PRIMARY |
| Task Statements | 1.2 (agentic patterns — parallelization), 5.2 (production workflow deployment) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 78 |

---

## One-Liner

Parallelization workflows split one complex task into independent sub-tasks that run concurrently (typically via `asyncio.gather`), then aggregate the results in a final LLM call — it's the "fan-out / fan-in" pattern applied to LLM reasoning.

---

## The Problem This Pattern Solves

Single-prompt complex decisions force Claude to juggle many criteria simultaneously. The lesson's canonical example: a material recommender that must choose between metal, polymer, ceramic, composite, elastomer, and wood for a given part image.

Naive approach (one prompt):
```
"Look at this part and pick the best material from: metal, polymer, ceramic, composite, elastomer, wood. Consider strength, weight, cost, manufacturability, corrosion resistance..."
```

Problems:
1. Claude splits attention across 6 materials × 5+ criteria = 30+ considerations
2. No independent deep-dive on any single material
3. Hard to optimize — you cannot A/B-test the "metal prompt" in isolation
4. Impossible to add a 7th material without rewriting the whole prompt

---

## The Parallelization Pattern

From Anthropic's "Building Effective Agents" blog post, parallelization comes in two flavors:

| Flavor | Purpose | Example |
|--------|---------|---------|
| **Sectioning** | Split a task into independent sub-tasks, each focusing on one aspect | Material recommender (one LLM per material) |
| **Voting** | Run the *same* task multiple times and take a majority/consensus | Moderation ("is this content safe?") with N voters |

Both run N LLM calls in parallel and aggregate results. The difference is whether each sub-task has *different* inputs/prompts (sectioning) or the *same* (voting).

---

## Canonical Structure

```
       ┌─→ sub-task 1 ──┐
input ─┼─→ sub-task 2 ──┼─→ aggregator ─→ final output
       └─→ sub-task N ──┘
```

1. **Split** — transform one input into N focused sub-tasks
2. **Fan-out** — run all N sub-tasks concurrently (`asyncio.gather`)
3. **Fan-in / Aggregate** — feed all sub-task results into a final LLM call for a single decision
4. **Return** — send the aggregated answer back to the user

---

## Python Implementation (asyncio.gather)

```python
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

MATERIALS = ["metal", "polymer", "ceramic", "composite", "elastomer", "wood"]

async def evaluate_material(image_b64: str, material: str) -> dict:
    """One specialized LLM call per material."""
    prompt = f"""
You are a materials engineer evaluating whether {material} is a good fit
for the pictured part. Focus ONLY on {material} criteria:

<criteria>
{MATERIAL_CRITERIA[material]}
</criteria>

Return JSON: {{"material": "{material}", "score": 0-10, "rationale": "..."}}
"""
    resp = await client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64",
                                             "media_type": "image/jpeg",
                                             "data": image_b64}},
                {"type": "text", "text": prompt},
            ],
        }],
    )
    return parse_json(resp.content[0].text)

async def aggregate(evaluations: list[dict]) -> str:
    """Fan-in: combine all specialized evaluations into a final pick."""
    prompt = f"""
Here are 6 independent material evaluations for the same part:

{json.dumps(evaluations, indent=2)}

Pick the single best material and justify your choice.
"""
    resp = await client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text

async def material_recommender(image_b64: str) -> str:
    # fan-out
    tasks = [evaluate_material(image_b64, m) for m in MATERIALS]
    evaluations = await asyncio.gather(*tasks)
    # fan-in
    return await aggregate(evaluations)
```

Key implementation notes:
- `AsyncAnthropic` (not `Anthropic`) so calls are awaitable
- `asyncio.gather(*tasks)` runs the fan-out stage in true concurrency
- Each sub-task is small, focused, and independently testable
- The aggregator sees all structured results at once

---

## Benefits

1. **Focused attention** — each Claude call concentrates on one aspect, improving accuracy.
2. **Independent optimization** — refine the metal prompt without touching others; A/B test per-material.
3. **Scalability** — add a 7th material by appending a prompt file; no regression risk on the other six.
4. **Reliability** — lower cognitive load per call produces more consistent outputs.
5. **Latency** — N calls in parallel take roughly the time of the slowest call, not N × average.

---

## When NOT to Use Parallelization

- Tasks where later steps *depend on* earlier outputs (use chaining instead — lesson 79).
- When the sub-tasks cannot be meaningfully separated (e.g., "summarize this article" is not parallelizable).
- When cost matters more than latency: parallelization runs *more* LLM calls, not fewer. You multiply token spend by N.

---

## Voting Variant

The same infrastructure supports a voting pattern: run the *identical* prompt N times and aggregate by majority rule. Useful for safety-critical decisions:

```python
async def moderation_vote(text: str, n: int = 5) -> bool:
    tasks = [is_safe(text) for _ in range(n)]
    votes = await asyncio.gather(*tasks)
    return sum(votes) > n / 2  # majority
```

Voting trades cost for reliability — classical ensemble technique applied to LLMs.

---

## Common Mistakes

1. **Forgetting the aggregation step.** Parallel sub-tasks alone do not produce a decision. You still need a final LLM (or rule-based) aggregator.
2. **Making sub-tasks depend on each other.** If sub-task 2 needs sub-task 1's output, it's a chain, not a parallel — using `asyncio.gather` will race or deadlock.
3. **Using `Anthropic` instead of `AsyncAnthropic`.** Sync clients block; you'll serialize instead of parallelize.
4. **Ignoring per-task timeouts.** One slow call can stall the whole gather. Wrap each with `asyncio.wait_for` or use `gather(return_exceptions=True)`.
5. **Exploding token costs.** Each parallel call is a separate API bill. Cap N and cache where possible.

---

> **Key Insight**
>
> Parallelization is the "focused attention" workflow — by giving each Claude call a single narrow responsibility, you get better analysis per call *and* lower total latency. The cost is N× API spend, so use it when quality matters more than cost, or when latency is the bottleneck. Remember both flavors for the exam: **sectioning** (different sub-tasks) and **voting** (same task N times).

---

## CCA Exam Relevance

- **D1 (22%) PRIMARY**: Expect a scenario question asking you to identify parallelization (keywords: "split", "run simultaneously", "fan out", "aggregate").
- **D5 (20%) SECONDARY**: Production patterns — `asyncio.gather`, latency/cost trade-offs.
- Signal words: "split into multiple independent evaluations", "run simultaneously", "aggregate results", "fan-out / fan-in".
- Know both variants (sectioning vs voting).

---

## Flashcards

| Front | Back |
|-------|------|
| What is a parallelization workflow? | Split one task into independent sub-tasks, run them concurrently, then aggregate the results |
| Name the two flavors of parallelization. | Sectioning (different sub-tasks on the same input) and voting (same task run N times) |
| What Python primitive executes the fan-out stage? | `asyncio.gather(*tasks)` with the `AsyncAnthropic` client |
| Why is parallelization better than one mega-prompt? | Focused attention per call, independent optimization, scalable, more reliable |
| What is the cost trade-off of parallelization? | N× API spend vs one call — you pay more tokens in exchange for quality and latency |
| When should you NOT use parallelization? | When sub-tasks depend on each other (use chaining) or when cost matters more than quality |
| What is the "voting" parallelization pattern used for? | Safety/consensus decisions — run the same prompt N times and take majority (e.g., moderation) |
| What client class enables concurrent Anthropic calls in Python? | `AsyncAnthropic` — the async variant of the Anthropic SDK client |
