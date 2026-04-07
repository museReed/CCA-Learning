# Adding Context — 工程深度笔记

| 项目 | 细节 |
|------|--------|
| 考试领域 | D3 — Effective Claude Code Usage (30%), D5 — Performance Optimization (12%) |
| Task Statements | 3.1 ★★★ (CLAUDE.md hierarchy), 5.1 ★★ (context preservation), 5.4 ★★ (large codebase context) |
| 考试场景 | S2 (Code Gen), S4 (Developer Productivity) |
| 来源 | claude-code-in-action / 02-getting-started / Lesson 07（视频 + 文字） |

---

## 一句话总结

Claude Code 的 context 管理是三层系统：`/init` 生成 CLAUDE.md，CLAUDE.md hierarchy 在三个层级提供持久化项目指令，`@` file mention 按需注入特定文件内容。

---

## /init 命令：引导 Context

首次在新项目中打开 Claude Code 时，执行 `/init`。此命令让 Claude：

1. **分析整个代码库** — 项目结构、架构、模式
2. **生成 CLAUDE.md 文件** — 摘要发现内容加上未来 session 的指令
3. **请求许可** — 你批准文件写入（Enter）或启用自动接受（Shift+Tab）

```
$ claude
> /init

Claude 分析你的代码库...
→ 识别项目目的、架构、关键文件
→ 将 CLAUDE.md 写入项目根目录
```

> [!NOTE] **讲师视频洞察**
>
> 讲师演示在 uigen 项目上执行 `/init`。Claude 读取整个代码库，识别为使用 Prisma/SQLite 的 Node.js 应用，并生成 CLAUDE.md 摘要架构、重要命令（`npm run dev`、`npm run setup`）和编码模式。讲师强调 CLAUDE.md「被包含在每个请求中」— 使其成为持久化的 system prompt。

---

## CLAUDE.md Hierarchy（Task 3.1 ★★★）


![Claude Md Hierarchy Priority Stack](../../visuals/claude-md-hierarchy-priority-stack-zh-TW.svg)
*圖：CLAUDE.md 階層 — local 覆蓋 project 覆蓋 global。*

这是本课最重要的考试概念。Claude Code 在三个层级识别 CLAUDE.md 文件：

```
优先级（最高 → 最低）：
┌─────────────────────────────────────────────┐
│ ~/.claude/CLAUDE.md          (Global)       │
│  → 适用于此机器上的所有项目                    │
│  → 个人偏好、全局规则                         │
├─────────────────────────────────────────────┤
│ ./CLAUDE.md                  (Project)      │
│  → 由 /init 生成，commit 到 repo             │
│  → 通过版本控制与团队共享                      │
├─────────────────────────────────────────────┤
│ ./CLAUDE.local.md            (Local)        │
│  → 不 commit 到版本控制                       │
│  → 此项目的个人覆盖设置                        │
└─────────────────────────────────────────────┘
```

**关键考试规则：越 local = 越高优先级。**

| 层级 | 文件 | 是否共享？ | 使用场景 |
|-------|------|---------|----------|
| Global | `~/.claude/CLAUDE.md` | 否（机器专属） | 「永远用 TypeScript」、「除非复杂否则不加注释」 |
| Project | `./CLAUDE.md` | 是（commit 到 repo） | 项目架构、命令、编码标准 |
| Local | `./CLAUDE.local.md` | 否（gitignored） | 个人覆盖、实验性指令 |

> [!TIP] **关键洞察**
>
> CLAUDE.md hierarchy 遵循与 CSS specificity 或环境变量优先级相同的覆盖模式：最具体的（local）赢过最一般的（global）。如果你的项目 CLAUDE.md 说「用 tabs」但 CLAUDE.local.md 说「用 spaces」，spaces 胜出。

---

## # Memory 命令

要更新 CLAUDE.md 而不手动编辑文件，使用 `#` 命令：

