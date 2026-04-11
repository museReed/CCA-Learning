# PDF Support — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 2.2 (content blocks), 2.1 (multimodal input), 5.2 (document processing pipelines) |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 54 |

---

## One-Liner

PDF support is a near drop-in extension of image support — you swap the block `type` from `"image"` to `"document"` and the media type to `application/pdf`, and Claude reads the full document including text, tables, charts, and embedded images.

---

## Why PDF Support Is a Big Deal

Most enterprise knowledge lives in PDFs: contracts, research papers, financial reports, insurance policies, compliance documents, product spec sheets. Before document support, extracting meaning from a PDF meant stitching together an OCR pass, a layout parser, a table extractor, and a chunking pipeline — each of which introduced its own error.

PDF support collapses that pipeline to a single API call. Claude reads the whole document directly and answers questions, summarizes content, or extracts structured data without the intermediate toolchain. You still need to think about how to chunk very long documents, but the common case is "send the PDF, ask the question, get the answer."

---

## Nearly Identical to Image Processing

The lesson's main point is that PDF support reuses the image-processing pattern almost verbatim. If you already know how to send an image, you already know 90% of PDF support.

Here is the full example from the lesson:

```python
with open("earth.pdf", "rb") as f:
    file_bytes = base64.standard_b64encode(f.read()).decode("utf-8")

messages = []

add_user_message(
    messages,
    [
        {
            "type": "document",
            "source": {
                "type": "base64",
                "media_type": "application/pdf",
                "data": file_bytes,
            },
        },
        {"type": "text", "text": "Summarize the document in one sentence"},
    ],
)

chat(messages)
```

Observe the structure: a `document` block and a `text` block together in a single user message's `content` list. The document block carries the base64-encoded PDF; the text block carries the question. Claude replies with a normal text block.

---

## Key Changes From Image Processing

The lesson enumerates exactly four differences when adapting your image code to PDFs:

1. **File extension**: `.png` → `.pdf` when opening the file.
2. **Variable name**: `image_bytes` → `file_bytes` for clarity (a convention, not a requirement — the API does not care what you name the local variable).
3. **Block `type`**: `"image"` → `"document"`.
4. **`media_type`**: `"image/png"` → `"application/pdf"`.

That is the entire diff. The `source.type: "base64"` stays the same. The data field still holds a base64 string. The text block is still structured the same way. Existing message-handling code that understands content blocks keeps working — it just has to recognize `"document"` as a valid block type.

---

## What Claude Can Extract From PDFs

The course explicitly calls out four categories of extraction Claude handles natively inside a PDF:

- **Text content** throughout the document.
- **Images and charts** embedded in the PDF.
- **Tables** and their data relationships.
- **Document structure and formatting.**

This is a bigger deal than it sounds. Tables inside PDFs have historically been painful — layout analysis has to infer row/column boundaries, merged cells, multi-line entries, and header hierarchies. Charts were effectively invisible without a separate vision step. Claude's native PDF support turns all four of those into "just ask a question."

Concretely, that means a single `document` block lets you:

- Summarize a 10-K filing.
- Pull specific numbers out of a financial table.
- Describe a chart without ever extracting it to PNG first.
- Ground a QA answer in a policy document's structure.

The course's running example is a Wikipedia article about Earth saved as a PDF, summarized in one sentence by Claude — a minimal demonstration that the document block works end-to-end.

---

## Production Considerations the Lesson Implies

The lesson itself is short and does not enumerate limits, but the same quota pattern as images applies in spirit: you need to plan for document size and count. For production PDF pipelines, think about:

- **Size bounds.** Very large PDFs can be expensive to include. Consider splitting documents by section for long-form content and routing only the relevant chunks to Claude.
- **Pre-processing.** If your PDFs come from OCR of scans, the quality of the PDF affects Claude's extraction accuracy. Clean PDFs → better answers.
- **Prompt structure.** As with images, the prompt discipline matters. A vague "tell me about this document" is worse than "summarize section 3 in one sentence" or "extract all dollar amounts in the executive summary as JSON."
- **Caching.** If you re-query the same document often, prompt caching becomes attractive because the document bytes dominate the input.

---

## Common Mistakes

1. **Using `type: "image"` for a PDF.** The block type must be `"document"`. Claude will reject or misinterpret an image block pointing at a PDF.
2. **Wrong `media_type`.** `application/pdf` exactly — not `pdf`, not `application/x-pdf`.
3. **Sending raw bytes instead of base64.** The `data` field is a base64 string, not raw bytes or a file path.
4. **Assuming PDF is cheap.** A long PDF costs real tokens on every call. Plan chunking and consider caching.
5. **Skipping the prompt layer.** The API gives you a document; you still have to ask a precise question. Summarize-the-whole-thing prompts produce vague answers.
6. **Forgetting that message-handling code must recognize `"document"` blocks.** If you built your handler to assume only `"text"` and `"image"` exist, adding PDFs silently breaks it.

---

> **Key Insight**
>
> PDF support is the image-block pattern with two fields changed: `type` becomes `"document"` and `media_type` becomes `"application/pdf"`. Everything else — base64 encoding, content-block structure, message flow, system prompts, tool use — stays identical. What actually differs is **production thinking**: PDFs are larger than screenshots, so chunking, caching, and precise prompts matter more than they do for one-off image inputs.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: PDFs are a content-block variant. Know that the block type is `"document"` (not `"pdf"`) and the media type is `"application/pdf"`.
- **D5 (Enterprise Deployment)**: document processing pipelines for RAG, contract analysis, policy QA — PDF support is often the simplest answer and beats hand-rolled OCR/layout pipelines.
- Exam scenario pattern: "You need Claude to read a PDF contract and extract the indemnification clause." The answer is a `document` content block with `application/pdf` media type, plus a precise extraction prompt.

---

## Flashcards

| Front | Back |
|-------|------|
| What block type does Claude use for PDFs? | `"document"` — not `"pdf"` or `"image"`. |
| What media type do you use for a PDF? | `"application/pdf"`. |
| How do you encode the PDF bytes for the API? | Base64-encode the file and pass the string as `source.data`, with `source.type: "base64"`. |
| What are the four things that change between image and PDF code? | File extension (`.png` → `.pdf`), variable name (`image_bytes` → `file_bytes`), block type (`"image"` → `"document"`), and media type (`image/png` → `application/pdf`). |
| What four kinds of content can Claude extract from a PDF natively? | Text content, embedded images and charts, tables and their data relationships, and document structure and formatting. |
| Why is native PDF support a bigger deal than it looks? | It collapses a traditional OCR + layout + table + chunking pipeline into a single API call, and it natively handles tables and charts that were historically painful. |
| What prompt pattern should you use when summarizing a PDF? | The same prompt discipline you use for text — be specific ("summarize section 3 in one sentence") rather than vague ("tell me about this document"). |
| When should you chunk a PDF before sending it to Claude? | When the document is large enough that either token cost or context length becomes the bottleneck, or when only a few sections are relevant to the question. |
