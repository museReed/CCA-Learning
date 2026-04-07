# Claude Code in Action — PM 战略总览

| Item | Detail |
|------|--------|
| Exam Domain | D2: Tool Design & MCP Integration (18%), D3: Claude Code Configuration & Workflows (20%) |
| Task Statements | 2.4 (MCP integration), 2.5 (built-in tools), 3.6 (CI/CD integration), 1.1 (agentic loops) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> [!NOTE] 本节所有内容均直接来自官方课程教材。

## One-Liner / TL;DR

Claude Code 通过自主多步骤任务执行、MCP 可扩展工具、以及 CI/CD 自动化质量闸门来创造商业价值——减少性能、分析、设计和合规方面的工程瓶颈。

## Core Concepts

### Claude Code 天生就是可扩展的

Claude 本质上是一个专业的工具使用者。Claude Code 内置文件 I/O、执行和搜索工具——但更关键的是，它设计为**可扩展**的。新功能可以通过 MCP 服务器添加，无需重新训练或修改代码。

### 内置工具 — PM 需要知道的

大多数任务不需要特别配置工具。Claude 智能地串接内置工具：

| 功能 | 商业影响 |
|------|---------|
| 文件 I/O（Read、Write、Edit） | 自主修改代码，不需人工陪伴 |
| 执行（Bash） | 自动运行测试、benchmark、构建 |
| 搜索（Grep、Glob） | 导航大型代码库以理解上下文 |
| Notebook（NotebookEdit） | 带执行的数据分析，不只是生成代码 |
| 网络（WebFetch、WebSearch） | 研究并验证实时信息 |

### 智能工具组合

让 Claude Code 真正强大的是它如何**组合**这些工具来处理复杂的多步骤问题。把它想成一个能自己规划工作、执行、检查结果、并反复迭代的能干团队成员——全程不需要逐步指示。

---

## 🎬 Demo 演练：性能优化 — chalk 库

> 即使是广泛使用的基础设施也可能有隐藏的性能提升空间——就像在你团队每天使用的流程中找到 3.9 倍的效率改善。

**商业背景**：chalk 是 npm 第 5 大下载量包（每周约 4.29 亿次下载）。这个规模的性能优化通常需要资深工程师时间，而且经常被延后。

| 步骤 | 发生了什么 | 截图 |
|------|-----------|------|
| 1 | 讲师介绍 chalk——npm 第 5 大下载量包，整个生态系统的基础设施 | ![chalk docs](../../visual-guide/frames/frame_016.jpg) |
| 2 | 展示规模：每周 4.29 亿次下载——这里的改善会波及整个生态系统 | ![429M downloads](../../visual-guide/frames/frame_022.jpg) |
| 3 | Claude 自主创建 todo 列表、运行 benchmark、找出性能最差的案例 | ![todo and benchmarks](../../visual-guide/frames/frame_027.jpg) |
| 4 | Claude 编写针对性测试文件并使用 CPU profiling 精确定位瓶颈 | ![CPU profiling](../../visual-guide/frames/frame_030.jpg) |
| 5 | Claude 实现修正并用 benchmark 验证改善结果 | ![3.9x improvement](../../visual-guide/frames/frame_032.jpg) |

**结果**：🏆 **3.9 倍吞吐量提升**——在步骤之间完全自主完成，无需人工介入。

**商业影响**：
- 资深工程师时间从例行优化工作中释放
- 性能改善由被动变为主动
- 可量化的成果（3.9 倍）并有完整审计记录

> [!TIP] **PM 为何关心**：Claude 自行创建任务列表并跟踪进度。这种自我管理能力意味着它能处理通常需要技术主管分解的复杂多步骤工作。

---

## 🎬 Demo 演练：Jupyter Notebook CSV 流失分析

> 「写分析代码」和「写、执行、读结果、优化」的差别，就是模板和实际洞察的差别。

**商业背景**：从数据中获取洞察需要分析师或数据科学家。当数据团队满载时，产品团队只能等待。

