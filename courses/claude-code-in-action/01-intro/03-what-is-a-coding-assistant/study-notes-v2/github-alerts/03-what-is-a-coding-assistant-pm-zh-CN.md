# What is a Coding Assistant? — PM / 非工程师路线

| Item | Detail |
|------|--------|
| Exam Domain | D1: Agentic Architecture & Orchestration, D2: Tool Design & MCP Integration |
| Task Statements | 1.1 (agentic loops), 2.1 (tool interfaces), 2.5 (built-in tools) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> [!NOTE]
> 本节所有内容均直接来自官方课程教材（视频字幕 + 讲师幻灯片）。

## One-Liner / TL;DR

Coding assistant 就像一个能思考问题又能动手做事的资深承包商 — 不只是站在旁边给建议而已。

## Core Concepts

### Coding Assistant 究竟是什么

Coding assistant 不仅仅是一个写代码的工具。把它想象成一个完整的问题解决系统：它理解你的需求、弄清楚需要什么信息、制定计划，然后执行。「助手」这个角色是关键 — 它代你行动，就像一个能思考又能动手的真人助理。

### Coding Assistant 的工作方式 — 三步骤循环

当你给 coding assistant 一个任务（例如「根据这个错误信息修复 bug」），它会遵循一个可重复的流程：

| 步骤 | 做什么 | 职场比喻 |
|------|--------|---------|
| 1 | **收集上下文** — 理解错误、找到相关文件、阅读相关代码 | 像新团队成员在处理问题前先翻阅 Slack 消息和文档 |
| 2 | **制定计划** — 决定修复问题的最佳方法 | 像资深工程师在写代码前先在白板上勾勒解决方案 |
| 3 | **采取行动** — 通过编辑文件、执行命令来实施修复 | 像工程师实际打开代码库并进行修改 |

> [!IMPORTANT]
> 步骤 1 和 3 需要**与外部世界交互** — 读取文件、执行命令。这就是魔法（和挑战）所在。就像给你的助手一把瑞士刀 — 每个工具让它能以不同方式与真实世界交互。

### Tool Use 的挑战

这是根本的限制：语言模型（AI「大脑」）只能处理文本并返回文本。它无法：
- 打开和读取你电脑上的文件
- 执行终端命令
- 写入或编辑代码文件
- 浏览网络

如果你问一个普通的语言模型「main.go 里有什么？」，它会告诉你它无法访问你的文件。它只能处理你给它的文本 — 就像一个只能通过书信沟通的专家顾问。

### Tool Use 的工作方式 — 完整流程

这就是 coding assistant 如何弥补差距的。课程中的 `ReadFile: main.go` 示例完整展示了发生什么：

| 步骤 | 发生什么 | 白话解释 |
|------|---------|---------|
| 1 | **你提问**：「main.go 文件里写了什么代码？」 | 你向 coding assistant 发送一个问题 |
| 2 | **Coding assistant** 在你的请求后附加工具指令 | 助手告诉 AI 大脑：「嘿，你有这些工具可以用 — 这是使用方法」 |
| 3 | **语言模型响应**：`ReadFile: main.go` | AI 大脑说：「我需要读那个文件 — 请对 main.go 使用 ReadFile 工具」 |
| 4 | **Coding assistant** 读取实际文件并将内容传回 | 助手去读取真正的文件，然后把内容交回给 AI 大脑 |
| 5 | **语言模型**根据文件内容提供最终回答 | 现在 AI 大脑能给你真正的答案，因为它看到了实际的代码 |

> [!NOTE]
> 这叫做**「tool use」** — 业界的标准术语。每个 coding assistant 都这样工作，但有些 AI 模型做得比其他的好得多。

### 为什么 Claude 的 Tool Use 很重要

Claude（AI 模型：Opus、Sonnet、Haiku）在 tool use 方面特别强。三个具体好处：

| 好处 | 对你的团队意味着什么 |
|------|-------------------|
| **处理更困难的任务** | Claude 能以创造性、出乎意料的方式组合工具，还能使用从未遇到过的工具 — 像一个不需要培训就能搞懂新软件的机灵员工 |
| **可扩展平台** | 容易添加功能 — Claude 无需重新训练即可适应。如果团队需要新的集成，直接加工具就好 |
| **更好的安全性** | 不需要预先扫描你的整个代码库或发送到外部服务器。Claude 按需读取文件 — 你的代码留在本地 |

## Demo Walkthrough: Tool Use Flow — Coding Assistant 如何读取文件

> [!NOTE]
> 以下演练重现讲师在视频中的演示（SRT 33-63）。

