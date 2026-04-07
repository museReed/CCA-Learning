# Implementing a Client — 工程深度解析

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | T2.2 實作 MCP client-server 通訊; T2.4 處理 tool discovery 和執行流程 |
| Source | introduction-to-model-context-protocol / 02-tools-and-inspector / Lesson 09 |

---

## 一句話摘要

建構 MCP client 端需要 SDK 的 Client 類別和 ClientSession，搭配兩個核心方法：`list_tools()` 用於探索、`call_tool()` 用於執行。

---

## Client 架構

MCP client 由兩個主要 SDK 類別組成：

```python
from mcp import ClientSession
from mcp.client import Client
```

**Client** — 管理連線生命週期（連接、斷開、傳輸管理）。

**ClientSession** — 提供與 MCP server 互動的方法（`list_tools()`、`call_tool()` 等）。

這兩個類別協同運作：Client 建立連線，ClientSession 使用該連線進行通訊。

```python
class MCPClient:
    def __init__(self):
        self.client = Client()
        self.session: ClientSession | None = None

    async def connect(self, server_script: str):
        """連接到 MCP server。"""
        server_params = StdioServerParameters(
            command="python",
            args=[server_script]
        )
        # 建立連線
        stdio_transport = await self.client.connect_stdio(server_params)
        self.session = ClientSession(*stdio_transport)
        await self.session.initialize()
```

> **Key Insight**
> `initialize()` 呼叫至關重要。它執行 MCP 握手，client 和 server 協商能力。沒有它，後續呼叫會失敗。

---

## 兩個核心方法

### list_tools() — Discovery

```python
async def discover_tools(self):
    """從 MCP server 探索可用的 tools。"""
    response = await self.session.list_tools()

    # response.tools 是 Tool 物件的列表
    for tool in response.tools:
        print(f"Tool: {tool.name}")
        print(f"  描述: {tool.description}")
        print(f"  Schema: {tool.inputSchema}")

    return response.tools
```

`list_tools()` 回傳 `ListToolsResult`，包含 tool 定義陣列。每個 tool 有：

- `name` — Tool 識別碼（例如 "read_doc_contents"）
- `description` — Tool 做什麼（來自 server 的 docstring）
- `inputSchema` — Tool 參數的 JSON schema

這就是你傳給 Claude 讓它知道有哪些 tools 可用的內容。

### call_tool() — Execution

```python
async def execute_tool(self, tool_name: str, tool_input: dict):
    """在 MCP server 上執行 tool。"""
    result = await self.session.call_tool(tool_name, tool_input)

    # result.content 包含 tool 輸出
    return result.content
```

`call_tool()` 接受兩個引數：

- `tool_name` — 要呼叫哪個 tool（字串）
- `tool_input` — tool 的引數（符合 inputSchema 的字典）

它回傳包含 tool 輸出的 `CallToolResult`。

> **Key Insight**
> tool_name 和 tool_input 通常直接來自 Claude 的 tool_use 回應。Claude 決定呼叫哪個 tool 及用什麼引數；你的 client 只是把該決定路由到 MCP server。

---

## 完整的 Client 端流程

以下是 client 如何在完整 agentic 迴圈中與 Claude 整合：

