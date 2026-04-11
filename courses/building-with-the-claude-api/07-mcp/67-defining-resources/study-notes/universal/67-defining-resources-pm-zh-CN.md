# Defining Resources — PM Perspective（简体中文）

| 项目 | 说明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（MCP primitives：tools vs resources vs prompts）、1.2（context 注入） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 67 |

---

## One-Liner

Resources 是 MCP 的"数据货架"——让 server 以结构化方式暴露只读数据（文档、记录、列表），应用可以直接拉取注入 Claude prompt，不用 tool call，也不让 Claude 自己猜要抓什么。

---

## 心智模型：餐厅菜单 vs 厨房

- **Resources = 菜单**：一张可读的清单，列出 server 能提供的东西。你（应用）从菜单挑，server 把东西端给你，你摆到 Claude 的盘子上。
- **Tools = 厨房**：Claude 下单"给我做个三明治"，厨房实际去做（动作、副作用）。

两者都由同一家餐厅（MCP server）提供。选菜单还是选厨房，就是选 resource 还是 tool。

---

## 为什么 PM 要关心

几乎所有"有 context 感"的 AI 功能——"@mention 文档"、"拉这条记录"、"给我这个客户的最新 notes"——背后都是 resources。分清楚这两者会影响：

- **谁驱动 fetch** — 用户 / 应用（resource）vs Claude（tool）
- **成本** — 拉一次 resource vs 给 Claude 一个可能调用很多次的 tool
- **延迟** — Resources 进第一个 prompt；tools 多一次 API round trip
- **可预测性** — Resources 永远注入相同数据；tools 由 Claude 决定，更灵活但不确定

PM 若搞混，要么为本该直接拉取的操作支付 tool call 成本，要么做出 Claude 明明有数据却在幻觉的产品。

---

## 功能示例：`@document` mention

课程用具体功能切入：CLI 中用户输入 `@`，弹出文档 autocomplete；选好提交，文档全文注入 prompt。

两个 resources：

| 操作 | Resource 类型 | 原因 |
|------|--------------|------|
| 列出所有文档给 autocomplete | Direct（静态 URI） | 固定、无参数、每次调用一样 |
| 用 ID 取单个文档 | Templated（带 `{doc_id}`） | 带参数、每次输出不同 |

零 tool call，拉数据完全不经 Claude round trip。应用直接从 server 拿数据塞进 prompt。

---

## Resource vs Tool — PM 速查表

| 产品场景 | Resource 或 Tool？ | 原因 |
|---------|--------------------|------|
| 用户输入 @filename 时插入文档内容 | Resource | 纯读、应用驱动、无需 Claude 判断 |
| Claude 回答时可自行搜索知识库 | Tool | Claude 决定何时搜 |
| 填充客户列表 dropdown | Resource | 静态列表拉取 |
| 更新客户电话 | Tool | 写入 / 副作用 |
| 显示当前 KPI dashboard | Resource | Pull-and-render |
| "如果日历有空就帮我订会议" | Tool（agentic） | Claude 推理、决定、行动 |

---

## 产品场景

### 什么时候用 Resources

| 需求 | 为什么适合 Resources |
|------|---------------------|
| 用户引用特定项目（@mention、/command、file picker） | 应用按用户选择驱动 fetch |
| 永远要注入的 context（公司 style guide、术语表、schema） | 拉一次，每次对话都带上 |
| UI 元件清单（autocomplete、dropdown） | Direct resource 对应静态集合 |
| 数据驱动 onboarding（"你的上一笔订单"） | 每个用户拉一次、注入 prompt |

### 什么时候改用 Tools

| 需求 | 为什么适合 Tools |
|------|-----------------|
| 是否要 fetch 由 Claude 判断 | 只有 tools 让 Claude 有选择 |
| 有副作用的操作 | Resources 是只读的 |
| 参数需要靠推理决定 | Tool input 可在对话中动态合成 |

---

## PM 决策框架

规格"拉取类"功能前问自己：

| 问题 | 若 Yes | 意义 |
|------|--------|------|
| 是由用户（而非 Claude）决定拉哪个项目？ | Yes | Resource |
| 纯读、无副作用？ | Yes | Resource |
| 希望每次对话都一定把数据放进 prompt？ | Yes | Resource |
| 希望 Claude 认为不必要时可以跳过 fetch？ | Yes | Tool |
| 操作会修改数据？ | Yes | Tool |

---

## PM 常见错误

1. **把所有 MCP 能力都当 tool** — 最便宜、最可预测的原语常常是 resource。先问"谁决定？"再规格
2. **不考虑 URI namespace** — URI 就是 API，烂 URI（`docs://d1`、`docs://d2`）以后会很痛，要像设计 REST API 一样认真
3. **以为 resources 是免费的** — 注入的内容仍然吃 token，大文档会撑爆 context window
4. **把读写混在同一个原语** — 读用 resource、写用 tool，安全 review 与审计 log 会简单很多
5. **跳过 Inspector 验证** — MCP Inspector 可以在 client 还没写之前证明 resource 能用，PM 应把它当成交付要求

> **Key Insight**
>
> Resources 是让产品对 Claude 说"这就是你需要的数据"而不是"这些是你也许能用的工具"的原语。每次强迫 Claude 选择，都要付 token 成本并引入方差。Resources 是 PM 保留"确定性"与"成本控制"的武器，同时还能给 Claude 新鲜、相关的 context。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：Resources 是 MCP 三个 primitives 之一（tools、resources、prompts），知道 direct vs templated 的差异
- **D1（Agentic Architecture）**：Resources 是不经 tool call 把 context 塞进 agent loop 的方式，由 client 拉取后注入 prompt
- 考题模式："应用要按用户选择把文档内容放进 prompt，是 tool 还是 resource？" → resource

---

## Flashcards

| Front | Back |
|-------|------|
| Resources 与 tools 的"菜单 vs 厨房"比喻？ | Resources 是菜单（应用挑出数据端给 Claude），tools 是厨房（Claude 选择去做的动作） |
| Resources 有哪两种？ | Direct（静态 URI、固定调用）和 templated（带参数的 URI、参数化调用） |
| 什么时候该用 resource 而非 tool？ | 当应用（而非 Claude）决定 fetch、fetch 无副作用、数据应一律出现在 prompt 里 |
| 举一个 direct vs templated resource 的产品示例。 | Direct：列出所有文档给 autocomplete。Templated：用 `{doc_id}` 取特定文档 |
| Resources 仍然会有哪种成本？ | Token 成本——注入的内容会计入 context window |
| 为什么 URI 设计要认真对待？ | URI 是 server 的 API 契约，烂 URI 与烂 REST route 一样难改 |
| 对 Claude 而言 resources 与 tools 有何不同？ | Claude 不会"决定"调用 resource；resource 由 client 拉取注入 prompt，Claude 只看到结果 |
| 上线前应要求使用哪个验证工具？ | MCP Inspector，它列出 direct 与 templated resources，可以先端到端测试 |
