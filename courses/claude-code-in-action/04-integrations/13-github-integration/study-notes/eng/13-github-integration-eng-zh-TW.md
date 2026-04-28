# GitHub Integration — 工程師視角


![Github Workflows Two Actions](../../visuals/github-workflows-two-actions-zh-TW.svg)
*圖：GitHub 工作流 — @claude 提及 + PR 審查。*

| 項目 | 內容 |
|------|------|
| 考試對應 | D3 — Claude Code Configuration & Workflows（佔 20%） |
| Task Statements | 3.6 ★★★（CI/CD integration）、2.4 ★★（MCP integration）、1.1 ★（agentic loops） |
| 課程來源 | claude-code-in-action / 04-integrations / Lesson 13 |

---


![Permission Model Local Vs Ci](../../visuals/permission-model-local-vs-ci-zh-TW.svg)
*圖：權限模型 — 本地互動 vs CI 非互動。*

## 一句話理解

Claude Code 的 GitHub 整合提供兩個自動化 workflow：`@claude` 提及觸發互動式任務（issues/PRs），以及自動 PR review。兩者都用 `-p` flag 以非互動模式運行，搭配明確的 `allowed_tools` 權限清單。

---

## 兩個預設 Workflow

整合安裝後會在 `.github/workflows/` 放兩個 workflow 檔案：

<!-- diagram: github-integration-workflows — /install-github-app → PR 帶 2 個 workflow 檔 → Merge → (1) @claude Mention Action / (2) PR Review Action -->
> 📎 流程圖由 nanobanana 產出

### 1. Mention Action（`@claude`）

在 issue 或 PR 留言中提到 `@claude` 就會觸發。

| 步驟 | 發生什麼事 |
|------|-----------|
| 1. 使用者提及 `@claude` | 「修好 toggle button」附上截圖 |
| 2. GitHub Action 啟動 | Workflow 啟動，建立環境 |
| 3. Claude 分析 | 建立 task checklist，規劃方法 |
| 4. Claude 執行 | 存取 codebase、跑工具、測試 app |
| 5. Claude 回報 | 直接在 issue/PR 裡貼出結果 |

### 2. PR Review Action

PR 建立時自動觸發。

| 步驟 | 發生什麼事 |
|------|-----------|
| 1. PR 被開啟 | 開發者推送變更 |
| 2. GitHub Action 啟動 | Workflow 自動運行 |
| 3. Claude review | 分析變更、檢查問題 |
| 4. Claude 回報 | 在 PR 上貼出詳細 review |

> 🎬 **影片補充**
>
> 講師在 demo 中建了一個假的 bug report 附截圖，提及 `@claude`，Claude 自動透過 Playwright 導航到 app、測試按鈕、確認功能正常、並貼出結果。Claude 執行前先建了一份 step-by-step checklist — 這就是 **agentic loop** 模式（plan → execute → observe → report）。

---

## 設定流程

```bash
# 在 Claude Code 裡執行：
/install-github-app
```

三個步驟：
1. 在 GitHub 上安裝 Claude Code app
2. 加入 API key
3. 自動生成一個 PR，包含 workflow 檔案

Merge 這個 PR 後，`.github/workflows/` 裡就會出現兩個 workflow 檔案。

---

## 自訂 Workflow

### 加入專案設定步驟

Claude 運行前可以先準備環境：

```yaml
- name: Project Setup
  run: |
    npm run setup
    npm run dev:daemon
```

### Custom Instructions

提供 Claude 環境的 context：

```yaml
custom_instructions: |
  The project is already set up with all dependencies installed.
  The server is already running at localhost:3000. Logs from it
  are being written to logs.txt. If needed, you can query the
  db with the 'sqlite3' cli. If needed, use the mcp__playwright
  set of tools to launch a browser and interact with the app.
```

> 💡 **重要細節**
>
> Custom instructions 告訴 Claude CI 環境裡有什麼。因為 Claude 是以非互動模式運行（`-p` flag），它無法自行探索，所以這些指示至關重要。

