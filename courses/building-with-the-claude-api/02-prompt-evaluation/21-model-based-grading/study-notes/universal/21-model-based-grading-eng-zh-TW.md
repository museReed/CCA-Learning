# 模型評分 Model-Based Grading — 工程深入

| 項目 | 說明 |
|------|------|
| 考試領域 | D3 — Evaluation（20%）主要；D5 — Enterprise Deployment（20%）次要 |
| 任務聲明 | 3.4（LLM-as-judge 評分）、3.3（測試案例執行）、5.4（eval 驅動迭代） |
| 來源 | building-with-the-claude-api / 02-prompt-evaluation / Lesson 21 |

---

## 一句話重點

Model-based grading 把第二次 Claude 呼叫當成「評審」，回傳結構化的品質分數（1-10）加上 reasoning —— 讓主觀的輸出品質變成可追蹤、可迭代的客觀指標。

---

## 評分問題

建立 prompt evaluation workflow 時，你需要一個**客觀訊號**來衡量輸出品質。來源把 grader 定義為一個 function：吃 model output、吐出可量測的回饋 —— 通常是 1-10 的數字，10 代表高品質、1 代表低品質。

grader 有三大類：

| Grader 類型 | 做什麼 | 適合情境 |
|-------------|--------|----------|
| **Code grader** | 以程式碼做檢查（長度、關鍵字、syntax、可讀性） | 客觀、規則化的屬性 |
| **Model grader** | 呼叫另一個 AI model 評估品質 | 主觀品質、instruction following、helpfulness |
| **Human grader** | 由真人手動審查評分 | 最細膩的判斷 —— 但慢且繁瑣 |

Model graders 是中間橋樑：比 code 更彈性，比真人更快更便宜。

---

## Model Grader 擅長什麼

來源列出 model grader 擅長處理的主觀維度：

- Response quality（回應品質）
- Quality of instruction following（指令遵循程度）
- Completeness（完整度）
- Helpfulness（有用程度）
- Safety（安全性）

這些全都不是 regex 可以檢查的 —— 需要對「意義」做判斷。

---

## 先定評分標準

寫 grader 之前，必須先把評分標準定清楚。來源以 code-generation prompt 為例，列出三個標準：

- **Format** —— 只能回傳 Python、JSON 或 Regex，不可加任何解釋
- **Valid Syntax** —— 產出的程式碼必須能正確 parse
- **Task Following** —— 回應要精準對應使用者的任務

前兩項適合 **code grader**（便宜、deterministic）；第三項 Task Following 更適合 **model grader**，因為需要理解輸出是否真的解決了使用者問題。

---

## Model Grader Function

幾乎照抄來源：

```python
def grade_by_model(test_case, output):
    # Create evaluation prompt
    eval_prompt = """
    You are an expert code reviewer. Evaluate this AI-generated solution.

    Task: {task}
    Solution: {solution}

    Provide your evaluation as a structured JSON object with:
    - "strengths": An array of 1-3 key strengths
    - "weaknesses": An array of 1-3 key areas for improvement
    - "reasoning": A concise explanation of your assessment
    - "score": A number between 1-10
    """

    messages = []
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")

    eval_text = chat(messages, stop_sequences=["```"])
    return json.loads(eval_text)
```

三個值得注意的工程細節：

1. **assistant prefill 寫 `` ```json ``** —— 強制 Claude 立即開始吐 JSON，不會先來段開場白。
2. **`stop_sequences=["```"]`** —— 一碰到結尾 code fence 就停，得到乾淨可 parse 的字串。
3. **結構化輸出** —— 要求 `strengths`、`weaknesses`、`reasoning` 伴隨 `score`，強迫 model 替自己辯護。來源指出：沒這個上下文，model 傾向「往中間值靠，分數都落在 6 左右」。

---

## 為什麼 strengths + weaknesses + reasoning 很重要

