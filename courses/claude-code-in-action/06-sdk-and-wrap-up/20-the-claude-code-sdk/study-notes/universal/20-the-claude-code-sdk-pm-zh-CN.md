# The Claude Code SDK — PM 视角

| 项目 | 内容 |
|------|------|
| 考试对应 | D2 — Tool Integration & MCP（占 20%）、D3 — Claude Code Configuration & Workflows（占 20%）、D1 — Agentic Architecture（占 27%） |
| Task Statements | 2.4（MCP integration — SDK 以编程方式扩展 Claude Code）、3.6（CI/CD integration — SDK 驱动自动化工作流）、1.1（agentic loops — SDK 以编程方式执行完整 agentic loop） |
| 课程来源 | claude-code-in-action / 06-sdk-and-wrap-up / Lesson 20 |

---

## TL;DR

Claude Code SDK 让其他程序可以在没有人类操作键盘的情况下使用 Claude Code。它是相同的 Claude Code — 相同规则、相同能力 — 但由脚本和 pipeline 控制而非人类。默认只能读取、不能写入，这是刻意的安全设计。PM 需要理解这点，因为它决定了哪些自动化工作流是可行的，以及如何在需求中描述它们。

---

![Sdk Architecture](../../visuals/sdk-architecture-zh-TW.svg)
*圖：Claude Code SDK 架構 — 三個進入點、同一引擎、權限模型。*


## PM 为什么需要了解 SDK

SDK 将 Claude Code 从开发者工具转变为**自动化组件**。这对产品很重要：

| 没有 SDK | 有 SDK |
|---------|--------|
| Claude Code 一次帮一位开发者 | Claude Code 在 CI/CD 中为每个 PR 运行 |
| 人类必须手动输入每个 prompt | 脚本在事件（git push、build、排程）触发时启动 Claude Code |
| 权限由开发者即时批准 | 权限必须预先配置 — 没有人类在循环中 |

> 💡 **PM 重点**
> SDK 是 Claude Code 从「一位开发者的助手」扩展到「团队级自动化」的方式。任何涉及自动化 AI code review、代码生成或分析的需求，大概率需要 SDK。

---

## 心智模型：聘请承包商

把终端中的 Claude Code 想象成承包商在你身边工作 — 你告诉他做什么、看着他工作、逐步批准。

SDK 就像给承包商**书面工作指令**：

| 方面 | 终端（当面） | SDK（书面工作指令） |
|------|------------|-------------------|
| 沟通 | 即时对话 | 预先写好的指令 |
| 监督 | 你看着每一步 | 你事后审查结果 |
| 权限 | 当下说「好，去做吧」 | 必须在工作指令中预先指定 |
| 安全 | 你可以随时叫停 | 安全规则必须预先配置 |
| 规模 | 一次一个项目 | 同时处理多个项目 |

关键差异：**没有人类监督时，你需要更严格的前期规则。**

---

## 三种使用 SDK 的方式

SDK 有三种接口。PM 不需要知道语法，但应了解权衡：

| 接口 | 最适合 | 团队特征 |
|------|-------|---------|
| TypeScript | 丰富的集成、实时消息处理 | 有 Node.js/TypeScript 专长的团队 |
| Python | 数据 pipeline、ML 工作流、脚本 | Python 为主的技术栈 |
| CLI（pipe 模式） | Shell 脚本、快速自动化、bash-based CI | DevOps 团队、简单集成 |

> 💡 **PM 重点**
> 规划 SDK 集成时，问你的工程团队哪个接口适合他们的技术栈。功能完全相同 — 只有编程语言不同。

---

## 默认只读：一个产品决策

SDK 默认为**只读**模式。Claude 可以分析代码、找出问题、报告发现 — 但无法修改任何东西，除非被显式授权。

这不是限制 — 这是刻意的产品安全决策。

### 场景分析：为什么只读很重要

想象一个每晚的 CI 作业，用 Claude Code 审查所有未关闭的 PR：

| 场景 | 权限级别 | 会发生什么 |
|------|---------|-----------|
| PR 分析 + 评论 | 只读（默认） | Claude 读取代码、生成 review 评论。安全。 |
| 自动修正格式 | 读取 + Edit | Claude 读取代码并修改文件。需要信任编辑逻辑。 |
| 自动修正 + commit + push | 读取 + Edit + Bash | Claude 可以执行任意 shell 命令。没有护栏时风险很高。 |

每往上一个权限阶梯，都增加能力和风险。SDK 强制你显式做出这个权衡。

> 🎯 **考试重点**
> 最小权限原则：只授予特定任务所需的权限。Code review bot 应该只读。格式化 bot 需要 Edit。部署 bot 需要 Bash。绝不授予超过所需的权限。

