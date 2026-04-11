# Multi-Turn Conversations — Engineering Deep Dive（简体中文）

| 项目 | 内容 |
|------|------|
| Exam Domain | D1 — Agentic Architecture (22%) 主要；D5 — Enterprise Deployment (20%) 次要 |
| Task Statements | 1.2（agentic loop 基础）、1.1（对话状态管理）、5.3（状态性的生产 pattern） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 07 |

---

## One-Liner

Anthropic API 是 **stateless** 的——Claude 在调用之间没有记忆——所以 client 要完全负责维护对话历史并在每次请求时重放。这就是你未来要做的每个 agent 跟 chat feature 的机械基础。

---

## 核心原则：Statelessness

Claude 这个模型不存储你的对话。每次 `messages.create()` 都是一个全新的请求，没有任何之前交流的记忆。如果你调用：

```python
client.messages.create(model=model, max_tokens=1000, messages=[
    {"role": "user", "content": "What is quantum computing?"}
])
# → 很好的回答

client.messages.create(model=model, max_tokens=1000, messages=[
    {"role": "user", "content": "Write another sentence"}
])
# → Claude 根本不知道"another sentence"在指什么；会写完全不相关的句子
```

第二次调用没有任何 context。Claude 会写一个跟量子计算完全无关的句子，因为它从没看过第一次交流。**这不是 bug，是根本设计。**

| 属性 | Anthropic API |
|------|---------------|
| 服务器端记得你的对话？ | 没有 |
| 对话 ID？ | 没有（API 层没有） |
| 谁拥有历史？ | 你的应用 |
| 历史怎么重放？ | 你的代码每次都发完整 `messages` list |

---

## 解法：Client 端历史

要做多轮对话，你必须：

1. **在应用代码里维护一个 messages list。**
2. **每次请求都发完整的历史。**

流程：

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  Turn 1:                                        │
│   messages = [user: "Define quantum computing"] │
│   response = create(messages)                   │
│   messages.append(assistant: response.text)     │
│                                                 │
│  Turn 2:                                        │
│   messages.append(user: "Write another          │
│                         sentence")              │
│   response = create(messages)   ← 发完整历史    │
│   messages.append(assistant: response.text)     │
│                                                 │
│  Turn N:                                        │
│   messages 无限增长；每次调用都重放整份。       │
│                                                 │
└─────────────────────────────────────────────────┘
```

每一轮都追加两个 entry：前一次的 assistant 回复 + 新的 user 问题。

---

## Helper Functions：最小 Chat 骨架

这一课推荐三个一行 helper：

```python
def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
    )
    return message.content[0].text
```

这三个函数是让调用点保持可读、历史变动规则保持一致的最干净做法。

---

## 组起来

```python
from dotenv import load_dotenv
load_dotenv()

from anthropic import Anthropic

client = Anthropic()
model = "claude-sonnet-4-5"

def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
    )
    return message.content[0].text

# 从空 list 开始
messages = []

# Turn 1
add_user_message(messages, "Define quantum computing in one sentence")
answer = chat(messages)
add_assistant_message(messages, answer)

# Turn 2 —— Claude 现在有完整 turn 1 的 context
add_user_message(messages, "Write another sentence")
final_answer = chat(messages)
add_assistant_message(messages, final_answer)

