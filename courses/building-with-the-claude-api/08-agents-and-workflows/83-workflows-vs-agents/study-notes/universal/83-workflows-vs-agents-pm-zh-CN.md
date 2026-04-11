# Workflows vs Agents — PM 视角

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture (22%);D5 — Enterprise Deployment (20%) |
| Task Statements | 1.1 (agent vs workflow 架构)、1.2 (agentic loop)、5.1 (production pattern 选型) |
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 83 |

---

## 一句话总结

Workflow 是你能完整写清楚的 AI 功能的可靠、便宜、可预测架构;Agent 是你没办法写清楚的功能的灵活、昂贵、较不可预测架构——PM 的工作是把 pattern 对应到问题,而不是在 roadmap review 时挑听起来比较帅的那一个。

---

## PM 为什么该关心

每个 AI 功能的 PRD 都在暗中做这个架构选择。如果你不刻意选,工程团队会帮你选——通常选他们觉得比较有趣的那个,也就是 agent。六个月后你会在开会讨论为什么每 ticket 成本是 workflow 方案的 10 倍,而那个 workflow 本来可以用三分之一的时间上线。

这是那种"对用户最好的答案几乎永远是比较不华丽的那个"的决策。

---

## 心智模型:流水线 vs 工作坊

**Workflow = 流水线**。每个站做一个工作。原料从头进,产品从尾出。质量高、产能高、成本低,每个站都可以独立度量。缺点:这条线只能做一种产品。要换产品就要重新设计线。

**Agent = 工匠工作坊**。工匠墙上挂着工具,客户给他一个目标("帮我做张桌子")。他根据这个特定需求挑工具、决定顺序。输出比较灵活——"帮我做张有多一个抽屉的桌子"走一样流程。缺点:慢、每件成本高、比较难量,因为每次都不一样。

大部分产品应该:流水线处理 80% 流量,工作坊处理需要手工的 20%。

---

## 完整比较表(PM 视角)

| 维度 | Workflow | Agent |
|------|----------|-------|
| **可靠度** | 高 — 每次相同结果 | 较低 — 偶尔会脱轨 |
| **每任务 cost** | 低、可预测 | 高、变动(1x-10x workflow 成本) |
| **Latency** | 低、可预测 | 较高、变动 |
| **Eval 复杂度** | 中等 — 逐步测试 | 高 — 必须测 emergent 行为 |
| **灵活性** | 低 — 只能做你写的 | 高 — 处理新情境 |
| **首次发布时间** | 前期较长(要设计流程) | 前期较短(设计工具箱) |
| **处理新用户请求的时间** | 一张新 ticket + 新分支 | 通常为零—— agent 直接处理 |
| **非预期失败的 support ticket** | 低 | 高、较难诊断 |
| **用户信任** | 靠可预测性稳定累积 | 高度依赖 inspection 和护栏 |

---

## 产品使用场景

### 什么时候选 Workflow

| 情境 | 为什么 |
|------|--------|
| "用 3 个 bullet 摘要这篇文章" | 纯转换,已知单一输入 |
| "抽取发票金额" | 合规要求 deterministic 行为 |
| "翻译产品描述" | 可度量、可 cache、便宜 |
| "客服 ticket 分类" | 窄、可重复、eval 友好 |
| 任何受管制或审计流程 | 可预测性不可妥协 |

### 什么时候选 Agent

| 情境 | 为什么 |
|------|--------|
| 跨未知 codebase 的编码助手 | 无法事先列出用户会问什么 |
| "帮我搞税务"对话工具 | 每个用户的问题路径都不同 |
| 创意内容生成 | 创意需要 tool 重组 |
| 开放式 debug 助手 | 无法事先预测 bug |
| 跨混乱 schema 的内部"数据分析师" | 每个问题都需要重新探索 |

---

## Cost 和 Latency——商业数学

典型 3 步骤任务:

| Metric | Workflow | Agent |
|--------|----------|-------|
| 每任务 token 数 | ~3,000(固定) | ~3,000 - 30,000(变动) |
| 每任务 latency | ~3-6 秒 | ~5-30 秒 |
| Cost 倍数 | 1x(baseline) | 1x 到 10x |
| Support ticket | 1x(baseline) | 1.5x 到 3x(debuggability 成本) |

**PM 心法**:workflow 95% 准确、agent 96% 准确时,workflow 胜。你付 5-10 倍 cost 换 1 个百分点的准确度,这点通常用更好的 eval 或 workflow 重试就能补回来。

---

## PM 决策框架

每个 AI 功能跑这个序列:

| 步骤 | 问题 | Yes 去 | No 去 |
|------|------|--------|-------|
| 1 | 我能事先完整列出用户流程吗? | Workflow | 第 2 步 |
| 2 | 任务是纯转换(A -> B)吗? | Workflow | 第 3 步 |
| 3 | 请求多元且不可预测吗? | 第 4 步 | Workflow |
| 4 | 动作取决于实时环境 state 吗? | Agent + inspection | 第 5 步 |
| 5 | 我们负担得起 5-10x cost 和 eval 复杂度吗? | Agent | 拆成更小的 workflow |

最后一个 sanity check:**如果我们做成 workflow,用户会发现差别吗?** 答案是"不会"就发 workflow。

---

## PM 常见错误

1. **因为 agent 听起来潮就选 agent** — "agentic"在 roadmap review 好卖,但大部分功能应该是 workflow。先把可靠度搞定。
2. **没预留 agent 的 cost 倍数** — 每请求 cost 可能跳 5-10 倍没人预测到。承诺前先估 agent cost。
3. **时程没算 eval 复杂度** — Agent 的 eval 案例需要 3-10 倍多。加进估时,不要当成免费。
4. **PRD 写死 tool 顺序** — 逼工程团队进 workflow 模式,即使 agent 更适合。写目标,不要写序列。
5. **漏掉混合方案** — Production 系统很少是纯 agent 或纯 workflow。Classifier + router 通常是两边的优点都拿到。

> **Key Insight**
>
> 默认答案是 workflow。用户问题真的需要、而且你接受 cost、latency、eval overhead 时才选 agent。用户不在乎你的架构,他们在乎功能稳定、负担得起、可预测。把 pattern 对齐到问题是 agentic 产品里最高杠杆的 PM 决策。

---

## CCA 考试关联

- **D1 (Agentic Coding & Architecture)**:会出"workflow vs agent"情境题。公式:可预测且窄 -> workflow;不可预测且广 -> agent;默认永远 workflow。
- **D5 (Enterprise Deployment)**:Production trade-off(cost、latency、eval、reliability)大部分功能都偏向 workflow。这会直接考。
- 考题提示字:"compliance""predictable""cheapest" -> workflow;"varied requests""creative combinations""novel situations" -> agent。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Anthropic 对 workflow vs agent 的默认建议是什么? | 默认 workflow;只有 workflow 解不了的问题才用 agent。 |
| 流水线 vs 工作坊的类比是什么? | Workflow = 流水线(单一产品、高产能、便宜、可预测)。Agent = 工作坊(工匠配工具,灵活但慢且贵)。 |
| 列出三个 workflow 在 production 胜 agent 的维度。 | 可靠度、cost、latency、debuggability、可预测性、eval 简单度(任三)。 |
| PM 什么时候该选 agent 而不是 workflow? | 用户请求多元、不可预测、需要创意 tool 组合,而且 workflow 准确度不够时。 |
| 同一个任务 agent 相较 workflow 的典型 cost 倍数是多少? | 1x 到 10x,看 agent 跑几次 loop 迭代。 |
| 什么 PRD 错误会逼工程团队选错架构? | 写死 tool 顺序而不是写用户目标——会强制 workflow 模式,即使 agent 更适合。 |
| Production 系统常用的混合 pattern 是什么? | Workflow router 把简单案例送到 workflow 分支,难案例送到 agent。 |
| 决定选 agent 前的最后 sanity check 问题是什么? | 如果做成 workflow,用户会发现差别吗?不会就发 workflow。 |
