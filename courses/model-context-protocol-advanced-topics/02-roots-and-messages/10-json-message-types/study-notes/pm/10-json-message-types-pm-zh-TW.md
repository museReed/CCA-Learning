# JSON Message Types — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.4 (client-server communication patterns), 2.6 (MCP protocol specification) |
| Source | model-context-protocol-advanced-topics / 02-roots-and-messages / Lesson 10 |

---

## One-Liner

MCP 通訊使用兩種 JSON 訊息 — 對話（request-response）和公告（notification）— 在一個 client 和 server 都能主動開口的雙向協議中。

---

![Message Types](../../visuals/message-types-zh-TW.svg)


## 心智模型：對講機 vs. 廣播器

| 訊息類型 | 類比 | 行為 |
|---------|------|------|
| **Request-Result** | 對講機對話 | 「收到嗎？」...「收到，資訊如下」 |
| **Notification** | 廣播器公告 | 「注意：進度 50%」（不需回應） |

關鍵差異：對講機訊息等待回覆；廣播器公告不等。

---

## PM 為什麼需要理解訊息類型

你不需要讀 JSON，但需要理解其影響：

### 1. 錯誤處理需求

- **Request-Result**：如果回應永遠不來，產品必須處理逾時和重試
- **Notification**：如果丟失，不會壞 — 但使用者錯過狀態更新

這影響你可靠性的驗收標準。

### 2. 產品架構決策

- 知道 MCP 是 **雙向的** 意味著 server 不只是被動的 tool 提供者 — 它可以主動向 client 請求（如 sampling）
- 這開啟了簡單 request-response API 無法支援的產品可能性

### 3. Transport 選擇

不同部署環境支援不同 transport。理解訊息類型幫助評估哪個 transport 適合你的產品。

---

## 兩類訊息

### 類別 1：Request-Result（對話）

有人問問題，有人回答。

| 誰問 | 問什麼 | 誰答 |
|------|--------|------|
| Client | 「執行這個 tool」（CallTool） | Server |
| Client | 「你有哪些 tools？」（ListTools） | Server |
| Client | 「給我這個 resource」（ReadResource） | Server |
| Client | 「讓我們連線」（Initialize） | Server |
| Server | 「請幫我呼叫 Claude」（CreateMessage — sampling） | Client |
| Server | 「我可以存取哪些目錄？」（ListRoots） | Client |

注意 **兩端都能提問**。這就是 MCP 雙向的原因。

### 類別 2：Notification（公告）

有人分享資訊，不期望回應。

| 誰公告 | 說什麼 |
|--------|--------|
| Server | 「進度：50% 完成」 |
| Server | 「Log：搜尋資料庫中...」 |
| Server | 「我的 tool 清單已變更」 |
| Server | 「某個 resource 已更新」 |
| Client | 「我的 root 目錄已變更」 |

---

## 雙向：兩端都能說話

這是關鍵的架構洞察。MCP 不像 web API 只有 client 發起：

| 傳統 API | MCP 協議 |
|---------|----------|
| Client 發送 request | Client 發送 request |
| Server 回應 | Server 回應 |
| Server 無法發起 | **Server 可以發起**（sampling、root 查詢） |
| 單向關係 | **Peer-to-peer 關係** |

> **Key Insight**
> MCP 是雙向道路。作為 PM，這意味著你可以設計 server 主動請求東西的產品功能 — 如透過 sampling 請 client 摘要資料。這是 REST API 原生不支援的能力。

---

## 規格用 TypeScript 撰寫

官方 MCP 規格在 GitHub 上，用 TypeScript 撰寫。PM 要點：

- TypeScript 用於 **描述資料結構**（如 schema），非必要語言
- Server 和 client 可用 **任何語言** 建置（Python, Go, JavaScript, Rust）
- 規格是訊息長什麼樣的 **source of truth**
- 工程師辯論「這個訊息有哪些欄位？」時 — 規格就是答案

---

## 每種訊息類型的產品影響

| 訊息類型 | 產品影響 | PM 關注點 |
|---------|---------|----------|
| CallToolRequest/Result | 核心 tool 執行 | 必須定義逾時和錯誤狀態 |
| InitializeRequest/Result | 連線設定 | 預先定義支援的 capabilities |
| CreateMessageRequest/Result | Sampling（server 使用 AI） | 成本轉移到 client — 定價影響 |
| ProgressNotification | 長時間操作的 UX | 必須設計載入狀態 |
| LoggingNotification | 除錯和監控 | 必須定義 log 保留策略 |
| ToolListChangedNotification | 動態 tool 發現 | UI 必須處理 tool 清單更新 |

---

## 常見考試情境

### 情境：Transport 中訊息丟失

問：「一個 progress notification 在傳輸中丟失。會發生什麼？」
答：不會壞 — 使用者錯過一次狀態更新但 tool 繼續運作。Notification 是 fire-and-forget。

問：「一個 CallToolResult 在傳輸中丟失。會發生什麼？」
答：Client 逾時且必須重試。Request-Result 配對需要回應 — 缺少 result 就是失敗。

這個區別經常被考。

---

## CCA Exam Relevance

- **D2 Task 2.4**：Communication patterns — 知道兩類訊息和每端發送什麼
- **D2 Task 2.6**：Protocol specification — 知道它用 TypeScript 做型別描述
- 關鍵區別：Request 有 `id` 欄位，Notification 沒有
- 知道 MCP 是雙向的 — server 可以發起 request（sampling、list_roots）
- 考試哲學：**Protocol literacy** — 理解訊息類型影響錯誤處理和架構

---

## Flashcards

| Front | Back |
|-------|------|
| MCP 訊息分為哪兩類？ | Request-Result 配對（期望回應）和 Notification（fire-and-forget） |
| 協議中 Request 和 Notification 怎麼區分？ | Request 有 `id` 欄位且期望回應；Notification 無 `id` 且不期望回應 |
| MCP 是只有 client 發起的協議嗎？ | 不是 — 它是雙向的；client 和 server 都能發起 request |
| MCP 規格用什麼撰寫？ | TypeScript — 用於型別描述，非必要的實作語言 |
| Notification 丟失會怎樣？ | 不會壞 — 接收方錯過資訊性更新但功能繼續 |
| Request Result 丟失會怎樣？ | 發送方必須處理逾時並可能重試 — 這是失敗情境 |
| 舉一個 server 發起 request 的例子？ | CreateMessageRequest（sampling）— server 請 client 呼叫 Claude |
| 為什麼 transport 選擇對 MCP 很重要？ | 所有 transport 必須支援雙向通訊，因為兩端都能發起訊息 |
