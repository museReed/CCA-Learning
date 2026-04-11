# Implementing a Client — PM Perspective（简体中文）

| 项目 | 说明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（MCP primitives：client/server 集成）、1.2（agentic loop）、2.2（content block types） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 66 |

---

## One-Liner

MCP client 就像"万能旅行转接头"，让任何 Claude 产品都能插入任意 MCP server。做一个 client，生态里所有的 MCP server 立刻都变成你可用的功能——tool 集成从"工程定制"变成"配置即用"。

---

## 心智模型：旅行万能转接头

想象你的产品是一台笔记本，世界各地的 MCP server 是不同墙上的插座。没有转接头时，每次出国（每次集成）都要带一根新的电源线。**MCP client 就是那个万能转接头**：做一次，可以插进任何 MCP server，充电方式完全一样。

- 你的产品 = Claude 应用
- MCP server = 一包能力（读文档、查 CRM、发邮件）
- MCP client = 标准接口，让产品能跟任何 server 对话

关键是：client **不会因集成不同而定制**。不管要接哪个 MCP server，client 的代码形状都一样。

---

## 为什么 PM 要关心

MCP 之前，"加一个 tool"意味着工程 ticket：写 schema、写 dispatcher、测试、上线。每次集成都费时间。MCP 之后，加一个 tool 可以只是"指向新的 server"。

| 没有 MCP | 有 MCP Client |
|---------|---------------|
| 每个集成都是定制代码 | 集成是可插拔的 server |
| Tool schema 写在你的应用里 | Schema 写在 server，动态发现 |
| 资源清理与生命周期自己管 | 藏在 client wrapper 里 |
| 难以跨产品复用 | 任何兼容 MCP 的应用都能复用 |

对产品管理层而言，这是 **time-to-value 杠杆**：工程团队做一次 client，之后每个新能力都可以是 server 项目（甚至由其他团队 / 社区完成）。

---

## Client 到底在做什么（不讲代码）

Client 只有两个工作：

1. **问 server："你能做什么？"** — tool 发现。Server 返回一份 tool 菜单（名字、描述、输入）。你的应用把菜单转给 Claude，让它知道自己的选项。
2. **被要求时执行 tool** — 当 Claude 说"我要调用 `read_doc_contents` 并带这个 doc ID"，client 把请求转给 server，再把答案送回来。

其他事情——启动、清理、消息 framing、subprocess 生命周期——全藏在 client 里。产品团队看不到。

---

## 产品场景

### 值得投入做 MCP Client 的场景

| 场景 | 为什么划算 |
|------|-----------|
| 预期未来集成很多 tool | 一个 client，无限 server |
| 公司内多个团队各自做 tool | 每个团队独立上线 server |
| 想用社区 / 开源的 tool 集成 | MCP 是标准，即插即用 |
| 有多个 Claude 应用 | 共用同一批 server |

### 不需要做 Client 的场景

| 场景 | 更简单的替代 |
|------|-------------|
| 单一产品，只有两三个硬编码 tool | 直接用本地 Python function 即可 |
| 一次性 prototype | inline tool 更快 |
| 禁止 spawn subprocess 的安全环境 | 把 tool 内嵌进应用 |

---

## PM 决策框架

决定是否做 MCP client 前问自己：

| 问题 | 若 Yes | 意义 |
|------|--------|------|
| 未来半年要集成至少 3 个不同 tool 面？ | Yes | MCP client 划算 |
| 希望其他团队能独立上线能力、不动我的代码库？ | Yes | MCP client 是理想选择 |
| 已经有现成 MCP server 能接我要的系统？ | Yes | 做 client 等于免费解锁 |
| 产品跑在不能 spawn subprocess 的环境？ | Yes | 重新评估，本地 tool 也许更安全 |

---

## 可靠性、延迟、可观测性

用了 MCP client 会新增一个失败面：server 启动失败、handshake 失败、tool call 超时。PM 要预算：

- **启动检查** — server subprocess 起不来时要优雅降级（如隐藏依赖 tool 的功能）
- **每个 tool 的错误处理** — 每个 `call_tool` 都可能失败，要设计"数据源暂时不可用"的 UX
- **Logging 与审计** — 每个 tool call 都可能有副作用，要记录 name、arguments、result
- **延迟** — 第一次调用含 handshake 与 `list_tools` round trip，后续更快但仍受网络影响

这些都要写进上线清单。

---

## PM 常见错误

1. **把 client 当"下水道工程"** — 其实它是可观测性、可靠性、安全的咽喉点，要好好投入
2. **期待零集成成本** — MCP 让集成便宜很多但不是免费，你仍要决定信任哪些 server、怎么鉴权、怎么处理错误
3. **忽略 tool 发现 UX** — `list_tools` 一多就是几十个 tool，要有策略决定哪些暴露给哪些用户
4. **忽视 subprocess 安全** — spawn MCP server 就是在跑代码。如果代码来自第三方，要当依赖处理（sandbox、pin 版本、code review）
5. **重写 SDK 已有的 client** — 薄封装是为了易用，不是为了改 transport

> **Key Insight**
>
> MCP client 是 MCP 最小的一块，却是决定你的产品能否参与生态的那一块。做了，世界上所有 MCP server 都是你潜在的功能；不做，每个集成都要手写。对 PM 而言，"是否投资 MCP"真正的意思是："你希望产品 roadmap 靠社区复利增长，还是只能随自己写代码的速度线性增长？"

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：要知道 `list_tools` 和 `call_tool` 是 client 与 server 的最小契约
- **D1（Agentic Architecture）**：agent loop 不变——MCP 是 dispatch 替换，不是新范式
- 考题模式："应用要用 MCP server，client 必须暴露哪两个方法？" → `list_tools()` 与 `call_tool()`

---

## Flashcards

| Front | Back |
|-------|------|
| MCP client 的"万能转接头"比喻？ | Client 是通用转接头，让产品插进任何 MCP server，不必每个集成都定制布线 |
| MCP client 做哪两件事？ | 1）发现 server 提供的 tool、2）代表 Claude 执行 tool |
| 什么时候不值得做 MCP client？ | 只有几个硬编码 tool、一次性 prototype、或禁止 spawn subprocess 的环境 |
| MCP 带来什么隐藏风险？ | 运行第三方 server 代码——要当依赖处理，做 code review、sandbox、pin 版本 |
| MCP 驱动功能的 PRD 要包含什么？ | 启动与错误处理、tool 发现 UX、每次调用的 log、server down 的 fallback、延迟预算 |
| 为什么 MCP 是 PM 的"time-to-value 杠杆"？ | Client 做完后，每个新集成可以是别人写的 server，roadmap 可复利 |
| MCP 改变了 Claude 处理 tool call 的方式吗？ | 没有，agent loop 完全一样，MCP 只改变了 tool 代码放哪、怎么被调用 |
| Client 最小契约是什么？ | `list_tools()` 做发现、`call_tool(name, input)` 做执行 |
