# Introducing Hooks — 工程师视角

| 项目 | 内容 |
|------|------|
| 考试对应 | D3 — Claude Code Configuration & Workflows（占 20%） |
| Task Statements | 3.2（custom commands & hooks）、1.5（Agent SDK hooks） |
| 课程来源 | claude-code-in-action / 05-hooks / Lesson 14 |

---

## 一句话理解

Hooks 就是 Claude Code 工具执行 pipeline 上的 **middleware**。你写过 iOS 的 `URLProtocol` 拦截器吗？或者用过 Express 的 middleware？Hook 就是同一件事——在 tool 执行前后插入你自己的逻辑。

---

## 工具执行流程

当你对 Claude Code 说话，背后发生的事情如下：

![Tool Execution Pipeline](../../visuals/tool-execution-pipeline-zh-TW.svg)
*圖：Claude Code 如何處理工具呼叫 — 模型提出請求，系統透過 Hook 攔截，再執行。*
> 📎 流程图由 nanobanana 产出

重点：Hook 插在**工具执行的前后**，不是插在 Claude 思考的前后。

---

## 你已经熟悉的类比

| 你用过的技术 | 对应的 Hook 概念 | 行为 |
|------------|----------------|------|
| iOS `URLProtocol` 拦截 request | PreToolUse Hook | 检查 request，决定放行或拦截 |
| Express `app.use()` middleware | PreToolUse Hook | 在 handler 之前执行验证逻辑 |
| iOS `URLSession` delegate `didReceive` | PostToolUse Hook | response 回来后做后处理 |
| Git `pre-commit` hook | PreToolUse Hook | commit 前跑 lint，不过就挡下 |
| Git `post-commit` hook | PostToolUse Hook | commit 后触发 CI/通知 |
| Muse 的 `workflow-gate` | PreToolUse 概念 | 写 code 前先检查 issue/branch |

如果你理解 Git hooks，那 Claude Code hooks 就是同一套概念搬到 AI 工具上。

---

## 两种 Hook

### 1. PreToolUse — 事前拦截器

工具执行**之前**触发。**可以阻止操作**。

![PreToolUse Flow](../../../16-implementing-a-hook/visuals/env-guard-flow-zh-TW.svg)
*圖：.env 檔案守衛資料流 — PreToolUse 攔截 Read 呼叫，阻擋敏感檔案存取。*
> 📎 流程图由 nanobanana 产出

设定方式：

```json
"PreToolUse": [
  {
    "matcher": "Read",
    "hooks": [
      {
        "type": "command",
        "command": "node /home/hooks/read_hook.ts"
      }
    ]
  }
]
```

`matcher` 就是 pattern matching — 指定要拦截哪个工具。这里是只拦截 `Read`。

> 💡 **什么时候该用 PreToolUse？**
>
> 当操作**绝对不能发生**的时候。比如：
> - 禁止 Claude 读取 `.env` 或 credentials 文件
> - 禁止修改 `migrations/` 目录
> - 退款超过 $500 必须转人工
>
> 考试的核心思维是：**需要 100% 保证的事，用 hook（deterministic）；「尽量」就好的事，用 prompt（probabilistic）**。

### 2. PostToolUse — 事后处理器

工具执行**之后**触发。**不能阻止**（已经发生了），但可以：

![PostToolUse Feedback Loop](../../../16-implementing-a-hook/visuals/self-correcting-loop-zh-TW.svg)
*圖：自我修正回饋迴路 — Claude 嘗試、Hook 攔截並說明原因、Claude 自動調整做法。*
> 📎 流程图由 nanobanana 产出

设定方式：

```json
"PostToolUse": [
  {
    "matcher": "Write|Edit|MultiEdit",
    "hooks": [
      {
        "type": "command",
        "command": "node /home/hooks/edit_hook.ts"
      }
    ]
  }
]
```

注意 matcher 可以用 `|` 匹配多个工具，就像 regex 的 OR。

> 🎬 **影片补充**
>
> 讲师特别强调，PostToolUse hook 回传的讯息会**直接进入 Claude 的 context**。也就是说，如果你的 hook 跑 linter 然后回报 "Line 42: unused variable"，Claude 会在下一轮自动修正那个 variable。这是一个 **self-correcting feedback loop**，不需要人介入。

---

## 设定档的层级

Hook 定义在 Claude 的 settings 文件里，有三层：

| 层级 | 路径 | 适用范围 | 是否 commit 到 Git |
|------|------|----------|-------------------|
| 全域 | `~/.claude/settings.json` | 这台电脑所有项目 | 否 |
| 项目（共用） | `.claude/settings.json` | 整个团队 | **是** |
| 项目（个人） | `.claude/settings.local.json` | 只有你自己 | 否（gitignore） |

