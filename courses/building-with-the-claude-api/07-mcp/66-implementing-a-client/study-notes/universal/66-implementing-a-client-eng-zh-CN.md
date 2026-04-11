# Implementing a Client — Engineering Deep Dive（简体中文）

| 项目 | 说明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（MCP primitives：client/server、list_tools、call_tool）、2.2（content block types）、1.2（agentic loop 集成） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 66 |

---

## One-Liner

MCP client 是对 MCP Python SDK `ClientSession` 的轻量封装，对外暴露两个核心方法 `list_tools()` 与 `call_tool()`，让应用程序可以发现并调用服务端 tools，而不必关心 transport、handshake 或资源清理。

---

## 为什么要自己写一个 Client class

真实项目中通常只会实作 **MCP client 或 MCP server 之一**，不会两边都写。本课程为了教学才两边都做。MCP client 有两层：

1. **`ClientSession`** — MCP Python SDK 提供的底层连接原语，负责协议 handshake、消息 framing、async 生命周期
2. **`MCPClient`** — 你自己写的 class，包裹在 `ClientSession` 外层：
   - 用 async context manager 管理 session 的启动与清理
   - 暴露好用的方法（`list_tools`、`call_tool`，之后还有 `read_resource`、`list_prompts`、`get_prompt`）
   - 把 transport 细节（stdio subprocess、command + args）隐藏起来

最关键的理由是 **资源清理**：`ClientSession` 需要 async teardown。包在 context manager 里，调用端就绝对不会忘记关 subprocess。

---

## Client 如何融入 Agent Loop

CLI 需要从 MCP server 获取两项能力：

1. 取得可用 tool 列表，转发给 Claude（让 Claude 知道自己能调用什么）
2. 当 Claude 发出 `tool_use` block 时，实际执行 tool（把结果喂回 agent loop）

```
┌────────────┐   list_tools()    ┌────────────┐
│ CLI / App  │ ────────────────▶ │ MCPClient  │
│            │ ◀──────────────── │            │
│            │     [tools]       └────────────┘
│            │                         │
│            │   ── call_tool() ──────▶│
│            │ ◀─── ToolResult ────────│
└────────────┘                         ▼
                                  MCP Server
                                  (subprocess)
```

MCP client 就是桥梁：左侧是应用逻辑，右侧是 MCP server，agent loop 把两端包起来。

---

## 两个核心方法

### `list_tools()`

```python
async def list_tools(self) -> list[types.Tool]:
    result = await self.session().list_tools()
    return result.tools
```

- 调用 session 内建的 `list_tools()`
- 返回 `types.Tool` 数组，每个对象含 `name`、`description`、`inputSchema`
- 应用程序会把它们转成 Anthropic API 所需格式，放进 `client.messages.create(..., tools=...)`

### `call_tool()`

```python
async def call_tool(
    self, tool_name: str, tool_input: dict
) -> types.CallToolResult | None:
    return await self.session().call_tool(tool_name, tool_input)
```

- 接收 Claude 在 `tool_use` block 中指定的 `name` 与 `input`
- 委派给 session 的 `call_tool()`，通过 MCP transport 发送请求并等待 server 响应
- 返回的 `CallToolResult.content` 会变成下一轮 API 调用里的 `tool_result` 内容

两个方法故意写得很薄——真正干活的是 SDK，你的 class 只负责提供稳定友好的接口。

---

## 直接测试 Client

同一个文件带有测试 harness，可以不经过 Claude 单独测试 client：

```python
async with MCPClient(
    command="uv", args=["run", "mcp_server.py"]
) as client:
    result = await client.list_tools()
    print(result)
```

跑起来应该会打印前几课定义的 `read_doc_contents` 与 `edit_document`。这是 smoke test——如果列表能拿回来，说明 handshake、transport、decoder 都正常。

---

## End-to-End 流程（用户提问时会发生什么）

