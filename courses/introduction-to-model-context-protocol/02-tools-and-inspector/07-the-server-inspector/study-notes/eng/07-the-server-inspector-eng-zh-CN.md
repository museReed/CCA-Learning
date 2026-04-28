# The Server Inspector — 工程深度解析

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | T2.6 测试与调试 MCP server; T2.7 部署前验证 tool 行为 |
| Source | introduction-to-model-context-protocol / 02-tools-and-inspector / Lesson 07 |

---

## 一句话摘要

MCP Inspector 是浏览器界面的调试工具，让你无需构建完整应用程序就能交互式测试 MCP server，通过 `mcp dev` 在 localhost:6274 运行。

---

## 什么是 MCP Inspector？

MCP Inspector 是 MCP SDK 提供的开发工具，给你一个浏览器界面的 UI 来测试 MCP server。不需要为了测试 tools 是否运作而构建完整的应用程序（client、Claude 集成、用户界面），你可以用 Inspector 直接与 MCP server 交互。

```bash
# 对你的 MCP server 启动 Inspector
mcp dev mcp_server.py
```

这个命令会：

1. 以子进程启动你的 MCP server
2. 在 `http://localhost:6274` 启动 web UI
3. 自动建立 MCP 连接

> **Key Insight**
> Inspector 消除了 MCP 开发的鸡生蛋问题。你不需要可用的 client 来测试 server，也不需要可用的 server 来理解 server 提供什么。它把两端的开发解耦了。

---

## Inspector 界面

在浏览器打开 `localhost:6274` 时，你会看到 Inspector UI 的几个关键组件：

### Connect 按钮

界面顶部是 **Connect** 按钮。点击它建立 Inspector（作为 client）与你的 server 之间的 MCP 连接。连接状态指示器显示你是否已连接。

### 三个主要标签页

Inspector 把 MCP server 的能力整理到三个标签页：

| 标签页 | 显示什么 |
|--------|---------|
| **Resources** | Server 提供的数据源（文件、数据库等） |
| **Tools** | Server 提供的可执行函数 |
| **Prompts** | Server 提供的可重用 prompt 模板 |

### Tools 标签页

点击 Tools 标签页显示 server 提供的所有 tools 列表。每个 tool 条目显示：

- Tool 名称
- Tool 描述（来自 docstring）
- 输入参数及其类型和描述

你可以选择任何 tool，在输入字段输入参数值，点击 **Run Tool** 执行。

---

## 测试工作流

使用 Inspector 的标准开发工作流遵循此模式：

### 1. 写你的 Tool

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-tools")

@mcp.tool()
def calculate_total(prices: list[float], tax_rate: float = 0.1) -> float:
    """计算含税总价。

    Args:
        prices: 各品项价格列表。
        tax_rate: 税率（十进制，默认 0.1 = 10%）。
    """
    subtotal = sum(prices)
    return subtotal * (1 + tax_rate)
```

### 2. 启动 Inspector

```bash
mcp dev mcp_server.py
```

### 3. 连接并测试

1. 打开 `http://localhost:6274`
2. 点击 **Connect**
3. 切到 **Tools** 标签页
4. 选择 `calculate_total`
5. 输入测试值：`prices: [10.0, 20.0, 30.0]`、`tax_rate: 0.08`
6. 点击 **Run Tool**
7. 验证输出：`64.8`

### 4. 迭代

如果输出错误或 tool 报错，修正代码再重新测试。Inspector 维持连接，所以你可以重复测试而不需重启。

> **Key Insight**
> Inspector 中 tool 调用之间的状态是持久的。如果第一次 tool 调用创建了文件，后续 tool 调用可以读取该文件。这让你能测试多步骤工作流而不需在每次调用之间重置。

---

## 调用间的状态持久性

Inspector 最有用的功能之一是状态在同一 session 的 tool 调用之间持久存在。这对测试有副作用的 tools 至关重要：

```python
@mcp.tool()
def create_note(title: str, content: str) -> str:
    """创建新笔记。"""
    notes_db[title] = content
    return f"笔记 '{title}' 已创建"

@mcp.tool()
def read_note(title: str) -> str:
    """读取现有笔记。"""
    return notes_db.get(title, "找不到笔记")
```

在 Inspector 中，你可以：

1. 调用 `create_note(title="meeting", content="讨论 Q3 目标")`
2. 然后调用 `read_note(title="meeting")`
3. 验证它返回"讨论 Q3 目标"

这个顺序测试能力对验证协同运作的 tools 至关重要。

---

## 用 Inspector 调试

Inspector 对于调试这些常见问题特别有价值：

**Schema 问题**：如果你的 tool 输入 schema 不对（缺字段、类型错误），你会在 Tools 标签页立即看到。Inspector 显示你的 server 确切提供的 schema。

**参数描述**：你可以在 Inspector UI 中阅读参数描述来验证它们是否清楚有用——Claude 会看到同样的描述。

**错误处理**：故意发送无效输入来验证你的错误消息是有信息量的，而不只是 stack trace。

**返回值**：验证 tool 输出结构够好、信息够充分让 Claude 能解读。

---

## 在开发工作流中的定位

Inspector 在 MCP 开发工作流中的定位如下：

```
写 Tool 代码  →  用 Inspector 测试  →  修正问题  →  与 Client 集成
                        ↑                    |
                        └────────────────────┘
```

在所有 tools 通过 Inspector 测试之前，不应进入 client 集成。这节省大量调试时间，因为 Inspector 问题（schema、参数、错误）比 client 端问题容易诊断得多——在 client 端，问题可能在 client 代码、传输层或 server 中。

> **Key Insight**
> Inspector 不只是方便——它是必要的质量关卡。跳过 Inspector 测试直接进入 client 集成，就像跳过单元测试直接做集成测试。你会花更多时间调试，而非更少。

---

## CCA 考试关联性

本课涵盖 **Domain 2 (18%)** 的测试与调试：

- **`mcp dev` 命令**：知道这个命令对 MCP server 文件启动 Inspector
- **localhost:6274**：Inspector 的默认 URL
- **三个标签页**：Resources、Tools、Prompts——知道每个显示什么
- **状态持久性**：理解 tool 状态在 session 内的调用之间持久存在
- **开发工作流**：Inspector 位于写代码和 client 集成之间

---

## Flashcards

| Front | Back |
|-------|------|
| 什么命令启动 MCP Inspector？ | `mcp dev mcp_server.py` — 它启动 server 并打开浏览器界面的测试 UI。 |
| MCP Inspector 在什么 URL 运行？ | `http://localhost:6274` |
| MCP Inspector 有哪三个标签页？ | Resources（数据源）、Tools（可执行函数）和 Prompts（可重用模板）。 |
| Inspector 中 tool 调用之间的状态是否持久？ | 是的。如果一次 tool 调用创建了数据，后续调用可以在同一 session 中访问它。 |
| 为什么应在与 client 集成前先用 Inspector 测试？ | Inspector 问题（schema、参数、错误）比 client 端问题容易诊断得多，在 client 端问题可能在多个层中。 |
| 在 Inspector 的 Tools 标签页中可以验证什么？ | Tool 名称、描述、参数类型、参数描述和输入 schema——Claude 会看到完全相同的内容。 |
| 如何用 Inspector 测试错误处理？ | 故意发送无效输入，验证错误消息有信息量且有上下文，而非原始 stack trace。 |
| 标准 MCP 开发工作流是什么？ | 写 tool 代码 → 用 Inspector 测试 → 修正问题 → 与 client 集成。不要跳过 Inspector 步骤。 |
