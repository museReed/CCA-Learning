# The Claude Code SDK — 工程师视角


![Sdk Architecture](../../visuals/sdk-architecture-zh-TW.svg)
*圖：Claude Code SDK 架構 — 三個進入點、同一引擎、權限模型。*

| 项目 | 内容 |
|------|------|
| 考试对应 | D2 — Tool Integration & MCP（占 20%）、D3 — Claude Code Configuration & Workflows（占 20%）、D1 — Agentic Architecture（占 27%） |
| Task Statements | 2.4（MCP integration — SDK 以编程方式扩展 Claude Code）、3.6（CI/CD integration — SDK 驱动自动化工作流）、1.1（agentic loops — SDK 以编程方式执行完整 agentic loop） |
| 课程来源 | claude-code-in-action / 06-sdk-and-wrap-up / Lesson 20 |

---

## 一句话理解

Claude Code SDK 让你从 TypeScript、Python 或 CLI 以编程方式执行 Claude Code — 继承所有设置和权限 — 默认为只读模式，需要通过 `allowedTools` 显式授权才能写入，是交互式 Claude Code 与自动化 pipeline 之间的桥梁。

---

## SDK 是什么，为什么存在

终端中的 Claude Code 是交互式的 — 人类打字、看回复。SDK 把人从循环中移除：你的代码发送 prompt 并处理回复。

关键点：SDK **不是**独立产品。它底层运行的是完全相同的 Claude Code，这意味着：

- 它读取 `CLAUDE.md` 文件
- 它遵守 `.claude/settings.json` 的权限设置
- 它使用相同的工具（Read、Write、Edit、Bash 等）
- 它遵循相同的 agentic loop 架构

> 💡 **核心洞察**
> SDK 就是没有终端 UI 的 Claude Code。相同引擎、相同配置、相同能力 — 不同接口。

---

## 三种访问方式

SDK 通过三种接口提供：

### 1. TypeScript（主要方式）

```typescript
import { query } from "@anthropic-ai/claude-code";

const messages = await query({
  prompt: "这个项目中有哪些重复的 query？",
  options: {
    maxTurns: 10,
  },
});

for await (const message of messages) {
  if (message.type === "text") {
    console.log(message.content);
  }
}
```

### 2. Python

```python
import subprocess
import json

result = subprocess.run(
    ["claude", "--print", "--output-format", "json", "Find duplicate queries"],
    capture_output=True, text=True
)
response = json.loads(result.stdout)
```

### 3. CLI（Pipe 模式）

```bash
echo "Find duplicate queries" | claude --print --output-format json
```

> 🎬 **讲师视频重点**
> 讲师先演示 TypeScript SDK，因为它提供最丰富的 API，支持 async iteration 逐条读取消息。Python 和 CLI 则是通过 subprocess 调用 `claude` CLI binary。

---

## 权限模型：默认只读

这是 SDK 中最重要的安全概念：

```typescript
// 默认：Claude 只能读取文件，不能修改
const messages = await query({
  prompt: "分析这个 codebase",
});

// 显式写入：必须指定 allowedTools
const messages = await query({
  prompt: "在 package.json 加入一个 test script",
  options: {
    allowedTools: ["Edit", "Write", "Bash"],
  },
});
```

**为什么默认只读？** 编程化执行时没有人类在循环中，没有人可以批准危险操作。SDK 默认采取最安全的姿态。

| 权限级别 | Claude 可以做什么 | 使用场景 |
|---------|------------------|---------|
| 默认（无 `allowedTools`） | 读取文件、分析代码、回答问题 | Code review、分析、文档查询 |
| `allowedTools: ["Edit"]` | 读取 + 修改现有文件 | 自动重构、代码修正 |
| `allowedTools: ["Edit", "Write"]` | 读取 + 修改 + 创建文件 | 代码生成、Scaffolding |
| `allowedTools: ["Edit", "Write", "Bash"]` | 完全访问包含 shell 命令 | CI/CD pipeline、Build 自动化 |

