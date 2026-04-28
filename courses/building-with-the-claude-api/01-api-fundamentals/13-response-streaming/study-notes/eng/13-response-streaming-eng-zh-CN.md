# Response Streaming — 工程深度解析

| 项目 | 细节 |
|------|------|
| 考试领域 | D5 — Enterprise Deployment (20%) |
| Task Statements | 5.2（streaming 与响应速度）、5.3（production 模式） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 13 |

---

## 一句话总结

Response streaming 把单次 blocking API 调用换成 server-sent 的渐进事件流，让你的 client 在 Claude 生成时就能把文字显示出来，把用户感受到的延迟从「10-30 秒的转圈」降到「第一个 token 不到一秒」。

---

## 延迟问题

一次完整的 Claude completion 对长响应可能花 10 到 30 秒。非 streaming 的流程中，你的服务器调用 `messages.create(...)`，等整段响应，再转给 client。这几秒间，用户盯着转圈没有任何反馈——经典的「是不是坏了？」时刻，直接击垮感受质量。

根本原因是长文生成是 token by token。就算 Claude 立刻开始产 token，默认 API 调用会把它们全部留在 server 端，直到消息完成才给出来。

Streaming 的解法是**边生成边转发部分输出**——Claude 正在写的字会在几百毫秒内出现在用户 UI 上。

---

## 为什么感受延迟 > 实际延迟

总生成时间在 streaming 下不会改变。改变的是用户看到的**第一个字节时间**（TTFB）。人类对响应速度的感受来自第一个可见的生命迹象，不是完成时间戳。15 秒的 streamed 响应感觉比 5 秒的 blocking 响应快，因为用户看到文字持续出现。

这是基本 UX 原则：进度指示和渐进渲染胜过转圈。Streaming 就是用户现在从任何 LLM 产品期待的 ChatGPT 式体验。

---

## Stream Event 类型

`stream=True` 时，API 会发送一连串有类型的 events，而不是单一响应。课程涵盖六种 event 类型：

| Event | 含义 |
|-------|------|
| `MessageStart` | 新消息开始 |
| `ContentBlockStart` | 新 content block 开始（text、tool_use 等）|
| `ContentBlockDelta` | 一块生成文字（或其他 content delta）|
| `ContentBlockStop` | 当前 content block 完成 |
| `MessageDelta` | 顶层消息 metadata 更新 |
| `MessageStop` | Stream 结束 |

`ContentBlockDelta` events 载着你要显示的实际 token chunks。其他载结构性 metadata（你在哪个 block、消息是否完成）。

纯文字 UI 只需要 deltas。对更丰富的集成（tool use、多 content blocks），start/stop events 告诉你当前该把内容 append 进哪个 block。

---

## 用原始 Events 做基础 Streaming

最直白的形式是直接 iterate events：

```python
from anthropic import Anthropic

client = Anthropic()

messages = [{"role": "user", "content": "Write a 1 sentence description of a fake database"}]

stream = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=messages,
    stream=True,
)

for event in stream:
    print(event)
```

这给你所有 event 类型的顺序。适合 debug 或建立需要对 tool_use delta 和 text delta 分开处理的 custom dispatch 逻辑。

---

## 用 SDK 做简化的 Text Streaming

对常见情况——「我只要 text chunks 一来就拿到」——SDK 提供更高层级的 helper：

```python
with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=messages,
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

和原始形式的关键差别：

- 用 `client.messages.stream(...)`（不是 `.create(..., stream=True)`）
- 用 `with` context 管理——确保底层 HTTP 连接被清掉
- `stream.text_stream` 只 yield text chunks。所有结构事件都帮你过滤掉
- `flush=True` 很重要——不加 buffering 会把 streaming 效果藏起来

这是你在 90% production chat UI 会用的形式。

---

## Streaming 后获取最终消息

Streaming 对用户很好，但你的 backend 通常还需要完整消息给：

- 数据库存储（chat history）
- Analytics / logging
- 喂到下一轮对话
- 计算 token 用量 / 费用

Stream 结束后，你可以获取组好的消息：

```python
with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=messages,
) as stream:
    for text in stream.text_stream:
        send_chunk_to_client(text)

    final_message = stream.get_final_message()
    store_in_database(final_message)
