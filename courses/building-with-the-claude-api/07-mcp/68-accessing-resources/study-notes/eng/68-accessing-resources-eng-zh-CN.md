# Accessing Resources — Engineering Deep Dive（简体中文）

| 项目 | 说明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（MCP primitives：client 端 resource 访问）、2.2（content block types）、1.2（context 注入 agent loop） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 68 |

---

## One-Liner

Accessing resources 是"定义 resources"的 client 对偶——你在 MCP client 上添加 `read_resource(uri)`，按 MIME type 解析返回的 `contents` list，把结果交给应用在 Claude 看到之前注入 prompt。

---

## 为什么 Resources 比 Tool Call 更适合注入 context

本课开篇的核心论点：resources 让 server 暴露"可直接塞进 prompt"的数据，无需 tool call。优势是效率：

- **不必第二次 round trip** — 没有 `tool_use` / `tool_result` 循环
- **确定性** — 数据一定存在，不用等 Claude 决定
- **调试简单** — content block 更少，trace 容易读

用户输入 `@report.pdf` 发送时，应用通过 MCP client 抓取 resource，把文本 inline 进 prompt，Claude 在第一次 API 调用就收到整份文档。

---

## 实现 `read_resource`

在 MCP client 添加新方法：

```python
async def read_resource(self, uri: str) -> Any:
    result = await self.session().read_resource(AnyUrl(uri))
    resource = result.contents[0]
    # ... 按 MIME type 解析（见下一节）
```

要点：

- URI 要用 `AnyUrl`（pydantic）包一层再传给 SDK，保证类型正确
- `session().read_resource(...)` 是底层 SDK 调用
- response 的 `contents` 是 **list**，通常取第一个元素——包含实际数据与 metadata（含 MIME type）

返回类型标为 `Any`，因为不同 resource 会返回不同 Python 类型（字符串、dict、list、二进制），视 MIME type 而定。

---

## 按 MIME Type 解析

Resource 可能返回异构数据，client 必须按类型分支处理：

```python
if isinstance(resource, types.TextResourceContents):
    if resource.mimeType == "application/json":
        return json.loads(resource.text)

    return resource.text
```

本课涵盖两种情况：

1. **`application/json`** — server 返回结构化数据。用 `json.loads(resource.text)` 转成 Python 对象（dict 或 list）
2. **`text/plain`**（或其他文本）— 直接返回 `resource.text`

MIME type 是 server 通过 `@mcp.resource(mime_type=...)` 给 client 的契约，让 client 不用猜。

其他内容类型（二进制、图像）可以增加分支，但本课专注 text 与 JSON——足以覆盖 document mention 场景。

---

## 必要 Imports

两个 import 缺一不可：

```python
import json
from pydantic import AnyUrl
```

- `json` — 解析 JSON body
- `AnyUrl` — pydantic 的 URL 类型；`read_resource` 需要类型化 URL，不接受原始字符串

少了任一个都会报类型错误或运行时异常。

---

## 用 CLI 测试 Resource 访问

End-to-end 测试走 CLI：用户问"What's in the @report.pdf document?"时，系统会：

1. 用 autocomplete 列出可用 resources（`list_resources` 或类似）
2. 让用户选一个
3. 自动抓取 resource 内容（通过 `read_resource`）
4. 把内容放进送给 Claude 的 prompt

Claude 收到时文档已经在 context 中——不需要 tool call。

---

## 与应用集成

关键设计点：MCP client 代码会被 **应用其他部分** 使用。`read_resource` 是基础构件，上层组件调用它来：

- 抓文档内容注入 prompt
- 填 @mention autocomplete
- 把 resource 数据集成进 prompt

这种分层很重要：

| 层 | 职责 |
|----|------|
| MCP client | 跟 MCP server 沟通、解析响应 |
| 应用层 | 决定何时抓、注入到哪里 |
| Prompt builder | 组装最终发给 Claude 的消息 |

Client 故意做得"笨"——只负责读。业务逻辑留在应用层。

---

## 为什么比 Tool Call 更高效

比较两种做法对应同一用户意图（"读 report.pdf"）：

| 方法 | Round trips | Content blocks | 确定性 |
|------|------------|----------------|--------|
| Tool call（`read_doc_contents`） | 2（tool_use + tool_result） | tool_use、tool_result、最终文本 | Claude 决定是否调用 |
| Resource fetch（`read_resource`） | 1 | 只有 prompt 文本 | 应用保证一定抓 |

对于用户明确驱动的 context（"我在 @mention 这份文档"），resource 路径严格更优：更少 API 调用、更少 token、更快响应。

---

## Common Mistakes

1. **传入原始字符串 URI** — `read_resource` 需要 `AnyUrl`，跳过 `AnyUrl(uri)` 会引发类型错误
2. **忘记按 MIME type 分支** — 无条件返回 `resource.text` 会把 JSON 变成原始字符串，下游解析就坏了
3. **假设 `contents` 一定只有一个元素** — SDK 返回 list，通常取第一个但不保证，这个假设要写进注释
4. **双重 parse JSON** — server 若已用 `mime_type="application/json"` 序列化，text 本身就是 JSON；用 `json.loads` 正确，不要在 server 端再包一层
5. **把业务逻辑放进 `read_resource`** — Client 要薄，"何时抓"归应用层

> **Key Insight**
>
> `read_resource` 是 `@mcp.resource()` 的对称镜像——一边序列化，另一边反序列化，MIME type 是粘合剂。理解这种对称性，resource 支持的功能就会像干净的数据通道，而不是权宜 tool call。每个 MCP client 都有这三行 pattern：调用 `read_resource`、取 `contents[0]`、按 `mimeType` 分支。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：`read_resource` 是 `@mcp.resource()` 的 client 对偶；知道 method signature、`AnyUrl` 的用法、MIME type 分支模式
- **D1（Agentic Architecture）**：Resources 把 context 注入 agent loop 而无需 tool call，缩短 loop 并提高确定性
- 考题模式："要传给 `session.read_resource()` 的类型是什么？" → `AnyUrl`（来自 pydantic），而不是原始 string

---

## Flashcards

| Front | Back |
|-------|------|
| Client 读 resource 的核心方法？ | `async def read_resource(self, uri: str)`，内部调用 `self.session().read_resource(AnyUrl(uri))` |
| 传给 SDK 之前 URI 要用什么包一层？ | pydantic 的 `AnyUrl` |
| Response 的 `contents` 是什么？ | Resource content 对象 list，通常取 `result.contents[0]` |
| 如何解析 JSON 型 resource 响应？ | 检查 `resource.mimeType == "application/json"`，返回 `json.loads(resource.text)` |
| 如何解析纯文本 resource 响应？ | 直接返回 `resource.text` |
| Client 做 resource 访问需要哪两个 import？ | `import json` 与 `from pydantic import AnyUrl` |
| 为什么 resources 比 tool call 更高效？ | 一次 round trip 就够，数据直接内嵌 prompt，跳过 tool_use / tool_result 循环 |
| 谁决定调用 `read_resource`？ | 应用（按用户动作或策略），不是 Claude——Claude 不看 URI，只看到结果文本 |
