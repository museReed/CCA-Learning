# Implementing a Client — PM 战略概览

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | T2.2 实现 MCP client-server 通信; T2.4 处理 tool discovery 和执行流程 |
| Source | introduction-to-model-context-protocol / 02-tools-and-inspector / Lesson 09 |

---

## 一句话摘要

MCP client 是你产品中的协调层，在用户、Claude 和外部服务之间协调——就像一位知道什么时候该问谁什么事的项目经理。

---

## Client 就是项目经理

把 MCP client 想象成协调复杂请求的项目经理：

1. **接收** — 利益相关者（用户）提交请求
2. **资源调查** — PM 检查哪些团队（MCP server）可用及提供什么服务
3. **专家咨询** — PM 把请求和可用资源呈现给决策者（Claude）
4. **委派** — 决策者说"请数据团队拉这份报告"— PM 路由请求
5. **交付** — PM 收集结果带回给决策者做最终建议
6. **响应** — 决策者为利益相关者组成精炼的答案

这六步模式是每个 MCP 驱动的产品交互的核心。

> **PM Takeaway**
> Client 是协调层，不是智能层。Claude 提供智能（决定做什么）。MCP server 提供能力（做事）。Client 连接它们。这个关注点分离是理解架构的关键。

---

## 两个核心操作

每个 MCP client 与 MCP server 只做两件事：

### "你能做什么？"（Discovery）

在任何工作开始前，client 会问每个 MCP server 它提供什么 tools。这就像 PM 与新供应商的第一次会议——"让我看看你的服务目录。"

响应是结构化的能力清单：tool 名称、描述，以及每个 tool 需要什么输入。这份目录传给 Claude 让它做出明智决策。

### "请做这件事"（Execution）

当 Claude 决定使用 tool 时，client 接受 Claude 的具体请求并发送到正确的 MCP server。这就像 PM 发送详细的工作订单给供应商："用参数 Z 对数据集 Y 执行分析 X。"

Server 做完工作返回结果，client 把结果传回 Claude 做解读。

> **PM Takeaway**
> 这两个操作——discovery 和 execution——是 client 与 MCP 做的唯一的事。如果团队中有人描述更复杂的交互，他们可能是在描述多轮同样的两个操作。

---

## 五步产品流程

从产品角度，每次用户与 MCP 驱动的 tools 交互都遵循五个步骤：

**步骤 1：发现能力** — 你的产品检查有哪些 tools 可用。这自动且对用户不可见地发生。

**步骤 2：向 Claude 呈现上下文** — 你的产品把用户的问题连同 tool 目录发送给 Claude。Claude 同时看到用户要什么和它有什么 tools 可以用。

**步骤 3：Claude 做决定** — Claude 要么直接回答（如果不需要 tools）或决定用特定输入调用特定 tool。这是"AI 判断"步骤。

**步骤 4：执行动作** — 你的产品把 Claude 的 tool 请求发送到适当的 MCP server。Server 做工作——查询数据库、获取文件、跑计算。

**步骤 5：交付答案** — 你的产品把 tool 结果送回 Claude，它为用户组成自然语言响应。

用户看不到这些复杂性。他们问问题然后得到答案。五个步骤在毫秒到秒内完成。

> **PM Takeaway**
> 步骤 3 是产品质量胜负的关键。Claude 选择正确 tool 的能力取决于 tool 描述的质量（来自 server）和用户问题的清晰度。两者都是产品设计关切。

---

## 双调用模式

一个微妙但重要的方面：每次使用 tool 的交互中，产品会对 Claude 做两次独立调用。

**第一次调用**："用户问 X。这些是可用 tools。你想怎么做？"
**Claude 响应**："我想用输入 Z 调用 tool Y。"

**第二次调用**："Tool Y 返回了这些结果。现在请回答用户的原始问题。"
**Claude 响应**："根据数据，答案是..."

这个双调用模式有产品影响：

- **延迟**：涉及 tools 时两次 API 调用意味着更长的响应时间
- **成本**：每次交互两次 Claude API 调用（对定价模型很重要）
- **质量**：第二次调用受益于具体数据，常常产生比仅第一次调用更好的响应

> **PM Takeaway**
> 估算产品的响应时间和 API 成本时，记住使用 tool 的交互需要两次 Claude API 调用。不使用 tool 的交互只需一次。你的产品中这两种类型的混合比例决定整体性能和成本。

---

## 产品团队应理解的错误场景

四种类型的失败可能发生，每种对用户端有不同影响：

1. **Tool 找不到** — Claude 请求的 tool 不存在。通常是配置问题。
2. **无效输入** — Claude 发送了错误类型的数据给 tool。通常是 tool 描述清晰度问题。
3. **Server 错误** — MCP server 或外部服务失败。基础设施问题。
4. **传输错误** — Client 和 server 之间的连接中断。网络问题。

每种需要不同的错误处理和不同的用户消息。

---

## CCA 考试关联性

本课完成 **Domain 2 (18%)**：

- Client 使用两个 SDK 类：Client（连接）和 ClientSession（通信）
- 两个核心方法：`list_tools()` 和 `call_tool()`
- 从 discovery 到最终响应的五步 agentic 流程
- 双调用模式（每次使用 tool 的交互两次 Claude API 调用）
- 错误处理：检查 `result.isError` 捕获 tool 级别失败

---

## Flashcards

| Front | Back |
|-------|------|
| 用商业语言描述 MCP client 的角色是什么？ | 它是协调层——就像一位调查可用资源、向决策者（Claude）呈现选项、路由执行请求的项目经理。 |
| MCP client 与 MCP server 只做哪两个操作？ | Discovery（问有哪些 tools 可用）和 Execution（用特定输入调用特定 tool）。 |
| MCP 产品流程的五个步骤是什么？ | 1) 发现能力, 2) 向 Claude 呈现上下文, 3) Claude 做决定, 4) 执行动作, 5) 交付答案。 |
| 为什么使用 tool 的交互需要两次 Claude API 调用？ | 第一次：Claude 收到查询和 tools，决定做什么。第二次：Claude 收到 tool 结果，组成最终响应。 |
| 双调用模式的成本影响是什么？ | 每次使用 tool 的交互花费两次 Claude API 调用而非一次，影响定价模型和使用量预估。 |
| 五步流程中哪一步决定产品质量？ | 步骤 3（Claude 的决定）——取决于 tool 描述质量和用户问题清晰度，两者都是产品设计关切。 |
| MCP client 有哪四种错误类型？ | Tool 找不到（配置）、无效输入（描述清晰度）、Server 错误（基础设施）、传输错误（网络）。 |
| 用户在五步 MCP 流程中体验到什么？ | 什么也没有。他们问问题然后得到答案。所有五步透明地在毫秒到秒内发生。 |
