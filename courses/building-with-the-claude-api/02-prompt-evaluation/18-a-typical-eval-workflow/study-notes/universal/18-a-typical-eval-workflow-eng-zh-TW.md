# A Typical Eval Workflow — Engineering Deep Dive（繁體中文）

| 項目 | 內容 |
|------|------|
| Exam Domain | D3 — Evaluation & Iteration（20%，主要）；D5 — Enterprise Deployment（20%，次要） |
| Task Statements | 3.1（eval 設計）、3.2（測試資料集）、3.3（eval 執行） |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 18 |

---

## 一句話摘要

Prompt evaluation 工作流是一個五步驟循環 — draft、dataset、run、grade、iterate — 把主觀的 prompt engineering 變成可量測、可重現、甚至可以放進 CI 的流程。

---

## 五步驟工作流

課程定義了「最小可行」的 eval 工作流。市面上每一個開源或付費的 eval 工具，本質上都是這五個步驟的更精緻實作。

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ 1. Draft     │ → │ 2. Dataset   │ → │ 3. Run       │ → │ 4. Grade     │ → │ 5. Iterate   │
│   a prompt   │   │              │   │   Claude     │   │   outputs    │   │   prompt     │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
        ▲                                                                             │
        └─────────────────────────────────────────────────────────────────────────────┘
                                  迭代直到分數進入平台期
