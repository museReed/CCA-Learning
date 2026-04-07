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

## 背景：从理论到实践

Lesson 15 教了你*定义* hook 的四步骤框架。这堂课完整走过一个可运行的实现 — 一个防止 Claude 读取 `.env` 文件的 PreToolUse hook。

> 💡 **iOS/Swift 类比**

![.env Guard Flow](../../visuals/env-guard-flow-zh-TW.svg)
*圖：.env 檔案守衛資料流 — PreToolUse 攔截 Read 呼叫，阻擋敏感檔案存取。*

>
> 这就像从概念上理解 `URLProtocol` 到实际继承它、注册它、然后在 Xcode debugger 中看到你的拦截器触发。真正的学习发生在你看到各部分连接起来的时候。

---

## 逐步实现

### 1. 配置 `settings.local.json`

打开 `.claude/settings.local.json` 并加入 PreToolUse hook：

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

关键配置细节：
- **`matcher: "Read|Grep"`** — 拦截两个能访问文件内容的工具
- **`command`** — 指向实现逻辑的 Node.js 脚本
- **`type: "command"`** — 告诉 Claude Code 这是要执行的 shell command

> 📝 **为什么用 `settings.local.json`？**
>
> 这个文件被 gitignore — 用于你的个人设置。用 `.claude/settings.json`（没有 `.local`）放团队共用的 hook，应 commit 到版本控制。

### 2. 编写 Hook 脚本

脚本从 stdin 读取、解析 JSON、检查文件路径、以适当的 code 结束：

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

> ⚠️ **关键实现细节**
>
> 1. **从 stdin 读取，不是 argv** — Tool call 数据通过 standard input 传入
> 2. **用 `console.error()`，不是 `console.log()`** — 反馈必须送到 stderr
> 3. **同时检查 `file_path` 和 `path`** — 不同工具在 `tool_input` 中可能用不同字段名
> 4. **Exit code 2，不是 1** — Code 1 是一般错误；code 2 专门表示"封锁此 tool call"

### 3. 重启并测试

保存两个文件后：

1. **重启 Claude Code** — Hook 变更只在重启后生效
2. **用 Read 测试**：请 Claude 读取 `.env` — 应被封锁
3. **用 Grep 测试**：请 Claude grep `.env` — 也应被封锁
4. **用允许的文件测试**：请 Claude 读取其他文件 — 应正常工作

> 🎬 **讲师视频洞察**
>
> Claude 在回应中识别出 hook 反馈："I was prevented by a read hook from accessing that file." 这展示了反馈回路 — Claude 不只是失败；它理解*原因*并将此传达给用户。

---

## 常见实现错误

| ❌ 错误 | ✅ 修正 | 为什么 |
|-----------|--------|-----|
| 用 `console.log()` 做反馈 | 用 `console.error()` | exit code 2 时只有 stderr 会送给 Claude |
| 以 exit code 1 封锁 | 以 exit code 2 封锁 | Code 1 = 一般错误；Code 2 = 刻意封锁 |
| 只读 tool_input.file_path | 同时检查 tool_input.path | Grep 用 `path`，Read 用 `file_path` |
| 忘记重启 Claude Code | 改 hook 后一定要重启 | Hook 在启动时加载 |
| 用 `process.argv` 取输入 | 用 `process.stdin` | Tool call 数据通过 stdin 传入 |

---

## 反模式（考试常考）

| ❌ 错误做法 | ✅ 正确做法 | 为什么 |
|-------------------|---------------------|-----|
| 在脚本中检查 tool_name 来过滤工具 | 用 config 中的 matcher 做工具过滤 | 关注点分离 |
| 在 settings.json 中写 inline hook 逻辑 | 用外部脚本文件 | 可维护性、可测试性 |
| 静默封锁不反馈 | 封锁时一定要写 stderr | Claude 需要知道*原因* |
| 只防护 Read | 同时防护 Read 和 Grep | 两个工具都能暴露文件内容 |

---

## 练习题

### Q1：开发者生产力场景（S4）

你实现了一个 PreToolUse hook 来防止 Claude 读取 `.env` 文件。Hook 脚本用了 `console.log("Access denied")` 和 `process.exit(2)`。Claude 成功封锁了读取但没显示 "Access denied" 信息。问题是什么？

- A. Exit code 应该是 1，不是 2
- B. 反馈必须写到 stderr（`console.error()`），不是 stdout（`console.log()`）
- C. Matcher 除了 `Read` 还应包含 `Write`
- D. Hook 需要返回 JSON 响应而非纯文本信息

<details><summary>答案</summary>

**B** — Hook 以 exit code 2 结束时，只有 stderr 输出会转发给 Claude 作为反馈。`console.log()` 写到 stdout，不会被捕获。

- A：Code 1 是一般错误
- C：Write 不相关
- D：纯文本写到 stderr 是正确机制
</details>

### Q2：CI/CD 集成场景（S5）

团队想实现一个 hook，检查 Claude 是否在执行潜在危险的 Bash 命令（如 `rm -rf`）。哪个实现方法正确？

- A. PostToolUse hook，在执行后还原危险命令的结果
- B. PreToolUse hook，matcher 为 `Bash`，读取 stdin JSON，检查 `tool_input.command`，若命令符合黑名单则以 exit code 2 结束
- C. PreToolUse hook，matcher 为 `.*`，封锁所有包含 "rm" 的 tool call
- D. 在 system prompt 加入"永不执行 rm -rf"

<details><summary>答案</summary>

**B** — 需要 PreToolUse 在执行前封锁。Matcher 专门指向 `Bash`。脚本检查 `tool_input.command` 并应用黑名单检查。

- A：PostToolUse 太晚了
- C：`.*` 太广泛
- D：Prompt-based，有非零失败率

> 考试哲学：**Deterministic > Probabilistic**
</details>

### Q3：客户支持代理场景（S1）

你正在为客服代理实现一个 PreToolUse hook。Hook 必须在退款金额超过 $500 时封锁 `process_refund` 工具。测试中 hook 允许了 $600 的退款。最可能的原因是什么？

- A. Exit code 应该是 1 而不是 2
- B. 脚本在检查 `tool_input.refund_amount` 而不是工具实际使用的字段名
- C. 应该用 PostToolUse hook 而不是 PreToolUse
- D. Matcher 应该是 `.*` 来拦截所有 tool call

<details><summary>答案</summary>

**B** — 最常见的实现 bug 是 `tool_input` 中的字段名不匹配。每个工具定义自己的 input schema。脚本必须使用工具期望的确切字段名。

- A：Exit code 2 对封锁来说是正确的
- C：PostToolUse 无法封锁
- D：Matcher 应指向特定工具
</details>
