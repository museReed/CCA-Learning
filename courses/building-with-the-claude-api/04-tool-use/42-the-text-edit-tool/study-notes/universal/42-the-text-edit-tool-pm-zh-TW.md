# Text Editor Tool — PM Perspective

| 項目 | 內容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%)、D1 — Agentic Architecture (22%) |
| Task Statements | 2.3（built-in / server tools）、1.2（tool 編排） |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 42 |

---

## One-Liner

Text editor tool 讓你的產品可以在任意 workflow 中嵌入一個「迷你版 Claude Code」——Claude 已經知道怎麼編輯檔案，你只要提供一個可以寫入的沙盒環境。

---

## Mental Model：IKEA 家具組

從零買 tool 像是用原木打造一張椅子——每一處接合都得自己設計。Text editor tool 則像一套 IKEA 組合包：Anthropic 出所有零件（schema + 指令詞彙），你只要提供工作空間（你的檔案系統或沙盒）。

| 項目 | 自訂 Tool | Text Editor Tool |
|------|----------|------------------|
| Schema 定義 | 你寫 | Claude 內建 |
| 指令詞彙 | 你設計 | 預先定義（view、create、str_replace、insert、undo_edit） |
| 執行程式 | 你寫 | **還是你寫** |
| 沙盒 / 安全模型 | 你負責 | **還是你負責** |

加速效果真實存在，但安全責任完全沒變。

---

## 你的產品得到什麼

Text editor tool 立刻解鎖以下能力：

- **讀檔案**（任意粒度——整檔或特定行範圍）
- **列目錄**
- **建立新檔案**
- **在檔案中替換字串**
- **在指定行插入文字**
- **復原最近的編輯**

這是一個 code editor 的完整詞彙。你可以建構的產品：

- 接收 repo 與 style guide、自動重寫程式碼的 PR refactoring bot
- 把 Markdown 檔改寫成新 schema 的內容遷移 agent
- 讓 README 與 code 同步的文件自動更新器
- 為使用者沙盒設定 config 的 onboarding assistant

---

## Product Use Cases

### Text Editor Tool 發光發熱的時機

| 產品 | 適合度 | 原因 |
|------|-------|------|
| 程式碼重構工具 | 強 | 核心 loop 就是 view → edit → save |
| 文件生成器 | 強 | Claude 可以讀 code、建立文件檔 |
| 模板 scaffolder | 強 | Claude 以標準結構建立多個檔案 |
| 內部 developer agent | 強 | 聚焦於受控的 repo 沙盒 |
| 無頭自動化（CI） | 強 | 檔案是通用介面 |

### 不適合的情況

| 產品 | 更好的替代 |
|------|-----------|
| 結構化資料編輯（DB 記錄） | 用你的 DB schema 自己建 tool |
| UI / 視覺編輯 | 用專門的設計工具 |
| 單一原子內容編輯 | 直接產生文字，不走檔案 I/O |
| 協作即時文件編輯 | 改用 document-sync 服務 |

---

## 沙盒問題

既然由你的程式執行 Claude 的檔案指令，blast radius 就是你決定。這是 PM 的關鍵決策：

| 沙盒範圍 | 風險 | 使用情境 |
|---------|-----|---------|
| 整個檔案系統 | 極高——Claude 可寫任何地方 | 絕對不要上 production |
| 專案目錄 | 中等——有範圍但仍然不小 | 內部 developer 工具 |
| 獨立 workspace 目錄 | 低——邊界清楚 | 面向使用者的產品 |
| 只讀 | 極低 | 分析 / review agent |
| 虛擬檔案系統（記憶體） | 最低 | Preview-only 體驗 |

先用最嚴格的沙盒滿足產品價值，只有在明確理由下才放寬。

---

## PM Decision Framework

| 問題 | 如果 Yes | 行動 |
|------|---------|------|
| 產品的核心 workflow 是編輯檔案嗎？ | Yes | Text editor tool 很適合 |
| 能定義嚴格的沙盒目錄嗎？ | Yes | 可上 production |
| Claude 需要建立多個相關檔案嗎？ | Yes | Text editor 天然支援 |
| 使用者期待 undo 功能嗎？ | Yes | 在 handler 中實作 `undo_edit` |
| 產品需要寫入關鍵系統路徑嗎？ | Yes | **停下來**——改設計成沙盒化 |

---

## Hybrid 責任模型

這是 built-in tool 最重要的 PM insight：**Anthropic 擁有 schema，你擁有 runtime**。也就是說：

- 你決定「檔案」的定義（可以是 S3 物件、Git blob、記憶體字串）
- 你決定 `create` 的成本（例如按檔計費的產品）
- 你決定保留與 undo 行為
- 你決定 logging、稽核、合規

PM 有時以為 built-in = fully managed，其實不是。Built-in 只代表「schema 預先接好了」；所有營運面你還是要自己出。

---

## Common PM Mistakes

1. **以為 text editor tool 是 fully managed** — Anthropic 給 schema，但沙盒、安全、檔案操作都要你的團隊建。
2. **沒實作 `undo_edit`** — 編輯器類型的產品使用者期待 undo，忽略它會破壞心智模型。
3. **沙盒開太大就上線** — 「只有內部用」會擴散到 production；一開始就嚴格。
4. **忽略 audit logging** — Claude 的編輯必須可追蹤，才好 debug、合規、rollback。
5. **忘記 `view` 也能看目錄** — 這個 tool 是關於導覽，不只是編輯；list 與 read 都要支援。

> **Key Insight**
>
> Built-in tool 是 hybrid：Anthropic 出 schema，你出 runtime 與安全模型。Text editor tool 的產品價值是省去幾週的 schema / 指令設計工作，但沒省掉沙盒、稽核、undo 這些營運面工作。預算要抓好。

---

## CCA Exam Relevance

- **D2 (Tool Design)**：Text editor tool 是 built-in（schema 內建）tool 且需要開發者執行的典型。
- **D1 (Agentic Architecture)**：檔案操作是天然的多輪模式——view、edit、verify、重複。
- 考題常區分「built-in 但本地執行」（text editor）與「built-in 且託管執行」（web search）。

---

## Flashcards

| Front | Back |
|-------|------|
| Text editor tool 中 Anthropic 提供什麼？ | Schema 與指令詞彙——Claude 已經知道怎麼用 |
| 開發者還要提供什麼？ | 執行程式——真正在磁碟上讀、寫、建立、復原檔案 |
| 這個 tool 支援哪些檔案操作？ | view、create、str_replace、insert、undo_edit |
| 上線前 PM 最關鍵的決策是什麼？ | 沙盒——Claude 被允許動哪個目錄、路徑或虛擬檔案系統 |
| 為什麼這是 hybrid 責任模型？ | Schema 由 Anthropic 完全 managed，runtime 與安全完全由開發者負責 |
| 列出三個 text editor tool 很適合的產品。 | 重構 bot、文件生成器、模板 scaffolder |
| Tool 整合之外 PM 還要編哪些預算？ | 沙盒、稽核 logging、undo 行為、路徑驗證 |
| 如果 handler 沒實作 `undo_edit` 會怎樣？ | Claude 的 undo 嘗試靜默失敗，使用者心智模型被破壞 |
