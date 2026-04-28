# Sending Tool Results — Engineering Deep Dive（简中）

| 项目 | 内容 |
|------|------|
| 考试领域 | D2 — Tool Design & MCP Integration (18%) / D1 — Agentic Architecture (22%) |
| Task Statements | 2.4（tool_result block 格式）、2.2（content block 处理）、1.2（收尾 tool-use loop） |
| 来源 | building-with-the-claude-api / 04-tool-use / Lesson 37 |

---

## 一句话总结

Tool 执行结果要通过 `tool_result` content block 包在一条 **user** message 里送回 Claude，每个 result 都要用 `tool_use_id` 精准对应前面 `ToolUseBlock.id`。

---

## 从 Tool 请求到执行

当 Claude 送回一个 `ToolUseBlock` 后，你用 block 的 `input` dict 去调用本地函数。Python 的 `**` 解包会把 dict 变成关键字参数：

```python
tool_block = response.content[1]  # 例如 [TextBlock, ToolUseBlock]
result = get_current_datetime(**tool_block.input)
# 等同 get_current_datetime(format="HH:MM:SS")
```

`input` dict 保证符合 tool 的 `input_schema`（假设 Claude 遵守规则），所以 unpacking 就是 JSON Schema 和你函数签名之间的标准桥梁。

---

## `tool_result` Block 的结构

`tool_result` block 是 user role 下的 content block，只有这几个字段：

| 字段 | 类型 | 用途 |
|------|------|------|
| `type` | 字面量 `"tool_result"` | 告诉 API 这个 block 是 tool 返回 |
| `tool_use_id` | 字符串 | 必须对应前面 `ToolUseBlock` 的 `id` |
| `content` | 字符串或 block list | 你 tool 的输出，序列化后的内容 |
| `is_error` | 布尔 | tool 失败就填 `True`，Claude 会据此处理错误 |

```python
messages.append({
    "role": "user",
    "content": [{
        "type": "tool_result",
        "tool_use_id": response.content[1].id,
        "content": "15:04:22",
        "is_error": False
    }]
})
```

关键不变式：**前一条 assistant message 里的每一个 `ToolUseBlock` 都必须在下一条 user message 中对应一个 `tool_result`**。API 会严格验证这个配对，不符就报 400。

---

## Content 序列化规则

`content` 字段可以接字符串或 block list。非 trivial 的数据请序列化成 JSON：

```python
import json

tool_output = {"time": "15:04:22", "timezone": "UTC", "epoch": 1762978180}
result_block = {
    "type": "tool_result",
    "tool_use_id": tool_block.id,
    "content": json.dumps(tool_output),
    "is_error": False
}
```

Claude 被训练成能读 tool result 里的 JSON 字符串，所以结构化数据就用 `json.dumps`。二进制数据（图片、文件）则要用 list-of-blocks 形式，内部放 image block。

---

## 同一回合处理多个 Tool Call

如果 Claude 在一次响应里要了超过一个 tool（例如「10+10 是多少？30+30 是多少？」会产生两个 `ToolUseBlock`），你必须在**单一一条 user message** 里送回**所有**对应的 `tool_result` block：

```python
tool_use_blocks = [b for b in response.content if b.type == "tool_use"]

tool_results = []
for tub in tool_use_blocks:
    output = run_tool(tub.name, tub.input)
    tool_results.append({
        "type": "tool_result",
        "tool_use_id": tub.id,
        "content": json.dumps(output),
        "is_error": False
    })

messages.append({"role": "user", "content": tool_results})
```

Result 在 content list 里的顺序不重要——靠 `tool_use_id` 配对。但**不能漏**：少一个就会 400。

---

## 用 `is_error` 处理错误

Tool 抛异常时，不能省略 result block。改成填 `is_error: True`，把错误信息放进 `content`：

```python
try:
    output = run_tool(tub.name, tub.input)
    block = {
        "type": "tool_result",
        "tool_use_id": tub.id,
        "content": json.dumps(output),
        "is_error": False
    }
except Exception as e:
    block = {
        "type": "tool_result",
        "tool_use_id": tub.id,
        "content": f"Error: {e}",
        "is_error": True
    }
```

Claude 会读错误信息，可能重试不同参数、把失败回报给使用者、或选另一种策略。默默丢掉失败的 tool 会破坏 ID 配对，直接 400。

---

## Follow-Up API 调用

后续 request 必须：

1. 带完整的对话历史（原始 user message + assistant tool-use message + 新的 user tool-result message）
2. 仍然要带 `tools=[...]`——Claude 需要 schema 去解析 tool 引用
3. 用同一个 `model` 和 `max_tokens` 配置

```python
client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,  # 已经有 3 条以上的 message，包含 tool-result
    tools=[get_current_datetime_schema]
)
```

Claude 下一个响应会把 tool 输出整合成自然语言。如果它还要调用别的 tool，就再 loop 一次。

---

## 常见错误

1. **把 `tool_result` 放在 assistant message**——必须放在 **user** role message，assistant role 的 tool result 会被拒绝。
2. **漏 `tool_use_id`** 或填错值——API 会报 400「mismatched tool_use_id」。
3. **`content` 直接塞 dict/object** 而没序列化——`content` 必须是字符串（或 block list），结构化数据请 `json.dumps`。
4. **忘记填 `is_error`**——默认是 `False`，失败时没填就等于告诉 Claude 成功，会导致 hallucination。
5. **Claude 要多个 tool 但只回一个结果**——每个 `ToolUseBlock` 都要在同一回合有对应的 `tool_result`。
6. **follow-up 没带 `tools=[...]`**——Claude 会拒绝引用不存在 schema 的历史。

---

> **Key Insight**
>
> `tool_use_id` 是你代码和 Claude 之间的契约。Assistant 送出的每一个 `ToolUseBlock` 都必须在下一条 **user** message 中有**恰好一个**对应 ID 的 `tool_result`。把它想成是 content block 层级的请求/响应配对，而不是 message 层级——而且即使是错误也要用 `is_error: True` 的 `tool_result` 送回去，不能整个 block 不送。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：记住 `tool_result` block 的四个字段，以及它在哪个 role（`user`）里。
- **D1（Agentic Architecture）**：把请求/结果配对理解成 agentic loop 的基本单位。
- 考题会丢坏掉的 `tool_result`（错 role、漏 ID、塞 dict）问你会出什么错。

---

## Flashcards

| 题目 | 答案 |
|------|------|
| `tool_result` block 要放在哪个 role 的 message 里？ | `user` role——Claude 把 tool result 看成用户提供的 context |
| `tool_result` block 哪个字段用来配对前面的 tool-use 请求？ | `tool_use_id`——必须精准对应 `ToolUseBlock.id` |
| `tool_result` 的 `content` 字段类型是什么？ | 字符串（或给图片/文件用的 block list）——结构化数据用 `json.dumps` |
| Tool 抛异常时 `is_error` 要设什么？ | `True`——并把错误信息放进 `content`，不要直接丢掉 block |
| 把 `ToolUseBlock.input` 解包成关键字参数的 Python 语法？ | `my_function(**tool_block.input)` |
| Claude 要两个 tool 但你只回一个 result 会怎样？ | API 会 400，说 `tool_use_id` 配对失败 |
| follow-up API 调用还需要带 `tools=[...]` 吗？ | 需要——Claude 要 schema 才能解析对话历史中的 tool 引用 |
| 一回合有多个 tool call 怎么处理？ | 全部执行、收集每个 `tool_result` block、用**单一**一条 user message 一起送回去 |
