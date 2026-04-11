# Project Setup — PM 视角

| 项目 | 说明 |
|------|------|
| 考试领域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.3（MCP primitives）、1.2（agent loop 集成）、2.1（tool schemas） |
| 来源 | building-with-the-claude-api / 07-mcp / Lesson 63 |

---

## 一句话总结

Lesson 63 是"环境就绪"检查点：在团队写任何 MCP 代码之前，先验证 baseline CLI chatbot 能和 Claude 讲话——因为后面每一个 MCP 功能都是叠在这个 baseline 上面。

---

## 心智模型：IKEA 组装前的检查页

把这节课想成 IKEA 说明书的第一页："打开箱子、把零件排出来、确认每项都在"。你还没组任何东西，你只是在确认自己**可以**组装。

| IKEA 步骤 | MCP 项目步骤 |
|----------|-------------|
| 开箱把零件排出来 | 解压 `cli_project.zip` |
| 核对零件清单 | 确认 `main.py`、`mcp_client.py`、`mcp_server.py` 都在 |
| 检查工具 | 装好 `uv` 或 `pip` + venv |
| 检查接头 | 在 `.env` 加上 `ANTHROPIC_API_KEY` |
| 试锁一颗螺丝 | 问 bot `what's 1+1?` |

跳过 IKEA 检查页的结果是书架晃。跳过 Lesson 63 的结果是你之后抓 MCP bug 时，发现那些 bug 根本是设置问题伪装的——而这类 bug 最吃工程时间。

---

## 为什么这节课对 PM 重要

PM 可能会想"为什么要花一节课做'装起来'？"。三个理由：

1. **环境是 AI 功能阵亡的地方。**"demo 没事"→"prod 出问题"通常是环境问题，不是代码问题。MCP 在一般的 Claude API 使用上面再多叠 subprocesses 和 SDK 版本。
2. **项目形状 = 你的功能形状。** 这节课的 CLI chatbot 就是最小可行的参考架构：host + client + server + env file。PM 只要把这个三位组合内化，就能对未来任何 MCP 功能做 reasoning。
3. **定义 bootstrap 阶段的 "done"。** 这节课给团队一个清楚的 initial setup 验收标准：`what's 1+1?` 有回答就算。这就少了一次"到底通了没？"的模糊对话。

---

## 产品相关的架构提醒

这节课明确指出真实项目通常只做 MCP client **或** MCP server 的其中一边，不会两边都做：

| 团队意图 | 做哪边 |
|---------|-------|
| "我们要做一个 Claude 驱动的聊天，处理我们的内部数据" | MCP client + 现有 server |
| "我们要把我们的 SaaS 开放给市场上所有 AI agent" | MCP server 给别人用 |
| "我们在做平台层" | 可能两边都做，但应该在不同 repo |

从 PM 角度这是一个**一次下定、长期遵守的 scoping 决策**：

- MCP server 作者 = 你在把数据/动作产品化给 agents。
- MCP client 作者 = 你在把 AI 体验产品化给用户。

这门课把两边做在同一个 repo 纯粹是为了教学——别让它模糊你产品的 scope。

---

## 示范项目的产品应用

这节课的 CLI chatbot 是玩具，但形状可以直接用：

| 实际产品 | 形状怎么对应 |
|---------|-------------|
| 内部文档助手 | 内存 docs → 真实 knowledge base；CLI → 网页 UI |
| 会改 config 的开发者工具 CLI | find-and-replace tool → 模板化 config 修改 |
| Ops runbook 助手 | read + update tools → runbook 读取和修改 |
| 合规审查机器人 | read tool → 读政策文档；update tool → 提议红字修改 |

只要 PM 在评估的 AI 功能是"读+写小块有限数据集"，都能把这个项目当作可动的模板。

---

## PM 决策框架

在团队带着真实产品场景进入这节课前要问：

1. **我们产品是哪一边？** Client（消费 server）、server（发布 tools）、还是少见的两边都做？
2. **Prod 的 secret 放哪？** `.env` 开发用没问题；production 要用 secret manager。
3. **我们的最小可行数据集是什么？** 在 demo 里是 dict。在 prod 是你能安全让 Claude 读写的东西。
4. **CLI 和 UI 层谁拥有？** 这节课用 CLI；你产品会有真的前端。计划好转换。
5. **"setup works"的验收标准？** 抄这节课的做法——定义一个小小的可测试 smoke check。

---

## 运营和成本笔记

就算是空白 project 也有成本含义：

| 项目 | PM 为什么该在意 |
|------|---------------|
| API key | `what's 1+1?` 一跑就开始计费 |
| `uv` vs `pip` | 影响 CI 时间和 onboarding 速度 |
| `.env` 政策 | Secret 外泄风险——第一天就 gitignore |
| Starter code vs completed code | Anthropic 提供 `cli_project.zip` 和 `cli_project_COMPLETE.zip`，选一份当参考 |

---

## 常见 PM 错误

1. **把 Lesson 63 当成可以跳** — baseline 坏掉会让后面每一课都更难 debug。
2. **以为 CLI 就是最终 UX** — 它是课程产物；你的产品需要真 UI。
3. **模糊 client/server 的所有权** — 不要只因为课程这样做就把"两边都做"塞到同一个 service。
4. **API key 永远住在 `.env`** — 上线前要规划搬到 secret manager。
5. **没定义 smoke test** — 抄 `1+1?` 的模式，缩放到你自己产品真实的数据路径。

> **Key Insight**
>
> 这节课看起来像 DevOps 管道，但它偷偷塞给 PM 一个很有价值的成品：一个**最小可行的 MCP 架构**（host + client + server + env + baseline check）。任何你要 scope 的真实产品，都可以视为这个形状的专门化。把这个形状记住，它到处都在重复出现。

---

## CCA 考试重点

- **D2（Tool Design & MCP Integration）**：知道 Ch07 的工作示例是一个 CLI chatbot，对内存文档做 read 和 update tools。
- **D1（Agentic Architecture）**：认识 host/client/server 三位组合是 MCP 的标准排版。
- 预期会有情境题问：给定产品目标，团队该做 client 还是 server？

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Lesson 63 实际在教什么？ | 如何 bootstrap Ch07 项目，让 chatbot 在任何 MCP 代码写出来之前就能和 Claude 讲话。 |
| Baseline smoke test 是什么？ | 问 bot `what's 1+1?` 并确认 Claude 有回答。 |
| Production 时团队该同时做 MCP client 和 server 吗？ | 通常只做一边——课程是为了教学才两边做。 |
| Demo 把 document 存在哪？ | 内存 Python dict——没有数据库。 |
| README 支持哪两条安装路径？ | `uv run main.py`（推荐）和标准 Python + pip + `python main.py`。 |
| 第一次跑之前必备的 secret 是什么？ | `.env` 里的 `ANTHROPIC_API_KEY` |
| "client 或 server，不是两边"的备注 PM 要带走什么？ | 你产品通常只挑一个角色；混用是 scoping 出问题的征兆。 |
| 这节课给 PM 什么具体成品？ | 一个可重用的 MCP 最小可行架构模板：host + client + server + env + baseline check。 |
