# Prompt Caching — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D5 — Enterprise Deployment (20%) |
| Task Statements | 5.1 (cost/latency optimization), 5.2 (production performance) |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 56 |

---

## One-Liner

Prompt caching is the "bulk discount" of the Claude API — if your product keeps sending the same large chunk of context over and over, you can make every call after the first one noticeably faster and cheaper, with zero user-facing change.

---

## Why PMs Should Care

Every time your app calls Claude, the model re-does a pile of expensive setup work (tokenization, embeddings, context analysis) before it writes a single word of output — and then throws that work away. If your product sends the same 6,000-token system prompt or the same long PDF on every call, you are **paying for and waiting on that setup every single time**.

Prompt caching changes the economics. You pay for the setup once, then get the same setup "for free" (cheaper and faster) on every follow-up call within an hour. For any product doing repeat interactions over stable context, this is the biggest single lever on unit economics and perceived speed.

---

## Mental Model: The Coffee Shop Pour-Over

Imagine a pour-over coffee shop that grinds beans fresh for every order:

| Step | Without caching | With caching |
|------|----------------|--------------|
| First customer orders an Ethiopia pour-over | Grind beans, heat water, brew | Grind beans, heat water, brew (pay full cost) |
| Second customer orders the same thing | Grind beans again, heat water again, brew | Reuse the pre-ground beans and hot water (pay only for the brew) |

The grinding and water-heating are the preprocessing. The brewing is the actual generation. Prompt caching means you stop re-grinding identical orders. The customer still gets a fresh cup — they just get it faster and the shop's margins go up.

---

## Product Use Cases

### When Caching Pays Off

| Scenario | Why it works |
|----------|-------------|
| Chat product with a long system persona / guidelines | The persona is identical on every turn — cache it once. |
| Document Q&A (ask many questions about one PDF) | The document is stable; only the question varies. |
| Coding assistant with a big repo context | The codebase context is sent on every request. |
| Agent loop with fixed tool definitions | The tool schemas are the same every turn. |
| Iterative content editing (same draft, many edits) | The draft is constant, the instructions change. |

### When Caching Does NOT Help

| Scenario | Why it does not help |
|----------|---------------------|
| One-off prompts (no repeats) | You pay the cache-write cost for nothing. |
| Prompts that always change | Cache never hits; nothing to reuse. |
| Very low-frequency usage (calls hours apart) | Cache expires after an hour — entries are gone before reuse. |
| Tiny prompts | Savings are negligible; overhead is not worth the complexity. |

---

## PM Decision Framework

When deciding whether to turn on prompt caching for a feature:

| Question | Why it matters |
|----------|---------------|
| Is there a large, stable chunk of context sent on every request? | Caching targets large, stable prefixes — that is where the savings live. |
| Do users interact frequently within an hour? | The 1-hour TTL rewards high-frequency repeat usage. |
| Is input token cost a material share of my unit economics? | If yes, caching can move the needle on gross margin. |
| Is perceived latency a top user complaint? | Caching reduces time-to-first-token on cached prefixes. |
| Is the content genuinely identical across calls (byte for byte)? | Caching is extremely sensitive to any change in the cached prefix. |

If most answers are yes, caching should be on the roadmap — likely ahead of other model-side optimizations.

---

## Business Impact

| Metric | Typical effect of prompt caching |
|--------|----------------------------------|
| **Cost per conversation** | Drops — cached prefixes are billed at a significant discount. |
| **Latency / time-to-first-token** | Drops — preprocessing is skipped on cache hits. |
| **Gross margin on AI features** | Rises — the per-call unit cost falls on hot workflows. |
| **User retention (indirect)** | Can rise — faster responses feel snappier and more "polished." |

These are all production wins with no visible product change and no extra user friction. That is rare.

---

## Common PM Mistakes

1. **Treating caching as a "later" optimization** — by the time you notice the bill, you have been paying twice for months of traffic. If your product has any repeat-context pattern, scope caching into v1.
2. **Confusing caching with memory or personalization** — caching is about *reusing computation*, not *remembering the user*. It does not change what Claude knows; it only speeds up what it already processes.
3. **Ignoring the 1-hour TTL in metric modeling** — projecting "x% of calls cached" without checking call frequency will overstate savings on low-traffic features.
4. **Underinvesting in "context stability"** — if your team rewrites the system prompt on every sprint, cache entries get invalidated constantly. Stable context is a pre-requisite.
5. **Not telling finance / ops when caching ships** — the cost curve suddenly bends. Make sure cost models reflect it so forecasts stay honest.

---

> **Key Insight**
>
> Prompt caching is an **invisible product improvement**: users never see it, but they feel it. Lower cost per call protects gross margin, and lower latency improves how snappy the product feels. For any AI feature built on a large stable context, caching is the single highest-leverage optimization a PM can push for — it is pure upside with no UX trade-off.

---

## CCA Exam Relevance

- **D5 (Enterprise Deployment)** — caching sits squarely under task 5.1 (cost and latency). Expect questions that ask how to optimize repeat-context workflows.
- Know that caching reduces **both** cost and latency, not just one.
- Know the 1-hour TTL and that caching only helps when content is reused within that window.
- Watch for scenarios framed as "same long document, many questions" or "same system prompt on every turn" — the answer is prompt caching.

---

## Flashcards

| Front | Back |
|-------|------|
| In plain terms, what does prompt caching do for a product? | It saves and reuses Claude's expensive preprocessing work so repeat calls over the same context are faster and cheaper. |
| What is the 1-hour rule PMs must remember? | Cached content lives for one hour; after that it expires and must be recreated. |
| Which two business metrics does caching move? | Cost per call (down) and latency / time-to-first-token (down). |
| Which product patterns benefit most from caching? | Large stable system prompts, document Q&A, coding assistants with repo context, agent loops with fixed tools, iterative editing. |
| Which products do NOT benefit from caching? | One-off prompts, content that always changes, low-frequency usage (calls more than an hour apart), tiny prompts. |
| Is caching automatic? | No — it must be explicitly enabled; without opt-in Claude throws preprocessing away. |
| Does caching change what Claude "knows" about the user? | No — it only reuses computation. It is not memory or personalization. |
| Why should caching be scoped into v1, not "later"? | Because every week without it is a week of paying twice on repeat-context traffic; the savings never accrue retroactively. |
