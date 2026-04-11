# A Multi-Index RAG Pipeline — Engineering Deep Dive（工程深入）

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Architecture（22%）主领域；D5 — Enterprise Deployment（20%）次领域 |
| Task Statements | 1.3（context management）、5.2（production search infrastructure） |
| 来源 | building-with-the-claude-api / 05-rag / Lesson 51 |

---

## 一句话总结

Multi-index RAG pipeline 把 `VectorIndex` 和 `BM25Index` 包在同一个 `Retriever` 底下，把 query 分发给两个 index，再用 reciprocal rank fusion 合并结果——把两套独立的搜索系统变成一个 hybrid retrieval 层。

---

## Multi-Index 架构

`VectorIndex` 和 `BM25Index` 原本就共享几乎相同的 API——`add_document()` 和 `search()`。这个一致性就是能写一个干净 wrapper 的关键：

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
                       合并后的 top-k 结果
```

`Retriever` 是一个薄的 coordinator：写入时广播给所有 index；读取时把 query fan-out 给所有 index，然后把排序合并成一个单一排序列表。

---

## 理解 Reciprocal Rank Fusion（RRF）

合并不同搜索方法的结果比看起来难。每个方法有自己的 scoring system——BM25 分数不能跟 cosine distance 比。你不能直接 union 两份 result list，也不能平均它们的 score。

技巧是忽略原始分数，只看**排名（rank）**，也就是每份列表中的位置。Reciprocal rank fusion 把这个想法公式化：

```
RRF_score(d) = Σ  1 / (k + rank_i(d))
              i
```

其中：

- `d` 是 document
- `i` 是 ranking source 的 index（VectorIndex、BM25Index、…）
- `rank_i(d)` 是 document `d` 在 ranking `i` 中的 1-based 排名
- `k` 是平滑常数（常用 60；课程为了示范清楚用 1）

在**多个** index 中都排前面的 document 累积最高分，排到最上面。只在一个 index 中排前面的不会被取消，但会被扣分。

### 实作例子

搜索 "INC-2023-Q4-011"：

- VectorIndex 返回：Section 2（rank 1）、Section 7（rank 2）、Section 6（rank 3）
- BM25Index 返回：Section 6（rank 1）、Section 2（rank 2）、Section 7（rank 3）

使用 `k = 1`：

- Section 2：`1/(1+1) + 1/(1+2) = 0.5 + 0.333 = 0.833`
- Section 7：`1/(1+2) + 1/(1+3) = 0.333 + 0.25 = 0.583`
- Section 6：`1/(1+3) + 1/(1+1) = 0.25 + 0.5 = 0.75`

最终合并排名：**Section 2（0.833）> Section 6（0.75）> Section 7（0.583）**。

直觉上：Section 2 在两份列表都排前面，所以赢。Section 6 在 BM25 排第一但在 vector 排第三，仍然赢过处处中段的 Section 7。

---

## Retriever 类

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
        # 从所有 index 取得结果
        all_results = []
        for idx, results in enumerate(all_results):
            for rank, (doc, _) in enumerate(results):
                # 追踪 document 在不同 index 的 rank
                # 套用 RRF 评分公式
        # 返回合并并排序的结果
```

设计重点：

- **Variadic indexes**——`*indexes: SearchIndex` 让 Retriever 接受任意数量的具体 index 实作。至少要有一个。
- **写入广播**——`add_document` 把同一个 payload forward 给每个 index。每个 index 用自己的格式存（`VectorIndex` 存 vector，`BM25Index` 存 raw text）。
- **统一搜索**——调用者只跟 `Retriever.search(query_text, k)` 互动。不知道、也不在乎底下有哪些 index。
- **可设定的 `k_rrf`**——RRF 平滑常数以参数暴露，默认 60（教科书常值；课程示范用 1）。

核心洞见：让每个搜索实作的 API 保持一致，合并就变成一个 trivial 的 wrapper，而不是一场纠结的 integration。

---

## 测试 Hybrid 结果

