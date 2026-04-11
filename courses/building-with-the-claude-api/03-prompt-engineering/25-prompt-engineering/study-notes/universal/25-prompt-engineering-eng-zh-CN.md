# Prompt Engineering — 工程深度解析

| 项目 | 内容 |
|------|------|
| 考试领域 | D3 — Evaluation & Iteration (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 3.1（prompt 设计与迭代）、1.1（指令遵循） |
| 来源 | building-with-the-claude-api / 03-prompt-engineering / Lesson 25 |

---

## 一句话总结

Prompt engineering 是一个可度量、可迭代的循环——写 baseline、用 evaluator 打分、一次只套用一个技巧、再重新打分——不是靠凑字眼的猜谜游戏。

---

## 迭代改进循环

课程把 prompt engineering 定义成一个严谨的 cycle，重复跑到分数过关为止：

1. **设定目标** — 定义 prompt 要完成什么。
2. **写初版 prompt** — 故意写一个「简陋 baseline」。
3. **评估 prompt** — 用数据集和评分标准跑一遍。
4. **套用一个技巧** — clarity、specificity、examples、XML tags 等。
5. **重新评估** — 确认改动真的让分数上升。

第 4、5 步会一直重复。纪律是：**每次迭代只改一件事**，这样才能把分数变化归因到那个技巧，而不是一堆修改的混合结果。

这跟 ML 模型开发是同一套科学方法循环——prompt 是假设、evaluation dataset 是测试集、score 是目标函数。

---

## 贯穿示例：运动员餐单生成器

课程整堂用同一个具体任务：根据身高、体重、目标、饮食限制，生成一日餐单。用同一个任务跑所有迭代是故意设计的——这样分数才有可比性。

---

## Evaluation Harness

`PromptEvaluator` 类负责驱动整个循环。创建时要指定并发上限：

```python
evaluator = PromptEvaluator(max_concurrent_tasks=5)
```

课程明确提醒：先从低数字（约 3）开始避免 rate limit，只有 API quota 允许时才拉高。Concurrency 是与 prompt 质量正交的旋钮——只影响墙钟时间，不影响分数。

---

## 生成测试数据集

不用手写 test case，evaluator 可以根据任务描述和输入规格自动生成：

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

关键指引：**迭代阶段 `num_cases` 保持在 2-3**。你要最优化的是迭代速度，不是统计严谨度。最终验证阶段再拉高数量。

---

## Baseline Prompt

故意写烂的 baseline 本身就是重点——你需要一个够差的起点才量得出进步：

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

「What should this person eat?」是问句不是指令，没给 Claude 任何长度、格式、营养细节、时间的目标。第一轮典型分数大约 **2.3 / 10**，课程明说这完全正常。

---

## 加入评分标准跑评估

除了数据集，还可以注入领域专属的评分 criteria，让 judge model 按你真正在乎的标准打分：

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

`extra_criteria` 就是你的 rubric。不给的话，judge 会自己编一个通用的「这个餐单合不合理？」scale。给了以后，分数才会反映业务需求。

---

## 解读结果

Evaluator 会产出两样东西：数字分数和详细 HTML 报告。报告列出每个 case 的 model output，以及 grader 的推理过程——这里才看得到 case 为什么失败，不是只看到它失败了。这份「为什么」就是下一次迭代的原料。

---

## 为什么一次只改一个技巧

如果你一次同时套用 clarity + specificity + examples + XML 结构，分数从 2.3 跳到 6.8，你无法归因。下次遇到新 prompt 时，你不会知道哪个技巧才是对的。单技巧迭代才能累积出「哪种任务要用哪招」的个人 playbook。

---

## 常见错误

1. **没有 baseline** — 直接写「好 prompt」，结果没有分数可以比对。
2. **多技巧一次改** — 同时改一堆东西，无法归因哪个技巧有效。
3. **太早用太多 test case** — 迭代变慢、还没值得大规模验证就烧掉 API 额度。
4. **忽略 judge 的推理** — 只看数字分数，浪费报告里最有价值的信号。
5. **没给 `extra_criteria`** — 默认 rubric 跟你的实际需求对不上，分数变噪声。

> **Key Insight**
>
> Prompt engineering 不是「写一个更好的 prompt」，而是 **instrument 一个循环**：baseline、打分、改一件事、再打分。Evaluator 是显微镜，没有它就是在猜。2.3/10 的第一次尝试完全正常——真正要盯的是每次迭代的 delta，不是起点的绝对数字。

---

## CCA 考试相关性

- **D3 (Evaluation & Iteration)**：认得出 baseline → eval → iterate 这个标准流程。
- **D1 (Agentic Architecture)**：prompt 是你操纵 agent 行为的杠杆；同一套迭代逻辑直接套用到 agent 的 system prompt 调校。
- 题目可能这样出：「团队有个 prompt 得分 2.3/10，下一步该做什么？」答案永远不是「从头重写」，而是「套一个技巧再评估」。
- 要知道 `max_concurrent_tasks` 是 rate-limit 旋钮，不是质量旋钮。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Prompt engineering 循环的五个步骤？ | 1) 设目标、2) 写初版 prompt、3) 评估、4) 套用技巧、5) 重新评估。重复 4-5。 |
| 为什么一次只改一件事？ | 才能把分数变化归因到那个技巧，建立可靠的技巧选择模型。 |
| 第一次尝试的典型分数是多少？ | 大约 2.3/10——课程说低分很正常，不用气馁。 |
| 迭代时为什么 dataset 只放 2-3 个 case？ | 为了迭代速度。最终验证阶段才拉高数量。 |
| `max_concurrent_tasks` 控制什么？ | Evaluator API 调用的并发数。先从 3 开始避免 rate limit。 |
| `extra_criteria` 的用途？ | 告诉 grading model 要用什么领域专属标准打分，让分数反映实际需求。 |
| Evaluation 会产出哪两个东西？ | 数字分数和详细 HTML 报告（含每个 case 的 output 和 grader 推理）。 |
| 为什么要故意写烂的 baseline？ | 因为进步只能以 delta 衡量，没有差的起点就没有衡量基准。 |
