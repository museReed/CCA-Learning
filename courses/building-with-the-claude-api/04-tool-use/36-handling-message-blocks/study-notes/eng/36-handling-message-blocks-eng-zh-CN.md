# Handling Message Blocks — Engineering Deep Dive（简中）

| 项目 | 内容 |
|------|------|
| 考试领域 | D2 — Tool Design & MCP Integration (18%) / D1 — Agentic Architecture (22%) |
| Task Statements | 2.2（content block 处理）、2.1（tool schema 集成）、1.2（agentic loop 基础） |
| 来源 | building-with-the-claude-api / 04-tool-use / Lesson 36 |

---

## 一句话总结

只要在 request 中传入 `tools=[...]`，Claude 的响应 `content` 就不再是单一字符串，而是一个由 `TextBlock`、`ToolUseBlock` 等 typed block 组成的 list；你的代码必须迭代这些 block、完整保留到对话历史、并按 block type 进行分发。

---

## 从纯文本响应到 Multi-Block 响应

没有 tools 时，`response.content` 实际上就是一个 `TextBlock`。一旦 request 带 `tools=[...]`，Claude 就可能决定调用函数，assistant message 就会变成**异构的 block list**：

```python
response = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    tools=[get_current_datetime_schema],
)

# response.content 现在是 block 的 list：
# [TextBlock(text="我可以帮你查当前时间..."),
#  ToolUseBlock(id="toolu_01...", name="get_current_datetime", input={})]
```

关键变化：`response.content` **永远是一个 list**，单次回合可能同时包含说明文字与一个或多个 tool use 请求。

---

## `ToolUseBlock` 的结构

每个 tool-use block 有四个你必须处理的字段：

| 字段 | 用途 |
|------|------|
| `type` | 永远是 `"tool_use"`——用它来过滤 block |
| `id` | 每次调用唯一 ID（如 `toolu_01A09q90qw...`）。必须在对应的 `tool_result` 中回填这个 ID |
| `name` | 模型选择的函数名（必须对应你注册的 schema） |
| `input` | 符合该 tool `input_schema` 的参数 dict |

```python
for block in response.content:
    if block.type == "tool_use":
        tool_id = block.id
        tool_name = block.name
        tool_args = block.input  # dict，用 ** 解包
```

---

## 在对话历史中保留完整 Content

Claude 是 stateless 的——历史记录由**你**管理。当 assistant 返回 multi-block content 时，必须把**整个 `response.content` list** append 回去，不能只保留 text：

```python
messages.append({
    "role": "assistant",
    "content": response.content   # 保留所有 block，包含 ToolUseBlock
})
```

如果把它扁平化成字符串、或者把 tool-use block 丢掉，下一次 API 调用就会出错：因为下一条 user message 里的 `tool_result` 会引用一个已经不存在于历史中的 `tool_use_id`，API 对这个配对非常严格。

---

## `stop_reason` 作为 Loop 信号

每个 response 除了 content list，还有 `stop_reason`。当 Claude 输出 tool-use block 时，`stop_reason == "tool_use"`。这就是标准的信号，告诉你代码必须先跑 tool、把结果送回来，才能拿到最终回答。其他常见值：`"end_turn"`（Claude 说完了）、`"max_tokens"`、`"stop_sequence"`。

---

## 升级 Helper Function 处理 Multi-Block

如果你之前写的 helper 默认只处理纯文本：

```python
# 旧版（纯文本）——加 tools 后会出错
def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})
```

升级成可以接受字符串或完整 `Message` 对象：

```python
from anthropic.types import Message

def add_assistant_message(messages, message):
    content = message.content if isinstance(message, Message) else message
    messages.append({"role": "assistant", "content": content})
```

这种多态处理在引入 tool 后是必需的——原本传字符串的调用点现在都要能处理 typed block list。

---

## 完整 Tool-Use 流程（单次回合）

1. 发送 user message + `tools=[...]` schema list
2. 收到 assistant message，`content = [TextBlock, ToolUseBlock]`，`stop_reason="tool_use"`
3. 迭代 `response.content`，找出 `ToolUseBlock`，提取 `id`、`name`、`input`
4. 在本地执行真正的函数
5. append 一条 user message，里面放一个 `tool_result` block，`tool_use_id` 对应刚才的 `id`
6. 再调一次 API（**仍然要带 `tools=[...]`**），拿到最终的自然语言回答

每一步都依赖完整保留 block 结构——漏掉任何一块整条链路就会断。

---

## 常见错误

1. **把 `response.content` 当字符串用**——启用 tools 后它是 typed block 的 list，要用 `response.content[0].text` 或 iterate。
2. **存历史时把 `ToolUseBlock` 丢掉**——下一回合的 `tool_result` 会引用不存在的 `id`，API 直接报 400。
3. **假设一个响应只有一个 block**——Claude 可能同一回合发说明文字 + 多个 tool-use block。
4. **follow-up 调用忘了带 `tools=[...]`**——即使你已经有 tool 结果，Claude 还是需要 schema 才能解析历史中的 tool 引用。
5. **用 index（`content[1]`）抓 tool-use block**——Claude 可能省略 text block 或调换顺序，永远要 filter `block.type == "tool_use"`。

---

> **Key Insight**
>
> 只要你在 request 里加 `tools=[...]`，就跨过了一条契约边界：响应变成异构 block list、历史必须精准保留 block 身份（特别是 `tool_use_id`）。原本假设「assistant content 是字符串」的代码会悄悄坏掉，而且错误会在后续回合以看不懂的 400 出现。从第一天就把 helper 写成能吃 `Message` 对象。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：理解 `TextBlock` vs `ToolUseBlock` 的区别，以及 `input_schema` 如何对应到 `ToolUseBlock.input`。
- **D1（Agentic Architecture）**：这一课是 agentic loop 的基础——`stop_reason == "tool_use"` 是正式的继续信号。
- 考题常会给一段把 `response.content` 当字符串处理的代码，问你哪里会出错。

---

## Flashcards

| 题目 | 答案 |
|------|------|
| 启用 tools 后 `response.content` 是什么类型？ | 一个 typed content block 的 list（`TextBlock`、`ToolUseBlock` 等） |
| `ToolUseBlock` 有哪四个字段？ | `type`、`id`、`name`、`input` |
| 哪个 `stop_reason` 值代表 Claude 要调用 tool？ | `"tool_use"` |
| 为什么必须把完整的 `response.content` append 到历史，而不能只存 text？ | 因为下一个 `tool_result` 会引用 `ToolUseBlock.id`，那个 ID 必须存在于对话历史中 |
| 如何安全地在 response 中找出 tool-use block？ | 用 `block.type == "tool_use"` 过滤，不要用 index |
| follow-up API 调用发 tool_result 时还需要带 `tools=[...]` 吗？ | 要——Claude 需要 schema 才能解析历史中的 tool 引用 |
| 把 `ToolUseBlock.input` 解包成 keyword arguments 的 Python 语法？ | `my_function(**block.input)` |
| 如果 helper 把 `response.content` 扁平化成字符串会怎样？ | 后续回合会出错，因为 `tool_result` 里的 `tool_use_id` 在历史中找不到对应 |
