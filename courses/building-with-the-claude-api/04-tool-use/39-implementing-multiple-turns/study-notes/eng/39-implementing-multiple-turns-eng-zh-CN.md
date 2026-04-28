# Implementing Multiple Turns — Engineering Deep Dive（简中）

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture (22%) / D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 1.2（agentic loop 实现）、2.4（multi-turn tool loops）、1.3（multi-turn 对话管理） |
| 来源 | building-with-the-claude-api / 04-tool-use / Lesson 39 |

---

## 一句话总结

Agentic loop 就是一个 `while True`：调用 Claude、检查 `response.stop_reason != "tool_use"` 就 break，否则执行每一个 `tool_use` block、把每个结果包成 `tool_result` block、再 loop 一次。

---

## 标准 Agentic Loop

这就是整个 agentic 生态系统建立其上的那个 pattern：

```python
def run_conversation(messages):
    while True:
        response = chat(messages, tools=[get_current_datetime_schema])
        add_assistant_message(messages, response)
        print(text_from_message(response))

        if response.stop_reason != "tool_use":
            break

        tool_results = run_tools(response)
        add_user_message(messages, tool_results)

    return messages
```

**每次迭代五个步骤：**

1. 用当前的历史和 tool schema 调用 Claude
2. 把完整的 assistant message append 到历史
3. 把 text block 显示给用户（进度指示）
4. 检查 `stop_reason`——不是 `"tool_use"` 就 break
5. 执行所有 tool-use block，把结果以 user message 的形式 append 回去

Loop 会在 `stop_reason` 不是 `"tool_use"` 时结束——通常是 `"end_turn"`，但也可能是 `"max_tokens"` 或 `"stop_sequence"`。

---

## `stop_reason` 是权威信号

Response 上的 `stop_reason` 是**唯一**可靠的信号，用来判断 Claude 还想不想用 tool：

| `stop_reason` 值 | 意思 | Loop 动作 |
|-----------------|------|-----------|
| `"tool_use"` | Claude 想跑一或多个 tool | 执行并 loop |
| `"end_turn"` | Claude 已经完成答案 | Break，返回最终响应 |
| `"max_tokens"` | 撞到输出长度上限 | Break，警告用户，可能要加 token 重试 |
| `"stop_sequence"` | 匹配到 stop sequence | Break |

不要试着从 block 内容推断。Claude 可以同一回合送出 text block **和** tool-use block；靠「response 里有 text 所以应该结束了」是经典 bug。

---

## `run_tools`——过滤再执行

`run_tools` 遍历 response content，挑出 `tool_use` block，执行每一个，并返回一个 `tool_result` block 的 list：

```python
import json

def run_tools(message):
    tool_requests = [
        block for block in message.content if block.type == "tool_use"
    ]
    tool_result_blocks = []

    for tool_request in tool_requests:
        try:
            tool_output = run_tool(tool_request.name, tool_request.input)
            tool_result_blocks.append({
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": json.dumps(tool_output),
                "is_error": False
            })
        except Exception as e:
            tool_result_blocks.append({
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": f"Error: {e}",
                "is_error": True
            })

    return tool_result_blocks
```

这个函数保留两个不变式：

1. **每个 tool-use block 都有对应的 result block**（即使失败也有）
2. **`tool_use_id` 精准回填**，让 API 能配对请求和响应

---

## `run_tool`——可扩展的 Tool Routing

`run_tool` 把 tool name 对应到实际函数。最简单是 `if/elif`，但生产系统通常用 dict-based registry：

```python
TOOL_REGISTRY = {
    "get_current_datetime": get_current_datetime,
    "add_duration_to_datetime": add_duration_to_datetime,
    # 这里注册更多 tool
}

def run_tool(tool_name, tool_input):
    if tool_name not in TOOL_REGISTRY:
        raise ValueError(f"Unknown tool: {tool_name}")
    return TOOL_REGISTRY[tool_name](**tool_input)
```

Registry pattern 让「加新 tool」变成纯数据改动——不用动 loop 逻辑本身。搭配 `run_tools`，你就有一个能扩展到几十个 tool 而不用重写结构的 agent。

---

## Loop 内的错误处理

Lesson 强调**tool 层**要做好错误处理，而不是 loop 层。当 tool 抛异常：

