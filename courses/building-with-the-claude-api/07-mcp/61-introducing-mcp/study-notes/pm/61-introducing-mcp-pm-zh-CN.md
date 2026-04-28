# Introducing MCP — PM 视角

| 项目 | 说明 |
|------|------|
| 考试领域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.3（MCP primitives）、2.1（tool schemas）、1.2（agent loop 集成） |
| 来源 | building-with-the-claude-api / 07-mcp / Lesson 61 |

---

## 一句话总结

MCP 是 Claude 集成的"不要重造轮子"层：你的团队不用为每一个想接入的 SaaS 都去写 tool 定义、测试、持续维护，而是直接安装一个现成的 MCP 服务器，就能免费继承整个 tool 目录。

---

## 心智模型：Claude 的 App Store

把 Ch04 的 tool use 想象成教 Claude 如何使用一个你定制打造的设备；MCP 就是那个设备连上去的 **App Store**：

| 没有 MCP | 有 MCP |
|---------|--------|
| 每个集成都是定制品 | 集成可以"安装" |
| 工程团队拥有每个 tool schema | 服务提供者或社区拥有 |
| 加 GitHub 要写几十个 schema | 加 GitHub 只要装一个 server |
| 每次 API 改版都是你的维护问题 | 上游发新版本 |

"App Store"不是官方说法，但它抓住了最重要的产品真相：MCP 彻底改变了集成工作的经济学。

---

## 这节课为什么对 PM 重要

一个产品团队在评估"我们能不能做一个 AI 助手，让它回答用户关于我们 GitHub / Jira / Sentry / Notion 的问题？"历来的答案都是：

> "可以，但要花 3-6 个月工程来写和维护这些 tool 集成。"

MCP 把这个时间线大幅压缩。粗略估计：

| 集成来源 | 大概多久可以"Claude 能用" |
|---------|-------------------------|
| 为单一 SaaS 定制写 tools | 数周到数月 |
| 安装官方 MCP server | 数小时 |
| 安装社区 MCP server | 数小时（加上 due diligence） |
| 还没有 MCP server | 回到原本的时间线 |

PM 在评估任何会接触外部系统的 AI 功能时，第一个该问的问题是："这个服务有没有现成的 MCP server？"

---

## 用 PM 语言翻译 GitHub 示例

这节课用 GitHub 当主要示例。PM 应该这样内化：

> "让 Claude 能回答*任何* GitHub 问题，成本是多少？"

没有 MCP 的话，"任何 GitHub 问题"意味着你要承诺编写、测试、维护一个 tool 给用户可能提到的每个功能：repos、PRs、issues、projects、releases、actions、reviews、members、permissions、search、notifications。那是一个跨季度的项目——还轮不到 Jira 或 Slack。

有了 MCP，"任何 GitHub 问题"只要连到 GitHub MCP 服务器——tools 都已经写好了，服务提供者（或可信的社区）会维护它们。

---

## 产品应用场景

### MCP 是对的答案

| 场景 | 为什么 MCP 合适 |
|------|---------------|
| 横跨多个 SaaS 工具的 AI 助手 | N 个 install 命令换 N 个生态 |
| 来自利益相关人的长尾集成需求 | 可以增量加，不用重构架构 |
| 内部"AI 对公司数据"的 pilot | 把内部 API 包成一个 MCP server，所有 Claude 产品都能用 |
| 需要很多小动作的 agent workflow | 每个动作都是现成的 MCP tool |

### MCP 太重了

| 场景 | 改用什么 |
|------|---------|
| 对简单内部 endpoint 的一次性查询 | 直接写 tool 比装 server 快 |
| 只需要读一份静态文档 | 用 resource 或纯 context |
| 还在验证用户是否需要这个功能 | 先 hard-code，等信号明确再说 |

---

## PM 决策框架

有人提议"我们加 X 集成"时要问：

1. **厂商有没有官方 MCP server？** 先从这里开始——质量最高。
2. **有社区 MCP server 吗？** 可以用，但要做安全和维护的 due diligence。
3. **如果都没有，这个功能值得自己写吗？** 用"每周会用或涉及安全"的标准。
4. **我们真正需要厂商 API 的哪个子集？** 避免 scope creep——如果只要 3 个功能，不要装 80 个 tools。
5. **MCP server 挂掉时有什么 fallback？** MCP server 是独立 process，要规划失败场景。

---

## 隐藏的 PM 优势

Tools/prompts/resources 这三种 primitive 也是 PM 的杠杆点：

| Primitive | PM 真正买到的东西 |
|-----------|------------------|
| Tools | 助手能代替用户做的动作 |
| Prompts | 预先写好的 workflow，一键加载 |
| Resources | 助手可以读取的策展过的数据面 |

PM 可以把 MCP 采用 scope 成"装这个 server 用它的 tools，顺便把它的 prompts 开放给 power users"——同一个 server 能交付多层价值。

---

## 生态定位

PM 也该知道：

| 事实 | 产品含义 |
|------|---------|
| MCP 是开放协议 | 你没有被锁在 Anthropic；集成可以搬到其他 model host |
| 任何人都能写 server | 厂商、社区、你的内部平台团队 |
| 服务提供者常发布官方 server | 评估功能时第一站 |
| 生态成长很快 | "还没有 MCP server"这个答案的半衰期很短 |

---

## 常见 PM 错误

1. **把 MCP 当成技术细节** — 它是每一次集成的 *buy vs build* 决策。
2. **没问用户实际需要什么 tools 就装一堆 server** — tool 泛滥会膨胀 context 拖慢响应。
3. **以为 MCP 解决 auth** — 凭证管理、rate limits、权限还是你产品的问题。
4. **忘了预算 server 的更新** — MCP server 有版本，过期的版本会默默出错。
5. **把 MCP 和 tool use 搞混** — tool use 是 Claude 协议，MCP tools 还是跑在上面。你不能跳过学 tool use。

> **Key Insight**
>
> MCP 不是技术升级，而是**经济**升级。它把"让 AI 功能接触真实系统"的主要成本（编写和维护 tool 集成）交给别人承担。PM 的工作是注意到："我们该自己写这个集成吗？"的答案已经从"好几个月的工作"变成"一行 install 命令"——然后重新排优先级。

---

## CCA 考试重点

- **D2（Tool Design & MCP Integration）**：知道 MCP 是什么、谁在写 MCP servers、三种 primitives。
- **D1（Agentic Architecture）**：了解 MCP 是 agent 插入的可重复使用集成层。
- 考题常问"MCP 解决什么问题？"——答案是*编写/维护 tool 集成的负担*。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| MCP 一句话 pitch 是什么？ | 一个让你"安装"现成 tool 集成到 Claude 的协议，而不用自己写。 |
| PM 在评估新 Claude 集成时第一个该问什么？ | "这个服务有没有官方或社区的 MCP server？" |
| MCP 的三种 primitives 是什么？ | Tools、Prompts、Resources |
| MCP 取代 tool use 吗？ | 不——它是分发层，还是跑在 tool use 上面。 |
| 谁常写 MCP server？ | 服务提供者（官方）、社区维护者、或你自己的内部团队 |
| PM 采用 MCP server 时该预算什么？ | Token 成本、延迟、故障面、安全审查、版本维护 |
| MCP 是 Anthropic 专属吗？ | 不——它是开放协议，任何 model host 或 application 都能用。 |
| GitHub 示例中呈现的主要问题是什么？ | 要为单一服务的 API 编写和维护几十个定制 tools。 |
