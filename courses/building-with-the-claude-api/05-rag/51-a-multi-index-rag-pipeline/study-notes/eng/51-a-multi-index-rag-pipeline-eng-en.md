# A Multi-Index RAG Pipeline — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Architecture (22%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 1.3 (context management), 5.2 (production search infrastructure) |
| Source | building-with-the-claude-api / 05-rag / Lesson 51 |

---

## One-Liner

A multi-index RAG pipeline wraps `VectorIndex` and `BM25Index` behind a single `Retriever` that forwards queries to both and merges results via reciprocal rank fusion — turning two independent search systems into one hybrid retrieval layer.

---

## The Multi-Index Architecture

Both `VectorIndex` and `BM25Index` already share nearly identical APIs — `add_document()` and `search()`. That consistency is what makes a clean wrapper possible:

```
                       ┌─────────────┐
  add_document() ────▶ │             │ ────▶ VectorIndex.add_document
                       │  Retriever  │ ────▶ BM25Index.add_document
  search(query)  ────▶ │             │
                       │             │ ────▶ VectorIndex.search
                       │             │ ────▶ BM25Index.search
                       └──────┬──────┘
                              │  reciprocal rank fusion
                              ▼
                       merged top-k results
```

The `Retriever` is a thin coordinator. It broadcasts writes to every underlying index and, on read, fans out the query to all indexes and merges the rankings into a single sorted list.

---

## Understanding Reciprocal Rank Fusion (RRF)

Merging results from different search methods is harder than it looks. Each method has its own scoring system — BM25 scores are not comparable to cosine distances. You cannot just union the two result lists or average their scores.

The trick is to ignore the raw scores and use **rank** (position in each list) instead. Reciprocal rank fusion formalizes this:

```
RRF_score(d) = Σ  1 / (k + rank_i(d))
              i
```

Where:

- `d` is a document
- `i` indexes each ranking source (VectorIndex, BM25Index, ...)
- `rank_i(d)` is the 1-based rank of document `d` in ranking `i`
- `k` is a smoothing constant (often 60; the lesson uses 1 for clearer results)

Documents that rank highly in **multiple** indexes accumulate more score and rise to the top. Documents that rank highly in only one are not disqualified but are penalized.

### Worked Example

Searching for "INC-2023-Q4-011":

- VectorIndex returns: Section 2 (rank 1), Section 7 (rank 2), Section 6 (rank 3)
- BM25Index returns: Section 6 (rank 1), Section 2 (rank 2), Section 7 (rank 3)

With `k = 1`:

- Section 2: `1/(1+1) + 1/(1+2) = 0.5 + 0.333 = 0.833`
- Section 7: `1/(1+2) + 1/(1+3) = 0.333 + 0.25 = 0.583`
- Section 6: `1/(1+3) + 1/(1+1) = 0.25 + 0.5 = 0.75`

Final merged ranking: **Section 2 (0.833) > Section 6 (0.75) > Section 7 (0.583)**.

Intuitively: Section 2 ranked well in both lists, so it wins. Section 6 ranked #1 in BM25 but #3 in vectors, and still beats Section 7 which was only mid-ranked everywhere.

---

## The Retriever Class

```python
class Retriever:
    def __init__(self, *indexes: SearchIndex):
        if len(indexes) == 0:
            raise ValueError("At least one index must be provided")
        self._indexes = list(indexes)

    def add_document(self, document: Dict[str, Any]):
        for index in self._indexes:
            index.add_document(document)

    def search(self, query_text: str, k: int = 1, k_rrf: int = 60):
        # Get results from all indexes
        all_results = []
        for idx, results in enumerate(all_results):
            for rank, (doc, _) in enumerate(results):
                # Track document ranks across indexes
                # Apply RRF scoring formula
        # Return merged and sorted results
```

Key design points:

- **Variadic indexes** — `*indexes: SearchIndex` lets the Retriever accept any number of concrete index implementations. At least one must be supplied.
- **Broadcast writes** — `add_document` simply forwards the same payload to every index. Each index stores it in its own format (vector for `VectorIndex`, raw text for `BM25Index`).
- **Unified search** — callers only interact with `Retriever.search(query_text, k)`. They never know or care which underlying indexes exist.
- **Configurable `k_rrf`** — the RRF smoothing constant is exposed as a parameter with a default (60 is a common textbook value; the lesson uses 1 for demonstration clarity).

