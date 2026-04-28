# Sampling Walkthrough — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Model Context Protocol (23%) |
| Task Statements | 2.2 (MCP primitives), 2.3 (sampling) |
| Source | model-context-protocol-advanced-topics / 01-sampling-and-notifications / Lesson 04 |

---

## One-Liner

Sampling allows an MCP server to request LLM text generation from the client via `create_message()`, with the client implementing a callback that converts MCP message formats to its LLM SDK and returns a `CreateMessageResult`.

---

## How Sampling Works

Sampling is the mechanism that lets a server ask the client to generate text using an LLM. The server never talks to the LLM directly -- it delegates through the client.

### The Flow

1. **Server initiates** -- Inside a tool function, call `ctx.session.create_message()` with a list of `SamplingMessage` objects
2. **Client callback fires** -- The client's `sampling_callback` receives the messages
3. **Client converts formats** -- MCP messages are not guaranteed to be compatible with any specific LLM SDK; you must convert them
4. **Client calls LLM** -- Using whatever SDK (Anthropic, OpenAI, etc.)
5. **Client returns result** -- Wrap the generated text in a `CreateMessageResult`
6. **Server receives text** -- The server can use, chain, or return the result

---

## Server Side: Initiating a Sampling Request

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

Key points:
- `create_message()` is called on `ctx.session` (the server's session to the client)
- Messages use MCP types (`SamplingMessage`, `TextContent`), not Anthropic SDK types
- You can pass a `system_prompt` and `max_tokens`
- The result may contain different content types; check `.content.type`

---

## Client Side: Implementing the Callback

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

Critical detail: **MCP messages are not Anthropic SDK messages**. You must write conversion logic to transform `SamplingMessage` objects into the format your LLM SDK expects.

---

## Wiring the Callback

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

The `sampling_callback` parameter on `ClientSession` is what connects the client's LLM logic to the server's sampling requests. If you forget this, the server's `create_message()` calls will fail.

---

## After the Server Gets the Result

Once the client returns text, the server can:
- **Use it in a workflow** -- as part of a multi-step tool execution
- **Make another sampling call** -- chain multiple LLM generations
- **Return it directly** -- pass the text back as the tool result

---

## CCA Exam Relevance

- Sampling is a **D2 core primitive** (Task 2.2, 2.3). Expect questions about the flow direction (server initiates, client executes).
- The message format conversion requirement is a common exam trap -- MCP types are NOT the same as Anthropic SDK types.
- The callback must be passed to `ClientSession` -- forgetting this wiring is a frequent error scenario in exam questions.
- Sampling enables the "server asks for intelligence" pattern, which is different from the normal "client calls tools on server" flow.

---

## Flashcards

| # | Question | Answer |
|---|----------|--------|
| 1 | Which side initiates a sampling request in MCP? | The **server** initiates by calling `ctx.session.create_message()` |
| 2 | What method does the server call to request text generation? | `ctx.session.create_message()` with a list of `SamplingMessage` objects |
| 3 | Why is message format conversion needed in the sampling callback? | MCP `SamplingMessage` objects are not guaranteed to be compatible with any specific LLM SDK (e.g., Anthropic). You must convert them manually. |
| 4 | What must the sampling callback return? | A `CreateMessageResult` containing the role, model, and generated content as a `TextContent` |
| 5 | Where is the sampling callback wired in? | As the `sampling_callback` parameter in the `ClientSession` constructor |
| 6 | Can a server make multiple sampling calls within a single tool execution? | Yes -- the server can chain multiple `create_message()` calls |
| 7 | What happens if the client does not provide a sampling callback? | The server's `create_message()` calls will fail because there is no handler registered |
| 8 | What MCP types are used to construct a sampling request? | `SamplingMessage` for messages and `TextContent` for text content |
