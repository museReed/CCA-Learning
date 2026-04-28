# Log and Progress Notifications — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server capabilities), 2.5 (server-to-client communication) |
| Source | model-context-protocol-advanced-topics / 01-sampling-and-notifications / Lesson 05 |

---

## One-Liner

MCP server 使用 `ctx.info()` 記錄日誌、`ctx.report_progress()` 回報進度，在長時間操作中透過單向 notification 即時回饋給 client。

---

## 兩種 Notification 機制

MCP 提供兩種方式讓 server 即時推送資訊給 client：

| 機制 | 方法 | 用途 | 方向 |
|------|------|------|------|
| Logging | `ctx.info()`, `ctx.debug()`, `ctx.warning()`, `ctx.error()` | 狀態訊息、除錯資訊 | Server -> Client（fire-and-forget） |
| Progress | `ctx.report_progress(current, total)` | 完成百分比 | Server -> Client（fire-and-forget） |

兩者都是 **notification**，不是 request — server 不等待回應。

---

## Logging：Server 端實作

Context 物件提供標準 log level 方法：

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

Log level 遵循標準慣例：`debug` < `info` < `warning` < `error`。

---

## Progress：Server 端實作

在迴圈中使用 `report_progress()` 顯示完成度：

```python
@mcp.tool()
async def batch_process(ctx: Context, items: list[str]) -> str:
    total = len(items)
    results = []

    for i, item in enumerate(items):
        ctx.report_progress(i, total)
        result = await process_item(item)
        results.append(result)

    # 標示完成
    ctx.report_progress(total, total)

    return format_results(results)
```

重點：
- `current` 是目前步驟（從 0 開始）
- `total` 是總步驟數
- Client 計算百分比：`current / total * 100`

---

## Client 端：接收 Notification

Client 在初始化 `ClientSession` 時提供 callback：

```python
def handle_logging(message: LoggingMessageNotification) -> None:
    level = message.params.level    # "info", "debug", "warning", "error"
    data = message.params.data      # 日誌訊息內容
    print(f"[{level.upper()}] {data}")

def handle_progress(
    progress_token: str | int,
    current: float,
    total: float | None
) -> None:
    if total:
        pct = int(current / total * 100)
        print(f"Progress: {pct}% ({current}/{total})")

# 在 session 建立時傳入 callback
async with ClientSession(
    read, write,
    logging_callback=handle_logging,
) as session:
    await session.initialize()
```

重要區別：
- `logging_callback` 設定在 **session level**（`ClientSession` 初始化時）
- `progress_callback` 設定在 **每次 tool call**（呼叫特定 tool 時）

---

## 不同 Client 的呈現方式

同樣的 notification 在不同 client 上有不同呈現：

| Client 類型 | Logging 呈現 | Progress 呈現 |
|------------|-------------|--------------|
| CLI | 終端機 `print()` | 文字進度條 |
| Web app | WebSocket/SSE 推送到前端 | JavaScript 進度條 |
| Desktop app | 原生通知區域 | 原生進度指示器 |
| IDE extension | Output panel | 狀態列進度條 |

Server 發送相同資料 — client 決定如何顯示。

---

## Notification 是可選的

Logging 和 progress 都是 **可選但強烈建議使用的**：

- Server 可以直接發送，不需檢查 client 是否支援
- Client 可以忽略它們而不影響功能
- Fire-and-forget（不需要確認）
- 對 tool 回傳值零影響

> **Key Insight**
> Logging 和 progress notification 是 MCP 版的 UX 打磨。它們不改變 tool 的功能，但大幅改善使用者在長時間操作中的體驗。一個靜默處理 30 秒的 tool 感覺像壞了；加上進度更新的同一個 tool 感覺很靈敏。

---

## 常見模式

### 模式 1：多步驟 Pipeline

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

### 模式 2：帶 Logging 的錯誤恢復

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

- **D2 Task 2.3**：Server capabilities — notification 是可宣告的功能
- **D2 Task 2.5**：Server-to-client communication — logging 和 progress 是主要範例
- 考試會測試區分 notification（單向）和 request（雙向）的能力
- 知道 notification 是可選的且不影響 tool 輸出
- 核心考試哲學：**好的 UX 不是可選項** — 即使後端 tool 也應該溝通狀態

---

## Flashcards

| Front | Back |
|-------|------|
| MCP 提供哪兩種即時回饋機制？ | Logging（`ctx.info()` 等）和 Progress（`ctx.report_progress()`） |
| MCP notification 是單向還是雙向？ | 單向（fire-and-forget）— server 發送，不期望回應 |
| `logging_callback` 在 client 哪裡設定？ | Session level，在 `ClientSession` 初始化時傳入 |
| `progress_callback` 在 client 哪裡設定？ | 每次 tool call 時設定，不在 session level |
| `report_progress()` 接受什麼參數？ | `current`（目前步驟）和 `total`（總步驟數） |
| Notification 會影響 tool 的回傳值嗎？ | 不會 — 純粹是資訊性的，且為可選的 |
| Context 物件提供哪四個 log level？ | `debug`、`info`、`warning`、`error` |
| 為什麼 progress notification 對 UX 很重要？ | 靜默處理 30 秒的 tool 感覺壞了；有進度更新會感覺靈敏 |