### MCP Server 設定

在 GitHub Actions 環境設定 MCP server：

```yaml
mcp_config: |
  {
    "mcpServers": {
      "playwright": {
        "command": "npx",
        "args": [
          "@playwright/mcp@latest",
          "--allowed-origins",
          "localhost:3000;cdn.tailwindcss.com;esm.sh"
        ]
      }
    }
  }
```

---

## 工具權限：`-p` Flag 和 `allowed_tools`

這是本單元**最重要的考試概念**。

Claude 在 GitHub Actions 裡以 `-p` flag（非互動 / print 模式）運行。這個模式沒有人可以核准權限，所以**每個工具都必須明確列出**：

```yaml
allowed_tools: "Bash(npm:*),Bash(sqlite3:*),mcp__playwright__browser_snapshot,mcp__playwright__browser_click,..."
```

> ⚠️ **考試關鍵細節**
>
> 跟本地開發不同，在 GitHub Actions 裡**不能用** `mcp__playwright` 來允許一個 server 的所有工具。每個 MCP 工具都必須逐一列出。講師原話：「There is no shortcut for permissions like we saw previously.」

| 環境 | 權限方式 | 範例 |
|------|---------|------|
| 本地開發 | 整個 server 允許 | `"allow": ["mcp__playwright"]` |
| GitHub Actions (CI) | 逐一列出工具 | `allowed_tools: "mcp__playwright__browser_click,mcp__playwright__browser_snapshot,..."` |

> 🎯 **考試重點**
>
> `-p` flag 是 Claude 在非互動 CI 模式運行的關鍵指標。CI/CD 情境題（S5）通常會包含這個 flag。看到 `-p` 就要想到：明確權限、無人核准、需要 `allowed_tools`。

---

## CI 中的 Agentic Loop

Claude 透過 `@claude` 提及運行時，展現了 agentic loop 模式：

1. **Plan** — Claude 建立步驟 checklist（在 GitHub 留言中可見）
2. **Execute** — Claude 執行工具（Bash、Playwright、Read、Write）
3. **Observe** — Claude 評估結果
4. **Report** — Claude 在 issue/PR 回報結果

這是 Task Statement 1.1（agentic loops）在 CI/CD 環境的應用。迴圈是自主的——步驟之間不需要人工介入。

---

## 你已經熟悉的類比

| 你用過的技術 | GitHub 整合對應 | 行為 |
|------------|----------------|------|
| CI/CD bots（Dependabot、Renovate） | PR Review Action | 自動化 PR 分析 |
| ChatOps（Slack 裡的 `/deploy`） | `@claude` mention | 從留言觸發 agent |
| Jenkins pipeline agent | GitHub Actions 裡的 Claude | 非互動工具執行 |
| 程式碼品質工具（SonarQube） | PR Review Action | 自動化品質關卡 |

---

## 設定層級

| 層級 | 設定什麼 | 在哪裡 |
|------|---------|--------|
| Workflow YAML | Claude 何時運行、環境設定 | `.github/workflows/*.yml` |
| `custom_instructions` | Claude 對環境的認知 | Workflow YAML 裡面 |
| `mcp_config` | Claude 能存取什麼工具 | Workflow YAML 裡面 |
| `allowed_tools` | Claude 被允許使用什麼 | Workflow YAML 裡面 |
| `CLAUDE.md` | 專案層級的指示 | 專案根目錄 |

---

## 常見反模式

| 反模式 | 為什麼錯 | 正確做法 |
|--------|---------|---------|
| 在 CI 裡不逐一列出 MCP 工具 | Claude 無法使用未明確允許的工具 | 在 `allowed_tools` 逐一列出 |
| 忘記在 Claude 運行前設定環境 | Claude 找不到正在運行的服務 | 在 Claude action 前加 setup 步驟 |
| 沒提供 CI 環境的 `custom_instructions` | Claude 浪費 token 探索有什麼可用 | 告訴 Claude 什麼已經在運行 |
| 在 CI 裡用互動模式 | CI 沒有人可以核准權限 | 用 `-p` flag 切非互動模式 |

