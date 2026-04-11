# Project Setup — 工程深度解析

| 项目 | 说明 |
|------|------|
| 考试领域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.3（MCP primitives）、1.2（agent loop 集成）、2.1（tool schemas） |
| 来源 | building-with-the-claude-api / 07-mcp / Lesson 63 |

---

## 一句话总结

Lesson 63 把动手做的 MCP 项目搭起来——一个 CLI chatbot，同一个 codebase 里有自定义的 MCP client 和自定义的 MCP server，并确立后续 lesson 64、65 会延伸的目录结构、环境变量和"hello world" baseline。

---

## 我们要做什么

这个项目是一个 command-line chatbot，让用户通过 Claude 和一组内存里的文档交互。它有两个主要组件，会在 Ch07 后面的 lessons 渐进实现：

| 组件 | 用途 |
|------|------|
| **MCP client** | 处理用户 chat loop，并转发 tool use requests |
| **自定义 MCP server** | 管理文档操作（读取和更新） |

MCP server 会对外提供两个必要的 tools（lesson 64 会细讲）：

1. 一个**读取** tool，返回某份文档的内容。
2. 一个**更新** tool，用 find-and-replace 修改文档。

文档存在一个普通的 Python dict 里——没有数据库——让焦点放在 MCP 机制本身，而不是 persistence 的管道。

---

## 重要的架构备注

这节课明确点出一个设计警告：**真实世界的项目通常只会实现 MCP client 或 MCP server 的其中一边，不会两边都做**。常见模式：

| 角色 | 示例 |
|------|------|
| MCP server 作者 | 你把内部服务的功能开放给其他开发者 |
| MCP client 作者 | 你做一个 app 连到现成的 MCP servers（如 GitHub、Sentry） |

这门课在同一个 repo 两边都做**只是为了教学**——这样你不用切 codebase 就能看到协议两端如何对话。不要误以为这是 production 推荐做法。

---

## 项目结构

解压缩 lesson 附的 `cli_project.zip` 之后，你至少会看到：

| 文件 | 角色 |
|------|------|
| `main.py` | 进入点，跑 CLI chat loop |
| `mcp_client.py` | MCP client 实现（后面会填） |
| `mcp_server.py` | 自定义 MCP server（后面会填） |
| `.env` | 环境变量文件——放 `ANTHROPIC_API_KEY` |
| `README.md` | 逐步的设置说明 |

`.env` 是关键：没有 Anthropic API key，chatbot 根本无法调用 Claude。不管是 `uv` 还是纯 `pip` 路径，都预期第一次跑之前 key 已经就位。

---

## 安装依赖

README 记录了两条支持的安装路径：

### 方式 1 — UV（推荐）

```bash
# 在项目目录
uv run main.py
```

`uv` 是 Astral 出的 Python package manager（跟 ruff 同作者），把 venv 管理和 dependency 安装包成一个命令。如果项目有 `pyproject.toml` 或 `uv.lock`，`uv run` 会在执行前自动解析和安装依赖。

### 方式 2 — 标准 Python + pip

```bash
# 创建并激活 venv，然后
pip install -r requirements.txt
python main.py
```

任何一条路最后都会得到：

- `anthropic` SDK 装好
- `mcp`（Python MCP SDK）装好
- 一个能跑 `main.py` 的 Python interpreter

---

## "Hello World" Baseline

开始实现任何 MCP 功能前，这门课要求你先用一个小问题验证 baseline：

```
> what's 1+1?
```

你应该很快得到 Claude 的回应。这个 sanity check 确认三件事：

1. `.env` 被 `main.py` 读到了。
2. 你的 API key 有效（不是 401）。
3. Claude SDK 正确安装，可以调用。

如果这里失败，就不要继续往 lesson 64-65 推进——MCP 只会在已经坏掉的设置上加更多移动零件。

---

## 为什么这节课重要

一个能跑的 baseline 是后续所有有意义调试的前提。Lesson 65 的 MCP inspector 和 lesson 64 的 tool 实现都假设你已经能从 `main.py` 打到 Claude。这节课很短，因为它的任务不是教概念——它是在为接下来整章排除环境借口。

具体来说，Lesson 63 建立了：

| 设置项目 | 后面哪些 lessons 会用到 |
|---------|-----------------------|
| 有 `ANTHROPIC_API_KEY` 的 `.env` | 从这里开始每一课 |
| 可运作的 `main.py` CLI | 64、65、66、68、70 |
| 装好的 `mcp` Python SDK | 64（`FastMCP`）、65（`mcp dev`） |
| 装好的 `anthropic` Python SDK | 每次调用 Claude |

---

## Python MCP SDK 技术栈

Lesson 63 还没写任何 MCP 代码，但已经装了你下一步要用的 runtime。后面 lessons 会用到的两个相关 import：

```python
from mcp.server.fastmcp import FastMCP   # lesson 64
from anthropic import Anthropic          # 每一课
```

`FastMCP` 是高阶的 server builder（decorator + type hints）；`mcp` 包也附了 client API 和 CLI inspector（`mcp dev`，lesson 65 会用）。

---

## 常见错误

1. **跳过 baseline 测试。** 如果 `what's 1+1?` 都不行，停下来修设置——不要在上面堆 MCP。
2. **忘了 `.env`。** Anthropic SDK 是从环境变量读 `ANTHROPIC_API_KEY`；少了 key 会在调用时才报错，不是 import 时。
3. **用 global Python interpreter。** `uv` 和 venv 都会隔离依赖；global 安装容易和 `mcp` 包版本冲突。
4. **以为 production 也要两边都做。** 重读"重要的架构备注"——真实项目通常只做一边。
5. **忽略 README。** README 带着精确的设置步骤；Anthropic 的课程项目和它高度耦合。

> **Key Insight**
>
> 这节课的真正重点是**消除设置上的模糊**。MCP 带进来比纯 tool use 更多的移动零件（subprocesses、transports、SDK 版本）。之后要调试这些的唯一办法，是从一个已知正常的 baseline 开始。让 `what's 1+1?` 跑起来是 5 分钟的投资，接下来四节课都在赚回来。

---

## CCA 考试重点

- **D2（Tool Design & MCP Integration）**："CLI chatbot + 内存文档 + 读/写 tools"是 MCP 入门的经典示例——考试情境题可能会呼应它。
- **D1（Agentic Architecture）**：了解 `main.py` 是 host、`mcp_client.py` 是 client、`mcp_server.py` 是 server——这个三位组合会在后面题目反复出现。
- 要记得"client 和 server 两边都做"是教学选择，不是 production 推荐。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Ch07 的示范项目是什么？ | 一个 CLI chatbot，用 MCP client 加上自定义 MCP server 来读取和更新内存里的文档集合。 |
| 自定义 MCP server 会对外提供哪两个 tools？ | 一个读取文档的 tool 和一个编辑文档（find and replace）的 tool。 |
| 为什么这门课在同一个 repo 里做 client 和 server？ | 纯粹为了教学，让你在同一个 codebase 看到 MCP 协议的两边。 |
| 真实世界的做法通常长怎样？ | 只做 client 或 server 其中一边——不会两边都做——把服务开放给别人或消费现成的 servers。 |
| 第一次跑之前要在 `.env` 加什么？ | `ANTHROPIC_API_KEY` |
| 推荐用哪个 Python 工具跑这个项目？ | `uv run main.py` |
| 设置完的 baseline sanity check 是什么？ | 问 chatbot `what's 1+1?` 并确认 Claude 有回答。 |
| starter 项目有哪些文件？ | `main.py`、`mcp_client.py`、`mcp_server.py`、`.env`、和一份 README。 |
