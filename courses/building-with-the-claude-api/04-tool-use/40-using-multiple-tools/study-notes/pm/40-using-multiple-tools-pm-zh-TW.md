# 使用多個 Tools — PM Perspective

| 項目 | 內容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%)、D1 — Agentic Architecture (22%) |
| Task Statements | 2.1（tool schema 與選擇）、1.2（tool 編排） |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 40 |

---

## One-Liner

讓 Claude 擁有多個 tools，就像請了一個通才，然後給他一條腰帶、上面掛滿專用工具——每新增一項能力都能立刻與既有能力組合，核心產品不用重寫。

---

## Mental Model：瑞士刀

單 tool 的 agent 是螺絲起子；多 tool 的 agent 是瑞士刀。有趣的產品行為來自**組合**：

| 元件 | 單獨使用 | 與其他組合 |
|------|---------|-----------|
| 查行事曆 | 「我今天有什麼行程？」 | 「把我下午 3 點的會議移到 4 點會議結束之後」 |
| 日期運算 | 「30 天後是幾號？」 | 「合約簽訂後 2 週安排一次 follow-up」 |
| 提醒 | 「週五提醒我」 | 「護照到期前 3 天提醒我」 |

使用者很少只做單 tool 的動作，真實需求都是組合的——所以你的 tool catalog 也必須能組合。

---

## Product Use Cases

### 什麼時候該加新 Tool

| 情境 | 為什麼需要多個 tool |
|------|--------------------|
| 排程助手 | 需要日期運算 + 行事曆 + 提醒 + 通知一起運作 |
| 研究 copilot | 需要 web search + 文件檢索 + 摘要 + 引用 |
| 客服 agent | 需要 ticket 查詢 + 知識庫搜尋 + 升級 |
| DevOps 助手 | 需要 log 查詢 + metric 查詢 + runbook + incident 建立 |

### 什麼時候該忍住不加

| 反模式 | 更好的做法 |
|--------|-----------|
| 「以防萬一」先加個 tool | 等到有具體使用者需求再加；砍掉沒用的 |
| 暴露 20+ 個狹窄的 tool，讓 Claude 選 | 合併成較少、較豐富、帶參數的 tool |
| 重複建立行為相似的 tool | 每個能力只保留一個標準 tool |

多一個 tool 的成本不是零：更多 tool 就是每個請求都要多塞 token、Claude 更容易選錯、維護成本也更高。

---

## PM Decision Framework

規劃 tool catalog 成長時，問以下問題：

| 問題 | 如果 Yes | 行動 |
|------|---------|------|
| 有真實使用者需求需要串接 tool 嗎？ | Yes | 補上缺的能力 |
| 既有的兩個 tool description 有重疊嗎？ | Yes | 合併或澄清 |
| 這個新 tool 單獨使用也有價值嗎？ | Yes | 上線 |
| 加進去會讓總數超過 15-20 個嗎？ | Yes | 考慮改用 MCP server 分組 |
| 能用改寫既有 tool description 解決嗎？ | Yes | 先改 description |

---

## 組合原則

Tool 能鏈式組合時，產品價值會複利成長：

- **1 個 tool** → 價值 = N
- **3 個 tool** → 價值 ≈ 3N + 組合數
- **10 個 tool** → 價值隨著有用的組合數成長，而不是 tool 的總數

這就是 Slack、Zapier、IFTTT 成功的原因——平台在擁有足夠多 primitive 可以組合出有意義的 workflow 時才變得有價值。你的 AI 產品也遵循相同的 S 曲線：前期慢、然後在組合能力達成時急速轉折。

---

## Claude 如何選 Tool（PM 能怎麼影響）

Claude 讀取每個 tool 的 **description** 並挑最符合的那個。PM 可以透過以下方式改善準確度：

1. **寫動作導向的祈使句描述** — 「Creates a reminder at a specific datetime」勝過「Reminder utility」
2. **標註使用限制** — 「Use only for dates in the future」可以防止誤用
3. **避免重疊** — 兩個 tool 能做類似的事，Claude 會隨機選一個，應該合併
4. **用真實使用者的說法測試** — 翻真實對話記錄，確認正確的 tool 會被觸發

Description 就是產品表面，請用跟按鈕文字、empty state 一樣的嚴謹度對待它。

---

## Common PM Mistakes

1. **把 tool description 當成隨便寫的 docstring** — 它是 Claude 選擇的主要訊號，請像 UX copy 一樣投入。
2. **上線第一天就推出龐大的 tool catalog** — 從 2-3 個開始，觀察使用狀況，依據真實需求擴充。
3. **沒有追蹤 Claude 實際選了哪個 tool** — 沒量測就沒法優化，請記錄 tool selection 事件。
4. **忽略 parallel vs. sequential 的成本差異** — parallel 呼叫是一次 API round-trip，sequential chain 是多次，延遲會累積。
5. **以為 tool 越多代表能力越強** — 能力是來自「有用的組合」，不是 catalog 大小。

> **Key Insight**
>
> Multi-tool agent 的產品價值來自**組合**，不是來自 tool 數量。每一個新 tool 都必須證明自己能解鎖既有 tool 做不到的鏈式 workflow。CCA 考試的核心概念：tool 選擇是 model-controlled 的，由 description 品質驅動，不是列表中的順序。

---

## CCA Exam Relevance

- **D2 (Tool Design)**：理解 Claude 基於 schema name + description 選 tool，寫得好的 description 是準確度的主要槓桿。
- **D1 (Agentic Architecture)**：理解 parallel vs. sequential tool execution 以及它們共用的 agentic loop。
- 情境題常給一個擁有 3-5 個 tool 的 agent，問某個使用者請求會觸發哪個——答案是由 description 的符合度決定。

---

## Flashcards

| Front | Back |
|-------|------|
| Multi-tool agent 為什麼比 single-tool 有價值？ | 組合——價值來自有用的 chain-workflow 數量，不是 tool 總數 |
| Claude 如何決定要呼叫哪個 tool？ | 將使用者請求與每個 tool 的 name 和 description 做匹配 |
| PM 能改善 tool selection 準確度的主要槓桿？ | 寫動作導向、祈使句形式的 description；避免 tool 之間重疊 |
| 為什麼 PM 不該「以防萬一」就加 tool？ | 多餘的 tool 吃 token、讓選擇出錯、增加維護成本；要有真實需求才加 |
| 暴露 20+ 個狹窄 tool 的風險是什麼？ | Claude 要從更多選項中挑，準確度下降，token 成本升高 |
| parallel 何時比 sequential tool 呼叫便宜？ | 當 tool 彼此獨立時——parallel 是一次 round-trip，sequential 是多次 |
| PM 要追蹤什麼訊號來優化 tool catalog？ | 不同使用者說法下 Claude 實際選了哪個 tool，以便調整 description |
| Multi-tool agent 的核心產品心智模型？ | 瑞士刀——個別 tool 沒那麼重要，重要的是它們能組合出什麼 |
