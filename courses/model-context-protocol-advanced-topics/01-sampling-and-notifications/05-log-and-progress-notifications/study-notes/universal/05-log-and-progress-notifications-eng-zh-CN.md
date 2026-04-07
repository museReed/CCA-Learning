# Log and Progress Notifications — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server capabilities), 2.5 (server-to-client communication) |
| Source | model-context-protocol-advanced-topics / 01-sampling-and-notifications / Lesson 05 |

---

## One-Liner

MCP server 使用 `ctx.info()` 记录日志、`ctx.report_progress()` 汇报进度，在长时间操作中通过单向 notification 实时反馈给 client。

---

## 两种 Notification 机制

MCP 提供两种方式让 server 实时推送信息给 client：

| 机制 | 方法 | 用途 | 方向 |
|------|------|------|------|
| Logging | `ctx.info()`, `ctx.debug()`, `ctx.warning()`, `ctx.error()` | 状态消息、调试信息 | Server -> Client（fire-and-forget） |
| Progress | `ctx.report_progress(current, total)` | 完成百分比 | Server -> Client（fire-and-forget） |

两者都是 **notification**，不是 request — server 不等待响应。

---

## Logging：Server 端实现

Context 对象提供标准 log level 方法：

```python
@mcp.tool()
async def analyze_data(ctx: Context, dataset_url: str) -> str:
    ctx.info("Starting data analysis...")

    ctx.debug(f"Fetching dataset from {dataset_url}")
    data = await fetch_dataset(dataset_url)

    ctx.info(f"Loaded {len(data)} records")

    if len(data) > 100000:
        ctx.warning("Large dataset detected — analysis may take longer")

    try:
        result = process(data)
    except Exception as e:
        ctx.error(f"Analysis failed: {e}")
        raise

    ctx.info("Analysis complete")
    return result
```

Log level 遵循标准惯例：`debug` < `info` < `warning` < `error`。

---

## Progress：Server 端实现

在循环中使用 `report_progress()` 显示完成度：

```python
@mcp.tool()
async def batch_process(ctx: Context, items: list[str]) -> str:
    total = len(items)
    results = []

    for i, item in enumerate(items):
        ctx.report_progress(i, total)
        result = await process_item(item)
        results.append(result)

    # 标示完成
    ctx.report_progress(total, total)

    return format_results(results)
```

要点：
- `current` 是当前步骤（从 0 开始）
- `total` 是总步骤数
- Client 计算百分比：`current / total * 100`

---

## Client 端：接收 Notification

Client 在初始化 `ClientSession` 时提供 callback：

```python
def handle_logging(message: LoggingMessageNotification) -> None:
    level = message.params.level    # "info", "debug", "warning", "error"
    data = message.params.data      # 日志消息内容
    print(f"[{level.upper()}] {data}")

def handle_progress(
    progress_token: str | int,
    current: float,
    total: float | None
) -> None:
    if total:
        pct = int(current / total * 100)
        print(f"Progress: {pct}% ({current}/{total})")

# 在 session 创建时传入 callback
async with ClientSession(
    read, write,
    logging_callback=handle_logging,
) as session:
    await session.initialize()
```

重要区别：
- `logging_callback` 设置在 **session level**（`ClientSession` 初始化时）
- `progress_callback` 设置在 **每次 tool call**（调用特定 tool 时）

---

## 不同 Client 的呈现方式

同样的 notification 在不同 client 上有不同呈现：

| Client 类型 | Logging 呈现 | Progress 呈现 |
|------------|-------------|--------------|
| CLI | 终端 `print()` | 文字进度条 |
| Web app | WebSocket/SSE 推送到前端 | JavaScript 进度条 |
| Desktop app | 原生通知区域 | 原生进度指示器 |
| IDE extension | Output panel | 状态栏进度条 |

Server 发送相同数据 — client 决定如何显示。

---

## Notification 是可选的

Logging 和 progress 都是 **可选但强烈建议使用的**：

- Server 可以直接发送，不需检查 client 是否支持
- Client 可以忽略它们而不影响功能
- Fire-and-forget（不需要确认）
- 对 tool 返回值零影响

> **Key Insight**
> Logging 和 progress notification 是 MCP 版的 UX 打磨。它们不改变 tool 的功能，但大幅改善用户在长时间操作中的体验。一个静默处理 30 秒的 tool 感觉像坏了；加上进度更新的同一个 tool 感觉很灵敏。

---

## 常见模式

### 模式 1：多步骤 Pipeline

```python
@mcp.tool()
async def research(ctx: Context, query: str) -> str:
    ctx.info("Step 1/3: Searching databases...")
    ctx.report_progress(0, 3)
    results = await search(query)

    ctx.info("Step 2/3: Filtering results...")
    ctx.report_progress(1, 3)
    filtered = await filter_results(results)

    ctx.info("Step 3/3: Generating summary...")
    ctx.report_progress(2, 3)
    summary = await summarize(filtered)

    ctx.report_progress(3, 3)
    ctx.info("Research complete")
    return summary
```

### 模式 2：带 Logging 的错误恢复

```python
@mcp.tool()
async def fetch_with_retry(ctx: Context, url: str) -> str:
    for attempt in range(3):
        try:
            ctx.debug(f"Attempt {attempt + 1}/3")
            return await fetch(url)
        except TimeoutError:
            ctx.warning(f"Attempt {attempt + 1} timed out, retrying...")
    ctx.error("All attempts failed")
    raise RuntimeError("Failed after 3 retries")
```

---

## CCA Exam Relevance

- **D2 Task 2.3**：Server capabilities — notification 是可声明的功能
- **D2 Task 2.5**：Server-to-client communication — logging 和 progress 是主要范例
- 考试会测试区分 notification（单向）和 request（双向）的能力
- 知道 notification 是可选的且不影响 tool 输出
- 核心考试哲学：**好的 UX 不是可选项** — 即使后端 tool 也应该沟通状态

---

## Flashcards

| Front | Back |
|-------|------|
| MCP 提供哪两种实时反馈机制？ | Logging（`ctx.info()` 等）和 Progress（`ctx.report_progress()`） |
| MCP notification 是单向还是双向？ | 单向（fire-and-forget）— server 发送，不期望响应 |
| `logging_callback` 在 client 哪里设置？ | Session level，在 `ClientSession` 初始化时传入 |
| `progress_callback` 在 client 哪里设置？ | 每次 tool call 时设置，不在 session level |
| `report_progress()` 接受什么参数？ | `current`（当前步骤）和 `total`（总步骤数） |
| Notification 会影响 tool 的返回值吗？ | 不会 — 纯粹是信息性的，且为可选的 |
| Context 对象提供哪四个 log level？ | `debug`、`info`、`warning`、`error` |
| 为什么 progress notification 对 UX 很重要？ | 静默处理 30 秒的 tool 感觉坏了；有进度更新会感觉灵敏 |