| 步骤 | 发生了什么 | 截图 |
|------|-----------|------|
| 1 | 讲师提供视频流媒体平台用户 CSV 数据，要求 Claude 分析流失模式 | ![CSV dataset](../../visual-guide/frames/frame_037.jpg) |
| 2 | Claude 写分析代码、执行 notebook 单元格、读取实际输出 | ![notebook execution](../../visual-guide/frames/frame_041.jpg) |
| 3 | 根据发现的结果，Claude 定制下一步分析——逐步深入洞察 | ![iterative analysis](../../visual-guide/frames/frame_044.jpg) |

**结果**：通过反复执行产生完整的流失分析——不只是生成代码。

**商业影响**：
- 产品团队不用等数据团队就能获得初步数据洞察
- 分析质量更高，因为 Claude 根据实际结果迭代
- 缩短产品决策的洞察时间

> [!TIP] **PM 为何关心**：Claude 不只是生成代码就交出去。它执行、读取结果、并调整。这就是「拿到模板」和「拿到实际答案」的差别。

---

## 🎬 Demo 演练：使用 Playwright MCP 调整 UI 样式

> 当利益相关者问「Claude 能做 X 吗？」答案通常是「可以，用对的 MCP 服务器」。这是你可以纳入规划的能力。

**商业背景**：UI 样式迭代会在开发者和设计师之间产生来回沟通。每个循环耗费数小时或数天。

| 步骤 | 发生了什么 | 截图 |
|------|-----------|------|
| 1 | 讲师展示一个 UI 生成应用程序——聊天界面和标题栏需要样式调整 | ![unstyled UI](../../visual-guide/frames/frame_049.jpg) |
| 2 | Claude Code 获得 Playwright MCP 服务器访问权——通过配置添加浏览器控制工具 | ![Playwright MCP](../../visual-guide/frames/frame_054.jpg) |
| 3 | Claude 打开浏览器、导航到应用程序、截图评估当前状态 | ![browser screenshot](../../visual-guide/frames/frame_058.jpg) |
| 4 | Claude 更新样式、重新截图验证，反复迭代直到精致 | ![improved styling](../../visual-guide/frames/frame_061.jpg) |

**结果**：通过视觉反馈循环达成精致、专业的界面——以分钟计而非小时。

**商业影响**：
- 更快的设计迭代周期（分钟而非小时）
- 开发者自主处理样式调整
- MCP 扩展性意味着新功能无需重新训练——可以纳入规划

> [!TIP] **PM 为何关心**：MCP 就是扩展性的故事。新功能通过配置添加，不是工程工作。这代表你可以将 Claude Code 的能力增长纳入路线图。

---

## 🎬 Demo 演练：GitHub PR Review——拦截 PII 泄露

> 合规风险在合并前拦截，而非在生产环境中。扩展审查能力不需要多聘资深工程师。

**商业背景**：人工代码审查会遗漏跨领域的问题，如 PII 泄露，尤其在 infrastructure-as-code 中，数据流跨越多个文件和资源。

**情境**：AWS 基础架构含 DynamoDB → Lambda → S3 bucket。S3 bucket 与外部营销合作伙伴共享。数月后，开发者将用户 email 加入 Lambda 导出——忘了 bucket 是对外共享的。这导致 PII 泄露给外部合作伙伴。

| 步骤 | 发生了什么 | 截图 |
|------|-----------|------|
| 1 | Claude Code 在 GitHub Actions 中运行——由 PR 或 `@claude` 提及自动触发 | ![GitHub Actions](../../visual-guide/frames/frame_066.jpg) |
| 2 | AWS 情境：DynamoDB → Lambda → 与外部合作伙伴共享的 S3 bucket | ![AWS architecture](../../visual-guide/frames/frame_072.jpg) |
| 3 | 开发者添加一行 Lambda 代码——用户 email 现在流向共享 S3 bucket | ![one-line change](../../visual-guide/frames/frame_083.jpg) |
| 4 | 创建包含 email 添加的 Pull Request | ![PR created](../../visual-guide/frames/frame_094.jpg) |
| 5 | Claude Code 拦截 PII 泄露——追踪完整数据流并解释外部合作伙伴风险 | ![PII caught](../../visual-guide/frames/frame_098.jpg) |

