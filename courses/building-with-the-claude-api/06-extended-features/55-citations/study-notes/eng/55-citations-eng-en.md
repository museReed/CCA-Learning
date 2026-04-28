# Citations — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D4 — AI Safety & Alignment (20%) — primary; D2 — Tool Design & MCP Integration (18%) — secondary |
| Task Statements | 4.2 (grounded outputs), 2.2 (content blocks), 5.4 (trust and verifiability) |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 55 |

---

## One-Liner

Citations turn Claude's document-grounded answers from opaque text into a verifiable trail — for every claim, you get the exact source text, which document it came from, and where in that document it lives.

---

## The Trust Problem Citations Solve

When Claude answers a question about a document you provided, users cannot tell, just from the text, whether the answer came from your document or from the model's training data. That ambiguity is a trust killer for any feature where the source matters: legal research, financial analysis, medical information, compliance QA.

Citations fix this by creating an explicit, machine-readable trail from every statement in Claude's response back to the source text that grounds it. The model does not just answer — it shows its receipts.

---

## Enabling Citations

Citations turn on with two additions to the `document` content block: a human-readable `title` and a `citations.enabled` flag.

```python
{
    "type": "document",
    "source": {
        "type": "base64",
        "media_type": "application/pdf",
        "data": file_bytes,
    },
    "title": "earth.pdf",
    "citations": { "enabled": True }
}
```

Two fields matter:

- **`title`** — a readable name for the document. This is what users see in the UI when a citation appears; it is also what Claude uses internally to distinguish between multiple documents in the same request.
- **`citations.enabled`** — the switch that tells Claude to track source provenance for every statement it makes.

The rest of the document block is unchanged from the PDF support pattern.

---

## Response Structure When Citations Are On

With citations disabled, Claude's response is a simple text block. With citations enabled, Claude returns a richer structure where text segments are accompanied by citation metadata. Each citation contains:

- **`cited_text`** — the exact text from your document that supports the statement. This is the ground truth the model points at, character-for-character.
- **`document_index`** — which document Claude is referencing, useful when a single request contains multiple documents.
- **`document_title`** — the title you assigned to the document (the same string you put in the document block).
- **`start_page_number`** — where in the document the cited text begins.
- **`end_page_number`** — where the cited text ends.

For a PDF, `start_page_number` and `end_page_number` are page numbers. For plain text sources, these are replaced by **character positions** that pinpoint the exact span inside the text.

---

## Citations With Plain Text Sources

Citations are not a PDF-only feature. You can enable them on plain text documents by changing the `source` block:

```python
{
    "type": "document",
    "source": {
        "type": "text",
        "media_type": "text/plain",
        "data": article_text,
    },
    "title": "earth_article",
    "citations": { "enabled": True }
}
```

The differences from the PDF case:

- `source.type` is `"text"` instead of `"base64"`.
- `source.media_type` is `"text/plain"`.
- `source.data` contains the raw article text, not base64 bytes.
- The returned citations use **character positions** (start_index / end_index) instead of page numbers.

This matters for RAG pipelines: when your retrieval step surfaces a chunk of plain text, you can pass it in as a citable document and get precise character spans back, which makes hover-over UIs or highlighting tooling very clean to build.

---

## Building User Interfaces With Citations

The real product leverage of citations is the UI layer. A typical pattern:

1. Claude's response arrives with citation-annotated segments.
2. The UI renders the answer text as normal, but each cited span gets a marker (a small number, a highlighted background, or an inline icon).
3. Hovering or clicking the marker opens a popover that shows the `cited_text`, the `document_title`, and a jump-to-page or jump-to-character action.
4. The user can verify the claim in place, without leaving the answer view.

This turns Claude from a "black box that answers" into a "research assistant that shows its work." Users who need to trust the output can check it in two clicks; users who do not care can ignore the markers.

---

## When to Use Citations

The lesson names four situations where citations earn their cost and complexity:

- **Users need to verify information for accuracy.** High-stakes answers — legal, medical, financial — require proof.
- **You are working with authoritative documents.** If the document is the source of truth (a contract, a regulation, a clinical guideline), users should be able to point at it.
- **Transparency about information sources is critical.** Some products — enterprise search, research tools, knowledge bases — live or die on source transparency.
- **Users might want to explore the broader context around specific facts.** Citations are a hook for drill-down UX; users can jump from an answer to the surrounding paragraph to the full document.

---

## Common Mistakes

1. **Forgetting the `title` field.** Citations use the title as the document identifier in the response. Without it, the user sees a blank or generic label and cannot distinguish between documents.
2. **Enabling citations but not displaying them.** If you switch the flag on but render the answer as plain text, you pay the token cost with none of the trust benefit.
3. **Assuming page numbers work for plain-text sources.** Plain-text citations return character positions, not pages. Your UI has to branch on source type.
4. **Not handling the richer response structure.** Citations-enabled responses are more complex than a single text block. Your content-block handler must iterate and pull citation metadata correctly.
5. **Mixing cited and uncited documents in one request without tracking which is which.** `document_index` tells you which document a citation points at — use it.
6. **Assuming citations verify correctness.** A citation proves the source text exists and Claude read it — it does not prove Claude's interpretation is correct. Treat citations as provenance, not as accuracy guarantees.

---

> **Key Insight**
>
> Citations are the grounding layer that converts Claude's document answers into verifiable claims. The API surface is tiny — a `title` field and a `citations.enabled` flag — but the product impact is enormous: for every high-stakes document workflow (legal, medical, financial, compliance), citations are the difference between a feature users can ship and one they cannot. Pair citations with PDF support and you have the canonical enterprise document stack.

---

## CCA Exam Relevance

- **D4 (AI Safety & Alignment)**: grounded outputs and verifiable responses are core safety concerns. Citations are the standard mechanism for producing verifiable, source-linked answers.
- **D2 (Tool Design & MCP Integration)**: citations extend the `document` content block. Know the `title` and `citations.enabled` fields plus the citation metadata shape (`cited_text`, `document_index`, `document_title`, page or character positions).
- Exam scenario pattern: "Users need to verify that Claude's answer came from a specific source." The answer is citations enabled on the document block, with the UI surfacing `cited_text` and `document_title`.

---

## Flashcards

| Front | Back |
|-------|------|
| What two fields do you add to a document block to enable citations? | A `title` field (readable document name) and `"citations": {"enabled": True}`. |
| What are the five pieces of information inside a citation object? | `cited_text`, `document_index`, `document_title`, `start_page_number`, and `end_page_number`. |
| How do citations differ between PDF and plain-text sources? | PDF citations return page numbers; plain-text citations return character positions inside the text. |
| What `source.type` and `media_type` do you use for a plain-text citable document? | `source.type: "text"` and `media_type: "text/plain"`, with the raw article text in `data`. |
| When should you use citations? | When users need to verify information, when you are working with authoritative documents, when source transparency is critical, or when users may want to explore context. |
| Why is a `title` field required when enabling citations? | It is the document identifier returned in each citation and the label users see in the UI; without it, multi-document responses are ambiguous. |
| What is the difference between a citation and a correctness guarantee? | A citation proves the source text exists and Claude read it; it does not prove Claude's interpretation of that text is correct. |
| What is the canonical UX pattern for citations? | Render the answer with inline markers on cited spans, and on hover show `cited_text` and `document_title` with a jump-to-source action. |
| Why are citations critical for legal, medical, and financial products? | Users in those domains must verify the source of any claim before acting on it; citations provide the auditable trail that makes those features shippable. |
