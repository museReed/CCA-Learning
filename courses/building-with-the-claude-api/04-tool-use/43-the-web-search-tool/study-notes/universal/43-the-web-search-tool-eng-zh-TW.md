# Web Search Tool — Engineering Deep Dive

| 項目 | 內容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%)、D4 — AI Safety & Alignment (20%) |
| Task Statements | 2.3（built-in server tools）、2.1（tool schema）、4.2（grounding 與 citation） |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 43 |

---

## One-Liner

Web search tool 是 Anthropic 完全託管的 server tool：你只需要給一個很小的 schema stub，Anthropic 會在他們的伺服器上處理整個搜尋、結果抓取、citation 產生——完全不需要你的本地實作。

---

## 關鍵區分：Server Tool vs. Client-Executed Tool

不同於自訂 tool（schema 與實作都你寫）或 text editor tool（Claude 知 schema、你執行指令），web search tool 是 **server tool**：

| Tool 類型 | 誰定義 Schema | 誰執行 |
|-----------|---------------|-------|
| 自訂 tool | 你 | 你 |
| Text editor（built-in） | Anthropic | 你 |
| Web search（server tool） | Anthropic | **Anthropic** |

Runtime 你什麼都不用做。Claude 向 Anthropic 的 web search 後端發出呼叫，結果透過 API response 回來。

---

## 前置條件：在 Console 啟用

使用 web search 前，你的 Anthropic 組織必須在 privacy 設定啟用它：

```
https://console.anthropic.com/settings/privacy
```

這是 org level 的 opt-in。若設定是關的，包含 web search tool 的請求會失敗。PM 請把它視為任何會用到此 tool 的環境 deployment checklist 的一個項目。

---

## 宣告 Tool

Schema stub 有三個必填欄位：

```python
web_search_schema = {
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": 5,
}
```

| 欄位 | 意義 |
|------|------|
| `type` | Versioned 的 server tool 識別字，必須對應你使用的模型版本 |
| `name` | 固定為 `web_search` |
| `max_uses` | 每個請求的搜尋次數上限 |

`max_uses` 上限很重要，因為 Claude 可能會依初步結果發**後續搜尋**。一個使用者問題可能隨著 Claude 精煉理解而變成三、四次查詢。`max_uses` 就是你的成本與延遲天花板。

---

## 限制搜尋網域

可以用 `allowed_domains` 限制哪些網域可搜尋：

```python
web_search_schema = {
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": 5,
    "allowed_domains": ["nih.gov"],
}
```

使用情境：

- **醫療建議** → 限 PubMed / NIH 獲得實證來源
- **法律研究** → 限 `.gov` 或 `.edu` 網域
- **公司專屬資料** → 限公司官網
- **學術** → 限同儕審查來源

Domain 限制不只是過濾搜尋，更是你控制**內容品質與信任**的主要槓桿。

---

## Response Block 類型

啟用 web search 的 response 除了一般 text，還會包含幾種新的 block：

| Block 類型 | 用途 |
|------------|-----|
| `text` | Claude 的一般解釋文字 |
| `ServerToolUseBlock` | 顯示 Claude 實際下的搜尋 query |
| `WebSearchToolResultBlock` | 包含完整搜尋結果 |
| `WebSearchResultBlock` | 單筆結果（title + URL + snippet） |
| Citation block | 來自來源、支撐 Claude 陳述的逐字引用 |

因為執行是 server-side 的，`ServerToolUseBlock` 與 `WebSearchToolResultBlock` 會在同一個 response 一併回傳——不需要做第二次 round trip。

```python
for block in response.content:
    if block.type == "text":
        render_text(block.text)
    elif block.type == "server_tool_use":
        log_query(block.input["query"])
    elif block.type == "web_search_tool_result":
        render_source_list(block.content)
```

---

## Citation 與 Grounding

Claude 會用 **citation block** 標註文字輸出，內容包括：

- 來源網域與頁面標題
- 來源 URL
- 支撐該陳述的具體引用文字

這讓 grounded generation 真正可行：使用者可以點到來源驗證任何陳述。它也給你一個產品介面——「來源」面板——相較於沒有 grounding 的 LLM 回應，信任感大幅提升。