| 步骤 | 发生什么 | 截图 |
|------|---------|------|
| 1 | 纯语言模型被要求读取文件 — 它回应完全做不到 | ![LM 限制](../../visual-guide/frames/frame_034.jpg) |
| 2 | Coding assistant 在请求中加入工具指令（「这些是你可以用的工具」） | ![工具指令](../../visual-guide/frames/frame_045.jpg) |
| 3 | 模型以结构化的请求响应：`ReadFile: main.go` — 要求助手使用工具 | ![ReadFile 工具调用](../../visual-guide/frames/frame_050.jpg) |
| 4 | 助手从磁盘读取实际文件并将内容传回模型 | ![文件内容传回](../../visual-guide/frames/frame_056.jpg) |
| 5 | 模型现在基于实际文件内容给出真正的回答 | ![最终回答](../../visual-guide/frames/frame_060.jpg) |

**结果**：模型现在能有效地「读取文件」 — 不是因为它获得了新能力，而是因为 coding assistant 充当它的双手，帮它获取所需的东西。

## Instructor Tips

> [!TIP]
> 「Coding assistant 不仅仅是一个写代码的工具」— 讲师强调，理解底层发生什么事能帮助你更有效地使用这些工具，并对何时及如何部署它们做出更好的决策。

> [!TIP]
> 逐步演示清楚展示 AI 模型从未真正「读取」文件 — coding assistant（模型外面的软件包装层）负责做真实世界的工作。模型只是传达它需要什么。

## Key Takeaways

1. Coding assistant 使用语言模型（AI 大脑）来完成复杂的编程任务
2. 语言模型需要工具才能做真实世界的工作 — 它们无法自己读取文件或执行命令
3. 并非所有语言模型的 tool use 能力都一样好 — 这是关键的差异化因素
4. Claude 强大的 tool use 能力带来更好的安全性（代码留在本地）、容易定制化（添加工具）和处理更困难问题的能力

---

# PART 2: Study Aids

> [!NOTE]
> 补充学习材料，非来自官方课程。

## Familiar Analogies

- **行政助理比喻** — 没有工具的语言模型就像一个被锁在房间里、没有电话、电脑和文件的天才助理。如果你带资料给他，他能提供很好的建议，但他无法自己查任何东西。Tool use 就是把他的电话和电脑还给他。
- **食谱 vs. 厨房** — 知道食谱（模型的知识）但没有厨房（工具）是没用的。Coding assistant 就是让厨师（模型）能真正下厨的厨房。
- **App 集成** — 就像 Slack 加上集成功能（Google Drive、Jira、GitHub）后变得更强大，语言模型加上工具也是。每个工具就像一个集成，让它能做新的事情。

## CCA Exam Connection

> [!TIP]
> **考试提示**：本单元教授每个 coding assistant 背后的基础架构。需要记住的关键概念：
> - 三步骤循环：收集上下文、制定计划、采取行动
> - 语言模型无法直接访问文件或执行命令 — 需要 tool use
> - 五步骤 tool use 流程（特别是：每一步骤谁做什么）
> - Claude 的三大优势：更困难的任务、可扩展性、安全性
> - 语言模型（思考）和 coding assistant（行动）的区别

## Anti-Patterns

| 常见误解 | 为什么是错的 | 实际情况 |
|---------|-------------|---------|
| 「AI 直接读取我的文件」 | 语言模型只处理文本 — 没有文件系统访问权限 | Coding assistant 读取文件并将文本内容传递给模型 |
| 「所有 AI 代码工具基本上都一样」 | Tool use 质量在不同模型间差异很大 | Claude 被特别指出在 tool use 方面特别强 |
| 「我的代码会被上传到云端」 | 这是假设基于索引的架构 | Claude 的 tool-use 方法按需读取文件 — 你的代码留在你的机器上 |
| 「Coding assistant 只是高级版的自动补全」 | 自动补全是单一、狭隘的动作 | Coding assistant 执行完整循环：理解问题、计划、执行 — 可能经过多个回合 |

## Practice Questions

**Q1.** 在 tool use 交互中，语言模型响应了 `ReadFile: main.go`。接下来会发生什么？

- A) 语言模型直接从电脑的文件系统打开文件
- B) Coding assistant 拦截响应，从磁盘读取文件，并将内容传回模型
- C) 用户必须手动将文件内容复制粘贴到聊天中
- D) 模型从云端仓库下载文件

> [!NOTE]
> **答案：B。** 语言模型无法访问文件系统。Coding assistant（软件包装层）拦截结构化的工具调用，读取实际文件，并以文本形式将内容传回给模型处理。

**Q2.** 一位产品经理正在评估 coding assistant。以下哪一项是 Claude 强大 tool use 能力的明确好处？

- A) 它处理代码的速度比其他语言模型更快
- B) 它需要预先索引整个代码库才能达到最佳效果
- C) 它能以创造性的方式组合工具来处理更困难的任务
- D) 它只能使用它被特别训练过的工具

> [!NOTE]
> **答案：C。** Claude 能以有趣且出乎意料的方式组合工具，甚至能使用从未见过的工具。速度（A）未被提及，预先索引（B）与课程所述相反，而（D）与可扩展性好处矛盾。
