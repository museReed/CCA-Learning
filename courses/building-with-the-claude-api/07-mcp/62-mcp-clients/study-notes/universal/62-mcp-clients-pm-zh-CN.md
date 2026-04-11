# MCP Clients — PM 视角

| 项目 | 说明 |
|------|------|
| 考试领域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.3（MCP primitives 和协议）、2.4（multi-turn loops）、1.2（agent loop 集成） |
| 来源 | building-with-the-claude-api / 07-mcp / Lesson 62 |

---

## 一句话总结

MCP client 是坐在你产品服务器里面的"万用转接头"，它会对任何 MCP server 讲 MCP 协议——这块组件让你的团队从 stdio 换到 HTTP、从 local dev 换到 production，都不用重写 agent。

---

## 心智模型：游乐园的服务台

把你产品的后端想成游客服务中心，MCP client 就是柜台：

| 游乐园比喻 | 产品/MCP 对应 |
|-----------|--------------|
| 游客问有哪些游乐设施 | 用户问 AI 助手问题 |
| 服务台查询哪些设施开放 | Server 调用 `list_tools` 发现 MCP tools |
| 服务台交给游客一张票 | Server 通过 MCP client 转发 tool call |
| 游客去玩 | MCP server 执行真正的集成 |
| 服务台记录结果 | Server 把结果返给 Claude |

服务台不负责"开动设施"——它只是把游客连到设施上。这就是 MCP client 在你 agent 里扮演的角色。

---

## 这节课为什么对 PM 重要

Lesson 62 看起来很技术，但它带来三个会塑造产品的含义：

1. **集成层是可替换的。** 因为 MCP 是 transport-agnostic，你选哪个 vendor（stdio 开发、HTTP production、未来的 remote MCP）是 PM/ops 决策，不是重写。
2. **你产品的 agent loop 有明确边界。** 所有外部系统访问都流经一个可识别的组件（MCP client），所以 governance、logging、rate limits、policy 都可以集中在一处。
3. **跨 SaaS workflow 变成组合问题。** 一旦你的 client 会讲 MCP，每个新集成都是"加一个 server"，不是"加一条代码路径"。

---

## 产品应用场景

### MCP client 抽象能发挥的地方

| 场景 | Client 层为什么重要 |
|------|-------------------|
| Multi-tenant AI 助手 | 每个 tenant 可以有自己的一组 MCP server 连接，全通过同一个 client 加载 |
| 持续演进的 production infra | 本地用 stdio 开始，需要共享时切 HTTP——产品代码不用改 |
| Compliance / 审计 | 所有 tool calls 流经单一点，容易 log 和审查 |
| 新 tools 渐进 rollout | PM 可以在 client 层用 feature flag 控制 MCP servers |

### 抽象不太明显的场景

| 场景 | 会发生什么 |
|------|-----------|
| 只有一个集成的产品 | client + server 的 overhead 感觉像繁文缛节 |
| 从不需要 live actions 的产品 | 不需要 tool use，也就不需要 MCP |
| 延迟预算紧的消费产品 | 每层 MCP 都加毫秒——要仔细量 |

---

## 用 PM 语言看"10 步骤流程"

这节课画了"用户问'我有哪些 repositories？'"的详细 10 步骤图。PM 友好的摘要是：

1. 用户发问。
2. 产品服务器决定咨询 agent。
3. Server 向 MCP client 要 tool 菜单。
4. Server 把问题 + 菜单交给 Claude。
5. Claude 说"调用这个 tool"。
6. Server 通过 MCP client → MCP server → GitHub 转发调用。
7. GitHub 回复 → MCP server 包装 → MCP client 呈现。
8. Server 把结果返给 Claude。
9. Claude 格式化为用户友好的回答。
10. 用户看到答案。

对 PM 来说，重要的观察是**跳了几次**——每一跳都有成本（延迟、失败风险、log 面），roadmap 要把它算进去。MCP client 就是把这些复杂度最糟的部分从你产品代码中抽离的那个组件。

