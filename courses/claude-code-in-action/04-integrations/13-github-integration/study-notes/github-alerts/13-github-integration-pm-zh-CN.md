# GitHub Integration — PM 视角


![Github Workflows Two Actions](../../visuals/github-workflows-two-actions-zh-TW.svg)
*圖：GitHub 工作流 — @claude 提及 + PR 審查。*


![Github Integration Workflows](../../visuals/github-integration-workflows-zh-TW.svg)
*圖：GitHub 整合 — 兩個自動化工作流。*

| 项目 | 内容 |
|------|------|
| 考试对应 | D3 — Claude Code Configuration & Workflows（占 20%） |
| Task Statements | 3.6 ★★★（CI/CD integration）、2.4 ★★（MCP integration）、1.1 ★（agentic loops） |
| 课程来源 | claude-code-in-action / 04-integrations / Lesson 13 |

---

## TL;DR

Claude Code 的 GitHub 集成把 Claude 变成住在你 GitHub workflow 里的自动化团队成员。两个能力：(1) 在 issue/PR 里 `@claude` 提及触发交互式任务执行，(2) 每个 PR 自动 review。PM 需要理解这个，因为它定义了 AI 如何融入 code review 和 CI/CD 流程 — 以及权限治理该怎么做。

---

## Mental Model: 自动化团队成员


![Permission Model Local Vs Ci](../../visuals/permission-model-local-vs-ci-zh-TW.svg)
*圖：權限模型 — 本地互動 vs CI 非互動。*

| 角色 | 人类对应 | Claude GitHub 集成 |
|------|---------|-------------------|
| PR Reviewer | 资深工程师 review 代码 | PR Review Action — 自动、一致 |
| Issue Responder | On-call 工程师 triage bug | `@claude` mention — 即时、自主 |
| QA Tester | Merge 前手动测试 | Claude + Playwright — 自动化视觉测试 |
| 记录者 | 工程师记录调查结果 | Claude 在 issue/PR 贴出详细报告 |

> [!IMPORTANT]
> **考试核心哲学（PM 必记）**
>
> - **自动化 code review 是结构性地抓问题** — 每次都跑，不是靠人记得
> - **`-p` flag = 非交互模式** — Claude 不需人工核准就运行，所以权限必须明确
> - **Architecture > Prompt** — 结构化的 CI 集成胜过叫开发者记得去 review

---

## 两个 Workflow：做什么

### 1. `@claude` Mention — 交互式任务执行

任何人都可以在 issue 或 PR 留言中提及 `@claude` 来触发 Claude。

**PM 应用场景**：Bug triage — QA 工程师截图一个 bug，提及 `@claude`，Claude 调查、测试、回报，不需要开发者介入。

### 2. PR Review — 自动 Code Review

每个 PR 自动触发 Claude review 变更。

**PM 应用场景**：品质关卡 — 不管团队忙不忙，每个 PR 都有基本 review。

> [!TIP]
> **PM 决策框架**
>
> 把这两个想成不同的产品能力：
> - `@claude` mention = **随需 AI agent**（reactive，使用者触发）
> - PR review = **自动化品质关卡**（proactive，always-on）

---

## PM 该理解的设置

| 设置层 | 做什么 | PM 该关心的 |
|--------|--------|-----------|
| `custom_instructions` | 告诉 Claude CI 环境的信息 | 确保 Claude 知道你的测试基础设施 |
| `mcp_config` | 给 Claude 存取工具（例如 Playwright） | 决定 Claude **能做什么** |
| `allowed_tools` | 控制 Claude 可以使用哪些工具 | **安全治理** — 每个工具明确列出 |
| Setup 步骤 | 在 Claude 运行前准备环境 | 确保 app 已启动让 Claude 测试 |

> [!TIP]
> **PM Takeaway**
>
> `allowed_tools` 设置是权限边界。在 CI/CD 里，每个工具都必须逐一列出——没有「允许全部」的选项。这是刻意的安全设计。

---

## 商业影响

| 面向 | GitHub 集成前 | GitHub 集成后 |
|------|-------------|-------------|
| PR Review 覆盖率 | 取决于 reviewer 是否有空 | 100% — 每个 PR 都被 review |
| Bug Triage 响应时间 | 数小时（等开发者调查） | 数分钟（Claude 立即调查） |
| 代码品质一致性 | 因 reviewer 而异 | 标准化 — Claude 用同样方式检查每个 PR |
| 开发者 context switching | 频繁（review 请求打断 flow） | 减少 — Claude 处理第一轮 review |

---

## Instructor Insights（视频补充）

1. **Claude 执行前先建立可见的计划** — 通过 `@claude` 触发时，Claude 会在留言中贴出步骤 checklist。这个透明度对建立团队信任很重要。
2. **CI 里的端到端测试** — 讲师设置 Claude 启动 app、通过 Playwright 打开浏览器、测试 UI 功能——全在 GitHub Action 里完成。
3. **明确权限是不可妥协的** — 讲师强调在 GitHub Actions 里，每个 MCP 工具都必须逐一列出。没有捷径。

---

## Practice Questions

### 第一题：CI/CD Pipeline 情境

你的团队想在 GitHub Actions 加自动化 PR review。工程师问能不能用跟本地开发一样的权限设置（`.claude/settings.local.json` 里的 `mcp__playwright`）。你怎么回答？

- A. 可以，CI 用同样的设置
- B. 不行 — 在 GitHub Actions 里，每个工具必须在 `allowed_tools` 逐一列出。CI 模式没有 blanket server-level permission
- C. 不行 — MCP server 不能在 GitHub Actions 里使用
- D. 可以，但要把 `mcp__playwright` 加到 `.claude/settings.json`（project shared）而不是 local

<details><summary>答案与解析</summary>

**B** — 在 GitHub Actions（用 `-p` flag 的非交互模式）里，每个 MCP 工具都必须在 `allowed_tools` 逐一列出。

- A 错误假设 CI 和本地用同一套权限模型
- C 错误 — MCP server 可以在 CI 里用，只是权限更严格
- D 混淆了 settings 文件 scope 和 CI 权限需求

> [!IMPORTANT]
> **PM 重点**：规划 CI/CD 集成时，要考虑明确权限的需求。每加一个新的 MCP 工具到 workflow，`allowed_tools` 都需要更新。

</details>

### 第二题：开发者生产力情境

QA 团队通过建 GitHub issue 附截图来回报 bug。目前每个 bug 都需要开发者手动调查。Claude Code 的 GitHub 集成怎么帮忙？

- A. 加 `@claude` mention 支持，让 QA 可以直接在 issue 里触发 Claude 调查 bug，包含通过 Playwright 做浏览器测试
- B. 设置自动 PR review 在 bug 到 QA 之前就抓住
- C. 把 Claude 的调查结果加到 CLAUDE.md 让开发者知道常见 bug
- D. 设置 PreToolUse hook 防止 bug 被引入

<details><summary>答案与解析</summary>

**A** — `@claude` mention workflow 正好就是为这个场景设计的。

- B 是预防性的，但没有解决现有的 bug triage
- C 是文档化，不是自动化
- D 是开发期的控制，不是 QA workflow

> [!IMPORTANT]
> **PM 重点**：`@claude` mention 把 bug triage 从「需要开发者介入的阻塞活动」变成「AI 自动化的 workflow」。

</details>