> 🎯 **考试重点**
> 最小权限原则适用：只授予 SDK 调用实际需要的工具。Code review pipeline 不应该有 `Bash` 访问权限。

---

## 基本使用模式

核心模式是：**import -> query -> iterate**

```typescript
import { query } from "@anthropic-ai/claude-code";

// 1. 发送 prompt（启动 agentic loop）
const conversation = await query({
  prompt: "找出 src/ 中所有重复的数据库 query",
  options: {
    maxTurns: 10,         // 限制 agentic loop 迭代次数
    allowedTools: [],      // 只读（默认）
  },
});

// 2. 异步迭代消息
for await (const message of conversation) {
  switch (message.type) {
    case "text":
      console.log("Claude 说:", message.content);
      break;
    case "tool_use":
      console.log("Claude 使用工具:", message.name);
      break;
    case "error":
      console.error("错误:", message.content);
      break;
  }
}
```

`query()` 函数返回一个 async iterable — 消息会随着 Claude 思考和行动流式传入，就像终端体验一样。

> 💡 **核心洞察**
> `maxTurns` 控制 Claude 可以执行多少次 agentic loop 迭代。每个 turn 可能包含多个 tool call。设太低可能让 Claude 无法完成复杂任务；设太高可能造成不必要的成本。

---

## 实际使用场景

SDK 的真正威力在 pipeline 集成中展现：

### Git Hooks

```typescript
// pre-commit hook：检查 secrets
const result = await query({
  prompt: "检查 staged 文件中是否有硬编码的 secrets 或 API keys",
  options: { maxTurns: 5 },
});
```

### Build Scripts

```typescript
// Post-build：生成 changelog
const result = await query({
  prompt: "比较 HEAD 与上一个 tag，生成一条 changelog 条目",
  options: { maxTurns: 10 },
});
```

### CI/CD Pipelines

```typescript
// PR review bot
const result = await query({
  prompt: `Review 这个 PR diff 找出问题:\n${prDiff}`,
  options: {
    maxTurns: 15,
    allowedTools: [],  // 只读用于 review
  },
});
```

> 🎬 **讲师视频重点**
> 讲师演示了两步骤工作流：先用只读模式调用 SDK 找出重复 query，再用 `allowedTools: ["Edit"]` 修改 `package.json`。这展示了渐进式权限提升模式。

---

## 安全性：设置继承

SDK 继承 `.claude/settings.json` 的所有设置：

```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep"],
    "deny": ["Bash(rm *)"]
  }
}
```

即使你的 SDK 代码传入 `allowedTools: ["Bash"]`，settings 中的 deny 规则仍然适用。这是纵深防御：

1. **第一层**：SDK `allowedTools` — 调用者授予的权限
2. **第二层**：`.claude/settings.json` — 项目允许的权限
3. **第三层**：Global settings — 用户系统级允许的权限

> 🎯 **考试重点**
> SDK 权限是调用者授予（`allowedTools`）和设置允许的**交集**。如果 settings deny `Bash(rm *)`，即使有 `allowedTools: ["Bash"]`，SDK 也无法执行 `rm`。

---

## 总结表格

| 概念 | 重点 | 考试相关性 |
|------|------|-----------|
| SDK 用途 | 以编程方式执行 Claude Code，无需终端 UI | D1 1.1 — 自动化中的 agentic loop |
| 三种接口 | TypeScript（主要）、Python、CLI | D2 2.4 — 编程化工具集成 |
| 默认只读 | 无写入权限，除非 `allowedTools` 显式授权 | D3 3.6 — 安全的 CI/CD 集成 |
| 设置继承 | SDK 遵守 `.claude/settings.json` 和 `CLAUDE.md` | D3 3.6 — 配置传播 |
| Async Iteration | `for await (const msg of conversation)` 模式 | D1 1.1 — 流式 agentic 响应 |
| maxTurns | 控制 agentic loop 深度 | D1 1.1 — 循环终止控制 |
| Pipeline 集成 | Git hooks、CI/CD、build scripts、自动化 | D3 3.6 — CI/CD 集成 |

