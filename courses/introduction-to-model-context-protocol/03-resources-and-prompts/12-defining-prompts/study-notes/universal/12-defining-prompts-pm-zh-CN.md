# 定义 Prompts — PM 视角

| 项目 | 细节 |
|------|--------|
| 考试范畴 | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server primitives), 2.6 (prompt template design), 1.3 (prompt engineering for tools) |
| 来源 | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 12 |

---

## 一句话摘要

MCP prompts 就像团队打包进产品的专家脚本 — 用户不需要成为 prompt 工程专家，就能获得一致、高质量的 AI 交互。

---

## 为什么 PM 应该关心 Prompts

Prompts 解决了一个根本的产品问题：**专家用户与新手用户之间的质量差距**。

| 用户类型 | 没有 MCP Prompts | 有 MCP Prompts |
|-----------|-------------------|-----------------|
| 专家用户 | 写出好 prompt，得到好结果 | 同样好的结果，速度稍快 |
| 一般用户 | 写出普通 prompt，得到普通结果 | 通过预建模板获得专家级结果 |
| 新用户 | 不知道该问什么，结果差 | 通过 slash commands 发现工作流程 |

这与 email 模板、Notion 模板库或 Figma 组件库是相同的原理 — 封装专业知识以供重复使用。

---

## 心智模型：餐厅菜单

把 MCP primitives 想象成与餐厅交互的不同方式：

| 交互 | MCP Primitive | 谁决定 | 餐厅类比 |
|-------------|---------------|-------------|-------------------|
| 主厨即兴发挥 | **Tool** | 主厨（Claude） | 「主厨推荐 — 给我惊喜」 |
| 服务生送水 | **Resource** | 餐厅（app） | 水自动出现在桌上 |
| 顾客从菜单点餐 | **Prompt** | 顾客（用户） | 「我要 7 号套餐」 |

Prompts 就是菜单。厨房（MCP server 开发者）精心设计了每道菜（prompt 模板）。顾客（用户）从测试过的选项中挑选，得到可预测的高质量结果。

---

## 产品使用场景

### 何时使用 Prompts

| 场景 | 为什么 Prompts 有效 |
|----------|-----------------|
| 「把这份文档转成 markdown」 | 测试过的模板比用户的临时请求更能处理边界案例 |
| 「从我的笔记生成周报摘要」 | 用户难以自己撰写的复杂指令 |
| 「分析这个数据集并创建报告」 | 含多个步骤的领域专属工作流程 |
| 「翻译这份文档并保留格式」 | 需要精心 prompt engineering 的细腻指令 |

### 何时不该用 Prompts

| 场景 | 更好的替代方案 |
|----------|--------------------|
| 用户提出自由问题 | 让 Claude 直接处理 — 不需要模板 |
| App 需要预加载 context | 用 **resource** — app-controlled |
| Claude 需要决定何时行动 | 用 **tool** — model-controlled |

---

## Slash Command UX 模式

Prompts 天然对应 Slack、Notion、Discord 等工具中熟悉的 slash command 模式：

1. **用户输入 `/`** — 可用 prompts 作为命令菜单出现
2. **用户选择命令**（如 `/format`）— 被提示输入必要参数
3. **用户提供参数**（如选择文档）— prompt 模板被填入
4. **模板发送给 Claude** — Claude 收到精心设计的指令
5. **Claude 执行** — 使用可用的 tools 来完成 prompt 的指令

从用户角度，这感觉像「工作流程按钮」— 一键（或命令）触发复杂、可靠的操作。

---

## 产品四大好处

1. **一致性** — 每个用户得到相同质量的指令，消除「prompt 乐透」
2. **专业知识编码** — 开发者的领域知识烘焙进模板中
3. **可重用性** — 多个 client 应用可共享同一 server 的 prompts
4. **集中维护** — 在 server 上更新 prompt，所有 clients 自动获得改进

---

## PM 常见错误

1. **不投资 prompt 质量** — 把 prompts 当简单字符串而非需要迭代的测试模板
2. **太多 prompts** — 用选择淹没用户；策展一组聚焦的高价值工作流程
3. **PRD 中没有指定 prompt 参数** — 用户需要清楚的参数描述；列入验收标准
4. **混淆 prompts 和 system instructions** — prompts 是用户触发的工作流程，不是永远开启的行为规则

> **Key Insight**
>
> Prompts 是 **user-controlled** primitive。用户明确决定何时使用，不同于 tools（Claude 决定）或 resources（app 决定）。对 PM 来说，这直接对应到「工作流程功能」— 用户启动结构化、可重复流程的功能。CCA 考试中，控制模型区分（model / app / user）是 D1 和 D2 中最常考的概念。

---

## CCA 考试关联

- **D2 (Tool Design & MCP Integration)**：知道何时建议用 prompts vs. tools vs. resources。触发条件是：「预定义工作流程」+「用户启动」= prompt。
- **D1 (Agentic Architecture)**：Prompts 属于用户控制层。
- 注意考题中的「workflow」或「slash command」— 这些几乎都指向 prompts。

---

## Flashcards

| 正面 | 背面 |
|-------|------|
| 谁控制 MCP prompts 的触发时机？ | 用户（user-controlled）— 通过 slash commands、按钮或菜单 |
| MCP prompts 解决什么产品问题？ | 专家与新手用户之间的质量差距 — prompts 将专业知识封装为可重用模板 |
| MCP prompts 的餐厅类比是什么？ | 菜单 — 厨房设计每道菜（模板），顾客（用户）从测试过的选项中挑选 |
| PM 何时该选 prompt 而非 tool？ | 工作流程是预定义的、可重复的、且由用户明确触发时 |
| Prompts 天然对应什么 UX 模式？ | Slash commands（`/format`、`/summarize`）— 从 Slack、Notion、Discord 熟悉的模式 |
| MCP prompts 的四大产品好处是什么？ | 一致性、专业知识编码、可重用性、集中维护 |
| Prompts 和 system instructions 有什么不同？ | Prompts 是用户触发的工作流程；system instructions 是永远开启的行为规则 |
| 用户选择 prompt 并提供参数后会发生什么？ | 模板填入参数后作为精心设计的指令发送给 Claude |
