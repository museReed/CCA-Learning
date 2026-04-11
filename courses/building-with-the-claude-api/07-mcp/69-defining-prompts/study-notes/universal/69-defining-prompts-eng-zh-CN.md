# Defining Prompts — Engineering Deep Dive（简体中文）

| 项目 | 说明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（MCP primitives：tools、resources、prompts）、1.2（seed agent loop）、2.2（base.Message content blocks） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 69 |

---

## One-Liner

Prompts 是 MCP 的第三个原语——预先调优过的高质量指令模板。Server 作者把"怎么写才能得到好结果"的 know-how 封装起来，让 client 可以按名字调用，而不是要求终端用户自己学 prompt engineering。

---

## Prompts 解决的问题

用户当然可以自己写指令——"convert report.pdf to markdown"也能用。但结果好坏完全取决于 prompt 写得多好，而大多数用户不是 prompt 工程师。本课的核心观点：

> 用户虽然能自己完成任务，但使用 server 作者精心设计与测试过的 prompt，能得到更一致、更高质量的结果。

Prompts 把专家知识外化。开发者知道怎么写一个能产出优质 markdown 的 prompt，就把它固化成 server 端可复用的模板。

---

## Prompts 在 MCP 原语中的位置

| 原语 | 目的 | 示例 |
|------|------|------|
| Tool | 执行动作 | `edit_document(doc_id, new_content)` |
| Resource | 暴露数据 | `docs://documents/{doc_id}` |
| Prompt | 预先调优的指令模板 | `format(doc_id)` 把文档改成 markdown |

Prompt 不是"Claude 要读的文字"，而是一个 **可调用的模板**：client 带参数调用，拿回一串可以直接发给 Claude 的消息。

---

## Prompts 怎么运作

- 用 `@mcp.prompt()` 装饰器定义
- 每个 prompt 带 `name` 与 `description`
- 返回一个消息 list（user / assistant），组成完整的对话开场
- Prompt 应该高质量、测试过、与 server 主要用途相关

Client 之后按名字调用时，server 会用 client 提供的参数执行装饰过的 function，把返回的消息 list 转交给 client，client 原封不动发给 Claude。

---

## 实现 Format 命令 — Imports

先从 MCP SDK import base message types：

```python
from mcp.server.fastmcp import base
```

`base` 提供 `UserMessage`、`AssistantMessage` 等类型化对象，用来组 prompt 的消息 list。

---

## 实现 Format 命令 — 定义

```python
@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format."
)
def format_document(
    doc_id: str = Field(description="Id of the document to format")
) -> list[base.Message]:
    prompt = f"""
Your goal is to reformat a document to be written with markdown syntax.

The id of the document you need to reformat is:

{doc_id}


Add in headers, bullet points, tables, etc as necessary. Feel free to add in extra formatting.
Use the 'edit_document' tool to edit the document. After the document has been reformatted...
"""

    return [
        base.UserMessage(prompt)
    ]
```

要点：

- `@mcp.prompt(name=..., description=...)` 把 prompt 注册到 server，client 列清单时会看到这些字符串
- `doc_id: str = Field(description="...")` 是带 metadata 的参数，description 会传给 client 让用户知道要填什么
- Function body 用 f-string 组多行模板，返回 **消息 list**，这里只有一条 `UserMessage`
- 注意 prompt 内容引用了 `edit_document` **tool**——prompt 可以与 server 其他 tool / resource 合奏，是"用 server 能力组装工作流"的 recipe

---

## 为什么返回类型是 `list[base.Message]`

Prompts 可以编码多轮对话。例如你也可以预置一条 assistant 消息：

- `base.UserMessage(...)` — 用户"说"的
- `base.AssistantMessage(...)` — 预置的 assistant 响应（适合 few-shot conditioning）

返回 list 让 server 作者完全控制 prompt 启动时 Claude 看到的对话状态，client 只是回放消息。

---

## 用 MCP Inspector 测试

