# 定义 Hooks — PM 视角

| 项目 | 细节 |
|------|---------|
| 考试范围 | D3 — Claude Code Configuration & Workflows（占考试 20%） |
| Task Statements | 3.2 (custom commands & hooks), 1.5 (Agent SDK hooks) |
| 课程来源 | claude-code-in-action / 05-hooks / Lesson 15 |

---

## 重点摘要

定义一个 hook 遵循四个步骤，就像在工厂设置质量检查站：（1）决定在工作完成*前*还是*后*检查，（2）选择要监控哪条生产线，（3）编写检查程序，（4）决定批准还是退回。PM 必须理解这个流程，才能撰写正确的验收标准，并与工程师沟通什么可以被*保证*、什么只是*尽力而为*。

---

## PM 为何需要理解 Hook 定义

当你撰写 PRD 时，你在指定需求。有些需求*必须* 100% 达成（合规、安全），有些则是*尽力而为*（语气、格式）。理解四步骤 hook 定义流程帮助你：

1. **指定执行机制** — 不只说"什么"，还说"怎么做"
2. **评估工程量** — hook 需要写脚本，不只是改 prompt
3. **设定合理期望** — hook 是确定性的；prompt 是概率性的

---

## 心智模型：工厂质量检查站


![Four-Step Hook Definition](../../visuals/four-step-process-zh-TW.svg)
*圖：定義 Hook 的四步驟流程 — Event → Matcher → Command → Exit Code。*

把 Claude Code 想象成工厂生产线。工具是机器（钻孔、焊接、喷漆）。Hook 是你安装的质量检查站：

| 步骤 | 工厂类比 | Hook 定义 |
|------|----------------|-----------------|
| 1. 前还是后？ | 钻孔前检查原料，还是焊接后检查成品？ | PreToolUse 在动作前封锁；PostToolUse 在动作后检查 |
| 2. 哪条线？ | 监控喷漆室和焊接站 | `matcher`：`"Read|Grep"` 选择要监控的工具 |
| 3. 检查程序 | 质检员按照检查清单 | Command 脚本读取 tool call 数据（JSON）并应用规则 |
| 4. 通过或退回？ | 绿灯（继续）或红灯（停线） | Exit code 0（允许）或 2（封锁） |

> 💡 **PM 决策框架**
>
> 撰写验收标准时问自己："这是绿灯/红灯需求（hook），还是指导方针（prompt）？"
> - **红灯**："系统必须阻止读取凭证" → Hook
> - **指导方针**："系统应以友善语气回应" → Prompt

---

## 以商业语言描述四步骤

### 第一步：前还是后？

| 需求类型 | Hook 类型 | 商业示例 |
|-----------------|-----------|-----------------|
| 预防 / 合规 | **PreToolUse** | 未经主管批准，封锁超过 $500 的退款 |
| 记录 / 质量检查 | **PostToolUse** | 记录每次客户互动到 CRM |
| 自动修正 | **PostToolUse** | 每次文档编辑后执行拼写检查 |

> ⚠️ **PM 必知**
>
> 如果你的需求写"绝不可以"或"必须永远防止"，在验收标准中指定 PreToolUse。PostToolUse 无法防止 — 它只在事后反应。

### 第二步：监控哪些操作？

`matcher` 字段选择哪些 AI 工具会触发检查站。常见场景：

| PM 需求 | 工程师翻译为 |
|---------------|----------------------|
| "Claude 不可读取凭证文件" | `matcher: "Read|Grep"` |
| "自动格式化 Claude 写的每个文件" | `matcher: "Write|Edit|MultiEdit"` |
| "记录所有 shell 命令" | `matcher: "Bash"` |
| "监控所有操作" | `matcher: ".*"` |

> 💡 **PM 常见疏忽**
>
> PM 经常忘记 `Grep`（搜索）也能暴露文件内容，不只 `Read`。务必问工程师："还有哪些工具可以访问这些数据？"

### 第三步：检查逻辑

Hook command 收到的是 Claude 要做什么的详细信息 — 不只是"Claude 想读文件"，而是具体的"Claude 想用 Read 工具读取 `/src/config/.env`"。

这种精细度意味着 hook 可以根据文件路径、命令内容或任何其他参数做出非常精确的判断。

### 第四步：裁决

| 裁决 | Exit Code | 接下来发生什么 |
|---------|-----------|-------------------|
| 批准 | 0 | Tool call 正常执行 |
| 退回 | 2 | Tool call 被封锁；Claude 收到拒绝原因并调整方法 |

拒绝反馈创造了自我修正回路 — Claude 不是静默失败；它理解*原因*并尝试替代方法。

---

## 讲师洞察（来自视频）

PM 应注意的讲师重点：

