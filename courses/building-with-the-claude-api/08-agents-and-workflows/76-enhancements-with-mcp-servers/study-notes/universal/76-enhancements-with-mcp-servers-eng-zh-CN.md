# Enhancements with MCP Servers — Engineering Deep Dive（简体中文）

| 项目 | 内容 |
|------|------|
| 考试 Domain | D3 — Claude Code Configuration (20%) / D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 3.2（Claude Code MCP 集成）、2.3（MCP primitives）、1.1（Claude Code 扩展模型） |
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 76 |

---

## 一句话总结

Claude Code 内建 MCP client，可通过 `claude mcp add [server-name] [command-to-start-server]` 注册任意 MCP server 扩展能力 —— 这是官方扩展点，也是 Claude Code 能跟随你的 workflow 成长的原因。

---

## MCP 扩展模型

Claude Code 默认工具涵盖文件操作、终端、Web 访问。其他所有东西 —— 你的数据库、内部 API、第三方 SaaS —— 都通过 MCP server 进来。架构：

```
┌────────────────────────────────────────┐
│          Claude Code (CLI)             │
│  ┌──────────────────────────────────┐  │
│  │      内置工具                     │  │
│  │  File / Bash / Web / To-do       │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │      MCP Client（内建）           │  │
│  └────────┬─────────┬──────────┬────┘  │
└───────────┼─────────┼──────────┼───────┘
            │         │          │
       ┌────▼──┐ ┌────▼──┐  ┌────▼──┐
       │Sentry │ │Jira   │  │自建   │
       │MCP    │ │MCP    │  │MCP    │
       │Server │ │Server │  │Server │
       └───────┘ └───────┘  └───────┘
```

每个 MCP server 可以提供三种 primitive：

| Primitive | 用途 | 示例 |
|-----------|------|------|
| **Tools** | 执行动作 | `document_path_to_markdown(path)` |
| **Prompts** | 可复用模板 | 一个 `/summarize` slash 命令 |
| **Resources** | 访问数据 | Fixture 文件或 DB row |

这对应到 MCP 课程已经学过的通用 MCP 控制模型：tool 由 model 控制、prompt 由 user 控制、resource 由 app 控制。

---

## `claude mcp add` 命令

注册语法就一条：

```bash
claude mcp add [server-name] [command-to-start-server]
```

### 参数

- **`server-name`** —— 你自选的简短标识符（如 `documents`）。Claude Code 内部用这个名字。
- **`command-to-start-server`** —— 启动 MCP server 进程的精确 shell 命令。Claude Code 把它 spawn 成子进程，通过 stdio 通信。

### 具体示例

如果你的文档处理 server 在项目目录下用 `uv run main.py` 启动，注册命令是：

```bash
claude mcp add documents uv run main.py
```

之后 Claude Code 每次启动会自动 spawn 这个 server 并连上。该 server 提供的 tool、prompt、resource 都会纳入 agent 可用范围。

考试重点：注册是一次性动作 —— `claude mcp add` 跑一次后，Claude Code 会记住，每次启动自动重连。

---

## 实例：文档处理

Lesson 示范的标准案例：一个自建 MCP server，提供 `document_path_to_markdown` tool，能读 PDF 和 Word 文档并返回 markdown。

流程：

1. 写好有 `document_path_to_markdown` tool 的 MCP server。
2. 注册：`claude mcp add documents uv run main.py`。
3. 在 Claude Code session 里问："把 tests/fixtures/mcp_docs.docx 文件转成 markdown"。
4. Claude Code 识别意图、挑到自定义 tool、调用、拿回 markdown 内容。

用户完全没明说 tool 名称。Claude 从 request 推断该用哪个 tool，示范 MCP tool 的 model-controlled 特性。

---

## 热门 MCP 集成（考试清单）

Lesson 明确点名以下 server —— 预期会考辨认题：

| Server | 解锁什么 |
|--------|---------|
| **sentry-mcp** | 自动发现并修复 Sentry 里记录的 bug |
| **playwright-mcp** | 给 Claude 浏览器自动化能力做测试与排错 |
| **figma-context-mcp** | 把 Figma 设计稿暴露给 Claude |
| **mcp-atlassian** | 让 Claude 访问 Confluence 和 Jira |
| **firecrawl-mcp-server** | 加上网页爬取能力 |
| **slack-mcp** | 让 Claude 在 Slack 发消息或回复特定 thread |

