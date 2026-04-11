# Tool Functions — Engineering Deep Dive

| 项目 | 内容 |
|------|------|
| 考试 Domain | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.2（tool function 定义）、2.1（tool schema 设计）、1.2（agentic loop 基础） |
| 来源 | building-with-the-claude-api / 04-tool-use / Lesson 34 |

---

## 一句话总结

Tool function 就是一个普通的 Python 函数 — 但它的输入、错误消息、行为是刻意设计成**给 LLM 读、给 LLM 自我修复**，而不只是给人类工程师看。

---

## 什么是 Tool Function

Tool function 就是你的应用在 Claude 输出 `tool_use` block 时会执行的一般 Python callable。Python 这端没有魔法 — 魔法在于 function 与 LLM 之间的**契约**：

- 名字清楚 → Claude 挑得到正确的函数
- 参数名字清楚 → Claude 填得到正确的参数
- 验证 + 描述性的错误 → Claude 下一轮可以自我修正
- 返回类型可预测 → Claude 可以对结果推理

Tool function 是技术栈的底层。JSON schema（Lesson 35）是 Claude 读的文档。Agentic loop 用 Claude 给的参数调用函数。

---

## 第一个 Tool：`get_current_datetime`

```python
from datetime import datetime

def get_current_datetime(date_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)
```

三个值得拆开来看的地方：

1. **默认参数**（`date_format="%Y-%m-%d %H:%M:%S"`）— 让 Claude 在常见场景下不用传参数就能调用。Schema 会标这个参数为 optional。
2. **使用前验证** — `if not date_format: raise ValueError(...)` 挡掉 Python 原本会默默接受的退化值（空字符串够 falsy，`strftime("")` 会返回空字符串）。
3. **`strftime` 格式透传** — 把日期格式化交给 Python 身经百战的 `datetime` 模块，而不是自己重造轮子。

### 使用示例

```python
get_current_datetime()           # "2026-04-11 14:30:25"
get_current_datetime("%H:%M")     # "14:30"
get_current_datetime("%A")        # "Saturday"
```

---

## Tool Function 的 Best Practices

### 1. 描述性的名字

Function 名字：`get_current_datetime` — 人类一眼看懂意图。对比 `gcdt` 或 `datetime_fn`。Claude 会把名字当成决定是否调用这个函数的强先验。

参数名字：`date_format`，不是 `fmt` 或 `d`。每个字符都是 Claude 会读的文档。

### 2. 验证输入

```python
def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)
```

常见的验证 pattern：

- 空字符串（`if not s`）— LLM 意外频繁会出这种。
- 类型错（`if not isinstance(x, int)`）— 尤其是 JSON 反序列化之后。
- 超出范围（`if not 0 <= p <= 100`）。
- 格式不符（regex、enum 成员）。

每个参数要问自己：「LLM 可能输出什么最糟糕的输入，会让我静默产出错答案？」针对那个验证。

### 3. 有意义的错误消息

**差**：`raise ValueError("invalid input")`
**好**：`raise ValueError("date_format cannot be empty")`
**更好**：`raise ValueError("date_format cannot be empty; use a valid strftime pattern like '%Y-%m-%d'")`

错误消息是 Claude 唯一的反馈通道。每一条错误消息都是一段迷你 prompt，告诉下一轮怎么修正。如果你写「invalid input」，Claude 可能用同样的错输入再试一次。如果你写「expected an ISO-8601 date like 2026-01-15, got 'next Friday'」，Claude 就知道该怎么修。

这是与传统错误消息设计最大的转变：**错误消息不再只是给人看，而是 LLM 的修复信号**。

---

## Tool Function 如何跟 Loop 集成

```python
# agent loop 的 pseudo-code
while True:
    response = client.messages.create(..., tools=tool_schemas, messages=messages)

    if response.stop_reason != "tool_use":
        break  # 最终文字响应在 response.content 里

    for block in response.content:
        if block.type != "tool_use":
            continue
        fn = TOOL_REGISTRY[block.name]
        try:
            result = fn(**block.input)
            tool_result_content = str(result)
            is_error = False
        except Exception as e:
            tool_result_content = f"Error: {e}"
            is_error = True

        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": tool_result_content,
                "is_error": is_error,
            }],
        })
```

