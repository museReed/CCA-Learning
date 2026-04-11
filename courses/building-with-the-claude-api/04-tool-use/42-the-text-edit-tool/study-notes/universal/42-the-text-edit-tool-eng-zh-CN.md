# Text Editor Tool — Engineering Deep Dive

| 项目 | 内容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%)、D1 — Agentic Architecture (22%) |
| Task Statements | 2.3（built-in / server tools）、2.1（tool schema 与选择）、1.2（tool 编排） |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 42 |

---

## One-Liner

Text editor tool 是 Anthropic 内置的 tool:Claude 本身已经知道完整 schema,你只需要声明一个很小的 stub（`type` + `name`）,然后自己写执行 Claude 指令用的文件操作实现。

---

## 为什么叫"内置" Tool

大部分 tool 需要你准备两件事：

1. 描述每个参数的完整 JSON schema
2. 实际执行的 Python 函数

Text editor tool 不一样。Anthropic 在模型内部**预先定义好完整 schema**,涵盖所有支持的文件操作。你：

- **不需要**定义 `path`、`command`、`old_str`、`new_str` 这些参数
- **不需要**写完整 JSON schema
- **需要**声明一个小 stub 告诉 Claude "启用这个内置 tool"
- **需要**写实际操作文件的本地函数

Claude 那一侧是黑箱;你这一侧依然重要。

---

## 支持的操作

Text editor tool 让 Claude 能像使用本地编辑器的软件工程师一样工作：

| Operation | 功能 |
|-----------|-----|
| **view** | 读取文件或列出目录;可以看特定行范围 |
| **create** | 创建新文件并写入初始内容 |
| **str_replace** | 将文件中某个字符串换成另一个（最常见的编辑） |
| **insert** | 在指定行号插入文字 |
| **undo_edit** | 撤销最近一次的编辑 |

这些合起来涵盖核心编辑能力——读、写、创建、修改、还原。

---

## 声明 Stub

Stub 内容依 Claude 模型系列而异。Lesson 给的 helper：

```python
def get_text_edit_schema(model: str) -> dict:
    if model.startswith("claude-3-7-sonnet"):
        return {
            "type": "text_editor_20250124",
            "name": "str_replace_editor",
        }
    elif model.startswith("claude-3-5-sonnet"):
        return {
            "type": "text_editor_20241022",
            "name": "str_replace_editor",
        }
    # 最新的 version string 请查 Anthropic 官方文档
```

重点：

- `type` 是**按模型系列 versioned** 的,字符串必须跟你使用的模型对得上。Anthropic 把对应表放在 `docs.anthropic.com/en/docs/agents-and-tools/tool-use/text-editor-tool`。
- `name` 对应每个 version 是固定的（比如上面两个版本都是 `str_replace_editor`）。
- Claude 会在内部把 stub 展开成完整 schema,你看不到参数定义。

---

## 当成普通 Tool 传进去

```python
import anthropic

client = anthropic.Anthropic()
model = "claude-3-5-sonnet-20241022"

response = client.messages.create(
    model=model,
    max_tokens=2048,
    tools=[get_text_edit_schema(model)],
    messages=[
        {"role": "user", "content": "Open ./main.py 并总结内容"},
    ],
)
```

Claude 会返回一个 `tool_use` block,`name` 是 `str_replace_editor`,`input` 包含 Claude 想执行的指令（比如 `{"command": "view", "path": "./main.py"}`）。你的代码要根据 `input["command"]` dispatch 并执行动作。

---

## 提供实现

你负责真正操作文件系统。最小版本的 dispatcher：

```python
def run_text_editor(tool_input: dict) -> str:
    command = tool_input["command"]
    path = tool_input["path"]

    if command == "view":
        with open(path) as f:
            return f.read()

    elif command == "create":
        with open(path, "w") as f:
            f.write(tool_input["file_text"])
        return f"已创建 {path}"

    elif command == "str_replace":
        with open(path) as f:
            content = f.read()
        new_content = content.replace(
            tool_input["old_str"],
            tool_input["new_str"],
            1,
        )
        with open(path, "w") as f:
            f.write(new_content)
        return "替换完成"

    elif command == "insert":
        # 在 tool_input["insert_line"] 插入文字
        ...

    elif command == "undo_edit":
        # 还原前一版本
        ...

    else:
        return f"未知 command: {command}"
```

