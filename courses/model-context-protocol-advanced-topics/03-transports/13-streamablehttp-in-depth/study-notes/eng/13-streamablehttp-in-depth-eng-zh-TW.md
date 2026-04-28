# StreamableHTTP In Depth — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.1 (MCP transport 選擇), 2.4 (遠端 server 配置), 2.5 (SSE streaming 模式) |
| Source | model-context-protocol-advanced-topics / 03-transports / Lesson 13 |

---

## One-Liner

SSE（Server-Sent Events）是部分恢復 HTTP 上 server-to-client 通訊的 workaround，使用雙連線架構 — primary SSE 處理 server-initiated 訊息，per-tool SSE stream 處理特定呼叫的結果。

---

![Streamable Http Sse](../../visuals/streamable-http-sse-zh-TW.svg)


## SSE 解決什麼問題

HTTP 只能由 client 發起。但 MCP 需要 server 推送訊息（progress、log、sampling request）。**SSE** 翻轉了這個限制：client 開啟一個持久連線，server 隨時可以透過該連線推送事件。

```
傳統 HTTP：
  Client ──request──→ Server
  Client ←──response── Server
  （server 無法發起）

使用 SSE：
  Client ──GET /sse──→ Server
  Client ←──event 1─── Server  （server 隨時推送）
  Client ←──event 2─── Server
  Client ←──event 3─── Server
  ...
```

---

## 連線建立順序

| 步驟 | 動作 | 細節 |
|------|------|------|
| 1 | Client 發送 Initialize Request | POST 到 server |
| 2 | Server 回傳 Initialize Result + **session ID** | Session ID 追蹤此 client |
| 3 | Client 發送 Initialized Notification | 帶 session ID 的 POST |
| 4 | Client 開啟 SSE 連線 | **GET request** — 保持開啟接收 server-initiated 訊息 |

Session ID 至關重要 — 它將 GET SSE 連線與同一 client 的 POST 請求連結起來。

```python
# 步驟 1-3：正常 handshake
session_id = initialize_handshake(server_url)

# 步驟 4：開啟持久 SSE 連線
sse_stream = requests.get(f"{server_url}/sse",
    headers={"Mcp-Session-Id": session_id},
    stream=True
)
```

---

## 雙 SSE 架構

這是核心架構概念。有**兩種** SSE 連線：

### 1. Primary SSE 連線（GET）

- 初始化後開啟一次
- **全 session 保持開啟**
- 傳輸 **server-initiated 訊息**：sampling request、root list request
- 把它想成「通用通知頻道」

### 2. Tool-Specific SSE 連線（POST）

- 為**每次 tool call** 建立
- Tool call 完成時**自動關閉**
- 傳輸 **tool 專屬訊息**：progress 更新、log 條目、最終結果
- 把它想成「per-task 頻道」

```
Client                          Server
  │                               │
  │──── GET /sse ────────────────→│  （Primary SSE — 保持開啟）
  │←─── server-initiated msgs ───│
  │                               │
  │──── POST /tools/call ────────→│  （Tool SSE — 自動關閉）
  │←─── progress, logs, result ──│
  │                               │
  │──── POST /tools/call ────────→│  （另一個 Tool SSE）
  │←─── progress, logs, result ──│
```

> 💡 **Key Insight**
> 雙 SSE 設計意味著 server 可以透過 tool SSE 推送特定 tool call 的 progress，**同時**透過 primary SSE 推送無關的 server-initiated request。它們是獨立的頻道。

---

## 訊息路由規則

理解哪些訊息走哪個頻道是考試關鍵：

| 訊息類型 | SSE 頻道 | 原因 |
|---------|---------|------|
| Progress notification | Tool-specific SSE | 綁定到特定 tool call |
| Log 訊息 | Tool-specific SSE | 在 tool 執行期間產生 |
| Tool 結果 | Tool-specific SSE | 該次呼叫的最終答案 |
| CreateMessage（sampling） | Primary SSE | Server-initiated，不綁定 tool call |
| ListRoots | Primary SSE | Server-initiated，不綁定 tool call |

---

## 什麼會破壞 SSE 機制

Lesson 12 的兩個配置旗標直接影響 SSE：

| 旗標 | 對 SSE 的影響 |
|------|-------------|
| `stateless_http=true` | 無 session ID → 無 primary SSE 連線 → 無 server-initiated 訊息 |
| `json_response=true` | 完全無 streaming → tool call 只回傳最終 JSON → 執行期間無 progress/log |

兩個旗標都啟用 = SSE 完全停用。回到基本 HTTP request-response。

---

## CCA 考試重點

- **SSE 架構題**：知道雙連線模型 — primary（持久、server-initiated）vs tool-specific（per-call、自動關閉）。
- **訊息路由**：Progress 和 log 走 tool SSE。Sampling 和 roots 走 primary SSE。
- **旗標影響**：`stateless_http` 殺死 primary SSE。`json_response` 殺死所有 streaming。
- **Session ID**：連結 GET 和 POST 連線。沒有它，server 無法關聯請求。
- 考試哲學：**SSE 是 workaround，不是完整解決方案** — 它只是部分恢復 server→client 通訊。

---

## Flashcards

| Front | Back |
|-------|------|
| SSE 在 MCP 中解決什麼問題？ | HTTP server 無法主動通訊 — SSE 提供持久連線讓 server 推送事件 |
| 兩種 SSE 連線類型是什麼？ | Primary SSE（GET、保持開啟、server-initiated 訊息）和 Tool-specific SSE（POST、per-call、自動關閉） |
| Progress notification 路由到哪裡？ | Tool-specific SSE 連線（綁定到特定 tool call） |
| Sampling（CreateMessage）request 路由到哪裡？ | Primary SSE 連線（server-initiated，不綁定任何 tool call） |
| Session ID 的作用是什麼？ | 將持久 GET SSE 連線與同一 client 的 POST 請求連結起來 |
| `stateless_http=true` 會怎樣？ | 無 session ID、無 primary SSE 連線、無 server-initiated 訊息 |
| `json_response=true` 會怎樣？ | 完全無 SSE streaming — 只回傳最終 JSON 結果 |
| SSE 的建立順序是？ | Initialize Request → Initialize Result（取得 session ID）→ Initialized Notification → GET request 開啟 primary SSE |
