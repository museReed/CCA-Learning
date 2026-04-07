# 访问 Resources — 工程深入解析

| 项目 | 细节 |
|------|--------|
| 考试范畴 | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP client implementation), 2.4 (resource consumption patterns), 2.5 (content type handling) |
| 来源 | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 11 |

---

## 一句话摘要

Client 端通过 `read_resource()` 搭配 `AnyUrl` 访问资源，处理 `ReadResourceResult.contents` 列表，并根据 MIME type 分支解析 JSON 或返回原始文本。

---

## Client 端 Resource 访问模式

Lesson 10 介绍了如何在 server 端定义 resources，本课聚焦在消费这些 resources 的 client 端代码。核心 function 是 `read_resource()`。

### 核心实现

```python
import json
from pydantic import AnyUrl

async def read_resource(self, uri: str) -> Any:
    result = await self.session().read_resource(AnyUrl(uri))
    resource = result.contents[0]

    if isinstance(resource, types.TextResourceContents):
        if resource.mimeType == "application/json":
            return json.loads(resource.text)

    return resource.text
```

### 逐行解析

1. **`AnyUrl(uri)`** — Pydantic 的 URL 验证器。接受任何 URI scheme（`docs://`、`file://`、自定义 scheme），在解析时验证格式。
2. **`result.contents[0]`** — 响应有 `contents` 列表。取第一个元素，因为单一 resource 请求通常返回一个项目。
3. **`isinstance(resource, types.TextResourceContents)`** — 类型检查，确认是文本内容（相对于二进制 `BlobResourceContents`）。
4. **MIME type 分支** — 如果是 `application/json`，用 `json.loads()` 解析。否则返回原始 `.text` 字符串。

---

## 响应结构深入解析

Server 返回的 `ReadResourceResult` 结构如下：

```
ReadResourceResult
  └── contents: list[TextResourceContents | BlobResourceContents]
        └── [0]
              ├── uri: str
              ├── mimeType: str
              ├── text: str  (TextResourceContents)
              └── blob: bytes (BlobResourceContents)
```

关键设计决策：
- **`contents` 是一个列表** — 虽然通常只有一个项目，但协议支持返回多个 content block
- **两种 content 类型** — `TextResourceContents` 用于文本数据，`BlobResourceContents` 用于二进制
- **MIME type 在 content 对象上** — 不在 result 包装器上，因为每个 content block 可以有不同类型

---

## MIME Type 处理策略

| MIME Type | 解析策略 | 返回类型 |
|-----------|---------------|-------------|
| `application/json` | `json.loads(resource.text)` | `dict` 或 `list` |
| `text/plain` | `resource.text` | `str` |
| `text/markdown` | `resource.text` | `str` |
| 二进制类型 | `resource.blob` | `bytes` |

---

## `@` 自动补全 UX 模式

从用户角度看，resource 访问驱动 `@mention` 工作流程：

1. **用户输入 `@`** — client 调用 `list_resources()` 填充自动补全下拉菜单
2. **用户用方向键浏览** — 从列表中选择想要的 resource
3. **用户按空格键确认** — client 调用 `read_resource(selected_uri)`
4. **内容注入 prompt** — resource 内容成为 prompt context 的一部分，不需要 tool call

这与 tool 根本不同：数据在 Claude **开始推理之前**就在 prompt 中，带来更快更准确的响应。

---

## 测试 Resource 访问

在 MCP Inspector 中：
1. 切换到 **Resources** 标签页
2. 点击 direct resource 立即读取
3. 对 templated resources，填入参数值
4. 查看响应结构：URI、MIME type、内容

在你的 CLI client 中：
1. 输入 `@` 触发自动补全
2. 选择一个 resource
3. 验证内容出现在 prompt context 中
4. 确认 Claude 可以在响应中引用该内容

---

## 常见错误

1. **忘记 `AnyUrl()` 包装** — 传入原始字符串而非用 Pydantic 的 `AnyUrl` 包装会导致类型错误
2. **没有处理 `contents` 列表** — 直接访问 `result.text` 而非 `result.contents[0].text`
3. **漏掉 JSON 解析** — 将 `application/json` 内容当作原始文本处理，导致 prompt 中出现字符串编码的 JSON
4. **忽略二进制 resources** — 没有处理非文本数据的 `BlobResourceContents`

> **Key Insight**
>
> Resource 内容直接进入 prompt — 不经过 tool call 处理。这意味着数据作为一级 context 提供给 Claude，降低延迟且避免模型需要「询问」信息。CCA 考试要记住：resources 是 **app-controlled**，在模型推理**开始前**注入 context。

---

## CCA 考试关联

- **D2 (Tool Design & MCP Integration)**：要熟悉 `read_resource()` 模式 — `AnyUrl`、`contents[0]`、MIME type 分支。这是可考的实现细节。
- **D1 (Agentic Architecture)**：理解 resources 不需 tool call 就能将 context 注入 prompt，对已知数据需求更有效率。
- 场景题可能描述「数据出现在聊天中」或「不需 Claude 询问就可用」— 这是 resource 访问，不是 tool 调用。

---

## Flashcards

| 正面 | 背面 |
|-------|------|
| `read_resource()` 中包装 URI 的 Pydantic 类型是什么？ | `AnyUrl` — 验证 URI 格式并接受任何 scheme（docs://、file:// 等） |
| 如何从 `ReadResourceResult` 访问实际内容？ | `result.contents[0]` — contents 字段是列表，取第一个元素 |
| Client 应如何处理 resource 的 `application/json` MIME type？ | 调用 `json.loads(resource.text)` 将 JSON 字符串解析为 Python dict/list |
| 用户选择 `@mention` 时，resource 内容去哪里？ | 直接注入 prompt context — 不触发 tool call |
| MCP resource 响应中的两种 content 类型是什么？ | `TextResourceContents`（文本/JSON 数据）和 `BlobResourceContents`（二进制数据） |
| 为什么 resource 访问比 tool 获取数据更快？ | Resource 数据在 Claude 开始推理前就在 prompt 中 — 不需要额外往返 |
| `@mention` 模式中什么触发自动补全列表？ | 用户输入 `@` 时，client 调用 `list_resources()` |
| MIME type 不是 `application/json` 时的默认回退是什么？ | 返回 `resource.text` 作为原始字符串 |
