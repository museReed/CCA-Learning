# Prompts in the Client — PM Perspective（繁體中文)

| 項目 | 說明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（client 端 MCP prompt 使用）、1.2（agent loop seeding） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 70 |

---

## One-Liner

把 prompts 接進 client，是讓它們從「server 端潛能」變成「使用者看得到的按鈕」的最後一哩。這一步讓你的產品可以出 slash-command、快捷動作、模板選單——所有 prompt engineering 的複雜度都藏在一個點擊後面。

---

## 心智模型：有名字按鈕的遙控器

想像你的 MCP server 是一台全能電器——什麼都能煮。沒有 client 端 prompt 接線時，使用者站在電器前翻說明書打原始指令。接進來後，你給他們一支遙控器：

- `/format` 按鈕 → 把文件改成 markdown
- `/summarize` 按鈕 → 濃縮內容
- `/translate` 按鈕 → 轉換語言

每個按鈕都是預先工程化的食譜。使用者按下、也許選個參數（哪份文件），電器就動起來。食譜在 server，按鈕在 client。這一課就是在講怎麼接線。

---

## 為什麼 PM 要在意

這是 prompts 從「工程抽象」變成「demo 時可以指給人看的產品功能」的分水嶺。沒接 client：prompts 等於隱形。接了之後：

- 使用者看到 **可發現的選單**，不是一個空文字框
- Onboarding 可以「試試這個 prompt」起手
- 客服可以說「按 `/format` 修掉這份文件」
- 分析可以追蹤哪些 prompt 被使用
- 行銷可以秀出具體指令

兩個 client 方法（`list_prompts`、`get_prompt`）程式碼很小但產品面很大。你想上的每個 prompt 能不能紅，取決於 client 暴露得好不好。

---

## Client 對使用者呈現什麼

典型使用者視角流程：

1. 使用者打 `/` 或按「指令」按鈕
2. Client 呼叫 `list_prompts()`，渲染帶名字與描述的選單
3. 使用者挑一個（例如 `format`）
4. Client 讀參數 metadata，要求必要輸入（例如「哪份文件？」）
5. Client 背後呼叫 `get_prompt("format", {"doc_id": "report.pdf"})`
6. Server 回完整訊息 list——使用者看不到這一步
7. Client 把訊息送給 Claude 並顯示串流回應

使用者視角：「我選了一個動作，它就成功了。」PM 視角：上面每一步都是設計決策。

---

## 產品場景

### Client 端 Prompt 接線的亮點情境

| 情境 | 為什麼適合 |
|------|-----------|
| 功能多、動作多的複雜應用 | Slash menu 勝過把所有事塞進自由 prompt |
| 新使用者 onboarding | 策劃過的 prompt 立即 demo 產品能力 |
| 團隊分享最佳實踐 workflow | Prompts 變組織知識 |
| 減輕客服負擔 | 「按 `/format`」比「複製這段 prompt」好懂 |
| 品牌一致的輸出 | 每個 prompt 鎖定一種風格 / 格式 |

### 過頭的情況

| 情境 | 更好做法 |
|------|---------|
| 一次性 prototype | 跳過整套管線，直接寫死文字 |
| 完全自由 chat 產品 | Prompts 限制多於幫助 |
| 還沒有 MCP server | 先建 server（Lesson 69） |

---

## PM 決策框架

設計 prompt 驅動的功能時問自己：

| 問題 | 若是 Yes | 意義 |
|------|---------|------|
| 使用者要自己發現 prompt？ | Yes | 必須接 client 端 listing（`list_prompts`） |
| Prompt 有參數？ | Yes | 要設計參數 picker UX（dropdown、autocomplete、表單） |
| Prompt 會被反覆呼叫？ | Yes | 考慮放成 top-level 按鈕，而不是埋在選單 |
| 想要 prompt 使用量遙測？ | Yes | 埋點在 client 端（server 端執行產品團隊看不到） |
| 名字要配合品牌語氣？ | Yes | 名字與描述就是 marketing copy，要這樣對待 |

---

## UX 設計重點

Prompts 出現在 client 這邊，這些都是 PM / 設計的決策：

- **命名** — `/format` 比 `/do_format_thing_v2` 好。短、動詞開頭、意圖明顯
- **描述** — 一行、成果導向（「Rewrite document in markdown」），不要功能導向（「用 MCP prompt `format_document` 帶 doc_id」）
- **參數收集** — 多數使用者不讀表單。提供預設值、智慧 autocomplete、合理 fallback
- **可發現性** — `/` 選單、快捷動作列、onboarding 提示，至少挑一種
- **回饋** — `get_prompt` 跑時要顯示 loading，之後串流 Claude 回應
- **錯誤處理** — server 不可達或 prompt 出錯時顯示「指令暫時無法使用」，不要露 stack trace

---

## PM 常見錯誤

1. **上 prompt 卻沒有發現機制** — 使用者找不到等同不存在
2. **名字與描述晦澀** — 把 prompt metadata 當 microcopy 看待，像按鈕 label 一樣迭代
3. **沒有參數 UX** — 使用者寧可離開也不會自己打 `doc_id`，要有 picker
4. **沒有分析** — 看不到哪些 prompt 被用就沒法淘汰失敗品
5. **脆弱錯誤路徑** — Server 出事要優雅降級，不能讓使用者看到 Python exception

> **Key Insight**
>
> `list_prompts` 與 `get_prompt` 是 PM 能要求的最便宜投入、最大產品影響。它們把工程維護的食譜轉成產品可見的動作，第一次接線之後，每個新 prompt 都不用再做工程工作。Client 接得好，server 作者新出的 prompt 自動出現在產品裡——roadmap 自動駕駛。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：知道 client 暴露 `list_prompts` 與 `get_prompt` 讓使用者發現並呼叫 prompt
- **D1（Agentic Architecture）**：Prompts seed agent loop，其餘（tool、resource）照常
- 考題模式：「MCP server 的 prompts 怎麼呈現給使用者？」→ client 實作 `list_prompts` / `get_prompt`，典型 UI 是 slash menu

---

## Flashcards

| Front | Back |
|-------|------|
| 「有名字按鈕的遙控器」比喻？ | Server 是全能電器，client 的 prompt 接線就是遙控器，每個按鈕對應一個預先工程化的食譜 |
| 哪兩個 client 方法把 prompts 暴露給使用者？ | `list_prompts()` 做發現、`get_prompt(name, args)` 做呼叫 |
| 為什麼 prompts 需要 client 端接線？ | 沒接使用者找不到、也觸發不了，等同不存在 |
| 好 prompt 名字長什麼樣？ | 短、動詞開頭、一看就懂——例如 `/format`，不是 `/do_format_thing_v2` |
| 為什麼分析埋點是 PM 的責任？ | Server 端執行產品團隊看不到，埋點必須在使用者真正互動的 client 端 |
| UX 應該怎麼收參數？ | 用 picker、autocomplete、預設值，不要讓使用者自己打原始參數 key |
| Server 在 `get_prompt` 出錯時怎麼辦？ | Client 要優雅降級——顯示「指令暫時無法使用」，不露 stack trace |
| 為什麼 client 端 prompt 接線是 MCP 的「最後一哩」？ | 因為 tool、resource、server prompt 若沒在 client 變成可發現動作，對使用者就沒用 |
