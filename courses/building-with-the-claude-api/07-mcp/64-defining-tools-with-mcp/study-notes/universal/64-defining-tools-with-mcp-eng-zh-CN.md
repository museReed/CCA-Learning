# Defining Tools with MCP — 工程深度解析

| 项目 | 说明 |
|------|------|
| 考试领域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.1（tool schema 设计）、2.3（MCP primitives：tools）、1.2（agent loop 集成） |
| 来源 | building-with-the-claude-api / 07-mcp / Lesson 64 |

---

## 一句话总结

Lesson 64 演示 Python MCP SDK（`FastMCP`）如何把 tool 编写压缩成"decorator + type hints"——SDK 会从你的 function signature 和 Pydantic `Field` 注解自动生成 JSON schema，让你写正常 Python 而不是手工 JSON Schema。

---

## 为什么需要 SDK

Ch04 的 tool use 里，每个 tool 定义都要写一大段冗长的 JSON schema：

```python
tools = [{
    "name": "read_doc_contents",
    "description": "...",
    "input_schema": {
        "type": "object",
        "properties": {
            "doc_id": {"type": "string", "description": "..."}
        },
        "required": ["doc_id"]
    }
}]
```

一个 tool 还好，二十个 tool 就痛苦了。Python MCP SDK（`mcp.server.fastmcp.FastMCP`）用 decorator 驱动的模式：

- 拿一个普通的 Python 函数
- 读取它的 type hints 和 `Field(description=...)` 注解
- 自动生成对应的 JSON schema
- 把 tool 注册到 MCP server

结果是：tool 定义缩到几行，看起来就像普通 Python 代码。

---

## 建立 Server

