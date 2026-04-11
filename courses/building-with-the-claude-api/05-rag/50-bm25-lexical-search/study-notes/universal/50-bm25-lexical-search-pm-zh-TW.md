# BM25 Lexical Search — PM Perspective（產品視角）

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Architecture（22%）主領域；D5 — Enterprise Deployment（20%）次領域；D2 — Tool Design（18%）也相關 |
| Task Statements | 1.3（context management）、5.2（production search infrastructure） |
| 來源 | building-with-the-claude-api / 05-rag / Lesson 50 |

---

## 一句話總結

BM25 是一個不起眼、已有數十年歷史的搜尋技術，卻悄悄拯救了你的 RAG 產品——在使用者輸入精確 order ID 而你的 AI 助理很有自信地回傳錯的 ticket 的那天。

---

## Mental Model：聰明實習生 vs Ctrl-F 高手

想像兩位助理幫你在一份 500 頁報告裡找資料：

- **聰明實習生（語意搜尋）**：把報告讀完，歸納主題。問「上一季發生什麼事？」他答得很好。問「incident INC-2023-Q4-011 怎樣？」他很有自信地描述另一個 incident，因為他記得「那個是資安相關」，沒去檢查編號。
- **Ctrl-F 高手（BM25）**：任何字面 string 都能瞬間找到，但零理解力。問「上一季發生什麼事？」他聳肩。問「INC-2023-Q4-011」他立刻指出提到這個 ID 的那三頁。

好的研究團隊兩種都要。這就是 hybrid retrieval 對 RAG 產品做的事。

---

## PM 為什麼要在意

純語意 RAG 是 AI 功能最常見的早期失敗模式。產品在 demo 時很漂亮（概念問題答得很好），但實際使用就崩了，因為真實使用者常常輸入：

- Order ID：「查訂單 #78921 狀態」
- SKU：「SKU-GX-42B 還有貨嗎？」
- Error code：「ERR_UNAUTHORIZED_10031 是什麼？」
- Ticket 編號、CVE ID、invoice 編號、員工編號、合約代碼。

這些都可能被純語意搜尋漏掉，回一個很自信但錯誤的答案。BM25（或任何 lexical search）是便宜又可靠的 safety net。

---

## Product Use Cases

### BM25 / Hybrid 是對的選擇

| User Need | 為什麼 BM25 有幫助 |
|-----------|---------------------|
| 精確 ticket / order / incident 查詢 | ID 必須字面符合 |
| 技術文件的 error code 搜尋 | Code 是罕見 token，BM25 一擊命中 |
| 法律合約條款搜尋 | 字面 phrase 關鍵 |
| 產品 SKU / barcode 查詢 | 精確 token，沒語意代理 |
| 法遵 / 政策關鍵字稽核 | 需要字面比對，不是 paraphrase |

### 單靠 BM25 不夠

| User Need | 為什麼還是需要語意搜尋 |
|-----------|------------------------|
| 「怎麼退款？」 | 使用者絕不會打「refund policy section 4」 |
| 「上一季有什麼重點發現？」 | 純概念，沒字面關鍵字 |
| 多語言或改述的 query | BM25 只看字面，太淺 |
| 容錯的產品搜尋 | Lexical match 對拼錯就失效 |

**真正的答案是 hybrid**——兩種並行——不是選邊站。

---

## 四步驟（大白話）

1. **把問題拆成字**——「a INC-2023-Q4-011」變 `["a", "INC-2023-Q4-011"]`。
2. **算每個字有多常見**——「a」到處都是，ID 只出現一次。
3. **罕見字多給分**——ID 被當作強 signal；「a」被當作 noise。
4. **按總分排序文件**——提到罕見字的文件勝出。

注意這裡沒有模型、沒有 embedding API、沒有 GPU。BM25 純粹是文字計數。這就是為什麼它又便宜又快。

---

## PM 決策框架

