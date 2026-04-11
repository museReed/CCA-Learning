# Prompts in the Client — PM Perspective（简体中文）

| 项目 | 说明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（client 端 MCP prompt 使用）、1.2（agent loop seeding） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 70 |

---

## One-Liner

把 prompts 接进 client，是让它们从"server 端潜能"变成"用户看得到的按钮"的最后一公里。这一步让你的产品可以出 slash-command、快捷动作、模板画廊——所有 prompt engineering 的复杂度都藏在一次点击后面。

---

## 心智模型：有名字按钮的遥控器

想象你的 MCP server 是一台全能电器——什么都能煮。没接 client 时，用户站在电器前翻说明书打原始指令。接上后，你给他们一个遥控器：

- `/format` 按钮 → 把文档改成 markdown
- `/summarize` 按钮 → 浓缩内容
- `/translate` 按钮 → 转换语言

每个按钮都是预先工程化的食谱。用户按下、或许选个参数（哪份文档），电器就动起来。食谱在 server，按钮在 client。这一课就是在讲怎么接线。

---

## 为什么 PM 要关心

这是 prompts 从"工程抽象"变成"demo 时可以指给人看的产品功能"的分水岭。没接 client：prompts 等同隐形。接了之后：

- 用户看到 **可发现的菜单**，不是空文本框
- Onboarding 可以用"试试这个 prompt"起手
- 客服可以说"按 `/format` 修好这份文档"
- 分析可以跟踪哪些 prompt 被使用
- 营销可以展示具体指令

两个 client 方法（`list_prompts`、`get_prompt`）代码很小但产品面很大。你想上的每个 prompt 能不能火，取决于 client 暴露得好不好。

---

## Client 对用户呈现什么

典型用户视角流程：

1. 用户打 `/` 或点"命令"按钮
2. Client 调用 `list_prompts()`，渲染带名字与描述的菜单
3. 用户挑一个（如 `format`）
4. Client 读参数 metadata，要求必要输入（如"哪份文档？"）
5. Client 后台调用 `get_prompt("format", {"doc_id": "report.pdf"})`
6. Server 返回完整消息 list——用户看不到这一步
7. Client 把消息送给 Claude 并显示流式响应

用户视角："我选了一个动作，它就成功了。"PM 视角：上面每一步都是设计决策。

---

## 产品场景

### Client 端 Prompt 接线的亮点场景

| 场景 | 为什么适合 |
|------|-----------|
| 功能多、动作多的复杂应用 | Slash menu 胜过把所有事塞进自由 prompt |
| 新用户 onboarding | 策划过的 prompt 立即 demo 产品能力 |
| 团队分享最佳实践 workflow | Prompts 变组织知识 |
| 减轻客服负担 | "按 `/format`"比"复制这段 prompt"好懂 |
| 品牌一致的输出 | 每个 prompt 锁定一种风格 / 格式 |

### 过头的情况

| 场景 | 更好做法 |
|------|---------|
| 一次性 prototype | 跳过整套管线，直接写死文本 |
| 完全自由 chat 产品 | Prompts 限制多于帮助 |
| 还没有 MCP server | 先建 server（Lesson 69） |

---

## PM 决策框架

设计 prompt 驱动的功能时问自己：

| 问题 | 若 Yes | 意义 |
|------|--------|------|
| 用户要自己发现 prompt？ | Yes | 必须接 client 端 listing（`list_prompts`） |
| Prompt 带参数？ | Yes | 设计参数 picker UX（dropdown、autocomplete、表单） |
| Prompt 会被反复调用？ | Yes | 考虑放成 top-level 按钮，而不是埋在菜单 |
| 想要 prompt 使用量遥测？ | Yes | 埋点在 client 端（server 端执行产品团队看不到） |
| 名字要配合品牌语气？ | Yes | 名字与描述就是 marketing copy，要这样对待 |

---

## UX 设计重点

Prompts 出现在 client 这边，这些都是 PM / 设计的决策：

- **命名** — `/format` 比 `/do_format_thing_v2` 好。短、动词开头、意图明显
- **描述** — 一行、成果导向（"Rewrite document in markdown"），不要功能导向（"用 MCP prompt `format_document` 带 doc_id"）
- **参数收集** — 多数用户不读表单。提供默认值、智能 autocomplete、合理 fallback
- **可发现性** — `/` 菜单、快捷动作栏、onboarding 提示，至少挑一种
- **反馈** — `get_prompt` 运行时显示 loading，之后流式显示 Claude 响应
- **错误处理** — server 不可达或 prompt 出错时显示"指令暂时不可用"，不要露 stack trace

---

## PM 常见错误

1. **上 prompt 却没有发现机制** — 用户找不到等同于不存在
2. **名字与描述晦涩** — 把 prompt metadata 当 microcopy 看待，像按钮 label 一样迭代
3. **没有参数 UX** — 用户宁可离开也不会自己敲 `doc_id`，要有 picker
4. **没有分析** — 看不到哪些 prompt 被用就没法淘汰失败品
5. **脆弱的错误路径** — Server 出事要优雅降级，不能让用户看到 Python exception

> **Key Insight**
>
> `list_prompts` 与 `get_prompt` 是 PM 能要求的最便宜投入、最大产品影响。它们把工程维护的食谱转成产品可见的动作，第一次接线之后，每个新 prompt 都不用再做工程工作。Client 接得好，server 作者新出的 prompt 自动出现在产品里——roadmap 自动驾驶。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：知道 client 暴露 `list_prompts` 与 `get_prompt` 让用户发现并调用 prompt
- **D1（Agentic Architecture）**：Prompts seed agent loop，其余（tool、resource）照常
- 考题模式："MCP server 的 prompts 怎么呈现给用户？" → client 实现 `list_prompts` / `get_prompt`，典型 UI 是 slash menu

---

## Flashcards

| Front | Back |
|-------|------|
| "有名字按钮的遥控器"比喻？ | Server 是全能电器，client 的 prompt 接线就是遥控器，每个按钮对应一个预工程化的食谱 |
| 哪两个 client 方法把 prompts 暴露给用户？ | `list_prompts()` 做发现、`get_prompt(name, args)` 做调用 |
| 为什么 prompts 需要 client 端接线？ | 不接用户找不到、也触发不了，等同于不存在 |
| 好 prompt 名字长什么样？ | 短、动词开头、一看就懂——如 `/format`，而不是 `/do_format_thing_v2` |
| 为什么分析埋点是 PM 的责任？ | Server 端执行产品团队看不到，埋点必须在用户真正交互的 client 端 |
| UX 应该怎么收参数？ | 用 picker、autocomplete、默认值，不要让用户自己敲原始参数 key |
| Server 在 `get_prompt` 出错时怎么办？ | Client 要优雅降级——显示"指令暂时不可用"，不露 stack trace |
| 为什么 client 端 prompt 接线是 MCP 的"最后一公里"？ | 因为 tool、resource、server prompt 若没在 client 变成可发现动作，对用户就没用 |
