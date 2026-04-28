# MCP Clients — 工程深度解析

| 项目 | 说明 |
|------|------|
| 考试领域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.3（MCP primitives 和协议）、2.4（multi-turn tool loops）、1.2（agent loop 集成） |
| 来源 | building-with-the-claude-api / 07-mcp / Lesson 62 |

---

## 一句话总结

MCP client 是你服务器里面用来讲 MCP 协议和 MCP servers 通信的通信桥——它把 transport、discovery（`ListTools`）、invocation（`CallTool`）都抽象化，让你的 app 代码对远端 tools 的使用几乎和本地函数一样。

---

## Client 的角色

Lesson 61 介绍了 MCP 的架构层面；Lesson 62 聚焦在 client 这一半。你的 application 里有一块代码负责：

1. 通过某种 transport 建立和 MCP server 的连接。
2. 问 server"你提供哪些 tools？"
3. 时机到时，把 Claude 的 tool-use 请求转给 server。
4. 把 server 的结果往上返回给你的 agent loop。

这块就是 **MCP client**。它是你自己服务器里的一个 library，不是独立服务。如果你用过 HTTP client（例如 `requests.Session`）调 REST API，MCP client 对 MCP servers 扮演的角色一模一样。

---

## Transport Agnostic 通信

MCP 的核心设计特性之一是 **transport agnostic**——client 和 server 可以用任何合理的媒介通信。目前最常见的设置：

| Transport | 使用场景 |
|-----------|---------|
| **stdio**（标准输入输出） | client 和 server 在同一台机器；server 是 subprocess |
| **HTTP** | client 和 server 在不同机器；网络可访问的 server |
| **WebSockets** | 跨网络的双向流 |
| **其他网络协议** | 定制化部署 |

重要的含义：**同样的 MCP 协议消息不管 transport 是哪种都能用**。从 stdio（本地开发）切换到 HTTP（production）不会改变 `ListToolsRequest` 或 `CallToolRequest` 的形状——只是字节的传送方式改了。

---

## 核心消息类型

MCP 定义了一套消息类型。最常用的两个（也是 Lesson 62 强调的）：

### 1. List Tools

```
Client  ──▶  ListToolsRequest   ──▶  Server
Client  ◀──  ListToolsResult    ◀──  Server
```

Client 问 server"你提供哪些 tools？"，server 回一个结构化的 tool 定义清单。每个定义包含 name、description 和 input schema——形状跟你 Claude API `tools` array 预期的完全一样，这不是巧合。

### 2. Call Tool

```
Client  ──▶  CallToolRequest   ──▶  Server
Client  ◀──  CallToolResult    ◀──  Server
```

Client 请 server 用特定参数执行某个 tool。Server 执行后返回结果。然后你的服务器把这个结果包成 `tool_result` block 送给 Claude。

这两个消息类型涵盖了 tools 的"discovery → invocation"完整循环。后面的 lessons 会介绍类似的消息给 resources 和 prompts。

---

## 完整流程示例（查 repository）

Lesson 62 走过一个具体例子：用户问"我有哪些 repositories？"。以下是完整序列：

```
┌──────┐    1 query     ┌────────────┐    2 ListToolsReq ┌─────────┐
│ User │ ─────────────▶ │ 你的服务器 │ ────────────────▶ │  MCP    │
└──────┘                │ + MCP      │ ◀────────────────│ Server  │
                        │  client    │ 3 ListToolsResult│         │
                        │            │                   │         │
                        │            │  4 messages w/    ┌─────────┐
                        │            │ ──── tools ─────▶│ Claude  │
                        │            │ ◀──── tool_use ──│  API    │
                        │            │  5 tool_use      └─────────┘
                        │            │
                        │            │  6 CallToolReq   ┌─────────┐
                        │            │ ────────────────▶│  MCP    │
                        │            │                  │ Server  │
                        │            │                  │    │    │
                        │            │                  │    ▼    │
                        │            │                  │ GitHub  │
                        │            │                  │   API   │
                        │            │                  │    │    │
                        │            │  7 CallToolResult│ ◀──┘    │
                        │            │ ◀────────────────│         │
                        │            │                  └─────────┘
                        │            │  8 tool_result   ┌─────────┐
                        │            │ ────────────────▶│ Claude  │
                        │            │ ◀── final answer ┤  API    │
                        │            │  9               └─────────┘
                        └────────────┘
                             │  10 final answer
                             ▼
                        ┌──────┐
                        │ User │
                        └──────┘
```

逐步解析：

