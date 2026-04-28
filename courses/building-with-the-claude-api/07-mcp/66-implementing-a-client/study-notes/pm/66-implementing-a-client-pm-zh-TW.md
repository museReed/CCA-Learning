# Implementing a Client — PM Perspective（繁體中文）

| 項目 | 說明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（MCP primitives：client/server 整合）、1.2（agentic loop）、2.2（content block types） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 66 |

---

## One-Liner

MCP client 就像「萬國轉接頭」，讓你的 Claude 產品可以插進任何一台 MCP server。做一個 client，生態系所有 MCP server 瞬間都變成可用的功能——tool 整合從「工程客製」變成「設定即用」。

---

## 心智模型：旅行萬國轉接頭

想像你的產品是一台筆電，世界各地的 MCP server 是不同的牆壁插座。沒有轉接頭的話，每次出國（每次整合）都要帶一條新的電源線。**MCP client 就是那個萬國轉接頭**：做一次，可以插進任何 MCP server，筆電充電方式完全一樣。

- 你的產品 = Claude 應用
- MCP server = 一包能力（讀文件、查 CRM、寄 email）
- MCP client = 標準介面，讓你的產品能跟任何 server 對話

重點是：client **不會因整合不同而客製化**。不管你的產品要接哪個 MCP server，client 的程式碼形狀都一樣。

---

## 為什麼 PM 要在意

MCP 之前，「多加一個 tool」意味著工程 ticket：寫 schema、寫 dispatcher、測試、上線。每個整合都耗時間。MCP 之後，多加一個 tool 可以只是「指向新的 server」。

| 沒有 MCP | 有 MCP Client |
|---------|---------------|
| 每個整合都是客製程式 | 整合是可插拔的 server |
| Tool schema 寫在你的應用裡 | Schema 寫在 server，動態探索 |
| 資源清理與生命週期自己管 | 藏在 client wrapper 內 |
| 難以跨產品重用 | 任何相容 MCP 的應用都能重用 |

對產品高層來說，這是 **time-to-value 槓桿**：工程團隊做一次 client，之後每個新能力都可以是 server 專案（甚至是別人做的）。

---

## Client 實際做什麼（不講 code）

Client 只有兩個工作：

1. **問 server「你能做什麼？」** — tool 探索。Server 回一份 tool 選單（名字、說明、輸入）。你的應用把選單轉給 Claude，讓 Claude 知道自己的選項。
2. **被要求時執行 tool** — 當 Claude 說「我要呼叫 `read_doc_contents` 並帶這個 doc ID」，client 把請求轉給 server，再把答案傳回來。

其他事情——啟動、清理、訊息 framing、subprocess 生命週期——全藏在 client 裡。產品團隊看不到。

---

## 產品場景

### 值得投資做 MCP Client 的情境

| 情境 | 為什麼划算 |
|------|-----------|
| 預期未來整合很多 tool | 一個 client，無限 server |
| 公司內多個團隊各自做 tool | 每個團隊獨立上線 server |
| 想用社群 / 開源的 tool 整合 | MCP 是標準，即插即用 |
| 有多個 Claude 應用 | 共用同一批 server |

### 不需要做 Client 的情境

| 情境 | 更簡單的替代 |
|------|-------------|
| 單一產品、只有兩三個硬寫的 tool | 直接用本地 Python function 即可 |
| 用完就丟的 prototype | inline tool 更快 |
| 禁止 spawn subprocess 的安全環境 | 把 tool 內嵌進應用 |

---

## PM 決策框架

決定要不要做 MCP client 前問自己：

| 問題 | 若是 Yes | 意義 |
|------|---------|------|
| 未來半年內會整合至少 3 個不同 tool 面向？ | Yes | MCP client 划算 |
| 希望其他團隊能獨立上線能力、不動我的 codebase？ | Yes | MCP client 理想 |
| 已經有現成的 MCP server 能接我要的系統？ | Yes | 做 client 等於免費解鎖 |
| 產品跑在不能 spawn subprocess 的環境？ | Yes | 重新評估，本地 tool 可能更安全 |

---

## 可靠度、延遲、可觀測性

用了 MCP client 會多一個失敗面：server 可能啟動失敗、handshake 可能失敗、tool call 可能 timeout。PM 要預算：

- **啟動檢查** — server subprocess 起不來時要優雅降級（例如隱藏依賴 tool 的功能）
- **每個 tool 的錯誤處理** — 每個 `call_tool` 都可能失敗，要設計「資料來源暫時不可用」的 UX
- **Logging 與稽核** — 每個 tool call 都可能有副作用，要記錄 name、arguments、result
- **延遲** — 第一次呼叫含 handshake 與 `list_tools` round trip，後續較快但仍受網路影響

這些都要寫進上線清單。

---

## PM 常見錯誤

1. **把 client 當「水管工」** — 實際上它是可觀測性、可靠度、安全的咽喉點，要好好投資
2. **期待零整合成本** — MCP 讓整合便宜很多但不是免費，你還是要決定信任哪些 server、怎麼驗證、怎麼處理錯誤
3. **忽略 tool 探索 UX** — `list_tools` 一多就是幾十個 tool，要有策略決定哪些暴露給哪些使用者
4. **忽略 subprocess 安全** — spawn MCP server 就是執行程式碼。若程式碼由第三方提供，要當相依套件對待（sandbox、pin 版本、code review）
5. **重寫 SDK 已有的 client** — 薄封裝是為了好用，不是為了改 transport

> **Key Insight**
>
> MCP client 是 MCP 最小的一塊，卻是決定你的產品能不能參與生態系的那一塊。做了，世界上所有 MCP server 都是你潛在的功能；不做，你就永遠要手寫每個整合。對 PM 而言，「要不要投資 MCP」的真實意思是：「你希望產品 roadmap 靠社群複利，還是只能等自己寫 code？」

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：認得 `list_tools` 與 `call_tool` 是 client 與 server 的最小契約
- **D1（Agentic Architecture）**：agent loop 不變——MCP 是 dispatch 替換，不是新典範
- 考題模式：「應用要用 MCP server，client 必須暴露哪兩個方法？」→ `list_tools()` 與 `call_tool()`

---

## Flashcards

| Front | Back |
|-------|------|
| MCP client 的「萬國轉接頭」比喻是什麼？ | Client 是通用轉接頭，讓產品插進任何 MCP server，不必每個整合都客製佈線 |
| MCP client 做哪兩件事？ | 1）探索 server 提供的 tool、2）代表 Claude 執行 tool |
| 什麼時候不值得做 MCP client？ | 只有幾個硬寫 tool、用完即丟的 prototype、或禁止 spawn subprocess 的環境 |
| MCP 帶來什麼隱藏風險？ | 執行第三方 server 程式碼——要當相依套件處理，code review、sandbox、pin 版本 |
| MCP 驅動功能的 PRD 要含什麼？ | 啟動與錯誤處理、tool 探索 UX、每次呼叫的 log、server down 的 fallback、延遲預算 |
| 為什麼 MCP 是 PM 的「time-to-value 槓桿」？ | Client 做完後，每個新整合可以是別人寫的 server，roadmap 可複利 |
| MCP 改變 Claude 處理 tool call 的方式嗎？ | 沒有，agent loop 完全一樣，MCP 只改變 tool code 放哪、怎麼被呼叫 |
| Client 最小契約是什麼？ | `list_tools()` 做探索、`call_tool(name, input)` 做執行 |
