# The Server Inspector — 工程深度解析

| 項目 | 說明 |
|------|------|
| 考試領域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.3（MCP primitives）、2.1（tool schema 設計）、1.2（agent loop 整合） |
| 來源 | building-with-the-claude-api / 07-mcp / Lesson 65 |

---

## 一句話總結

MCP Inspector 是一個瀏覽器基礎的開發工具——隨 Python MCP SDK 附上（用 `mcp dev` 啟動）——讓你直接 `list` 和 `call` 你 server 的 tools、resources、prompts，不需要先把 server 串到 Claude 或真實 application。

---

## 問題：除錯的回饋迴圈

當你在做 MCP server 時，要驗證它的 tools 有兩條路：

| 路徑 | 回饋迴圈 |
|------|---------|
| 串到完整的 Claude application 裡 | 慢、吵、MCP bug 和 prompt/agent bug 混在一起 |
| 透過 MCP 協定直接驗證 | 快、隔離、秒級暴露 MCP bug |

第一條是你最終需要的，但也是除錯最糟的地方。你無法分辨失敗是來自 tool 本身、prompt、Claude 選 tool 的判斷、還是你的 agent loop。**Inspector** 透過給你第二條開箱路徑把回饋迴圈壓縮。

---

## 啟動 Inspector

在 Python 環境啟動後（精確指令看專案的 README）執行：

```bash
mcp dev mcp_server.py
```

這條指令會：

1. 在 **6277 port** 啟動一個 development server。
2. 印出 Inspector UI 的本地 URL。
3. 載入你的 MCP server code，讓它的 tools、resources、prompts 可被發現。

接著你在瀏覽器打開那個 URL，就會看到 **MCP Inspector dashboard**。

> 備註：這節課明確說 Inspector「正在積極開發中」，所以確切 UI 可能和課程截圖不同。**能力**（list tools、call tools、看結果）不變。

---

## 連線和發現 Tools

Inspector workflow 是從左側 sidebar 驅動的。核心步驟：

1. **點「Connect」** — 和你的 server 建立 MCP 協定 session。
2. **導到「Tools」** — 切到導覽列的 tools 檢視。
3. **點「List Tools」** — 送一個 `ListToolsRequest` 並渲染回應。
4. **選擇一個 tool** — 開啟該 tool input schema 的表單檢視。
5. **填入參數** — 表單是從你 Python type hints + `Field(description=...)` 產生的。
6. **點「Run Tool」** — 送一個 `CallToolRequest` 並內聯顯示結果。

每個互動都 1:1 對應到一則真實的 MCP 協定訊息，所以你在 Inspector 測的東西就是真實 MCP client 會看到的東西。

除了 Tools，導覽列也有 **Resources** 和 **Prompts** 的區塊（後面的 lessons 會用），讓你在同一個 UI 測三種 primitives。

---

## 實際範例：演練 document tools

用 Lesson 64 的 server，以下是你如何不啟動 chatbot 就從 Inspector 驗證兩個 tools：

### 1. 讀取文件

- Tool：`read_doc_contents`
- 參數：`doc_id = "deposition.md"`
- 預期結果：`"This deposition covers the testimony of Angela Smith, P.E."`

### 2. 編輯再讀取

- Tool：`edit_document`
- 參數：`doc_id = "deposition.md"`、`old_str = "Angela Smith"`、`new_str = "Jane Doe"`
- Inspector 確認呼叫完成。

編輯之後立刻再跑 `read_doc_contents` 用同樣的 ID——你應該會看到文字已經被替換。這個**鏈結驗證**模式是個低成本的方法，用來確認變更類的 tool 真的有效。

因為文件活在記憶體 dict 裡，重啟 server 會清掉改動。Debug 時這是功能——每次 session 都從乾淨狀態開始。

---

## 啟用的開發迴圈

Inspector 建立一個緊湊、可重複的迴圈：

```
┌─────────────────────────┐
│ 1. 編輯 mcp_server.py    │
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 2. 重啟 `mcp dev`        │  （或靠 auto-reload）
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 3. 在 UI List Tools     │
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 4. 帶輸入 Run Tool       │
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 5. 檢視結果              │
└───────────┬─────────────┘
            ▼
          (重複)
```

