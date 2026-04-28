# Notifications 實作演練 — 工程深度解析

| 項目 | 詳情 |
|------|------|
| 考試領域 | D2 — 模型上下文協議 (23%) |
| 任務說明 | 2.2 (MCP 基本要素 — 通知) |
| 來源 | model-context-protocol-advanced-topics / 01-sampling-and-notifications / 第 06 課 |

---

## 一句話摘要

MCP 通知讓伺服器在工具執行期間透過 `Context` 物件發送日誌訊息和進度更新，而客戶端則定義日誌和進度回呼函數來向使用者顯示這些資訊。

---

## 兩種通知類型

MCP 支援兩種通知機制，兩者都是「發射即忘」（伺服器不等待回應）：

| 類型 | 伺服器 API | 用途 |
|------|-----------|------|
| **日誌記錄** | `ctx.info()`、`ctx.warning()`、`ctx.debug()`、`ctx.error()` | 以不同嚴重等級發送結構化日誌訊息 |
| **進度報告** | `ctx.report_progress(current, total)` | 回報任務完成百分比 |

---

## 伺服器端：使用 Context 發送通知

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

關鍵重點：
- **`Context` 是最後一個參數** — 工具函數自動接收它作為最後一個參數
- **日誌方法** — `ctx.info()`、`ctx.warning()`、`ctx.debug()`、`ctx.error()` 對應標準日誌等級
- **進度報告** — `ctx.report_progress(current, total)`，其中 `current` 是已完成的工作量，`total` 是總量
- 兩者都是**非同步**呼叫，會將訊息發送給客戶端

---

## 客戶端：定義回呼函數

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

日誌回呼接收 `LoggingMessageNotificationParams`，其 `.data` 欄位包含日誌訊息。進度回呼接收 `progress`、`total`（可選）和 `message`（可選）。

---

## 將回呼連接到會話

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

關鍵連接細節：
- **日誌回呼**透過 `logging_callback=` 傳入 `ClientSession` 建構函數
- **進度回呼**透過 `progress_callback=` 傳入 `call_tool()`

這是不同的連接點，因為日誌記錄適用於整個會話，而進度追蹤是針對每次工具呼叫的。

---

## 日誌 vs 進度：何時使用哪個

| 使用情境 | 機制 | 原因 |
|---------|------|------|
| 告知使用者目前步驟 | `ctx.info()` | 人類可讀的狀態訊息 |
| 警告效能降低 | `ctx.warning()` | 嚴重等級對過濾很重要 |
| 顯示完成百分比 | `ctx.report_progress()` | 用於 UI 進度條的數值進度 |
| 除錯工具內部 | `ctx.debug()` | 可在生產環境中過濾掉 |
| 回報可恢復的錯誤 | `ctx.error()` | 發出問題信號但不中斷 |

---

## CCA 考試相關性

- 通知是 **D2 基本要素**（任務 2.2）。預期考題會涉及每個回呼的連接位置。
- 關鍵區別是：`logging_callback` 在 `ClientSession` 上，`progress_callback` 在 `call_tool()` 上。
- `Context` 會自動作為最後一個參數提供給工具函數——你不需要手動建構它。
- 通知是**發射即忘**——伺服器不等待確認。
- 日誌等級（`info`、`warning`、`debug`、`error`）可能出現在測試適當嚴重等級選擇的考試情境中。

---

## 記憶卡

| # | 問題 | 答案 |
|---|------|------|
| 1 | 伺服器工具函數如何接收 Context 物件？ | 自動作為最後一個參數——不需要手動建構 |
| 2 | Context 物件上有哪四個日誌方法？ | `ctx.info()`、`ctx.warning()`、`ctx.debug()`、`ctx.error()` |
| 3 | `ctx.report_progress()` 的參數是什麼？ | `current`（已完成的工作量）和 `total`（總工作量） |
| 4 | 日誌回呼連接在哪裡？ | `ClientSession` 建構函數，透過 `logging_callback=` |
| 5 | 進度回呼連接在哪裡？ | `call_tool()` 方法，透過 `progress_callback=` |
| 6 | 為什麼日誌和進度回呼連接在不同的位置？ | 日誌記錄適用於整個會話；進度追蹤是針對每次工具呼叫的 |
| 7 | MCP 通知是同步的還是發射即忘的？ | 發射即忘——伺服器不等待確認 |
| 8 | 日誌回呼接收什麼型別？ | `LoggingMessageNotificationParams`，帶有 `.data` 欄位 |