```

---

## Step 1：起草 Prompt

從你本來就會寫的 prompt 開始。課程刻意用了一個極簡 baseline：

```python
prompt = f"""
Please answer the user's question:

{question}
"""
```

Baseline 的價值不在於它寫得好，而在於它「可量測」。有了 baseline，你才能證明後續迭代真的是改善。

---

## Step 2：建立 Eval Dataset

資料集是一組能代表 production 流量的範例輸入。每一筆都是要被插進 prompt template 的槽位。

課程用的三個問題：

- "What's 2+2?"
- "How do I make oatmeal?"
- "How far away is the Moon?"

實務上你可能有數十、數百甚至數千筆紀錄。兩種建法：
- 手工打造（高保真、低產能）；
- 用 Claude 自動生成（較低保真、高產能 — 見 Lesson 19）。

最重要的特性是資料集要**反映真實輸入分布**，不能只有 happy path。

---

## Step 3：餵進 Claude

對每一筆資料集輸入，把它內插進 template 然後把完整 prompt 送給 Claude。以第一題為例：

```
Please answer the user's question:
What's 2+2?
```

Claude 會回出例如「2 + 2 = 4」、煮燕麥片的步驟、月球距離等。這就是 grader 要評分的原始輸出。

Lesson 20 會把這步包進 `run_prompt(test_case)` 函式。

---

## Step 4：餵進 Grader

Grader 才是把這個循環從「意見」變成「工程流程」的關鍵元件。它檢視原始輸入和 Claude 的輸出，吐出一個數值分數 — 課程用 **1 到 10 分**，10 代表完美答案。

課程範例的分數：

| 測試案例 | Grader 分數 |
|----------|------------|
| 數學：「What's 2+2?」 | 10（完美） |
| 燕麥：「How do I make oatmeal?」 | 4（需要改進） |
| 月球：「How far away is the Moon?」 | 9（非常好） |

彙總分數：`(10 + 4 + 9) / 3 = 7.66`。

Grader 本身可以是 code-based（regex、JSON schema 檢查）或 model-based（用另一個 LLM 來評分），後面章節會介紹。

---

## Step 5：改 Prompt 並重跑

有了 7.66 的 baseline，你改 prompt 的某個東西然後重跑整條 pipeline。課程示範了一個簡單改進 — 多加一行指引：

```python
prompt = f"""
Please answer the user's question:

{question}

Answer the question with ample detail
"""
```

同一個資料集跑 v2 prompt，新的平均分變成 **8.7**。因為差異是數值，沒得吵 — v2 在這個資料集上客觀優於 v1。

一直迭代直到分數進入平台期，或者「足夠 production」為止。

---

## 為什麼這個工作流很重要

這個流程提供三個 ad-hoc 測試做不到的能力：

1. **Prompt 版本的數值比較** — 你挑分數高的那個，不是感覺順的那個。
2. **挑出最佳版本** — 你能把客觀最高分的 prompt 上線，而不是某個運氣好的。
3. **持續迭代** — 每次改動都對同一個資料集量測，形成 regression 安全網。

這個工作流「把 prompt engineering 的猜測成分移除」，讓你有信心說改動真的是改善而不是另一種變體。

---

## 規模化考量（超出課程範圍）

五個步驟是最小集。真實 production eval pipeline 會再疊上：

- **版本化資料集** — 每次資料集修訂都存 checkpoint，可以重現舊分數。
- **平行執行** — 數千筆資料集受益於並行 API 呼叫。
- **CI 整合** — 每個改動 prompt 的 PR 都跑 pipeline，擋 regression。
- **多個 grader** — 單一分數會隱藏維度上的 trade-off；production 會用多個 rubric（正確性、格式、語氣）。
- **分層抽樣** — 資料集內有加權桶，讓稀有類別不會被常見類別淹沒。

這些都不改變核心循環，只是把它在規模上 operationalize。

---

## 常見錯誤

1. **沒有 baseline 分數** — 沒 baseline 的迭代等於無法驗證改動是否真的有改善。
2. **資料集只有 happy path** — 資料集的意義是暴露失敗模式，不是證明容易的題目可以過。
3. **憑眼睛看輸出、跳過 grader** — 沒有數值 scorer，「迭代」只是意見洗牌。
4. **同時改 prompt 和 dataset** — 你不會知道分數變動是來自 prompt 還是 dataset。
5. **分數一升就停** — 第一個改善很少是最佳改善；持續迭代直到進入平台期。

---

> **Key Insight**
>
> 五步驟工作流的全部威力在於「資料集保持不變、只變 prompt」。這讓 prompt 被隔離成自變數，分數的每次變動都能歸因到 prompt。若在兩次跑之間同時動了 dataset，你就摧毀了這個實驗。CCA 考試裡，draft → dataset → run → grade → iterate 這個順序是 D3 最可測的序列。

---

## CCA 考試相關性

- **D3（Evaluation & Iteration）**：記住五步驟順序；知道 baseline 是為了啟用數值比較；理解「feed through grader」輸出 1-10 分。
- **D5（Enterprise Deployment）**：認知到這個工作流就是 production 準備度的閘門 — 沒 eval 迴圈就不能部署。
- 考題觸發詞：「用客觀數據改進 prompt 的流程是什麼」→ 答案就是這個五步驟循環。

---

## Flashcards

| Front | Back |
|-------|------|
| 典型 eval 工作流的五個步驟是什麼？ | 1) 起草 prompt、2) 建立 eval 資料集、3) 餵進 Claude、4) 餵進 grader、5) 改 prompt 並重複。 |
| 課程用的 grader 分數尺度是什麼？ | 1 到 10 分，10 為完美答案，分數越低代表越需要改進。 |
| 課程用的 baseline prompt 是什麼？ | `Please answer the user's question: {question}` 內插進 f-string。 |
| 課程如何示範迭代？ | 在 prompt 裡加一句「Answer the question with ample detail」，平均分從 7.66 升到 8.7。 |
| 為什麼資料集要在迭代之間保持不變？ | 這樣分數差異才能歸因於 prompt 改動，而不是輸入改動。 |
| Step 3 做什麼？ | 把每筆資料集輸入內插進 prompt template 並送進 Claude；完整回應成為 grading 的原料。 |
| 這個工作流解鎖哪三個好處？ | 版本的數值比較、客觀挑出最佳版本、可持續量測的迭代。 |
| 建資料集的兩種方式？ | 手工建立，或用 Claude 自動生成（Lesson 19 會介紹）。 |
