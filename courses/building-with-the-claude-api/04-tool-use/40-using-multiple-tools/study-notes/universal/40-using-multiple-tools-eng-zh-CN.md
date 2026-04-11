# 使用多个 Tools — Engineering Deep Dive

| 项目 | 内容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%)、D1 — Agentic Architecture (22%) |
| Task Statements | 2.1（tool schema 与选择）、1.2（tool 编排）、2.4（多轮 tool loop） |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 40 |

---

## One-Liner

Claude 可以在一次对话中自行选择并串联多个 tools；只要已经搭好核心的 tool-handling 基础架构（schema 列表 + router 函数），新增 tool 就是一个简单的四步模式,成本随 tool 数量线性增长。

---

## 核心模式

从单个 tool 扩展到多个 tools,每新增一个 tool 只需做四件事：

1. 实现 Python 函数
2. 定义 JSON schema
3. 把 schema 添加到 `tools=[...]` 列表
4. 在 tool router 添加 `elif` 分支

外层的 agentic loop 完全不用改。原有的 `stop_reason == "tool_use"` 判断与 message 累积逻辑都继续有效。

---

## 示例：三个 tool 的提醒 Agent

```python
tools = [
    get_current_datetime_schema,
    add_duration_to_datetime_schema,
    set_reminder_schema,
]

def run_tool(tool_name: str, tool_input: dict):
    if tool_name == "get_current_datetime":
        return get_current_datetime(**tool_input)
    elif tool_name == "add_duration_to_datetime":
        return add_duration_to_datetime(**tool_input)
    elif tool_name == "set_reminder":
        return set_reminder(**tool_input)
    else:
        raise ValueError(f"未知 tool: {tool_name}")

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    messages=messages,
)
```

Router 本质上是一个 dispatch table；当 tool 数量超过 5 个时,建议改用 dict registry：

```python
TOOL_REGISTRY = {
    "get_current_datetime": get_current_datetime,
    "add_duration_to_datetime": add_duration_to_datetime,
    "set_reminder": set_reminder,
}

def run_tool(tool_name, tool_input):
    return TOOL_REGISTRY[tool_name](**tool_input)
```

---

## Claude 如何选择 Tool

列表中有多个 tools 时,Claude 会读取每个 schema 的 `name` 和 `description`,然后结合当前对话上下文决定调用哪个（或不调用）。选择依据包括：

- **Description 质量** — 清晰、动作导向的描述胜过模糊描述
- **输入参数名称** — 命名清楚的参数减少歧义
- **用户请求用词** — "提醒我" 明显对应到 `set_reminder`
- **链式依赖** — 如果某 tool 需要的数据还没有,Claude 可能先调用另一个 tool 来获取

这也是为什么 tool description 和实现本身一样重要。

---

## 链式调用与 Agentic Loop

示例 prompt：*"帮我设定看医生的提醒,在 2050 年 1 月 1 日之后的第 177 天。"*

Claude 通常会跨多轮生成多个 tool_use block：

1. **Turn 1** — Claude 发出 `add_duration_to_datetime(start="2050-01-01", days=177)` 的 `tool_use`
2. **你的代码**执行函数、返回 `"2050-06-27"` 作为 `tool_result`
3. **Turn 2** — Claude 收到结果后发出 `set_reminder(date="2050-06-27", description="doctor appointment")`
4. **你的代码**执行函数、返回确认消息
5. **Turn 3** — Claude 发出最后的 `text` block,总结做了什么

Agent loop 会持续调用 API,直到 `stop_reason != "tool_use"`。

---

## Parallel vs. Sequential Tool Calls

一个 assistant message **可以同时包含多个 tool_use block（parallel）**,前提是这些 tool 彼此独立。例如用户问"东京天气怎么样,同时 AAPL 现在股价多少？",Claude 可能在同一个 response 中同时发出 `get_weather` 和 `get_stock_price`。你必须执行每一个,并在**单个 user message** 中一次返回**所有** `tool_result` block。

