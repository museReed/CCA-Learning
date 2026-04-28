# Welcome to the Course — Engineering Deep Dive（简体中文）

| 项目 | 内容 |
|------|------|
| Exam Domain | D1 — Agentic Coding Fundamentals (22%) 主要；D5 — Enterprise Deployment (20%) 次要 |
| Task Statements | 1.1（对 Claude 能力的基础理解）、5.1（模型选择与部署准备） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 02 |

---

## One-Liner

这堂导览课程勾勒出完整学习路径——从 API 访问、提示工程、工具使用、RAG、MCP、Claude Code 到代理工作流——并设定先决条件：Python、Notebook 及 Anthropic API 密钥。

---

## 课程拓扑结构

课程遵循明确的依赖链。每个模块都建立在前一个模块之上：

```
API 基础 → 提示评估 → 提示工程 → 工具使用 → RAG → MCP → Claude Code / Computer Use → 工作流与代理
```

| 模块 | 你会构建什么 | CCA 考试对应 |
|------|------------|-------------|
| API 基础 | 第一次请求、多轮对话、流式传输 | D5：每个生产应用都从这里开始 |
| 提示评估 | 评估框架、测试数据集 | D1：无法衡量就无法改进 |
| 提示工程 | 清晰度、具体性、XML 结构 | D1：提示设计是核心代理技能 |
| 工具使用 | 工具 schema、多工具编排 | D2：MCP 和工具设计的基础 |
| RAG | 分块、嵌入向量、检索 | D5：企业级知识接地 |
| MCP | Server、Client、Resource、Prompt | D2：连接 Claude 与外部世界的协议 |
| Claude Code + Computer Use | 终端代理、浏览器代理 | D1/D3：代理式编码的实践 |
| 工作流与代理 | 并行化、串联、路由 | D1：代理架构模式 |

---

## 先决条件清单

在编写任何代码之前，确认以下环境就绪：

```bash
# 1. 支持 Notebook 的 Python 环境
python3 --version          # 建议 3.10+
pip install jupyter anthropic

# 2. Anthropic API 密钥
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. 验证访问
python3 -c "from anthropic import Anthropic; print(Anthropic().messages.create(model='claude-sonnet-4-5', max_tokens=50, messages=[{'role':'user','content':'ping'}]).content[0].text)"
```

上述任何一步失败，就先修好再继续。整门课程都在 Notebook 中执行，环境坏掉等于学习速度归零。

---

## 成功策略（工程视角）

| 讲师建议 | 工程解读 |
|---------|---------|
| 跟着我一起写代码 | 每段代码都自己打一遍；肌肉记忆能巩固 API 模式 |
| 加快播放速度 | 1.5x–2x 先扫概念，再暂停实现 |
| 扩展 / 修改 Notebook | 最好的学习发生在你故意把东西弄坏的时候 |
| 遇到问题就问 Claude | 用 Claude 来调试 Claude API 代码——这是元学习 |

最后一点常被低估：用 Claude 调试 Claude API 代码是一个紧密的反馈回路，完美映射了真实的代理式编码工作流。

---

## 常见错误

1. **跳过环境设置** —— 所有 API 课程中一半的"卡住"时刻都是 import 错误和缺少密钥，而非概念性问题。
2. **只看不写** —— 被动观看视频对 API 模式的记忆留存率接近零。
3. **直接跳到代理** —— 依赖链是真实存在的；没有提示工程知识就使用工具会导致脆弱的 schema。
4. **忽略提示评估** —— 讲师称之为"最重要的实践"。跳过评估的工程师写出的提示在自己机器上能用，但在生产环境中失败。

> **核心洞察**
>
> 这不是一门"看了就会"的课程——而是"边做边破"的课程。依赖链意味着每个模块会产出成品（Notebook、提示、工具 schema），作为下一个模块的输入。跳过任何一个模块等于漏掉一个依赖项，而不只是错过内容。

---

## CCA 考试相关性

- **D1（代理式编码基础）**：课程拓扑结构就是 CCA 技能地图——API → 提示 → 工具 → 代理，映射考试的预期进程。
- **D5（企业部署模式）**：先决条件（API 密钥管理、环境设置）是企业部署的第一天必备。
- 预期考试会假设你对此处列出的每个模块都有实操经验；这堂课就是整个路线图。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 这门课程的三个先决条件是什么？ | 基础 Python 知识、Notebook 环境、Anthropic API 密钥 |
| 课程模块顺序是什么？ | API 基础 → 提示评估 → 提示工程 → 工具使用 → RAG → MCP → Claude Code/Computer Use → 工作流与代理 |
| 为什么讲师强调要跟着写代码？ | 被动观看对 API 模式的记忆留存接近零；打字能建立肌肉记忆 |
| 讲师称哪个模块为"最重要的实践"？ | 提示评估——唯一能在规模化验证提示有效性的方法 |
| 课程涵盖哪两个 Anthropic 自建的代理？ | Claude Code（终端代理）和 Computer Use（浏览器代理） |
| 为什么模块顺序是依赖链？ | 每个模块的产出（Notebook、schema、提示）是下一个模块的输入 |
| 卡住时的建议策略是什么？ | 问 Claude 求助——用 Claude 调试 Claude API 代码是一个元学习回路 |
