# Adding Context — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows, D5: Context Management |
| Task Statements | 3.1 (CLAUDE.md hierarchy), 5.1 (context preservation), 5.4 (large codebase context) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> 本节所有内容均直接来自官方课程教材。

## One-Liner / TL;DR

CLAUDE.md 是你团队为 AI 助手准备的 onboarding 文档 — `/init` 生成它，三层层级在组织中强制执行标准，`@` 文件引用控制 AI 永远了解你项目的哪些内容。

## Core Concepts

### Context 管理原则

把 Claude Code 想象成加入你项目的新外包人员。如果你把公司里每份文档都堆在他桌上，他会不知所措且表现不佳。如果你只给关键的架构文档、代码标准，并指引他找到正确的文件，他就能快速上手。

课程明确指出：太多不相关的 context 会降低 Claude Code 的效能。一般项目有数十甚至数百个文件。理想是给 Claude 刚好足以完成任务的信息 — 不多不少。这直接影响开发者生产力和 AI 输出质量。

### /init 命令 — 自动化项目 Onboarding

首次在新项目中运行 Claude Code 时，`/init` 命令就像执行一次自动化 onboarding。Claude 会：

1. **阅读整个 codebase** — 理解项目目的、架构和模式
2. **识别重要内容** — 关键命令、重要文件、项目结构
3. **创建 onboarding 文档** — 生成 CLAUDE.md 文件，摘要其发现

开发者批准文件创建（Enter 接受，Shift+Tab 为自动接受模式）。这是每个项目的一次性设置。

**PM 重点：** `/init` 消除了「AI 不了解我们项目」的问题。一个命令，每位开发者的 AI 助手就理解项目架构。

### CLAUDE.md 文件 — 持久的团队配置

CLAUDE.md 有两个用途：

1. **AI 的项目知识库** — 架构、命令、代码风格（像 AI 真的会读的内部 wiki）
2. **自定义行为指示** — AI 在每次交互中遵循的规则

内容包含在每个对 Claude 的请求中 — 它是持久的 system prompt。把它想成塑造项目上所有 AI 行为的配置文件。

### CLAUDE.md 文件位置 — 三层策略系统

Claude Code 在三个层级识别 CLAUDE.md 文件，运作方式如同企业策略层级：

| 层级 | 文件 | 是否共享？ | PM 类比 |
|------|------|-----------|---------|
| 项目 | `./CLAUDE.md` | 是 — 提交至版本控制，与团队共享 | **部门策略** — 适用于项目上的每个人。由 `/init` 生成，在 Git 中版本控制。 |
| 本地 | `./CLAUDE.local.md` | 否 — 不提交至版本控制 | **个人例外** — 此项目的个人指示。其他团队成员看不到。 |
| 全局 | `~/.claude/CLAUDE.md` | 否 — 机器专属 | **全公司策略** — 适用于此开发者机器上的所有项目。个人跨项目偏好。 |

> **团队标准化：** 项目 CLAUDE.md 是你的杠杆。它提交至版本控制，意味着每位 clone repo 的开发者都继承相同的 AI 配置。这就是你在不依赖个人纪律的情况下，在团队中强制执行一致代码标准的方式。

### 使用 # Memory Mode 添加自定义指令 — 更新团队 Wiki

Claude Code 中的 `#` 命令进入「memory mode」— 不需手动打开 CLAUDE.md 文件就能更新的快捷方式。开发者输入指示，选择要加入哪个 CLAUDE.md 文件，Claude 智能合并。

**示例：** Tech lead 注意到 Claude 写太多代码注释。他们输入：
```
> # Don't write comments so often
```
这被合并入项目 CLAUDE.md。现在团队中每位开发者都受益于这条指示。

### 使用 @ 提及文件 — 控制 AI 焦点

`@` 语法将特定文件内容包含在对 Claude 的请求中。存在两种使用模式：

**在聊天中（临时，一次性）：**
```
> How does the auth system work? @auth
```
文件内容仅包含在该请求中。适合探索性工作。

**在 CLAUDE.md 中（持久，每次请求）：**
```markdown
The database schema is defined in @prisma/schema.prisma.
```
被引用的文件自动包含在每个请求中。Claude 可以立即回答关于数据结构的问题，无需搜索。

> **Context window 警告** — CLAUDE.md 中的每个 `@` 引用在每次请求时都消耗 context window 空间。这是预算权衡：更多持久 context = Claude 推理的空间更少。只放关键的跨领域文件。

## Demo Walkthrough：运行 /init 生成 CLAUDE.md

