# PDF Support — PM Perspective

| 項目 | 內容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — 主要；D5 — Enterprise Deployment (20%) — 次要 |
| Task Statements | 2.2（content blocks）、2.1（多模態輸入）、5.2（文件處理） |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 54 |

---

## One-Liner

PDF support 把「讓 Claude 讀公司文件」從一個多週的整合專案變成一種新 content block——把傳統的 OCR 加 layout 管線收斂成單次 API 呼叫，讓每一類以文件為核心的產品突然變得可行。

---

## Mental Model：取代文件入料團隊

多數企業都有一個——無論正式或非正式——負責從 PDF 擷取結構化意義的團隊。法務讀合約、財務從財報擷取數字、合規部門把政策對規範做比對、營運部門讀供應商規格書。

PDF support 就是把一條 Claude 驅動的入料管線交到這個團隊手上：一次 API 呼叫就讀整份文件、理解結構、讀表格與圖表、回答人類原本要手動處理的問題。人不會不見，他們的工作從「讀並擷取」變成「審查 Claude 擷取出來的東西」。

---

## PM 為什麼該在意

每個碰 PDF 的企業產品過去都苦於擷取可靠度。傳統 stack 長這樣：OCR 引擎 → layout parser → table detector → chunking 邏輯 → prompt 管線。每一階都加 latency、成本與錯誤。升級其中一環很少能修另一環。

PDF support 用單次 Claude 呼叫取代整條 stack，原生讀文字、表格、圖表與結構。產品面的意涵是：一堆「太難可靠上線」的功能變得一個 sprint 就能做：

- **合約 QA**——「這份 MSA 的免責條款是什麼？」
- **財務擷取**——「從這份 10-Q 拉出所有營收項目。」
- **政策合規**——「這份政策文件有提到資料保存嗎？引出章節。」
- **規格書摘要**——「給非技術買家一份產品規格摘要。」
- **研究消化**——「這篇論文對方法 X 的結論是什麼？」

PM 的工作從「怎麼蓋 parsing 管線？」變成「我們要模型回答的精確問題是什麼？」

---

## Product Use Cases

### PDF support 合適的情境

| 需求 | 為何可行 |
|------|---------|
| 單份文件的摘要或 QA | 單次 API 呼叫，原生讀文字 + 表格 + 圖表 |
| 從已知文件類型擷取特定欄位 | 明確 prompt + rubric 產生可靠的結構化輸出 |
| 把答案錨在權威文件上 | 完美搭配 citations 做可追溯的依據 |
| 取代脆弱的 OCR / layout 管線 | 原生能力一次移除好幾個失敗模式 |
| 分析 PDF 內的圖表或表格 | 不需要額外的 vision 或擷取步驟 |

### PDF support 不夠的情境

| 需求 | 更好的選擇 |
|------|-----------|
| 在上千份文件中搜尋 | 你還是需要 RAG——PDF support 取代擷取階段，不取代檢索階段 |
| 即時掃描大量即時文件 | 大語料要先一次前處理並 cache / 建索引 |
| 低品質掃描件的像素級表單擷取 | 針對標準化表單，專門 OCR 工具在成本和準確度上可能更優 |
| 高敏感度文件搭配嚴格資料管控 | 先檢視資料駐地和加密要求；document support 仍然要把 bytes 送上網路 |

---

## PM 決策框架

| 問題 | 若答 Yes | 意涵 |
|------|---------|------|
| 使用者 workflow 要讀的 PDF 變異太大、傳統 parser 搞不定嗎？ | Yes | PDF support 是強力候選。 |
| 文件裡有表格、圖表或複雜 layout 嗎？ | Yes | 原生 PDF 讀取在這裡相對 legacy 管線有巨大優勢。 |
| 使用者會需要驗證答案來源嗎？ | Yes | 把 PDF support 和 citations（課程 55）配對。 |
| 文件通常非常長或在多次呼叫裡重複？ | Yes | 規劃 chunking 與 prompt caching 控成本。 |
| 問題的類別明確（摘要、欄位擷取、QA）？ | Yes | Prompt 寫成精確問題，不要「跟我說一下這份」。 |
| 我們處理受管制或機密資料嗎？ | Yes | 出貨前審廠商的資料處理、logging 與保存政策。 |

---

## Cost、Latency、UX 權衡

PDF support 比看起來更貴。長 PDF 主導每次呼叫的輸入 tokens。三個要預算的 pattern：