```
> # Use comments sparingly. Only comment complex code.
```

Claude 智能地合并此指令到你的 CLAUDE.md — 不是盲目追加。这称为「memory mode」因为它跨 session 持续有效。

---

## @ File Mention：精确 Context 注入（Tasks 5.1, 5.4）

需要 Claude 聚焦特定文件时，使用 `@` 语法：

```
> How does the auth system work? @auth
```

Claude 显示 auth 相关文件列表让你选择。选中文件的内容被包含在当前请求中。

**两种使用模式：**

### 1. 交互式 @ mention（在聊天中）

输入 `@` 后跟部分文件名。Claude 提供自动完成建议。文件内容注入到该单一请求。

### 2. CLAUDE.md 中的 @ mention（持久化）

```markdown
# CLAUDE.md
The database schema is defined in @prisma/schema.prisma.
Reference it when working with data models.
```

当 `@` 在 CLAUDE.md 中使用，被引用的文件会在**每个请求**中自动包含。强大但昂贵 — 每个 turn 都消耗 context window。

> [!WARNING] **Context Window 警告**
>
> CLAUDE.md 中的每个 `@` 引用永久占用 context window 空间。只引用真正在大多数请求中需要的文件。偶尔需要的文件，改用交互式 `@` mention。

> [!NOTE] **讲师视频洞察**
>
> 讲师将 `@prisma/schema.prisma` 加入 CLAUDE.md，让 Claude 始终知道数据结构。他解释这意味着「Claude 可以立即回答关于数据结构的问题，不需要每次都搜索和读取 schema 文件。」这是用 context window 空间换取响应速度。

---

## 大型代码库的 Context 管理策略（Task 5.4）

```
Context 预算分配：
┌────────────────────────────────────────────┐
│  CLAUDE.md（始终加载）              ~5-10%  │
│  CLAUDE.md 中的 @ 引用             ~5-15%  │
│  每次请求的交互式 @ mention         ~10-20% │
│  Claude 通过工具读取的文件          ~30-50% │
│  对话历史                          ~20-30% │
│  Claude 的响应                     ~10-20% │
└────────────────────────────────────────────┘
```

**策略：**
- 只将关键的横切文件放在 CLAUDE.md `@` 引用中（schema、API 契约）
- 对任务特定的文件使用交互式 `@`
- 让 Claude 通过工具（Read、Glob、Grep）探索发现文件
- 太多不相关的 context **降低性能** — 少即是多

---

## 熟悉的类比

| 概念 | 类比 | 为何合适 |
|---------|---------|-------------|
| CLAUDE.md | `.bashrc` / `.zshrc` — 每次 session 启动时加载 | 塑造所有行为的持久化设置 |
| CLAUDE.md hierarchy | CSS specificity：inline > ID > class > element | 更具体的（local）覆盖更一般的（global） |
| `/init` | `git init` + README 生成 | 用 metadata 引导项目 |
| CLAUDE.md 中的 `@` | 文件顶部的 `import` 语句 | 始终可用，始终加载 |
| 交互式 `@` | 动态 `import()` | 按需加载，仅在需要时 |
| `#` memory 命令 | `git config --global` | 持久化设置供未来使用 |

---

## 考试重点

| 考试概念 | 本课教了什么 |
|-------------|-------------------------|
| **CLAUDE.md hierarchy (3.1) ★★★** | 三个层级：global > project > local。越 local = 越高优先级。Project CLAUDE.md 通过版本控制共享。 |
| **Context preservation (5.1) ★★** | CLAUDE.md 跨 session 持续有效。CLAUDE.md 中的 `@` 引用始终加载。`#` 命令更新记忆。 |
| **Large codebase context (5.4) ★★** | 太多 context 损害性能。只对关键文件在 CLAUDE.md 中使用 `@`。让 Claude 通过工具发现其余部分。 |

