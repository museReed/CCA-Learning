# Making Changes — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows |
| Task Statements | 3.4 (plan mode vs direct), 3.5 (iterative refinement) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> 本节所有内容均直接来自官方课程教材。

## One-Liner / TL;DR

Claude Code 在基本聊天之外有两个强大功能——Planning Mode（行动前先研究和提案）和 Thinking Modes（针对更难的问题进行更深度的推理）——加上截图视觉输入，改变了设计到开发的交接方式。

## Core Concepts

### 截图精确沟通

开发者可以直接将截图粘贴到 Claude Code 中，用视觉方式沟通 UI 变更：

1. 截取要修改的元素的截图
2. 用 **Ctrl+V** 粘贴（macOS 上不是 Cmd+V）
3. 描述想要的变更

**PM 重点：** 这改变了设计到开发的交接方式。设计师和 PM 可以提供标注过的截图——「改这个特定元素」——而不是撰写详细的规格书。视觉沟通现在是 AI 辅助开发的一等公民输入方式。

### Planning Mode

Planning Mode 就像请你的助理在行动前先做研究和提案——类似于初级开发者在写代码前先写设计文档。

**启用方式：** 按 **Shift+Tab 两次**（若已在自动接受模式则按一次）。

在 Planning Mode 中，Claude 会：

1. **读取更多文件** — 广泛研究代码库，像开发者在修改前先熟悉新的 repo
2. **创建详细的实现计划** — 呈现逐步的提案
3. **展示预计的操作** — 在任何代码变更前完全透明
4. **等待批准** — 开发者审查并可调整方向，就像在 sprint 承诺前审查设计文档

这不只是「较慢的执行」。它是一个根本不同的工作流程，收集更多上下文、捕捉依赖关系，并降低多文件不完整变更的风险。

### Thinking Modes

Thinking Modes 给 Claude 渐进式更多的推理时间——像给顾问额外的天数进行更深入的分析，而不是快速给意见。

| 模式 | 推理深度 | 商业类比 |
|------|---------|---------|
| "Think" | 基础延伸 | 快速 30 分钟分析 |
| "Think more" | 延伸 | 半天深度研究 |
| "Think a lot" | 全面 | 一整天的策略会议 |
| "Think longer" | 延长时间 | 多天的研究项目 |
| "Ultrathink" | 最大化 | 一周的全面审计 |

每个等级让 Claude 有渐进式更多的 token 进行更深入的分析。开发者在提示中包含关键字来启用。

### Planning vs Thinking — 广度 vs 深度

这两个功能处理不同类型的复杂度：

| 维度 | Planning Mode | Thinking Mode |
|------|--------------|---------------|
| **作用** | 广泛研究代码库 | 对问题进行更深入的推理 |
| **商业类比** | 项目启动——在承诺前调查所有利益相关者和系统 | 策略深潜——对特定决策进行彻底分析 |
| **复杂度类型** | 广度——多个文件、多个组件 | 深度——复杂逻辑、模糊需求 |
| **启动方式** | Shift+Tab 两次（切换） | 提示中的关键字（"think"、"ultrathink"） |
| **成本驱动** | 更多文件读取（工具调用） | 更多推理 token |

**PM 决策框架：**
- **简单任务**（修正错字、改颜色）→ 直接执行。快速、便宜。
- **多文件任务**（跨 15 个文件重命名、新增涉及多个模块的功能）→ Planning Mode。更多 token 但能捕捉依赖关系。
- **复杂逻辑**（设计缓存算法、调试 race condition）→ Thinking Mode。更多推理 token。
- **既广又深**（从零构建新账务模块）→ Planning Mode + Thinking。最高 token 成本但对复杂工作质量最好。

两个功能都会消耗额外 token——这是 PM 应该监控的成本-质量取舍。

### Git 集成

Claude Code 也兼任 Git 助手——开发者可以请它暂存变更并创建附有描述性消息的 commit，不需离开终端。这串接了开发到提交的工作流程，特别是在反复修改之后。

## Demo Walkthrough: Screenshot Paste — 居中占位文字

| 步骤 | 发生了什么 | 画面 |
|------|-----------|------|
| 1. 启动开发服务器 | 讲师运行 `npm run dev` 并在 localhost:3000 打开应用程序 | ![frame_003](../../visual-guide/frames/frame_003.jpg) |
| 2. 发现问题 | 占位文字位于左侧面板但未居中 | ![frame_006](../../visual-guide/frames/frame_006.jpg) |
| 3. 截图 + 粘贴 | 截取占位文字的截图，用 Ctrl+V 粘贴到 Claude Code | ![frame_009](../../visual-guide/frames/frame_009.jpg) |
| 4. 结果 | Claude 搜索代码库、更新样式——占位文字已居中 | ![frame_012](../../visual-guide/frames/frame_012.jpg) |

