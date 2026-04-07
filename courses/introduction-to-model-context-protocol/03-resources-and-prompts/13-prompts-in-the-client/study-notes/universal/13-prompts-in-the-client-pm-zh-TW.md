# Client 端的 Prompts — PM 視角

| 項目 | 細節 |
|------|--------|
| 考試範疇 | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP client implementation), 2.6 (prompt consumption patterns), 1.3 (prompt orchestration) |
| 來源 | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 13 |

---

## 一句話摘要

Client 端的 prompt 整合就像在產品中安裝「快速操作」選單 — 使用者看到一個策展過的專家工作流程清單，選一個、填入細節，每次都得到一致的結果。

---

## 為什麼 PM 需要理解 Client 端 Prompts

本課完成了 prompts 端到端運作的全貌。PM 需要知道：

1. **使用者如何發現 prompts** — 透過 slash commands、按鈕或選單
2. **使用者如何參數化 prompts** — 需要提供什麼輸入
3. **Prompts 如何編排 tools** — prompts 給指令，tools 做工作
4. **三方控制模型** — 所有 MCP 架構決策的基礎

---

## 心智模型：自助點餐機

把三種 MCP primitives 想像成速食餐廳的不同點餐體驗：

| 體驗 | MCP Primitive | 誰決定 | 點餐機類比 |
|------------|---------------|-------------|---------------|
| 廚房決定煮什麼 | **Tool** | 主廚（Claude） | 廚房做他們覺得你需要的東西 |
| 飲料機自動倒水 | **Resource** | 餐廳系統（app） | 水自動出現在你桌上 |
| 自助點餐機點餐 | **Prompt** | 顧客（使用者） | 你點「3 號套餐」、客製配料、確認 |

---

## 端到端使用者旅程

### 步驟 1：發現
使用者在聊天中輸入 `/`。下拉選單出現顯示可用工作流程：
- `/format` — 將文件轉寫為 Markdown
- `/summarize` — 建立文件摘要
- `/analyze` — 生成分析報告

### 步驟 2：選擇與參數
使用者選擇 `/format`。系統詢問必要資訊：
- 「哪份文件？」— 顯示文件選擇器

### 步驟 3：執行
使用者確認。幕後：
1. Prompt 模板填入使用者的參數
2. 指令發送給 Claude
3. Claude 讀取文件（使用 tools）並重新格式化
4. 結果出現在聊天中

### 步驟 4：結果
使用者看到專業格式化的 markdown 文件。每次相同品質，不論使用者的 prompt engineering 能力。

---

## 三方控制模型 — 主框架

這是 Chapters 2-3 中最重要的概念，也是 CCA 考試的基石：

| Primitive | 控制者 | 考試關鍵字 | 產品範例 |
|-----------|-----------|-------------|-----------------|
| **Tools** | Claude（model-controlled） | 「Claude 決定」、「自主地」 | Claude 在幕後執行計算 |
| **Resources** | 應用程式（app-controlled） | 「預載」、「UI context」 | Google Drive 文件注入聊天 |
| **Prompts** | 使用者（user-controlled） | 「Slash command」、「workflow 按鈕」 | 使用者點擊「摘要」工作流程按鈕 |

### PM 決策流程

設計功能時，問：

1. 「誰應該決定何時發生這件事？」
   - **使用者明確觸發** → Prompt
   - **Claude 在推理時決定** → Tool
   - **App 自動預載** → Resource

2. 「這是有已知步驟的可重複工作流程嗎？」
   - **是** → Prompt
   - **否，是即興的** → 讓 Claude 用 tools 處理

---

## Prompts + Tools：編排模式

PM 的關鍵洞察：**prompts 不取代 tools — 它們編排 tools**。

| Prompts 做什麼 | Tools 做什麼 |
|-----------------|---------------|
| 提供專家指令 | 執行特定動作 |
| 定義「做什麼」 | 處理「怎麼做」 |
| 使用者控制的觸發 | 模型控制的執行 |

**PM 意涵**：撰寫 prompt 驅動功能的 PRD 時，需確保必要的 tools 也可用。沒有必要 tools 的 prompt 就像沒有食材的食譜。

---

## 產品設計考量

### Prompt 可發現性
- 使用者如何找到可用 prompts？（Slash 選單、工具列、新手引導）
- Prompts 是否應分類？（按任務類型、使用頻率）
- 對新使用者，`/` 提示應多顯眼？

### 參數體驗
- 每個 prompt 需要什麼參數？
- 參數能從 context 自動填入嗎？（當前文件、選取的文字）
- 缺少必要參數時會發生什麼？

---

## PM 常見錯誤

1. **把 prompts 設計成 tools** — 使用者觸發的就是 prompt；Claude 決定的就是 tool
2. **忘記 tool 依賴** — prompts 通常需要 tools 來完成指令；確保兩者都可用
3. **選擇過多** — 策展 5-10 個高價值 prompts，而非 50 個很少用的
4. **沒有參數預設值** — 從 context 預填參數（當前文件、選取文字）來減少摩擦

> **Key Insight**
>
> 三方控制模型是所有 MCP 架構決策的主框架：Tools = model-controlled、Resources = app-controlled、Prompts = user-controlled。對 PM 來說，這直接轉化為產品設計：「誰啟動這個動作？」決定該用哪個 primitive。CCA 考試中，這個區分幾乎出現在每一題 D1 和 D2 情境題中。

---

## CCA 考試關聯

- **D2 (Tool Design & MCP Integration)**：知道兩個 client 方法（`list_prompts` 和 `get_prompt`）以及 slash command UX 模式。
- **D1 (Agentic Architecture)**：三方控制模型是最常考的概念。
- **考試信號詞**：「slash command」/「workflow button」/「user triggers」→ Prompt。「Claude decides」/「autonomously」→ Tool。「Pre-loaded context」/「UI data」→ Resource。

---

## Flashcards

| 正面 | 背面 |
|-------|------|
| 三種 MCP 控制模型是什麼？ | Tools = model-controlled（Claude 決定）、Resources = app-controlled（app 程式碼決定）、Prompts = user-controlled（使用者決定） |
| Prompts 的 slash command 模式是什麼？ | 使用者輸入 `/`、看到可用 prompts、選擇一個、提供參數、系統將插值訊息發送給 Claude |
| Prompts 和 tools 如何協作？ | Prompts 提供「做什麼」（指令），tools 提供「怎麼做」（能力）— Claude 使用 tools 完成 prompt 指令 |
| Prompts 的自助點餐機類比是什麼？ | 使用者從策展選單（prompts）中選擇、客製選項（參數），得到一致結果 |
| PM 設計 prompt 驅動功能時應確保什麼？ | 必要的 tools 也可用 — 沒有必要 tools 的 prompt 就像沒有食材的食譜 |
| PM 如何在 prompt、tool 和 resource 之間做決定？ | 問「誰應該決定何時發生？」— 使用者觸發 = Prompt、Claude 決定 = Tool、App 預載 = Resource |
| 什麼考試信號詞表示答案是 prompt？ | 「Slash command」、「workflow button」、「user triggers」、「predefined workflow」 |
| Claude 介面中三種 primitive 的範例各是什麼？ | Prompts = 聊天下方的 workflow 按鈕、Resources = 「Add from Google Drive」、Tools = 幕後程式碼執行 |
