# The Server Inspector — PM 視角

| 項目 | 說明 |
|------|------|
| 考試領域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.3（MCP primitives）、2.1（tool schema 設計）、1.2（agent loop 整合） |
| 來源 | building-with-the-claude-api / 07-mcp / Lesson 65 |

---

## 一句話總結

MCP Inspector 是你 AI 功能 tool 的「QA 站」——一個瀏覽器 UI，讓團隊任何人在 tool 還沒碰到 Claude 或真實使用者之前，就能直接演練——大幅降低 debug 和驗收測試成本。

---

## 心智模型：Tool 的產品測試實驗室

想像你要推出一個新實體產品。出貨前，你會把原型送進測試實驗室：按按鈕、確認輸出、檢查 edge cases。這就是 MCP Inspector 對軟體 tools 做的事：

| 產品測試實驗室 | MCP Inspector |
|--------------|---------------|
| 工作台上的原型 | 用 `mcp dev` 跑的 MCP server |
| 按每個按鈕 | 點「List Tools」和「Run Tool」 |
| 驗證每個輸出 | 讀 panel 裡的結果 |
| 記錄缺陷 | 收集失敗的輸入回饋給團隊 |
| 出貨前簽核 | 在接到 Claude 之前確認 tool 能動 |

重點是：你不會把微波爐直接給顧客來發現它會爆炸。你也不該把壞掉的 MCP tool 直接推到 production 的 Claude flow 裡才發現。

---

## 為什麼這節課對 PM 重要

三個形塑產品的理由：

1. **驗收測試變得 PM 也能做。** Inspector 是一個 UI——PM 或 QA 不用跑 Claude API 呼叫、不用寫測試 code 就能演練 tool。意思是 PM 可以直接驗證 tool 行為。
2. **Debug 成本下降。** Claude「做錯事」時，第一個問題通常是「是 tool 壞掉，還是 Claude 用錯？」Inspector 秒級就能答。
3. **Tool 可 demo。** Inspector 也是一個 live demo surface。你可以對利害關係人展示「這個 tool 用真實輸入做什麼」——不需要協調跑完整 app。

---

## 產品應用場景

### 什麼時候該把 Inspector-first 當團隊規範

| 情境 | 為什麼 |
|------|-------|
| QA 在 release 前跑驗收測試 | 新或改的 tool 都先在 Inspector 驗過 |
| PM 驗收工程 handoff | PM 可以點每個 tool 確認符合 spec |
| 利害關係人 demo | 展示原始 tool 結果不需要 LLM 包裝 |
| Bug triage 會議 | 在 Inspector 重現「tool X 回傳意外資料」，不需要 chatbot |

### 只靠 Inspector 不夠的情境

| 情境 | 還需要什麼 |
|------|-----------|
| End-to-end agent 行為 | 完整 chatbot + prompts + Claude |
| Tool description 品質 | Chatbot 看 Claude 會不會選對 tool |
| 多輪 workflow | 完整 agent loop；Inspector 只測單次呼叫 |
| Multi-tenant 或 auth 情境 | 需要真實 client 連線路徑 |

---

## PM 決策框架：採用 Inspector-first 測試

你在做用 MCP tool 的 AI 功能時要問：

1. **新 tool 能在 merge 前都在 Inspector 驗過嗎？** 把它變成 PR 的檢查項。
2. **QA 驗收流程裡有 Inspector 嗎？** 訓練一次；每次 release 都有回報。
3. **每個 tool 有標準化的 Inspector 測試 case 嗎？** 標準化「list → call read → call edit → re-read」。
4. **失敗 case 也有測嗎？** 不只 happy path——丟假輸入驗證錯誤訊息。
5. **Inspector URL 有放進團隊 onboarding 文件嗎？** 讓新人發現它很簡單。

---

## Inspector 在 PM 層級改變了什麼

歷史上，測試 AI 功能是：

