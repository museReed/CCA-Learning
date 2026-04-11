# Anthropic Apps — Engineering Deep Dive（简体中文）

| 项目 | 内容 |
|------|------|
| 考试 Domain | D1 — Agentic Coding & Architecture (22%) |
| Task Statements | 1.1（Claude Code 概览）、1.2（agentic patterns）、1.4（Computer Use 作为 agent 案例） |
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 73 |

---

## 一句话总结

Anthropic 推出两款旗舰 agent 应用 —— Claude Code（终端编程助手）和 Computer Use（桌面交互工具集），两者都是 agentic loop 的标准参考实现：tool integration、多步执行、环境交互、自主解题。

---

## Anthropic 的应用接口

Anthropic 通过多个接口暴露 Claude，本模块聚焦在两个最能体现 agent 设计的接口：

| 接口 | 形式 | 是否 agent | 用途 |
|------|------|-----------|------|
| Claude.ai | 网页聊天 UI | 对话式、工具有限 | 消费级助手 |
| Anthropic API | HTTP endpoint | 基础原语 —— 由你来搭 agent | 开发者平台 |
| **Claude Code** | 终端 CLI | **是 —— 完整 agent** | 编程 agent |
| **Computer Use** | 桌面工具集 | **是 —— 完整 agent** | 操作 GUI 的 agent |

Claude Code 和 Computer Use 并不只是「恰好用了 Claude 的产品」，它们展示了一个良构 agent 的样子，并且直接映射到你之后要在 API 上自建的模式。

---

## 为什么这些应用算 Agent

课程把 agent 定义为同时具备四个特性的系统。Claude Code 和 Computer Use 都满足全部四项：

| 特性 | Claude Code 示例 | Computer Use 示例 |
|------|------------------|-------------------|
| **Tool integration** | 文件编辑、shell 执行、web fetch、MCP | 截图、鼠标点击、键盘输入 |
| **多步任务执行** | Plan → 读文件 → 编辑 → 测试 → commit | 打开浏览器 → 导航 → 填表 → 提交 |
| **环境交互** | 读写文件系统和 shell | 读写桌面 GUI 状态 |
| **自主解题** | 测试失败时反复 debug | 页面重载后自动重试点击 |

每一轮都会把 tool 调用结果喂回下一轮给 model，形成标准的 tool-use loop，直到达到自然停止条件（`end_turn` stop_reason，或宿主程序侧的最大轮数保险丝）。

---

## Claude Code：终端原生 Agent

Claude Code 在终端里跑成一个持久进程。主要特性：

- **接口**：CLI，而非网页聊天
- **默认内置工具**：文件读写、grep/glob、bash 执行、web fetch、to-do 规划
- **扩展点**：MCP servers（Lesson 76 会讲）
- **Context 策略**：项目级 `CLAUDE.md` memory 文件，提供持久 context
- **认证**：运行 `claude` 命令并登录 Anthropic 账号

可以把 Claude Code 理解为「人类打英文、Claude 打代码」的 IDE。Agent 负责：
1. 理解需求
2. 读足够多的代码库以形成计划
3. 编辑文件
4. 跑测试/脚本验证
5. 汇报结果

这正是我们之后要在 raw API 上自建的 loop。

---

## Computer Use：GUI 级 Agent

Computer Use 把 Claude 延伸到纯文本之外的环境。它提供的工具让 model 真正驱动桌面：

- 截图（vision 输入 → 推理）
- 把鼠标移动/点击到指定像素坐标
- 用键盘打字
- 通过 GUI 应用操作文件系统

为何重要：大多数企业软件没有干净的 API。Computer Use 让 Claude 可以跟任何 UI 交互 —— 旧桌面软件、网页 dashboard、VDI 环境 —— 把像素平面当作接口。

每次动作后 model 会收到新截图，判读后决定下一步鼠标/键盘动作。这就是多模态 tool-use loop 的具体示例。

---

## 为什么用这些作案例

对 agent 开发者来说，这两个 app 是参考实现，可回答：

- 大规模 tool schema 长什么样？（读它们暴露的 tool 定义）
- 多轮 context 怎么组织？（观察 Claude Code 的 CLAUDE.md 行为）
- 如何限制自主性又不把 agent 阉割掉？（看 permission prompt 与确认步骤）
- 边界情况哪里难？（错误恢复、context 管理、模糊状况下的 tool choice）

当你在 API 上自建，本质上就是为特定领域打造自己的 Claude Code。

---

## 常见错误

1. **把 Claude Code 当黑盒子** —— 考试预期你知道它是 *agent*，不是聊天 app，并能识别其 loop 结构。
2. **混淆 Claude.ai 和 Claude Code** —— Claude.ai 是工具有限的聊天 UI；Claude Code 是具备完整文件/shell 访问的终端 agent。
3. **以为 Computer Use 可取代 API-based agent** —— 它是一个特定工具集，不是通用模式。大多数 production agent 使用 typed tool，不用截图。
4. **忘了 MCP 扩展性** —— 默认工具只是起点，两者都可通过 MCP server 扩展。

> **关键洞察**
>
> 从考试角度看，Claude Code 与 Computer Use 不是「产品」，而是 **标准 agent 实现**，展示 agent 的四项特性（tool integration、多步执行、环境交互、自主解题）。CCA 考题常把场景描述为「这算不算 agent？」并期望你能映射到这四项特性。

---

## CCA 考试重点

- **D1（Agentic Coding & Architecture）**：熟记 agent 定义，知道 Claude Code 是 Anthropic 的参考 agent。会出「下列哪项是 agent 特性」这类题。
- **D3（Claude Code Configuration）**：Lesson 73 是 Claude Code 题组（约 20% 考题）的入口，后续 lesson 会深入 CLI 命令与 config。
- 注意题目对比 Claude.ai、API、Claude Code 的差异 —— 要分清哪个是聊天、哪个是原语、哪个是 agent。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 本 lesson 强调哪两个 Anthropic app 是 agent 参考实现？ | Claude Code 和 Computer Use |
| Agent 的四项特性是什么？ | Tool integration、多步执行、环境交互、自主解题 |
| Claude Code 跑在哪个接口？ | 终端 / 命令行 —— CLI agent |
| Computer Use 让 Claude 交互的对象是什么？ | 完整桌面环境（通过截图、鼠标、键盘） |
| 为什么用这两个 app 作为案例？ | 它们展示了让 agent 在真实场景中有效运行的关键原则 |
| Claude Code 与 Claude.ai 有何区别？ | Claude.ai 是工具有限的聊天 UI；Claude Code 是具备文件/shell 访问和 MCP 扩展能力的终端 agent |
| 为什么 Computer Use 对企业用例有价值？ | 它能驱动没有开放 API 的应用，直接用 GUI 交互 |
| Claude Code 与 MCP 的关系？ | Claude Code 内建 MCP client，可通过自定义 MCP server 扩展工具集 |
