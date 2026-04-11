# Sending Tool Results — PM Perspective（繁中）

| 項目 | 內容 |
|------|------|
| 考試領域 | D2 — Tool Design & MCP Integration (18%) / D1 — Agentic Architecture (22%) |
| Task Statements | 2.4（tool_result block 格式）、2.2（content block 處理）、1.2（收尾 tool-use loop） |
| 來源 | building-with-the-claude-api / 04-tool-use / Lesson 37 |

---

## 一句話總結

把 tool 結果送回 Claude 是「收件回執」的動作——一個格式嚴格的封包，用來收掉「Claude 要了一個東西」和「Claude 有足夠資訊可以回答」之間的迴圈。

---

## 心智模型：餐廳點餐票系統

想像一間忙碌的餐廳廚房：

| 廚房流程 | Claude tool-use 流程 |
|----------|---------------------|
| 外場寫票 #47：「漢堡，五分熟」 | Claude 發出 `ToolUseBlock(id="toolu_47", name="cook", input={"item":"burger"})` |
| 廚師做漢堡 | 你的程式執行 function |
| 廚師把票 #47 夾在盤子上 | 你送回 `tool_result` block，`tool_use_id="toolu_47"` |
| 盤子送到票 #47 對應的桌子 | Claude 用結果回答使用者 |

票號（`tool_use_id`）是神聖的。廚師忘了夾票，沒人知道漢堡要送哪一桌。一張票回兩個漢堡、或兩張票只回一個，整個出餐流程就會垮。Anthropic API 處理 tool result 的方式就是這樣。

---

## 為什麼 PM 要在乎

Tool result 是大多數 tool-use 功能在 production 壞掉的故障面：

| 故障模式 | 使用者看到的症狀 |
|----------|------------------|
| 後端在 tool 執行到一半 crash、丟掉結果 | Claude 整個卡住或回「抱歉我無法協助」 |
| 後端忘了用 `is_error: True` 標錯誤 | Claude 自信地給出錯誤答案（hallucinate 成功） |
| 多個 tool call 但後端只回一個結果 | 使用者看到 400，整段對話救不回來 |
| 後端直接塞 dict 而沒 serialize | 對話壞在看不懂的 validation error |

每一個都是產品品質問題。懂 tool-result 契約的 PM 可以寫出更好的 acceptance criteria，在 staging 就攔下來，不要等到上線日。

---

## 產品應用場景：錯誤能見度

Tool 失敗不只是工程問題——它是 UX 決策：

| 策略 | 什麼時候用 | UX 影響 |
|------|-----------|---------|
| 透過 `is_error: True` 把錯誤丟給 Claude | 大多數情況 | Claude 會自然解釋問題（「我抓不到股價，API 好像掛了，要再試一次嗎？」） |
| 在 Claude 看到前就攔下錯誤 | Rate limit、安全錯誤 | 自己做 UI toast，完全繞過 Claude |
| 靜默指數退避重試 | 暫時性網路錯誤 | 使用者看不到，但會增加延遲 |

預設模式——`is_error: True`——會給 Claude 足夠資訊優雅降級。跳過這個會讓 Claude 幻覺出成功，這是最糟的使用者體驗。

---

## PM 決策框架

任何使用 tool 的功能，PRD 都應該回答：

| 問題 | 為什麼重要 |
|------|-----------|
| 每個 tool 的 timeout 預算是多少？ | 慢 tool 會讓 UX 出現死區，需要 progress event |
| 如何把 tool 錯誤傳達給使用者？ | 透過 Claude（`is_error: True`）還是透過自己的 UI？ |
| Claude 如果連呼叫同一個 tool 兩次怎麼辦？ | Cache？冪等性？權限升級？ |
| Claude 可以看到敏感的錯誤細節嗎？ | 送進 Claude 前要剝掉內部 stack trace |
| 如何記錄 tool_use_id 配對以便觀測？ | Debug production 對話時非常關鍵 |

---

## 常見 PM 錯誤

1. **PRD 沒寫錯誤處理**——工程預設「log 然後丟掉」，會默默壞掉對話
2. **以為 tool result 就是 function 回傳值**——它有嚴格格式（role=user、content block 有特定欄位），會限制工程做法
3. **忽略多 tool 同時呼叫的情況**——「Claude 一次叫兩個 tool 怎麼辦」是真的設計問題，不是 edge case
4. **沒編觀測性預算**——tool_use_id 追蹤對 debug production 很重要，但通常一開始沒排進 scope
5. **把 `is_error` 當工程細節**——它其實是產品決策：要讓 Claude 解釋失敗，還是用自己的 UI 擋掉？

---

> **Key Insight**
>
> 每一個 `tool_result` 都是用 `tool_use_id` 做 key 的回執。PM 教訓：tool 失敗其實是偽裝的產品功能。選「Claude 看到錯誤並解釋」（`is_error: True`）還是「繞過 Claude 自己顯示錯誤」是 UX 決策，直接影響使用者信任和復原率。不要隨便上線——要刻意設計。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：記住 `tool_result` block 的欄位，以及它住在 user role message 裡。
- **D1（Agentic Architecture）**：理解 tool_result 是 agentic 請求/回應配對的後半段。
- 考題會描述 tool 失敗的情境，問你如何告知 Claude——答案幾乎永遠是「送一個 `is_error: True` 的 `tool_result` block」。

---

## Flashcards

| 題目 | 答案 |
|------|------|
| 用什麼比喻來理解 `tool_use_id` / `tool_result` 配對？ | 餐廳點餐票——每張票號都要從外場送到廚房再送回桌子 |
| 為什麼 `is_error: True` 是 PM 要在乎的事，不只是工程 flag？ | 它決定 Claude 要不要跟使用者解釋失敗，或是 UI 自己擋掉——這是影響信任的 UX 決策 |
| Tool result 最糟的故障模式是什麼？ | 靜默成功——忘了填 `is_error: True`，讓 Claude 幻覺出成功結果 |
| 任何使用 tool 的功能 PRD 必須寫什麼？ | Timeout 預算、錯誤處理策略、多 tool 行為、tool_use_id 的觀測性 |
| 為什麼 `content` 直接塞 dict 會壞？ | API 要求 `content` 是字串（或 block list），dict 要 JSON serialize |
| Claude 一次叫兩個 tool，要回幾個結果？ | 剛好兩個——每個 `ToolUseBlock` 都要在同回合有對應的 `tool_result` |
| `tool_result` block 放在 message 結構的哪裡？ | 放在 user role message 的 `content` array 裡 |
| Production 中後端掉了一個 tool result 會怎樣？ | 下一次 API 呼叫回 400，對話救不回來，使用者會看到錯誤 |