1. **启动** — CLI 进入 `MCPClient` context manager，spawn `mcp_server.py` subprocess 并完成 MCP handshake
2. **Tool 发现** — CLI 调用 `client.list_tools()`，存起来或转为 Anthropic tool schema
3. **第一次调用 Claude** — 用户问题 + tool 定义送到 `client.messages.create()`
4. **Claude 发出 `tool_use`** — 例如 `read_doc_contents(doc_id="report.pdf")`
5. **Dispatch** — CLI 调用 `client.call_tool("read_doc_contents", {"doc_id": "report.pdf"})`
6. **Server 执行** — 返回 `CallToolResult`，里面包含文档内容
7. **第二次调用 Claude** — CLI 把 `tool_result` block（附带原本 `tool_use_id`）append 进 messages，再调一次 Claude
8. **最终答复** — Claude 生成用户看到的回答

这就是第 4 章讲的 tool use 循环——MCP 只是把「本地 Python function dispatch」替换成「经由协议调用 server」。

---

## Common Mistakes

1. **在 context 之外调用 `session()`** — `ClientSession` 必须在 `async with` 块内使用，否则 subprocess 会泄漏
2. **把原始 `CallToolResult` 直接回给 Claude** — 必须封装成 `tool_result` content block，并带上正确的 `tool_use_id`
3. **忘记传 subprocess command** — `MCPClient` 需要 `command` 和 `args`（如 `command="uv", args=["run", "mcp_server.py"]`），路径错就拿不到任何 tool
4. **把 `list_tools()` 当便宜操作** — 它是 async round trip，应该 per session 缓存，别每条用户消息都重调
5. **同步 / 异步混用** — MCP SDK 全 async，sync 代码在没有 event loop 的情况下会报错

> **Key Insight**
>
> MCP client 不是重写你的 agent loop——它是 **transport 替换**。原本调用本地 Python function 的地方，改成调用 `client.call_tool(...)` 即可。Agent loop、`tool_use` / `tool_result` 协议、Anthropic API 契约完全不变。MCP 的威力正来自这种可分离性：你的 server 可被任何 Claude 应用复用，而无需改动 agent loop。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：要知道 MCP client 是 `ClientSession` 的封装，核心方法是 `list_tools()` / `call_tool()`，用来替代本地 tool dispatch
- **D1（Agentic Architecture）**：agent loop 本身不因 MCP 改变，client 只是换了一种拿 tool、执行 tool 的方式
- 考题模式："MCP-based 应用中 tool 实际在哪里执行？" → 在 server 上，通过 client 的 `call_tool()` 触发

---

## Flashcards

| Front | Back |
|-------|------|
| MCP client 分哪两层？ | `ClientSession`（SDK 提供的 transport/handshake 原语）+ 自写的 `MCPClient` class（负责生命周期与友好 API） |
| 为什么要把 `ClientSession` 包进自己的 class？ | 用 context manager 保证 async 清理，并提供稳定友好的对外接口 |
| MCP client 至少要实现哪两个方法？ | `list_tools()` 与 `call_tool(tool_name, tool_input)` |
| `list_tools()` 返回什么？ | `types.Tool` 数组，含 `name`、`description`、`inputSchema`，可直接转发给 Claude |
| `call_tool()` 的参数与返回？ | 参数：`tool_name` 与 `tool_input` dict；返回 `CallToolResult | None` |
| 如何单独测试 client？ | 直接运行该文件：`async with MCPClient(command="uv", args=["run", "mcp_server.py"]) as client: await client.list_tools()` |
| MCP 改变了 agent loop 吗？ | 没有，只有 tool dispatch 那一步换成了 `client.call_tool(...)`，loop、stop_reason、tool_result 协议完全不变 |
| 课程里使用的 command / args 组合？ | `command="uv"`、`args=["run", "mcp_server.py"]`，通过 stdio spawn server subprocess |
