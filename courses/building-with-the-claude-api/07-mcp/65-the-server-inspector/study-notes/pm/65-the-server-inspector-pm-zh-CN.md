# The Server Inspector — PM 视角

| 项目 | 说明 |
|------|------|
| 考试领域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.3（MCP primitives）、2.1（tool schema 设计）、1.2（agent loop 集成） |
| 来源 | building-with-the-claude-api / 07-mcp / Lesson 65 |

---

## 一句话总结

MCP Inspector 是你 AI 功能 tool 的"QA 站"——一个浏览器 UI，让团队任何人在 tool 还没接触 Claude 或真实用户之前，就能直接演练——大幅降低 debug 和验收测试成本。

---

## 心智模型：Tool 的产品测试实验室

想象你要推出一个新实体产品。出货前，你会把原型送进测试实验室：按按钮、确认输出、检查 edge cases。这就是 MCP Inspector 对软件 tools 做的事：

| 产品测试实验室 | MCP Inspector |
|--------------|---------------|
| 工作台上的原型 | 用 `mcp dev` 跑的 MCP server |
| 按每个按钮 | 点"List Tools"和"Run Tool" |
| 验证每个输出 | 读 panel 里的结果 |
| 记录缺陷 | 收集失败的输入反馈给团队 |
| 出货前签核 | 在接到 Claude 之前确认 tool 能动 |

重点是：你不会把微波炉直接给顾客来发现它会爆炸。你也不该把坏掉的 MCP tool 直接推到 production 的 Claude flow 里才发现。

---

## 为什么这节课对 PM 重要

三个塑造产品的理由：

1. **验收测试变得 PM 也能做。** Inspector 是一个 UI——PM 或 QA 不用跑 Claude API 调用、不用写测试代码就能演练 tool。意思是 PM 可以直接验证 tool 行为。
2. **Debug 成本下降。** Claude"做错事"时，第一个问题通常是"是 tool 坏掉，还是 Claude 用错？"Inspector 秒级就能答。
3. **Tool 可 demo。** Inspector 也是一个 live demo surface。你可以对利益相关人展示"这个 tool 用真实输入做什么"——不需要协调跑完整 app。

---

## 产品应用场景

### 什么时候该把 Inspector-first 当团队规范

| 场景 | 为什么 |
|------|-------|
| QA 在 release 前跑验收测试 | 新或改的 tool 都先在 Inspector 验过 |
| PM 验收工程 handoff | PM 可以点每个 tool 确认符合 spec |
| 利益相关人 demo | 展示原始 tool 结果不需要 LLM 包装 |
| Bug triage 会议 | 在 Inspector 重现"tool X 返回意外数据"，不需要 chatbot |

### 只靠 Inspector 不够的场景

| 场景 | 还需要什么 |
|------|-----------|
| End-to-end agent 行为 | 完整 chatbot + prompts + Claude |
| Tool description 质量 | Chatbot 看 Claude 会不会选对 tool |
| 多轮 workflow | 完整 agent loop；Inspector 只测单次调用 |
| Multi-tenant 或 auth 场景 | 需要真实 client 连接路径 |

---

## PM 决策框架：采用 Inspector-first 测试

你在做用 MCP tool 的 AI 功能时要问：

1. **新 tool 能在 merge 前都在 Inspector 验过吗？** 把它变成 PR 的检查项。
2. **QA 验收流程里有 Inspector 吗？** 训练一次；每次 release 都有回报。
3. **每个 tool 有标准化的 Inspector 测试 case 吗？** 标准化"list → call read → call edit → re-read"。
4. **失败 case 也有测吗？** 不只 happy path——丢假输入验证错误消息。
5. **Inspector URL 有放进团队 onboarding 文档吗？** 让新人发现它很简单。

---

## Inspector 在 PM 层级改变了什么

历史上，测试 AI 功能是：

> "问 chatbot 几个问题，看答案对不对。"

这纯粹是 end-to-end——慢、不稳、遮住 bug 真正位置。Inspector 给一个不同的测试单位：

> "直接打 tool；它行为符合 spec 吗？"

这比较接近 PM 已经会做的正常软件 QA。Inspector 把 MCP tools 带进**可测试软件组件**的领域，而不是"神奇黑盒 AI 输出"。这对任何做 Claude 基础功能的团队是信心层级的转变。

---

## 运营考量

| 考量 | PM 为什么该在意 |
|------|---------------|
| `mcp dev` 只能 dev 用 | 不要在 production 跑，它不是真实 client surface |
| UI 在积极变动 | 训练概念（list、call、chain）而不是截图 |
| Port `6277` 冲突 | 被挡的话开发流程卡住——标记为 infra 项目 |
| Inspector 结果该记录 | 如果团队用它做验收，要留记录 |
| Inspector 不测 prompts | 记得：只有通过 Claude 才会出的 bug，Inspector 无法重现 |

---

## 常见 PM 错误

1. **以为 end-to-end 测试就够了。** End-to-end 会藏住 bug 在哪；Inspector 会暴露它。
2. **跳过负面测试 case。** PM 验收测试应该包含"坏输入 → 看到合理错误"。
3. **把 Inspector 当成只有工程用。** 它是 UI，任何人都能用。让 QA 和 PM 开车。
4. **不 versioning Inspector 测试 case。** 留一份标准测试清单——不然 regression 会溜进来。
5. **把 Inspector 成功等同产品成功。** Inspector 验证 tool；你还需要 agent/chatbot 测试验证体验。

> **Key Insight**
>
> MCP Inspector 把 MCP tool 测试从"AI 魔法的一部分"搬到"正常产品 QA 的一部分"。它把 tools 重新框成可检视、可测试、可重现的组件——也让 PM 不用跑 code 就能拥有 tool 验收。任何 MCP 基础的功能，"我们有 Inspector 测过吗？"都该变成 definition-of-done 的一项。

---

## CCA 考试重点

- **D2（Tool Design & MCP Integration）**：知道 `mcp dev mcp_server.py` 启动浏览器基础的 Inspector，且它暴露 Tools、Resources、Prompts 区块。
- **D1（Agentic Architecture）**：认识 Inspector 是无 LLM 的测试表面——在隔离 tool bug 和 agent bug 时有用。
- 情境题："一个 tool 在 Inspector 能动但在 chatbot 不行——bug 可能出在哪？"→ 不是 tool 本身，更可能是 prompt、tool description、或 agent loop。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 用 PM 的话说，MCP Inspector 是什么？ | 一个浏览器基础的 QA 站，让团队任何人直接演练 tools，不需要 Claude。 |
| 为什么 Inspector-first 测试是产品赢家？ | 把 tool bug 和 LLM bug 隔离、降低 debug 成本、让 PM/QA 不写代码就能做验收测试。 |
| Inspector 能测试 prompts 或 agent 行为吗？ | 不能——它只测 MCP server 的 tools/resources/prompts primitives。 |
| PM 该在新 MCP tool 的 definition-of-done 加什么？ | "Inspector 已测（happy path + 至少一个失败 case）"。 |
| Inspector 能测哪三种 primitive？ | Tools、Resources、Prompts。 |
| 为什么 Inspector 通过后还要跑 chatbot 测试？ | 验证 Claude 会正确选择并使用 tool——这是体验层级的关注点。 |
| Inspector 的 demo 价值是什么？ | 利益相关人可以看到原始 tool 输出，不需要完整 app runtime。 |
| Inspector 可以在 production 跑吗？ | 不行——它只能 dev 用（`mcp dev`）。 |