The key insight is that by keeping the API consistent across every search implementation, combining them becomes a trivial wrapper rather than a tangled integration.

---

## Testing the Hybrid Approach

Recall the earlier problem: pure vector search for "what happened with INC-2023-Q4-011?" returned the cybersecurity incident first but then the wrong second result (financial analysis) instead of the software engineering section.

With the hybrid Retriever, the output becomes:

1. Section 10: Cybersecurity Analysis — Incident Response Report (most relevant)
2. Section 2: Software Engineering — Project Phoenix Stability Enhancements (second most relevant)
3. Section 5: Legal Developments (third)

This matches intuition: both sections that actually mention the incident rise to the top, and the spurious financial section drops out because BM25 does not give it any literal-token support.

---

## Extensibility: The SearchIndex Protocol

Every index — present or future — implements the same `SearchIndex` protocol: `add_document()` and `search()`. That means the Retriever is automatically compatible with any new search methodology you bolt on:

- A keyword-based index
- A graph-based search over a knowledge graph
- A specialized domain index (e.g., symbol search for code)
- A recent-documents index that prioritizes freshness

Just implement the two methods and pass an instance to `Retriever(...)`. RRF handles the fusion automatically. This modular approach keeps each search implementation focused and testable while providing a clean combination point.

---

## Common Mistakes

1. **Merging by raw scores** — BM25 scores and cosine distances are not comparable. Always use rank-based fusion (RRF), not score arithmetic.
2. **Ignoring the `k` constant** — `k` in the RRF formula is not the same as the top-k of the search result. Confusing them leads to miscalibrated scores.
3. **Assuming more indexes always help** — each new index adds latency and compute. Add only indexes that demonstrably improve eval metrics.
4. **Broadcasting writes without deduplication** — if the same document is added twice to the Retriever, each underlying index sees two copies. Deduplicate at ingest.
5. **Forgetting to pass `k_rrf` through the API** — defaults are fine for most cases but production eval may require tuning.

> **Key Insight**
>
> Reciprocal rank fusion is the trick that makes multi-index retrieval "just work." It sidesteps the incompatibility between different scoring systems by ranking-only arithmetic. Combined with a consistent `SearchIndex` protocol, it lets you treat hybrid retrieval as a composition problem rather than an integration problem.

---

## CCA Exam Relevance

- **D1 (Agentic Architecture)**: hybrid retrieval and rank fusion are the canonical advanced RAG patterns. Expect questions about combining search modalities.
- **D5 (Enterprise Deployment)**: modular retriever design is a production concern — knowing how to scale by adding independent indexes without tearing out the retrieval layer.
- Exam pattern: "You have a semantic index and a BM25 index with incompatible scores — how do you merge their results?" → Reciprocal rank fusion over the per-index ranks.

---

## Flashcards

| Front | Back |
|-------|------|
| What does the Retriever class do? | Wraps multiple `SearchIndex` implementations behind a single `add_document` / `search` API, broadcasting writes and merging reads via RRF. |
| Why can't you merge BM25 and cosine scores directly? | They use incompatible scoring systems — you must rank-normalize instead. |
| What is the RRF formula? | `RRF_score(d) = Σ 1 / (k + rank_i(d))` — sum, across all rankings i, of the reciprocal of (k plus the document's rank in that ranking). |
| What is the `k` constant in RRF, and what value does the lesson use? | A smoothing constant — often 60 in practice, but the lesson uses 1 for clearer demonstration math. |
| In the worked example, why did Section 2 win? | It ranked #1 in VectorIndex and #2 in BM25, scoring 0.833 under RRF — the highest combined score. |
| What two methods define the SearchIndex protocol? | `add_document(dict)` and `search(query, k)`. |
| How does the Retriever handle adding new index types later? | Any class implementing `add_document` and `search` drops in unchanged — RRF handles fusion automatically. |
| How did the hybrid Retriever fix the earlier problematic query result? | The wrong "financial analysis" section dropped out, and the two sections actually mentioning the incident ID rose to the top. |
