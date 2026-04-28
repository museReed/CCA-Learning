# Introducing Retrieval Augmented Generation — 工程深度解析

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Architecture (22%) 主要；D4 — Safety & Alignment (20%) 次要 |
| Task Statements | 1.3（context management）、4.1（grounded responses） |
| 来源 | building-with-the-claude-api / 05-rag / Lesson 45 |

---

## 一句话总结

RAG（Retrieval Augmented Generation）解决「文档太大塞不进 prompt」的问题：先把文档切成 chunks 存起来，用户提问时只注入最相关的片段。

---

## 能力墙：大型文档

想象一份 800 页的财报，用户问「这家公司有哪些 risk factors？」。原始文字放不进一次 `messages.create` 调用。这不是 prompt engineering 问题，而是架构问题。

三个力量把「全部塞进去」的做法打掉：

- **context window 硬限制** — 有些文档就是比模型支持的长度还长。
- **质量下降** — prompt 太长时 Claude 效果会变差，相关信号会被噪音淹没。
- **成本与延迟** — prompt 越大 token 越多，处理越慢。

---

## 做法 1：Prompt Stuffing（基线做法）

最简单的做法是把文档所有文字抽出来直接放进 prompt：

```
Answer the user's question about the financial document.

<user_question>
{user_question}
</user_question>

<financial_document>
{financial_document}
</financial_document>
```

短文档这样做完全 OK，也是当内容舒服放进 context 时的正确默认值。它有一个重要优点：零预处理、零 retrieval 逻辑、搜索层零 bug。

一旦文档（或整个 corpus）超过 context window 的舒适比例，它就失效。

---

## 做法 2：RAG — 先切块再检索

RAG 走两个阶段：

1. **预处理（offline）** — 把每份文档切成较小的 chunks 存起来。每份文档做一次。
2. **查询时（online）** — 用户提问时，在 chunks 里搜索最相关的几块，只把那几块塞进 prompt。

所以用户问「What risks does this company face?」会触发一次 lookup，找到 "Risk Factors" 那一节，那一块（加上问题）才是 Claude 看到的内容。

这就是 RAG 的基本形状：**chunk → index → retrieve → prompt**。Lessons 46-48 逐步填满每个步骤。

---

## 好处

- **聚焦** — Claude 只看到相关内容，推理时不会被干扰
- **可扩展** — 可以处理远大于 context window 的文档与 corpus
- **多文档** — 单一 index 可以跨多份文件
- **更便宜更快** — prompt 小 token 成本低、延迟低

---

## 挑战

- **预处理成本** — 每次新增或更新文档都需要跑 chunking pipeline
- **retrieval 质量** — 需要真的能找到「相关」chunks 的搜索机制；retrieval 烂了答案就错
- **context 不足** — 被捞回来的 chunk 可能缺了 Claude 需要的周边上下文（例如定义在前一节）
- **chunking 策略选择** — 等长切割、按 section 切、semantic 切，各有取舍

RAG 用**复杂度**换**可扩展性与效率**。corpus 放得进 context 就不要用 RAG；放不进就几乎一定要用。

---

## 何时用 RAG

| 场景 | 用 RAG？ |
|------|----------|
| 5 页 PDF、单一文档 | 不用 — 直接塞 prompt |
| 800 页的财务申报 | 要 |
| 公司知识库上千篇文章 | 要 |
| 单一用户问题查一份固定的 2000-token FAQ | 不用 |
| 需要实时、变动的数据（天气、股价） | 不用 — 用 **tool use** |

RAG 适合**大型、相对稳定的 corpus**，需要在文字上做 semantic search。Tool use 适合**实时、动态数据源**，需要实时读取。

---

## CCA Task 对应

- **Task 1.3（Context Management）** — RAG 是 context management 的代表 pattern。你在决定*哪些* context 进 window，不只是*要不要*放 context。
- **Task 4.1（Grounded Responses）** — 注入来源 chunks 给 Claude 一个事实基础，降低幻觉。这把 RAG 连到 Safety & Alignment 领域。

---

## 工程深度：为什么 RAG 属于 D1

架构层面看，RAG 是一个 **retriever + generator** pipeline。retriever 不是 Claude 的一部分，是你拥有的 deterministic 代码；generator 是 Claude，用你 retriever 组好的 prompt 来调用。这个分离很重要：

1. **retriever 可以单元测试** — 给 query X，是否返回 chunk Y？
2. **retriever 可以替换** — 从 keyword 换成 semantic 换成 hybrid search，都不用动模型
3. **可以审计 grounding** — 每个答案都可以追到特定 chunk，这是 safety 赢面

RAG 也是走向 agentic architecture 最简单的第一步。retrieval 一旦变成 function call，就离把它包成 Claude 自己选择调用的 **tool** 不远，这就是 RAG 与 Ch04（Tool Use）交汇点。

---

## 常见错误

1. **prompt stuffing 就够用还硬要 RAG** — 文档放得进 context 的话，RAG 只是增加复杂度没有好处。
2. **把 RAG 和 tool use 搞混** — RAG 处理静态文字 corpus；tool use 处理实时数据。两个是不同 pattern。
3. **把 retrieval 当成解决了的问题** — 糟糕的 chunking 或 retrieval 会默默返回错的 chunks，Claude 会很有信心地根据错内容回答。
4. **prompt 里没有 citation 标记** — 不标明 chunk 来源，就失去 RAG 一半的价值（可审计性）。
5. **忘了 chunk overlap / 边界 context** — 定义或 header 被切掉，chunk 看起来相关但缺关键细节。

> **关键洞察**
>
> RAG 不是模型能力，而是**应用层架构**。Claude 不会「做 RAG」；是你的代码组出含 retrieved chunks 的 prompt 再交给 Claude。也就是说每个 RAG bug 都是应用层 bug，每个 RAG 改善都是应用层改动。pipeline 要自己拥有。

---

## CCA 考试关联

- **D1（Agentic Architecture）**：RAG 是基础的 context augmentation pattern。预期会看到「大型 corpus、问问题」的情境题 → RAG。
- **D4（Safety & Alignment）**：RAG 把回答 grounded 在 retrieved text，降低幻觉，这是核心 alignment pattern。
- 注意陷阱：题目描述**实时数据**（天气、价格）应答 **tool use**，不是 RAG。描述**稳定文档 corpus** 才答 RAG。

---

## Flashcards

| Front | Back |
|-------|------|
| RAG 解决什么问题？ | 处理无法塞进单一 prompt 的大型文档：切成 chunks、查询时只注入相关片段。 |
| RAG pipeline 的两个阶段？ | 预处理（chunk + index）与查询时（retrieve + prompt）。 |
| 为什么不全部塞进 prompt？ | context window 限制、长 prompt 质量下降、成本与延迟变高。 |
| RAG 相对 prompt stuffing 的三个好处？ | 聚焦相关内容、可扩展到大型 corpus、成本与延迟较低。 |
| RAG 的三个挑战？ | 需要预处理 pipeline、retrieval 质量难做、chunk 可能缺周边 context。 |
| 什么情况**不**该用 RAG？ | 文档放得进 context window，或需要实时数据（用 tool use）。 |
| RAG 主要对应哪个 CCA 领域？ | D1 — Agentic Architecture，通过 context management。 |
| RAG 为什么能降低幻觉？ | 把权威来源文字注入 prompt，给 Claude 一个 grounded 的事实基础。 |
