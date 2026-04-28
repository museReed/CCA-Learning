# Agents 与 Workflows — PM 视角

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture(22%)— 主要 |
| 任务陈述 | 1.1(agent 与 workflow 定义)、1.2(agentic 模式)、5.2(production workflow 部署)|
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 77 |

---

## 一句话总结

作为 PM,你在 AI 功能架构上最关键的一次决定就是 **workflow vs agent** — workflow 给你可预测、能上线的功能; agent 解锁开放式能力,但代价是测试成本、成本浮动和 eval 复杂度。

---

## 心智模型: 流水线 vs 侦探

| | 流水线(Workflow)| 侦探(Agent)|
|---|--------------------------|-------------------|
| **招聘说明** | "每一件都做 A → B → C" | "破案。这是你的工具: 警徽、手机、车。" |
| **可预测性** | 每件产出都一样 | 每个案件都不同 |
| **失败形态** | 传送带坏了(修你的代码)| 判断失误(重新训练侦探)|
| **录用标准** | 你能画出流程图 | 你信任侦探的推理 |
| **成本** | 每件可预测 | 每案差异巨大 |
| **扩展方式** | 增加更多产线 | 招更好的侦探 |

大部分 production AI 产品是流水线(workflow),偶尔加几个侦探工位(agent)处理流水线搞不定的案件。Anthropic 的建议: **先从流水线开始**。

---

## 产品场景

### 适合 Workflow 的场景

| 场景 | 为什么 Workflow |
|------|---------------|
| PDF 发票 → 结构化数据 | 固定的输入输出,已知字段 |
| 客服工单 → 草稿回复 | 预先定义的步骤: 分类 → 检索 → 草稿 → 审核 |
| 零件图片 → 3D CAD 文件 | 顺序确定性 pipeline(课程示例)|
| 保留格式翻译文档 | 已知变换,每步可测 |
| SaaS metric 每日报表 | 可重复的调度,固定数据源 |

### 适合 Agent 的场景

| 场景 | 为什么 Agent |
|------|-------------|
| 能读写文件的编程助手 | 无法预测用户需要哪些文件 |
| 浏览并引用来源的研究助手 | 搜索路径取决于找到的东西 |
| DevOps 事件响应 | 下一步取决于实时系统状态 |
| 自定义数据分析 chatbot | 用户问开放式问题 |

### 两者都不用的情况(单次 Claude 调用就够)

- 任务一个 prompt 就装得下
- 不需要 tool use
- 输出短且终结

不是什么任务都需要 orchestration。把单次任务过度工程化成 workflow 是 PM 常见错误。

---

## PM 决策框架

*按顺序*问这些问题:

1. **你能画出流程图吗?** 能 → workflow。
2. **你有端到端的 eval 吗?** 没有 → workflow(没有 eval 不能上 agent)。
3. **财务能接受每次请求成本浮动吗?** 不能 → workflow(agent 会循环)。
4. **Ops 能 debug 长度变动的 trace 吗?** 不能 → workflow(trace 很快变乱)。
5. **只有走到这一步?** 你可能真的有 agent 用例。时间线按 workflow 的 2-3 倍估。

---

## "就做个 Agent" 的四个隐形成本

PM 经常低估 agent 比 workflow 难上线多少:

1. **Eval 成本** — workflow 可以用小数据集按步测试; agent 需要端到端轨迹覆盖多样化输入。
2. **成本浮动** — workflow 每次 run 的 token 账单可预测; agent 会循环、尖峰、爆预算。
3. **可观测性成本** — workflow 对应干净的 span; agent 需要 replayable trajectory,很贵才能搭起来。
4. **支持成本** — workflow 坏了工程师修代码; agent 判断失误时 PM 要决定这是 prompt 问题、tool 问题还是 model 问题。

这些成本在上线*之后*才出现,这就是为什么 Anthropic 建议从 workflow 开始。

---

## Evaluator-Optimizer 模式(PM 最爱)

课程的 CAD 示例介绍了 **evaluator-optimizer** 模式: producer 产出, grader 评估, feedback loop 重复直到 grader 接受。

从 PM 角度看,这个模式给你:

- **功能内置质检** — grader 就是你的自动化 QA
- **有界限的迭代** — 你设上限, 成本可预测
- **自我修正但不交出控制权** — 仍然是 workflow

适用于"草稿"可接受但需要"可发布版本"的功能: 自动生成营销文案、自动修图、自动写 SQL。

---

## PM 常见错误

1. **把多步 prompt chain 叫做"我们的 agent"。** 那是 workflow。用错词会让 stakeholder 和投资人期待失准。
2. **没 eval 就上 agent。** Agent 可靠度取决于你建的 eval。没 eval = 不能上。
3. **Agent 功能承诺固定费率。** 没有 guardrail 时,一个烂 query 可以花 50 倍平均成本。要么分 tier, 要么强制步骤上限。
4. **以为 "agent" 就是 "聪明"。** Agent 是*自主*, 不见得*更有能力*。设计良好的 workflow 常常胜过天真的 agent。
5. **没规划 evaluator-optimizer 模式。** 很多产品需求("草稿要可发布, 不能只是凑合")被这个模式优雅解决 — 但要明确设计才行。

---

> **关键洞察**
>
> Workflow vs agent 的决定, 是 PM 在 AI 功能上最大的架构决策。Workflow 给你可预测、可上线、可控成本 — 但你要事先知道流程。Agent 给你灵活性 — 但代价是 eval 工作量、成本浮动、debug 难度。Anthropic 自己的建议是: **先做 workflow**, 只有在任务真的无法写成流程图时才升级成 agent。大部分 "我们需要 agent" 的对话最后都会变成 "其实 workflow 就行"。

---

## CCA 考试关联

- **D1(22%)主要**: 这是考最多的领域。预期要你分类场景 — 把流程图启发式背起来。
- **D5(20%)次要**: 这个区别重要的原因是 production — 可观测性、成本、eval。
- Workflow 的考试信号词: "predefined steps"、"predetermined series"、"orchestrated"、"pipeline"。
- Agent 的考试信号词: "given a goal"、"Claude decides"、"autonomous"、"open-ended"。

---

## Flashcards

| 题目 | 答案 |
|------|------|
| PM 判断 workflow vs agent 的核心问题? | 运行前你能画出流程图吗? |
| 为什么 Anthropic 建议先从 workflow 开始? | 更便宜、更可预测、更好测、上线更快 |
| Workflow 的流水线类比? | 每一件都是已知步骤, 坏了就修代码 |
| Agent 的侦探类比? | 给目标和工具, 自己想办法下一步, 失败在判断上 |
| 列出 agent 比 workflow 多出的四个隐形成本。 | Eval 成本、成本浮动、可观测性成本、支持成本 |
| Evaluator-optimizer 模式的 PM 定义? | 自动质检 — producer 草稿, grader 审核, 循环直到接受 |
| 什么时候 workflow 和 agent 都不该用? | 任务单一 prompt 就能完成且不需 tool use 时 |
| PM 处理 agent 最大的错误? | 没有端到端 eval 就上线, 且没设步骤上限 |
