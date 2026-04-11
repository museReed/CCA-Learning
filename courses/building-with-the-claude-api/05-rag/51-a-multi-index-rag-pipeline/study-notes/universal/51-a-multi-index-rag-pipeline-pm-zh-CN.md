# A Multi-Index RAG Pipeline — PM Perspective（产品视角）

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Architecture（22%）主领域；D5 — Enterprise Deployment（20%）次领域 |
| Task Statements | 1.3（context management）、5.2（production search infrastructure） |
| 来源 | building-with-the-claude-api / 05-rag / Lesson 51 |

---

## 一句话总结

Multi-index RAG pipeline 是一种架构 pattern，让你可以持续加入新的搜索能力（语义、keyword、recency、domain-specific）而不需要重构——给你的产品在学到用户真正会问什么后，提升 retrieval 品质的空间。

---

## Mental Model：专家评审团

想象一个料理比赛有三位评审：风味专家、摆盘专家、技法专家。每位用完全不同的尺度打分——星星、字母、百分比。你不能直接平均他们的分数，数字不可比。

所以你改要求每位评审对菜色**排名**：第一、第二、第三。然后一道在多位评审都排名前面的菜就会浮到整体最上面，就算没有任何单一评审的原始分数会选它。

这就是 reciprocal rank fusion 对搜索做的事：

- **向量搜索**是"风味"评审——理解意思。
- **BM25** 是"食材标签"评审——检查字面匹配。
- 未来的 index 是新评审——recency、domain、graph——各自有不同视角。

Retriever 是那位收集排名、产出公平最终分数的主评审。

---

## PM 为什么要在意

Multi-index retrieval 是 RAG 从 prototype 走向可扩展产品的转折点。它重要是因为：

- **成长路径已经内建**——加入新 retrieval signal（freshness、popularity、domain）不必动其他产品部分。
- **品质会复利**——每个新 index 接住前一个漏掉的；合并后的品质打败任何单一方法。
- **故障模式彼此隔离**——一个 index 退化，其他还可以服务。运维上这很珍贵。
- **Eval 变可控**——可以独立 A/B test 每个 index（加一个、量测、留下或移除）。

---

## Product Use Cases

### Multi-Index Retriever 划算的情况

| User Need | 为什么多 index 有帮助 |
|-----------|------------------------|
| 概念 + 字面混合的 query | 语义 + BM25 各自覆盖 |
| Freshness 重要（"这周有什么新的？"） | 在现有两个之外加 recency index |
| 多 domain 知识库 | 加 domain-routing index 给专业文档加权 |
| Long-tail query（"罕见产品名"） | Lexical index 接住语义漏掉的 |
| 法律 / 合规同时需要主题与字面 | Hybrid 是唯一可靠答案 |

### Multi-Index 过头的情况

| User Need | 更好的方案 |
|-----------|------------|
| 超小语料（<100 份文档） | 一个 index 就够，运维成本占比太高 |
| 永远只问概念问题 | 纯语义就好——加更多之前要先量测 |
| Latency 预算很紧（<100ms） | 每加一个 index 都拉长 latency，要算取舍 |
| 早期 MVP | 先 ship 纯语义，等真实 query 逼你才加 BM25 |

---

## Reciprocal Rank Fusion（大白话）

想象每个搜索方法给你一个 **top-3 list**。你不在乎每个方法有多自信；你只在乎每份文档在每份 list 上是第几名。

- 第一名 = 很多分
- 第二名 = 少一点分
- 第三名 = 一点点分
- 没上 list = 那个 source 给 0 分

把每份文档在所有 list 拿到的分数加起来。总分最高的赢。在两份 list 都排前面的文档，几乎一定会赢过只在一份 list 排前面的。

这就是 reciprocal rank fusion。它是一个公平合并搜索结果的方法，不需要底下的方法对"分数"意思达成共识。

---

## PM 决策框架

