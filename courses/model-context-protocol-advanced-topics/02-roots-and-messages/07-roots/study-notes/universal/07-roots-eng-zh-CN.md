# Roots — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.2 (MCP security model), 2.3 (MCP server capabilities) |
| Source | model-context-protocol-advanced-topics / 02-roots-and-messages / Lesson 07 |

---

## One-Liner

Roots 授予 MCP server 访问特定文件和目录的权限，解决文件路径发现问题，同时提供安全边界限制 server 可访问的范围。

---

![Roots Access](../../visuals/roots-access-zh-TW.svg)


## Roots 解决的问题

没有 roots 时，处理文件的 MCP server 面临根本性问题：**它怎么知道该去哪里找？**

- Claude 无法搜索整个文件系统
- 用户不应该需要输入完整路径如 `/Users/reed/Documents/project/src/main.py`
- Server 对用户的工作空间毫无概念

Roots 通过给 server 一份核准的起始目录清单来解决问题。

---

## Roots 如何运作

流程很直观：

```
Client                     Server
  |                          |
  |-- list_roots() --------->|  (server 问：「我能访问什么？」)
  |<-- [Root("/projects"),   |
  |     Root("/data")]  -----|  (client 答：「这些目录」)
  |                          |
  |                          |-- read_dir("/projects") -->
  |                          |-- 找到目标文件 ----------->
  |                          |-- 对文件使用 tool -------->
```

1. Server 调用 `list_roots()` 发现核准的目录
2. Server 读取这些目录寻找文件
3. Server 只在 root 边界内操作

---

## Server 端：使用 Roots

```python
@mcp.tool()
async def find_and_read(ctx: Context, filename: str) -> str:
    # 步骤 1：获取核准的 roots
    roots = await ctx.session.list_roots()

    # 步骤 2：在 roots 内搜索
    for root in roots:
        root_path = Path(root.uri.replace("file://", ""))
        for path in root_path.rglob(filename):
            if path.is_file():
                return path.read_text()

    return f"File '{filename}' not found in any root"
```

要点：
- Roots 以 URI 格式返回（如 `file:///Users/reed/project`）
- Server 必须将 URI 转换为文件系统路径
- `rglob()` 在每个 root 内递归搜索

---

## Client 端：声明 Roots

Client 定义 server 可以访问哪些目录：

```python
from mcp import Root

roots = [
    Root(uri="file:///Users/reed/projects/my-app", name="My App"),
    Root(uri="file:///Users/reed/data", name="Data Directory"),
]

# Roots 在 client session 设置时提供
async with ClientSession(read, write) as session:
    await session.initialize()
    # Client 通过 list_roots handler 暴露 roots
```

Client 完全控制暴露什么 — 这是安全特性。

---

## 安全性：SDK 不会自动强制执行

这是考试最关键的重点：

**MCP SDK 不会自动强制 root 边界。** Server 收到 root 清单，但没有任何机制阻止它访问那些 roots 之外的文件。你必须自己实现强制执行：

```python
def is_path_allowed(file_path: str, roots: list[Root]) -> bool:
    """检查路径是否在核准的 root 内。"""
    target = Path(file_path).resolve()
    for root in roots:
        root_path = Path(root.uri.replace("file://", "")).resolve()
        if target.is_relative_to(root_path):
            return True
    return False

@mcp.tool()
async def safe_read(ctx: Context, file_path: str) -> str:
    roots = await ctx.session.list_roots()

    if not is_path_allowed(file_path, roots):
        raise PermissionError(f"Access denied: {file_path} is outside approved roots")

    return Path(file_path).read_text()
```

务必使用 `.resolve()` 防止 path traversal 攻击（如 `../../etc/passwd`）。

> **Key Insight**
> Roots 是 **惯例**，不是 sandbox。SDK 提供发现核准目录的机制，但 server 开发者必须自己实现访问控制。这是常考题 — 答案永远是「自己实现 `is_path_allowed()`」。

---

## Roots 的好处

| 好处 | 说明 |
|------|------|
| **用户友好** | 用户说「看我的项目」而不是打完整路径 |
| **聚焦搜索** | Server 搜索特定目录，非整个文件系统 |
| **安全边界** | 限制 server 应访问的范围（有强制时） |
| **灵活性** | Client 可动态新增/移除 roots |
| **多项目支持** | 多个 roots 可指向不同项目 |

---

## Path Traversal 防护

实现 `is_path_allowed()` 时，处理这些攻击向量：

```python
# 需防范的危险输入：
"../../../etc/passwd"           # 相对路径逃脱
"/Users/reed/projects/../.ssh"  # 路径中段穿越
"./symlink_to_root"             # Symlink 逃脱

# 防御：永远先解析为绝对路径
target = Path(file_path).resolve()  # 解析 symlinks 和 ..
```

---

## CCA Exam Relevance

- **D2 Task 2.2**：MCP 安全模型 — roots 是主要的文件系统安全机制
- **D2 Task 2.3**：Server capabilities — `list_roots()` 是基础功能
- 预期考题关于 enforcement — 答案永远是「SDK 不自动强制，需手动实现」
- Path traversal 防护是常见情境题
- 核心考试哲学：**Validation > Trust** — 不要假设 server 会自律

---

## Flashcards

| Front | Back |
|-------|------|
| MCP roots 解决什么问题？ | 文件路径发现 — 给 server 核准的起始目录，而非搜索整个文件系统 |
| MCP SDK 会自动强制 root 边界吗？ | 不会 — server 收到 root 清单但必须手动实现 `is_path_allowed()` 强制执行 |
| Server 调用什么方法发现核准目录？ | `ctx.session.list_roots()` |
| Roots 以什么格式返回？ | URI（如 `file:///Users/reed/project`） |
| 为什么检查路径时必须调用 `.resolve()`？ | 防止使用 `..` 或 symlink 的 path traversal 攻击 |
| 谁控制暴露哪些 roots？ | Client — 在 session 设置时定义 root 清单 |
| Roots 可以动态变更吗？ | 可以 — client 可在 session 期间新增或移除 roots |
| Roots 背后的安全哲学是什么？ | 惯例而非 sandbox — 机制存在但 enforcement 是开发者的责任 |
