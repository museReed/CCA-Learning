# JSON Message Types — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.4 (client-server communication patterns), 2.6 (MCP protocol specification) |
| Source | model-context-protocol-advanced-topics / 02-roots-and-messages / Lesson 10 |

---

## One-Liner

所有 MCP 通訊使用 JSON 訊息，分為兩類：Request-Result 配對（雙向、期望回應）和 Notification（單向、fire-and-forget），形成 client 和 server 都能主動發起通訊的雙向協議。

---

![Message Types](../../visuals/message-types-zh-TW.svg)


## 兩類訊息

MCP 中每個訊息都屬於兩類之一：

| 類別 | 模式 | 期望回應？ | 範例 |
|------|------|----------|------|
| **Request-Result** | 發送者送出 request，接收者回傳 result | 是 | CallToolRequest/Result, ListPromptsRequest/Result |
| **Notification** | 發送者送出，結束 | 否 | ProgressNotification, LoggingNotification |

這個區別是根本性的 — 它決定了你如何設計錯誤處理、逾時和訊息排序。

---

## Request-Result 配對

Request 總是配對一個 Result 類型。發送者 block（或 await）直到 result 到達。

### 常見 Request-Result 配對

| Request | Result | 發起者 | 用途 |
|---------|--------|--------|------|
| `CallToolRequest` | `CallToolResult` | Client | 在 server 上執行 tool |
| `ListPromptsRequest` | `ListPromptsResult` | Client | 探索可用 prompts |
| `ReadResourceRequest` | `ReadResourceResult` | Client | 讀取 server resource |
| `InitializeRequest` | `InitializeResult` | Client | 建立連線、協商 capabilities |
| `CreateMessageRequest` | `CreateMessageResult` | Server | Sampling — 請 client 呼叫 LLM |
| `ListRootsRequest` | `ListRootsResult` | Server | 探索 client 的核准目錄 |

```json
// 範例：CallToolRequest
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_files",
    "arguments": {
      "query": "config.yaml"
    }
  }
}

// 範例：CallToolResult
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Found config.yaml at /project/config.yaml"
      }
    ]
  }
}
```

注意 `id` 欄位 — 它關聯 request 和對應的 result（JSON-RPC 2.0 標準）。

---

## Notifications

Notification 是 fire-and-forget。沒有 `id` 欄位，不期望回應。

### 常見 Notifications

| Notification | 發送者 | 用途 |
|-------------|--------|------|
| `ProgressNotification` | Server | 回報 tool 執行進度 |
| `LoggingMessageNotification` | Server | 發送 log 訊息給 client |
| `ToolListChangedNotification` | Server | 通知 client 可用 tools 已變更 |
| `ResourceUpdatedNotification` | Server | 通知 client resource 已修改 |
| `RootsListChangedNotification` | Client | 通知 server roots 已更新 |

```json
// 範例：ProgressNotification（沒有 "id" 欄位）
{
  "jsonrpc": "2.0",
  "method": "notifications/progress",
  "params": {
    "progressToken": "task-123",
    "progress": 75,
    "total": 100
  }
}
```

與 request 的關鍵差異：**沒有 `id` 欄位** = notification。

---

## 雙向協議

MCP 是雙向的 — 兩端都能發起通訊：

```
Client                          Server
  |                               |
  |-- InitializeRequest --------->|  (Client 發起)
  |<-- InitializeResult ----------|
  |                               |
  |-- CallToolRequest ----------->|  (Client 發起)
  |<-- ProgressNotification ------|  (Server 推送)
  |<-- LoggingNotification -------|  (Server 推送)
  |<-- CallToolResult ------------|
  |                               |
  |<-- CreateMessageRequest ------|  (Server 發起 — sampling！)
  |-- CreateMessageResult ------->|
  |                               |
  |-- RootsListChanged ---------->|  (Client 推送 notification)
```

這不同於簡單的 HTTP API（只有 client 發起）。MCP 中雙方都是 peer。

---

## 規格文件

MCP 規格在 GitHub 上以 **TypeScript** 撰寫。重要背景：

- TypeScript 用於 **型別描述**，非執行
- 規格定義訊息結構，非實作語言
- Server 可用任何語言撰寫（Python, Go, Rust 等）
- TypeScript 型別作為所有實作的標準參考

```typescript
// 來自規格 — 定義結構，非執行期程式碼
interface CallToolRequest {
  method: "tools/call";
  params: {
    name: string;
    arguments?: Record<string, unknown>;
  };
}
```

---

## Client vs. Server 訊息

理解哪端發送什麼：

| Client 發送（給 Server） | Server 發送（給 Client） |
|-------------------------|-------------------------|
| `InitializeRequest` | `InitializeResult` |
| `CallToolRequest` | `CallToolResult` |
| `ListPromptsRequest` | `ListPromptsResult` |
| `ReadResourceRequest` | `ReadResourceResult` |
| `RootsListChangedNotification` | `ProgressNotification` |
| `CreateMessageResult`（回應） | `CreateMessageRequest`（sampling） |
| | `LoggingMessageNotification` |
| | `ToolListChangedNotification` |

---

## 為什麼 Transport 選擇重要

理解訊息類型對選擇正確 transport 至關重要：

| Transport | 支援雙向？ | 支援 Notification？ |
|-----------|----------|-------------------|
| **stdio** | 是（stdin/stdout） | 是 |
| **SSE** | 是（HTTP POST + SSE stream） | 是 |
| **Streamable HTTP** | 是 | 是 |

所有 MCP transport 都必須支援雙向通訊，因為協議本質就是雙向的。

> **Key Insight**
> MCP 不是 REST API。它是在 transport 層之上的 peer-to-peer 協議。Client 和 server 都可以發送 request 和 notification。理解這個雙向本質對設計穩健的 MCP 整合至關重要 — 你必須處理兩個方向的傳入訊息。

---

## CCA Exam Relevance

- **D2 Task 2.4**：Client-server communication patterns — 兩類訊息定義了協議
- **D2 Task 2.6**：MCP 協議規格 — 知道它用 TypeScript 做型別描述
- 預期考題區分 Request（有 `id`，期望回應）和 Notification（無 `id`，fire-and-forget）
- 知道每端可以發送哪些訊息 — sampling 翻轉了典型方向
- 核心考試哲學：**理解協議** — 訊息類型決定錯誤處理、逾時和 transport 需求

---

## Flashcards

| Front | Back |
|-------|------|
| MCP 訊息分為哪兩類？ | Request-Result 配對（雙向、期望回應）和 Notification（單向、fire-and-forget） |
| JSON 中如何區分 Request 和 Notification？ | Request 有 `id` 欄位；Notification 沒有 |
| MCP 是單向還是雙向？ | 雙向 — client 和 server 都能發起 request 和 notification |
| MCP 規格用什麼語言撰寫？ | TypeScript — 用於型別描述，非執行 |
| 舉一個 server 發起 request 的例子？ | `CreateMessageRequest`（sampling）— server 請 client 呼叫 LLM |
| Server 的 tool 清單變更時發送什麼 notification？ | `ToolListChangedNotification` |
| MCP 使用哪個 JSON-RPC 版本？ | JSON-RPC 2.0 |
| 為什麼 MCP transport 必須支援雙向通訊？ | 因為 client 和 server 都能發起 request（如 client 呼叫 tool，server 請求 sampling） |
