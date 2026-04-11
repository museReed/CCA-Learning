# A Multi-Index RAG Pipeline — PM Perspective（產品視角）

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Architecture（22%）主領域；D5 — Enterprise Deployment（20%）次領域 |
| Task Statements | 1.3（context management）、5.2（production search infrastructure） |
| 來源 | building-with-the-claude-api / 05-rag / Lesson 51 |

---

## 一句話總結

Multi-index RAG pipeline 是一種架構 pattern，讓你可以持續加入新的搜尋能力（語意、keyword、recency、domain-specific）而不需要重構——給你的產品在學到使用者真正會問什麼後，提升 retrieval 品質的空間。

---

## Mental Model：專家評審團

想像一個料理比賽有三位評審：風味專家、擺盤專家、技法專家。每位用完全不同的尺度打分——星星、字母、百分比。你不能直接平均他們的分數，數字不可比。

所以你改要求每位評審對菜色**排名**：第一、第二、第三。然後一道在多位評審都排名前面的菜就會浮到整體最上面，就算沒有任何單一評審的原始分數會選它。

這就是 reciprocal rank fusion 對搜尋做的事：

- **向量搜尋**是「風味」評審——理解意思。
- **BM25** 是「食材標籤」評審——檢查字面比對。
- 未來的 index 是新評審——recency、domain、graph——各自有不同視角。

Retriever 是那位收集排名、產出公平最終分數的主評審。

---

## PM 為什麼要在意

Multi-index retrieval 是 RAG 從 prototype 走向可擴充產品的轉折點。它重要是因為：

- **成長路徑已經內建**——加入新 retrieval signal（freshness、popularity、domain）不必動其他產品部分。
- **品質會複利**——每個新 index 接住前一個漏掉的；合併後的品質打敗任何單一方法。
- **故障模式彼此隔離**——一個 index 退化，其他還可以服務。維運上這很珍貴。
- **Eval 變可控**——可以獨立 A/B test 每個 index（加一個、量測、留下或移除）。

---

## Product Use Cases

### Multi-Index Retriever 划算的情況

| User Need | 為什麼多 index 有幫助 |
|-----------|------------------------|
| 概念 + 字面混合的 query | 語意 + BM25 各自覆蓋 |
| Freshness 重要（「這週有什麼新的？」） | 在現有兩個之外加 recency index |
| 多 domain 知識庫 | 加 domain-routing index 給專業文件加權 |
| Long-tail query（「罕見產品名」） | Lexical index 接住語意漏掉的 |
| 法律 / 法遵同時需要主題與字面 | Hybrid 是唯一可靠答案 |

### Multi-Index 過頭的情況

| User Need | 更好的方案 |
|-----------|------------|
| 超小語料（<100 份文件） | 一個 index 就夠，維運成本占比太高 |
| 永遠只問概念問題 | 純語意就好——加更多之前要先量測 |
| Latency 預算很緊（<100ms） | 每加一個 index 都拉長 latency，要算取捨 |
| 早期 MVP | 先 ship 純語意，等真實 query 逼你才加 BM25 |

---

## Reciprocal Rank Fusion（大白話）

想像每個搜尋方法給你一個 **top-3 list**。你不在乎每個方法有多自信；你只在乎每份文件在每份 list 上是第幾名。

- 第一名 = 很多分
- 第二名 = 少一點分
- 第三名 = 一點點分
- 沒上 list = 那個 source 給 0 分

把每份文件在所有 list 拿到的分數加起來。總分最高的贏。在兩份 list 都排前面的文件，幾乎一定會贏過只在一份 list 排前面的。

這就是 reciprocal rank fusion。它是一個公平合併搜尋結果的方法，不需要底下的方法對「分數」意思達成共識。

---

## PM 決策框架

