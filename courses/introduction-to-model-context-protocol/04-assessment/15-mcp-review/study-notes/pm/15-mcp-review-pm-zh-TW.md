# MCP 複習 — PM 視角

| 項目 | 細節 |
|------|--------|
| 考試範疇 | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server primitives), 2.4-2.6 (resource/tool/prompt design), 1.1 (agentic architecture) |
| 來源 | introduction-to-model-context-protocol / 04-assessment / Lesson 15 |

---

## 一句話摘要

MCP 有三個 AI 產品建構模組 — Tools（AI 決定）、Resources（app 決定）、Prompts（使用者決定）— 知道該用哪個是 PM 影響的最重要架構決策。

---

![Three Primitives](../../visuals/three-primitives-zh-TW.svg)


## 三大建構模組：商業類比

把 MCP 驅動的產品想像成一間**智慧辦公室**：

| 建構模組 | 辦公室類比 | 誰決定 | 產品範例 |
|----------------|---------------|-------------|-----------------|
| **Tools** | 你請的專業顧問 — 他們決定跑什麼分析、何時跑 | Claude（AI） | Claude 在幕後執行計算 |
| **Resources** | 研究助理在會議前預先收集簡報資料 | 你的 app | Google Drive 文件注入聊天 context |
| **Prompts** | 員工遵循的作業手冊 — 他們選擇何時使用 | 使用者 | 使用者點擊「摘要」工作流程按鈕 |

---

## 為什麼 PM 需要理解

你規格的每個 AI 功能都歸入三個類別之一，基於**誰應該控制它**：

### 1. Tools — 「讓 AI 決定」

**何時使用**：AI 需要能力來自主完成任務。

| 產品場景 | 為什麼用 Tools |
|-----------------|-----------|
| AI 在聊天中計算運費 | AI 決定何時需要計算 |
| AI 查詢庫存資料庫 | AI 根據對話決定檢查庫存 |
| AI 發送通知 email | AI 決定發送的正確時機 |

**PM 考量**：Tools 對使用者不可見。使用者不點按鈕；AI 自己決定。

### 2. Resources — 「讓 App 決定」

**何時使用**：你的應用需要資料用於顯示或預載 context。

| 產品場景 | 為什麼用 Resources |
|-----------------|---------------|
| 自動完成下拉顯示可用文件 | App 為 UI 取得列表 |
| 使用者輸入 `@report.pdf` 引用檔案 | App 將內容注入 prompt |
| 側邊欄顯示相關文件 | App 決定什麼 context 相關 |

**PM 考量**：Resources 讓體驗感覺即時。資料在 AI 開始思考前就預載好了。

### 3. Prompts — 「讓使用者決定」

**何時使用**：你想要使用者明確觸發的預定義、可重複工作流程。

| 產品場景 | 為什麼用 Prompts |
|-----------------|-------------|
| `/format` slash command | 使用者決定重新格式化 |
| 「生成週報」按鈕 | 使用者按需觸發 |
| 「翻譯成西班牙文」選單選項 | 使用者啟動工作流程 |

**PM 考量**：Prompts 封裝專業知識。使用者不需要自己寫指令就能獲得專家級結果。

---

## PM 決策框架

撰寫 AI 功能的 PRD 時，用這個流程：

**問題 1**：「誰應該決定何時發生？」
- **AI 自主決定** → Tool
- **App 預載資料** → Resource
- **使用者明確觸發** → Prompt

**問題 2**：「這涉及讀取資料還是執行動作？」
- **讀取資料用於顯示或 context** → Resource
- **執行有潛在副作用的動作** → Tool
- **遵循預定義工作流程** → Prompt

**問題 3**：「如果出錯會怎樣？」
- **嚴重後果（財務、合規）** → Tool + 防護（hooks）
- **輕微 UX 問題** → 任何 primitive，按控制模型選
- **工作流程不一致** → Prompt（為了可重複性）

---

## 它們如何協作：一個產品故事

想像一個文件管理 AI 助手：

