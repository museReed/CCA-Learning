# The STDIO Transport — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.1 (MCP transport 选择), 2.3 (server 生命周期管理) |
| Source | model-context-protocol-advanced-topics / 03-transports / Lesson 11 |

---

## One-Liner

Stdio 是 MCP 的「仅限本地」transport — 就像同一栋大楼内的直拨电话，功能完整但无法对外连线。

---

![Transport Comparison](../../visuals/transport-comparison-zh-TW.svg)


## 快递类比

把 MCP transport 想成**消息的递送方式**：

- **Stdio** = 大楼内部信件系统。快速、可靠、服务齐全 — 但只在大楼内运作。
- **StreamableHTTP** = 邮局服务。可以跨城市寄送，但某些服务（如当日急件）无法提供。

作为 PM，transport 的选择直接影响**产品能支持哪些功能**。

---

## 运作方式（商业视角）

MCP client（你的 AI 应用程序）在同一台电脑上**启动 server 作为辅助程序**。它们通过直接管道沟通 — 就像两位同事互传便条。

**Handshake** — 开始工作前的三步建立连接：

| 步骤 | 发生什么 | 商业类比 |
|------|---------|---------|
| 1. Initialize Request | Client 自我介绍 | 「嗨，我是 AI 应用，我需要工具 X、Y、Z」 |
| 2. Initialize Result | Server 回应能力 | 「收到，我可以提供工具 A、B、C」 |
| 3. Initialized Notification | Client 确认 | 「太好了，开始工作吧」 |

---

## PM 为何该关心 Transport 选择

### 完整功能访问

Stdio 支持**所有四种通信模式**：

| 模式 | 商业意义 | 示例 |
|------|---------|------|
| Client 询问 server | AI 请求工具 | 「查询这位客户的订单」 |
| Server 回答 client | 工具返回结果 | 「这是订单详情」 |
| Server 询问 client | Server 需要输入 | 「我需要用户批准才能继续」 |
| Client 回答 server | Client 提供输入 | 「用户已批准退款」 |

后两种模式（server-initiated）对于 **agentic workflow** 至关重要 — server 需要请求人类批准或额外上下文。

> 💡 **Key Insight**
> 评估 MCP server 供应商时，要问：「你的 transport 支持 server-initiated request 吗？」如果不支持，human-in-the-loop 批准流程等功能就无法运作。

---

## PM 决策框架

| 问题 | 是 → Stdio | 否 → 考虑 HTTP |
|------|-----------|---------------|
| Server 在同一台机器上吗？ | 是 | 需要远程 |
| 是用于开发/测试吗？ | 是 | 大规模 Production |
| 需要所有 MCP 功能吗？ | 是 | 可以牺牲部分 |
| 一次只有一位用户？ | 是 | 需要多用户 |

### 一句话总结取舍

Stdio 给你 **100% 的 MCP 功能**，但限制你只能**本地单机部署**。

---

## 产品影响

| 场景 | Transport 影响 |
|------|---------------|
| 开发者工具（IDE plugin） | Stdio 完美 — 与 IDE 一起本地执行 |
| 有 AI 功能的 SaaS 产品 | 无法使用 Stdio — 需要远程 transport |
| 企业内部本地机器工具 | Stdio 适合桌面部署 |
| 云端托管 AI agent | 必须使用 StreamableHTTP 或类似方案 |

---

## CCA 考试重点

- **情境题**：「哪种 transport 适合本地开发工具？」→ Stdio
- **功能比较**：Stdio = 完整功能、仅限本地。以此为基准线。
- **Handshake 知识**：三步消息，按顺序。Initialize Request → Initialize Result → Initialized Notification。
- **取舍题**：Stdio 的限制在于部署范围，而非功能性。

---

## Flashcards

| Front | Back |
|-------|------|
| 用商业术语描述 Stdio transport？ | 直接的本地通信通道 — 像大楼内部信件系统。服务齐全，但完全没有远程能力 |
| Stdio 对产品施加什么限制？ | Server 必须与 client 在同一台机器上运行 — 无法远程或云端部署 |
| 为什么「server-initiated request」对 PM 很重要？ | 它支持 human-in-the-loop 批准、进度更新和 sampling 等功能 — 对 agentic workflow 至关重要 |
| MCP 连接建立的三个步骤是？ | Initialize Request → Initialize Result → Initialized Notification（三步 handshake） |
| PM 何时应该选 Stdio 而非 HTTP transport？ | 当产品在本地运行（开发工具、桌面应用）且需要完整 MCP 功能支持时 |
| Stdio 支持但 HTTP 可能不支持的功能？ | Server-initiated request（sampling、root listing）和 server-initiated notification（progress、logging） |
| Stdio 的部署限制是什么？ | 仅限单机 — 无法远程托管 server 或从中央 server 服务多位用户 |
| Stdio 在考试中与其他 transport 的关系？ | Stdio 是具备完整能力的基准线 — 其他 transport 用功能换取远程访问和可扩展性 |