1. **工具发现是动态的** — 加入 MCP server 后可用工具会改变。工程师可以问 Claude"列出你可用的工具"来发现什么可以被监控。
2. **Matcher 使用类 regex 语法** — Pipe 符号 `|` 代表 OR。这是技术细节，但 PM 应知道一个 hook 可以监控多个工具。
3. **stderr 反馈很关键** — 当 hook 封锁动作时，错误信息直接发送给 Claude。好的错误信息帮助 Claude 找替代方案；差的信息造成困惑。

---

## 反模式（考试常考）

| ❌ 错误做法 | ✅ 正确做法 | 为什么 |
|-------------------|---------------------|-----|
| PRD 写"必须防止 X"但不指定执行机制 | 验收标准中指定"通过 PreToolUse hook 执行" | 不指定的话，工程师可能用 prompt 方案 |
| 假设 PostToolUse 能防止动作 | 预防需求用 PreToolUse | PostToolUse 在动作之后才运行 — 太晚了 |
| 多个工具能做同样的事却只监控一个 | 问工程师哪些工具能访问数据 | Grep 和 Read 一样能读文件内容 |
| 略过拒绝信息 | hook 规格中要求清楚的反馈信息 | Claude 需要反馈才能自我修正 |

---

## 练习题

### Q1：客户支持场景（S1）

你正在为 AI 客服代理撰写 PRD。其中一项需求："代理绝不可访问存储在 `.credentials` 目录的客户付款数据。"工程师提议将此指令加到 system prompt。你应该建议什么？

- A. 接受工程师提案 — prompt 指令足以做访问控制
- B. 要求 PreToolUse hook，封锁对 `.credentials` 路径的 Read 和 Grep 操作
- C. 要求 PostToolUse hook，记录 Claude 访问 `.credentials` 文件的时间
- D. 将限制加到 CLAUDE.md 并设为团队共用项目设置

<details><summary>答案</summary>

**B** — "绝不可访问"是合规需求，需要确定性执行。PreToolUse hook 在动作发生前封锁。Read 和 Grep 都必须涵盖，因为两者都能暴露文件内容。

- A 是 prompt-based，有非零失败率 — 合规需求不可接受
- C 是 PostToolUse — 太晚了，文件已被读取
- D 仍是 prompt 指令，不是程序化执行

**PM 重点**：当你在 PRD 写"绝不可"，你在指定确定性需求。执行机制必须相符 — 用 hook，不是 prompt。
</details>

### Q2：开发者生产力场景（S4）

你的团队希望 Claude Code 在每次文件编辑后自动执行代码格式化。格式化不应封锁 Claude 的工作 — 只是清理格式。你在需求中应指定什么方法？

- A. PreToolUse hook 搭配 Write|Edit，在 Claude 写文件前执行格式化
- B. PostToolUse hook 搭配 Write|Edit|MultiEdit，Claude 编辑后执行格式化，exit code 0
- C. 在 system prompt 加入"永远格式化你的代码"
- D. PostToolUse hook 搭配 Read，Claude 读取文件后执行格式化

<details><summary>答案</summary>

**B** — 格式化必须在文件被编辑后进行（PostToolUse）。Matcher 应涵盖所有编辑操作（Write、Edit、MultiEdit）。Exit code 0 代表"正常继续" — 不封锁。

- A 在编辑前执行 — 还没有东西可以格式化
- C 是 prompt-based，无法保证一致的格式化
- D 指向错误的工具 — Read 不修改文件

**PM 重点**："每次编辑后自动" + "不应封锁" = PostToolUse 搭配 exit code 0。这是质量增强，不是合规闸门。
</details>

### Q3：代码生成场景（S2）

团队用 Claude Code 生成 API endpoint 代码。他们希望确保所有生成的文件遵循项目命名惯例（`snake_case`）。若文件不符合惯例，生成应被封锁。你应该要求什么 hook 配置？

- A. PostToolUse hook 搭配 Write，检查命名并记录警告
- B. PreToolUse hook 搭配 Write，验证文件名并在不合规时以 exit code 2 封锁
- C. 在 CLAUDE.md 加入命名惯例示例
- D. PostToolUse hook 搭配 Write，创建后重新命名文件

<details><summary>答案</summary>

**B** — "应被封锁"代表预防，需要 PreToolUse。Hook 在 Write 操作执行前检查 tool input 中的文件名。

- A 是 PostToolUse — 文件已用错误名称写入
- C 是 prompt-based 且为概率性的
- D 是事后修补 — 比预防更复杂且更容易出错

**PM 重点**："不合规则封锁"是关键句。封锁需要 PreToolUse。若需求是"不合规则修正"，PostToolUse 才合适。
</details>