---

## 渲染模式

Response 的 block 類型對應特定 UI 元件：

1. **Text block** → 主答案區塊的常規內容
2. **Web search result block** → 「來源清單」，通常放在回答上方或側邊
3. **Citation block** → 行內徽章或 footnote，顯示來源網域與頁面標題，可外連

把每種 block 視為不同的 UI 槽，不要合併成一個字串。

---

## 什麼時候用 Web Search Tool

Lesson 指出四個主要使用情境：

- **時事** — 超出模型訓練 cutoff 的資訊
- **專門資訊** — 不在 Claude 訓練資料中的
- **事實查核**與權威來源
- **研究工作**需要最新資訊

你只要把 schema 加入 tools 陣列，Claude 會自動判斷是否要搜尋。不需要特別指示 Claude 用它，模型會根據問題內容自己決定。

---

## 成本與延遲

- 每次搜尋都會增加延遲（伺服器要 fetch、parse、回傳結果）
- `max_uses` 決定每個請求的搜尋次數上限——依使用情境價值設定
- Domain 限制可以縮小搜尋面、加快速度
- Streaming 依然可用；search block 會沿同一個事件序列 stream

高流量 production 使用時請儀表化：

- 每請求的平均搜尋次數（注意是否上漂）
- 啟用 search vs. 不啟用的首個 text token 時間
- Citation 點擊率（使用者對來源的信任訊號）

---

## Common Mistakes

1. **忘記在 console 啟用 web search** — 請求會靜默失敗或回錯；請先檢查 org 設定。
2. **`max_uses` 設太高** — 在推測性問題上的失控搜尋鏈會把成本與延遲翻倍。
3. **沒渲染 citation** — 失去 server tool 最大的產品優勢：可驗證、有 grounding 的答案。
4. **敏感主題沒用 `allowed_domains`** — 醫療、法律、財務主題從權威來源限制中受益極大。
5. **當 server tool 就夠用時還自己實作 web search** — 重新實作意味著更多 code、更差的 citation、也沒有內建的 rendering block。

> **Key Insight**
>
> 像 web search 這樣的 server tool 是最快把「需要新鮮或權威資料」的 production 級 AI 功能上線的路徑。你出一個 schema stub，Anthropic 出整個執行、解析、citation pipeline。你唯一要寫的 code 是渲染 response block 的 UI。

---

## CCA Exam Relevance

- **D2 (Tool Design)**：理解 web search 是「server tool」——Anthropic 執行呼叫，你不提供任何本地函式。
- **D4 (AI Safety & Alignment)**：Citation 與 grounding 是關鍵的信任功能，考題會測「無 grounding 的 LLM 輸出」vs.「帶 citation 的答案」。
- 題目常對比：自訂 tool（兩者都要）、text editor（只給 schema）、web search（什麼都不用——完全託管）。

---

## Flashcards

| Front | Back |
|-------|------|
| 「server tool」與 text editor tool 的差別？ | Server tool 完全由 Anthropic 的基礎設施執行——你不提供任何本地函式 |
| Web search schema stub 需要哪些欄位？ | `type`（versioned）、`name`（`web_search`）、`max_uses` |
| `max_uses` 控制什麼？ | 單一請求中 Claude 能執行的最大搜尋次數（控成本 / 延遲） |
| 如何限定搜尋到特定網域？ | 在 schema 裡設 `allowed_domains`，例如 `["nih.gov"]` |
| 使用 web search 前必須在 Anthropic console 做什麼？ | 在 privacy 設定中啟用 web search tool |
| 列出 web-search response 中的三種新 block 類型。 | `ServerToolUseBlock`、`WebSearchToolResultBlock`、`WebSearchResultBlock`，以及 citation block |
| Citation block 的目的是什麼？ | 引用支撐 Claude 陳述的具體來源文字，實現 grounded、可驗證的答案 |
| 什麼時候 PM 會選 web search tool 而不是自訂搜尋整合？ | 需要新鮮 / 權威資料、又想不自己實作就拿到自動 citation 與 grounding 時 |
