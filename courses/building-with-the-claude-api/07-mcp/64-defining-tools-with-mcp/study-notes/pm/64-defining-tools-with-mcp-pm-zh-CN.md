# Defining Tools with MCP — PM 视角

| 项目 | 说明 |
|------|------|
| 考试领域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.1（tool schemas）、2.3（MCP primitives：tools）、1.2（agent loop 集成） |
| 来源 | building-with-the-claude-api / 07-mcp / Lesson 64 |

---

## 一句话总结

Lesson 64 是 tool 编写变**便宜**的时刻：Python MCP SDK 把手写 JSON Schema 替换成 decorated function，把"写出第一个 tool 的时间"从"一整天样板"压缩到"一段 Python"——这会改变 PM 该怎么 scope AI 功能。

---

## 心智模型：从电路图到名片

SDK 出现之前，加 tool 像在画电路图：

| SDK 之前（手写 JSON） | 有 SDK（decorator + type hints） |
|--------------------|-----------------------------|
| 长长的 JSON Schema 文档 | Decorated Python function |
| 很容易漏 `required` key | SDK 从 function signature 自动填 |
| 非作者工程师难读 | 读起来像业务逻辑 |
| 文档离 code 很远 | Description 就在参数旁边 |

把 MCP tool（加上 SDK）想象成**名片**：小、标准化、易读——新 tool 几行就能写完，直接递给 Claude 用。

---

## 为什么这节课对 PM 重要

SDK 的人体工学带来三个产品层级的后果：

1. **Tool 数量变便宜。** 加一个新 tool 只要几分钟，PM 可以安全地要求更细致的功能——每个 intent 一个 tool——而不是把行为塞在 mega-tool 里。
2. **Description 变成产品文案。** `description` 是 Claude 的操作手册；写好它是 PM/writer 的工作，不只是工程的。它就是 tool 的 prompt engineering。
3. **错误处理是 UX 的一部分。** Tool 失败时（`ValueError`），Claude 会把错误呈现给用户。也就是说 tool 错误消息是**用户可见的文案**。PM 该 review。

---

## 两个 Demo Tools 的走查

这节课针对内存文档集合实现了两个 tools：

| Tool | 业务角色 |
|------|---------|
| `read_doc_contents` | "让 Claude 用 ID 查特定文档" |
| `edit_document` | "让 Claude 提议并执行 find/replace 编辑" |

Description 明确警告 Claude 注意细节陷阱——例如 `old_str` 指定"必须精确匹配，包括空白"。PM 读到这里应该把 tool description 当成 **Claude 和真实世界副作用之间的 guardrail**。

### Find/Replace 的警告（产品警示）

`edit_document` 用 Python 的 `str.replace`，会替换文档里**所有**出现位置。Demo 这样没问题；真实产品里这是枪自己的脚：

> "把 'budget' 这个词换成 'expenditure'"可能默默把整份文档的每个 budget 都换掉，而不是用户原本想改的那一处。

PM 该标记这一点。真实产品通常需要：

- 对 match 做唯一性检查
- 套用前预览
- 所有编辑的 audit log
- 破坏性动作的用户确认

---

## 产品应用场景

### 轻量 tool 编写有回报的地方

| 场景 | 为什么合适 |
|------|----------|
| 快速功能迭代 | 新 tool 只是约 10 行改动，PM 可以试验 |
| Domain 专属助手 | 一个 domain 动作一个 tool（读政策、提议编辑、发摘要） |
| 内部平台团队 | 通过共享 MCP server 标准化公司 tool 函数库 |
| Tool 目录 | 多个 tool 各司其职，Claude 在 runtime 选择 |

### 低摩擦是风险的地方

| 场景 | 警告 |
|------|------|
| 变更 production 系统 | 低摩擦让风险 tool 很容易就 ship——要强制 review |
| Tool 名字歧义 | Claude 的选择取决于 description 质量，草率的文案 = 选错 tool |
| Tool 重叠 | 两个 tool 做类似的事会让 Claude 混淆；PM 该去重 |
| 沉默的 side effect | `edit_document` 替换所有匹配项；真实产品需要明确确认 |

