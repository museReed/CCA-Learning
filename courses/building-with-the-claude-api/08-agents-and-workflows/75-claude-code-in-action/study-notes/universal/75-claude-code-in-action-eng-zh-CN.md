# Claude Code in Action — Engineering Deep Dive（简体中文）

| 项目 | 内容 |
|------|------|
| 考试 Domain | D3 — Claude Code Configuration (20%) |
| Task Statements | 3.1（Claude Code 配置与命令）、3.3（CLAUDE.md memory）、1.2（agentic workflow patterns） |
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 75 |

---

## 一句话总结

Claude Code 最有效的 workflow 是"context → plan → implement"：先加载相关文件，请 Claude 拟计划（明确不要写代码），再请它实现；`/init` 会产生 `CLAUDE.md` memory 文件，跨 session 保留项目 context。

---

## `/init` 命令与 CLAUDE.md

开始新项目时先跑 `/init`。这会触发 Claude Code：

1. 扫描整个代码库
2. 推断项目结构、依赖、coding style 与架构
3. 把总结写入一个特殊文件 `CLAUDE.md`

`CLAUDE.md` 在该项目之后每一场对话中自动带入作为 context，是让 agent 跨 session"记住"你项目的持续 memory。

### CLAUDE.md 的三种 scope

| Scope | 用途 | 会 commit 进 git 吗？ |
|-------|------|--------------------|
| **Project** | 整个项目团队共享 | 会 |
| **Local** | 你个人的笔记 | 不会 |
| **User** | 应用于你所有项目 | 不会（user-global） |

跑 `/init` 时可以加特殊指示，告诉 Claude 聚焦哪些区域。产生的文件通常包含 build 命令、coding guideline、项目特定的 pattern。

### `#` 快捷键添加笔记

你不用打开文件就能追加笔记到任一 `CLAUDE.md`。输入：

```
# 永远使用描述性的变量名
```

…Claude Code 会问你要加到哪个 scope（project / local / user），然后自动追加。

---

## 标准 Workflow：Context → Plan → Implement

Lesson 的核心主张：Claude Code 只有在你提供足够 context 与结构时，才能成为 effort multiplier。三步推荐流程：

### Step 1 —— 喂 context 给 Claude

在请它写任何代码之前，先找出能体现你 pattern 的现有文件，请 Claude 读。这样 agent 就有你 coding style 和现有功能的示例可参考。

```
> 读 math.py 和 document.py 这两个文件
```

### Step 2 —— 请 Claude 拟计划（明确不要写代码）

请 Claude 思考问题并写出计划。**明确告诉它先不要写代码** —— 只给方法和步骤。

```
> 请计划实现 document_path_to_markdown tool：
1. 建立一个 function：
   - 接受文件路径参数
   - 验证文件存在
   - 从扩展名判断文件类型
   - 读取文件 binary 数据
   - 利用已有的 binary_document_to_markdown function
   - 返回 markdown 字符串
2. 加上合适的 documentation
3. 向 MCP server 注册这个 tool
4. 添加 tests
```

### Step 3 —— 请 Claude 实现计划

计划谈好了，才请它实现：

```
> 实现上面的计划
```

Claude 会根据前面累积的 context 与 plan 写代码、更新相关文件、加 test、跑测试套件验证。

这个三步 pattern 呼应了考试会测的 agent 设计原则"think then act" —— 它不只是 Claude Code 的 idiom，而是一般 agent 的 best practice。

---

## 测试驱动开发 Workflow

Lesson 介绍的 TDD 变体能产出更稳健的代码：

1. **喂 context** —— 同上
2. **请 Claude 列出 test cases** —— 这个功能要哪些 test 才算验证完成？
3. **请 Claude 实现 test** —— 选最相关的那些请它写出来
4. **请 Claude 写出能通过 test 的代码** —— 它会反复迭代直到全绿

这招有效是因为：test 给了 Claude 一个具体的成功标准。不是"写一个做 X 的 function"，而是有可验证的目标（全绿的 test），agent 会持续迭代直到达成。

---

## 额外命令列表

