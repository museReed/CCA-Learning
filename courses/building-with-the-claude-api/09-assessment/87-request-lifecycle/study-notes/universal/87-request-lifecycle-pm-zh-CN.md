# 请求生命周期 Request Lifecycle — PM 视角

| 项目 | 说明 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture（22%）主要；D5 — Enterprise Deployment（20%）次要 |
| 任务声明 | 1.1（API request flow）、5.1（secure architecture）、5.3（stop reasons 与 token 限制） |
| 来源 | building-with-the-claude-api / 09-assessment / Lesson 87 |

---

## 一句话重点

Claude request lifecycle 是你产品里每一次 AI 交互的解剖图 —— 看懂它，PM 就能在第一行 code 被写之前，把安全性、延迟预算、成本、事故应对的决策做对。

---

## 为什么 PM 要在意

PM 不需要写 `ast.parse` 也不需要实现 tokenization —— 但 PM **需要**决定架构、审 security、设 token 预算、owning 事故处理。上述每一个决策都藏在这五步流程里：

| PM 决策 | 对应生命周期步骤 |
|---------|------------------|
| "API key 放在哪？" | 步骤 1-2（绝不能在 client） |
| "最坏延迟是多少？" | 步骤 3（model）+ 1-2、4-5 的网络 |
| "每次请求的成本上限？" | 步骤 2（max_tokens）+ 步骤 4（usage） |
| "答案被截断时 UX 怎么处理？" | 步骤 4（stop_reason） |
| "事故 triage 流程？" | 每一步 —— 生命周期就是那张地图 |

跳过这个知识，团队会在没有你的情况下做这些决策，而且通常做错。

---

## 心智模型：餐厅点餐

把每个 Claude request 想成在厨房讲不同语言的餐厅点餐：

| 步骤 | 餐厅比喻 | 生命周期步骤 |
|------|----------|--------------|
| 客人告诉服务员要什么 | 用户跟你的 app 对话 | Request to server |
| 服务员把点单翻成厨房听得懂的语言 | 你的 server 调用 Anthropic API | Request to API |
| 厨房做菜 | Claude 执行 tokenize、embed、contextualize、generate | Model processing |
| 服务员把菜端出来 | API 返回 message、usage、stop_reason | Response to server |
| 把菜放到客人面前 | 你的 server 把文字转回 UI | Response to client |

服务员（你的 server）是不可协商的。你不会让客人自己走进厨房 —— 也绝不让 client 直接调 Anthropic API，同样原因：会破坏厨房的安全和速度保证。

---

## 产品使用场景：每一步为什么重要

### 安全（步骤 1-2）

来源立场明确：**绝不从 client-side 代码调用 Anthropic API**。Client 里的 API key 可以被挖出来做未授权请求。对 PM 而言，这在每个 AI feature 的 PRD 中都是不可协商的安全要求：

- API key 放在 server 的安全存储
- Client 只跟你的 server 讲话，绝不碰 Anthropic
- Server 加 authentication、rate limiting、audit logging

### 成本与延迟（步骤 2-3）

每个 request 都必须含 `max_tokens`。这是 PM 手上最重要的成本杠杆。设太高，脱缰的生成会毁掉 unit economics。设太低，Claude 会讲到一半被截断，用户沮丧。PM 常见做法是按 feature 分层：短回复 256、长解释 2048、文档草稿 8192。

### Response 处理（步骤 4）

API response 有三个 PM 该在乎的字段：

| 字段 | PM 关注点 |
|------|-----------|
| Message | 用户实际看到的内容 |
| Usage | 驱动计费、预算追踪、per-user 额度 |
| Stop Reason | 决定 feature 是正常工作还是被悄悄截断 |

stop_reason 是三者中最阴险的。如果 app 忽略它，`max_tokens` 截断看起来就跟完整答案一样 —— 只差一段文字不见了。永远在 UX 中明确处理 stop reason（例如"响应被切断 —— 要继续吗？"）。

---

## 四个内部阶段 —— PM 为什么要懂