```

这是两全其美的模式：client 看到 streamed tokens，服务器最终拿到完全结构化的 `Message` 对象（content blocks、stop_reason、usage 等）。

---

## 架构：Streaming 的位置

典型 streaming chat stack 长这样：

```
Browser ──HTTP/WebSocket/SSE──▶ 你的服务器 ──Anthropic SDK stream──▶ Claude API
   ▲                              │  │
   │                              │  └──(在 MessageStop) 存 final_message 进 DB
   └─────────── chunks ───────────┘
```

你的服务器实质上是一个 proxy：

1. 接受用户请求
2. 对 Anthropic 开启 streaming 调用
3. 把每个 text chunk 转给浏览器（通过 SSE 或 WebSocket）
4. 完成时把最终消息写到数据库

关键：**不要**把你的 Anthropic API key 暴露给浏览器。就算直接 streaming 在技术上做得到，为了安全也必须走 streaming proxy 模式。

---

## Streaming 和 Tool Use

Tools 开启时 streaming 仍然有效，但 event 类型会更丰富——你会在 stream 里看到 `tool_use` content blocks。你要嘛用原始 event loop 处理，要嘛靠 SDK helper 自动组装。纯文字 UI 用 `stream.text_stream` 会隐藏 tool_use 噪音；显示「Claude 正在调用 tool X…」的 agentic UI 就要原始 events。

---

## 常见错误

1. **Chat UI 不用 `stream=True`**——默认 blocking 行为对长响应是糟糕 UX。Streaming 是 production 默认模式，不是优化
2. **忘了 context manager**——`client.messages.stream(...)` 必须用 `with`，否则 HTTP 连接会泄漏
3. **忽略非 delta events**——只看 `ContentBlockDelta` 会错过 stop reason、tool_use blocks、usage metadata
4. **不调用 `get_final_message()`**——你会失去结构化消息，必须自己从 chunks 重组
5. **从浏览器直接 stream 到 Anthropic**——这会泄漏你的 API key。永远经过自己的服务器 proxy

> **Key Insight**
>
> Streaming 不会让 Claude 更快——它让 Claude *感觉*快，把感受延迟从响应结束挪到第一个 token。这是原型 LLM 应用和 production 应用在 UX 上最重要的单一差别。任何面向用户的 chat 体验，streaming 是必要，不是可选。

---

## CCA 考试重点

- **D5.2（streaming 与响应速度）**：预期会直接考如何启用 `stream=True`、区分 `messages.create(stream=True)` vs `messages.stream(...)`、以及知道 event 类型
- **D5.3（production 模式）**：streaming 是 production chat UI 的标准模式——注意围绕用户感受延迟的考题
- 记住 event 名称（`MessageStart`、`ContentBlockStart`、`ContentBlockDelta`、`ContentBlockStop`、`MessageDelta`、`MessageStop`）——这些会考

---

## Flashcards

| 题目 | 答案 |
|------|------|
| 怎么在原始 Anthropic API 调用启用 streaming？ | 把 `stream=True` 传给 `client.messages.create(...)` |
| Streaming text 的高层 SDK 方法是什么？ | `client.messages.stream(...)`——搭配 `with` context manager 使用 |
| 哪个 event 类型含实际生成的 text chunks？ | `ContentBlockDelta`——载着渐进的 text（或其他 content）delta |
| 主要六个 stream event 类型是什么？ | MessageStart、ContentBlockStart、ContentBlockDelta、ContentBlockStop、MessageDelta、MessageStop |
| Streaming 会降低总生成时间吗？ | 不会——总时间一样。它通过边生成边显示文字来降低用户感受延迟 |
| 怎么在 streaming 结束后获取完整组好的消息？ | 在 `with` block 内 iterate `stream.text_stream` 后调用 `stream.get_final_message()` |
| `stream.text_stream` 过滤掉什么？ | 所有非 text 结构事件——只 yield 纯 text chunks |
| 为什么 streaming 要走自己的服务器而不是浏览器？ | 为了不暴露你的 Anthropic API key。服务器当 streaming proxy |
| 在 streaming 语境下「time to first byte」是什么？ | 用户看到第一块生成文字前的延迟——对感受速度才是关键的数字 |
