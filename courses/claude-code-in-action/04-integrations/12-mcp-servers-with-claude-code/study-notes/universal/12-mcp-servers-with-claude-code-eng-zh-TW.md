# MCP Servers with Claude Code — 工程師視角


![Mcp Server Ecosystem Taxonomy](../../visuals/mcp-server-ecosystem-taxonomy-zh-TW.svg)
*圖：MCP Server 生態分類。*

| 項目 | 內容 |
|------|------|
| 考試對應 | D2 — Tool Use & Integration（佔 18%） |
| Task Statements | 2.4 ★★★（MCP integration）、2.1 ★★（tool interfaces）、2.3 ★★（tool distribution） |
| 課程來源 | claude-code-in-action / 04-integrations / Lesson 12 |

---

## 一句話理解

MCP (Model Context Protocol) server 就是 Claude Code 的 **plugin 架構** — 不改核心就能加新工具，跟 VS Code extension 或 Chrome DevTools Protocol 是同一套思路。

---

## MCP Server 怎麼運作

MCP server 可以跑在**遠端**或**本地**。它們透過標準化的 protocol 把工具暴露給 Claude Code，讓 Claude 在 runtime 動態發現和呼叫。

<!-- diagram: mcp-architecture — Claude Code ↔ MCP Protocol ↔ MCP Server (Playwright / DB / API) ↔ 外部系統 (瀏覽器 / 資料庫 / 服務) -->
> 📎 架構圖由 nanobanana 產出

重點：MCP server 擴展 Claude 能力的方式是**不修改 Claude Code 本身**。這就是 plugin pattern — VS Code extension、Webpack plugin、Kubernetes operator 都是這套哲學。

---

## 你已經熟悉的類比

| 你用過的技術 | MCP Server 對應 | 為什麼像 |
|------------|----------------|---------|
| VS Code extension | MCP server | 不 fork editor 就能加功能 |
| Express middleware | MCP tool handler | 透過標準化介面處理請求 |
| Chrome DevTools Protocol | Playwright MCP | 程式化控制瀏覽器 |
| Kubernetes operator | MCP server | 透過標準 API 擴展平台能力 |
| npm package | MCP server package | CLI 安裝、設定、使用 |

---

## 安裝 MCP Server

課程用 Playwright MCP server 做示範。在你的 **terminal** 執行（不是在 Claude Code 裡面）：

```bash
claude mcp add playwright npx @playwright/mcp@latest
```

這個指令做兩件事：
1. **命名** MCP server 為 `playwright`
2. **註冊** 啟動指令（`npx @playwright/mcp@latest`），在本地執行

> 💡 **重要細節**
>
> `claude mcp add` 是在你的 **terminal** 執行，不是在 Claude Code session 裡面。這會把 server 註冊到專案的 MCP 設定中。

---

## 權限管理

Claude 第一次使用 MCP 工具時，每次都會問你要不要允許。如果覺得煩，可以在 `.claude/settings.local.json` 裡預先授權：

```json
{
  "permissions": {
    "allow": ["mcp__playwright"],
    "deny": []
  }
}
```

> ⚠️ **雙底線**
>
> 格式是 `mcp__<server_name>` — 注意是**兩個**底線。這是考試常考的細節。

`allow` 陣列支援不同粒度：
- `mcp__playwright` — 允許 Playwright server 的**所有**工具
- `mcp__playwright__browser_click` — 只允許**特定**工具

> 🎯 **考試重點**
>
> 考試會考 blanket `mcp__<server>` allow（方便但安全性低）vs 逐一列出工具權限（囉嗦但符合 least-privilege）的取捨。在 CI/CD 環境中，**必須逐一列出每個工具** — 沒有捷徑（Unit 13 會詳細講）。

---

## 實際案例：視覺回饋迴圈

課程展示了一個強大的用法 — 用 Playwright 建立 UI component 生成的**視覺回饋迴圈**：

1. Claude 透過 Playwright 打開瀏覽器，導航到 `localhost:3000`
2. Claude 透過 app 生成一個測試 component
3. Claude **實際看到**視覺結果（不只是看程式碼）
4. Claude 發現 styling 問題（例如「generic 的紫到藍漸層」）
5. Claude 更新 `@src/lib/prompts/generation.tsx` 裡的生成 prompt
6. Claude 用改善後的 prompt 生成新 component
7. 結果：視覺品質顯著提升

> 🎬 **影片補充**
>
> 講師對品質提升的程度感到驚訝。關鍵優勢是 Claude 能看到**真實的視覺輸出**，不只是程式碼。這把「程式碼生成」和「視覺評估」之間的 feedback loop 閉合了 — 以前只有人工 review 才能做到。

---

## MCP Server 生態系

Playwright 只是冰山一角。生態系包括：

