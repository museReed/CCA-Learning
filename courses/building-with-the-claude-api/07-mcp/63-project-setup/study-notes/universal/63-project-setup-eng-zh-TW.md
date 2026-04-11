# Project Setup — 工程深度解析

| 項目 | 說明 |
|------|------|
| 考試領域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.3（MCP primitives）、1.2（agent loop 整合）、2.1（tool schemas） |
| 來源 | building-with-the-claude-api / 07-mcp / Lesson 63 |

---

## 一句話總結

Lesson 63 把動手做的 MCP 專案架起來——一個 CLI chatbot，同一個 codebase 裡有自訂的 MCP client 和自訂的 MCP server，並定下後續 lesson 64、65 會延伸的目錄結構、環境變數和「hello world」baseline。

---

## 我們要做什麼

這個專案是一個 command-line chatbot，讓使用者透過 Claude 和一組記憶體裡的文件互動。它有兩個主要元件，會在 Ch07 後面的 lessons 漸進實作：

| 元件 | 用途 |
|------|------|
| **MCP client** | 處理使用者 chat loop，並轉送 tool use requests |
| **自訂 MCP server** | 管理文件操作（讀取和更新） |

MCP server 會對外提供兩個必要的 tools（lesson 64 會細講）：

1. 一個**讀取** tool，回傳某份文件的內容。
2. 一個**更新** tool，用 find-and-replace 修改文件。

文件存在一個普通的 Python dict 裡——沒有資料庫——讓焦點放在 MCP 機制本身，而不是 persistence 的管線。

---

## 重要的架構備註

這節課明確點出一個設計警告：**真實世界的專案通常只會實作 MCP client 或 MCP server 的其中一邊，不會兩邊都做**。常見模式：

| 角色 | 範例 |
|------|------|
| MCP server 作者 | 你把內部服務的功能開放給其他開發者 |
| MCP client 作者 | 你做一個 app 連到現成的 MCP servers（如 GitHub、Sentry） |

這門課在同一個 repo 兩邊都做**只是為了教學**——這樣你不用切 codebase 就能看到協定兩端如何對話。不要誤以為這是 production 推薦做法。

---

## 專案結構

解壓縮 lesson 附的 `cli_project.zip` 之後，你至少會看到：

| 檔案 | 角色 |
|------|------|
| `main.py` | 進入點，跑 CLI chat loop |
| `mcp_client.py` | MCP client 實作（後面會填） |
| `mcp_server.py` | 自訂 MCP server（後面會填） |
| `.env` | 環境變數檔——放 `ANTHROPIC_API_KEY` |
| `README.md` | 逐步的設定說明 |

`.env` 是關鍵：沒有 Anthropic API key，chatbot 根本無法呼叫 Claude。不管是 `uv` 還是純 `pip` 路徑，都預期第一次跑之前 key 已經就位。

---

## 安裝相依性

README 記錄了兩條支援的安裝路徑：

### 方式 1 — UV（推薦）

```bash
# 在專案目錄
uv run main.py
```

`uv` 是 Astral 出的 Python package manager（跟 ruff 同作者），把 venv 管理和 dependency 安裝包成一個指令。如果專案有 `pyproject.toml` 或 `uv.lock`，`uv run` 會在執行前自動解析和安裝相依性。

### 方式 2 — 標準 Python + pip

```bash
# 建立並啟動 venv，然後
pip install -r requirements.txt
python main.py
```

任何一條路最後都會得到：

- `anthropic` SDK 裝好
- `mcp`（Python MCP SDK）裝好
- 一個能跑 `main.py` 的 Python interpreter

---

## 「Hello World」Baseline

開始實作任何 MCP 功能前，這門課要求你先用一個小問題驗證 baseline：

```
> what's 1+1?
```

你應該很快得到 Claude 的回應。這個 sanity check 確認三件事：

1. `.env` 被 `main.py` 讀到了。
2. 你的 API key 有效（不是 401）。
3. Claude SDK 正確安裝，可以呼叫。

如果這裡失敗，就不要繼續往 lesson 64-65 推進——MCP 只會在已經壞掉的設定上加更多移動零件。