| 步骤 | 发生什么 | 截图 |
|------|---------|------|
| 1 | 开发者打开终端，用 `claude` 命令启动 Claude Code | |
| 2 | 运行 `/init` — Claude 分析整个 codebase | ![/init 命令](../../visual-guide/frames/frame_019.jpg) |
| 3 | Claude 识别项目目的、架构、命令、重要文件 | ![Codebase 分析](../../visual-guide/frames/frame_022.jpg) |
| 4 | 摘要结果并写入 CLAUDE.md | |
| 5 | 权限提示 — Enter 接受，Shift+Tab 自动接受 | ![权限提示](../../visual-guide/frames/frame_025.jpg) |

## Demo Walkthrough：使用 # Memory Mode

| 步骤 | 发生什么 | 截图 |
|------|---------|------|
| 1 | Claude 在生成的代码中写太多注释 | |
| 2 | 输入 `#` 进入 memory mode | ![Memory mode](../../visual-guide/frames/frame_044.jpg) |
| 3 | 输入：「don't write comments so often」 | ![添加指示](../../visual-guide/frames/frame_048.jpg) |
| 4 | 选择项目 CLAUDE.md 为目标 | |
| 5 | 指示合并至 CLAUDE.md — 现在适用于所有团队成员 | ![已合并](../../visual-guide/frames/frame_050.jpg) |
| 6 | 打开文件验证指示已添加 | |

## Demo Walkthrough：使用 @ 文件提及

| 步骤 | 发生什么 | 截图 |
|------|---------|------|
| 1 | 想了解认证系统 | |
| 2 | 使用 `@auth` 将认证文件包含在请求中 | ![@ auth](../../visual-guide/frames/frame_055.jpg) |
| 3 | 直接将 Claude 指向相关文件，而非让它搜索 | |
| 4 | 展示 CLAUDE.md 中的 `@` 语法用于持久引用 | ![CLAUDE.md 中的 @](../../visual-guide/frames/frame_060.jpg) |
| 5 | 引用 `@prisma/schema.prisma` — 数据库 schema 文件 | |
| 6 | 使用 `#` 将 schema 引用永久加入 CLAUDE.md | ![Schema 引用](../../visual-guide/frames/frame_064.jpg) |
| 7 | 询问 user 属性 — Claude 立即回答，无需搜索文件 | ![即时回答](../../visual-guide/frames/frame_068.jpg) |

## 讲师提示

- `/init` 是一次性投资，在每次后续交互中都有回报
- CLAUDE.md 是控制团队 AI 行为最具影响力的单一配置
- `#` 快捷方式让 tech lead 不需打开文件就能更新全团队 AI 行为
- 对 `@` 引用要有策略性 — 每个都是永久的 context 成本
- 定期审查 CLAUDE.md，移除过时或低价值的指示

## Key Takeaways

1. 太多不相关的 context 会降低 AI 效能 — 少即是多
2. `/init` 通过分析整个 codebase 生成 CLAUDE.md — AI 的自动化项目 onboarding
3. CLAUDE.md 包含在每个请求中 — 它是团队的 AI 配置文件
4. 三个层级：项目（全团队，版本控制）、本地（个人）、全局（所有项目）
5. `#` memory mode 无需手动编辑即可更新 CLAUDE.md — 快速行为调整
6. 聊天中的 `@` = 一次性 context；CLAUDE.md 中的 `@` = 每次请求的持久 context
7. Context window 是有限预算 — 优化 `@` 引用如同优化数据库查询

---

# PART 2: Study Aids

> 补充学习资料，非官方课程内容。

## Familiar Analogies

| 概念 | PM 类比 | 为何适合 |
|------|---------|---------|
| CLAUDE.md | 团队为 AI 助手准备的 onboarding 文档 | 告诉 AI 项目的一切，每次都加载 |
| CLAUDE.md 层级 | 企业策略层级：全公司 < 部门 < 个人例外 | 更具体的覆盖更通用的；本地偏好覆盖团队默认 |
| `/init` 命令 | 让新员工走 onboarding 流程 — 读完所有文档，了解组织 | 一次性设置，在每次未来交互中产生回报 |
| CLAUDE.md 中的 `@` | 定期会议中的固定议程项目 | 永远讨论，永远存在 — 消耗时间但确保覆盖 |
| 聊天中的 `@` | 在某次会议中提出的临时议题 | 一次性，与情境相关 — 不消耗定期时间 |
| `#` memory 命令 | 更新团队 wiki 或知识库 | 持久性变更，不因人员异动而消失 |
| Context window 预算 | 会议时间预算 — 总共 60 分钟 | 固定议程项目加载太多就没时间讨论新话题 |

