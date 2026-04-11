# A Multi-Index RAG Pipeline — Engineering Deep Dive（工程深入）

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Architecture（22%）主領域；D5 — Enterprise Deployment（20%）次領域 |
| Task Statements | 1.3（context management）、5.2（production search infrastructure） |
| 來源 | building-with-the-claude-api / 05-rag / Lesson 51 |

---

## 一句話總結

Multi-index RAG pipeline 把 `VectorIndex` 和 `BM25Index` 包在同一個 `Retriever` 底下，把 query 分發給兩個 index，再用 reciprocal rank fusion 合併結果——把兩套獨立的搜尋系統變成一個 hybrid retrieval 層。

---

## Multi-Index 架構

`VectorIndex` 和 `BM25Index` 原本就共享幾乎相同的 API——`add_document()` 和 `search()`。這個一致性就是能寫一個乾淨 wrapper 的關鍵：

```
                       ┌─────────────┐
  add_document() ────▶ │             │ ────▶ VectorIndex.add_document
                       │  Retriever  │ ────▶ BM25Index.add_document
  search(query)  ────▶ │             │
                       │             │ ────▶ VectorIndex.search
                       │             │ ────▶ BM25Index.search
                       └──────┬──────┘
                              │  reciprocal rank fusion
                              ▼
                       合併後的 top-k 結果
```

`Retriever` 是一個薄的 coordinator：寫入時廣播給所有 index；讀取時把 query fan-out 給所有 index，然後把排序合併成一個單一排序列表。

---

## 理解 Reciprocal Rank Fusion（RRF）

合併不同搜尋方法的結果比看起來難。每個方法有自己的 scoring system——BM25 分數不能跟 cosine distance 比。你不能直接 union 兩份 result list，也不能平均它們的 score。

技巧是忽略原始分數，只看**排名（rank）**，也就是每份列表中的位置。Reciprocal rank fusion 把這個想法公式化：

```
RRF_score(d) = Σ  1 / (k + rank_i(d))
              i
```

其中：

- `d` 是 document
- `i` 是 ranking source 的 index（VectorIndex、BM25Index、…）
- `rank_i(d)` 是 document `d` 在 ranking `i` 中的 1-based 排名
- `k` 是平滑常數（常用 60；課程為了示範清楚用 1）

在**多個** index 中都排前面的 document 累積最高分，排到最上面。只在一個 index 中排前面的不會被取消，但會被扣分。

### 實作例子

搜尋 "INC-2023-Q4-011"：

- VectorIndex 回傳：Section 2（rank 1）、Section 7（rank 2）、Section 6（rank 3）
- BM25Index 回傳：Section 6（rank 1）、Section 2（rank 2）、Section 7（rank 3）

使用 `k = 1`：

- Section 2：`1/(1+1) + 1/(1+2) = 0.5 + 0.333 = 0.833`
- Section 7：`1/(1+2) + 1/(1+3) = 0.333 + 0.25 = 0.583`
- Section 6：`1/(1+3) + 1/(1+1) = 0.25 + 0.5 = 0.75`

最終合併排名：**Section 2（0.833）> Section 6（0.75）> Section 7（0.583）**。

直覺上：Section 2 在兩份列表都排前面，所以贏。Section 6 在 BM25 排第一但在 vector 排第三，仍然贏過處處中段的 Section 7。

---

## Retriever 類別

```python
class Retriever:
    def __init__(self, *indexes: SearchIndex):
        if len(indexes) == 0:
            raise ValueError("At least one index must be provided")
        self._indexes = list(indexes)

    def add_document(self, document: Dict[str, Any]):
        for index in self._indexes:
            index.add_document(document)

    def search(self, query_text: str, k: int = 1, k_rrf: int = 60):
        # 從所有 index 取得結果
        all_results = []
        for idx, results in enumerate(all_results):
            for rank, (doc, _) in enumerate(results):
                # 追蹤 document 在不同 index 的 rank
                # 套用 RRF 評分公式
        # 回傳合併並排序的結果
```

設計重點：

- **Variadic indexes**——`*indexes: SearchIndex` 讓 Retriever 接受任意數量的具體 index 實作。至少要有一個。
- **寫入廣播**——`add_document` 把同一個 payload forward 給每個 index。每個 index 用自己的格式存（`VectorIndex` 存 vector，`BM25Index` 存 raw text）。
- **統一搜尋**——呼叫者只跟 `Retriever.search(query_text, k)` 互動。不知道、也不在乎底下有哪些 index。
- **可設定的 `k_rrf`**——RRF 平滑常數以參數暴露，預設 60（教科書常值；課程示範用 1）。

