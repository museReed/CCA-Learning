# Agents 与 Tools — PM 视角

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture (22%) |
| Task Statements | 1.1 (agent 架构)、1.2 (agentic loop)、1.3 (agent 中的 tool use)、5.1 (production pattern 选型) |
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 81 |

---

## 一句话总结

Agent 让你只出一个功能就能处理许多不可预期的用户需求——你把目标和一个简单的工具箱交给 Claude,剩下的 Claude 自己搞定,不用你们团队把每一种用户流程预先写死。

---

## PM 为什么该关心

对 PM 来说,"要做 agent 还是 workflow"其实是一个产品策略问题:"用户请求是窄而可预测,还是宽而开放?"

| 情境 | Workflow 给你 | Agent 给你 |
|------|---------------|------------|
| 有限、重复使用场景 | 最高可靠度 | 不必要的复杂度 |
| 创意、开放式请求 | 脆弱、让用户受挫 | 灵活与惊喜 |
| "我们知道用户会问的 5 件事" | Workflow 胜 | 过度工程 |
| "用户问的我们都没想过" | PM backlog 补不完 | Agent 胜 |

Agent 让你出"一个完整能力",而不是 N 个 feature flag。

---

## 心智模型:瑞士军刀 vs 厨房小工具抽屉

一个专用化的 workflow 就像厨房那个放满单功能小工具的抽屉:

- 牛油果切片器——切牛油果很好,苹果不能用
- 分蛋器——只能分蛋
- 压蒜器——压蒜很好,姜就不行

Agent 则是瑞士军刀:

- 刀、剪刀、螺丝刀、开罐器——每个工具都很单纯
- 由 **用户的创意** 决定怎么组合
- 一支工具覆盖制造商从没想过的情境

用产品术语讲:如果你的 PRD 里列了一大串"功能 X、功能 Y、功能 Z"都在解相关问题,那你可能在做厨房小工具抽屉,其实该做瑞士军刀。

---

## 产品使用场景

### 什么时候选 Agent

| 情境 | 为什么 Agent 胜出 |
|------|-------------------|
| "帮我搞税务"助手 | 用户会问五花八门的问题,不可能事先列完 |
| AI 写代码助手(Claude Code) | 任何语言、任何 codebase——不可能每个情境都预先做 workflow |
| 创意内容工作室 | "帮我做个宣传片"可以有一千种意思 |
| 跨内部混乱数据的客服 copilot | 不同客户对不同系统有不同问题 |

### 什么时候选 Workflow

| 情境 | 为什么 Workflow 胜出 |
|------|---------------------|
| "这份会议记录帮我摘要" | 已知输入、已知输出 |
| "把这段产品描述翻译" | Deterministic、可测量、eval 便宜 |
| "抽取发票字段" | 合规/审计要求行为可预测 |
| 受管制流程(法律、医疗) | 每一步都需要可验证 |

---

## "可组合工具"原则(PM 版)

工程师会问你:"要做 `refactor_function` 这种 tool 还是 `edit_file` 这种?"答案几乎永远是比较通用的那个。为什么这对 roadmap 很重要:

1. **范围自动扩大** — 一个通用 tool 覆盖了原本要开一堆 ticket 才能处理的用户请求。
2. **Roadmap 抗意外** — 当用户要求你没想过的事情(一定会),agent 已经能处理。
3. **要维护的 feature 变少** — 每个窄 tool 都是一个要做 eval、要监控、要下架的 feature。
4. **出货更快** — 五个 primitive 比五十个专用 tool 早半年上线。

**PRD 红旗**:如果你的 PRD 列了 20 个窄 AI 动作,工程团队可能花 6 个月还是覆盖不到用户需求。改问:"覆盖 80% 情境的最小工具箱是什么?"

---

## PM 决策框架

规划 AI 功能时,走这串问题:

| 问题 | 如果 Yes | 方向 |
|------|----------|------|
| 你能事先列出所有用户流程吗? | Yes | Workflow |
| 用户的请求变化大、不可预测? | Yes | Agent |
| "答错"会有合规或安全风险? | Yes | Workflow(可预测) |
| 需要处理创意组合? | Yes | Agent |
| 每多一个情境就多一个 sprint? | Yes | 大概是 agent——你在跟错的 pattern 打架 |
| 每次请求的成本非常敏感? | Yes | Workflow(便宜、token 少) |

---

## PM 常见错误

1. **写死流程而不是目标** — PRD 写"先调用 tool A 再调用 tool B",即使 agent 更适合也把工程团队逼进 workflow 模式。
2. **用户一抱怨就加新 tool** — 正确做法是改进 system prompt 跟 tool 描述,不是硬塞 `handle_edge_case_47`。
3. **窄问题硬上 agent** — "摘要这篇文章"不需要 agent。你付 3 倍 cost 换不到任何灵活性。
4. **没预留 eval 复杂度** — Agent 的 eval 难度是 workflow 的 3–10 倍。不先规划,release cycle 会卡住。
5. **忽略 latency 影响** — 每次 agent loop 都多一次 round trip,话多的 agent 对用户来说就是慢。

> **Key Insight**
>
> 无法事先列出用户流程时选 agent,其他时候选 workflow。大部分 production AI 功能要么是假装成 agent 的 workflow,要么是被 workflow 式 PRD 淹死的 agent。把 pattern 对齐到问题,是 agentic 产品里最高杠杆的 PM 决策。

---

## CCA 考试关联

- **D1 (Agentic Coding & Architecture)**:题目常问"用户想做 X,你要做 workflow 还是 agent?"口诀:不可预测 = agent,可预测 = workflow。
- **D5 (Enterprise Deployment)**:要记得 agent 比较贵、比较难 eval,这是主要 production trade-off。
- 考题关键字:"varied requests""novel combinations" -> agent;"well-defined steps""known sequence" -> workflow。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| PM 什么时候该选 agent 而不是 workflow? | 用户请求多元、不可预测、无法事先列完时。 |
| 抽象 tool vs 专用 tool 的产品类比是什么? | 瑞士军刀(通用 primitive) vs 厨房小工具抽屉(每种情境一支工具)。 |
| 列出两个 workflow 胜 agent 的产品情境。 | 摘要会议记录、抽发票字段、翻译描述、受管制法律流程(任两个)。 |
| 为什么 agent 比 workflow 贵? | 每次 loop 迭代都是一次 API 调用和更多 token,开放式推理每个任务用更多 compute。 |
| PRD 出现什么红旗代表你该做 agent? | 一长串窄 AI 动作,都在解相关问题。 |
| 举三个 PM 必须规划的 agent 缺点。 | Cost 高、可靠度低、eval 难、latency 慢、行为不可预测(任三)。 |
| PM 为什么不该在 PRD 里过度指定 tool 顺序? | 会把工程团队逼进 workflow 模式,即使 agent 更适合,结果失去灵活性优势。 |
| Agent 设计最重要的 PM trade-off 是什么? | 灵活性 vs 可预测性——Agent 能处理新情境但比较难测、难 eval、难控制。 |