```python
import anthropic
from mcp import ClientSession

class AgenticMCPClient:
    def __init__(self):
        self.claude = anthropic.Anthropic()
        self.session: ClientSession = None  # 連接時設定

    async def handle_query(self, user_query: str) -> str:
        # 步驟 1：探索 tools
        tools_response = await self.session.list_tools()
        claude_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            }
            for tool in tools_response.tools
        ]

        # 步驟 2：發送查詢 + tools 給 Claude
        messages = [{"role": "user", "content": user_query}]
        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=claude_tools,
            messages=messages
        )

        # 步驟 3：檢查 Claude 是否要使用 tool
        if response.stop_reason == "tool_use":
            tool_block = next(
                b for b in response.content
                if b.type == "tool_use"
            )

            # 步驟 4：透過 MCP 執行 tool
            tool_result = await self.session.call_tool(
                tool_block.name,
                tool_block.input
            )

            # 步驟 5：把結果送回 Claude
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

五個關鍵步驟：

1. **探索** — `list_tools()` 取得可用 tools
2. **呈現** — Tool schema 與使用者查詢一起傳給 Claude
3. **決定** — Claude 回傳 `tool_use` 區塊（或直接回答）
4. **執行** — `call_tool()` 在 MCP server 上執行 tool
5. **解讀** — Claude 收到結果並生成最終回應

---

## 執行 Client

```bash
uv run mcp_client.py
```

`uv` 執行器處理依賴解析和虛擬環境管理。執行時，client：

1. 連接到指定的 MCP server
2. 探索可用 tools
3. 進入互動迴圈，使用者可以提問
4. 透過 MCP 路由 tool 呼叫，透過 Claude 路由回應

---

## Client 端的錯誤處理

```python
async def safe_call_tool(self, tool_name: str, tool_input: dict):
    try:
        result = await self.session.call_tool(tool_name, tool_input)
        if result.isError:
            return f"Tool 錯誤: {result.content}"
        return result.content
    except Exception as e:
        return f"MCP 通訊錯誤: {str(e)}"
```

關鍵錯誤場景：

- **Tool 找不到** — tool 名稱不符合任何已註冊的 tool
- **無效輸入** — tool_input 不符合預期 schema
- **Server 錯誤** — MCP server 遇到內部錯誤
- **傳輸錯誤** — 與 MCP server 的連線中斷

> **Key Insight**
> `call_tool()` 後一定要檢查 `result.isError`。成功的 MCP 往返仍可能包含 tool 層級的錯誤。傳輸成功了但 tool 執行失敗了。

---

## CCA 考試關聯性

本課完成 **Domain 2 (18%)** 的 client-server 全貌：

- **兩個 SDK 類別**：知道 Client 處理連線、ClientSession 處理通訊
- **兩個核心方法**：`list_tools()` 用於探索、`call_tool()` 用於執行
- **Agentic 迴圈**：理解從探索經 Claude 決策到最終回應的五步流程
- **`uv run`**：知道這是 MCP client 的典型執行方式
- **錯誤處理**：理解 `result.isError` 在傳輸成功時仍能捕獲 tool 層級錯誤

---

## Flashcards

| Front | Back |
|-------|------|
| 建構 MCP client 的兩個主要 SDK 類別是什麼？ | Client（管理連線生命週期）和 ClientSession（提供 list_tools 和 call_tool 方法）。 |
| `list_tools()` 回傳什麼？ | ListToolsResult，包含 tool 定義陣列，每個有 name、description 和 inputSchema。 |
| `call_tool()` 接受哪兩個引數？ | tool_name（識別要呼叫哪個 tool 的字串）和 tool_input（符合 tool inputSchema 的字典）。 |
| tool_name 和 tool_input 通常從哪來？ | 來自 Claude 的 tool_use 回應區塊。Claude 決定呼叫哪個 tool 及用什麼引數。 |
| `session.initialize()` 做什麼？ | 執行 MCP 握手，client 和 server 協商能力。在任何其他 MCP 呼叫之前必須執行。 |
| 完整 client 端 agentic 流程的五個步驟是什麼？ | 1) 探索 tools, 2) 呈現 tools + 查詢給 Claude, 3) Claude 決定 tool use, 4) 透過 MCP 執行 tool, 5) 送結果給 Claude 取得最終回應。 |
| 如何執行 MCP client？ | `uv run mcp_client.py` — uv 處理依賴解析和虛擬環境管理。 |
| 為什麼 call_tool() 後要檢查 `result.isError`？ | 成功的 MCP 傳輸往返仍可能包含 tool 層級錯誤。連線成功了但 tool 本身失敗了。 |