**结果**：PII 泄露在合并前被拦截。Claude 追踪从 DynamoDB 经 Lambda 到共享 S3 bucket 的数据——理解基础架构，而非只是扫描关键字。

**商业影响**：
- 合规风险在合并前拦截，而非在生产环境
- 扩展审查能力不需要多聘资深工程师
- 理解基础架构脉络，而非只是代码语法
- 不论审查者是否可用，都有一致的审查质量

> [!TIP] **PM 关键要点**：Claude 拦截到这个问题不是因为有人写了规则说「检查 PII」。它理解了 Terraform 基础架构流程并辨识出风险。这就是 **Architecture > Prompt**——Claude 以结构化方式推理系统。

---

## 讲师提示

1. **Claude 自我管理复杂任务** — 它创建 todo 列表并跟踪进度，处理通常需要技术主管分解的工作
2. **从内置工具开始** — 大多数任务不需要特别配置；只在真正需要时才添加 MCP
3. **执行，不只是生成** — 「执行-观察-优化」循环产生明显更好的结果
4. **MCP 是配置，不是工程** — 添加功能是配置变更，不是开发项目
5. **CI/CD 自动化拦截人工遗漏** — 对跨文件数据流和合规特别有价值

## Key Takeaways

1. 🔧 **内置工具处理大部分任务** — 不需要特别配置就能开始获得价值
2. 🤖 **自主多步骤执行** — Claude 规划、执行、观察和优化，不需要逐步指引
3. 🔌 **MCP = 计划性扩展** — 通过配置添加功能，纳入路线图
4. 🏗️ **CI/CD 集成提供合规价值** — 自动审查拦截架构风险，不只是语法错误
5. 📊 **可量化的成果** — 3.9 倍性能提升、PII 在合并前拦截、更快的迭代周期

---

# PART 2: Study Aids

> [!TIP] 补充学习资料，非官方课程内容。

## Familiar Analogies

- **工具串接 = 生产线** — 每个站点（工具）做好一件事；序列创造成品。Claude 是决定什么去哪里、顺序如何的厂长。
- **MCP = Claude 的 App Store** — 内置工具是预装 app。MCP 服务器是你为特定需求安装的额外 app（浏览器控制、API 访问）。不需要全装——只装需要的。
- **CI/CD 审查 = 自动化质量检查** — 就像生产线上的品控检查点。每个 PR 通过，问题在出货前拦截，不需增加人力就能扩展。
- **执行-观察-优化 = 科学方法** — 假设（写代码）、实验（执行）、观察（读结果）、优化（调整方法）。Claude 用数据科学家实际工作的方式做数据科学。

## CCA Exam Connection

> [!TIP] 本课演示四种商业相关模式：

| 模式 | Demo | 商业价值 | Task Statement |
|------|------|---------|----------------|
| 自主任务管理 | Demo 1（chalk，4.29 亿次下载） | 减少资深工程师在性能工作上的瓶颈 | 1.1: Agentic loops |
| 执行-观察-优化 | Demo 2（Jupyter 流失分析） | 不依赖数据团队就能获得数据洞察 | 3.5: Iterative refinement |
| 通过 MCP 计划性扩展 | Demo 3（Playwright 浏览器） | 通过配置而非工程添加功能 | 2.4: MCP integration |
| 自动化合规审查 | Demo 4（GitHub Actions，PII） | 合并前风险检测，不增加人力 | 3.6: CI/CD pipelines |

## PM 决策框架

| 问题 | 指引 |
|------|------|
| 「我们需要 MCP 服务器吗？」 | 先不用。只在内置工具无法覆盖特定需求时才添加（如浏览器测试、API 集成） |
| 「Claude Code 适合放在哪里？」 | CI/CD 用于自动审查（Demo 4），开发者生产力用于临时任务（Demos 1-3） |
| 「如何衡量 ROI？」 | 每项任务节省的时间、合并前拦截的问题、专家瓶颈的减少 |
| 「采用风险是什么？」 | 内置工具低风险（不需配置）。MCP 中风险（需要配置）。CI/CD 低风险（标准 GitHub Actions） |
| 「推行顺序是什么？」 | 第一阶段：内置工具 → 第二阶段：CI/CD 审查 → 第三阶段：MCP 扩展 |

