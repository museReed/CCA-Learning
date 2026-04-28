# Sampling — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server capabilities), 2.4 (client-server communication patterns) |
| Source | model-context-protocol-advanced-topics / 01-sampling-and-notifications / Lesson 03 |

---

## One-Liner

Sampling 讓 MCP server 透過已連接的 client 呼叫 Claude，反轉了一般的請求流向，使 server 不需要自己管理 API key 或 LLM 基礎設施就能使用 AI 能力。

---

![Sampling Flow](../../visuals/sampling-flow-zh-TW.svg)


## Sampling 運作方式

標準 MCP 流程是 **Client -> Server**（client 要求 server 執行 tool）。Sampling 把這個方向翻轉：

```
Server                    Client                   Claude
  |                         |                        |
  |-- create_message() ---->|                        |
  |                         |-- API call ----------->|
  |                         |<-- response -----------|
  |<-- SamplingResult ------|                        |
```

Server 從不直接與 Claude 對話，而是請 **client** 代為呼叫。

---

## Server 端實作

Server 端使用 context 物件的 `session.create_message()` 方法：

```python
@mcp.tool()
async def summarize_research(ctx: Context, topic: str) -> str:
    # 收集資料（server 自己的邏輯）
    results = await fetch_research_data(topic)

    # 請 client 幫忙呼叫 Claude 做摘要
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

重點：
- `SamplingMessage` 封裝發送給 client 的 prompt
- Server 指定 `max_tokens`，但 client 決定使用哪個 model
- Server **不需要 API key** — client 負責認證

---

## Client 端實作

Client 建立 `ClientSession` 時必須提供 `sampling_callback`：

```python
async def handle_sampling(message: CreateMessageRequest) -> CreateMessageResult:
    # Client 決定用哪個 model 並發送 API 呼叫
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

# 在 session 初始化時傳入 callback
async with ClientSession(read, write, sampling_callback=handle_sampling) as session:
    await session.initialize()
```

Client 擁有完整控制權：
- 選擇呼叫哪個 model（可升級或降級）
- Rate limiting 與成本管理
- 請求過濾（可拒絕 sampling 請求）

---

## 架構優勢

| 優勢 | 說明 |
|------|------|
| **Server 不需 API key** | Server 從不直接碰 Claude API |
| **成本轉移到 client** | 執行 client 的一方負擔 AI 費用 |
| **降低 server 複雜度** | Server 專注於 domain logic，不需管 LLM 編排 |
| **適合 public server** | 任何人都能連接，各自使用自己的 credentials |
| **Client 控制 model** | Client 而非 server 選擇 model |

---

## 何時使用 Sampling

適合使用 sampling 的情境：
- 建置 **public MCP server**（如研究工具），不想替每個使用者支付 AI 費用
- Server 需要 AI 能力但應保持 **stateless 且無需 key**
- 希望 **client 保有控制權** 來選擇 model 和管理支出

不適合的情境：
- Server 需要保證特定 model 行為（client 可能換 model）
- 低延遲至關重要（多一跳增加延遲）
- Server 需要在內部串聯多次 LLM 呼叫（改用直接 API）

> **Key Insight**
> Sampling 翻轉了 MCP 的經濟模型：由 client 而非 server 承擔 AI 費用。這讓建置開源 MCP server 變得可行，作者不需要負擔 API 成本。

---

## CCA Exam Relevance

- **D2 Task 2.3**：理解 MCP server capabilities — sampling 是 server 可宣告的進階功能
- **D2 Task 2.4**：Client-server communication patterns — sampling 是 server-initiated communication 的主要範例
- 預期考試會出現 sampling vs. 直接 API 呼叫的情境題
- 核心取捨：便利性和成本轉移 vs. server 端失去 model 控制權

---

## Flashcards

| Front | Back |
|-------|------|
| MCP sampling 讓 server 可以做什麼？ | 請求已連接的 client 代為呼叫 LLM，不需自己的 API key |
| Server 用哪個方法發起 sampling？ | `ctx.session.create_message()` 搭配 `SamplingMessage` 物件 |
| Sampling 中誰支付 AI 使用費？ | Client，因為實際 API 呼叫由 client 發出 |
| Client 必須提供什麼 callback 才能支援 sampling？ | `sampling_callback`，在建立 `ClientSession` 時傳入 |
| Client 可以拒絕 server 的 sampling 請求嗎？ | 可以 — client 擁有完整控制權，可以過濾或拒絕請求 |
| 為什麼 sampling 適合 public MCP server？ | 每個連接的 client 使用自己的 API credentials 並支付自己的費用 |
| Sampling 的主要延遲代價是什麼？ | 多一段網路跳轉：Server -> Client -> Claude -> Client -> Server |
| Sampling 請求中的 prompt 用什麼資料結構封裝？ | `SamplingMessage`，包含 `role` 和 `content`（通常是 `TextContent`） |
