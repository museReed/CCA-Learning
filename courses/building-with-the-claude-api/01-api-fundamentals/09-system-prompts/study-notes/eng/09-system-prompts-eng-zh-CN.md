# System Prompts — 工程深度解析

| 项目 | 细节 |
|------|------|
| 考试领域 | D5 — Enterprise Deployment (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 5.1（模型选择与配置）、5.3（production 模式）、1.2（agentic loop 基础） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 09 |

---

## 一句话总结

System prompt 是一个独立于 `messages` 的顶层指令通道，用来定义 Claude 在整个对话中的 persona、任务范围与响应规则，是你在多轮交互中锁定行为的确定性锚点。

---

## 为什么 System Prompt 重要

没有 system prompt，Claude 会用通用的 helpful assistant 模式回应。这对随意 Q&A 没问题，但 production 应用几乎都需要更窄、更有主张的行为配置。

以数学家教 chatbot 为例，学生问「How do I solve 5x + 2 = 3 for x?」。通用 Claude 会直接给出完整解答——这就是**错的产品行为**。好的家教应该：

- 给提示而不是完整答案
- 一步一步引导学生思考
- 用类似题目示范做法

并且明确不应该：

- 直接给答案
- 让学生去用计算器

这是**行为规范**，不是知识缺口。System prompt 就是你编码这份规范的地方。

---

## API 接口

Anthropic Messages API 提供一个专属的 `system` 参数，和 `messages` array 分开：

```python
from anthropic import Anthropic

client = Anthropic()

system_prompt = """
You are a patient math tutor.
Do not directly answer a student's questions.
Guide them to a solution step by step.
"""

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    system=system_prompt,
    messages=[{"role": "user", "content": "How do I solve 5x + 2 = 3 for x?"}],
)
print(response.content[0].text)
```

关键属性：

- `system` 是纯字符串（若要用 prompt caching 则可以是 text block list）
- **不是** `messages` 的一部分。Anthropic API 里没有 `{"role": "system", ...}` 这种写法
- Claude 把 system prompt 当作比 user message 更高优先级的 context
- 它持续整个 turn——你不必每条消息重复注入，但每次 API 调用都要带上它

---

## 前后对比

没有 system prompt：

> To solve 5x + 2 = 3, subtract 2 from both sides: 5x = 1. Then divide by 5: x = 0.2.

带上家教 system prompt：

> Great question! What do you think would be a good first step to isolate x? Consider what operation we might need to perform on both sides to start moving terms around.

同一个模型、同一个 user message——行为完全不同。差别全在 system prompt。

---

## 构建一个灵活的 chat 函数

把 system prompt 写死在代码里是错误的抽象。包一个辅助函数，让 `system` 变成可选参数：

```python
def chat(messages, system=None):
    params = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 1000,
        "messages": messages,
    }
    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text
```

这个条件判断很重要：**API 不接受 `system=None`**。你必须先组 kwargs dict，只在 `system` 是非空字符串时才插入。这是 production 的真实坑——传 `None` 会触发 validation error。

使用方式：

```python
# 通用行为
answer = chat(messages)

# 家教行为
tutor_system = """
You are a patient math tutor.
Do not directly answer a student's questions.
Guide them to a solution step by step.
"""
answer = chat(messages, system=tutor_system)
```

---

## System Prompt 该放什么

一个强的 system prompt 通常结合：

1. **身份 / persona**——「You are a senior security engineer reviewing code for vulnerabilities.」
2. **任务范围**——Claude 该处理什么、不该处理什么
3. **响应格式**——语气、长度、结构、markdown 使用
4. **Guardrails**——硬规则（「永远不泄露 API keys」「拒绝无关问题」）
5. **示例**——理想输出的 few-shot 示范

要声明式、要具体。「Be helpful」是噪音。「永远返回含 `summary` 与 `action_items` keys 的 JSON」才是有用信号。

---

## System Prompt 与 Agentic Loop

在 agentic 应用（D1）中，system prompt 定义了 agent 的**身份与运作规则**——也就是 tool-use loop 每一轮都不变的常量。Tools 在每轮可能进出，但 system prompt 是稳定的契约。这就是为什么 CCA 考试常把 agent 设计题包成「这个约束该放哪？」——答案几乎永远是 system prompt，而不是逐条 user message 的指令。

---

## 常见错误

1. **把指令写在 user message 而不是 `system`**——在多轮 context 中指令会被稀释，Claude 会把它当成一次性请求处理
2. **传 `system=None`**——SDK 会拒绝。要条件式组 kwargs
3. **用 `{"role": "system", ...}` message**——那是 OpenAI 的惯例，不是 Anthropic。会被当 user message，行为错乱
4. **把动态数据塞进 system prompt**——system prompt 应该稳定；volatile context（用户资料、当前文档）要放在第一条 user message 或独立 content block，这样 prompt caching 才能生效
5. **不迭代**——system prompt 是产品。版本化、A/B 测试、回归要当回事

> **Key Insight**
>
> System prompt 是你和 Claude 之间的*行为契约*——唯一一个你可以锁死身份、任务、guardrails 的地方。所有会变的东西（user input、retrieved context、tool results）走 `messages`；所有不会变的东西走 `system`。把这两者搞混，你会不是把 persona 泄漏到每个 user turn，就是让 prompt 的静态部分无法被 cache。

---

## CCA 考试重点

- **D5 (Enterprise Deployment)**：production 应用需要一致的行为——system prompt 是在规模下强制这种一致性的标准机制
- **D1 (Agentic Architecture)**：system prompt 定义了 agent 在多轮 loop 中的持续身份。Tool-use agents 靠它保持专注
- 注意「如何确保 Claude 表现得像 {role}？」这种考题——答案一定是 system prompt，不是在 user message 做 prompt engineering

---

## Flashcards

| 题目 | 答案 |
|------|------|
| Anthropic API 用哪个参数设置 system prompt？ | `system`——`messages.create()` 的顶层字符串参数，和 `messages` array 分开 |
| 可以传 `system=None` 给 `messages.create()` 吗？ | 不行——API 会拒绝。要条件式组 kwargs，只在有提供时才加入 `system` |
| `{"role": "system", ...}` message 在 Anthropic API 里该放哪？ | 哪都不该放——那是 OpenAI 惯例。Anthropic 用独立的顶层 `system` 参数 |
| 为什么数学家教 chatbot 需要 system prompt？ | 为了覆盖 Claude 直接给答案的默认行为，强制逐步 Socratic 引导 |
| System prompt 通常包含哪五样东西？ | 身份/persona、任务范围、响应格式、guardrails、可选的 few-shot 示例 |
| 在 agentic loop 中，system prompt 扮演什么角色？ | 每一轮都不变的行为契约——tools 和 user messages 会变，但 system prompt 锁住身份和规则 |
| Volatile 的用户 context 应该放在 system prompt 吗？ | 不应该——volatile context 要放在 `messages`，避免破坏 prompt caching 并可随 turn 演化 |
| System prompt 和 user 指令的区别是什么？ | System prompt 持续整个对话且优先级更高；user 指令是单轮输入，被当成 request 层级 context |