---

## 记忆卡

| # | 正面 | 背面 | 记忆锚点 |
|---|------|------|---------|
| 1 | Claude Code SDK 的默认权限级别是什么？ | 只读。写入需要通过 `allowedTools` 显式授权。 | "没有钥匙就不能进" — SDK 默认门是锁的 |
| 2 | 访问 Claude Code SDK 的三种方式？ | TypeScript（`@anthropic-ai/claude-code`）、Python（subprocess）、CLI（pipe 模式） | 三扇门通往同一个房间 |
| 3 | SDK 中 `maxTurns` 控制什么？ | Claude 每次 query 可以执行的 agentic loop 迭代次数 | 就像赛车设定圈数上限 |
| 4 | SDK 会遵守 `.claude/settings.json` 吗？ | 会 — 它继承所有设置，包含 allow/deny 规则 | 相同引擎、相同规则手册 |
| 5 | 如何在 TypeScript SDK 中授予写入权限？ | 在 options 中传入 `allowedTools: ["Edit", "Write"]` | 显式的钥匙开显式的门 |
| 6 | CI/CD code review pipeline 推荐的权限模型？ | 只读（不设 `allowedTools`）— review 不需要写入权限 | 审计员，不是编辑者 |
| 7 | TypeScript SDK 的核心使用模式？ | Import `query` -> 带 prompt 和 options 调用 -> async iterate 消息 | Import、query、iterate |
| 8 | SDK 为什么默认只读？ | 没有人类在循环中批准危险操作 — 最小权限原则 | 没有主管就不给剪刀 |

---

## 练习题

### Q1：CI/CD 集成场景

团队想在 CI pipeline 中用 Claude Code SDK 加入自动化 code review 步骤。Review 只分析 PR，绝不修改代码。哪个配置正确？

- A. `allowedTools: ["Read", "Grep", "Glob"]`
- B. `allowedTools: []`（或完全省略这个字段）
- C. `allowedTools: ["Edit"]` 搭配 settings 中的 deny 规则
- D. `allowedTools: ["Bash"]` 来执行分析命令

<details><summary>答案</summary>

**B** — SDK 默认就是只读模式。对于只需分析（不需修改）的 code review pipeline，传空的 `allowedTools` 数组或省略即可。Claude 仍然可以读取文件、搜索代码、生成分析。

- A 不正确，因为 Read/Grep/Glob 默认就可用 — 不需列出
- C 授予不必要的写入权限再试图限制 — 违反最小权限原则
- D 授予远超 review 所需的 shell 访问权限

关键：SDK 的默认只读姿态就是分析类任务的正确选择。
</details>

### Q2：Agentic Loop 场景

你用 SDK 自动化 dependency 更新。Claude 需要读取 `package.json`、检查过期的 dependency 并更新它们。执行后你发现 Claude 在分析后停下，没有进行修改。最可能的原因是什么？

- A. `maxTurns` 设太低
- B. SDK 处于只读模式（没有 `allowedTools` 授权 Edit）
- C. `.claude/settings.json` deny 了 Write 权限
- D. TypeScript SDK 不支持文件修改

<details><summary>答案</summary>

**B** — SDK 默认只读。没有 `allowedTools: ["Edit"]`，Claude 可以分析 `package.json` 但无法修改它。Claude 会报告发现结果但跳过编辑步骤。

- A 可能导致过早停止，但描述的症状（分析后在编辑前停止）指向权限问题，不是 turn 限制
- C 有可能但不太可能是首要原因 — SDK 自身的只读默认会先触发
- D 事实错误 — TypeScript SDK 在授权后完全支持文件修改

关键：当 SDK 只分析不修改时，先检查 `allowedTools`。
</details>

