# MCP Servers with Claude Code — PM 視角


![Mcp Server Ecosystem Taxonomy](../../visuals/mcp-server-ecosystem-taxonomy-zh-TW.svg)
*圖：MCP Server 生態分類。*

| 項目 | 內容 |
|------|------|
| 考試對應 | D2 — Tool Use & Integration（佔 18%） |
| Task Statements | 2.4 ★★★（MCP integration）、2.1 ★★（tool interfaces）、2.3 ★★（tool distribution） |
| 課程來源 | claude-code-in-action / 04-integrations / Lesson 12 |

---


![Mcp Plugin Architecture Flow](../../visuals/mcp-plugin-architecture-flow-zh-TW.svg)
*圖：MCP 外掛架構流程。*


![Mcp Architecture](../../visuals/mcp-architecture-zh-TW.svg)
*圖：MCP Server 架構 — Claude Code ↔ 協定 ↔ Server ↔ 外部系統。*

## TL;DR

MCP server 是 Claude Code 的 plugin 系統。它讓你擴展 Claude 能做的事 — 瀏覽網頁、查資料庫、操作 API — 不需要改 Claude Code 本身。PM 的關鍵洞察：MCP server 把「Claude 做不到 X」變成「Claude 做得到 X」，而且是在架構層面解決。這跟 prompt engineering 根本不同 — prompt 只能在 Claude 既有能力範圍內運作。

---

## Why PMs Need to Understand MCP Servers

1. **界定產品能力範圍** — 知道有哪些 MCP server 存在，就知道哪些 Claude 驅動的功能是可行的
2. **Build vs. configure 決策** — 很多能力已經有現成的 MCP server，不需要客製開發
3. **安全與權限治理** — MCP server 需要明確的權限管理，影響你的 risk assessment
4. **CI/CD 影響** — 自動化 pipeline 裡的 MCP server 需要跟本地開發不同的權限設定

---

## Mental Model: AI 工具的 App Store

| 概念 | App Store 類比 | MCP Server 實際 |
|------|---------------|----------------|
| 核心產品 | 開箱即用的 iPhone | Claude Code 內建工具（Read、Write、Bash 等） |
| 擴展 | 安裝一個 app | 加入 MCP server |
| 權限 | 「允許存取相機？」 | 「允許 mcp__playwright 工具？」 |
| 生態系 | App Store 目錄 | MCP server registry |
| 設定 | App 設定 | `.claude/settings.local.json` |

> [!IMPORTANT]
> **考試核心哲學（PM 必記）**
>
> - **Architecture > Prompt** — 如果 Claude 需要某種能力，給它工具（MCP server）。不要試圖用 prompt 讓它做結構上做不到的事。
> - **Explicit Permissions > Blanket Access** — 特別是在 CI/CD 裡，每個工具都必須逐一允許。

---

## Product Scenario Walkthrough

### Scenario: 改善 UI Component 生成品質

你的團隊用 AI 生成 component。生成出來的 component 看起來很 generic — 全是紫到藍漸層和標準的 Tailwind patterns。產品目標是生成更有創意、更有辨識度的 component。

| 做法 | 實現方式 | 結果 |
|------|----------|------|
| 只用 prompt engineering | 在生成 prompt 加「要更有創意」 | 改善有限 — Claude 沒有視覺回饋 |
| MCP + 視覺回饋迴圈 | 安裝 Playwright MCP → Claude 生成 component → Claude 打開瀏覽器看結果 → Claude 根據視覺評估更新 prompt | 顯著改善 — Claude 根據實際視覺輸出迭代 |

> [!TIP]
> **PM 決策框架**
>
> 問自己：「這需要 Claude 感知或互動 context window 以外的東西嗎？」
> - 是 → 你需要 MCP server（架構解決方案）
> - 否 → Prompt engineering 可能就夠了

---

## MCP Server 的商業影響

