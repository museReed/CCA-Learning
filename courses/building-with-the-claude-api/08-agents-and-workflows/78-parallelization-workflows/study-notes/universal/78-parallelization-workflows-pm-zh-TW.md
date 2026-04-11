# Parallelization Workflows — PM 觀點

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture(22%)— 主要 |
| 任務陳述 | 1.2(agentic 模式 — parallelization)、5.2(production workflow 部署)|
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 78 |

---

## 一句話總結

當品質取決於「每個準則的深度」時,parallelization workflow 就是正確的產品選擇:不要叫 Claude 在一個 prompt 裡同時應付 10 個準則,而是平行跑 10 份聚焦的子分析,再匯總出結論 — 答案更好、延遲差不多,代價是 API 花費變多。

---

## 心智模型:品酒小組

想像你要為餐廳菜單挑一支酒。

| 做法 | 長什麼樣 | 結果 |
|------|---------|------|
| 一位通才品酒師 | 「這支酒好嗎?」 — 全包一次答 | 普通、搖擺的判斷 |
| **專家小組(parallelization)** | 一位專精酸度、一位 tannin、一位尾韻、一位性價比、一位配餐,加一位主審匯總 | 各軸深度足夠 + 整合最終判定 |

Parallelization workflow 就是專家小組。每位專家只專注於*一個*軸向;一位主審看完所有專家筆記後做最後裁決。決策更好、比依序跑還快,但代價是每位專家都要付錢。

---

## 產品場景

### 適合 Parallelization 的情境

| 場景 | 為什麼 Parallelization 有效 |
|------|---------------------------|
| 材料推薦(課程範例)| 每種材料都需要深入、專門的評估 |
| 履歷篩選(按面向分優缺點)| 技能、經驗、文化適配獨立評估 |
| 內容 moderation 投票 | 高風險決策跑 N 次安全檢查取多數決 |
| 多準則 code review | 安全 reviewer + 風格 reviewer + 效能 reviewer + 可維護性 reviewer |
| 多視角客戶回饋分析 | 情感、急迫性、主題、是否要行動 — 各自一個子任務 |
| 跨多面向文件比較 | 法律、財務、技術面向並行分析 |

### 不該用 Parallelization 的情境

| 場景 | 更好的選擇 |
|------|-----------|
| 有序列依賴的任務 | 用 **chaining**(Lesson 79)|
| 單純單一答案的問題 | 一個 Claude 呼叫就夠 |
| 成本是首要限制 | 單一 prompt + 精心設計的準則 |
| 子任務無法真正獨立 | Chaining 或 agent |

---

## 兩種變體

| 變體 | 產品用途 | 範例 |
|------|---------|------|
| **Sectioning** | 把一個決策拆成多個面向 | 材料推薦(每種材料一個 LLM)|
| **Voting** | 同一評估跑 N 次求可靠度 | Moderation:「這安全嗎?」× 5 投票者,多數決 |

Sectioning 靠聚焦注意力提升*品質*。Voting 靠平均化噪音提升*可靠度*。有些功能兩者都需要(例如「3 個風險類別各跑 5 次安全投票」)。

---

## PM 決策框架

問自己:

| 問題 | 是 | 行動 |
|------|----|------|
| 決策是否依賴多個獨立準則? | 是 | Sectioning 候選 |
| 子任務是否需要彼此的輸出? | 是 | 不是 parallelization — 用 chaining |
| 品質 > 成本? | 是 | Parallelization 合適 |
| 延遲是關鍵 metric? | 是 | 平行 N 呼叫 ≈ 最慢一次(好消息!)|
| 需要高可靠度的二元決策? | 是 | Voting 變體 |

---

## 業務價值翻譯

把這個架構向工程或財務提案時,翻成商業語言:

- **品質** — 「每個準則得到專家級分析,而不是整體的通才分析」
- **延遲** — 「使用者等的是最慢子任務,不是所有子任務加總 — 感知速度差不多」
- **成本** — 「API 帳單乘以 N,但每個子任務通常比單一巨型 prompt 更小更快,實際成本不一定爆」
- **可擴充** — 「加一個準則 = 加一個 prompt 檔,現有準則零回歸風險」
- **A/B 測試** — 「改一個子任務 prompt 不用重測其他」

---

## PM 必須要求的 Production Guardrails

準備出貨 parallelization workflow 時,要請工程加上:

1. **Per-task timeout** — 單一慢呼叫不該拖住整個請求
2. **部分結果處理** — 6 個子任務成功 5 個失敗 1 個時,能否產生可用匯總?
3. **Fan-out 上限** — 不讓 N 依使用者輸入無限成長
4. **成本警示** — parallelization 會乘 token 花費,異常要看得到
5. **Aggregator fallback** — aggregator LLM 失敗時有沒有規則型 fallback?

---

## PM 常見錯誤

1. **把 parallelization 和 agent 混淆。** Parallelization 跑的是多個*預先決定*的子任務,程式碼仍然掌握 flow。它仍是 workflow。
2. **少了 aggregator 步驟。** 把「這裡有 6 份分析」丟給使用者是失敗 — 使用者要一個答案,不要陪審團。一定要把 aggregator prompt 排進時程。
3. **低估 API 花費。** Parallelization 是最容易不知不覺讓 token 帳單翻 5-10 倍的模式。一開始就把單位經濟模型算好。
4. **該用 sectioning 卻用 voting。** Voting 很貴 — 只用在可靠度比深度重要的高風險二元決策。
5. **忘了 partial-failure 語意。** 一個子任務錯了,功能會優雅降級還是整個請求爆掉? 要在 PRD 寫清楚。

---

> **關鍵洞察**
>
> Parallelization 是「專家小組」workflow — 每個 Claude 呼叫負責一個窄工作,再由主審匯總結果。決策依賴多個獨立準則、每個都值得聚焦分析時,就是標準產品選擇。用品質和延遲的勝利換更高的 API 花費,而且永遠要包含 aggregator 步驟。考試記得兩種變體:**sectioning**(不同子任務)求深度,**voting**(同任務 N 次)求可靠度。

---

## CCA 考試關聯

- **D1(22%)主要**: Parallelization 是「Building Effective Agents」四大 workflow 模式之一,預期有情境題。
- **D5(20%)次要**: Production 部署 — 延遲、成本、部分失敗。
- 考試訊號字:「split into independent evaluations」、「run simultaneously」、「aggregate」、「fan out / fan in」。
- 兩種變體都要背(sectioning、voting)且各記一個範例。

---

## Flashcards

| 題目 | 答案 |
|------|------|
| Parallelization workflow 的產品定義? | 平行跑多個聚焦的子分析,再匯總成一個答案 |
| 品酒小組的類比是什麼? | 專家各評一個準則,主審把筆記整合成最終判定 |
| Parallelization 的兩種變體? | Sectioning(不同子任務求深度)與 voting(同任務重複求可靠)|
| PM 什麼時候該避免 parallelization? | 子任務互相依賴、或成本是首要限制時 |
| 主要的延遲優勢? | 總時間 ≈ 最慢子任務,而不是所有子任務加總 |
| 主要的成本代價? | 比單一呼叫多 N 倍 API 花費,token 帳單乘 N |
| Parallelization 最關鍵的 production guardrail? | 每任務 timeout 與 partial-failure 處理 |
| Parallelization 是 workflow 還是 agent? | Workflow — 程式碼掌握 fan-out/fan-in,Claude 不決定 |
