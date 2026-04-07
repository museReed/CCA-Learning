# Another Useful Hook — PM 视角

| 项目 | 内容 |
|------|------|
| 考试对应 | D3 — Claude Code Configuration & Workflows（占 20%）、D1 — Agentic Architecture（占 27%） |
| Task Statements | 1.5（Agent SDK hooks）、3.2（custom commands & hooks）、1.7（session state & resumption） |
| 课程来源 | claude-code-in-action / 05-hooks / Lesson 19（纯文字课程） |

---

## TL;DR


![Hook 分類總覽](../../visuals/hook-taxonomy-zh-TW.svg)
*圖：Hook 完整分類 — 全部 9 種 Hook 依生命週期、是否可攔截、用途分類。*

Claude Code 有 9 种 hook 类型——不只是 PreToolUse 和 PostToolUse。额外的 hook（`Stop`、`SubagentStop`、`Notification`、`PreCompact`、`UserPromptSubmit`、`SessionStart`、`SessionEnd`）覆盖了完整的 AI session 生命周期。对 PM 来说，这代表你可以在 AI 工作流的**每个阶段**指定自动化——从 session 开始到结束，而不只是工具执行期间。

---

## 为什么 PM 需要知道所有 Hook 类型

理解完整的 hook 分类让你能写出更精确的需求：

| PM 的问题 | 对应 Hook | 需求示例 |
|----------|----------|---------|
| 「AI 完成任务后会发生什么？」 | `Stop` | 「每次 review session 后生成摘要报告」 |
| 「环境如何设置？」 | `SessionStart` | 「Claude 启动时加载项目配置」 |
| 「子任务完成后怎么处理？」 | `SubagentStop` | 「coordinator 使用前验证 subagent 输出」 |
| 「如何保存 context？」 | `PreCompact` | 「自动压缩前 extract 关键决策」 |
| 「能验证用户输入吗？」 | `UserPromptSubmit` | 「处理前根据 template 检查 prompt」 |

不知道这些 hook 类型的话，PM 只能写出模糊的需求如「系统应该记录所有东西」——工程师无法精确实现。

---

## 心智模型：酒店住客生命周期

把 AI session 想成酒店住客的住宿过程：

| 酒店事件 | Hook 类型 | 发生什么 |
|---------|----------|---------|
| 住客 check in | `SessionStart` | 房间准备好、加载偏好设置 |
| 住客提出要求（客房服务） | `PreToolUse` | 验证要求是否允许、确认额度 |
| 要求完成 | `PostToolUse` | 质量检查、更新账单 |
| 住客找前台但没人 | `Notification` | 通知经理（需要权限或闲置中） |
| 礼宾部完成委托的跑腿 | `SubagentStop` | 带着结果汇报给住客 |
| 房间变得凌乱 | `PreCompact` | 客房在打扫前保存重要物品 |
| 住客投意见箱 | `UserPromptSubmit` | 前台先审阅再转交管理层 |
| 住客今天的要求都完成了 | `Stop` | 准备每日摘要 |
| 住客 check out | `SessionEnd` | 结账、清理、累积会员积分 |

> 💡 **PM 重点**
>
> 你不需要理解每个 hook 的技术实现。你需要知道**哪些生命周期时刻可以自动化**，这样你才能写出工程师能对应到特定 hook 类型的需求。

---

## 可变数据问题（PM 简化版）

工程师面临的一个挑战：每种 hook 类型收到不同的数据。这对 PM 很重要，因为它影响每个阶段有什么信息可用：

| Hook 类型 | 可用数据 | PM 影响 |
|----------|---------|--------|
| `PreToolUse` / `PostToolUse` | 哪个工具、什么输入、什么输出 | 可以根据特定工具动作做决策 |
| `Stop` | Session ID、transcript 路径 | 可以生成摘要但不知道最后一个具体动作 |
| `Notification` | Session ID、通知详情 | 可以警报但 context 有限 |
| `SubagentStop` | Session ID、subagent 输出 | 可以验证子任务结果 |

> 🎯 **PM 为什么要在意**
>
> 如果你写的需求是「记录 Claude 做的每个 database query」，工程师需要知道这代表 PostToolUse hook 挂在 database 工具上（有 `tool_input` 包含 query）。如果你写「每次 session 结束后摘要 Claude 做了什么」，那是 Stop hook（有 `transcript_path` 但没有个别工具数据）。

---

## 产品场景演练

### 场景：AI 驱动的 Code Review Pipeline

你是 CI/CD 系统的 PM，使用 Claude Code 做自动化 code review。不同 hook 类型的应用方式：

| Pipeline 阶段 | Hook 类型 | 自动化 |
|-------------|----------|--------|
| Pipeline 启动 | `SessionStart` | 加载 repo 配置、设置 review 范围 |
| Claude review 一个文件 | `PostToolUse` | 读完文件后跑 linter |
| Claude 写 review 评论 | `PostToolUse` | 验证评论格式 |
| Research subagent 调查一个 pattern | `SubagentStop` | 验证研究结果是结构化的 |
| Context 变大 | `PreCompact` | 裁剪前保存关键发现 |
| Claude 完成 review | `Stop` | 生成 review 摘要、写到 PR |
| Pipeline 结束 | `SessionEnd` | 清理临时文件、更新指标 |

**PRD 用语**：
- 不要写：「系统应该自动生成 review 摘要」
- 要写：「一个 `Stop` hook 在 Claude 完成回应后生成结构化 review 摘要并写到 PR」

