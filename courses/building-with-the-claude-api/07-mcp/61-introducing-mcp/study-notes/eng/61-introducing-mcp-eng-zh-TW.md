# Introducing MCP — 工程深度解析

| 項目 | 說明 |
|------|------|
| 考試領域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.3（MCP primitives：tools/resources/prompts）、2.1（tool schema 設計）、1.2（agent loop 整合） |
| 來源 | building-with-the-claude-api / 07-mcp / Lesson 61 |

---

## 一句話總結

Model Context Protocol（MCP）是一層通訊協定，讓你可以把「別人已經寫好」的 tools 直接插進 Claude，而不用自己寫 schema 和實作——它把「撰寫工具」的負擔從你的 server 轉移到專門的 MCP server。

---

## MCP 要解決的問題

學完 Ch04 的 tool use 之後，你會撞到下一面牆：**工具撰寫的規模**。想像你要做一個 chat 介面，讓使用者問 Claude 關於 GitHub 的事：

> "我所有 repo 裡面有哪些還沒合的 pull request？"

要回答這個，Claude 需要能打 GitHub API 的 tools。GitHub 功能面非常廣——repos、pull requests、issues、projects、commits、reviews、actions。一個「完整」的 GitHub chatbot 代表你要自己寫**好幾十個** tools，每個都要：

1. 一份 JSON schema 描述輸入
2. 一個 Python function 實作呼叫
3. 測試、錯誤處理、auth、rate-limit 處理
4. GitHub API 改版時持續維護

這是單一開發者很難扛下的工作量，而且每整合一個新服務（Slack、Jira、Sentry、Figma...）都要從頭來一次。

---

## MCP 如何改變這個局面

MCP 把 tool **定義**和**執行**的負擔，從你的 application server 移到專門的 **MCP server**。你不用自己寫 GitHub tools，而是連到一個已經內建這些功能的 GitHub MCP server：

```
┌────────────────┐                      ┌──────────────────────┐
│  你的 server   │                      │   GitHub MCP Server  │
│  (MCP client)  │ ◀─── MCP protocol ──▶│  - list_repos        │
│                │                      │  - list_prs          │
│  Claude API    │                      │  - create_issue      │
│  integration   │                      │  - ...（更多）        │
└────────────────┘                      └──────────────────────┘
```

MCP server 就是一層包在外部服務（GitHub、AWS、Jira...）外面的 wrapper，對外提供現成的 tools、prompts、resources。任何會講 MCP 協定的 application 都能接上並立刻使用。

---

## MCP Server 對外提供什麼

一個 MCP server 提供三種 primitive 類型（後面的 lessons 會深入每一種，但你現在就該認識）：

| Primitive | 用途 |
|-----------|------|
| **Tools** | Claude 可以呼叫的 function，用來執行動作或取得資料 |
| **Prompts** | 可重複使用的 prompt 範本，由 host application 顯示 |
| **Resources** | Claude 可以讀取的資料（檔案、記錄等） |

Lesson 61 著重 tools；resources 和 prompts 在 Ch07 後面的 lessons 處理。

---

## 誰會寫 MCP Server？

任何人都可以寫。實務上分三層：

| 作者 | 範例 |
|------|------|
| 服務提供者官方 | AWS 官方釋出 MCP server，內建 EC2、S3、IAM 等 tools |
| 社群 | 開源的 `sentry-mcp`、`playwright-mcp`、`firecrawl-mcp-server` 等 |
| 你自己（內部） | 針對公司內部 API 寫的自訂 server |

共通模式：想整合服務 X 時，**先確認是否已有現成的 MCP server，再決定要不要自己寫 tools**。

---

## MCP 和直接 Tool Use 的差別

很常見的誤解是把 MCP 當成 tool use 的替代品。其實兩者是互補的：

| 概念 | 是什麼 |
|------|-------|
| **Tool use** | Claude API 的協定：`tool_use` request block → `tool_result` reply block |
| **MCP** | 一個獨立的協定，用來**打包和分發**工具，讓別人定義和執行它們 |

使用 MCP 時，你的 server 對 Claude 仍然是在做一般的 tool use 呼叫。差別在於**是誰**寫的和執行 tool 的實作：

