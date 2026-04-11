# Making a Request — Engineering Deep Dive（简体中文）

| 项目 | 内容 |
|------|------|
| Exam Domain | D5 — Enterprise Deployment (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 5.1（model selection）、5.3（production patterns）、1.2（agentic loop 基础） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 06 |

---

## One-Liner

`client.messages.create()` 是 Anthropic API 的原子单位——三个必需参数（`model`、`max_tokens`、`messages`）产生一个 response，文本在 `response.content[0].text`。这个调用就是 agents、tool use、streaming 等所有上层 feature 的基础。

---

## 环境配置：最小可行 Stack

在调用任何 API 前，两个包是必需的：

```bash
%pip install anthropic python-dotenv
```

- **`anthropic`** —— 官方 Python SDK。包住 REST API，处理认证、重试、pagination。
- **`python-dotenv`** —— 把本地 `.env` 载进 `os.environ`，让 SDK 能自动读 `ANTHROPIC_API_KEY`。

`.env` 放在 notebook 或 entry point 旁边：

```
ANTHROPIC_API_KEY="sk-ant-api03-...your-key..."
```

两条规则救你免于意外泄漏凭证：

| 规则 | 原因 |
|------|------|
| `.env` 加进 `.gitignore` | 防止 commit |
| 绝不用字符串 literal 把 key 写进代码 | 防止它出现在 notebook、log、Slack |

---

## Client 对象

一个 process 一个 instance，每次调用都重用：

```python
from dotenv import load_dotenv
load_dotenv()

from anthropic import Anthropic

client = Anthropic()           # 从环境变量自动读 ANTHROPIC_API_KEY
model = "claude-sonnet-4-5"    # 把 model 名字钉在一个地方
```

把 model 名字钉在变量里（而不是到处洒字符串 literal）是一个小习惯，但回报很大：未来要升级 model，只要改一行。

---

## 三个必需参数

```python
message = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "What is quantum computing? Answer in one sentence"}
    ],
)
```

| 参数 | 类型 | 用途 |
|------|------|------|
| `model` | string | 用哪个 model，例如 `"claude-sonnet-4-5"` |
| `max_tokens` | int | 输出长度上限（不是目标） |
| `messages` | list[dict] | 对话历史（见下一节） |

### `max_tokens` 是上限不是目标

这是新手最常见的误解。`max_tokens=1000` **不是**告诉 Claude"写 1000 个 token 的输出"，而是告诉 Claude"你最多可以写 1000 个 token；遇到自然结束或写到 1000，哪个先到看哪个"。

| 行为 | 正确理解 |
|------|---------|
| 设预算？ | 是 |
| 设目标？ | 不是 |
| 强迫输出变长？ | 不能（要用 prompt 措辞去引导） |
| 打到上限时 `stop_reason == "max_tokens"`？ | 是 |

实务规则：把 `max_tokens` 设成你预期最长合理回复的 1.5 倍。太低会真的截断；太高不会浪费（你只为实际生成的 token 付费），但会掩盖 prompt bug。

---

## `messages` List

`messages` 是一个有序的 dict list，每个 dict 有 `role` 和 `content`：

```python
messages = [
    {"role": "user",      "content": "Define quantum computing"},
    {"role": "assistant", "content": "Quantum computing uses qubits..."},
    {"role": "user",      "content": "Give me a concrete example"},
]
```

| Role | 谁写的 | 何时 |
|------|-------|------|
| `user` | 人（或你的后端代写） | 永远是第一个和最后一个 |
| `assistant` | 之前 Claude 的回复你重播回来 | 在 user turn 之间，提供上下文 |

两个不变式必须成立：

1. **第一个 message 必须是 `user`**。忘了从 `assistant` 开始，API 会拒绝。
2. **Turn 必须交替**。连续两个 `user` message 不允许；要合并或塞一个 assistant turn。

这就是 Lesson 07 用来建立多轮对话的形状——每次追问都追加两个 entry（前一次的 assistant 回复 + 新的 user 问题）。

---

## 取出 response 文本

Response 对象是结构化的（带 usage、stop_reason、metadata），所以拉出文本要一行：

```python
message = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[{"role": "user", "content": "What is quantum computing? Answer in one sentence"}],
)

print(message.content[0].text)
```

为什么是 `content[0].text` 而不只是 `content`？

- `content` 是一个 **content block 的 list**，不是字符串。
- 单纯文本回复时，list 只有一个 `TextBlock` 在 index 0。
- 有 tool use 时（Lesson 32 之后），同一个 list 可能交错出现 `tool_use` 和 text block。
- 索引 `[0]` 在最简单情况可以用，但是坏习惯——生产环境要 iterate 并 pattern-match block type。

```python
# 生产环境更安全的 pattern
for block in message.content:
    if block.type == "text":
        print(block.text)
    elif block.type == "tool_use":
        handle_tool_use(block)
```

---

## 完整 End-to-End 示例

```python
from dotenv import load_dotenv
load_dotenv()

from anthropic import Anthropic

client = Anthropic()
model = "claude-sonnet-4-5"

def ask(question: str, max_tokens: int = 1024) -> str:
    """Single-turn 问答 helper。"""
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": question}],
    )
    # 生产环境 iterate；demo 可以用 index。
    return response.content[0].text

print(ask("What is quantum computing? Answer in one sentence."))
```

差不多 15 行代码，就是完整最小可行 Claude 集成。课程后面所有东西——多轮、streaming、tool use、agents——都是叠在这个骨架上面。

---

## Common Mistakes

1. **把 `max_tokens` 当目标** —— Claude 遇到 `end_turn` 就停，这个参数是 cap 不是配额。
2. **`messages` 从 `assistant` 开始** —— 无效请求；第一个 turn 必须是 `user`。
3. **连续两个 `user` message** —— 无效；要合并或中间塞 assistant turn。
4. **把 `response.content` 当字符串用** —— 它是 content block 的 list；用 `response.content[0].text` 或 iterate。
5. **Model 名字到处硬编码** —— 钉在一个变量，升级 model 才会是一行改动。

> **Key Insight**
>
> `client.messages.create()` 看起来小得吓人——三个参数、一个 response——但它是你未来会出的每个 Claude feature 的 **原子**。多轮是这个调用跑 loop；tool use 是这个调用跑两次；agents 是这个调用跑 loop 加分支；streaming 是这个调用加 flag。把三个必需参数和 `content[0].text` 提取方法深度内化，你就能推理所有上层 pattern。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）**：考题会问 `max_tokens` 语义、必需参数集、怎么读 response envelope。
- **D1（Agentic Architecture）**：每个 agent loop 都是 `messages.create()` 的 for-loop；熟悉原子调用是所有 D1 内容的前置。
- 情境触发："`max_tokens` 是什么意思？"→ 永远是"输出长度的上限，不是目标"。

---

## Flashcards

| Front | Back |
|-------|------|
| `client.messages.create()` 三个必需参数是什么？ | `model`、`max_tokens`、`messages` |
| `max_tokens` 设的是目标长度还是上限？ | 上限——Claude 自然遇到 `end_turn` 就停，或打到 `max_tokens` 被截 |
| `messages` 第一个消息 role 必须是什么？ | `user`——从 `assistant` 开始是无效的 |
| 怎么取简单回复的纯文本？ | `response.content[0].text` |
| 为什么 `response.content` 是 list 不是字符串？ | 它是有序的 content block list；tool use 时 `text` 和 `tool_use` 类型可以交错 |
| Lesson 06 安装哪两个包？ | `anthropic`（SDK）和 `python-dotenv`（载 `.env`） |
| 为什么 model 名字要钉在单一变量？ | 这样升级 model 只改一行，不用 find-and-replace |
| SDK 会自动读哪个环境变量？ | `ANTHROPIC_API_KEY` |