```python
# 从 assistant turn 收集所有 tool_use block
tool_uses = [b for b in response.content if b.type == "tool_use"]

# 执行并构建 tool_result block
tool_results = [
    {
        "type": "tool_result",
        "tool_use_id": tu.id,
        "content": str(run_tool(tu.name, tu.input)),
    }
    for tu in tool_uses
]

# 在单个 user message 中发送全部结果
messages.append({"role": "user", "content": tool_results})
```

相比之下,Sequential chaining（Tool A 的结果喂给 Tool B）需要多次 API 往返,会以多个 turn 的形式累积在 `messages` 中。

---

## Multi-Tool 请求的 Message 结构

多 tool 请求的对话历史如下：

```
user:      "177 天后设提醒"
assistant: [text "我得先算日期"] + [tool_use add_duration_to_datetime]
user:      [tool_result "2050-06-27"]
assistant: [text "现在设置提醒"] + [tool_use set_reminder]
user:      [tool_result "已设置"]
assistant: [text "完成,提醒定在 2050 年 6 月 27 日"]
```

注意 assistant message 可以同时包含 text block 和 tool_use block。回放历史时**不要把 text block 丢掉** — Claude 会把它们当作推理上下文。

---

## Common Mistakes

1. **忘了注册 schema** — 函数和 router case 都写好了,但忘了加进 `tools=[...]` 列表,Claude 永远不知道这个 tool 存在。
2. **Router 对未知 tool 静默忽略** — 遇到未知 name 应该直接 raise,让 schema 拼写错误立刻暴露,而不是静默返回 `None`。
3. **Claude 同时发多个 parallel tool_use,但只回了一个 tool_result** — API 会报错,因为 tool_use_id 集合对不上。
4. **把 assistant message 的 text block 丢掉** — assistant 的 content 是 block list,加入历史时要保留所有 block。
5. **Tool description 太模糊** — "helper tool""utility" 这类描述会让 Claude 选错 tool,应该写动作导向的描述:"Adds a duration in days to a starting datetime"。

> **Key Insight**
>
> N 个 tool 的 agentic loop 与 1 个 tool 的 loop 完全相同。只要 `stop_reason == "tool_use"` 处理正确,扩展纯粹就是注册更多 schema 和 dispatch case。架构成本是固定的,唯一的变动成本是写出高质量的 tool description。

---

## CCA Exam Relevance

- **D2 (Tool Design)**：理解 Claude 如何基于 schema 和 description 在多个 tool 之间做选择,常考 tool dispatch 模式。
- **D1 (Agentic Architecture)**：识别 parallel tool_use 场景,并知道必须在单个 user turn 中返回所有 tool_result。
- **Task 2.4（多轮 tool loop）**：追踪链式 tool-use 序列并指出 loop 在哪里终止,是常见题型。

---

## Flashcards

| Front | Back |
|-------|------|
| 给 multi-tool agent 新增一个 tool 的四个步骤？ | 1) 实现函数 2) 定义 schema 3) 加入 tools 列表 4) 加上 router case |
| Claude 如何在多个 tool 之间做选择？ | 基于每个 tool 的 name、description、参数名称以及当前对话上下文 |
| 一个 assistant message 可以包含多个 tool_use block 吗？ | 可以,parallel 调用会以多个 tool_use block 的形式出现在同一个 response,必须在一个 user message 中全部回复 |
| 每个返回的 tool_result 必须带什么？ | 对应 assistant tool_use block 的 `tool_use_id` |
| Agentic loop 什么时候停止？ | 当 `stop_reason` 不再是 `"tool_use"`（通常变成 `"end_turn"`） |
| 为什么要保留 assistant turn 的 text block？ | Claude 会把它们当作推理上下文,删掉会让后续轮次变差 |
| 大型 `if/elif` router 的可扩展替代方案？ | 用 dict 构造 tool registry,把 name 映射到 callable |
| Tool description 过于模糊有什么风险？ | Claude 可能选错 tool 或误用,导致错误的 tool 调用 |
