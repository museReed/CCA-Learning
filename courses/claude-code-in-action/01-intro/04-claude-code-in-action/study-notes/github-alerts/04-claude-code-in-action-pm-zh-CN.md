# Claude Code in Action — PM 策略概览

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

Claude Code 通过自主多步骤任务执行、MCP 可扩展工具、以及 CI/CD 中的自动化质量闸门，减少工程瓶颈 — 涵盖性能、分析、设计与合规面向。

---

## 内建工具：PM 需要知道的事

Claude Code 默认搭载读写文件、执行命令、搜索代码库的工具。PM 的关键洞察：**大多数任务不需要额外配置特殊工具**。Claude 会智慧地串联这些内建工具。

| 能力 | 商业影响 |
|------------|----------------|
| 文件 I/O（Read, Write, Edit） | 自主修改代码，无需人工逐步指导 |
| 执行（Bash） | 自动执行测试、benchmark、构建 |
| 搜索（Grep, Glob） | 在大型代码库中导航理解上下文 |
| Notebook（NotebookEdit） | 有执行能力的数据分析，而非只是代码生成 |

> [!TIP]
> **PM 为何该关注**
> 规划 Claude Code 导入时，从内建工具开始。大多数工程任务无需额外设置成本即可涵盖。

---

## Demo 1：自动化性能审计

**商业问题**：性能优化需要资深工程师、耗时、且常被排到低优先级。

**发生了什么**：Claude 自主对 chalk 包（每周 4.29 亿次下载）进行 profiler 分析、找到瓶颈、实现修复、验证 3.9 倍吞吐量提升 — 步骤之间完全无需人工介入。

**商业影响**：
- 资深工程师时间从例行优化工作中释放
- 性能改善主动发生，而非被动应对
- 可量化的成果（3.9 倍提升）附带完整审计轨迹

> [!NOTE]
> **讲师洞察**
> Claude 创建自己的任务清单并追踪进度。这种自我管理能力意味着它能处理通常需要技术主管分解任务的复杂多步骤工作。

---

## Demo 2：无需数据团队的数据洞察

**商业问题**：从数据中获取洞察需要数据分析师或数据科学家。数据团队满载时形成瓶颈。

**发生了什么**：Claude 在 Jupyter notebook 中分析视频流媒体平台的用户流失数据。关键是，它执行自己的分析代码、读取结果、并根据发现定制后续分析。

**商业影响**：
- 产品团队无需等待数据团队即可获取初步数据洞察
- 分析质量更高，因为 Claude 根据实际结果迭代
- 减少产品决策的洞察获取时间

> [!TIP]
> **PM 为何该关注**
> 「写分析代码」与「写代码、执行、读结果、改进」的差别，就是模板与真正洞察的差别。Claude Code 做的是后者。

---

## Demo 3：无需设计师瓶颈的快速 UI 迭代

**商业问题**：UI 样式迭代在开发者和设计师之间产生来回。每个循环需要数小时到数天。

**发生了什么**：Claude 通过 Playwright MCP 获得浏览器控制工具。它打开应用、截图查看当前状态、修改样式、重新截图验证，反复迭代直到结果正确。

**商业影响**：
- 更快的设计迭代周期（分钟而非小时）
- 开发者可自主处理样式微调
- MCP 扩展性意味着新能力无需重新训练

> [!TIP]
> **PM 为何该关注**
> MCP 是扩展性的故事。当利益相关方问「Claude 能做 X 吗？」答案常常是「可以，用对的 MCP server 就行。」这是你可以纳入规划的能力。

---

## Demo 4：代码审查中的自动化合规检查

**商业问题**：人工代码审查会遗漏跨领域的关注点，如 PII 暴露，特别是在 infrastructure-as-code 中数据流横跨多个文件的情况。

**发生了什么**：Claude Code 在 GitHub Actions 中作为自动 PR 审查者执行。它发现一个代码变更会通过与外部合作伙伴共享的 S3 bucket 暴露用户 email（PII）— 通过理解 Terraform 基础设施流程。

**商业影响**：
- 合规风险在 merge 前被拦截，而非在生产环境
- 扩展审查能量无需增聘更多资深工程师
- 理解基础设施上下文，而非只是代码语法

> [!IMPORTANT]
> **考试重点**
> 这是 Architecture > Prompt：Claude 结构性理解基础设施。PM 应知道 Claude Code 的 CI/CD 集成提供的是合规价值，而不只是代码质量。

---

## PM 决策框架

| 问题 | 指引 |
|----------|----------|
| 「需要 MCP servers 吗？」 | 先不用。只在内建工具无法覆盖特定需求时才加（如浏览器测试、API 集成） |
| 「Claude Code 适合放在工作流的哪里？」 | CI/CD 用于自动审查（Demo 4），开发者生产力用于临时任务（Demo 1-3） |
| 「如何衡量 ROI？」 | 每任务节省时间、merge 前拦截的问题数、专家瓶颈的减少 |
| 「导入风险？」 | 内建工具低风险（无需设置）。MCP 中等（需要配置）。CI/CD 低风险（标准 GitHub Actions） |

---

## 练习题

### Q1：导入策略
你的工程团队想导入 Claude Code。CTO 要求你提出分阶段推行方案。根据本课的 Demo，最有效的顺序是什么？

<details><summary>答案</summary>

**第一阶段**：内建工具用于开发者生产力（Demo 1-2 — 性能优化、数据分析）。零额外设置，即时产生价值。**第二阶段**：CI/CD 集成用于自动 PR 审查（Demo 4 — 合规/安全）。需要 GitHub Actions 配置但提供组织层级价值。**第三阶段**：MCP 扩展用于特定工作流（Demo 3 — 浏览器测试、外部 API）。只在特定需求出现时。这遵循考试原则「适度响应」— 先简单，需要时再扩展。
</details>

### Q2：利益相关方沟通
一位注重安全的副总裁问：「如何确保 Claude Code 能拦截我们基础设施中的 PII 暴露？」最佳回应是什么？

<details><summary>答案</summary>

Claude Code 可以集成到 CI/CD pipeline 中作为自动 PR 审查者。它读取 infrastructure-as-code（如 Terraform）并追踪跨资源的数据流。在 Demo 4 中它拦截 PII 暴露不是因为被告知要找 PII，而是因为它理解用户数据正流向共享的外部 bucket。关键优势：它理解架构，所以能拦截基于规则的扫描器遗漏的问题。这是 Architecture > Prompt 哲学。
</details>

### Q3：ROI 论证
你的团队每周花 20 小时在代码审查上。你会如何包装 Claude Code 的 CI/CD 集成来论证设置投资的合理性？

<details><summary>答案</summary>

定位为增强而非替代。Claude Code 处理审查的第一轮 — 自动拦截结构性问题、安全顾虑和合规风险。人工审查者则专注于商业逻辑和架构决策。预期影响：审查周期时间减少 30-50%、PII/合规逃脱接近零、且不论审查者是否有空都维持一致的审查质量。设置成本是标准的 GitHub Actions workflow — 通常只需几小时的工程时间。
</details>
