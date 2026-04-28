# Prompt Caching — Engineering Deep Dive（简体中文）

| 项目 | 详情 |
|------|------|
| 考试领域 | D5 — Enterprise Deployment (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 5.1（成本／延迟优化）、5.2（生产性能）、1.2（多轮效率） |
| 来源 | building-with-the-claude-api / 06-extended-features / Lesson 56 |

---

## One-Liner

Prompt caching 是一种生产级优化，把 Claude 每次请求都要做的 preprocessing（tokenization、embeddings、上下文分析）缓存起来，让后续相同前缀的请求直接复用，而不是每次都从头重算——结果就是更快、更便宜。

---

## Claude 一般怎么处理请求？

你发给 Claude 的每条消息，在真正产出任何输出 token 之前，都要先走一条昂贵的 preprocessing 流水线：

1. **Tokenization（分词）** — 把 prompt 切成一个个 token。
2. **Embedding（向量化）** — 每个 token 转成高维向量。
3. **上下文分析** — 根据上下文补充语境，让后面的 attention 能对整个序列进行推理。
4. **生成** — 前三步做完之后，才开始真正产出文字。

关键点：回答发完之后，**这些 preprocessing 结果全部被丢弃**。一分钟后你再发同一份 6K token 的 prompt，Claude 会把整个流程再跑一遍。

---

## 为什么「丢弃」是问题

只要你的 workflow 会重复用到同一份 base content，这种浪费就非常明显：

- 一次对话里你反复让 Claude 精炼同一份 summary。
- 对同一份 50 页 PDF 连续问 20 个问题的文档分析流程。
- Agent loop 每一轮都带着相同的 system prompt + tool schema。

第 2 次请求时，Claude 得把刚才几秒前才分析过的内容重新 preprocess 一遍。课程原话：「*我刚刚处理过那条消息、结果全丢了——明明可以复用！*」

这个成本要付两次：一次是延迟（输入处理时间），一次是金钱（输入 token 计费）。

---

## Prompt Caching 如何解决？

Prompt caching 改写这条 workflow，核心是：**把 preprocessing 的结果保留下来，不再丢弃**。

- 第一次请求，Claude 照常 preprocess，但把中间状态写入 cache。
- Cache 像一张查找表：「如果我之后再看到一模一样的前缀，就直接复用结果。」
- 后续请求如果发的前缀一模一样，命中 cache，跳过 preprocessing 直接进入生成，只对新的（未 cache 的）token 计费。

结果：昂贵的 preprocessing 费用被摊平到许多次调用之间，而不是每次都重付一次。

---

## 主要好处

| 好处 | 生产含义 |
|------|----------|
| **更快的响应** | Cache 命中的请求跳过 tokenization／embedding／上下文处理，time-to-first-token 下降。 |
| **更低的成本** | 命中的部分按显著折扣计费，不再按全新 input token 付费。 |
| **自动优化** | 第一次请求写入 cache，后续请求自动读取——无需客户端缓存管理。 |

---

## 重要限制

| 限制 | 含义 |
|------|------|
| **Cache 存活 1 小时** | 只对「同一小时内频繁重复调用」的 workflow 有效。闲置的对话会被清除。 |
| **使用场景有限** | 只有在重复发送相同内容时才有用，一次性 prompt 没有收益。 |
| **需要高频率** | 同一前缀重用得越频繁，省得越多；零星调用可能连设置成本都不划算。 |

---

## Prompt Caching 什么时候最有用？

课程点出两个典型场景：

1. **文档分析 workflow** — 同一份大型文档被多次引用，你在上面问不同的问题。文档只 cache 一次，后续问题便宜地读。
2. **迭代编辑任务** — base content（例如草稿）不变，你只针对特定部分反复调整。草稿被 cache，修改是增量。

更广义地说，只要是「**大而稳定的前缀 + 小而变动的后缀**」的 workflow，都是强候选。

---

## Common Mistakes

1. **对一次性 prompt 启用 cache** — 为永远不会再被读取的内容支付 cache-write 附加费。Cache 只有在一小时内被重用才省钱。
2. **以为 caching 会自动发生** — 不会。没有明确 opt-in（cache breakpoint，见 lesson 57），Claude 照常丢弃 preprocessing。
3. **忽略 1 小时 TTL** — 把依赖 cache 的 workflow 设计成低频执行，cache entry 还没被重用就过期了。
4. **以为 cache 只省延迟** — 它同时节约可观的 input token 成本，这在生产中通常是更大的胜利。
5. **低估 preprocessing 成本** — 以为 input token 「免费」。对大型 system prompt 和 tool schema 来说，它占总成本和总延迟的比例比想象中大得多。

---

> **Key Insight**
>
> Prompt caching 本质是**摊平（amortization）技巧**：大而稳定前缀的昂贵 preprocessing 只付一次，之后一小时内所有共用这段前缀的调用都可以复用。在生产中，这是 agent loop、RAG 管道、以及任何重复发送相同 context 的 workflow 最大的单项成本／延迟优化手段。是 D5 Enterprise Deployment 的基本功。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）** — caching 是 task 5.1（成本／延迟）下核心的生产优化。要知道 caching **同时**降低成本和延迟。
- **D1（Agentic Architecture）** — 带稳定 system prompt 和 tool schema 的 agent loop 是 caching 的典型受益者；同样的 context 每轮都要发一次。
- 常见考题问法：「同一个大 prompt 会被重复发送时，如何降低成本和延迟？」→ 答案是 prompt caching。

---

## Flashcards

| Front | Back |
|-------|------|
| Prompt caching 解决什么问题？ | Claude 每次请求都要重跑昂贵的 preprocessing（tokenization、embeddings、上下文分析），即使刚刚才处理过同样内容。Caching 复用那份工作。 |
| Claude 一般做哪四个 preprocessing 步骤？ | Tokenization、embedding、基于上下文的分析，然后才是输出生成。 |
| Cache 存活多久？ | 一小时。 |
| Prompt caching 提供哪两个好处？ | 更快的响应（更低延迟）以及 cache 部分更低的成本。 |
| 什么情境下 prompt caching 没用？ | 一次性 prompt、一小时内打不到同一前缀的零星 workflow、或每次都在变的内容。 |
| 举两个典型的 prompt caching 场景。 | 文档分析 workflow（对同一份长文档问很多问题）和迭代编辑任务（同一份 base content 反复精修）。 |
| Prompt caching 是自动的吗？ | 不是——必须明确启用；不 opt-in 的话 Claude 照常丢弃 preprocessing。 |
| 启用 caching 后，第一次请求发生什么？ | Claude 照常做 preprocessing，但把中间结果存起来，后续请求便可复用而不用重算。 |
