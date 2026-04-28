# The Server Inspector — 工程深度解析

| 项目 | 说明 |
|------|------|
| 考试领域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.3（MCP primitives）、2.1（tool schema 设计）、1.2（agent loop 集成） |
| 来源 | building-with-the-claude-api / 07-mcp / Lesson 65 |

---

## 一句话总结

MCP Inspector 是一个浏览器基础的开发工具——随 Python MCP SDK 附上（用 `mcp dev` 启动）——让你直接 `list` 和 `call` 你 server 的 tools、resources、prompts，不需要先把 server 串到 Claude 或真实 application。

---

## 问题：调试的反馈循环

当你在做 MCP server 时，要验证它的 tools 有两条路：

| 路径 | 反馈循环 |
|------|---------|
| 串到完整的 Claude application 里 | 慢、吵、MCP bug 和 prompt/agent bug 混在一起 |
| 通过 MCP 协议直接验证 | 快、隔离、秒级暴露 MCP bug |

第一条是你最终需要的，但也是调试最糟的地方。你无法分辨失败是来自 tool 本身、prompt、Claude 选 tool 的判断、还是你的 agent loop。**Inspector** 通过给你第二条开箱路径把反馈循环压缩。

---

## 启动 Inspector

在 Python 环境启动后（精确命令看项目的 README）执行：

```bash
mcp dev mcp_server.py
```

这条命令会：

1. 在 **6277 port** 启动一个 development server。
2. 打印出 Inspector UI 的本地 URL。
3. 加载你的 MCP server 代码，让它的 tools、resources、prompts 可被发现。

接着你在浏览器打开那个 URL，就会看到 **MCP Inspector dashboard**。

> 备注：这节课明确说 Inspector"正在积极开发中"，所以确切 UI 可能和课程截图不同。**能力**（list tools、call tools、看结果）不变。

---

## 连接和发现 Tools

Inspector workflow 是从左侧 sidebar 驱动的。核心步骤：

1. **点"Connect"** — 和你的 server 建立 MCP 协议 session。
2. **导到"Tools"** — 切到导航栏的 tools 视图。
3. **点"List Tools"** — 送一个 `ListToolsRequest` 并渲染响应。
4. **选择一个 tool** — 打开该 tool input schema 的表单视图。
5. **填入参数** — 表单是从你 Python type hints + `Field(description=...)` 生成的。
6. **点"Run Tool"** — 送一个 `CallToolRequest` 并内联显示结果。

每个交互都 1:1 对应到一则真实的 MCP 协议消息，所以你在 Inspector 测的东西就是真实 MCP client 会看到的东西。

除了 Tools，导航栏也有 **Resources** 和 **Prompts** 的区块（后面的 lessons 会用），让你在同一个 UI 测三种 primitives。

---

## 实际示例：演练 document tools

用 Lesson 64 的 server，以下是你如何不启动 chatbot 就从 Inspector 验证两个 tools：

### 1. 读取文档

- Tool：`read_doc_contents`
- 参数：`doc_id = "deposition.md"`
- 预期结果：`"This deposition covers the testimony of Angela Smith, P.E."`

### 2. 编辑再读取

- Tool：`edit_document`
- 参数：`doc_id = "deposition.md"`、`old_str = "Angela Smith"`、`new_str = "Jane Doe"`
- Inspector 确认调用完成。

编辑之后立刻再跑 `read_doc_contents` 用同样的 ID——你应该会看到文字已经被替换。这个**链式验证**模式是个低成本的方法，用来确认变更类的 tool 真的有效。

因为文档活在内存 dict 里，重启 server 会清掉改动。Debug 时这是功能——每次 session 都从干净状态开始。

---

## 启用的开发循环

Inspector 建立一个紧凑、可重复的循环：

```
┌─────────────────────────┐
│ 1. 编辑 mcp_server.py    │
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 2. 重启 `mcp dev`        │  （或靠 auto-reload）
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 3. 在 UI List Tools     │
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 4. 带输入 Run Tool       │
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 5. 查看结果              │
└───────────┬─────────────┘
            ▼
          (重复)
```

