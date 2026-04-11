# Introducing MCP — 工程深度解析

| 项目 | 说明 |
|------|------|
| 考试领域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.3（MCP primitives：tools/resources/prompts）、2.1（tool schema 设计）、1.2（agent loop 集成） |
| 来源 | building-with-the-claude-api / 07-mcp / Lesson 61 |

---

## 一句话总结

Model Context Protocol（MCP）是一层通信协议，让你可以把"别人已经写好"的 tools 直接接入 Claude，而不用自己写 schema 和实现——它把"编写工具"的负担从你的服务器转移到专门的 MCP 服务器。

---

## MCP 要解决的问题

学完 Ch04 的 tool use 之后，你会撞上下一堵墙：**工具编写的规模**。想象你要做一个 chat 界面，让用户问 Claude 关于 GitHub 的事：

> "我所有 repo 里有哪些还没合的 pull request？"

要回答这个问题，Claude 需要能调 GitHub API 的 tools。GitHub 功能面非常广——repos、pull requests、issues、projects、commits、reviews、actions。一个"完整"的 GitHub chatbot 意味着你要自己写**几十个** tools，每个都要：

1. 一份 JSON schema 描述输入
2. 一个 Python 函数实现调用
3. 测试、错误处理、auth、rate-limit 处理
4. GitHub API 改版时持续维护

这是单个开发者很难扛下的工作量，而且每集成一个新服务（Slack、Jira、Sentry、Figma...）都要从头来一遍。

---

## MCP 如何改变这个局面

MCP 把 tool **定义**和**执行**的负担，从你的 application 服务器转移到专门的 **MCP 服务器**。你不用自己写 GitHub tools，而是连到一个已经内置这些功能的 GitHub MCP 服务器：

```
┌────────────────┐                      ┌──────────────────────┐
│  你的服务器    │                      │   GitHub MCP Server  │
│  (MCP client)  │ ◀─── MCP protocol ──▶│  - list_repos        │
│                │                      │  - list_prs          │
│  Claude API    │                      │  - create_issue      │
│  integration   │                      │  - ...（更多）        │
└────────────────┘                      └──────────────────────┘
```

MCP 服务器是包在外部服务（GitHub、AWS、Jira...）外面的一层 wrapper，对外提供现成的 tools、prompts、resources。任何会讲 MCP 协议的 application 都可以接上并立即使用。

---

## MCP Server 对外提供什么

一个 MCP 服务器提供三种 primitive 类型（后面的 lessons 会深入每一种，但你现在就该认识）：

| Primitive | 用途 |
|-----------|------|
| **Tools** | Claude 可以调用的函数，用来执行动作或获取数据 |
| **Prompts** | 可重复使用的 prompt 模板，由 host application 展示 |
| **Resources** | Claude 可以读取的数据（文件、记录等） |

Lesson 61 聚焦 tools；resources 和 prompts 在 Ch07 后面的 lessons 处理。

---

## 谁来写 MCP Server？

任何人都可以写。实际上分三层：

| 作者 | 示例 |
|------|------|
| 服务提供者官方 | AWS 官方发布 MCP 服务器，内置 EC2、S3、IAM 等 tools |
| 社区 | 开源的 `sentry-mcp`、`playwright-mcp`、`firecrawl-mcp-server` 等 |
| 你自己（内部） | 针对公司内部 API 写的自定义服务器 |

共通模式：想集成服务 X 时，**先确认是否已有现成的 MCP 服务器，再决定要不要自己写 tools**。

---

## MCP 和直接 Tool Use 的区别

一个常见的误解是把 MCP 当成 tool use 的替代品。其实两者是互补的：

| 概念 | 是什么 |
|------|-------|
| **Tool use** | Claude API 协议：`tool_use` request block → `tool_result` reply block |
| **MCP** | 一个独立的协议，用来**打包和分发**工具，让别人定义和执行它们 |

使用 MCP 时，你的服务器对 Claude 仍然是在做一般的 tool use 调用。区别在于**是谁**写的和执行 tool 的实现：