---

## 模擬考題

### 第一題：CI/CD Pipeline 情境

你的團隊想在 GitHub Actions 裡加 Claude Code 做自動化 PR review。Claude 需要存取 PostgreSQL 資料庫來驗證 migration 檔案。正確的設定是哪個？

- A. 在 `.claude/settings.local.json` 的 allow list 加 `mcp__postgresql`
- B. 在 workflow YAML 的 `mcp_config` 設定 PostgreSQL MCP server，並在 `allowed_tools` 逐一列出每個 PostgreSQL 工具
- C. 在 `custom_instructions` 寫「你可以存取 PostgreSQL」但不設定 MCP server
- D. 在 `mcp_config` 設定 PostgreSQL MCP server，在 `allowed_tools` 用 `mcp__postgresql` 允許所有工具

<details><summary>答案與解析</summary>

**B** — 在 GitHub Actions 裡，你必須在 `mcp_config` 設定 MCP server 並在 `allowed_tools` 逐一列出每個工具。CI 裡沒有 MCP 工具權限的捷徑。

- A 設定的是本地設定，不是 CI
- C 告訴 Claude 有 PostgreSQL 但沒給實際存取
- D 用了 blanket permission，在 GitHub Actions 裡不可用——每個工具都必須逐一列出

考試哲學：CI/CD 環境中 **Explicit Permissions > Blanket Access**。
</details>

### 第二題：開發者生產力情境

開發者想在 GitHub issue 裡提及 Claude 時，讓 Claude 自動測試 UI 變更。App 跑在 `localhost:3000`。Workflow 設定需要哪些步驟？

- A. 只要加 `@claude` mention 支援——Claude 會自己搞定
- B. 加 setup 步驟啟動 dev server、在 `mcp_config` 設定 Playwright MCP、在 `allowed_tools` 列出 Playwright 工具、在 `custom_instructions` 說明已運行的 server
- C. 把 Playwright MCP 加到 `.claude/settings.json` 然後把 app 部署到公開 URL
- D. 在 `custom_instructions` 告訴 Claude 用 `curl` 測試 app

<details><summary>答案與解析</summary>

**B** — 四個元件都需要：環境設定（啟動 server）、MCP 設定（給 Claude 瀏覽器工具）、明確權限（列出每個 Playwright 工具）、custom instructions（告訴 Claude 什麼已在運行）。

- A 不夠——Claude 在 CI 裡需要明確設定
- C 混淆了本地和 CI 設定方式
- D 沒有給 Claude 實際的瀏覽器互動能力

考試哲學：**Architecture > Prompt** — 給 Claude 工具和環境，不要期望它靠 `curl` 搞定。
</details>

### 第三題：CI/CD 自動化情境

你的團隊在 GitHub Actions 設定了 Claude Code 做 PR review。工程師發現 Claude 沒有使用 Playwright MCP server，儘管已在 `mcp_config` 設定好了。最可能的問題是什麼？

- A. Playwright MCP server 跟 GitHub Actions 不相容
- B. 個別的 Playwright 工具沒有在 `allowed_tools` 列出
- C. MCP 設定變更後需要重啟 Claude
- D. `custom_instructions` 沒有提到 Playwright

<details><summary>答案與解析</summary>

**B** — 在 GitHub Actions 裡，在 `mcp_config` 設定 MCP server 不夠。該 server 的每個工具都必須在 `allowed_tools` 逐一列出。這是最常見的設定錯誤。

- A 不正確——Playwright 可以在 GitHub Actions 裡使用
- C 不正確——Claude 每次 action 運行都是全新啟動
- D 可能有幫助但不是 root cause——工具需要明確權限，不只是指示

考試關鍵詞：`allowed_tools` 是 CI/CD 模式的權限閘門。
</details>
