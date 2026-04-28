# Running the Eval — PM Perspective（简体中文）

| 项目 | 内容 |
|------|------|
| Exam Domain | D3 — Evaluation & Iteration（20%，主要）；D5 — Enterprise Deployment（20%，次要） |
| Task Statements | 3.3（eval 执行）、3.1（eval 设计）、3.2（测试数据集） |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 20 |

---

## 一句话摘要

Eval runner 是 AI 团队的"组装产线" — 最小的三阶段机器，拿一份数据集、吐出结构化质量数据，把过去靠感觉的东西变成能上 dashboard、能 diff、能据以上线的信息。

---

## 心智模型：组装产线

把 eval runner 想成一个小型工厂，有三个工作站：

| 工作站 | 工程名称 | 做什么 |
|--------|----------|--------|
| 工作台 | `run_prompt` | 把 template 和一条测试案例组成完整 prompt、送进 Claude、收原始输出 |
| 质检站 | `run_test_case` | 拿输出给 scorer 评分，把分数附上 |
| 传送带 | `run_eval` | 把每一条测试案例送进产线，最后收集一份整齐报表 |

PM 不用自己写代码，但应该知道有这三个工作站存在 — 因为这三站就是"我们测试过一些案例"与"我们有 eval pipeline"的区别。

---

## "Walking Skeleton"模式

本课最重要的 PM 概念是 walking skeleton：一条 pipeline 里每个函数都存在，但有些是 placeholder 实现。本课 grader 暂时硬编码成 `score = 10`，让 pipeline 的其余部分可以在真实 grading 逻辑实现前先做端到端验证。

为什么 PM 要关心：

- **集成风险提前消除** — grader 还没好前就可以向利益相关者 demo pipeline。
- **范围受保护** — 之后每一个阶段（真正的 grader、并行执行、dashboards）都能插进骨架，不用动骨架本身。
- **时间线诚实** — "我们有 walking skeleton"是一个真实里程碑；"我们有看起来像 eval 的东西"不是。

工程师说"我们做好 eval pipeline 了"时，请问：是 walking skeleton 还是 production-ready？这两个之间差好几个月，应该分开追踪。

---

## 结果结构是 PM 的合约

Pipeline 产出的每个 result dict 都有三个 key：

| Key | 内容 | PM 为什么关心 |
|-----|------|---------------|
| `output` | Claude 的完整文本响应 | 客户本来会看到的东西 |
| `test_case` | 原始输入 | 审查失败案例的上下文 |
| `score` | 数值质量分数 | 上线/OKR 的头条指标 |

PM 的价值在于：一旦结果结构锁定，你就能叠上 dashboards、regression 追踪、发布报表，不用再让工程师动 instrumentation。这个结构就是产品质量的合约。

---

## 产品场景

### Walking-skeleton runner 够用的情境

| 场景 | 原因 |
|------|------|
| 向高层 demo "我们有 eval 了" | Pipeline 端到端可跑，分数是 placeholder — 用来讲故事足够 |
| 新 AI 功能的早期范围讨论 | 证明团队能在 grader 还没好之前就能迭代 |
| Runner 自身的无 regression 重构 | 合约稳定；换内部实现很安全 |

### 需要真正 grader 的情境（Lesson 21–22）

| 场景 | 原因 |
|------|------|
| 任何面向客户的发布 | 硬编码 10 代表没质量信号；不能据此上线 |
| 比较两个 prompt 版本 | Placeholder grader 永远打平手 — 迭代没有用 |
| Prompt 改动的 regression CI | 你需要真实数字才能检测"改动让东西变差" |

---

## PM 决策框架

团队反馈"eval 成功跑完了"时请问：

