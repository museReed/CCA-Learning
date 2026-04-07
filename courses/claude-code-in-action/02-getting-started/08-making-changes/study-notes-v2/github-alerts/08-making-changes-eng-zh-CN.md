# Making Changes — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows |
| Task Statements | 3.4 (plan mode vs direct), 3.5 (iterative refinement) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> 本节所有内容均直接来自官方课程教材。

## One-Liner / TL;DR

Claude Code 提供三种操作模式应对不同复杂度：截图视觉沟通实现精确 UI 修改、Planning Mode 进行广泛的多文件探索、Thinking Modes 进行深度推理——每种都会消耗更多 token。

## Core Concepts

### 截图精确沟通

沟通 UI 变更最有效的方式是直接让 Claude 看到你看到的画面：

1. 截取你想修改的元素的截图
2. 在 Claude Code 聊天中使用 **Ctrl+V** 粘贴（macOS 上不是 Cmd+V）
3. 描述你想对截图中元素做的修改

Claude 同时处理图片和文字指令（多模态输入），精确理解要修改哪个元素以及如何修改。这消除了纯文字描述如「左侧面板的占位文字」的模糊性。

### Planning Mode

Planning Mode 将规划与执行分离，让 Claude 在行动前先探索你的代码库。

**启用方式：** 按 **Shift+Tab 两次**（若已在自动接受模式则按一次）。

在 Planning Mode 中，Claude 会：

1. **读取更多文件** — 更广泛地探索代码库以理解全貌
2. **创建详细的实现计划** — 明确展示它打算做什么
3. **展示预计的操作** — 呈现计划供你审查
4. **等待你的批准** — 在执行任何变更前给你机会审查和调整方向

这与直接执行有根本性的不同。规划阶段的额外文件读取通常能捕捉到直接执行会遗漏的依赖关系和边界情况。

### Thinking Modes

Thinking Modes 让 Claude 在回应前有渐进式更多的 token 用于内部推理。在你的提示中包含关键字：

| 模式 | 推理深度 | 最适用场景 |
|------|---------|-----------|
| "Think" | 基础延伸 | 中等复杂度 |
| "Think more" | 延伸 | 复杂逻辑 |
| "Think a lot" | 全面 | 多步骤算法 |
| "Think longer" | 延长时间 | 深度分析 |
| "Ultrathink" | 最大化 | 最困难的问题、模糊的需求 |

每个等级让 Claude 在回应前有渐进式更多的 token 进行更深入的分析。

### Planning vs Thinking — 广度 vs 深度

这两个功能解决不同的问题，且可以组合使用：

| 维度 | Planning Mode | Thinking Mode |
|------|--------------|---------------|
| **作用** | 读取更多文件，创建行动计划 | 对问题进行更深入的推理 |
| **复杂度类型** | 广度——多个文件、多个组件 | 深度——复杂逻辑、模糊需求 |
| **启动方式** | Shift+Tab 两次（切换） | 提示中的关键字（"think"、"ultrathink"） |
| **用户交互** | 审查-批准循环 | 不需要额外交互 |
| **成本驱动** | 更多文件读取（工具调用） | 更多推理 token |

**何时使用 Planning Mode：** 需要广泛理解代码库、多步骤实现、跨多个文件的变更、不熟悉的代码库。

**何时使用 Thinking Mode：** 复杂逻辑、困难的调试、算法挑战、模糊的需求。

**组合使用：** 对于同时需要广度（多文件）和深度（复杂推理）的任务，启用 Planning Mode 并在提示中加入 "ultrathink"。两者都会消耗额外 token——按比例使用。

### Git 集成

Claude Code 也是一个优秀的 Git 助手。完成修改后，你可以请 Claude 暂存和提交，并附上描述性的消息——在不离开终端的情况下串接开发到提交的工作流程。

## Demo Walkthrough: Screenshot Paste — 居中占位文字

| 步骤 | 发生了什么 | 画面 |
|------|-----------|------|
| 1. 启动开发服务器 | 讲师运行 `npm run dev` 并在 localhost:3000 打开应用程序 | ![frame_003](../../visual-guide/frames/frame_003.jpg) |
| 2. 发现问题 | 占位文字位于左侧面板但未居中 | ![frame_006](../../visual-guide/frames/frame_006.jpg) |
| 3. 截图 + 粘贴 | 截取占位文字的截图，用 Ctrl+V 粘贴到 Claude Code | ![frame_009](../../visual-guide/frames/frame_009.jpg) |
| 4. 结果 | Claude 搜索代码库、更新样式——占位文字已居中 | ![frame_012](../../visual-guide/frames/frame_012.jpg) |