---

## SDK 如何融入 Pipeline

SDK 最有用的角色是更大自动化工作流中的**组件**：

### 场景 1：Git Pre-Commit Hook

**业务需求**：防止意外提交 secrets

**流程**：开发者提交代码 -> SDK 分析 staged 文件（只读） -> 发现 secrets 时阻止提交

**权限**：只读（默认） — 只需分析，不需修改

### 场景 2：CI/CD Code Review

**业务需求**：每个 PR 都获得自动化第一轮审查

**流程**：PR 开启 -> CI 触发 SDK -> SDK 读取 diff 并生成 review -> 在 PR 上发布评论

**权限**：只读 — review 生成文字输出，不修改代码

### 场景 3：自动化 Dependency 更新

**业务需求**：无需手动工作即可保持 dependency 最新

**流程**：每周排程 -> SDK 检查过期包 -> SDK 更新配置文件 -> 创建 PR

**权限**：读取 + Edit — 必须修改配置文件

> 🎬 **讲师视频重点**
> 讲师展示两步骤演示：先用只读模式找出 codebase 中的重复 query，再授予 Edit 权限更新 package.json。这种渐进式权限模式是推荐做法 — 先分析，只修改需要的部分。

---

## 安全性：设置继承

SDK 继承项目配置中的所有安全规则。这意味着：

1. **项目级规则**（`.claude/settings.json`）适用于 SDK 调用
2. **Deny 规则无法被覆盖** — SDK 调用者无法绕过
3. **纵深防御**：即使 SDK 授予权限，项目设置仍可阻止

### 场景分析：多层安全

一家公司在 `.claude/settings.json` 中设置了这些规则：
- 允许：Read、Grep、Glob
- 禁止：删除文件的 Bash 命令

工程师写了一个 SDK 脚本，授予 `allowedTools: ["Bash"]`。

**结果**：Claude 可以执行 Bash 命令，但删除命令除外。Settings 的 deny 规则是 SDK 无法绕过的护栏。

> 💡 **PM 重点**
> 撰写 SDK 自动化需求时，同时指定 SDK 权限和项目设置。它们作为层级配合工作 — SDK 授予能力，settings 定义边界。

---

## SDK 功能的 PM 需求清单

指定 SDK 功能时，应包含：

| 需求领域 | 该指定什么 | 示例 |
|---------|-----------|------|
| 任务范围 | AI 应分析或修改什么 | 「审查 PR diff 中的所有 Python 文件」 |
| 权限级别 | 只读、Edit、Write、Bash 或组合 | 「分析用只读；自动修正模式用 Edit」 |
| 触发条件 | 什么事件启动 SDK 调用 | 「PR 创建时」或「每晚凌晨 2 点」 |
| 输出 | 结果送到哪里 | 「发布为 PR 评论」或「写入审计日志」 |
| 护栏 | AI 不得做什么 | 「不得修改测试文件」或「最多 10 个 agentic turn」 |
| 失败处理 | SDK 调用失败时怎么办 | 「记录错误并通知团队频道」 |

---

## 反模式（考试常考）

| 错误做法 | 正确做法 | 原因 |
|---------|---------|------|
| 授予完整权限「以策安全」 | 只授予最小所需权限 | 权限越多 = 风险越大。「安全」意味着更少权限，不是更多 |
| 把 SDK 当作不同于 Claude Code 的产品 | 理解 SDK 是相同引擎的编程接口 | 相同设置、相同工具、相同能力 |
| 需求中略过权限级别 | 明确指定每个自动化的只读 vs. 写入 | 工程师无法猜测预期的安全姿态 |
| 假设 SDK 自动化不需要人类监督 | 为高风险 SDK 操作设计审查检查点 | 没有人类在循环中意味着预配置的规则必须完善 |

---

## 总结表格

| 概念 | 重点 | 考试相关性 |
|------|------|-----------|
| SDK 用途 | 以编程方式执行 Claude Code 作为 pipeline 组件 | D1 1.1 — 自动化中的 agentic loop |
| 三种接口 | TypeScript、Python、CLI — 相同能力 | D2 2.4 — 编程化工具集成 |
| 默认只读 | 安全优先：除非显式授权否则不能写入 | D3 3.6 — 安全的 CI/CD 集成 |
| 设置继承 | 项目设置是 SDK 无法绕过的护栏 | D3 3.6 — 纵深防御 |
| Pipeline 集成 | Git hooks、CI/CD、build scripts、排程作业 | D3 3.6 — 工作流自动化 |
| 权限升级 | 先分析（只读），再修改（显式授权） | D3 3.6 — 渐进式权限模型 |

---

## 记忆卡