| 问题 | 好答案 | 坏答案 |
|------|--------|--------|
| Grader 是真的还是 placeholder？ | 真的（lesson 21/22） | "现在先硬编码 10"（开发可以，上线不行） |
| 结果有存起来能跨跑比对吗？ | 有，存在磁盘或 DB | "只打印到 notebook 里" |
| 一次 eval 要跑多久？ | 符合迭代节奏 | 慢到每次改 prompt 都跑不起 |
| 我能看三键结果格式吗？ | 可以，在 dashboard 上 | "就是一串输出" |
| 同样输入重跑会得到同样输出吗？ | 大致是（可比较） | "结果会随机跑" → 需要讨论 `temperature` |

---

## 性能现实检查

课程指出即使用 Haiku，一次完整 eval 也要大约 **30 秒**。对 PM 来说这是个早期警告：

- **30 秒 × 1,000 条 = 8 小时。** 生产规模需要并行化。
- **重跑成本很重要。** 如果每个 prompt PR 都触发 8 小时 eval，工程师会停止执行。设计时要符合迭代节奏。
- **成本预算。** 每次跑都要钱，规模越大越明显。从第一天就把这算进功能的运营成本。

---

## PM 常见错误

1. **把 walking skeleton 庆祝为"eval 完成"** — 它是基础，不是可上线的功能；真正 grader 在 lesson 21–22。
2. **没把 `results` 存下来** — 每次跑完 notebook 一关就消失，没历史、没 diff、没 regression 信号。
3. **忽略执行时间** — 大规模下串行循环会变得不可用；在数据集成长前就推动并行化。
4. **忘记结果结构是合约** — 下游工具依赖 `output / test_case / score`，悄悄改这个结构会静默弄坏 dashboards。
5. **把"walking skeleton"和"生产 pipeline"混为一谈** — 两者差好几个月；当作不同里程碑追踪。

---

> **Key Insight**
>
> Walking-skeleton eval runner 是把 prompt 质量变成 dashboard-ready 指标的最便宜方法，甚至在 grader 还没做出来之前就可以。只要有三函数 pipeline 和稳定的结果结构，你就能在上面叠观测、CI、regression 追踪，不用再动工程。CCA 考题只要问"实际怎么对数据集执行 eval"就是 D3 task 3.3，答案永远是 `run_eval → run_test_case → run_prompt` 分层加上结构化结果 dict。

---

## CCA 考试相关性

- **D3（Evaluation & Iteration）**：理解三函数分解；知道 result dict 有 `output`、`test_case`、`score`；认得 walking-skeleton 模式。
- **D5（Enterprise Deployment）**：这条 pipeline 是生产 eval 的基底；稳定合约让 dashboards、CI、regression gate 成为可能。
- 考题触发词：任何问到 eval *执行机制*的题都对应本课的三函数。

---

## Flashcards

| Front | Back |
|-------|------|
| Eval runner 的三个函数各做什么？ | `run_eval` 遍历数据集、`run_test_case` 串 prompt 和 grader、`run_prompt` 合并 template 和输入并调用 Claude。 |
| 本课的 "walking skeleton" 是什么？ | 一条有 placeholder 实现（如 `score = 10`）的完整 pipeline，让集成能在每一阶段生产前就端到端验证。 |
| 每个 result dict 有哪三个 key？ | `output`（Claude 响应）、`test_case`（原始输入）、`score`（数值质量分数）。 |
| 为什么稳定的结果结构对 PM 有价值？ | 它是合约 — dashboards、regression 追踪、发布报表都能在上面叠，不用再让工程动 instrumentation。 |
| 课程说 Haiku 一次 eval 大约多久？ | 完整小数据集大约 30 秒。 |
| 为什么 PM 要关心并行化？ | 因为串行循环随数据集大小线性扩展，大规模下每次改 prompt 都跑不起。 |
| 什么时候 walking-skeleton runner 不足以上线？ | 你需要真实质量信号时 — 任何面向客户的发布，因为 placeholder 分数会让 eval 失去意义。 |
| "结果有打印但没存"会造成什么 PM 风险？ | 没历史 diff、没 regression 检测，也无法把质量变动归因到特定 prompt 版本。 |
