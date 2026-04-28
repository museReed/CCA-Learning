# Enhancements with MCP Servers — PM Perspective（简体中文）

| 项目 | 内容 |
|------|------|
| 考试 Domain | D3 — Claude Code Configuration (20%) / D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 3.2（Claude Code MCP 集成）、2.3（MCP primitives）、1.1（Claude Code 扩展模型） |
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 76 |

---

## 一句话总结

MCP server 是 Claude Code 的"app store" —— 让 PM 能用模块化能力（Sentry、Jira、Slack、Figma、内部自定义 API）组合 agent，不用拜托 Anthropic 或工程师开发，只要一条命令：`claude mcp add`。

---

## 心智模型：Agent 的插件架构

把 Claude Code 想成插线板，MCP server 想成你插上去的电器：

| 插线板类比 | Claude Code 实际对应 |
|-----------|---------------------|
| 插线板本体 | Claude Code 与它内置的文件、shell、Web 工具 |
| 每个插座 | 一个 MCP client 连接 |
| 插上去的电器 | MCP server（sentry-mcp、playwright-mcp、内部自建 server） |
| 新增电器 | `claude mcp add [name] [command]` |

关键洞察：插线板从设计上就是要你能插任何东西。你不用把插线板寄回工厂才能加新电器。

---

## 为什么这 lesson 对 PM 重要

Lesson 75 为止，Claude Code 看起来像 coding assistant。Lesson 76 揭示它实际是什么 —— **workflow orchestration 平台**。有了 MCP server，Claude Code 能横跨你整条工具链：

| 没 MCP 之前 | 有 MCP 之后 |
|------------|------------|
| 读写代码 | 读 Jira ticket、写代码、查 Sentry、更新 Slack |
| 局限在终端 | 横跨整个 SaaS stack |
| 帮个人 | 能驱动整个团队的 workflow |

对 PM 评估 Claude Code 在组织中的定位来说，这是它从"不错的开发工具"升级为"平台决策"的关键 moment。

---

## 产品使用场景

### 何时投资 MCP server

| 场景 | 要加的 MCP server |
|------|------------------|
| 生产环境 bug triage | sentry-mcp + mcp-atlassian + slack-mcp |
| Spec-driven 功能开发 | mcp-atlassian + figma-context-mcp |
| QA 自动化 | playwright-mcp +（内部 fixture server） |
| 研究与爬虫 | firecrawl-mcp-server |
| 内部系统访问 | 为你的 API 自建 MCP server |

### 何时 MCP server 是过度工程

| 场景 | 替代方案 |
|------|---------|
| 一次性调用你 API 的脚本 | 请 Claude 写 Python 脚本跑一次 |
| 只读文档 | 用 Claude Code 内置 web fetch |
| 一个月才做一次的动作 | 手动仍比建集成便宜 |

好的判断原则：只有每周都会用或是关键安全流程，才值得建或装 MCP server。

---

## 六个生态 Server（PM 必记）

PM 要能快速回答"生态里已经有这个了吗？"的问题：

| Server | 业务用例 | 决策框架 |
|--------|---------|---------|
| **sentry-mcp** | 自动发现与修复 bug | "把 Claude 接到我们的监控平台" |
| **playwright-mcp** | 浏览器自动化做测试 | "让 Claude 跑 end-to-end 测试" |
| **figma-context-mcp** | Claude 读设计文件 | "让 Claude 实现设计稿" |
| **mcp-atlassian** | Claude 读 Jira/Confluence | "让 Claude 看 spec 和 ticket" |
| **firecrawl-mcp-server** | Claude 爬网页 | "让 Claude 做竞品研究" |
| **slack-mcp** | Claude 发 Slack 消息 | "让 Claude 跟团队沟通" |

利益相关方问"Claude 能不能做 X？"时，先查这份清单，再谈自建。

---

## PM 决策框架

团队提议"加一个 MCP server"时，问：

1. **生态里已经有了吗？** 先查上面六个加广义的 MCP ecosystem。
2. **这个 workflow 实际需要哪种 primitive？** Tool（动作）、prompt（模板）还是 resource（数据）？多半是 tool。
3. **信任边界在哪？** 每个 MCP server 是独立进程 —— 集成会触及生产环境吗？要加批准步骤。
4. **谁拥有这个 server？** 内部 server 要有 owner team。外部 server 要 pin 版本并有更新计划。
5. **Server 挂掉时的 fallback 是什么？** Claude Code 的 agent loop 会退化 —— 要预先规划。

