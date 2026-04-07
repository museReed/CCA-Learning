# Making Changes — 工程深度笔记

| 项目 | 细节 |
|------|--------|
| 考试领域 | D1 — Agentic Coding Fundamentals (22%), D3 — Effective Claude Code Usage (30%) |
| Task Statements | 3.4 ★★★ (plan mode vs direct), 3.5 ★★★ (iterative refinement), 1.1 ★ (agentic loops) |
| 考试场景 | S2 (Code Gen), S4 (Developer Productivity) |
| 来源 | claude-code-in-action / 02-getting-started / Lesson 08（视频 + 文字） |

---

## 一句话总结

Claude Code 提供三种操作模式应对不同复杂度：直接执行用于简单变更，Planning Mode 用于复杂的多文件重构，Thinking Modes 用于模糊问题的深度推理。

---

## 截图沟通

告诉 Claude 要改什么最精确的方式是展示给它看：

1. **截取屏幕截图** — 你想修改的 UI 元素
2. **用 Ctrl+V 粘贴**（macOS 上不是 Cmd+V）到 Claude Code 聊天中
3. **描述你想要的变更** — 相对于截图

> 🎬 **讲师视频洞察**
>
> 讲师演示粘贴 uigen 应用的截图并请 Claude 修改 UI。他特别强调用 Ctrl+V — 「是 Ctrl+V，不是 Cmd+V」— 因为这是 Claude Code 用于图片粘贴的快捷键。

这是**多模态输入** — Claude 同时处理图片和文字指令来理解变更。截图消除了关于你指的是哪个元素的歧义。

---

## Planning Mode（Task 3.4 ★★★）


![Planning Mode Execution Flow](../../visuals/planning-mode-execution-flow-zh-TW.svg)
*圖：Plan Mode 執行流程 — 探索、規劃、審查、執行。*


![Plan Mode Flow](../../visuals/plan-mode-flow-zh-TW.svg)
*圖：三種模式對應不同複雜度。*

Planning Mode 是 Claude Code 处理复杂、多文件变更的机制。它将**规划**与**执行**分离。

### 如何启用

按 `Shift+Tab` 两次（如果已经自动接受编辑则按一次）：

```
普通模式：  提问 → Claude 立即执行
Plan Mode：提问 → Claude 规划 → 你审核 → Claude 执行
```

### Planning Mode 做什么

1. **读取更多文件** — Claude 更广泛地探索你的代码库
2. **创建详细计划** — 展示它打算做什么
3. **等待批准** — 你在任何变更前审核并可以重新导向
4. **执行计划** — 只在你确认后

```
┌──────────┐    ┌─────────────────┐    ┌──────────────┐
│ 你提问   │───→│ Claude 探索     │───→│ Claude 规划  │
└──────────┘    │（读取文件、     │    │（逐步        │
                │  搜索代码）     │    │  行动清单）   │
                └─────────────────┘    └──────┬───────┘
                                              │
                                              ▼
                                       ┌──────────────┐
                                       │ 你审核       │
                                       │ 计划         │
                                       └──────┬───────┘
                                              │
                                    ┌─────────┴─────────┐
                                    ▼                   ▼
                              ┌──────────┐        ┌──────────┐
                              │ 批准     │        │ 重新导向 │
                              │ → 执行   │        │ → 重新规划│
                              └──────────┘        └──────────┘
```

> 💡 **关键洞察**
>
> Planning Mode 不只是「较慢的执行」。它是根本不同的工作流，在行动前收集更多 context。规划阶段的额外文件读取通常能捕捉到直接执行会遗漏的依赖和边界情况。

### 何时使用 Planning Mode

| 使用 Planning Mode | 使用直接执行 |
|-------------------|---------------------|
| 多文件重构 | 单文件编辑 |
| 架构变更 | 简单 bug fix |
| 跨模块的新功能实现 | 添加一个 CSS class |
| 不确定范围的任务 | 确切知道要改什么 |
| 不熟悉的代码库 | 充分理解的代码 |

---

## Thinking Modes（Extended Thinking）


![Thinking Modes Token Spectrum](../../visuals/thinking-modes-token-spectrum-zh-TW.svg)
*圖：Thinking Mode 頻譜 — 從 standard 到 ultrathink。*

