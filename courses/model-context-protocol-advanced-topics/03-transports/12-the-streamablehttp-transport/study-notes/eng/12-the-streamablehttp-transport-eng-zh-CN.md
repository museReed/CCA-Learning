# The StreamableHTTP Transport — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.1 (MCP transport 选择), 2.4 (远程 server 配置) |
| Source | model-context-protocol-advanced-topics / 03-transports / Lesson 12 |

---

## One-Liner

StreamableHTTP 通过 HTTP 实现远程 MCP server，但 HTTP 的 request-response 模型意味着 server 无法主动发起通信 — 以完整 MCP 能力换取远程托管。

---

## 为什么需要 StreamableHTTP

Stdio 要求同机器部署。对于服务多用户或在云端运行的 production 系统，需要 HTTP。StreamableHTTP 将 MCP 桥接到 Web — 但 HTTP 有一个根本限制：

**HTTP 只能由 client 发起。** Server 只能回应请求，无法主动向 client 发送消息。

---

## 两个关键配置标志

StreamableHTTP 的行为由 server 上的两个 boolean 设置控制：

| 标志 | 默认值 | 用途 |
|------|--------|------|
| `stateless_http` | `false` | 设为 `true` 时停用 session 追踪 |
| `json_response` | `false` | 设为 `true` 时返回纯 JSON 而非 SSE stream |

两者默认为 `false`（最少限制）。启用任一个都会**移除能力**。

```python
# Server 配置示例
mcp_server = MCPServer(
    stateless_http=False,  # 默认：启用 session
    json_response=False,   # 默认：启用 SSE streaming
)
```

> 💡 **Key Insight**
> 把这些标志想成**限制开关**。启用越多，server 越简单 — 但可用的 MCP 功能越少。

---

## HTTP 破坏了什么

核心限制：**server 无法通过纯 HTTP 主动向 client 发起请求**。

### 受影响的 Server-Initiated 功能

| 功能 | 作用 | 无法使用时的影响 |
|------|------|----------------|
| `CreateMessage`（Sampling） | Server 请求 LLM 生成文字 | 无 server 端 AI 调用 |
| `ListRoots` | Server 查询 client 的 workspace | 无文件系统感知能力 |
| Progress Notification | Server 报告任务进度 | Client 对长时间操作无能见度 |
| Logging Notification | Server 发送日志消息 | 无实时调试信息 |

### 仍然可用的功能

所有 **client-initiated** 功能正常运作：

- `tools/call` — client 调用 server 工具
- `resources/read` — client 读取 server 资源
- `prompts/get` — client 获取 prompt 模板

---

## 能力光谱

```
完整 MCP（Stdio）
    │
    ▼
StreamableHTTP（默认值）      ← SSE workaround 部分恢复 server→client
    │
    ▼
StreamableHTTP + stateless   ← 无 session，无任何 server-initiated
    │
    ▼
StreamableHTTP + json_response ← 完全无 streaming
    │
    ▼
两个标志都启用               ← 最大限制，最简单的 server
```

每往下一步都是**用功能换取简洁/可扩展性**。

---

## 何时使用 StreamableHTTP

| 场景 | 建议配置 |
|------|---------|
| 远程 server，需要大部分功能 | 默认值（两者都 `false`） |
| 需要水平扩展 | `stateless_http=true` |
| 简单的 request-response API | 两者都 `true` |
| 需要 sampling/progress | 只能用默认值 — 标志会破坏这些功能 |
| 本地开发 | 改用 Stdio |

---

## CCA 考试重点

- **Transport 取舍题**：StreamableHTTP = 远程托管、能力降低。要知道确切哪些功能会坏掉。
- **标志行为**：`stateless_http` 和 `json_response` 都默认为 `false`。启用是限制而非增强。
- **Server-initiated vs client-initiated**：HTTP 只影响 server-initiated 模式。Client→server 永远正常。
- 考试哲学：**远程访问有代价** — 每个网络限制都会移除 MCP 功能。

---

## Flashcards

| Front | Back |
|-------|------|
| HTTP 对 MCP 的根本限制是什么？ | HTTP 只能由 client 发起 — server 无法主动向 client 发送消息 |
| StreamableHTTP 的两个配置标志是？ | `stateless_http` 和 `json_response`，两者默认为 `false` |
| 启用 `stateless_http` 会怎样？ | 停用 session 追踪 — 无 server-initiated request、无 sampling、无 progress notification |
| `json_response=true` 的效果？ | 返回纯 JSON 而非 SSE stream — 无 streaming，只有最终结果 |
| 列举两个被 HTTP 破坏的 server-initiated 功能 | CreateMessage（sampling）和 Progress Notification |
| 哪些 client-initiated 功能在 HTTP 上仍然正常？ | tools/call、resources/read、prompts/get — 所有 client→server 请求正常运作 |
| StreamableHTTP 的能力取舍是什么？ | 用远程托管能力换取 server-initiated MCP 功能的减少/丧失 |
| 何时应该使用 StreamableHTTP 默认值（两者都 false）？ | 需要远程托管但仍想要最大 MCP 能力（包括 SSE workaround）时 |