| 直接 tools | MCP tools |
|-----------|-----------|
| 你自己写 schema | MCP 服务器内置 schema |
| 你自己实现函数 | MCP 服务器执行函数 |
| 你自己维护集成 | Server 作者维护 |
| 你拥有代码 | 你只是 consume server |

无论哪种方式，你的服务器都会从 Claude 收到 `tool_use` block，执行它（MCP 的话是请 MCP client 去转发），再返回 `tool_result`。Agent loop 本质没变。

---

## Mental Model：工具分发层

如果 tool use 是 Claude 的电源插头，那 MCP 就是电网。它标准化了：

- **Discovery**："这个服务器提供哪些 tools？"
- **Invocation**："用这些参数调用这个 tool"
- **Transport**：现在主要是 stdio，复杂场景会用 HTTP/WebSockets（lesson 62 细讲）

真正的好处是**组合性（composability）**。只要你有 MCP client，就能同时连 N 个不同的 MCP 服务器，把它们的 tools 拼成一个 agent——完全不用写任何 schema。

---

## 这节课在整章的位置

Lesson 61 是概念介绍，后面会动手做：

| Lesson | 重点 |
|--------|------|
| 61（本节） | 为什么需要 MCP、它解决什么问题 |
| 62 | MCP client：transport 无关性、消息类型 |
| 63 | CLI MCP 示例项目的初始化 |
| 64 | 用 Python SDK 定义 tools |
| 65 | 用 MCP inspector 调试 |

---

## 常见错误

1. **把 MCP 当成 tool use 的替代品** — MCP 是 tool use 之上的"分发层"，不是替代品。
2. **生态已有 server 还硬要自己写** — 先查 `sentry-mcp`、`playwright-mcp`、`mcp-atlassian` 等现成的。
3. **以为 MCP server 跑在你的 process 里** — 它是独立 process（通常是 subprocess），通过 transport 通信。错误模式是网络型的。
4. **以为 MCP 会帮你处理 auth** — 它不会。credentials 还是通过你的环境变量传，每个 server 都有自己的 auth 流程。
5. **误以为 MCP 是 Anthropic 专属** — 它是开放协议，任何 model provider、任何 application 都能使用。

> **Key Insight**
>
> MCP 最好的心智模型是"**工具的 package manager**"。Tool use 给了 Claude 调用函数的能力；MCP 给了整个生态一个发布这些函数的方法，让你不用每次都重写一遍。每次准备动手写 tool schema 之前，先问："有没有人已经发布 MCP 服务器了？"

---

## CCA 考试重点

- **D2（Tool Design & MCP Integration）**：MCP 的定义、三种 primitives（tools/prompts/resources）、MCP 和直接 tool use 的区别。
- **D1（Agentic Architecture）**：MCP 作为跨系统 agent 的基础构建单元。
- 题目常见框架："MCP 解决什么问题？"——答案永远是*编写和维护工具集成的负担*。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| MCP 的全称是什么？ | Model Context Protocol |
| MCP 的核心价值是什么？ | 把编写和执行 tool 定义的负担，从你的服务器转移到专门的 MCP 服务器。 |
| MCP 的三种 primitives 是什么？ | Tools、Prompts、Resources |
| 谁可以写 MCP server？ | 任何人——服务提供者常发布官方 server；社区和内部团队也会发布。 |
| MCP 是 tool use 的替代品吗？ | 不是。MCP 是互补的——tool use 是 Claude API 协议，MCP 是在它之上的分发层。 |
| 为什么有人要写 GitHub MCP server 而不是直接调用 GitHub API？ | 让每个使用者都拿到现成的 tool schemas 和实现，不用每个 app 各自重写。 |
| 从概念上 MCP server 扮演什么角色？ | 包在外部服务外面的 wrapper，打包出可重复使用的 tools、prompts、resources。 |
| 生态已有某服务的 MCP server 时该怎么办？ | 直接用它，不要自己从头写 tool 定义。 |
