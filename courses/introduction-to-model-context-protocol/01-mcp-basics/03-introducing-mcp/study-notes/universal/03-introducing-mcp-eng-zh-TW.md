# Introducing MCP — 工程深度解析

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | T2.1 設計與實作 tool schemas; T2.3 設定 MCP server 連線 |
| Source | introduction-to-model-context-protocol / 01-mcp-basics / Lesson 03 |

---

## 一句話摘要

MCP 是一個標準化通訊協定層，讓 Claude 透過專用的 MCP server 存取外部工具與資料，不再需要手寫整合程式碼。

---

![Mcp Architecture](../../visuals/mcp-architecture-zh-TW.svg)


## MCP 到底是什麼

Model Context Protocol (MCP) 是位於你的應用程式與外部服務之間的**通訊協定**。與其為 Claude 需要存取的每個服務手寫 tool schema 和 API 整合程式碼，MCP 把這個責任委派給專用的 MCP server。

核心架構遵循一個簡單的模式：

```
你的應用程式 (MCP Client)
        |
        v
    MCP Server（例如 GitHub MCP Server）
        |
        v
    外部服務（例如 GitHub API）
```

每個 MCP server 提供一個標準化介面，包含 **tools**、**prompts** 和 **resources**。你的應用程式只需要會說 MCP 協定——server 處理所有服務特定的細節。

> **Key Insight**
> MCP 之於 AI 工具整合，就像 USB 之於硬體周邊設備。不再需要為每個裝置準備專用接頭，一個標準化協定就能搞定所有連接。

---

## MCP 解決的問題

假設你在打造一個聊天介面，使用者問 Claude 關於他們的 GitHub 資料。使用者問：「我所有 repo 中有哪些 open pull requests？」

沒有 MCP 的話，你需要：

1. **定義 tool schemas** — 為每個 GitHub 操作寫 JSON schema（repos、PRs、issues、projects 等）
2. **實作 handler 函式** — 把 Claude 的 tool call 轉譯成 GitHub API 請求的程式碼
3. **處理認證** — OAuth tokens、rate limiting、pagination
4. **持續維護** — GitHub API 改版、棄用、新功能

```python
# 沒有 MCP：你要自己寫和維護這些
tools = [
    {
        "name": "get_pull_requests",
        "description": "List open PRs across repositories",
        "input_schema": {
            "type": "object",
            "properties": {
                "state": {"type": "string", "enum": ["open", "closed", "all"]},
                "repo": {"type": "string"}
            }
        }
    },
    # ... 幾十個 tool 定義
]

def handle_get_pull_requests(state, repo):
    # 認證、分頁、錯誤處理...
    response = requests.get(f"https://api.github.com/repos/{repo}/pulls",
                          params={"state": state},
                          headers={"Authorization": f"token {token}"})
    # ... 更多程式碼
```

有了 MCP，GitHub MCP server 直接提供這一切。你的程式碼只需連上 MCP server 並傳遞 tool call。

> **Key Insight**
> 真正要命的是維護負擔。光是 GitHub 就有數百個 API endpoint。沒有 MCP，每次 API 變更都可能破壞你的 tool 定義。MCP server 把維護工作集中化了。

---

## MCP 架構元件

### MCP Client

MCP Client 就是你的應用程式——代表 Claude 連接 MCP server 的系統。它負責：

- 透過 `ListToolsRequest` 探索可用的 tools
- 透過 `CallToolRequest` 執行 tools
- 管理傳輸層（stdio、HTTP、WebSockets）

### MCP Server

MCP Server 是一個獨立程序，封裝外部服務。它：

- 定義 tool schemas（名稱、描述、輸入參數）
- 實作 tool 執行邏輯
- 處理服務特定的認證和錯誤處理
- 在 tools 之外也提供 prompts 和 resources

### 誰來建 MCP Server？

任何人都可以撰寫 MCP server。實務上：

- **服務提供者**常會發布官方 MCP server（例如 AWS、GitHub）
- **社群貢獻者**為熱門服務建立 server
- **你自己**可以為內部工具和 API 建立自訂 MCP server

---

## MCP vs. Tool Use：關鍵區別

這是常見的考試主題。MCP 和 tool use 是**互補的，不是相同的**：

| 概念 | 它做什麼 |
|------|---------|
| **Tool Use** | Claude 決定呼叫 tool、格式化輸入、處理結果的機制 |
| **MCP** | 提供 tool 定義和執行基礎設施給 Claude 的協定 |

這樣想：tool use 是**動詞**（Claude 呼叫 tool），而 MCP 是**名詞**（提供並執行那些 tools 的系統）。

沒有 MCP 你仍然有 tool use——只是要自己寫所有 tool 定義。沒有 tool use，MCP server 就沒用——因為 Claude 沒有機制去呼叫它們。

> **Key Insight**
> CCA 考試中，不要把 MCP 和 tool use 混為一談。MCP 是關於*誰定義和維護 tools*。Tool use 是關於 *Claude 如何呼叫它們*。它們一起運作但是不同概念。

---

## CCA 考試關聯性

本課直接對應 **Domain 2: Tool Design & MCP Integration (18%)**。重點考試角度：

- **架構理解**：掌握 Client-Server 關係及各元件的功能
- **問題辨識**：辨認何時 MCP 是正確的解法（大量 API 端點、維護負擔、標準化需求）
- **MCP vs. tool use**：此區別出現在多道考題中，要精確描述各概念涵蓋的範圍
- **Server 撰寫權**：理解 MCP 是一個開放生態系，不是 Anthropic 獨佔的封閉系統

---

## Flashcards

| Front | Back |
|-------|------|
| MCP 主要解決什麼問題？ | 消除為 Claude 需要存取的每個外部服務手動撰寫、測試和維護 tool schemas 及整合程式碼的需求。 |
| MCP server 可以提供哪三種能力？ | Tools、prompts 和 resources。 |
| MCP 和 tool use 的關係是什麼？ | 它們互補：MCP 提供 tool 定義和執行基礎設施；tool use 是 Claude 呼叫那些 tools 的機制。 |
| 誰可以撰寫 MCP server？ | 任何人——服務提供者、社群貢獻者，或建立自訂整合的個人開發者。 |
| MCP Client 的角色是什麼？ | MCP Client 是你的應用程式，連接 MCP server、探索可用 tools、路由 tool 執行請求。 |
| 在 MCP 架構中，tool 執行實際發生在哪裡？ | 在 MCP server 上，不是在你的應用程式 server 上。MCP server 處理所有服務特定的實作細節。 |
| 為什麼 MCP 被比喻為 USB？ | 就像 USB 用一個協定標準化硬體連接，MCP 標準化 AI 工具整合，不需要為每個服務準備專用接頭。 |
| 沒有 MCP 的情況下，GitHub 整合你需要自己實作什麼？ | 每個操作的 tool schema、API 呼叫的 handler 函式、認證處理、分頁、速率限制，以及因應 API 變更的持續維護。 |