---

## PM 决策框架

审视用 MCP client 的 agent 功能时要问：

1. **我们要用哪个 transport？** stdio 适合本地 dev；HTTP 适合共享/远端 server。产品团队通常从 stdio 开始。
2. **MCP client 实例的 lifecycle 谁拥有？** 一个 global client 还是每个 request 一个？会影响并发和成本。
3. **MCP server 在调用中挂掉会怎样？** 用户看到的失败模式是你要设计的。
4. **MCP server 延迟要怎么反映到我们的 SLOs？** 慢的 MCP server 看起来就是慢的 assistant。
5. **Tool calls 的审计 log 放哪？** 放在 client 层的 middleware——不要散在各处。

---

## 成本视角

这节课的 10 步骤图有实际成本含义：

| 成本轴 | 来源 |
|-------|------|
| API tokens | 每轮都要把 `list_tools` 的所有 tool 定义送给 Claude |
| 延迟 | 两次 Claude round trip + 两次 MCP server round trip + 外部 API 时间 |
| 故障面 | Happy path 有五个 process 间边界，每个都可能失败 |
| 工程时间 | 大部分复杂度被 client library 隐藏——这是 PM 赢到的部分 |

每次 PM 提议"多加几个 MCP server"时，都该理性思考这些成本。更多 server = `list_tools` 响应里更多 tools = 每轮更多 tokens。

---

## 常见 PM 错误

1. **把 MCP client 当成"之后再说"的 infra** — 它是今天的产品决策，塑造你 agent 的演进。
2. **没问团队选了哪个 transport** — stdio vs HTTP 有 ops、成本、扩展的后果。
3. **以为 tool listing 是免费的** — 每个 tool 定义每轮都在吃 tokens。
4. **把 MCP client 和 Claude SDK 搞混** — Claude SDK 对 Claude 讲话；MCP client 对 MCP servers 讲话。
5. **忘记错误 UX** — MCP server 失败会通过你产品 UI 显现；要设计"tool 失败"的消息。

> **Key Insight**
>
> MCP client 是你产品通往外部能力的**单一门**。Agent 能在真实世界做的每件事都要经过这扇门。这让 client 成为实施产品 policy 的最佳位置——logging、rate limits、per-tenant 访问、feature flags、audit trails。把它当成平台 surface，不只是一个 library import。

---

## CCA 考试重点

- **D2（Tool Design & MCP Integration）**：知道 client 会发 `ListTools` 和 `CallTool` 消息，以及 MCP 是 transport-agnostic 的。
- **D1（Agentic Architecture）**：能追踪 10 步骤流程——特别是哪些跳点是 MCP client 经手、哪些是 Claude API 直接通信。
- 预期会有 PM 味的情境题："你要为所有 tool calls 加 audit logging——要放哪？"→ MCP client 层。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 用 PM 的话说，MCP client 是什么？ | 你服务器里面的单一门，所有外部 tool calls 都要经过它。 |
| 为什么 transport-agnosticism 是产品赢家？ | 你可以从本地 stdio 演进到网络 HTTP，不用重写 agent 逻辑。 |
| MCP client 主要用哪两种消息类型？ | `ListToolsRequest/Result`（discovery）和 `CallToolRequest/Result`（execution）。 |
| 谁和 Claude API 讲话——server、client 还是两者？ | 产品服务器和 Claude 讲话；MCP client 只和 MCP servers 讲话。 |
| 多加 MCP tools 会花你产品什么成本？ | 每轮的 tokens、延迟、审计/ops 面。 |
| PM 该把 tool use 的 policy control 放哪？ | 放在 MCP client 层——单一瓶颈点。 |
| "10 步骤流程"在演示什么？ | 单一用户问题如何变成跨用户、server、MCP client、MCP server、Claude 的协调序列。 |
| 从产品角度，MCP server uptime 谁负责？ | 写/host server 的人——但用户看到的失败模式是你要设计的。 |
