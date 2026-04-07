# The STDIO Transport — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.1 (MCP transport 選擇), 2.3 (server 生命週期管理) |
| Source | model-context-protocol-advanced-topics / 03-transports / Lesson 11 |

---

## One-Liner

Stdio 是 MCP 的「僅限本地」transport — 就像同一棟大樓內的直撥電話，功能完整但無法對外連線。

---

![Transport Comparison](../../visuals/transport-comparison-zh-TW.svg)


## 快遞類比

把 MCP transport 想成**訊息的遞送方式**：

- **Stdio** = 大樓內部信件系統。快速、可靠、服務齊全 — 但只在大樓內運作。
- **StreamableHTTP** = 郵局服務。可以跨城市寄送，但某些服務（如當日急件）無法提供。

作為 PM，transport 的選擇直接影響**產品能支援哪些功能**。

---

## 運作方式（商業視角）

MCP client（你的 AI 應用程式）在同一台電腦上**啟動 server 作為輔助程式**。它們透過直接管道溝通 — 就像兩位同事互傳便條。

**Handshake** — 開始工作前的三步建立連線：

| 步驟 | 發生什麼 | 商業類比 |
|------|---------|---------|
| 1. Initialize Request | Client 自我介紹 | 「嗨，我是 AI 應用，我需要工具 X、Y、Z」 |
| 2. Initialize Result | Server 回應能力 | 「收到，我可以提供工具 A、B、C」 |
| 3. Initialized Notification | Client 確認 | 「太好了，開始工作吧」 |

---

## PM 為何該關心 Transport 選擇

### 完整功能存取

Stdio 支援**所有四種通訊模式**：

| 模式 | 商業意義 | 範例 |
|------|---------|------|
| Client 詢問 server | AI 請求工具 | 「查詢這位客戶的訂單」 |
| Server 回答 client | 工具回傳結果 | 「這是訂單詳情」 |
| Server 詢問 client | Server 需要輸入 | 「我需要使用者批准才能繼續」 |
| Client 回答 server | Client 提供輸入 | 「使用者已批准退款」 |

後兩種模式（server-initiated）對於 **agentic workflow** 至關重要 — server 需要請求人類批准或額外上下文。

> 💡 **Key Insight**
> 評估 MCP server 供應商時，要問：「你的 transport 支援 server-initiated request 嗎？」如果不支援，human-in-the-loop 批准流程等功能就無法運作。

---

## PM 決策框架

| 問題 | 是 → Stdio | 否 → 考慮 HTTP |
|------|-----------|---------------|
| Server 在同一台機器上嗎？ | 是 | 需要遠端 |
| 是用於開發/測試嗎？ | 是 | 大規模 Production |
| 需要所有 MCP 功能嗎？ | 是 | 可以犧牲部分 |
| 一次只有一位使用者？ | 是 | 需要多使用者 |

### 一句話總結取捨

Stdio 給你 **100% 的 MCP 功能**，但限制你只能**本地單機部署**。

---

## 產品影響

| 場景 | Transport 影響 |
|------|---------------|
| 開發者工具（IDE plugin） | Stdio 完美 — 與 IDE 一起本地執行 |
| 有 AI 功能的 SaaS 產品 | 無法使用 Stdio — 需要遠端 transport |
| 企業內部本地機器工具 | Stdio 適合桌面部署 |
| 雲端託管 AI agent | 必須使用 StreamableHTTP 或類似方案 |

---

## CCA 考試重點

- **情境題**：「哪種 transport 適合本地開發工具？」→ Stdio
- **功能比較**：Stdio = 完整功能、僅限本地。以此為基準線。
- **Handshake 知識**：三步訊息，按順序。Initialize Request → Initialize Result → Initialized Notification。
- **取捨題**：Stdio 的限制在於部署範圍，而非功能性。

---

## Flashcards

| Front | Back |
|-------|------|
| 用商業術語描述 Stdio transport？ | 直接的本地通訊通道 — 像大樓內部信件系統。服務齊全，但完全沒有遠端能力 |
| Stdio 對產品施加什麼限制？ | Server 必須與 client 在同一台機器上運行 — 無法遠端或雲端部署 |
| 為什麼「server-initiated request」對 PM 很重要？ | 它支援 human-in-the-loop 批准、進度更新和 sampling 等功能 — 對 agentic workflow 至關重要 |
| MCP 連線建立的三個步驟是？ | Initialize Request → Initialize Result → Initialized Notification（三步 handshake） |
| PM 何時應該選 Stdio 而非 HTTP transport？ | 當產品在本地運行（開發工具、桌面應用）且需要完整 MCP 功能支援時 |
| Stdio 支援但 HTTP 可能不支援的功能？ | Server-initiated request（sampling、root listing）和 server-initiated notification（progress、logging） |
| Stdio 的部署限制是什麼？ | 僅限單機 — 無法遠端託管 server 或從中央 server 服務多位使用者 |
| Stdio 在考試中與其他 transport 的關係？ | Stdio 是具備完整能力的基準線 — 其他 transport 用功能換取遠端存取和可擴展性 |