每次迭代只碰 MCP server——沒有 Claude API 呼叫、沒有 prompt engineering、沒有 chat loop。這個隔離性正是 Inspector 的價值。

---

## 為什麼這在架構上重要

Inspector 是一種對「**MCP 是協定**，不是 Claude 特定功能」的承認。一個協定需要一個獨立於特定消費者（Claude、其他 LLM、自動化）的通用除錯 client。`mcp dev` 就是那個通用 client。

具體來說：

| 沒有 Inspector | 有 Inspector |
|---------------|-------------|
| 每次測試都需要 Claude API key | 可以離線於 Claude |
| Tool bug 會遮住 prompt bug | Tool bug 被隔離 |
| 回饋迴圈：分鐘級 | 回饋迴圈：秒級 |
| 沒 chatbot 就無法驗證 tool schema | Schema 立刻渲染成表單 |

---

## Inspector 不會做的事

界線要說清楚：

| 能力 | Inspector 有嗎？ |
|------|---------------|
| 演練 tools、resources、prompts | 有 |
| 把自動產生的 schema 渲染成表單 | 有 |
| 用產生的 tool 呼叫 Claude | 沒有——那要用完整的 chatbot |
| 取代 end-to-end 測試 | 沒有——integration tests 還是要跑 |
| 部署你的 server | 沒有——`mcp dev` 只在 dev 用 |

Inspector 的價值在於**把 MCP 行為從 LLM 行為隔離**。你的 tools 在 Inspector 通過後，就進到接上 agent 的階段。

---

## 常見錯誤

1. **跳過 Inspector 直接做 chatbot 整合。** 你失去了隔離的回饋迴圈，最後會一次 debug 兩層。
2. **沒先點 Connect。** 左側的 Connect 按鈕才會實際開始 session；不點它，「List Tools」會回空。
3. **以為 UI 是穩定的。** 這節課警告 Inspector UI「正在積極開發中」——學概念（list、call、chain），不是精確像素。
4. **忘了 port。** 預設是 `6277`；如果被佔用指令會告訴你。
5. **只測 happy path。** 也塞一個假 `doc_id`——驗證你的 `ValueError` 乾淨地呈現。

> **Key Insight**
>
> Inspector 是**協定除錯器**。它把「我的 tool 能動嗎？」和「Claude 會好好用我的 tool 嗎？」這兩個很不同的問題分開——如果你只做 end-to-end 測試，這兩個會混在一起。養成每個新 tool、每次既有 tool 的改動都先打 Inspector 的習慣。它會為 Ch07 後面的 lessons 省下好幾個小時的糾結 debug。

---

## CCA 考試重點

- **D2（Tool Design & MCP Integration）**：知道 Python MCP SDK 附一個瀏覽器基礎的 Inspector，用 `mcp dev mcp_server.py` 啟動，可演練 Tools、Resources、Prompts。
- **D1（Agentic Architecture）**：認識 Inspector 是 MCP 的隔離測試表面，和完整 agent 測試不同。
- 預期的情境題：「你的 tool 在 Inspector 能動，但在 chatbot 失敗——這是哪一類 bug？」——答：不是 MCP bug，可能是 prompt、schema description 或 agent-loop bug。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 怎麼啟動 MCP Inspector？ | 在啟動的 Python 環境裡跑 `mcp dev mcp_server.py`。 |
| Inspector 預設用哪個 port？ | `6277` |
| Inspector sidebar 第一個要點的按鈕是什麼？ | 「Connect」——它和你的 MCP server 開 session。 |
| Inspector 讓你演練哪三種 primitive？ | Tools、Resources、Prompts。 |
| 點「List Tools」在協定層做什麼？ | 送 `ListToolsRequest` 並渲染回傳的 `ListToolsResult`。 |
| 「Run Tool」在協定層做什麼？ | 送帶表單輸入的 `CallToolRequest` 並顯示 `CallToolResult`。 |
| 這節課示範的鏈結驗證模式是什麼？ | 呼叫 `edit_document` 然後立刻呼叫 `read_doc_contents` 確認編輯生效。 |
| Inspector 對 debug 最大的價值是什麼？ | 它把 MCP 行為從 LLM 行為隔離——tool bug 不再遮住 prompt bug。 |
