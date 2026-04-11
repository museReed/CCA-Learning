# Prompt Caching — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D5 — Enterprise Deployment (20%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 5.1 (cost/latency optimization), 5.2 (production performance), 1.2 (multi-turn efficiency) |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 56 |

---

## One-Liner

Prompt caching is a production optimization that saves Claude's per-request preprocessing work (tokenization, embeddings, context analysis) so identical prefixes on follow-up requests run faster and cost less instead of being recomputed from scratch.

---

## How Claude Normally Processes Requests

Every message you send to Claude goes through an expensive preprocessing pipeline *before* any output tokens are generated:

1. **Tokenization** — the prompt is broken into smaller pieces (tokens).
2. **Embedding** — each token is turned into a high-dimensional vector.
3. **Context analysis** — the model adds context from surrounding tokens so later attention layers can reason over the sequence.
4. **Generation** — only after steps 1-3 does Claude actually start producing output text.

The important bit: after the response is streamed back, **all of that preprocessing work is thrown away**. The tokenization, the embeddings, the context — discarded. If you send the same 6K-token prompt one minute later, Claude redoes every step.

---

## The Problem with Discarding Work

This waste becomes obvious in any workflow that reuses the same base content:

- A conversation where you keep asking Claude to refine the same summary.
- A document-analysis loop asking 20 questions about one 50-page PDF.
- An agent that carries the same system prompt + tool schema across every turn.

On request #2, Claude has to redo all the preprocessing on content it just analyzed seconds ago. As the lesson phrases it: *"I just processed that message and threw away all the work I did — I could have reused it!"*

The cost is paid twice: once in latency (input processing time), once in dollars (input token billing).

---

## How Prompt Caching Solves This

Prompt caching changes the workflow by **saving the preprocessing results instead of discarding them**.

- On the first request, Claude does the usual preprocessing, but stores the intermediate state in a cache.
- The cache acts like a lookup table: "If I ever see this exact prefix again, reuse the work I already did."
- Follow-up requests that send the same prefix hit the cache and skip straight to generation, charging only for new (uncached) tokens.

The net effect: the expensive preprocessing is amortized across many calls instead of being paid on every single call.

---

## Key Benefits

| Benefit | What it means in production |
|---------|-----------------------------|
| **Faster responses** | Cached requests skip tokenization/embedding/context work, reducing time-to-first-token. |
| **Lower costs** | Cached portions of requests are billed at a significant discount vs. fresh input tokens. |
| **Automatic optimization** | The first request writes to the cache; subsequent requests read from it — no client-side cache management needed. |

---

## Important Limitations

| Limitation | Implication |
|-----------|-------------|
| **Cache duration: 1 hour** | Useful only for workflows with frequent repeat calls within the same hour. Idle conversations get purged. |
| **Limited use cases** | Caching only helps when you send the *same* content repeatedly; one-off prompts see no benefit. |
| **High-frequency requirement** | The more often the same prefix is reused, the bigger the savings — sporadic calls may not justify the setup. |

---

## When Prompt Caching Works Best

The lesson highlights two canonical patterns where caching pays off:

1. **Document analysis workflows** — the same large document is referenced while you ask many different questions. The document gets cached once, then read cheaply on every follow-up.
2. **Iterative editing tasks** — the base content (e.g., a draft) stays constant while you refine specific aspects. The draft is cached, edits are incremental.

More broadly, any workflow where **a large, stable prefix is paired with a small, variable suffix** is a strong candidate.

---

## Common Mistakes

1. **Caching one-off prompts** — paying the cache-write surcharge on content that is never read back. The cache only saves money if reused within one hour.
2. **Assuming caching is automatic** — it is not. Without an explicit opt-in (cache breakpoints, covered in lesson 57), Claude discards preprocessing as usual.
3. **Ignoring the 1-hour TTL** — building cache-reliant workflows that run at low frequency means cache entries expire before they are reused.
4. **Treating cache savings as latency-only** — you also get substantial cost savings on cached input tokens, which is often the bigger production win.
5. **Underestimating preprocessing cost** — believing input token processing is "free." For large system prompts and tool schemas, it is a significant share of total cost and latency.

---

> **Key Insight**
>
> Prompt caching is an **amortization trick**: the expensive preprocessing of a large, stable prefix is paid once and reused across every subsequent call that shares that prefix, up to one hour. In production, this is the single biggest cost/latency optimization for agent loops, RAG pipelines, and any workflow where the same context is hit repeatedly. It is a D5 Enterprise Deployment fundamental.

---

## CCA Exam Relevance

- **D5 (Enterprise Deployment)** — caching is one of the core production optimizations tested under task 5.1 (cost/latency). Know that caching reduces *both* cost and latency on the cached prefix.
- **D1 (Agentic Architecture)** — agent loops with stable system prompts and tool schemas are the prototypical caching beneficiary; the same context is sent on every turn of the loop.
- Watch for exam questions framed as: "How do you reduce cost and latency when the same large prompt is sent repeatedly?" → answer is prompt caching.

---

## Flashcards

| Front | Back |
|-------|------|
| What problem does prompt caching solve? | Claude redoes expensive preprocessing (tokenization, embeddings, context analysis) on every request, even when the same content was just processed. Caching reuses that work. |
| What are the four preprocessing steps Claude normally performs? | Tokenization, embedding creation, context analysis based on surrounding text, then output generation. |
| How long does a cached prompt live? | One hour. |
| What two benefits does prompt caching deliver? | Faster responses (lower latency) and lower costs on the cached portion of the request. |
| When does prompt caching NOT help? | One-off prompts, sporadic workflows that do not hit the same prefix within one hour, or content that changes on every request. |
| Name two canonical use cases for prompt caching. | Document analysis workflows (many questions about the same long document) and iterative editing tasks (same base content refined repeatedly). |
| Is prompt caching automatic? | No — it must be enabled explicitly; without opt-in Claude discards preprocessing work as usual. |
| What happens on the initial request when caching is enabled? | Claude performs normal preprocessing but stores the intermediate state so follow-up requests can reuse it instead of recomputing. |
