# 访问 Resources — PM 视角

| 项目 | 细节 |
|------|--------|
| 考试范畴 | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP client implementation), 2.4 (resource consumption patterns), 2.5 (content type handling) |
| 来源 | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 11 |

---

## 一句话摘要

访问 resources 就像你的 app 从共享硬盘拉出文件，在会议开始前放到桌上 — Claude 不需要开口询问就能立即看到数据。

---

## 为什么 PM 需要理解 Resource 访问

Resource 访问是驱动以下功能的 client 端模式：
- **文档引用**（聊天界面中的 `@plan.md`）
- **Context 面板**（侧边栏显示相关数据）
- **自动补全下拉菜单**（从可用项目中选择）

理解这个模式能帮助 PM：
1. **规格正确的交互模型** — 用户即时看到数据，而非等 Claude「查询」
2. **设定合理的性能预期** — resource 注入比 tool 获取数据更快
3. **设计更好的 UX 流程** — `@mention` 模式是经过验证的交互范式

---

## 心智模型：会议前简报

想象你在组织一场会议：

| 方式 | 类比 | MCP 对应 | 用户体验 |
|----------|---------|----------------|-----------------|
| **会前简报** | 助理打印相关报告，会议开始前放在桌上 | **Resource 访问** | 快速 — 所有人可以立即参考文件 |
| **会中查找** | 有人说「让我去档案室看看」然后离开去取文件 | **Tool call** | 较慢 — 会议暂停等待获取数据 |

Resources 就是会前简报。你的应用程序预先收集数据，交给 Claude 作为 context。Claude 不需要「离开会议室」去找信息。

---

## `@Mention` 用户旅程

Resource 访问所驱动的逐步 UX 流程：

1. **用户在聊天输入框中输入 `@`** — app 向 server 查询可用 resources
2. **自动补全下拉菜单出现** — 显示可用的文档、数据源或参考
3. **用户选择项目**（方向键 + 空格键）— app 获取该 resource 的完整内容
4. **内容静默注入 prompt** — 用户看不到原始内容；它成为隐藏的 context
5. **用户按 Enter 发送** — Claude 同时收到用户的问题和引用的文档
6. **Claude 带着完整 context 回复** — 没有「让我查一下」的延迟，没有额外的 tool call

这与 Claude 官方界面中的「Add from Google Drive」是相同的模式。

---

## 产品意义

### 性能
Resource 注入在 Claude 开始推理前完成，这意味着：
- **没有额外延迟** — 不需要 tool call
- **不浪费 token** — Claude 不需要描述它要查什么
- **第一次回复就已充分了解** — 不需要后续往返

### 数据格式意识
Resources 带有格式提示（MIME types），影响 app 处理方式：

| 数据格式 | App 行为 | PM 考量 |
|-------------|-------------------|------------------|
| 结构化数据（JSON） | 解析为对象用于丰富显示 | 可在 UI 中驱动表格、图表或筛选器 |
| 纯文本 | 直接显示或注入聊天 | 实现简单但视觉呈现有限 |
| 二进制（PDF、图片） | 需要特殊渲染 | 你的 UI 规格需要查看器组件 |

### 错误处理
如果 resource 找不到或不可用，app 应优雅处理。在 PRD 中应指定：
- 引用的文档不可用时用户看到什么
- 是否显示警告或静默忽略
- 回退行为（例如 Claude 仍可在没有 resource 的情况下回答）

---

## PM 常见错误

1. **该用 resource 的场景设计成 tool 型 UX** — 如果用户明确选择要包含什么数据，用 resources（不是 tools）
2. **没有规格化自动补全体验** — resource 驱动的自动补全需要设计规格：搜索行为、结果排序、显示格式
3. **忽略数据大小** — 大型 resources（整个数据库、巨大文件）在注入前应分页或摘要
4. **以为 Claude 控制 resource 访问** — resources 是 app-controlled；Claude 不决定何时获取

> **Key Insight**
>
> 由 resources 驱动的 `@mention` 模式创造了一种用户体验：context 在 AI 开始思考**之前**就已收集完毕。这根本性地比 tool 获取数据更快且更可预测。撰写 PRD 时，总是问：「这笔数据能作为 resource 预先加载，还是 Claude 需要决定何时获取？」

---

## CCA 考试关联

- **D2 (Tool Design & MCP Integration)**：预期会有关于 client 端 resource 模式的题目。要知道 `read_resource()` 返回 `contents` 列表，MIME types 决定解析行为。
- **D1 (Agentic Architecture)**：Resource 访问通过在模型推理前注入数据到 prompt 来降低延迟。这是一个关键的架构权衡。
- 注意描述「数据出现在界面中」或「context 被预先加载」的场景 — 这描述的是 resource 访问，不是 tool call。

---

## Flashcards

| 正面 | 背面 |
|-------|------|
| `@mention` 模式中什么触发自动补全下拉菜单？ | 用户输入 `@` 时，client 向 server 查询可用 resources |
| Resource 内容如何传递给 Claude？ | 直接注入 prompt context — 不需要 tool call |
| Resource 访问的会议室类比是什么？ | 会前简报：助理打印报告，会议开始前放在桌上 |
| 为什么 resource 访问对用户来说比 tool 获取数据更快？ | 数据在 Claude 开始推理前就在 prompt 中 — 没有额外往返或「让我查一下」的延迟 |
| 什么决定 client 如何解析 resource 内容？ | Resource 上的 MIME type — `application/json` 解析为 JSON，`text/plain` 用作原始文本 |
| 谁控制 resources 的访问时机 — Claude、app 还是用户？ | 应用代码（app-controlled），虽然用户可能通过输入 `@` 触发 |
| PM 应在 PRD 中为 resource 错误处理指定什么？ | 引用文档不可用时用户看到什么、警告行为、回退行为 |
| 什么真实功能展示了 resource 访问模式？ | Claude 的「Add from Google Drive」— app 获取文档内容并注入为 prompt context |