每次迭代只碰 MCP server——没有 Claude API 调用、没有 prompt engineering、没有 chat loop。这个隔离性正是 Inspector 的价值。

---

## 为什么这在架构上重要

Inspector 是一种对"**MCP 是协议**，不是 Claude 特定功能"的承认。一个协议需要一个独立于特定消费者（Claude、其他 LLM、自动化）的通用调试 client。`mcp dev` 就是那个通用 client。

具体来说：

| 没有 Inspector | 有 Inspector |
|---------------|-------------|
| 每次测试都需要 Claude API key | 可以离线于 Claude |
| Tool bug 会遮住 prompt bug | Tool bug 被隔离 |
| 反馈循环：分钟级 | 反馈循环：秒级 |
| 没 chatbot 就无法验证 tool schema | Schema 立刻渲染成表单 |

---

## Inspector 不会做的事

边界要说清楚：

| 能力 | Inspector 有吗？ |
|------|---------------|
| 演练 tools、resources、prompts | 有 |
| 把自动生成的 schema 渲染成表单 | 有 |
| 用生成的 tool 调用 Claude | 没有——那要用完整的 chatbot |
| 取代 end-to-end 测试 | 没有——integration tests 还是要跑 |
| 部署你的 server | 没有——`mcp dev` 只在 dev 用 |

Inspector 的价值在于**把 MCP 行为从 LLM 行为隔离**。你的 tools 在 Inspector 通过后，就进到接上 agent 的阶段。

---

## 常见错误

1. **跳过 Inspector 直接做 chatbot 集成。** 你失去了隔离的反馈循环，最后会一次 debug 两层。
2. **没先点 Connect。** 左侧的 Connect 按钮才会实际开始 session；不点它，"List Tools"会回空。
3. **以为 UI 是稳定的。** 这节课警告 Inspector UI"正在积极开发中"——学概念（list、call、chain），不是精确像素。
4. **忘了 port。** 默认是 `6277`；如果被占用命令会告诉你。
5. **只测 happy path。** 也塞一个假 `doc_id`——验证你的 `ValueError` 干净地呈现。

> **Key Insight**
>
> Inspector 是**协议调试器**。它把"我的 tool 能动吗？"和"Claude 会好好用我的 tool 吗？"这两个很不同的问题分开——如果你只做 end-to-end 测试，这两个会混在一起。养成每个新 tool、每次既有 tool 的改动都先打 Inspector 的习惯。它会为 Ch07 后面的 lessons 省下好几个小时的纠结 debug。

---

## CCA 考试重点

- **D2（Tool Design & MCP Integration）**：知道 Python MCP SDK 附一个浏览器基础的 Inspector，用 `mcp dev mcp_server.py` 启动，可演练 Tools、Resources、Prompts。
- **D1（Agentic Architecture）**：认识 Inspector 是 MCP 的隔离测试表面，和完整 agent 测试不同。
- 预期的情境题："你的 tool 在 Inspector 能动，但在 chatbot 失败——这是哪一类 bug？"——答：不是 MCP bug，可能是 prompt、schema description 或 agent-loop bug。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 怎么启动 MCP Inspector？ | 在启动的 Python 环境里跑 `mcp dev mcp_server.py`。 |
| Inspector 默认用哪个 port？ | `6277` |
| Inspector sidebar 第一个要点的按钮是什么？ | "Connect"——它和你的 MCP server 开 session。 |
| Inspector 让你演练哪三种 primitive？ | Tools、Resources、Prompts。 |
| 点"List Tools"在协议层做什么？ | 送 `ListToolsRequest` 并渲染返回的 `ListToolsResult`。 |
| "Run Tool"在协议层做什么？ | 送带表单输入的 `CallToolRequest` 并显示 `CallToolResult`。 |
| 这节课演示的链式验证模式是什么？ | 调用 `edit_document` 然后立刻调用 `read_doc_contents` 确认编辑生效。 |
| Inspector 对 debug 最大的价值是什么？ | 它把 MCP 行为从 LLM 行为隔离——tool bug 不再遮住 prompt bug。 |
