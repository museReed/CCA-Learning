# Claude Code Setup — PM Perspective（繁體中文）

| 項目 | 內容 |
|------|------|
| 考試 Domain | D3 — Claude Code Configuration (20%) |
| Task Statements | 3.1（Claude Code 安裝與設定）、3.2（認證）、1.1（Claude Code 概觀） |
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 74 |

---

## 一句話總結

Claude Code 的設定刻意設計成三步驟、低摩擦流程 —— 低啟動能量是刻意的產品決策，決定了開發者採用率，也決定你實際上能瞄準哪些 persona。

---

## 心智模型：可安裝的同事

安裝 Claude Code 比較不像裝 app，更像聘請同事。三個步驟對應：

| 步驟 | 招聘比喻 |
|------|---------|
| 安裝 Node.js | 先確認辦公室有新同事需要的電源插座 |
| `npm install -g @anthropic-ai/claude-code` | 新同事自備筆電報到（CLI 執行檔） |
| `claude` + 帳號登入 | 新同事簽了聘僱合約（你的 Anthropic 帳號） |

花 60 秒設定完，「同事」就能跟你配對寫 code。這是目前最快可取得真實 agent 的路徑 —— 大多數 agent 產品需要多上好幾倍的設定。

---

## 為什麼設定摩擦很重要

設定的每一步都會流失使用者。Claude Code 的三步流程已經逼近理論最小值：

| 設定複雜度 | 典型產品 | Claude Code |
|-----------|---------|-------------|
| 0 步 | 網頁 app —— 連結點開 | — |
| 1 步 | 瀏覽器擴充 —— 安裝一次 | — |
| **3 步** | 帶相依性的 CLI 工具 | **Claude Code** |
| 5+ 步 | 桌面 app + API key + 設定檔 | 多數企業 agent |

Claude Code 團隊的產品決策：把門檻壓在「任何熟悉終端機的開發者」。這句話定義了可觸及的受眾。

---

## 產品使用情境

### 何時推薦「安裝 Claude Code」

| 情境 | 為什麼合適 |
|------|-----------|
| 團隊已經習慣 npm | 沒有新工具要學 |
| 需要檔案系統 + git + shell 存取 | 內建工具已涵蓋 |
| 後續要用 MCP server 擴充 | 擴充點從第一天就存在 |
| 想要帳號式計費，不用 raw key | 登入模型直接搞定 |

### 何時不該推薦 Claude Code

| 情境 | 更好的替代 |
|------|-----------|
| 非技術使用者 | 用 Claude.ai 或 app 內建的 chat widget |
| 嚴格企業環境、沒有 npm | 做 web 工具或用 Claude.ai for business |
| 只用 Windows 且沒 WSL | 評估 Claude.ai 或 API-based 工具 |
| 功能要 GUI 不是 CLI | 用 API 自建 UI |

---

## PM 決策框架

如果你在問「我們團隊要不要採用 Claude Code？」，檢查：

1. **開發者是否本來就住在終端機？** 是的話採用成本趨近零。
2. **每台開發機都有 npm 或 WSL 嗎？** 這是硬性前提。
3. **我們需要帳號式認證還是已經有 API key 管理？** Claude Code 預期帳號登入。
4. **第一年會需要 MCP 擴充嗎？** 需要的話 Claude Code 是理想選擇；不需要的話 raw API 可能更簡單。
5. **設定出問題時誰負責支援？** 三步流程很少出錯，但還是得有人回答「為什麼 `claude` 說 command not found？」

---

## 四大內建能力（用戶開箱即得）

從 PM 角度看，開發者完成安裝那一刻，以下能力直接繼承：

| 能力 | 商業價值 |
|------|---------|
| File operations | Agent 能讀寫 codebase —— 能真做事，不只是聊天 |
| Terminal access | Agent 能跑 test、linter、腳本 —— 閉合驗證迴圈 |
| Web access | Agent 能抓最新文件 —— 不用再抱怨「training data 過期」 |
| MCP server support | 之後加的任何東西都能擴充 agent 而不用重新發佈 |

了解這份清單很重要，因為當有人問「Claude Code 到底做什麼？」，這四點就是核心答案。

---

## 認證方式決策

Claude Code 用 **帳號式登入**，不是 raw API key。產品層面的影響：

| 面向 | 帳號登入（Claude Code） | Raw API key |
|------|------------------------|-------------|
| 使用者體驗 | 一次登入，自動復用 | 剪貼，常不小心 commit 進 git |
| 安全性 | Anthropic 管理 session | 使用者自管 secret |
| 計費 | 綁在使用者訂閱上 | 綁在你的 API organization 上 |
| 合規 | 較簡單 —— infra 不用放 secret | 較難 —— 要管 key rotation |
| 撤銷 | 使用者登出或 Anthropic 撤銷 | 你手動輪換 key |

PM 推動「推薦工程師使用某個 coding agent」時，帳號登入通常是贏家。但如果是「要做一個背後用 Claude 的產品」，API key 才是對的模型。

---

## 常見 PM 錯誤

1. **以為「支援 Windows」等於任何 Windows** —— 實際只有 WSL；要提前告知 Windows 使用者。
2. **把設定當 rollout 計畫的附屬事項** —— 就算只有三步，還是會有人卡住，文件要寫。
3. **混淆 Claude Code 登入與 Anthropic API key** —— 兩條不同的計費路徑，有不同的運維模型。
4. **忽略四大內建能力** —— 「檔案 + 終端 + 網頁 + MCP」是對利害關係人溝通的最低可行功能清單。
5. **沒有 rollback 計畫** —— 如果某人機器上 `claude` 出問題，`npm uninstall -g @anthropic-ai/claude-code` 必須寫進文件作為逃生門。

> **關鍵洞察**
>
> 設定摩擦是 **產品槓桿**，不是技術雜務。Claude Code 的三步安裝是刻意的：把受眾擴大到任何熟悉 npm 的開發者，同時仍保有完整 agent 功能。PM 比較 agent 平台時，「啟動能量」是最重要的單一問題。

---

## CCA 考試重點

- **D3（Claude Code Configuration）**：會出安裝步驟、平台支援、認證模型的題目。
- **D1（Agentic Coding & Architecture）**：要理解為什麼 agent 產品要維持輕量安裝路徑。
- 小心 Windows/WSL 陷阱題和精確 package 名稱題。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Claude Code 需要幾個設定步驟？ | 三個：裝 Node.js、`npm install -g @anthropic-ai/claude-code`、跑 `claude` 並登入 |
| Claude Code 用什麼認證模型？ | 透過 Anthropic 帳號做帳號式登入，不用 raw API key |
| Claude Code 支援哪些作業系統？ | macOS、Windows（透過 WSL）、Linux |
| 安裝後使用者直接獲得的四大能力是什麼？ | File operations、terminal access、web access、MCP server support |
| 為什麼設定摩擦對 PM 採用決策很重要？ | 每一步都會流失使用者 —— 三步流程把受眾定在「熟悉終端機的開發者」 |
| PM 何時「不該」推薦 Claude Code？ | 使用者非技術人員、Windows 沒 WSL、或需要 GUI 而非 CLI 的情境 |
| Claude Code 計費與直接用 Anthropic API 有何差異？ | Claude Code 綁在使用者 Anthropic 帳號訂閱；API 用組織擁有的 API key |
| PM 為何傾向帳號登入勝過 API key？ | 更好的 UX、無 secret 洩漏風險、Anthropic 管理 session、合規更容易 |
