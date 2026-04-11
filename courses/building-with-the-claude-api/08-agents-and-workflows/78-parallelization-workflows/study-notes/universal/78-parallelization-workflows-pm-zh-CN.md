# Parallelization Workflows — PM 视角

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture(22%)— 主要 |
| 任务陈述 | 1.2(agentic 模式 — parallelization)、5.2(production workflow 部署)|
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 78 |

---

## 一句话总结

当质量取决于"每个标准的深度"时, parallelization workflow 就是正确的产品选择: 不要让 Claude 在一个 prompt 里同时应付 10 个标准, 而是并行跑 10 份聚焦的子分析, 再汇总出结论 — 答案更好、延迟差不多, 代价是 API 花费变多。

---

## 心智模型: 品酒小组

想象你要为餐厅菜单挑一支酒。

| 做法 | 长什么样 | 结果 |
|------|---------|------|
| 一位通才品酒师 | "这支酒好吗?" — 全包一次答 | 普通、摇摆的判断 |
| **专家小组(parallelization)** | 一位专精酸度、一位 tannin、一位尾韵、一位性价比、一位配餐,加一位主审汇总 | 各轴深度足够 + 整合最终裁定 |

Parallelization workflow 就是专家小组。每位专家只专注于*一个*轴向; 一位主审看完所有专家笔记后做最后裁决。决策更好、比按顺序跑还快,但代价是每位专家都要付钱。

---

## 产品场景

### 适合 Parallelization 的场景

| 场景 | 为什么 Parallelization 有效 |
|------|---------------------------|
| 材料推荐(课程示例)| 每种材料都需要深入、专门的评估 |
| 简历筛选(按维度分优缺点)| 技能、经验、文化匹配独立评估 |
| 内容 moderation 投票 | 高风险决策跑 N 次安全检查取多数决 |
| 多标准 code review | 安全 reviewer + 风格 reviewer + 性能 reviewer + 可维护性 reviewer |
| 多视角客户反馈分析 | 情感、紧急性、主题、是否要行动 — 各自一个子任务 |
| 跨多维度文档比较 | 法律、财务、技术维度并行分析 |

### 不该用 Parallelization 的场景

| 场景 | 更好的选择 |
|------|-----------|
| 有序列依赖的任务 | 用 **chaining**(Lesson 79)|
| 单纯单一答案的问题 | 一个 Claude 调用就够 |
| 成本是首要约束 | 单一 prompt + 精心设计的标准 |
| 子任务无法真正独立 | Chaining 或 agent |

---

## 两种变体

| 变体 | 产品用途 | 示例 |
|------|---------|------|
| **Sectioning** | 把一个决策拆成多个维度 | 材料推荐(每种材料一个 LLM)|
| **Voting** | 同一评估跑 N 次求可靠性 | Moderation: "这安全吗?" × 5 投票者, 多数决 |

Sectioning 靠聚焦注意力提升*质量*。Voting 靠平均化噪音提升*可靠性*。有些功能两者都需要(例如 "3 个风险类别各跑 5 次安全投票")。

---

## PM 决策框架

问自己:

| 问题 | 是 | 动作 |
|------|----|------|
| 决策是否依赖多个独立标准? | 是 | Sectioning 候选 |
| 子任务是否需要彼此的输出? | 是 | 不是 parallelization — 用 chaining |
| 质量 > 成本? | 是 | Parallelization 合适 |
| 延迟是关键 metric? | 是 | 并行 N 调用 ≈ 最慢一次(好消息!)|
| 需要高可靠性的二元决策? | 是 | Voting 变体 |

---

## 业务价值翻译

把这个架构向工程或财务提案时, 翻成商业语言:

- **质量** — "每个标准得到专家级分析, 而不是整体的通才分析"
- **延迟** — "用户等的是最慢子任务, 不是所有子任务加总 — 感知速度差不多"
- **成本** — "API 账单乘以 N, 但每个子任务通常比单一巨型 prompt 更小更快, 实际成本不一定爆"
- **可扩展** — "加一个标准 = 加一个 prompt 文件, 现有标准零回归风险"
- **A/B 测试** — "改一个子任务 prompt 不用重测其他"

---

## PM 必须要求的 Production Guardrails

准备上线 parallelization workflow 时, 要请工程加上:

1. **Per-task timeout** — 单一慢调用不该拖住整个请求
2. **部分结果处理** — 6 个子任务成功 5 个失败 1 个时, 能否产生可用汇总?
3. **Fan-out 上限** — 不让 N 依用户输入无限增长
4. **成本警报** — parallelization 会乘 token 花费, 异常要看得到
5. **Aggregator fallback** — aggregator LLM 失败时有没有规则型 fallback?

---

## PM 常见错误

1. **把 parallelization 和 agent 混淆。** Parallelization 跑的是多个*预先决定*的子任务, 代码仍然掌握 flow。它仍是 workflow。
2. **少了 aggregator 步骤。** 把 "这里有 6 份分析" 丢给用户是失败 — 用户要一个答案, 不要陪审团。一定要把 aggregator prompt 排进时间线。
3. **低估 API 花费。** Parallelization 是最容易不知不觉让 token 账单翻 5-10 倍的模式。一开始就把单位经济模型算好。
4. **该用 sectioning 却用 voting。** Voting 很贵 — 只用在可靠性比深度重要的高风险二元决策。
5. **忘了 partial-failure 语义。** 一个子任务错了, 功能会优雅降级还是整个请求崩? 要在 PRD 写清楚。

---

> **关键洞察**
>
> Parallelization 是 "专家小组" workflow — 每个 Claude 调用负责一个窄工作, 再由主审汇总结果。决策依赖多个独立标准、每个都值得聚焦分析时, 就是标准产品选择。用质量和延迟的胜利换更高的 API 花费, 而且永远要包含 aggregator 步骤。考试记得两种变体: **sectioning**(不同子任务)求深度, **voting**(同任务 N 次)求可靠性。

---

## CCA 考试关联

- **D1(22%)主要**: Parallelization 是 "Building Effective Agents" 四大 workflow 模式之一, 预期有场景题。
- **D5(20%)次要**: Production 部署 — 延迟、成本、部分失败。
- 考试信号词: "split into independent evaluations"、"run simultaneously"、"aggregate"、"fan out / fan in"。
- 两种变体都要背(sectioning、voting)且各记一个示例。

---

## Flashcards

| 题目 | 答案 |
|------|------|
| Parallelization workflow 的产品定义? | 并行跑多个聚焦的子分析, 再汇总成一个答案 |
| 品酒小组的类比是什么? | 专家各评一个标准, 主审把笔记整合成最终裁定 |
| Parallelization 的两种变体? | Sectioning(不同子任务求深度)与 voting(同任务重复求可靠)|
| PM 什么时候该避免 parallelization? | 子任务互相依赖、或成本是首要约束时 |
| 主要的延迟优势? | 总时间 ≈ 最慢子任务, 而不是所有子任务加总 |
| 主要的成本代价? | 比单一调用多 N 倍 API 花费, token 账单乘 N |
| Parallelization 最关键的 production guardrail? | 每任务 timeout 与 partial-failure 处理 |
| Parallelization 是 workflow 还是 agent? | Workflow — 代码掌握 fan-out/fan-in, Claude 不决定 |
