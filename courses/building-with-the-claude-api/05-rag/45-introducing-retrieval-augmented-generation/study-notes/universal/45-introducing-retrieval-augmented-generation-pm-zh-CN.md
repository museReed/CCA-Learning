# Introducing Retrieval Augmented Generation — PM 视角

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Architecture (22%) 主要；D4 — Safety & Alignment (20%) 次要 |
| Task Statements | 1.3（context management）、4.1（grounded responses） |
| 来源 | building-with-the-claude-api / 05-rag / Lesson 45 |

---

## 一句话总结

RAG 是让「用 AI 问遍公司整个知识库」变成可交付产品功能的关键：它让 Claude 能回答那些根本放不进一次对话的文档。

---

## 心智模型：研究助理与档案柜

想象两种助理的差别：

| 助理类型 | 运作方式 | 限制 |
|----------|----------|------|
| **纯记忆型** | 靠学校学的知识回答 | 训练没碰过的主题就没办法 |
| **Prompt-stuffer** | 你把 800 页报告整本交给他再问 | 他被信息淹没、失焦，影印账单爆炸 |
| **RAG 研究员** | 你问问题；他走到档案柜、抽出最相关的一个文件夹、读完、回答 | 可扩展到超大资料库；每个答案都 grounded 在特定来源 |

RAG 就是 **档案柜 + 研究员** 的 pattern。预处理（chunking + indexing）等于整理档案柜；查询（retrieval + prompt）等于研究员去抽对的文件夹。

---

## RAG 解决的商业问题

每个知识密集的产品都会撞上同一面墙：**「AI 读得到我们的东西吗？」**

- 客服：「能不能从我们 2,000 篇 help articles 回答？」
- 法务：「能不能搜索合同封存库？」
- 企业搜索：「能不能看懂我们 10 年的 Confluence？」
- 财务分析：「能不能从这份 800 页的 10-K 抽出 risk factors？」

没有 RAG，答案是「只有放得进一次 prompt 才行」，而这几乎永远不够。有了 RAG，你对任意大小的 corpus 都有故事可讲。

---

## 产品用例

### 适合 RAG 的场景

| 场景 | 为什么 RAG 赢 |
|------|----------------|
| 知识库 Q&A | corpus 大、问题窄、答案要能引用来源 |
| 「Chat with your PDF」 | 单一文档太大塞不进 context |
| 企业内部搜索 | 多文档、多来源、内容会演进 |
| 领域专家（医疗、法律） | 大量参考资料，答案需要 grounded |
| 客服 copilot | 上千篇 help articles，要找对的那一篇 |

### 不适合 RAG 的场景

| 场景 | 更好的替代 |
|------|------------|
| 可以塞进 prompt 的短 PDF | **直接 prompt** — RAG 是过度工程 |
| 「今天天气如何？」 | **Tool use** — 你要的是实时数据，不是静态文档 |
| 「帮我发这封邮件」 | **Tool use** — 你要的是动作，不是 retrieval |
| 闲聊、不需要知识 grounding | **单纯 Claude** — 不需要 corpus |

---

## RAG 的成本／复杂度取舍

RAG 不是免费的。作为 PM，你拿以下换到以下：

| 放弃 | 换到 |
|------|------|
| 工程简洁 | 突破 context window 的 scale |
| 零 infra 起点 | 每次查询更便宜、更快的 prompt |
| 「把文档丢进去就好」的 UX | 可审计、可引用的答案 |
| 零搜索质量 bug | 本来做不到的功能 |

陷阱是不需要 RAG 时就往 RAG 跳。如果你的知识库舒服放得进 prompt，最简单的架构就是最好的。等 corpus 体积逼你上去时才上。

---

## PM 决策框架

当 stakeholder 说「我们要 AI 读我们的文档」时，问这些：

