# Adding Context — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows, D5: Context Management |
| Task Statements | 3.1 (CLAUDE.md hierarchy), 5.1 (context preservation), 5.4 (large codebase context) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> [!NOTE]
> 本节所有内容均直接来自官方课程教材。

## One-Liner / TL;DR

Context 管理是 Claude Code 中最具影响力的技能 — `/init` 生成 CLAUDE.md，三层 CLAUDE.md 层级提供持久指令，`#` memory mode 更新它们，`@` 文件提及则按需注入特定文件内容。

## Core Concepts

### Context 管理原则

太多不相关的 context 会降低 Claude Code 的效能。一般项目可能有数十甚至数百个文件，每个都包含大量信息。当你向 Claude 提问或交付任务时，存在一个理想的信息量 — 刚好足以理解如何回答或完成任务。一旦开始加入不相关的信息，效能就会下降。

引导 Claude 找到相关文件和文档非常重要。Claude Code 不需要手把手也能运作，但给予适当指引会得到最佳结果。

### /init 命令

首次在新项目中打开 Claude Code 时，执行 `/init`。Claude 将：

1. **分析整个 codebase** — 项目目的、整体架构、代码模式与结构
2. **识别关键元素** — 相关命令、重要文件、项目结构
3. **生成 CLAUDE.md 文件** — 将分析结果摘要写入此文件

当 Claude 尝试创建文件时，会询问权限：
- **Enter** — 批准文件写入
- **Shift+Tab** — 允许 Claude Code 自由写入项目中的文件（自动接受模式）

### CLAUDE.md 文件

CLAUDE.md 文件有两个用途：

1. **引导 Claude 理解 codebase** — 帮助 Claude 更快找到相关代码（命令、架构、风格）
2. **自定义指示** — 提供一般性指引给 Claude 的位置

此文件的内容会包含在你对 Claude 的每个请求中 — 它的功能等同于持久的 system prompt。

### CLAUDE.md 文件位置

Claude Code 在三个层级识别 CLAUDE.md 文件：

| 层级 | 文件 | 是否共享？ | 说明 |
|------|------|-----------|------|
| 项目 | `./CLAUDE.md` | 是 — 提交至版本控制 | 由 `/init` 生成。通过 Git 与其他工程师共享。包含项目特定的 Claude 指示。 |
| 本地 | `./CLAUDE.local.md` | 否 — 不提交 | 你希望 Claude 只为你遵循的个人指示。不与其他工程师共享。 |
| 全局 | `~/.claude/CLAUDE.md` | 否 — 机器专属 | 适用于你在这台机器上运行的所有项目的指示。 |

> [!TIP]
> 讲师鼓励打开生成的 CLAUDE.md 文件并查看其内容。由于它包含在每个请求中，了解其内容有助于优化 context。

### 使用 # Memory Mode 添加自定义指令

要更新 CLAUDE.md 而不需手动编辑文件，在 Claude Code 中使用 `#` 命令。这会进入「memory mode」，允许你智能地编辑 CLAUDE.md 文件。

**示例：**
```
> # Don't write comments so often
```

输入指令后，指定要加入哪个 CLAUDE.md 文件（项目、本地或全局）。Claude 会智能地将指令合并至该文件 — 不是盲目附加。

### 使用 @ 提及文件

使用 `@` 加上文件路径，将文件内容包含在请求中。这是将 Claude 指向特定方向的技巧。

**在聊天中（一次性 context）：**
```
> How does the auth system work? @auth
```
提及文件时，它会自动包含在对 Claude 的请求中。Claude 会显示认证相关文件供你选择。

**在 CLAUDE.md 中（持久 context）：**
```markdown
The database schema is defined in @prisma/schema.prisma.
Reference it when working with data models.
```
当 `@` 用在 CLAUDE.md 中，被引用文件的内容会自动包含在每个请求中。这意味着 Claude 可以立即回答相关问题，无需先读取文件。

> [!WARNING]
> CLAUDE.md 中每个 `@` 引用都会永久占用 context window 空间。仅引用在大多数请求中真正需要的文件。偶尔需要的文件请改用聊天中的交互式 `@` 提及。

## Demo Walkthrough：运行 /init 生成 CLAUDE.md

| 步骤 | 发生什么 | 截图 |
|------|---------|------|
| 1 | 讲师在项目中打开终端，用 `claude` 命令启动 Claude Code | |
| 2 | 运行 `/init` — Claude 开始分析整个 codebase | ![/init 命令](../../visual-guide/frames/frame_019.jpg) |
| 3 | Claude 识别项目目的、架构、相关命令、重要文件 | ![Codebase 分析](../../visual-guide/frames/frame_022.jpg) |
| 4 | Claude 摘要结果并写入 CLAUDE.md 文件 | |
| 5 | 权限提示出现 — Enter 接受，或 Shift+Tab 自由写入 | ![权限提示](../../visual-guide/frames/frame_025.jpg) |

