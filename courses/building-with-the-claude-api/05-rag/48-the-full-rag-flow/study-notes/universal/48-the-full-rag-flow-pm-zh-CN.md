# The Full RAG Flow — PM 视角

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Architecture (22%) 主要；D4 — Safety & Alignment (20%) 次要 |
| Task Statements | 1.3（context management）、4.1（grounded responses） |
| 来源 | building-with-the-claude-api / 05-rag / Lesson 48 |

---

## 一句话总结

完整 RAG flow 有六步，干净地切成「一次性预处理 pipeline」和「每次查询 pipeline」两半 — 搞懂这个切割是 PM 推理任何 RAG 功能成本、延迟、内容新鲜度的方式。

---

## 心智模型：图书馆卡片目录

想象一座用户还没进来的图书馆：

| 阶段 | 图书馆比喻 | RAG 步骤 |
|------|------------|----------|
| Setup | 馆员读每本书、写索引卡 | Chunk + embed + store |
| 等待 | 卡片目录整齐待命 | Vector DB 已就绪 |
| 问题 | 访客问「关于中世纪烹饪的书？」 | User query 到达 |
| 查找 | 馆员翻卡找最接近的匹配 | Embed query + cosine similarity |
| 答复 | 馆员把相关书交给访客 | Retrieved chunks 进 prompt |
| 综合 | 访客读书、写报告 | Claude 写最终答案 |

图书馆能运作只因有人事先做了索引工作。那就是 RAG 的预处理 pipeline。查询时步骤则是馆员迎接每位访客。

---

## PM 白话的六步

```
[预处理 — 每份文档付钱一次，受惠于未来所有 query]
1. Chunk:       「把文档切成可搜索片段」
2. Embed:       「把每片转成意义坐标」
3. Store:       「把所有坐标放进 vector database」

[查询时 — 每次用户请求付钱一次]
4. Embed query: 「把用户问题转成意义坐标」
5. Search:      「用 cosine similarity 找最接近坐标」
6. Prompt:      「问题 + top 匹配交给 Claude 回答」
```

**PM 关键洞察**：新增一份文档，1-3 跑一次。今天有一百万用户问问题，4-6 跑一百万次。预算成本和延迟代表要知道哪一步住在哪一半。

---

## 为什么这个切割对产品规划重要

| 维度 | 预处理侧（1-3） | 查询时侧（4-6） |
|------|-----------------|------------------|
| 谁付钱？ | 被未来所有 query 摊提 | 每次用户请求付一次 |
| 延迟敏感？ | 不 — 后台跑 | 是 — 用户在等 |
| 新鲜度影响 | 过时 index 代表过时答案 | 永远读 index 最新状态 |
| 失败爆炸范围 | 坏 batch 污染未来 retrieval | 坏 query 伤害一次用户交互 |
| 成本优化 | 更少 re-index、更 aggressive batch | 更小 top-k、缓存 embedding |

产品决策会打在不同半边。「我们要答案反映今天更新」是预处理问题。「我们要 2 秒内答」是查询时问题。

---

## 「bug」例子当产品课

lesson 的玩具例子用一个含「bug」字的医疗研究 chunk（XDR-47 病毒那种）和一个软件工程 chunk。用户问「How many bugs did engineers fix this year?」。

keyword retriever 可能返回医疗 chunk 只因字面含「bug」。cosine-similarity retriever 会正确返回软件 chunk，因为 query 的语义方向匹配软件 chunk 的语义方向（cosine similarity 0.983 vs. 0.398）。

**这就是 RAG 做对的产品价值**：用户拿到他们想问的答案，而不是关键词找到的答案。对于客服、法律、企业搜索产品，这个差异会反映在客户满意度上。

---

## 给 PM 的 Cosine Similarity

你不需要数学，但需要直觉：

| 分数 | 意义 | PM 白话 |
|------|------|---------|
| +1.0 | 向量同方向 | 完美匹配 |
| ~0.9 | 方向非常接近 | 很有信心相关 |
| ~0.5 | 大致同社区 | 可能相关 |
| 0.0 | 垂直 | 无有意义关联 |
| -1.0 | 反方向 | 反相关 |

