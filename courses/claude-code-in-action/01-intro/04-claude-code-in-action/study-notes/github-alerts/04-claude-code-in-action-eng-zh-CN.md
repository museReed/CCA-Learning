# Claude Code in Action — 工程深度解析

| 项目 | 细节 |
|------|--------|
| 考试领域 | D2 — Tool Design & MCP Integration (18%), D3 — Claude Code Configuration & Workflows (20%) |
| 任务声明 | 2.5 (built-in tools), 2.4 (MCP integration), 3.6 (CI/CD), 1.1 (agentic loops) |
| 来源 | claude-code-in-action / 01-intro / Lesson 04 |

---


![Tool Chaining Patterns Matrix](../../visuals/tool-chaining-patterns-matrix-zh-TW.svg)
*圖：四個 Demo 的工具鏈接模式矩陣。*


![Tool Chain Pattern](../../visuals/tool-chain-pattern-zh-TW.svg)
*圖：Claude Code 中三種工具鏈接模式。*


![Builtin Vs Mcp Decision Tree](../../visuals/builtin-vs-mcp-decision-tree-zh-TW.svg)
*圖：決策樹 — 內建工具 vs MCP Server。*

## 一句话摘要

Claude Code 的威力来自内建工具的智慧串联、通过 MCP 轻松扩展能力、以及无缝的 CI/CD 集成 — 而非单一工具的能力。

---

## 内建工具总览

Claude Code 默认搭载涵盖文件 I/O、执行与搜索的工具组：

| 工具 | 用途 | 类别 |
|------|---------|----------|
| Read | 读取文件内容（支持图片、PDF、notebook） | 文件 I/O |
| Write | 创建或覆写文件 | 文件 I/O |
| Edit | 对既有文件做精准修改 | 文件 I/O |
| Bash | 执行 shell 命令 | 执行 |
| Grep | 用正则搜索文件内容（基于 ripgrep） | 搜索 |
| Glob | 按名称/模式查找文件 | 搜索 |
| NotebookEdit | 编辑 Jupyter notebook 单元格 | Notebook |
| WebFetch | 获取与分析网页内容 | 网络 |
| WebSearch | 搜索网络上的最新信息 | 网络 |

> [!TIP]
> **关键洞察**
> 威力不在任何单一工具 — 而在 Claude 如何智慧地将它们串联起来。本课每个 Demo 展示不同的串联模式。

---

## Demo 1：性能优化 — 智慧工具串联

**情境**：chalk 是 npm 第五大热门包（每周约 4.29 亿次下载）。即使微小的性能改善也会对整个生态系统产生巨大影响。

**Claude 的工具链**：
1. **规划** — 创建结构化待办清单追踪多步骤工作
2. **搜索** — 用 Grep/Glob 找到性能相关的代码路径
3. **benchmark** — 通过 Bash 执行既有 benchmark 建立基线
4. **聚焦** — 编写针对性测试文件隔离热点路径
5. **profiler** — 通过 Bash 执行 CPU profiler，Read 读取输出
6. **修复** — 用 Edit 实现优化
7. **验证** — 重跑 benchmark 确认改善

**成果**：目标操作的吞吐量提升 3.9 倍。

> [!NOTE]
> **讲师洞察**
> Claude 会创建待办清单来追踪自己在复杂任务中的进度。这种自我管理行为是自然涌现的 — 这就是 agentic loops 如何在多步骤中维持一致性。

> [!IMPORTANT]
> **考试重点**
> 这是 Task 1.1（agentic loops）的经典范例：Claude 自主规划、执行、观察、改进，步骤之间无需人类介入。

---

## Demo 2：数据分析 — 执行与迭代

**情境**：视频流媒体平台用户的 CSV 数据集。目标：分析用户流失模式。

**Claude 的做法**：
1. Read 读取 CSV 了解结构
2. 在 Jupyter notebook 中编写分析代码
3. **执行单元格并读取输出** — 这是关键差异
4. 根据实际结果，定制下一步分析
5. 反复改进可视化与统计检验

> [!TIP]
> **关键洞察**
> Claude 不只是生成代码然后期待它能跑。它执行、观察结果、然后调整。这个「执行→观察→改进」循环产出的分析质量远优于纯生成方式。

---

## Demo 3：MCP 扩展性 — Playwright 浏览器控制

**情境**：一个从文字描述生成 UI 组件的小应用。Claude 需要调整输出的视觉样式。

**Claude 的做法**：
1. 通过 Playwright MCP server 获得浏览器控制工具
2. 打开浏览器，截图查看当前状态
3. 通过 Edit 修改 CSS/样式
4. 重新截图验证视觉结果
5. 反复迭代直到样式符合预期

**关键技术要点**：
- MCP 工具通过配置文件添加 — 不需重新训练
- Claude 仅凭工具描述就能适应新工具
- 工具描述的质量决定 Claude 使用该工具的效果