## Demo Walkthrough：使用 # Memory Mode

| 步骤 | 发生什么 | 截图 |
|------|---------|------|
| 1 | 讲师注意到 Claude 在生成的代码中使用过多注释 | |
| 2 | 输入 `#` 进入 memory mode | ![进入 memory mode](../../visual-guide/frames/frame_044.jpg) |
| 3 | 输入指示：「don't write comments so often」 | ![添加指示](../../visual-guide/frames/frame_048.jpg) |
| 4 | 指定加入项目 CLAUDE.md 文件 | |
| 5 | Claude 智能地将指示合并至现有 CLAUDE.md | ![指示已合并](../../visual-guide/frames/frame_050.jpg) |
| 6 | 打开文件并通过搜索验证指示已添加 | |

## Demo Walkthrough：使用 @ 文件提及

| 步骤 | 发生什么 | 截图 |
|------|---------|------|
| 1 | 讲师想了解认证系统如何运作 | |
| 2 | 使用 `@auth` 提及认证文件 — 文件内容包含在请求中 | ![@ 提及 auth](../../visual-guide/frames/frame_055.jpg) |
| 3 | 说明这是将 Claude 指向特定方向的优秀技巧 | |
| 4 | 展示 CLAUDE.md 中也能使用相同的 `@` 语法进行持久引用 | ![CLAUDE.md 中的 @](../../visual-guide/frames/frame_060.jpg) |
| 5 | 提及 `@prisma/schema.prisma` — 定义所有数据表和记录类型的数据库 schema | |
| 6 | 使用 `#` memory mode 将 schema 引用加入 CLAUDE.md | ![添加 schema 引用](../../visual-guide/frames/frame_064.jpg) |
| 7 | 询问「user 有哪些属性？」— Claude 立即回答，无需读取 schema 文件 | ![即时回答](../../visual-guide/frames/frame_068.jpg) |

## 讲师提示

- 首次在新项目中使用 Claude Code 时运行 `/init`
- 打开并查看生成的 CLAUDE.md，了解 Claude 对你项目的认知
- `#` 快捷方式比手动编辑 CLAUDE.md 更快 — Claude 会智能合并指令
- 当你已知相关文件时，使用 `@` 提及可节省时间
- 将关键的跨领域文件（如数据库 schema）用 `@` 放入 CLAUDE.md，让 Claude 随时具备该 context
- 要有选择性 — CLAUDE.md 中过多 `@` 引用会浪费 context window 并降低效能

## Key Takeaways

1. 太多不相关的 context 会降低 Claude Code 效能 — 给予恰到好处的指引
2. `/init` 通过分析 codebase 启动项目 context，生成 CLAUDE.md
3. CLAUDE.md 包含在每个请求中 — 它是持久的 system prompt
4. 三个 CLAUDE.md 层级：项目（共享）、本地（个人）、全局（所有项目）
5. `#` memory mode 让你智能更新 CLAUDE.md，无需手动编辑
6. 聊天中的 `@` 提供一次性 context；CLAUDE.md 中的 `@` 提供每次请求的持久 context
7. CLAUDE.md 中被引用的文件会自动加载 — Claude 可以立即回答而不需搜索

---

# PART 2: Study Aids

> [!NOTE]
> 补充学习资料，非官方课程内容。

## Familiar Analogies

| 概念 | 类比 | 为何适合 |
|------|------|---------|
| CLAUDE.md | `.bashrc` / `.zshrc` — 每次 shell session 加载 | 影响所有行为的持久配置，自动加载 |
| CLAUDE.md 层级 | CSS specificity：inline > class > element | 更具体的（本地）覆盖更通用的（全局） |
| `/init` | `git init` + 自动生成的 README | 以 metadata 和结构摘要启动项目 |
| CLAUDE.md 中的 `@` | 文件顶部的 `import` 语句 | 始终加载，始终可用 |
| 聊天中的交互式 `@` | 动态 `import()` | 按需加载，仅在该请求需要时使用 |
| `#` memory 命令 | `git config --global` 设置 | 为所有未来 session 持久保存指示 |
| Context window 预算 | 运行中程序的 RAM | 有限资源 — 加载过多会减少处理空间 |

## CCA Exam Connection

