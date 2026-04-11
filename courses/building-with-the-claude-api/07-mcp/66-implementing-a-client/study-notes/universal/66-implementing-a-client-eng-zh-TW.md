# Implementing a Client — Engineering Deep Dive（繁體中文）

| 項目 | 說明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（MCP primitives：client/server、list_tools、call_tool）、2.2（content block types）、1.2（agentic loop 整合） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 66 |

---

## One-Liner

MCP client 是 MCP Python SDK `ClientSession` 的薄封裝，對外暴露兩個關鍵方法 `list_tools()` 與 `call_tool()`，讓應用程式可以探索並呼叫 server 端的 tools，不必操心 transport、handshake 或資源清理。

---

## 為什麼要自己寫一個 Client class

真實專案中你通常只會實作 **MCP client 或 MCP server 其中一邊**，不會兩邊都寫。本課程為了教學才兩邊都做。MCP client 有兩層：

1. **`ClientSession`** — MCP Python SDK 提供的底層連線物件，負責協議 handshake、訊息 framing、async 生命週期。
2. **`MCPClient`** — 你自己寫的 class，包在 `ClientSession` 外面：
   - 用 async context manager 管理 session 的啟動與清理
   - 提供好用的方法（`list_tools`、`call_tool`，以及後續的 `read_resource`、`list_prompts`、`get_prompt`）
   - 把 transport 細節（stdio subprocess、command + args）藏起來

最關鍵的理由是 **資源清理**：`ClientSession` 需要 async teardown。包在 context manager 裡面，呼叫端就絕對不會忘記關 subprocess。

---

## Client 如何嵌入 Agent Loop

CLI 需要從 MCP server 拿到兩個能力：

1. 取得可用 tool 清單，轉發給 Claude（讓 Claude 知道自己可以呼叫什麼）
2. 當 Claude 發出 `tool_use` block 時，實際執行 tool（把結果喂回 agent loop）

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

MCP client 就是橋樑：左邊是應用邏輯，右邊是 MCP server，agent loop 把兩端包起來。

---

## 兩個核心方法

### `list_tools()`

```python
async def list_tools(self) -> list[types.Tool]:
    result = await self.session().list_tools()
    return result.tools
```

- 呼叫 session 內建的 `list_tools()`
- 回傳一個 `types.Tool` 陣列，每個物件包含 `name`、`description`、`inputSchema`
- 應用程式會把這些 tool 轉成 Anthropic API 所需格式，塞進 `client.messages.create(..., tools=...)`

### `call_tool()`

```python
async def call_tool(
    self, tool_name: str, tool_input: dict
) -> types.CallToolResult | None:
    return await self.session().call_tool(tool_name, tool_input)
```

- 接收 Claude 在 `tool_use` block 中指定的 `name` 與 `input`
- 委派給 session 的 `call_tool()`，透過 MCP transport 送出請求並等 server 回應
- 回傳的 `CallToolResult.content` 會變成下一輪 API 呼叫的 `tool_result` 內容

兩個方法故意寫得很薄——真正工作交給 SDK，你的 class 只是提供穩定友善的介面。

---

## 直接測試 Client

同一個檔案包含測試 harness，不經過 Claude 就能單獨測 client：

```python
async with MCPClient(
    command="uv", args=["run", "mcp_server.py"]
) as client:
    result = await client.list_tools()
    print(result)
```

跑起來應該會看到前幾課定義的 `read_doc_contents` 與 `edit_document` 這兩個 tool 被印出來。這是 smoke test——如果列表回得來，代表 handshake、transport、decoder 都正常。

---

## End-to-End 流程（使用者問問題時發生什麼）

1. **啟動** — CLI 進入 `MCPClient` context manager，spawn `mcp_server.py` subprocess，完成 MCP handshake
2. **Tool 探索** — CLI 呼叫 `client.list_tools()`，存起來或轉成 Anthropic tool schema
3. **第一次呼叫 Claude** — 使用者問題 + tool 定義送到 `client.messages.create()`
4. **Claude 發出 `tool_use`** — 例如 `read_doc_contents(doc_id="report.pdf")`
5. **Dispatch** — CLI 呼叫 `client.call_tool("read_doc_contents", {"doc_id": "report.pdf"})`
6. **Server 執行** — 回傳 `CallToolResult`，裡面有文件內容
7. **第二次呼叫 Claude** — CLI 把 `tool_result` block（帶原本的 `tool_use_id`）append 進 messages，再呼叫一次 Claude
8. **最終回覆** — Claude 合成使用者看到的答案

這就是第四章的 tool use 迴圈——MCP 只是把「本地 Python function dispatch」換成「透過協議呼叫 server」。

---

## Common Mistakes

1. **在 context 外呼叫 `session()`** — `ClientSession` 必須在 `async with` 內才能用，否則 subprocess 會漏
2. **把 raw `CallToolResult` 直接丟給 Claude** — 還是要包成 `tool_result` content block，並帶正確的 `tool_use_id`
3. **忘記帶 subprocess command** — `MCPClient` 需要 `command` 與 `args`（例如 `command="uv", args=["run", "mcp_server.py"]`），路徑錯就 zero tools
4. **把 `list_tools()` 當便宜操作** — 它是 async round trip，應該 per session 快取一次，不要每次使用者訊息都重呼
5. **同步 / 非同步混用** — MCP SDK 全 async，sync 程式碼沒有 event loop 會噴錯

> **Key Insight**
>
> MCP client 不是重寫你的 agent loop——它是 **transport 替換**。你原本呼叫本地 Python function 的地方，改成呼叫 `client.call_tool(...)` 就好。Agent loop、`tool_use` / `tool_result` 協議、Anthropic API 契約完全不變。MCP 的力量就來自這種可分離性：你的 server 可以被任何 Claude 應用重用，不必改 agent loop。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：知道 MCP client 是 `ClientSession` 的封裝，核心方法是 `list_tools()` / `call_tool()`，用來取代本地 tool dispatch
- **D1（Agentic Architecture）**：agent loop 本身不因 MCP 改變，client 只是換了一種拿 tool、執行 tool 的方式
- 考題模式：「MCP-based app 中 tool 實際在哪裡執行？」→ 在 server，透過 client 的 `call_tool()` 觸發

---

## Flashcards

| Front | Back |
|-------|------|
| MCP client 分哪兩層？ | `ClientSession`（SDK 提供的 transport/handshake 原語）＋ 自寫的 `MCPClient` class（負責生命週期與好用 API） |
| 為什麼要把 `ClientSession` 包在自己的 class 裡？ | 用 context manager 保證 async 清理，並提供穩定友善的對外介面 |
| MCP client 最少要實作哪兩個方法？ | `list_tools()` 與 `call_tool(tool_name, tool_input)` |
| `list_tools()` 回傳什麼？ | 一個 `types.Tool` 陣列，含 `name`、`description`、`inputSchema`，可直接轉給 Claude |
| `call_tool()` 的參數與回傳？ | 參數：`tool_name` 與 `tool_input` dict；回傳 `CallToolResult | None` |
| 如何單獨測 client？ | 直接跑該檔案，`async with MCPClient(command="uv", args=["run", "mcp_server.py"]) as client: await client.list_tools()` |
| MCP 改變 agent loop 嗎？ | 沒有，只有 tool dispatch 那一步變成 `client.call_tool(...)`，loop、stop_reason、tool_result 協議完全不變 |
| 課程使用的 command / args 組合是什麼？ | `command="uv"`、`args=["run", "mcp_server.py"]`，透過 stdio spawn server subprocess |
