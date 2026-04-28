# Client 端的 Prompts — PM 视角

| 项目 | 细节 |
|------|--------|
| 考试范畴 | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP client implementation), 2.6 (prompt consumption patterns), 1.3 (prompt orchestration) |
| 来源 | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 13 |

---

## 一句话摘要

Client 端的 prompt 集成就像在产品中安装「快速操作」菜单 — 用户看到一个策展过的专家工作流程清单，选一个、填入细节，每次都得到一致的结果。

---

## 为什么 PM 需要理解 Client 端 Prompts

本课完成了 prompts 端到端运作的全貌。PM 需要知道：

1. **用户如何发现 prompts** — 通过 slash commands、按钮或菜单
2. **用户如何参数化 prompts** — 需要提供什么输入
3. **Prompts 如何编排 tools** — prompts 给指令，tools 做工作
4. **三方控制模型** — 所有 MCP 架构决策的基础

---

## 心智模型：自助点餐机

把三种 MCP primitives 想象成快餐厅的不同点餐体验：

| 体验 | MCP Primitive | 谁决定 | 点餐机类比 |
|------------|---------------|-------------|---------------|
| 厨房决定做什么 | **Tool** | 主厨（Claude） | 厨房做他们觉得你需要的东西 |
| 饮料机自动倒水 | **Resource** | 餐厅系统（app） | 水自动出现在你桌上 |
| 自助点餐机点餐 | **Prompt** | 顾客（用户） | 你点「3 号套餐」、定制配料、确认 |

---

## 端到端用户旅程

### 步骤 1：发现
用户在聊天中输入 `/`。下拉菜单出现显示可用工作流程：
- `/format` — 将文档转写为 Markdown
- `/summarize` — 创建文档摘要
- `/analyze` — 生成分析报告

### 步骤 2：选择与参数
用户选择 `/format`。系统询问必要信息：
- 「哪份文档？」— 显示文档选择器

### 步骤 3：执行
用户确认。幕后：
1. Prompt 模板填入用户的参数
2. 指令发送给 Claude
3. Claude 读取文档（使用 tools）并重新格式化
4. 结果出现在聊天中

### 步骤 4：结果
用户看到专业格式化的 markdown 文档。每次相同质量，不论用户的 prompt engineering 能力。

---

## 三方控制模型 — 主框架

这是 Chapters 2-3 中最重要的概念，也是 CCA 考试的基石：

| Primitive | 控制者 | 考试关键字 | 产品示例 |
|-----------|-----------|-------------|-----------------|
| **Tools** | Claude（model-controlled） | 「Claude 决定」、「自主地」 | Claude 在幕后执行计算 |
| **Resources** | 应用程序（app-controlled） | 「预加载」、「UI context」 | Google Drive 文档注入聊天 |
| **Prompts** | 用户（user-controlled） | 「Slash command」、「workflow 按钮」 | 用户点击「摘要」工作流程按钮 |

### PM 决策流程

设计功能时，问：

1. 「谁应该决定何时发生这件事？」
   - **用户明确触发** → Prompt
   - **Claude 在推理时决定** → Tool
   - **App 自动预加载** → Resource

2. 「这是有已知步骤的可重复工作流程吗？」
   - **是** → Prompt
   - **否，是即兴的** → 让 Claude 用 tools 处理

---

## Prompts + Tools：编排模式

PM 的关键洞察：**prompts 不取代 tools — 它们编排 tools**。

| Prompts 做什么 | Tools 做什么 |
|-----------------|---------------|
| 提供专家指令 | 执行特定动作 |
| 定义「做什么」 | 处理「怎么做」 |
| 用户控制的触发 | 模型控制的执行 |

**PM 意义**：撰写 prompt 驱动功能的 PRD 时，需确保必要的 tools 也可用。没有必要 tools 的 prompt 就像没有食材的食谱。

---

## 产品设计考量

### Prompt 可发现性
- 用户如何找到可用 prompts？（Slash 菜单、工具栏、新手引导）
- Prompts 是否应分类？（按任务类型、使用频率）
- 对新用户，`/` 提示应多显眼？

### 参数体验
- 每个 prompt 需要什么参数？
- 参数能从 context 自动填入吗？（当前文档、选取的文字）
- 缺少必要参数时会发生什么？

---

## PM 常见错误

1. **把 prompts 设计成 tools** — 用户触发的就是 prompt；Claude 决定的就是 tool
2. **忘记 tool 依赖** — prompts 通常需要 tools 来完成指令；确保两者都可用
3. **选择过多** — 策展 5-10 个高价值 prompts，而非 50 个很少用的
4. **没有参数默认值** — 从 context 预填参数（当前文档、选取文字）来减少摩擦

> **Key Insight**
>
> 三方控制模型是所有 MCP 架构决策的主框架：Tools = model-controlled、Resources = app-controlled、Prompts = user-controlled。对 PM 来说，这直接转化为产品设计：「谁启动这个动作？」决定该用哪个 primitive。CCA 考试中，这个区分几乎出现在每一题 D1 和 D2 场景题中。

---

## CCA 考试关联

- **D2 (Tool Design & MCP Integration)**：知道两个 client 方法（`list_prompts` 和 `get_prompt`）以及 slash command UX 模式。
- **D1 (Agentic Architecture)**：三方控制模型是最常考的概念。
- **考试信号词**：「slash command」/「workflow button」/「user triggers」→ Prompt。「Claude decides」/「autonomously」→ Tool。「Pre-loaded context」/「UI data」→ Resource。

---

## Flashcards

| 正面 | 背面 |
|-------|------|
| 三种 MCP 控制模型是什么？ | Tools = model-controlled（Claude 决定）、Resources = app-controlled（app 代码决定）、Prompts = user-controlled（用户决定） |
| Prompts 的 slash command 模式是什么？ | 用户输入 `/`、看到可用 prompts、选择一个、提供参数、系统将插值消息发送给 Claude |
| Prompts 和 tools 如何协作？ | Prompts 提供「做什么」（指令），tools 提供「怎么做」（能力）— Claude 使用 tools 完成 prompt 指令 |
| Prompts 的自助点餐机类比是什么？ | 用户从策展菜单（prompts）中选择、定制选项（参数），得到一致结果 |
| PM 设计 prompt 驱动功能时应确保什么？ | 必要的 tools 也可用 — 没有必要 tools 的 prompt 就像没有食材的食谱 |
| PM 如何在 prompt、tool 和 resource 之间做决定？ | 问「谁应该决定何时发生？」— 用户触发 = Prompt、Claude 决定 = Tool、App 预加载 = Resource |
| 什么考试信号词表示答案是 prompt？ | 「Slash command」、「workflow button」、「user triggers」、「predefined workflow」 |
| Claude 界面中三种 primitive 的示例各是什么？ | Prompts = 聊天下方的 workflow 按钮、Resources = 「Add from Google Drive」、Tools = 幕后代码执行 |
