# Prompt Caching — Engineering Deep Dive（繁體中文）

| 項目 | 詳情 |
|------|------|
| 考試領域 | D5 — Enterprise Deployment (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 5.1（成本／延遲優化）、5.2（production 效能）、1.2（multi-turn 效率） |
| 來源 | building-with-the-claude-api / 06-extended-features / Lesson 56 |

---

## One-Liner

Prompt caching 是 production 等級的優化機制，把 Claude 每次 request 要做的 preprocessing 工作（tokenization、embeddings、context 分析）存起來，讓後續同前綴的 request 能直接重用，而不是每次從零重算——結果就是更快、更便宜。

---

## Claude 一般怎麼處理 request？

每條你送給 Claude 的訊息，在真正產出任何輸出 token 之前，都要先走一條昂貴的 preprocessing pipeline：

1. **Tokenization（斷詞）** — 把 prompt 切成一個個 token。
2. **Embedding（向量化）** — 每個 token 轉成高維向量。
3. **Context 分析** — 根據上下文補充語境，讓後面的 attention 能推理整個序列。
4. **生成** — 前三步做完，才開始真正產出文字。

關鍵點：回傳完答案之後，**這些 preprocessing 結果全部被丟掉**。一分鐘後你再送同一份 6K token 的 prompt，Claude 會把所有步驟重跑一次。

---

## 為什麼「丟掉」會是問題

只要你的 workflow 重複用到同一份 base content，這種浪費就很明顯：

- 一個對話裡你不斷要 Claude 改寫同一份 summary。
- 對同一份 50 頁 PDF 連問 20 個問題的文件分析流程。
- Agent loop 每一輪都要帶同樣的 system prompt + tool schema。

第 2 次 request 時，Claude 得把剛剛幾秒前才分析過的內容再 preprocess 一遍。課程原話：「*我剛剛才處理過那段訊息、然後把結果全丟了——明明可以重用！*」

這個成本要付兩次：一次是延遲（input 處理時間），一次是金錢（input token 計費）。

---

## Prompt Caching 怎麼解？

Prompt caching 改寫這條 workflow，核心是：**preprocessing 的結果不再丟掉，而是存起來**。

- 第一次 request，Claude 照常 preprocess，但把中間結果寫入 cache。
- Cache 像一張對照表：「如果我之後再看到一模一樣的前綴，就直接重用結果。」
- 後續 request 如果送了一模一樣的前綴，命中 cache，就跳過 preprocessing 直接進入生成，只為新的（未 cache 的）token 計費。

結果：昂貴的 preprocessing 費用被攤平在許多次呼叫之間，而不是每次都重新付一次。

---

## 主要好處

| 好處 | Production 意義 |
|------|-----------------|
| **更快的回應** | Cache 命中的 request 跳過 tokenization／embedding／context，time-to-first-token 下降。 |
| **更低的成本** | 命中的部分以顯著折扣計費，不再按 fresh input token 收費。 |
| **自動化優化** | 第一次 request 寫入 cache，後續 request 自動讀取——不用自己寫 client 端快取邏輯。 |

---

## 重要限制

| 限制 | 含義 |
|------|------|
| **Cache 存活 1 小時** | 只對「同一小時內頻繁重複呼叫」的 workflow 有用。閒置對話過期就沒了。 |
| **使用場景有限** | 只有你「重複送同樣內容」時才有用，一次性 prompt 沒有幫助。 |
| **需要高頻率** | 同一前綴重用越頻繁，省得越多；零星呼叫可能連設定成本都不划算。 |

---

## Prompt Caching 什麼時候最有用？

課程點出兩個典型場景：

1. **文件分析 workflow** — 同一份大型文件被多次引用，你在上面問不同問題。文件只 cache 一次，後續問題便宜地讀。
2. **反覆編輯任務** — base content（例如草稿）不變，你只針對特定段落反覆微調。草稿被 cache，修訂是增量。

更廣義地說，只要是「**大而穩定的前綴 + 小而變動的後綴**」的 workflow，都是強力候選。

---

## Common Mistakes

1. **對一次性 prompt 開 cache** — 為永遠不會再被讀的內容付 cache-write 附加費。Cache 只有「一小時內被重用」才省錢。
2. **以為 caching 會自動發生** — 不會。沒有明確 opt-in（cache breakpoint，見 lesson 57），Claude 照常丟掉 preprocessing。
3. **忽略 1 小時 TTL** — 把依賴 cache 的 workflow 設計成低頻執行，cache entry 重用前就過期。
4. **以為 cache 只省延遲** — 它同時省可觀的 input token 成本，通常這才是 production 最大的勝利。
5. **低估 preprocessing 成本** — 以為 input token 「免錢」。面對大型 system prompt 和 tool schema，它佔總成本和總延遲比想像中大很多。

---

> **Key Insight**
>
> Prompt caching 本質是**攤平（amortization）技巧**：大而穩定前綴的昂貴 preprocessing 只付一次，之後一小時內所有共用這段前綴的呼叫都可重用。在 production，這是 agent loop、RAG pipeline、以及任何重複送同樣 context 的 workflow 最大單一的成本／延遲優化手段。是 D5 Enterprise Deployment 的基本功。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）** — caching 是 task 5.1（成本／延遲）下核心的 production 優化。要知道 caching 同時降**成本和延遲**。
- **D1（Agentic Architecture）** — agent loop 帶穩定的 system prompt 和 tool schema，是 caching 的典型受益者；同樣的 context 每輪都要送一次。
- 考題常見問法：「同一個大 prompt 要被重複送時，怎麼降低成本與延遲？」→ 答案是 prompt caching。

---

## Flashcards

| Front | Back |
|-------|------|
| Prompt caching 解什麼問題？ | Claude 每次 request 都要重跑昂貴的 preprocessing（tokenization、embeddings、context 分析），即使剛剛才處理過同樣內容。Caching 重用那份工作。 |
| Claude 一般做哪四個 preprocessing 步驟？ | Tokenization、embedding、基於上下文的 context 分析，然後才是輸出生成。 |
| Cache 存活多久？ | 一小時。 |
| Prompt caching 提供哪兩個好處？ | 更快的回應（更低延遲）以及 cache 部分更低的成本。 |
| 什麼情境下 prompt caching 沒用？ | 一次性 prompt、一小時內打不到同一前綴的零星 workflow、或每次都在變的內容。 |
| 說兩個典型的 prompt caching 場景。 | 文件分析 workflow（對同一份長文件問很多問題）和反覆編輯任務（同一份 base content 反覆微調）。 |
| Prompt caching 是自動的嗎？ | 不是——必須明確啟用；不 opt-in 的話 Claude 照常丟掉 preprocessing。 |
| 啟用 caching 後，第一次 request 發生什麼事？ | Claude 照常做 preprocessing，但把中間結果存起來，後續 request 便可重用而不用重算。 |
