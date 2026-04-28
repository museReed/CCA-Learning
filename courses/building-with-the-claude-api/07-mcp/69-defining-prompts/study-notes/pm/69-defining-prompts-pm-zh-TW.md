# Defining Prompts — PM Perspective（繁體中文）

| 項目 | 說明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（MCP primitives：prompts）、1.2（agent loop priming） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 69 |

---

## One-Liner

Prompts 是 MCP 的「精選集」——由 server 作者策劃、專家級調校過的指令。讓使用者不必學 prompt engineering 也能穩定拿到高品質結果，把「自由輸入、結果不穩」變成「可預期、品牌一致」的功能。

---

## 心智模型：食譜

- 使用者自己寫 prompt 像自家廚房即興發揮，有時做得很好，有時難以下嚥
- Prompts 是餐廳老闆給的食譜，照著做每次都是主廚水準
- 使用者還是能透過參數客製（`doc_id` 就像換食材），但方法是鎖定的

好的 MCP server 會為最常見的 use case 出食譜。使用者從 slash menu 選，server 負責複雜的 prompt 工作。

---

## 為什麼 PM 要在意

自由 prompt 相當於 AI 產品的「打指令列」。專家愛用，其他人看到就跑。Prompts 把專家知識轉成：

- **穩定品質** — 每個使用者都拿到同樣測試過的結果
- **可發現的功能** — prompts 變成 slash-command、快捷動作、按鈕
- **品牌語氣** — 你的寫作風格、格式、語調都內建在模板裡
- **新手捷徑** — 新使用者按「run prompt」馬上看到好結果
- **成本控制** — 調校過的 prompt 通常比使用者自己打的更短、更聚焦

對 PM 而言，prompts 是 tool 與 resource 之上的產品化層。

---

## 產品場景

### 什麼時候 Prompts 划算

| 情境 | 為什麼適合 |
|------|-----------|
| 使用者重複做的任務（改格式、摘要、翻譯） | 一次寫好最佳版本 |
| 措辭至關重要的任務（語氣、結構、合規） | 把措辭鎖定 |
| 希望暴露成 slash-command 或快捷動作的功能 | Prompts 天生對應 UI |
| 低信心使用者想「就給我好的結果」 | 把 prompt 複雜度藏在按鈕後 |

### Prompts 過頭時

| 情境 | 更適合 |
|------|--------|
| 一次性任務、沒有回頭客 | 自由輸入即可 |
| 任務變異大、約束反而害人 | 讓使用者自己寫 |
| 任務其實是查資料 | 用 resource |
| 任務其實是執行動作 | 用 tool |

---

## 使用者怎麼體驗一個 Prompt

從使用者角度看，prompt 通常是：

1. CLI 或 chat UI 的 slash-command（`/format`、`/summarize`）
2. 圖形介面的按鈕或快捷動作
3. 首次啟動時的模板選擇器

他們選、填一兩個參數（例如哪份文件），系統就跑完整的預先工程化指令。使用者從不需要看、也從不需要寫底層 prompt 文字。

---

## PM 決策框架

做 prompt 前問自己：

| 問題 | 若是 Yes | 意義 |
|------|---------|------|
| 輸出品質對措辭高度敏感？ | Yes | 出 prompt |
| 許多使用者重複做的任務？ | Yes | 出 prompt |
| 你的團隊才有做好這件事的專業？ | Yes | 出 prompt（外化專業） |
| 使用者想用很多創意方式做這件事？ | Yes | 不要做 prompt，保留自由輸入 |
| Prompt 需要 live data？ | Yes | Prompt 結合 resource 或 tool |

---

## 品質門檻：什麼時候 prompt「夠好」可以上線？

本課的建議很嚴格：只上真的比使用者自己寫更好的 prompt。大致 checklist：

1. **用 5+ 真實輸入測過** — 每次都產出好結果？
2. **清楚的參數 schema** — 每個參數都有 description，讓 client 顯示
3. **與你的 tool / resource 一致** — prompt 引用真實存在的 server 原語
4. **撐得住邊界情況** — 空輸入、非標準 doc ID、極端長度
5. **一行描述** — 使用者靠這行選擇

若你的 prompt 贏不了使用者臨時打的 30 秒版本，不要上——會訓練使用者對 prompts 失去信任。

---

## PM 常見錯誤

1. **上太多 prompts** — 多到使用者掃不完會 decision paralysis，3–10 個好 prompts 勝過 50 個平庸的
2. **描述模糊** — 使用者看不出 prompt 做什麼就不會選，要像按鈕 label 一樣寫
3. **把 prompts 當靜態設定** — 它們需要版本控制、eval、迭代，跟其他面向模型的 code 一樣
4. **把資料混進 prompt** — 如果你發現要把文件內容寫進 prompt，其實要的是 resource
5. **不量化 prompt 品質** — 追蹤哪些 prompt 被選、哪些導致 rework，淘汰失敗者

> **Key Insight**
>
> Prompts 是讓 MCP 從「開發者 SDK」變成「產品表面」的原語。Tool 與 resource 讓 server 有能力，prompts 讓它好用。懂這件事的 PM 會出「小而精的高品質動作清單」——AI 產品版的 Notion 或 Linear slash-menu——使用者覺得拿到好用工具，而且從頭到尾不用打開文字框。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：Prompts 是 tool / resource 之後的第三種 MCP 原語，知道它帶參數、回傳一串訊息
- **D1（Agentic Architecture）**：Prompts 用高品質對話開場 seed agent loop
- 考題模式：「Server 作者要上線一個可重用的『改寫成 markdown』指令，哪個原語？」→ prompt

---

## Flashcards

| Front | Back |
|-------|------|
| Prompts 的「食譜」比喻是什麼？ | 使用者自己寫 prompt 是即興廚師；prompts 是餐廳老闆給的食譜，使用者換食材（參數），每次都拿到主廚水準 |
| 為什麼 prompts 是產品化層？ | 把專家 prompt engineering 轉成使用者能用的 slash-command 或快捷動作 |
| 什麼時候 PM 不該做 prompt？ | 任務變異大、一次性任務，或其實是查資料（resource）或動作（tool） |
| 一個 prompt 要「可上線」需要什麼？ | 真實輸入測過、清楚參數 schema、配合 server tool/resource、處理邊界情況、一行清楚描述 |
| 描述模糊為什麼會殺死 prompt？ | 使用者依描述選 prompt，模糊的沒人挑，浪費工程資源 |
| 上 50 個平庸 prompt 還是 5 個精品？ | 5 個精品——prompt 太多造成 decision paralysis 並稀釋認知品質 |
| Prompts 怎麼跟 tools 與 resources 組合？ | Prompt 可引用 tool（例如「用 `edit_document` 存結果」）或 resource，像多步 workflow 的食譜 |
| 若 prompt 把文件內容寫死而非參數化會怎樣？ | 你其實想要的是 resource——prompt 是模板、resource 是資料 |