这给工程师一个明确的实现目标。

---

## Debug Hook：PM 应该知道它存在

工程师用一个简单的 debug 技巧来发现每个 hook 收到什么数据：

```json
{
  "matcher": "*",
  "hooks": [{ "type": "command", "command": "jq . > log.json" }]
}
```

**PM 为什么要在意**：如果工程师说「我们不知道这个生命周期阶段有什么数据可用」，答案是：用 debug hook 去发现。这防止需求因为「我们需要先调查」而被挡住。

---

## PM 的 Hook 类型决策框架

写需求时，用这个决策树：

1. **需要在 AI 动作之前发生？** → PreToolUse（可以阻止）
2. **需要在 AI 动作之后发生？** → PostToolUse（只能反馈）
3. **需要在 Claude 回应完成时发生？** → Stop
4. **需要在子任务完成时发生？** → SubagentStop
5. **需要在 SESSION 开始/结束时发生？** → SessionStart / SessionEnd
6. **需要在 CONTEXT 即将被裁剪时发生？** → PreCompact
7. **需要在用户提交 PROMPT 时发生？** → UserPromptSubmit
8. **需要在 Claude 需要注意时发生？** → Notification

> 💡 **简单规则**
>
> 把 hook 跟**生命周期时刻**配对，而不是动作。「Claude 完成后」是 Stop hook，不是在每个工具上挂 PostToolUse hook。

---

## Anti-Patterns（考试常考）

| ❌ 错误做法 | ✅ 正确做法 | 为什么 |
|-----------|-----------|--------|
| 写「系统应该记录所有东西」 | 指定哪种 hook 类型记录什么数据 | 模糊需求导致 over-engineering 或 under-engineering |
| 假设所有 hook 提供相同数据 | 理解数据因 hook 类型而异 | 需求可能要求该生命周期阶段没有的数据 |
| 用 PostToolUse 做 session 结束动作 | 用 Stop hook 做 session 结束动作 | PostToolUse 每个工具都触发，Stop 只在结束时触发一次 |
| Multi-agent 设计忽略 SubagentStop | 用 SubagentStop 验证子任务输出 | 没有验证，coordinator 可能处理格式错误的 subagent 数据 |

---

## 模拟考题

### 第一题：CI/CD Pipeline 场景

你的团队 CI pipeline 用 Claude Code 做自动化 PR review。Claude 完成 review 后，你需要把摘要写到 log 文件做审计。哪个做法正确？

- A. PostToolUse hook，`matcher: "*"`，每次 tool call 后追加到 log
- B. Stop hook，读取 transcript 并生成结构化摘要
- C. SessionEnd hook，写出所有数据的 raw dump
- D. Notification hook，Claude 闲置时发送摘要

<details><summary>答案与解析</summary>

**B** — Stop hook 正好在 Claude 完成回应时触发。它可以通过 `transcript_path` 访问完整对话记录来生成有意义的摘要。这是「Claude 完成后」的正确 lifecycle moment。

- A 在每次 tool call 后都触发，生成很多不完整的条目——不是干净的摘要
- C 在整个 session 结束时才触发，可能太迟或太广泛
- D 在闲置或需要权限时触发，不是完成时

**PM 重点**：「Claude 完成后」对应的是 `Stop` hook，不是 PostToolUse。把 lifecycle moment 对对是写出可实现需求的关键。
</details>

### 第二题：Multi-Agent Research 场景

一个 coordinator agent 把研究任务分派给 subagent。你需要确保每个 subagent 返回结构化 JSON 数据后，coordinator 才能处理它。需求里该怎么写？

- A. 在 coordinator 的 system prompt 加上验证指示
- B. 实现 SubagentStop hook，验证 subagent 的输出结构
- C. 在 coordinator 的 tool calls 上挂 PostToolUse hook
- D. 加 PreCompact hook，在 context 裁剪前检查数据

<details><summary>答案与解析</summary>

**B** — `SubagentStop` 在 subagent 完成时触发，这正是应该做输出验证的时间点。它在 coordinator 处理可能格式错误的数据之前提供 deterministic 的验证。

- A 是 prompt-based（probabilistic），把负担加在 coordinator 上
- C 在 coordinator 自己的 tool calls 上触发，不是 subagent 完成时
- D 是关于 context 管理，不是输出验证

**PM 重点**：在 multi-agent 架构中，验证指定在 **agent 之间的边界**——那就是 SubagentStop hook 的位置。
</details>

### 第三题：Developer Productivity 场景

你的开发团队希望启动 Claude Code session 时，自动加载项目特定的 context（coding standards、架构决策）。应该用哪种 hook？

- A. PreToolUse hook，在第一次 tool call 前加载 context
- B. UserPromptSubmit hook，在第一个 prompt 前注入 context
- C. SessionStart hook，session 开始时加载项目 context
- D. Notification hook，Claude 请求权限时加载 context

<details><summary>答案与解析</summary>

**C** — `SessionStart` 在 session 开始或恢复时触发，是加载环境和项目 context 的自然位置。

- A 只在特定工具被调用时触发，可能不是第一个动作
- B 在每次用户 prompt 时都触发，不只是 session 开始——会重复加载 context
- D 在通知时触发，跟 session 初始化无关

**PM 重点**：环境设置属于 `SessionStart`，不属于 per-action hook。这确保 context 加载一次，整个 session 都可用。
</details>