| 问题 | 如果答 Yes | 含义 |
|------|-----------|------|
| 用户同时问概念与字面 query？ | Yes | 需要 hybrid——至少语义 + BM25。 |
| Freshness 是产品承诺？ | Yes | 加一个 recency / time-weighted index。 |
| 有不同的内容 domain（docs、tickets、code）？ | Yes | 考虑 per-domain index，按 query 类型 routing。 |
| 有 eval set？ | No | 先建一个——没量测就调不了 multi-index。 |
| Latency 预算很紧？ | Yes | 从两个 index 开始，量测，再扩张。 |

---

## 成本、延迟、运维取舍

每多一个 index 都有成本。好的 PM 要明确编列：

- **Index 建构成本**——每次 ingest 都要写到每个 index。要编列 CPU + memory + storage。
- **Query 延迟**——每个 index 都加 latency，通常并行，所以总延迟是 max(per-index latency) + fusion overhead。
- **运维面向**——每个 index 都是新的会坏、会 stale、会需要 reindex 的东西。
- **Eval 复杂度**——加 index 意味着 re-run eval set，确认没把既有成果搞烂。

建议顺序：先上纯语义 → 字面 query 开始失败时加 BM25 → 只有在真的需要 freshness 时加 recency → 只有在 eval 证明 routing 赢的时候加 domain index。

---

## PM 常见错误

1. **因为听起来很聪明就加 index**——没 eval 的话，新 index 可能反而伤害品质。一定要量测。
2. **把 RRF 当魔法**——只有当每个 index 真的贡献有用排名时品质才会提升。没用的 index 还是照吃 latency。
3. **跳过 eval set**——没 eval 就不知道哪个 index 造成什么改变，regression 会躲起来。
4. **忽略延迟复利**——每个 index 都有 latency 成本；"六个 index 并行"不是免费的。
5. **把 retrieval 细节露给用户**——做对的 multi-index retrieval 对用户是隐形的，他们不该看到"哪个 index 找到这个 chunk"。细节内部留。

> **核心洞见**
>
> Multi-index retrieval 是让你的 RAG 产品能持续改进而不用改写的架构。Retriever + RRF pattern 是一份组合契约：每个新的 retrieval signal 都能干净插入、独立量测，要么改善产品、要么被移除。这个**可组合性**正是 RAG 玩具跟 RAG 平台的差别。

---

## CCA 考试关联

- **D1（Agentic Architecture）**：hybrid retrieval 与 rank fusion 是核心进阶 RAG pattern。
- **D5（Enterprise Deployment）**：modular retriever 设计是 production RAG 能 scale 而不拆掉 retrieval 层的关键。
- 题目 pattern："如何合并两个分数不兼容的 retrieval 系统？"→ 对 rank 做 reciprocal rank fusion，不是 score。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 专家评审团 analogy 怎么对应 multi-index retrieval？ | 每个搜索方法是个有自己尺度的评审；把他们的意见 rank-normalize，选多位评审都排前面的那道菜。 |
| 为什么 reciprocal rank fusion 用 rank 而不是 raw score？ | 因为不同搜索方法用不兼容的 scoring system——rank 是唯一的通用货币。 |
| 什么时候该加第二个 index 到你的 RAG 产品？ | 当 eval set 显示概念或字面 query 开始失败，而有互补方法可以接住的时候。 |
| Index 加入的建议顺序？ | 先语义 → 字面 query 失败时加 BM25 → freshness 重要时加 recency → eval 证明有效时加 domain-routing。 |
| 新 index 怎么影响 latency？ | 每个都加 latency（通常并行）；总延迟是 max(per-index) 加上 fusion overhead。加之前先算预算。 |
| 加 index 的隐形成本？ | Ingest 运算、存储、运维面、eval 复杂度——不只 query latency。 |
| Multi-index RAG 最大的 PM 错误是什么？ | 没有 eval set 就加 index，没人能证明有没有改善。 |
| Multi-index retrieval 对终端用户是否可见？ | 不——它应该完全是内部的。用户只看到"答案变好"，永远看不到哪个 index 拿了什么。 |
