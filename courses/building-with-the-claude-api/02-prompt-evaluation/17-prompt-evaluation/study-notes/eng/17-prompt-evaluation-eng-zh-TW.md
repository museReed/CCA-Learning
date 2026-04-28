# Prompt Evaluation — Engineering Deep Dive（繁體中文）

| 項目 | 內容 |
|------|------|
| Exam Domain | D3 — Evaluation & Iteration（20%，主要）；D5 — Enterprise Deployment（20%，次要） |
| Task Statements | 3.1（eval 設計）、3.2（測試資料集）、3.3（eval 執行） |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 17 |

---

## 一句話摘要

Prompt engineering 是教你「如何寫」prompt 的技巧；prompt evaluation 則是自動化的度量方法，用來告訴你「這些 prompt 在真實輸入分布下到底有沒有用」。

---

## 兩個不同的紀律：工程 vs. 評估

使用 Claude 時，工作可以清楚分成兩塊。多數初學者只學會第一塊，就把東西推上 production，對 prompt 在真實流量下的表現完全沒有能見度。

| 紀律 | 核心關注 | 產出物 |
|------|----------|--------|
| Prompt engineering | *如何*寫出有效的 prompt | Multishot 範例、XML tags、system prompt、結構化輸出指令 |
| Prompt evaluation | Prompt *到底*表現多好 | 測試資料集、grader、數值分數、版本比較 |

Prompt engineering 是一門手藝；prompt evaluation 是把回饋循環閉起來的量測系統。

---

## 寫完 Prompt 後的三條路

你寫完第一版 prompt 之後，通常會面臨三個選擇，但只有一個選項能擴展到 production。

**選項 1 — 測一次就上。** 跑一兩筆輸入看起來還行就直接上線。風險：真實用戶馬上就會送來你沒測過的輸入，然後 prompt 就無聲無息地掛掉。

**選項 2 — 測幾次，邊角案例隨手修一修。** 比選項 1 好一點。你針對幾個你想得到的邊角案例迭代。風險：人類想像力無法取代真實輸入分布，用戶還是會讓你驚訝。

**選項 3 — 把 prompt 丟進 evaluation pipeline。** 建立資料集、用客觀 grader 評分，依指標迭代。代價：前期工和 API 花費較多。好處：你帶著「量測出來的信心」而不是「樂觀」上線。

課程講得很直白：選項 3 是唯一能產出可靠 AI 應用的路。選項 1 和 2 是「所有工程師都會掉進去的常見陷阱」。

---

## 為什麼測試陷阱這麼誘人

選項 1 和 2 感覺「很有生產力」，因為每改一版 prompt 就能立刻看到 Claude 回出更好的答案 — 立即多巴胺。但這種「軼事式驗證」極具誤導性。Production 流量有兩個手動測試無法重現的特性：

1. **量** — 真實用戶每天生成數千筆輸入，分布的尾端就是 prompt 崩壞的地方。
2. **不可預測性** — 用戶用開發者從沒想過的方式問問題、注入邊角案例、串接上下文。

一個在三筆手挑輸入上看起來「還不錯」的 prompt，在 production 可能有 30% 的失敗率，而你只會從一堆憤怒的客服工單得知這件事。

---

## Evaluation-First 的方法論

系統化的替代方案是：在打磨 prompt 之前，先投資一條 evaluation pipeline。報酬是四個具體能力：

- **在 production 之前找出弱點** — 失敗案例出現在你的筆電上，而不是客戶工單上。
- **客觀比較 prompt 版本** — 兩個 prompt 產出兩個數值，你拿分數高的那個，沒有爭論空間。
- **帶信心迭代** — 每次改動都對資料集驗證，你知道這是真的改善還是瞎貓遇到死老鼠。
- **建出可靠的應用** — 品質變成系統的可量測屬性，不再靠感覺。

代價是前期要花力氣建 eval harness，但這會累積複利：未來每一次 prompt 改動都走同一條 pipeline，邊際成本趨近於零。

---

## 在 CCA 課綱中的位置

Prompt evaluation 正好坐在兩個 domain 的交界：

- **D3 Evaluation & Iteration（20%）** — 這節課定義了這門紀律本身：量測、資料集驅動的迭代、客觀比較。
- **D5 Enterprise Deployment（20%）** — Eval 是 production 發佈前的品質閘門。沒有 eval pipeline 的 LLM 功能不該上線。

後面幾課會把這個流程 operationalize：18 講典型工作流、19 講資料集生成、20 建 eval runner、21–22 講 model-based 與 code-based grading。

---

## 常見錯誤

1. **把 prompt engineering 跟 prompt evaluation 混為一談** — 以為只靠寫 prompt 的技巧就夠，沒有量測層。
2. **只在一筆 happy-path 案例上測試** — 掉進選項 1 然後宣告完工。
3. **相信自己手挑的邊角案例涵蓋真實使用** — 選項 2 給你假信心，因為開發者的想像力不是 production 流量的隨機抽樣。
4. **因為「太貴」而跳過 eval** — Prompt 在 production 壞掉的代價（客服負擔、品牌傷害、流失）遠遠大於跑一次 eval 的費用。
5. **把 eval 分數當成最終答案而非回饋訊號** — 目標是迭代，不是一次性的數字。

---

> **Key Insight**
>
> Prompt evaluation 是把 prompt engineering 從手藝變成工程紀律的關鍵。沒有 eval，每次改 prompt 都是猜；有了 eval，每次改 prompt 都是可量測的改善。考 CCA 時只要看到「reliability」「iteration」「version comparison」這類字眼，答案一定指向 D3 的 eval pipeline。

---

## CCA 考試相關性

- **D3（Evaluation & Iteration）**：要能分辨 prompt engineering 與 prompt evaluation；要能辨認三條路並知道為什麼選項 3 才正確。
- **D5（Enterprise Deployment）**：Eval 是 production 準備度的前置條件；要能說明為什麼 ad-hoc 測試不夠。
- 考題關鍵字：「reliable」「measure」「objective」「iterate」「compare versions」→ 答案是 eval pipeline，不是再多調幾次 prompt。

---

## Flashcards

| Front | Back |
|-------|------|
| Prompt engineering 和 prompt evaluation 有什麼差別？ | Prompt engineering 是寫有效 prompt 的技巧集合；prompt evaluation 是自動化量測 prompt 表現的方法。 |
| 寫完 prompt 後有哪三條路？ | 1) 測一次就上、2) 測幾次補邊角案例、3) 丟進 eval pipeline 並依客觀指標迭代。 |
| 為什麼選項 1 和 2 在 production 會失敗？ | 真實用戶會送來開發者從未想過的輸入；手動測試無法重現 production 的量與不可預測性。 |
| 選項 3 的成本與效益？ | 前期工作與 API 成本較高，但能產出可量測的信心，在部署前抓出失敗案例。 |
| Evaluation-first 解鎖哪四項能力？ | 提早找出弱點、客觀比較版本、帶信心迭代、建出可靠應用。 |
| Prompt evaluation 主要對應哪個 CCA domain？ | D3 — Evaluation & Iteration（20%）。 |
| 課程中提到 prompt engineering 包含哪些技巧？ | Multishot prompting、XML tags 結構化，以及其他 best practices。 |
| 考題看到「reliability」要怎麼答？ | 要保證 prompt 可靠，答案是 evaluation pipeline，不是更多 prompt 調整。 |
