# MCP Clients — PM 战略概览


![Mcp Message Flow](../../visuals/mcp-message-flow-zh-TW.svg)

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | T2.2 实现 MCP client-server 通信; T2.4 处理 tool discovery 和执行流程 |
| Source | introduction-to-model-context-protocol / 01-mcp-basics / Lesson 04 |

---

## 一句话摘要

MCP client 就像产品内建的万能遥控器，能自动发现并操控任何兼容的智能设备（MCP server），无需针对每个设备单独编程。

---

## Client 就是万能遥控器

把你的 AI 产品想象成智能家居中枢。MCP client 就是内建在中枢里的万能遥控器。当你接上新的智能设备（MCP server）时，遥控器会自动：

1. **发现**设备能做什么（开灯、调温度、锁门）
2. **呈现选项**给用户（或在这里是给 Claude）
3. **发送指令**当用户想要完成某件事
4. **回报结果**给用户

这个遥控器的美妙之处在于，无论制造商是谁，它都能与任何兼容设备运作。不管是 Philips 灯泡还是 Nest 温控器，同一个遥控器都能操控。

> **PM Takeaway**
> 规划产品的集成能力时，MCP client 是一次性的工程投资。一旦建好，新增服务集成就变成配置任务，而非开发项目。

---

## 请求-响应之舞

MCP 通信遵循一个简单的两步之舞，映射了组织中委派工作的方式：

### 第一步："你能做什么？"（Discovery）

在你的产品能使用任何服务之前，MCP client 会问每个 MCP server："你提供什么 tools？"Server 响应一份能力菜单。

这就像新员工入职第一天——他们跟每个部门主管坐下来问："你的团队提供什么服务？你需要我提供什么信息才能办事？"

### 第二步："请做这件事"（Execution）

当 Claude 决定需要某个 tool 时，MCP client 发送具体请求："用这些输入执行这个 tool。"Server 执行并返回结果。

这就像发工作请求给那个部门："请拉出亚太区 Q3 销售报告。"部门做完工作，把报告送回来。

> **PM Takeaway**
> 先发现再执行的模式意味着你的产品能动态适应可用的服务。如果明天加了一个新的 MCP server，Claude 会自动知道它的 tools，不需要改核心产品的任何代码。

---

## 完整的用户旅程（12 步）

理解完整流程帮助 PM 识别瓶颈、错误或用户体验问题可能出现的位置：

1. **用户提问** — "我有哪些 open pull requests？"
2. **产品连接相关 MCP server** — 在这个案例中是 GitHub MCP server
3. **产品发现可用 tools** — 得知 `get_pull_requests` 等 tools 存在
4. **产品发送查询 + tools 给 Claude** — "用户想知道 PR 信息，这些是你可以用的 tools"
5. **Claude 分析并决定** — 判断 `get_pull_requests` 是正确的 tool
6. **Claude 指定 tool 调用** — "调用 `get_pull_requests`，参数 `state=open`"
7. **产品执行 tool** — 发送请求到 GitHub MCP server
8. **MCP server 返回结果** — 包含详细信息的 open PR 列表
9. **产品把结果送给 Claude** — "这是 tool 返回的内容"
10. **Claude 组成响应** — 格式化为有帮助的自然语言答案
11. **用户收到答案** — 干净、对话式的响应

两个影响产品质量的关键交接点：

- **步骤 4-6**：Claude 的 tool 选择准确度取决于好的 tool 描述
- **步骤 8-10**：Claude 的响应质量取决于结构化的 tool 输出

> **PM Takeaway**
> 这个流程中的每一步都是潜在的失败或延迟点。当用户反馈响应缓慢或不正确时，这个流程给你一个框架来识别问题出在哪——是 tool discovery、Claude 的决策、tool 执行，还是响应生成？

---

## 传输选项：部署决策

MCP client 可以通过三个通道与 MCP server 沟通。这是你的工程团队会做的部署决策：

**stdio（本地）** — 就像同事坐在你旁边。快速、简单，但只在所有东西在同一台机器上时才能用。适合开发和测试。

**HTTP（远程）** — 就像用 email 沟通。跨距离运作、可靠，但每条消息有些额外开销。适合需要远程服务的生产环境。

**WebSockets（持久）** — 就像保持电话线开着。始终连接、即时来回，但需要维护连接。适合实时、高频交互。

> **PM Takeaway**
> 传输选择影响延迟、可靠性和基础设施成本。大多数生产环境产品，HTTP 是务实的默认选择。如果你的使用场景需要 WebSockets 的实时优势，请与工程团队讨论。

---

## CCA 考试关联性

**Domain 2 (18%)** 的重点领域：

- 理解 MCP client 作为通信桥梁的角色（不是 tool 的实现者）
- 先发现再执行的两阶段流程
- 传输层无关性作为架构原则
- Agentic 工作流中的双重 Claude API 调用模式

---

## Flashcards

| Front | Back |
|-------|------|
| MCP client 简单来说做什么？ | 它发现 MCP server 有哪些 tools 并路由执行请求——就像能与任何兼容设备运作的万能遥控器。 |
| MCP 通信的两个阶段是什么？ | Discovery（问有哪些 tools）和 Execution（用特定输入调用特定 tool）。 |
| 为什么 agentic 流程需要两次 Claude 调用？ | 第一次：Claude 收到查询和 tool 选项，决定用哪个 tool。第二次：Claude 收到 tool 结果，生成最终响应。 |
| MCP 有哪三种传输选项？ | stdio（本地、快速）、HTTP（远程、可靠）和 WebSockets（持久、实时）。 |
| MCP client 如何影响集成新服务的时间？ | Client 建好后，新增服务变成配置工作（连接新 MCP server），而非开发工作（写定制化集成代码）。 |
| 12 步流程中两个关键交接点是什么？ | Tool 选择准确度（取决于好的 tool 描述）和响应质量（取决于结构化的 tool 输出）。 |
| 用商业语言描述"传输层无关性"是什么？ | 你的产品可以连接本地、远程或持久连接的 MCP server——全用同一套 client 代码，降低工程开销。 |
| MCP client 在产品架构中位于哪里？ | 在你的应用程序 server 内部，作为处理 MCP 协议通信的特定组件。它不是整个应用程序。 |
