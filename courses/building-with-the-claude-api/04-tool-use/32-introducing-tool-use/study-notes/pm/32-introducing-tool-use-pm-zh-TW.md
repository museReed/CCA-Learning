# 介紹 Tool Use — PM Perspective

| 項目 | 內容 |
|------|------|
| 考試 Domain | D2 — Tool Design & MCP Integration (18%) 主要;D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 1.2(agentic loop 基礎)、2.1(tool schema 設計)、2.4(multi-turn tool loop) |
| 來源 | building-with-the-claude-api / 04-tool-use / Lesson 32 |

---

## 一句話總結

Tool use 是讓 Claude 從「博學的聊天機器人」變成「能幹的隊友」的功能 — 也是任何依賴即時資料或真實動作的產品,要把 AI 功能做成商業可行的關鍵。

---

## 心智模型:飯店禮賓人員

想像一位飯店禮賓人員讀過所有旅遊書,但被規定永遠不能離開大廳。

- 問這座城市的歷史 — 答得完美。
- 問「那間餐廳現在還開著嗎?」— 禮賓只能聳肩。

Tool use 就像給這位禮賓一支**電話和一份可撥打的電話清單**。現在你問那間餐廳,他拿起電話打過去問,拿到答案再回你。從客人角度看,禮賓突然變得超級有用 — 可是他並沒有變聰明,只是**能接觸到外面的世界了**。

這是 Claude API 對 PM 最大的那一把鑰匙。

---

## PM 為何要關心

過去一年出貨的 AI 功能,幾乎沒有哪個不依賴 tool use。以下需求都在暗示「你需要 tools」:

- 「顯示這位客戶最新的訂單」
- 「幫我週二下午三點約個會」
- 「摘要這張 Jira ticket 的目前狀態」
- 「寄一封提醒信給團隊」
- 「我使用者要去的城市現在天氣怎樣?」

沒有 tools,上面每一題的答案都是「我不知道」。有 tools 就能拿到即時、可信、可執行的答案。

---

## 產品使用情境

### 非用 Tool Use 不可的情境

| 使用者需求 | 為何只有 tools 能解 |
|----------|------------|
| 即時資料(股價、天氣、比分) | 不在訓練資料裡 — 必須 live fetch |
| 私有/內部資料(CRM、內部 wiki) | 訓練時從未看過 |
| 使用者個人狀態(我的行事曆、信箱) | 因人而異 — 不可能 pre-train |
| 需要副作用的動作(寄信、開 ticket) | 必須在現實世界真的發生 |
| 即時計算(查 DB、算即時數字) | 必須執行程式碼,不能幻想 |

### Tool Use 過度設計的情境

| 使用者需求 | 更好的替代方案 |
|----------|----------|
| 一般知識問答 | 基礎模型就夠 |
| 創意寫作/腦力激盪 | 不需要外部資料 |
| 重寫/摘要使用者貼上的內容 | 文字已經在 prompt 裡 |
| 解釋概念 | 訓練資料就足夠 |

---

## 四步驟流程(白話版)

1. **App 問 Claude** — 「這是使用者的問題,你可以用的工具在這。」
2. **Claude 舉手** — 「我要舊金山的天氣。幫我呼叫那個工具。」
3. **App 幫忙做** — 去打真正的天氣 API,拿到真資料。
4. **App 回 Claude** — 「天氣資料給你。」然後 Claude 綜合所有東西,回給使用者最終答案。

同一個使用者問題會產生兩次 API call。這有成本、延遲、可靠度的代價,排工期時要考慮進去。

---

## PM 決策框架

規劃 AI 功能時問自己:

| 問題 | 若是 | 意涵 |
|------|------|------|
| 答案依賴比模型訓練日期更新的資料嗎? | 是 | 需要 tools |
| 這功能需要真的執行動作,不只是聊? | 是 | 需要 tools |
| 這功能需要個別使用者/租戶的資料? | 是 | 需要 tools |
| 使用者會因為資料過期而抱怨? | 是 | 需要 tools |
| 功能純粹是語言處理(翻譯、摘要、改寫)? | 是 | 大概不需要 tools |