| 直接 tools | MCP tools |
|-----------|-----------|
| 你自己寫 schema | MCP server 內建 schema |
| 你自己實作 function | MCP server 執行 function |
| 你自己維護整合 | Server 作者維護 |
| 你擁有 code | 你只是 consume server |

無論哪種方式，你的 server 都會從 Claude 收到 `tool_use` block，執行它（MCP 的話是請 MCP client 去轉送），再回傳 `tool_result`。Agent loop 本質沒變。

---

## Mental Model：工具分發層

如果 tool use 是 Claude 的電源插頭，那 MCP 就是電網。它標準化了：

- **Discovery**：「這個 server 提供哪些 tools？」
- **Invocation**：「用這些參數呼叫這個 tool」
- **Transport**：現在主要是 stdio，複雜情境會用 HTTP/WebSockets（lesson 62 細講）

真正的好處是**組合性（composability）**。只要你有 MCP client，就能同時連 N 個不同的 MCP servers，把它們的 tools 拼成一個 agent——完全不用寫任何 schema。

---

## 這節課在整章的位置

Lesson 61 是概念介紹，後面會動手做：

| Lesson | 重點 |
|--------|------|
| 61（本節） | 為什麼需要 MCP、它解決什麼問題 |
| 62 | MCP client：transport 無關性、訊息類型 |
| 63 | CLI MCP 範例專案的初始化 |
| 64 | 用 Python SDK 定義 tools |
| 65 | 用 MCP inspector 除錯 |

---

## 常見錯誤

1. **把 MCP 當成 tool use 的替代品** — MCP 是 tool use 之上的「分發層」，不是替代品。
2. **生態系已有 server 還硬要自己寫** — 先查 `sentry-mcp`、`playwright-mcp`、`mcp-atlassian` 等現成的。
3. **以為 MCP server 跑在你的 process 裡** — 它是獨立 process（通常是 subprocess），透過 transport 通訊。錯誤模式是網路型的。
4. **以為 MCP 會幫你處理 auth** — 它不會。credentials 還是透過你的環境變數傳，每個 server 都有自己的 auth 流程。
5. **誤以為 MCP 是 Anthropic 專屬** — 它是開放協定，任何 model provider、任何 application 都能使用。

> **Key Insight**
>
> MCP 最好的心智模型是「**工具的 package manager**」。Tool use 給了 Claude 呼叫 function 的能力；MCP 給了整個生態系一個發行這些 function 的方法，讓你不用每次都重寫一遍。每次準備動手寫 tool schema 之前，先問：「有沒有人已經發佈 MCP server 了？」

---

## CCA 考試重點

- **D2（Tool Design & MCP Integration）**：MCP 的定義、三種 primitives（tools/prompts/resources）、MCP 和直接 tool use 的差別。
- **D1（Agentic Architecture）**：MCP 作為跨系統 agent 的基礎建構單元。
- 題目常見框架：「MCP 解決什麼問題？」——答案永遠是*撰寫和維護工具整合的負擔*。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| MCP 的全名是什麼？ | Model Context Protocol |
| MCP 的核心價值是什麼？ | 把撰寫和執行 tool 定義的負擔，從你的 server 轉移到專門的 MCP servers。 |
| MCP 的三種 primitives 是什麼？ | Tools、Prompts、Resources |
| 誰可以寫 MCP server？ | 任何人——服務提供者常釋出官方 server；社群和內部團隊也會發佈。 |
| MCP 是 tool use 的替代品嗎？ | 不是。MCP 是互補的——tool use 是 Claude API 協定，MCP 是在它之上的分發層。 |
| 為什麼有人要寫 GitHub MCP server 而不是直接呼叫 GitHub API？ | 讓每個使用者都拿到現成的 tool schemas 和實作，不用每個 app 各自重寫。 |
| 從概念上 MCP server 扮演什麼角色？ | 包在外部服務外面的 wrapper，打包出可重複使用的 tools、prompts、resources。 |
| 生態系已有某服務的 MCP server 時該怎麼辦？ | 直接用它，不要自己從頭寫 tool 定義。 |
