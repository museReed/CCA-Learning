# BM25 Lexical Search — Engineering Deep Dive（工程深入）

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Architecture（22%）主领域；D5 — Enterprise Deployment（20%）次领域；D2 — Tool Design（18%）也相关（retrieval 作为 tool） |
| Task Statements | 1.3（context management）、5.2（production search infrastructure） |
| 来源 | building-with-the-claude-api / 05-rag / Lesson 50 |

---

## 一句话总结

BM25 是一个经典 lexical search 算法，用来补语义搜索的不足——稳定匹配精确 term（ID、代号、罕见字），正是 embedding 悄悄失灵的那一半检索品质。

---

## 问题：语义搜索抓不到精确 term

想象你要在报告里找 incident ID `INC-2023-Q4-011`。语义搜索擅长概念相似——它知道"incident report"跟"cybersecurity event"相关——但它会返回概念上接近却**实际上没有你要的 ID** 的段落。课程范例中，纯语义搜索查这个 incident ID 时，带出了正确的 cybersecurity section，但也带出了一个完全不相关的 financial analysis section。

为什么？embedding 把文字压缩成稠密 vector，罕见 token 会被平均掉。像 `INC-2023-Q4-011` 这种字面 string 几乎没有语义邻居，所以包含它的问题的 embedding 被周围的字主导——最后匹配到的是那些字，不是那个 ID。

---

## Hybrid Search 策略

修正方式不是取代语义搜索，而是**并行运行两种**搜索再合并：

- **Semantic search**——embedding、cosine similarity，擅长概念问题。
- **Lexical search**——经典 token 匹配（BM25），擅长精确 term 命中。
- **Merged results**——合并两者，返回统一列表。

两种方法互补，对方漏掉的我接住。合在一起就是更强韧的检索层。

---

## BM25 怎么运作

BM25（Best Match 25）对一个 query 用四步骤对 document 打分：

1. **Tokenize query**——把用户问题切成 term。`"a INC-2023-Q4-011"` 变 `["a", "INC-2023-Q4-011"]`。
2. **计算 term frequency**——每个 term 在所有 document 里出现几次。`"a"` 可能整份语料出现 5 次；`"INC-2023-Q4-011"` 可能只出现 1 次。
3. **用稀有度加权**——越稀有的 term 权重越高。常见字（`"a"`、`"the"`）几乎不贡献；罕见 term（`"INC-2023-Q4-011"`）主导整个分数。
4. **排序 document**——返回累积加权 term frequency 最高的 document。

核心直觉：**到处都出现的 term 是 noise；只出现在一个地方的 term 是很强的 signal。** BM25 就是把这个直觉变成一个分数。

---

## 实现 BM25 搜索

课程提供一个简单包装类 `BM25Index`，API 和 `VectorIndex` 对齐：

```python
# 1. 用 section 切 chunk
chunks = chunk_by_section(text)

# 2. 建 BM25 store，加入 document
store = BM25Index()
for chunk in chunks:
    store.add_document({"content": chunk})

# 3. 搜索
results = store.search("What happened with INC-2023-Q4-011?", 3)

# 打印结果
for doc, distance in results:
    print(distance, "\n", doc["content"][:200], "\n----\n")
```

两个 API 细节值得记住：

- `add_document({"content": chunk})`——document 用 dict payload 存，形状跟 vector store 一样，所以上层两种 index 可互换。
- `store.search(query_text, k)`——吃 raw query text（BM25 自己做 tokenization，不需要 embedding 调用），返回 top-k 的 (doc, distance) pair。

`INC-2023-Q4-011` 的查询输出现在正确地把字面提到 incident ID 的两个 section——Software Engineering 跟 Cybersecurity——排在前面。

---

## 为什么这对精确匹配更好

BM25 擅长精确匹配是因为它：

- **给罕见 term 高权重**——只出现一次的 incident ID 具有最大辨别力。
- **忽略常见字**——类似 stop-word 的 term 贡献几乎为零。
- **按 term frequency 打分，不看意思**——没有语义平滑化把字面 token 冲掉。
- **处理技术 token 很好**——ID、SKU、error code、函数名、CVE 编号都受益。

反面：BM25 对概念相似度很弱。如果用户问"上一季出了什么事？"BM25 没办法把它配到标题叫"Cybersecurity Analysis"的段落。那正是语义搜索的主场。

---

## API 一致性铺陈下一课

注意 `BM25Index` 和 `VectorIndex` 共享几乎相同的接口：

| 方法 | BM25Index | VectorIndex |
|------|-----------|-------------|
| `add_document(dict)` | 存 raw text | 存 vector + metadata |
| `search(query, k)` | 返回 top-k BM25 分数 | 返回 top-k cosine distance |

这不是巧合。一致 API 是下一课 multi-index Retriever 能成立的条件——单一 wrapper 把同一个 query 转发到两个 index，然后用 reciprocal rank fusion 合并结果。

---

## 常见错误

1. **以为语义搜索能找到精确 ID**——经常找不到。任何 token literal 都该走 BM25。
2. **用 BM25 取代语义搜索**——会失去概念理解能力。正确 pattern 是 hybrid，不是二选一。
3. **BM25 前不切 chunk**——BM25 是对 document 打分；chunking 决定你的 document 粒度。
4. **BM25 payload 只存 text**——加上 metadata（section title、doc id）让下游合并与 attribution 可以运作。
5. **跳过 normalization**——大小写与标点差异会伤害 BM25。课程的基本 tokenizer 隐藏了这点，production 系统必须正视。

> **核心洞见**
>
> 语义搜索处理意思；BM25 处理字面 token。Production RAG 系统几乎都需要两者，因为 user query 总是混着概念意图和具体识别码。Hybrid pattern 不是 optimization——它是默认选项。

---

## CCA 考试关联

- **D1（Agentic Architecture）**：hybrid retrieval 是经典的进阶 RAG pattern；要了解 semantic 与 lexical 的互补角色。
- **D5（Enterprise Deployment）**：BM25 运行很便宜（ingest 与 query 都不需要调用 embedding API），对成本与 latency 很重要。
- **D2（Tool Design）**：当你把 retrieval 包成 Claude 可以调用的 tool 时，知道这个 tool 是 BM25 / 语义 / hybrid 会影响你怎么描述给模型。
- 题目 pattern："语义搜索对一个包含特定 ID 的 query 返回不相关结果——要加什么？"→ BM25 / hybrid search。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| BM25 是什么缩写？ | Best Match 25——一个经典 lexical search 算法。 |
| BM25 解决语义搜索的什么问题？ | 漏掉精确 term 匹配（ID、代号、罕见字），这些被 embedding 冲淡了。 |
| BM25 打分的四步骤是哪四个？ | 1) Tokenize query、2) 算 term frequency、3) 按稀有度加权、4) 按累积加权频率排序 document。 |
| 为什么罕见 term 在 BM25 权重较高？ | 因为辨别力更高——只出现在一处的 term 是强 signal。 |
| BM25 query time 需要调用 embedding API 吗？ | 不用——BM25 直接在 token 上运作，不需要 embedding。 |
| Hybrid search 是要用 BM25 取代语义搜索吗？ | 不是——hybrid 是并行跑两种再合并，不是取代。 |
| `BM25Index` 跟 `VectorIndex` 共享哪些 API 方法？ | `add_document(dict)` 和 `search(query, k)`——一致的 API 让统一的 Retriever 成立。 |
| BM25 什么时候会失效？ | 当 query 是概念性的、和相关文档完全没字面 token 重叠时。这时需要语义搜索。 |