---

## 成本、延遲、可靠度的取捨

Tool use 強大但不是白吃的午餐。要先規劃:

- **延遲加倍** — 每一輪 tool-using turn 至少兩次 API round trip 加上工具本身的延遲。
- **Token 成本提高** — 對話歷史每輪成長;tool 定義每次 call 都算 input token。
- **新的失敗模式** — 上游 API 可能 fail、timeout、回壞資料。app 必須優雅處理。
- **可觀測性負擔** — 必須 log 每次 tool call 的參數與結果,才能 debug 生產問題。

好的 PM 習慣:在 PRD 裡加一條「tool reliability SLA」以及「tool 失敗時的 fallback 行為」。

---

## PM 常犯的錯

1. **相信 prompt engineering 能取代 tools** — 資料不在訓練裡,再神的 prompt 也變不出來。早點找工程師 escalate。
2. **低估延遲** — 兩次 API call 加一次工具呼叫輕鬆吃掉 3 到 5 秒。記得設計 loading state。
3. **沒預算處理 tool 錯誤** — 上游 API 會掛。要定義掛掉時使用者看到什麼。
4. **一次塞太多 tools** — 從一兩個高價值工具開始。每多一個 tool 就多一條 bug 與模型混淆的路徑。
5. **忘了 tool call 是可稽核的** — 每一個 Claude 採取的動作都該被 log,尤其是寫入操作。

> **Key Insight**
>
> Tool use 是決定你的 AI 產品是「花俏的 autocomplete」還是「真正助手」的那個功能。任何需要即時資訊、個人資料或真實動作的產品需求,都暗示著要用 tool use。這個區別是 AI PM 的入門門檻,也是 CCA 考試 D1(agentic architecture)與 D2(tool design)重複出現的考點。

---

## CCA 考試重點

- **D2(Tool Design & MCP Integration)**:認得 tool_use request/response 模式;知道 `tool_result` 必須指回 `tool_use_id`。
- **D1(Agentic Architecture)**:tool use loop 是所有 agent pattern 的基礎。Multi-turn reasoning with tools 是標準 agent 範例。
- 考題常見模式:情境問「Claude 該如何回答關於現在 X 的問題?」— 答案永遠是「定義一個 tool 讓 Claude 呼叫」。

---

## Flashcards

| Front | Back |
|-------|------|
| Tool use 的「飯店禮賓」比喻是什麼? | 禮賓讀遍所有書但不能離開大廳。Tools 就是給他一支電話,讓他可以打給外面的世界。 |
| 什麼情況下 tool use 不是對的答案? | 純語言處理(翻譯、摘要、改寫、腦力激盪)且不需要外部資料時。 |
| 加上 tool use 後延遲會怎樣? | 通常至少加倍 — 每個使用者問題至少兩次 API call 加上工具本身的延遲。 |
| 需要 tool use 的五大產品情境? | 即時資料、私有/內部資料、使用者個人狀態、有副作用的動作、即時計算。 |
| 為何 tool use 是 AI 產品的關鍵解鎖? | 它讓 Claude 能取得即時資料、執行真實動作,從博學聊天機器人變成能幹隊友。 |
| 任何用 tool 的功能在 PRD 裡一定要包含什麼? | Tool reliability SLA、tool 失敗時的 fallback、loading state UX、log/稽核需求。 |
| Prompt engineering 能取代 tools 抓即時資料嗎? | 不能 — 訓練裡沒有的資料,再怎麼巧妙的 prompt 也生不出來。 |
| 一次用到 tool 的使用者問題要幾次 API call? | 至少兩次 — 一次收 tool_use 請求,一次送 tool_result 拿最終答案。 |