| # | 正面 | 背面 | 记忆锚点 |
|---|------|------|---------|
| 1 | Claude Code SDK 的默认权限级别是什么？ | 只读。写入需要显式的权限授予。 | 承包商拿到「只看不动」的工作指令 |
| 2 | SDK 提供哪三种接口？ | TypeScript、Python、CLI（pipe 模式）— 功能完全相同 | 打到同一间办公室的三条电话线 |
| 3 | SDK 为什么默认只读？ | 没有人类在循环中批准危险操作 — 最小权限原则 | 无人监督的承包商要更严格的规定 |
| 4 | SDK 会遵守项目设置吗？ | 会 — settings 中的 deny 规则无法被 SDK 权限授予覆盖 | 大楼保安优先于你的访客证 |
| 5 | SDK 自动化需要修改代码时，推荐做法是什么？ | 先用只读模式分析，再用显式权限授予修改 | 先验房再装修 |
| 6 | 列举三个 SDK 实际使用场景 | Git pre-commit hook（Secret 检测）、CI/CD code review、自动化 dependency 更新 | 保安、品检员、维修队 |
| 7 | PM 为 SDK 功能撰写需求时应指定什么？ | 任务范围、权限级别、触发条件、输出目的地、护栏、失败处理 | 完整的工作指令清单 |
| 8 | SDK 权限和项目设置如何互动？ | 取交集 — SDK 授予能力，settings 定义边界。Deny 规则永远胜出。 | 同一扇门上的两把锁 |

---

## 练习题

### 问题 1：CI/CD Pipeline 场景

团队希望 Claude Code 自动审查每个 PR 并发布评论。Review 应分析代码质量但绝不修改文件。作为 PM，需求中哪个权限规格是正确的？

- A. 「授予完整访问权，让 Claude 可以彻底审查代码」
- B. 「使用只读模式 — Claude 分析并生成 review 文字，不修改文件」
- C. 「授予 Edit 权限，让 Claude 可以修正 review 中发现的问题」
- D. 「授予 Bash 权限，让 Claude 可以在 review 过程中执行测试套件」

<details><summary>答案与说明</summary>

**B** — 只发布评论的 code review 只需要读取代码和生成文字。只读模式恰好提供此能力，且安全性最高。

- A 违反最小权限 — review 不需要写入权限
- C 混淆了 review 和 auto-fix — 这应该是分开的功能，各有各的权限
- D 增加不必要的风险 — 跑测试和 code review 是不同的事

**PM 重点**：将「分析」功能（只读）和「修改」功能（写入权限）分开。绝不将它们绑在同一个权限级别下。
</details>

### 问题 2：自动化安全场景

工程师提议一个 SDK 自动化，每周更新 dependency。脚本授予 `allowedTools: ["Edit", "Write", "Bash"]`。项目设置 deny `Bash(rm *)`。自动化会意外删除文件吗？

- A. 会 — `allowedTools` 覆盖项目设置
- B. 不会 — 项目设置的 deny 规则始终优先于 SDK 授权
- C. 会 — 但只在 Claude 判断删除是必要的情况下
- D. 不会 — 有任何 deny 规则时 `Bash` 完全被停用

<details><summary>答案与说明</summary>

**B** — 项目设置作为 SDK 授权无法绕过的护栏。`Bash(rm *)` 的 deny 规则无论 `allowedTools` 指定什么都会阻止文件删除。

- A 错误 — SDK 授权永远无法覆盖 settings deny 规则
- C 错误 — Claude 无法通过推理绕过 deny 规则
- D 错误 — 只有特定 pattern 被封锁，不是所有 Bash 用法

**PM 重点**：项目设置是你的安全网。撰写需求时，同时指定 SDK 权限和项目设置的 deny 规则以实现纵深防御。
</details>

### 问题 3：产品规划场景

你正在规划一个新功能：「AI 驱动的代码生成，从模板创建 boilerplate 文件。」最小所需的 SDK 权限级别是什么？

- A. 只读（默认）
- B. 仅 Edit
- C. Edit + Write
- D. Edit + Write + Bash

<details><summary>答案与说明</summary>

**C** — 创建新文件的代码生成需要 Write 权限（创建新文件）。如果生成也修改现有文件（例如更新 index），还需要 Edit。文件创建不需要 Bash。

- A 不足 — 只读模式无法创建文件
- B 不足 — Edit 修改现有文件但无法创建新文件
- D 授予不必要的 Bash 访问权 — 文件创建不需要 shell 命令

**PM 重点**：将每个功能动作对应到最小所需工具。「创建新文件」= Write。「修改现有文件」= Edit。「执行 shell 命令」= Bash。只授予所需的。
</details>