创建一个 MCP server 只要一行 import + 一行初始化：

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")
```

- `"DocumentMCP"` 是 server 的名字（呈现给 clients 的标识名）。
- `log_level="ERROR"` 在开发时压掉吵人的 info log。

`mcp` 对象是一个 registry，你把 tools（以及后面的 lessons 要加的 resources 和 prompts）挂在上面。

---

## 内存文档存储

这节课把普通 Python dict 当"数据库"用：

```python
docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditure",
    "outlook.pdf": "This document presents the projected future performance of the",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment"
}
```

Key 是 document ID，value 是文字内容。没有 persistence——文档活在 process memory。这样做是刻意的，让焦点放在 MCP 编写而不是 DB 管道上。

---

## Tool 1：`read_doc_contents`

Decorator 驱动的读取 tool：

```python
@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string."
)
def read_document(
    doc_id: str = Field(description="Id of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    return docs[doc_id]
```

底层发生的事：

| Source 元素 | 变成什么 |
|------------|---------|
| `@mcp.tool(name=..., description=...)` | MCP schema 里 tool 的顶层 metadata |
| `doc_id: str` type hint | 生成的 JSON Schema 里的 `{"type": "string"}` |
| `Field(description="...")` | `doc_id` property 的 `description` |
| Function body | Claude 发 `CallToolRequest` 时执行的 callable |
| `raise ValueError(...)` | 会变成 Claude 能读的 tool 错误，可能可以修正 |

注意函数名（`read_document`）和 MCP tool 名（`read_doc_contents`）是独立的；decorator 的 `name=` 才是权威。

---

## Tool 2：`edit_document`

第二个 tool 是简单的 find-and-replace 编辑器：

```python
@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string."
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace."),
    new_str: str = Field(description="The new text to insert in place of the old text.")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
```

工程细节：

- 三个参数，每个都用 `Field(description=...)` 注解，让 Claude 理解角色。
- `old_str` description 明写"must match exactly, including whitespace"——这是面向 Claude 的文档，可减少不稳定的编辑。
- 实现用 Python 内建 `str.replace`，会替换**所有**出现位置；如果你真实系统需要唯一性，要加一个 match-count check。
- 函数没有显式 return；它直接 mutate dict。

---

## 用 `ValueError` 做错误处理

两个 tools 收到无效 `doc_id` 时都 `raise ValueError`。MCP SDK 会把这些转成 tool error response，Claude 在下一个 `tool_result` block 收到，让它可以：

- 道歉并请用户提供有效 ID
- 用看起来相似的 ID 重试
- 升级成"找不到这份文档"的最终回答

这是**结构化错误**模式：你给 Claude 一段可读的解释，而不是默默失败；agent loop 就能把错误纳入推理。

---

## SDK 方式的关键好处

这节课列了五个相较手写 tool schema 的赢面：

1. **自动从 Python type hints 生成 JSON Schema**。
2. **干净、可读的代码**——tool body 看起来像普通 Python。
3. **用 Pydantic `Field` 内建参数验证**。
4. **减少样板**——不用手写 `{"type": "object", "properties": ...}` 的 dict。
5. **开发时的类型安全和 IDE 支持**。

Meta-point：SDK 让你专注在**业务逻辑**（tool 做什么），协议层（schema、序列化）自动处理。

---

## 课程没演示的进阶考量

Source 刻意简化，但真实 server 还该考虑：

| 关注点 | 为什么 |
|-------|-------|
| Return type hints | 完全类型化的 return 让 FastMCP 能描述结果形状 |
| 带 default 的 optional 参数 | 用 `Field(default=..., description=...)` |
| 长描述 | `description` 是 Claude 的操作手册——值得投资写清楚 |
| Side-effect logging | `edit_document` 修改 state；prod 应每次调用都 audit-log |
| 并发安全 | dict 是共享 state；prod 要用 lock 或 async-safe store |

这些不是完成这门课项目的必要项目，但能区分"demo 能跑"和"能上线给用户"。

---

## 常见错误

1. **忘了 `Field` description。** 没有的话 Claude 只看到参数名字——tool 质量立刻下降。
2. **用函数名当 MCP tool 名。** Claude 看到的是 decorator 的 `name=`；函数名是内部的。
3. **让错误变未处理 exception 冒上来。** `ValueError` 会被转成可读的 tool error；其他 exception 比较吵且不好恢复。
4. **以为 tool name 和 schema 是稳定的。** 如果你改名或改形状，clients（包括 lesson 65 的 MCP inspector）要重新 list tools。
5. **靠 description 做 prompt engineering。** Description 要诚实；不要塞相互矛盾的指示让 Claude 混淆。

> **Key Insight**
>
> Python MCP SDK 把 tool 编写变成普通 Python 代码 + 两撮 metadata（`@mcp.tool(...)` + `Field(description=...)`）。这就是 MCP 的核心生产力赢面：你用"decorated function"换掉"手写 JSON Schema"，framework 搞定协议。课程后面加的每个 tool 都是这个模式。

---

## CCA 考试重点

- **D2（Tool Design & MCP Integration）**：知道 `FastMCP("Name", log_level=...)`、`@mcp.tool(name, description)` decorator、以及 `Field(description=...)` 如何填入 schema。
- **D1（Agentic Architecture）**：理解 `ValueError` 如何在 agent loop 里被呈现成 Claude 可恢复的 tool error。
- 情境题可能问："SDK 怎么知道要 require `doc_id`？"——答：因为它是没有 default 的 positional 参数，SDK 把它标成 schema 中的 required。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Python MCP SDK 用哪个 class 初始化 server？ | `FastMCP`（来自 `mcp.server.fastmcp`） |
| 怎么声明一个 tool？ | 用 `@mcp.tool(name=..., description=...)` decorate 一个函数 |
| 怎么为 Claude 文档化一个参数？ | 用 Pydantic 的 `Field(description="...")` 当参数 default |
| SDK 从你的 type hints 生成什么？ | JSON Schema（包含 `type`、`properties`、`required`） |
| 两个 demo tools 的数据持久化方式？ | 没有——文档活在 module-level 的 Python dict（内存） |
| `read_doc_contents` 收到不存在的 doc_id 会怎样？ | Tool `raise ValueError`，变成送给 Claude 的 tool error |
| Demo server 对外提供几个 tools？ | 两个——`read_doc_contents` 和 `edit_document` |
| 这节课列出 SDK 方法的哪五个好处？ | 自动 JSON Schema、干净代码、Pydantic validation、减少样板、类型安全/IDE 支持 |
