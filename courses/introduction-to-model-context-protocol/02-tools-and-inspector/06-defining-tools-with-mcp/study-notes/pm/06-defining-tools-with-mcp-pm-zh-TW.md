# Defining Tools with MCP — PM 策略概覽

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | T2.1 設計與實作 tool schemas; T2.5 使用 MCP SDK 定義型別安全的 tools |
| Source | introduction-to-model-context-protocol / 02-tools-and-inspector / Lesson 06 |

---

## 一句話摘要

MCP SDK 把 tool 建立從為期數週的規格撰寫專案，變成寫一個帶好描述的 Python 函式——大幅降低給 Claude 新能力所需的工程量。

---

![Tools Decorator](../../visuals/tools-decorator-zh-TW.svg)


## 舊方式：規格驅動開發

在 MCP SDK 之前，讓 Claude 存取新 tool 需要一個多步驟流程，很像撰寫法律合約：

1. **寫 JSON schema** — 每個參數、其型別、約束和描述的正式規格
2. **寫 handler 函式** — 實際做事的程式碼
3. **保持同步** — 每次函式改變，schema 也必須改
4. **測試 schema** — 驗證 Claude 正確解讀 schema

這就像要求每個員工在做任何工作之前先寫正式職位描述，然後每次職責變更時更新那份文件。

> **PM Takeaway**
> 舊方式造成「tool 瓶頸」——每個新能力都需要先完成 schema 規格工作才能建任何實際功能。FastMCP 完全移除了這個瓶頸。

---

## 新方式：直接寫函式

用 FastMCP，工程工作流大幅簡化：

1. 寫一個做你想做的事的 Python 函式
2. 加一個裝飾器（`@mcp.tool()`）
3. 寫一個好的 docstring 解釋它做什麼

就這樣。SDK 自動從程式碼本身產生正式規格。函式本身就是規格。

想像兩者的差異：

- **舊方式**：撰寫詳細的 10 頁需求文件、取得核准、然後聘請承包商做事
- **新方式**：在對話中描述你需要什麼，工作立即開始

給 PM 的關鍵洞察是 **tool 描述的品質**（docstring）直接影響 Claude 使用 tool 的效果。這是產品思維重要的地方——不在技術 schema，而在清楚表達 tool 做什麼、何時使用、回傳什麼。

> **PM Takeaway**
> Tool 描述是產品設計決策，不只是技術細節。寫得好的描述意味著 Claude 在正確的時間選擇正確的 tool。模糊的描述意味著 Claude 犯錯或完全忽略 tool。

---

## 為什麼描述是產品決策

當 Claude 收到使用者查詢時，它會讀過所有可用的 tool 描述並決定使用哪個（如果有的話）。這就像客戶在目錄中閱讀產品描述。

考慮同一個 tool 的兩種描述：

**模糊**：「讀取文件」

**精確**：「讀取並回傳指定檔案路徑的完整文字內容。當使用者詢問文件內容、需要檢閱檔案、或想在文件中搜尋時使用。」

精確的描述給 Claude 清楚的信號，說明何時及如何使用 tool。模糊的描述留下太多歧義。

這直接映射到產品文案撰寫——描述越清楚，使用者體驗越好。

---

## 錯誤訊息即使用者體驗

當 tools 失敗時，Claude 收到的錯誤訊息決定它如何優雅地處理情況。好的錯誤訊息就像好的客服培訓：

**差的錯誤**：「操作失敗」
- Claude 告訴使用者：「出了問題。請再試一次。」

**好的錯誤**：「在 /reports/q3.pdf 找不到文件。reports 目錄包含：q1.pdf、q2.pdf、q4.pdf」
- Claude 告訴使用者：「我找不到 q3.pdf，但我看到有 q1、q2 和 q4 報告。要我讀其中一個嗎？」

> **PM Takeaway**
> 錯誤訊息是使用者體驗的一部分，即使使用者從未直接看到。它們決定 Claude 是優雅復原還是給出死胡同回應。審查 tool 規格時，永遠檢查錯誤處理設計。

---

## 驗證安全網

FastMCP 在 tool 程式碼執行前自動驗證輸入。這就像在生產線前設置品質管控檢查站：

- 如果 Claude 發送數字而預期是文字字串，驗證會攔截
- 如果缺少必填欄位，驗證會攔截
- 如果值超出允許範圍，驗證會攔截

這意味著 tool 開發者可以專注於「快樂路徑」——輸入正確時會發生什麼——讓 SDK 處理輸入錯誤。更少 bug、更少防禦性程式碼、更快開發。

---

## 對產品團隊的策略影響

**更快的能力擴展**：為 AI 產品新增 tool 從數天降到數小時。這意味著產品可以更快回應使用者回饋和市場需求。

**更低的工程門檻**：初級開發者也能建立 MCP tools。SDK 處理複雜的協定細節，開發者專注於商業邏輯。

**更好的 tool 品質**：自動驗證在 bug 觸達使用者前攔截。Schema-程式碼同步消除了整類「測試時能用但生產環境失敗」的問題。

**描述驅動設計**：PM 能做的最有影響力的事是確保 tool 描述清楚、具體、且與使用者意圖對齊。這是產品專業直接改善 AI 表現的地方。

---

## CCA 考試關聯性

本課涵蓋 **Domain 2 (18%)**，重點在：

- 理解 `@mcp.tool()` 從 Python 函式自動產生 schema
- 知道 docstring 變成 Claude 用於選擇的 tool 描述
- 辨認好的描述改善 tool 選擇準確度
- 理解驗證和錯誤處理模式

---

## Flashcards

| Front | Back |
|-------|------|
| MCP SDK 從 tool 建立流程中消除了什麼？ | 手動 JSON schema 撰寫。SDK 從 Python 函式簽章和 type hints 自動產生 schema。 |
| 為什麼 tool 描述是產品決策？ | 因為 Claude 讀描述來決定用哪個 tool。清楚、具體的描述帶來更好的 tool 選擇和更好的使用者體驗。 |
| 好的和差的 tool 錯誤訊息有什麼區別？ | 好的錯誤包含上下文（什麼出錯、有什麼替代方案）。差的錯誤是通用的（「失敗」）。好的錯誤讓 Claude 優雅復原。 |
| FastMCP 中「自動驗證」是什麼意思？ | SDK 在 tool 程式碼執行前自動檢查 Claude 的 tool 輸入是否符合預期型別和約束，及早攔截錯誤。 |
| FastMCP 如何影響開發速度？ | 新增 tool 從數天（手動 schema + handler + 測試）降到數小時（寫函式 + 裝飾器 + docstring）。 |
| PM 能為 MCP tools 做的最有影響力的事是什麼？ | 確保 tool 描述清楚、具體、且與使用者意圖對齊——這直接影響 Claude 選擇和使用 tools 的效果。 |
| FastMCP 中 schema-程式碼同步如何運作？ | Schema 從程式碼本身產生，所以它們永遠不會不同步。函式的變更自動更新 schema。 |
| Claude 發送無效輸入到 FastMCP tool 時會發生什麼？ | Pydantic 驗證在 tool 函式執行前攔截型別錯誤，回傳清楚的錯誤訊息給 Claude。 |
