# Useful Hooks — PM 视角

| 项目 | 内容 |
|------|------|
| 考试对应 | D3 — Claude Code Configuration & Workflows（占 20%）、D1 — Agentic Architecture（占 27%） |
| Task Statements | 1.5（Agent SDK hooks）、3.2（custom commands & hooks）、1.2（multi-agent coordinator-subagent patterns） |
| 课程来源 | claude-code-in-action / 05-hooks / Lesson 18 |

---

## TL;DR

本课介绍两个解决实际 AI 开发问题的 hook：(1) **type-checking hook**，在 AI 修改代码后抓出连锁错误；(2) **duplication prevention hook**，用第二个 AI instance 审查改动是否重复。对 PM 来说，关键洞察是：AI 工具有可预测的盲点，而 **hook 提供了 prompt 指示无法达成的确定性保障**。

---

## 为什么 PM 需要知道这些

这两个 hook 解决了 AI 辅助开发中的两大常见失败模式：

| 失败模式 | 商业影响 | Hook 解决方案 |
|---------|---------|-------------|
| AI 改了函数但坏了其他文件 | Bug 上了 production，开发者信任度下降 | Type-checking hook 自动抓错 |
| AI 建了重复代码而非重用既有的 | 技术债累积，维护成本上升 | Duplication review hook 标记冗余代码 |

**PM 重点**：撰写 acceptance criteria 时，你需要明确指出哪些质量关卡是自动化的（hook）vs 哪些是 best-effort 的（prompt）。

---

## 心智模型：工厂质量管控

### Hook 1：生产线上的即时检查员

想象工厂组装线上，机器人修改了一个零件。生产线上的即时检查员立刻确认这个修改有没有导致下游组装问题：

| 工厂 | AI 开发 |
|------|--------|
| 机器人修改零件 | Claude 修改 function signature |
| 检查员确认下游零件是否还能组装 | PostToolUse hook 跑 type checker |
| 零件不合？→ 送回返工 | 有 type errors？→ Claude 修正 |
| 不需要人工介入 | 不需要开发者介入 |

**重点**：检查员在**每次修改后自动执行**——不是等有人想到才去检查。

### Hook 2：独立审计员


![型別檢查回饋迴路](../../visuals/type-check-feedback-loop-zh-TW.svg)
*圖：TypeScript 型別檢查回饋迴路 — PostToolUse 執行 tsc，錯誤回饋給 Claude 自動修正。*

再想象工厂有很多零件仓库。当工人制作新零件时，独立审计员会检查仓库里是否已经有类似的零件：

| 工厂 | AI 开发 |
|------|--------|
| 工人制作新零件 | Claude 写新的 database query |
| 审计员检查现有库存 | 第二个 Claude instance 审查既有 queries |
| 发现重复？→ 用现有零件 | 发现重复？→ 重用既有 query |
| 多花审计时间，但减少浪费 | 多花 API 费用，但 codebase 更干净 |

> 💡 **PM 决策点**
>
> Duplication hook 每次编辑都要多花时间和钱。这是经典的 **质量 vs 速度 trade-off**，PM 必须评估。讲师建议：只监控最关键的目录——不要什么都审计。

---

## AI 失焦：PM 必须知道的现象


![多 Agent 審查](../../visuals/multi-agent-review-zh-TW.svg)
*圖：多 Agent 審查模式 — PostToolUse hook 啟動第二個 Claude 實例審查變更。*

视频展示了一个关于 AI 能力限制的关键洞察：

| 任务类型 | AI 行为 | 结果 |
|---------|---------|------|
| 简单聚焦：「打印 pending 订单」 | Claude 找到并重用既有代码 | 正确 |
| 复杂多步骤：「建 Slack 集成，含订单提醒」 | Claude 写了全新的重复代码 | 错误 |

**为什么 PM 要关心**：当你写的 feature 需求涉及很多步骤，AI **更可能产生冗余代码**。这不是 bug——这是 context 运作方式的可预测限制。Hook 补偿了这个限制。

> 🎯 **考试核心哲学**
>
> **Architecture > Prompt** — 结构性保障（hook）比指示性的（prompt）更可靠。
> **Independent review > Self-review** — 独立审查者能抓到原始工作者遗漏的问题。

---

## 产品场景演练

### 场景：多团队的电商平台

你是一个电商平台的 PM。后端有 50+ 个 SQL query 文件横跨多个领域（订单、库存、客户、支付）。三个开发团队每天都使用 Claude Code。

| 问题 | 没有 Hook | 有 Hook |
|------|----------|--------|
| A 团队新增「获取 pending 订单」query | 跟 B 团队的既有 query 重复 | 第二个 Claude instance 抓到 duplicate |
| 开发者修改 API response type | 其他 12 个文件的 call site 静默坏掉 | Type checker hook 立即抓到所有 12 个错误 |
| 复杂 feature 横跨多个领域 | Claude 创建冗余的工具函数 | Scoped review hook 标记既有替代方案 |

**PRD 影响**：你的 acceptance criteria 应该指明：
- 「所有 TypeScript 编辑必须触发自动 type checking」（= PostToolUse hook）
- 「关键目录的新 query 必须经过 duplicate 审查」（= duplication review hook）
- 这些**不是可选的开发者偏好**——它们是**必要的质量关卡**

> 💡 **PM 跟工程师沟通的框架**
>
> 不要说「Claude 应该检查有没有重复」（prompt-based，不可靠），而是说：「我们需要一个 PostToolUse hook，自动审查 queries 目录的改动是否有 duplication。」这给工程师一个清晰的架构需求。

