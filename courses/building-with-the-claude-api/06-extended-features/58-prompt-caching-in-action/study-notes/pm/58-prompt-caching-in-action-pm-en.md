# Prompt Caching in Action — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D5 — Enterprise Deployment (20%) |
| Task Statements | 5.1 (cost/latency optimization), 5.2 (production performance) |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 58 |

---

## One-Liner

Turning caching on in a real product means agreeing on which tool list and system prompt stay frozen, wiring the cache markers in, and watching the usage counters in production to verify that the savings you promised in the business case actually show up.

---

## Why PMs Should Care

Caching is one of the few optimizations where the product-level decision — "we promise this chunk of context will stay identical across calls" — does most of the work. Once engineering has converted the tools list and system prompt to the cacheable form, the feature either saves money or silently does nothing. That outcome depends entirely on:

1. **What the product keeps stable.** Large stable system prompt? Stable tool schemas? Both? Neither?
2. **Whether anyone is watching.** Cache savings only count if someone checks the dashboards.

A PM who owns this lesson can walk into a roadmap meeting and say, "caching is on, here are the three things that would break it, and here is the number we are watching to prove it works."

---

## Mental Model: The Subscription Coffee Mug

Think of the Starbucks reusable-mug discount. The first time you buy a coffee, nothing special happens. The second time, if you bring the same mug, you get a discount. If you forget the mug, you pay full price. If the mug is tiny, they do not bother. If the deal has been sitting dormant too long, it expires.

| Coffee shop analogy | Caching analogy |
|--------------------|-----------------|
| Bring the same mug | Send the same prefix |
| Discount on refill | Lower cost on cache read |
| First visit pays normal price | `cache_creation_input_tokens` on first call |
| Each matching visit is cheaper | `cache_read_input_tokens` on follow-up calls |
| Mug too small → no discount | Prefix under 1,024 tokens → no cache |
| Forget the mug once → pay full price | Change a character → cache miss |

The loyalty program only works if the customer (your app) consistently brings the same mug (same prefix).

---

## Product Use Cases

### The Three Highest-Value Targets

| Target | Typical size | Why it is a good caching candidate |
|--------|-------------|-----------------------------------|
| Large system prompt | ~6K tokens | Defines the product persona; stable across every call. |
| Tool schemas | ~1.7K tokens | Tool definitions do not change mid-session. |
| Repeated message content | Varies | Any workflow that re-sends the same chunks (document Q&A, rolling chat history). |

### Partial Hits as a Product Win

Because tools, system prompt, and messages cache independently, a product team can:

- **Tune the system prompt** (maybe the weakest-performing layer) while leaving the tools layer untouched — and keep the cache savings on tools.
- **Add a new tool** and know that only the tools layer takes a cache-write hit; the system prompt cache stays warm.
- **Deploy A/B tests at the system-prompt layer** with a clear idea of the cost impact: one group pays cache-write on the new prompt, the other continues reading from the cached version.

This granularity means caching does not have to be an "all or nothing" gate on experimentation.

---

## PM Decision Framework

When scoping caching in a real launch:

| Question | Why it matters |
|----------|---------------|
| Which layer (tools / system / messages) owns the biggest stable chunk? | That is where you place the first breakpoint; that is where the biggest savings live. |
| Can we commit to freezing that layer for at least a week at a time? | Constant edits destroy the savings; stability is the contract. |
| Who owns the "is the cache actually working?" dashboard? | Without someone watching `cache_read_input_tokens`, the savings are invisible and claim-only. |
| What is the expected hit rate? | Use this to set a target (e.g., "after launch, 70% of non-first calls should be cache reads"). |
| How will we notify the team before a cache-invalidating change? | A quick Slack message before a system-prompt rewrite saves a surprise spike in the cost chart. |

---

## Business Metrics to Watch

| Metric | What to track |
|--------|---------------|
| **Cache hit rate** | `cache_read_input_tokens / (cache_read + cache_creation)` — higher is better. |
| **Cost per conversation** | Should drop after caching ships; compare against a baseline period. |
| **Time-to-first-token** | Should drop on cached requests; good for any latency-sensitive UX. |
| **Cache invalidation events** | Count how many system-prompt / tool edits land per week; if it is too high, savings will never materialize. |
| **TTL-expiry misses** | If most first calls after idle hours show `cache_creation_input_tokens`, your usage pattern may be below the 1-hour frequency threshold. |

---

## Common PM Mistakes

1. **Launching caching without dashboards** — if you cannot see `cache_read_input_tokens`, you cannot tell finance whether caching paid off.
2. **Letting copy teams edit the system prompt weekly without a heads-up** — every rewrite is a 1-hour cache reset. Establish a change process.
3. **Ignoring partial hits** — teams often think "we changed the system prompt, caching is broken" when in reality the tools layer is still hitting. Partial hits are normal and valuable.
4. **Celebrating first-call savings** — the first call is always a cache *write*, which costs *more*, not less. Savings only accrue on follow-up calls within the hour.
5. **Not communicating the 1-hour TTL to ops / on-call** — if overnight traffic drops, the morning's first calls will all be cache-writes, and the cost chart will look weird.
6. **Mixing caching with memory expectations** — stakeholders sometimes hear "cache" and assume Claude is remembering things. It is not. Clarify: caching is cost/latency, not product memory.

---

> **Key Insight**
>
> Caching in action is less about flipping a switch and more about **owning a stability contract**. The product team decides what stays frozen; the platform writes the `cache_control` markers; the observability layer reports `cache_read_input_tokens` vs. `cache_creation_input_tokens`. If any of those three pieces is missing, the launch does not actually save money — it just claims to.

---

## CCA Exam Relevance

- **D5 (Enterprise Deployment)** — expect scenarios where caching is enabled but no savings are seen; the answer is usually a product-level cause (system prompt being edited, variable content in the prefix, partial hits misread as full misses).
- Know that `cache_read_input_tokens` is the field that proves a hit; `cache_creation_input_tokens` is the field that shows a write.
- Know that partial hits are expected behavior because tools, system prompt, and messages cache independently.
- Remember the 1-hour TTL and how it interacts with low-frequency traffic patterns.

---

## Flashcards

| Front | Back |
|-------|------|
| What does a PM actually commit to when turning on caching? | That certain layers of context (tools list, system prompt, stable prefixes) will stay byte-identical across calls. |
| Which usage field proves the cache was read on a call? | `cache_read_input_tokens` — the tokens Claude reused from the cache. |
| Which usage field proves the cache was written on a call? | `cache_creation_input_tokens` — the tokens Claude just wrote into the cache. |
| What is a "partial hit" and why is it a good thing for PMs? | A cache hit on one layer (e.g., tools) and a cache write on another (e.g., system prompt). It lets you tune one layer without losing savings on another. |
| Why is the first call after caching ships always more expensive, not less? | Because it is a cache write (`cache_creation_input_tokens`), not a read. Savings begin on follow-up calls within the 1-hour window. |
| Name the three product layers that benefit most from caching. | Large system prompt (~6K tokens), tool schemas (~1.7K tokens), and repeated message content. |
| What happens when the team rewrites the system prompt on a Friday afternoon? | All system-prompt caches are invalidated; every next call pays cache-write until the new prompt stabilizes. |
| Why is a "cache hit rate" dashboard part of the PM checklist? | Because without it, caching claims are unverifiable — the savings cannot be reported to finance without evidence. |
