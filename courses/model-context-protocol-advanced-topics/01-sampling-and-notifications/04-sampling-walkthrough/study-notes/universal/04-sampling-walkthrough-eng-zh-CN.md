# Sampling 实操演练 — 工程深度解析

| 项目 | 详情 |
|------|------|
| 考试领域 | D2 — 模型上下文协议 (23%) |
| 任务说明 | 2.2 (MCP 基本要素), 2.3 (采样) |
| 来源 | model-context-protocol-advanced-topics / 01-sampling-and-notifications / 第 04 课 |

---

## 一句话摘要

Sampling 允许 MCP 服务器通过 `create_message()` 向客户端请求 LLM 文本生成，客户端需实现一个回调函数，将 MCP 消息格式转换为其 LLM SDK 格式，并返回 `CreateMessageResult`。

---

## Sampling 的运作原理

Sampling 是一种让服务器要求客户端使用 LLM 生成文本的机制。服务器永远不会直接与 LLM 通信——它通过客户端来委派。

### 完整流程

1. **服务器发起请求** — 在工具函数内，调用 `ctx.session.create_message()`，传入一组 `SamplingMessage` 对象
2. **客户端回调触发** — 客户端的 `sampling_callback` 接收到消息
3. **客户端转换格式** — MCP 消息不保证与任何特定 LLM SDK 兼容；你必须自行转换
4. **客户端调用 LLM** — 使用任何 SDK（Anthropic、OpenAI 等）
5. **客户端返回结果** — 将生成的文本包装在 `CreateMessageResult` 中
6. **服务器接收文本** — 服务器可以使用、串联或返回该结果

---

## 服务器端：发起 Sampling 请求

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

关键重点：
- `create_message()` 是在 `ctx.session` 上调用的（服务器到客户端的会话）
- 消息使用 MCP 类型（`SamplingMessage`、`TextContent`），而非 Anthropic SDK 类型
- 你可以传入 `system_prompt` 和 `max_tokens`
- 结果可能包含不同的内容类型；需检查 `.content.type`

---

## 客户端：实现回调函数

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

关键细节：**MCP 消息并非 Anthropic SDK 消息**。你必须编写转换逻辑，将 `SamplingMessage` 对象转换为你的 LLM SDK 所期望的格式。

---

## 连接回调函数

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

`ClientSession` 上的 `sampling_callback` 参数是将客户端的 LLM 逻辑连接到服务器 sampling 请求的关键。如果忘记传入，服务器的 `create_message()` 调用将会失败。

---

## 服务器获取结果后

客户端返回文本后，服务器可以：
- **在工作流程中使用** — 作为多步骤工具执行的一部分
- **再次发起 sampling 调用** — 串联多次 LLM 生成
- **直接返回** — 将文本作为工具结果传回

---

## CCA 考试相关性

- Sampling 是 **D2 核心基本要素**（任务 2.2、2.3）。预期考题会涉及流程方向（服务器发起，客户端执行）。
- 消息格式转换是常见的考试陷阱——MCP 类型与 Anthropic SDK 类型不同。
- 回调函数必须传入 `ClientSession`——忘记这个连接是考试中常见的错误情境。
- Sampling 实现了「服务器请求智能」的模式，这与一般的「客户端调用服务器工具」流程不同。

---

## 记忆卡

| # | 问题 | 答案 |
|---|------|------|
| 1 | 在 MCP 中，哪一方发起 sampling 请求？ | **服务器**通过调用 `ctx.session.create_message()` 发起 |
| 2 | 服务器调用什么方法来请求文本生成？ | `ctx.session.create_message()`，传入一组 `SamplingMessage` 对象 |
| 3 | 为什么 sampling 回调中需要消息格式转换？ | MCP 的 `SamplingMessage` 对象不保证与任何特定 LLM SDK（如 Anthropic）兼容，必须手动转换。 |
| 4 | Sampling 回调必须返回什么？ | 一个 `CreateMessageResult`，包含角色、模型和生成的内容（`TextContent`） |
| 5 | Sampling 回调在哪里连接？ | 作为 `ClientSession` 构造函数的 `sampling_callback` 参数 |
| 6 | 服务器能否在单次工具执行中发起多次 sampling 调用？ | 可以——服务器可以串联多次 `create_message()` 调用 |
| 7 | 如果客户端未提供 sampling 回调会怎样？ | 服务器的 `create_message()` 调用将会失败，因为没有注册处理程序 |
| 8 | 用来构建 sampling 请求的 MCP 类型有哪些？ | `SamplingMessage` 用于消息，`TextContent` 用于文本内容 |
