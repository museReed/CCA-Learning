# Agents 与 Tools — Engineering 深度解析

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture (22%) |
| Task Statements | 1.1 (agent 架构)、1.2 (agentic loop)、1.3 (agent 中的 tool use)、5.1 (production pattern 选型) |
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 81 |

---

## 一句话总结

Agent = Claude + 一组抽象、可组合的 tools,跑在 agentic loop 里面;相较于 workflow 预先写死的步骤顺序,agent 让 Claude 自己在执行时决定该调用哪些 tool、以什么顺序调用,以完成用户给的目标。

---

## Workflow vs Agent:核心差异

在 workflow 里,开发者把 tool 调用顺序写死在代码中:"先 A,再 B,再 C"。控制流由开发者拥有。

在 agent 里,你只给 Claude 一个目标 + 一个工具箱,控制流由 Claude 决定。同一份 agent 代码可以处理"现在几点?"和"下周三早上七点提醒我去健身房",你的 Python 代码里完全没有 if/else 分支。

```python
# Workflow:由开发者控制顺序
def schedule_reminder(task, when):
    now = get_current_datetime()
    target = add_duration_to_datetime(now, when)
    return set_reminder(task, target)

# Agent:由 Claude 控制顺序
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[get_current_datetime, add_duration_to_datetime, set_reminder],
    messages=[{"role": "user", "content": "下周三提醒我去健身房"}]
)
# Claude 自己决定:get_current_datetime -> add_duration_to_datetime -> set_reminder
```

---

## Datetime 例子 — Emergent Tool Chaining

三个简单的 tools:

- `get_current_datetime` — 返回当前日期时间
- `add_duration_to_datetime` — 返回 `datetime + duration`
- `set_reminder` — 在指定时间创建提醒

看 Claude 怎么把这三个 tool 组合成不同行为:

| 用户请求 | Tool 序列 |
|----------|-----------|
| "现在几点?" | `get_current_datetime` |
| "11 天后是星期几?" | `get_current_datetime` -> `add_duration_to_datetime` |
| "下周三提醒我去健身房" | `get_current_datetime` -> `add_duration_to_datetime` -> `set_reminder` |
| "我的 90 天保修什么时候到期?" | 先问用户购买日期,再串接 tools |

这个 agent 并没有被明确编程去识别"下周三"或"90 天保修"——是 Claude 的推理能力把自然语言转成正确的 tool 链。这叫做 **emergent composition**,也是 agent 存在的全部理由。

---

## 设计原则:抽象的 Tool 胜过专用的 Tool

在 agent 系统中,tool 设计的首要原则是:**选择 primitive、抽象的 tool,不要选窄、专门的 tool**。Claude Code 是最佳示范:

| 有的 tool | 没有的 tool |
|-----------|-------------|
| `bash`(执行任何 shell 命令) | `install_npm_dependency` |
| `read`(读任何文件) | `read_python_imports` |
| `write`(写任何文件) | `create_react_component` |
| `edit`(修改文件) | `refactor_function` |
| `glob` / `grep` | `find_unused_variables` |

六个 primitive 让 Claude 可以重构代码、安装依赖、跑测试、写 migration、做 security audit——这些是 Claude Code 开发团队从来没明确规划过的情境。如果换成 `refactor_function` 这种专用 tool,只能处理一种窄情境,其他场景全部失效。

**心法**:如果一个 tool 可以用 Unix 动词描述,那它大概就在对的抽象层级。

---

## 设计可组合的 Tool Set

一个设计良好的 agent tool set,是少量可以 **组合** 的 primitive。例子:social media video agent。