**Cosine distance** 是 `1 - cosine similarity`。小距离＝高相似度。产品仪表板有时显示其中之一；知道两者是同一指标、极性相反。

PM 应该问：「我们的 top-k similarity 门槛是多少？」和「top match 相似度低于 X 时，要不要显示『没有好答案』回应而不是编造一个？」

---

## 产品用例

| 场景 | pipeline 落点 |
|------|---------------|
| 客服 copilot | 重度 help articles 预处理；快速查询时 retrieval |
| Chat-with-your-PDF | 用户上传 → 上传时预处理 → 对话时 query |
| 企业知识搜索 | 持续 re-index Confluence/Drive；高 QPS query 路径 |
| 法律研究 | 大 corpus，稀少但高风险查询；质量优于速度 |

---

## PM 决策框架

任何 RAG 产品，要能回答：

| 问题 | 哪一半 | 为什么 |
|------|--------|--------|
| 文档多常变？ | 预处理 | 驱动 re-indexing 计划与成本 |
| Corpus 多大？ | 预处理 | 驱动存储与 embedding 成本 |
| 每日多少查询？ | 查询时 | 驱动每次查询预算 |
| 延迟 SLO 是什么？ | 查询时 | 驱动 top-k、caching、模型选择 |
| retrieval 找不到好匹配怎么办？ | 查询时 | 塑造「无答案」UX 避免幻觉 |
| 怎么对用户显示 citation？ | 查询时 | 最终 prompt／UI 步骤的一部分 |
| 文档变更时怎么 re-index？ | 预处理 | 必须是 owned 工程流程 |

---

## 常见 PM 错误

1. **混淆预处理与查询时成本** — 搞不清楚为什么 RAG 某些情境贵、某些情境便宜。
2. **没有 stale-index 计划** — 用户会发现文档更新要好几天才反映在答案里。
3. **没设 similarity 门槛** — 低置信度匹配被当高置信度匹配对待，导致错答案。
4. **没有「无答案」UX** — retrieval 找不到好东西时 Claude 还是会产出，用户拿到编造内容。
5. **UI 略过 citation** — 用户无法验证答案，就抓不到 retrieval 失败，信任默默崩塌。

> **关键洞察**
>
> 六步 RAG flow 其实是两个 pipeline 共享一个 vector database。预处理是你对每份文档付一次的投资；查询时是你每次用户请求要付的经常性成本。PM 把这两半分清楚就能推理单位经济、延迟预算、新鲜度、失败模式 — 这就是「RAG 功能能交付」与「RAG 功能在生产默默坏掉」的差别。

---

## CCA 考试关联

- **D1（Agentic Architecture）**：端对端 RAG 题会考你是否知道六步顺序和 cosine similarity 在哪一步。
- **D4（Safety & Alignment）**：grounding flow（retrieve chunk、用 XML tag 包、交给 Claude）是课程里经典的降幻觉 pattern。
- 熟悉 cosine similarity 范围（-1 到 +1）和 cosine distance 关系（1 - cosine similarity）。

---

## Flashcards

| Front | Back |
|-------|------|
| RAG flow 的两半是什么？ | 预处理（chunk、embed、store — 每份文档一次）和查询时（embed query、retrieve、prompt — 每次用户请求一次）。 |
| RAG 的图书馆类比是什么？ | 馆员事先索引书；访客提问时馆员查最接近的索引卡并交出相关书。 |
| Cosine similarity 范围？ | -1 到 +1。 |
| cosine similarity 0.983 代表什么？ | 极高相似度 — 两向量几乎同方向。 |
| 「bug」例子的 similarity 分数差是多少？ | Query 对软件 chunk = 0.983；Query 对医疗 chunk = 0.398。 |
| PM 为什么在意预处理／查询时切割？ | 它决定成本、延迟、新鲜度、失败模式在生产怎么表现。 |
| 什么是 cosine distance？ | `1 - cosine similarity` — 一种报告惯例，小值代表高相似度。 |
| 举一个由查询时半边驱动的产品决策。 | 延迟 SLO、top-k 大小、「无答案」UX、caching 策略。 |
| 举一个由预处理半边驱动的产品决策。 | Re-indexing 计划、chunking 策略、embedding provider 选择、corpus 大小预算。 |
