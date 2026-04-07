# 定义 Hooks — 工程师深入解析

| 项目 | 细节 |
|------|--------|
| 考试领域 | D3 — Claude Code Configuration & Workflows (20%) |
| Task Statements | 3.2 (custom commands & hooks), 1.5 (Agent SDK hooks for tool call interception) |
| 来源 | claude-code-in-action / 05-hooks / Lesson 15 |

---

## 一句话摘要

定义一个 hook 分四步：选择 PreToolUse 或 PostToolUse、通过 `matcher` 选取要拦截的工具、编写从 stdin 读取 tool call JSON 的 command、返回 exit code（0 = 允许，2 = 封锁）。

---

## 背景：这堂课的定位

前一堂课你学了 hooks *是什么*。这堂课专注在*如何定义*一个 hook ——这四步骤心智模型适用于从简单文件防护到复杂合规闸门的所有场景。

> [!TIP]
> **iOS/Swift 类比**
>
> 定义 hook 就像注册一个 `URLProtocol` 子类：你声明要拦截*哪些* request（`canInit(with:)`），写处理逻辑，然后返回结果。系统会在正确的时间点自动调用你。

---

## 四步骤 Hook 定义流程

### 第一步 — 选择 Pre 或 Post

| 决策 | PreToolUse | PostToolUse |
|----------|-----------|-------------|
| 何时执行？ | tool 执行**之前** | tool 执行**之后** |
| 能封锁吗？ | 可以（exit code 2） | 不行（已经执行了） |
| 类比 | `URLProtocol.canInit(with:)` — 加载前拒绝 | `URLSessionTaskDelegate.didFinishCollecting` — 完成后检查 |

> [!WARNING]
> **关键决策点**
>
> 如果目标是**阻止**一个动作，**必须**用 PreToolUse。PostToolUse hook 无法撤销已经发生的事情 — tool 已经执行完了。

### 第二步 — 选择要监控的 Tools（Matcher）

`matcher` 字段使用类似 regex 的语法来指定触发 hook 的工具：

```json
"matcher": "Read"          // 单一工具
"matcher": "Read|Grep"     // 多个工具（OR）
"matcher": ".*"            // 所有工具（通配符）
```

可以匹配的内建工具：

| 工具 | 用途 |
|------|---------|
| `Read` | 读取文件内容 |
| `Write` | 创建或覆写文件 |
| `Edit` | 修改现有文件 |
| `MultiEdit` | 一次调用中多处修改 |
| `Bash` | 执行 shell 命令 |
| `Grep` | 搜索文件内容 |
| `Glob` | 按模式查找文件 |
| `WebFetch` | 获取 URL 内容 |

> [!TIP]
> **发现可用工具**
>
> 直接问 Claude："列出你目前可使用的所有 tool 名称。"当 MCP server 加入自定义工具时特别有用。

### 第三步 — 编写 Command（stdin JSON）

你的 hook command 会从 standard input 收到一个 JSON 对象：

```json
{
  "session_id": "2d6a1e4d-6...",
  "transcript_path": "/Users/sg/...",
  "hook_event_name": "PreToolUse",
  "tool_name": "Read",
  "tool_input": {
    "file_path": "/code/queries/.env"
  }
}
```

你的 command 应检查的关键字段：

| 字段 | 用途 |
|-------|---------|
| `tool_name` | Claude 正在调用哪个工具 |
| `tool_input` | Claude 传入的参数（文件路径、命令等） |
| `hook_event_name` | 确认这是 PreToolUse 还是 PostToolUse |
| `session_id` | 识别当前 session（用于 logging） |

> [!NOTE]
> **实现备注**
>
> Command 可以是任何可执行程序：Node.js 脚本、shell script、Python 脚本，甚至编译过的二进制文件。Claude 不在乎语言 — 只看 exit code。

### 第四步 — 返回 Exit Code

| Exit Code | 含义 | 适用对象 |
|-----------|---------|-----------|
| `0` | 允许 — tool call 继续执行 | PreToolUse 和 PostToolUse |
| `2` | 封锁 — tool call 被拒绝 | **仅 PreToolUse** |

以 exit code 2 结束时：
- 写到 **stderr** 的文本会作为反馈发送给 Claude
- Claude 看到拒绝原因后可以调整行为

