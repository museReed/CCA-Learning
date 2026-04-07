# Defining Tools with MCP — PM 战略概览


![Tools Decorator](../../visuals/tools-decorator-zh-TW.svg)

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | T2.1 设计与实现 tool schemas; T2.5 使用 MCP SDK 定义类型安全的 tools |
| Source | introduction-to-model-context-protocol / 02-tools-and-inspector / Lesson 06 |

---

## 一句话摘要

MCP SDK 把 tool 创建从为期数周的规格编写项目，变成写一个带好描述的 Python 函数——大幅降低给 Claude 新能力所需的工程量。

---

## 旧方式：规格驱动开发

在 MCP SDK 之前，让 Claude 访问新 tool 需要一个多步骤流程，很像撰写法律合同：

1. **写 JSON schema** — 每个参数、其类型、约束和描述的正式规格
2. **写 handler 函数** — 实际做事的代码
3. **保持同步** — 每次函数改变，schema 也必须改
4. **测试 schema** — 验证 Claude 正确解读 schema

这就像要求每个员工在做任何工作之前先写正式职位描述，然后每次职责变更时更新那份文件。

> **PM Takeaway**
> 旧方式造成"tool 瓶颈"——每个新能力都需要先完成 schema 规格工作才能建任何实际功能。FastMCP 完全移除了这个瓶颈。

---

## 新方式：直接写函数

用 FastMCP，工程工作流大幅简化：

1. 写一个做你想做的事的 Python 函数
2. 加一个装饰器（`@mcp.tool()`）
3. 写一个好的 docstring 解释它做什么

就这样。SDK 自动从代码本身生成正式规格。函数本身就是规格。

想象两者的差异：

- **旧方式**：撰写详细的 10 页需求文档、获得审批、然后聘请承包商做事
- **新方式**：在对话中描述你需要什么，工作立即开始

给 PM 的关键洞察是 **tool 描述的质量**（docstring）直接影响 Claude 使用 tool 的效果。这是产品思维重要的地方——不在技术 schema，而在清楚表达 tool 做什么、何时使用、返回什么。

> **PM Takeaway**
> Tool 描述是产品设计决策，不只是技术细节。写得好的描述意味着 Claude 在正确的时间选择正确的 tool。模糊的描述意味着 Claude 犯错或完全忽略 tool。

---

## 为什么描述是产品决策

当 Claude 收到用户查询时，它会读过所有可用的 tool 描述并决定使用哪个（如果有的话）。这就像客户在目录中阅读产品描述。

考虑同一个 tool 的两种描述：

**模糊**："读取文档"

**精确**："读取并返回指定文件路径的完整文字内容。当用户询问文档内容、需要查阅文件、或想在文档中搜索时使用。"

精确的描述给 Claude 清楚的信号，说明何时及如何使用 tool。模糊的描述留下太多歧义。

这直接映射到产品文案撰写——描述越清楚，用户体验越好。

---

## 错误消息即用户体验

当 tools 失败时，Claude 收到的错误消息决定它如何优雅地处理情况。好的错误消息就像好的客服培训：

**差的错误**："操作失败"
- Claude 告诉用户："出了问题。请再试一次。"

**好的错误**："在 /reports/q3.pdf 找不到文档。reports 目录包含：q1.pdf、q2.pdf、q4.pdf"
- Claude 告诉用户："我找不到 q3.pdf，但我看到有 q1、q2 和 q4 报告。要我读其中一个吗？"

> **PM Takeaway**
> 错误消息是用户体验的一部分，即使用户从未直接看到。它们决定 Claude 是优雅恢复还是给出死胡同响应。审查 tool 规格时，永远检查错误处理设计。

---

## 验证安全网

FastMCP 在 tool 代码执行前自动验证输入。这就像在生产线前设置品质管控检查站：

- 如果 Claude 发送数字而预期是文字字符串，验证会拦截
- 如果缺少必填字段，验证会拦截
- 如果值超出允许范围，验证会拦截

这意味着 tool 开发者可以专注于"快乐路径"——输入正确时会发生什么——让 SDK 处理输入错误。更少 bug、更少防御性代码、更快开发。

---

## 对产品团队的战略影响

**更快的能力扩展**：为 AI 产品新增 tool 从数天降到数小时。这意味着产品可以更快响应用户反馈和市场需求。

**更低的工程门槛**：初级开发者也能创建 MCP tools。SDK 处理复杂的协议细节，开发者专注于业务逻辑。

**更好的 tool 质量**：自动验证在 bug 触达用户前拦截。Schema-代码同步消除了整类"测试时能用但生产环境失败"的问题。

**描述驱动设计**：PM 能做的最有影响力的事是确保 tool 描述清楚、具体、且与用户意图对齐。这是产品专业直接改善 AI 表现的地方。

---

## CCA 考试关联性

本课涵盖 **Domain 2 (18%)**，重点在：

- 理解 `@mcp.tool()` 从 Python 函数自动生成 schema
- 知道 docstring 变成 Claude 用于选择的 tool 描述
- 辨认好的描述改善 tool 选择准确度
- 理解验证和错误处理模式

---

## Flashcards

| Front | Back |
|-------|------|
| MCP SDK 从 tool 创建流程中消除了什么？ | 手动 JSON schema 编写。SDK 从 Python 函数签名和 type hints 自动生成 schema。 |
| 为什么 tool 描述是产品决策？ | 因为 Claude 读描述来决定用哪个 tool。清楚、具体的描述带来更好的 tool 选择和更好的用户体验。 |
| 好的和差的 tool 错误消息有什么区别？ | 好的错误包含上下文（什么出错、有什么替代方案）。差的错误是通用的（"失败"）。好的错误让 Claude 优雅恢复。 |
| FastMCP 中"自动验证"是什么意思？ | SDK 在 tool 代码执行前自动检查 Claude 的 tool 输入是否符合预期类型和约束，及早拦截错误。 |
| FastMCP 如何影响开发速度？ | 新增 tool 从数天（手动 schema + handler + 测试）降到数小时（写函数 + 装饰器 + docstring）。 |
| PM 能为 MCP tools 做的最有影响力的事是什么？ | 确保 tool 描述清楚、具体、且与用户意图对齐——这直接影响 Claude 选择和使用 tools 的效果。 |
| FastMCP 中 schema-代码同步如何运作？ | Schema 从代码本身生成，所以它们永远不会不同步。函数的变更自动更新 schema。 |
| Claude 发送无效输入到 FastMCP tool 时会发生什么？ | Pydantic 验证在 tool 函数执行前拦截类型错误，返回清楚的错误消息给 Claude。 |
