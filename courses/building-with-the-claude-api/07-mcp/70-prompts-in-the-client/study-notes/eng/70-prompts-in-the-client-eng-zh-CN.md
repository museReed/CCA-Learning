# Prompts in the Client — Engineering Deep Dive（简体中文）

| 项目 | 说明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（MCP primitives：client 端 prompt 访问）、1.2（seed agent loop）、2.2（message content blocks） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 70 |

---

## One-Liner

从 client 使用 prompt 就是在 MCP client 加两个方法：`list_prompts()` 做发现、`get_prompt(name, args)` 取得已插值的消息 list，直接送给 Claude 作为新对话的开场。

---

## Client 端契约

Server 用 `@mcp.prompt()` 定义的 prompt，要 client 暴露两个方法才真正可用：

1. **`list_prompts()`** — 返回 server 知道的所有 prompt，含名字、描述、参数 metadata
2. **`get_prompt(prompt_name, args)`** — 用给定参数执行 server 的 prompt function，返回结果消息 list

两个方法就位后，应用就能做 slash menu UI、为每个 prompt 显示描述、向用户收参数、然后启动一个组好的 Claude 对话。

---

## 实现 `list_prompts`

```python
async def list_prompts(self) -> list[types.Prompt]:
    result = await self.session().list_prompts()
    return result.prompts
```

这是对 session 的直通：

- `self.session().list_prompts()` 调 MCP SDK，向 server 询问目前注册的 prompt
- SDK 返回 `ListPromptsResult`，你把 `result.prompts` 当 `types.Prompt` list 返回

每个 `types.Prompt` 对象带：

- `name` — 字符串标识（如 `"format"`）
- `description` — UI 显示用的人类可读说明
- 参数 metadata — 名字、描述、是否必填

应用用这些信息组 picker、校验输入、或做权限控制。

---

## 实现 `get_prompt`

```python
async def get_prompt(self, prompt_name, args: dict[str, str]):
    result = await self.session().get_prompt(prompt_name, args)
    return result.messages
```

这个方法带参数取指定的 prompt：

- `prompt_name` — 从 `list_prompts()` 看到的名字
- `args` — dict，key 对应 server 端 function 的参数名
- session 的 `get_prompt` 发请求给 server，server 执行 prompt function 并返回 `list[base.Message]`
- 你把 `result.messages` 返回出去——就是可以直接发给 Claude 的对话

---

## Prompt 参数怎么运作

Server 端 prompt function 会有参数。例如：

```python
def format_document(doc_id: str):
    # doc_id 会被插值进 prompt 模板
```

Client 调用 `get_prompt("format", {"doc_id": "report.pdf"})` 时，MCP SDK 会把 dict 当 keyword arguments 喂给 `format_document(doc_id="report.pdf")`。Function 执行、插值、返回消息 list。Client 看不到中间模板，只看到最终消息。

这种参数化是 prompt 能复用的原因：一个 server 端模板服务无限参数组合。

---

## 在 CLI 测试 Prompts

`list_prompts` 与 `get_prompt` 接好后，CLI 把 prompts 暴露为 slash-command。打 `/` 会弹出 prompt 菜单。选一个后可能还要填参数（如"要 format 哪份文档？"），然后完整 prompt 送给 Claude。

典型 workflow：

1. **用户选 prompt**（如 `/format`）
2. **系统要求必要参数**（如哪份文档）
3. **Client 调用 `get_prompt(name, args)`** — 收到插值后的消息
4. **Client 把消息送给 Claude** — Claude 用这个 seed 开始对话
5. **Claude 正常进行** — 可能调用 tool、读 resource、生成最终答复

---

## 完整 Prompt 驱动的 Agent Loop

从 server 作者视角，prompt 是食谱；从 client 视角，是预组好的对话开场。合起来：

