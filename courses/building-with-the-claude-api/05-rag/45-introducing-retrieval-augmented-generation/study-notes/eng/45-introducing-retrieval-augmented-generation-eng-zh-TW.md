# Introducing Retrieval Augmented Generation — 工程深度解析

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Architecture (22%) 主要；D4 — Safety & Alignment (20%) 次要 |
| Task Statements | 1.3（context management）、4.1（grounded responses） |
| 來源 | building-with-the-claude-api / 05-rag / Lesson 45 |

---

## 一句話總結

RAG（Retrieval Augmented Generation）解決「文件太大塞不進 prompt」的問題：先把文件切成 chunks 存起來，使用者提問時只注入最相關的片段。

---

## 能力牆：大型文件

想像一份 800 頁的財報，使用者問「這家公司有哪些 risk factors？」。原始文字放不進一次 `messages.create` 呼叫。這不是 prompt engineering 問題，而是架構問題。

三個力量把「全部塞進去」的做法打掉：

- **context window 硬限制** — 有些文件就是比模型支援的長度還長。
- **品質下降** — prompt 太長時 Claude 效果會變差，相關訊號會被雜訊淹沒。
- **成本與延遲** — prompt 越大 token 越多，處理越慢。

---

## 做法 1：Prompt Stuffing（基準做法）

最簡單的做法是把文件所有文字抽出來直接放進 prompt：

```
Answer the user's question about the financial document.

<user_question>
{user_question}
</user_question>

<financial_document>
{financial_document}
</financial_document>
```

短文件這樣做完全 OK，也是當內容舒服放進 context 時的正確預設值。它有一個重要優點：零前處理、零 retrieval 邏輯、搜尋層零 bug。

一旦文件（或整個 corpus）超過 context window 的舒適比例，它就失效。

---

## 做法 2：RAG — 先切塊再檢索

RAG 走兩個階段：

1. **前處理（offline）** — 把每份文件切成較小的 chunks 存起來。每份文件做一次。
2. **查詢時（online）** — 使用者提問時，在 chunks 裡搜尋最相關的幾塊，只把那幾塊塞進 prompt。

所以使用者問「What risks does this company face?」會觸發一次 lookup，找到 "Risk Factors" 那一節，那一塊（加上問題）才是 Claude 看到的內容。

這就是 RAG 的基本形狀：**chunk → index → retrieve → prompt**。Lessons 46-48 逐步填滿每個步驟。

---

## 好處

- **聚焦** — Claude 只看到相關內容，推理時不會被干擾
- **可擴展** — 可以處理遠大於 context window 的文件與 corpus
- **多文件** — 單一 index 可以跨多份檔案
- **更便宜更快** — prompt 小 token 成本低、延遲低

---

## 挑戰

- **前處理成本** — 每次新增或更新文件都需要跑 chunking pipeline
- **retrieval 品質** — 需要真的能找到「相關」chunks 的搜尋機制；retrieval 爛了答案就錯
- **context 不足** — 被撿回來的 chunk 可能缺了 Claude 需要的周邊脈絡（例如定義在前一節）
- **chunking 策略選擇** — 等長切割、按 section 切、semantic 切，各有取捨

RAG 用**複雜度**換**可擴展性與效率**。corpus 放得進 context 就不要用 RAG；放不進就幾乎一定要用。

---

## 何時用 RAG

| 情境 | 用 RAG？ |
|------|----------|
| 5 頁 PDF、單一文件 | 不用 — 直接塞 prompt |
| 800 頁的財務申報 | 要 |
| 公司知識庫上千篇文章 | 要 |
| 單一使用者問題查一份固定的 2000-token FAQ | 不用 |
| 需要即時、變動的資料（天氣、股價） | 不用 — 用 **tool use** |

RAG 適合**大型、相對穩定的 corpus**，需要在文字上做 semantic search。Tool use 適合**即時、動態資料來源**，需要即時讀取。

---