---

## 组合故事：把 Server 叠成 Workflow

本 lesson 对 PM 最重要的概念是：你可以组合多个 MCP server 覆盖完整 workflow。示例 —— 生产环境 bug workflow：

| 步骤 | 发生什么 | 使用的 MCP server |
|-----|---------|------------------|
| 1. 新 error 进来 | 告诉 Claude："修最新的 Sentry P1" | sentry-mcp |
| 2. 读 ticket | Claude 找出关联 Jira ticket | mcp-atlassian |
| 3. 读相关代码 | Claude 用内置文件工具 | （内置） |
| 4. 实现修复 | Claude 改文件、跑 test | （内置） |
| 5. 浏览器验证 | Claude 跑 Playwright 测试 | playwright-mcp |
| 6. 通知团队 | Claude 在 Slack 贴总结 | slack-mcp |

四个 MCP server 加上 Claude Code 内置工具，就涵盖整个生产 hotfix workflow。PM 的任务是识别哪些这类 stack 对组织有价值，然后批准 rollout。

---

## 定价与运维视角

加 MCP server 有真实的运维成本。PM 要编预算：

| 成本 | 说明 |
|------|------|
| Token 成本 | 工具越多，每回合吃的 context window 越大 |
| 延迟 | 每个 MCP server 是子进程 —— 慢的 server 拖慢 agent |
| 失败面 | 任何 server 挂掉都可能在 workflow 中中断 agent |
| 安全审查 | 每个集成都是新数据路径 —— 要 review |
| 更新 | Server 有版本；过时版本会静默挂掉 |

这些都不是 deal-breaker，只是 rollout 计划要覆盖的项。

---

## 常见 PM 错误

1. **生态已有时还自建** —— 先查六个 named server。
2. **想到什么 server 都加** —— 每个都耗 context 和延迟；要 curate。
3. **没定义 owner** —— 没 owner 的内部 MCP server 会快速腐烂。
4. **忽略信任边界** —— 能发 Slack 消息的 server 也能发错消息。破坏性动作要加确认步骤。
5. **混淆 MCP server 与 API key** —— MCP 是 protocol，不是凭证。Auth 仍然是你的问题。

> **关键洞察**
>
> MCP 把 Claude Code 从开发工具变成 **workflow orchestration 平台**。`claude mcp add` 这条命令是 PM 视角中 agent 从"帮忙写代码"毕业到"驱动跨系统 workflow"的 moment。把 MCP 采用视为平台决策，不是开发者个人喜好。

---

## CCA 考试重点

- **D3（Claude Code Configuration）**：要记得 `claude mcp add` 命令和 Claude Code 内建 MCP client 的事实。
- **D2（Tool Design & MCP Integration）**：要知道三种 primitive（tool、prompt、resource）。
- **D1（Agentic Coding & Architecture）**：准备好场景题 —— 组合多个 server 成 workflow。
- 对 named server 的辨认题（sentry、playwright、figma、atlassian、firecrawl、slack）概率很高。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| PM 需要批准/文档化、用来加 MCP server 的命令是什么？ | `claude mcp add [server-name] [command-to-start-server]` |
| MCP server 可暴露的三种 primitive 是什么？ | Tools（执行动作）、Prompts（可复用模板）、Resources（访问数据） |
| 让 Claude 自动处理 monitoring 平台记录的 bug，用哪个 MCP server？ | `sentry-mcp` |
| 让 Claude 读 Jira ticket 和 Confluence 页面用哪个 MCP server？ | `mcp-atlassian` |
| 让 Claude 在团队频道发消息用哪个 MCP server？ | `slack-mcp` |
| 决定是否自建 MCP server 的 PM 判断标准？ | 集成是否每周都会用或是关键安全流程？是则建；否则延后 |
| 举一个涵盖生产 hotfix workflow 的四 server stack。 | sentry-mcp（triage）+ mcp-atlassian（ticket）+ playwright-mcp（验证）+ slack-mcp（通知），加上 Claude Code 内置工具 |
| 采用 MCP server 时 PM 要编的运维成本有哪些？ | Token 成本、延迟、失败面、安全审查、版本/更新维护 |
