# Text Embeddings — PM 视角

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Architecture (22%) 主要；D4 — Safety & Alignment (20%) 次要 |
| Task Statements | 1.3（context management）、4.1（grounded responses） |
| 来源 | building-with-the-claude-api / 05-rag / Lesson 47 |

---

## 一句话总结

Embeddings 是「意义的 GPS 坐标」，它让你的 RAG 功能有能力把用户问题对应到正确 chunk — 同时悄悄把第二个 vendor 引入你的 stack。

---

## 心智模型：想法的 GPS 坐标

想象把你 corpus 的每一句话都放进一张巨大的高维地图。关于「revenue」的句子落在一个社区；关于「risk factors」的落在另一个；关于「supply chain」的落在第三个。

用户提问时，你把他们的*问题*放到同一张地图上，找最近的邻居。那些邻居就是最可能回答问题的 chunks。

| 概念 | PM 白话 |
|------|---------|
| Embedding model | 制图师 — 把文字变成坐标 |
| Embedding 向量 | 地图上的特定坐标 |
| Semantic similarity | 两个坐标之间的距离 |
| Semantic search | 「找地图上最近的邻居」 |

优雅之处在于即使字词不同也有效。「这家公司赚了多少？」会落在「Revenue: $X million」附近，因为制图师懂意义，不只是关键词。

---

## 为什么 PM 要关心 embeddings

Embeddings 看起来是工程实现细节，但驱动用户看得到的结果：

- **retrieval 质量** — 更好的 embedding model 代表更高几率找到对的 chunk
- **每次查询成本** — 每个用户问题都触发一次 embedding 调用；provider 定价直接影响单位经济
- **延迟** — embedding 是每次查询额外的 network hop；吃掉你的 p95 延迟预算
- **vendor 多样性** — embeddings 把第二个 AI vendor（VoyageAI）引入，和 Anthropic 并存，有自己的 SLO 和 outage 风险
- **keyword vs. semantic 取舍** — embeddings 帮助用自然语言提问的用户，但对输入确切词的用户来说纯 keyword search 还是更快

---

## 两 vendor 的现实

PM 常漏掉这块：RAG 功能不是「Anthropic 的 AI」，是「Anthropic **加** VoyageAI 的 AI」。因为 Anthropic 目前不提供 embedding，你需要第二个 AI provider，它的 API 对每次查询都是 critical。

这代表功能可用性现在被以下约束：
- Anthropic 的 uptime（generation）
- VoyageAI 的 uptime（embeddings）
- 你的 vector database 的 uptime（retrieval）

三个 vendor、三个 SLO、三条事件通道。要事先规划。

---

## 产品用例

### Embeddings 在以下情境发光

| 场景 | 理由 |
|------|------|
| 用户用自然语言提问 | 比对意义不是关键词 |
| corpus 使用用户不认识的术语 | 「Profit」能匹配「net income」 |
| 用户改写或问模糊问题 | semantic similarity 宽容字词 |
| 多语言支持 | multilingual embedding 可跨语言匹配 |

### Embeddings 吃力在以下情境

| 场景 | 更好的替代 |
|------|------------|
| 用户输入确切产品代码 | Keyword／lexical search |
| 查询是短 token（「SKU-4821」） | 结构化搜索，不是 embedding |
| 需要可解释的匹配 | keyword search 匹配看得见；embedding 是黑盒 |
| 成本吃紧且 corpus 很小 | 小 corpus 可能不值得建 embedding pipeline |

这就是 Lessons 49-51 介绍 BM25 等混合方法的原因 — 纯 semantic 或纯 keyword 都不完美。

---

## Input type 有差

VoyageAI 的 API 有 `input_type` 参数，让你告诉模型某段文字是 **query**（用户问题）还是 **document**（corpus 里的 chunk）。模型是非对称调校过的 — 同一段文字依 input type 产出略不同的向量。

对 PM 而言这是你可以验证工程有没有用好的质量杠杆。「query 有标 query，document 有标 document 吗？」是 RAG review 会议里合理的问题。

