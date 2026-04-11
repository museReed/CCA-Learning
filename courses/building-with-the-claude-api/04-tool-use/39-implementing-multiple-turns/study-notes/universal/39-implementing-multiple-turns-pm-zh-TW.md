# Implementing Multiple Turns — PM Perspective（繁中）

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture (22%) / D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 1.2（agentic loop 實作）、2.4（multi-turn tool loops）、1.3（multi-turn 對話管理） |
| 來源 | building-with-the-claude-api / 04-tool-use / Lesson 39 |

---

## 一句話總結

Agentic loop 是那個把 Claude 從 chatbot 變成 agent 的 15 行引擎——一旦你的團隊能可靠地 ship 它，所有你腦中想得到的 agent 產品就都可行了。

---

## 心智模型：咖啡師和點餐單

想像一個咖啡師看著點餐單做飲料：

| 步驟 | 咖啡廳 | Agentic Loop |
|------|--------|--------------|
| 讀點餐單 | 使用者問問題 | 用 messages 呼叫 Claude |
| 「還需要做什麼嗎？」 | 「Claude 要 tool 嗎？」 | 檢查 `stop_reason` |
| 要：磨豆、打奶泡⋯⋯ | 要：執行 tool | 執行 tool-use block |
| 把每個步驟的結果交回咖啡師 | 把 tool result 加到歷史 | Loop 回 Claude |
| 不要：完成飲料、結束 | 不要：回傳最終文字 | Break loop |

咖啡師會一直問自己「還有下一步嗎？」直到飲料完成。Loop 做的就是這件事——一直問 Claude「你還要做什麼動作嗎？」直到 Claude 說「不用了，我做完了」。

---

## 為什麼這解鎖了真正的產品價值

沒有 loop，你只能 ship「Claude 回答問題」。有了 loop，你可以 ship：

| 產品 | 做什麼 |
|------|--------|
| Coding assistant | 讀檔、跑測試、寫 patch、迭代 |
| 旅行規劃 | 查機票、篩價格、訂、確認 |
| 客服 agent | 讀 ticket、查 CRM、查知識庫、草擬回覆 |
| 數據分析師 | 跑 SQL、解讀結果、產生圖、寫摘要 |

Loop 是「agent」之所以是一個類別而不只是 buzzword 的原因。所有真實世界的 Claude agent——從 Claude Code 到 MCP client——都是這 15 行 pattern 加上 production hardening 的變體。

---

## 產品應用場景：何時該投資

### Loop 會回報成本的時候

| 信號 | 產品意義 |
|------|---------|
| 使用者想要「fire and forget」的工作流 | Loop 讓 Claude 自主完成多步驟任務 |
| 答案依賴外部資料 | Tool 呼叫抓資料，loop 迭代直到完成 |
| 使用者願意用延遲換品質 | Multi-turn loop 用速度換正確性 |
| 功能受益於迭代優化 | Loop 可以重試、篩選、比較、收斂 |

### Loop 是大材小用的時候

| 信號 | 更簡單的做法 |
|------|--------------|
| 單次查詢立即答案 | 一次 tool call，不用 loop |
| 純靜態知識 Q&A | 完全不用 tool |
| 即時對話 UI | 直接 streaming，不用 loop 那麼複雜 |

---

## PM 決策框架

規劃 agentic loop 功能前問：

| 問題 | 為什麼重要 |
|------|-----------|
| 迭代上限是多少？ | 無限 loop 會卡好幾分鐘、燒 token |
| 迭代之間怎麼顯示進度？ | 使用者要看得到每一步，不然會以為壞了 |
| 使用者可以中途取消嗎？ | 多步驟 agent 必須可以被打斷 |
| Loop 撞到上限但沒有最終答案怎麼辦？ | 「部分結果」UX 要設計 |
| 單一對話的 token 預算怎麼抓？ | 每次迭代都讓歷史變長，要規劃最糟情況 |
| 如何稽核跑過哪些 tool？ | Debug 和 compliance 都需要 |
| Tool 失敗的重試策略是什麼？ | 交給 Claude 處理、還是應用層硬重試？ |

---

## 常見 PM 錯誤

1. **把 loop 當成技術細節**——它是產品功能介面，每一回合都有 UX 決策（進度、取消、部分結果）
2. **沒設可見的迭代上限**——失控 loop 浪費預算、把使用者卡住；上限要調參數並寫進文件
3. **把 tool 錯誤藏起來不給 Claude 看**——tool 失敗的話 Claude 要用 `is_error=True` 知道，這樣才能恢復；藏起來會 hallucinate
4. **沒有觀測性計劃**——production debug agent loop 需要 log 每次迭代的 tool call 和結果
5. **沒平行化就上線**——能平行跑的 tool 不要串行，否則延遲翻倍或翻三倍

---

## 成本與延遲規劃

每多一次迭代就增加：

| 成本 | 典型量級 |
|------|---------|
| 一趟 API round trip | +300ms 到 +1s |
| 歷史變長 | 每次迭代 +10% 到 +30% input token |
| Tool 執行時間 | 看 tool 而定（毫秒到秒） |
| Output token | 每回合 +幾百 |

一個 5 次迭代的 loop 很容易就用掉單次呼叫 5 倍的 input token，wall time 要 3-10 秒。Prompt caching（課程後面會講）是 token 成本的標準緩解方式，但延遲成本是這個 pattern 的本質。

---

> **Key Insight**
>
> Agentic loop 是分開「Claude 功能」和「Claude agent」的最小單位。15 行程式碼解鎖一個新的產品類別。但那 loop 的每一行都對應一個產品決策：要迭代多久、進度怎麼顯示、失敗怎麼處理、成本上限在哪。把 loop 當「後端的事」的 PM 會 ship 壞掉的 agent；把它當「有五個旋鈕的產品介面」的 PM 會 ship 好的 agent。

---

## CCA Exam Relevance

- **D1（Agentic Architecture）**：Agentic loop 是標準的 agent pattern。考題會問 `stop_reason` 處理和迭代控制。
- **D2（Tool Design & MCP Integration）**：理解錯誤如何用 `is_error=True` 傳遞，以及藏錯誤為什麼會破壞 Claude 的恢復能力。
- 考題描述「Claude 連續做多個 tool 呼叫」——答案永遠是一個有 stop_reason 檢查的 loop。

---

## Flashcards

| 題目 | 答案 |
|------|------|
| 用什麼比喻來理解 agentic loop？ | 咖啡師看點餐單——一直問「還有下一步嗎？」直到飲料完成 |
| 哪一行程式碼是 loop 退出的信號？ | `if response.stop_reason != "tool_use": break` |
| 為什麼 agentic loop 是產品介面而不只是工程？ | 每次迭代都有 PM 決策：進度 UX、取消、成本、重試、部分結果 |
| Agentic loop 功能最大的隱藏成本是什麼？ | 歷史變長——每次迭代都加 token 到後續呼叫 |
| Production agent loop 必須包含哪些安全機制？ | Max iteration 上限、每次迭代的觀測性、用 `is_error=True` 傳遞錯誤 |
| 為什麼藏錯誤不給 Claude 看會適得其反？ | Claude 以為 tool 成功就無法恢復，會 hallucinate 出結果 |
| 哪些產品是靠 agentic loop 才有可能？ | Coding assistant、旅行規劃、客服 agent、數據分析師——任何需要多步推理的功能 |
| PM 應該為 5 次迭代的 agentic loop 抓多少延遲預算？ | 3 到 10 秒 wall time，加上隨迭代深度放大的 token 成本 |
