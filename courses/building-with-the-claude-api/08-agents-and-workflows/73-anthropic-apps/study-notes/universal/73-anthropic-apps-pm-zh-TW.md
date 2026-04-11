# Anthropic Apps — PM Perspective（繁體中文）

| 項目 | 內容 |
|------|------|
| 考試 Domain | D1 — Agentic Coding & Architecture (22%) |
| Task Statements | 1.1（Claude Code 概觀）、1.2（agentic patterns）、1.4（Computer Use 作為 agent 案例） |
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 73 |

---

## 一句話總結

Claude Code 與 Computer Use 是 Anthropic 兩款旗艦 agent 產品 —— 是你設計 AI workflow 功能時的 UX、信任模型與價值主張的參考基準。

---

## 心智模型：實習生比喻

把三種介面想成三種不同的助手：

| 介面 | 對應的助手 | 可以請它做什麼 |
|------|-----------|----------------|
| Claude.ai | 聰明的朋友，用訊息問他 | 快速解答、草稿、發想 |
| Anthropic API | 工作檯上的零件盒 | 你自己組裝成產品 |
| **Claude Code** | 坐在你鍵盤旁的工程實習生 | 「修這個 bug、跑測試、開 PR」 |
| **Computer Use** | 操作電腦的虛擬操作員 | 「登入 dashboard、匯出報表、寄出 email」 |

PM 觀點：Claude.ai 是產品，API 是基礎建材，而 Claude Code 與 Computer Use 是 *agent 產品* —— 它們會做事，不只是回答。

---

## 為什麼 PM 應該在意

現今大多數 AI 功能還是聊天介面。真正有趣的產品類別（也是整個產業正在前進的方向）是 agent。Claude Code 與 Computer Use 正是兩種主要 agent 原型的最佳案例：

| 原型 | 範例 | 最適合的情境 |
|------|------|-------------|
| Domain-native agent | Claude Code（終端機、檔案工具） | 目標領域有乾淨、typed 的工具 |
| GUI-driving agent | Computer Use（透過截圖操作桌面） | 目標領域沒有 API，只有 UI |

規劃 AI 功能時，先決定屬於哪一種原型。Native agent 比較便宜、快速、可靠；GUI-driving agent 能解鎖其他方法碰不到的場景。

---

## 產品使用情境

### 適合採用 Domain-Native Agent（Claude Code 原型）

| 情境 | 為什麼合適 |
|------|-----------|
| 在 IDE 或 CLI 裡的開發者工具 | 已有乾淨的工具整合（檔案系統、git、language server） |
| SQL 資料庫的資料分析助手 | 可以開出 typed 工具 —— query、schema、metric catalog |
| 對接工單 API 的客服 operator | 有一等公民的 API，動作可靠、可稽核 |

### 適合採用 GUI-Driving Agent（Computer Use 原型）

| 情境 | 為什麼合適 |
|------|-----------|
| 自動化沒有 API 的老舊桌面軟體 | 只剩 UI 可用，agent 必須「看得懂並點得對」 |
| 跨第三方網頁應用的 QA 測試 | 需要視覺回歸與互動流程 |
| 取代脆弱 macro 的企業 RPA | Agent 能用 vision 適應 layout 變動 |

### 不該用的情境

| 情境 | 更好的替代 |
|------|-----------|
| 應用程式內的簡單問答 | 直接用 API 做 chat，不需要 agent |
| 完全確定的固定流程 | 傳統 workflow / RPA 腳本即可，不用 LLM |
| 極低延遲的即時需求 | 走固定程式碼 —— agent loop 太慢 |

---

## PM 決策框架

看到一個新的「AI 功能」提案時，問這些問題：