1. **Chunking。** 若使用者對長文件問的是狹窄問題，只把相關 section 送給 Claude。PRD 要寫清楚 chunk 的挑選方式（啟發式、embedding 搜尋、section 標題）。
2. **Caching。** 同一份文件被反覆 query 時，prompt caching 讓文件 bytes 在第一次呼叫之後幾乎免費。這是 Claude API 裡最乾淨的成本勝利之一。
3. **Latency。** Prompt 裡放長 PDF 會拖慢第一個 token。互動功能要顯示 loading state，描述模型正在做什麼（「正在讀合約…」）。

PDF 功能的 PRD 清單：

- 預期文件大小分佈。
- Chunking 或 caching 計畫。
- Prompt 精準度計畫（功能問的是什麼問題？）。
- 有標註的 eval set，涵蓋你在乎的擷取。
- 若答案具後果，要有 human-in-the-loop 審核流程。

---

## 和 Citations 的配對

課程 55（Citations）是 PDF support 的天然搭檔。Citations 把 Claude 的答案變成可驗證的軌跡：使用者能看到 PDF 裡哪幾句話支撐那個答案。任何使用者需要信任答案的功能——法務、財務、醫療、合規——都應該把 PDF support 和 citations 配對。這是 API 裡企業文件 workflow 槓桿最高的組合。

---

## Common PM Mistakes

1. **以為 PDF support 取代 RAG。** 它取代單份文件內的擷取階段，不取代多份文件間的檢索。語料有上千份，仍然需要檢索。
2. **寫含糊 prompt。** 「跟我說這份合約」不達標。寫精確的：「用兩句話摘要責任條款並列出上限金額。」
3. **忘記對重複 query 用 prompt caching。** 每次都送整份 50 頁 PDF 而不 cache，財務會注意到這條 line item。
4. **沒搭配 citations。** 以文件為依據的功能應該讓使用者能驗證；citations 是那層信任的 UX。
5. **跳過資料處理審查。** PDF 常含機密資訊。出貨前確認廠商資料政策。
6. **沒建 eval set。** 擷取功能 demo 漂亮、在 production 默默壞掉。一份小型標註集能早期抓到 regression。

---

> **Key Insight**
>
> PDF support 不是炫目的功能，但它是讓嚴肅的企業文件 workflow 不用再蓋 OCR 加 layout stack 的那個功能。真正的產品槓桿來自三個紀律：精準的 prompt、用 chunking 或 caching 控成本、以及搭配 citations 拿到可驗證答案。把這三件事做對，一大類「太難上線」的文件功能就變成兩週的工程。

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**：把 PDF 認成 `document` content block + `application/pdf` media type——和 image block 同一套 pattern。
- **D5 (Enterprise Deployment)**：文件處理管線、chunking、caching、以及和 citations 配對都是 production 考點。
- 情境題：「你要 Claude 回答一份 PDF 合約的問題並顯示來源。」預期答案是 `document` block + `application/pdf` + 啟用 citations。

---

## Flashcards

| Front | Back |
|-------|------|
| PDF support 的文件入料團隊類比是什麼？ | PDF support 給企業一條 Claude 驅動的入料管線，像法務或財務團隊那樣讀文件，取代脆弱的 OCR / layout stack。 |
| 什麼時候 PDF support 是錯的工具？ | 問題是大語料檢索（仍需 RAG）、低品質掃描件的像素級表單擷取、或嚴格資料駐地管控下的文件處理。 |
| PDF 功能的三個 PM 權衡？ | 文件大小（token 隨長度成長）、chunking vs 整份送、以及對同文件重複 query 的 prompt caching。 |
| 哪個 extended feature 是 PDF support 的天然搭檔？ | Citations——把 Claude 的擷取變成 PDF 內可驗證的來源指針。 |
| PDF 功能的 PRD 該包含什麼？ | 預期文件大小、chunking / caching 計畫、精準 prompt / 問題規格、有標註的 eval set、以及資料處理審查。 |
| 哪個常見 PM 錯誤把 PDF support 當全套 RAG？ | 以為它取代檢索。它只取代單份文件內的擷取階段；多份文件間的檢索仍是另一個問題。 |
| 為什麼企業文件功能應該把 PDF support 與 citations 配對？ | 讓使用者能驗證答案來源——對法務、財務、醫療、合規這類信任不可妥協的工作流至關重要。 |
| PDF support 怎麼改變 PM 的工作？ | 從「怎麼蓋 parsing 管線？」變成「模型該回答的精確問題是什麼，以及我們怎麼驗證它？」 |