## CCA Exam Connection

作为 PM，聚焦于以下考试角度：

**团队标准化（Task 3.1）** — 提交至版本控制的项目 CLAUDE.md = 所有开发者一致的 AI 行为。这是你的策略执行机制。

**Onboarding 效率（Task 5.1）** — 新开发者通过 CLAUDE.md 自动继承项目 context。不需手动 AI 培训。

**效能管理（Task 5.4）** — 如果开发者反映「Claude 变慢/不准确」，检查 CLAUDE.md 中的 context 过载。太多 `@` 引用是最常见的原因。

**决策规则：**「新加入的团队成员需要这个吗？」如果是，放入项目 CLAUDE.md。如果是个人的，用本地或全局。

## Anti-Patterns

| Anti-Pattern | 为何失败 | 正确做法 |
|-------------|---------|---------|
| Repo 中没有 CLAUDE.md | 每位开发者的 AI 每次 session 从零开始 | 运行 `/init`，提交 CLAUDE.md，持续维护 |
| 使用 CLAUDE.local.md 存放团队标准 | 本地文件被 gitignore — 团队看不到 | 使用项目 CLAUDE.md 存放共享标准 |
| CLAUDE.md 中塞满 `@` 引用 | Context window 饱和，效能下降 | 每季审计引用；仅保留跨领域文件 |
| 每位开发者各自配置 AI 规则 | 造成不一致和配置漂移 | 通过版本控制集中在项目 CLAUDE.md |
| 生成后就不再审查 CLAUDE.md | 过时的指示误导 AI | 像对待文档一样 — 定期审查和更新 |
| 将个人风格偏好放入项目 CLAUDE.md | 将一个人的偏好强加给整个团队 | 使用 CLAUDE.local.md 或 ~/.claude/CLAUDE.md 存放个人偏好 |

## Practice Questions

**Q1.** 你的 CTO 问：「如何确保所有 30 位使用 Claude Code 的开发者遵循相同的代码标准？」哪种方式正确？

- A) 发邮件请每位开发者配置自己的设置
- B) 将代码标准加入项目 CLAUDE.md 并提交至 repository
- C) 创建 CLAUDE.local.md 模板，请每位开发者复制
- D) 使用 Anthropic dashboard 设置组织级规则

> **答案：B。** 项目 CLAUDE.md 提交至版本控制，自动应用于每位 clone repo 的开发者。不需手动设置，不会漂移。选项 C 使用错误的文件类型（local 被 gitignore）。选项 D 不存在。

**Q2.** 开发者反映 Claude Code 响应自上周起变慢且不准确。调查发现他们在 CLAUDE.md 中加入了 12 个 `@` 文件引用。你建议什么？

- A) 升级到更高的 API 层级以获得更多 context window
- B) 审计 `@` 引用 — 仅保留跨领域文件，其余移至交互式 `@` 提及
- C) 完全移除 CLAUDE.md 从头开始
- D) 建议切换到更简单的项目结构

> **答案：B。** 课程明确教导过多 context 会降低效能。审计并优化 — 保留 schema 和 API contract，移除任务特定的引用。这是适度且有针对性的。

**Q3.** 新开发者加入你的团队。他们从未使用过 Claude Code。到达高效 AI 辅助开发的最快路径是什么？

- A) 提供 2 小时的 prompt engineering 培训
- B) 让他们安装 Claude Code 并 pull repo — 已提交的 CLAUDE.md 自动提供项目 context
- C) 请他们运行 `/init` 生成新的 CLAUDE.md
- D) 分享你个人的 CLAUDE.local.md

> **答案：B。** 如果团队维护了已提交的 CLAUDE.md，新开发者自动继承所有项目 context。选项 C 会覆盖团队现有的 CLAUDE.md。选项 D 分享的是个人、被 gitignore 的设置。

**Q4.** 开发者应该把不影响团队的个人代码偏好（如「永远使用 dark theme 示例」）放在哪里？

- A) 项目 CLAUDE.md
- B) CLAUDE.local.md 或 ~/.claude/CLAUDE.md
- C) Codebase 中的注释
- D) 环境变量

> **答案：B。** CLAUDE.local.md 用于个别项目的个人偏好（gitignored）。~/.claude/CLAUDE.md 用于跨项目的个人偏好（机器专属）。两者都不会与团队共享。