**PM 重点：** 从「我看到一个问题」到「问题解决」整个过程不到一分钟。不需要 Jira ticket、不需要设计规格、不需要 CSS 文件名。开发者用截图给 Claude 看问题，然后用一句话描述修改。

## Demo Walkthrough: Plan Mode + Thinking — 复杂功能实现

| 步骤 | 发生了什么 | 画面 |
|------|-----------|------|
| 1. 发现问题 | 生成 card 组件后，讲师注意到 "String Replace Editor"——显示给用户的技术工具名称 | ![frame_018](../../visual-guide/frames/frame_018.jpg) |
| 2. 截图记录问题 | 截取技术文字的截图并粘贴到 Claude Code | ![frame_027](../../visual-guide/frames/frame_027.jpg) |
| 3. 启用 Plan Mode | 按 Shift+Tab 两次启用 Planning Mode——Claude 会在行动前先研究和规划 | ![frame_035](../../visual-guide/frames/frame_035.jpg) |
| 4. 加入 ultrathink | 加入 "ultrathink" 以获得最大推理深度；说明广度（规划）vs 深度（思考） | ![frame_049](../../visual-guide/frames/frame_049.jpg) |
| 5. 组合执行 | Plan Mode + ultrathink 同时运作——广泛的代码库探索搭配深度推理 | ![frame_054](../../visual-guide/frames/frame_054.jpg) |
| 6. 功能完成 | 技术工具名称被替换为用户友好的消息：「Creating file:」和「Editing file:」 | ![frame_069](../../visual-guide/frames/frame_069.jpg) |
| 7. 验证 | 后续编辑确认功能正常——显示「Editing app.jsx」而非工具名称 | ![frame_075](../../visual-guide/frames/frame_075.jpg) |

**PM 重点：** 这是一个 UX 改善，涉及多个文件且需要理解应用程序如何渲染工具交互。用 Planning Mode + ultrathink，开发者大约两分钟完成。没有 AI 辅助的话，这需要：(1) 找出工具名称在哪里渲染、(2) 追踪数据流、(3) 修改显示逻辑、(4) 测试创建和编辑两条路径。轻松就是 1-2 小时的任务压缩到几分钟。

## Instructor Tips

- **Ctrl+V** 粘贴截图，不是 Cmd+V——这是 macOS 用户常遇到的问题
- Planning Mode 适合开发者事前不知道完整范围的任务
- Ultrathink 用于最困难的问题——它是最大推理能力
- 两个功能都有 token 成本——团队应该制定按比例使用的指引
- Claude Code 也处理 Git 暂存和提交——开发者少一次上下文切换

## Key Takeaways

1. 截图实现视觉沟通——PM 和设计师可以提供标注图片而非撰写书面规格
2. Planning Mode（Shift+Tab 两次）= 请 Claude 在行动前先研究和提案——降低复杂任务的风险
3. Thinking Modes（think / think more / think a lot / think longer / ultrathink）= 给 Claude 更多推理时间处理更难的问题
4. Planning 和 Thinking 可以组合——广度 + 深度用于最复杂的任务
5. 两个功能都增加 token 成本——PM 应监控使用并制定按比例使用的指引
6. Claude Code 也处理 Git 操作——暂存和提交并附描述性消息

---

# PART 2: Study Aids

> 补充学习资料，非官方课程内容。

## Familiar Analogies

- **截图粘贴** — 像设计师在 mockup 上圈选元素并写「改这个」。视觉上下文消除了关于讨论哪个元素的来回沟通。
- **Planning Mode** — 像请初级开发者在写代码前先写设计文档。他们研究代码库、找出所有需要改动的文件，并在提交任何代码前呈现计划供审查。
- **Thinking Modes** — 像给顾问额外的分析时间。快速意见需要 30 分钟；彻底的分析需要一周。每个思考等级是不同的推理时间预算。
- **Ultrathink** — 像委托全面审计而非抽样检查。最大分析资源带来结果的最大信心。
- **Planning + Thinking 组合** — 像项目启动（调查所有团队和系统）之后接深度技术设计会议（解决最难的架构问题）。复杂项目两者都需要。
- **简单任务用直接执行** — 像一则快速的 Slack 消息：「修正第 42 行的错字。」不需要开会，不需要规划文档，直接做。