| 影響面 | 沒有 MCP | 有 MCP |
|--------|---------|--------|
| 視覺 QA | 人工 review | Claude 透過 Playwright 自動驗證 UI |
| 資料庫操作 | 複製貼上 query 結果給 Claude | Claude 直接查詢 DB |
| API 測試 | 手動測 endpoint | Claude 測試 endpoint 並驗證回應 |
| 開發速度 | Claude 盲寫程式碼 | Claude 生成、驗證、自主迭代 |

---

## 權限治理

MCP server 有一套權限模型，PM 應該了解以做 risk assessment：

| 設定 | 位置 | 誰控制 | 安全等級 |
|------|------|--------|---------|
| 本地全部允許 | `.claude/settings.local.json` | 個人開發者 | 低 — 方便開發 |
| 專案共用 | `.claude/settings.json` | 團隊 / Tech Lead | 中 — 團隊標準 |
| CI/CD 明確列出 | GitHub Actions workflow 檔 | DevOps / 團隊 | **高 — 逐一列出每個工具** |

> [!TIP]
> **PM Takeaway**
>
> 在 production/CI 環境裡，MCP 工具權限必須逐一列出。沒有「允許這個 server 的所有工具」的捷徑。這是刻意的安全設計 — 要納入你的 risk assessment。

---

## Instructor Insights（影片補充）

1. **視覺回饋改變一切** — 講師對 Claude 能看到實際 UI 輸出後的品質提升感到驚訝。這意味著視覺驗證能力應該是任何 UI 導向 AI workflow 的標配。
2. **MCP server 是擴展性的核心** — 講師把 MCP 定位為擴展 Claude Code 的主要方式。如果你的產品 roadmap 包含 Claude 原生沒有的 AI 能力，MCP server 就是答案。
3. **生態系快速成長** — 講師建議探索跟你專案需求相符的 MCP server，暗示生態系已經成熟到可以用在 production。

---

## Practice Questions

### 第一題：開發者生產力情境

你的團隊希望 Claude Code 能驗證生成的 UI component 是否符合設計規格。目前開發者是手動比對截圖。你會建議什麼？

- A. 把設計規格加到 CLAUDE.md，讓 Claude 知道要瞄準什麼
- B. 安裝 Playwright MCP server，讓 Claude 打開瀏覽器，視覺化比對生成的 component 和規格
- C. 建立 PostToolUse hook，每次寫檔後跑 visual regression test
- D. 讓開發者截圖貼到 Claude Code 對話裡做 review

<details><summary>答案與解析</summary>

**B** — Playwright MCP server 讓 Claude 有實際的瀏覽器存取，能看到和評估 UI 輸出。這建立了自動化的視覺回饋迴圈。

- A 給 Claude 知識但沒有視覺感知能力
- C 可行但需要既有的測試基礎設施
- D 可行但是手動流程，失去了自動化的好處

> [!IMPORTANT]
> **PM 重點**：當落差是「Claude 無法感知某個東西」時，解決方案是 MCP server 賦予它感知能力 — 不是 prompt 描述它應該感知什麼。

</details>

### 第二題：Code Generation 情境

一個 PM 在 scope 一個需要 Claude 跟 PostgreSQL 資料庫互動的 AI 功能。工程師說「我們直接在 prompt 給 Claude schema 讓它寫 query 就好」。更好的做法是什麼？

- A. 工程師的做法是對的 — 在 prompt 提供 schema context 就夠了
- B. 安裝 PostgreSQL MCP server，讓 Claude 直接查詢和驗證 live 資料庫
- C. 建立一個 custom tool 包裝資料庫 query，透過 Agent SDK 暴露
- D. B 和 C 都是對的，取決於這是 Claude Code 還是 Agent SDK 應用

<details><summary>答案與解析</summary>

**D** — 對 Claude Code workflow 來說，PostgreSQL MCP server（B）是正確做法。對 Agent SDK 應用來說，custom tool（C）是正確做法。核心原則一樣：給 Claude 結構化的資料庫存取，不要只靠 prompt 裡的 schema 知識。

> [!IMPORTANT]
> **PM 重點**：工程師的「就跟 Claude 說」做法（A）是典型的 prompt-over-architecture 反模式。永遠優先給 Claude 真正的工具，而非在 prompt 裡描述能力。

</details>
