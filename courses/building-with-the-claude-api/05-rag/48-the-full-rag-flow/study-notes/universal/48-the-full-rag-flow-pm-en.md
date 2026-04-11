# The Full RAG Flow — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Architecture (22%) — primary; D4 — Safety & Alignment (20%) — secondary |
| Task Statements | 1.3 (context management), 4.1 (grounded responses) |
| Source | building-with-the-claude-api / 05-rag / Lesson 48 |

---

## One-Liner

The full RAG flow has six steps, cleanly split into a one-time preprocessing pipeline and a per-query pipeline — understanding this split is how PMs reason about cost, latency, and content freshness in any RAG feature.

---

## Mental Model: A Library Card Catalog

Think of a library before a user walks in:

| Stage | Library Analogy | RAG Step |
|-------|-----------------|----------|
| Setup | A librarian reads every book and writes index cards | Chunk + embed + store |
| Waiting | The card catalog sits ready | Vector DB sits populated |
| Question | A visitor asks "books about medieval cooking?" | User query arrives |
| Lookup | Librarian flips through cards to find the closest matches | Embed query + cosine similarity |
| Answer | Librarian hands over the relevant books | Retrieved chunks go into the prompt |
| Synthesis | The visitor reads the books and writes an essay | Claude writes the final answer |

The library only works because someone did the indexing work ahead of time. That is the preprocessing pipeline in RAG. The query-time steps are the librarian greeting each visitor.

---

## The Six Steps in PM Terms

```
[Preprocessing — costs money once per document, benefits every future query]
1. Chunk:       "Cut the document into searchable pieces"
2. Embed:       "Turn each piece into a meaning coordinate"
3. Store:       "File all coordinates in a vector database"

[Query time — costs money per user request]
4. Embed query: "Turn the user's question into a meaning coordinate"
5. Search:      "Find the closest coordinates via cosine similarity"
6. Prompt:      "Hand the question + top matches to Claude for an answer"
```

**Key PM insight**: if you add one document, steps 1-3 run once. If you get a million users asking questions today, steps 4-6 run a million times. Budgeting cost and latency means knowing which step lives in which half.

---

## Why the Split Matters for Product Planning

| Dimension | Preprocessing Side (1-3) | Query-Time Side (4-6) |
|-----------|--------------------------|------------------------|
| Who pays? | Amortized across all future queries | Paid per user request |
| Latency sensitive? | No — runs in the background | Yes — users wait for it |
| Freshness impact | A stale index means stale answers | Always reads latest state of the index |
| Failure blast radius | A bad batch corrupts future retrieval | A bad query harms one user interaction |
| Cost optimization | Fewer re-indexes, batch more aggressively | Smaller top-k, cached embeddings |

Product decisions hit different halves. "We want answers to reflect today's doc update" is a preprocessing problem. "We want answers in under 2 seconds" is a query-time problem.

---

## The "Bug" Example as a Product Lesson

The lesson's toy example uses a medical research chunk containing the word "bug" (as in XDR-47 virus) and a software engineering chunk. A user asks "How many bugs did engineers fix this year?".

A keyword retriever might return the medical chunk because it literally contains "bug". A cosine-similarity retriever correctly returns the software chunk because the query's semantic direction matches the software chunk's semantic direction (cosine similarity 0.983 vs. 0.398).

**This is the product value of RAG done right**: users get the answer they meant, not the answer the keywords would have found. For a support, legal, or enterprise search product, this difference shows up as customer satisfaction.

---

## Cosine Similarity, for PMs

You do not need the math, but you need the intuition:

| Score | Meaning | PM Translation |
|-------|---------|----------------|
| +1.0 | Vectors point the same way | Perfect match |
| ~0.9 | Very similar direction | Confidently relevant |
| ~0.5 | Same general neighborhood | Maybe relevant |
| 0.0 | Perpendicular | No meaningful relationship |
| -1.0 | Opposite directions | Anti-related |