Inspector 有专门的 Prompts 区。测试步骤：

1. 跑 `uv run mcp dev mcp_server.py`
2. 浏览器打开 Inspector
3. 进 Prompts、选 prompt、填参数
4. Inspector 会显示生成的消息（就是即将发给 Claude 的内容）

这让你在接 client 之前就能确认变量正确插值、消息结构符合预期。

---

## Best Practices

本课提到：

1. **聚焦在 server 主要用途的任务** — 文档 server 应该出 `format`、`summarize`、`outline` 这类 prompt
2. **写详细具体的指令** — 模糊 prompt 产出模糊结果
3. **用不同输入充分测试** — 用 Inspector
4. **描述要清晰** — 用户按 description 挑 prompt
5. **设计 prompt 与 tool / resource 合奏** — 范围清晰的 prompt 会自然串到 server 的 tool（如 format prompt 最后调用 `edit_document`）

核心观点：**Prompt 是你作为 server 作者的专业**，以 client 可调用的形式固化。如果用户三十秒就能自己写出来，大概不需要做成 prompt；如果你花了一周才调出最佳措辞，那才是值得暴露的知识。

---

## Common Mistakes

1. **把 prompt 当原始字符串** — prompt 是 callable，返回 `base.Message` list，不是模板字符串
2. **忘了 `Field(description=...)`** — 没它，client 端无法告诉用户要填什么
3. **把 prompt 应该抓的数据写死** — 若 prompt 需要文档文本，应该引用对应的 tool / resource，不要把数据固化进 prompt
4. **写低成本 prompt** — 比用户自己打的还差的 prompt 是负价值，只上真正证明比 ad-hoc 更好的 prompt
5. **混淆 prompt 与 resource** — Prompt 是指令模板，resource 是数据，不要用 prompt 返回文档内容

> **Key Insight**
>
> Prompts 是大多数 MCP 讨论忽略的原语。Tools 给 Claude 能力，resources 给 context，prompts 给 **方向**。三种原语都有的 server 组合起来像一个小产品：client 能发现"能做什么"（tools）、"有什么数据"（resources）、"有哪些精心策划的起点"（prompts）。实务上，prompt 会变成用户看到的 slash-command 或快捷动作。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：Prompts 是 tools、resources 之外的第三种 MCP 原语；知道 `@mcp.prompt()` 装饰器、`name` / `description`、返回类型 `list[base.Message]`、参数的 `Field(description=...)`
- **D1（Agentic Architecture）**：Prompts 用 server 作者预先工程化的高质量开场消息 seed agent loop
- 考题模式："Server 作者要上线一个可复用、带参数的文档改写 markdown 指令，该用哪个 MCP 原语？" → prompt，用 `@mcp.prompt()` 定义

---

## Flashcards

| Front | Back |
|-------|------|
| MCP 的 prompts 是什么？ | Server 定义的预先调优、带参数的指令模板，client 可按名字调用，取得给 Claude 的高质量对话开场 |
| 定义 prompt 的装饰器？ | `@mcp.prompt(name=..., description=...)` |
| Prompt function 返回什么？ | `list[base.Message]`——组成对话开场的 user/assistant 消息 list |
| base message types 从哪里 import？ | `from mcp.server.fastmcp import base`，提供 `base.UserMessage`、`base.AssistantMessage` 等 |
| 参数 description 怎么到用户？ | 通过 `Field(description="...")` 放在参数上，MCP SDK 会传给 client |
| 为什么要出 prompt 而不是让用户自己写？ | Server 作者有测试过的专业级 prompt，暴露出来可以在不要求用户学 prompt engineering 的情况下提升结果质量 |
| 怎么在接 client 之前测 prompt？ | 跑 `uv run mcp dev mcp_server.py`，用 MCP Inspector 的 Prompts 区看生成的消息 |
| Format 示例怎么与其他 MCP 原语联动？ | 它引用 `edit_document` tool，显示 prompt 可以串接 tool 与 resource 完成任务 |