> 「問 chatbot 幾個問題，看答案對不對。」

這純粹是 end-to-end——慢、不穩、遮住 bug 真正位置。Inspector 給一個不同的測試單位：

> 「直接打 tool；它行為符合 spec 嗎？」

這比較接近 PM 已經會做的正常軟體 QA。Inspector 把 MCP tools 帶進**可測試軟體元件**的領域，而不是「神奇黑盒 AI 輸出」。這對任何做 Claude 基礎功能的團隊是信心層級的轉變。

---

## 運營考量

| 考量 | PM 為什麼該在意 |
|------|---------------|
| `mcp dev` 只能 dev 用 | 不要在 production 跑，它不是真實 client surface |
| UI 在積極變動 | 訓練概念（list、call、chain）而不是截圖 |
| Port `6277` 衝突 | 被擋的話開發流程卡住——標記為 infra 項目 |
| Inspector 結果該記錄 | 如果團隊用它做驗收，要留記錄 |
| Inspector 不測 prompts | 記得：只有透過 Claude 才會出的 bug，Inspector 無法重現 |

---

## 常見 PM 錯誤

1. **以為 end-to-end 測試就夠了。** End-to-end 會藏住 bug 在哪；Inspector 會暴露它。
2. **跳過負面測試 case。** PM 驗收測試應該包含「壞輸入 → 看到合理錯誤」。
3. **把 Inspector 當成只有工程用。** 它是 UI，任何人都能用。讓 QA 和 PM 開車。
4. **不 versioning Inspector 測試 case。** 留一份標準測試清單——不然 regression 會溜進來。
5. **把 Inspector 成功等同產品成功。** Inspector 驗證 tool；你還需要 agent/chatbot 測試驗證體驗。

> **Key Insight**
>
> MCP Inspector 把 MCP tool 測試從「AI 魔法的一部分」搬到「正常產品 QA 的一部分」。它把 tools 重新框成可檢視、可測試、可重現的元件——也讓 PM 不用跑 code 就能擁有 tool 驗收。任何 MCP 基礎的功能，「我們有 Inspector 測過嗎？」都該變成 definition-of-done 的一項。

---

## CCA 考試重點

- **D2（Tool Design & MCP Integration）**：知道 `mcp dev mcp_server.py` 啟動瀏覽器基礎的 Inspector，且它暴露 Tools、Resources、Prompts 區塊。
- **D1（Agentic Architecture）**：認識 Inspector 是無 LLM 的測試表面——在隔離 tool bug 和 agent bug 時有用。
- 情境題：「一個 tool 在 Inspector 能動但在 chatbot 不行——bug 可能出在哪？」→ 不是 tool 本身，更可能是 prompt、tool description、或 agent loop。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 用 PM 的話說，MCP Inspector 是什麼？ | 一個瀏覽器基礎的 QA 站，讓團隊任何人直接演練 tools，不需要 Claude。 |
| 為什麼 Inspector-first 測試是產品贏家？ | 把 tool bug 和 LLM bug 隔離、降低 debug 成本、讓 PM/QA 不寫 code 就能做驗收測試。 |
| Inspector 能測試 prompts 或 agent 行為嗎？ | 不能——它只測 MCP server 的 tools/resources/prompts primitives。 |
| PM 該在新 MCP tool 的 definition-of-done 加什麼？ | 「Inspector 已測（happy path + 至少一個失敗 case）」。 |
| Inspector 能測哪三種 primitive？ | Tools、Resources、Prompts。 |
| 為什麼 Inspector 通過後還要跑 chatbot 測試？ | 驗證 Claude 會正確選擇並使用 tool——這是體驗層級的關注點。 |
| Inspector 的 demo 價值是什麼？ | 利害關係人可以看到原始 tool 輸出，不需要完整 app runtime。 |
| Inspector 可以在 production 跑嗎？ | 不行——它只能 dev 用（`mcp dev`）。 |
