# Tool Choice 参数 — 工程深度解析

| 项目 | 内容 |
|------|------|
| 考试范围 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| 任务陈述 | 2.1（tool schema 设计）、2.2（content blocks）、1.2（agentic loop 控制） |
| 来源 | 补充教材 — 填补 building-with-the-claude-api / 04-tool-use 的课程空缺 |

---

## 一句话总结

`tool_choice` 是 Claude 工具调用行为的方向盘 — 让你声明 Claude 在这一轮"可以"、"必须"或"不可以"调用工具，并可选择性指定调用哪一个工具。

---

## 四种模式

| 模式 | 语法 | 行为 | `stop_reason` |
|------|------|------|---------------|
| `auto` | `{"type": "auto"}` | **默认值。** Claude 自行决定是否调用工具。响应可能是 TextBlock（对话）或 ToolUseBlock。 | `end_turn` 或 `tool_use` |
| `any` | `{"type": "any"}` | Claude 必须调用其中一个提供的工具，由它自己挑选。响应一定是 ToolUseBlock。 | `tool_use` |
| `tool` | `{"type": "tool", "name": "get_weather"}` | 强制 Claude 调用某个指定名称的工具。 | `tool_use` |
| `none` | `{"type": "none"}` | 停用本轮的工具调用；Claude 只会以纯文本响应。 | `end_turn` |

### `auto` — 让 Claude 决定

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "auto"},  # 等同于省略 tool_choice
    messages=messages,
)
```

最适合通用 agent 与聊天界面。Claude 决定要调用工具时，会先产出自然的 chain-of-thought 推理文本，让你看得到它的思路。

### `any` — Claude 必须调用某个工具

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "any"},
    messages=messages,
)
# response.content[0].type == "tool_use" — 保证成立
```

最适合每一轮都必须产出结构化动作的工作流。Claude 仍然会根据消息自行挑工具，但无法逃逸到纯文本响应。

### `tool` — 强制使用特定工具

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "tool", "name": "extract_invoice"},
    messages=messages,
)
```

最适合结构化数据抽取 — 该工具的 `input_schema` 就变成一份有类型的输出契约。这是 Claude API 中最接近"JSON mode"的惯用做法。

### `none` — 本轮停用工具

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,  # 仍然声明
    tool_choice={"type": "none"},
    messages=messages,
)
```

在 agent loop 里面很好用 — 当你想让 Claude 总结、反思，或在所有工具结果都收集完毕后产出最终给用户看的文本时，用这个模式阻止它又去调用工具。

---

## 与 `stop_reason` 的交互

tool_choice 模式会直接决定你必须处理哪些 `stop_reason`：

| 模式 | 可能的 `stop_reason` | 你的代码必须处理的分支 |
|------|----------------------|------------------------|
| `auto` | `end_turn`、`tool_use`、`max_tokens`、`stop_sequence` | 两大分支：纯文本响应 vs 工具调用 |
| `any` | `tool_use`（加上 `max_tokens` 边界情况） | 单一分支：永远执行工具 |
| `tool` | `tool_use`（加上 `max_tokens` 边界情况） | 单一分支：永远执行被强制的工具 |
| `none` | `end_turn`、`max_tokens`、`stop_sequence` | 单一分支：只有纯文本响应 |

这对 loop 控制很重要。使用 `auto` 时，你的 agent loop 在 `end_turn` 时退出。使用 `any` 时，loop 只能通过切换到 `auto` 或 `none`，或是你的代码根据工具结果判定为终止状态来中止。

---

## `disable_parallel_tool_use`

```python
tool_choice={"type": "any", "disable_parallel_tool_use": True}
```

默认情况下，Claude 在单次响应中可以发出多个 `tool_use` block（parallel tool use）。设为 `disable_parallel_tool_use: true` 会强制**每轮最多只能有一个** `tool_use` block。

- 与 `any` 或 `tool` 搭配，适合需要严格"一次一个动作"的场景（状态机、事务型流程）。
- 与 `auto` 搭配也合法 — 当你的执行器无法安全地并行调用工具时很有用。
- 代价：失去了并行调用带来的延迟优势。

