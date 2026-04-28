# Implementing the RAG Flow — PM Perspective（产品视角）

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Architecture（22%）主领域；D5 — Enterprise Deployment（20%）次领域 |
| Task Statements | 1.3（context management）、5.2（production search infrastructure） |
| 来源 | building-with-the-claude-api / 05-rag / Lesson 49 |

---

## 一句话总结

RAG 把一堆私有文档变成产品功能——五步骤流程（切、embed、存、对 query embed、搜索）是让 Claude"认识你们公司"所需最小的投资。

---

## Mental Model：会贴便利贴的图书馆员

想象你请了一位聪明的研究助理，他知道所有公开资料，但从没看过你们内部 wiki。你不可能每次问问题前都让他读 10,000 页。

所以你：

1. 把 wiki 切成一张张主题便利贴（**chunk**）。
2. 每张便利贴贴上一张颜色贴纸代表它的意思（**embed**）。
3. 按颜色把便利贴归档到一个巨大墙面组织器（**vector store**）。
4. 用户问问题时，你在问题上贴一张相同规格的颜色贴纸（**query embedding**）。
5. 走到墙边拿几张颜色最接近的便利贴（**similarity search**）。

助理只读这几张便利贴回答——快、准、而且有实际 wiki 作根据。

---

## PM 为什么要在意

以下需求默认答案都是 RAG：

- "助理要认得我们内部文档。"
- "它要能回答我们产品目录的问题。"
- "客服要能看到相关的过去工单。"
- "工具要能参照公司政策回答。"

没有 RAG，Claude 只能给通用答案。有 RAG，Claude 的答案**以贵公司 source of truth 为基础**——底层文档一更新，答案就跟着更新。

---

## Product Use Cases

### RAG 是对的选择

| User Need | 为什么 RAG 合适 |
|-----------|-----------------|
| "问我们知识库"的助理 | 语料庞大、问题多样、需要新鲜度 |
| 客服自助化 | 要根据现行 help article 作答 |
| 内部 wiki / onboarding copilot | 员工对已知文档问非结构化问题 |
| 产品目录搜索（"推荐 1,500 美元以下笔电"） | 意图语义比规格更重要 |
| 合同 / 政策查询 | 大型法律语料，每次查询聚焦 |

### RAG 过头或不对的情况

| User Need | 更好的方案 |
|-----------|------------|
| 一般聊天或 brainstorm | 基本模型就够 |
| 精确 unique ID 查询 | 正常 DB query，不用 vector search |
| 实时数据（价格、库存） | Tool use，不要用会 stale 的 index |
| 超小语料（<几页） | 直接贴在 system prompt |

---

## 五步骤（大白话）

1. **Chunk**——把每份文档切成一小段一小段。
2. **Embed**——把每段变成一个表达它意思的 vector。
3. **Store**——把 vector 连同原文存进可搜索的 index。
4. **Embed 问题**——把 user query 转成同一类型的 vector。
5. **搜索**——返回最相似的 chunks 给 Claude 当 context。

产品洞见：步骤 1–3 是**批量预处理**（付一次），步骤 4–5 在每笔 user query 都要跑（按次付）。

---

## PM 决策框架

| 问题 | 如果答 Yes | 含义 |
|------|-----------|------|
| 语料是否大于 context window？ | Yes | 必须用 RAG。 |
| 内容更新频率高于每月一次？ | Yes | 编列 ingestion/refresh pipeline 预算。 |
| 用户问的是语义问题（不是精确查）？ | Yes | Vector search 是对的检索模式。 |
| 用户也会问具体 ID / SKU / error code？ | Yes | 规划 hybrid search（后续课程）。 |
| 语料属机密？ | Yes | 评估 vector store 自建还是云端以符合合规。 |

---

## 成本与新鲜度现实检查

RAG 有三个经常性成本中心，PM 常常低估：

- **Embedding 成本**：每个 chunk embed 一次；每个 query 每次都 embed。会随语料和流量放大。
- **存储成本**：vector index 随语料大小和 chunk 数量成长。要编列 index rebuild 成本。
- **Ingestion / refresh latency**：如果文档每天更新，index 不跑 refresh job 会一天内就 stale。一开始就决定 SLA。

好 PM 的习惯：PRD 里写一行"RAG freshness SLA"——例如"知识库答案最多不超过 24 小时 stale"。

---

## PM 常见错误

1. **承诺实时知识，但 index 每晚才 refresh**——用户几天内就抓到 stale 答案。
2. **忽略 chunking 策略**——糟糕 chunking 会悄悄拉低答案品质，还被骂"Claude 很笨"。
3. **没做 eval 就 ship**——上线前要有一组"问题 + 预期 citation"的 test set 才抓得到 regression。
4. **没 log retrieved chunks**——用户抱怨答案烂，看不到当时取回哪些 chunks 根本没法 debug。
5. **以为语义搜索能处理精确查询**——经常漏 ID 和代号，通常需要 hybrid search（BM25 + 语义）。

> **核心洞见**
>
> RAG 不是模型功能——它是**数据 pipeline 的产品决策**。品质上限由语料整理、chunking 策略、freshness SLA 决定，不是由模型决定。把 RAG 当成"神奇地让 Claude 认得我们文档"的 PM 会低投入在 pipeline 上，最终 ship 出令人失望的功能。

---

## CCA 考试关联

- **D1（Agentic Architecture）**：RAG 是扩充 Claude 知识超越训练数据的经典 pattern。
- **D5（Enterprise Deployment）**：了解 production 跑 vector index 的成本与 freshness 取舍。
- 题目模式："Claude 不认识我们内部文档——该用什么 pattern？"→ RAG。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 便利贴图书馆员 analogy 怎么对应 RAG？ | 把 wiki 切成便利贴、每张贴一张意思贴纸、按颜色归档、把问题贴同类贴纸、抓最近的便利贴。 |
| 什么时候 RAG 是错的工具？ | 精确 ID 查询（用 DB）、实时数据（用 tool use）、或超小语料（直接放 system prompt）。 |
| 哪些 RAG 步骤是 batch 预处理？哪些是 per-request？ | Chunk、embed、store 是预处理（付一次）。embed query + 搜索每次 user request 都跑。 |
| RAG 功能 PRD 必须写什么？ | Freshness SLA、eval set、retrieval logging、embedding + vector store 成本预算。 |
| 为什么 chunking 策略对 PM 很重要？ | 烂 chunking 会悄悄拉垮答案品质，却被误会成"模型很笨"——其实是你管的 pipeline bug。 |
| 让 Claude"认得你们公司"所需最小的单位是什么？ | 五步骤 RAG 流程：chunk、embed、store、embed query、搜索。 |
| RAG index 该多久 refresh 一次？ | 取决于底层文档更新频率；SLA 是 PM 在 PRD 里的决策。 |
| 用户在 RAG 功能里问精确 ID，你要怎么办？ | 规划 hybrid search——把 BM25 lexical search 跟 semantic search 合并（下几节课会教）。 |