> [!TIP]
> **考试关联**
> 这演示了 Task 2.4：将 MCP servers 集成到 Claude Code 与 agent 工作流。考试哲学：**Tool description > Few-shot** — 清晰的工具描述比示例更重要。

---

## Demo 4：CI/CD 集成 — 自动化 PR 安全审查

**情境**：Claude Code 在 GitHub Actions 中执行，由 PR 创建或 `@claude` 提及触发。

**场景**：
- AWS 基础设施用 Terraform 定义
- 架构：DynamoDB table -> Lambda function -> S3 bucket
- 该 S3 bucket 与外部合作伙伴共享
- 一个 PR 将用户 email 加入数据流
- 将 PII（email）送入共享 bucket = **安全/合规风险**

**Claude 的发现**：识别出 PII 暴露风险 — 不是因为被告知「检查 PII」，而是因为它理解了 Terraform 基础设施流程，识别出用户 email 最终会出现在共享的 S3 bucket 中。

> [!IMPORTANT]
> **考试重点**
> 直接对应 Task 3.6（CI/CD integration），体现考试哲学：**Architecture > Prompt**。Claude 通过结构性理解基础设施代码来发现问题，而非被告知要找什么。

---

## 工具串联模式（考试重点）

| 模式 | Demo 范例 | 任务声明 | 适用场景 |
|---------|-------------------|----------------|---------------|
| 规划 -> 执行 -> 验证 | chalk 优化 (D1) | 1.1: Agentic loops | 复杂多步骤任务 |
| 执行 -> 观察 -> 改进 | Jupyter 分析 (D2) | 3.5: 迭代改进 | 数据分析、调试 |
| 通过 MCP 采用新工具 | Playwright 浏览器 (D3) | 2.4: MCP integration | 内建工具不足时 |
| CI 中的自动审查 | GitHub PR 审查 (D4) | 3.6: CI/CD pipelines | 代码审查、合规 |
| 适度的工具选择 | 所有 Demo | 2.5: Built-in tools | 先简单，需要时再扩展 |

> [!TIP]
> **考试哲学：适度响应**
> 从内建工具开始。只在内建能力真的不足时才加入 MCP servers 或自定义工具。考试测的是你知道「何时」该扩展，而非只是「如何」扩展。

---

## 练习题

### Q1：CI/CD 安全审查
你的团队使用 Terraform 管理 AWS 基础设施。一位初级工程师提交的 PR 将 `user_phone` 字段加入一个 Lambda function，该 function 会写入与第三方分析伙伴共享的 S3 bucket。你该如何配置 Claude Code 来拦截此问题？

<details><summary>答案</summary>

配置 Claude Code 为 PR 创建时触发的 GitHub Actions workflow。Claude 会读取 Terraform 文件，理解数据流（Lambda -> 共享 S3 bucket），并标记 `user_phone` 是被送往外部伙伴的 PII。关键洞察：你不需要写 prompt 说「检查 PII」— Claude 理解 infrastructure-as-code 并能追踪数据流。这就是 Architecture > Prompt 的实践（Task 3.6）。
</details>

### Q2：工具选择
你需要 Claude Code 优化一个 Python 函数的性能。以下哪个内建工具序列是最佳做法？

A) 直接用已知的优化模式 Edit 代码
B) Read 代码 -> Bash（执行 profiler）-> Read profiler 输出 -> Edit（应用修复）-> Bash（重跑 benchmark）
C) 从头 Write 一个全新实现
D) Grep 搜索代码库中类似的优化然后复制

<details><summary>答案</summary>

**B**。这遵循 Demo 1 的「规划 -> profiler -> 修复 -> 验证」模式。关键在于 Claude 应在优化前先测量（执行 profiler），然后验证改善（重跑 benchmark）。选项 A 跳过测量。选项 C 不成比例。选项 D 未针对特定瓶颈。测试 Task 2.5（有效使用内建工具）和 Task 1.1（agentic loop 设计）。
</details>

### Q3：MCP 扩展性
你希望 Claude Code 验证网页应用的登录页面在 CSS 变更后是否正确渲染。哪种方式最合适？

A) 让 Claude Read CSS 文件并推理视觉外观
B) 加入 Playwright MCP server 让 Claude 可以截图并视觉验证
C) 为每个 CSS 属性编写单元测试
D) 用 Bash 执行 headless 浏览器并存储截图供人工审查

<details><summary>答案</summary>

**B**。这完全符合 Demo 3。Playwright MCP 赋予 Claude 打开浏览器、截图、视觉验证的能力 — 建立紧密的反馈循环。选项 A 无法验证视觉渲染。选项 C 脆弱且不测试视觉外观。选项 D 需要人工审查，失去自动化的好处。测试 Task 2.4（MCP integration）和「内建工具不足时才用 MCP 扩展」的原则。
</details>
