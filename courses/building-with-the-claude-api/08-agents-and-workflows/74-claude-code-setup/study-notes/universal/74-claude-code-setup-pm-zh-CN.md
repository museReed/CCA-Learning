# Claude Code Setup — PM Perspective（简体中文）

| 项目 | 内容 |
|------|------|
| 考试 Domain | D3 — Claude Code Configuration (20%) |
| Task Statements | 3.1（Claude Code 安装与配置）、3.2（认证）、1.1（Claude Code 概览） |
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 74 |

---

## 一句话总结

Claude Code 的配置刻意设计成三步、低摩擦流程 —— 低启动能量是刻意的产品决策，决定了开发者采用率，也决定你实际上能瞄准哪些 persona。

---

## 心智模型：可安装的同事

安装 Claude Code 不太像装 app，更像聘用同事。三步对应：

| 步骤 | 招聘类比 |
|------|---------|
| 安装 Node.js | 先确认办公室有新同事需要的电源插座 |
| `npm install -g @anthropic-ai/claude-code` | 新同事自备笔记本报到（CLI 可执行文件） |
| `claude` + 账号登录 | 新同事签了聘用合同（你的 Anthropic 账号） |

花 60 秒配置完，"同事"就能跟你结对写代码。这是目前最快拿到一个真正 agent 的路径 —— 大多数 agent 产品需要多出好几倍的配置。

---

## 为什么配置摩擦很重要

配置的每一步都会流失用户。Claude Code 的三步流程已逼近理论最小值：

| 配置复杂度 | 典型产品 | Claude Code |
|-----------|---------|-------------|
| 0 步 | 网页 app —— 打开链接 | — |
| 1 步 | 浏览器扩展 —— 一次安装 | — |
| **3 步** | 带依赖的 CLI 工具 | **Claude Code** |
| 5+ 步 | 桌面 app + API key + 配置文件 | 大多数企业 agent |

Claude Code 团队的产品决策：把门槛压在"任何熟悉终端的开发者"。这句话定义了可触达受众。

---

## 产品使用场景

### 何时推荐"安装 Claude Code"

| 场景 | 为什么合适 |
|------|-----------|
| 团队已经熟悉 npm | 没有新工具要学 |
| 需要文件系统 + git + shell 访问 | 内置工具已覆盖 |
| 后续要用 MCP server 扩展 | 扩展点从第一天就存在 |
| 想要账号级计费，不用 raw key | 登录模型直接搞定 |

### 何时不该推荐 Claude Code

| 场景 | 更好的替代 |
|------|-----------|
| 非技术用户 | 用 Claude.ai 或 app 内的 chat widget |
| 严格企业环境、没有 npm | 做 web 工具或用 Claude.ai for business |
| 只用 Windows 且没 WSL | 评估 Claude.ai 或 API-based 工具 |
| 功能要 GUI 不是 CLI | 用 API 自建 UI |

---

## PM 决策框架

如果你在问"我们团队要不要采用 Claude Code？"，检查：

1. **开发者是否本来就住在终端里？** 是的话采用成本近零。
2. **每台开发机都有 npm 或 WSL 吗？** 这是硬性前提。
3. **我们需要账号认证还是已经有 API key 管理？** Claude Code 预期账号登录。
4. **第一年会需要 MCP 扩展吗？** 需要的话 Claude Code 是理想选择；不需要的话 raw API 可能更简单。
5. **配置出问题时谁负责支持？** 三步流程很少出错，但还是得有人回答"为什么 `claude` 说 command not found？"

---

## 四大内置能力（用户开箱即得）

从 PM 角度看，开发者完成安装那一刻，以下能力直接继承：

| 能力 | 业务价值 |
|------|---------|
| 文件操作 | Agent 能读写 codebase —— 能真做事，不只是聊天 |
| 终端访问 | Agent 能跑 test、linter、脚本 —— 闭合验证循环 |
| Web 访问 | Agent 能抓最新文档 —— 不用再抱怨"训练数据过期" |
| MCP server 支持 | 之后加的任何东西都能扩展 agent 而无需重新发布 |

了解这份清单很重要，因为当有人问"Claude Code 到底做什么？"时，这四点就是核心答案。

---

## 认证方式决策

Claude Code 用 **账号登录**，而非 raw API key。产品层面的影响：

| 方面 | 账号登录（Claude Code） | Raw API key |
|------|----------------------|-------------|
| 用户体验 | 一次登录，自动复用 | 复制粘贴，经常不小心 commit 进 git |
| 安全性 | Anthropic 管理 session | 用户自管 secret |
| 计费 | 绑在用户订阅上 | 绑在你的 API organization 上 |
| 合规 | 更简单 —— infra 里不放 secret | 更难 —— 要管 key rotation |
| 撤销 | 用户登出或 Anthropic 撤销 | 你手动轮换 key |

PM 推动"推荐工程师使用某个 coding agent"时，账号登录通常是赢家。但如果是"做一个背后用 Claude 的产品"，API key 才是对的模型。

---

## 常见 PM 错误

1. **以为"支持 Windows"等于任何 Windows** —— 实际只有 WSL；要提前告知 Windows 用户。
2. **把配置当 rollout 计划的附带事项** —— 就算只有三步，还是会有人卡住，文档要写。
3. **混淆 Claude Code 登录与 Anthropic API key** —— 两条不同计费路径，有不同运维模型。
4. **忽略四大内置能力** —— "文件 + 终端 + Web + MCP"是对利益相关方沟通的最低可行功能清单。
5. **没有 rollback 计划** —— 如果某人机器上 `claude` 出问题，`npm uninstall -g @anthropic-ai/claude-code` 必须写进文档作为逃生出口。

> **关键洞察**
>
> 配置摩擦是 **产品杠杆**，不是技术杂务。Claude Code 的三步安装是刻意的：把受众扩大到任何熟悉 npm 的开发者，同时保有完整 agent 功能。PM 比较 agent 平台时，"启动能量"是最重要的单一问题。

---

## CCA 考试重点

- **D3（Claude Code Configuration）**：会出安装步骤、平台支持、认证模型的题目。
- **D1（Agentic Coding & Architecture）**：要理解为什么 agent 产品要维持轻量安装路径。
- 小心 Windows/WSL 陷阱题和精确包名题。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Claude Code 需要几个配置步骤？ | 三个：装 Node.js、`npm install -g @anthropic-ai/claude-code`、跑 `claude` 并登录 |
| Claude Code 用什么认证模型？ | 通过 Anthropic 账号做账号登录，不用 raw API key |
| Claude Code 支持哪些操作系统？ | macOS、Windows（通过 WSL）、Linux |
| 配置后用户直接获得的四大能力是什么？ | 文件操作、终端访问、Web 访问、MCP server 支持 |
| 为什么配置摩擦对 PM 采用决策很重要？ | 每一步都会流失用户 —— 三步流程把受众定在"熟悉终端的开发者" |
| PM 何时"不该"推荐 Claude Code？ | 用户非技术人员、Windows 没 WSL、或需要 GUI 而非 CLI 的情境 |
| Claude Code 计费与直接用 Anthropic API 有何差异？ | Claude Code 绑在用户 Anthropic 账号订阅；API 用组织所有的 API key |
| PM 为何倾向账号登录而非 API key？ | 更好的 UX、无 secret 泄漏风险、Anthropic 管理 session、合规更容易 |
