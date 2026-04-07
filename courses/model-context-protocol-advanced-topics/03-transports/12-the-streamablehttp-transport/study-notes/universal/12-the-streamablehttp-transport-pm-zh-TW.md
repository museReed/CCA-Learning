# The StreamableHTTP Transport — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.1 (MCP transport 選擇), 2.4 (遠端 server 配置) |
| Source | model-context-protocol-advanced-topics / 03-transports / Lesson 12 |

---

## One-Liner

StreamableHTTP 讓你的 MCP server 上網，但就像從私人辦公室搬到公共櫃台 — 增加了可及性，卻失去了主動找人的能力。

---

## 櫃台類比

- **Stdio** = 私人辦公室。你和同事面對面坐著，任何人都能隨時發起對話。
- **StreamableHTTP** = 服務櫃台。訪客（client）可以走過來提問，但櫃台人員（server）**不能離開櫃台**去找訪客 — 必須等人來。

這是 HTTP 的根本限制：**server 只能回應，不能主動發起**。

---

## 對產品的意義

### 仍然可用的功能（Client-Initiated）

| 功能 | 使用者體驗 |
|------|----------|
| Tool call | 使用者問 AI，AI 呼叫 server 工具 — 完美運作 |
| Resource read | AI 從 server 取得資料 — 完美運作 |
| Prompt template | AI 從 server 載入模板 — 完美運作 |

### 有風險的功能（Server-Initiated）

| 功能 | 失去什麼 | 產品影響 |
|------|---------|---------|
| Sampling（CreateMessage） | Server 無法請求 AI 生成文字 | 無 server 端 AI 推理 |
| Progress notification | Server 無法回報「完成 50%...」 | 使用者在長任務中看不到進度 |
| Logging | Server 無法推送除錯訊息 | Production 更難排查問題 |
| Root listing | Server 無法問「開了哪些檔案？」 | 無 workspace 感知功能 |

> 💡 **Key Insight**
> 如果你的產品路線圖包含 **server 需要向 client 提問**的功能（如「批准這個操作？」或「應該用哪個檔案？」），啟用限制性設定的 StreamableHTTP 會阻擋這些功能。

---

## 兩個配置開關

把它們想成基礎架構團隊可以設定的**限制等級**：

| 設定 | 關閉（預設） | 開啟 | 商業影響 |
|------|------------|------|---------|
| `stateless_http` | Server 記住每個 client session | Server 將每個請求視為獨立 | 更容易擴展，但失去進度追蹤和 server-initiated 功能 |
| `json_response` | Server 可以逐步串流結果 | Server 最後才一次回傳 | 基礎架構更簡單，但使用者等待更久 |

### 限制光譜

```
最多功能 ◄──────────────────────────────► 最簡單架構

兩者都關        stateless 開      json 開         兩者都開
（預設）        或 json 開       或 stateless     （最大限制）
```

---

## PM 決策矩陣

| 商業需求 | 建議設定 |
|---------|---------|
| 「需要即時進度條」 | 兩個旗標都關（預設） |
| 「需要擴展到一萬使用者」 | `stateless_http=true`（接受功能損失） |
| 「簡單的 webhook 風格整合」 | 兩個旗標都開 |
| 「Server 需要呼叫 AI 模型」 | 兩個旗標都關 + SSE 設定 |
| 「只需要基本工具存取」 | 任何配置都行 |

---

## 利害關係人溝通的核心取捨

| 維度 | Stdio | StreamableHTTP（預設） | StreamableHTTP（限制） |
|------|-------|----------------------|---------------------|
| 部署 | 僅限本地 | 遠端/雲端 | 遠端/雲端 |
| 可擴展性 | 單一使用者 | 中等 | 高 |
| 功能覆蓋 | 100% | ~80%（有 SSE workaround） | ~50% |
| 基礎架構複雜度 | 最低 | 中等 | 低 |

---

## CCA 考試重點

- **情境題**：「Web 應用的遠端 MCP server」→ StreamableHTTP。然後檢查場景需要哪些功能來決定旗標設定。
- **取捨題**：知道每個限制等級確切失去哪些功能。
- **旗標預設值**：都是 `false` — 這是常考的。啟用是限制而非增強。
- **方向不要搞混**：Client→server 永遠可用。只有 server→client 受影響。

---

## Flashcards

| Front | Back |
|-------|------|
| 用商業術語描述 StreamableHTTP 的功能？ | 遠端 MCP server 託管 — server 可以在雲端，透過網路服務使用者 |
| HTTP 對 MCP 的根本限制是什麼？ | Server 無法主動發起通訊 — 只能回應 client 請求 |
| 哪些產品功能需要 server-initiated request？ | 進度條、人工審批流程、server 端 AI 推理（sampling） |
| 兩個旗標的預設值是？ | `stateless_http` 和 `json_response` 都預設為 `false`（最少限制） |
| 開啟 `stateless_http` 會怎樣？ | Server 忘記 session — 更容易擴展但失去進度追蹤和 server-initiated 功能 |
| 開啟 `json_response` 會怎樣？ | 無 streaming — server 一次回傳完整結果而非逐步更新 |
| PM 何時應該接受功能取捨？ | 當可擴展性或基礎架構簡潔性比 server-initiated 功能更重要時 |
| 不管旗標怎麼設，哪些功能永遠可用？ | Client-initiated 功能：tool call、resource read、prompt template 取得 |
