# Running the Eval — PM Perspective（繁體中文）

| 項目 | 內容 |
|------|------|
| Exam Domain | D3 — Evaluation & Iteration（20%，主要）；D5 — Enterprise Deployment（20%，次要） |
| Task Statements | 3.3（eval 執行）、3.1（eval 設計）、3.2（測試資料集） |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 20 |

---

## 一句話摘要

Eval runner 是 AI 團隊的「組裝產線」— 最小的三階段機器，拿一份資料集、吐出結構化品質數據，把過去靠感覺的東西變成能上 dashboard、能 diff、能據以上線的資訊。

---

## 心智模型：組裝產線

把 eval runner 想成一個小型工廠，有三個工作站：

| 工作站 | 工程名稱 | 做什麼 |
|--------|----------|--------|
| 工作檯 | `run_prompt` | 把 template 和一筆測試案例組成完整 prompt、送進 Claude、收原始輸出 |
| 品檢站 | `run_test_case` | 拿輸出給 scorer 評分，把分數附上 |
| 輸送帶 | `run_eval` | 把每一筆測試案例送進產線，最後收集一份整齊報表 |

PM 不用自己寫程式碼，但應該知道有這三個工作站存在 — 因為這三站就是「我們測試過一些案例」與「我們有 eval pipeline」的區別。

---

## 「Walking Skeleton」模式

這一課最重要的 PM 概念是 walking skeleton：一條 pipeline 裡每個函式都存在，但有些是 placeholder 實作。這節課 grader 暫時寫死成 `score = 10`，讓 pipeline 的其餘部分可以在真實 grading 邏輯實作前先做端對端驗證。

為什麼 PM 要在意：

- **整合風險提早消除** — grader 還沒好前就可以向利害關係人 demo pipeline。
- **範疇受保護** — 之後每一個階段（真正的 grader、平行執行、dashboards）都能插進骨架，不用動骨架本身。
- **時程誠實** — 「我們有 walking skeleton」是一個真實里程碑；「我們有看起來像 eval 的東西」不是。

工程師說「我們做好 eval pipeline 了」時，請問：是 walking skeleton 還是 production-ready？這兩個之間差好幾個月，應該分開追蹤。

---

## 結果結構是 PM 的合約

Pipeline 產出的每個 result dict 都有三個 key：

| Key | 內容 | PM 為什麼在意 |
|-----|------|----------------|
| `output` | Claude 的完整文字回應 | 客戶本來會看到的東西 |
| `test_case` | 原始輸入 | 審查失敗案例的脈絡 |
| `score` | 數值品質分數 | 上線/OKR 的頭條指標 |

PM 的價值在於：一旦結果結構鎖定，你就能疊上 dashboards、regression 追蹤、發佈報表，不用再叫工程師動 instrumentation。這個結構就是產品品質的合約。

---

## 產品場景

### Walking-skeleton runner 夠用的情境

| 場景 | 原因 |
|------|------|
| 對高層 demo「我們有 eval 了」 | Pipeline 端對端可跑，分數是 placeholder — 用來講故事夠了 |
| 新 AI 功能的早期範疇討論 | 證明團隊能在 grader 還沒好之前就能迭代 |
| Runner 自身的無 regression 重構 | 合約穩定；換內部實作很安全 |

### 需要真正 grader 的情境（Lesson 21–22）

| 場景 | 原因 |
|------|------|
| 任何面向客戶的發佈 | 寫死 10 代表沒品質訊號；不能據此上線 |
| 比較兩個 prompt 版本 | Placeholder grader 永遠打平手 — 迭代沒有用 |
| Prompt 改動的 regression CI | 你需要真實數字才能偵測「改動讓東西變差」 |

---

## PM 決策框架

團隊回報「eval 成功跑完了」時請問：

