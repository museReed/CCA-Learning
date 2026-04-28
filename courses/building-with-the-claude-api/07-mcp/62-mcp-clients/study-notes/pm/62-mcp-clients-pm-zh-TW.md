# MCP Clients — PM 視角

| 項目 | 說明 |
|------|------|
| 考試領域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.3（MCP primitives 和協定）、2.4（multi-turn loops）、1.2（agent loop 整合） |
| 來源 | building-with-the-claude-api / 07-mcp / Lesson 62 |

---

## 一句話總結

MCP client 是坐在你產品 server 裡面的「萬用轉接頭」，它會對任何 MCP server 講 MCP 協定——這塊元件讓你的團隊從 stdio 換到 HTTP、從 local dev 換到 production，都不用重寫 agent。

---

## 心智模型：遊樂園的服務台

把你產品的後端想成遊客服務中心，MCP client 就是櫃檯：

| 遊樂園比喻 | 產品/MCP 對應 |
|-----------|--------------|
| 遊客問有哪些遊樂設施 | 使用者問 AI 助理問題 |
| 服務台查詢哪些設施開放 | Server 呼叫 `list_tools` 發現 MCP tools |
| 服務台交給遊客一張票 | Server 透過 MCP client 轉送 tool call |
| 遊客去玩 | MCP server 執行真正的整合 |
| 服務台記錄結果 | Server 把結果回給 Claude |

服務台不負責「開動設施」——它只是把遊客連到設施上。這就是 MCP client 在你 agent 裡扮演的角色。

---

## 這節課為什麼對 PM 重要

Lesson 62 看起來很技術，但它帶來三個會形塑產品的意涵：

1. **整合層是可替換的。** 因為 MCP 是 transport-agnostic，你選哪個 vendor（stdio 開發、HTTP production、未來的 remote MCP）是 PM/ops 決策，不是重寫。
2. **你產品的 agent loop 有明確邊界。** 所有外部系統存取都流經一個可識別的元件（MCP client），所以 governance、logging、rate limits、policy 都可以集中在一處。
3. **跨 SaaS workflow 變成組合問題。** 一旦你的 client 會講 MCP，每個新整合都是「加一個 server」，不是「加一條程式路徑」。

---

## 產品應用場景

### MCP client 抽象能發揮的地方

| 情境 | Client 層為什麼重要 |
|------|-------------------|
| Multi-tenant AI 助理 | 每個 tenant 可以有自己的一組 MCP server 連線，全透過同一個 client 載入 |
| 持續演進的 production infra | 本地用 stdio 開始，需要共享時切 HTTP——產品 code 不用改 |
| Compliance / 稽核 | 所有 tool calls 流經單一點，容易 log 和審查 |
| 新 tools 漸進 rollout | PM 可以在 client 層用 feature flag 控制 MCP servers |

### 抽象不太明顯的情境

| 情境 | 會發生什麼 |
|------|-----------|
| 只有一個整合的產品 | client + server 的 overhead 感覺像繁文縟節 |
| 從不需要 live actions 的產品 | 不需要 tool use，也就不需要 MCP |
| 延遲預算緊的消費產品 | 每層 MCP 都加毫秒——要仔細量 |

---

## 用 PM 語言看「10 步驟流程」

這節課畫了「使用者問『我有哪些 repositories？』」的詳細 10 步驟圖。PM 友善的摘要是：

1. 使用者發問。
2. 產品 server 決定諮詢 agent。
3. Server 向 MCP client 要 tool 菜單。
4. Server 把問題 + 菜單交給 Claude。
5. Claude 說「呼叫這個 tool」。
6. Server 透過 MCP client → MCP server → GitHub 轉送呼叫。
7. GitHub 回覆 → MCP server 包裝 → MCP client 呈現。
8. Server 把結果回給 Claude。
9. Claude 格式化為使用者友善的回答。
10. 使用者看到答案。

對 PM 來說，重要的觀察是**跳了幾次**——每一跳都有成本（延遲、失敗風險、log 面），roadmap 要把它算進去。MCP client 就是把這些複雜度最糟的部分從你產品 code 中抽離的那個元件。

