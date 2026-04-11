# Tool Schemas — Engineering Deep Dive

| 项目 | 内容 |
|------|------|
| 考试 Domain | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.1（tool schema 设计）、2.2（tool function 定义）、1.2（agentic loop 基础） |
| 来源 | building-with-the-claude-api / 04-tool-use / Lesson 35 |

---

## 一句话总结

Tool schema 是一份 JSON Schema 文档，包含三个顶层字段（`name`、`description`、`input_schema`）— 它是你的 Python 函数对 Claude 公开的 API contract，文字质量直接决定 Claude 会不会挑对 tool、会不会带对参数。

---

## 三个必填字段

每一个发送到 Anthropic API 的 tool 定义都必须包含：

| 字段 | 类型 | 用途 |
|------|------|------|
| `name` | string | Claude 引用 tool 的标识名称，必须与 function registry 的 key 一致。 |
| `description` | string | 3-4 句，告诉 Claude tool 做什么、何时用、返回什么。 |
| `input_schema` | JSON Schema object | 描述函数参数的 JSON Schema。 |

这三个字段组成 Claude 每次决定是否调用 tool 时会读的 contract。

---

## 完整示例：`get_current_datetime`

```python
from datetime import datetime
from anthropic.types import ToolParam

def get_current_datetime(date_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)

get_current_datetime_schema: ToolParam = {
    "name": "get_current_datetime",
    "description": (
        "Returns the current date and time formatted according to "
        "the specified format string. Use this whenever you need to "
        "know the current moment in time, for example when a user "
        "asks what time it is or you need to timestamp a reminder. "
        "Returns a string formatted per Python's strftime codes."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": (
                    "A strftime format string such as '%Y-%m-%d %H:%M:%S'. "
                    "Defaults to ISO-style date and time if not provided."
                ),
                "default": "%Y-%m-%d %H:%M:%S",
            }
        },
        "required": [],
    },
}
```

注意**命名约定**：函数叫 `get_current_datetime`，schema 变量叫 `get_current_datetime_schema`。镜像命名让你很容易把实现与 schema 对起来。

---

## `input_schema` 的结构解析

`input_schema` 就是标准的 JSON Schema 片段。三个最重要的部分：

### 1. `type: "object"`

Tool 的输入永远是 object（命名参数的 key-value map）。因为 API 会把 `input` 以 JSON object 传入，你的代码用 `**block.input` 展开。

### 2. `properties`

`properties` 中的每个 key 是一个参数名。每个 value 是描述该参数类型、约束，以及**最重要的 description** 的子 schema。

```python
"properties": {
    "date_format": {
        "type": "string",
        "description": "A strftime format string...",
        "default": "%Y-%m-%d %H:%M:%S"
    }
}
```

每个属性的 `description` 是你告诉 Claude「该传什么样的值」的机会。把它当成写给 LLM 看的 docstring。

### 3. `required`

一个数组，列出哪些参数是必填的。没列在这里的就是 optional，Claude 可以省略不填。因为 `date_format` 有 default，所以是 optional，`required` 是空数组。

```python
"required": []              # 全部 optional
"required": ["city"]         # city 必填，其他 optional
"required": ["city", "date"] # 都必填
```

---

## 为什么描述质量决定一切

两个代码一模一样但 description 不同的 tool，表现会天差地别：

| 描述 | 结果 |
|------|------|
| 「Gets the time」 | Claude 可能跟其他时间 tool 混淆；使用不稳定。 |
| 「Returns the current date and time formatted per strftime codes. Use when the user asks 'what time is it' or when you need to timestamp a new record. Returns a formatted string.」 | Claude 正确选中、带对格式、合理解读结果。 |

**描述的 best practices：**

- 3-4 句（足够 context，不要写小说）。
- 说明**做什么**与**返回什么**。
- 说明 Claude **何时**该用它（「何时」这句最常被省略，但最有价值）。
- 提到相关 tool 避免混淆（例如「要把日期字符串转时间戳，请用 `parse_datetime`」）。
- 对参数，用具体示例描述合法值、单位、格式。

---

## 生成 Schema：让 Claude 自己写

与其手写 schema，你可以让 Claude 帮你生成：

1. 复制 tool function 的代码。
2. 问 Claude 类似：「请为这个函数写一份合法的 JSON schema 用于 tool calling。遵循附件文档的 best practices。」
3. 把 Anthropic 的 tool-use 文档当作 context 附上。
4. 把生成的 schema 粘到代码，用 `{function_name}_schema` 命名约定。

这本身就是 tool-use 原则的 meta 应用：用 AI 来打造 AI 自己的输入。

---

## 用 `ToolParam` 做类型安全

