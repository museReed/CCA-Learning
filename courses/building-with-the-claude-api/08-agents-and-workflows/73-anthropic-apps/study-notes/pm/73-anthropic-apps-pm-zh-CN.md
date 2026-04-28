# Anthropic Apps — PM Perspective（简体中文）

| 项目 | 内容 |
|------|------|
| 考试 Domain | D1 — Agentic Coding & Architecture (22%) |
| Task Statements | 1.1（Claude Code 概览）、1.2（agentic patterns）、1.4（Computer Use 作为 agent 案例） |
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 73 |

---

## 一句话总结

Claude Code 与 Computer Use 是 Anthropic 的两款旗舰 agent 产品 —— 它们是你设计 AI workflow 功能时的 UX、信任模型与价值主张的参考基准。

---

## 心智模型：实习生类比

把三种接口想成三种不同的助手：

| 接口 | 对应的助手 | 可以让它做什么 |
|------|-----------|----------------|
| Claude.ai | 聪明的朋友，用消息问他 | 快速解答、草稿、头脑风暴 |
| Anthropic API | 工作台上的零件盒 | 你自己组装成产品 |
| **Claude Code** | 坐在你键盘旁的工程实习生 | "修这个 bug、跑测试、开 PR" |
| **Computer Use** | 操作电脑的虚拟操作员 | "登入 dashboard、导出报表、发邮件" |

PM 视角：Claude.ai 是产品，API 是基础设施，而 Claude Code 和 Computer Use 是 *agent 产品* —— 它们会做事，而不只是回答问题。

---

## 为什么 PM 要关心

现今大部分 AI 功能还是聊天界面。真正有趣的产品类别（也是整个行业正在前进的方向）是 agent。Claude Code 与 Computer Use 正是两种主要 agent 原型的最佳案例：

| 原型 | 示例 | 最适合的场景 |
|------|------|-------------|
| Domain-native agent | Claude Code（终端、文件工具） | 目标领域有干净、typed 的工具 |
| GUI-driving agent | Computer Use（通过截图操作桌面） | 目标领域没有 API，只有 UI |

规划 AI 功能时，先决定属于哪种原型。Native agent 更便宜、更快、更可靠；GUI-driving agent 能解锁其他方法搞不定的场景。

---

## 产品使用场景

### 何时用 Domain-Native Agent（Claude Code 原型）

| 场景 | 为什么合适 |
|------|-----------|
| 在 IDE 或 CLI 里的开发者工具 | 已有干净的工具集成（文件系统、git、language server） |
| SQL 数据库的数据分析助手 | 可以暴露 typed 工具 —— query、schema、metric catalog |
| 对接工单 API 的客服 operator | 有一等公民的 API，动作可靠、可审计 |

### 何时用 GUI-Driving Agent（Computer Use 原型）

| 场景 | 为什么合适 |
|------|-----------|
| 自动化没有 API 的旧桌面软件 | 只剩 UI 可用，agent 必须"看得懂并点得对" |
| 跨第三方 Web 应用的 QA 测试 | 需要视觉回归与交互流程 |
| 取代脆弱 macro 的企业 RPA | Agent 能用 vision 适应 layout 变化 |

### 不适合的场景

| 场景 | 更好的替代 |
|------|-----------|
| 应用内的简单问答 | 直接用 API 做 chat，不需要 agent |
| 完全确定的固定流程 | 传统 workflow / RPA 脚本即可，不用 LLM |
| 极低延迟的实时需求 | 走固定代码路径 —— agent loop 太慢 |

---

## PM 决策框架

看到一个新的"AI 功能"提案时，问这些问题：

1. **这真的是 agent 吗？** 是否需要多步工具执行、环境交互、自主决策？如果不需要，那是 chat 功能 —— 风险小、天花板也低。
2. **适合哪种原型？** Native tool 风格（Claude Code）还是 GUI-driving 风格（Computer Use）？
3. **信任边界在哪？** Agent 代替用户行动。人类在哪一步批准？
4. **失败模式是什么？** 文件损坏、误点、不可逆动作 —— 先设计保险再动工。
5. **参考实现教了我们什么？** 两个 app 都有 permission prompt、memory（CLAUDE.md）、迭代式 workflow —— 直接借用这些模式。

---

## 信任与控制的权衡

Agent 的强大在于会"行动"，这同时是风险来源。Claude Code 与 Computer Use 都展示了这个光谱：

| 控制层级 | Claude Code 行为 | 用户体验 |
|---------|-----------------|---------|
| 只读 | 先显示计划，要求批准 | 安全但慢 |
| 逐步确认 | 每次编辑或 shell 命令前询问 | 平衡 |
| 自动批准 | 一次执行一整批变更 | 快但风险高 |

PM 的任务是挑一个默认值并提供合理的逃生出口。课程讲得很清楚：好的 agent 是 **协作伙伴**，不是完全自主的行动者。

---

## 常见 PM 错误

1. **只说"做一个 agent"却没定义原型** —— native-tool agent 与 GUI-driving agent 的成本和可靠度差很大。
2. **以为 Claude.ai 的 UX 可以直接套到 agent** —— agent 需要计划界面、权限确认、恢复机制，而 chat UI 没有这些。
3. **忽略 context 问题** —— Claude Code 大量投资在 CLAUDE.md，因为 context 管理占了一半工作。临时 prompt 无法 scale。
4. **把 Computer Use 当成"省下做 API 的便宜替代"** —— 它可行，但更慢、更脆弱、更费 token。能做 API 就先做 API。
5. **为了"更自主"跳过人类批准步骤** —— 对任何破坏性动作，批准不是可选项。

> **关键洞察**
>
> Claude Code 与 Computer Use 不只是产品，而是 **PM 层级的参考设计** —— 对应两种主流 agent 原型：native-tool agent 与 GUI-driving agent。研究它们的 UX 选择（权限确认、持久 memory 文件、"先规划再执行"流程），你就有了自己 agent 功能的设计模板。

---

## CCA 考试重点

- **D1（Agentic Coding & Architecture）**：看到"这是不是 agent"的场景时，要能映射到四项特性。
- **D3（Claude Code Configuration）**：这 lesson 是后续 Claude Code 重头戏题组的入口，先记住应用分类术语。
- 题目常对比 chat、API、agent —— 要知道每种扮演什么角色。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Anthropic 的两款旗舰 agent 应用是什么？ | Claude Code 和 Computer Use |
| 实习生类比中，Claude Code 等同什么角色？ | 坐在你键盘旁、实际动手做事的工程实习生 |
| 本 lesson 提出的两种主流 agent 原型是什么？ | Domain-native agent（Claude Code 风格）与 GUI-driving agent（Computer Use 风格） |
| PM 何时应优先选 native-tool agent 而非 GUI-driving？ | 只要目标领域有干净 API 或 typed 工具 —— 便宜且可靠 |
| GUI-driving agent 适合什么时候用？ | 目标 app 没有 API 只有 UI（旧桌面软件、第三方 dashboard） |
| PM 必须管理的信任权衡是什么？ | Agent 代替用户行动 —— 必须在只读、逐步确认、自动批准之间选择默认值 |
| 为什么 CLAUDE.md 对 PM 有意义？ | 它展示了"持久 context"这个产品模式 —— 提醒 agent UX 不只是 prompt，还包括记忆 |
| Computer Use 能取代搭建正式 API 吗？ | 不行 —— 它只是没 API 时的 fallback，更慢、更脆弱、更贵 |