要记对配对 —— 例如"哪个 MCP server 能让 Claude Code 修复 monitoring 平台记录的 bug？"答案是 `sentry-mcp`。

---

## 组合多个 MCP Server

真正的威力来自组合多个 server 配合你的开发流程：

| 阶段 | MCP server | Claude 做什么 |
|-----|-----------|--------------|
| Triage | sentry-mcp | 拉生产环境错误细节 |
| Context | mcp-atlassian | 读 Jira ticket 需求 |
| Implement | （内置文件工具） | 改代码 |
| Verify | playwright-mcp | 跑浏览器测试 |
| Notify | slack-mcp | 在团队频道发完成消息 |

每个 server 加上一片垂直能力。堆起来后，Claude Code 从 coding assistant 变成横跨整个工具链的 workflow orchestrator。

这个组合 pattern —— **每个专业化 server 只做一件事，由 agent 编排** —— 正是 MCP 的架构理想，也会出现在考题里。

---

## 为什么用 MCP 而非"把更多工具写死进 Claude Code"

设计动机（超出来源的补充）：

1. **解耦** —— Anthropic 不用维护所有可能的 tool。长尾需求由生态处理。
2. **安全边界** —— 每个 MCP server 是独立进程，有自己的权限和生命周期。
3. **社区贡献** —— 任何人都能发布 MCP server；生态不靠 Anthropic 工程资源扩张。
4. **组合性** —— 堆叠多个小型 server 比一个塞 200 个工具、互抢 context window 的巨兽 agent 干净得多。

---

## 常见错误

1. **命令语法错** —— 是 `claude mcp add [name] [command]`，不是 `claude mcp install` 或 `claude add-server`。
2. **忘记 server 必须能跑** —— Claude Code 会把 MCP server spawn 成子进程，传的命令必须实际启动有效的 MCP server。
3. **把 MCP 混为一般 HTTP API** —— MCP 讲的是通过 stdio 或 SSE 的特定 protocol，不是 raw REST。
4. **以为 server 会自动安装** —— Claude Code 不会从 registry 拉 MCP server；你要先自己装好再注册。
5. **每次 session 都跑 `claude mcp add`** —— 注册会持久化，每台机器每个 server 只要做一次。

> **关键洞察**
>
> MCP 扩展点是 Claude Code 最重要的架构事实：它的强大不是靠 Anthropic 加功能，而是靠你（或社区）接上 MCP server。考试必背那句：**`claude mcp add [server-name] [command-to-start-server]`** —— 精确语法要背熟。题目常会同时考这条命令和 primitive 三元组（tool、prompt、resource）。

---

## CCA 考试重点

- **D3（Claude Code Configuration）**：直接考 `claude mcp add` 语法，以及 Claude Code 内建 MCP client 的事实。
- **D2（Tool Design & MCP Integration）**：要知道 MCP server 可提供 tool、prompt、resource 三种 primitive。
- **D1（Agentic Coding & Architecture）**：预期会出"组合多个 MCP server 成 workflow"的场景题。
- 预期会考上述生态 server 的辨认题（sentry-mcp、playwright-mcp、figma-context-mcp、mcp-atlassian、firecrawl-mcp-server、slack-mcp）。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 注册 MCP server 到 Claude Code 的命令是什么？ | `claude mcp add [server-name] [command-to-start-server]` |
| Claude Code 靠什么内建组件才能扩展 MCP？ | 一个 MCP client —— 它可连到任一你注册的 MCP server |
| MCP server 可暴露给 Claude Code 的三种 primitive 是什么？ | Tools（动作）、Prompts（模板）、Resources（数据） |
| 如何注册一个用 `uv run main.py` 启动、名叫 `documents` 的 server？ | `claude mcp add documents uv run main.py` |
| Claude Code 会自动重连注册过的 MCP server 吗？ | 会 —— 注册会持久化，每次 Claude Code 启动都会自动 spawn |
| 想让 Claude 自动从 monitoring 平台找 bug 并修，该用哪个 MCP server？ | `sentry-mcp` |
| 想给 Claude 浏览器自动化能力用哪个 MCP server？ | `playwright-mcp` |
| 想读 Jira ticket 或 Confluence 页面用哪个 MCP server？ | `mcp-atlassian` |
| 为什么 Claude Code 选 MCP 而不是把所有 tool 写死？ | MCP 解耦生态、支持社区贡献、提供进程级安全边界、维持 Claude Code 内置表面精简 |