你也可以用 `/hooks` 指令在 Claude Code 里面互动式设定，不用手动改 JSON。

> 🎯 **考试重点**
>
> Settings hierarchy 的优先顺序是考试常考题。记住跟 Git config 一样的逻辑——越 local 的优先级越高。

---

## 实际应用场景

| 场景 | Hook 类型 | 做什么 |
|------|----------|--------|
| 自动格式化 | PostToolUse on Write/Edit | 写完文件后跑 `prettier` |
| 自动跑测试 | PostToolUse on Write/Edit | 编辑后跑 `npm test` |
| 存取控制 | PreToolUse on Read | 禁止读取敏感文件 |
| 程序码品质 | PostToolUse on Write/Edit | 跑 linter → 回馈给 Claude → 自动修正 |
| 操作日志 | PostToolUse on all | 记录 Claude 存取/修改了哪些文件 |
| 命名规范 | PostToolUse on Write | 检查新文件是否符合命名惯例 |

---

## 考试必记：Hook vs Prompt 的选择

这是考试最爱出的 trade-off 题型，跨 D1 和 D3：

| 情境 | 用 Hook | 用 Prompt | 判断依据 |
|------|---------|----------|---------|
| 退款超过 $500 必须转人工 | ✅ | ❌ | 「必须」= deterministic |
| 回复语气要友善 | ❌ | ✅ | 偏好 = probabilistic OK |
| 身份验证后才能做财务操作 | ✅ | ❌ | 合规需求 = 不能有例外 |
| 尽量写简短的回复 | ❌ | ✅ | 「尽量」= best effort |
| 每次编辑后自动格式化 | ✅ | ❌ | 一致性 = 不能漏 |

> 💡 **判断口诀**
>
> 题目出现「must / always / guaranteed / compliance」→ Hook。出现「prefer / usually / best practice」→ Prompt。

---

## 模拟考题

### 第一题：CI/CD Pipeline 情境

你的团队用 Claude Code 做 CI 自动化 PR review。你需要确保 Claude **绝对不会**修改 `migrations/` 目录里的文件。最可靠的方式是什么？

- A. 在 system prompt 加上指示：「不要修改 migrations 目录的文件」
- B. 设定 PreToolUse hook，拦截所有对 `migrations/` 路径的 Write/Edit 操作
- C. 把 `migrations/` 目录设成作业系统层级的只读权限
- D. 设定 PostToolUse hook，在 Claude 修改 migration 文件后自动 revert

<details><summary>答案与解析</summary>

**B** — PreToolUse hook 在操作发生前 deterministic 地阻止。

- A 是 prompt-based，有非零失败率（题目已经暗示「有时候会改到」）
- C 在 OS 层级挡住了，但 Claude 还是会尝试写入、浪费 token，而且错误讯息对 Claude 不够明确
- D 是事后补救——damage 已经造成，revert 的复杂度也高于直接 block

考试哲学：**Deterministic > Probabilistic**、**Validation > Trust**
</details>

### 第二题：开发者生产力情境

你希望 Claude Code 每次建立或编辑文件后，自动跑 `prettier` 格式化。正确的设定是哪个？

- A. PreToolUse hook，matcher 设为 `Write|Edit`，执行 prettier
- B. PostToolUse hook，matcher 设为 `Write|Edit|MultiEdit`，执行 prettier
- C. PostToolUse hook，matcher 设为 `Read`，执行 prettier
- D. PreToolUse hook，matcher 设为 `Bash`，执行 prettier

<details><summary>答案与解析</summary>

**B** — 格式化应该在文件写入/编辑**之后**执行（PostToolUse），而且要涵盖所有编辑类工具（包含 MultiEdit）。

- A 在文件还没写入前跑 formatter，没东西可以 format
- C 对错了工具——Read 是读取，不是编辑
- D 跟文件编辑无关
</details>

### 第三题：Customer Support Agent 情境

一个 Agent SDK 应用处理客户退款。公司政策规定：超过 $500 的退款必须转交给人工客服。该怎么 enforce 这个规则？

- A. 在 agent 的 system prompt 里说明 $500 的上限
- B. 用 PostToolUse hook 在退款处理后检查金额
- C. 用 tool call interception hook 拦截超过 $500 的 `process_refund` 呼叫，改为触发 `escalate_to_human`
- D. 用 few-shot examples 示范 $500 门槛的正确行为

<details><summary>答案与解析</summary>

**C** — PreToolUse interception 提供 deterministic 的合规保证。

- A 是 probabilistic（prompt 有失败率）
- B 太迟了——退款已经处理完毕
- D 也不能保证合规

考试哲学：**Deterministic > Probabilistic**、**Architecture > Prompt**
</details>
