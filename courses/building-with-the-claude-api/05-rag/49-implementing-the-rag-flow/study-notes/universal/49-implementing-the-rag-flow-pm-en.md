# Implementing the RAG Flow — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Architecture (22%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 1.3 (context management), 5.2 (production search infrastructure) |
| Source | building-with-the-claude-api / 05-rag / Lesson 49 |

---

## One-Liner

RAG turns a pile of private documents into a product feature — the five-step flow (chunk, embed, store, embed query, search) is the smallest investment that makes Claude "know your company."

---

## Mental Model: The Librarian With Sticky Notes

Imagine hiring a brilliant research assistant who knows everything publicly available but has never seen your internal wiki. You cannot reasonably ask them to read 10,000 pages before every question.

Instead, you:

1. Cut the wiki into topic-sized notes (**chunk**).
2. Tag each note with a colored sticker that captures its meaning (**embed**).
3. File the notes by color in a giant wall organizer (**vector store**).
4. When a user asks a question, you put a matching colored sticker on the question (**query embedding**).
5. Walk to the wall and grab the notes whose stickers are closest (**similarity search**).

The assistant then reads only those few notes to answer — fast, accurate, grounded in the actual wiki.

---

## Why PMs Should Care

RAG is the default answer for any product requirement that sounds like:

- "The assistant should know our internal documentation."
- "It should answer questions about our product catalog."
- "Customer support agents should see relevant past tickets."
- "The tool should reference company policies when replying."

Without RAG, Claude gives generic answers. With RAG, Claude gives answers grounded in **your company's source of truth** — and the answer updates the moment the underlying document updates.

---

## Product Use Cases

### When RAG Is the Right Call

| User Need | Why RAG Fits |
|-----------|--------------|
| "Ask our knowledge base" assistants | Corpus is large, queries are varied, freshness matters |
| Customer support deflection | Agents ground answers in current help articles |
| Internal wiki / onboarding copilots | Employees ask unstructured questions about known documents |
| Product catalog search ("find me a laptop under $1,500") | Semantic intent over specs |
| Contract / policy lookup | Large legal corpus, specific retrieval per query |

### When RAG Is Overkill or Wrong

| User Need | Better Alternative |
|-----------|--------------------|
| Generic chat or brainstorming | Base model is fine |
| Exact lookups by unique ID | Use a normal database query, not vector search |
| Real-time data (prices, inventory) | Use tool use, not a stale index |
| Tiny corpus (< a few pages) | Just paste it into the system prompt |

---

## The Five Steps in Plain English

1. **Chunk** — break each document into bite-sized sections.
2. **Embed** — convert each section into a vector that captures its meaning.
3. **Store** — save the vectors alongside the original text in a searchable index.
4. **Embed the question** — convert the user's query into the same kind of vector.
5. **Search** — return the most similar chunks to hand to Claude as context.

The product insight: steps 1–3 are **batch preprocessing** (you pay once), and steps 4–5 run on every user query (you pay per-request).

---

## PM Decision Framework

| Question | If Yes | Implication |
|----------|--------|-------------|
| Do you have a corpus bigger than the context window? | Yes | RAG is required. |
| Does content update more than once a month? | Yes | Budget for an ingestion/refresh pipeline. |
| Do users ask semantic questions (not exact lookups)? | Yes | Vector search is the right retrieval mode. |
| Do users also ask for specific IDs / SKUs / error codes? | Yes | Plan for hybrid search (next lessons). |
| Is the corpus confidential? | Yes | Evaluate vector store hosting (self-host vs cloud) for compliance. |

---

## Cost & Freshness Reality Check

RAG has three recurring cost centers. PMs routinely under-budget them:

- **Embedding cost**: every chunk embedded once; every query embedded every time. Scales with corpus and traffic.
- **Storage cost**: vector indexes grow with corpus size and chunk count. Plan for index rebuild cost.
- **Ingestion/refresh latency**: if your docs update daily, the index is stale by end of day unless you run a refresh job. Decide the SLA up front.

Good PM hygiene: a "RAG freshness SLA" line in the PRD — e.g., "knowledge base answers are never more than 24 hours stale."

---

## Common PM Mistakes

1. **Promising real-time knowledge when the index refreshes nightly** — users spot stale answers within days.
2. **Ignoring chunking strategy** — bad chunking silently degrades answer quality and is blamed on "Claude being dumb."
3. **Shipping without eval** — you need a test set of questions + expected citations before launch to catch regressions.
4. **Not logging retrieved chunks** — when users report bad answers you cannot debug without seeing what was retrieved.
5. **Assuming semantic search handles exact lookups** — it often misses IDs and codes. Hybrid search (BM25 + semantic) is usually needed.

> **Key Insight**
>
> RAG is not a model feature — it is a **data pipeline product decision**. Your quality ceiling is set by corpus curation, chunking strategy, and freshness SLA, not by the model. PMs who treat RAG like "magic Claude knows our docs" under-invest in the pipeline and ship disappointing features.

---

## CCA Exam Relevance

- **D1 (Agentic Architecture)**: recognize RAG as the canonical pattern for extending Claude's knowledge beyond training data.
- **D5 (Enterprise Deployment)**: know the cost and freshness trade-offs of running a vector index in production.
- Exam pattern: "Claude does not know our internal documents — what pattern do we use?" → RAG.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the librarian-with-sticky-notes analogy for RAG? | Cut the wiki into notes, tag each with a meaning-sticker, file by color, match the user's question to the same kind of sticker, grab the nearest notes. |
| When is RAG the wrong tool? | Exact ID lookups (use DB), real-time data (use tool use), or tiny corpora (paste into system prompt). |
| Which RAG steps are batch preprocessing vs per-request? | Chunk, embed, store are preprocessing (pay once). Embed query + search run per user request. |
| What must be in the PRD for any RAG feature? | Freshness SLA, eval set, retrieval logging, cost budget for embeddings + vector store. |
| Why does chunking strategy matter for PMs? | Bad chunking silently degrades answers and looks like "model is dumb" — it is actually a pipeline bug you own. |
| What is the smallest unit that makes Claude "know your company"? | The five-step RAG flow: chunk, embed, store, embed query, search. |
| How often should you refresh a RAG index? | As often as the underlying docs change; the SLA is a PM decision in the PRD. |
| What do you do when users ask for exact IDs inside a RAG feature? | Plan for hybrid search — combine BM25 lexical search with semantic search (covered in next lessons). |
