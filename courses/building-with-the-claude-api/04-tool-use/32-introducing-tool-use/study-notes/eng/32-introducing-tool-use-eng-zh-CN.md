# 介绍 Tool Use — Engineering Deep Dive

| 项目 | 内容 |
|------|------|
| 考试 Domain | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 1.2（agentic loop 基础）、2.1（tool schema 设计）、2.4（multi-turn tool loop） |
| 来源 | building-with-the-claude-api / 04-tool-use / Lesson 32 |

---

## 一句话总结

Tool use 是一套结构化的 request/response 协议，让 Claude 能主动请求你的应用去获取外部数据或执行动作，填补训练数据与实时世界之间的鸿沟。

---

## 没有 Tools 时的问题：静态知识的边界

没有 tools，Claude 就被训练截止日期锁死。用户问「旧金山现在天气如何？」只会得到：

> 「抱歉，我无法访问最新的天气信息。」

这是能力的墙，不是 prompt 写不好的问题。再怎么调 prompt 也变不出训练数据里没有的实时信息。同样的墙出现在：

- 实时股价、赛事比分、新闻头条
- 公司内部数据库与 CRM 记录
- 用户个人状态（日程、文件、偏好）
- 任何需要真实世界副作用的操作（发邮件、写文件、触发 workflow）

Tools 是架构层面的答案：与其用 prompt 绕过限制，不如通过结构化方式**扩展** Claude 的能力，让它能向你的代码求助。

---

## Tool Use 的四步骤流程

```
┌──────────┐   1. 用户问题 + 工具定义            ┌─────────┐
│  Client  │ ─────────────────────────────────▶ │ Claude  │
│  (app)   │                                     │   API   │
│          │ ◀──────────────────────────────────│         │
│          │   2. tool_use request (name + args) └─────────┘
│          │
│          │   3. 本地执行 function
│          │
│          │   4. tool_result 带回结果           ┌─────────┐
│          │ ─────────────────────────────────▶ │ Claude  │
│          │ ◀──────────────────────────────────│   API   │
│          │   5. 最终自然语言回复                └─────────┘
└──────────┘
```

1. **初始请求** — 把用户问题加上可用工具列表（name、description、input_schema）POST 到 `/v1/messages`。
2. **工具请求** — Claude 的 `stop_reason` 返回 `"tool_use"`，`content` 里会有 `tool_use` block，包含 `id`、`name`、`input`（JSON 参数）。
3. **本地执行** — 你的服务器读 tool_use block，调用对应的 Python 函数，拿到结果。
4. **最终回复** — 把 assistant 消息与一条新的 user 消息（含 `tool_result` block，用 `tool_use_id` 对应）追加进去，再调一次 API。Claude 综合所有信息产生最终答案。

---

## 最小可行 Python 示例

```python
from anthropic import Anthropic

client = Anthropic()

tools = [{
    "name": "get_weather",
    "description": "返回指定城市的当前天气。",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "城市名，例如 San Francisco"}
        },
        "required": ["city"]
    }
}]

messages = [{"role": "user", "content": "旧金山现在天气怎么样？"}]

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    messages=messages,
)

if response.stop_reason == "tool_use":
    tool_use = next(b for b in response.content if b.type == "tool_use")
    result = fetch_weather(tool_use.input["city"])  # 你的函数

    messages.append({"role": "assistant", "content": response.content})
    messages.append({
        "role": "user",
        "content": [{
            "type": "tool_result",
            "tool_use_id": tool_use.id,
            "content": result,
        }],
    })

    final = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )
    print(final.content[0].text)
```

核心观念：**tool use 是 multi-turn**。一个用户问题通常会跨越两次（或更多）API 调用。

---

## 为什么 Tools 比 Fine-tune 更适合实时数据

| 方式 | 新鲜度 | 成本 | 运维 |
|------|--------|------|------|
| Fine-tune 最新数据 | 数小时到数天 stale | 高（retrain） | 持续 retrain |
| RAG（vector search） | 看 index 更新频率 | 中（embedding + 存储） | 需维护 index pipeline |
| **Tool use** | 实时 — 直接打 live source | 按次计费 | 零 — source of truth 在上游 |

Tools 是唯一一种让 Claude 直接读取系统真实来源的模式。不缓存、不过期。

---

## 关键优势

- **实时信息** — 获取训练数据里没有的最新数据
- **外部系统集成** — 对接数据库、SaaS API、内部服务
- **动态响应** — 每次答案都基于最新状态
- **结构化交互** — Claude 通过 `input_schema` 明确声明它要什么
- **可执行动作** — tools 不只读取，还能写入，这是 Claude 变成 agent 的关键

---

## 常见错误

1. **忘了第二次 API 调用** — 把 `tool_use` block 直接返回给用户，没有实际执行并把结果送回 Claude。
2. **`tool_use_id` 对不上** — `tool_result` 必须引用原始 `tool_use` 的 `id`，否则 Claude 会断开 context。
3. **用字符串传递 assistant 消息** — assistant message 的 `content` 必须保留完整数组，不可压成纯文本。
4. **以为 tools 是可有可无** — 需要实时数据时，没有 prompt engineering 的替代方案，只能用 tools。
5. **没处理 `stop_reason`** — 要分支判断是否进入下一轮 loop，或直接回最终答案。

> **Key Insight**
>
> Tool use 不是单次 API call，而是**一个 loop**。每一轮检查 `stop_reason`，若是 `tool_use` 就本地执行、附上 `tool_result`，再调一次 API。这个 loop 是 CCA 整个 agentic 章节的基础。搞懂它就同时解锁 D1（agents）与 D2（tool design）。

---

## CCA 考试重点

- **D2（Tool Design & MCP Integration）**：tool_use request/response 流程、`tool_use` 与 `tool_result` block 类型、`input_schema` 即为 JSON Schema。
- **D1（Agentic Architecture）**：tool use 这个 loop 就是最小的 agentic loop。Multi-turn tool call 是更复杂 agent pattern 的起点。
- 考题常见场景：「Claude 需要实时天气」→ 答案永远是 tools，不是 prompt engineering。

---

## Flashcards

| Front | Back |
|-------|------|
| Tool use 解决什么问题？ | Claude 训练截止的限制 — 让它能获取实时数据与外部系统，补上模型原本不知道的信息。 |
| 哪个 `stop_reason` 代表 Claude 想调用工具？ | `"tool_use"` |
| Claude 要求工具时会返回什么 content block？ | `tool_use` block，含 `id`、`name`、`input`（JSON 参数）。 |
| 你的 app 如何把工具结果回传给 Claude？ | 发一条新的 user message，里面放 `tool_result` block，用 `tool_use_id` 对应原 tool_use。 |
| 一次 tool use round trip 最少要几次 API call？ | 至少两次 — 一次收 tool_use 请求，一次送 tool_result 拿最终答案。 |
| Tool use 的四个步骤是？ | 1) 初始请求带 tools，2) Claude 返回 tool_use，3) 本地执行，4) 返回 tool_result，Claude 产出最终答案。 |
| 为何 prompt engineering 替代不了 tools 的实时数据需求？ | 因为那些数据从来没在训练数据里 — 再怎么 prompt 都生不出来。 |
| Tools 能有副作用吗？ | 可以 — tools 能读（天气 API）也能写（发邮件、创建记录），这正是 Claude 变成 agent 的关键。 |
