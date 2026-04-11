# A Multi-Index RAG Pipeline — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Architecture (22%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 1.3 (context management), 5.2 (production search infrastructure) |
| Source | building-with-the-claude-api / 05-rag / Lesson 51 |

---

## One-Liner

A multi-index RAG pipeline is the architectural pattern that lets you keep adding search capabilities (semantic, keyword, recency, domain-specific) without re-architecting — giving your product room to grow retrieval quality as you learn what your users actually ask.

---

## Mental Model: The Panel of Expert Judges

Imagine a cooking competition with three judges: a flavor expert, a presentation expert, and a technique expert. Each scores dishes on a completely different scale — stars, letters, percentages. You cannot just average their scores; the numbers are not comparable.

Instead, you ask each judge to **rank** the dishes: 1st, 2nd, 3rd. Then a dish that ranks high with multiple judges rises to the top overall, even if no single judge's raw score would have picked it.

This is exactly what reciprocal rank fusion does for search:

- **Vector search** is the "flavor" judge — understands meaning.
- **BM25** is the "ingredients label" judge — checks literal match.
- Future indexes are new judges — recency, domain, graph — each with their own perspective.

The Retriever is the head judge who collects rankings and produces a fair final score.

---

## Why PMs Should Care

Multi-index retrieval is the point where RAG goes from a prototype to a scalable product. It matters because:

- **Growth path is built in** — you add new retrieval signals (freshness, popularity, domain) without touching the rest of the product.
- **Quality compounds** — each new index catches what the previous ones miss; compounded quality beats any single retrieval method.
- **Failure modes isolate** — if one index degrades, the others still serve. That is operationally precious.
- **Eval becomes tractable** — you can A/B test indexes independently (add one, measure, keep or drop).

---

## Product Use Cases

### When a Multi-Index Retriever Pays Off

| User Need | Why Multiple Indexes Help |
|-----------|---------------------------|
| Mixed conceptual + literal queries | Semantic + BM25 cover both |
| Freshness matters ("what's new this week?") | Add a recency index alongside the existing two |
| Multi-domain knowledge base | Add a domain-routing index that boosts specialist docs |
| Long-tail queries ("unusual product names") | Lexical index catches what semantic misses |
| Legal / compliance with both themes and exact wording | Hybrid is the only reliable answer |

### When Multi-Index Is Overkill

| User Need | Better Alternative |
|-----------|--------------------|
| Tiny corpus (<100 docs) | One index is plenty; ops overhead dominates |
| Only conceptual questions, ever | Pure semantic is fine — measure before adding more |
| Tight latency budget (<100ms) | Each extra index adds latency; measure trade-off |
| Early-stage MVP | Ship semantic-only, then add BM25 when real queries demand it |

---

## Reciprocal Rank Fusion in Plain English

Imagine each search method gives you a **top-3 list**. You do not care how confident each method is; you only care about where each document showed up on each list.

- First place on a list = lots of credit
- Second place = less credit
- Third place = a little credit
- Not on a list at all = no credit from that source

Add up a document's credits from every list. The document with the most total credit wins. A document that showed up high in two lists will almost always beat one that showed up high in only one.

That is reciprocal rank fusion. It is a way to merge search results fairly without needing the underlying methods to agree on what a "score" means.

---

## PM Decision Framework

| Question | If Yes | Implication |
|----------|--------|-------------|
| Do users ask both conceptual and literal queries? | Yes | You need hybrid — at least semantic + BM25. |
| Is freshness a product promise? | Yes | Add a recency/time-weighted index. |
| Are there distinct content domains (docs, tickets, code)? | Yes | Consider per-domain indexes and route by query type. |
| Do you have an eval set? | No | Build one first — you cannot tune multi-index without measurement. |
| Is latency budget tight? | Yes | Start with two indexes, measure, then expand. |

---

## Cost, Latency & Operational Trade-offs

Each index you add costs something. A good PM budgets explicitly:

- **Index build cost** — every ingest writes to every index. Budget CPU + memory + storage.
- **Query latency** — each index adds latency, usually in parallel, so total latency is max(per-index latency) + fusion overhead.
- **Ops surface** — every index is a new thing that can break, get stale, or need reindexing.
- **Eval complexity** — adding an index means re-running the eval set to confirm it does not regress existing wins.

Recommended sequence: ship with semantic only → add BM25 when literal queries fail → add recency only if you measurably need freshness → add domain indexes only if the eval set shows routing wins.

---

## Common PM Mistakes

1. **Adding indexes because they sound clever** — without eval, new indexes can hurt quality. Always measure.
2. **Treating RRF as magic** — it only improves quality if each index actually contributes useful rankings. A useless index still costs latency.
3. **Skipping the eval set** — without it, you have no way to know which index changed what, and regressions hide.
4. **Ignoring latency compounding** — each index has a latency cost; a budget of "six indexes in parallel" is not free.
5. **Forgetting user-facing surface** — multi-index retrieval is invisible to users if done right, and they should never see "which index found this chunk." Keep it internal.

> **Key Insight**
>
> Multi-index retrieval is the architecture that lets your RAG product keep improving without rewrites. The Retriever + RRF pattern is a composition contract: every new retrieval signal plugs in cleanly, gets measured independently, and either improves the product or gets removed. That composability is what separates a RAG toy from a RAG platform.

---

## CCA Exam Relevance

- **D1 (Agentic Architecture)**: hybrid retrieval and rank fusion are core advanced RAG patterns.
- **D5 (Enterprise Deployment)**: modular retriever design is how production RAG systems scale without tearing out the retrieval layer.
- Exam pattern: "How do you combine two retrieval systems with incompatible scoring?" → Reciprocal rank fusion on ranks, not scores.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the panel-of-judges analogy for multi-index retrieval? | Each search method is a judge with its own scoring scale; you rank-normalize their opinions and pick the dish that most judges rank high. |
| Why does reciprocal rank fusion use rank instead of raw scores? | Because different search methods use incompatible scoring systems — rank is the only common currency. |
| When should you add a second index to your RAG product? | When your eval set shows conceptual or literal queries are failing that a complementary method would catch. |
| What is the recommended rollout sequence for indexes? | Semantic first → add BM25 when literal queries fail → add recency only if freshness matters → add domain-routing only if eval shows a win. |
| How do new indexes affect latency? | Each adds latency (usually in parallel); total becomes max(per-index) plus fusion overhead. Budget before adding. |
| What is the hidden cost of adding an index? | Ingest compute, storage, ops surface, and eval complexity — not just query latency. |
| What's the biggest PM mistake with multi-index RAG? | Adding indexes without an eval set, so nobody can prove they help or hurt. |
| Is multi-index retrieval visible to end users? | No — it should be fully internal. Users just see "better answers"; they never see which index returned what. |