---

## PM 決策框架

審視用 MCP client 的 agent 功能時要問：

1. **我們要用哪個 transport？** stdio 適合本地 dev；HTTP 適合共享/遠端 server。產品團隊通常從 stdio 開始。
2. **MCP client 實例的 lifecycle 誰擁有？** 一個 global client 還是每個 request 一個？會影響並發和成本。
3. **MCP server 在呼叫中掛掉會怎樣？** 使用者看到的失敗模式是你要設計的。
4. **MCP server 延遲要怎麼反映到我們的 SLOs？** 慢的 MCP server 看起來就是慢的 assistant。
5. **Tool calls 的稽核 log 放哪？** 放在 client 層的 middleware——不要散在各處。

---

## 成本視角

這節課的 10 步驟圖有實際成本含義：

| 成本軸 | 來源 |
|-------|------|
| API tokens | 每輪都要把 `list_tools` 的所有 tool 定義送給 Claude |
| 延遲 | 兩次 Claude round trip + 兩次 MCP server round trip + 外部 API 時間 |
| 故障面 | Happy path 有五個 process 間邊界，每個都可能失敗 |
| 工程時間 | 大部分複雜度被 client library 隱藏——這是 PM 贏到的部分 |

每次 PM 提議「多加幾個 MCP server」時，都該理性思考這些成本。更多 server = `list_tools` 回應裡更多 tools = 每輪更多 tokens。

---

## 常見 PM 錯誤

1. **把 MCP client 當成「之後再說」的 infra** — 它是今天的產品決策，形塑你 agent 的演進。
2. **沒問團隊選了哪個 transport** — stdio vs HTTP 有 ops、成本、擴展的後果。
3. **以為 tool listing 是免費的** — 每個 tool 定義每輪都在吃 tokens。
4. **把 MCP client 和 Claude SDK 搞混** — Claude SDK 對 Claude 講話；MCP client 對 MCP servers 講話。
5. **忘記錯誤 UX** — MCP server 失敗會透過你產品 UI 顯現；要設計「tool 失敗」的訊息。

> **Key Insight**
>
> MCP client 是你產品通往外部能力的**單一門**。Agent 能在真實世界做的每件事都要經過這扇門。這讓 client 成為實施產品 policy 的最佳位置——logging、rate limits、per-tenant 存取、feature flags、audit trails。把它當成平台 surface，不只是一個 library import。

---

## CCA 考試重點

- **D2（Tool Design & MCP Integration）**：知道 client 會發 `ListTools` 和 `CallTool` 訊息，以及 MCP 是 transport-agnostic 的。
- **D1（Agentic Architecture）**：能追蹤 10 步驟流程——特別是哪些跳點是 MCP client 經手、哪些是 Claude API 直接溝通。
- 預期會有 PM 味的情境題：「你要為所有 tool calls 加 audit logging——要放哪？」→ MCP client 層。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 用 PM 的話說，MCP client 是什麼？ | 你 server 裡面的單一門，所有外部 tool calls 都要經過它。 |
| 為什麼 transport-agnosticism 是產品贏家？ | 你可以從本地 stdio 演進到網路 HTTP，不用重寫 agent 邏輯。 |
| MCP client 主要用哪兩種訊息類型？ | `ListToolsRequest/Result`（discovery）和 `CallToolRequest/Result`（execution）。 |
| 誰和 Claude API 講話——server、client 還是兩者？ | 產品 server 和 Claude 講話；MCP client 只和 MCP servers 講話。 |
| 多加 MCP tools 會花你產品什麼成本？ | 每輪的 tokens、延遲、稽核/ops 面。 |
| PM 該把 tool use 的 policy control 放哪？ | 放在 MCP client 層——單一瓶頸點。 |
| 「10 步驟流程」在示範什麼？ | 單一使用者問題如何變成跨使用者、server、MCP client、MCP server、Claude 的協調序列。 |
| 從產品角度，MCP server uptime 誰負責？ | 寫/host server 的人——但使用者看到的失敗模式是你要設計的。 |
