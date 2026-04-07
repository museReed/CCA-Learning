# Sampling — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server capabilities), 2.4 (client-server communication patterns) |
| Source | model-context-protocol-advanced-topics / 01-sampling-and-notifications / Lesson 03 |

---

## One-Liner

Sampling 讓 MCP server 借用 client 的 AI 大腦而非自備，將成本與複雜度轉移給連接方。

---

![Sampling Flow](../../visuals/sampling-flow-zh-TW.svg)


## 心智模型：翻譯員類比

想像你在東京經營一個旅遊服務台（MCP server）。一位法國遊客（使用者）帶著自己的隨行翻譯（MCP client + Claude）前來。你不需要自己雇法語翻譯，只要對遊客的翻譯員說話，請他們轉達就好。

| 角色 | 類比 | MCP 對應 |
|------|------|----------|
| 旅遊服務台 | 提供在地知識 | MCP server（domain logic） |
| 遊客的翻譯員 | 轉達與翻譯 | MCP client（呼叫 Claude） |
| 遊客 | 想要答案 | 終端使用者 |

服務台不需要學法語，遊客的翻譯員搞定一切。這就是 sampling。

---

## PM 為什麼要懂 Sampling

Sampling 從根本上改變了 MCP server 的 **商業模式**：

### 沒有 Sampling（傳統模式）
- Server 方為每次 AI 呼叫付費
- 必須管理 API key、帳單、rate limit
- 擴展成本隨使用者線性成長
- 開源的障礙：誰來付 API 帳單？

### 有 Sampling
- 每個 client 為自己的 AI 使用付費
- Server 零 AI 基礎設施成本
- Server 純粹專注於領域專業
- 對開源友善：無持續成本

> **Key Insight**
> Sampling 就是 AI 工具的「BYOB（Bring Your Own Brain）」模式。它移除了建置和分享 MCP server 最大的障礙：LLM API 呼叫的成本。

---

## 產品情境演練

### 情境：研究聚合工具

你的團隊正在建置一個搜尋學術論文並摘要結論的 public MCP server。比較兩種方式：

| 面向 | 直接 API（Server 付費） | Sampling（Client 付費） |
|------|------------------------|----------------------|
| 每用戶成本 | Server 承擔所有 AI 費用 | Server 零成本 |
| API key 管理 | Server 需要 key、輪替、安全措施 | 不需要 — client 處理 |
| Model 控制 | Server 選擇 model | Client 選擇 model |
| 擴展考量 | 每增加一個使用者就增加 server 帳單 | Server 成本固定（只有運算） |
| 使用者信任 | 使用者信任 server 處理資料 | 使用者自己的 client 處理資料 |

**PM 決策**：對於面向公眾的研究工具，sampling 明顯更優 — 它解決了「越多使用者 = 越多成本」的單位經濟問題。

---

## 取捨矩陣

| 面向 | Sampling 勝出 | 直接 API 勝出 |
|------|--------------|--------------|
| 成本歸屬 | Server 零 AI 成本 | Server 控制品質 |
| Model 一致性 | — | 保證 model 版本 |
| 設定複雜度 | Server 端更低 | Client 端更低 |
| 公開發佈 | 理想選擇 | 大規模不可行 |
| 延遲 | — | 更少網路跳轉 |
| 合規 | Client 控制資料流 | Server 控制資料流 |

---

## 流程說明（無程式碼）

1. 使用者請 client 使用 server tool（如「摘要這份研究」）
2. Server 收集領域資料（搜尋論文、彙整結果）
3. Server 請 client：「請讓 Claude 幫我摘要這些」
4. Client 使用自己的 API key 呼叫 Claude
5. Client 將 Claude 的回應傳回 server
6. Server 將最終結果交付給使用者

Server 從不直接碰 AI。它是 **請求者**，不是 **呼叫者**。

---

## 治理考量

作為 PM，需要與團隊討論以下事項：

- **Client 可以拒絕**：Client 沒有義務滿足 sampling 請求。Server 必須優雅處理拒絕情況。
- **Client 選擇 model**：如果產品依賴特定 model 的能力，sampling 無法保證。
- **資料流經 client**：Client 會看到所有 sampling 內容。對於敏感資料，需評估是否可接受。
- **Server 無法記錄 AI 呼叫**：因為 client 發出呼叫，server 無法直接記錄或稽核 AI 互動。

---

## CCA Exam Relevance

- **D2 Task 2.3**：Sampling 作為進階 MCP capability — 知道何時建議使用
- **D2 Task 2.4**：Server-initiated communication pattern — sampling 是典型範例
- 預期情境題會比較不同商業場景下 sampling vs. 直接 API
- 考試核心哲學：**Architecture > Prompt** — 選擇正確的通訊模式是架構決策

---

## Flashcards

| Front | Back |
|-------|------|
| MCP sampling 解決什麼商業問題？ | 將 LLM 呼叫成本轉移給 client，消除 server 營運者的 AI API 費用 |
| Sampling 中誰持有 API key？ | Client — server 完全不需要 |
| 為什麼 sampling 適合開源 MCP server？ | 每個使用者的 client 支付自己的 AI 費用，server 作者無持續 API 成本 |
| Sampling 對產品品質的主要風險？ | Client 控制 model 選擇 — server 無法保證使用哪個 model |
| 誰發起 sampling 請求？ | Server 發起，請 client 代為呼叫 Claude |
| Client 可以拒絕 sampling 請求嗎？ | 可以 — client 有完全自主權決定接受、修改或拒絕 |
| Sampling 的「BYOB」類比是什麼？ | 「Bring Your Own Brain」— 每個 client 自帶 AI 能力到 server |
| PM 何時應建議不使用 sampling？ | 產品需要保證 model 行為、特定 model 版本、或 server 端 AI 呼叫稽核記錄時 |
