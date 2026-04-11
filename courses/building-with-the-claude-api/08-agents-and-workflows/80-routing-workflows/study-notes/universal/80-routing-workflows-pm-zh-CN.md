# Routing Workflows — PM 视角

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture(22%)— 主要 |
| 任务陈述 | 1.2(agentic 模式 — routing)、5.2(production workflow 部署)|
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 80 |

---

## 一句话总结

Routing 是 "分诊台" workflow — 在做真正的工作前, 先用一个快速分类器决定哪个专用 pipeline 处理这个请求。当产品处理截然不同的请求类型、且每类都值得不同处理时, 就是正确的架构。

---

## 心智模型: 医院分诊台

走进急诊室时, 你第一个见到的是分诊护士。他们问几个问题决定你去哪里:

| 分诊结果 | Pipeline |
|---------|---------|
| 胸痛 | 心内科 |
| 骨折 | 骨科 |
| 发烧咳嗽 | 普通内科 |
| 精神相关 | 身心科 |

分诊护士不是心内科或骨科医师 — 他们是分类器。他们把病人送给能真正治疗的专科。每个专科都为自己的案件量优化, 不是为 "什么都做"。

Routing workflow 就是分诊台。一个小分类器 LLM 调用决定哪个专用 prompt(或子 pipeline)处理请求。每个专科只做一件事做得很好。

---

## 产品场景

### 适合 Routing 的场景

| 场景 | 为什么 Routing |
|------|---------------|
| 客服 bot(账务 / 技术 / 退款)| 每类需要不同的工具、KB、语气 |
| 内容生成(教育 / 娱乐 / 评论)— 课程示例 | 每类需要不同的风格 |
| 多领域助手(编程 / 写作 / 数学)| 每领域需要不同 context 和 prompt |
| 意图型 routing(问题 / 任务 / 闲聊)| 不同响应类型、不同延迟预算 |
| 多层级模型选择 | 简单请求送 Haiku、复杂请求送 Opus |
| 本地化 pipeline(英 / 中 / 日)| 不同 prompt、本地特定工具 |

### 不适合 Routing 的场景

| 场景 | 更好的选择 |
|------|-----------|
| 单一请求类型且范围窄 | 一个 prompt 就好 |
| 分类器无法区分的重叠类别 | Chaining 或 agent |
| 对延迟超敏感(每 ms 都要省)| 跳过分类调用, 用一个好 prompt |
| 类别不断变动 | Routing 很脆 — 考虑 agent |

---

## 两步结构

```
用户输入 ──→ [分诊 LLM 调用] ──→ 类别 ──→ [专科 pipeline] ──→ 输出
```

1. **分诊调用** — 快速、便宜、结构化输出(一个类别标签)
2. **专科调用** — 较慢、较贵、为该类优化

PM 必须在 PRD 明确说明两次调用。各有自己的延迟预算、模型选择、prompt、eval、fallback 行为。

---

## PM 必须理解的 `tool_choice` 技巧

工程应该用 Claude tool use 配合 `tool_choice` 强制特定 tool 调用来实现分类器。PM 不用写代码, 但要懂为什么这很重要:

- **可靠性** — 强制结构化 tool call 保证分类器返回有效类别, 不是自由文字 "应该是教育类?"
- **安全** — `enum` 清单防止 Claude 发明你的 pipeline 处理不了的新类别
- **Debug** — 结构化输出容易 log 和检查

如果工程说 "我们会问 Claude 再 parse 响应", 要反推: 那很脆。要求用 `tool_choice={"type": "tool", "name": "..."}` + enum schema。

---

## PM 决策框架

| 问题 | 是 | 动作 |
|------|----|------|
| 你的产品处理截然不同的请求类型? | 是 | Routing 候选 |
| 类别可以写在一页纸上吗? | 是 | 类别够清楚 |
| 每类都能因为专用 prompt 或 tool set 受益? | 是 | Routing |
| Claude(或更便宜的分类器)能可靠分类? | 是 | Routing 可行 |
| 多一次 LLM 调用的延迟和成本可接受? | 是 | 上线 |
| 类别是否大量重叠? | 否 | Routing 才可靠 |

