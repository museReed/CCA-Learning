# Summary and Next Steps — PM 视角

| 项目 | 内容 |
|------|------|
| 考试对应 | 全部 5 个 Domain（D1-D5） |
| Task Statements | 复习：1.1、2.1、2.4、3.1、3.2、3.6 |
| 课程来源 | claude-code-in-action / 06-sdk-and-wrap-up / Lesson 22 |

---

## TL;DR

课程以三个建议收尾：保持更新、勇于实验、善用自动化。对 PM 来说，这是综合盘点的时刻 — 理解 Claude Code 在整个技术栈上的能力（agentic 执行、tool 集成、配置、CI/CD 自动化），并将其转化为产品决策、团队工作流和自动化策略。

---

![Course Review Map](../../visuals/course-review-map-zh-TW.svg)
*圖：課程章節對應 CCA 考試領域。*


## 我们学到了什么：逐章节 PM 重点

| 章节 | 学到什么 | PM 行动项目 |
|------|---------|------------|
| 01 — Intro | Claude Code 是 agentic coding assistant，能自主计划、执行和迭代。与 autocomplete 本质不同。 | **撰写定位文档**，在 build-vs-buy 评估时区分 agentic AI 和 autocomplete 工具。 |
| 02 — Getting Started | 通过 `CLAUDE.md` 进行 project setup，定义 Claude 如何理解你的 codebase。Context window 有限且需要管理。 | **定义项目标准**的 `CLAUDE.md` — 每个团队项目应包含哪些惯例、约束和 context？ |
| 03 — Context & Commands | Custom commands 创建可重复使用的工作流。Context 可通过 `@file` 引用精确控制。 | **识别团队重复性工作流**（code review、bug triage、release notes）可转为 custom commands。 |
| 04 — Integrations | MCP servers 扩展 Claude 的能力。GitHub integration 自动化 PR review 和 issue 响应。 | **评估** 与你技术栈相关的 MCP servers。**建立自动 PR review** 作为质量门。 |
| 05 — Hooks | Hooks 在 tool 执行级别强制执行策略。9 种 hook 类型涵盖完整生命周期。 | **定义治理策略**（如"禁止直接访问 production DB"）通过 hooks 强制执行。 |
| 06 — SDK & Wrap Up | SDK 提供 programmatic 集成。课程以三个前瞻性建议收尾。 | **规划集成路线图** — Claude Code 在你的 CI/CD pipeline 中的 programmatic 定位在哪？ |

---

## 三个建议的 PM 视角

### 1. Stay Updated — 追踪平台路线图

Claude Code 持续活跃演进。新能力会改变什么是可行的。

**PM 行动：**
- 订阅 Claude Code changelog 和 release notes
- 维护能力清单 — Claude Code 今天能做什么 vs 三个月前不能做什么
- 每季重新检视"目前不可行"的决策，因为能力在演进

### 2. Experiment — 建立团队肌肉记忆

定制化（CLAUDE.md、commands、MCP servers）是让 Claude Code 从通用助手变成团队专用工具的关键。

**PM 行动：**
- 在 sprint 中分配 Claude Code 实验时间（custom commands、MCP server 试用）
- 为组织项目创建共享的 `CLAUDE.md` template
- 记录团队使用哪些 MCP servers 及原因

### 3. Automate — 设计事件驱动工作流

GitHub integration 将 Claude Code 从开发者工具转变为团队自动化层。

**PM 行动：**
- 将团队的重复性任务映射到潜在自动化触发条件（PR 创建、Issue 开启、`@claude` mention）
- 定义自动响应的 SLA（如"PR 创建后 5 分钟内完成 review"）
- 建立治理框架，定义 Claude 可以和不可以自主做什么

---

## 课程 vs 考试 Domain 对照（PM 视角）

| Domain | 权重 | PM 应该知道什么 | 对应章节 |
|--------|------|----------------|---------|
| D1 — Agentic Architecture | 27% | Claude 如何自主计划和执行。为什么有时会失败（context 限制、tool 选择）。 | 01、02、06 |
| D2 — Tool Use & MCP | 20% | MCP 作为扩展模型。如何评估和集成第三方工具。 | 04 |
| D3 — Configuration | 20% | `CLAUDE.md` 作为团队标准。Commands 作为可重用工作流。Hooks 作为策略强制。CI/CD 作为自动化。 | 02、03、04、05 |
| D4 — Security & Trust | 15% | Permission model（3 层）。为什么 CI 需要明确权限。基于 Hook 的访问控制。 | 02、04、05 |
| D5 — Developer Productivity | 18% | 何时使用 Claude Code。自动化如何减少苦力。衡量生产力提升。 | 01、04、06 |

---

## PM 决策框架：投资优先顺序

根据完整课程内容，以下是优先投资框架：