```python
tools = [
    {
        "name": "bash",
        "description": "执行 shell 命令,包括 FFMPEG 视频处理",
        "input_schema": {"type": "object", "properties": {"command": {"type": "string"}}}
    },
    {
        "name": "generate_image",
        "description": "从 text prompt 生成图片",
        "input_schema": {"type": "object", "properties": {"prompt": {"type": "string"}}}
    },
    {
        "name": "text_to_speech",
        "description": "把文字转成音频文件",
        "input_schema": {"type": "object", "properties": {"text": {"type": "string"}, "voice": {"type": "string"}}}
    },
    {
        "name": "post_media",
        "description": "把媒体文件上传到社交平台",
        "input_schema": {"type": "object", "properties": {"file_path": {"type": "string"}, "platform": {"type": "string"}}}
    }
]
```

这组 tool 可以支持:

- "发一条做菜视频" -> image + TTS + bash(FFMPEG) + post_media
- "先生成一个示例图给我看,等我确认再继续" -> image,暂停等 feedback,再继续
- "再好笑一点" -> 用不同的 prompt 重新生成

这些流程都没有被写死。它们是 agent 针对同一组四个 tool 推理出来的结果。

---

## Agentic Loop(Runtime 视角)

```python
messages = [{"role": "user", "content": user_goal}]
while True:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        tools=tools,
        messages=messages
    )
    messages.append({"role": "assistant", "content": response.content})

    if response.stop_reason == "end_turn":
        break

    if response.stop_reason == "tool_use":
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })
        messages.append({"role": "user", "content": tool_results})
```

这个 loop 就是 agent 的全部。你不需要预先决定会跑几轮—— Claude 通过 `stop_reason == "end_turn"` 自己决定何时结束。

---

## 常见错误

1. **Tool 过度专用化** — 写 `refactor_python_class` 而不是 `edit`。你用一个可用场景换来几十个破损场景。
2. **没有 loop 终止保护** — 让 agent 无限跑下去。永远要设最大迭代数(例如 25)避免失控的 cost。
3. **把 agent 当伪装的 workflow 使用** — 如果你发现自己在写 `if tool_name == X: 强制调用 Y`,那你要的是 workflow,不是 agent。
4. **Tool 描述太模糊** — Claude 只能选它看得懂的 tool。把描述写得像在 onboard 新工程师一样清楚。
5. **忘记 tool_results 是 user role 的消息** — 在 Anthropic API 里,tool result 是用 `role: "user"` 发回去的,不是独立的 role。

> **Key Insight**
>
> Agent 适合在"你没办法事先列出步骤"的情境。给 Claude 小、抽象、可组合的 tool 加上清楚的目标,然后让 agentic loop 去组合。开发者的工作从"写控制流"变成"设计对的工具箱"。

---

## CCA 考试关联

- **D1 (Agentic Coding & Architecture)**:会考"agent 跟 workflow 差在哪"、"哪个 tool 设计支持 agent"。答案几乎永远是比较抽象的 primitive。
- **D5 (Enterprise Deployment)**:Agent 比较难做 eval 而且每个任务成本较高——这些 trade-off 要记住。
- 题目里看到这些关键字:"unpredictable requests""varied tasks""creative combination" -> agent;"known sequence""repeatable""reliable" -> workflow。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Agent 跟 workflow 最关键的差别是什么? | Workflow 里开发者把 tool 顺序写死;Agent 里 Claude 在 runtime 根据目标决定 tool 顺序。 |
| 为什么 agent tool 要设计成抽象而不是专用? | 抽象 tool(bash、read、edit)可以组合出开发者从没预期的情境;专用 tool(refactor_function)只对一种情境有效。 |
| 举三个 Claude Code 的 primitive tool。 | bash、read、write、edit、glob、grep(任选三个)。 |
| Agent 收到"我的 90 天保修什么时候到期?"会怎么处理? | 它会识别出缺少信息,先问用户购买日期,然后串接 get_current_datetime 和 add_duration_to_datetime。 |
| 哪个 stop_reason 表示 agent 想调用 tool? | `tool_use` |
| 哪个 stop_reason 表示 agentic loop 该结束? | `end_turn` |
| 在 Anthropic API 里,tool_result content block 是用哪个 role 发回给 Claude? | `user` |
| 每个 production agent loop 都该有什么保护? | 最大迭代数限制,避免失控的 cost 和无限循环。 |