Thinking modes 在响应前给 Claude 更多 token 进行内部推理。这与 Planning Mode 是正交的 — 它们解决不同的问题。

### 频谱

| 模式 | 推理深度 | 最适合 |
|------|----------------|----------|
| （默认） | 标准 | 多数任务 |
| "Think" | 基本扩展 | 中等复杂度 |
| "Think more" | 扩展 | 复杂逻辑 |
| "Think a lot" | 全面 | 多步算法 |
| "Think longer" | 延长时间 | 深度分析 |
| "Ultrathink" | 最大化 | 最困难的问题、模糊需求 |

每个级别逐步给 Claude 更多 token 进行内部推理。

> 🎬 **讲师视频洞察**
>
> 讲师解释 thinking modes 给 Claude「更多 token 来推理问题」。他将 ultrathink 定位为最大推理能力，在 Claude 挣扎于特别复杂或模糊的任务时很有用。他也提到成本权衡：「两个功能都消耗额外的 token。」

---

## Planning Mode vs Thinking Mode（关键考试区别）

这是考试最重要的区别之一：

| 维度 | Planning Mode | Thinking Mode |
|-----------|--------------|---------------|
| **做什么** | 读取更多文件，创建行动计划 | 更深度地推理问题 |
| **复杂度类型** | 广度 — 多文件、多组件 | 深度 — 复杂逻辑、模糊需求 |
| **输出** | 你在执行前审核的计划 | 更彻底推理的响应 |
| **激活** | Shift+Tab（切换） | 在 prompt 中加关键字（"think"、"ultrathink"） |
| **用户交互** | 审核-批准循环 | 不需要额外交互 |
| **成本驱动** | 更多文件读取（tool call） | 更多推理 token |

```
复杂度矩阵：
                        低推理            高推理
                        复杂度            复杂度
                    ┌─────────────────┬─────────────────┐
低代码库             │   直接           │   Think /       │
复杂度              │   执行           │   Ultrathink    │
                    ├─────────────────┼─────────────────┤
高代码库             │   Planning       │   Planning +    │
复杂度              │   Mode           │   Thinking Mode │
                    └─────────────────┴─────────────────┘
```

> 💡 **关键洞察**
>
> 你可以组合两种模式。对于需要理解多个文件（广度）又要解决复杂算法（深度）的任务，使用 Planning Mode 加上 "think" 或 "ultrathink" 关键字。这让 Claude 同时获得广泛 context 和深度推理。

---

## 迭代改进工作流（Task 3.5 ★★★）

完整的迭代工作流结合所有三种技术：

1. **初始请求** — 描述你想要的（文字 + 可选截图）
2. **Claude 实现** — 直接执行或通过 Planning Mode
3. **你审核** — 在浏览器/IDE 中检查结果
4. **提供反馈** — 结果截图 + 描述要改什么
5. **Claude 改进** — 基于你的反馈迭代
6. **重复** 直到满意

> ⚠️ **成本考量**
>
> Planning Mode 和 Thinking Modes 都消耗额外 token。Planning Mode 读取更多文件（tool call token）。Thinking modes 使用更多推理 token。在任务复杂度足以证明成本合理时使用，不要作为每个请求的默认。

---

## 熟悉的类比

| 概念 | 类比 | 为何合适 |
|---------|---------|-------------|
| 直接执行 | 请资深工程师修一个 typo — 直接做 | 简单任务，不需要规划 |
| Planning Mode | Sprint 前的架构审核 — 先规划再建造 | 复杂任务需要前期探索 |
| Thinking modes | 给考试题目额外时间 | 更多时间 = 困难问题更好的推理 |
| Ultrathink | 困难设计问题的白板 session | 最大推理资源应对最大复杂度 |
| 截图输入 | 指着特定按钮说「改这个」 | 视觉沟通消除歧义 |

---

## 考试重点

| 考试概念 | 本课教了什么 |
|-------------|-------------------------|
| **Plan mode vs direct (3.4) ★★★** | Planning Mode 用于多文件/复杂任务；直接用于简单编辑。Planning 读取更多文件并创建可审核的计划。 |
| **Iterative refinement (3.5) ★★★** | 提问 → 实现 → 审核 → 反馈 → 改进循环。截图加速沟通。 |
| **Agentic loops (1.1) ★** | 迭代改进就是实践中的 agentic loop — 收集 context、规划、行动、评估、重复。 |