## CCA Exam Connection

> [!TIP]
> 作为 PM，你需要知道：
> - **Planning Mode vs Thinking Mode** — 广度 vs 深度。这是最容易出题的区分。Planning 读取更多文件；Thinking 推理更深入。
> - **成本影响** — 两个功能都增加 token 消耗。预期会有关于何时成本合理 vs 浪费的考题。
> - **启动方式** — Shift+Tab 两次启用 Planning Mode；提示中的关键字启用 Thinking Modes。
> - **截图输入** — Ctrl+V（非 Cmd+V）粘贴图片。改变了设计到开发的交接方式。
> - **组合模式** — 知道两者可以同时使用，以及何时适合。
> - **按比例使用** — 考试会测试你是否理解将工具能力配对到任务复杂度。

## Anti-Patterns

| Anti-Pattern | 为何失败 | 正确做法 |
|-------------|---------|---------|
| 要求所有任务都用 Planning Mode | 浪费 token 并减慢简单变更的速度 | 制定指引：多文件任务用 Planning Mode，简单编辑用直接执行 |
| 忽视强大功能的 token 成本 | 整个团队默认用 ultrathink 导致预算超支 | 制定团队指引——按任务复杂度配对模式 |
| 截图就够的时候还写详细文字规格 | 比视觉沟通更慢且更模糊 | 鼓励 UI 变更使用截图沟通 |
| 为了降成本而禁止 ultrathink | 移除了真正复杂任务的有价值工具 | 保留给复杂任务；禁止滥用，不是禁止功能本身 |
| 不审查 Planning Mode 的输出 | 违背了审查-批准循环的目的 | 确保开发者在批准前一定审查计划 |
| 以为 Claude Code 只能写代码 | 错过了暂存和提交的 Git 集成 | 将 Git 工作流程纳入团队的 Claude Code 使用模式 |

## Practice Questions

**Q1.** 你的工程团队这个月 Claude Code token 用量翻倍了。调查发现开发者大部分任务都用 "ultrathink"，包括简单的任务。适当的 PM 回应是什么？

- A) 完全禁止 ultrathink
- B) 制定指引：保留 ultrathink 给复杂推理任务，简单变更用直接执行，多文件工作用 Planning Mode
- C) 接受较高的成本作为更好质量的代价
- D) 要求开发者减少使用 Claude Code 的频率

> [!NOTE]
> **答案：B。** 问题是滥用，不是功能本身。制定按任务复杂度配对模式的使用指引能同时优化质量和成本。这是按比例的回应。

**Q2.** 你的设计团队问：「我们可以把截图给开发者让 Claude 实现吗？」根据本课程，正确答案是什么？

- A) 不行，Claude Code 不支持图片输入
- B) 可以，开发者可以用 Ctrl+V 直接将截图粘贴到 Claude Code，Claude 用视觉上下文来实现或修改 UI 元素
- C) 只有先把截图转换成文字描述才行
- D) 截图只能用于错误报告，不能用于新设计

> [!NOTE]
> **答案：B。** 截图沟通是主要的输入方式。设计师提供截图，开发者用 Ctrl+V 粘贴，Claude 用多模态理解来实现变更。这改变了设计到开发的交接方式。

**Q3.** 你正在为一组混合任务估算 sprint velocity。哪个模式对应是正确的？

- A) 简单 bug fix → Planning Mode；复杂重构 → 直接执行
- B) 简单 bug fix → 直接执行；多文件重构 → Planning Mode；复杂算法 → Thinking Mode；复杂新模块 → Planning Mode + Thinking
- C) 所有任务 → Ultrathink 以获得最佳质量
- D) 所有任务 → Planning Mode 以确保安全

> [!NOTE]
> **答案：B。** 按任务复杂度配对模式。简单任务需要直接执行（快速、便宜）。多文件任务需要 Planning Mode（广度）。复杂推理需要 Thinking Mode（深度）。同时具备两者的任务需要组合使用。每个任务都用最强模式会浪费 token 而没有相应的收益。

**Q4.** Claude Code 中如何启用 Planning Mode？

- A) 在提示中输入 "plan"
- B) 按 Shift+Tab 两次（若已在自动接受模式则按一次）
- C) 使用 `--plan` 命令行标志
- D) 在项目设置中启用

> [!NOTE]
> **答案：B。** Planning Mode 通过 Shift+Tab 键盘快捷键切换。这与 Thinking Modes 不同，Thinking Modes 是通过提示中的关键字启用（think、ultrathink 等）。
