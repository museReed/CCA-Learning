# The Server Inspector — 工程深度解析

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | T2.6 測試與除錯 MCP server; T2.7 部署前驗證 tool 行為 |
| Source | introduction-to-model-context-protocol / 02-tools-and-inspector / Lesson 07 |

---

## 一句話摘要

MCP Inspector 是瀏覽器介面的除錯工具，讓你無需建完整應用程式就能互動式測試 MCP server，透過 `mcp dev` 在 localhost:6274 執行。

---

## 什麼是 MCP Inspector？

MCP Inspector 是 MCP SDK 提供的開發工具，給你一個瀏覽器介面的 UI 來測試 MCP server。不需要為了測試 tools 是否運作而建立完整的應用程式（client、Claude 整合、使用者介面），你可以用 Inspector 直接與 MCP server 互動。

```bash
# 對你的 MCP server 啟動 Inspector
mcp dev mcp_server.py
```

這個指令會：

1. 以子程序啟動你的 MCP server
2. 在 `http://localhost:6274` 啟動 web UI
3. 自動建立 MCP 連線

> **Key Insight**
> Inspector 消除了 MCP 開發的雞生蛋問題。你不需要可用的 client 來測試 server，也不需要可用的 server 來理解 server 提供什麼。它把兩端的開發解耦了。

---

## Inspector 介面

在瀏覽器開啟 `localhost:6274` 時，你會看到 Inspector UI 的幾個關鍵元件：

### Connect 按鈕

介面頂部是 **Connect** 按鈕。點擊它建立 Inspector（作為 client）與你的 server 之間的 MCP 連線。連線狀態指示器顯示你是否已連線。

### 三個主要頁籤

Inspector 把 MCP server 的能力整理到三個頁籤：

| 頁籤 | 顯示什麼 |
|------|---------|
| **Resources** | Server 提供的資料源（檔案、資料庫等） |
| **Tools** | Server 提供的可執行函式 |
| **Prompts** | Server 提供的可重用 prompt 範本 |

### Tools 頁籤

點擊 Tools 頁籤顯示 server 提供的所有 tools 列表。每個 tool 條目顯示：

- Tool 名稱
- Tool 描述（來自 docstring）
- 輸入參數及其型別和描述

你可以選擇任何 tool，在輸入欄位輸入參數值，點擊 **Run Tool** 執行。

---

## 測試工作流

使用 Inspector 的標準開發工作流遵循此模式：

### 1. 寫你的 Tool

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-tools")

@mcp.tool()
def calculate_total(prices: list[float], tax_rate: float = 0.1) -> float:
    """計算含稅總價。

    Args:
        prices: 各品項價格列表。
        tax_rate: 稅率（十進位，預設 0.1 = 10%）。
    """
    subtotal = sum(prices)
    return subtotal * (1 + tax_rate)
```

### 2. 啟動 Inspector

```bash
mcp dev mcp_server.py
```

### 3. 連線並測試

1. 開啟 `http://localhost:6274`
2. 點擊 **Connect**
3. 切到 **Tools** 頁籤
4. 選擇 `calculate_total`
5. 輸入測試值：`prices: [10.0, 20.0, 30.0]`、`tax_rate: 0.08`
6. 點擊 **Run Tool**
7. 驗證輸出：`64.8`

### 4. 迭代

如果輸出錯誤或 tool 報錯，修正程式碼再重新測試。Inspector 維持連線，所以你可以重複測試而不需重啟。

> **Key Insight**
> Inspector 中 tool 呼叫之間的狀態是持久的。如果第一次 tool 呼叫建立了檔案，後續 tool 呼叫可以讀取該檔案。這讓你能測試多步驟工作流而不需在每次呼叫之間重置。

---

## 呼叫間的狀態持久性

Inspector 最有用的功能之一是狀態在同一 session 的 tool 呼叫之間持久存在。這對測試有副作用的 tools 至關重要：

