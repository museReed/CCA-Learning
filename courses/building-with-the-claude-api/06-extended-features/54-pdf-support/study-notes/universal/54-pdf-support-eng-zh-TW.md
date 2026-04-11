# PDF Support — Engineering Deep Dive

| 項目 | 內容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — 主要；D5 — Enterprise Deployment (20%) — 次要 |
| Task Statements | 2.2（content blocks）、2.1（多模態輸入）、5.2（文件處理管線） |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 54 |

---

## One-Liner

PDF support 幾乎是 image support 的 drop-in 延伸——把 block `type` 從 `"image"` 換成 `"document"`，media type 換成 `application/pdf`，Claude 就能讀整份文件，包含文字、表格、圖表與內嵌影像。

---

## 為什麼 PDF support 是大事

大多數企業知識都活在 PDF 裡：合約、研究論文、財報、保單、合規文件、產品規格書。有 document support 之前，要從 PDF 擷取意義得把 OCR、layout parser、table extractor、chunking 管線串在一起——每一段都會引入自己的錯誤。

PDF support 把整條管線收斂成單次 API 呼叫。Claude 直接讀整份文件回答問題、摘要內容或擷取結構化資料，不需要中間那串工具鏈。你仍然需要思考超長文件怎麼切，但常見情境就是「送 PDF、問問題、拿答案」。

---

## 幾乎和 image processing 一樣

課程最重要的一點：PDF support 幾乎原樣重用 image processing 的 pattern。如果你已經會送圖，就已經會 90% 的 PDF support。

以下是課程裡的完整範例：

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

觀察結構：一個 `document` block 和一個 `text` block 放在同一個 user message 的 `content` list 裡。Document block 裝 base64 編碼的 PDF；text block 裝問題。Claude 回一個普通 text block。

---

## 和 image processing 的差別

課程明確列出從 image 程式碼轉到 PDF 只有四個差別：

1. **副檔名**：開檔時 `.png` → `.pdf`。
2. **變數名**：`image_bytes` → `file_bytes`，為了可讀性（這只是慣例；API 不在意你本地變數叫什麼）。
3. **Block `type`**：`"image"` → `"document"`。
4. **`media_type`**：`"image/png"` → `"application/pdf"`。

整個 diff 就這樣。`source.type: "base64"` 不變。Data 欄位仍然放 base64 字串。Text block 的結構不變。能處理 content blocks 的既有訊息處理程式照舊能用——它只需要把 `"document"` 認成一種合法的 block type。

---

## Claude 能從 PDF 擷取什麼

課程明確點出 Claude 在 PDF 裡原生處理的四類內容：

- **文件內各處的文字內容**。
- **PDF 內嵌的圖片與圖表**。
- **表格**與其中的資料關聯。
- **文件結構與排版**。

這比聽起來更重要。PDF 裡的表格歷來很麻煩——layout 分析得推論 row/column 邊界、合併儲存格、多行項目、header 階層。圖表在沒有額外 vision 步驟前等於看不見。Claude 的原生 PDF support 把這四件事都變成「直接問就好」。

具體來說，一個 `document` block 讓你可以：

- 摘要一份 10-K 申報文件。
- 從財務表格裡抓特定數字。
- 不用先把圖表拉成 PNG 就能描述它。
- 把 QA 答案錨在一份政策文件的結構上。

課程用的例子是一份存成 PDF 的 Earth 維基文章，請 Claude 用一句話摘要——最小可行示範，證明 document block 端到端都能通。

---

## 課程暗示的 production 考量

課程本身很短，沒列出限制，但配額思維上和 image 同款。做 production PDF 管線時要想：

- **大小邊界。** 非常大的 PDF 每次塞進去都貴。對長篇內容考慮按 section 切檔，只把相關片段送給 Claude。
- **前處理。** 如果你的 PDF 是掃描文件 OCR 而來，PDF 品質直接影響 Claude 的擷取準確度。乾淨 PDF → 更好的答案。
- **Prompt 結構。** 和圖像一樣，prompt 紀律很重要。含糊的「跟我說這份文件」比「用一句話摘要第 3 節」或「把 executive summary 裡所有金額以 JSON 擷取」差很多。
- **Caching。** 如果你常對同一份文件發多個 query，prompt caching 會變得很有吸引力，因為 PDF bytes 佔了輸入的主體。

---

## Common Mistakes

1. **PDF 用 `type: "image"`。** Block type 必須是 `"document"`，對 PDF 用 image block 會被拒絕或誤讀。
2. **錯的 `media_type`。** 必須完全是 `application/pdf`——不是 `pdf`、不是 `application/x-pdf`。
3. **送原始 bytes 而不是 base64。** `data` 欄位是 base64 字串，不是 raw bytes 或檔案路徑。
4. **以為 PDF 便宜。** 長 PDF 每次呼叫都燒真 token。規劃 chunking、考慮 caching。
5. **跳過 prompt 層。** API 給你一份文件；你還是得問一個精準問題。「摘要整份」會產出含糊答案。
6. **忘了訊息處理程式要認 `"document"` blocks。** 如果你的 handler 假設只有 `"text"` 和 `"image"`，加 PDF 會默默壞掉。

---

> **Key Insight**
>
> PDF support 就是 image-block 的 pattern 改兩個欄位：`type` 變 `"document"`、`media_type` 變 `"application/pdf"`。其他所有東西——base64 編碼、content-block 結構、message flow、system prompt、tool use——都完全一樣。真正不同的是 **production 思維**：PDF 比截圖大，所以 chunking、caching、精準 prompt 比一次性圖像輸入更重要。

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**：PDF 是 content-block 變體。記得 block type 是 `"document"`（不是 `"pdf"`），media type 是 `"application/pdf"`。
- **D5 (Enterprise Deployment)**：RAG 的文件處理管線、合約分析、政策 QA——PDF support 常常是最簡單的答案，勝過手搓的 OCR / layout 管線。
- 考題情境：「你要 Claude 讀一份 PDF 合約並擷取免責條款。」答案是 `document` content block + `application/pdf` media type + 一個精準的擷取 prompt。

---

## Flashcards

| Front | Back |
|-------|------|
| Claude 對 PDF 用哪種 block type？ | `"document"`——不是 `"pdf"` 也不是 `"image"`。 |
| PDF 的 media type 是？ | `"application/pdf"`。 |
| 怎麼把 PDF bytes 編碼給 API？ | 把檔案 base64 編碼，字串放在 `source.data`，配 `source.type: "base64"`。 |
| Image 程式碼轉 PDF 要改哪四件事？ | 副檔名（`.png` → `.pdf`）、變數名（`image_bytes` → `file_bytes`）、block type（`"image"` → `"document"`）、media type（`image/png` → `application/pdf`）。 |
| Claude 原生可以從 PDF 擷取哪四種內容？ | 文字內容、內嵌圖片與圖表、表格與資料關聯、文件結構與排版。 |
| 為什麼原生 PDF support 比表面看更重要？ | 它把傳統 OCR + layout + table + chunking 管線收斂成一次 API 呼叫，並原生處理歷來麻煩的表格與圖表。 |
| 摘要 PDF 該用哪種 prompt pattern？ | 和文字一樣的 prompt 紀律——要精準（「用一句話摘要第 3 節」）而不是含糊（「跟我說這份文件」）。 |
| 何時該先把 PDF 切片再送給 Claude？ | 當 token 成本或 context 長度成為瓶頸，或只有少數 section 和問題相關時。 |
