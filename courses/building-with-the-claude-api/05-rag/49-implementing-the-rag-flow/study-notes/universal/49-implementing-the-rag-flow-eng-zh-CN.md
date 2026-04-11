# Implementing the RAG Flow — Engineering Deep Dive（工程深入）

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Architecture（22%）主领域；D5 — Enterprise Deployment（20%）次领域 |
| Task Statements | 1.3（context management）、5.2（production search infrastructure） |
| 来源 | building-with-the-claude-api / 05-rag / Lesson 49 |

---

## 一句话总结

实现 RAG 是一条五步骤 pipeline：切 chunk、生成 embedding、把 vector 和原文一起存、对 user query 生成 embedding、用 cosine similarity 搜索——把语义检索变成具体、可复现的代码流程。

---

## RAG 五步骤 Pipeline

```
┌──────────┐  1. chunk_by_section   ┌──────────┐
│ report   │ ─────────────────────▶ │  chunks  │
│  .md     │                         └────┬─────┘
└──────────┘                              │
                                          ▼
                               2. generate_embedding(chunks)
                                          │
                                          ▼
                               3. VectorIndex.add_vector(
                                      embedding,
                                      {"content": chunk})
                                          │
                   ┌──────────────────────┘
                   ▼
        4. user_embedding = generate_embedding(question)
                   │
                   ▼
        5. store.search(user_embedding, k=2)
                   │
                   ▼
         [(doc, distance), ...]
```

RAG 这个概念——"回答前先找出相关文字"——全部可以压缩成这五个固定步骤。检索端没有魔法；魔法全部在把文字映射到有意义向量空间的 embedding 模型里。

---

## 步骤 1：切 chunk

```python
with open("./report.md", "r") as f:
    text = f.read()

chunks = chunk_by_section(text)
chunks[2]  # 测试看是否正确切到目录
```

之前课程介绍的 `chunk_by_section` 函数会把文档切成逻辑上的段落。每个 chunk 变成可独立检索的单位。切法很关键：切太小会失去上下文；切太大 embedding 会稀释掉辨别度。

---

## 步骤 2：批量生成 embedding

```python
embeddings = generate_embedding(chunks)
```

embedding helper 同时支持单一 string 和 list of strings，所以整份语料可以一次调用产出。这点在 production 很重要，因为 embedding API 通常按次计费，批量调用远比 N 次单独调用便宜又快。

---

## 步骤 3：存进 vector database

```python
store = VectorIndex()

for embedding, chunk in zip(embeddings, chunks):
    store.add_vector(embedding, {"content": chunk})
```

注意 payload 是 `{"content": chunk}`。vector 只是 record 的一半——另一半是原始文字（或指向原文的 reference）。没有原文的话，nearest-neighbor 搜索回来的只是无意义的浮点数，根本没东西能塞回 Claude。

### 为什么要存原文？

query 时必须回传实际的内容塞进 prompt。embedding vector 只是 index 的 key；value 必须是人类可读的文字。变化做法包括：

- 完整 chunk 文字（最简单）
- 一个 pointer（doc_id + offset）延后取回
- 文字再加上 metadata（section title、source URL、timestamp）

---

## 步骤 4：对 user query 生成 embedding

```python
user_embedding = generate_embedding(
    "What did the software engineering dept do last year?"
)
```

关键是**语料与 query 必须用同一个 embedding 模型**。混用模型会产生不兼容的向量空间，similarity 分数就变没意义。

---

## 步骤 5：用 cosine distance 搜索

```python
results = store.search(user_embedding, 2)

for doc, distance in results:
    print(distance, "\n", doc["content"][0:200], "\n")
```

`store.search(query_vector, k)` 返回前 k 个最近的 document，连同 distance。distance 越小 = similarity 越高。课程范例中：

- Section 2（Software Engineering）→ distance 0.71（最接近）
- Methodology section → distance 0.72（第二接近）

这个排序就是你交回给 Claude 当 grounded context 的内容。

---

## 接下来：纯语义搜索的极限

这节课结尾有个警告：这个基本流程对干净的语义问题可以，但遇到需要**精确 term 匹配**（incident ID、product SKU、error code）就会失灵。这正是后面课程要引入 BM25 与 hybrid retrieval 的原因。

---

## 常见错误

1. **只存 embedding 不存原文**——失去把实际内容回传给 Claude 的能力。
2. **语料与 query 用不同 embedding 模型**——向量空间不兼容，similarity 就变垃圾。
3. **跳过 batch embedding**——每个 chunk 单独调用在 production 又慢又贵。
4. **忽略 chunk 大小**——过大稀释相关度；过小丢失上下文。
5. **把 distance 返回给用户**——distance 是 debug 信号，不是产品输出。返回 content，log distance。

> **核心洞见**
>
> RAG pipeline 本身是一个**确定性的预处理 + 查询**工作，不是 AI feature。智能完全来自 (a) 把语义映射到几何的 embedding 模型 (b) 下游在 retrieved chunks 上推理的 LLM。让 pipeline 保持无聊、可替换，品质就会从你能独立升级的组件身上长出来。

---

## CCA 考试关联

- **D1（Agentic Architecture）**：RAG 是 context management 的经典 pattern。题目常包装成"我要怎么让 Claude 认识它原本不知道的东西？"
- **D5（Enterprise Deployment）**：vector store 选型、embedding 成本、batch 处理、pipeline 新鲜度都是 deployment/scale 题目会出现的 production 议题。
- 注意会有误导选项建议"fine-tune"来解决"Claude 不认识我们内部文档"——RAG 几乎都是正解。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| RAG 流程有哪五个步骤？ | 1) 切文字、2) 对每个 chunk 生成 embedding、3) 把 embedding + 原文存进 vector index、4) 对 user query 生成 embedding、5) 在 store 中搜 top-k 最近的 chunks。 |
| 为什么必须把原文和 embedding 一起存？ | query 时要把实际内容喂给 Claude——只有 embedding 的话是一堆看不懂的浮点数。 |
| 语料与 query 必须用同一个 embedding 模型吗？ | 是。不同模型产生不兼容的向量空间，cosine similarity 就变没意义。 |
| `store.search(user_embedding, 2)` 返回什么？ | 一个 (document, distance) tuple 的 list——最接近的两个 chunks 和它们的 cosine distance。 |
| 课程范例中，"What did the software engineering dept do last year?"的最接近结果是？ | Section 2（Software Engineering），distance 0.71。 |
| distance 越低代表 similarity 越高还是越低？ | 越低 = similarity 越高（在向量空间中越接近）。 |
| 为什么要批量 embed 而不是 loop 逐笔？ | embedding API 按次计费，批量处理便宜又低延迟。 |
| 下一课要解决纯语义搜索的哪个极限？ | 精确 term 匹配，例如 incident ID——语义搜索可能漏掉字面上的 token match。 |
