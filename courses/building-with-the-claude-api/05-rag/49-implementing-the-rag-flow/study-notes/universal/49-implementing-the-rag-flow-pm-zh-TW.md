# Implementing the RAG Flow — PM Perspective（產品視角）

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Architecture（22%）主領域；D5 — Enterprise Deployment（20%）次領域 |
| Task Statements | 1.3（context management）、5.2（production search infrastructure） |
| 來源 | building-with-the-claude-api / 05-rag / Lesson 49 |

---

## 一句話總結

RAG 把一堆私有文件變成產品功能——五步驟流程（切、embed、存、對 query embed、搜尋）是讓 Claude「認識你們公司」所需最小的投資。

---

## Mental Model：會貼便利貼的圖書館員

想像你請了一位聰明的研究助理，他知道所有公開資料，但從沒看過你們內部 wiki。你不可能每次問問題前都叫他讀 10,000 頁。

所以你：

1. 把 wiki 切成一張張主題便利貼（**chunk**）。
2. 每張便利貼貼上一張顏色貼紙代表它的意思（**embed**）。
3. 按顏色把便利貼歸檔到一個巨大牆面組織器（**vector store**）。
4. 使用者問問題時，你在問題上貼一張相同規格的顏色貼紙（**query embedding**）。
5. 走到牆邊拿幾張顏色最接近的便利貼（**similarity search**）。

助理只讀這幾張便利貼回答——快、準、而且有實際 wiki 作根據。

---

## PM 為什麼要在意

以下需求預設答案都是 RAG：

- 「助理要認得我們內部文件。」
- 「它要能回答我們產品目錄的問題。」
- 「客服要能看到相關的過去工單。」
- 「工具要能參照公司政策回答。」

沒有 RAG，Claude 只能給通用答案。有 RAG，Claude 的答案**以貴公司 source of truth 為基礎**——底層文件一更新，答案就跟著更新。

---

## Product Use Cases

### RAG 是對的選擇

| User Need | 為什麼 RAG 合適 |
|-----------|-----------------|
| 「問我們知識庫」的助理 | 語料龐大、問題多樣、需要新鮮度 |
| 客服自助化 | 要根據現行 help article 作答 |
| 內部 wiki / onboarding copilot | 員工對已知文件問非結構化問題 |
| 產品目錄搜尋（「推薦 1,500 美元以下筆電」） | 意圖語意比規格更重要 |
| 合約 / 政策查詢 | 大型法律語料，每次查詢聚焦 |

### RAG 過頭或不對的情況

| User Need | 更好的方案 |
|-----------|------------|
| 一般聊天或 brainstorm | 基本模型就夠 |
| 精確 unique ID 查詢 | 正常 DB query，不用 vector search |
| 即時資料（價格、庫存） | Tool use，不要用會 stale 的 index |
| 超小語料（<幾頁） | 直接貼在 system prompt |

---

## 五步驟（大白話）

1. **Chunk**——把每份文件切成一小段一小段。
2. **Embed**——把每段變成一個表達它意思的 vector。
3. **Store**——把 vector 連同原文存進可搜尋的 index。
4. **Embed 問題**——把 user query 轉成同一類型的 vector。
5. **搜尋**——回傳最相似的 chunks 給 Claude 當 context。

產品洞見：步驟 1–3 是**批次預處理**（付一次），步驟 4–5 在每筆 user query 都要跑（按次付）。

---

## PM 決策框架

| 問題 | 如果答 Yes | 含義 |
|------|-----------|------|
| 語料是否大於 context window？ | Yes | 必須用 RAG。 |
| 內容更新頻率高於每月一次？ | Yes | 編列 ingestion/refresh pipeline 預算。 |
| 使用者問的是語意問題（不是精確查）？ | Yes | Vector search 是對的檢索模式。 |
| 使用者也會問具體 ID / SKU / error code？ | Yes | 規劃 hybrid search（後續課程）。 |
| 語料屬機密？ | Yes | 評估 vector store 自架還是雲端以符合法遵。 |

---

## 成本與新鮮度現實檢查

RAG 有三個經常性成本中心，PM 常常低估：

- **Embedding 成本**：每個 chunk embed 一次；每個 query 每次都 embed。會隨語料和流量放大。
- **儲存成本**：vector index 隨語料大小和 chunk 數量成長。要編列 index rebuild 成本。
- **Ingestion / refresh latency**：如果文件每天更新，index 不跑 refresh job 會一天內就 stale。一開始就決定 SLA。

好 PM 的習慣：PRD 裡寫一行「RAG freshness SLA」——例如「知識庫答案最多不超過 24 小時 stale」。

---

## PM 常見錯誤

1. **承諾即時知識，但 index 每晚才 refresh**——使用者幾天內就抓到 stale 答案。
2. **忽略 chunking 策略**——糟糕 chunking 會悄悄拉低答案品質，還被罵「Claude 很笨」。
3. **沒做 eval 就 ship**——上線前要有一組「問題 + 預期 citation」的 test set 才抓得到 regression。
4. **沒 log retrieved chunks**——使用者抱怨答案爛，看不到當時取回哪些 chunks 根本沒法 debug。
5. **以為語意搜尋能處理精確查詢**——經常漏 ID 和代號，通常需要 hybrid search（BM25 + 語意）。

> **核心洞見**
>
> RAG 不是模型功能——它是**資料 pipeline 的產品決策**。品質上限由語料整理、chunking 策略、freshness SLA 決定，不是由模型決定。把 RAG 當成「神奇地讓 Claude 認得我們文件」的 PM 會低投入在 pipeline 上，最終 ship 出令人失望的功能。

---

## CCA 考試關聯

- **D1（Agentic Architecture）**：RAG 是擴充 Claude 知識超越訓練資料的經典 pattern。
- **D5（Enterprise Deployment）**：了解 production 跑 vector index 的成本與 freshness 取捨。
- 題目模式：「Claude 不認識我們內部文件——該用什麼 pattern？」→ RAG。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 便利貼圖書館員 analogy 怎麼對應 RAG？ | 把 wiki 切成便利貼、每張貼一張意思貼紙、按顏色歸檔、把問題貼同類貼紙、抓最近的便利貼。 |
| 什麼時候 RAG 是錯的工具？ | 精確 ID 查詢（用 DB）、即時資料（用 tool use）、或超小語料（直接放 system prompt）。 |
| 哪些 RAG 步驟是 batch 預處理？哪些是 per-request？ | Chunk、embed、store 是預處理（付一次）。embed query + 搜尋每次 user request 都跑。 |
| RAG 功能 PRD 必須寫什麼？ | Freshness SLA、eval set、retrieval logging、embedding + vector store 成本預算。 |
| 為什麼 chunking 策略對 PM 很重要？ | 爛 chunking 會悄悄拉垮答案品質，卻被誤會成「模型很笨」——其實是你管的 pipeline bug。 |
| 讓 Claude「認得你們公司」所需最小的單位是什麼？ | 五步驟 RAG 流程：chunk、embed、store、embed query、搜尋。 |
| RAG index 該多久 refresh 一次？ | 取決於底層文件更新頻率；SLA 是 PM 在 PRD 裡的決策。 |
| 使用者在 RAG 功能裡問精確 ID，你要怎麼辦？ | 規劃 hybrid search——把 BM25 lexical search 跟 semantic search 合併（下幾堂課會教）。 |
