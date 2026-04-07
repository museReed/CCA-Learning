# StreamableHTTP In Depth — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.1 (MCP transport 选择), 2.4 (远程 server 配置), 2.5 (SSE streaming 模式) |
| Source | model-context-protocol-advanced-topics / 03-transports / Lesson 13 |

---

## One-Liner

SSE 就像给 server 一支对讲机回 client — 一个 workaround，部分恢复了 HTTP 通常阻挡的「server 可以先开口」的能力。

---

![Streamable Http Sse](../../visuals/streamable-http-sse-zh-TW.svg)


## 对讲机类比

回想 Lesson 12 的服务柜台：
- HTTP = 柜台人员被固定在柜台，只能回应来访者
- **SSE** = 柜台人员拿到一支对讲机。访客留下一个无线电频道，柜台人员随时可以推送更新

但有个关键：server 拿到**两个对讲机频道**，而非一个。

---

## 两个频道，两个用途

### 频道 1：通用广播（Primary SSE）

- 全程开启，持续整个 session
- Server 推送**通用公告**：「我需要你批准某件事」或「你的 workspace 有哪些文件？」
- 商业类比：办公室广播系统

### 频道 2：任务专属更新（Tool SSE）

- 特定任务开始时开启，完成时关闭
- Server 推送**任务进度**：「完成 50%」、「找到 3 个结果」、「这是最终答案」
- 商业类比：特定项目会议的专线电话

```
通用广播（一直开着）
├── 「我需要批准这个动作」
├── 「你的 workspace 有哪些文件？」
└── （持续开启...）

任务频道 #1（tool call A）
├── 「处理中... 25%」
├── 「处理中... 75%」
├── 「这是结果」
└── （自动关闭）

任务频道 #2（tool call B）
├── 「开始分析...」
├── 「完成 — 这是你的报告」
└── （自动关闭）
```

> 💡 **Key Insight**
> 这种双频道设计是远程 MCP server 能同时显示个别任务进度条 AND 处理批准请求的原因。没有 SSE，HTTP 上两者都不可能。

---

## 对产品功能的意义

| 功能 | 需要哪个频道 | 有 SSE 能用吗？ |
|------|------------|---------------|
| Tool call 的进度条 | Tool SSE | 可以 |
| 实时 log streaming | Tool SSE | 可以 |
| Server 发起的批准流程 | Primary SSE | 可以 |
| Server 端 AI 推理（sampling） | Primary SSE | 可以 |
| 基本 tool call + 回应 | 都不需要（纯 HTTP） | 永远可以 |

### 建设成本

SSE 需要：
1. **Session ID** 系统（server 必须追踪 client）
2. 持久的 **GET 连接**（client 保持一个频道开启）
3. 正确的**消息路由**（server 将正确消息送到正确频道）

这比基本 HTTP 有更多基础架构复杂度。

---

## 配置标志如何杀死 SSE

| 标志 | 什么会死 | 产品影响 |
|------|---------|---------|
| `stateless_http=true` | Primary SSE 频道（无 session） | 无批准流程、无 sampling — server 变成「只能被问」 |
| `json_response=true` | 所有 SSE 频道（无 streaming） | 无进度条、无实时 log — 用户只能等最终结果 |
| 两者都启用 | 所有 SSE 相关功能 | 回到基本 HTTP：问问题、得答案。就这样。 |

---

## PM 决策：SSE 值得增加的复杂度吗？

| 如果你的产品需要... | 需要 SSE？ | 复杂度成本 |
|-------------------|----------|----------|
| 长时间操作的进度指示器 | 需要 | 中等 — 需要 session 管理 |
| Server 发起的人工批准 | 需要 | 中等 — 需要 primary SSE 频道 |
| 简单 tool call 加即时结果 | 不需要 | 保持简单，跳过 SSE |
| 结果的实时流式传输 | 需要 | 中等 — tool SSE 频道 |
| 最大可扩展性 | 不需要 — SSE 让扩展更难 | 考虑 stateless 模式 |

---

## CCA 考试重点

- **架构题**：知道两种 SSE 频道类型及其用途。Primary = server-initiated。Tool = per-call progress。
- **消息路由**：「Progress notification 去哪里？」→ Tool SSE。「Sampling request 去哪里？」→ Primary SSE。
- **标志影响**：`stateless_http` 杀死 primary SSE。`json_response` 杀死所有 SSE。两者 = 完全没有 SSE。
- **取舍框架**：SSE 部分恢复 server→client 能力。它是 workaround，不是完整解决方案。

---

## Flashcards

| Front | Back |
|-------|------|
| SSE 在 MCP 的背景下是什么？ | 一个 workaround，给 server 一个持久频道通过 HTTP 向 client 推送消息 |
| 两种 SSE 频道类型是？ | Primary SSE（通用、持久、server-initiated 消息）和 Tool SSE（per-call、暂时、progress/结果） |
| Primary SSE 支持什么商业功能？ | Server 发起的批准流程和 sampling — server 可以向 client 请求输入 |
| Tool SSE 支持什么商业功能？ | 个别 tool call 的进度条和实时 log |
| Session ID 的用途是？ | 将持久 GET SSE 连接与同一 client 的 POST 请求链接起来 |
| 哪个标志杀死 Primary SSE 频道？ | `stateless_http=true` — 无 session 代表无持久 server→client 频道 |
| 哪个标志杀死所有 SSE streaming？ | `json_response=true` — 只返回最终 JSON，完全无 streaming |
| SSE 是 server→client 通信的完整解决方案吗？ | 不是 — 它是部分 workaround。完整的双向通信只存在于 Stdio transport |
