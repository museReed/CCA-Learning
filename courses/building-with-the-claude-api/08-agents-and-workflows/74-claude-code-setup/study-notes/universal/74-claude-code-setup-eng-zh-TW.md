# Claude Code Setup — Engineering Deep Dive（繁體中文）

| 項目 | 內容 |
|------|------|
| 考試 Domain | D3 — Claude Code Configuration (20%) |
| Task Statements | 3.1（Claude Code 安裝與設定）、3.2（認證）、1.1（Claude Code 概觀） |
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 74 |

---

## 一句話總結

Claude Code 是終端機原生的 coding agent，用 `npm install -g @anthropic-ai/claude-code` 安裝，以 `claude` 指令啟動，並可透過 MCP 擴充 —— 從全新機器到可用 agent，總共三條指令。

---

## Claude Code 出廠內建什麼

在開始安裝前，先記住 agent 出廠預設帶了什麼，這樣「下列哪項 Claude Code 支援？」的題目才答得出來：

| 工具類別 | 功能 |
|---------|------|
| **File operations** | 搜尋、讀取、編輯專案中任一檔案 |
| **Terminal access** | 在對話中直接執行 shell 指令 |
| **Web access** | 抓取文件頁面、搜尋網路、拉取程式碼範例 |
| **MCP server support** | 透過註冊 MCP server 擴充工具 |

MCP 整合是考試最重要的類別 —— 它是官方擴充點。心智模型就是「內建工具 + MCP」。

---

## 支援平台

Claude Code 是跨平台 CLI，lesson 明定支援：

- **macOS** —— 原生
- **Windows** —— 透過 WSL（Windows Subsystem for Linux）
- **Linux** —— 原生

在 Windows 上，直接用 PowerShell/cmd **不是**受支援的路徑，你必須在 WSL 裡跑。考題至少會出一題把 Windows 丟進安裝情境。

---

## 三步驟安裝流程

整個流程只有三步，要按順序背下來：

### Step 1 —— 安裝 Node.js

Claude Code 以 npm package 形式發佈，所以需要 Node 與 npm。Lesson 建議先確認：

```bash
npm help
```

有跑就代表已裝；沒有就去 `nodejs.org/en/download` 下載。

### Step 2 —— 全域安裝 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

這條指令幾個常見考試陷阱：

- `-g` flag（global）—— 必要，因為 `claude` 要在 PATH 上。
- Package 名稱是 `@anthropic-ai/claude-code`（scoped 在 `@anthropic-ai` 組織下）—— 不是 `claude` 也不是 `anthropic-claude-code`。
- 它是 npm package，不是 `pip install`，也不是獨立 binary。

### Step 3 —— 啟動並認證

```bash
claude
```

第一次啟動時，Claude Code 會要求登入 Anthropic 帳號。登入後會直接進入當前工作目錄的互動式 agent session。

---

## 認證模型

Lesson 描述的是類似瀏覽器的登入流程，綁定 Anthropic 帳號。重點：

- 登入綁的是 **Anthropic 帳號**，不是貼在 config 檔裡的 API key。
- 第一次跑 `claude` 會觸發登入流程。
- 認證完後後續 session 會自動重用憑證。
- 計費和用量走你的帳號 —— 這跟直接用 `ANTHROPIC_API_KEY` 環境變數呼叫 Anthropic API 不一樣。

考試重點差異：**Anthropic API 計費用 API key；Claude Code 用帳號登入**。

---

## 全新 Mac 的完整安裝 Session

```bash
# 1. 確認是否已有 Node
npm help
# 若未安裝，到 nodejs.org/en/download 下載並安裝

# 2. 全域安裝 Claude Code
npm install -g @anthropic-ai/claude-code

# 3. 驗證已在 PATH 上
which claude
# /usr/local/bin/claude  （或類似）

# 4. 啟動、認證、進入專案
cd ~/projects/my-app
claude
# 首次執行：開啟登入流程
# 登入後：進入互動式 agent prompt
```

四條指令跑完就得到一個以當前目錄為預設 project root 的終端機 agent。

---

## 裝完馬上能做什麼

`claude` 跑起來後，就可以直接用自然語言下指令，agent 會自動使用內建工具。第一個 session 可以試：

- `讀 README.md 並總結這個專案`
- `找出所有引用到舊 API endpoint 的檔案`
- `跑測試套件並回報失敗項目`

這些指令直接可用，不需任何額外設定。進階設定（CLAUDE.md、MCP server、自訂指令）會在後續 lesson 講。

---

## 常見錯誤

1. **漏掉 `-g` flag** —— 本地安裝不會把 `claude` 放到 PATH 上。
2. **Package 名稱寫錯** —— 正確的 scoped 名稱是 `@anthropic-ai/claude-code`。
3. **Windows 上沒裝 WSL 就直接跑** —— Lesson 明定 Windows 需透過 WSL，不是原生 PowerShell。
4. **嘗試設 `ANTHROPIC_API_KEY` 而不是登入** —— Claude Code 用帳號登入，不用 raw API key。
5. **跳過 `npm help` 檢查** —— 沒裝 Node 的機器會安裝失敗。

> **關鍵洞察**
>
> CCA 考試把 Claude Code 的安裝流程當成「常識題」，必須一字不差背下來：**Node.js → `npm install -g @anthropic-ai/claude-code` → `claude` → 帳號登入**。沒有可選步驟，而且 Windows 明確指的是 WSL。背熟這句話就是穩拿分。

---

## CCA 考試重點

- **D3（Claude Code Configuration）**：這 lesson 是佔考題約 20% 的基礎，會出直接問安裝指令和平台支援的題目。
- **D1（Agentic Coding & Architecture）**：要知道 Claude Code 是 agent application，不是 chat app，而 MCP 是它的擴充機制。
- 預期至少有一題問 npm package 的精確名稱 —— `@anthropic-ai/claude-code`。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Claude Code 的三個安裝步驟是什麼？ | 1) 安裝 Node.js、2) `npm install -g @anthropic-ai/claude-code`、3) 跑 `claude` 並登入 |
| Claude Code 的精確 npm package 名稱是什麼？ | `@anthropic-ai/claude-code` |
| 為什麼安裝指令要用 `-g` flag？ | 全域安裝會把 `claude` 執行檔放到 PATH 上，任何目錄都能啟動 |
| Claude Code 支援哪些作業系統？ | macOS、Windows（透過 WSL）、Linux |
| Claude Code 的認證模型是什麼？ | 透過 Anthropic 帳號做帳號登入，不是 raw `ANTHROPIC_API_KEY` |
| Claude Code 內建的四類工具是什麼？ | File operations、terminal access、web access、MCP server support |
| 如何檢查 Node.js 是否已安裝？ | 跑 `npm help` |
| 第一次啟動 Claude Code 的指令是什麼？ | `claude` —— 會觸發登入流程 |