Claude 内部处理有四阶段：**tokenization、embedding、contextualization、generation**。PM 不需要实现，但在概念层面懂它们能解锁更好的产品直觉：

| 阶段 | PM 洞察 |
|------|--------|
| **Tokenization** | 成本和长度以 token 计，不是以字。含大量 code 或非英文的输入比你预想的贵。 |
| **Embedding** | 每个 token 起初承载**所有**可能意义 —— 所以短而有歧义的输入会产出不可靠的结果。 |
| **Contextualization** | 周围字词消歧义 —— 所以框架好的 prompt 胜过裸指令。 |
| **Generation** | Claude 用受控随机性，不是纯最高概率 —— 所以同输入有时产不同输出，"deterministic"不是预设。 |

---

## PM 决策框架

| 问题 | 若答 Yes | 行动 |
|------|---------|------|
| 我们的架构有 server 介于 client 和 Anthropic 之间吗？ | Yes | 通过安全审查 |
| 每个 request 有合理的 `max_tokens` 吗？ | Yes | 通过成本审查 |
| App 有区分 `end_turn` 和 `max_tokens` 这些 stop reason 吗？ | Yes | 通过 UX 审查 |
| Per-user token usage 有 log 且有预算吗？ | Yes | 通过财务审查 |
| 事故发生时团队知道是哪一步坏掉吗？ | Yes | 通过事故审查 |

---

## 常见 PM 错误

1. **放任工程 ship client 直连 API** —— 即将发生的信息安全事故。这该在每个安全审查被挡下。
2. **不 own max_tokens** —— 留给工程 default，成本就会随使用线性扩张，没有产品输入。
3. **UX spec 里忽略 stop_reason** —— 答案悄悄截断，用户觉得 AI 很笨。
4. **PRD 里把 words 和 tokens 搞混** —— "200 字上限"不等于 `max_tokens=200`；token 可以是子字。
5. **期待 deterministic 输出** —— generation 步骤用受控随机性；同输入可能产不同输出，acceptance test 必须考虑这点。

> **关键洞察**
>
> 每一个高深的 Claude 模式 —— tool use、streaming、caching、agents —— 都是这同一个五步生命周期的变体。把这个模型装在脑里的 PM，拿到任何 AI feature 提案都能立刻问出对的问题：安全、成本、延迟、失败处理。跳过的 PM 只能猜，而且通常在最贵的那些上猜错。

---

## CCA 考试相关性

- **D1（Agentic Architecture）**：生命周期是所有 agentic 模式的基础。常考"X 发生在 request flow 的哪一步？"
- **D5（Enterprise Deployment）**：安全架构、token 预算、stop-reason 处理是生产部署必备。
- 注意："为什么 client 和 Anthropic 之间要有 server？"→ API key 安全性，永远是。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Claude request lifecycle 的五个步骤？ | Client 到 server → server 到 API → model 处理 → API 到 server → server 到 client。 |
| 为什么 PM 必须要求 client 和 Anthropic API 之间有 server？ | 为了保护 API key —— client 的 key 可被挖出来做未授权请求。 |
| Server 角色的餐厅比喻？ | 服务员 —— 不可协商的中介，介于客人和厨房之间。 |
| 每个 API request 必备的四个字段？ | API Key、Model、Messages、Max Tokens。 |
| Claude 内部处理的四个阶段？ | Tokenization、embedding、contextualization、generation。 |
| 哪个 response 字段告诉你答案是否被悄悄截断？ | `stop_reason` —— 如果是 `max_tokens` 就是被截断了。 |
| PM 在 request 层级拥有什么成本杠杆？ | `max_tokens` —— 直接限制单次请求的成本和延迟。 |
| 为什么 Claude 相同请求不总是 deterministic？ | Generation 步骤用概率和受控随机性的混合。 |
| `usage` 字段让 PM 能做什么？ | 计费、预算追踪、per-user 额度。 |
| PRD 里为什么要区分 words 和 tokens？ | Token 可能是子字、空白或符号 —— "200 words"不等于 `max_tokens=200`。 |
