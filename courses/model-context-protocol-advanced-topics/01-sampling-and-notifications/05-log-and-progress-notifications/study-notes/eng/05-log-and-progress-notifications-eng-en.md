# Log and Progress Notifications — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server capabilities), 2.5 (server-to-client communication) |
| Source | model-context-protocol-advanced-topics / 01-sampling-and-notifications / Lesson 05 |

---

## One-Liner

MCP servers use `ctx.info()` for logging and `ctx.report_progress()` for progress tracking, sending real-time feedback to clients during long-running operations via one-way notifications.

---

## Two Notification Mechanisms

MCP provides two distinct ways for servers to push real-time information to clients:

| Mechanism | Method | Purpose | Direction |
|-----------|--------|---------|-----------|
| Logging | `ctx.info()`, `ctx.debug()`, `ctx.warning()`, `ctx.error()` | Status messages, debug info | Server -> Client (fire-and-forget) |
| Progress | `ctx.report_progress(current, total)` | Completion percentage | Server -> Client (fire-and-forget) |

Both are **notifications**, not requests — the server does not wait for a response.

---

## Logging: Server-Side Implementation

The Context object exposes standard log-level methods:

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

Log levels follow standard conventions: `debug` < `info` < `warning` < `error`.

---

## Progress: Server-Side Implementation

Use `report_progress()` within loops to show completion:

```python
@mcp.tool()
async def batch_process(ctx: Context, items: list[str]) -> str:
    total = len(items)
    results = []

    for i, item in enumerate(items):
        ctx.report_progress(i, total)
        result = await process_item(item)
        results.append(result)

    # Signal completion
    ctx.report_progress(total, total)

    return format_results(results)
```

Key details:
- `current` is the current step (0-indexed start)
- `total` is the total number of steps
- Client calculates percentage: `current / total * 100`

---

## Client-Side: Receiving Notifications

The client provides callbacks when initializing `ClientSession`:

```python
def handle_logging(message: LoggingMessageNotification) -> None:
    level = message.params.level    # "info", "debug", "warning", "error"
    data = message.params.data      # The log message content
    print(f"[{level.upper()}] {data}")

def handle_progress(
    progress_token: str | int,
    current: float,
    total: float | None
) -> None:
    if total:
        pct = int(current / total * 100)
        print(f"Progress: {pct}% ({current}/{total})")

# Pass callbacks during session creation
async with ClientSession(
    read, write,
    logging_callback=handle_logging,
    # progress_callback is per-tool-call, not session-level
) as session:
    await session.initialize()
```

Important distinction:
- `logging_callback` is set at **session level** (in `ClientSession` init)
- `progress_callback` is set **per tool call** (when invoking a specific tool)

---

## Presentation Varies by Client Type

The same notifications render differently depending on the client:

| Client Type | Logging Presentation | Progress Presentation |
|-------------|---------------------|----------------------|
| CLI | `print()` to terminal | Text-based progress bar |
| Web app | WebSocket/SSE push to frontend | JavaScript progress bar |
| Desktop app | Native notification area | Native progress indicator |
| IDE extension | Output panel | Status bar progress |

The server sends the same data — the client decides how to display it.

---

## Notifications Are Optional

Both logging and progress are **optional but highly recommended**:

- Server can send them without checking if client supports them
- Client can ignore them without breaking functionality
- They are fire-and-forget (no acknowledgment needed)
- Zero impact on tool return values

> **Key Insight**
> Logging and progress notifications are the MCP equivalent of UX polish. They do not change what the tool does, but they dramatically improve the user's experience during long-running operations. A tool that silently processes for 30 seconds feels broken; the same tool with progress updates feels responsive.

---

## Common Patterns

### Pattern 1: Multi-Step Pipeline

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

### Pattern 2: Error Recovery with Logging

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

- **D2 Task 2.3**: Server capabilities — notifications are a declared capability
- **D2 Task 2.5**: Server-to-client communication — logging and progress are the primary examples
- Expect questions distinguishing notifications (one-way) from requests (bidirectional)
- Know that notifications are optional and do not affect tool output
- Key exam philosophy: **UX matters** — even backend tools should communicate status

---

## Flashcards

| Front | Back |
|-------|------|
| What two notification mechanisms does MCP provide for real-time feedback? | Logging (`ctx.info()` etc.) and Progress (`ctx.report_progress()`) |
| Are MCP notifications one-way or bidirectional? | One-way (fire-and-forget) — server sends, no response expected |
| Where is `logging_callback` configured in the client? | At session level, passed to `ClientSession` during initialization |
| Where is `progress_callback` configured in the client? | Per tool call, not at session level |
| What parameters does `report_progress()` take? | `current` (current step) and `total` (total steps) |
| Do notifications affect the tool's return value? | No — they are purely informational and optional |
| What are the four log levels available on the Context object? | `debug`, `info`, `warning`, `error` |
| Why are progress notifications important for UX? | A tool that silently processes for 30 seconds feels broken; progress updates make it feel responsive |
