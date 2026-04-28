# State and the StreamableHTTP Transport — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.1 (MCP transport 選擇), 2.4 (遠端 server 配置), 2.6 (水平擴展模式) |
| Source | model-context-protocol-advanced-topics / 03-transports / Lesson 14 |

---

## One-Liner

當你的 MCP server 變得熱門需要擴展時，你面臨選擇：用複雜基礎架構保留豐富功能，或走 stateless 路線簡單擴展但失去進度追蹤和 AI sampling 等關鍵能力。

---

![Scaling Tradeoff](../../visuals/scaling-tradeoff-zh-TW.svg)


## 連鎖餐廳類比

想像你的 MCP server 是一家餐廳：

- **單一店面**（一個 server instance）：服務生記得你的點餐，可以查看餐點進度，還會主動推薦甜點。完整服務。
- **連鎖擴張**（水平擴展）：你在調度員後面開了多家分店。客人打電話到 A 店預約，但餐點訂單被送到 B 店。B 店完全不知道預約的事。

這就是擴展 MCP server 的**協調問題**。

---

## 為什麼這對你的產品很重要

隨著使用者增長，單一 MCP server instance 無法承受負載。你需要在 load balancer 後面放多個 instance。但 MCP 的 session 模型假設只有一個 server：

| Client 做什麼 | 哪個 Instance 處理 |
|--------------|-------------------|
| 開啟 SSE 連線（持久） | Instance A |
| 發起 tool call（POST） | Instance B（隨機！） |
| 期望收到 progress 更新 | Instance A 有 SSE... 但 B 有任務 |

Load balancer 不理解 MCP session。它只是分配請求。

> 💡 **Key Insight**
> 這不是 bug — 而是 stateful protocol（帶 session 的 MCP）和 stateless 基礎架構（HTTP load balancer）之間的根本張力。每個建構 production MCP server 的團隊都會碰到這面牆。

---

## 兩種擴展策略

### 策略 1：Sticky Session（保留功能）

強制 load balancer 永遠將同一 client 路由到同一 server instance。

| 優點 | 缺點 |
|------|------|
| 保留所有 MCP 功能 | 負載分配不均 |
| 不需要改 code | 每個 client 有單點故障 |
| 熟悉的模式 | 較難自動擴展 |

### 策略 2：走 Stateless（輕鬆擴展）

啟用 `stateless_http=true` — 每個請求獨立。

| 優點 | 缺點 |
|------|------|
| 任何 instance 處理任何請求 | 無進度追蹤 |
| 標準 load balancing 可用 | 無 server-initiated 功能 |
| 輕鬆自動擴展 | 無 sampling（server 不能呼叫 AI） |
| 更好的容錯性 | 無初始化 = 無 capability 協商 |

---

## 利害關係人功能影響摘要

| 功能 | 有狀態 | Stateless | 商業影響 |
|------|--------|-----------|---------|
| 進度條 | 可用 | 失去 | 使用者在長時間操作時盲等 |
| Sampling（AI 推理） | 可用 | 失去 | Server 無法讓 AI 協助決策 |
| 批准流程 | 可用 | 失去 | 無 server 端的 human-in-the-loop |
| 基本 tool call | 可用 | 可用 | 核心功能保留 |
| Resource read | 可用 | 可用 | 資料存取保留 |
| 自動擴展 | 複雜 | 簡單 | 基礎架構團隊可用標準工具 |
| 容錯性 | 差（session 遺失） | 優秀（無狀態可遺失） | Instance 故障時更好的正常運行時間 |

---

## 何時選擇哪種方案

| 場景 | 建議方案 |
|------|---------|
| < 100 同時使用者 | 單一 server，兩個旗標都 false（完整功能） |
| 100-10K 使用者，功能重要 | Sticky session（保留狀態） |
| 10K+ 使用者，基本工具存取 | Stateless 模式 |
| 簡單 API 整合 | Stateless + JSON response |
| Prototype/MVP | 單一 server，所有功能 |

---

## `json_response` 旗標（額外簡化）

在 stateless 之上，還可以啟用 `json_response=true`：

| 不啟用（預設） | 啟用 `json_response=true` |
|--------------|--------------------------|
| 結果即時串流 | 最後一次回傳 |
| 使用者看到部分進度 | 使用者等待，然後一次取得全部 |
| 更複雜的基礎架構 | 標準 REST API 行為 |

兩個旗標都開 = 最簡單的 MCP server。本質上就是帶 MCP 訊息格式的 REST API。

---

## CCA 考試重點

- **擴展情境題**：「Load balancer 後面的 MCP server」→ 雙連線問題 → stateless 是典型答案。
- **取捨分析**：知道 `stateless_http=true` 確切失去什麼 — 五個功能停用。
- **無需初始化**：Stateless 模式跳過 handshake — 任何 instance、任何請求、無需設定。
- **旗標組合**：兩者都 true = 最簡單的 server。考試可能問「最大可擴展性用哪個配置？」
- 考試哲學：**MCP transport 設計中，擴展上去 = 功能下來**。

---

## Flashcards

| Front | Back |
|-------|------|
| MCP 面臨什麼擴展問題？ | 來自同一 client 的兩個連線（SSE + POST）可能命中 load balancer 後面的不同 server instance |
| MCP 水平擴展的標準解決方案是？ | `stateless_http=true` — 消除 session 狀態，讓任何 instance 處理任何請求 |
| 走 stateless 後使用者失去什麼？ | 進度條、sampling、server 發起的批准流程、resource subscription |
| 走 stateless 後使用者保留什麼？ | 基本 tool call 和 resource read — 所有 client-initiated 功能 |
| Stateless 提供什麼基礎架構好處？ | 標準 round-robin load balancing、輕鬆自動擴展、更好的容錯性 |
| `json_response=true` 在 stateless 之上加了什麼？ | 消除 streaming — 只有最終 JSON 回應，行為像標準 REST API |
| PM 何時應選 sticky session 而非 stateless？ | 當產品需要進度追蹤、sampling 或批准流程，且使用者數量可控時 |
| 最簡單的 MCP server 配置是什麼？ | 兩者都設為 `true` — 帶 MCP 訊息格式的基本 HTTP request-response |
