# Making a Request — PM Perspective（简体中文）

| 项目 | 内容 |
|------|------|
| Exam Domain | D5 — Enterprise Deployment (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 5.1（model selection）、5.3（production patterns）、1.2（agentic loop 基础） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 06 |

---

## One-Liner

单次 Claude 请求是任何 AI feature 最小的产品价值单位——三个参数决定 feature 的质量、成本、失败模式。所以 PM 要像 review UI 文案那样 review `model`、`max_tokens`、`messages`。

---

## Mental Model：自动售货机交易

把 `client.messages.create()` 想成自动售货机：

| 自动售货机 | Claude 请求 |
|----------|------------|
| 选机器（咖啡 vs 汽水） | 选 `model`（Sonnet、Haiku、Opus） |
| 投正确的钱 | 提供 API key |
| 按按钮（哪个商品） | 发 `messages`（prompt） |
| 机器吐出最多一份商品 | Claude 回最多 `max_tokens` 的内容 |
| 收据含价格 | `response.usage` 含 input/output token 数 |

你产品里每个 feature 都是几千次这种交易组成的系统。质量、成本、延迟都是三个参数选择的涌现结果。

---

## 三个参数就是产品决策

### Model

选 model 是伪装成技术决策的产品决策。它在速度、能力、成本之间权衡。

| Model 档次 | 适合 | PM 考量 |
|-----------|------|--------|
| Sonnet（平衡） | 大多数 feature 的 default | 好基准，从这里开始 |
| Haiku（快、便宜） | 摘要、分类、高量 | 每次调用便宜，难题可能错过细节 |
| Opus（最强） | 推理重的 feature、复杂草稿 | 每次调用贵，留给高价值流程 |

注：课程里的 model 名称是示例；实际使用时永远跟工程师确认当前 model（例如 `claude-sonnet-4-5`）。

### `max_tokens`

这是你每次调用的成本上限。对 `max_tokens` 没意见的 PM 等于让工程师默默决定 feature 质量。

| Feature 类型 | 建议 max_tokens | 理由 |
|-------------|----------------|------|
| 聊天回复 | 500–1000 | 短回复，留空间给细节 |
| 文档摘要 | 1000–2000 | 有界但需要喘息空间 |
| 长篇草稿（email、blog） | 2000–4000 | 除非要快，否则值得花钱 |
| 分类 / 路由 | 50–100 | 单 token 答案，浪费 token = 浪费钱 |

**关键澄清**：`max_tokens` 是上限，不是目标。想要更长的输出，要在 prompt 里要求，不是把上限调高。

### `messages`

Messages list 是你的"对话状态"。单轮 feature（问答、摘要）只有一个 entry。多轮 feature（chat、agent）会增长。Lesson 07 会细讲多轮。

---

## Product Use Cases

### 单次请求就够的时候

| Feature | 为什么单轮就够 |
|---------|--------------|
| "帮我摘要这份文档" | 一问一答 |
| "翻译这段文字" | 无状态转换 |
| "分类这张 ticket" | 路由决策，没有后续 |
| "把这封信改成更友善的语气" | 发射后不管的转换 |

### 需要不止一次调用的时候

| Feature | 为什么单轮不够 |
|---------|--------------|
| 带历史的聊天 | 需要 `messages` 随时间增长（Lesson 07） |
| 使用 tool 的 agent | 需要依 `stop_reason` 分支的 loop（Lesson 32+） |
| Streaming 输出 | 同一个调用加 `stream=True` flag |

---

## PM Decision Framework：Pre-Launch 问卷

Claude feature 出货前，PRD 要回答这些问题：

| 问题 | 默认 |
|------|------|
| 要调用哪个 model？ | 没特别原因就 Sonnet 起步 |
| `max_tokens` 设多少？ | 合理回复最长长度 × 1.5 |
| 单轮还是多轮？ | 默认单轮，除非用户要追问 |
| 典型一次调用多少钱？ | 计算：（平均 input + output token）× 价格 |
| 调用中给用户看什么？ | Loading state、streaming、optimistic UI |
| `stop_reason == "max_tokens"` 怎么办？ | 定义截断 UX |
| 怎么测 prompt 质量？ | Eval harness 或人工 review loop |

---

## 成本经济学白话版

每次调用有两个成本部分：

- **Input tokens** —— 你发出去的所有东西长度（system prompt + messages）
- **Output tokens** —— Claude 回复的长度

你按方向按百万 token 付费。PM 的启示：

| 杠杆 | 对成本的影响 |
|------|-------------|
| 较短的 prompt | 线性便宜 input |
| 较紧的 `max_tokens` | 盖住最坏情况 output 成本 |
| 较小的 model | 显著便宜但可能降质量 |
| 把多个问题 batch 成一次调用 | 省每调用 overhead 但失败会绑一起 |
| 用 tool use 取代巨大 context window | 每调用 input token 变少（Lesson 32+） |

经验法则：多数 feature 的账单被 input token 主宰，因为你一直重发 context。Lesson 07（多轮）会让这个效应戏剧化。

---

## Common PM Mistakes

1. **对 `max_tokens` 没意见** —— 让工程师默默决定 feature 质量上限，而你不知道被盖住了。
2. **以为 model 越大越好** —— 分类和路由 Haiku 比 Sonnet 在成本上完胜，而且用户察觉不到差别。
3. **PRD 跳过 prompt 迭代** —— Prompt 是产品文案，应该跟 UI 文字一样 review。
4. **没排 prompt eval infra 的预算** —— 没办法量质量就没办法安全做 A/B。
5. **以为单轮永远比较便宜** —— 长期 chat 如果硬做单轮，重发 context 比多轮更浪费 token。

> **Key Insight**
>
> `messages.create()` 三个参数不是技术冷知识——它们是任何 Claude feature 的三大产品决策：能力（model）、成本上限（max_tokens）、对话设计（messages）。PRD 里三个都明确签核的 PM，feature 会命中成本与质量目标。三个都丢给工程师的 PM，feature 会默默 miss 目标然后被怪"AI 不行"。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）**：情境题问 model selection、`max_tokens` 大小、成本权衡。
- **D1（Agentic Architecture）**：每个 agent 都是在这个单一调用上跑 loop；熟悉原子单位是前置。
- 情境触发："AI feature 太慢/太贵/太短"→ 答案通常都住在三个参数其中一个。

---

## Flashcards

| Front | Back |
|-------|------|
| `messages.create()` 三个跟产品有关的参数是什么？ | `model`（能力）、`max_tokens`（成本上限）、`messages`（对话设计） |
| `max_tokens` 是设目标还是上限？ | 上限——想要更长的输出要在 prompt 里要求，不是调高上限 |
| 为什么 PM 该对 model 选择有意见？ | 它在成本、速度、能力之间权衡；没 PM 介入工程师会默认一个 |
| 什么时候该用较小的 model（Haiku）？ | 分类、路由、高量摘要——用户察觉不到差别的地方 |
| 每次调用的两个成本部分是什么？ | Input tokens（发出去）与 output tokens（Claude 写的） |
| Claude 调用符合什么自动售货机比喻？ | 选机器（model）、投币（API key）、按钮（messages）、拿商品上限一份（max_tokens）、收据（usage） |
| 为什么 prompt 质量是 PM 的事？ | Prompt 是产品文案，决定输出质量，值得 PRD 级别的关注 |
| A/B 测 prompt 前需要什么？ | Prompt 评估 infra 来量质量变化 |
