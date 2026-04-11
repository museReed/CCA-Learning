# Defining Resources — Engineering Deep Dive（简体中文）

| 项目 | 说明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（MCP primitives：tools vs resources vs prompts）、2.2（content block types）、1.2（把 context 注入 agent loop） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 67 |

---

## One-Liner

Resources 是 MCP 中"暴露数据"的原语，行为像 HTTP GET handler，用 URI 寻址，用 MIME type 决定序列化方式，分两种：direct（静态 URI）和 templated（带参数的 URI）。

---

## Resource vs Tool：心智切分

MCP server 有三种原语：tools、resources、prompts。决定一个新能力属于哪种时，第一个要问的就是"它是 resource 还是 tool？"

| 方面 | Resource | Tool |
|------|----------|------|
| 用途 | 暴露数据（读） | 执行动作（读或写） |
| 类比 | HTTP GET | HTTP POST / RPC |
| 标识 | URI（`docs://documents/{id}`） | Named function + JSON schema |
| 典型用法 | 取文档、列清单 | 编辑、删除、发送 |
| 谁决定调用 | Client / 应用，直接塞进 prompt | Claude 在推理时自己决定 |

经验法则：如果是 pure read、用户或应用想直接在 prompt 中引用，就做成 resource；如果是动作（尤其希望 Claude 在 agent loop 里自主调用），就做成 tool。

---

## 动机示例：`@document_name` mention

课程用一个具体功能切入 resources：用户在 CLI 输入 `@`，应用弹出文档 autocomplete；选好并提交后，应用把文档内容注入 prompt。

需要两个操作：

1. **列出所有文档** → 给 autocomplete
2. **取特定文档内容** → 注入 prompt

两个都是纯读，完美对应 resources。

---

## Request / Response 流程

Resources 走 request-response 模式：client 发 `ReadResourceRequest` 带 URI，server 回数据。URI 就是 resource 的地址。

```
Client ── ReadResourceRequest(uri="docs://documents/report.pdf") ──▶ Server
Client ◀──────── TextResourceContents(text=..., mimeType=...) ────── Server
```

故意做得很简单：没有 schema negotiation、没有 tool loop、没有第二次 Claude 调用。Resources 就是用 URI 拉数据。

---

## 两种 Resource

### Direct Resources

固定 URI，不会变。用于静态数据端点，例如"给我所有文档的清单"。

### Templated Resources

URI 嵌入大括号参数。Python SDK 会解析 URI、抽出参数，以 keyword argument 传给你的 function。用于带参数的取值，例如"给我文档 X"。

URI template 的参数名必须跟 function signature 完全一致——SDK 按名字配对。

---

## 用 `@mcp.resource()` 实现

### Direct Resource：列出文档

```python
@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    return list(docs.keys())
```

- URI `docs://documents` 是静态的
- 返回 Python list，SDK 看到 `application/json` 会自动序列化
- 没有参数，就是纯粹的目录列表

### Templated Resource：取单个文档

```python
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]
```

- URI 中的 `{doc_id}` 变成 function keyword argument
- `mime_type="text/plain"` 因为返回值是纯文本
- 错误抛 Python exception，SDK 会转成正确的错误 response

---

## MIME Types

Resources 可以返回任何数据类型：字符串、JSON、二进制。`mime_type` 告诉 client 怎么解析：

- `application/json` — 结构化 JSON，SDK 自动序列化
- `text/plain` — 纯文本
- 其他任何合法 MIME type

关键便利：**SDK 会帮你序列化**。你只要返回 Python 值（list、dict、str），SDK 根据 MIME type 转换，不用自己做 `json.dumps`。

---

## 用 MCP Inspector 测试

Dev mode 启动 server：

```bash
uv run mcp dev mcp_server.py
```

浏览器打开 Inspector，会看到两个相关区域：

- **Resources** — 列出 direct / 静态 resources
- **Resource Templates** — 列出 templated resources 与参数 schema

点任何一个都可以跑一次，看到 client 实际会收到的 response 结构。这是验证 URI、MIME type、return shape 最快的方式，接 client 之前先测过。

---

## 关键规则

- Resources 暴露数据；tools 执行动作
- Direct = 静态 URI；templated = 带 `{params}` 的 URI
- Templated URI 的参数名必须与 function argument 名字一致
- MIME type 指引 client 解析，并启用自动序列化
- Python SDK 自动序列化——不要自己转 JSON

---

## Common Mistakes

1. **用 resource 做有副作用的操作** — 写入、发送、删除属于 tools，不是 resources
2. **URI 参数和 function argument 名字不一致** — `{doc_id}` 必须对应 `doc_id: str`
3. **自己做 JSON 序列化** — 设了 `mime_type="application/json"` 后 SDK 会做，重复序列化会产生嵌套 JSON 字符串
4. **忘了设 `mime_type`** — client 靠它决定怎么 parse，设错或默认会把本该是 JSON 的变成纯文本
5. **不用 Inspector 先测** — 跳过 MCP Inspector 意味着第一次真实调用就是第一次测试

> **Key Insight**
>
> Resources 是 **以 URI 寻址的数据端点**。URI 就是整个 API 契约——选好 URI（如 `docs://documents/{doc_id}`）等同于设计 REST API。好的 resource 设计：稳定的 URI、清晰的 MIME type、明确的 tool/resource 切分。Resource 由 client 决定是否拉取；tool 由 Claude 决定是否调用。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：Resources 是 MCP 三个 primitives 之一（tools、resources、prompts）；认得 `@mcp.resource()` 装饰器、URI 与 `mime_type`；知道 direct vs templated 的差异
- **D1（Agentic Architecture）**：Resources 是 MCP server 向 agent loop 提供 context 的方式，不需要 tool call——由 client 拉取后注入
- 考题模式："Server 要以 ID 暴露文档内容，让 client 注入 prompt，该用 tool 还是 resource？" → resource

---

## Flashcards

| Front | Back |
|-------|------|
| MCP 的 resources 是什么？ | Server 端以 URI 寻址的数据端点，类似 HTTP GET handler，用来暴露数据而非执行动作 |
| Resources 有哪两种？ | Direct（静态 URI 如 `docs://documents`）和 templated（带参数如 `docs://documents/{doc_id}`） |
| 定义 resource 的装饰器？ | `@mcp.resource(uri, mime_type=...)` |
| Templated URI 参数怎么到你的 function？ | SDK 从 URI 解析后以 keyword argument 传入，按名字配对 |
| 什么时候用 resource、什么时候用 tool？ | Resource 给 client 要拉的纯读；tool 给动作（尤其希望 Claude 自主调用的） |
| `mime_type` 参数做什么？ | 告诉 client 怎么解析 response，并启用 SDK 自动序列化（如 `application/json`） |
| 怎么本地测试 resources？ | `uv run mcp dev mcp_server.py`，用浏览器的 MCP Inspector，会看到 Resources 与 Resource Templates |
| 要不要自己 JSON 序列化返回值？ | 不用，SDK 会根据 `mime_type` 自动处理 |
