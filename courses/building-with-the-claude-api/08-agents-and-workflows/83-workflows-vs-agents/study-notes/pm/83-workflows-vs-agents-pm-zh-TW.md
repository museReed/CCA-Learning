# Workflows vs Agents — PM 觀點

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture (22%);D5 — Enterprise Deployment (20%) |
| Task Statements | 1.1 (agent vs workflow 架構)、1.2 (agentic loop)、5.1 (production pattern 選型) |
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 83 |

---

## 一句話總結

Workflow 是你能完整寫清楚的 AI 功能的可靠、便宜、可預測架構;Agent 是你沒辦法寫清楚的功能的彈性、昂貴、較不可預測架構——PM 的工作是把 pattern 對應到問題,而不是在 roadmap review 時挑聽起來比較帥的那一個。

---

## PM 為什麼該在意

每個 AI 功能的 PRD 都在暗中做這個架構選擇。如果你不刻意選,工程團隊會幫你選——通常選他們覺得比較有趣的那個,也就是 agent。六個月後你會在開會討論為什麼每 ticket 成本是 workflow 方案的 10 倍,而那個 workflow 本來可以用三分之一的時間上線。

這是那種「對使用者最好的答案幾乎永遠是比較不華麗的那個」的決策。

---

## 心智模型:生產線 vs 工作坊

**Workflow = 生產線**。每個站做一個工作。原料從頭進,產品從尾出。品質高、產能高、成本低,每個站都可以獨立量。缺點:這條線只能做一種產品。要換產品就要重新設計線。

**Agent = 工匠工作坊**。工匠牆上掛著工具,客戶給他一個目標(「幫我做張桌子」)。他根據這個特定需求挑工具、決定順序。輸出比較彈性——「幫我做張有多一個抽屜的桌子」走一樣流程。缺點:慢、每件成本高、比較難量,因為每次都不一樣。

大部分產品應該:生產線處理 80% 流量,工作坊處理需要手工的 20%。

---

## 完整比較表(PM 視角)

| 維度 | Workflow | Agent |
|------|----------|-------|
| **可靠度** | 高 — 每次相同結果 | 較低 — 偶爾會脫軌 |
| **每任務 cost** | 低、可預測 | 高、變動(1x-10x workflow 成本) |
| **Latency** | 低、可預測 | 較高、變動 |
| **Eval 複雜度** | 中等 — 逐步測試 | 高 — 必須測 emergent 行為 |
| **彈性** | 低 — 只能做你寫的 | 高 — 處理新情境 |
| **首次出貨時間** | 前期較長(要設計流程) | 前期較短(設計工具箱) |
| **處理新使用者請求的時間** | 一張新 ticket + 新分支 | 通常為零—— agent 直接處理 |
| **非預期失敗的 support ticket** | 低 | 高、較難診斷 |
| **使用者信任** | 靠可預測性穩定累積 | 高度依賴 inspection 和護欄 |

---

## 產品使用情境

### 什麼時候選 Workflow

| 情境 | 為什麼 |
|------|--------|
| 「用 3 個 bullet 摘要這篇文章」 | 純轉換,已知單一輸入 |
| 「抽取發票金額」 | 合規要求 deterministic 行為 |
| 「翻譯產品描述」 | 可量、可 cache、便宜 |
| 「客服 ticket 分類」 | 窄、可重複、eval 友好 |
| 任何受管制或稽核流程 | 可預測性不可妥協 |

### 什麼時候選 Agent

| 情境 | 為什麼 |
|------|--------|
| 跨未知 codebase 的寫程式助手 | 無法事先列出使用者會問什麼 |
| 「幫我搞稅務」對話工具 | 每個使用者的問題路徑都不同 |
| 創意內容生成 | 創意需要 tool 重組 |
| 開放式 debug 助手 | 無法事先預測 bug |
| 跨混亂 schema 的內部「資料分析師」 | 每個問題都需要重新探索 |

---

## Cost 和 Latency——商業數學

典型 3 步驟任務:

| Metric | Workflow | Agent |
|--------|----------|-------|
| 每任務 token 數 | ~3,000(固定) | ~3,000 - 30,000(變動) |
| 每任務 latency | ~3-6 秒 | ~5-30 秒 |
| Cost 倍數 | 1x(baseline) | 1x 到 10x |
| Support ticket | 1x(baseline) | 1.5x 到 3x(debuggability 成本) |

**PM 心法**:workflow 95% 準確、agent 96% 準確時,workflow 勝。你付 5-10 倍 cost 換 1 個百分點的準確度,這點通常用更好的 eval 或 workflow 重試就能補回來。

---

## PM 決策框架

每個 AI 功能跑這個序列:

| 步驟 | 問題 | Yes 去 | No 去 |
|------|------|--------|-------|
| 1 | 我能事先完整列出使用者流程嗎? | Workflow | 第 2 步 |
| 2 | 任務是純轉換(A -> B)嗎? | Workflow | 第 3 步 |
| 3 | 請求多元且不可預測嗎? | 第 4 步 | Workflow |
| 4 | 動作取決於即時環境 state 嗎? | Agent + inspection | 第 5 步 |
| 5 | 我們負擔得起 5-10x cost 和 eval 複雜度嗎? | Agent | 拆成更小的 workflow |

最後一個 sanity check:**如果我們做成 workflow,使用者會發現差別嗎?** 答案是「不會」就出 workflow。

---

## PM 常見錯誤

1. **因為 agent 聽起來潮就選 agent** — 「agentic」在 roadmap review 好賣,但大部分功能應該是 workflow。先把可靠度搞定。
2. **沒預留 agent 的 cost 倍數** — 每請求 cost 可能跳 5-10 倍沒人預測到。承諾前先估 agent cost。
3. **時程沒算 eval 複雜度** — Agent 的 eval 案例需要 3-10 倍多。加進估時,不要當成免費。
4. **PRD 寫死 tool 順序** — 逼工程團隊進 workflow 模式,即使 agent 更適合。寫目標,不要寫序列。
5. **漏掉混合方案** — Production 系統很少是純 agent 或純 workflow。Classifier + router 通常是兩邊的優點都拿到。

> **Key Insight**
>
> 預設答案是 workflow。使用者問題真的需要、而且你接受 cost、latency、eval overhead 時才選 agent。使用者不在乎你的架構,他們在乎功能穩定、負擔得起、可預測。把 pattern 對齊到問題是 agentic 產品裡最高槓桿的 PM 決策。

---

## CCA 考試關聯

- **D1 (Agentic Coding & Architecture)**:會出「workflow vs agent」情境題。公式:可預測且窄 -> workflow;不可預測且廣 -> agent;預設永遠 workflow。
- **D5 (Enterprise Deployment)**:Production trade-off(cost、latency、eval、reliability)大部分功能都偏向 workflow。這會直接考。
- 考題提示字:「compliance」「predictable」「cheapest」 -> workflow;「varied requests」「creative combinations」「novel situations」 -> agent。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Anthropic 對 workflow vs agent 的預設建議是什麼? | 預設 workflow;只有 workflow 解不了的問題才用 agent。 |
| 生產線 vs 工作坊的類比是什麼? | Workflow = 生產線(單一產品、高產能、便宜、可預測)。Agent = 工作坊(工匠配工具,彈性但慢且貴)。 |
| 列出三個 workflow 在 production 勝 agent 的維度。 | 可靠度、cost、latency、debuggability、可預測性、eval 簡單度(任三)。 |
| PM 什麼時候該選 agent 而不是 workflow? | 使用者請求多元、不可預測、需要創意 tool 組合,而且 workflow 準確度不夠時。 |
| 同一個任務 agent 相較 workflow 的典型 cost 倍數是多少? | 1x 到 10x,看 agent 跑幾次 loop 迭代。 |
| 什麼 PRD 錯誤會逼工程團隊選錯架構? | 寫死 tool 順序而不是寫使用者目標——會強制 workflow 模式,即使 agent 更適合。 |
| Production 系統常用的混合 pattern 是什麼? | Workflow router 把簡單案例送到 workflow 分支,難案例送到 agent。 |
| 決定選 agent 前的最後 sanity check 問題是什麼? | 如果做成 workflow,使用者會發現差別嗎?不會就出 workflow。 |
