# Sampling — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server capabilities), 2.4 (client-server communication patterns) |
| Source | model-context-protocol-advanced-topics / 01-sampling-and-notifications / Lesson 03 |

---

## One-Liner

Sampling 让 MCP server 通过已连接的 client 调用 Claude，反转了一般的请求流向，使 server 不需要自己管理 API key 或 LLM 基础设施就能使用 AI 能力。

---

![Sampling Flow](../../visuals/sampling-flow-zh-TW.svg)


## Sampling 运作方式

标准 MCP 流程是 **Client -> Server**（client 要求 server 执行 tool）。Sampling 把方向翻转：

```
Server                    Client                   Claude
  |                         |                        |
  |-- create_message() ---->|                        |
  |                         |-- API call ----------->|
  |                         |<-- response -----------|
  |<-- SamplingResult ------|                        |
```

Server 从不直接与 Claude 对话，而是请 **client** 代为调用。

---

## Server 端实现

Server 端使用 context 对象的 `session.create_message()` 方法：

```python
@mcp.tool()
async def summarize_research(ctx: Context, topic: str) -> str:
    # 收集数据（server 自己的逻辑）
    results = await fetch_research_data(topic)

    # 请 client 帮忙调用 Claude 做摘要
    response = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=f"Summarize these research results:\n{results}"
                )
            )
        ],
        max_tokens=1024
    )

    return response.content.text
```

要点：
- `SamplingMessage` 封装发送给 client 的 prompt
- Server 指定 `max_tokens`，但 client 决定使用哪个 model
- Server **不需要 API key** — client 负责认证

---

## Client 端实现

Client 创建 `ClientSession` 时必须提供 `sampling_callback`：

```python
async def handle_sampling(message: CreateMessageRequest) -> CreateMessageResult:
    # Client 决定用哪个 model 并发送 API 调用
    response = await anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=message.params.max_tokens,
        messages=[
            {"role": m.role, "content": m.content.text}
            for m in message.params.messages
        ]
    )
    return CreateMessageResult(
        role="assistant",
        content=TextContent(type="text", text=response.content[0].text),
        model="claude-sonnet-4-20250514"
    )

# 在 session 初始化时传入 callback
async with ClientSession(read, write, sampling_callback=handle_sampling) as session:
    await session.initialize()
```

Client 拥有完整控制权：
- 选择调用哪个 model（可升级或降级）
- Rate limiting 与成本管理
- 请求过滤（可拒绝 sampling 请求）

---

## 架构优势

| 优势 | 说明 |
|------|------|
| **Server 不需 API key** | Server 从不直接碰 Claude API |
| **成本转移到 client** | 运行 client 的一方承担 AI 费用 |
| **降低 server 复杂度** | Server 专注于 domain logic，不需管 LLM 编排 |
| **适合 public server** | 任何人都能连接，各自使用自己的 credentials |
| **Client 控制 model** | Client 而非 server 选择 model |

---

## 何时使用 Sampling

适合使用 sampling 的情境：
- 构建 **public MCP server**（如研究工具），不想替每个用户支付 AI 费用
- Server 需要 AI 能力但应保持 **stateless 且无需 key**
- 希望 **client 保有控制权** 来选择 model 和管理支出

不适合的情境：
- Server 需要保证特定 model 行为（client 可能换 model）
- 低延迟至关重要（多一跳增加延迟）
- Server 需要在内部串联多次 LLM 调用（改用直接 API）

> **Key Insight**
> Sampling 翻转了 MCP 的经济模型：由 client 而非 server 承担 AI 费用。这让构建开源 MCP server 变得可行，作者不需要承担 API 成本。

---

## CCA Exam Relevance

- **D2 Task 2.3**：理解 MCP server capabilities — sampling 是 server 可声明的高级功能
- **D2 Task 2.4**：Client-server communication patterns — sampling 是 server-initiated communication 的主要范例
- 预期考试会出现 sampling vs. 直接 API 调用的情境题
- 核心取舍：便利性和成本转移 vs. server 端失去 model 控制权

---

## Flashcards

| Front | Back |
|-------|------|
| MCP sampling 让 server 可以做什么？ | 请求已连接的 client 代为调用 LLM，不需自己的 API key |
| Server 用哪个方法发起 sampling？ | `ctx.session.create_message()` 搭配 `SamplingMessage` 对象 |
| Sampling 中谁支付 AI 使用费？ | Client，因为实际 API 调用由 client 发出 |
| Client 必须提供什么 callback 才能支持 sampling？ | `sampling_callback`，在创建 `ClientSession` 时传入 |
| Client 可以拒绝 server 的 sampling 请求吗？ | 可以 — client 拥有完整控制权，可以过滤或拒绝请求 |
| 为什么 sampling 适合 public MCP server？ | 每个连接的 client 使用自己的 API credentials 并支付自己的费用 |
| Sampling 的主要延迟代价是什么？ | 多一段网络跳转：Server -> Client -> Claude -> Client -> Server |
| Sampling 请求中的 prompt 用什么数据结构封装？ | `SamplingMessage`，包含 `role` 和 `content`（通常是 `TextContent`） |