| 問題 | 好答案 | 壞答案 |
|------|--------|--------|
| Grader 是真的還是 placeholder？ | 真的（lesson 21/22） | 「現在先寫死 10」（開發可以，上線不行） |
| 結果有存起來能跨跑比對嗎？ | 有，存在磁碟或 DB | 「只印到 notebook 裡」 |
| 一次 eval 要跑多久？ | 符合迭代節奏 | 慢到每次改 prompt 都跑不起 |
| 我能看三鍵結果格式嗎？ | 可以，在 dashboard 上 | 「就是一串輸出」 |
| 同樣輸入重跑會得到同樣輸出嗎？ | 大致是（可比較） | 「結果會隨機跑」→ 需要討論 `temperature` |

---

## 效能現實檢查

課程指出即使用 Haiku，一次完整 eval 也要大約 **30 秒**。對 PM 來說這是個早期警告：

- **30 秒 × 1,000 筆 = 8 小時。** Production 規模需要平行化。
- **重跑成本很重要。** 如果每個 prompt PR 都觸發 8 小時 eval，工程師會停止執行。設計時要符合迭代節奏。
- **成本預算。** 每次跑都要錢，規模越大越明顯。從第一天就把這算進功能的營運成本。

---

## PM 常見錯誤

1. **把 walking skeleton 慶祝成「eval 完成」** — 它是基礎，不是可上線的功能；真正 grader 在 lesson 21–22。
2. **沒把 `results` 存下來** — 每次跑完 notebook 一關就消失，沒歷史、沒 diff、沒 regression 訊號。
3. **忽略執行時間** — 大規模下序列迴圈會變得無法使用；在資料集成長前就推動平行化。
4. **忘記結果結構是合約** — 下游工具靠 `output / test_case / score`，悄悄改這個結構會靜默弄壞 dashboards。
5. **把「walking skeleton」跟「production pipeline」混為一談** — 兩者差好幾個月；當成不同里程碑追蹤。

---

> **Key Insight**
>
> Walking-skeleton eval runner 是把 prompt 品質變成 dashboard-ready 指標的最便宜方法，甚至在 grader 還沒做出來之前就可以。只要有三函式 pipeline 和穩定的結果結構，你就能在上面疊觀測、CI、regression 追蹤，不用再動工程。CCA 考題只要問「實際怎麼對資料集執行 eval」就是 D3 task 3.3，答案永遠是 `run_eval → run_test_case → run_prompt` 分層加上結構化結果 dict。

---

## CCA 考試相關性

- **D3（Evaluation & Iteration）**：理解三函式分解；知道 result dict 有 `output`、`test_case`、`score`；認得 walking-skeleton 模式。
- **D5（Enterprise Deployment）**：這條 pipeline 是 production eval 的基底；穩定合約讓 dashboards、CI、regression gate 成為可能。
- 考題觸發詞：任何問到 eval *執行機制*的題都對應本課的三函式。

---

## Flashcards

| Front | Back |
|-------|------|
| Eval runner 的三個函式各做什麼？ | `run_eval` 走資料集、`run_test_case` 串 prompt 和 grader、`run_prompt` 合併 template 和輸入並呼叫 Claude。 |
| 本課的「walking skeleton」是什麼？ | 一條有 placeholder 實作（例如 `score = 10`）的完整 pipeline，讓整合能在每一階段 production 前就端對端驗證。 |
| 每個 result dict 有哪三個 key？ | `output`（Claude 回應）、`test_case`（原始輸入）、`score`（數值品質分數）。 |
| 為什麼穩定的結果結構對 PM 有價值？ | 它是合約 — dashboards、regression 追蹤、發佈報表都能在上面疊，不用再叫工程動 instrumentation。 |
| 課程說 Haiku 一次 eval 大約多久？ | 完整小資料集大約 30 秒。 |
| 為什麼 PM 要在意平行化？ | 因為序列迴圈隨資料集大小線性擴展，大規模下每次改 prompt 都跑不起。 |
| 什麼時候 walking-skeleton runner 不足以上線？ | 你需要真實品質訊號時 — 任何面向客戶的發佈，因為 placeholder 分數會讓 eval 失去意義。 |
| 「結果有印出但沒存」會造成什麼 PM 風險？ | 沒歷史 diff、沒 regression 偵測，也無法把品質變動歸因到特定 prompt 版本。 |