`anthropic` SDK 暴露了一个 `ToolParam` TypedDict，可用于静态分析：

```python
from anthropic.types import ToolParam

get_current_datetime_schema = ToolParam(
    name="get_current_datetime",
    description="Returns the current date and time...",
    input_schema={
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": "...",
                "default": "%Y-%m-%d %H:%M:%S",
            }
        },
        "required": [],
    },
)
```

好处：

- IDE 对三个必填字段有自动补全。
- Mypy/pyright 可以在 runtime 前抓到像 `descripton` 这种拼错。
- 代码自我文档化。

非强制 — API 也接受一般 dict — 但生产环境强烈建议用。

---

## Tool 定义常用的 JSON Schema 功能

| 功能 | 示例 | 用途 |
|------|------|------|
| `type` | `"string"`、`"integer"`、`"boolean"`、`"array"`、`"object"`、`"number"` | 声明 JSON 类型 |
| `description` | 自由文字 | 给 LLM 读的逐参数指引 |
| `default` | 字面值 | Claude 省略 optional 参数时使用 |
| `enum` | `["celsius", "fahrenheit"]` | 限制在固定允许值集合 |
| `items` | schema | 描述数组元素类型 |
| `minimum` / `maximum` | 数值 | 数值范围 |
| `pattern` | regex | 字符串格式验证 |
| `required` | 名称数组 | 必填属性名 |

`enum` 特别强大：强迫 Claude 从定义好的集合里挑，消除模糊性。

---

## 常见错误

1. **缺 `type: "object"`** — 每个 `input_schema` 都必须从 `type: "object"` 开始，不能只放 `properties`。
2. **空的或含糊的 description** — 「Gets data」对 Claude 等于没说。要投资文字。
3. **忘了写 `required`** — 省略不代表「全部必填」，代表「全部 optional」。要明确。
4. **Schema 与函数不一致** — schema 写 `city`，函数用 `location`。Claude 会传 `city`，代码直接炸。
5. **Pattern 过度限制** — 正则拒绝了你没预期到的合法输入，卡住正当使用。
6. **把实现细节放进 description** — Claude 不需要知道你打的是 SQLite；它需要知道 tool 在概念上做什么。

> **Key Insight**
>
> Tool schema 不是接线 — 它是**LLM 可读的 API contract**。描述里的每个字、每个参数注解都会改变 Claude 调用 tool 的决策。你花在 schema 描述上的工程时间，会变成更少的误选 tool、更少的错误参数、更少的挫折用户。CCA 考试 D2 反复出 `input_schema` 结构与 description best practice 的题目。

---

## CCA 考试重点

- **D2（Tool Design & MCP Integration）**：Tool 定义结构（`name`、`description`、`input_schema`）、JSON Schema 基础、`required` 语意、enum 用法。
- **D1（Agentic Architecture）**：Schema 质量直接影响 Claude 在 agent loop 中选 tool。
- **D5（Enterprise Deployment）**：生产代码用 `ToolParam` 做类型安全。
- 预期题型：「Tool 定义的三个必填字段是什么？」或「两个 tool 存在时 Claude 如何决定调用哪个？」— 答：description 质量与名称清晰度。

---

## Flashcards

| Front | Back |
|-------|------|
| Tool 定义的三个必填字段是什么？ | `name`、`description`、`input_schema`。 |
| `input_schema` 最上层的 `type` 永远必须是什么？ | `"object"` — tool 输入永远是 JSON object。 |
| `input_schema` 里的 `required` 是什么意思？ | 一个数组列出必填的属性名；没列的就是 optional。 |
| 为什么 tool schema 的 description 质量这么关键？ | Claude 读 description 来决定何时调用 tool 与如何填参数 — 文字质量直接影响正确性。 |
| 课程建议 schema 用什么命名约定？ | `{function_name}_schema` — 镜像函数名称，让实现与 schema 对得起来。 |
| `ToolParam` 是什么、何时用？ | `anthropic.types` 中的 TypedDict，让 tool schema 可做静态类型检查；生产代码建议用，支持 IDE 与 mypy。 |
| 不手写 JSON Schema 怎么生成 schema？ | 让 Claude 帮你生成 — 粘贴函数代码与 tool-use 文档，请它写格式正确的 schema。 |
| 为什么 property schema 要用 `enum`？ | 把 Claude 限制在固定合法值集合（如 `["celsius", "fahrenheit"]`），消除模糊性。 |
| Schema 的参数名若与 Python 函数的参数名不一致会怎样？ | 函数调用会失败 — Claude 传 schema 的名字、`**block.input` 展开到函数，Python 会抛 `TypeError`。 |