> [!IMPORTANT] **考试笔记**
>
> 考试哲学是「Architecture > Prompt」。CLAUDE.md 是 context 管理的架构方法 — 它是配置文件，不是 prompt。当考试问到「跨 session 提供一致 context」时，答案是 CLAUDE.md，不是「写更好的 prompt」。

---

## 练习题

### Q1：CLAUDE.md 优先级

你的项目 CLAUDE.md 说「用 2-space 缩进」。你的个人 CLAUDE.local.md 说「用 4-space 缩进」。你的全局 ~/.claude/CLAUDE.md 说「用 tabs」。Claude 遵循哪个风格？

- A. Tabs（global 有最高优先级）
- B. 2-space 缩进（项目 CLAUDE.md 是标准）
- C. 4-space 缩进（local 覆盖 project 和 global）
- D. Claude 问你要用哪一个

<details><summary>答案</summary>

**C** — 在 CLAUDE.md hierarchy 中，越 local = 越高优先级。CLAUDE.local.md 覆盖 CLAUDE.md，而 CLAUDE.md 覆盖 ~/.claude/CLAUDE.md。

考试哲学：**Architecture > Prompt** — hierarchy 是确定性的配置系统，不是协商。
</details>

### Q2：Context Window 管理


![Context Window Budget Allocation](../../visuals/context-window-budget-allocation-zh-TW.svg)
*圖：Context Window 預算分配。*

一位开发者在大型 monorepo 中将 15 个 `@` 文件引用加入 CLAUDE.md。他们注意到 Claude 的响应变慢且不准确。最可能的原因和修复是什么？

- A. Claude Code 对多个 `@` 引用有 bug；更新到最新版本
- B. `@` 引用消耗了太多 context window，留给 Claude 推理的空间更少；移除非必要引用，改用交互式 `@` mention
- C. 文件太大；将它们拆分成更小的文件
- D. CLAUDE.md 最多只能有 10 个 `@` 引用；移除多余的

<details><summary>答案</summary>

**B** — 课程明确指出太多不相关的 context 降低 Claude 的性能。CLAUDE.md 中的每个 `@` 引用在每次请求中加载，消耗 context window 空间。修复方法是只保留关键的横切文件，对任务特定的文件使用交互式 `@`。

考试哲学：**Proportionate response** — 让 context 匹配任务，而不是加载所有东西。
</details>

### Q3：团队 Context 共享

你的团队想确保所有使用 Claude Code 的开发者遵循相同的编码标准。哪个方法正确？

- A. 每个开发者将标准加入他们的 ~/.claude/CLAUDE.md
- B. 将标准加入项目 CLAUDE.md 并 commit 到版本控制
- C. 将标准加入项目中的 CLAUDE.local.md
- D. 使用 `#` 命令在每个开发者的 session 中设置标准

<details><summary>答案</summary>

**B** — 项目 CLAUDE.md commit 到版本控制，与所有团队成员共享。这是团队级标准的正确位置。

考试哲学：**Architecture > Prompt** — 使用内置的配置 hierarchy 而不是各开发者临时设置。
</details>

---

## 反模式

| 反模式 | 为何失败 | 更好的方法 |
|-------------|-------------|-----------------|
| 把所有东西都放在 CLAUDE.md `@` 引用中 | 消耗 context window，降低性能 | 只引用横切文件；其余用交互式 `@` |
| 从不执行 `/init` | Claude 每次 session 都从零开始 | 执行一次 `/init`，之后逐步维护 CLAUDE.md |
| 用 CLAUDE.local.md 放团队标准 | CLAUDE.local.md 是 gitignored；队友看不到 | 用项目 CLAUDE.md 放共享标准 |
| 每次手动编辑 CLAUDE.md | 容易出错且繁琐 | 用 `#` 命令进行智能合并 |
| 忽略全局 CLAUDE.md | 错失个人跨项目偏好的机会 | 在 ~/.claude/CLAUDE.md 设置个人编码风格 |
