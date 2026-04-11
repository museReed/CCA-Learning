# Multi-Turn Conversations with Tools — Engineering Deep Dive（简中）

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture (22%) / D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 1.3（multi-turn conversation management）、1.2（agentic loop 实现）、2.4（multi-turn tool loops） |
| 来源 | building-with-the-claude-api / 01-api-fundamentals / Lesson 38 |

---

## 一句话总结

当 Claude 需要串联多个 tool call 才能回答一个用户问题时，就会出现 multi-turn tool 对话；唯一的实现方式是一个**循环**，不断往返调 API，直到 Claude 不再要求 tool 为止。

---

## 为什么需要 Multi-Turn

有些问题没办法用一次 tool 调用回答。「103 天之后是几号？」会拆解成：

1. `get_current_datetime()` → 今天日期
2. `add_duration_to_datetime(date, +103 days)` → 目标日期

Claude 没办法事先把两次调用都打包好，因为第二次依赖第一次的输出。每次调用都变成独立回合，服务器端（你的代码）负责推动这个循环。

```
用户问题
  ↓
Claude → tool_use: get_current_datetime
  ↓
Server 执行 tool → tool_result
  ↓
Claude → tool_use: add_duration_to_datetime(date=..., days=103)
  ↓
Server 执行 tool → tool_result
  ↓
Claude → 最终文字答案（stop_reason="end_turn"）
```

---

## 对话 Loop 骨架

标准模式是一个 `while True` loop，当 Claude 不再要求 tool 时 break：

```python
def run_conversation(messages):
    while True:
        response = chat(messages)
        add_assistant_message(messages, response)

        # 伪代码——Lesson 39 会看到真正的 stop_reason 检查
        if not response_is_asking_for_a_tool(response):
            break

        tool_result_blocks = run_tools(response)
        add_user_message(messages, tool_result_blocks)

    return messages
```

三个重点：

1. **`add_assistant_message` 保留完整 block list**（text + tool-use blocks）
2. **`run_tools` 执行每一个 tool-use block** 并一次返回所有结果
3. **`add_user_message` 吃 tool result** 把结果包成单一条 user-role message 送回去

---

## 重构 Helper Function 支持 Multi-Block

Lesson 强调：实现 loop 之前，你的 helper 必须升级成能接 `Message` 对象，不只是字符串。

### `add_user_message`——接字符串、block list 或 Message

```python
from anthropic.types import Message

def add_user_message(messages, message):
    content = message.content if isinstance(message, Message) else message
    messages.append({"role": "user", "content": content})
```

这种多态让你可以用这些方式调用：
- 纯字符串（`"现在几点？"`）
- content block list（tool result blocks）
- API 返回的完整 `Message` 对象

### `add_assistant_message`——同样的多态

```python
def add_assistant_message(messages, message):
    content = message.content if isinstance(message, Message) else message
    messages.append({"role": "assistant", "content": content})
```

### `chat`——接受 tools、返回完整 Message 对象

```python
def chat(messages, system=None, temperature=1.0, stop_sequences=[], tools=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }
    if tools:
        params["tools"] = tools
    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message
```

一旦有 tool 介入，返回整个 `Message`（而不是 `.content[0].text`）是**必需的**——你需要 block list、`stop_reason` 和 usage data 来驱动 loop。

### `text_from_message`——需要时抽出显示用的文字

```python
def text_from_message(message):
    return "\n".join(
        [block.text for block in message.content if block.type == "text"]
    )
```

用 `block.type == "text"` 过滤是从混合 block 响应中拉出用户可见说明的标准做法。

---

## 对话累积的语义

每个回合至少会在历史中多加一条消息：

| 回合 | 加到 `messages` 的内容 |
|------|-----------------------|
| 0 | 用户问题 |
| 1 | Assistant message：`text + tool_use_1` |
| 2 | User message：`tool_result_1` |
| 3 | Assistant message：`text + tool_use_2` |
| 4 | User message：`tool_result_2` |
| 5 | Assistant message：最终文字（`stop_reason=end_turn`） |

注意 assistant 和 user message **严格交替**——tool result 永远是 user message 送回来，绝对不能是 assistant message。这保留了 API 强制的交替不变式。

---

## Context Window 考量

每次迭代会让 `messages` 增长一条（有时两条）消息。长 tool 链会让你撞到 context window 上限。缓解策略：

1. **用 `max_iterations` 计数器卡住 loop**，防止 agent 失控
2. **摘要中间 tool 结果**，如果里面有不再需要的冗长数据
3. **用 prompt caching**（课程后面会讲），分摊历史增长的成本
4. **让 tool 响应短一点**——返回简洁 JSON 的 tool 比返回整个网页的 tool 好太多

---

## 常见错误

1. **只 append `.content[0].text` 到历史**——会丢 tool-use block，下一回合 `tool_use_id` 就配对不上
2. **忘了每次 loop 都要带 `tools=[...]`**——Claude 每次都需要 schema，即使只是在响应 tool result
3. **用字符串调用 `add_user_message` 来送 tool result**——tool result 必须是 content-block list
4. **没有 loop 上限**——坏掉的 tool 或搞混的 Claude 会产生无限 tool-use loop，烧光 token
5. **用「有没有 text content」当 break 条件**——Claude 可以同一回合吐 text 加 tool_use；永远检查 `stop_reason`

---

> **Key Insight**
>
> Multi-turn tool 对话不是特例——它是通例。单回合 tool use 只是「loop 跑完一次就结束」的情况。即使你第一个 tool-use 功能只需要单一 tool，也把它写成标准 loop 形式，将来产品需要 tool 串联时就不用重写。前期投资在 helper function 的多态处理，就是让 loop 实现变轻松的关键。

---

## CCA Exam Relevance

- **D1（Agentic Architecture）**：这是核心的 agentic loop 问题。考题会问「什么信号让 loop 继续」、「Claude 怎么知道要串联 tool」。
- **D2（Tool Design & MCP Integration）**：理解 tool schema 必须在每次 loop 迭代都带上。
- 考试提示：问 multi-turn tool 对话的题目几乎都在考 loop 结构——把 `while` 模式背熟。

---

## Flashcards

| 题目 | 答案 |
|------|------|
| 为什么有些问题需要 multi-turn tool 对话？ | 因为第二个 tool call 依赖第一个的输出（例如「103 天后」要先知道今天） |
| 用什么控制结构实现 multi-turn tool 对话？ | `while` loop，持续调用 API 直到 Claude 不再要 tool |
| `add_assistant_message` 除了字符串还要接什么？ | 完整 `Message` 对象——才能保留包含 tool-use block 的整个 block list |
| 为什么 `chat` 要返回整个 `Message` 而不只是 text？ | 因为你需要 `content`（block list）、`stop_reason` 和 usage data 来驱动 loop |
| 哪个 helper 从混合 block 消息中抽出用户可见文字？ | `text_from_message`——用 `block.type == "text"` 过滤再合并 |
| 为什么要用 `max_iterations` 卡住 loop？ | 防止失控的 agent 或坏掉的 tool 产生无限 loop |
| Multi-turn tool 对话的交替不变式是什么？ | Assistant 和 user message 必须严格交替；tool result 永远放在 user message |
| 为什么不能用「有 text 就 break」？ | Claude 可以同回合吐 text 加 tool_use——永远改用 `stop_reason` 检查 |