1. **User** 提交查询给你的服务器。
2. **你的服务器**意识到需要先告诉 Claude 有哪些 tools 可用，所以向 MCP client 要。
3. **MCP client** 发 `ListToolsRequest` 给 MCP server，拿到 `ListToolsResult`。
4. 你的服务器带着用户问题 + tool list 调用 Claude。
5. Claude 返回 `tool_use` block。
6. 你的服务器把 tool use 细节交给 MCP client，client 发 `CallToolRequest` 给 MCP server。MCP server 实际去调 GitHub API。
7. GitHub 回复 → MCP server 包装结果 → `CallToolResult` 回到 MCP client。
8. 你的服务器把结果加到 message list 再调用 Claude。
9. Claude 格式化最终回答。
10. 你的服务器把回答返回给用户。

这就是 Ch04 tool use 同一个 agentic loop——区别在于 tool listing 和 tool execution 通过 MCP client 代理，而不是你自己服务器里实现。

---

## MCP Client 帮你抽象掉什么

写得好的 MCP client 会隐藏：

| 关注点 | Client 帮你处理 |
|-------|---------------|
| Transport 协商 | 根据连接配置选择 stdio、HTTP 等 |
| 消息框架 | 在 wire 上序列化/反序列化 JSON-RPC 风格消息 |
| 请求/响应关联 | 把响应配对到对应的进行中请求 |
| 错误信封 | 区分协议层错误和 tool 层错误 |
| Lifecycle | 启动/停止 server subprocess（适用时） |

你的 application 代码通常只看到 `client.list_tools()` 和 `client.call_tool(name, args)`——这些是简单的 async method，返回数据，不是一堆 JSON-RPC 管道。

---

## 为什么 Transport Agnosticism 重要

两个工程上的理由：

1. **Local dev 和 production 的一致性。** 开发时写 stdio，production 切 HTTP，agent 逻辑不用动。
2. **Process 隔离和安全性。** stdio 的 MCP server 跑在 subprocess，崩溃被隔离；HTTP 的 MCP server 跑在不同 host，blast radius 更小。你的 agent 代码根本不需要知道是哪一种。

这也解释了为什么 MCP servers 可以安全组合：每个都独立、不共享内存，protocol 处理 handshake。

---

## 常见错误

1. **把 MCP client 当成"和 Claude 讲话的那个"** — 它不是。Client 是和 MCP servers 讲话；你的 application 和 Claude API 仍然是分开通信。
2. **忘了在第一次调用 Claude 前调用 `list_tools`** — Claude 需要先拿到 tool 定义，不然它无法选 tool。
3. **以为 stdio 是玩具 transport** — 大部分真实的 MCP 集成都跑在 stdio；它是主要的本地开发路径，production 也能用。
4. **混淆 `CallToolResult` 和 `tool_result`** — `CallToolResult` 是 MCP 层的响应；`tool_result` 是你把它包成 Claude API content block 之后的产物。
5. **以为一个 tool call 会立即返回** — tool 执行可能包含外部 API 延迟（GitHub、DB 等），所以 client 默认是 async。

> **Key Insight**
>
> MCP client 把"我 agent 能调用远端 tool 吗？"变成和"我 agent 能调用本地函数吗？"一样的形状——而且不绑定任何特定 transport。把 list-tools + call-tool 这个循环掌握熟，Lesson 63-65 才会看懂。后面所有东西都是更多 primitives 跑在同样的两个模式上。

---

## CCA 考试重点

- **D2（Tool Design & MCP Integration）**：知道 MCP client 是什么、`ListTools` 和 `CallTool` 的区别、transport agnosticism 概念。
- **D1（Agentic Architecture）**：本节课的 10 步骤图是"agent + MCP"的标准流程，可能出现在情境题。
- 考试陷阱：题目会问每个消息类型*出现在流程的哪里*（client↔server、server↔Claude）。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| MCP client 的角色是什么？ | 你服务器里面的 library，用 MCP 协议和 MCP servers 讲话，处理 transport、discovery、invocation。 |
| MCP 的"transport agnostic"是什么意思？ | Client 和 server 可以用 stdio、HTTP、WebSockets 或其他 transport，同样的消息类型通用。 |
| Client 用哪个 MCP 消息类型发现可用 tools？ | `ListToolsRequest`，server 回 `ListToolsResult`。 |
| Client 用哪个 MCP 消息类型执行 tool？ | `CallToolRequest`，server 回 `CallToolResult`。 |
| 在 10 步骤流程中，MCP client 直接和 Claude 讲话吗？ | 不——是你的服务器和 Claude 讲话；MCP client 只和 MCP servers 讲话。 |
| 最常见的本地 MCP transport 是什么？ | stdio（标准输入输出）——通常 server 跑在 subprocess。 |
| `CallToolResult` 和 Claude 预期的 `tool_result` block 差在哪？ | `CallToolResult` 是 MCP 层的响应；你服务器要把它包成 `tool_result` content block 才能给下一次 Claude API call。 |
| 回答"我有哪些 repositories"这个例子要几次 round trip？ | 和 Claude 两次（初始+最终），和 MCP server 两次（list_tools + call_tool）。 |
