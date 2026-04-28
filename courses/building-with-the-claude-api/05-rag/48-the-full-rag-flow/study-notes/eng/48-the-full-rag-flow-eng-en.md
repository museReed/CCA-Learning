# The Full RAG Flow — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Architecture (22%) — primary; D4 — Safety & Alignment (20%) — secondary |
| Task Statements | 1.3 (context management), 4.1 (grounded responses) |
| Source | building-with-the-claude-api / 05-rag / Lesson 48 |

---

## One-Liner

The full RAG flow is a six-step pipeline — chunk → embed → store → embed query → similarity search → prompt Claude — where cosine similarity is the metric that turns "find relevant text" into "find closest vector".

---

## The Six Steps

```
  [Preprocessing — runs once per document]
  1. Chunk source text
  2. Generate embeddings for each chunk
  3. Store embeddings in a vector database
                      │
                      ▼
  [Query time — runs per user request]
  4. Embed the user's query
  5. Find similar embeddings (cosine similarity)
  6. Build final prompt with retrieved chunks → Claude
```

Steps 1-3 are **preprocessing** — they happen ahead of time, once per document. Steps 4-6 are **query time** — they happen on every user request. The split is the whole reason RAG scales: expensive work is done once, cheap work is done per query.

---

## Step 1: Chunk the Source Text

Break each document into manageable chunks. The lesson uses two toy sections:

- Section 1 — Medical Research: *"This year saw significant strides in our understanding of XDR-47, a 'bug' we have not seen before."*
- Section 2 — Software Engineering: *"This division dedicated significant effort to studying various infection vectors in our distributed systems."*

Notice the lexical trap: the medical section uses "bug", and the software section uses "infection vectors". Keyword search would happily cross-wire these. RAG has to do better.

---

## Step 2: Generate Embeddings

Feed each chunk into an embedding model (VoyageAI in this course) and get back a numerical vector.

The lesson uses a **toy two-dimensional model** to make the geometry visible. In this imaginary model:

- Dimension 1 = "how much the text talks about the medical field"
- Dimension 2 = "how much the text talks about software engineering"

The medical chunk embeds as `[0.97, 0.34]` — very medical, but with some software lexical leakage from the word "bug". The software chunk embeds as `[0.30, 0.97]` — heavily software, but with some medical signal from "infection vectors".

Real models use hundreds or thousands of dimensions and are not interpretable per-dimension. The toy model exists only to illustrate what similarity looks like geometrically.

---

## Normalization

Most embedding APIs normalize vectors to unit length (magnitude 1.0). The math is handled automatically; you do not usually do it yourself. After normalization:

- `[0.97, 0.34]` → `[0.944, 0.331]`
- `[0.30, 0.97]` → `[0.295, 0.955]`

You can visualize normalized vectors as points on a unit circle (or unit hypersphere in high dimensions). Normalization is what makes **cosine similarity** and **dot product** equivalent, and it is why vector databases can optimize similarity search.

---

## Step 3: Store in a Vector Database

A vector database is a specialized store optimized for:

- **Storing** long lists of floats
- **Searching** for the vectors closest to a query vector (approximate nearest neighbor)
- **Scaling** to millions or billions of vectors

After this step, preprocessing is done. The pipeline pauses and waits for a user query. All work up to this point is amortized over every future query.

---

## Step 4: Process the User Query

When a user asks *"I'm curious about the company. In particular, what did the software engineering dept do this year?"*, you run the query through the **same** embedding model used for the chunks.

The toy example gives the raw vector `[0.1, 0.89]` — low medical, high software engineering. After normalization: `[0.112, 0.993]`.

Critical: use the same model. And if the provider supports it, use `input_type="query"` here (vs. `input_type="document"` for the chunks in Step 2).

---

## Step 5: Find Similar Embeddings via Cosine Similarity

Send the query vector to the vector database and ask for the closest stored vectors.

### How Cosine Similarity Works

Cosine similarity measures the cosine of the angle between two vectors:

- Range: **-1 to +1**
- Values close to **+1** → high similarity (vectors point in nearly the same direction)
- Values close to **-1** → very different (vectors point in opposite directions)
- **0** → perpendicular (no meaningful relationship)

In the toy example:

| Comparison | Cosine Similarity |
|------------|-------------------|
| Query vs. Software chunk | **0.983** (very high) |
| Query vs. Medical chunk | 0.398 (much lower) |

The vector database returns the software chunk — exactly what the user wanted, despite both chunks containing overlapping vocabulary ("bug", "infection vectors").

### Cosine Distance