---

## 何时用哪个模式 — 决策指南

```
有时需要实时数据、有时纯聊天？              → auto
每一轮都必须产出结构化动作？                 → any
从非结构化输入中抽取有类型数据？             → tool（指定名称）
Agent loop 中的总结/反思轮？                 → none
严格一次一个动作的状态机？                   → any + disable_parallel_tool_use
```

---

## 常见错误

1. **在聊天 agent 上用 `any`** — 会在每一轮都强制工具调用，包含"你好""谢谢"这种闲聊，产出毫无意义的 tool_use block。
2. **预期 `tool` 或 `any` 模式会产出 chain-of-thought** — 当 Claude 被强制调用工具时，不会在 tool_use block 之前输出推理文本，你会失去可观察性。只有 `auto` 允许自然的 CoT。
3. **忘了 `none` 模式仍然需要声明 `tools=`** — 工具列表还是要带；`none` 只是停用本轮的调用行为。
4. **以为 `auto` 在有工具可用时一定会调用** — `auto` 代表 Claude 可以"选择不调用"。如果你的使用场景一定要调用工具，请用 `any` 或 `tool`。
5. **执行器不支持并行时没设 `disable_parallel_tool_use`** — Claude 可能同时发出两个 tool_use block，你的串行执行器会卡死或造成状态重复应用。

---

> **关键洞察**
>
> `tool_choice` 是你把 Claude 从"对话助理"转换成"确定性组件"的开关。`auto` 把方向盘交给 Claude（灵活、推理透明）；`any`/`tool` 把方向盘交回给你的代码（结构化、保证动作，但推理不透明）。选对模式是在"灵活性"与"控制力"之间做 trade-off — 而这个 trade-off 正是 CCA D1（agent 设计）与 D2（tool 设计）的核心。

---

## CCA 考试相关性

- **D2（Tool Design & MCP Integration）**：四种模式的语法、行为与使用时机都是直接可考的。预期会看到"哪个 `tool_choice` 设定能保证 Claude 会调用工具？"这类题目。
- **D1（Agentic Architecture）**：`tool_choice` 控制 loop 的终止与结构。用 `none` 做总结轮、用 `any` 做动作轮是核心的 agent pattern。
- **陷阱题**：考题可能描述一个"JSON 抽取"场景 — 正确答案是 `{"type": "tool", "name": "..."}`，不是 `any`，也不是靠 prompt 技巧。

---

## 闪卡

| 正面 | 背面 |
|------|------|
| `tool_choice` 的默认值是什么？ | `{"type": "auto"}` — Claude 自行决定是否调用工具。 |
| 哪个 `tool_choice` 模式能保证 Claude 会调用工具？ | `{"type": "any"}` — Claude 必须从提供的工具中挑一个。 |
| 如何强制 Claude 调用某个指定名称的工具？ | `{"type": "tool", "name": "<tool_name>"}` |
| `{"type": "none"}` 的作用是什么？ | 停用本轮的工具调用；Claude 只会以纯文本响应，`stop_reason` 为 `end_turn`。 |
| 哪个模式会保留 Claude 在工具调用前的 chain-of-thought 推理？ | 只有 `auto`。`any` 与 `tool` 会抑制推理文本，直接输出 tool_use block。 |
| `tool_choice: auto` 下可能的 `stop_reason` 有哪些？ | `end_turn`（文本响应）或 `tool_use`（工具调用）。 |
| `disable_parallel_tool_use: true` 强制了什么？ | 每轮最多只能有一个 `tool_use` block，即使 Claude 本来可以并行调用多个工具。 |
| 什么时候会在 agent loop 中使用 `tool_choice: none`？ | 在所有工具结果都收集完后的总结/反思轮，强制产出最终文本答案。 |
| 为什么 `any` 不适合通用聊天 agent？ | 它会在每一轮都强制工具调用，连闲聊都会产出毫无意义的 tool_use block。 |
| Claude API 中最接近"JSON mode"的 `tool_choice` 模式是哪个？ | `{"type": "tool", "name": "..."}` — 工具的 `input_schema` 就是有类型的输出契约。 |