全是 → routing 是对的选择。一个 "否" 通常就否决了。

---

## PM 必须要求的 Production 规格

1. **Enum 约束的 tool 分类器** — 用 `tool_choice` 配合预定义 enum, 不用自由文字
2. **低置信度 fallback** — 分类器不确定时, route 到默认/通用 pipeline 或人工审核
3. **Per-category 可观测性** — log 类别分布、每类转化率、每类失败率
4. **便宜分类器模型** — 分类用小模型(例如 Haiku)降成本
5. **每分支 eval** — 每个专科 pipeline 需要自己的 eval 数据集; 通用 eval 会漏掉 per-category 质量下降
6. **滥用保护** — 恶意输入可能试图触发错误分支; 要验证类别选择合理

---

## 业务价值论述

- **质量** — "每种请求类型都有专属、优化的处理器, 而不是一个通用 prompt 应付全部"
- **可扩展** — "加一个新请求类型 = 加一个新分支, 现有类型零回归风险"
- **成本** — "简单请求送便宜模型, 复杂请求送顶级模型"
- **延迟** — "便宜分类 + 聚焦专科常常比慢通用 prompt 还快"
- **可观测性** — "我们看得到用户送哪种请求, 哪种表现差"

---

## PM 常见错误

1. **类别太多。** PM 爱建分类, 分类器讨厌分类太多。控制在 10 以下。超过就 chain 或子分类。
2. **类别重叠。** 一个请求可以归两类时, 分类器会摇摆。定义类别要让每个请求有唯一归属。
3. **没有 fallback pipeline。** 不要假设分类器一定对。为低置信度案件准备默认 "通用" pipeline。
4. **把 routing 和 agent 混淆。** Routing workflow 仍是 workflow — 代码在分类后挑 pipeline。Agent 则是让 Claude 自主挑工具。PM 在设计文档中常搞混。
5. **忘了 per-category metric。** 有 routing 的产品需要每类一个 dashboard — 否则看不出哪个分支在退化。

---

> **关键洞察**
>
> Routing 是 "分诊台" workflow — 先分类, 再分派到专科。当你的 app 处理多样化请求类型、每种都值得聚焦处理时, 就是标准产品选择。Production 关键细节是分类器实现: 用强制 tool use + enum input schema 保证有效类别标签。考试记得: **routing 是 workflow(代码分派), 不是 agent(Claude 决定)。**

---

## CCA 考试关联

- **D1(22%)主要**: Routing 是四大 workflow 模式之一, 预期有场景题。
- **D2(18%)次要**: `tool_choice="tool"` 强制工具使用会被明确测试。
- **D5(20%)次要**: Production 模式 — 便宜分类器模型、每分支 eval、fallback pipeline。
- 信号词: "categorize"、"classifier"、"dispatch"、"different types of requests"、"specialized pipeline"。
- 陷阱: routing ≠ agent。Routing 是一次分类调用后的预定分派。

---

## Flashcards

| 题目 | 答案 |
|------|------|
| Routing 的产品定义? | 分诊步骤分类请求, 再由代码分派到专用 pipeline |
| 分诊台的类比是什么? | 护士问几个问题后把病人送去心内科、骨科或普通内科 |
| 为什么分类器要用强制 tool use? | 从 enum 保证结构化类别标签, 不用 parse 自由文字 |
| PM 设计 routing 功能的关键错误? | 类别太多或重叠 — 分类器会不可靠 |
| Routing 最必要的 production guardrail? | 低置信度分类器输出的 fallback/默认 pipeline |
| Routing 是 workflow 还是 agent? | Workflow — 代码在分类后掌握分派决策 |
| PM 应该要求的成本优化? | 分类器步骤用更小/便宜的模型(分类比生成简单)|
| Routing 产品除了整体质量还需要什么 metric? | Per-category metric — 类别分布与每分支失败率 |
