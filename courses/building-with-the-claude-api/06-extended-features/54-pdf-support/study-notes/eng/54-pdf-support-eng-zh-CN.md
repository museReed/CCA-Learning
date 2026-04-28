# PDF Support — Engineering Deep Dive

| 项目 | 内容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — 主要；D5 — Enterprise Deployment (20%) — 次要 |
| Task Statements | 2.2（content blocks）、2.1（多模态输入）、5.2（文档处理管线） |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 54 |

---

## One-Liner

PDF support 几乎是 image support 的 drop-in 扩展——把 block `type` 从 `"image"` 换成 `"document"`，media type 换成 `application/pdf`，Claude 就能读整份文档，包括文字、表格、图表和内嵌图像。

---

## 为什么 PDF support 是大事

大多数企业知识都活在 PDF 里：合同、研究论文、财报、保单、合规文档、产品规格书。有 document support 之前，要从 PDF 抽取意义得把 OCR、layout parser、table extractor、chunking 管线串在一起——每一段都会引入自己的错误。

PDF support 把整条管线收敛成单次 API 调用。Claude 直接读整份文档回答问题、摘要内容或抽取结构化数据，不需要中间那串工具链。你仍然需要思考超长文档怎么切，但常见情境就是"送 PDF、问问题、拿答案"。

---

## 几乎和 image processing 一样

课程最重要的一点：PDF support 几乎原样重用 image processing 的 pattern。如果你已经会发送图，就已经会 90% 的 PDF support。

以下是课程里的完整示例：

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

观察结构：一个 `document` block 和一个 `text` block 放在同一个 user message 的 `content` list 里。Document block 装 base64 编码的 PDF；text block 装问题。Claude 回一个普通 text block。

---

## 和 image processing 的差别

课程明确列出从 image 代码转到 PDF 只有四个差别：

1. **扩展名**：打开文件时 `.png` → `.pdf`。
2. **变量名**：`image_bytes` → `file_bytes`，为了可读性（这只是惯例；API 不在意你本地变量叫什么）。
3. **Block `type`**：`"image"` → `"document"`。
4. **`media_type`**：`"image/png"` → `"application/pdf"`。

整个 diff 就这样。`source.type: "base64"` 不变。Data 字段仍然放 base64 字符串。Text block 的结构不变。能处理 content blocks 的既有消息处理代码照旧能用——它只需要把 `"document"` 认成一种合法的 block type。

---

## Claude 能从 PDF 抽取什么

课程明确点出 Claude 在 PDF 里原生处理的四类内容：

- **文档内各处的文字内容**。
- **PDF 内嵌的图片与图表**。
- **表格**与其中的数据关联。
- **文档结构与排版**。

这比听起来更重要。PDF 里的表格历来很麻烦——layout 分析得推断 row/column 边界、合并单元格、多行条目、header 层级。图表在没有额外 vision 步骤前等于看不见。Claude 的原生 PDF support 把这四件事都变成"直接问就好"。

具体来说，一个 `document` block 让你可以：

- 摘要一份 10-K 申报文档。
- 从财务表格里抓特定数字。
- 不用先把图表转成 PNG 就能描述它。
- 把 QA 答案锚在一份政策文档的结构上。

课程用的例子是一份存成 PDF 的 Earth 维基文章，请 Claude 用一句话摘要——最小可行演示，证明 document block 端到端都能通。

---

## 课程暗示的 production 考量

课程本身很短，没列出约束，但配额思路上和 image 同款。做 production PDF 管线时要想：

- **大小边界。** 非常大的 PDF 每次塞进去都贵。对长篇内容考虑按 section 切档，只把相关片段发送给 Claude。
- **前处理。** 如果你的 PDF 是扫描文档 OCR 而来，PDF 质量直接影响 Claude 的抽取准确度。干净 PDF → 更好的答案。
- **Prompt 结构。** 和图像一样，prompt 纪律很重要。含糊的"跟我说这份文档"比"用一句话摘要第 3 节"或"把 executive summary 里所有金额以 JSON 抽取"差很多。
- **Caching。** 如果你常对同一份文档发多个 query，prompt caching 会变得很有吸引力，因为 PDF bytes 占了输入的主体。

---

## Common Mistakes

1. **PDF 用 `type: "image"`。** Block type 必须是 `"document"`，对 PDF 用 image block 会被拒绝或误读。
2. **错的 `media_type`。** 必须完全是 `application/pdf`——不是 `pdf`、不是 `application/x-pdf`。
3. **发送原始 bytes 而不是 base64。** `data` 字段是 base64 字符串，不是 raw bytes 或文件路径。
4. **以为 PDF 便宜。** 长 PDF 每次调用都烧真 token。规划 chunking、考虑 caching。
5. **跳过 prompt 层。** API 给你一份文档；你还是得问一个精准问题。"摘要整份"会产出含糊答案。
6. **忘了消息处理代码要认 `"document"` blocks。** 如果你的 handler 假设只有 `"text"` 和 `"image"`，加 PDF 会默默坏掉。

---

> **Key Insight**
>
> PDF support 就是 image-block 的 pattern 改两个字段：`type` 变 `"document"`、`media_type` 变 `"application/pdf"`。其他所有东西——base64 编码、content-block 结构、message flow、system prompt、tool use——都完全一样。真正不同的是 **production 思维**：PDF 比截图大，所以 chunking、caching、精准 prompt 比一次性图像输入更重要。

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**：PDF 是 content-block 变体。记得 block type 是 `"document"`（不是 `"pdf"`），media type 是 `"application/pdf"`。
- **D5 (Enterprise Deployment)**：RAG 的文档处理管线、合同分析、政策 QA——PDF support 常常是最简单的答案，胜过手搓的 OCR / layout 管线。
- 考题情境："你要 Claude 读一份 PDF 合同并抽取免责条款。"答案是 `document` content block + `application/pdf` media type + 一个精准的抽取 prompt。

---

## Flashcards

| Front | Back |
|-------|------|
| Claude 对 PDF 用哪种 block type？ | `"document"`——不是 `"pdf"` 也不是 `"image"`。 |
| PDF 的 media type 是？ | `"application/pdf"`。 |
| 怎么把 PDF bytes 编码给 API？ | 把文件 base64 编码，字符串放在 `source.data`，配 `source.type: "base64"`。 |
| Image 代码转 PDF 要改哪四件事？ | 扩展名（`.png` → `.pdf`）、变量名（`image_bytes` → `file_bytes`）、block type（`"image"` → `"document"`）、media type（`image/png` → `application/pdf`）。 |
| Claude 原生可以从 PDF 抽取哪四种内容？ | 文字内容、内嵌图片与图表、表格与数据关联、文档结构与排版。 |
| 为什么原生 PDF support 比表面看更重要？ | 它把传统 OCR + layout + table + chunking 管线收敛成一次 API 调用，并原生处理历来麻烦的表格与图表。 |
| 摘要 PDF 该用哪种 prompt pattern？ | 和文字一样的 prompt 纪律——要精准（"用一句话摘要第 3 节"）而不是含糊（"跟我说这份文档"）。 |
| 何时该先把 PDF 切片再发送给 Claude？ | 当 token 成本或 context 长度成为瓶颈，或只有少数 section 和问题相关时。 |