> [!CAUTION]
> **Exit code 2 仅适用于 PreToolUse**
>
> 在 PostToolUse hook 中使用 exit code 2 不会有封锁效果 — tool 已经执行完了。

---

## 完整配置示例

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

---

## 反模式（考试常考）

| ❌ 错误做法 | ✅ 正确做法 | 为什么 |
|-------------------|---------------------|-----|
| 用 PostToolUse 来"防止"文件读取 | 用 PreToolUse 在执行前封锁 | PostToolUse 无法撤销已完成的读取 |
| 在 system prompt 加"永不读取 .env" | 用 PreToolUse hook 搭配 Read\|Grep | Prompt 指令有非零失败率 |
| 只 match `Read` 来防护文件访问 | Match `Read\|Grep`（两者都能访问文件内容） | Grep 也能暴露文件内容 |
| 在 matcher 里硬编码文件路径 | 用 matcher 选工具，在 command 逻辑中检查路径 | Matcher 选的是工具，不是文件路径 |
| exit code 2 时忘记处理 stderr | 将清楚的拒绝原因写到 stderr | Claude 需要反馈来理解为何操作被封锁 |

---

## 练习题

### Q1：开发者生产力场景（S4）

你正在为一个处理敏感客户数据的团队构建 Claude Code 工作流程。`.env` 文件包含 API key 和数据库凭证。你需要确保 Claude **永远**不能通过任何工具访问其内容。哪个 hook 配置正确？

- A. PostToolUse hook，matcher 为 `Read`，检查文件路径中的 `.env`
- B. PreToolUse hook，matcher 为 `Read`，检查文件路径中的 `.env`
- C. PreToolUse hook，matcher 为 `Read|Grep`，检查文件路径中的 `.env`
- D. 在 CLAUDE.md 加入"永远不要读取 .env 文件"

<details><summary>答案</summary>

**C** — 需要 PreToolUse 才能在执行前封锁。`Read` 和 `Grep` 都能访问文件内容，所以 matcher 必须涵盖两者。

- A 用了 PostToolUse — 太晚了，文件已读取
- B 漏了 `Grep` — Claude 仍能通过 grep 搜索 `.env` 内容
- D 是 prompt-based，有非零失败率

> [!IMPORTANT]
> 考试哲学：**Deterministic > Probabilistic**、**Architecture > Prompt**

</details>

### Q2：CI/CD 集成场景（S5）

你的 CI pipeline 用 Claude Code 生成文档。你想记录 Claude 执行的每个 Bash 命令供审计，但不封锁任何操作。哪个 hook 定义合适？

- A. PreToolUse hook，matcher 为 `Bash`，logging 后 exit code 0
- B. PostToolUse hook，matcher 为 `Bash`，logging 后 exit code 0
- C. PreToolUse hook，matcher 为 `Bash`，logging 后 exit code 2
- D. PostToolUse hook，matcher 为 `.*`，exit code 2

<details><summary>答案</summary>

**B** — 审计 logging 应在命令执行后（PostToolUse）进行，这样也能捕获结果。Exit code 0 允许正常操作。

- A 在执行前运行 — 无法 log 尚未执行的命令结果
- C 封锁了操作，违背目的
- D match 所有工具（不必要）且用 exit code 2（封锁一切）
</details>

### Q3：多代理研究场景（S3）

研究代理使用多个 MCP tool 查询不同数据源。你需要将这些工具返回的所有日期字段标准化为 ISO 8601 格式。哪个 hook 方法正确？

- A. PreToolUse hook，在工具执行前转换日期
- B. PostToolUse hook，在每个工具返回后标准化日期
- C. 在每个工具的 description 加入日期格式指示
- D. PreToolUse hook，封锁返回非 ISO 日期的工具

<details><summary>答案</summary>

**B** — 数据标准化必须在工具返回数据后进行（PostToolUse）。

- A 在工具执行前运行 — 还没有数据可以标准化
- C 是 prompt-based，无法保证格式一致性
- D 无法在工具执行前知道它会返回什么格式

> [!IMPORTANT]
> 考试哲学：**Architecture > Prompt**、**Deterministic > Probabilistic**

</details>