| 問題 | 如果答 Yes | 含義 |
|------|-----------|------|
| 使用者同時問概念與字面 query？ | Yes | 需要 hybrid——至少語意 + BM25。 |
| Freshness 是產品承諾？ | Yes | 加一個 recency / time-weighted index。 |
| 有不同的內容 domain（docs、tickets、code）？ | Yes | 考慮 per-domain index，按 query 類型 routing。 |
| 有 eval set？ | No | 先建一個——沒量測就調不了 multi-index。 |
| Latency 預算很緊？ | Yes | 從兩個 index 開始，量測，再擴張。 |

---

## 成本、延遲、維運取捨

每多一個 index 都有成本。好的 PM 要明確編列：

- **Index 建構成本**——每次 ingest 都要寫到每個 index。要編列 CPU + memory + storage。
- **Query 延遲**——每個 index 都加 latency，通常並行，所以總延遲是 max(per-index latency) + fusion overhead。
- **維運面向**——每個 index 都是新的會壞、會 stale、會需要 reindex 的東西。
- **Eval 複雜度**——加 index 意味著 re-run eval set，確認沒把既有成果搞爛。

建議順序：先上純語意 → 字面 query 開始失敗時加 BM25 → 只有在真的需要 freshness 時加 recency → 只有在 eval 證明 routing 贏的時候加 domain index。

---

## PM 常見錯誤

1. **因為聽起來很聰明就加 index**——沒 eval 的話，新 index 可能反而傷害品質。一定要量測。
2. **把 RRF 當魔法**——只有當每個 index 真的貢獻有用排名時品質才會提升。沒用的 index 還是照吃 latency。
3. **跳過 eval set**——沒 eval 就不知道哪個 index 造成什麼改變，regression 會躲起來。
4. **忽略延遲複利**——每個 index 都有 latency 成本；「六個 index 並行」不是免費的。
5. **把 retrieval 細節露給使用者**——做對的 multi-index retrieval 對使用者是隱形的，他們不該看到「哪個 index 找到這個 chunk」。細節內部留。

> **核心洞見**
>
> Multi-index retrieval 是讓你的 RAG 產品能持續改進而不用改寫的架構。Retriever + RRF pattern 是一份組合契約：每個新的 retrieval signal 都能乾淨插入、獨立量測，要嘛改善產品、要嘛被移除。這個**可組合性**正是 RAG 玩具跟 RAG 平台的差別。

---

## CCA 考試關聯

- **D1（Agentic Architecture）**：hybrid retrieval 與 rank fusion 是核心進階 RAG pattern。
- **D5（Enterprise Deployment）**：modular retriever 設計是 production RAG 能 scale 而不拆掉 retrieval 層的關鍵。
- 題目 pattern：「如何合併兩個分數不相容的 retrieval 系統？」→ 對 rank 做 reciprocal rank fusion，不是 score。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 專家評審團 analogy 怎麼對應 multi-index retrieval？ | 每個搜尋方法是個有自己尺度的評審；把他們的意見 rank-normalize，選多位評審都排前面的那道菜。 |
| 為什麼 reciprocal rank fusion 用 rank 而不是 raw score？ | 因為不同搜尋方法用不相容的 scoring system——rank 是唯一的通用貨幣。 |
| 什麼時候該加第二個 index 到你的 RAG 產品？ | 當 eval set 顯示概念或字面 query 開始失敗，而有互補方法可以接住的時候。 |
| Index 加入的建議順序？ | 先語意 → 字面 query 失敗時加 BM25 → freshness 重要時加 recency → eval 證明有效時加 domain-routing。 |
| 新 index 怎麼影響 latency？ | 每個都加 latency（通常並行）；總延遲是 max(per-index) 加上 fusion overhead。加之前先算預算。 |
| 加 index 的隱形成本？ | Ingest 運算、儲存、維運面、eval 複雜度——不只 query latency。 |
| Multi-index RAG 最大的 PM 錯誤是什麼？ | 沒有 eval set 就加 index，沒人能證明有沒有改善。 |
| Multi-index retrieval 對終端使用者是否可見？ | 不——它應該完全是內部的。使用者只看到「答案變好」，永遠看不到哪個 index 拿了什麼。 |