回想之前的问题：纯向量搜索查"what happened with INC-2023-Q4-011?"时，第一名是 cybersecurity 但第二名却是错的 financial analysis section，而不是 software engineering section。

用 hybrid Retriever 后，输出变成：

1. Section 10：Cybersecurity Analysis — Incident Response Report（最相关）
2. Section 2：Software Engineering — Project Phoenix Stability Enhancements（第二相关）
3. Section 5：Legal Developments（第三）

这符合直觉：两个实际提到 incident 的 section 都浮到上面，而多余的 financial section 因为 BM25 不给它任何字面 token 的支持，直接掉出去。

---

## 可扩展性：SearchIndex Protocol

每个 index——现在或未来——都实作同一个 `SearchIndex` protocol：`add_document()` 和 `search()`。所以 Retriever 自动兼容于你之后加入的任何新搜索方法：

- Keyword-based index
- Knowledge graph 上的 graph-based search
- 特化 domain index（例如代码的 symbol search）
- 优先新文档的 recency-based index

实作那两个 method，把 instance 传进 `Retriever(...)` 即可。RRF 自动处理 fusion。这种 modular 设计让每个搜索实作维持专注且可测试，同时提供干净的组合点。

---

## 常见错误

1. **用原始分数合并**——BM25 分数和 cosine distance 不可比。永远用 rank-based fusion（RRF），不要用 score 算术。
2. **搞混 RRF 公式里的 `k`**——RRF 公式里的 `k` 跟 search result 的 top-k 不是同一个。搞混会让分数失准。
3. **以为 index 越多越好**——每加一个 index 都增加 latency 和 compute。只加在 eval 上真的改善 metrics 的 index。
4. **写入广播但没做 deduplication**——同一份 document 加两次会进到每个 index 各两份。Ingest 时要去重。
5. **忘记把 `k_rrf` 开放成 API 参数**——默认值大多数情境没问题，但 production eval 可能要调。

> **核心洞见**
>
> Reciprocal rank fusion 是让 multi-index retrieval"就是会动"的关键技巧。它用纯 rank 的算术绕过不同 scoring system 的不兼容问题。配上一致的 `SearchIndex` protocol，hybrid retrieval 就变成一个**组合问题**，而不是 integration 问题。

---

## CCA 考试关联

- **D1（Agentic Architecture）**：hybrid retrieval 和 rank fusion 是经典的进阶 RAG pattern。题目会问如何合并搜索模态。
- **D5（Enterprise Deployment）**：modular retriever 设计是 production 议题——要知道如何加独立 index 来 scale，不必拆掉整个 retrieval 层。
- 题目 pattern："你有一个语义 index 和一个 BM25 index 分数不兼容——怎么合并结果？"→ 用 per-index rank 的 reciprocal rank fusion。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Retriever class 做什么？ | 把多个 `SearchIndex` 实作包在单一 `add_document` / `search` API 底下，写入广播、读取用 RRF 合并。 |
| 为什么 BM25 跟 cosine 分数不能直接合并？ | 它们用不兼容的 scoring system——要改用 rank normalization。 |
| RRF 公式是什么？ | `RRF_score(d) = Σ 1 / (k + rank_i(d))`——对所有 ranking i 加总"(k + 文档在该 ranking 的排名) 的倒数"。 |
| RRF 里的 `k` 常数是什么？课程用哪个值？ | 平滑常数——实务常用 60，课程为了示范数学清楚用 1。 |
| 实作例子中 Section 2 为什么赢？ | 它在 VectorIndex 排第一、在 BM25 排第二，RRF 得 0.833——总分最高。 |
| SearchIndex protocol 有哪两个 method？ | `add_document(dict)` 和 `search(query, k)`。 |
| Retriever 之后加新 index type 要怎么做？ | 任何实作了 `add_document` 和 `search` 的类直接插进去——RRF 自动处理 fusion。 |
| Hybrid Retriever 怎么修好之前问题的 query 结果？ | 错误的"financial analysis"section 掉出去，两个真的提到 incident ID 的 section 浮到顶。 |