---

## PM 决策框架

签核 RAG 功能前，要有这些的清楚答案：

| 问题 | 为什么 |
|------|--------|
| 我们用哪个 embedding provider？ | 引入 vendor 依赖 |
| 每次查询成本是多少？ | 和使用量相乘 |
| embedding 调用的 p95 延迟是多少？ | 累加到用户感知的总延迟 |
| query 和 document 的 `input_type` 用对了吗？ | 做对就是免费质量提升 |
| VoyageAI 挂掉怎么办？ | fallback 计划 — cache、keyword search、降级模式 |
| 如何对我们特定内容评估 embedding 质量？ | 通用 benchmark 会骗人；要有领域 eval set |

---

## 「黑盒」UX 挑战

Embedding 是黑盒。retrieval 失败无法靠指某个关键词来解释。当用户问「为什么挑*那个* chunk？」，诚实的答案只有「它的向量最接近你 query 的向量」。这很少令人满意。

两个产品回应：
1. **逐字显示 chunk 作为 citation** — 让用户看到 retrieve 到什么，即使不懂为什么
2. **记录 retrieval score** — 让工程能在 score 可疑偏低时 debug
3. **提供 keyword fallback** — semantic retrieval 失败时让用户强制 exact 搜索

---

## 常见 PM 错误

1. **不知道有两个 vendor** — 上 RAG 功能却没意识到 Anthropic 不提供 embedding。
2. **没有每次查询成本模型** — 忘了每个用户问题都触发 VoyageAI 调用，单位经济变模糊。
3. **以为 keyword search 过时了** — 没有；有些用户查询还是 exact matching 服务得更好。
4. **把 embedding 当「纯工程」** — embedding 选择影响 retrieval 质量，用户看得到。
5. **embedding outage 没 fallback** — VoyageAI 挂掉，整个 RAG 功能就挂，除非你事先规划。

> **关键洞察**
>
> Embedding 是 RAG 从模型功能变成**多 vendor、多延迟、多失败模式** pipeline 的地方。把 embedding 当实现细节的 PM，会被生产成本、延迟、outage 吓到。对的视角：embedding 是基础 infrastructure 依赖，对你产品的重要性等同你的 database。

---

## CCA 考试关联

- **D1（Agentic Architecture）**：embedding 是 RAG 的 retrieval 骨干。记基本事实 — 它是什么、谁提供（本课程是 VoyageAI）、-1 到 +1 的范围。
- **D4（Safety & Alignment）**：更好 embedding → 更好 retrieval → 更好 grounding → 更少幻觉。embedding 是 retrieval 质量的起点。
- 注意 Anthropic／VoyageAI 分工的题目 — 「本课程用哪个 provider 做 embedding？」是合理考题。

---

## Flashcards

| Front | Back |
|-------|------|
| embeddings 的 PM 友好比喻？ | 意义的 GPS 坐标 — 每个句子落在语义地图，retrieval 找最近邻居。 |
| 本课程推荐哪家做 embeddings？ | VoyageAI — Anthropic 目前不提供 embeddings。 |
| embeddings 引入什么多 vendor 风险？ | RAG 功能现在同时依赖 Anthropic 和 VoyageAI；任一 outage 功能就坏。 |
| 何时 semantic search 比 keyword search 差？ | 用户输入确切代码、短 token 或结构化标识符时。 |
| `input_type` 为什么对 PM 重要？ | 对问题用「query」、对 chunks 用「document」是免费 retrieval 质量提升。 |
| embedding 的「黑盒」UX 挑战？ | 你无法靠关键词解释 retrieval 匹配；用户可能问「为什么这个 chunk？」诚实答案是「向量距离」。 |
| 列出 embedding 增加的三个成本／延迟因素。 | 每次查询 embedding 成本、embedding API 延迟、整个 corpus 的预处理成本。 |
| RAG 验收 checklist 里 PM 应该要求什么？ | provider 确认、每次查询成本理解、embedding outage fallback、retrieval 质量的领域 eval set。 |