| 问题 | 如果「是」 |
|------|------------|
| 整个 corpus 舒服放得进一次 prompt 吗？ | 跳过 RAG — 直接塞 |
| 内容是稳定的（非实时）吗？ | RAG 可行 |
| 用户需要 AI 引用或链接到来源吗？ | RAG — retrieved chunks 让 citation 很自然 |
| corpus 每天／每小时在变吗？ | RAG 但要有清楚的 re-indexing 计划 |
| 这其实是实时数据（天气、股价）吗？ | **不是** RAG — 用 tool use |
| 用户会在广大 library 里问窄问题吗？ | RAG 理想 |

---

## 「retrieval 质量」这个产品风险

这是 PM 最常漏掉的一块：**RAG 会默默失败**。

一般 AI 功能给错答案就是错答案，有人会开 ticket。RAG 功能里，不管 retrieval 层抓回什么 chunk，Claude 都会很有信心地根据它回答，即使那 chunk 是错的。用户看到的是流畅、权威、错的答案。

这代表：

- retrieval 质量是**产品质量**问题，不只是工程细节
- 你需要测试 retriever 的 eval，不只是测试模型的 eval
- citation 是用户端的安全功能，让他们能自我查核
- 「置信度」要来自来源，不是来自 Claude 的语气

PM 如果略过这块，就是客服团队被「AI 跟我讲错」淹没的那个人。

---

## 常见 PM 错误

1. **太早上 RAG** — corpus 放得进 10K tokens 就硬上整套 vector database pipeline。
2. **UX 没设计 citation** — Claude 不引用任何东西，用户无法查核，信任崩盘。
3. **把 retriever 当「做完了」** — 没 eval、没监控、默默返回错 chunk。
4. **把 RAG 和 tool use 搞混** — 拿 RAG 去 pitch 一个其实需要实时数据的功能。
5. **忽略 re-indexing 成本** — 忘记每次文档更新都触发一个工程要负责的预处理 pipeline。

> **关键洞察**
>
> RAG 把「懂东西的 AI」变成「读你东西的 AI」。对产品而言，这就是新奇 chatbot 与可交付功能的差别。陷阱是 retrieval 质量会变成产品质量指标：retrieval 烂，模型再怎么调都救不了答案。要上 RAG 的 PM 必须自己拥有 retrieval 的 eval loop，不只是 generation。

---

## CCA 考试关联

- **D1（Agentic Architecture）**：情境题若写「大型文档 corpus ＋ 问问题」→ 答 RAG。熟悉形状：chunk → index → retrieve → prompt。
- **D4（Safety & Alignment）**：RAG 把回答 grounded 在来源文字，这是标准的降幻觉 pattern。
- 注意与 tool use 的对照：实时／动态数据用 tool use，不是 RAG。静态／文档 corpus 用 RAG。

---

## Flashcards

| Front | Back |
|-------|------|
| 用一句话说，RAG 让产品能做什么？ | 能对大到塞不进一次 prompt 的 corpus 提问。 |
| RAG 的「档案柜」类比是什么？ | 预处理＝整理档案柜；查询时＝研究员抽对的文件夹。 |
| PM 何时应该选 prompt stuffing 而不是 RAG？ | corpus 舒服放得进 context window 时，RAG 是不必要的复杂度。 |
| PM 何时应该选 tool use 而不是 RAG？ | 数据是实时／动态（天气、价格、live 系统）而非静态文档时。 |
| RAG 功能隐藏的产品风险是什么？ | retrieval 默默失败 — Claude 很有信心地根据错 chunk 回答。 |
| 为什么 RAG UX 的 citation 很重要？ | 让用户能验证来源，在信任答案前抓到 retrieval 错误。 |
| 举三个 RAG 明显胜出的商业场景。 | 知识库 Q&A、chat-with-your-PDF、企业内部搜索。 |
| 选 RAG 要 PM 放弃什么？ | 工程简洁 — 换来 scale、成本效率、可引用性。 |
