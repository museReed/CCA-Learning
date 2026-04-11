# Tool Schemas — PM Perspective

| 項目 | 內容 |
|------|------|
| 考試 Domain | D2 — Tool Design & MCP Integration (18%) 主要;D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.1(tool schema 設計)、2.2(tool function 定義)、1.2(agentic loop 基礎) |
| 來源 | building-with-the-claude-api / 04-tool-use / Lesson 35 |

---

## 一句話總結

Tool schema 是你的 AI 在決定如何幫使用者之前會讀的產品文案 — 把它的文字當成 app store 描述來對待,因為 Claude 就是這樣看它。

---

## 心智模型:菜單項目描述

想像一份餐廳菜單:

- 菜名 **name**(「辣味鮪魚捲」)— 告訴客人這東西存在。
- 菜單敘述 **description**(「新鮮黃鰭鮪、辣醬美乃滋、蔥、6 貫」)— 告訴客人何時該點、能預期什麼。
- **過敏原/辣度/價格** 註記 — 限制誰該點。

Tool schema 對 Claude 來說正是這樣:

| 菜單概念 | Schema 欄位 |
|----------|-------------|
| 菜名 | `name` |
| 菜單敘述 | `description` |
| 食材/過敏原/辣度 | `input_schema.properties`(含 type、description、enum) |
| 必選選項(如「請選配菜」) | `input_schema.required` |

敘述含糊的菜單(「魚料理 $12」)點單少、客人疑惑多。敘述豐富的菜單能把對的菜送到對的人。Tool schema 也一樣。

---

## 為何 PM 應該擁有描述文案

多數工程師會很樂意寫「Gets current time」這種一句話描述然後閃人。那句話是*Claude 每次呼叫時會讀的產品文案*。寫一份好描述只花幾分鐘,可靠度紅利卻龐大。

PM 應該:

1. **每個 tool 的 `description` 都要 review**,像審 app store 列表或 onboarding 文案一樣。
2. **提供「何時使用」那一句** — 這是描述裡最有價值的一句,工程師最常跳過。
3. **列出相關 tool** 幫 Claude 區分。
4. **在屬性描述裡放具體範例**。

---

## 產品情境:Schema 品質真正改變結果的地方

| 情境 | Schema 品質如何幫忙 |
|------|--------------------|
| 多個類似的 tool(如多個日曆動作) | 描述讓 Claude 挑對而非用猜的 |
| 使用者講話含糊 | 「何時使用」那句把 Claude 引導到對的 tool |
| 嚴格的參數格式(ID、日期、SKU) | 屬性描述與 enum 避免呼叫格式錯誤 |
| 不同語言的使用者 | 豐富的描述讓 Claude 把翻譯對應到對的 tool |
| 高風險動作(付款、刪除) | 明確的必填欄位避免意外遺漏 |

---

## 三個欄位的白話解釋

| 欄位 | 對 PM 而言的意思 |
|------|-------------------|
| `name` | 內部 ID。當作 slug。短、無歧義、snake_case。 |
| `description` | 銷售話術。告訴 Claude *做什麼*、*何時用*、*回傳什麼*。3-4 句。 |
| `input_schema` | 訂單表格。哪些欄位必填、哪些值合法、什麼單位、什麼格式。 |

把這三個當成 PRD 的三個欄位:身分、價值主張、設定。

---

## 「何時使用」那一句

Schema 文案最常被省略的,就是告訴 Claude**何時**該挑這個 tool 而不是別個。例:

- 差:「回傳今天的日期。」
- 好:「回傳今天的日期。**當使用者問今天、明天、或任何相對日期時使用此 tool。**」

PRD 裡,每個 tool 都明確寫一行:

> Claude 應在此時使用此 tool:*(一句話)*

這會逼 PM 與工程師在寫 code 前先對齊 tool 的用途,這句話接著就直接寫進描述。

---

## PM 對 Schema 設計的決策框架

對功能中每個 tool 問:

| 問題 | 產出 |
|------|------|
| 什麼名字能無歧義地標示這個 tool? | `name` |
| 「何時使用」的一句話是什麼? | `description` 第一句 |
| 這個 tool 回傳什麼、什麼格式? | `description` 最後一句 |
| 哪些參數是嚴格必填? | `input_schema.required` |
| 每個參數,合法值是什麼?(enum?範圍?格式?) | 屬性 `type`、`enum`、`description` 內範例 |
| 有沒有 Claude 可能混淆的相關 tool? | `description` 內交叉引用 |
| Claude 傳錯參數會發生什麼? | 定義復原 UX(連結到 tool function 的錯誤處理) |

---

## PM 常犯的錯

1. **讓工程把一句話描述出貨** — 跳過文案 review,Claude 就會把使用者請求導錯路。
2. **寫實作細節而非意圖** — 「呼叫 /v1/time endpoint」對 Claude 毫無幫助。
3. **忘了列舉合法值** — 「溫度單位」應該是 `enum: ["celsius", "fahrenheit"]`,不是自由字串。
4. **沒交叉引用相似 tool** — 在多 tool 系統裡,Claude 需要協助區分。「此 tool 回傳現在時間;要排程未來事件請用 `create_reminder`。」
5. **改 code 沒改 schema** — 參數改名與新增 optional 欄位都必須同步到 schema,否則 Claude 的先驗會過期。

> **Key Insight**
>
> Tool schema 描述是你的 AI 會讀並據以行動的產品文案。把它當成工程的事後補充,等於 app 上架卻留空 app store 描述:下載變少、體驗變差。PM 要像擁有 UI 文案那樣嚴格擁有 schema 文案,才能做出感覺明顯更能幹的功能。CCA 考試 D2 的 tool design 與選擇類題目會直接考這點。

---

## CCA 考試重點

- **D2(Tool Design & MCP Integration)**:Tool 定義三個必填欄位、描述 best practice、`required` 語意、`enum` 用於限制值。
- **D1(Agentic Architecture)**:描述品質驅動 Claude 在 agent loop 中選 tool。
- 預期會出產品框架的題目:「團隊有兩個類似 tool,Claude 常選錯,最可能的修正是?」— 答:改善描述、加入「何時使用」句、在 tool 間交叉引用。

---

## Flashcards

| Front | Back |
|-------|------|
| Tool 定義的三個必填欄位是什麼? | `name`、`description`、`input_schema`。 |
| Tool schema 的菜單項目比喻是什麼? | Name 是菜名、description 是菜單敘述、properties 是食材/限制、required 是「必選配菜」。 |
| Schema 描述最常被跳過的一句是? | 「何時使用」那一句 — 告訴 Claude 當多個 tool 可選時該挑哪個。 |
| 為何 PM 應該 review tool 描述? | 它是 Claude 每次呼叫時都會讀的產品文案;直接影響功能可靠度與使用者體驗。 |
| 要怎麼避免 Claude 混淆兩個相似的 tool? | 在每個描述內交叉引用(「若要做 X 請改用 `other_tool`」)。 |
| 什麼時候該在參數描述用 `enum`? | 當合法值是固定集合(如單位、狀態、類別)時 — 消除模糊性。 |
| Tool schema 的 `required` 是什麼意思? | 它列出 Claude 必須提供的參數名;沒列的就是 optional。 |
| PRD 裡哪一行能捕捉 tool 對 Claude 的用途? | 「Claude 應在此時使用此 tool:*(一句話)*」— 直接寫進描述。 |
