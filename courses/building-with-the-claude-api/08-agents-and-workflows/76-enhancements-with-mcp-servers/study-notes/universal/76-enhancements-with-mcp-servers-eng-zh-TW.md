# Enhancements with MCP Servers — Engineering Deep Dive（繁體中文）

| 項目 | 內容 |
|------|------|
| 考試 Domain | D3 — Claude Code Configuration (20%) / D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 3.2（Claude Code MCP 整合）、2.3（MCP primitives）、1.1（Claude Code 擴充模型） |
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 76 |

---

## 一句話總結

Claude Code 內建 MCP client，可透過 `claude mcp add [server-name] [command-to-start-server]` 註冊任意 MCP server 擴充能力 —— 這是官方擴充點，也是 Claude Code 能跟著你的 workflow 成長的原因。

---

## MCP 擴充模型

Claude Code 預設工具涵蓋檔案操作、終端機、web 存取。其他所有東西 —— 你的資料庫、內部 API、第三方 SaaS —— 都透過 MCP server 進來。架構：

```
┌────────────────────────────────────────┐
│          Claude Code (CLI)             │
│  ┌──────────────────────────────────┐  │
│  │      內建工具                     │  │
│  │  File / Bash / Web / To-do       │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │      MCP Client（內建）           │  │
│  └────────┬─────────┬──────────┬────┘  │
└───────────┼─────────┼──────────┼───────┘
            │         │          │
       ┌────▼──┐ ┌────▼──┐  ┌────▼──┐
       │Sentry │ │Jira   │  │自建   │
       │MCP    │ │MCP    │  │MCP    │
       │Server │ │Server │  │Server │
       └───────┘ └───────┘  └───────┘
```

每個 MCP server 可以提供三種 primitive：

| Primitive | 用途 | 例子 |
|-----------|------|------|
| **Tools** | 執行動作 | `document_path_to_markdown(path)` |
| **Prompts** | 可重用模板 | 一個 `/summarize` slash 指令 |
| **Resources** | 存取資料 | Fixture 檔案或 DB row |

這對應到 MCP 課程已經學過的一般 MCP 控制模型：tool 由 model 控制、prompt 由 user 控制、resource 由 app 控制。

---

## `claude mcp add` 指令

註冊語法就一條：

```bash
claude mcp add [server-name] [command-to-start-server]
```

### 參數

- **`server-name`** —— 你自選的簡短識別碼（例如 `documents`）。Claude Code 內部用這個名字。
- **`command-to-start-server`** —— 啟動 MCP server process 的確切 shell 指令。Claude Code 會把它 spawn 成子 process，透過 stdio 溝通。

### 具體範例

如果你的文件處理 server 在專案目錄下用 `uv run main.py` 啟動，註冊指令是：

```bash
claude mcp add documents uv run main.py
```

之後 Claude Code 每次啟動會自動 spawn 這個 server 並連上。該 server 提供的 tool、prompt、resource 都會納入 agent 可用範圍。

考試重點：註冊是一次性動作 —— `claude mcp add` 跑一次後，Claude Code 會記住，每次啟動自動重連。

---

## 實例：文件處理

Lesson 示範的標準案例：一個自建 MCP server，提供 `document_path_to_markdown` tool，能讀 PDF 與 Word 文件並回傳 markdown。

流程：

1. 寫好有 `document_path_to_markdown` tool 的 MCP server。
2. 註冊：`claude mcp add documents uv run main.py`。
3. 在 Claude Code session 裡問：「把 tests/fixtures/mcp_docs.docx 檔案轉成 markdown」。
4. Claude Code 辨識意圖、挑到自訂 tool、呼叫、取回 markdown 內容。

使用者完全沒明說 tool 名稱。Claude 從 request 推斷該用哪個 tool，示範 MCP tool 的 model-controlled 特性。

---

## 熱門 MCP 整合（考試清單）

Lesson 明確點名以下 server —— 預期會考辨認題：

| Server | 解鎖什麼 |
|--------|---------|
| **sentry-mcp** | 自動發現並修復 Sentry 裡記錄的 bug |
| **playwright-mcp** | 給 Claude 瀏覽器自動化能力做測試與排錯 |
| **figma-context-mcp** | 把 Figma 設計稿暴露給 Claude |
| **mcp-atlassian** | 讓 Claude 存取 Confluence 和 Jira |
| **firecrawl-mcp-server** | 加上網頁爬取能力 |
| **slack-mcp** | 讓 Claude 在 Slack 發訊息或回覆特定 thread |