---

## PM 的 Trade-off 分析

| 因素 | Type-Checking Hook | Duplication Review Hook |
|------|-------------------|------------------------|
| 每次触发的成本 | 低（~2-5 秒） | 高（~10-30 秒 + API 费用） |
| 覆盖范围 | 所有 TypeScript 文件 | Scope 到关键目录 |
| 误报率 | 接近零（compiler 是 deterministic） | 低但可能有（AI 判断） |
| 设置复杂度 | 简单（一个命令） | 中等（需要 TypeScript SDK 集成） |
| **建议** | 所有项目都启用 | 只在高价值目录启用 |

---

## 讲师视频洞察

1. **任务复杂度会降低 AI 发现既有代码的能力** — 任务简单时，Claude 会找到既有代码。任务复杂时，Claude 失焦并写出 duplicate。这是一个**可预测的模式**，不是随机 bug。
2. **Hook 可以使用 TypeScript SDK** — 这意味着 hook 可以程序化地启动独立的 Claude Code instance。这开启了 hook 系统里的 multi-agent review pattern。
3. **「It really comes down to trade-offs」** — 讲师明确把这定位成 cost-benefit 决策，而不是普适的 best practice。PM 应该逐目录评估。

---

## Anti-Patterns（考试常考）

| ❌ 错误做法 | ✅ 正确做法 | 为什么 |
|-----------|-----------|--------|
| PRD 写「AI 应该总是检查 type」 | 要求用 PostToolUse hook 做 type checking | Prompt-based 需求有非零失败率 |
| 假设 AI 会找到既有代码 | 实现自动化 duplication review | 复杂任务中 AI 会失焦——视频已演示 |
| 用 review hook 监控所有目录 | 只 scope 到关键目录 | 低价值目录的成本大于收益 |
| 依赖 code review 抓 duplicate | 用 hook 作为第一道防线 | 人工 reviewer 也会漏；hook 是一致的 |

---

## 模拟考题

### 第一题：Developer Productivity 场景

你的工程团队反馈 Claude Code 修改共用 TypeScript 工具函数时，经常引入 type errors。这些错误在 code review 时才被发现，但那时开发者已经去做其他任务了。作为 PM，你应该在团队的开发流程里加入什么需求？

- A. 在团队的 CLAUDE.md 加上指示：「修改共用工具函数后，必须跑 type checker」
- B. 要求工程师在每次 Claude Code session 结束后手动跑 `tsc --noEmit`
- C. 实现一个 PostToolUse hook，在每次文件编辑后自动跑 type checker
- D. 排程每日 batch type-check 任务，把累积的错误用 email 通知工程师

<details><summary>答案与解析</summary>

**C** — PostToolUse hook 提供即时、自动的反馈，开发者零负担。Type errors 在同一个 Claude Code session 里就被抓到并修正，开发者还没离开就解决了。

- A 是 prompt 指示——Claude 可能会忽略，复杂任务时尤其严重
- B 增加手动开销，开发者会忘记
- D 延迟了错误检测好几个小时，增加修正成本

**PM 重点**：目标是**在错误产生的当下就抓住**，而不是在下游。Hook 做得到；prompt 和手动流程做不到。
</details>

### 第二题：电商平台场景

你的电商平台有一个 `queries/` 目录，里面有 200+ 个 SQL 函数。使用 Claude Code 的工程师反馈定期出现 duplicate queries。Duplication 在 Claude 被分配多步骤任务时最严重。什么做法最能平衡质量与成本？

- A. 配置 PostToolUse hook，启动另一个 Claude instance 审查整个项目的所有文件改动
- B. 配置 PostToolUse hook，启动另一个 Claude instance 只审查 `queries/` 目录的改动
- C. 在 system prompt 加 few-shot examples，展示如何搜索既有 queries
- D. 把所有 queries 合并到更少的文件里，增加 Claude 看到既有 query 的机会

<details><summary>答案与解析</summary>

**B** — 把 review hook scope 到只有 `queries/` 目录，在质量（抓 duplicate）和成本（不对每个文件编辑增加开销）之间取得平衡。讲师明确建议这个做法。

- A 太贵了——审查整个项目的每个文件改动会大幅拖慢开发
- C 是 prompt-based，视频已经演示了这个失败模式
- D 是糟糕的软件架构，会造成维护问题

**PM 重点**：质量关卡应该**针对高风险区域**，而不是普遍适用。这是「proportionate response」原则。
</details>

### 第三题：Multi-Agent 架构场景

产品团队正在讨论是否实现 query duplication hook。工程 lead 说它每次 query 文件编辑会多花 15-20 秒。作为 PM，你应该如何框架这个决策？

- A. 拒绝 hook，因为它拖慢开发者
- B. 对所有目录都启用 hook 以最大化代码质量
- C. 评估 trade-off：只在 duplication 有高商业影响的关键目录实现 hook
- D. 用每周代码 duplication 审计取代 hook

<details><summary>答案与解析</summary>

**C** — 这是 proportionate response。Hook 每次编辑都有成本，所以应该针对 duplication 影响最大的目录（如支付 queries、订单 queries）。低风险目录（如测试工具）可能不值得这个开销。

- A 忽视了已被证实的质量问题
- B 过度套用解决方案，造成不必要的开销
- D 延迟检测并增加修正成本

**PM 重点**：考试考的是 proportionate response。「总是」和「从不」的答案通常是错的——适合场景的解决方案才是正确的。
</details>
