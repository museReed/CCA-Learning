# 模型评分 Model-Based Grading — 工程深入

| 项目 | 说明 |
|------|------|
| 考试领域 | D3 — Evaluation（20%）主要；D5 — Enterprise Deployment（20%）次要 |
| 任务声明 | 3.4（LLM-as-judge 评分）、3.3（测试案例执行）、5.4（eval 驱动迭代） |
| 来源 | building-with-the-claude-api / 02-prompt-evaluation / Lesson 21 |

---

## 一句话重点

Model-based grading 把第二次 Claude 调用当成"评审"，返回结构化的质量分数（1-10）加上 reasoning —— 让主观的输出质量变成可追踪、可迭代的客观指标。

---

## 评分问题

建立 prompt evaluation workflow 时，你需要一个**客观信号**来衡量输出质量。来源把 grader 定义为一个函数：吃 model output、吐出可量测的反馈 —— 通常是 1-10 的数字，10 代表高质量、1 代表低质量。

grader 有三大类：

| Grader 类型 | 做什么 | 适合场景 |
|-------------|--------|----------|
| **Code grader** | 用代码做检查（长度、关键字、syntax、可读性） | 客观、规则化的属性 |
| **Model grader** | 调用另一个 AI model 评估质量 | 主观质量、instruction following、helpfulness |
| **Human grader** | 由真人手动审查评分 | 最细腻的判断 —— 但慢且繁琐 |

Model graders 是中间桥梁：比 code 更灵活，比真人更快更便宜。

---

## Model Grader 擅长什么

来源列出 model grader 擅长处理的主观维度：

- Response quality（响应质量）
- Quality of instruction following（指令遵循程度）
- Completeness（完整度）
- Helpfulness（有用程度）
- Safety（安全性）

这些全都不是 regex 可以检查的 —— 需要对"意义"做判断。

---

## 先定评分标准

写 grader 之前，必须先把评分标准定清楚。来源以 code-generation prompt 为例，列出三个标准：

- **Format** —— 只能返回 Python、JSON 或 Regex，不能加任何解释
- **Valid Syntax** —— 产出的代码必须能正确 parse
- **Task Following** —— 响应要精准对应用户的任务

前两项适合 **code grader**（便宜、deterministic）；第三项 Task Following 更适合 **model grader**，因为需要理解输出是否真的解决了用户问题。

---

## Model Grader 函数

几乎照抄来源：

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

三个值得注意的工程细节：

1. **assistant prefill 写 `` ```json ``** —— 强制 Claude 立即开始吐 JSON，不会先来段开场白。
2. **`stop_sequences=["```"]`** —— 一碰到结尾 code fence 就停，得到干净可 parse 的字符串。
3. **结构化输出** —— 要求 `strengths`、`weaknesses`、`reasoning` 伴随 `score`，强迫 model 替自己辩护。来源指出：没这个上下文，model 倾向"往中间值靠，分数都落在 6 左右"。

---

## 为什么 strengths + weaknesses + reasoning 很重要

这是整课最关键的洞察。如果你只问分数，model grader 会退化到平均值（分数 ≈ 6）。逼 grader 在决定分数**之前**写出优缺点，相当于迷你版 chain-of-thought：model 要先建立论证，再挑出与论证一致的分数。你得到：

- **不再退化到 6** —— 分数分布在完整范围
- **可追溯的评分** —— 分数意外时，reasoning 告诉你原因
- **可执行的信号** —— weaknesses 直接变成你的 prompt 调整 backlog

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

每个 test case 现在同时返回原始输出、客观分数、和辩护理由。reasoning 字段至关重要 —— 让工程师可以快速 sanity check grader 在这类任务上是否可信。

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

平均值就成为这个 prompt 的"质量指标"。改 prompt、重跑、比较平均值。来源直白点出 model graders"somewhat capricious（有点随性）"—— 但随性的方式很一致，所以 **delta（差值）** 可信，即使绝对分数会抖动。

---

## 常见错误

1. **只要分数** —— grader 退化到 6。一定要先要求 strengths、weaknesses、reasoning。
2. **忘了 assistant prefill** —— 没配 `` ```json `` + `stop_sequences=["```"]`，你就得去 parse 任意散文。
3. **把绝对分数当 ground truth** —— model graders 有随机性。要信 prompt 版本之间的 delta，不要信绝对数字。
4. **用 model grader 做 deterministic 检查** —— 浪费又慢。syntax、长度、keyword 检查用 code grader。
5. **没记录 reasoning 字段** —— 分数意外时，你需要辩护理由才能 debug。

> **关键洞察**
>
> Model graders 在"先论证、再给分"时表现最好。逼 grader 先写出 strengths、weaknesses、reasoning，分数就变成论证的结果，而不是随便猜的数字。这一个技巧就能把"到处打 6 分"的不可靠评审变成可迭代的质量指标。

---

## CCA 考试相关性

- **D3（Evaluation）**：Model-based grading 是 LLM-as-judge 的范式。会考何时用 model vs code vs human grader，以及如何组 grader prompt。
- **D5（Enterprise Deployment）**：自动化评分是 eval 驱动 prompt 迭代、以及生产环境 prompt CI 的基础。
- 注意情境题："你要衡量 instruction following 质量"→ 答案是 model grader，不是 code grader。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| grader 有哪三种类型？ | Code graders、model graders、human graders。 |
| grader 的典型分数范围？ | 1 到 10 之间的数字，10 代表高质量、1 代表低质量。 |
| 为什么要连 strengths/weaknesses/reasoning 一起要？ | 没有这个上下文，model grader 会退化到 6 分左右的中间值。 |
| 在 code-gen 范例中，哪个评分标准最适合 model grader？ | Task Following —— 因为需要灵活判断输出是否真的解决用户任务。 |
| 哪两个技巧可让 grader 的 JSON 输出干净？ | assistant prefill 写 `` ```json `` 配 `stop_sequences=["```"]`。 |
| model graders 擅长评估哪些维度？ | Response quality、instruction following、completeness、helpfulness、safety。 |
| 如何把每个 test case 分数转为 prompt 层级指标？ | 对所有 test case 分数取 mean。 |
| 为什么 model graders 是"capricious 但有用"？ | 绝对分数会抖动，但 prompt 版本之间的 delta 仍是可追踪的一致 baseline。 |