要記對配對 —— 例如「哪個 MCP server 能讓 Claude Code 修復 monitoring 平台記錄的 bug？」答案是 `sentry-mcp`。

---

## 組合多個 MCP Server

真正的威力來自組合多個 server 配合你的開發流程：

| 階段 | MCP server | Claude 做什麼 |
|-----|-----------|--------------|
| Triage | sentry-mcp | 抓生產環境錯誤細節 |
| Context | mcp-atlassian | 讀 Jira ticket 需求 |
| Implement | （內建檔案工具） | 改 code |
| Verify | playwright-mcp | 跑瀏覽器測試 |
| Notify | slack-mcp | 在團隊頻道發完成訊息 |

每個 server 加上一片垂直能力。疊起來後，Claude Code 從 coding assistant 變成橫跨整個工具鏈的 workflow orchestrator。

這個組合 pattern —— **每個專業化 server 只做一件事，由 agent 編排** —— 正是 MCP 的架構理想，也會出現在考題裡。

---

## 為什麼用 MCP 而非「把更多工具寫死進 Claude Code」

設計動機（超出來源的補充）：

1. **解耦** —— Anthropic 不用維護所有可能的 tool。長尾需求由 ecosystem 處理。
2. **安全邊界** —— 每個 MCP server 是獨立 process，有自己的權限和生命週期。
3. **社群貢獻** —— 任何人都能發佈 MCP server；生態不靠 Anthropic 工程資源擴張。
4. **組合性** —— 堆疊多個小型 server 比一個塞 200 個工具、互搶 context window 的巨獸 agent 乾淨得多。

---

## 常見錯誤

1. **指令語法錯** —— 是 `claude mcp add [name] [command]`，不是 `claude mcp install` 或 `claude add-server`。
2. **忘記 server 必須能跑** —— Claude Code 會把 MCP server spawn 成子 process，傳的指令必須實際啟動有效的 MCP server。
3. **把 MCP 混為一般 HTTP API** —— MCP 講的是透過 stdio 或 SSE 的特定 protocol，不是 raw REST。
4. **以為 server 會自動安裝** —— Claude Code 不會從 registry 拉 MCP server；你要先自己裝好再註冊。
5. **每次 session 都跑 `claude mcp add`** —— 註冊會持久化，每台機器每個 server 只要做一次。

> **關鍵洞察**
>
> MCP 擴充點是 Claude Code 最重要的架構事實：它的強大不是靠 Anthropic 加功能，而是靠你（或社群）接上 MCP server。考試必背那句：**`claude mcp add [server-name] [command-to-start-server]`** —— 精確語法要背熟。題目常會同時考這條指令和 primitive 三元組（tool、prompt、resource）。

---

## CCA 考試重點

- **D3（Claude Code Configuration）**：直接考 `claude mcp add` 語法，以及 Claude Code 內建 MCP client 的事實。
- **D2（Tool Design & MCP Integration）**：要知道 MCP server 可提供 tool、prompt、resource 三種 primitive。
- **D1（Agentic Coding & Architecture）**：預期會出「組合多個 MCP server 成 workflow」的情境題。
- 預期會考上述生態 server 的辨認題（sentry-mcp、playwright-mcp、figma-context-mcp、mcp-atlassian、firecrawl-mcp-server、slack-mcp）。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 註冊 MCP server 到 Claude Code 的指令是什麼？ | `claude mcp add [server-name] [command-to-start-server]` |
| Claude Code 靠什麼內建元件才能擴充 MCP？ | 一個 MCP client —— 它可連到任一你註冊的 MCP server |
| MCP server 可暴露給 Claude Code 的三種 primitive 是什麼？ | Tools（動作）、Prompts（模板）、Resources（資料） |
| 如何註冊一個用 `uv run main.py` 啟動、名叫 `documents` 的 server？ | `claude mcp add documents uv run main.py` |
| Claude Code 會自動重連註冊過的 MCP server 嗎？ | 會 —— 註冊會持久化，每次 Claude Code 啟動都會自動 spawn |
| 想讓 Claude 自動從 monitoring 平台找 bug 並修，該用哪個 MCP server？ | `sentry-mcp` |
| 想給 Claude 瀏覽器自動化能力用哪個 MCP server？ | `playwright-mcp` |
| 想讀 Jira ticket 或 Confluence 頁面用哪個 MCP server？ | `mcp-atlassian` |
| 為什麼 Claude Code 選擇 MCP 而不是把所有 tool 寫死？ | MCP 解耦生態、支援社群貢獻、提供 process 層級的安全邊界、維持 Claude Code 內建介面精簡 |
