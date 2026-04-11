# Text Chunking Strategies — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Architecture (22%) — primary; D4 — Safety & Alignment (20%) — secondary |
| Task Statements | 1.3 (context management), 4.1 (grounded responses) |
| Source | building-with-the-claude-api / 05-rag / Lesson 46 |

---

## One-Liner

Chunking is the RAG step that decides what "a retrievable unit" means — and a bad chunking strategy silently poisons every downstream retrieval, letting irrelevant content into prompts and producing confident wrong answers.

---

## Why Chunking Is the Highest-Leverage Step

Consider a document with two sections: medical research and software engineering. A user asks "How many bugs did engineers fix this year?". If chunking is bad, the word "bug" appearing in the medical section (as in "XDR-47, a bug we have not seen before") gets pulled into the context — and Claude happily answers about a virus instead of software defects.

This is the core failure mode: **a chunk looked relevant because it shared a keyword, but the surrounding meaning was different**. Chunking determines the granularity at which semantic similarity is evaluated. Too coarse and chunks mix topics; too fine and chunks lose context.

---

## Strategy 1: Size-Based Chunking

The simplest approach — divide text into equal-length strings. A 325-character document might become three chunks of roughly 108 characters each.

**Pros:**
- Trivial to implement
- Works with any document type (text, code, logs, anything)
- Predictable chunk count and size

**Cons:**
- Words get cut off mid-sentence
- Chunks lose important context from surrounding text
- Section headers can be separated from their content

### Fix: Add Overlap

Overlap means each chunk includes some characters from neighboring chunks — giving you a sliding window that preserves boundary context.

```python
def chunk_by_char(text, chunk_size=150, chunk_overlap=20):
    chunks = []
    start_idx = 0

    while start_idx < len(text):
        end_idx = min(start_idx + chunk_size, len(text))
        chunk_text = text[start_idx:end_idx]
        chunks.append(chunk_text)

        start_idx = (
            end_idx - chunk_overlap if end_idx < len(text) else len(text)
        )

    return chunks
```

Two things to notice:
1. The loop advances by `chunk_size - chunk_overlap` effectively — overlap shrinks the net step.
2. The terminal branch sets `start_idx = len(text)` to guarantee loop exit; no off-by-one.

---

## Strategy 2: Structure-Based Chunking

Split on the document's natural structure — headers, paragraphs, sections. Best when you control the format (Markdown, internal reports with guaranteed heading style).

```python
def chunk_by_section(document_text):
    pattern = r"\n## "
    return re.split(pattern, document_text)
```

**Pros:**
- Cleanest, most meaningful chunks — each one is a complete semantic unit
- Natural boundaries match how humans think about the document
- A chunk "about risk factors" actually contains the Risk Factors section

**Cons:**
- Only works when structure is guaranteed — plain text or scanned PDFs have no headers to split on
- Section sizes vary wildly; one section might be 50 words, another 5000
- A single giant section can still blow past your token budget

Structure-based is the **ideal** when the format cooperates, and the **wrong tool** when it does not.

---

## Strategy 3: Semantic-Based Chunking

Split into sentences first, then use NLP to measure how related consecutive sentences are, and build chunks from groups of related sentences.

**Pros:**
- Produces the most semantically coherent chunks
- Boundaries follow meaning, not characters or headers

**Cons:**
- Computationally expensive (you are running a semantic similarity model during preprocessing)
- Complex to implement correctly
- Harder to tune than size or sentence approaches

Use semantic chunking when chunk quality is critical and you have the compute budget to justify it.

---

## Strategy 4: Sentence-Based Chunking (The Practical Middle Ground)

Split into sentences with a regex, then group sentences into chunks with optional sentence overlap.

```python
def chunk_by_sentence(text, max_sentences_per_chunk=5, overlap_sentences=1):
    sentences = re.split(r"(?<=[.!?])\s+", text)

    chunks = []
    start_idx = 0

    while start_idx < len(sentences):
        end_idx = min(start_idx + max_sentences_per_chunk, len(sentences))
        current_chunk = sentences[start_idx:end_idx]
        chunks.append(" ".join(current_chunk))

        start_idx += max_sentences_per_chunk - overlap_sentences

        if start_idx < 0:
            start_idx = 0

    return chunks
```

