# MCP Clients — 工程深度解析

| 項目 | 說明 |
|------|------|
| 考試領域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.3（MCP primitives 和協定）、2.4（multi-turn tool loops）、1.2（agent loop 整合） |
| 來源 | building-with-the-claude-api / 07-mcp / Lesson 62 |

---

## 一句話總結

MCP client 是你 server 裡面用來講 MCP 協定和 MCP servers 溝通的通訊橋——它把 transport、discovery（`ListTools`）、invocation（`CallTool`）都抽象化，讓你的 app code 對遠端 tools 的使用幾乎和本地 function 一樣。

---

## Client 的角色

Lesson 61 介紹了 MCP 的架構層面；Lesson 62 聚焦在 client 這一半。你的 application 裡有一塊程式碼負責：

1. 透過某種 transport 建立和 MCP server 的連線。
2. 問 server「你提供哪些 tools？」
3. 時機到時，把 Claude 的 tool-use 請求轉給 server。
4. 把 server 的結果往上回給你的 agent loop。

這塊就是 **MCP client**。它是你自己 server 裡的一個 library，不是獨立服務。如果你用過 HTTP client（例如 `requests.Session`）打 REST API，MCP client 對 MCP servers 扮演的角色一模一樣。

---

## Transport Agnostic 通訊

MCP 的核心設計特性之一是 **transport agnostic**——client 和 server 可以用任何合理的媒介通訊。目前最常見的設定：

| Transport | 使用情境 |
|-----------|---------|
| **stdio**（標準輸入輸出） | client 和 server 在同一台機器；server 是 subprocess |
| **HTTP** | client 和 server 在不同機器；網路可存取的 server |
| **WebSockets** | 跨網路的雙向串流 |
| **其他網路協定** | 客製化部署 |

重要的含義：**同樣的 MCP 協定訊息不管 transport 是哪種都能用**。從 stdio（本地開發）切換到 HTTP（production）不會改變 `ListToolsRequest` 或 `CallToolRequest` 的形狀——只是 bytes 的傳送方式改了。

---

## 核心訊息類型

MCP 定義了一套訊息類型。最常用的兩個（也是 Lesson 62 強調的）：

### 1. List Tools

```
Client  ──▶  ListToolsRequest   ──▶  Server
Client  ◀──  ListToolsResult    ◀──  Server
```

Client 問 server「你提供哪些 tools？」，server 回一個結構化的 tool 定義清單。每個定義包含 name、description 和 input schema——形狀跟你 Claude API `tools` array 預期的完全一樣，這不是巧合。

### 2. Call Tool

```
Client  ──▶  CallToolRequest   ──▶  Server
Client  ◀──  CallToolResult    ◀──  Server
```

Client 請 server 用特定參數執行某個 tool。Server 執行後回傳結果。然後你的 server 把這個結果包成 `tool_result` block 送給 Claude。

這兩個訊息類型涵蓋了 tools 的「discovery → invocation」完整循環。後面的 lessons 會介紹類似的訊息給 resources 和 prompts。

---

## 完整流程範例（查 repository）

Lesson 62 走過一個具體例子：使用者問「我有哪些 repositories？」。以下是完整序列：

```
┌──────┐    1 query     ┌────────────┐    2 ListToolsReq ┌─────────┐
│ User │ ─────────────▶ │ 你的 server │ ────────────────▶ │  MCP    │
└──────┘                │ + MCP      │ ◀────────────────│ Server  │
                        │  client    │ 3 ListToolsResult│         │
                        │            │                   │         │
                        │            │  4 messages w/    ┌─────────┐
                        │            │ ──── tools ─────▶│ Claude  │
                        │            │ ◀──── tool_use ──│  API    │
                        │            │  5 tool_use      └─────────┘
                        │            │
                        │            │  6 CallToolReq   ┌─────────┐
                        │            │ ────────────────▶│  MCP    │
                        │            │                  │ Server  │
                        │            │                  │    │    │
                        │            │                  │    ▼    │
                        │            │                  │ GitHub  │
                        │            │                  │   API   │
                        │            │                  │    │    │
                        │            │  7 CallToolResult│ ◀──┘    │
                        │            │ ◀────────────────│         │
                        │            │                  └─────────┘
                        │            │  8 tool_result   ┌─────────┐
                        │            │ ────────────────▶│ Claude  │
                        │            │ ◀── final answer ┤  API    │
                        │            │  9               └─────────┘
                        └────────────┘
                             │  10 final answer
                             ▼
                        ┌──────┐
                        │ User │
                        └──────┘
```

逐步解析：