1. **這真的是 agent 嗎？** 是否需要多步驟工具執行、環境互動、自主決策？如果不用，那是 chat 功能 —— 風險小，天花板也低。
2. **適合哪種原型？** Native tool 風格（Claude Code）或 GUI-driving 風格（Computer Use）？
3. **信任邊界在哪？** Agent 代替使用者行動。人類在哪一步核准？
4. **失敗模式是什麼？** 檔案毀損、誤點、不可逆動作 —— 先設計保險再動工。
5. **參考實作教了我們什麼？** 兩個 app 都有 permission prompt、memory（CLAUDE.md）、迭代式 workflow —— 直接借走這些 pattern。

---

## 信任與控制的取捨

Agent 強大之處在於會「行動」，這同時是風險來源。Claude Code 與 Computer Use 都示範了這個光譜：

| 控制層級 | Claude Code 行為 | 使用者體驗 |
|---------|-----------------|-----------|
| 唯讀 | 先顯示計畫，要求核准 | 安全但慢 |
| 逐步確認 | 每次編輯或 shell 指令前詢問 | 平衡 |
| 自動核准 | 一次執行一整批變更 | 快但風險高 |

PM 的任務是挑一個預設值並提供合理的逃生門。課程講得很明白：好的 agent 是 **協作夥伴**，不是完全自主的行動者。

---

## 常見 PM 錯誤

1. **只說「做一個 agent」卻沒定義原型** —— native-tool agent 與 GUI-driving agent 的成本和可靠度差很多。
2. **以為 Claude.ai 的 UX 可以直接套到 agent** —— agent 需要計畫介面、權限確認、復原機制，而 chat UI 沒有這些。
3. **忽略 context 問題** —— Claude Code 大量投資在 CLAUDE.md，因為 context 管理佔了一半工作。臨時 prompt 無法 scale。
4. **把 Computer Use 當成「省下做 API 的便宜替代」** —— 它可行，但更慢、更脆弱、更花 token。能做 API 就先做 API。
5. **為了「更自主」跳過人類核准步驟** —— 對任何破壞性動作，核准不是可選項目。

> **關鍵洞察**
>
> Claude Code 與 Computer Use 不只是產品，而是 **PM 層級的參考設計** —— 對應兩種主流 agent 原型：native-tool agent 與 GUI-driving agent。研究它們的 UX 抉擇（權限確認、持久 memory 檔、「先規劃再執行」流程），你就有一份自己 agent 功能的設計範本。

---

## CCA 考試重點

- **D1（Agentic Coding & Architecture）**：看到「這是不是 agent」的情境時，要能對應到四項特性。
- **D3（Claude Code Configuration）**：這 lesson 是後續 Claude Code 重頭戲題組的入口，先記住應用分類語彙。
- 題目常對比 chat、API、agent —— 要知道每種扮演什麼角色。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Anthropic 的兩款旗艦 agent 應用是什麼？ | Claude Code 與 Computer Use |
| 實習生比喻中，Claude Code 等同什麼角色？ | 坐在你鍵盤旁、實際動手做事的工程實習生 |
| 本 lesson 提出的兩種主流 agent 原型是什麼？ | Domain-native agent（Claude Code 風格）與 GUI-driving agent（Computer Use 風格） |
| PM 何時應優先選 native-tool agent 而非 GUI-driving？ | 只要目標領域有乾淨 API 或 typed 工具 —— 便宜且可靠 |
| GUI-driving agent 適合什麼時候用？ | 目標 app 沒有 API 只有 UI（老舊桌面軟體、第三方 dashboard） |
| PM 必須管理的信任取捨是什麼？ | Agent 代替使用者行動 —— 必須在唯讀、逐步確認、自動核准之間選擇預設值 |
| 為什麼 CLAUDE.md 對 PM 有意義？ | 它示範了「持久 context」這個產品 pattern —— 提醒 agent UX 不只是 prompt，還包含記憶 |
| Computer Use 能取代建置正式 API 嗎？ | 不行 —— 它只是沒 API 時的 fallback，速度較慢、較脆弱、成本較高 |