1. 在 `run_tools` 里面 catch 住
2. 建一个 `tool_result` block，`is_error=True`，错误字符串放 `content`
3. 继续 loop——让 Claude 决定下一步

Claude 处理错误的能力很强：它可能用修正后的参数重试、换别的 tool、或把失败回报给用户。你代码的工作只是忠实地把「发生什么事」传达出来。

**不要**试着隐藏错误或跳过失败的 block——那会破坏 `tool_use_id` 配对不变式，API 直接 400。

---

## 完整工作流程

```
┌────────────────────────────────┐
│ 用户送出问题                      │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│ chat(messages, tools=[...])    │◀───────────┐
└──────────────┬─────────────────┘            │
               ▼                              │
┌────────────────────────────────┐            │
│ add_assistant_message          │            │
│ print text_from_message        │            │
└──────────────┬─────────────────┘            │
               ▼                              │
         stop_reason                          │
        == "tool_use"?                        │
        /           \                         │
       否            是                       │
       ▼              ▼                       │
   ┌───────┐   ┌───────────────┐              │
   │ break │   │ run_tools     │              │
   └───────┘   │ (exec + wrap) │              │
               └──────┬────────┘              │
                      ▼                       │
               ┌──────────────────┐           │
               │ add_user_message │           │
               │ (tool_results)   │───────────┘
               └──────────────────┘
```

每次迭代严格交替 assistant/user message。历史会一直增长，直到 Claude 收敛到最终答案。

---

## 常见错误

1. **用 `block.type == "tool_use"` 检查取代 `stop_reason`**——平时会动，但如果 Claude 送了你不想执行的 tool_use block 就会坏
2. **执行 tool 前忘了 append assistant message**——会破坏历史顺序，下次 API 调用会被拒
3. **返回错误数量的 `tool_result` block**——每个 `tool_use` 都要对应一个 result，失败也要
4. **每次 loop 没带 `tools=[...]`**——Claude 需要 schema 才能解析历史中的 tool 引用
5. **把可以并行的 tool 串行跑**——IO-bound 的 tool 用 `asyncio.gather` 或 thread pool 可以大幅降延迟
6. **没有 max iterations**——搞混的 Claude 会无限 loop 烧 token，永远要加上限

---

> **Key Insight**
>
> Agentic loop 出奇地小——大概 15 行 Python——但它是所有 agent framework（LangChain、AutoGPT、Claude Code、MCP client）的原子单位。掌握这个 pattern，你就懂所有 tool-using agent 的运作原理。信号永远是 `stop_reason != "tool_use"`；动作永远是「执行 tool 并 loop」。其他都是生产加固：并行化、缓存、观测性、迭代上限。

---

## CCA Exam Relevance

- **D1（Agentic Architecture）**：这就是 THE agentic loop。`stop_reason` 检查和 loop 结构一定会考好几题。
- **D2（Tool Design & MCP Integration）**：理解 `run_tools` 如何过滤 block 并建 `tool_result` block。
- 主要考试情境：「怎么知道何时停止 loop」、「tool 中途失败怎么办」、「一个 response 多个 tool 调用怎么处理」。

---

## Flashcards

| 题目 | 答案 |
|------|------|
| 退出 agentic loop 的确切条件是什么？ | `response.stop_reason != "tool_use"`——不是 tool_use 就 break |
| `run_tools` 做什么？ | 过滤 content 中的 `tool_use` block、用 `run_tool` 执行每一个、返回 `tool_result` block 的 list |
| `run_tools` 怎么处理异常？ | Catch 住、建一个 `is_error=True`、错误信息在 `content` 的 `tool_result` block，继续 loop |
| 为什么要用 `TOOL_REGISTRY` dict 而不是 if/elif？ | 可扩展 routing——加新 tool 变成数据改动而非逻辑改动 |
| 把 `tool_input` dict 解包成函数关键字参数的 Python 语法？ | `tool_function(**tool_input)` |
| 如果 `tool_result` block 比 `tool_use` block 少会怎样？ | API 会 400，说 `tool_use_id` 配对少了 |
| 为什么 `add_assistant_message` 要在执行 tool 之前？ | 保持历史顺序——assistant message 必须先存在，user tool-result message 才能引用它 |
| 生产 agentic loop 必须加的最低限度安全机制是什么？ | `max_iterations` 上限，防止 Claude 失控产生无限 loop |