這是整課最關鍵的洞察。如果你只問分數，model grader 會退化到平均值（分數 ≈ 6）。逼 grader 在決定分數**之前**寫出優缺點，相當於迷你版 chain-of-thought：model 要先建立論證，再挑出與論證一致的分數。你得到：

- **不再退化到 6** —— 分數分佈在完整範圍
- **可追溯的評分** —— 分數意外時，reasoning 告訴你原因
- **可執行的訊號** —— weaknesses 直接變成你的 prompt 調整 backlog

---

## 整合到 Test Runner

```python
def run_test_case(test_case):
    output = run_prompt(test_case)

    # Grade the output
    model_grade = grade_by_model(test_case, output)
    score = model_grade["score"]
    reasoning = model_grade["reasoning"]

    return {
        "output": output,
        "test_case": test_case,
        "score": score,
        "reasoning": reasoning
    }
```

每個 test case 現在同時回傳原始輸出、客觀分數、和辯護理由。reasoning 欄位至關重要 —— 讓工程師可以快速 sanity check grader 在這類任務上是否可信。

---

## 全 dataset 取平均

```python
from statistics import mean

def run_eval(dataset):
    results = []

    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    average_score = mean([result["score"] for result in results])
    print(f"Average score: {average_score}")

    return results
```

平均值就成為這個 prompt 的「品質指標」。改 prompt、重跑、比較平均值。來源直白點出 model graders「somewhat capricious（有點隨性）」—— 但隨性的方式很一致，所以 **delta（差值）** 可信，即使絕對分數會抖動。

---

## 常見錯誤

1. **只要分數** —— grader 退化到 6。一定要先要求 strengths、weaknesses、reasoning。
2. **忘了 assistant prefill** —— 沒配 `` ```json `` + `stop_sequences=["```"]`，你就得去 parse 任意散文。
3. **把絕對分數當 ground truth** —— model graders 有隨機性。要信 prompt 版本之間的 delta，不要信絕對數字。
4. **用 model grader 做 deterministic 檢查** —— 浪費又慢。syntax、長度、keyword 檢查用 code grader。
5. **沒記錄 reasoning 欄位** —— 分數意外時，你需要辯護理由才能 debug。

> **關鍵洞察**
>
> Model graders 在「先論證、再給分」時表現最好。逼 grader 先寫出 strengths、weaknesses、reasoning，分數就變成論證的結果，而不是隨便猜的數字。這一個技巧就能把「到處打 6 分」的不可靠評審變成可迭代的品質指標。

---

## CCA 考試相關性

- **D3（Evaluation）**：Model-based grading 是 LLM-as-judge 的範式。會考何時用 model vs code vs human grader，以及如何組 grader prompt。
- **D5（Enterprise Deployment）**：自動化評分是 eval 驅動 prompt 迭代、以及生產環境 prompt CI 的基礎。
- 注意情境題：「你要衡量 instruction following 品質」→ 答案是 model grader，不是 code grader。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| grader 有哪三種類型？ | Code graders、model graders、human graders。 |
| grader 的典型分數範圍？ | 1 到 10 之間的數字，10 代表高品質、1 代表低品質。 |
| 為什麼要連 strengths/weaknesses/reasoning 一起要？ | 沒有這個上下文，model grader 會退化到 6 分左右的中間值。 |
| 在 code-gen 範例中，哪個評分標準最適合 model grader？ | Task Following —— 因為需要彈性判斷輸出是否真的解決使用者任務。 |
| 哪兩個技巧可讓 grader 的 JSON 輸出乾淨？ | assistant prefill 寫 `` ```json `` 配 `stop_sequences=["```"]`。 |
| model graders 擅長評估哪些維度？ | Response quality、instruction following、completeness、helpfulness、safety。 |
| 如何把每個 test case 分數轉為 prompt 層級指標？ | 對所有 test case 分數取 mean。 |
| 為什麼 model graders 是「capricious 但有用」？ | 絕對分數會抖動，但 prompt 版本之間的 delta 仍是可追蹤的一致 baseline。 |