**Cosine distance** is `1 - cosine similarity`. Small distance = high similarity. Product dashboards sometimes show one or the other; know that they are the same metric with opposite polarity.

PMs should ask: "What is our top-k similarity threshold?" and "When the top match has a similarity below X, do we show a 'no good answer' response instead of a fabricated one?"

---

## Product Use Cases

| Scenario | Where the Pipeline Sits |
|----------|-------------------------|
| Customer support copilot | Heavy preprocessing of help articles; fast query-time retrieval |
| Chat-with-your-PDF | User uploads → preprocess on upload → query during conversation |
| Enterprise knowledge search | Continuous re-indexing of Confluence/Drive; high QPS query path |
| Legal research | Large corpus, rare but high-stakes queries; quality over speed |

---

## PM Decision Framework

For any RAG product, be able to answer:

| Question | Which Half | Why |
|----------|-----------|-----|
| How often do docs change? | Preprocessing | Drives re-indexing schedule & cost |
| How big is the corpus? | Preprocessing | Drives storage and embedding cost |
| How many queries per day? | Query time | Drives per-query budget |
| What is the latency SLO? | Query time | Drives top-k, caching, model choice |
| What happens when retrieval has no good match? | Query time | Shapes "no answer" UX to avoid hallucination |
| How do we show citations to users? | Query time | Part of the final-prompt / UI step |
| How do we re-index when a doc changes? | Preprocessing | Must be an owned engineering process |

---

## Common PM Mistakes

1. **Conflating preprocessing and query-time costs** — confusing why RAG is expensive in some scenarios and cheap in others.
2. **No stale-index plan** — users notice when doc updates take days to show up in answers.
3. **Not setting a similarity threshold** — low-confidence matches get treated like high-confidence matches, leading to wrong answers.
4. **No "no answer" UX** — when retrieval finds nothing good, Claude still generates something, and users get a fabrication.
5. **Skipping citations in the UI** — users cannot verify answers, so they cannot catch retrieval failures, so trust erodes silently.

> **Key Insight**
>
> The six-step RAG flow is really two pipelines sharing a vector database. Preprocessing is an investment you make once per document; query time is a recurring cost you pay per user request. PMs who keep these two halves distinct can reason about unit economics, latency budgets, freshness, and failure modes — and that is the difference between a RAG feature that ships and one that quietly breaks in production.

---

## CCA Exam Relevance

- **D1 (Agentic Architecture)**: end-to-end RAG questions will test whether you know the order of the six steps and where cosine similarity fits.
- **D4 (Safety & Alignment)**: the grounding flow — retrieve chunk, wrap in XML tags, hand to Claude — is the canonical hallucination-reduction pattern in the course.
- Know the cosine similarity range (-1 to +1) and the cosine distance relation (1 - cosine similarity).

---

## Flashcards

| Front | Back |
|-------|------|
| What are the two halves of the RAG flow? | Preprocessing (chunk, embed, store — once per document) and query time (embed query, retrieve, prompt — once per user request). |
| What is the library analogy for RAG? | A librarian indexes books ahead of time; when a visitor asks a question, the librarian looks up the closest index cards and hands over the relevant books. |
| What is cosine similarity's range? | -1 to +1. |
| What does a cosine similarity of 0.983 mean? | Extremely high similarity — the two vectors point in almost the same direction. |
| In the "bug" example, what was the similarity score difference? | Query to software chunk = 0.983; query to medical chunk = 0.398. |
| Why do PMs care about the preprocessing / query-time split? | It determines how cost, latency, freshness, and failure modes behave in production. |
| What is cosine distance? | `1 - cosine similarity` — a reporting convention where small values mean high similarity. |
| Name a product decision driven by the query-time half. | Latency SLO, top-k size, "no answer" UX, caching strategy. |
| Name a product decision driven by the preprocessing half. | Re-indexing schedule, chunking strategy, embedding provider choice, corpus size budget. |
