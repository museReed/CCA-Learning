# The Server Inspector — PM 策略概覽

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | T2.6 測試與除錯 MCP server; T2.7 部署前驗證 tool 行為 |
| Source | introduction-to-model-context-protocol / 02-tools-and-inspector / Lesson 07 |

---

## 一句話摘要

MCP Inspector 是 AI 工具的試駕環境——就像展示間，你可以在投入生產前試用任何 tool。

---

## 為什麼 PM 應關心 Inspector

MCP Inspector 是開發工具，但它對產品有直接影響。它是你能看到 Claude 看到什麼的地方——tool 的名稱、描述和參數。如果在 Inspector 中看起來令人困惑，對 Claude 也會令人困惑，最終對使用者也是如此。

把 Inspector 想成**產品預覽環境**。在 tools 上線之前，你可以驗證：

- Tool 名稱是否直觀？
- 描述是否清楚到讓 Claude 選對 tool？
- 參數名稱和描述是否不言自明？
- 錯誤訊息是否幫助 Claude 優雅復原？

> **PM Takeaway**
> 安排團隊的 Inspector 審查會議。讓 PM 在 Inspector 中看 tool 描述，常能抓到工程師忽略的清晰度問題——因為他們已經知道 tool 做什麼。

---

## Inspector 作為品質關卡

在製造業中，產品出貨前會經過品質檢查站。MCP Inspector 對 AI tools 提供同樣的功能：

**沒有 Inspector 測試**：寫 tool → 部署 → 使用者遇到問題 → 在生產環境除錯

**有 Inspector 測試**：寫 tool → 在 Inspector 測試 → 修正問題 → 部署 → 使用者得到完善的體驗

Inspector 在問題觸達使用者前攔截三類問題：

1. **功能 bug** — Tool 沒有回傳正確結果
2. **Schema 問題** — 參數型別錯誤、缺描述、或錯誤標記為必填/選填
3. **UX 問題** — 描述模糊、錯誤訊息無幫助、回傳值格式差

> **PM Takeaway**
> 為任何新的 MCP tool 加上「Inspector 已測試」作為完成定義。沒有通過 Inspector 驗證的 tool 不應進入生產環境。

---

## Inspector 中你看到什麼

Inspector 呈現三類 MCP server 能力：

**Resources 頁籤** — 想像成「資料圖書館」書架。Server 能提供什麼資訊？檔案、資料庫記錄、設定資料等。

**Tools 頁籤** — 想像成「動作」選單。Server 能做什麼？建立檔案、查詢資料庫、發送訊息等。

**Prompts 頁籤** — 想像成「範本」抽屜。Server 提供什麼預寫的 prompt 模式？

產品評估時，你大部分時間都在 Tools 頁籤。每個 tool 條目顯示 Claude 決定是否使用它時看到的完全相同的內容。

---

## 狀態持久性：測試真實工作流

Inspector 的關鍵功能之一是 tool 狀態在呼叫之間持久存在。用產品語言來說，這意味著你可以測試完整的使用者工作流，而不只是孤立的動作。

多步驟工作流測試範例：

1. 建立文件（tool 呼叫 1）
2. 讀取文件以驗證正確建立（tool 呼叫 2）
3. 編輯文件（tool 呼叫 3）
4. 再次讀取以驗證編輯（tool 呼叫 4）

這映射真實使用者與你的產品互動的方式。每一步都依賴前一步，Inspector 讓你驗證整條鏈路都正確運作。

> **PM Takeaway**
> 在 Inspector 中審查 tools 時，不要只測快樂路徑。測試使用者實際會遵循的序列——包括邊界情況，如讀取不存在的文件，或編輯別人正在處理的文件。

---

## 開發回饋迴圈

Inspector 啟用了緊密的回饋迴圈，加速 tool 開發：

**傳統方式**（沒有 Inspector）：
1. 寫 tool 程式碼
2. 建 client 整合
3. 連接 Claude
4. 發送測試查詢
5. 如果出問題，找出哪一層失敗
6. 修正並從步驟 2 重新開始

**Inspector 方式**：
1. 寫 tool 程式碼
2. 開啟 Inspector
3. 直接測試 tool
4. 如果出問題，一定是 tool 程式碼的問題
5. 修正並立即重新測試

Inspector 方式更快是因為它消除了變數。當 tool 在 Inspector 中失敗時，你知道問題在 tool 程式碼中，不在 client、不在傳輸層、也不在 Claude 的解讀中。

---

## 連結 Inspector 洞察到產品決策

在 Inspector 中測試後，PM 可以對以下做出明智決策：

- **Tool 命名慣例** — Tools 命名是否一致？使用者能猜出「proc_doc_v2」做什麼嗎？
- **描述品質** — 只讀描述就能理解每個 tool 做什麼嗎？
- **參數設計** — 必填參數是否太多？預設值是否合理？
- **錯誤體驗** — 出問題時，錯誤訊息是否指向解決方案？

這些都是碰巧存在於程式碼中的產品設計決策。

---

## CCA 考試關聯性

本課涵蓋 **Domain 2 (18%)** 的測試概念：

- Inspector 透過 `mcp dev mcp_server.py` 在 `localhost:6274` 啟動
- 三個頁籤：Resources、Tools、Prompts
- 狀態在呼叫之間持久存在，支援多步驟測試
- Inspector 位於開發和 client 整合之間的工作流中

---

## Flashcards

| Front | Back |
|-------|------|
| 用商業語言描述 MCP Inspector 是什麼？ | AI 工具的試駕環境，你可以在上線前預覽和測試——就像 tool 能力的 staging 環境。 |
| 為什麼 PM 應該在 Inspector 中審查 tools？ | Tool 描述、參數名稱和錯誤訊息是直接影響 Claude 使用 tools 和使用者體驗產品的產品設計決策。 |
| Inspector 顯示哪三類內容？ | Resources（server 提供的資料）、Tools（server 能執行的動作）和 Prompts（可重用範本模式）。 |
| 狀態持久性對測試意味著什麼？ | 你可以測試每個 tool 呼叫依賴前一個呼叫的多步驟工作流，映射真實使用者的互動模式。 |
| Inspector 如何減少除錯時間？ | 它把 tool 問題從 client、傳輸和 Claude 解讀問題中隔離出來。如果 tool 在 Inspector 中失敗，問題一定在 tool 程式碼中。 |
| 新 MCP tools 的「完成定義」應是什麼？ | Inspector 已測試——沒有通過功能、schema 正確性和描述品質的 Inspector 驗證，tool 不應進入生產環境。 |
| PM 可以透過 Inspector 測試做出什麼產品決策？ | Tool 命名慣例、描述品質、參數設計、預設值和錯誤訊息的有用性。 |
| Inspector 如何融入開發工作流？ | 寫 tool 程式碼 → 用 Inspector 測試 → 修正問題 → 與 client 整合。跳過 Inspector 測試會導致後續更難診斷的問題。 |
