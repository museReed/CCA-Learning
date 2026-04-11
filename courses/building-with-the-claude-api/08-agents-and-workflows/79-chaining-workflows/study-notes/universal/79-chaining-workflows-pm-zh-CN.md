# Chaining Workflows — PM 视角

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture(22%)— 主要 |
| 任务陈述 | 1.2(agentic 模式 — chaining)、5.2(production workflow 部署)|
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 79 |

---

## 一句话总结

Chaining 是 "一次只做一件事" 的 workflow: 只要 Claude 在单一 prompt 里无法同时满足多个限制, 或任务有天然的顺序阶段, 就把它拆成聚焦的步骤, 输出从一步流到下一步。

---

## 心智模型: 编辑部

一篇杂志文章不是一个人一次全做完:

| 角色 | 工作 | Chaining 对应 |
|------|------|--------------|
| **记者** | 收集素材 | 步骤 1: 研究 LLM 调用 |
| **写手** | 把素材写成稿 | 步骤 2: 撰稿 LLM 调用 |
| **文字编辑** | 执行家规、去除陈词滥调 | 步骤 3: 修订 LLM 调用 |
| **事实核查** | 验证论点 | 步骤 4: 验证(可以非 LLM)|
| **发行** | 发布成品 | 步骤 5: 发布 API 调用 |

每个角色专注在自己最擅长的事, 工作从一个桌子流到下一个。Chaining workflow 就是把同样想法套在 Claude 上: 与其让一个 prompt 烂烂地演五个角色, 不如让五个聚焦调用各演好一个。

---

## 产品场景

### 适合 Chaining 的场景

| 场景 | 为什么 Chaining |
|------|---------------|
| 有品牌语气规则的营销文案生成 | 步骤 1 草稿、步骤 2 执行语气、步骤 3 缩短 |
| 语气校准的自动回复系统 | 分类意图 → 草稿回复 → 语气修正 → 发送 |
| 保留结构的文档翻译 | 提取结构 → 翻译文字 → 重组 |
| 数据到报表 pipeline | 抓数据 → 总结 → 格式化 → 加可视化 |
| 视频内容 pipeline(课程示例)| 热门话题 → 研究 → 脚本 → 视频 → 发布 |
| 法律合同审查 | 逐章节分析喂给最终建议 |

### 不适合 Chaining 的场景

| 场景 | 更好的选择 |
|------|-----------|
| 单一简单任务 | 一次 Claude 调用就好 |
| 独立子分析 | Parallelization(Lesson 78)|
| 开放式探索 | Agent(Lesson 77)|
| 延迟关键的实时功能 | 单一调用 — chaining 延迟会加总 |

---

## PM 熟悉的 "长 Prompt 问题"

这是 chaining 解决的 PM 最常见痛点。你写 PRD 说 "AI 要产出 X、Y、Z, 避免 A、B、C" — 工程建了包含所有规则的大 prompt — 输出还是不一致地违反规则。

**诊断**: 你同时要求 Claude *创作*好内容*又*执行六条限制。把工作拆开:

1. **第一次调用** — 只专注创作好内容
2. **第二次调用** — 只专注执行限制("删掉 X、替换 Y、调整语气 Z")

第二次调用会成功, 因为 Claude 不再是在创造力和合规之间取平衡 — 它只是在编辑。

这个模式适用于任何有 "输出要 X *而且* 避免 Y" 需求的功能。

---

## PM 决策框架

问这些问题:

| 问题 | 是 | 动作 |
|------|----|------|
| 任务是否有天然的顺序阶段? | 是 | Chaining 候选 |
| Claude 在单一 prompt 中忽略某些规则? | 是 | Chaining(拆生成/执行)|
| 后续步骤需要前面步骤的输出? | 是 | Chaining, 不是 parallelization |
| 可以在步骤间验证输出? | 是 | Chaining(加质量 gate)|
| 单一 prompt 已可靠运作? | 是 | 不要 chain — 保持简单 |

---

## 业务价值论述

为 chaining vs 单一大 prompt 提案时, 翻成商业语言:

- **质量** — "每步做好一件事, 而不是做几件都做得差"
- **可靠性** — "限制由专门的修订步骤执行, 不是碰运气"
- **可测试性** — "每步有清楚的 input/output, 可以独立 unit test 与 eval"
- **可观测性** — "失败出现在特定步骤, 不藏在巨型 prompt 里"
- **延迟取舍** — "总时间是各步时间加总, 预算大约是单一 prompt 的 2 倍"

---

## PM 要编进预算的隐形成本

1. **延迟会加总。** Chain 比单一 prompt 慢。如果步骤 1 是 2 秒、步骤 2 是 2 秒、步骤 3 是 2 秒, 总共 6 秒。用户感觉得到。必要时可以 streaming 中间输出。
2. **Token 成本会加总。** 每一步都付自己的 prompt token + 输出 token。早点算总成本。
3. **错误传递。** 步骤 2 输出烂会让步骤 3 更烂。要求工程在步骤间加验证。
4. **Debug 复杂度。** 多步骤失败需要 trace log — 把可观测性写进 spec。
5. **Eval 工作量放大。** 每步要自己的 eval 数据集*加上*端到端 eval。

---

## PM 常见错误

1. **该用单一 prompt 却 chain。** 过度工程化是真的。从最简单解法开始, 只有在单一 prompt 真的失败时才 chain。
2. **Chain 太长。** 3-5 步是甜蜜点。10+ 步的 chain 变脆且慢。如果你需要 10+ 步, 大概该拆成多个小 chain 加 checkpoint。
3. **漏了非 LLM hook。** Chain 可以在 LLM 调用间插入 code — PM 常忘记这点而要求 "什么都 AI", 错过确定性验证的机会。
4. **没为 eval 编预算。** 每个 chain 步骤都需要 eval。Eval 预算常常比初建预算还大。
5. **PRD 没写错误处理。** 步骤 3 失败会怎样? 重试? Fallback? 降级? 整个请求失败? 事先写清楚。

---

> **关键洞察**
>
> Chaining 是 "每个调用聚焦一个责任" 的模式。产品需要 Claude 平衡多个目标时(创作 + 执行、提取 + 重组、分类 + 响应), 把工作拆成顺序、单一目的的 LLM 调用。"长 prompt 问题" 是这模式解决的 PM 第一大痛点。考试记得: **chaining 有序列依赖, parallelization 没有。**

---

## CCA 考试关联

- **D1(22%)主要**: Chaining 是四大 workflow 模式之一, 预期有场景题要你区分 chaining、parallelization、routing。
- **D5(20%)次要**: Production 模式 — 错误处理、checkpointing、步骤间验证。
- Chaining 信号词: "sequential"、"output feeds next step"、"break into steps"、"focus on one aspect"。
- 最清楚的信号: 场景描述 "Claude 写 X, 然后我们请 Claude 修订 X" — 就是 chaining。

---

## Flashcards

| 题目 | 答案 |
|------|------|
| Chaining 的产品定义? | 把任务拆成顺序、聚焦的 LLM 调用, 每一步输出喂下一步 |
| Chaining 的编辑部类比? | 记者 → 写手 → 文字编辑 → 事实核查 → 发行; 每个角色聚焦, 工作在桌子间流动 |
| Chaining 解决的 "长 prompt 问题" 是什么? | Claude 在单一 prompt 同时创作内容与执行规则时会忽略限制 |
| Chaining 和 parallelization 的区别? | Chaining 有序列依赖; parallelization 是并行独立子任务 |
| PM 什么时候该避免 chaining? | 单一 prompt 可靠或延迟是首要约束时 |
| 列出三个 chaining 的 PM 错误。 | 不必要 chain、chain 太长、PRD 漏错误处理 |
| Chaining 功能要编哪些隐形成本? | 延迟加总、token 加总、每步 eval、错误处理、debug 复杂度 |
| Chaining 是 workflow 还是 agent? | Workflow — 代码掌握顺序, Claude 不决定下一步 |