| 問題 | 如果答 Yes | 含義 |
|------|-----------|------|
| 使用者會輸入字面識別碼（ID、code、SKU）？ | Yes | 組合裡要加 BM25。 |
| 語料是技術類（docs、reports、policies）？ | Yes | Hybrid 幾乎都是贏家。 |
| Latency budget 緊？ | Yes | BM25 latency 是免費的——不呼叫 embedding。 |
| Embedding API 帳單是痛點？ | Yes | BM25 能抵銷成本——query 時不跑 embedding。 |
| 使用者主要問概念問題？ | Yes | 語意搜尋為主，BM25 當安全網。 |

---

## 成本與延遲現實檢查

BM25 是你能加到 RAG 產品上最便宜的檢索：

- **Query 時不呼叫 embedding API**——BM25 完全在你自己的 process 中對 indexed text 跑。
- **Index 建得快**——文字 tokenization 與計數，不用 GPU 數學。
- **記憶體佔用小**——稀疏的 term-document matrix 壓縮效率很好。

不加 BM25 的代價很隱微但嚴重：使用者看到那些他們知道存在的 ID 被「很有自信地答錯」時，信任會悄悄流失。Hybrid search 是便宜的信任保險。

---

## PM 常見錯誤

1. **相信「向量搜尋解決一切」**——不會。使用者一打 ID，純向量 RAG 就破功。
2. **把 BM25 延後當 optimization**——它不是 optimization，它是精確查詢的 correctness feature。
3. **沒有字面 query 的 eval set**——eval 要混概念題跟 ID 題。少一種，regression 就躲起來。
4. **只把一種搜尋的結果拿出來**——hybrid 是合併，不是擇一。下一課講合併策略。
5. **低估使用者信任衝擊**——一個 ID 答錯失去的信任，比十個好答案累積的還多。

> **核心洞見**
>
> Hybrid retrieval 不是進階升級——它是**任何會有使用者輸入精確識別碼的 RAG 產品的基線**。語意搜尋給你「看起來厲害」的答案；BM25 給你字面 query 上「正確」的答案。認真的產品兩個都要。

---

## CCA 考試關聯

- **D1（Agentic Architecture）**：了解 hybrid retrieval 是兩種互補搜尋方法的組合。
- **D5（Enterprise Deployment）**：BM25 在維運上便宜——它是流量放大時不會讓 embedding 成本複利上升的檢索層。
- **D2（Tool Design）**：如果把 retrieval 暴露成 tool，BM25 / 語意 / hybrid 的選擇會形塑 tool description。
- 題目 pattern：「純語意搜尋對含特定 code 的 query 回傳不相關結果——怎麼修？」→ 加 BM25 / hybrid search。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 實習生 vs Ctrl-F analogy 怎麼對應 BM25？ | 語意搜尋像聰明實習生，理解主題；BM25 像 Ctrl-F 高手，找字面 string。團隊兩個都要。 |
| 純語意 RAG 產品什麼時候在 production 崩掉？ | 使用者第一次輸入精確 ID、SKU 或 error code 的時候——語意搜尋經常很自信地回錯文件。 |
| BM25 query time 需要呼叫 embedding API 嗎？ | 不用。它對 indexed text 跑，不呼叫模型，所以便宜又低延遲。 |
| BM25 四個打分步驟（大白話）？ | 1) 把 query 拆成字、2) 算每個字多常見、3) 罕見字多給分、4) 按總分排 document。 |
| RAG 產品應該用 BM25 取代語意搜尋嗎？ | 不——兩個並行跑（hybrid）。互相補漏。 |
| RAG eval set 應該長什麼樣？ | 概念題和字面識別碼題混搭，才能量化 hybrid 品質。 |
| 忽略 BM25 的 PM 最大風險是什麼？ | 使用者信任崩盤——一個 ID 答錯侵蝕的信任，比很多好的概念答案累積的還多。 |
| 哪類 token 最受益於 BM25？ | 罕見、技術性的字面 token：ID、SKU、error code、ticket 編號、CVE 編號、合約代碼。 |