**关键重点：** 一张截图加上一句指令就足以让 Claude 找到正确的文件并修复样式。不需要描述是哪个组件、哪个 CSS 文件或哪个 class 名称。

## Demo Walkthrough: Plan Mode + Thinking — 复杂功能实现

| 步骤 | 发生了什么 | 画面 |
|------|-----------|------|
| 1. 发现问题 | 生成 card 组件后，讲师注意到 "String Replace Editor"——显示给用户的技术工具名称 | ![frame_018](../../visual-guide/frames/frame_018.jpg) |
| 2. 截图记录问题 | 截取技术文字的截图并粘贴到 Claude Code | ![frame_027](../../visual-guide/frames/frame_027.jpg) |
| 3. 启用 Plan Mode | 按 Shift+Tab 两次启用 Planning Mode——Claude 会在行动前先研究和规划 | ![frame_035](../../visual-guide/frames/frame_035.jpg) |
| 4. 加入 ultrathink | 加入 "ultrathink" 以获得最大推理深度；说明广度（规划）vs 深度（思考） | ![frame_049](../../visual-guide/frames/frame_049.jpg) |
| 5. 组合执行 | Plan Mode + ultrathink 同时运作——Claude 广泛探索代码库同时进行深度推理 | ![frame_054](../../visual-guide/frames/frame_054.jpg) |
| 6. 功能完成 | 技术工具名称被替换为用户友好的消息：「Creating file:」和「Editing file:」 | ![frame_069](../../visual-guide/frames/frame_069.jpg) |
| 7. 验证 | 后续编辑确认功能正常——显示「Editing app.jsx」而非工具名称 | ![frame_075](../../visual-guide/frames/frame_075.jpg) |

**关键重点：** 这个复杂任务涉及多个文件，需要理解渲染管道。Planning Mode 找到所有相关文件；ultrathink 推理出映射逻辑。组合使用大约花了两分钟完成一个需要大量手动调查的功能。

## Instructor Tips

- 粘贴截图时专门使用 **Ctrl+V**——macOS 上的 Cmd+V 在 Claude Code 中不起作用
- Planning Mode 不只是「较慢的执行」——它是一个根本不同的工作流程，会收集更多上下文
- 当你不确定范围时，从 Planning Mode 开始；对于理解清楚的修改回到直接执行
- Ultrathink 是最高推理等级——在 Claude 处理复杂或模糊任务时使用
- Planning Mode 和 Thinking Modes 都会花费额外 token——按任务复杂度按比例使用
- Claude Code 也兼任 Git 助手——完成修改后用它来暂存和提交

## Key Takeaways

1. 截图消除模糊性——用 Ctrl+V 让 Claude 看到你看到的画面
2. Planning Mode（Shift+Tab 两次）= 广度——Claude 读取更多文件并在行动前创建计划
3. Thinking Modes（think / think more / think a lot / think longer / ultrathink）= 深度——更多推理 token 用于更困难的问题
4. Planning 和 Thinking 可以组合用于同时需要广度和深度的任务
5. 两个功能都会消耗额外 token——按任务复杂度按比例使用
6. Claude Code 也处理 Git 操作——暂存和提交并附描述性消息

---

# PART 2: Study Aids

> 补充学习资料，非官方课程内容。

## Familiar Analogies

- **截图粘贴** — 像是指着屏幕上的特定按钮说「改这个」。视觉沟通消除了用文字描述 UI 元素的模糊性。
- **Planning Mode** — 像建筑师在画蓝图前先做现场勘查。你不会在理解完整布局前就开始施工。额外的探索能捕捉到快速修补会遗漏的依赖关系。
- **Thinking Modes** — 像给工程师更多白板时间处理困难的设计问题。更多推理时间不代表要读更多文件——而是对同一问题进行更深入的分析。
- **Ultrathink** — 像是为关键系统组件进行三小时的设计审查会议。最大推理资源用于最大复杂度。
- **Planning + Thinking 组合** — 像跨团队冲刺规划（广度：谁负责什么）之后接深度技术设计会议（深度：如何实现）。复杂功能两者都需要。
- **五个思考等级** — 像调光器而非开关。你逐渐调高推理能力：think (25%)、think more (50%)、think a lot (75%)、think longer (90%)、ultrathink (100%)。