1. **User** 提交查詢給你的 server。
2. **你的 server** 意識到需要先告訴 Claude 有哪些 tools 可用，所以向 MCP client 要。
3. **MCP client** 發 `ListToolsRequest` 給 MCP server，拿到 `ListToolsResult`。
4. 你的 server 帶著使用者問題 + tool list 呼叫 Claude。
5. Claude 回傳 `tool_use` block。
6. 你的 server 把 tool use 細節交給 MCP client，client 發 `CallToolRequest` 給 MCP server。MCP server 實際去打 GitHub API。
7. GitHub 回覆 → MCP server 包裝結果 → `CallToolResult` 回到 MCP client。
8. 你的 server 把結果加到 message list 再呼叫 Claude。
9. Claude 格式化最終回答。
10. 你的 server 把回答回給使用者。

這就是 Ch04 tool use 同一個 agentic loop——差別在於 tool listing 和 tool execution 透過 MCP client 代理，而不是你自己 server 裡實作。

---

## MCP Client 幫你抽象掉什麼

寫得好的 MCP client 會隱藏：

| 關注點 | Client 幫你處理 |
|-------|---------------|
| Transport 協商 | 根據連線設定選擇 stdio、HTTP 等 |
| 訊息框架 | 在 wire 上序列化/反序列化 JSON-RPC 風格訊息 |
| 請求/回應關聯 | 把回應配對到對應的進行中請求 |
| 錯誤信封 | 區分協定層錯誤和 tool 層錯誤 |
| Lifecycle | 啟動/停止 server subprocess（適用時） |

你的 application code 通常只看到 `client.list_tools()` 和 `client.call_tool(name, args)`——這些是簡單的 async method，回傳資料，不是一堆 JSON-RPC 水管。

---

## 為什麼 Transport Agnosticism 重要

兩個工程上的理由：

1. **Local dev 和 production 的一致性。** 開發時寫 stdio，production 切 HTTP，agent 邏輯不用動。
2. **Process 隔離和安全性。** stdio 的 MCP server 跑在 subprocess，崩潰被隔離；HTTP 的 MCP server 跑在不同 host，blast radius 更小。你的 agent code 根本不需要知道是哪一種。

這也解釋了為什麼 MCP servers 可以安全組合：每個都獨立、不共享記憶體，protocol 處理 handshake。

---

## 常見錯誤

1. **把 MCP client 當成「和 Claude 講話的那個」** — 它不是。Client 是和 MCP servers 講話；你的 application 和 Claude API 仍然是分開溝通。
2. **忘了在第一次呼叫 Claude 前呼叫 `list_tools`** — Claude 需要先拿到 tool 定義，不然它無法選 tool。
3. **以為 stdio 是玩具 transport** — 大部分真實的 MCP 整合都跑在 stdio；它是主要的本地開發路徑，production 也能用。
4. **混淆 `CallToolResult` 和 `tool_result`** — `CallToolResult` 是 MCP 層的回應；`tool_result` 是你把它包成 Claude API content block 之後的產物。
5. **以為一個 tool call 會立即回傳** — tool 執行可能包含外部 API 延遲（GitHub、DB 等），所以 client 預設是 async。

> **Key Insight**
>
> MCP client 把「我 agent 能呼叫遠端 tool 嗎？」變成和「我 agent 能呼叫本地 function 嗎？」一樣的形狀——而且不綁定任何特定 transport。把 list-tools + call-tool 這個循環掌握熟，Lesson 63-65 才會看懂。後面所有東西都是更多 primitives 跑在同樣的兩個模式上。

---

## CCA 考試重點

- **D2（Tool Design & MCP Integration）**：知道 MCP client 是什麼、`ListTools` 和 `CallTool` 的差別、transport agnosticism 概念。
- **D1（Agentic Architecture）**：本節課的 10 步驟圖是「agent + MCP」的標準流程，可能出現在情境題。
- 考試陷阱：題目會問每個訊息類型*出現在流程的哪裡*（client↔server、server↔Claude）。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| MCP client 的角色是什麼？ | 你 server 裡面的 library，用 MCP 協定和 MCP servers 講話，處理 transport、discovery、invocation。 |
| MCP 的「transport agnostic」是什麼意思？ | Client 和 server 可以用 stdio、HTTP、WebSockets 或其他 transport，同樣的訊息類型通用。 |
| Client 用哪個 MCP 訊息類型發現可用 tools？ | `ListToolsRequest`，server 回 `ListToolsResult`。 |
| Client 用哪個 MCP 訊息類型執行 tool？ | `CallToolRequest`，server 回 `CallToolResult`。 |
| 在 10 步驟流程中，MCP client 直接和 Claude 講話嗎？ | 不——是你的 server 和 Claude 講話；MCP client 只和 MCP servers 講話。 |
| 最常見的本地 MCP transport 是什麼？ | stdio（標準輸入輸出）——通常 server 跑在 subprocess。 |
| `CallToolResult` 和 Claude 預期的 `tool_result` block 差在哪？ | `CallToolResult` 是 MCP 層的回應；你 server 要把它包成 `tool_result` content block 才能給下一次 Claude API call。 |
| 回答「我有哪些 repositories」這個例子要幾次 round trip？ | 和 Claude 兩次（初始+最終），和 MCP server 兩次（list_tools + call_tool）。 |