| 類別 | 範例 | 用途 |
|------|------|------|
| 瀏覽器自動化 | Playwright | 視覺測試、UI 互動 |
| 資料庫 | SQLite、PostgreSQL | 查詢和檢查數據 |
| API 測試 | REST clients | 程式化測試 endpoint |
| 檔案系統 | 進階檔案操作 | 進階檔案處理 |
| 雲端服務 | AWS、GCP 整合 | 管理基礎設施 |
| 開發工具 | Linter、formatter | 自動化程式碼品質 |

---

## 考試必記：Architecture > Prompt


![Mcp Plugin Architecture Flow](../../visuals/mcp-plugin-architecture-flow-zh-TW.svg)
*圖：MCP 外掛架構流程。*

MCP server 體現了 **Architecture > Prompt** 的考試哲學：

| 做法 | 範例 | 可靠性 |
|------|------|--------|
| Prompt: 「請檢查瀏覽器」 | 叫 Claude 去做視覺驗證 | 不可靠 — Claude 實際上看不到 |
| Architecture: Playwright MCP | 給 Claude 瀏覽器工具 | 可靠 — Claude 能跟真實 UI 互動 |
| Prompt: 「查一下資料庫」 | 期望 Claude 有 DB 存取 | 沒有 DB 工具就會失敗 |
| Architecture: DB MCP server | 提供真正的 DB 工具 | 可靠 — Claude 有實際的資料庫存取 |

> 💡 **判斷口訣**
>
> 考試問到「如何擴展 Claude Code 的能力」，答案幾乎都是 **MCP server**（架構層擴展），而不是 prompt instruction（期望 Claude 做到它結構上做不到的事）。

---

## 常見反模式

| 反模式 | 為什麼錯 | 正確做法 |
|--------|---------|---------|
| 在 Claude Code session 裡安裝 MCP | 必須在 terminal 執行 | 在 shell 裡用 `claude mcp add` |
| 用 `mcp_playwright`（單底線） | 命名規範錯誤 | 用 `mcp__playwright`（雙底線） |
| 在 CI/CD 裡允許所有 MCP 工具 | 安全風險，違反 least-privilege | 在 `allowed_tools` 裡逐一列出 |
| 靠 prompt 描述 Claude 沒有的能力 | 沒有工具就做不到 | 加一個有該能力的 MCP server |

---

## 模擬考題

### 第一題：開發者生產力情境

你在開發一個 web 應用，想讓 Claude Code 能視覺化驗證 UI 變更。最有效的做法是什麼？

- A. 在 CLAUDE.md 加指示，請 Claude 根據程式碼想像 UI 長什麼樣子
- B. 安裝 Playwright MCP server，設定 Claude 導航到正在運行的應用
- C. 手動截圖後貼到 Claude Code 對話中
- D. 寫詳細的 CSS 註解說明預期的視覺效果

<details><summary>答案與解析</summary>

**B** — Playwright MCP server 讓 Claude 有實際的瀏覽器互動能力。Claude 可以導航、截圖、直接評估視覺輸出。

- A 不可能 — Claude 無法從程式碼「想像」UI
- C 可行但是手動流程，打破了自動化迴圈
- D 不能讓 Claude 實際看到視覺結果

考試哲學：**Architecture > Prompt** — 給 Claude 工具，不要叫它想像。
</details>

### 第二題：Code Generation 情境

你的團隊用 Claude Code 生成 React component。生成出來的 component 一直 styling 很差。最佳改善方式是什麼？

- A. 在 system prompt 加更多 styling 範例
- B. 安裝 MCP server 讓 Claude 有瀏覽器存取，讓它視覺化評估生成結果，並根據實際結果更新生成 prompt
- C. 寫一個 PostToolUse hook，每次寫檔後跑 CSS linter
- D. 建立一份詳細的 style guide 文件，在 CLAUDE.md 裡引用

<details><summary>答案與解析</summary>

**B** — 這建立了一個視覺回饋迴圈，Claude 可以看到實際結果並迭代改善。這正是課程影片展示的 workflow。

- A 可能有幫助，但缺乏視覺驗證
- C 抓得到語法問題，但抓不到美學品質
- D 提供方針，但沒有驗證機制

考試哲學：**Architecture > Prompt** — 結構化的 feedback loop 勝過指導性的說明。
</details>

### 第三題：權限管理情境

一個開發者在專案裡加了 Playwright MCP server。他想在本地開發時允許所有 Playwright 工具，不要每次都問。在 `.claude/settings.local.json` 裡正確的設定是哪個？

- A. `"allow": ["playwright"]`
- B. `"allow": ["mcp_playwright"]`
- C. `"allow": ["mcp__playwright"]`
- D. `"allow": ["mcp__playwright__*"]`

<details><summary>答案與解析</summary>

**C** — 正確格式是雙底線：`mcp__playwright`。這會允許 Playwright server 的所有工具。

- A 少了 `mcp__` 前綴
- B 用了單底線（不正確）
- D 太過具體 — `mcp__playwright` 本身就已經允許該 server 的所有工具

重要細節：雙底線慣例是考試常考的知識點。
</details>
