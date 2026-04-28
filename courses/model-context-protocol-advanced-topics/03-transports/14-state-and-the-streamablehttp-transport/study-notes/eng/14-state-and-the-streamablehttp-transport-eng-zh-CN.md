# State and the StreamableHTTP Transport — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.1 (MCP transport 选择), 2.4 (远程 server 配置), 2.6 (水平扩展模式) |
| Source | model-context-protocol-advanced-topics / 03-transports / Lesson 14 |

---

## One-Liner

水平扩展产生协调问题 — 同一 client 的两个 SSE 连接可能命中不同 server instance，`stateless_http=true` 通过完全消除状态来解决此问题，代价是失去主要 MCP 功能。

---

![Scaling Tradeoff](../../visuals/scaling-tradeoff-zh-TW.svg)


## 扩展问题

当 MCP server 变得热门时，需要水平扩展 — 多个 server instance 在 load balancer 后面。这产生根本性的协调问题：

```
                    ┌─── Instance A
Client ──→ LB ─────┤
                    ├─── Instance B
                    └─── Instance C
```

回想 Lesson 13：client 维持**两个连接**：
1. **GET SSE**（持久，用于 server-initiated 消息）
2. **POST request**（每次 tool call）

Load balancer 可能将它们路由到**不同 instance**：

```
Client ── GET /sse ──→ LB ──→ Instance A  （primary SSE 在这）
Client ── POST /tool ──→ LB ──→ Instance B  （tool call 在这）
```

Instance B 处理 tool call，但 Instance A 持有 SSE 连接。Instance B 如何向 client 发送 progress 更新？

> 💡 **Key Insight**
> 让 SSE 在单一 server 上运作的双连接架构，在扩展时变成负担。Load balancer 不理解 MCP session 语义。

---

## 解决方案：`stateless_http=true`

终极手段：**消除所有状态**。启用后：

| 功能 | 状态 |
|------|------|
| Session ID | 停用 — 无追踪 |
| Server → Client request | 停用 — 无 CreateMessage、无 ListRoots |
| Sampling | 停用 |
| Progress notification | 停用 |
| Resource subscription | 停用 |
| Initialization handshake | **不需要** — 任何 instance 可处理任何请求 |

```python
# Stateless server — 不需要初始化
mcp_server = MCPServer(
    stateless_http=True,  # 每个请求独立
    json_response=False,  # 仍可 per-request streaming
)
```

### 关键好处

不需要初始化。任何 server instance 可以独立处理任何请求。Load balancer 直接 round-robin — 不需要 sticky session、不需要 session affinity。

---

## 解决方案：`json_response=true`

消除 streaming 的互补标志：

| `json_response=false`（默认） | `json_response=true` |
|-------------------------------|---------------------|
| Server 通过 SSE 流式传输结果 | Server 返回单一 JSON 回应 |
| Client 实时看到进度 | Client 等待完整结果 |
| 需要保持连接开启 | 标准 HTTP request-response |

---

## 决策矩阵

| 需求 | `stateless_http` | `json_response` | 结果 |
|------|-----------------|-----------------|------|
| 完整 MCP 功能，单一 server | `false` | `false` | 通过 SSE 使用所有功能 |
| 水平扩展，保留部分 streaming | `true` | `false` | Per-request streaming，无 server-initiated |
| 最大可扩展性，简单 API | `true` | `true` | 仅基本 request-response |
| 有 streaming 但需要 session | `false` | `false` | LB 需要 sticky session |

### 根本取舍

```
功能性 ◄─────────────────────► 可扩展性

完整 MCP          SSE workaround      Stateless         Stateless + JSON
（Stdio）        （单一 server）      （可扩展）        （最简单）
```

---

## 失去什么 vs 得到什么

### `stateless_http=true` 失去的

- 无 session ID
- 无 server → client request（CreateMessage、ListRoots）
- 无 sampling 能力
- 无 progress 报告
- 无 resource subscription

### `stateless_http=true` 得到的

- 不需要 initialization handshake
- 任何 instance 处理任何请求
- 标准 load balancer 即可运作（无需 sticky session）
- 更简单的 server 实现
- 更好的容错性（instance 故障不会丢失 session）

---

## CCA 考试重点

- **扩展题**：知道双连接模型与 load balancer 冲突 → `stateless_http` 是标准解决方案。
- **功能损失矩阵**：记住 `stateless_http=true` 确切停用什么 — 这是常考目标。
- **无需初始化**：Stateless 模式完全跳过三步 handshake。
- **标志组合**：两者都 `true` = 最简单的 MCP server（基本 HTTP request-response）。
- 考试哲学：**可扩展性与功能性在 MCP transport 设计中成反比**。

---

## Flashcards

| Front | Back |
|-------|------|
| StreamableHTTP 面临什么扩展问题？ | 来自同一 client 的两个连接（GET SSE + POST）可能命中 load balancer 后面的不同 server instance |
| `stateless_http=true` 如何解决扩展问题？ | 消除所有状态 — 无 session、无 SSE，任何 instance 独立处理任何请求 |
| `stateless_http=true` 停用哪五个功能？ | Session ID、server→client request、sampling、progress notification、resource subscription |
| Stateless 模式的关键好处是？ | 不需要初始化 — 任何 server instance 无需事先 handshake 即可处理任何请求 |
| `json_response=true` 做什么？ | 消除 streaming — server 返回单一最终 JSON 回应而非 SSE 事件 |
| 最简单的 MCP server 配置是？ | 两者都设为 `true` — 仅基本 HTTP request-response |
| 何时应该保持两个标志都为 false？ | 单一 server 部署且需要完整 MCP 功能（包括 SSE、sampling 和 progress）时 |
| 什么 load balancer 策略适用于 stateless MCP？ | Round-robin — 不需要 sticky session 或 session affinity |
