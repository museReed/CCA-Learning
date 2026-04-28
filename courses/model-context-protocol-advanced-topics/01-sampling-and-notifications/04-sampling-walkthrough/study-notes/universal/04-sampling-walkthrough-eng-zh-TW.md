# Sampling 實作演練 — 工程深度解析

| 項目 | 詳情 |
|------|------|
| 考試領域 | D2 — 模型上下文協議 (23%) |
| 任務說明 | 2.2 (MCP 基本要素), 2.3 (取樣) |
| 來源 | model-context-protocol-advanced-topics / 01-sampling-and-notifications / 第 04 課 |

---

## 一句話摘要

Sampling 允許 MCP 伺服器透過 `create_message()` 向客戶端請求 LLM 文字生成，客戶端需實作一個回呼函數，將 MCP 訊息格式轉換為其 LLM SDK 格式，並回傳 `CreateMessageResult`。

---

## Sampling 的運作原理

Sampling 是一種讓伺服器要求客戶端使用 LLM 生成文字的機制。伺服器永遠不會直接與 LLM 通訊——它透過客戶端來委派。

### 完整流程

1. **伺服器發起請求** — 在工具函數內，呼叫 `ctx.session.create_message()`，傳入一組 `SamplingMessage` 物件
2. **客戶端回呼觸發** — 客戶端的 `sampling_callback` 接收到訊息
3. **客戶端轉換格式** — MCP 訊息不保證與任何特定 LLM SDK 相容；你必須自行轉換
4. **客戶端呼叫 LLM** — 使用任何 SDK（Anthropic、OpenAI 等）
5. **客戶端回傳結果** — 將生成的文字包裝在 `CreateMessageResult` 中
6. **伺服器接收文字** — 伺服器可以使用、串連或回傳該結果

---

## 伺服器端：發起 Sampling 請求

```python
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import SamplingMessage, TextContent

mcp = FastMCP(name="Demo Server")

@mcp.tool()
async def summarize(text_to_summarize: str, ctx: Context):
    prompt = f"""
        Please summarize the following text:
        {text_to_summarize}
    """

    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user", content=TextContent(type="text", text=prompt)
            )
        ],
        max_tokens=4000,
        system_prompt="You are a helpful research assistant.",
    )

    if result.content.type == "text":
        return result.content.text
    else:
        raise ValueError("Sampling failed")
```

關鍵重點：
- `create_message()` 是在 `ctx.session` 上呼叫的（伺服器到客戶端的會話）
- 訊息使用 MCP 型別（`SamplingMessage`、`TextContent`），而非 Anthropic SDK 型別
- 你可以傳入 `system_prompt` 和 `max_tokens`
- 結果可能包含不同的內容型別；需檢查 `.content.type`

---

## 客戶端：實作回呼函數

```python
from mcp.client.session import RequestContext
from mcp.types import (
    CreateMessageRequestParams,
    CreateMessageResult,
    TextContent,
    SamplingMessage,
)

async def chat(input_messages: list[SamplingMessage], max_tokens=4000):
    messages = []
    for msg in input_messages:
        if msg.role == "user" and msg.content.type == "text":
            content = (
                msg.content.text
                if hasattr(msg.content, "text")
                else str(msg.content)
            )
            messages.append({"role": "user", "content": content})
        elif msg.role == "assistant" and msg.content.type == "text":
            content = (
                msg.content.text
                if hasattr(msg.content, "text")
                else str(msg.content)
            )
            messages.append({"role": "assistant", "content": content})

    response = await anthropic_client.messages.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
    )
    text = "".join([p.text for p in response.content if p.type == "text"])
    return text


async def sampling_callback(
    context: RequestContext, params: CreateMessageRequestParams
):
    text = await chat(params.messages)
    return CreateMessageResult(
        role="assistant",
        model=model,
        content=TextContent(type="text", text=text),
    )
```

關鍵細節：**MCP 訊息並非 Anthropic SDK 訊息**。你必須撰寫轉換邏輯，將 `SamplingMessage` 物件轉換為你的 LLM SDK 所期望的格式。

---

## 連接回呼函數

```python
async with ClientSession(
    read, write, sampling_callback=sampling_callback
) as session:
    await session.initialize()
    result = await session.call_tool(
        name="summarize",
        arguments={"text_to_summarize": "lots of text"},
    )
```

`ClientSession` 上的 `sampling_callback` 參數是將客戶端的 LLM 邏輯連接到伺服器 sampling 請求的關鍵。如果忘記傳入，伺服器的 `create_message()` 呼叫將會失敗。

---

## 伺服器取得結果後

客戶端回傳文字後，伺服器可以：
- **在工作流程中使用** — 作為多步驟工具執行的一部分
- **再次發起 sampling 呼叫** — 串連多次 LLM 生成
- **直接回傳** — 將文字作為工具結果傳回

---

## CCA 考試相關性

- Sampling 是 **D2 核心基本要素**（任務 2.2、2.3）。預期考題會涉及流程方向（伺服器發起，客戶端執行）。
- 訊息格式轉換是常見的考試陷阱——MCP 型別與 Anthropic SDK 型別不同。
- 回呼函數必須傳入 `ClientSession`——忘記這個連接是考試中常見的錯誤情境。
- Sampling 實現了「伺服器請求智慧」的模式，這與一般的「客戶端呼叫伺服器工具」流程不同。

---

## 記憶卡

| # | 問題 | 答案 |
|---|------|------|
| 1 | 在 MCP 中，哪一方發起 sampling 請求？ | **伺服器**透過呼叫 `ctx.session.create_message()` 發起 |
| 2 | 伺服器呼叫什麼方法來請求文字生成？ | `ctx.session.create_message()`，傳入一組 `SamplingMessage` 物件 |
| 3 | 為什麼 sampling 回呼中需要訊息格式轉換？ | MCP 的 `SamplingMessage` 物件不保證與任何特定 LLM SDK（如 Anthropic）相容，必須手動轉換。 |
| 4 | Sampling 回呼必須回傳什麼？ | 一個 `CreateMessageResult`，包含角色、模型和生成的內容（`TextContent`） |
| 5 | Sampling 回呼在哪裡連接？ | 作為 `ClientSession` 建構函數的 `sampling_callback` 參數 |
| 6 | 伺服器能否在單次工具執行中發起多次 sampling 呼叫？ | 可以——伺服器可以串連多次 `create_message()` 呼叫 |
| 7 | 如果客戶端未提供 sampling 回呼會怎樣？ | 伺服器的 `create_message()` 呼叫將會失敗，因為沒有註冊處理程式 |
| 8 | 用來建構 sampling 請求的 MCP 型別有哪些？ | `SamplingMessage` 用於訊息，`TextContent` 用於文字內容 |