> 🎯 **考试笔记**
>
> 当考试呈现「复杂多文件重构」场景时，答案几乎总是涉及 Planning Mode。当场景涉及「模糊需求」或「复杂算法」时，答案涉及 Thinking Modes。两者同时出现时，组合使用。

---

## 练习题

### Q1：模式选择

一位开发者需要重命名一个在 Node.js monorepo 中被 15 个文件引用的数据库字段。哪种方法最合适？

- A. 直接执行 — 直接请 Claude 重命名
- B. Planning Mode — 让 Claude 探索代码库、识别所有引用，并在变更前创建计划
- C. Ultrathink — 请 Claude 深度推理这个重命名
- D. 为每个需要变更的文件开一个新的 Claude session

<details><summary>答案</summary>

**B** — 这是经典的 Planning Mode 场景：影响多个文件的变更需要先广泛探索代码库。Planning Mode 会读取相关文件、识别所有引用，并呈现全面的计划。

- A 有遗漏某些文件引用的风险
- C 解决了错误的问题 — 这需要广度（多文件），不是深度（复杂推理）
- D 违背了 agentic coding 助手的目的

考试哲学：**Architecture > Prompt** — Planning Mode 是处理多文件复杂度的结构方法。
</details>

### Q2：组合模式

一位开发者被指派设计新的缓存策略，涉及修改数据访问层、API 路由和配置系统。最佳缓存算法取决于代码库中的特定访问模式。哪种方法最好？

- A. 直接执行配上详细的 prompt
- B. 只用 Planning Mode — 它会找出算法
- C. 只用 Ultrathink — 它会找出文件变更
- D. Planning Mode + ultrathink — Planning Mode 用于广泛的代码库理解，ultrathink 用于推理最佳缓存算法

<details><summary>答案</summary>

**D** — 此任务同时具有广度复杂度（跨代码库的多个组件）和深度复杂度（选择最佳缓存算法）。组合 Planning Mode 和 thinking mode 同时处理两个维度。

考试哲学：**Proportionate response** — 对特定的复杂度配置使用正确的工具组合。
</details>

### Q3：成本效益使用

一位初级开发者开始对每个请求都使用 "ultrathink"，包括简单任务如「添加一个 console.log 语句」。他们的 token 使用量增加了 5 倍。你给什么建议？

- A. Ultrathink 是免费的，让他们继续
- B. 将 thinking modes 保留给真正有复杂度的任务 — 模糊需求、复杂算法或困难调试。简单任务不会从额外推理 token 中受益。
- C. 他们应该改用 Planning Mode 而不是 ultrathink
- D. 他们永远不应该用 ultrathink — 它是实验性的

<details><summary>答案</summary>

**B** — Thinking modes 消耗额外 token。对于加 log 语句这种简单任务，标准执行就够了。Ultrathink 是给真正困难的问题 — 更多推理时间能产生更好结果的场景。

考试哲学：**Proportionate response** — 让工具的力量匹配任务的复杂度。不要用大炮打蚊子。
</details>

---

## 反模式

| 反模式 | 为何失败 | 更好的方法 |
|-------------|-------------|-----------------|
| 每个任务都用 Planning Mode | 简单变更浪费 token；不必要地更慢 | 简单、范围明确的变更用直接执行 |
| 琐碎任务用 ultrathink | 烧推理 token 却无益处 | 将 thinking modes 保留给真正复杂的问题 |
| 从不用 Planning Mode | 多文件变更中遗漏依赖 | 范围不明确或跨多文件时启用 Planning Mode |
| 只用文字描述 UI 变更 | 有歧义 — 「左边的按钮」可以指很多东西 | 粘贴截图并指向特定元素 |
| 跳过 Planning Mode 的审核步骤 | 失去意义；可能执行有缺陷的计划 | 批准执行前永远审核计划 |
| 用 Cmd+V 而不是 Ctrl+V 粘贴截图 | 图片不会粘贴入 Claude Code | 截图粘贴专用 Ctrl+V |