Notice the regex `(?<=[.!?])\s+` — a lookbehind that keeps the terminal punctuation on the previous sentence rather than stripping it. The overlap is now measured in **sentences**, not characters, which is a more meaningful unit.

Sentence-based is the sensible default when you do not have structural guarantees but you still want human-readable chunk boundaries.

---

## Choosing a Strategy

| Strategy | Best For | Avoid When |
|----------|----------|------------|
| **Structure-based** | Markdown, internal reports with guaranteed headers | Plain text, PDFs, mixed formats |
| **Sentence-based** | Most prose text documents | Code (sentences are not a concept) |
| **Size-based + overlap** | Any content type, code, logs, fallback | When you have better structure signals and want to use them |
| **Semantic** | High-stakes retrieval where quality justifies cost | Latency-sensitive or budget-constrained preprocessing |

**Production heuristic**: size-based chunking with overlap is the common go-to because it is simple, reliable, and works with anything. It will not be perfect, but it will not break your pipeline. Graduate to sentence/structure/semantic when you have evidence that retrieval quality is hurting.

There is **no single "best" strategy**. The right choice depends on your documents, use cases, and the quality/complexity trade-off you can afford.

---

## CCA Task Annotations

- **Task 1.3 (Context Management)** — chunking is how you control the granularity of retrievable context; chunk size determines what "a unit of knowledge" is for your system.
- **Task 4.1 (Grounded Responses)** — good chunking reduces the probability of pulling in off-topic text that would ground a wrong answer.

---

## Common Mistakes

1. **Assuming chunking is a solved problem** — default parameters on a chunking library will work until they do not, and then you will not know why retrieval started failing.
2. **No overlap in size-based chunking** — words and sentences get cut at boundaries, and chunks lose the context that makes them retrievable.
3. **Using structure-based chunking on unstructured text** — if there are no headers, the regex returns the whole document as one chunk.
4. **One-size-fits-all across document types** — code, prose, and tables need different strategies; do not force the same chunker on all of them.
5. **Not logging chunk IDs in production** — when retrieval returns the wrong chunk you cannot debug it unless you can trace which chunk was picked.

> **Key Insight**
>
> Chunking is the first place a RAG pipeline can silently lie to the user. Every downstream step — embedding, retrieval, prompt assembly — takes chunks as given. If a chunk crosses a topic boundary or cuts off a definition, the retrieval system will confidently return it, and Claude will confidently answer from it. Invest in chunking evals before you invest in retrieval tuning.

---

## CCA Exam Relevance

- **D1 (Agentic Architecture)**: chunking is the first decision in the RAG context-management pipeline. Know the four strategies, their trade-offs, and when to use each.
- **D4 (Safety & Alignment)**: bad chunking is a silent source of wrong answers — the "bug" example from the lesson is a classic exam scenario.
- Expect questions framed as "Markdown docs with guaranteed headers → which strategy?" (structure) and "plain text PDFs → which strategy?" (size+overlap or sentence).

---

## Flashcards

| Front | Back |
|-------|------|
| Name the four chunking strategies covered. | Size-based, structure-based, sentence-based, semantic-based. |
| What problem does chunk overlap solve? | Boundary context loss — it ensures complete words/sentences and preserves context shared between adjacent chunks. |
| When is structure-based chunking the best choice? | When you have guarantees about document structure (Markdown headers, templated reports). |
| What is the downside of structure-based chunking? | It only works when structure is present; plain text or PDFs without headers cannot use it. |
| Why is semantic chunking expensive? | It requires running NLP / similarity models during preprocessing to measure sentence relatedness. |
| What is the production fallback chunking strategy? | Size-based with overlap — it works on any content type. |
| Why is the "bug" example (medical vs. engineering) instructive? | It shows how bad chunking can pull an irrelevant chunk into the prompt simply because of keyword overlap. |
| In `chunk_by_char`, what does `start_idx = end_idx - chunk_overlap` do? | Advances the window by `chunk_size - chunk_overlap`, preserving overlap between adjacent chunks. |