## Anti-Patterns

| Anti-Pattern | 为何错误 | 正确做法 |
|-------------|---------|---------|
| 一开始就过度配置 MCP 服务器 | 在用内置工具证明价值前增加配置成本 | 先简单开始，特定需求出现时再扩展 |
| 把 Claude 当成「只生成」的工具 | 错过「执行-观察-优化」的优势（Demo 2） | 启用执行环境（notebook、bash） |
| 合规只靠人工代码审查 | 人工会遗漏跨文件数据流，无法扩展 | 在 CI/CD 中自动化初步审查（Demo 4） |
| 期望关键字式 PII 检测 | 遗漏架构风险（数据流向共享资源） | 利用 Claude 的基础架构理解能力 |
| 所有分析都等数据团队 | 为产品决策制造瓶颈 | 用 Claude 做初步分析，数据团队做验证 |

## Practice Questions

**Q1.** 你的工程团队要采用 Claude Code。CTO 要求分阶段推行计划。根据 demo，最有效的顺序是什么？

- A) 先 MCP 扩展，然后 CI/CD，然后内置工具
- B) 内置工具用于开发者生产力，然后 CI/CD 用于自动审查，然后 MCP 用于专门工作流
- C) 先 CI/CD 以获得即时合规价值，然后其他
- D) 同时全面部署所有功能

> [!NOTE] **答案：B。** 第一阶段：内置工具（零配置、立即产生价值——Demos 1-2）。第二阶段：CI/CD 集成（GitHub Actions 配置、全组织合规——Demo 4）。第三阶段：MCP 扩展（只在特定需求出现时——Demo 3）。这遵循相称回应原则。

**Q2.** 一位重视安全的 VP 问：「如何确保 Claude Code 能拦截我们基础架构中的 PII 泄露？」最佳回应是什么？

- A) 「我们会为每种 PII 字段类型编写明确规则」
- B) 「CI/CD 中的 Claude Code 读取 infrastructure-as-code 并追踪数据流——在 demo 中它通过理解架构而非被告知要找什么来拦截 PII 泄露」
- C) 「我们需要一个自定义 MCP 服务器来扫描 PII」
- D) 「Claude Code 无法可靠地拦截 PII——我们需要专门工具」

> [!NOTE] **答案：B。** Claude Code 理解 Terraform 基础架构并追踪数据流（DynamoDB → Lambda → 共享 S3 bucket）。它在未被明确告知检查 PII 的情况下拦截了用户 email 对外部合作伙伴的泄露。这就是 Architecture > Prompt——Claude 以结构化方式推理系统。

**Q3.** 你的团队每周花 20 小时在代码审查上。如何定位 Claude Code 的 CI/CD 集成来证明配置投资的正当性？

- A) 「它会替代所有人工代码审查」
- B) 「它增强人工审查——自动化初步审查拦截结构和合规问题，人工聚焦在业务逻辑和架构决策」
- C) 「它只能拦截 PII 问题，价值有限」
- D) 「它需要大量工程投资来配置」

> [!NOTE] **答案：B。** Claude Code 处理初步审查（结构问题、安全、合规）。人工审查者聚焦在业务逻辑和架构决策。预期：审查周期缩短 30-50%、合规遗漏趋近零、一致的质量。配置成本：标准 GitHub Actions workflow——几小时的工程时间。

**Q4.** 另一个团队的 PM 问：「Claude Code 能帮我们分析用户流失数据而不用等数据团队吗？」你怎么说？

- A) 「不行，Claude Code 只能写代码」
- B) 「可以——Claude 能在 Jupyter notebook 中写分析代码、执行、读取实际结果并迭代。像是有一个初步数据分析师，不过关键发现应由数据团队验证」
- C) 「可以，但只有配置专门的数据分析 MCP 服务器才行」
- D) 「不行，数据分析需要专门模型」

> [!NOTE] **答案：B。** Demo 2 正是展示了这个：Claude 通过写代码、执行单元格、读取输出、优化分析来分析流失数据。「执行-观察-优化」循环产生真正的洞察，不只是代码模板。用于初步分析；关键发现由数据团队验证。
