# Text Chunking Strategies — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Architecture (22%) — primary; D4 — Safety & Alignment (20%) — secondary |
| Task Statements | 1.3 (context management), 4.1 (grounded responses) |
| Source | building-with-the-claude-api / 05-rag / Lesson 46 |

---

## One-Liner

Chunking is the invisible product-quality knob of every RAG feature — it decides what "one unit of knowledge" looks like, and getting it wrong means your AI confidently cites the wrong paragraph.

---

## Mental Model: Cutting Cake for a Dinner Party

Imagine a multi-layer cake. Guests ask for "the chocolate layer" or "the strawberry layer". How you slice it matters:

| Slicing Style | What Each Guest Gets | Chunking Strategy |
|---------------|---------------------|-------------------|
| Random 2-inch cubes | Sometimes pure chocolate, sometimes half-chocolate-half-strawberry | Size-based, no overlap |
| Random 2-inch cubes with a smear from the next cube | Same, but you can see which layer is next | Size-based with overlap |
| Clean horizontal slices, one per layer | Exactly what they asked for | Structure-based |
| A chef who picks flavors to group | Smallest portions of pure flavor | Semantic |

A careless slice gives you a bite that crosses layers. The guest who asked for strawberry gets a blob of chocolate in their mouth and does not know why. **That is what bad chunking feels like to a user of a RAG feature.**

---

## Why This Is a PM Problem (Not Just Eng)

Chunking decisions drive user-visible behavior:

- **"The AI gave me an irrelevant answer"** → usually bad chunking
- **"The AI cut off mid-sentence in the citation"** → definitely bad chunking
- **"The AI answered using a different section than what I asked about"** → the classic "bug" example from this lesson
- **"Updates to our docs do not show up in answers"** → the re-chunking pipeline failed

A PM who thinks chunking is "something engineering handles" will be the one apologizing when the CEO demos the feature and gets a wrong answer.

---

## The Four Strategies, in PM Terms

| Strategy | PM Description | When to Pick It |
|----------|----------------|-----------------|
| **Size-based** | "Cut every 500 characters, add overlap" | Default for mixed content — cheap, reliable, predictable |
| **Structure-based** | "Split on the Markdown headers" | When you control the content format (internal docs, template reports) |
| **Sentence-based** | "Group 5 sentences at a time" | Prose-heavy content where sentences are meaningful units |
| **Semantic** | "Use NLP to keep related ideas together" | High-stakes retrieval (legal, medical) where quality justifies compute |

The one thing a PM needs to internalize: **none of these is universally "best"**. The right strategy depends on the content type, the quality bar, and the engineering budget.

---

## The "Bug" Example — Why Every PM Should Know It

The lesson uses a vivid example: a document has a medical research section and a software engineering section. The medical section happens to say "XDR-47, a bug we have not seen before". A user asks "How many bugs did engineers fix this year?".

A bad chunker might pull the medical chunk because it contains the word "bug". Claude then writes a fluent answer about viruses — wrong section, wrong domain, wrong answer, but phrased confidently.

This is the **silent failure** pattern. There is no error message. The logs look healthy. Only a user QA-ing the answer would spot it. For a PM, this is the kind of bug that destroys user trust by the tenth occurrence.

---

## Product Use Cases

### Use Structure-Based When...

| Signal | Reason |
|--------|--------|
| Content is written in Markdown | Headers are reliable boundaries |
| You own the authoring template (internal wiki, PRD template) | You can enforce structure |
| Each section has roughly consistent meaning | Semantic alignment comes for free |

### Use Size-Based + Overlap When...

| Signal | Reason |
|--------|--------|
| You cannot guarantee document structure | Fallback must work on anything |
| Content is mixed (docs + PDFs + code + logs) | One strategy for everything |
| You are shipping an MVP and want predictable behavior | Simplest to reason about |

### Use Sentence-Based When...

| Signal | Reason |
|--------|--------|
| Content is prose, no structure | Sentences are the natural unit |
| You want human-readable citations | Cut-off words look bad in a cite box |

### Use Semantic When...

| Signal | Reason |
|--------|--------|
| Domain is high-stakes (legal, medical, financial) | Wrong retrieval has real consequences |
| Retrieval is a proven product bottleneck | You have data showing chunk quality matters |
| You have compute budget to spare | Preprocessing is heavier |

---

## PM Decision Framework

When specifying a RAG feature, answer these before signing off:

| Question | Why It Matters |
|----------|----------------|
| What is our canonical content format? | Dictates whether structure-based is viable |
| What is our chunk size budget? | Ties directly to prompt size, cost, latency |
| Who owns chunk quality eval? | Must be a named owner, not "engineering in general" |
| How do users see citations? | If citations are visible, cut-off chunks look broken |
| How do we re-chunk when docs change? | Every content update has a preprocessing cost |

---

## Common PM Mistakes

1. **Treating chunking as an engineering implementation detail** — it is a product lever; chunk size directly affects what your users see.
2. **No chunk-quality eval** — shipping without a test set means you learn about bad chunking from angry users.
3. **Assuming one strategy fits all content types** — a platform with docs, PDFs, and code needs more than one chunker.
4. **Ignoring the re-indexing story** — every content update triggers preprocessing; if that pipeline is fragile, your "AI answers" feature silently goes stale.
5. **Not making citations auditable** — without visible source links, users cannot catch silent failures, and trust erodes.

> **Key Insight**
>
> Chunking is the silent cousin of retrieval. When someone says "our RAG system got the wrong answer", the root cause is chunking about half the time — a good chunk was never created, so good retrieval was impossible. For PMs, this means chunking quality is an eval target on day one, not a thing you "iterate on later".

---

## CCA Exam Relevance

- **D1 (Agentic Architecture)**: Know the four strategies, their trade-offs, and be ready for scenario questions ("Markdown docs with guaranteed headers → ?", "mixed PDFs → ?").
- **D4 (Safety & Alignment)**: The "bug" example maps directly to hallucination risk — a wrong chunk leads to a confidently wrong answer.
- Watch for exam framing around "overlap" — the correct answer to "how do you stop chunks from cutting off mid-sentence" is always overlap.

---

## Flashcards

| Front | Back |
|-------|------|
| Why should PMs care about chunking? | It is a silent driver of product quality — bad chunking causes confidently wrong answers that users cannot debug. |
| What is the "bug" example teaching? | How a keyword can match across unrelated domains (medical vs. software), producing a wrong but fluent answer. |
| What is the cake-slicing analogy? | A bad cut crosses layers and gives the guest a bite of the wrong flavor — bad chunking crosses topic boundaries. |
| When should a PM pick structure-based chunking? | When you control the content format (Markdown, templated reports) so headers are reliable boundaries. |
| What is the go-to fallback chunking strategy? | Size-based with overlap — it works on any content type, predictable behavior. |
| Why is chunk overlap important for user-visible citations? | Without overlap, chunks cut off mid-sentence and look broken when shown as a citation. |
| Who should own chunk-quality eval? | A named PM/engineering partnership — not "engineering in general"; it is a product metric. |
| What is the silent failure mode of bad chunking? | No error; logs look healthy; users get a confidently wrong answer based on an irrelevant chunk. |
