# Tool Functions — PM Perspective

| 項目 | 內容 |
|------|------|
| 考試 Domain | D2 — Tool Design & MCP Integration (18%) 主要;D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.2(tool function 定義)、2.1(tool schema 設計)、1.2(agentic loop 基礎) |
| 來源 | building-with-the-claude-api / 04-tool-use / Lesson 34 |

---

## 一句話總結

Tool function 是 Claude 實際執行的程式碼 — 你工程團隊怎麼寫它(命名、驗證、錯誤訊息)直接決定你的 AI 功能對使用者而言有多可靠。

---

## 心智模型:廚房出餐線

把你的 AI 產品想像成一間餐廳:

- **Claude** = 跟客人點餐、決定把每道任務丟給哪個廚檯的服務生。
- **Tool function** = 真正做菜的線上廚師。
- **Schema** = 服務生讀的食譜卡。
- **錯誤訊息** = 廚師出事時喊回去的話(「香菇不夠!」vs.「出事了!」)。

食譜卡清楚、廚師喊具體可行動內容的餐廳,運作順暢。廚師只會對服務生哼哼的餐廳,一片混亂。Tool function 就是你的出餐廚師 — PM 的職責是確保他們講話清楚。

---

## PM 為何要關心 Tool Function 設計

Tool function 設計看起來像工程細節,卻直接出現在使用者體驗上:

| Tool function 品質 | 使用者會看到的症狀 |
|-------------------|--------------------|
| 名字含糊 | Claude 挑錯 tool — 功能做錯事 |
| 沒輸入驗證 | Tool 回垃圾 — 使用者看到自信的胡說八道 |
| 錯誤訊息沒用 | Claude 無法復原 — 使用者看到「抱歉,我做不到」 |
| 錯誤訊息豐富可行動 | Claude 自我修正 — 使用者只看到正確答案 |

第三、第四列是重點。AI 功能「感覺可靠」與「感覺壞了」的差別,常常就在你的錯誤訊息能不能讓 Claude 自己復原。

---

## 設計好 Tool Function 的產品情境

### 投資會回本的情境

| 情境 | 為何好設計很重要 |
|------|-----------------|
| 高流量的使用者面向功能 | 微小的可靠度改善會在使用者間複利疊加 |
| 多步驟 workflow | 鏈中每個 tool 都是潛在失敗點 |
| 不可逆動作的功能 | 驗證能避免真實世界的損害 |
| 複雜參數(日期、ID、金額) | LLM 在沒有護欄時超容易出錯 |

### 過度設計的情境

| 情境 | 原因 |
|------|------|
| 內部開發工具 | 工程師能忍受粗糙的邊緣 |
| 一次性 prototype | 先出貨再補強 |
| 唯讀 debug 工具 | Blast radius 小 |

---

## 驗證 → 復原的 Loop

這是本課最重要的產品概念:

```
Claude 用壞輸入呼叫 tool
       ↓
Tool 丟出描述性錯誤
       ↓
錯誤變成 tool_result(is_error=True)
       ↓
Claude 下一輪讀到錯誤
       ↓
Claude 帶著修正後的輸入重試
       ↓
成功 — 使用者從未看到失敗
```

從使用者角度看,這個 loop 是隱形的。他們只看到「成功了」。但鏈上任何一環斷掉(錯誤訊息含糊、沒有捕捉例外、靜默失敗),整段就會塌成可見的錯誤。

PM 應該把「tool 錯誤復原」明確寫進 AI 功能的 PRD acceptance criteria。

---

## PM 決策框架

規劃 tool-using 功能時,文件上要寫清楚:

| 項目 | 為何重要 |
|------|----------|
| Tool 名稱與清楚的用途描述 | 影響 Claude 選 tool 的準確度 |
| 每個參數的允許值與格式 | 避免默默的垃圾輸出 |
| 非法輸入會發生什麼事 | 定義復原 UX |
| 若復原失敗,會給使用者看什麼訊息 | 使用者面向的文字需要 PM 審核 |
| 副作用與 idempotency | 決定重試是否安全 |
| 可觀測性 hook(log、metric) | 為生產 debug 做準備 |

---

## PM 常犯的錯

1. **把 tool function 當成「純工程」** — 跳過設計 review 導致命名、驗證、錯誤訊息不一致。
2. **沒在 PRD 寫錯誤訊息** — 工程師最後寫給開發者看的錯誤,Claude(與使用者)都無法用來復原。
3. **忽略 idempotency** — 若 Claude 因錯誤重試 create-reminder,你會多一筆提醒。PRD 應指定去重行為。
4. **低估名字的影響** — 「set_reminder」vs.「create_reminder」vs.「reminder」看似互換,實際上會改變 Claude 選對 tool 的機率。
5. **沒有可觀測性** — 沒 log tool call 與結果,生產失敗無法 debug、功能可靠度也無從測量。

> **Key Insight**
>
> Tool function 品質不是實作細節 — 它直接決定你 AI 功能的可靠度與 UX。你工程團隊寫的錯誤訊息,Claude 每次重試都會讀到,所以實際上是你產品文案的一部分。把 tool function review 當成 PRD 等級的事情來處理的 PM,會做出明顯更可靠的功能。CCA D2 直接測這一點。

---

## CCA 考試重點

- **D2(Tool Design & MCP Integration)**:Tool 命名、驗證、錯誤處理作為復原訊號、idempotency 顧慮。
- **D1(Agentic Architecture)**:錯誤如何透過 agent loop 流回並讓 Claude 自我修正。
- 預期會出「含糊錯誤」vs.「描述性錯誤」結果的對比題 — 描述性永遠勝出。

---

## Flashcards

| Front | Back |
|-------|------|
| Tool function 的餐廳比喻是什麼? | Tool function 是線上廚師、Claude 是服務生、schema 是食譜卡、錯誤訊息是廚師對服務生喊回去的話。 |
| 為何錯誤訊息對 PM 而不只是工程師重要? | 因為 Claude 重試時會讀它 — 錯誤訊息的品質決定使用者是看到可見失敗還是無感復原。 |
| Tool-using 功能的 PRD 應該寫什麼? | Tool 名稱與用途、參數驗證規則、錯誤復原 UX、使用者面向的錯誤文案、副作用/idempotency 規則、可觀測性 hook。 |
| 什麼是驗證-復原 loop? | 壞輸入 → 描述性錯誤 → tool_result with is_error → Claude 重新規劃 → 修正後重試 → 使用者從未看到失敗。 |
| 為何寫入型 tool 的 idempotency 是 PM 的事? | Claude 可能在錯誤後重試;沒有 idempotency 就會重複寫入,例如一次請求產生兩筆同樣的提醒。 |
| 含糊的 tool 名字會造成什麼使用者可見症狀? | Claude 挑錯 tool,功能做錯事 — 使用者看到自信的胡說八道。 |
| PM 在 tool function 設計 review 的角色是什麼? | 確保命名、驗證、錯誤文案、復原 UX 都在 PRD 裡明確定義並於實作前 review。 |
| 什麼時候投入大量 tool function 設計是過度設計? | 內部開發工具、一次性 prototype、唯讀 debug 工具,blast radius 小。 |
