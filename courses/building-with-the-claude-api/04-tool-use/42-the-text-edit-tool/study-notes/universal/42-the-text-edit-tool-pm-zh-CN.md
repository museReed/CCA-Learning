# Text Editor Tool — PM Perspective

| 项目 | 内容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%)、D1 — Agentic Architecture (22%) |
| Task Statements | 2.3（built-in / server tools）、1.2（tool 编排） |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 42 |

---

## One-Liner

Text editor tool 让你的产品可以在任意 workflow 中嵌入一个"迷你版 Claude Code"——Claude 已经知道怎么编辑文件,你只要提供一个可以写入的沙箱环境。

---

## Mental Model：宜家家具组

从零买 tool 像是用原木打造一把椅子——每一处接合都得自己设计。Text editor tool 则像一套宜家组合包:Anthropic 出所有零件（schema + 指令词汇）,你只要提供工作空间（你的文件系统或沙箱）。

| 项目 | 自定义 Tool | Text Editor Tool |
|------|------------|------------------|
| Schema 定义 | 你写 | Claude 内置 |
| 指令词汇 | 你设计 | 预先定义（view、create、str_replace、insert、undo_edit） |
| 执行代码 | 你写 | **还是你写** |
| 沙箱 / 安全模型 | 你负责 | **还是你负责** |

加速效果真实存在,但安全责任完全没变。

---

## 你的产品得到什么

Text editor tool 立刻解锁以下能力：

- **读文件**（任意粒度——整个文件或特定行范围）
- **列目录**
- **创建新文件**
- **在文件中替换字符串**
- **在指定行插入文字**
- **还原最近的编辑**

这是一个 code editor 的完整词汇。你可以构建的产品：

- 接收 repo 与 style guide、自动重写代码的 PR refactoring bot
- 把 Markdown 文件改写成新 schema 的内容迁移 agent
- 让 README 与 code 同步的文档自动更新器
- 为用户沙箱设置 config 的 onboarding assistant

---

## Product Use Cases

### Text Editor Tool 发光发热的时机

| 产品 | 适合度 | 原因 |
|------|-------|------|
| 代码重构工具 | 强 | 核心 loop 就是 view → edit → save |
| 文档生成器 | 强 | Claude 可以读 code、创建文档文件 |
| 模板 scaffolder | 强 | Claude 按标准结构创建多个文件 |
| 内部 developer agent | 强 | 聚焦于受控的 repo 沙箱 |
| 无头自动化（CI） | 强 | 文件是通用接口 |

### 不适合的情况

| 产品 | 更好的替代 |
|------|-----------|
| 结构化数据编辑（DB 记录） | 用你的 DB schema 自己建 tool |
| UI / 视觉编辑 | 用专门的设计工具 |
| 单一原子内容编辑 | 直接生成文字,不走文件 I/O |
| 协作实时文档编辑 | 改用 document-sync 服务 |

---

## 沙箱问题

既然由你的代码执行 Claude 的文件指令,blast radius 就是你决定。这是 PM 的关键决策：

| 沙箱范围 | 风险 | 使用场景 |
|---------|-----|---------|
| 整个文件系统 | 极高——Claude 可写任何地方 | 绝对不要上 production |
| 项目目录 | 中等——有范围但仍然不小 | 内部 developer 工具 |
| 独立 workspace 目录 | 低——边界清楚 | 面向用户的产品 |
| 只读 | 极低 | 分析 / review agent |
| 虚拟文件系统（内存） | 最低 | Preview-only 体验 |

先用最严格的沙箱满足产品价值,只有在明确理由下才放宽。

---

## PM Decision Framework

| 问题 | 如果 Yes | 行动 |
|------|---------|------|
| 产品的核心 workflow 是编辑文件吗？ | Yes | Text editor tool 很适合 |
| 能定义严格的沙箱目录吗？ | Yes | 可上 production |
| Claude 需要创建多个相关文件吗？ | Yes | Text editor 天然支持 |
| 用户期待 undo 功能吗？ | Yes | 在 handler 中实现 `undo_edit` |
| 产品需要写入关键系统路径吗？ | Yes | **停下来**——重新设计成沙箱化 |

---

## Hybrid 责任模型

这是 built-in tool 最重要的 PM insight：**Anthropic 拥有 schema,你拥有 runtime**。也就是说：

- 你决定"文件"的定义（可以是 S3 对象、Git blob、内存字符串）
- 你决定 `create` 的成本（比如按文件计费的产品）
- 你决定保留与 undo 行为
- 你决定 logging、审计、合规

PM 有时以为 built-in = fully managed,其实不是。Built-in 只代表"schema 预先接好了";所有运营面你还是要自己出。

---

## Common PM Mistakes

1. **以为 text editor tool 是 fully managed** — Anthropic 给 schema,但沙箱、安全、文件操作都要你的团队建。
2. **没实现 `undo_edit`** — 编辑器类型的产品用户期待 undo,忽略它会破坏心智模型。
3. **沙箱开太大就上线** — "只有内部用"会扩散到 production;一开始就严格。
4. **忽略 audit logging** — Claude 的编辑必须可追踪,才好 debug、合规、rollback。
5. **忘记 `view` 也能看目录** — 这个 tool 是关于导航,不只是编辑;list 与 read 都要支持。

> **Key Insight**
>
> Built-in tool 是 hybrid：Anthropic 出 schema,你出 runtime 与安全模型。Text editor tool 的产品价值是省去几周的 schema / 指令设计工作,但没省掉沙箱、审计、undo 这些运营面工作。预算要抓好。

---

## CCA Exam Relevance

- **D2 (Tool Design)**：Text editor tool 是 built-in（schema 内置）tool 且需要开发者执行的典型。
- **D1 (Agentic Architecture)**：文件操作是天然的多轮模式——view、edit、verify、重复。
- 考题常区分"built-in 但本地执行"（text editor）与"built-in 且托管执行"（web search）。

---

## Flashcards

| Front | Back |
|-------|------|
| Text editor tool 中 Anthropic 提供什么？ | Schema 与指令词汇——Claude 已经知道怎么用 |
| 开发者还要提供什么？ | 执行代码——真正在磁盘上读、写、创建、还原文件 |
| 这个 tool 支持哪些文件操作？ | view、create、str_replace、insert、undo_edit |
| 上线前 PM 最关键的决策是什么？ | 沙箱——Claude 被允许动哪个目录、路径或虚拟文件系统 |
| 为什么这是 hybrid 责任模型？ | Schema 由 Anthropic 完全 managed,runtime 与安全完全由开发者负责 |
| 列出三个 text editor tool 很适合的产品。 | 重构 bot、文档生成器、模板 scaffolder |
| Tool 集成之外 PM 还要编哪些预算？ | 沙箱、审计 logging、undo 行为、路径校验 |
| 如果 handler 没实现 `undo_edit` 会怎样？ | Claude 的 undo 尝试静默失败,用户心智模型被破坏 |
