# Client 端的 Prompts — 工程深入解析

| 项目 | 细节 |
|------|--------|
| 考试范畴 | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP client implementation), 2.6 (prompt consumption patterns), 1.3 (prompt orchestration) |
| 来源 | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 13 |

---

## 一句话摘要

Client 实现 `list_prompts()` 来发现可用 prompts，以及 `get_prompt(name, args)` 来获取插值后的消息，启用 slash command（`/`）UX 模式，让用户触发预定义工作流程。

---

## 两个 Client 端方法

### 1. `list_prompts()` — 发现

```python
async def list_prompts(self) -> list[types.Prompt]:
    result = await self.session().list_prompts()
    return result.prompts
```

此方法向 server 查询所有可用 prompts。每个 `types.Prompt` 对象包含：
- `name` — 标识符（用于 slash commands）
- `description` — 人类可读的说明
- `arguments` — 必要/可选参数列表

### 2. `get_prompt()` — 带插值的获取

```python
async def get_prompt(self, prompt_name, args: dict[str, str]):
    result = await self.session().get_prompt(prompt_name, args)
    return result.messages
```

此方法获取特定 prompt 并进行变量插值：
- `prompt_name` — 要获取哪个 prompt（如 `"format"`）
- `args` — 字符串对字符串的 dict（如 `{"doc_id": "plan.md"}`）
- 返回 `result.messages` — 准备好发送给 Claude 的 `base.Message` 对象列表

---

## 完整的 Prompt 工作流程

从用户交互到 Claude 响应的端到端流程：

```
1. 用户输入 "/"
   └── Client 调用 list_prompts()
       └── Server 返回可用 prompts

2. 用户选择 "/format"
   └── Client 显示参数输入
       └── 用户提供 doc_id = "plan.md"

3. Client 调用 get_prompt("format", {"doc_id": "plan.md"})
   └── Server 执行 format_document(doc_id="plan.md")
       └── 返回插值后的消息

4. Client 将消息发送给 Claude
   └── Claude 收到专家级指令
       └── Claude 使用 tools（如 edit_document）来完成

5. Claude 响应格式化后的文档
```

### 关键洞察：Prompts 编排 Tools

Claude 收到 prompt 消息后，通常需要使用可用的 **tools** 来完成任务。Prompts 提供指令，tools 提供能力。

---

## 三方控制模型

这是 Lessons 10-13 中最重要的概念，也是 CCA 考试核心主题：

| Primitive | 控制者 | 触发机制 | 类比 |
|-----------|-----------|-------------------|---------|
| **Tools** | Model-controlled | Claude 在推理时决定 | 主厨决定用什么食材 |
| **Resources** | App-controlled | 你的代码调用 `read_resource()` | 服务生自动送水 |
| **Prompts** | User-controlled | 用户输入 `/` 或点击按钮 | 顾客从菜单点餐 |

对应 Claude 官方界面：
- **Tools** — Claude 在幕后执行代码或计算
- **Resources** — 「Add from Google Drive」功能注入文档 context
- **Prompts** — 聊天输入下方的工作流程按钮

---

## Slash Commands：UX 模式

| 步骤 | 用户行为 | Client 行为 |
|------|-------------|-----------------|
| 1 | 输入 `/` | 调用 `list_prompts()`，显示命令菜单 |
| 2 | 选择命令 | 根据 prompt arguments 显示参数表单 |
| 3 | 提供参数 | 验证输入，准备 args dict |
| 4 | 确认 | 调用 `get_prompt(name, args)`，获取消息 |
| 5 | （自动） | 将消息发送给 Claude，显示响应 |

---

## Prompt Arguments：变量插值

`get_prompt()` 中的 `args` 参数始终是 `dict[str, str]` — 所有值都是字符串：

```python
# Client 端
messages = await client.get_prompt("format", {"doc_id": "plan.md"})

# Server 端（内部发生的事）
def format_document(doc_id: str = Field(...)):
    # doc_id = "plan.md" — 从 args 插值而来
    prompt = f"...{doc_id}..."
    return [base.UserMessage(prompt)]
```

即使参数代表数字或布尔值，也以字符串传递。Server function 处理必要的类型转换。

---

## 常见错误

1. **混淆 `list_prompts()` 和 `get_prompt()`** — `list_prompts()` 返回 metadata（名称、描述），`get_prompt()` 返回实际插值后的消息
2. **非字符串的 args 值** — `args` dict 必须是 `dict[str, str]`，不是 `dict[str, Any]`
3. **错误发送 prompt 消息** — `get_prompt()` 的消息直接进入对话，就像用户打的一样
4. **忘记 prompts 使用 tools** — prompts 提供指令，但 Claude 通常需要 tools 来完成任务；两者都必须可用

> **Key Insight**
>
> 三方控制模型（Tools = model-controlled、Resources = app-controlled、Prompts = user-controlled）是 CCA 考试中最重要的 MCP 架构概念。每个 primitive 服务不同的利益相关者：tools 服务 Claude，resources 服务你的应用，prompts 服务你的用户。

---

## CCA 考试关联

- **D2 (Tool Design & MCP Integration)**：要知道两个 client 方法 — `list_prompts()` 用于发现，`get_prompt(name, args)` 用于获取。`args` dict 是 `dict[str, str]`。
- **D1 (Agentic Architecture)**：三方控制模型是基石概念。预期场景题会问根据控制者该用哪个 primitive。
- 考题中出现「slash command」、「workflow button」或「user triggers」几乎都指向 prompts。

---

## Flashcards

| 正面 | 背面 |
|-------|------|
| 处理 MCP prompts 的两个 client 方法是什么？ | `list_prompts()` 用于发现可用 prompts，`get_prompt(name, args)` 用于获取插值后的消息 |
| `get_prompt()` 中 `args` 参数的类型是什么？ | `dict[str, str]` — 所有 key 和 value 都是字符串 |
| `get_prompt()` 返回什么？ | `result.messages` — 准备好发送给 Claude 的 `base.Message` 对象列表 |
| MCP prompts 对应什么 UI 模式？ | Slash commands（`/`）— 用户输入 `/`、看到可用命令、选择一个、提供参数 |
| Prompts 和 tools 如何协作？ | Prompts 提供指令（做什么），tools 提供能力（怎么做）— Claude 使用 tools 来完成 prompt 指令 |
| 三种 MCP 控制模型是什么？ | Tools = model-controlled（Claude 决定）、Resources = app-controlled（你的代码决定）、Prompts = user-controlled（用户决定） |
| 典型 client 中什么触发 `list_prompts()`？ | 用户在聊天输入中输入 `/` — client 向 server 查询可用 prompts |
| Claude 官方界面中什么展示了 prompt 模式？ | 聊天输入下方的工作流程按钮 — 预定义的、用户触发的工作流程 |