```
┌──────────┐                       ┌────────────┐    list_prompts()      ┌────────────┐
│  User    │                       │ Application│ ─────────────────────▶ │ MCP Server │
│          │                       │ (+ client) │                        │            │
│          │   选 "format"          │            │                        │            │
│          │ ─────────────────────▶ │            │                        │            │
│          │   doc_id="report.pdf"  │            │    get_prompt(...)     │            │
│          │ ─────────────────────▶ │            │ ─────────────────────▶ │            │
│          │                        │            │ ◀───────────────────── │            │
│          │                        │            │   messages=[...]       └────────────┘
│          │                        │            │                              │
│          │                        │            │   第一次调用 Claude          │
│          │                        │            │ ─────────────────────▶ ┌──────────┐
│          │                        │            │ ◀───────────────────── │  Claude  │
│          │                        │            │   tool_use(...)        │   API    │
│          │                        │            │                        └──────────┘
│          │                        │            │   loop 继续...
└──────────┘                        └────────────┘
```

Prompt 只 seed 对话，之后 tool use、resource access、多轮推理都照常走。

---

## Prompt Best Practices（本课提到）

- 与 server 用途相关
- 上线前充分测试
- 使用清晰具体的指令
- 设计时考虑与现有 tool 的协作
- 仔细想用户要提供什么参数

对应 Lesson 69 的 server 端 best practices，client 是 prompt 的消费者。

---

## Common Mistakes

1. **把 `get_prompt` 结果当纯文本** — 它是 **消息 list**，要通过 Anthropic API 的 messages 参数送，不是单个用户字符串
2. **传错参数名** — `args` 的 key 要与 server prompt function 的参数名完全一致，不一致就报错
3. **没先调 `list_prompts` 就调 `get_prompt`** — 技术上可以，但失去做 UI 与校验的机会
4. **跨 session 缓存 prompt 结果** — Prompt 输出是新对话的模板，后续对话状态是 per-session，缓存消息会误导状态模型
5. **忽略 description metadata** — prompts 的重点就是可发现性，把 description 传进 UI

> **Key Insight**
>
> `list_prompts` 与 `get_prompt` 很小——两个方法、几行代码——却是 MCP 产品表面的收尾。有了它们，你的 client 就多了"server 作者维护的预工程化动作菜单"。每次 server 作者改进一个 prompt，所有用它的 client 都自动升级。这种不对称复利让 prompts 变成三种 MCP 原语中对 PM 最友好的一个。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：知道 client 侧两个方法（`list_prompts`、`get_prompt`）、dict 传参、返回 `list[base.Message]`
- **D1（Agentic Architecture）**：Prompts 用策划的对话开场 seed agent loop，后续照常
- 考题模式："Client 如何带参数取 prompt？" → `await self.session().get_prompt(prompt_name, args)` 并返回 `result.messages`

---

## Flashcards

| Front | Back |
|-------|------|
| 使用 prompts 需要哪两个 client 方法？ | `list_prompts()` 做发现、`get_prompt(prompt_name, args)` 取插值后的消息 list |
| `list_prompts()` 返回什么？ | `result.prompts`——`types.Prompt` list，含 name、description、参数 metadata |
| `get_prompt` 返回什么？ | `result.messages`——`list[base.Message]`，可直接送给 Claude |
| Prompt 参数怎么传？ | 用 `dict[str, str]`，key 对应 server prompt function 的参数名 |
| Client 调 `get_prompt` 时 server 做什么？ | 用 args 当 keyword arguments 执行装饰过的 prompt function，返回结果消息 list |
| Client 拿到消息后怎么用？ | 送给 Claude 当新对话的开场，agent loop 照常进行（tool、resource、多轮） |
| CLI 中 prompt 怎么呈现给用户？ | Slash-command（如 `/format`），可选的参数 picker，然后送给 Claude |
| 为什么跨 session 缓存 `get_prompt` 结果有风险？ | Prompt 输出是新对话的模板，后续状态是 per-session，缓存消息会误导应用的状态模型 |