| 优先级 | 投资项目 | 成本 | 影响 | 理由 |
|--------|---------|------|------|------|
| 1 | `CLAUDE.md` 标准 | 低 | 高 | 每次互动都受益于清晰的项目 context。零持续成本。 |
| 2 | 自动 PR review（GitHub integration） | 中 | 高 | 100% review 覆盖率。捕捉结构性问题。减少开发者 context switching。 |
| 3 | 团队工作流 custom commands | 低 | 中 | 标准化团队与 Claude 的互动方式。跨项目可重用。 |
| 4 | MCP server 评估 | 中 | 中 | 扩展 Claude 的能力以匹配你的技术栈。 |
| 5 | 基于 Hook 的治理 | 高 | 中 | Tool 级别的策略强制。对安全敏感团队很重要。 |
| 6 | SDK 集成 | 高 | 视情况 | 用于自定工具的 programmatic 访问。ROI 取决于使用案例。 |

---

## 商业影响总结

| 指标 | 导入 Claude Code 前 | 完整导入后 |
|------|-------------------|-----------|
| PR review 覆盖率 | 不一致（取决于 reviewer 可用性） | 100% 自动化初步 review |
| Bug triage 时间 | 数小时（开发者调查） | 几分钟（Issue 中 `@claude` mention） |
| Onboarding 摩擦 | 高（手动学习项目惯例） | 较低（`CLAUDE.md` 编码惯例） |
| 策略遵循 | 人工 review | 自动化（hooks 在 tool 级别强制） |
| 重复性任务成本 | 每次都消耗开发者时间 | 一次性 command/automation 设置 |

---

## Practice Questions

### Question 1：策略场景

你的团队完成了 Claude Code in Action 课程。CTO 要求你提出分阶段导入计划。哪个顺序最合理？

- A. SDK 集成 → hooks → CLAUDE.md → GitHub integration
- B. CLAUDE.md 标准 → GitHub integration（PR review）→ custom commands → hooks
- C. Custom commands → MCP servers → CLAUDE.md → SDK
- D. 先 Hooks（安全）→ 其他随意

<details><summary>答案与解析</summary>

**B** — 从最低成本、最高影响开始。`CLAUDE.md` 是基础（每次互动都受益）。GitHub PR review 提供即时自动化价值。Custom commands 标准化团队工作流。Hooks 在治理需求成熟后导入。

- A 从最高成本项目（SDK）开始 — 优先顺序不佳
- C 跳过基础层（CLAUDE.md）
- D 安全优先但忽略了需要基本采用后才能做治理

**PM 重点**：基础先行（CLAUDE.md）→ 自动化（GitHub）→ 定制化（commands）→ 治理（hooks）→ programmatic 访问（SDK）。
</details>

### Question 2：生产力场景

团队中一位开发者说"Claude Code 就是个高级 autocomplete"。根据课程，你应该解释什么关键区别？

- A. Claude Code 使用更大的语言模型
- B. Claude Code 在 agentic loop 中运作 — 自主计划、执行工具、观察结果并迭代，不像 autocomplete 只预测下一个 token
- C. Claude Code 可以使用 MCP servers
- D. Claude Code 可以读取 CLAUDE.md 文件

<details><summary>答案与解析</summary>

**B** — 根本区别在于 agentic loop。Autocomplete 预测行内补全。Claude Code 自主规划多步骤方案、执行工具（文件读写、终端命令）、观察结果并迭代。这是第一章的核心概念（D1 — Agentic Architecture）。

- A 是技术细节，不是架构层面的区分
- C 和 D 是 agentic 架构中的功能，不是核心差异

**PM 重点**：Agentic loop 是定义性能力。其他一切（MCP、hooks、SDK）都建立在这个自主的 plan-execute-observe 循环之上。
</details>

### Question 3：自动化场景

你的团队想自动化三个任务：(1) PR code review、(2) 强制"production code 中禁止 console.log"策略、(3) 从 PR 描述生成 release notes。哪些 Claude Code 功能对应到每个？

- A. (1) GitHub PR Review Action、(2) PreToolUse hook、(3) Custom command
- B. (1) Custom command、(2) CLAUDE.md 指令、(3) GitHub mention
- C. (1) MCP server、(2) PostToolUse hook、(3) SDK integration
- D. (1) GitHub PR Review Action、(2) PostToolUse hook、(3) Custom command

<details><summary>答案与解析</summary>

**A** — (1) GitHub PR Review Action 专为自动 code review 设计。(2) PreToolUse hook 可拦截文件写入，检测到 `console.log` 就 block — 这是 blocking 策略强制。(3) Custom command 可模板化 release notes 生成工作流。

- B 用 CLAUDE.md 做策略强制 — 这是指导而非强制（Claude 仍可继续）
- C 用 PostToolUse 做策略 — PostToolUse 无法 block，只能在事后提供反馈
- D 用 PostToolUse — 同 C 的问题，无法防止违规

**PM 重点**：Blocking enforcement 需要 PreToolUse（唯一能阻止执行的 tool-level hook）。PostToolUse 是用来观察和反馈的，不是强制的。
</details>
