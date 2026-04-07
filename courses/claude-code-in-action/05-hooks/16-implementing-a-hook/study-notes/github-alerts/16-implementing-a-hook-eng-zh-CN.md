# 实现一个 Hook — 工程师深入解析

| 项目 | 细节 |
|------|--------|
| 考试领域 | D3 — Claude Code Configuration & Workflows (20%) |
| Task Statements | 3.2 (custom commands & hooks), 1.5 (Agent SDK hooks for tool call interception) |
| 来源 | claude-code-in-action / 05-hooks / Lesson 16 |

---

## 一句话摘要

实现一个 hook 就是在 `settings.local.json` 配置（matcher + command），然后编写脚本从 stdin 读取 JSON、检查 `tool_input`、以 exit code 0（允许）或 2（封锁 + stderr 反馈）结束。

---

## 逐步实现

### 1. 配置 `settings.local.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read|Grep",
        "hooks": [
          {
            "type": "command",
            "command": "node ./hooks/read_hook.js"
          }
        ]
      }
    ]
  }
}
```

> [!NOTE]
> **为什么用 `settings.local.json`？**
>
> 这个文件被 gitignore — 用于你的个人设置。用 `.claude/settings.json`（没有 `.local`）放团队共用的 hook。

### 2. 编写 Hook 脚本

```javascript
async function main() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }

  const toolArgs = JSON.parse(Buffer.concat(chunks).toString());

  const readPath =
    toolArgs.tool_input?.file_path || toolArgs.tool_input?.path || "";

  if (readPath.includes('.env')) {
    console.error("You cannot read the .env file");
    process.exit(2);
  }
}

main();
```

> [!WARNING]
> **关键实现细节**
>
> 1. **从 stdin 读取，不是 argv** — Tool call 数据通过 standard input 传入
> 2. **用 `console.error()`，不是 `console.log()`** — 反馈必须送到 stderr
> 3. **同时检查 `file_path` 和 `path`** — 不同工具可能用不同字段名
> 4. **Exit code 2，不是 1** — Code 2 专门表示"封锁此 tool call"

### 3. 重启并测试

> [!NOTE]
> **讲师视频洞察**
>
> Claude 在回应中识别出 hook 反馈："I was prevented by a read hook from accessing that file." 这展示了自我修正的反馈回路。

---

## 常见实现错误

| ❌ 错误 | ✅ 修正 | 为什么 |
|-----------|--------|-----|
| 用 `console.log()` 做反馈 | 用 `console.error()` | exit code 2 时只有 stderr 会送给 Claude |
| 以 exit code 1 封锁 | 以 exit code 2 封锁 | Code 1 = 一般错误；Code 2 = 刻意封锁 |
| 只读 tool_input.file_path | 同时检查 tool_input.path | Grep 用 `path`，Read 用 `file_path` |
| 忘记重启 Claude Code | 改 hook 后一定要重启 | Hook 在启动时加载 |

---

## 反模式（考试常考）

| ❌ 错误做法 | ✅ 正确做法 | 为什么 |
|-------------------|---------------------|-----|
| 在脚本中检查 tool_name 来过滤工具 | 用 config 中的 matcher 做工具过滤 | 关注点分离 |
| 静默封锁不反馈 | 封锁时一定要写 stderr | Claude 需要知道*原因* |
| 只防护 Read | 同时防护 Read 和 Grep | 两个工具都能暴露文件内容 |

---

## 练习题

### Q1：开发者生产力场景（S4）

你实现了一个 PreToolUse hook。脚本用了 `console.log("Access denied")` 和 `process.exit(2)`。Claude 封锁了读取但没显示信息。问题是什么？

- A. Exit code 应该是 1
- B. 反馈必须写到 stderr（`console.error()`），不是 stdout
- C. Matcher 还应包含 `Write`
- D. Hook 需要返回 JSON 响应

<details><summary>答案</summary>

**B** — exit code 2 时只有 stderr 输出会转发给 Claude。

> [!IMPORTANT]
> 关键原则：stderr = Claude 反馈；stdout = exit code 2 时被忽略
</details>

### Q2：CI/CD 集成场景（S5）

团队想实现 hook 检查 Claude 是否执行危险 Bash 命令。哪个方法正确？

- A. PostToolUse hook，执行后还原
- B. PreToolUse hook，matcher 为 `Bash`，读 stdin JSON，检查 `tool_input.command`，符合黑名单则 exit code 2
- C. PreToolUse hook，matcher 为 `.*`，封锁所有含 "rm" 的 tool call
- D. 在 system prompt 加入"永不执行 rm -rf"

<details><summary>答案</summary>

**B** — 需要 PreToolUse 在执行前封锁。Matcher 专门指向 `Bash`。

> [!IMPORTANT]
> 考试哲学：**Deterministic > Probabilistic**
</details>

### Q3：客户支持代理场景（S1）

你为客服代理实现 PreToolUse hook，封锁超过 $500 的退款。测试中 hook 允许了 $600 退款。最可能的原因？

- A. Exit code 应该是 1
- B. 脚本在检查错误的 `tool_input` 字段名
- C. 应该用 PostToolUse
- D. Matcher 应该是 `.*`

<details><summary>答案</summary>

**B** — 最常见的 bug 是 `tool_input` 字段名不匹配。每个工具定义自己的 input schema。

> [!IMPORTANT]
> 考试哲学：**Architecture > Prompt** — 实现正确性很重要
</details>