关键观察：

- 捕捉异常并以 `is_error: True` 的 `tool_result` 返回。不要让异常把 loop 打断 — 告诉 Claude 它就能恢复。
- `**block.input` 把 JSON 参数展开给 Python。类型不符会在 Python 调用点被挡下。
- `TOOL_REGISTRY` 就是个「tool 名字 → function 指针」的 dict。让 dispatch 超简单。

---

## Type Hint 对人与 Schema 都有帮助

Python type hint 在 runtime 是可有可无，但在设计阶段极有价值：

```python
def get_current_datetime(date_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    ...
```

- 让推导 schema（Lesson 35）变得超简单。
- 在 runtime 前就抓到开发者 bug。
- 对 review code 的同事传达意图。
- `inspect`、`pydantic` 之类的 library 可以从有 type hint 的函数自动生成 JSON Schema。

---

## 常见错误

1. **名字暧昧的函数** — `process`、`run`、`do_it`。Claude 从含糊的名字推不出用途。
2. **输入坏的也默默吃下去** — 接受 `None` 或空字符串却不验证，产出垃圾结果。
3. **神秘的错误消息** — 「error 42」告诉 Claude 什么都没有；「radius must be positive, got -3」告诉它要怎么修。
4. **没在 loop 层级捕捉异常** — 让 tool 异常把整段对话炸掉，而不是包成 tool_result error 喂回去。
5. **隐藏的副作用** — 名字没写清楚就静默写 DB 的 tool 很危险；用 `create_reminder` 取代 `reminder`。
6. **返回复杂对象没 `str()`** — `tool_result.content` 必须是可序列化的文字；把对象显式转字符串或 JSON。

> **Key Insight**
>
> Tool function 不是「内部工具」 — 它是你对 Claude 暴露的 **public API**。每个参数名、每个错误消息、每个返回类型都会被模型读到。把 tool function 当成文档完整的 SDK 设计，因为 Claude 就是这样看它的。CCA D2 常出这个角度的题目。

---

## CCA 考试重点

- **D2（Tool Design & MCP Integration）**：命名、验证、错误消息作为 LLM 可读的修复信号、默认参数。
- **D1（Agentic Architecture）**：Tool loop 内的异常处理；错误如何转成 tool_result block。
- 预期会出：「为什么 tool function 要 raise 描述性的错误？」— 答：让 Claude 在下一轮能自我修正。

---

## Flashcards

| Front | Back |
|-------|------|
| Tool function 是什么？ | 一般的 Python callable，Claude 输出 `tool_use` block 时会被调用；函数必须验证输入并返回可序列化的结果。 |
| 为什么 tool function 的错误消息很重要？ | 因为它是 Claude 唯一的反馈通道 — Claude 会读它并用来自我修正下一次 `tool_use` 调用。 |
| 什么是差的 tool function 名字？ | 任何像 `process`、`run`、`do_it` 这类含糊的名字 — Claude 推不出用途。 |
| 若 tool function 在 agent loop 内抛异常会怎样？ | 调用方应该捕捉并以 `is_error: True` 的 `tool_result` 返回 — 不要让它炸掉 loop。 |
| 为什么 tool function 要用默认参数？ | 让 Claude 在常见场景下能用最少的输入调用，只在必要时才带参数。 |
| `get_current_datetime` 验证了什么、为什么？ | 它拒绝空的 `date_format`，这样 `strftime("")` 才不会默默返回空字符串。 |
| Tool function 要怎么返回复杂对象？ | 转成字符串或 JSON — `tool_result.content` 必须是可序列化文字。 |
| Type hint 与 schema 有什么关系？ | Type hint 让 JSON Schema 可以自动生成，并让 Claude（透过 schema）与人类都看到清楚意图。 |