## CCA Task 對應

- **Task 1.3（Context Management）** — RAG 是 context management 的代表 pattern。你在決定*哪些* context 進 window，不只是*要不要*放 context。
- **Task 4.1（Grounded Responses）** — 注入來源 chunks 給 Claude 一個事實基礎，降低幻覺。這把 RAG 連到 Safety & Alignment 領域。

---

## 工程深度：為什麼 RAG 屬於 D1

架構層面看，RAG 是一個 **retriever + generator** pipeline。retriever 不是 Claude 的一部分，是你擁有的 deterministic 程式碼；generator 是 Claude，用你 retriever 組好的 prompt 來呼叫。這個分離很重要：

1. **retriever 可以單元測試** — 給 query X，是否回傳 chunk Y？
2. **retriever 可以替換** — 從 keyword 換成 semantic 換成 hybrid search，都不用動模型
3. **可以稽核 grounding** — 每個答案都可以追到特定 chunk，這是 safety 贏面

RAG 也是走向 agentic architecture 最簡單的第一步。retrieval 一旦變成 function call，就離把它包成 Claude 自己選擇呼叫的 **tool** 不遠，這就是 RAG 與 Ch04（Tool Use）交會點。

---

## 常見錯誤

1. **prompt stuffing 就夠用還硬要 RAG** — 文件放得進 context 的話，RAG 只是增加複雜度沒有好處。
2. **把 RAG 和 tool use 搞混** — RAG 處理靜態文字 corpus；tool use 處理即時資料。兩個是不同 pattern。
3. **把 retrieval 當成解決了的問題** — 糟糕的 chunking 或 retrieval 會默默回傳錯的 chunks，Claude 會很有信心地根據錯內容回答。
4. **prompt 裡沒有 citation 標記** — 不標明 chunk 來源，就失去 RAG 一半的價值（可稽核性）。
5. **忘了 chunk overlap / 邊界 context** — 定義或 header 被切掉，chunk 看起來相關但缺關鍵細節。

> **關鍵洞察**
>
> RAG 不是模型能力，而是**應用層架構**。Claude 不會「做 RAG」；是你的程式碼組出含 retrieved chunks 的 prompt 再交給 Claude。也就是說每個 RAG bug 都是應用層 bug，每個 RAG 改善都是應用層改動。pipeline 要自己擁有。

---

## CCA 考試關聯

- **D1（Agentic Architecture）**：RAG 是基礎的 context augmentation pattern。預期會看到「大型 corpus、問問題」的情境題 → RAG。
- **D4（Safety & Alignment）**：RAG 把回答 grounded 在 retrieved text，降低幻覺，這是核心 alignment pattern。
- 注意陷阱：題目描述**即時資料**（天氣、價格）應答 **tool use**，不是 RAG。描述**穩定文件 corpus** 才答 RAG。

---

## Flashcards

| Front | Back |
|-------|------|
| RAG 解決什麼問題？ | 處理無法塞進單一 prompt 的大型文件：切成 chunks、查詢時只注入相關片段。 |
| RAG pipeline 的兩個階段？ | 前處理（chunk + index）與查詢時（retrieve + prompt）。 |
| 為什麼不全部塞進 prompt？ | context window 限制、長 prompt 品質下降、成本與延遲變高。 |
| RAG 相對 prompt stuffing 的三個好處？ | 聚焦相關內容、可擴展到大型 corpus、成本與延遲較低。 |
| RAG 的三個挑戰？ | 需要前處理 pipeline、retrieval 品質難做、chunk 可能缺周邊 context。 |
| 什麼情況**不**該用 RAG？ | 文件放得進 context window，或需要即時資料（用 tool use）。 |
| RAG 主要對應哪個 CCA 領域？ | D1 — Agentic Architecture，透過 context management。 |
| RAG 為什麼能降低幻覺？ | 把權威來源文字注入 prompt，給 Claude 一個 grounded 的事實基礎。 |
