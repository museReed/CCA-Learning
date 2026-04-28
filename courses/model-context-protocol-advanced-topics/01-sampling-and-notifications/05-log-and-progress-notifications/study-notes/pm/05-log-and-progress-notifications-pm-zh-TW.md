# Log and Progress Notifications — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server capabilities), 2.5 (server-to-client communication) |
| Source | model-context-protocol-advanced-topics / 01-sampling-and-notifications / Lesson 05 |

---

## One-Liner

MCP server 可以在長時間操作中發送即時狀態更新和進度指示器給 client，將沈默的黑箱處理轉變為透明、友善的使用者體驗。

---

## 心智模型：餐廳廚房

把 MCP tool 想成餐廳廚房：

| 沒有 Notification | 有 Notification |
|------------------|-----------------|
| 你點餐後沈默等待 | 服務生說「您的前菜正在準備」 |
| 過了 20 分鐘 — 菜要來了嗎？ | 「主菜正在烤箱裡，還要 10 分鐘」 |
| 你考慮離開 | 「正在擺盤 — 馬上好！」 |
| 菜來了（或沒來） | 菜來了，而且全程都有被告知 |

Notification 不改變食物，改變的是 **用餐體驗**。

---

## 兩種即時回饋類型

| 類型 | 功能 | 類比 |
|------|------|------|
| **Logging** | 處理中的狀態訊息（「搜尋資料庫中...」「找到 42 筆結果」） | 服務生的口頭更新 |
| **Progress** | 完成百分比（30%、60%、90%） | 外送追蹤頁的進度條 |

兩者都是 **可選的** — tool 沒有它們也能運作。但它們大幅改善感知效能和使用者信任。

---

## PM 為什麼要在意

### 1. 使用者的速度感知

研究一致顯示，有進度指示器的任務感覺比沒有的更快，即使花費相同時間。對於可能跑 10-60 秒的 AI 工具，這至關重要。

### 2. 降低放棄率

使用者在長時間操作中沒有看到回饋時會：
- 認為工具壞了
- 重試（產生重複工作）
- 完全放棄工作流程

### 3. 除錯和支援

Logging 讓你的支援團隊能看到失敗操作中發生了什麼，不需要請使用者重現問題。

---

## 產品設計考量

撰寫 MCP tool 需求時，考慮：

| Tool 耗時 | 建議 UX |
|-----------|---------|
| < 2 秒 | 不需要 notification |
| 2-10 秒 | Logging 訊息（「搜尋中...」「處理中...」） |
| 10-60 秒 | Logging + 進度條 |
| > 60 秒 | Logging + 進度 + 考慮拆成更小步驟 |

---

## Client 呈現靈活性

Server 發送原始資料，不同 client 有不同呈現方式：

| Client 類型 | Logging 呈現 | Progress 呈現 |
|------------|-------------|--------------|
| Terminal/CLI | stdout 文字行 | ASCII 進度條 |
| Web app | Toast 通知或 log panel | HTML/CSS 進度條 |
| Desktop app | 系統通知區域 | 原生 OS 進度環 |
| 聊天介面 | 行內狀態訊息 | 動態載入指示器 |

> **Key Insight**
> 作為 PM，你指定 **溝通什麼資訊**（步驟、百分比、警告）。你 **不需要** 指定 **怎麼顯示** — 那是 client 的責任。這種關注點分離意味著一個設計良好的 server 在所有 client 類型上都能表現出色。

---

## Notification 是 Fire-and-Forget

PM 需要理解的關鍵架構細節：

- Notification 是 **單向的**：server 發送，不等待確認
- Client 忽略它們也不會壞
- **不影響** tool 的實際輸出
- 對處理時間增加的額外開銷極小

這意味著你永遠可以建議加上 notification — 沒有缺點。

---

## 錯誤溝通策略

Logging level 對應使用者面向的溝通層級：

| Level | 何時使用 | 使用者體驗 |
|-------|---------|-----------|
| Debug | 內部細節（URL、記錄數） | 通常不顯示給終端使用者 |
| Info | 主要里程碑（「步驟 2/4 完成」） | 作為狀態顯示給使用者 |
| Warning | 效能降低（「大型資料集，可能較慢」） | 提醒 — 使用者可決定是否等待 |
| Error | 失敗（「資料庫連線中斷」） | 錯誤訊息 — 使用者採取行動 |

---

## CCA Exam Relevance

- **D2 Task 2.3**：Server capabilities — notification 在設計良好的 server 中是預期的
- **D2 Task 2.5**：Server-to-client communication — logging 和 progress 是主要範例
- 考試測試理解 notification 是單向的（非 request-response）
- 核心哲學：**好的 UX 不是可選項** — 即使基礎設施 tool 也應溝通狀態

---

## Flashcards

| Front | Back |
|-------|------|
| MCP server 可以發送哪兩種即時回饋？ | Logging（狀態訊息）和 Progress（完成百分比） |
| MCP notification 是 tool 功能必需的嗎？ | 不是 — 可選但強烈建議用於 UX |
| Client 忽略 notification 會怎樣？ | 不會壞 — notification 是 fire-and-forget |
| 為什麼進度指示器對 AI 工具很重要？ | 有進度回饋的任務使用者感覺更快，也更不容易放棄 |
| 誰決定 notification 怎麼顯示？ | Client — server 發送原始資料，每個 client 適當渲染 |
| PM 在什麼 tool 耗時下應建議加 notification？ | 超過 2 秒的操作 |
| 四個 logging level 是什麼？ | Debug（內部）、Info（里程碑）、Warning（降級）、Error（失敗） |
| Notification 可以改變 tool 的回傳值嗎？ | 不可以 — 純粹是資訊性的旁路溝通 |