核心洞見：讓每個搜尋實作的 API 保持一致，合併就變成一個 trivial 的 wrapper，而不是一場糾結的 integration。

---

## 測試 Hybrid 結果

回想先前的問題：純向量搜尋查「what happened with INC-2023-Q4-011?」時，第一名是 cybersecurity 但第二名卻是錯的 financial analysis section，而不是 software engineering section。

用 hybrid Retriever 後，輸出變成：

1. Section 10：Cybersecurity Analysis — Incident Response Report（最相關）
2. Section 2：Software Engineering — Project Phoenix Stability Enhancements（第二相關）
3. Section 5：Legal Developments（第三）

這符合直覺：兩個實際提到 incident 的 section 都浮到上面，而多餘的 financial section 因為 BM25 不給它任何字面 token 的支持，直接掉出去。

---

## 可擴充性：SearchIndex Protocol

每個 index——現在或未來——都實作同一個 `SearchIndex` protocol：`add_document()` 和 `search()`。所以 Retriever 自動相容於你之後加入的任何新搜尋方法：

- Keyword-based index
- Knowledge graph 上的 graph-based search
- 特化 domain index（例如程式碼的 symbol search）
- 優先新文件的 recency-based index

實作那兩個 method，把 instance 傳進 `Retriever(...)` 即可。RRF 自動處理 fusion。這種 modular 設計讓每個搜尋實作維持專注且可測試，同時提供乾淨的組合點。

---

## 常見錯誤

1. **用原始分數合併**——BM25 分數和 cosine distance 不可比。永遠用 rank-based fusion（RRF），不要用 score 算術。
2. **搞混 RRF 公式裡的 `k`**——RRF 公式裡的 `k` 跟 search result 的 top-k 不是同一個。搞混會讓分數失準。
3. **以為 index 越多越好**——每加一個 index 都增加 latency 和 compute。只加在 eval 上真的改善 metrics 的 index。
4. **寫入廣播但沒做 deduplication**——同一份 document 加兩次會進到每個 index 各兩份。Ingest 時要去重。
5. **忘記把 `k_rrf` 開放成 API 參數**——預設值大多數情境沒問題，但 production eval 可能要調。

> **核心洞見**
>
> Reciprocal rank fusion 是讓 multi-index retrieval「就是會動」的關鍵技巧。它用純 rank 的算術繞過不同 scoring system 的不相容問題。配上一致的 `SearchIndex` protocol，hybrid retrieval 就變成一個**組合問題**，而不是 integration 問題。

---

## CCA 考試關聯

- **D1（Agentic Architecture）**：hybrid retrieval 和 rank fusion 是經典的進階 RAG pattern。題目會問如何合併搜尋模態。
- **D5（Enterprise Deployment）**：modular retriever 設計是 production 議題——要知道如何加獨立 index 來 scale，不必拆掉整個 retrieval 層。
- 題目 pattern：「你有一個語意 index 和一個 BM25 index 分數不相容——怎麼合併結果？」→ 用 per-index rank 的 reciprocal rank fusion。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Retriever class 做什麼？ | 把多個 `SearchIndex` 實作包在單一 `add_document` / `search` API 底下，寫入廣播、讀取用 RRF 合併。 |
| 為什麼 BM25 跟 cosine 分數不能直接合併？ | 它們用不相容的 scoring system——要改用 rank normalization。 |
| RRF 公式是什麼？ | `RRF_score(d) = Σ 1 / (k + rank_i(d))`——對所有 ranking i 加總「(k + 文件在該 ranking 的排名) 的倒數」。 |
| RRF 裡的 `k` 常數是什麼？課程用哪個值？ | 平滑常數——實務常用 60，課程為了示範數學清楚用 1。 |
| 實作例子中 Section 2 為什麼贏？ | 它在 VectorIndex 排第一、在 BM25 排第二，RRF 得 0.833——總分最高。 |
| SearchIndex protocol 有哪兩個 method？ | `add_document(dict)` 和 `search(query, k)`。 |
| Retriever 之後加新 index type 要怎麼做？ | 任何實作了 `add_document` 和 `search` 的類別直接插進去——RRF 自動處理 fusion。 |
| Hybrid Retriever 怎麼修好先前問題的 query 結果？ | 錯誤的「financial analysis」section 掉出去，兩個真的提到 incident ID 的 section 浮到頂。 |
