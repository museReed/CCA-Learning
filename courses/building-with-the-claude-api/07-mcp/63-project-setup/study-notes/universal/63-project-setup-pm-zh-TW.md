# Project Setup — PM 視角

| 項目 | 說明 |
|------|------|
| 考試領域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.3（MCP primitives）、1.2（agent loop 整合）、2.1（tool schemas） |
| 來源 | building-with-the-claude-api / 07-mcp / Lesson 63 |

---

## 一句話總結

Lesson 63 是「環境就緒」檢查點：在團隊寫任何 MCP 程式碼之前，先驗證 baseline CLI chatbot 能和 Claude 講話——因為後面每一個 MCP 功能都是疊在這個 baseline 上面。

---

## 心智模型：IKEA 組裝前的檢查頁

把這節課想成 IKEA 說明書的第一頁：「打開箱子、把零件排出來、確認每項都在」。你還沒組任何東西，你只是在確認自己**可以**組裝。

| IKEA 步驟 | MCP 專案步驟 |
|----------|-------------|
| 開箱把零件排出來 | 解壓 `cli_project.zip` |
| 核對零件清單 | 確認 `main.py`、`mcp_client.py`、`mcp_server.py` 都在 |
| 檢查工具 | 裝好 `uv` 或 `pip` + venv |
| 檢查接頭 | 在 `.env` 加上 `ANTHROPIC_API_KEY` |
| 試鎖一根螺絲 | 問 bot `what's 1+1?` |

跳過 IKEA 檢查頁的結果是書架晃。跳過 Lesson 63 的結果是你之後抓 MCP bug 時，發現那些 bug 根本是設定問題偽裝的——而這類 bug 最吃工程時間。

---

## 為什麼這節課對 PM 重要

PM 可能會想「為什麼要花一節課做『裝起來』？」。三個理由：

1. **環境是 AI 功能陣亡的地方。**「demo 沒事」→「prod 出包」通常是環境問題，不是程式碼問題。MCP 在一般的 Claude API 使用上面再多疊 subprocesses 和 SDK 版本。
2. **專案形狀 = 你的功能形狀。** 這節課的 CLI chatbot 就是最小可行的參考架構：host + client + server + env file。PM 只要把這個三位組合內化，就能對未來任何 MCP 功能做 reasoning。
3. **定義 bootstrap 階段的 "done"。** 這節課給團隊一個清楚的 initial setup 驗收標準：`what's 1+1?` 有回答就算。這就少了一次「到底通了沒？」的模糊對話。

---

## 產品相關的架構提醒

這節課明確指出真實專案通常只做 MCP client **或** MCP server 的其中一邊，不會兩邊都做：

| 團隊意圖 | 做哪邊 |
|---------|-------|
| 「我們要做一個 Claude 驅動的聊天，處理我們的內部資料」 | MCP client + 現有 server |
| 「我們要把我們的 SaaS 開放給市場上所有 AI agent」 | MCP server 給別人用 |
| 「我們在做平台層」 | 可能兩邊都做，但應該在不同 repo |

從 PM 角度這是一個**一次下定、長期遵守的 scoping 決策**：

- MCP server 作者 = 你在把資料/動作產品化給 agents。
- MCP client 作者 = 你在把 AI 體驗產品化給使用者。

這門課把兩邊做在同一個 repo 純粹是為了教學——別讓它模糊你產品的 scope。

---

## 示範專案的產品應用

這節課的 CLI chatbot 是玩具，但形狀可以直接用：

| 實際產品 | 形狀怎麼對應 |
|---------|-------------|
| 內部文件助理 | 記憶體 docs → 真實 knowledge base；CLI → 網頁 UI |
| 會改 config 的開發者工具 CLI | find-and-replace tool → 範本化 config 修改 |
| Ops runbook 助理 | read + update tools → runbook 讀取和修改 |
| 法遵審查機器人 | read tool → 讀政策文件；update tool → 提議紅字修改 |

只要 PM 在評估的 AI 功能是「讀+寫小塊有限資料集」，都能把這個專案當作可動的範本。

---

## PM 決策框架

在團隊帶著真實產品情境進入這節課前要問：

1. **我們產品是哪一邊？** Client（消費 server）、server（發佈 tools）、還是少見的兩邊都做？
2. **Prod 的 secret 放哪？** `.env` 開發用沒問題；production 要用 secret manager。
3. **我們的最小可行資料集是什麼？** 在 demo 裡是 dict。在 prod 是你能安全讓 Claude 讀寫的東西。
4. **CLI 和 UI 層誰擁有？** 這節課用 CLI；你產品會有真的前端。計畫好轉換。
5. **「setup works」的驗收標準？** 抄這節課的做法——定義一個小小的可測試 smoke check。

---

## 運營和成本筆記

就算是空白 project 也有成本意涵：

| 項目 | PM 為什麼該在意 |
|------|---------------|
| API key | `what's 1+1?` 一跑就開始計費 |
| `uv` vs `pip` | 影響 CI 時間和 onboarding 速度 |
| `.env` 政策 | Secret 外洩風險——第一天就 gitignore |
| Starter code vs completed code | Anthropic 提供 `cli_project.zip` 和 `cli_project_COMPLETE.zip`，選一份當參考 |

---

## 常見 PM 錯誤

1. **把 Lesson 63 當成可以跳** — baseline 壞掉會讓後面每一課都更難 debug。
2. **以為 CLI 就是最終 UX** — 它是課程產物；你的產品需要真 UI。
3. **模糊 client/server 的擁有權** — 不要只因為課程這樣做就把「兩邊都做」塞到同一個 service。
4. **API key 永遠住在 `.env`** — 上線前要規劃搬到 secret manager。
5. **沒定義 smoke test** — 抄 `1+1?` 的模式，縮放到你自己產品真實的資料路徑。

> **Key Insight**
>
> 這節課看起來像 DevOps 水管，但它偷偷塞給 PM 一個很有價值的成品：一個**最小可行的 MCP 架構**（host + client + server + env + baseline check）。任何你要 scope 的真實產品，都可以視為這個形狀的專門化。把這個形狀記住，它到處都在重複出現。

---

## CCA 考試重點

- **D2（Tool Design & MCP Integration）**：知道 Ch07 的工作範例是一個 CLI chatbot，對記憶體文件做 read 和 update tools。
- **D1（Agentic Architecture）**：認識 host/client/server 三位組合是 MCP 的標準排版。
- 預期會有情境題問：給定產品目標，團隊該做 client 還是 server？

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Lesson 63 實際在教什麼？ | 如何 bootstrap Ch07 專案，讓 chatbot 在任何 MCP code 寫出來之前就能和 Claude 講話。 |
| Baseline smoke test 是什麼？ | 問 bot `what's 1+1?` 並確認 Claude 有回答。 |
| Production 時團隊該同時做 MCP client 和 server 嗎？ | 通常只做一邊——課程是為了教學才兩邊做。 |
| Demo 把 document 存在哪？ | 記憶體 Python dict——沒有資料庫。 |
| README 支援哪兩條安裝路徑？ | `uv run main.py`（推薦）和標準 Python + pip + `python main.py`。 |
| 第一次跑之前必備的 secret 是什麼？ | `.env` 裡的 `ANTHROPIC_API_KEY` |
| 「client 或 server，不是兩邊」的備註 PM 要帶走什麼？ | 你產品通常只挑一個角色；混用是 scoping 出問題的徵兆。 |
| 這節課給 PM 什麼具體成品？ | 一個可重用的 MCP 最小可行架構範本：host + client + server + env + baseline check。 |
