# Rules of Prompt Caching — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D5 — Enterprise Deployment (20%) |
| Task Statements | 5.1 (cost/latency optimization), 5.2 (production performance) |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 57 |

---

## One-Liner

Prompt caching has a rulebook you must follow to get any discount: opt in explicitly, keep cached content byte-identical, meet a 1,024-token minimum, and budget your four available "cache cuts" like a scarce resource.

---

## Why PMs Should Care About the Rules

Engineering can turn on caching, but only a product-level decision about **what stays stable** actually makes caching pay off. If your product rewrites the system prompt every sprint, or lets users reorder tool definitions, or inserts the user's question into the middle of a "template," the cache breaks and the savings disappear.

In other words: the rules of caching are really rules about **how stable your context is** — and that is a product decision, not an engineering one.

---

## Mental Model: The Stamp-and-Ship Line at a Warehouse

Think of a shipping warehouse where boxes are stamped with labels. Every box moving down the conveyor belt has the same big company logo on the first three sides (stable) and a unique customer address on the fourth side (variable).

| Layer | Warehouse analogy | Caching analogy |
|-------|------------------|-----------------|
| Pre-stamped logo | A rubber stamp with the company logo | Tools + system prompt + stable context |
| Custom label | Hand-written customer address | User's specific question |
| Rule | The logo must be identical — smudge one letter and you reprint the whole side | Cached prefix must match byte-for-byte |
| Batch size rule | You can't pre-stamp tiny shipping slips — only full-size boxes | Minimum 1,024 tokens before the breakpoint |
| Cut-line rule | Only four stamping stations on the line | Up to four cache breakpoints per request |

The "stamp" only saves effort when everything to the left of it stays identical. The moment the stamp changes, you reprint everything.

---

## Product Use Cases

### Product Patterns That Survive the Rules

| Pattern | Why it fits the rules |
|---------|----------------------|
| Chat product with a locked system persona | Stable prefix → byte-exact on every turn |
| Coding assistant with versioned tool schemas | Tools only change between deploys, not mid-session |
| Document Q&A with a canonical PDF | Document is stable; only the user's question varies (and sits after the breakpoint) |
| Agent loop with a fixed toolbox | Tools + system prompt form a stable cacheable prefix every turn |

### Product Patterns That Break the Rules

| Pattern | Why it breaks |
|---------|--------------|
| "Personalized greeting" injected at the top of every prompt | User name is variable → cache miss every turn |
| A/B test that rewrites the system prompt per user | Prefixes differ → no one benefits from caching |
| Short prompts (< 1,024 tokens) | Below the floor → caching is a no-op |
| Feature that lets users reorder tool descriptions | Byte order changes → cache invalidated |

---

## PM Decision Framework

Before you scope caching into a feature, run through this checklist:

| Question | Why it matters |
|----------|---------------|
| Is there a stable chunk of context at least 1,024 tokens long? | Below this, the cache does nothing. |
| Can I guarantee that stable chunk sits at the *start* of the request? | The breakpoint cuts a prefix; variables must live *after* it. |
| Am I using fewer than 4 independent caching layers? | 4 is the hard cap — plan the budget. |
| Can I commit to keeping that prefix byte-exact across releases? | Even a whitespace rewrite breaks the cache. |
| Is the context reused within an hour? | TTL is 1 hour — cold features waste cache writes. |
| Do I know what changes when — so I can place breakpoints where they minimize invalidation? | Cache boundaries should align with change frequency. |

If you cannot answer "yes" to the first four, caching will underperform — or silently do nothing.

---

## Common PM Mistakes

1. **Treating caching as an engineering flag to flip** — it is actually a *context stability contract*. Product decisions determine whether the cache ever hits.
2. **Injecting variable content into the prefix** — putting the user's name, timestamp, or session ID at the top of the system prompt destroys cache hits on every call. Move variables to the end.
3. **Rewriting system prompts casually** — every copy edit invalidates the cache. Treat the cached system prompt like a versioned asset with a change log.
4. **Ignoring the 1,024-token floor in small features** — "We added caching but cost didn't drop" is often because the prefix was too short to qualify.
5. **Using all 4 breakpoints too early** — a feature that consumes the full breakpoint budget leaves no headroom for later optimizations. Keep one spare.
6. **Not communicating cache invalidation events** — a single "polish pass" on the system prompt can reset cache savings across the whole fleet for an hour. Everyone should know when that happens.

---

> **Key Insight**
>
> The rules of prompt caching are really a contract about *what your product promises to keep stable*. A good PM reads this lesson and asks, "Which parts of my prompts, tools, and context can I genuinely freeze?" That answer — not the engineering flag — determines whether caching delivers its advertised savings.

---

## CCA Exam Relevance

- **D5 (Enterprise Deployment)** — expect questions that test the mechanical rules: manual opt-in, byte-exact matching, 1,024-token floor, 4-breakpoint cap, 1-hour TTL, tools → system → messages ordering.
- Watch for scenarios where a PM is told "caching is on but we see no savings" — the answer is almost always a rule violation (e.g., variable content in the prefix, under-threshold content, or a casual edit to the system prompt).
- Know that system prompts and tool definitions are the *best* caching targets because they sit at the front of the processing order and rarely change.

---

## Flashcards

| Front | Back |
|-------|------|
| Is prompt caching automatic from a PM perspective? | No — engineering must explicitly opt in per block, and product must keep the content stable for it to pay off. |
| What minimum content length unlocks caching? | 1,024 tokens of cumulative content before and including the cache breakpoint. |
| How many cache breakpoints can a single request use? | Up to four. |
| Why does the user's question belong *after* the breakpoint, not before? | Because the cached prefix must be byte-identical; variable content in the prefix guarantees a cache miss. |
| What product layers are the best caching targets? | System prompts and tool definitions — large, stable, always first in the processing order. |
| What breaks a cache hit even though nothing "meaningful" changed? | Any whitespace edit, typo fix, added "please," or reordering of tool entries — caching is byte-exact. |
| Why should a PM care about the 1-hour TTL? | Low-frequency features expire their own cache entries before reuse, so caching yields nothing for them. |
| What is the PM's real job with prompt caching? | To guarantee context stability — the rules only pay off if product commits to keeping the cached prefix frozen. |
