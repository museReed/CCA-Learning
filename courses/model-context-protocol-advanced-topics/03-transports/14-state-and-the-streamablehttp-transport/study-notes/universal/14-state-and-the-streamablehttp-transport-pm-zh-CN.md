# State and the StreamableHTTP Transport — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.1 (MCP transport 选择), 2.4 (远程 server 配置), 2.6 (水平扩展模式) |
| Source | model-context-protocol-advanced-topics / 03-transports / Lesson 14 |

---

## One-Liner

当你的 MCP server 变得热门需要扩展时，你面临选择：用复杂基础架构保留丰富功能，或走 stateless 路线简单扩展但失去进度追踪和 AI sampling 等关键能力。

---

![Scaling Tradeoff](../../visuals/scaling-tradeoff-zh-TW.svg)


## 连锁餐厅类比

想象你的 MCP server 是一家餐厅：

- **单一店面**（一个 server instance）：服务生记得你的点餐，可以查看餐点进度，还会主动推荐甜点。完整服务。
- **连锁扩张**（水平扩展）：你在调度员后面开了多家分店。客人打电话到 A 店预约，但餐点订单被送到 B 店。B 店完全不知道预约的事。

这就是扩展 MCP server 的**协调问题**。

---

## 为什么这对你的产品很重要

随着用户增长，单一 MCP server instance 无法承受负载。你需要在 load balancer 后面放多个 instance。但 MCP 的 session 模型假设只有一个 server：

| Client 做什么 | 哪个 Instance 处理 |
|--------------|-------------------|
| 开启 SSE 连接（持久） | Instance A |
| 发起 tool call（POST） | Instance B（随机！） |
| 期望收到 progress 更新 | Instance A 有 SSE... 但 B 有任务 |

Load balancer 不理解 MCP session。它只是分配请求。

> 💡 **Key Insight**
> 这不是 bug — 而是 stateful protocol（带 session 的 MCP）和 stateless 基础架构（HTTP load balancer）之间的根本张力。每个构建 production MCP server 的团队都会碰到这面墙。

---

## 两种扩展策略

### 策略 1：Sticky Session（保留功能）

强制 load balancer 永远将同一 client 路由到同一 server instance。

| 优点 | 缺点 |
|------|------|
| 保留所有 MCP 功能 | 负载分配不均 |
| 不需要改 code | 每个 client 有单点故障 |
| 熟悉的模式 | 较难自动扩展 |

### 策略 2：走 Stateless（轻松扩展）

启用 `stateless_http=true` — 每个请求独立。

| 优点 | 缺点 |
|------|------|
| 任何 instance 处理任何请求 | 无进度追踪 |
| 标准 load balancing 可用 | 无 server-initiated 功能 |
| 轻松自动扩展 | 无 sampling（server 不能调用 AI） |
| 更好的容错性 | 无初始化 = 无 capability 协商 |

---

## 利益相关者功能影响摘要

| 功能 | 有状态 | Stateless | 商业影响 |
|------|--------|-----------|---------|
| 进度条 | 可用 | 失去 | 用户在长时间操作时盲等 |
| Sampling（AI 推理） | 可用 | 失去 | Server 无法让 AI 协助决策 |
| 批准流程 | 可用 | 失去 | 无 server 端的 human-in-the-loop |
| 基本 tool call | 可用 | 可用 | 核心功能保留 |
| Resource read | 可用 | 可用 | 数据访问保留 |
| 自动扩展 | 复杂 | 简单 | 基础架构团队可用标准工具 |
| 容错性 | 差（session 丢失） | 优秀（无状态可丢失） | Instance 故障时更好的正常运行时间 |

---

## 何时选择哪种方案

| 场景 | 建议方案 |
|------|---------|
| < 100 同时用户 | 单一 server，两个标志都 false（完整功能） |
| 100-10K 用户，功能重要 | Sticky session（保留状态） |
| 10K+ 用户，基本工具访问 | Stateless 模式 |
| 简单 API 集成 | Stateless + JSON response |
| Prototype/MVP | 单一 server，所有功能 |

---

## `json_response` 标志（额外简化）

在 stateless 之上，还可以启用 `json_response=true`：

| 不启用（默认） | 启用 `json_response=true` |
|--------------|--------------------------|
| 结果实时流式传输 | 最后一次返回 |
| 用户看到部分进度 | 用户等待，然后一次获取全部 |
| 更复杂的基础架构 | 标准 REST API 行为 |

两个标志都开 = 最简单的 MCP server。本质上就是带 MCP 消息格式的 REST API。

---

## CCA 考试重点

- **扩展情境题**：「Load balancer 后面的 MCP server」→ 双连接问题 → stateless 是典型答案。
- **取舍分析**：知道 `stateless_http=true` 确切失去什么 — 五个功能停用。
- **无需初始化**：Stateless 模式跳过 handshake — 任何 instance、任何请求、无需设置。
- **标志组合**：两者都 true = 最简单的 server。考试可能问「最大可扩展性用哪个配置？」
- 考试哲学：**MCP transport 设计中，扩展上去 = 功能下来**。

---

## Flashcards

| Front | Back |
|-------|------|
| MCP 面临什么扩展问题？ | 来自同一 client 的两个连接（SSE + POST）可能命中 load balancer 后面的不同 server instance |
| MCP 水平扩展的标准解决方案是？ | `stateless_http=true` — 消除 session 状态，让任何 instance 处理任何请求 |
| 走 stateless 后用户失去什么？ | 进度条、sampling、server 发起的批准流程、resource subscription |
| 走 stateless 后用户保留什么？ | 基本 tool call 和 resource read — 所有 client-initiated 功能 |
| Stateless 提供什么基础架构好处？ | 标准 round-robin load balancing、轻松自动扩展、更好的容错性 |
| `json_response=true` 在 stateless 之上加了什么？ | 消除 streaming — 只有最终 JSON 回应，行为像标准 REST API |
| PM 何时应选 sticky session 而非 stateless？ | 当产品需要进度追踪、sampling 或批准流程，且用户数量可控时 |
| 最简单的 MCP server 配置是什么？ | 两者都设为 `true` — 带 MCP 消息格式的基本 HTTP request-response |