1. **Resources** 驅動 `@mention` 自動完成 — 使用者輸入 `@` 時，app 從 MCP server 取得可用文件
2. **Prompts** 驅動 `/format` 命令 — 使用者選擇文件並觸發格式化工作流程
3. **Tools** 驅動實際編輯 — Claude 使用 `edit_document` tool 以 markdown 重寫內容

三個 primitives 都需要。Resources 處理資料，prompts 處理工作流程，tools 處理動作。

---

## PM 在 Primitive 選擇上的常見錯誤

| 錯誤 | 後果 | 正確做法 |
|---------|------------|-----------------|
| 對唯讀資料顯示指定 tool | 更慢的 UX（tool call 開銷） | 用 resource — 即時 context 注入 |
| 對使用者觸發的工作流程指定 tool | 結果不一致（AI 可能不完全遵循） | 用 prompt — 測試過的模板，一致的輸出 |
| 對有副作用的動作指定 resource | 違反唯讀契約 | 用 tool — 只有 tools 該有副作用 |
| 對自主 AI 行為指定 prompt | 使用者每次都要手動觸發 | 用 tool — 讓 AI 決定 |

---

## 主表格：考試準備總結

| 面向 | Tools | Resources | Prompts |
|-----------|-------|-----------|---------|
| 控制者 | AI（model） | App 程式碼 | 使用者 |
| 觸發 | AI 推理 | App 邏輯 | `/` 命令或按鈕 |
| 副作用？ | 有 | 無（唯讀） | 無（只有訊息） |
| UX 模式 | 不可見 | `@mention` | Slash commands |
| 產品類比 | 顧問 | 研究助理 | 作業手冊 |
| 考試關鍵字 | 「自主地」、「Claude 決定」 | 「預載」、「UI 資料」 | 「工作流程」、「slash command」 |

> **Key Insight**
>
> 三方控制模型是產品設計和 CCA 考試中最重要的單一概念。每個「該用哪個 primitive？」的問題都歸結為：「誰應該控制這個互動？」Model = Tool、App = Resource、User = Prompt。掌握這個框架就能回答任何 D2 情境題。

---

## CCA 考試關聯

- **D2 (Tool Design & MCP Integration)**：這是總結概念。知道三個 primitives、它們的控制模型、以及何時使用。
- **D1 (Agentic Architecture)**：控制模型對應架構層 — 模型層（tools）、應用層（resources）、使用者層（prompts）。
- **考試策略**：讀情境、辨識控制者（誰決定行動）、選對應的 primitive。這對 90%+ 的 D2 題目有效。

---

## Flashcards

| 正面 | 背面 |
|-------|------|
| MCP 三個 server primitives 及其控制者是什麼？ | Tools（Claude model-controlled）、Resources（app 程式碼 controlled）、Prompts（使用者 controlled） |
| 解決大多數「哪個 primitive？」決策的單一問題是什麼？ | 「誰應該控制這個互動？」— Model = Tool、App = Resource、User = Prompt |
| 三個 MCP primitives 的辦公室類比是什麼？ | Tools = 專業顧問（AI 決定）、Resources = 研究助理（app 預先收集）、Prompts = 作業手冊（使用者遵循） |
| PM 何時該在 PRD 中指定 Tool？ | AI 需要自主決定執行動作時（計算、API 呼叫、副作用） |
| PM 何時該在 PRD 中指定 Resource？ | App 需要唯讀資料用於 UI 顯示或在 AI 推理前預載 context |
| PM 何時該在 PRD 中指定 Prompt？ | 使用者應明確觸發預定義、可重複工作流程時（slash commands、按鈕） |
| PM 在 primitive 選擇中最大的錯誤是什麼？ | 該用 Resource 的場景用了 Tool — 為唯讀資料增加延遲和 tool call 開銷 |
| 三個 primitives 在產品中如何協作？ | Resources 供給資料到 UI、Prompts 讓使用者觸發工作流程、Tools 讓 Claude 執行動作完成工作流程 |
