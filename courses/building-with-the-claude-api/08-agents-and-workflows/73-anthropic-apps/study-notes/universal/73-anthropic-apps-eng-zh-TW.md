# Anthropic Apps — Engineering Deep Dive（繁體中文）

| 項目 | 內容 |
|------|------|
| 考試 Domain | D1 — Agentic Coding & Architecture (22%) |
| Task Statements | 1.1（Claude Code 概觀）、1.2（agentic patterns）、1.4（Computer Use 作為 agent 案例） |
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 73 |

---

## 一句話總結

Anthropic 推出兩款旗艦 agent 應用程式 —— Claude Code（終端機編碼助手）與 Computer Use（桌面互動工具組），兩者都是 agentic loop 的標準參考實作：tool integration、多步驟執行、環境互動與自主解題。

---

## Anthropic 的應用程式介面

Anthropic 透過多個介面提供 Claude，本模組聚焦在兩個展現 agent 設計精髓的介面：

| 介面 | 形式 | 是否為 agent | 用途 |
|------|------|-----------|------|
| Claude.ai | 網頁聊天介面 | 對話式、工具有限 | 一般消費者助手 |
| Anthropic API | HTTP endpoint | 基礎建材 —— 由你來組 agent | 開發者平台 |
| **Claude Code** | 終端機 CLI | **是 —— 完整 agent** | 編碼 agent |
| **Computer Use** | 桌面工具組 | **是 —— 完整 agent** | 操作 GUI 的 agent |

Claude Code 和 Computer Use 並不只是「剛好用到 Claude 的產品」，它們示範了一個建構良好的 agent 長什麼樣子，而且直接對應到你之後要在 API 上自行建立的 pattern。

---

## 為什麼這些應用程式算是 Agent

課程將 agent 定義為同時具備四項特性的系統。Claude Code 與 Computer Use 都符合全部四項：

| 特性 | Claude Code 範例 | Computer Use 範例 |
|------|------------------|-------------------|
| **Tool integration** | 檔案編輯、shell 執行、web fetch、MCP | 截圖、滑鼠點擊、鍵盤輸入 |
| **多步驟任務執行** | Plan → 讀檔 → 編輯 → 測試 → commit | 開瀏覽器 → 導覽 → 填表 → 送出 |
| **環境互動** | 讀寫檔案系統和 shell | 讀寫桌面 GUI 狀態 |
| **自主解題** | 測試失敗時反覆除錯 | 頁面重載後自動重試點擊 |

每一輪都會把 tool 回傳結果餵回下一輪給 model，形成標準的 tool-use loop，直到達成自然停止條件為止（`end_turn` stop_reason，或主程式端設的最大輪數保險絲）。

---

## Claude Code：終端機原生 Agent

Claude Code 在終端機裡跑成一個持續 process。主要特性：

- **介面**：CLI，不是網頁聊天室
- **內建工具**：檔案讀寫、grep/glob、bash 執行、web fetch、to-do 規劃
- **擴充點**：MCP servers（Lesson 76 會講）
- **Context 策略**：專案層級的 `CLAUDE.md` memory file，提供持續 context
- **認證**：跑 `claude` 指令並登入 Anthropic 帳號

你可以把 Claude Code 想成「由人類打英文、Claude 打程式碼」的 IDE。Agent 負責：
1. 理解需求
2. 讀足夠多的 codebase 來擬計畫
3. 編輯檔案
4. 跑測試/腳本驗證
5. 回報結果

這正是之後我們在 raw API 上要自建的 loop。

---

## Computer Use：GUI 層 Agent

Computer Use 把 Claude 延伸到純文字之外的環境。它提供的工具能讓 model 實際驅動桌面：

- 截圖（vision 輸入 → 推理）
- 把滑鼠移動/點擊到指定像素座標
- 用鍵盤打字
- 透過 GUI 應用程式操作檔案系統

為何重要：大多數企業軟體沒有乾淨的 API。Computer Use 讓 Claude 能跟任何 UI 互動 —— 老舊桌面軟體、網頁 dashboard、VDI 環境 —— 把像素平面當作介面。

每次操作後 model 會收到新的螢幕截圖，判讀後決定下一步的滑鼠/鍵盤動作。這就是多模態 tool-use loop 的具體範例。

---

## 為什麼用這些作為案例

對 agent 開發者來說，這兩個 app 是參考實作，可回答以下問題：

- 大規模的 tool schema 長什麼樣？（讀它們公開的 tool 定義）
- 多輪 context 該怎麼組？（觀察 Claude Code 的 CLAUDE.md 行為）
- 如何限制自主性又不會廢掉 agent？（看 permission prompt 與確認步驟）
- 邊界情境哪裡難？（錯誤復原、context 管理、模糊狀況下的 tool choice）

當你在 API 上自建，本質就是為特定領域打造自己的 Claude Code。

---

## 常見錯誤

1. **把 Claude Code 當黑盒子** —— 考試預期你知道它是 *agent*，不是聊天 app，而且能辨認其 loop 結構。
2. **混淆 Claude.ai 和 Claude Code** —— Claude.ai 是工具有限的聊天介面；Claude Code 是擁有完整檔案/shell 存取的終端機 agent。
3. **以為 Computer Use 可以取代 API-based agent** —— 它是特定工具組，不是通用 pattern。大多數 production agent 使用 typed tool，不用螢幕截圖。
4. **忘了 MCP 擴充性** —— 預設工具只是起點，兩者都可透過 MCP server 擴充。

> **關鍵洞察**
>
> 從考試觀點看，Claude Code 與 Computer Use 不是「產品」，而是 **標準 agent 實作**，示範 agent 的四項特性（tool integration、多步驟執行、環境互動、自主解題）。CCA 題目常把情境描述成「這算不算 agent？」並期望你能對應到這四項特性。

---

## CCA 考試重點

- **D1（Agentic Coding & Architecture）**：熟記 agent 定義，知道 Claude Code 是 Anthropic 的參考 agent。會出「下列何者為 agent 特性」這類題。
- **D3（Claude Code Configuration）**：Lesson 73 是進入 Claude Code 題組（佔考題約 20%）的起點，後續 lesson 會深入 CLI 指令與 config。
- 留意題目對比 Claude.ai、API、Claude Code 的差異 —— 要知道哪個是聊天室、哪個是基礎建材、哪個是 agent。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 本 lesson 強調哪兩個 Anthropic app 是 agent 的參考實作？ | Claude Code 與 Computer Use |
| Agent 的四項特性是什麼？ | Tool integration、多步驟執行、環境互動、自主解題 |
| Claude Code 跑在哪個介面？ | 終端機 / command line —— CLI agent |
| Computer Use 讓 Claude 互動的對象是什麼？ | 完整桌面環境（透過截圖、滑鼠、鍵盤） |
| 為什麼要用這兩個 app 作為案例？ | 它們示範了讓 agent 在真實世界中有效運作的關鍵原則 |
| Claude Code 與 Claude.ai 有何差異？ | Claude.ai 是工具有限的聊天室；Claude Code 是擁有檔案/shell 存取與 MCP 擴充能力的終端 agent |
| 為什麼 Computer Use 對企業用例有價值？ | 它能驅動沒有開放 API 的應用程式，直接用 GUI 互動 |
| Claude Code 與 MCP 的關係？ | Claude Code 內建 MCP client，可透過自訂 MCP server 擴充工具組 |
