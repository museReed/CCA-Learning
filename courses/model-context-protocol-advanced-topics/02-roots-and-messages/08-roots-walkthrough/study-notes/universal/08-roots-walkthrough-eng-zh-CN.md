# Roots 实操演练 — 工程深度解析

| 项目 | 详情 |
|------|------|
| 考试领域 | D2 — 模型上下文协议 (23%), D4 — 安全与防护机制 (15%) |
| 任务说明 | 2.2 (MCP 基本要素 — roots), 4.3 (访问控制) |
| 来源 | model-context-protocol-advanced-topics / 02-roots-and-messages / 第 08 课 |

---

## 一句话摘要

Roots 是客户端定义的 `file://` URI，告诉 MCP 服务器它被允许访问哪些目录。客户端通过回调提供它们，而服务器必须自行实现授权逻辑来执行访问边界。

---

## 什么是 Roots？

Roots 是 MCP 的**文件系统访问控制**机制。它们回答了一个问题：「这个服务器应该能看到哪些目录？」

关键特性：
- Roots 由**客户端定义**（通常来自用户输入）
- 它们使用 `file://` URI 格式
- 服务器在运行时**请求**客户端提供 roots（非写死）
- MCP SDK **不会**自动执行 root 边界——你必须自己实现

---

## 步骤 1：从用户输入定义 Roots

```python
# main.py
import sys

async def main():
    # 从命令行参数获取根目录
    root_paths = sys.argv[1:]
    if not root_paths:
        print("Usage: uv run main.py <root1> [root2] ...")
        sys.exit(1)

    # 将 roots 传给 MCP 客户端
    doc_client = await stack.enter_async_context(
        MCPClient(
            command="uv", args=["run", "mcp_server.py"], roots=root_paths
        )
    )
```

理想情况下，用户指定服务器可以访问哪些目录。程序接受 CLI 参数作为路径，并传给 `MCPClient`。

---

## 步骤 2：创建 Root 对象

```python
# mcp_client.py
from mcp.types import Root, ListRootsResult
from pydantic import FileUrl
from pathlib import Path

def _create_roots(self, root_paths: list[str]) -> list[Root]:
    """将路径字符串转换为 Root 对象。"""
    roots = []
    for path in root_paths:
        p = Path(path).resolve()
        file_url = FileUrl(f"file://{p}")
        roots.append(Root(uri=file_url, name=p.name or "Root"))
    return roots
```

根据 MCP 规范，所有 roots 必须有以 `file://` 开头的 URI。此函数将用户提供的路径转换为正确的 `Root` 对象。

---

## 步骤 3：Roots 回调

```python
# mcp_client.py
async def _handle_list_roots(
    self, context: RequestContext["ClientSession", None]
) -> ListRootsResult | ErrorData:
    """服务器请求 roots 时的回调。"""
    return ListRootsResult(roots=self._roots)
```

客户端不会立即将 roots 发送给服务器。相反，服务器在未来某个时间点请求它们。回调在 `ListRootsResult` 对象内返回 roots。

此回调传入 `ClientSession`：

```python
self._session = await self._exit_stack.enter_async_context(
    ClientSession(
        _stdio,
        _write,
        list_roots_callback=self._handle_list_roots
        if self._roots
        else None,
    )
)
```

---

## 步骤 4：服务器访问 Roots

```python
# mcp_server.py
@mcp.tool()
async def list_roots(ctx: Context):
    """列出所有可访问的根目录。"""
    roots_result = await ctx.session.list_roots()
    client_roots = roots_result.roots
    return [file_url_to_path(root.uri) for root in client_roots]
```

Roots 通过调用 `ctx.session.list_roots()` 来访问。这会向客户端发送请求，触发根目录列表回调。

服务器在两种场景中使用 roots：
1. **授权文件访问** — 在工具读取或写入文件之前
2. **为 LLM 解析路径** — 当 Claude 需要找到文件位置时（例如「读取 todos.txt」）

---

## 步骤 5：实现访问控制

**重要**：MCP SDK 不会执行 root 边界。你必须自己实现该检查。

```python
# mcp_server.py
async def is_path_allowed(requested_path: Path, ctx: Context) -> bool:
    roots_result = await ctx.session.list_roots()
    client_roots = roots_result.roots

    if not requested_path.exists():
        return False

    if requested_path.is_file():
        requested_path = requested_path.parent

    for root in client_roots:
        root_path = file_url_to_path(root.uri)
        try:
            requested_path.relative_to(root_path)
            return True
        except ValueError:
            continue

    return False
```

授权函数的运作方式：
1. 从客户端获取 roots 列表
2. 检查请求的路径是否存在
3. 对于文件，检查其父目录
4. 使用 `relative_to()` 验证路径是否在允许的 root 内
5. 如果没有匹配的 root，返回 `False`

---

## 步骤 6：在工具中使用授权

```python
@mcp.tool()
async def convert_video(input_path: str, format: str, *, ctx: Context):
    """将 MP4 视频文件转换为其他格式。"""
    input_file = VideoConverter.validate_input(input_path)

    # 确保输入文件在某个 root 内
    if not await is_path_allowed(input_file, ctx):
        raise ValueError(f"Access to path is not allowed: {input_path}")

    return await VideoConverter.convert(input_path, format)
```

每个访问文件系统的工具都应在继续之前调用 `is_path_allowed()`。

---

## CCA 考试相关性

- Roots 是 **D2 基本要素**（任务 2.2）也是 **D4 安全关注点**（任务 4.3）
- 最关键的考试重点：**MCP SDK 不会自动执行 root 边界**——你必须自己实现授权
- 回调模式（客户端通过 `list_roots_callback` 按需提供 roots）是常考重点
- Root URI 必须使用 `file://` 协议
- 预期会有场景题，访问控制缺失，你需要找出漏洞
- `relative_to()` 路径验证模式是 D4 中常见的实现细节考点

---

## 记忆卡

| # | 问题 | 答案 |
|---|------|------|
| 1 | 在 MCP 中，谁定义 roots？ | **客户端**定义 roots，通常基于用户输入 |
| 2 | Roots 必须使用什么 URI 协议？ | `file://` |
| 3 | MCP SDK 会自动执行 root 边界吗？ | **不会**——你必须自己实现授权逻辑 |
| 4 | 服务器如何向客户端请求 roots？ | 调用 `ctx.session.list_roots()`，触发客户端的 `list_roots_callback` |
| 5 | Roots 回调返回什么？ | 一个包含 `Root` 对象列表的 `ListRootsResult` 对象 |
| 6 | 用什么 Python 方法检查路径是否在 root 内？ | `Path.relative_to()`——如果路径在 root 外会抛出 `ValueError` |
| 7 | 服务器在哪两种场景中使用 roots？ | 1) 授权文件/文件夹访问，2) 为 LLM 解析路径 |
| 8 | `list_roots_callback` 在哪里注册？ | 在 `ClientSession` 构造函数中 |
