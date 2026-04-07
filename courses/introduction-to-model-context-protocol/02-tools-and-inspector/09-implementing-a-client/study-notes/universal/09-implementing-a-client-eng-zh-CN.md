# Implementing a Client — 工程深度解析

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | T2.2 实现 MCP client-server 通信; T2.4 处理 tool discovery 和执行流程 |
| Source | introduction-to-model-context-protocol / 02-tools-and-inspector / Lesson 09 |

---

## 一句话摘要

构建 MCP client 端需要 SDK 的 Client 类和 ClientSession，搭配两个核心方法：`list_tools()` 用于发现、`call_tool()` 用于执行。

---

## Client 架构

MCP client 由两个主要 SDK 类组成：

```python
from mcp import ClientSession
from mcp.client import Client
```

**Client** — 管理连接生命周期（连接、断开、传输管理）。

**ClientSession** — 提供与 MCP server 交互的方法（`list_tools()`、`call_tool()` 等）。

这两个类协同运作：Client 建立连接，ClientSession 使用该连接进行通信。

```python
class MCPClient:
    def __init__(self):
        self.client = Client()
        self.session: ClientSession | None = None

    async def connect(self, server_script: str):
        """连接到 MCP server。"""
        server_params = StdioServerParameters(
            command="python",
            args=[server_script]
        )
        # 建立连接
        stdio_transport = await self.client.connect_stdio(server_params)
        self.session = ClientSession(*stdio_transport)
        await self.session.initialize()
```

> **Key Insight**
> `initialize()` 调用至关重要。它执行 MCP 握手，client 和 server 协商能力。没有它，后续调用会失败。

---

## 两个核心方法

### list_tools() — Discovery

```python
async def discover_tools(self):
    """从 MCP server 发现可用的 tools。"""
    response = await self.session.list_tools()

    # response.tools 是 Tool 对象的列表
    for tool in response.tools:
        print(f"Tool: {tool.name}")
        print(f"  描述: {tool.description}")
        print(f"  Schema: {tool.inputSchema}")

    return response.tools
```

`list_tools()` 返回 `ListToolsResult`，包含 tool 定义数组。每个 tool 有：

- `name` — Tool 标识符（例如 "read_doc_contents"）
- `description` — Tool 做什么（来自 server 的 docstring）
- `inputSchema` — Tool 参数的 JSON schema

这就是你传给 Claude 让它知道有哪些 tools 可用的内容。

### call_tool() — Execution

```python
async def execute_tool(self, tool_name: str, tool_input: dict):
    """在 MCP server 上执行 tool。"""
    result = await self.session.call_tool(tool_name, tool_input)

    # result.content 包含 tool 输出
    return result.content
```

`call_tool()` 接受两个参数：

- `tool_name` — 要调用哪个 tool（字符串）
- `tool_input` — tool 的参数（符合 inputSchema 的字典）

它返回包含 tool 输出的 `CallToolResult`。

> **Key Insight**
> tool_name 和 tool_input 通常直接来自 Claude 的 tool_use 响应。Claude 决定调用哪个 tool 及用什么参数；你的 client 只是把该决定路由到 MCP server。

---

## 完整的 Client 端流程

以下是 client 如何在完整 agentic 循环中与 Claude 集成：

```python
import anthropic
from mcp import ClientSession

class AgenticMCPClient:
    def __init__(self):
        self.claude = anthropic.Anthropic()
        self.session: ClientSession = None  # 连接时设定

    async def handle_query(self, user_query: str) -> str:
        # 步骤 1：发现 tools
        tools_response = await self.session.list_tools()
        claude_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            }
            for tool in tools_response.tools
        ]

        # 步骤 2：发送查询 + tools 给 Claude
        messages = [{"role": "user", "content": user_query}]
        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=claude_tools,
            messages=messages
        )

        # 步骤 3：检查 Claude 是否要使用 tool
        if response.stop_reason == "tool_use":
            tool_block = next(
                b for b in response.content
                if b.type == "tool_use"
            )

            # 步骤 4：通过 MCP 执行 tool
            tool_result = await self.session.call_tool(
                tool_block.name,
                tool_block.input
            )

            # 步骤 5：把结果送回 Claude
            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_block.id,
                    "content": str(tool_result.content)
                }]
            })

            final_response = self.claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                tools=claude_tools,
                messages=messages
            )
            return final_response.content[0].text

        return response.content[0].text
```

