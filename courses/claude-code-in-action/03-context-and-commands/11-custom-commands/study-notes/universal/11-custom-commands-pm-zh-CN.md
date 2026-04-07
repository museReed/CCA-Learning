# Custom Commands — PM 视角


![Custom Commands Scope Architecture](../../visuals/custom-commands-scope-architecture-zh-TW.svg)
*圖：自訂指令範圍 — 專案 vs 使用者層級。*


![Custom Command Mechanism](../../visuals/custom-command-mechanism-zh-TW.svg)
*圖：自訂指令 — Markdown 檔案變成 Slash Command。*

| 项目 | 内容 |
|------|------|
| 考试对应 | D3 — Claude Code Configuration & Workflows（占 20%） |
| Task Statements | 3.2 ★★★（custom commands & skills）、3.1 ★★（CLAUDE.md config） |
| 课程来源 | claude-code-in-action / 03-context-and-commands / Lesson 11 |

---

## TL;DR

Custom commands 是你的工程团队可以创建和共享的可重复工作流程模板。不让每个开发者为常见任务（audit dependencies、写测试、review code）各写各的 prompt，团队在 `.claude/commands/` 里定义一次 command，所有人用同样的方式使用。PM 应该关注这件事，因为这就是你在团队中标准化 AI 辅助工作流程的方式 — 减少不一致和新人上手摩擦。

---

## 为什么 PM 需要知道这些

1. **一致性** — 当每个开发者都用 `/audit` 而不是各自版本的「检查我的 dependencies」，输出是可预测的
2. **新人上手** — 新的团队成员可以打 `/` 看到所有可用的工作流程，不用读文档
3. **流程编码化** — 你的团队最佳实践变成可执行的，不只是被文档记录
4. **可发现性** — Commands commit 到 repo 后，整个团队都看得到

---

## 心智模型：团队剧本

把 custom commands 想成**团队剧本** — 一套共享的标准操作程序。

| 没有 Commands | 有 Commands |
|-------------|-----------|
| 「我们团队怎么 audit dependencies？」— 问资深开发者 | 打 `/audit` — 每个人走同一个流程 |
| 「我们写测试的惯例是什么？」— 读文档 | 打 `/write_tests src/auth.ts` — 惯例已内建 |
| 每个开发者的输出略有不同 | 团队间标准化的输出 |
| 知识在人的脑子里 | 知识在 codebase 里 |

> 💡 **PM 重点**
>
> Custom commands 就是把部落知识变成共享基础设施的方式。如果你听到「只有 Alice 知道怎么做 X」，那个工作流程就应该变成一个 command。

---

## 它怎么运作（非技术摘要）

1. 开发者在项目的 `.claude/commands/` 文件夹里创建一个 markdown 文件
2. 文件名变成一个 slash command（例如 `audit.md` → `/audit`）
3. 文件包含给 Claude 的指示 — 检查什么、做什么、怎么回应
4. 特殊的 placeholder `$ARGUMENTS` 让用户在运行 command 时传入特定细节
5. 文件被 commit 到 repo，所以整个团队都能用

**示例**：`/write_tests src/auth.ts` 告诉 Claude：「按照我们项目的测试 patterns 为 `src/auth.ts` 写测试。」

---

## 产品情境演练

### 情境：在快速成长的团队中标准化代码质量

你的团队两个月内从 3 人成长到 8 人。你注意到：
- Code review 的评论很重复（「你忘了加测试」、「import pattern 不对」）
- 新工程师要一周才能学会项目惯例
- AI 产出的代码质量在开发者之间差异很大

| 问题 | Command 解决方案 | 影响 |
|------|----------------|------|
| 不一致的测试 patterns | `/write_tests $ARGUMENTS` — 编码测试惯例 | 所有 AI 产出的测试走同一个结构 |
| 忘记做 dependency audit | `/audit` — 跑完整的 audit + fix + test 循环 | 一键合规检查 |
| 质量不一的 code review | `/review $ARGUMENTS` — 标准化的 review checklist | 一致的 review 输出 |
| 新人上手慢 | 新开发者打 `/` 就能看到所有团队工作流程 | 自助式可发现性 |

> 🎯 **PM 重点**
>
> 规划 AI 辅助开发工作流程时，问工程团队：「哪些重复性任务应该变成 custom commands？」这是低成本、高影响的改善。

---

## Commands vs 其他设置

PM 常搞混什么时候用哪个工具。以下是实用的区分：

| 工具 | 类比 | PM 什么时候该要求 |
|------|------|-----------------|
| **Custom Commands** | SOP 剧本 | 「每个开发者都应该用同一个流程做 X」 |
| **CLAUDE.md** | 给 Claude 的项目 README | 「Claude 应该永远知道我们项目的 Y」 |
| **Hooks** | 自动合规检查 | 「Z 绝对不能发生 — 我们需要保证」 |
| **Memories** | 个人便利贴 | 个人偏好 — PM 不管这个 |

---

## 视频洞察

1. **Commands 是 markdown 文件** — 不需要写程序。PM 可以起草 command 模板然后交给工程团队审查。
2. **`$ARGUMENTS` 接受任何文字** — 不只是文件路径。你可以创建 `/estimate $ARGUMENTS`，其中参数是 feature 描述。
3. **需要重启** — 新增 commands 后，Claude Code 必须重启。在工作流程文档中要注意这点。

---

## 模拟考题

### 第一题：Developer Productivity 情境

你的工程团队用 Claude Code，但每个开发者为常见任务写自己的 prompt。这导致代码质量不一致。作为 PM，哪个建议对标准化最有影响？

- A. 写详细的 CLAUDE.md 指示涵盖每个工作流程
- B. 在 `.claude/commands/` 里为最常见的工作流程创建一组 custom commands，并 commit 到 repo
- C. 发一封团队 email 附上每个工作流程的建议 prompt
- D. 设置 hooks 来强制代码质量标准

<details><summary>答案与解析</summary>

**B** — Custom commands 把团队工作流程编码到项目结构中，让它们可发现、一致、可版本控制。它们特别针对「每个开发者写自己的 prompt」这个问题。

- A 是用来放持久性项目知识的，不是按需触发的工作流程
- C 是手动的，随时间会偏离，因为人们会修改 prompts
- D 是用来做 deterministic 强制执行的，不是工作流程标准化

**PM 重点**：当你想要每个人走同一个流程时，Commands 是对的工具。当你需要保证时，Hooks 是对的工具。
</details>

### 第二题：Code Generation 情境


![Claude Code Configuration Hierarchy](../../visuals/claude-code-configuration-hierarchy-zh-TW.svg)
*圖：Claude Code 設定階層。*

一位新工程师加入你的团队，问「我怎么知道有哪些 AI 工作流程可用？」Custom commands 的哪个特性解决了这个问题？

- A. Custom commands 会自动记录在 CLAUDE.md 里
- B. 在 Claude Code 里打 `/` 会列出所有可用的 commands，包括团队定义的 custom commands
- C. Custom commands 创建时会发通知
- D. Custom commands 只有创建它的开发者才能用

<details><summary>答案与解析</summary>

**B** — Custom commands 出现在 `/` 命令菜单里，跟内建命令并列。这让团队工作流程自动文档化，不用读外部文档就能发现。

- A 不是自动的 — CLAUDE.md 是独立的文件
- C 不是 commands 的功能
- D 不正确 — `.claude/commands/` 里的项目范围 commands 所有团队成员都能用

**PM 重点**：可发现性是 custom commands 相较于共享文档或部落知识的关键优势。
</details>