---

## PM 决策框架：review 一个 Tool PR

团队加新 MCP tool 时，PM 该检查：

1. **Tool `name` 清楚且动词化了吗？**（`read_doc_contents`，不是 `docs_tool_3`）
2. **`description` 有告诉 Claude 它做什么 AND 不做什么吗？**（例如"必须精确匹配，包括空白"）
3. **每个参数都有 `Field(description=...)` 吗？** 缺 description 会降低 tool 质量。
4. **失败时会怎样？** Tool 应该 raise 用户可读的错误，而不是默默失败。
5. **Tool 是破坏性的吗？** 如果是，产品流程有批准/确认吗？
6. **和既有 tools 有重叠吗？** 有的话合并或改名厘清。

---

## Description 就是文案撰写

MCP tool description 大概是 Claude 产品里最被低估的文案：

| 属性 | 含义 |
|------|------|
| Claude 读，不是用户读 | 没有营销包装；简明宣示性语言胜出 |
| 用于 tool 选择 | 歧义的 description → 叫错 tool |
| 约束 agent 行为 | 你可以设定期待（"只有你有精确 doc ID 才用"） |
| 工程 reviewer 看不出来 | Code review 抓不到弱文案——PM 必须 review |

PM 的直觉法则：如果 tool description 过不了技术写作的 review，它大概也过不了 Claude 的。

---

## 常见 PM 错误

1. **Review tool code 但不 review tool description** — description 是和 Claude 的 API contract。
2. **Scope mega-tools** — 一个"什么文档操作都做"的 tool 比三个专注的 tool 更难让 Claude 使用。
3. **忽略破坏性副作用** — `edit_document` 默默替换所有匹配项；需要产品 UX 来围住它。
4. **以为错误消息只是内部的** — `ValueError` 文字会通过 Claude 到达终端用户；要写清楚。
5. **把 SDK 人体工学当成"只是工程问题"** — 生产力赢面改变了 PM 能试验的速度。

> **Key Insight**
>
> 用 Python SDK 做的 MCP tool 定义是 PM 的 surface，不只是工程 surface。`name`、`description`、和参数 doc 是产品文案，会塑造 Claude 行为和用户可见的输出。当 tool 编写变这么便宜，瓶颈从工程努力转移到产品判断——那就是 PM 赚饭钱的地方。

---

## CCA 考试重点

- **D2（Tool Design & MCP Integration）**：知道 SDK 模式是 `FastMCP` + `@mcp.tool(...)` + `Field(description=...)`。
- **D1（Agentic Architecture）**：理解 tool error（raised exception）会通过 agent loop 传递，Claude 能把它纳入下一轮。
- 预期有情境题问 tool 命名、description 质量、错误呈现。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 从 SDK-based tool 模式 PM 该带走什么？ | Tool 编写现在够便宜，PM 可以要求更多、更窄的 tool，不是 mega-tool。 |
| 谁该 review tool 的 `description` 字段？ | PM——它是塑造 Claude 行为的产品文案。 |
| 这节课 `edit_document` 的隐藏风险是什么？ | 它叫 `str.replace`，会替换每个出现位置；真实产品需要唯一性或确认。 |
| Tool 错误为什么在产品层级重要？ | Tool `raise ValueError` 时，Claude 会把消息呈现给用户——它是用户可见文案。 |
| 参数没有 `Field` description 会怎样？ | Claude 只看到参数名，所以 tool 选择和使用质量下降。 |
| Demo server 对外提供几个 tools，各做什么？ | 两个：`read_doc_contents` 和 `edit_document`（find-and-replace）。 |
| PM 对 tool 重叠的规则是什么？ | 两个 tool 做类似的事会让 Claude 混淆——去重或改名。 |
| 一句话框架 tool description 给 PM？ | 它们是 Claude 的操作手册，因此是产品文案。 |
