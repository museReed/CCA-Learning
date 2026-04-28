# The Full RAG Flow — PM 視角

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Architecture (22%) 主要；D4 — Safety & Alignment (20%) 次要 |
| Task Statements | 1.3（context management）、4.1（grounded responses） |
| 來源 | building-with-the-claude-api / 05-rag / Lesson 48 |

---

## 一句話總結

完整 RAG flow 有六步，乾淨地切成「一次性前處理 pipeline」和「每次查詢 pipeline」兩半 — 搞懂這個切割是 PM 推理任何 RAG 功能成本、延遲、內容新鮮度的方式。

---

## 心智模型：圖書館卡片目錄

想像一座使用者還沒進來的圖書館：

| 階段 | 圖書館比喻 | RAG 步驟 |
|------|------------|----------|
| Setup | 館員讀每本書、寫索引卡 | Chunk + embed + store |
| 等待 | 卡片目錄整齊待命 | Vector DB 已就緒 |
| 問題 | 訪客問「關於中世紀烹飪的書？」 | User query 到達 |
| 查找 | 館員翻卡找最接近的匹配 | Embed query + cosine similarity |
| 答覆 | 館員把相關書交給訪客 | Retrieved chunks 進 prompt |
| 綜合 | 訪客讀書、寫報告 | Claude 寫最終答案 |

圖書館能運作只因有人事先做了索引工作。那就是 RAG 的前處理 pipeline。查詢時步驟則是館員迎接每位訪客。

---

## PM 白話的六步

```
[前處理 — 每份文件付錢一次，受惠於未來所有 query]
1. Chunk:       「把文件切成可搜尋片段」
2. Embed:       「把每片轉成意義座標」
3. Store:       「把所有座標放進 vector database」

[查詢時 — 每次使用者請求付錢一次]
4. Embed query: 「把使用者問題轉成意義座標」
5. Search:      「用 cosine similarity 找最接近座標」
6. Prompt:      「問題 + top 匹配交給 Claude 回答」
```

**PM 關鍵洞察**：新增一份文件，1-3 跑一次。今天有一百萬使用者問問題，4-6 跑一百萬次。預算成本和延遲代表要知道哪一步住在哪一半。

---

## 為什麼這個切割對產品規劃重要

| 維度 | 前處理側（1-3） | 查詢時側（4-6） |
|------|-----------------|------------------|
| 誰付錢？ | 被未來所有 query 攤提 | 每次使用者請求付一次 |
| 延遲敏感？ | 不 — 背景跑 | 是 — 使用者在等 |
| 新鮮度影響 | 過時 index 代表過時答案 | 永遠讀 index 最新狀態 |
| 失敗爆炸範圍 | 壞 batch 汙染未來 retrieval | 壞 query 傷害一次使用者互動 |
| 成本最佳化 | 更少 re-index、更 aggressive batch | 更小 top-k、快取 embedding |

產品決策會打在不同半邊。「我們要答案反映今天更新」是前處理問題。「我們要 2 秒內答」是查詢時問題。

---

## 「bug」例子當產品課

lesson 的玩具例子用一個含「bug」字的醫療研究 chunk（XDR-47 病毒那種）和一個軟體工程 chunk。使用者問「How many bugs did engineers fix this year?」。

keyword retriever 可能回傳醫療 chunk 只因字面含「bug」。cosine-similarity retriever 會正確回傳軟體 chunk，因為 query 的語意方向匹配軟體 chunk 的語意方向（cosine similarity 0.983 vs. 0.398）。

**這就是 RAG 做對的產品價值**：使用者拿到他們想問的答案，而不是關鍵字找到的答案。對於客服、法律、企業搜尋產品，這個差異會反映在客戶滿意度上。

---

## 給 PM 的 Cosine Similarity

你不需要數學，但需要直覺：

| 分數 | 意義 | PM 白話 |
|------|------|---------|
| +1.0 | 向量同方向 | 完美匹配 |
| ~0.9 | 方向非常接近 | 很有信心相關 |
| ~0.5 | 大致同社區 | 可能相關 |
| 0.0 | 垂直 | 無有意義關聯 |
| -1.0 | 反方向 | 反相關 |

**Cosine distance** 是 `1 - cosine similarity`。小距離＝高相似度。產品儀表板有時顯示其中之一；知道兩者是同一指標、極性相反。

