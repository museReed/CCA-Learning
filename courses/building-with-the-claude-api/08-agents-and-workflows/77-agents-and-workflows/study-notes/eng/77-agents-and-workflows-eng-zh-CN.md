# Agents 与 Workflows — 工程深度解析

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture（22%）— 主要 |
| 任务陈述 | 1.1（agent 与 workflow 定义）、1.2（agentic 模式）、5.2（production workflow 部署）|
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 77 |

---

## 一句话总结

**Workflow** 由*代码*通过预先定义的 LLM 调用序列来编排；**Agent** 由 *LLM 自己*编排，给定目标和工具集后由 Claude 决定下一步动作。选哪一种,取决于你能否事先完整描述任务流程。

---

## 最关键的区别（考试必考）

此区别来自 Anthropic 的 "Building Effective Agents" 博客文章（2024 年 12 月），是 CCA 考试 D1 领域最常被测的概念。

| 方面 | Workflow | Agent |
|------|----------|-------|
| **Control flow** | 代码预先定义 | LLM 动态决定 |
| **谁来编排** | 你的 Python/TS 代码 | Claude（通过 tool use loop）|
| **任务形态** | 已知、可重复 | 开放式 |
| **步骤数** | 固定序列（或固定分支）| 涌现式 — 依运行时 context 而定 |
| **可预测性** | 高 — 易于测试和追踪 | 较低 — 需要 evals 与 guardrails |
| **适合场景** | 你能画出流程图 | 你无法列举所有路径 |

**标准定义（务必牢记）：**

> Workflow 是对 Claude 的一系列调用，通过*预先决定*的步骤来解决特定问题。Agent 则是给 Claude 一个目标和一组工具，期望 Claude 自己想办法通过这些工具完成目标。

---

## 决策启发式

问自己一个问题：**"我能否在运行之前就画出解决方案的流程图?"**

- **可以 → workflow。** 把流程图写进代码里，你掌握控制权。
- **不行 → agent。** 给 Claude 工具和目标，然后运行 tool use loop。

另一个判断标准: 如果你的 app UX 把用户限制在一组已知任务(上传图片 → 得到 STEP 文件),几乎一定是 workflow。如果用户输入自由格式请求(编程助手、研究助手),几乎一定是 agent。

---

## 示例: Image to CAD Workflow

课程演示一个 web app: 用户拖放金属零件照片,系统产出 STEP 文件(3D CAD 格式):

```python
def image_to_cad_workflow(image_bytes: bytes) -> bytes:
    # Step 1: 描述对象
    description = claude_describe_image(image_bytes)

    # Step 2: 根据描述生成 CadQuery 代码
    cad_code = claude_write_cadquery(description)

    # Step 3: 执行 CadQuery 产生 rendering
    rendering = run_cadquery(cad_code)

    # Step 4: Grader 循环(evaluator-optimizer)
    for attempt in range(MAX_ATTEMPTS):
        grade = claude_grade(image_bytes, rendering)
        if grade.accepted:
            return export_step(cad_code)
        cad_code = claude_fix(cad_code, grade.feedback)
        rendering = run_cadquery(cad_code)

    raise RuntimeError("Grader 始终不接受输出")
```

代码掌握 control flow, Claude 在每次迭代中被当作*函数*调用四次。这就是 workflow 的特征。

---

## Evaluator-Optimizer 模式

上面的 CAD 示例是 Anthropic 博客中 **Evaluator-Optimizer** 模式的实例:

- **Producer** — 拿 input 产出 output(CadQuery 建模器)
- **Grader / Evaluator** — 按照标准给 output 打分
- **Feedback loop** — 如果没过,把 feedback 传回 producer
- **Iteration** — 重复直到接受或达到最大次数

这个模式让你获得"自我修正"行为,却*不需要*把控制权交给 Claude。代码决定何时停止、何时重试、最多试几次 — 这些都是 production 系统的关键属性。

Anthropic 博客中其他 workflow 模式:

| 模式 | 核心概念 | 课程 Lesson |
|------|---------|------------|
| Prompt chaining | 顺序 LLM 调用,上一步 output 喂下一步 | Lesson 79 |
| Parallelization | 把任务拆成并行子任务并汇总 | Lesson 78 |
| Routing | 分类器挑选专用处理器 | Lesson 80 |
| Orchestrator-workers | 中心 LLM 委派给 worker LLM | 后续 Lesson |
| Evaluator-optimizer | Producer + grader feedback loop | Lesson 77 |

---

## 为什么这个区别在 production 很重要

Workflow vs agent 的选择直接影响:

1. **可观测性** — workflow 每一步都容易记录(每节点一个 span);agent trace 长度变化,跨 run 比较困难。
2. **成本控制** — workflow 步骤数已知;agent 可能意外循环(预算耗尽是真实的 production 失败模式)。
3. **Eval 策略** — workflow 可以按步评估;agent 需要端到端 eval,覆盖多样化轨迹。
4. **失败模式** — workflow 的失败在*你的代码*;agent 的失败在 *Claude 的决策*,需要重新设计 prompt 和 tool set。
5. **上线速度** — workflow 更快能出货;agent 通常需要反复迭代工具集和 system prompt。

---

## 常见错误

1. **该用 workflow 时用了 agent。** 如果你能画出流程图,workflow 更便宜、更可靠、更好调试。Anthropic 明确建议从 workflow 开始。
2. **把什么都叫 "agent"。** 多步 prompt chain 但运行时没有 LLM control flow 的,是 workflow 不是 agent。考试要求精确。
3. **忘记 evaluator-optimizer loop 要有最大次数上限。** 否则一个烂的 grader 可以无限跑,把预算烧光。
4. **误以为 workflow 不能用 tool。** Workflow 绝对可以调用 tool,区别在于*谁决定顺序*,而不是有没有 tool。
5. **把 workflow pattern 当成理论。** 你还是要自己写代码,pattern 是食谱不是框架。

---

> **关键洞察**
>
> Workflow 和 agent 的区别在于**谁掌握 control flow**。Workflow 由你的代码掌握,agent 由 Claude 掌握。其他一切 — 可观测性、成本、eval 策略、失败模式 — 都由这一个问题衍生而来。CCA 考试常常用间接方式问这个概念("预先决定的步骤" = workflow, "Claude 决定下一步" = agent)— 训练自己抓出信号词。

---

## CCA 考试关联

- **D1(22%)主要**: Lesson 77 是最常被考的领域的基础章节。至少会有一题要你分类某场景是 agent 还是 workflow。
- **D5(20%)次要**: production 部署考量(可观测性、成本、eval 策略)都跟这个选择绑在一起。
- 指向 **workflow** 的信号词: "predetermined series"、"fixed steps"、"orchestrated by code"、"pipeline"。
- 指向 **agent** 的信号词: "given a goal and tools"、"Claude decides"、"autonomous"、"open-ended task"。

---

## Flashcards

| 题目 | 答案 |
|------|------|
| Workflow 与 agent 的核心区别? | 谁掌握 control flow — workflow 是代码, agent 是 Claude |
| 写出 workflow 的标准定义。 | 通过预先决定的步骤序列对 Claude 发起的一系列调用,以解决特定问题 |
| 写出 agent 的标准定义。 | 给 Claude 目标和工具,让 Claude 自己想办法完成目标 |
| 判断 workflow vs agent 的启发式? | 运行前能否画出流程图? 能 → workflow, 不能 → agent |
| Evaluator-optimizer 模式是什么? | Producer 产出结果, grader 评分, 不过就反馈重做直到接受 |
| 列出 Anthropic "Building Effective Agents" 中 4 个 workflow 模式。 | Prompt chaining、parallelization、routing、evaluator-optimizer(还有 orchestrator-workers) |
| 为什么 Anthropic 建议先用 workflow? | 比 agent 更便宜、更可观测、更好测、上线更快 |
| Agent 独有的 production 风险? | 步骤数无上限 / 预算耗尽 — 没有 guardrail 时会无限循环 |
