# Implementing the RAG Flow — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Architecture (22%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 1.3 (context management), 5.2 (production search infrastructure) |
| Source | building-with-the-claude-api / 05-rag / Lesson 49 |

---

## One-Liner

Implementing RAG is a five-step pipeline: chunk text, embed chunks, store vectors alongside original content, embed the user query, and search by cosine similarity — turning semantic retrieval into a concrete, reproducible code path.

---

## The Five-Step RAG Pipeline

```
┌──────────┐  1. chunk_by_section  ┌──────────┐
│ report   │ ────────────────────▶ │  chunks  │
│  .md     │                        └────┬─────┘
└──────────┘                             │
                                         ▼
                               2. generate_embedding(chunks)
                                         │
                                         ▼
                               3. VectorIndex.add_vector(
                                       embedding,
                                       {"content": chunk})
                                         │
                   ┌─────────────────────┘
                   ▼
        4. user_embedding = generate_embedding(question)
                   │
                   ▼
        5. store.search(user_embedding, k=2)
                   │
                   ▼
         [(doc, distance), ...]
```

The entire RAG concept — "find relevant text before answering" — collapses to these five deterministic steps. There is nothing magical about the retrieval side; the magic lives in the embedding model that maps text to a meaningful vector space.

---

## Step 1: Chunking the Text

```python
with open("./report.md", "r") as f:
    text = f.read()

chunks = chunk_by_section(text)
chunks[2]  # Test to see the table of contents
```

The `chunk_by_section` function (introduced in an earlier lesson) splits the document into logical sections. Each chunk becomes an independently retrievable unit. The chunking strategy matters: too small and you lose context; too large and embeddings become diluted and less discriminative.

---

## Step 2: Generate Embeddings in Batch

```python
embeddings = generate_embedding(chunks)
```

The embedding helper accepts both a single string and a list of strings, so you can embed the whole corpus in a single call. This matters in production because embedding APIs typically charge per request and benefit from batching — one batched call is much cheaper and faster than N individual calls.

---

## Step 3: Store in the Vector Database

```python
store = VectorIndex()

for embedding, chunk in zip(embeddings, chunks):
    store.add_vector(embedding, {"content": chunk})
```

Notice the payload: `{"content": chunk}`. The vector is only half the record — the other half is the original text (or a reference to it). Without that, a nearest-neighbor search returns meaningless floats and you cannot feed anything useful back to Claude.

### Why Store the Original Text?

At query time you need to return real content that goes into the prompt. The embedding vector is only a key into the index; the value must contain human-readable text. Variations include:

- Full chunk text (simplest)
- A pointer (doc_id + offset) to reconstruct lazily
- Text plus metadata (section title, source URL, timestamp)

---

## Step 4: Embed the User Query

```python
user_embedding = generate_embedding(
    "What did the software engineering dept do last year?"
)
```

Critically, the **same embedding model** must be used for both the corpus and the query. Mixing models produces incompatible vector spaces and similarity scores become meaningless.

---

## Step 5: Search by Cosine Distance

```python
results = store.search(user_embedding, 2)

for doc, distance in results:
    print(distance, "\n", doc["content"][0:200], "\n")
```

`store.search(query_vector, k)` returns the top-k nearest documents along with their distances. Lower distance = higher similarity. In the lesson's example:

- Section 2 (Software Engineering) → distance 0.71 (closest)
- Methodology section → distance 0.72 (second closest)

The ordering is what you hand back to Claude as grounded context.

---

## What's Next: The Limits of Pure Semantic Search

The lesson ends with a warning: this basic flow works for clean semantic questions but breaks down when you need **exact term matching** (incident IDs, product SKUs, error codes). That limitation is what motivates BM25 and hybrid retrieval in the next lessons.

---

## Common Mistakes

1. **Storing embeddings without the source text** — you lose the ability to hand real content back to Claude.
2. **Using different embedding models for corpus and query** — vector spaces do not match and similarity scores are meaningless.
3. **Skipping batch embedding** — calling `generate_embedding` per chunk is slow and expensive in production.
4. **Ignoring chunk size** — oversized chunks dilute relevance; undersized chunks lose context.
5. **Returning distances to the user** — distances are debug signal, not product output. Return content, log distances.

> **Key Insight**
>
> The RAG pipeline is a **deterministic preprocessing + lookup** job, not an AI feature in itself. The intelligence lives entirely in (a) the embedding model that maps meaning to geometry and (b) the downstream LLM that reasons over retrieved chunks. Keep the pipeline boring and the quality will come from the components you can swap out independently.

---

## CCA Exam Relevance

- **D1 (Agentic Architecture)**: RAG is one of the canonical context-management patterns. Expect questions that frame RAG as "how do I give Claude knowledge it does not have?"
- **D5 (Enterprise Deployment)**: vector store selection, embedding cost, batch processing, and pipeline freshness are production concerns that appear under deployment/scale questions.
- Watch for distractors that suggest fine-tuning as the answer to "Claude does not know our internal docs." RAG is almost always the correct production choice.

---

## Flashcards

| Front | Back |
|-------|------|
| What are the five steps of the RAG flow? | 1) Chunk the text, 2) embed each chunk, 3) store embeddings + text in a vector index, 4) embed the user query, 5) search the store for top-k nearest chunks. |
| Why must you store the original text alongside the embedding? | Because at query time you need real content to feed to Claude — embeddings alone are opaque floats. |
| Must the corpus and query use the same embedding model? | Yes. Different models produce incompatible vector spaces, making cosine similarity meaningless. |
| What does `store.search(user_embedding, 2)` return? | A list of (document, distance) tuples — the two nearest chunks with their cosine distances. |
| In the lesson example, what was the closest match for "What did the software engineering dept do last year?" | Section 2 (Software Engineering) with a distance of 0.71. |
| Does lower distance mean higher or lower similarity? | Lower distance = higher similarity (closer in vector space). |
| Why batch embed chunks in one call instead of looping? | Embedding APIs charge per request and batching is dramatically cheaper and lower-latency. |
| What limitation of pure semantic search does the next lesson address? | Exact-term matching for things like incident IDs — semantic search can miss literal token matches. |