PM 應該問：「我們的 top-k similarity 門檻是多少？」和「top match 相似度低於 X 時，要不要顯示『沒有好答案』回應而不是編造一個？」

---

## 產品用例

| 場景 | pipeline 落點 |
|------|---------------|
| 客服 copilot | 重度 help articles 前處理；快速查詢時 retrieval |
| Chat-with-your-PDF | 使用者上傳 → 上傳時前處理 → 對話時 query |
| 企業知識搜尋 | 持續 re-index Confluence/Drive；高 QPS query 路徑 |
| 法律研究 | 大 corpus，稀少但高風險查詢；品質優於速度 |

---

## PM 決策框架

任何 RAG 產品，要能回答：

| 問題 | 哪一半 | 為什麼 |
|------|--------|--------|
| 文件多常變？ | 前處理 | 驅動 re-indexing 排程與成本 |
| Corpus 多大？ | 前處理 | 驅動儲存與 embedding 成本 |
| 每日多少查詢？ | 查詢時 | 驅動每次查詢預算 |
| 延遲 SLO 是什麼？ | 查詢時 | 驅動 top-k、caching、模型選擇 |
| retrieval 找不到好匹配怎麼辦？ | 查詢時 | 塑造「無答案」UX 避免幻覺 |
| 怎麼對使用者顯示 citation？ | 查詢時 | 最終 prompt／UI 步驟的一部分 |
| 文件變更時怎麼 re-index？ | 前處理 | 必須是 owned 工程流程 |

---

## 常見 PM 錯誤

1. **混淆前處理與查詢時成本** — 搞不清楚為什麼 RAG 某些情境貴、某些情境便宜。
2. **沒有 stale-index 計畫** — 使用者會發現文件更新要好幾天才反映在答案裡。
3. **沒設 similarity 門檻** — 低信心匹配被當高信心匹配對待，導致錯答案。
4. **沒有「無答案」UX** — retrieval 找不到好東西時 Claude 還是會產出，使用者拿到編造內容。
5. **UI 略過 citation** — 使用者無法驗證答案，就抓不到 retrieval 失敗，信任默默崩塌。

> **關鍵洞察**
>
> 六步 RAG flow 其實是兩個 pipeline 共享一個 vector database。前處理是你對每份文件付一次的投資；查詢時是你每次使用者請求要付的經常性成本。PM 把這兩半分清楚就能推理單位經濟、延遲預算、新鮮度、失敗模式 — 這就是「RAG 功能能出貨」與「RAG 功能在 production 默默壞掉」的差別。

---

## CCA 考試關聯

- **D1（Agentic Architecture）**：端對端 RAG 題會考你是否知道六步順序和 cosine similarity 在哪一步。
- **D4（Safety & Alignment）**：grounding flow（retrieve chunk、用 XML tag 包、交給 Claude）是課程裡經典的降幻覺 pattern。
- 熟悉 cosine similarity 範圍（-1 到 +1）和 cosine distance 關係（1 - cosine similarity）。

---

## Flashcards

| Front | Back |
|-------|------|
| RAG flow 的兩半是什麼？ | 前處理（chunk、embed、store — 每份文件一次）和查詢時（embed query、retrieve、prompt — 每次使用者請求一次）。 |
| RAG 的圖書館類比是什麼？ | 館員事先索引書；訪客提問時館員查最接近的索引卡並交出相關書。 |
| Cosine similarity 範圍？ | -1 到 +1。 |
| cosine similarity 0.983 代表什麼？ | 極高相似度 — 兩向量幾乎同方向。 |
| 「bug」例子的 similarity 分數差是多少？ | Query 對軟體 chunk = 0.983；Query 對醫療 chunk = 0.398。 |
| PM 為什麼在意前處理／查詢時切割？ | 它決定成本、延遲、新鮮度、失敗模式在 production 怎麼表現。 |
| 什麼是 cosine distance？ | `1 - cosine similarity` — 一種報告慣例，小值代表高相似度。 |
| 舉一個由查詢時半邊驅動的產品決策。 | 延遲 SLO、top-k 大小、「無答案」UX、caching 策略。 |
| 舉一個由前處理半邊驅動的產品決策。 | Re-indexing 排程、chunking 策略、embedding provider 選擇、corpus 大小預算。 |
