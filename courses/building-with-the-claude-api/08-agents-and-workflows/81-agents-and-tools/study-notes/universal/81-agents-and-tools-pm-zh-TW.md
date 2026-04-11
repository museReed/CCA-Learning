# Agents 與 Tools — PM 觀點

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture (22%) |
| Task Statements | 1.1 (agent 架構)、1.2 (agentic loop)、1.3 (agent 中的 tool use)、5.1 (production pattern 選型) |
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 81 |

---

## 一句話總結

Agent 讓你只出一個功能就能處理許多不可預期的使用者需求——你把目標跟一個簡單的工具箱交給 Claude,剩下的 Claude 自己搞定,不用你們團隊把每一種使用流程預先寫死。

---

## PM 為什麼該在意

對 PM 來說,「要做 agent 還是 workflow」其實是一個產品策略問題:「使用者請求是窄而可預測,還是廣而開放?」

| 情境 | Workflow 給你 | Agent 給你 |
|------|---------------|------------|
| 有限、重複使用情境 | 最高可靠度 | 不必要的複雜度 |
| 創意、開放式請求 | 脆弱、讓使用者挫折 | 彈性與驚喜 |
| 「我們知道使用者會問的 5 件事」 | Workflow 勝 | 過度工程 |
| 「使用者問的我們都沒想過」 | PM backlog 補不完 | Agent 勝 |

Agent 讓你出「一個完整能力」,而不是 N 個 feature flag。

---

## 心智模型:瑞士刀 vs 廚房小工具抽屜

一個專門化的 workflow 就像廚房那個放滿單功能小工具的抽屜:

- 酪梨切片器——切酪梨很好,蘋果不能用
- 分蛋器——只能分蛋
- 壓蒜器——壓蒜很好,薑就不行

Agent 則是瑞士刀:

- 刀、剪刀、螺絲起子、開罐器——每個工具都很單純
- 由 **使用者的創意** 決定怎麼組合
- 一支工具涵蓋製造商從沒想過的情境

用產品術語講:如果你的 PRD 裡列了一大串「功能 X、功能 Y、功能 Z」都在解相關問題,那你可能在做廚房小工具抽屜,其實該做瑞士刀。

---

## 產品使用情境

### 什麼時候選 Agent

| 情境 | 為什麼 Agent 勝出 |
|------|-------------------|
| 「幫我搞稅務」助手 | 使用者會問五花八門的問題,不可能事先列完 |
| AI 寫程式助手(Claude Code) | 任何語言、任何 codebase——不可能每個情境都預先做 workflow |
| 創意內容工作室 | 「幫我做個宣傳片」可以有一千種意思 |
| 跨內部混亂資料的客服 copilot | 不同客戶對不同系統有不同問題 |

### 什麼時候選 Workflow

| 情境 | 為什麼 Workflow 勝出 |
|------|---------------------|
| 「這份會議逐字稿幫我摘要」 | 已知輸入、已知輸出 |
| 「把這段產品描述翻譯」 | Deterministic、可測量、eval 便宜 |
| 「抽取發票欄位」 | 合規/稽核要求行為可預測 |
| 受管制流程(法律、醫療) | 每一步都需要可驗證 |

---

## 「可組合工具」原則(PM 版)

工程師會問你:「要做 `refactor_function` 這種 tool 還是 `edit_file` 這種?」答案幾乎永遠是比較泛用的那個。為什麼這對 roadmap 很重要:

1. **範圍自動擴大** — 一個泛用 tool 涵蓋了原本要開一堆 ticket 才能處理的使用者請求。
2. **Roadmap 抗意外** — 當使用者要求你沒想過的事情(一定會),agent 已經能處理。
3. **要維護的 feature 變少** — 每個窄 tool 都是一個要做 eval、要監控、要下架的 feature。
4. **出貨更快** — 五個 primitive 比五十個專用 tool 早半年上線。

**PRD 紅旗**:如果你的 PRD 列了 20 個窄 AI 動作,工程團隊可能花 6 個月還是 cover 不到使用者需求。改問:「涵蓋 80% 情境的最小工具箱是什麼?」

---

## PM 決策框架

規劃 AI 功能時,走這串問題:

| 問題 | 如果 Yes | 方向 |
|------|----------|------|
| 你能事先列出所有使用者流程嗎? | Yes | Workflow |
| 使用者的請求變化大、不可預測? | Yes | Agent |
| 「答錯」會有合規或安全風險? | Yes | Workflow(可預測) |
| 需要處理創意組合? | Yes | Agent |
| 每多一個情境就多一個 sprint? | Yes | 大概是 agent——你在跟錯的 pattern 打架 |
| 每次請求的成本非常敏感? | Yes | Workflow(便宜、token 少) |

---

## PM 常見錯誤

1. **寫死流程而不是目標** — PRD 寫「先呼叫 tool A 再呼叫 tool B」,即使 agent 更適合也把工程團隊逼進 workflow 模式。
2. **使用者一抱怨就加新 tool** — 正確做法是改進 system prompt 跟 tool 描述,不是硬塞 `handle_edge_case_47`。
3. **窄問題硬上 agent** — 「摘要這篇文章」不需要 agent。你付 3 倍 cost 換不到任何彈性。
4. **沒預留 eval 複雜度** — Agent 的 eval 難度是 workflow 的 3–10 倍。不先規劃,release cycle 會卡住。
5. **忽略 latency 影響** — 每次 agent loop 都多一次 round trip,話多的 agent 對使用者來說就是慢。

> **Key Insight**
>
> 無法事先列出使用者流程時選 agent,其他時候選 workflow。大部分 production AI 功能要嘛是假裝成 agent 的 workflow,要嘛是被 workflow 式 PRD 淹死的 agent。把 pattern 對齊到問題,是 agentic 產品裡最高槓桿的 PM 決策。

---

## CCA 考試關聯

- **D1 (Agentic Coding & Architecture)**:題目常問「使用者想做 X,你要做 workflow 還是 agent?」口訣:不可預測 = agent,可預測 = workflow。
- **D5 (Enterprise Deployment)**:要記得 agent 比較貴、比較難 eval,這是主要 production trade-off。
- 考題關鍵字:「varied requests」「novel combinations」 -> agent;「well-defined steps」「known sequence」 -> workflow。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| PM 什麼時候該選 agent 而不是 workflow? | 使用者請求多元、不可預測、無法事先列完時。 |
| 抽象 tool vs 專用 tool 的產品類比是什麼? | 瑞士刀(通用 primitive) vs 廚房小工具抽屜(每種情境一支工具)。 |
| 列出兩個 workflow 勝 agent 的產品情境。 | 摘要逐字稿、抽發票欄位、翻譯描述、受管制法律流程(任兩個)。 |
| 為什麼 agent 比 workflow 貴? | 每次 loop 迭代都是一次 API 呼叫和更多 token,開放式推理每個任務用更多 compute。 |
| PRD 出現什麼紅旗代表你該做 agent? | 一長串窄 AI 動作,都在解相關問題。 |
| 舉三個 PM 必須規劃的 agent 缺點。 | Cost 高、可靠度低、eval 難、latency 慢、行為不可預測(任三)。 |
| PM 為什麼不該在 PRD 裡過度指定 tool 順序? | 會把工程團隊逼進 workflow 模式,即使 agent 更適合,結果失去彈性優勢。 |
| Agent 設計最重要的 PM trade-off 是什麼? | 彈性 vs 可預測性——Agent 能處理新情境但比較難測、難 eval、難控制。 |
