# Notifications 实操演练 — 工程深度解析

| 项目 | 详情 |
|------|------|
| 考试领域 | D2 — 模型上下文协议 (23%) |
| 任务说明 | 2.2 (MCP 基本要素 — 通知) |
| 来源 | model-context-protocol-advanced-topics / 01-sampling-and-notifications / 第 06 课 |

---

## 一句话摘要

MCP 通知让服务器在工具执行期间通过 `Context` 对象发送日志消息和进度更新，而客户端则定义日志和进度回调函数来向用户显示这些信息。

---

## 两种通知类型

MCP 支持两种通知机制，两者都是「发射即忘」（服务器不等待响应）：

| 类型 | 服务器 API | 用途 |
|------|-----------|------|
| **日志记录** | `ctx.info()`、`ctx.warning()`、`ctx.debug()`、`ctx.error()` | 以不同严重等级发送结构化日志消息 |
| **进度报告** | `ctx.report_progress(current, total)` | 报告任务完成百分比 |

---

## 服务器端：使用 Context 发送通知

```python
from mcp.server.fastmcp import FastMCP, Context
import asyncio

mcp = FastMCP(name="Demo Server")

@mcp.tool()
async def add(a: int, b: int, ctx: Context) -> int:
    await ctx.info("Preparing to add...")
    await ctx.report_progress(20, 100)

    await asyncio.sleep(2)

    await ctx.info("OK, adding...")
    await ctx.report_progress(80, 100)

    return a + b
```

关键重点：
- **`Context` 是最后一个参数** — 工具函数自动接收它作为最后一个参数
- **日志方法** — `ctx.info()`、`ctx.warning()`、`ctx.debug()`、`ctx.error()` 对应标准日志等级
- **进度报告** — `ctx.report_progress(current, total)`，其中 `current` 是已完成的工作量，`total` 是总量
- 两者都是**异步**调用，会将消息发送给客户端

---

## 客户端：定义回调函数

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import LoggingMessageNotificationParams

server_params = StdioServerParameters(
    command="uv",
    args=["run", "server.py"],
)

async def logging_callback(params: LoggingMessageNotificationParams):
    print(params.data)

async def print_progress_callback(
    progress: float, total: float | None, message: str | None
):
    if total is not None:
        percentage = (progress / total) * 100
        print(f"Progress: {progress}/{total} ({percentage:.1f}%)")
    else:
        print(f"Progress: {progress}")
```

日志回调接收 `LoggingMessageNotificationParams`，其 `.data` 字段包含日志消息。进度回调接收 `progress`、`total`（可选）和 `message`（可选）。

---

## 将回调连接到会话

```python
async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write, logging_callback=logging_callback
        ) as session:
            await session.initialize()

            await session.call_tool(
                name="add",
                arguments={"a": 1, "b": 3},
                progress_callback=print_progress_callback,
            )
```

关键连接细节：
- **日志回调**通过 `logging_callback=` 传入 `ClientSession` 构造函数
- **进度回调**通过 `progress_callback=` 传入 `call_tool()`

这是不同的连接点，因为日志记录适用于整个会话，而进度跟踪是针对每次工具调用的。

---

## 日志 vs 进度：何时使用哪个

| 使用场景 | 机制 | 原因 |
|---------|------|------|
| 告知用户当前步骤 | `ctx.info()` | 人类可读的状态消息 |
| 警告性能降低 | `ctx.warning()` | 严重等级对过滤很重要 |
| 显示完成百分比 | `ctx.report_progress()` | 用于 UI 进度条的数值进度 |
| 调试工具内部 | `ctx.debug()` | 可在生产环境中过滤掉 |
| 报告可恢复的错误 | `ctx.error()` | 发出问题信号但不中断 |

---

## CCA 考试相关性

- 通知是 **D2 基本要素**（任务 2.2）。预期考题会涉及每个回调的连接位置。
- 关键区别是：`logging_callback` 在 `ClientSession` 上，`progress_callback` 在 `call_tool()` 上。
- `Context` 会自动作为最后一个参数提供给工具函数——你不需要手动构建它。
- 通知是**发射即忘**——服务器不等待确认。
- 日志等级（`info`、`warning`、`debug`、`error`）可能出现在测试适当严重等级选择的考试场景中。

---

## 记忆卡

| # | 问题 | 答案 |
|---|------|------|
| 1 | 服务器工具函数如何接收 Context 对象？ | 自动作为最后一个参数——不需要手动构建 |
| 2 | Context 对象上有哪四个日志方法？ | `ctx.info()`、`ctx.warning()`、`ctx.debug()`、`ctx.error()` |
| 3 | `ctx.report_progress()` 的参数是什么？ | `current`（已完成的工作量）和 `total`（总工作量） |
| 4 | 日志回调连接在哪里？ | `ClientSession` 构造函数，通过 `logging_callback=` |
| 5 | 进度回调连接在哪里？ | `call_tool()` 方法，通过 `progress_callback=` |
| 6 | 为什么日志和进度回调连接在不同的位置？ | 日志记录适用于整个会话；进度跟踪是针对每次工具调用的 |
| 7 | MCP 通知是同步的还是发射即忘的？ | 发射即忘——服务器不等待确认 |
| 8 | 日志回调接收什么类型？ | `LoggingMessageNotificationParams`，带有 `.data` 字段 |