print(final_answer)
```

这下"Write another sentence"如预期运作——Claude 看得到整段对话，理解代词指涉的是量子计算。

---

## 隐藏成本：Token 线性增长

因为完整历史每轮都重放，**input token 会随对话长度线性增长**。第 N 轮时，你要再付一次 turn 1 到 turn N-1 的费用。

| Turn | Input tokens（约） | 累计 input 成本 |
|------|------------------|---------------|
| 1 | 50 | 50 |
| 2 | 150 | 200 |
| 3 | 300 | 500 |
| 10 | 2,000 | ~10,000 |
| 50 | 20,000 | ~500,000 |

两个实务后果：

1. **长聊天的账单由 input token 主宰。** Output 每轮可能就几百 token；input 会爆炸。
2. **最终会撞到 context window。** 每个 model 都有最大 context 长度；长对话在撞墙前要先截断或摘要。

缓解策略（超出 Lesson 07 范围但值得知道）：
- **Sliding window** —— 只留最近 N 轮。
- **Summarization** —— 把旧轮次压成滚动摘要。
- **Prompt caching** —— Anthropic 的 caching feature 让没变的 prefix 便宜重用（课程后面会教）。

---

## 为什么这对 agent 很重要

Lesson 07 教的是单一职责多轮 chat，但完全一样的 pattern 是每个 agent 的基础：

```python
# Agent loop —— 就是多轮 chat 加 stop_reason 分支
while True:
    response = client.messages.create(model=model, max_tokens=1024, messages=messages, tools=tools)
    messages.append({"role": "assistant", "content": response.content})

    if response.stop_reason == "end_turn":
        break

    if response.stop_reason == "tool_use":
        tool_result = execute_tool(response)
        messages.append({"role": "user", "content": [tool_result]})
        continue
```

结构相似性就是重点：**多轮 chat + stop_reason 分支 = agent**。搞懂 Lesson 07，你就懂了每个 D1 agent 的骨架。

---

## Common Mistakes

1. **忘记追加 assistant 回复** —— 下一轮没有 context，Claude 看起来像失忆。
2. **只追加 user message** —— API 拒绝连续两个 user turn；必须交替。
3. **把 API 当有状态的** —— 服务器端没有对话 ID；所有状态都在你这边。
4. **忽略 token 增长** —— 测试时好好的对话，在生产长 session 就爆掉。
5. **并行修改 `messages`** —— 多用户 chat server 必须每个对话隔离；所有用户共用一个 list 会把历史搞烂。

> **Key Insight**
>
> API 的 statelessness 不是限制——它是 **刻意的设计**，把记忆的完整控制权交给你。你决定留什么、丢什么、摘要什么、怎么做 per-user 隔离。所有花哨 feature（agent、tool use、streaming、caching）都坐在"维护 list、每轮重放"这个基础上。掌握这一课你就拥有整个 CCA 课纲每个上层 pattern 的心智模型。

---

## CCA Exam Relevance

- **D1（Agentic Architecture）**：多轮 loop 就是 agent loop。考题会用"Claude 怎么记住 context？"的框架——答案永远是"client 重放历史；API 是 stateless"。
- **D5（Enterprise Deployment）**：成本（线性 token 增长）与 scale（per-user 隔离）的启示。
- 情境触发："Claude 忘记我们在聊什么"→ 是 app 没有追加前一次交流；修复在 client，不是改 prompt。

---

## Flashcards

| Front | Back |
|-------|------|
| Claude 在 API 调用之间会存储对话历史吗？ | 不会——API 完全 stateless，历史由你的应用拥有 |
| 每一轮要做哪两个动作才能保持 context？ | 把前一次的 assistant 回复和新的 user 问题追加到 `messages` list，然后发整份 list |
| 为什么 input token 用量会随对话长度线性增长？ | 每次请求都重放完整历史，所以每次调用都把过去所有 turn 当 input 发 |
| Lesson 07 推荐的三个 helper 函数是什么？ | `add_user_message`、`add_assistant_message`、`chat` |
| 只追加 user message（没 assistant）会怎样？ | API 拒绝连续 user turn；对话必须交替 |
| 多轮 chat 跟 agent loop 有什么关系？ | Agent 就是多轮 chat 加 `stop_reason` 分支（tool_use vs end_turn） |
| 线性 token 增长有哪些缓解方法？ | Sliding window、旧 turn 摘要、prompt caching |
| 生产 chat app 的对话状态住哪？ | 特定用户的服务器端 session——绝不跨用户共用 |
