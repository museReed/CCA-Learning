# Prompt Engineering — 工程深度解析

| 項目 | 內容 |
|------|------|
| 考試領域 | D3 — Evaluation & Iteration (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 3.1（prompt 設計與迭代）、1.1（指令遵循） |
| 來源 | building-with-the-claude-api / 03-prompt-engineering / Lesson 25 |

---

## 一句話總結

Prompt engineering 是一個可量化、可迭代的迴圈——寫 baseline、用 evaluator 打分、一次只套用一個技巧、再重新打分——不是靠湊字眼的猜謎遊戲。

---

## 迭代改進迴圈

課程把 prompt engineering 定義成一個嚴謹的 cycle，重複跑到分數過關為止：

1. **設定目標** — 定義 prompt 要達成什麼。
2. **寫初版 prompt** — 刻意寫一個「簡陋 baseline」。
3. **評估 prompt** — 用資料集和評分準則跑過。
4. **套用一個技巧** — clarity、specificity、examples、XML tags 等。
5. **重新評估** — 確認改動真的讓分數上升。

第 4、5 步會一直重複。紀律是：**每次迭代只改一件事**，這樣才能把分數變化歸因到那個技巧，而不是一堆修改的混合結果。

這跟 ML 模型開發是同一套科學方法循環——prompt 是假設、evaluation dataset 是測試集、score 是目標函數。

---

## 貫穿範例：運動員餐單產生器

課程整堂用同一個具體任務：依照身高、體重、目標、飲食限制，生出一日餐單。用同一個任務跑所有迭代是刻意設計——這樣分數才有可比性。

---

## Evaluation Harness

`PromptEvaluator` class 負責驅動整個迴圈。建立時要指定併發上限：

```python
evaluator = PromptEvaluator(max_concurrent_tasks=5)
```

課程明確提醒：先從低數字（約 3）開始避免 rate limit，只有 API quota 允許時才拉高。Concurrency 是和 prompt 品質正交的旋鈕——只影響牆鐘時間，不影響分數。

---

## 產生測試資料集

不用手刻 test case，evaluator 可以依任務描述和輸入規格自動產生：

```python
dataset = evaluator.generate_dataset(
    task_description="Write a compact, concise 1 day meal plan for a single athlete",
    prompt_inputs_spec={
        "height": "Athlete's height in cm",
        "weight": "Athlete's weight in kg",
        "goal": "Goal of the athlete",
        "restrictions": "Dietary restrictions of the athlete"
    },
    output_file="dataset.json",
    num_cases=3
)
```

關鍵指引：**迭代階段 `num_cases` 保持在 2-3**。你要最佳化的是迭代速度，不是統計嚴謹度。最終驗證階段再拉高數量。

---

## Baseline Prompt

刻意寫爛的 baseline 本身就是重點——你需要一個夠差的起點才量得出進步：

```python
def run_prompt(prompt_inputs):
    prompt = f"""
What should this person eat?

- Height: {prompt_inputs["height"]}
- Weight: {prompt_inputs["weight"]}
- Goal: {prompt_inputs["goal"]}
- Dietary restrictions: {prompt_inputs["restrictions"]}
"""
    messages = []
    add_user_message(messages, prompt)
    return chat(messages)
```

「What should this person eat?」是問句不是指令，沒給 Claude 任何長度、格式、營養細節、時程的目標。第一輪典型分數大約 **2.3 / 10**，課程明講這完全正常。

---

## 加入評分準則跑評估

除了資料集，還可以注入領域專屬的評分 criteria，讓 judge model 按你真正在乎的標準打分：

```python
results = evaluator.run_evaluation(
    run_prompt_function=run_prompt,
    dataset_file="dataset.json",
    extra_criteria="""
The output should include:
- Daily caloric total
- Macronutrient breakdown
- Meals with exact foods, portions, and timing
"""
)
```

`extra_criteria` 就是你的 rubric。沒給的話，judge 會自己編一個通用的「這個餐單合不合理？」scale。給了以後，分數才會反映業務需求。

---

## 解讀結果

Evaluator 會產出兩樣東西：數字分數和詳細 HTML 報告。報告列出每個 case 的 model output，以及 grader 的推理過程——這裡才看得到 case 為什麼失敗，不是只看到它失敗了。這份「為什麼」就是下一次迭代的原料。

---

## 為什麼一次只改一個技巧

如果你一次同時套用 clarity + specificity + examples + XML 結構，分數從 2.3 跳到 6.8，你無法歸因。下次遇到新 prompt 時，你不會知道哪個技巧才是對的。單技巧迭代才能累積出「哪種任務要用哪招」的個人 playbook。

---

## 常見錯誤

1. **沒有 baseline** — 直接寫「好 prompt」，結果沒有分數可以比對。
2. **多技巧一次改** — 同時改一堆東西，無法歸因哪個技巧有效。
3. **太早用太多 test case** — 迭代變慢、還沒值得大規模驗證就燒掉 API 額度。
4. **忽略 judge 的推理** — 只看數字分數，浪費報告裡最有價值的訊號。
5. **沒給 `extra_criteria`** — 預設 rubric 跟你的實際需求對不上，分數變雜訊。

> **Key Insight**
>
> Prompt engineering 不是「寫一個更好的 prompt」，而是 **instrument 一個迴圈**：baseline、打分、改一件事、再打分。Evaluator 是顯微鏡，沒有它就是在猜。2.3/10 的第一次嘗試完全正常——真正要盯的是每次迭代的 delta，不是起點的絕對數字。

---

## CCA 考試相關性

- **D3 (Evaluation & Iteration)**：認得出 baseline → eval → iterate 這個標準流程。
- **D1 (Agentic Architecture)**：prompt 是你操縱 agent 行為的槓桿；同一套迭代邏輯直接套用到 agent 的 system prompt 調校。
- 題目可能這樣出：「團隊有個 prompt 得分 2.3/10，下一步該做什麼？」答案永遠不是「從頭重寫」，而是「套一個技巧再評估」。
- 要知道 `max_concurrent_tasks` 是 rate-limit 旋鈕，不是品質旋鈕。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Prompt engineering 迴圈的五個步驟？ | 1) 設目標、2) 寫初版 prompt、3) 評估、4) 套用技巧、5) 重新評估。重複 4-5。 |
| 為什麼一次只改一件事？ | 才能把分數變化歸因到那個技巧，建立可靠的技巧選擇模型。 |
| 第一次嘗試的典型分數是多少？ | 大約 2.3/10——課程說低分很正常，不用氣餒。 |
| 迭代時為什麼 dataset 只放 2-3 個 case？ | 為了迭代速度。最終驗證階段才拉高數量。 |
| `max_concurrent_tasks` 控制什麼？ | Evaluator API 呼叫的併發數。先從 3 開始避免 rate limit。 |
| `extra_criteria` 的用途？ | 告訴 grading model 要用什麼領域專屬標準打分，讓分數反映實際需求。 |
| Evaluation 會產出哪兩個東西？ | 數字分數和詳細 HTML 報告（含每個 case 的 output 和 grader 推理）。 |
| 為什麼要刻意寫爛的 baseline？ | 因為進步只能以 delta 衡量，沒有差的起點就沒有衡量基準。 |
