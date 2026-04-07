# JSON Message Types — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.4 (client-server communication patterns), 2.6 (MCP protocol specification) |
| Source | model-context-protocol-advanced-topics / 02-roots-and-messages / Lesson 10 |

---

## One-Liner

MCP 通信使用两种 JSON 消息 — 对话（request-response）和公告（notification）— 在一个 client 和 server 都能主动开口的双向协议中。

---

![Message Types](../../visuals/message-types-zh-TW.svg)


## 心智模型：对讲机 vs. 广播器

| 消息类型 | 类比 | 行为 |
|---------|------|------|
| **Request-Result** | 对讲机对话 | 「收到吗？」...「收到，信息如下」 |
| **Notification** | 广播器公告 | 「注意：进度 50%」（不需回应） |

关键差异：对讲机消息等待回复；广播器公告不等。

---

## PM 为什么需要理解消息类型

你不需要读 JSON，但需要理解其影响：

### 1. 错误处理需求

- **Request-Result**：如果响应永远不来，产品必须处理超时和重试
- **Notification**：如果丢失，不会坏 — 但用户错过状态更新

这影响你可靠性的验收标准。

### 2. 产品架构决策

- 知道 MCP 是 **双向的** 意味着 server 不只是被动的 tool 提供者 — 它可以主动向 client 请求（如 sampling）
- 这开启了简单 request-response API 无法支持的产品可能性

### 3. Transport 选择

不同部署环境支持不同 transport。理解消息类型帮助评估哪个 transport 适合你的产品。

---

## 两类消息

### 类别 1：Request-Result（对话）

有人问问题，有人回答。

| 谁问 | 问什么 | 谁答 |
|------|--------|------|
| Client | 「执行这个 tool」（CallTool） | Server |
| Client | 「你有哪些 tools？」（ListTools） | Server |
| Client | 「给我这个 resource」（ReadResource） | Server |
| Client | 「让我们连线」（Initialize） | Server |
| Server | 「请帮我调用 Claude」（CreateMessage — sampling） | Client |
| Server | 「我可以访问哪些目录？」（ListRoots） | Client |

注意 **两端都能提问**。这就是 MCP 双向的原因。

### 类别 2：Notification（公告）

有人分享信息，不期望回应。

| 谁公告 | 说什么 |
|--------|--------|
| Server | 「进度：50% 完成」 |
| Server | 「Log：搜索数据库中...」 |
| Server | 「我的 tool 清单已变更」 |
| Server | 「某个 resource 已更新」 |
| Client | 「我的 root 目录已变更」 |

---

## 双向：两端都能说话

这是关键的架构洞察。MCP 不像 web API 只有 client 发起：

| 传统 API | MCP 协议 |
|---------|----------|
| Client 发送 request | Client 发送 request |
| Server 响应 | Server 响应 |
| Server 无法发起 | **Server 可以发起**（sampling、root 查询） |
| 单向关系 | **Peer-to-peer 关系** |

> **Key Insight**
> MCP 是双向道路。作为 PM，这意味着你可以设计 server 主动请求东西的产品功能 — 如通过 sampling 请 client 摘要数据。这是 REST API 原生不支持的能力。

---

## 规格用 TypeScript 撰写

官方 MCP 规格在 GitHub 上，用 TypeScript 撰写。PM 要点：

- TypeScript 用于 **描述数据结构**（如 schema），非必要语言
- Server 和 client 可用 **任何语言** 构建（Python, Go, JavaScript, Rust）
- 规格是消息长什么样的 **source of truth**
- 工程师辩论「这个消息有哪些字段？」时 — 规格就是答案

---

## 每种消息类型的产品影响

| 消息类型 | 产品影响 | PM 关注点 |
|---------|---------|----------|
| CallToolRequest/Result | 核心 tool 执行 | 必须定义超时和错误状态 |
| InitializeRequest/Result | 连接设置 | 预先定义支持的 capabilities |
| CreateMessageRequest/Result | Sampling（server 使用 AI） | 成本转移到 client — 定价影响 |
| ProgressNotification | 长时间操作的 UX | 必须设计加载状态 |
| LoggingNotification | 调试和监控 | 必须定义 log 保留策略 |
| ToolListChangedNotification | 动态 tool 发现 | UI 必须处理 tool 清单更新 |

---

## 常见考试情境

### 情境：Transport 中消息丢失

问：「一个 progress notification 在传输中丢失。会发生什么？」
答：不会坏 — 用户错过一次状态更新但 tool 继续运作。Notification 是 fire-and-forget。

问：「一个 CallToolResult 在传输中丢失。会发生什么？」
答：Client 超时且必须重试。Request-Result 配对需要响应 — 缺少 result 就是失败。

这个区别经常被考。

---

## CCA Exam Relevance

- **D2 Task 2.4**：Communication patterns — 知道两类消息和每端发送什么
- **D2 Task 2.6**：Protocol specification — 知道它用 TypeScript 做类型描述
- 关键区别：Request 有 `id` 字段，Notification 没有
- 知道 MCP 是双向的 — server 可以发起 request（sampling、list_roots）
- 考试哲学：**Protocol literacy** — 理解消息类型影响错误处理和架构

---

## Flashcards

| Front | Back |
|-------|------|
| MCP 消息分为哪两类？ | Request-Result 配对（期望响应）和 Notification（fire-and-forget） |
| 协议中 Request 和 Notification 怎么区分？ | Request 有 `id` 字段且期望响应；Notification 无 `id` 且不期望回应 |
| MCP 是只有 client 发起的协议吗？ | 不是 — 它是双向的；client 和 server 都能发起 request |
| MCP 规格用什么撰写？ | TypeScript — 用于类型描述，非必要的实现语言 |
| Notification 丢失会怎样？ | 不会坏 — 接收方错过信息性更新但功能继续 |
| Request Result 丢失会怎样？ | 发送方必须处理超时并可能重试 — 这是失败情境 |
| 举一个 server 发起 request 的例子？ | CreateMessageRequest（sampling）— server 请 client 调用 Claude |
| 为什么 transport 选择对 MCP 很重要？ | 所有 transport 必须支持双向通信，因为两端都能发起消息 |
