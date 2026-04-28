# Notifications Walkthrough — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Model Context Protocol (23%) |
| Task Statements | 2.2 (MCP primitives — notifications) |
| Source | model-context-protocol-advanced-topics / 01-sampling-and-notifications / Lesson 06 |

---

## One-Liner

MCP notifications let a server emit log messages and progress updates during tool execution via the `Context` object, while the client defines logging and progress callbacks to display this information to the user.

---

## Two Types of Notifications

MCP supports two notification mechanisms, both fire-and-forget (the server does not wait for a response):

| Type | Server API | Purpose |
|------|-----------|---------|
| **Logging** | `ctx.info()`, `ctx.warning()`, `ctx.debug()`, `ctx.error()` | Emit structured log messages at different severity levels |
| **Progress** | `ctx.report_progress(current, total)` | Report task completion percentage |

---

## Server Side: Using Context for Notifications

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

Key points:
- **`Context` is the last argument** -- Tool functions automatically receive it as their last parameter
- **Logging methods** -- `ctx.info()`, `ctx.warning()`, `ctx.debug()`, `ctx.error()` correspond to standard log levels
- **Progress reporting** -- `ctx.report_progress(current, total)` where `current` is work done and `total` is the full amount
- Both are **async** calls that send messages to the client

---

## Client Side: Defining Callbacks

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

The logging callback receives `LoggingMessageNotificationParams` with a `.data` field containing the log message. The progress callback receives `progress`, `total` (optional), and `message` (optional).

---

## Wiring Callbacks to the Session

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

Critical wiring detail:
- **Logging callback** goes into `ClientSession` constructor via `logging_callback=`
- **Progress callback** goes into `call_tool()` via `progress_callback=`

These are different attachment points because logging applies to the entire session, while progress tracking is per-tool-call.

---

## Logging vs Progress: When to Use Each

| Use Case | Mechanism | Why |
|----------|-----------|-----|
| Informing user of current step | `ctx.info()` | Human-readable status message |
| Warning about degraded performance | `ctx.warning()` | Severity matters for filtering |
| Showing completion percentage | `ctx.report_progress()` | Numerical progress for UI bars |
| Debugging tool internals | `ctx.debug()` | Can be filtered out in production |
| Reporting recoverable errors | `ctx.error()` | Signals a problem without halting |

---

## CCA Exam Relevance

- Notifications are **D2 primitives** (Task 2.2). Expect questions about where each callback is attached.
- The key distinction is: `logging_callback` on `ClientSession`, `progress_callback` on `call_tool()`.
- `Context` is automatically provided as the last argument to tool functions -- you do not manually construct it.
- Notifications are **fire-and-forget** -- the server does not wait for acknowledgment.
- Logging levels (`info`, `warning`, `debug`, `error`) may appear in exam scenarios testing appropriate severity selection.

---

## Flashcards

| # | Question | Answer |
|---|----------|--------|
| 1 | How does a server tool function receive the Context object? | Automatically as its last argument -- no manual construction needed |
| 2 | Name the four logging methods available on the Context object. | `ctx.info()`, `ctx.warning()`, `ctx.debug()`, `ctx.error()` |
| 3 | What are the parameters of `ctx.report_progress()`? | `current` (work done) and `total` (total work) |
| 4 | Where is the logging callback attached? | To the `ClientSession` constructor via `logging_callback=` |
| 5 | Where is the progress callback attached? | To the `call_tool()` method via `progress_callback=` |
| 6 | Why are logging and progress callbacks attached at different points? | Logging applies session-wide; progress tracking is per-tool-call |
| 7 | Are MCP notifications synchronous or fire-and-forget? | Fire-and-forget -- the server does not wait for acknowledgment |
| 8 | What type does the logging callback receive? | `LoggingMessageNotificationParams` with a `.data` field |