> [!TIP]
> 本课涵盖三个高价值考试主题：
>
> **CLAUDE.md 层级（Task 3.1）** — 三个层级：项目（通过版本控制共享）、本地（个人，gitignored）、全局（机器上所有项目）。越本地 = 优先级越高。
>
> **Context 保存（Task 5.1）** — CLAUDE.md 跨 session 持久存在。CLAUDE.md 中的 `@` 引用始终加载。`#` 命令更新持久记忆。
>
> **大型 codebase context（Task 5.4）** — 过多 context 损害效能。CLAUDE.md 中的 `@` 应谨慎使用于跨领域文件。让 Claude 通过工具自行探索其余部分。
>
> 考试测试的关键区别：
> - CLAUDE.md（共享）vs CLAUDE.local.md（个人）— 都是项目层级但共享范围不同
> - CLAUDE.md 中的 `@`（每次请求）vs 聊天中的 `@`（一次性）— 持久 vs 按需 context
> - `/init`（生成初始 CLAUDE.md）vs `#`（添加指令至现有 CLAUDE.md）

## Anti-Patterns

| Anti-Pattern | 为何失败 | 正确做法 |
|-------------|---------|---------|
| 在 CLAUDE.md 中加入 15+ 个 `@` 引用 | 消耗 context window，降低效能和准确度 | 仅保留跨领域文件；其余用交互式 `@` |
| 从不运行 `/init` | Claude 每次 session 从零开始 | 首次使用时运行 `/init`，之后逐步维护 |
| 使用 CLAUDE.local.md 存放团队标准 | CLAUDE.local.md 被 gitignore — 队友看不到 | 使用项目 CLAUDE.md 存放共享标准 |
| 每次手动编辑 CLAUDE.md | 繁琐且容易出错 | 使用 `#` memory mode 进行智能合并 |
| 将个人偏好放入项目 CLAUDE.md | 通过版本控制将你的风格强加给整个团队 | 使用 CLAUDE.local.md 或 ~/.claude/CLAUDE.md 存放个人偏好 |
| 忽略全局 ~/.claude/CLAUDE.md | 错失跨项目个人偏好的机会 | 在全局文件中设置个人代码风格 |

## Practice Questions

**Q1.** 你的项目 CLAUDE.md 说「使用 2 空格缩进」。你的 CLAUDE.local.md 说「使用 4 空格缩进」。你的全局 ~/.claude/CLAUDE.md 说「使用 tab」。Claude 遵循哪个？

- A) Tab（全局优先级最高）
- B) 2 空格缩进（项目 CLAUDE.md 是标准）
- C) 4 空格缩进（本地覆盖项目和全局）
- D) Claude 询问你要用哪个

> [!NOTE]
> **答案：C。** 在 CLAUDE.md 层级中，越本地 = 优先级越高。CLAUDE.local.md 覆盖项目 CLAUDE.md，后者覆盖全局 ~/.claude/CLAUDE.md。

**Q2.** 开发者在 CLAUDE.md 中加入 12 个 `@` 文件引用。响应变慢且不准确。最可能的原因和修复方式？

- A) Claude Code 对多个 `@` 引用有 bug — 更新到最新版
- B) `@` 引用消耗过多 context window — 移除非必要引用，改用交互式 `@`
- C) 文件太大 — 拆分成更小的文件
- D) CLAUDE.md 有 10 个 `@` 引用的限制 — 移除多余的

> [!NOTE]
> **答案：B。** 课程明确指出过多不相关的 context 会降低效能。CLAUDE.md 中的每个 `@` 引用都在每次请求时加载。修复方式是仅保留关键的跨领域文件，任务特定的文件改用交互式 `@`。

**Q3.** 你的团队希望所有使用 Claude Code 的开发者遵循相同的代码标准。哪种方式正确？

- A) 每位开发者在自己的 ~/.claude/CLAUDE.md 中加入标准
- B) 将标准加入项目 CLAUDE.md 并提交至版本控制
- C) 将标准加入项目中的 CLAUDE.local.md
- D) 使用 `#` 在每位开发者的 session 中设置标准

> [!NOTE]
> **答案：B。** 项目 CLAUDE.md 提交至版本控制，与所有团队成员共享。这是架构性方法 — 不需逐人手动设置，不会产生配置漂移。

**Q4.** 在聊天消息中使用 `@schema.prisma` 与在 CLAUDE.md 中加入 `@schema.prisma` 有何不同？

- A) 没有差别 — 两者运作方式相同
- B) 在聊天中，文件仅包含在该请求中；在 CLAUDE.md 中，包含在每个请求中
- C) 在 CLAUDE.md 中文件被缓存；在聊天中每次重新读取
- D) `@` 语法仅在聊天中有效，不适用于 CLAUDE.md

> [!NOTE]
> **答案：B。** 聊天中的交互式 `@` 为当前请求提供一次性 context。CLAUDE.md 中的 `@` 使文件内容持久化 — 自动包含在每个请求中，以 context window 空间换取即时可用性。