You will also see **cosine distance** in vector database docs, defined as `1 - cosine_similarity`. With cosine distance:

- Values close to **0** → high similarity
- Larger values → less similarity

This is often easier to interpret because "distance" intuitively grows as things get less similar. Same underlying math, different reporting convention.

---

## Step 6: Build the Final Prompt

Combine the user's question and the retrieved chunk(s) into a prompt and send it to Claude:

```
Answer the user's question about the financial document.

<user_question>
How many bugs did engineers fix this year?
</user_question>

<report>
## Section 2: Software Engineering
This division dedicated significant effort to studying various infection vectors in our distributed systems
</report>
```

The retrieved chunk is wrapped in XML tags (`<report>`) so Claude knows which part is the user's question and which part is the grounding source. Claude then produces its answer from the combined context.

This is the "generation" half of retrieval-augmented generation. Note that Claude itself never called the vector database — your application did. From Claude's perspective, it received a normal prompt with an unusual amount of carefully selected context.

---

## Why the Lexical Trap Is the Point

The "bug" example is constructed precisely to embarrass keyword search. Both chunks contain disease-like language; a keyword-based retriever would likely return the medical chunk for "how many bugs did engineers fix". Cosine similarity on semantic embeddings handles this correctly because the query's vector direction (software-heavy) is close to the software chunk's direction.

This is why embeddings matter: they measure **semantic** direction, not **lexical** overlap.

---

## CCA Task Annotations

- **Task 1.3 (Context Management)** — the whole RAG flow is a context-management pipeline. Preprocessing decides what is retrievable; retrieval decides what is in-context; prompt assembly decides how Claude sees it.
- **Task 4.1 (Grounded Responses)** — the final prompt grounds Claude's answer in retrieved chunks. Wrapping chunks in XML tags signals "this is source material" to the model.

---

## Common Mistakes

1. **Forgetting to embed the query with the same model used for chunks** — vectors end up in incompatible spaces, similarity scores become meaningless.
2. **Skipping normalization** — if the provider does not normalize, and your database uses dot product, non-normalized vectors produce wrong rankings.
3. **Returning too many chunks** — top-k set too large pads the prompt with low-relevance content that can distract Claude.
4. **No XML/structured tagging in the final prompt** — Claude cannot distinguish question from source material, which weakens grounding.
5. **Not logging retrieval scores in production** — when an answer is wrong, you need the similarity scores of retrieved chunks to debug whether it was a retrieval or a generation problem.

> **Key Insight**
>
> The six-step RAG flow is really two halves glued together: an **offline preprocessing pipeline** (chunk → embed → store) that runs once per document, and an **online query pipeline** (embed query → retrieve → prompt) that runs per request. Every RAG bug you will ever debug lives in one of these six steps, so know where the boundaries are and which step owns which failure mode.

---

## CCA Exam Relevance

- **D1 (Agentic Architecture)**: the end-to-end RAG pipeline is a core agentic-pattern question. Expect exam items like "what is the correct order of the RAG steps" or "where does cosine similarity happen in the flow".
- **D4 (Safety & Alignment)**: RAG grounding reduces hallucination. The "bug" example is a textbook case of how good retrieval prevents confident wrong answers.
- Be ready to define cosine similarity, its range, and its relationship to cosine distance.

---

## Flashcards

| Front | Back |
|-------|------|
| List the six steps of the full RAG flow. | 1) Chunk text, 2) Generate embeddings, 3) Store in vector DB, 4) Embed user query, 5) Find similar embeddings (cosine similarity), 6) Build final prompt and call Claude. |
| Which steps are preprocessing vs. query time? | Steps 1-3 are preprocessing (once per document); steps 4-6 are query time (once per user request). |
| What is the range of cosine similarity? | -1 to +1. |
| What does cosine similarity of +1 mean? | The vectors point in the same direction — maximum similarity. |
| What does cosine similarity of 0 mean? | The vectors are perpendicular — no meaningful relationship. |
| How is cosine distance defined? | `1 - cosine_similarity`. Small values = high similarity; larger values = less similarity. |
| Why must the query and chunks use the same embedding model? | Otherwise the vectors live in different geometric spaces and similarity scores become meaningless. |
| What is normalization and why does it matter? | Scaling vectors to unit length (magnitude 1.0). It makes cosine similarity and dot product equivalent and enables efficient similarity search. |
| In the "bug" example, why does cosine similarity succeed where keyword search fails? | It compares semantic direction, not lexical overlap, so the query's software-heavy direction matches the software chunk despite shared vocabulary. |