## CCA Exam Connection

> [!TIP]
> 本单元涵盖两个高权重的任务陈述。预期考题会测试：
> - **Planning Mode vs Thinking Mode** — 广度 vs 深度的区分是最容易出题的概念。Planning = 读取更多文件；Thinking = 更多推理 token。
> - **何时使用哪种模式** — 给定情境（多文件重构 vs 算法挑战），识别正确的模式。
> - **组合模式** — 知道两者可以同时使用于同时具有广度和深度复杂度的任务。
> - **启动方式** — Shift+Tab 两次启用 Planning Mode；提示中的关键字启用 Thinking Modes。
> - **成本意识** — 两个功能都增加 token 用量；按比例使用是关键。
> - **截图输入** — Ctrl+V（非 Cmd+V）在 Claude Code 中粘贴图片。

## Anti-Patterns

| Anti-Pattern | 为何失败 | 正确做法 |
|-------------|---------|---------|
| 每个任务都用 Planning Mode | 在简单变更上浪费 token；不必要地变慢 | 简单且范围明确的变更使用直接执行 |
| 小任务也用 ultrathink | 浪费推理 token 却没有收益 | 保留 thinking modes 给真正复杂的问题 |
| 从不使用 Planning Mode | 在多文件变更中遗漏依赖关系 | 当范围不明确或跨多个文件时启用 Planning Mode |
| 只用文字描述 UI 变更 | 模糊——「左边的按钮」可能指很多东西 | 用 Ctrl+V 粘贴截图并指出特定元素 |
| 在 macOS 上用 Cmd+V 粘贴截图 | 图片不会粘贴进 Claude Code | 专门使用 Ctrl+V |
| 跳过 Planning Mode 的审查步骤 | 违背目的；可能执行有缺陷的计划 | 批准执行前一定要审查计划 |

## Practice Questions

**Q1.** 一位开发者需要重新命名一个在 Node.js monorepo 中被 15 个文件引用的数据库字段。哪种方式最适合？

- A) 直接执行——直接请 Claude 重新命名
- B) Planning Mode——让 Claude 探索代码库并在修改前创建计划
- C) Ultrathink——请 Claude 深入推理重新命名
- D) 为每个需要修改的文件开新的 Claude 会话

> [!NOTE]
> **答案：B。** 这是典型的 Planning Mode 场景：跨多个文件的变更需要先广泛探索代码库。Planning Mode 读取相关文件、识别所有引用，并呈现全面的计划。Ultrathink (C) 解决的是错误的问题——这需要广度，不是深度。

**Q2.** 一位开发者正在设计新的缓存策略，涉及修改数据访问层、API 路由和配置系统。最佳算法取决于特定的访问模式。哪种方式最好？

- A) 带有详细提示的直接执行
- B) 只用 Planning Mode
- C) 只用 Ultrathink
- D) Planning Mode + ultrathink——Planning Mode 用于广泛理解代码库，ultrathink 用于推理最佳算法

> [!NOTE]
> **答案：D。** 这个任务同时具有广度复杂度（多个组件）和深度复杂度（选择最佳算法）。组合 Planning Mode 和 ultrathink 能同时处理两个维度。

**Q3.** 如何在 Claude Code 中启用 Planning Mode？

- A) 在提示中输入 "plan"
- B) 按 Shift+Tab 两次（若已在自动接受模式则按一次）
- C) 启动 Claude 时使用 `--plan` 标志
- D) 在配置文件中启用

> [!NOTE]
> **答案：B。** Planning Mode 通过 Shift+Tab 键盘快捷键切换。从默认状态按两次（若已在自动接受模式则按一次）。它不是提示关键字——那是 Thinking Modes 的启动方式。

**Q4.** 一位初级开发者每个请求都使用 "ultrathink"，包括加 console.log 语句。Token 用量增加了 5 倍。该给什么建议？

- A) Ultrathink 是免费的，继续使用
- B) 保留 thinking modes 给真正复杂的任务；简单变更使用直接执行
- C) 所有任务都改用 Planning Mode
- D) 停止使用 Claude Code 以降低成本

> [!NOTE]
> **答案：B。** Thinking Modes 会消耗额外 token。简单任务使用标准执行即可。Ultrathink 是给真正困难的问题使用的，在这些问题中更多推理时间确实能产生更好的结果。按任务复杂度选择合适的工具。
