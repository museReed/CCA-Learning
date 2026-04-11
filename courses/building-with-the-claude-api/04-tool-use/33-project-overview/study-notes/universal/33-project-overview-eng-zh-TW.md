# 專案概覽:提醒應用 — Engineering Deep Dive

| 項目 | 內容 |
|------|------|
| 考試 Domain | D2 — Tool Design & MCP Integration (18%) 主要;D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.1(tool schema 設計)、1.2(agentic loop 基礎)、1.1(把功能拆成 tool 組合) |
| 來源 | building-with-the-claude-api / 04-tool-use / Lesson 33 |

---

## 一句話總結

提醒應用專案示範 tool use 的核心設計原則:把模型能力的缺口拆成**一個個小型、單一職責的 tool**,讓 Claude 在推理時自行組合,而不是硬寫一個「什麼都包」的大 function。

---

## 目標使用者體驗

```
使用者: 「幫我設一個提醒,我要看醫生。是下下個星期四。」

Claude: 「好,我會提醒你。」
```

表面上超簡單 — 但底下藏了三個 base model 解不了的能力缺口。

---

## Claude 與目標之間的三個缺口

| 缺口 | 為什麼重要 | 對應的 tool |
|------|------------|-------------|
| **時間感知有限** | Claude 大概知道今天日期,但不知道此刻精確時間 | `get_current_datetime` |
| **日期運算容易算錯** | 「下下個星期四」需要日期相加;LLM 常會算錯星期幾、跨月處理也會出包 | `add_duration_to_datetime` |
| **沒有提醒能力** | Claude 本身沒辦法把排程提醒寫到任何系統裡 | `set_reminder` |

每個缺口恰好對應一個 tool。這不是巧合 — 就是設計原則本身。

---

## 設計原則:一個缺口 = 一個 tool

```
┌────────────────────────────────────────┐
│         使用者目標:設定提醒              │
└────────────────────────────────────────┘
             │
   拆成原子步驟
             │
 ┌───────────┼────────────┐
 ▼           ▼            ▼
get_current_  add_duration_  set_reminder
datetime      to_datetime
(現在)        (現在 + 7 天)  (寫入)
```

為什麼原子 tool 勝過一個「parse_and_set_reminder」大 function:

1. **可組合** — `add_duration_to_datetime` 可以被其他日期運算需求(生日、截止日、續約)重用。
2. **可測試** — 每個 tool 只做一件事,單元測試很簡單。
3. **可觀測** — log 能清楚看到哪一步掛掉,而不是「大 function 回了錯東西」。
4. **發揮模型強項** — Claude 擅長規劃序列。如果你把順序預先寫死在一個 function,就浪費了這個能力。
5. **優雅降級** — `set_reminder` 失敗時,已經算好的時間戳不會連帶遺失。

---

## 這個專案隱含的 Agent Loop

雖然每個 tool 都很簡單,三個 tool 組合起來代表對話可能要**三輪** tool-use turn,Claude 才會吐最終答案:

```
Turn 1: user → "幫我下星期四提醒"
Turn 2: Claude → tool_use get_current_datetime
Turn 3: app   → tool_result "2026-04-11 14:30:00"
Turn 4: Claude → tool_use add_duration_to_datetime(now, +7 days)
Turn 5: app   → tool_result "2026-04-18 14:30:00"
Turn 6: Claude → tool_use set_reminder(when="2026-04-18 14:30:00", ...)
Turn 7: app   → tool_result "ok, reminder created"
Turn 8: Claude → "好,我會提醒你。"  (stop_reason=end_turn)
```

這就是最小可行的 **agent loop** 範例:Claude 自行規劃 tool call 的順序,完全由使用者的自然語言輸入驅動。你的程式碼不會寫死順序 — 只是重複執行 Claude 下一步要求的任何 tool,直到 `stop_reason != "tool_use"`。

---

## 漸進式建構順序

課程一次建一個 tool,最簡單的先做。這與任何 tool-use 專案的 best practice 一致:

1. **先做 read-only 的 tool**(`get_current_datetime`)— 沒副作用,最容易測。
2. **接著做 pure-function 的 tool**(`add_duration_to_datetime`)— 決定性,仍然沒外部副作用。
3. **最後才做有副作用的 tool**(`set_reminder`)— 持久化、失敗模式、稽核軌跡。

這個順序也是安全梯度。Read-only tool 出錯風險低;寫入 tool 需要更多驗證與測試。

---

## 這個專案教我們如何 Scoping AI 功能

底層功課是**AI 功能的 scoping**。一個 naive 的工程師可能會寫:

```python
def handle_reminder_request(user_text: str) -> str:
    # 解析文字、做所有事、回一句確認
    ...
```

...然後試著 prompt Claude 去呼叫這個巨型 function。會失敗因為:

- 你把所有苦工(解析、日期運算、持久化)又搬回命令式程式碼裡。
- Claude 沒機會推理,變成「文字轉 function call」的分類器。
- 你失去在其他功能重用這些能力的機會。

Tool use 典範把這個**倒過來**:給 Claude 小的 primitive,讓它去編排。這是從「LLM 只是個聰明的字串 function」過渡到「LLM 是個 planner」的橋樑。

---

## 常見錯誤

1. **把多個能力塞進一個 tool** — 例如一個 `schedule_reminder(natural_language_time)` 內部解析字串。請拆開。
2. **寫死 tool 呼叫順序** — 讓 Claude 決定。你的程式碼只負責派發它下一步要什麼。
3. **從寫入 tool 開始做** — 先做 read-only tool,比較安全可以反覆迭代。
4. **跳過玩具專案階段** — 直接跳進生產程式碼,會讓失敗模式在真實使用者上爆炸。
5. **沒規劃 multi-turn loop** — 即便是簡單功能都可能要 3+ 次 tool call;你的 message loop 必須能處理任意輪數。

> **Key Insight**
>
> 提醒專案是**能力拆解**(capability decomposition)的案例研究:模型的每個原生限制恰好對應一個原子 tool,由 Claude 在推理時組合起來。這個倒轉 — 「給模型 primitive,讓它規劃」 — 正是 CCA 考試 D1(agentic architecture)反覆測驗的心智轉換。看到多步驟的自然語言目標就該想到它。

---

## CCA 考試重點

- **D1(Agentic Architecture)**:理解單一使用者請求可能需要多輪 tool call 的 loop,全部由模型規劃。
- **D2(Tool Design & MCP Integration)**:拆解原則 — 一個能力缺口 = 一個 tool。
- 考題常見模式:題目描述一個功能(「下星期提醒我」)然後問該設計幾個 tool 或哪種 tool — 答案會強調原子 tool 讓 Claude 組合。

---

## Flashcards

| Front | Back |
|-------|------|
| 提醒專案的目標使用者互動是什麼? | 「幫我設一個提醒,我要看醫生。是下下個星期四。」→「好,我會提醒你。」 |
| 提醒專案識別出哪三個能力缺口? | 時間感知有限、日期運算不可靠、沒有內建提醒機制。 |
| 專案裡建了哪三個 tool? | `get_current_datetime`、`add_duration_to_datetime`、`set_reminder`。 |
| 為何要做三個小 tool 而非一個大 tool? | 可組合、可測試、可觀測、發揮模型推理強項、優雅降級。 |
| Tool 是以什麼順序引入,為什麼? | 最簡單、read-only 的先(`get_current_datetime`)、再 pure function、最後才是有副作用的(`set_reminder`)— 安全梯度。 |
| 一次提醒請求可能要幾輪 tool-use turn? | 最多三輪 — 每個 tool 一輪 — 才會讓 Claude 吐最終自然語言確認。 |
| 這個專案示範的設計原則是? | 一個能力缺口 = 一個原子 tool;讓 Claude 規劃組合。 |
| 「LLM as planner」是什麼意思? | 不把 LLM 當作把文字分類到一個大 function 的東西,而是給它小 primitive 讓它去編排。 |