---

## 為什麼這節課重要

一個能跑的 baseline 是後續所有有意義除錯的前提。Lesson 65 的 MCP inspector 和 lesson 64 的 tool 實作都假設你已經能從 `main.py` 打到 Claude。這節課很短，因為它的任務不是教概念——它是在為接下來整章排除環境藉口。

具體來說，Lesson 63 建立了：

| 設定項目 | 後面哪些 lessons 會用到 |
|---------|-----------------------|
| 有 `ANTHROPIC_API_KEY` 的 `.env` | 從這裡開始每一課 |
| 可運作的 `main.py` CLI | 64、65、66、68、70 |
| 裝好的 `mcp` Python SDK | 64（`FastMCP`）、65（`mcp dev`） |
| 裝好的 `anthropic` Python SDK | 每次呼叫 Claude |

---

## Python MCP SDK 技術棧

Lesson 63 還沒寫任何 MCP 程式碼，但已經裝了你下一步要用的 runtime。後面 lessons 會用到的兩個相關 import：

```python
from mcp.server.fastmcp import FastMCP   # lesson 64
from anthropic import Anthropic          # 每一課
```

`FastMCP` 是高階的 server builder（decorator + type hints）；`mcp` 套件也附了 client API 和 CLI inspector（`mcp dev`，lesson 65 會用）。

---

## 常見錯誤

1. **跳過 baseline 測試。** 如果 `what's 1+1?` 都不行，停下來修設定——不要在上面堆 MCP。
2. **忘了 `.env`。** Anthropic SDK 是從環境變數讀 `ANTHROPIC_API_KEY`；少了 key 會在呼叫時才報錯，不是 import 時。
3. **用 global Python interpreter。** `uv` 和 venv 都會隔離相依性；global 安裝容易和 `mcp` 套件版本打架。
4. **以為 production 也要兩邊都做。** 重讀「重要的架構備註」——真實專案通常只做一邊。
5. **忽略 README。** README 帶著精確的設定步驟；Anthropic 的課程專案和它高度耦合。

> **Key Insight**
>
> 這節課的真正重點是**消除設定上的模糊**。MCP 帶進來比純 tool use 更多的移動零件（subprocesses、transports、SDK 版本）。之後要除錯這些的唯一辦法，是從一個已知正常的 baseline 開始。讓 `what's 1+1?` 跑起來是 5 分鐘的投資，接下來四節課都在賺回來。

---

## CCA 考試重點

- **D2（Tool Design & MCP Integration）**：「CLI chatbot + 記憶體文件 + 讀/寫 tools」是 MCP 入門的經典範例——考試情境題可能會呼應它。
- **D1（Agentic Architecture）**：了解 `main.py` 是 host、`mcp_client.py` 是 client、`mcp_server.py` 是 server——這個三位組合會在後面題目反覆出現。
- 要記得「client 和 server 兩邊都做」是教學選擇，不是 production 推薦。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Ch07 的示範專案是什麼？ | 一個 CLI chatbot，用 MCP client 加上自訂 MCP server 來讀取和更新記憶體裡的文件集合。 |
| 自訂 MCP server 會對外提供哪兩個 tools？ | 一個讀取文件的 tool 和一個編輯文件（find and replace）的 tool。 |
| 為什麼這門課在同一個 repo 裡做 client 和 server？ | 純粹為了教學，讓你在同一個 codebase 看到 MCP 協定的兩邊。 |
| 真實世界的做法通常長怎樣？ | 只做 client 或 server 其中一邊——不會兩邊都做——把服務開放給別人或消費現成的 servers。 |
| 第一次跑之前要在 `.env` 加什麼？ | `ANTHROPIC_API_KEY` |
| 推薦用哪個 Python 工具跑這個專案？ | `uv run main.py` |
| 設定完的 baseline sanity check 是什麼？ | 問 chatbot `what's 1+1?` 並確認 Claude 有回答。 |
| starter 專案有哪些檔案？ | `main.py`、`mcp_client.py`、`mcp_server.py`、`.env`、和一份 README。 |
