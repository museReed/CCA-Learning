# The StreamableHTTP Transport — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.1 (MCP transport 選擇), 2.4 (遠端 server 配置) |
| Source | model-context-protocol-advanced-topics / 03-transports / Lesson 12 |

---

## One-Liner

StreamableHTTP 透過 HTTP 實現遠端 MCP server，但 HTTP 的 request-response 模型意味著 server 無法主動發起通訊 — 以完整 MCP 能力換取遠端託管。

---

## 為什麼需要 StreamableHTTP

Stdio 要求同機器部署。對於服務多使用者或在雲端運行的 production 系統，需要 HTTP。StreamableHTTP 將 MCP 橋接到 Web — 但 HTTP 有一個根本限制：

**HTTP 只能由 client 發起。** Server 只能回應請求，無法主動向 client 發送訊息。

---

## 兩個關鍵配置旗標

StreamableHTTP 的行為由 server 上的兩個 boolean 設定控制：

| 旗標 | 預設值 | 用途 |
|------|--------|------|
| `stateless_http` | `false` | 設為 `true` 時停用 session 追蹤 |
| `json_response` | `false` | 設為 `true` 時回傳純 JSON 而非 SSE stream |

兩者預設為 `false`（最少限制）。啟用任一個都會**移除能力**。

```python
# Server 配置範例
mcp_server = MCPServer(
    stateless_http=False,  # 預設：啟用 session
    json_response=False,   # 預設：啟用 SSE streaming
)
```

> 💡 **Key Insight**
> 把這些旗標想成**限制開關**。啟用越多，server 越簡單 — 但可用的 MCP 功能越少。

---

## HTTP 破壞了什麼

核心限制：**server 無法透過純 HTTP 主動向 client 發起請求**。

### 受影響的 Server-Initiated 功能

| 功能 | 作用 | 無法使用時的影響 |
|------|------|----------------|
| `CreateMessage`（Sampling） | Server 請求 LLM 生成文字 | 無 server 端 AI 呼叫 |
| `ListRoots` | Server 查詢 client 的 workspace | 無檔案系統感知能力 |
| Progress Notification | Server 回報任務進度 | Client 對長時間操作無能見度 |
| Logging Notification | Server 發送日誌訊息 | 無即時除錯資訊 |

### 仍然可用的功能

所有 **client-initiated** 功能正常運作：

- `tools/call` — client 呼叫 server 工具
- `resources/read` — client 讀取 server 資源
- `prompts/get` — client 取得 prompt 模板

---

## 能力光譜

```
完整 MCP（Stdio）
    │
    ▼
StreamableHTTP（預設值）      ← SSE workaround 部分恢復 server→client
    │
    ▼
StreamableHTTP + stateless   ← 無 session，無任何 server-initiated
    │
    ▼
StreamableHTTP + json_response ← 完全無 streaming
    │
    ▼
兩個旗標都啟用               ← 最大限制，最簡單的 server
```

每往下一步都是**用功能換取簡潔/可擴展性**。

---

## 何時使用 StreamableHTTP

| 場景 | 建議配置 |
|------|---------|
| 遠端 server，需要大部分功能 | 預設值（兩者都 `false`） |
| 需要水平擴展 | `stateless_http=true` |
| 簡單的 request-response API | 兩者都 `true` |
| 需要 sampling/progress | 只能用預設值 — 旗標會破壞這些功能 |
| 本地開發 | 改用 Stdio |

---

## CCA 考試重點

- **Transport 取捨題**：StreamableHTTP = 遠端託管、能力降低。要知道確切哪些功能會壞掉。
- **旗標行為**：`stateless_http` 和 `json_response` 都預設為 `false`。啟用是限制而非增強。
- **Server-initiated vs client-initiated**：HTTP 只影響 server-initiated 模式。Client→server 永遠正常。
- 考試哲學：**遠端存取有代價** — 每個網路限制都會移除 MCP 功能。

---

## Flashcards

| Front | Back |
|-------|------|
| HTTP 對 MCP 的根本限制是什麼？ | HTTP 只能由 client 發起 — server 無法主動向 client 發送訊息 |
| StreamableHTTP 的兩個配置旗標是？ | `stateless_http` 和 `json_response`，兩者預設為 `false` |
| 啟用 `stateless_http` 會怎樣？ | 停用 session 追蹤 — 無 server-initiated request、無 sampling、無 progress notification |
| `json_response=true` 的效果？ | 回傳純 JSON 而非 SSE stream — 無 streaming，只有最終結果 |
| 列舉兩個被 HTTP 破壞的 server-initiated 功能 | CreateMessage（sampling）和 Progress Notification |
| 哪些 client-initiated 功能在 HTTP 上仍然正常？ | tools/call、resources/read、prompts/get — 所有 client→server 請求正常運作 |
| StreamableHTTP 的能力取捨是什麼？ | 用遠端託管能力換取 server-initiated MCP 功能的減少/喪失 |
| 何時應該使用 StreamableHTTP 預設值（兩者都 false）？ | 需要遠端託管但仍想要最大 MCP 能力（包括 SSE workaround）時 |