除了 workflow，考试还要记这些命令：

| 命令 | 功能 |
|------|------|
| `/init` | 扫描代码库并产生 `CLAUDE.md` |
| `/clear` | 清空对话历史并重置 context |
| `#` | 追加笔记到 `CLAUDE.md`（会问 scope） |

这就是本 lesson 教的全部命令面。`/init`、`/clear`、`#` —— 预期会考直接记忆题。

---

## Claude Code 处理的日常任务

进入 session 后，Claude 还能处理本来要在编辑器和终端之间切换的日常开发事务：

- 把改动 stage 并 commit 到 git
- 跑测试
- 管理依赖包
- 执行临时 shell 命令

设计目标：你专注在大图景（要做什么、spec 长什么样），Claude 负责 glue work。

---

## 为什么"先计划再写代码"有效

这部分是超出来源的 WHY：

- **注意力预算** —— 先要求计划，model 的推理会集中在架构上，不是语法。之后实现时，架构和语法都会分到模型注意力。
- **错误成本** —— 计划改起来便宜，代码改起来贵。在计划阶段抓到方向错误，比重写代码便宜 10 倍。
- **人类 review** —— 计划很短，代码 diff 很长。Review 计划只要几秒，review diff 要几分钟。
- **Context 锚定** —— 对话中谈定的计划会变成 agent 生代码时回头参考的基准。

这就是为什么考试把"context → plan → implement"当成标准 agent workflow，而不是只是 Claude Code 的小技巧。

---

## 常见错误

1. **项目开始时没跑 `/init`** —— 失去持续 context，每场 session agent 都得重新学你的项目。
2. **没拟计划就开始要代码** —— 拿掉了最便宜的错误修正步骤。
3. **忘了喂 context** —— Claude 会猜你的惯例，产出跟代码库打架的代码。
4. **把 `#` 当 Markdown heading** —— 在 Claude Code 里，消息开头的 `#` 是 memory append 快捷键，不是 Markdown 格式。
5. **想跑 `/init` 却敲成 `/clear`** —— `/clear` 清当前对话；`/init` 建立项目记忆。效果相反。

> **关键洞察**
>
> 核心 workflow —— **context → plan → implement** —— 是唯一能让 Claude Code（以及一般 agent）发挥 10x 价值的 pattern。任何一步被跳过，产出质量都会显著下滑。考试可能直接问"推荐的 Claude Code workflow 是什么"或给场景问"少了哪一步"。

---

## CCA 考试重点

- **D3（Claude Code Configuration）**：直接记忆 `/init`、`/clear`、`#`、`CLAUDE.md` scope 的题目概率很高。
- **D1（Agentic Coding & Architecture）**："context → plan → implement" workflow 对应一般 agent best practice。
- 预期至少一题问 CLAUDE.md 三种 scope（project / local / user）。
- 预期有一题对比 `/init` 与 `/clear` —— 很容易搞混。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| `/init` 命令在 Claude Code 做什么？ | 扫描代码库以理解结构、依赖、风格与架构，并把总结写入 `CLAUDE.md` |
| `CLAUDE.md` 是什么？ | 自动在后续 Claude Code 对话中带入的 memory 文件，保存项目相关信息 |
| `CLAUDE.md` 的三种 scope 是什么？ | Project（共享、进 git）、Local（个人、不进 git）、User（跨所有项目） |
| `#` 命令在 Claude Code 做什么？ | 追加笔记到 `CLAUDE.md`，并询问使用 project、local 还是 user scope |
| 标准 Claude Code workflow 的三步是什么？ | 1) 读相关文件喂 context、2) 请 Claude 拟计划不写代码、3) 请 Claude 实现计划 |
| `/clear` 做什么？ | 清空当前 session 的对话历史并重置 context |
| Claude Code 的 TDD 变体 workflow 是什么？ | 喂 context → 请 Claude 头脑风暴 test cases → 实现 test → 写出能通过 test 的代码 |
| 为什么要先拟计划再实现？ | 计划修改便宜、review 快、能让 model 先专注架构再顾语法 —— 及早抓错 |
