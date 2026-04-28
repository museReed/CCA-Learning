# 定义 Prompts — 工程深入解析

| 项目 | 细节 |
|------|--------|
| 考试范畴 | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server primitives), 2.6 (prompt template design), 1.3 (prompt engineering for tools) |
| 来源 | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 12 |

---

## 一句话摘要

MCP prompts 是 server 端定义的参数化消息模板，返回 `list[base.Message]`，为用户提供预先构建且经过测试的指令，效果优于临时撰写的 prompt。

---

## 为什么需要 Prompts

用户已经可以直接向 Claude 提出任何要求。MCP prompts 的价值在于**专业知识封装**：

| 方式 | 质量 | 一致性 | 维护 |
|----------|---------|-------------|-------------|
| 用户自己写 prompt | 不稳定 — 取决于用户能力 | 低 — 每次不同 | 无 — 一次性 |
| MCP server 提供 prompt | 高 — 经开发者测试 | 高 — 每次用相同模板 | 集中化 — 更新一次，所有 client 受益 |

---

## `@mcp.prompt()` Decorator

Prompts 遵循与 tools 和 resources 相同的 decorator 模式：

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
<document_id>
{doc_id}
</document_id>

Add in headers, bullet points, tables, etc as necessary.
Feel free to add in structure.
Use the 'edit_document' tool to edit the document.
After the document has been reformatted...
"""
    return [
        base.UserMessage(prompt)
    ]
```

### 关键实现细节

1. **`name` 参数** — 成为 slash command 标识符（如 `/format`）
2. **`description` 参数** — 在 prompt 列表中显示给用户
3. **`Field(description=...)`** — Pydantic Field 用于参数文档说明
4. **返回类型 `list[base.Message]`** — 消息列表（UserMessage、AssistantMessage）发送给 Claude
5. **f-string 插值** — `{doc_id}` 在运行时替换为实际参数值

---

## Prompt 中的消息类型

Prompts 返回消息列表，可以包含：

```python
# 单一用户消息（最常见）
return [base.UserMessage(prompt_text)]

# 多轮对话（用于复杂工作流程）
return [
    base.UserMessage("Here is the task..."),
    base.AssistantMessage("I understand. Let me..."),
    base.UserMessage("Now proceed with step 2...")
]
```

多轮 prompts 适用于：
- **Few-shot 示例** — 在实际任务前示范 Claude 如何回应
- **复杂工作流程** — 引导 Claude 完成多步骤流程
- **角色设定** — 在任务指令前建立 Claude 的角色

---

## Prompt vs. Tool vs. Resource：控制模型

| Primitive | 控制者 | 触发方式 | 示例 |
|-----------|-----------|---------|---------|
| **Tool** | Claude（model-controlled） | Claude 在推理时决定 | `calculate_sqrt(3)` |
| **Resource** | 应用代码（app-controlled） | 你的代码调用 `read_resource()` | `@plan.md` 自动补全 |
| **Prompt** | 用户（user-controlled） | 用户输入 `/format` 或点击按钮 | `/format doc_id=plan.md` |

---

## 使用 MCP Inspector 测试

```bash
uv run mcp dev mcp_server.py
```

在 Inspector 中：
1. 切换到 **Prompts** 标签页
2. 从列表中选择 prompt
3. 填入参数值（如 `doc_id = "plan.md"`）
4. 点击「Get Prompt」查看插值后的消息
5. 验证 f-string 变量正确替换

---

## 设计最佳实践

1. **用 XML tag 标记变量边界** — `<document_id>{doc_id}</document_id>` 防止 prompt injection
2. **在 prompt 中引用可用的 tools** — 告诉 Claude 该用哪些 tools
3. **明确指定输出格式** — 如果要 markdown，就说「written with markdown syntax」
4. **用边界案例测试** — 空字符串、长文档、特殊字符
5. **保持 prompts 领域专属** — 文档 server 有格式化 prompts，数据 server 有分析 prompts

---

## 常见错误

1. **返回字符串而非 `list[base.Message]`** — prompts 必须返回 Message 对象列表
2. **忘记参数文档说明** — 用 `Field(description=...)` 让用户知道要提供什么
3. **没有引用 tools** — 如果 prompt 预期 Claude 使用特定 tools，要在 prompt 文本中明确提及
4. **过于泛用的 prompts** — prompts 应善用 server 的特定功能

> **Key Insight**
>
> Prompts 是 MCP 中的 **user-controlled** primitive。不同于 tools（Claude 决定何时行动）或 resources（你的 app 决定何时获取），prompts 通过 slash commands 或 UI 按钮给用户明确控制权。CCA 考试中，三方控制模型（model / app / user）是高频考点。

---

## CCA 考试关联

- **D2 (Tool Design & MCP Integration)**：要熟悉 `@mcp.prompt()` decorator 模式、返回类型（`list[base.Message]`）、以及通过 Pydantic `Field` 的参数处理。
- **D1 (Agentic Architecture)**：Prompts 代表 MCP 控制模型的用户控制层。
- 考试关键区分：「用户触发的预定义工作流程」= prompt。「Claude 决定行动」= tool。「App 获取数据」= resource。

---

## Flashcards

| 正面 | 背面 |
|-------|------|
| MCP prompt function 返回什么？ | `list[base.Message]` — UserMessage 和/或 AssistantMessage 对象的列表 |
| 谁控制 MCP prompts 的触发时机？ | 用户（user-controlled）— 通过 slash commands、按钮或菜单 |
| 定义 MCP prompt 的 decorator 是什么？ | `@mcp.prompt(name="...", description="...")` |
| 如何为用户说明 prompt 参数？ | 在 function 参数上使用 Pydantic `Field(description="...")` |
| 为什么在 prompt 模板中使用 XML tag 如 `<document_id>`？ | 明确标记变量边界、防止 prompt injection、帮助 Claude 识别结构化数据 |
| MCP 中 prompts 和 tools 的区别是什么？ | Prompts 是 user-controlled（用户明确触发），tools 是 model-controlled（Claude 决定何时调用） |
| MCP prompts 可以包含多轮对话吗？ | 可以 — 返回多个 UserMessage 和 AssistantMessage 对象，用于 few-shot 示例或复杂工作流程 |
| 部署前如何测试 prompts？ | 使用 MCP Inspector — 切换到 Prompts 标签页，填入参数，验证插值后的消息 |