五个关键步骤：

1. **发现** — `list_tools()` 获取可用 tools
2. **呈现** — Tool schema 与用户查询一起传给 Claude
3. **决定** — Claude 返回 `tool_use` 块（或直接回答）
4. **执行** — `call_tool()` 在 MCP server 上执行 tool
5. **解读** — Claude 收到结果并生成最终响应

---

## 运行 Client

```bash
uv run mcp_client.py
```

`uv` 运行器处理依赖解析和虚拟环境管理。运行时，client：

1. 连接到指定的 MCP server
2. 发现可用 tools
3. 进入交互循环，用户可以提问
4. 通过 MCP 路由 tool 调用，通过 Claude 路由响应

---

## Client 端的错误处理

```python
async def safe_call_tool(self, tool_name: str, tool_input: dict):
    try:
        result = await self.session.call_tool(tool_name, tool_input)
        if result.isError:
            return f"Tool 错误: {result.content}"
        return result.content
    except Exception as e:
        return f"MCP 通信错误: {str(e)}"
```

关键错误场景：

- **Tool 找不到** — tool 名称不匹配任何已注册的 tool
- **无效输入** — tool_input 不符合预期 schema
- **Server 错误** — MCP server 遇到内部错误
- **传输错误** — 与 MCP server 的连接中断

> **Key Insight**
> `call_tool()` 后一定要检查 `result.isError`。成功的 MCP 往返仍可能包含 tool 级别的错误。传输成功了但 tool 执行失败了。

---

## CCA 考试关联性

本课完成 **Domain 2 (18%)** 的 client-server 全貌：

- **两个 SDK 类**：知道 Client 处理连接、ClientSession 处理通信
- **两个核心方法**：`list_tools()` 用于发现、`call_tool()` 用于执行
- **Agentic 循环**：理解从发现经 Claude 决策到最终响应的五步流程
- **`uv run`**：知道这是 MCP client 的典型执行方式
- **错误处理**：理解 `result.isError` 在传输成功时仍能捕获 tool 级别错误

---

## Flashcards

| Front | Back |
|-------|------|
| 构建 MCP client 的两个主要 SDK 类是什么？ | Client（管理连接生命周期）和 ClientSession（提供 list_tools 和 call_tool 方法）。 |
| `list_tools()` 返回什么？ | ListToolsResult，包含 tool 定义数组，每个有 name、description 和 inputSchema。 |
| `call_tool()` 接受哪两个参数？ | tool_name（标识要调用哪个 tool 的字符串）和 tool_input（符合 tool inputSchema 的字典）。 |
| tool_name 和 tool_input 通常从哪来？ | 来自 Claude 的 tool_use 响应块。Claude 决定调用哪个 tool 及用什么参数。 |
| `session.initialize()` 做什么？ | 执行 MCP 握手，client 和 server 协商能力。在任何其他 MCP 调用之前必须执行。 |
| 完整 client 端 agentic 流程的五个步骤是什么？ | 1) 发现 tools, 2) 呈现 tools + 查询给 Claude, 3) Claude 决定 tool use, 4) 通过 MCP 执行 tool, 5) 送结果给 Claude 获取最终响应。 |
| 如何运行 MCP client？ | `uv run mcp_client.py` — uv 处理依赖解析和虚拟环境管理。 |
| 为什么 call_tool() 后要检查 `result.isError`？ | 成功的 MCP 传输往返仍可能包含 tool 级别错误。连接成功了但 tool 本身失败了。 |