```python
@mcp.tool()
def create_note(title: str, content: str) -> str:
    """建立新筆記。"""
    notes_db[title] = content
    return f"筆記 '{title}' 已建立"

@mcp.tool()
def read_note(title: str) -> str:
    """讀取現有筆記。"""
    return notes_db.get(title, "找不到筆記")
```

在 Inspector 中，你可以：

1. 呼叫 `create_note(title="meeting", content="討論 Q3 目標")`
2. 然後呼叫 `read_note(title="meeting")`
3. 驗證它回傳「討論 Q3 目標」

這個循序測試能力對驗證協同運作的 tools 至關重要。

---

## 用 Inspector 除錯

Inspector 對於除錯這些常見問題特別有價值：

**Schema 問題**：如果你的 tool 輸入 schema 不對（缺欄位、型別錯誤），你會在 Tools 頁籤立即看到。Inspector 顯示你的 server 確切提供的 schema。

**參數描述**：你可以在 Inspector UI 中閱讀參數描述來驗證它們是否清楚有用——Claude 會看到同樣的描述。

**錯誤處理**：故意發送無效輸入來驗證你的錯誤訊息是有資訊量的，而不只是 stack trace。

**回傳值**：驗證 tool 輸出結構夠好、資訊夠充分讓 Claude 能解讀。

---

## 在開發工作流中的定位

Inspector 在 MCP 開發工作流中的定位如下：

```
寫 Tool 程式碼  →  用 Inspector 測試  →  修正問題  →  與 Client 整合
                          ↑                    |
                          └────────────────────┘
```

在所有 tools 通過 Inspector 測試之前，不應進入 client 整合。這節省大量除錯時間，因為 Inspector 問題（schema、參數、錯誤）比 client 端問題容易診斷得多——在 client 端，問題可能在 client 程式碼、傳輸層或 server 中。

> **Key Insight**
> Inspector 不只是方便——它是必要的品質關卡。跳過 Inspector 測試直接進入 client 整合，就像跳過單元測試直接做整合測試。你會花更多時間除錯，而非更少。

---

## CCA 考試關聯性

本課涵蓋 **Domain 2 (18%)** 的測試與除錯：

- **`mcp dev` 指令**：知道這個指令對 MCP server 檔案啟動 Inspector
- **localhost:6274**：Inspector 的預設 URL
- **三個頁籤**：Resources、Tools、Prompts——知道每個顯示什麼
- **狀態持久性**：理解 tool 狀態在 session 內的呼叫之間持久存在
- **開發工作流**：Inspector 位於寫程式碼和 client 整合之間

---

## Flashcards

| Front | Back |
|-------|------|
| 什麼指令啟動 MCP Inspector？ | `mcp dev mcp_server.py` — 它啟動 server 並開啟瀏覽器介面的測試 UI。 |
| MCP Inspector 在什麼 URL 執行？ | `http://localhost:6274` |
| MCP Inspector 有哪三個頁籤？ | Resources（資料源）、Tools（可執行函式）和 Prompts（可重用範本）。 |
| Inspector 中 tool 呼叫之間的狀態是否持久？ | 是的。如果一次 tool 呼叫建立了資料，後續呼叫可以在同一 session 中存取它。 |
| 為什麼應在與 client 整合前先用 Inspector 測試？ | Inspector 問題（schema、參數、錯誤）比 client 端問題容易診斷得多，在 client 端問題可能在多個層中。 |
| 在 Inspector 的 Tools 頁籤中可以驗證什麼？ | Tool 名稱、描述、參數型別、參數描述和輸入 schema——Claude 會看到完全相同的內容。 |
| 如何用 Inspector 測試錯誤處理？ | 故意發送無效輸入，驗證錯誤訊息有資訊量且有上下文，而非原始 stack trace。 |
| 標準 MCP 開發工作流是什麼？ | 寫 tool 程式碼 → 用 Inspector 測試 → 修正問題 → 與 client 整合。不要跳過 Inspector 步驟。 |