你决定：

- 什么算 Claude 的文件系统沙箱
- 是否允许写入、只读、或限制路径
- 是否维护 undo stack 供 `undo_edit` 使用

---

## 示例 Workflow

Prompt：*"Open ./main.py,添加一个计算 pi 到小数第 5 位的函数,然后创建 ./test.py 并写单元测试。"*

Claude 的 turn 序列：

1. `tool_use`：`view ./main.py`
2. 你的代码返回文件内容
3. `tool_use`：`str_replace` 注入新函数
4. 你的代码执行替换并回报
5. `tool_use`：`create ./test.py` 含单元测试内容
6. 你的代码创建文件并回报
7. 最后 assistant text："完成——已新增 `compute_pi` 并写好测试。"

每个 `tool_use` 都是 agentic loop 中的一次往返。

---

## 为什么需要 Text Editor Tool

既然现代编辑器已经内置 AI 助手,为什么要通过 API 暴露这个？因为它可以：

- 为需要**以程序方式**编辑文件的应用服务（如 codemod 服务、迁移 bot）
- 在**没有完整编辑器**的 agent 环境中使用
- 让 **Claude 驱动的应用**原生嵌入文件编辑能力
- 在 CI pipeline 中做**无头自动化**

简言之,它让你可以在自家产品中复制"AI code editor"的功能,并能对文件系统接口做细致控制。

---

## Common Mistakes

1. **模型与 version string 对不上** — `text_editor_20241022` 配 3.7 Sonnet 或反过来。请一律查 Anthropic 官方文档最新对应。
2. **试图写完整 JSON schema** — 只需要 stub,Claude 已经知道参数。
3. **没实现 `undo_edit`** — Claude 尝试还原时,你的 handler 若忽略,workflow 就坏了。
4. **没做沙箱就执行** — Claude 可以写任意文件,必须限定目录并校验路径。
5. **忘了 `view` 也能针对目录** — 你必须支持列目录,不只是读文件。

> **Key Insight**
>
> "内置"形容的是 **schema**,不是 **执行**。Anthropic 把 schema 知识放在模型里,但你还是要自己写真正操作文件系统的 Python 代码。Text editor tool 是一种 hybrid：Anthropic 懂 API,你拥有 runtime。

---

## CCA Exam Relevance

- **D2 (Tool Design)**：Text editor tool 是 built-in（schema 内置）tool 的典型代表,由开发者提供执行逻辑。
- **D1 (Agentic Architecture)**：文件操作链（view → edit → create → test）是典型的多轮 agentic 模式。
- 题目可能对比 built-in tool（如 text editor）与 server tool（如 web search）,后者由 Anthropic 完全处理执行。

---

## Flashcards

| Front | Back |
|-------|------|
| 用 text editor tool 要声明什么？ | 一个小 stub,包含 `type`（versioned）与 `name`（比如 `str_replace_editor`） |
| Text editor tool 的 schema 由谁提供？ | Anthropic — Claude 已经知道参数,你不需要定义 |
| Text editor tool 的执行由谁提供？ | 开发者 — 你写执行 Claude 指令的文件操作函数 |
| Text editor tool 支持哪些操作？ | view、create、str_replace、insert、undo_edit |
| 为什么 `type` 字符串带日期（如 `text_editor_20241022`）？ | 因为 schema 按 Claude 模型系列 versioned,version 必须对应你的模型 |
| Claude 能不能用这个 tool 看目录？ | 可以——`view` 对文件和目录都有效 |
| 没沙箱跑 text editor tool 有什么风险？ | Claude 可以写任意文件,路径校验与沙箱目录是必要的 |
| 既然编辑器已经有 AI,为什么还需要这个 tool？ | 让 Claude 驱动的应用嵌入程序化文件编辑能力,适合 codemod、agent、无头自动化 |
