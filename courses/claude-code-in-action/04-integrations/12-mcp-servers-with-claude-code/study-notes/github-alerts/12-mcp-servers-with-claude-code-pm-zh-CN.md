# MCP Servers with Claude Code — PM 视角


![Mcp Server Ecosystem Taxonomy](../../visuals/mcp-server-ecosystem-taxonomy-zh-TW.svg)
*圖：MCP Server 生態分類。*

| 项目 | 内容 |
|------|------|
| 考试对应 | D2 — Tool Use & Integration（占 18%） |
| Task Statements | 2.4 ★★★（MCP integration）、2.1 ★★（tool interfaces）、2.3 ★★（tool distribution） |
| 课程来源 | claude-code-in-action / 04-integrations / Lesson 12 |

---


![Mcp Plugin Architecture Flow](../../visuals/mcp-plugin-architecture-flow-zh-TW.svg)
*圖：MCP 外掛架構流程。*


![Mcp Architecture](../../visuals/mcp-architecture-zh-TW.svg)
*圖：MCP Server 架構 — Claude Code ↔ 協定 ↔ Server ↔ 外部系統。*

## TL;DR

MCP server 是 Claude Code 的 plugin 系统。它让你扩展 Claude 能做的事 — 浏览网页、查数据库、操作 API — 不需要改 Claude Code 本身。PM 的关键洞察：MCP server 把「Claude 做不到 X」变成「Claude 做得到 X」，而且是在架构层面解决。这跟 prompt engineering 根本不同 — prompt 只能在 Claude 既有能力范围内运作。

---

## Why PMs Need to Understand MCP Servers

1. **界定产品能力范围** — 知道有哪些 MCP server 存在，就知道哪些 Claude 驱动的功能是可行的
2. **Build vs. configure 决策** — 很多能力已经有现成的 MCP server，不需要定制开发
3. **安全与权限治理** — MCP server 需要明确的权限管理，影响你的 risk assessment
4. **CI/CD 影响** — 自动化 pipeline 里的 MCP server 需要跟本地开发不同的权限设置

---

## Mental Model: AI 工具的 App Store

| 概念 | App Store 类比 | MCP Server 实际 |
|------|---------------|----------------|
| 核心产品 | 开箱即用的 iPhone | Claude Code 内建工具（Read、Write、Bash 等） |
| 扩展 | 安装一个 app | 加入 MCP server |
| 权限 | 「允许存取相机？」 | 「允许 mcp__playwright 工具？」 |
| 生态系 | App Store 目录 | MCP server registry |
| 设置 | App 设置 | `.claude/settings.local.json` |

> [!IMPORTANT]
> **考试核心哲学（PM 必记）**
>
> - **Architecture > Prompt** — 如果 Claude 需要某种能力，给它工具（MCP server）。不要试图用 prompt 让它做结构上做不到的事。
> - **Explicit Permissions > Blanket Access** — 特别是在 CI/CD 里，每个工具都必须逐一允许。

---

## Product Scenario Walkthrough

### Scenario: 改善 UI Component 生成品质

你的团队用 AI 生成 component。生成出来的 component 看起来很 generic — 全是紫到蓝渐变和标准的 Tailwind patterns。产品目标是生成更有创意、更有辨识度的 component。

| 做法 | 实现方式 | 结果 |
|------|----------|------|
| 只用 prompt engineering | 在生成 prompt 加「要更有创意」 | 改善有限 — Claude 没有视觉反馈 |
| MCP + 视觉反馈回路 | 安装 Playwright MCP → Claude 生成 component → Claude 打开浏览器看结果 → Claude 根据视觉评估更新 prompt | 显著改善 — Claude 根据实际视觉输出迭代 |

> [!TIP]
> **PM 决策框架**
>
> 问自己：「这需要 Claude 感知或交互 context window 以外的东西吗？」
> - 是 → 你需要 MCP server（架构解决方案）
> - 否 → Prompt engineering 可能就够了

---

## MCP Server 的商业影响

| 影响面 | 没有 MCP | 有 MCP |
|--------|---------|--------|
| 视觉 QA | 人工 review | Claude 通过 Playwright 自动验证 UI |
| 数据库操作 | 复制粘贴 query 结果给 Claude | Claude 直接查询 DB |
| API 测试 | 手动测 endpoint | Claude 测试 endpoint 并验证响应 |
| 开发速度 | Claude 盲写代码 | Claude 生成、验证、自主迭代 |

---

## 权限治理

MCP server 有一套权限模型，PM 应该了解以做 risk assessment：

| 设置 | 位置 | 谁控制 | 安全等级 |
|------|------|--------|---------|
| 本地全部允许 | `.claude/settings.local.json` | 个人开发者 | 低 — 方便开发 |
| 项目共用 | `.claude/settings.json` | 团队 / Tech Lead | 中 — 团队标准 |
| CI/CD 明确列出 | GitHub Actions workflow 文件 | DevOps / 团队 | **高 — 逐一列出每个工具** |

> [!TIP]
> **PM Takeaway**
>
> 在 production/CI 环境里，MCP 工具权限必须逐一列出。没有「允许这个 server 的所有工具」的捷径。这是刻意的安全设计 — 要纳入你的 risk assessment。

---

## Instructor Insights（视频补充）

1. **视觉反馈改变一切** — 讲师对 Claude 能看到实际 UI 输出后的品质提升感到惊讶。这意味着视觉验证能力应该是任何 UI 导向 AI workflow 的标配。
2. **MCP server 是扩展性的核心** — 讲师把 MCP 定位为扩展 Claude Code 的主要方式。如果你的产品 roadmap 包含 Claude 原生没有的 AI 能力，MCP server 就是答案。
3. **生态系快速成长** — 讲师建议探索跟你项目需求相符的 MCP server，暗示生态系已经成熟到可以用在 production。

---

## Practice Questions

### 第一题：开发者生产力情境

你的团队希望 Claude Code 能验证生成的 UI component 是否符合设计规格。目前开发者是手动比对截图。你会建议什么？

- A. 把设计规格加到 CLAUDE.md，让 Claude 知道要瞄准什么
- B. 安装 Playwright MCP server，让 Claude 打开浏览器，视觉化比对生成的 component 和规格
- C. 建立 PostToolUse hook，每次写文件后跑 visual regression test
- D. 让开发者截图贴到 Claude Code 对话里做 review

<details><summary>答案与解析</summary>

**B** — Playwright MCP server 让 Claude 有实际的浏览器存取，能看到和评估 UI 输出。这建立了自动化的视觉反馈回路。

- A 给 Claude 知识但没有视觉感知能力
- C 可行但需要既有的测试基础设施
- D 可行但是手动流程，失去了自动化的好处

> [!IMPORTANT]
> **PM 重点**：当落差是「Claude 无法感知某个东西」时，解决方案是 MCP server 赋予它感知能力 — 不是 prompt 描述它应该感知什么。

</details>

### 第二题：Code Generation 情境

一个 PM 在 scope 一个需要 Claude 跟 PostgreSQL 数据库交互的 AI 功能。工程师说「我们直接在 prompt 给 Claude schema 让它写 query 就好」。更好的做法是什么？

- A. 工程师的做法是对的 — 在 prompt 提供 schema context 就够了
- B. 安装 PostgreSQL MCP server，让 Claude 直接查询和验证 live 数据库
- C. 建立一个 custom tool 包装数据库 query，通过 Agent SDK 暴露
- D. B 和 C 都是对的，取决于这是 Claude Code 还是 Agent SDK 应用

<details><summary>答案与解析</summary>

**D** — 对 Claude Code workflow 来说，PostgreSQL MCP server（B）是正确做法。对 Agent SDK 应用来说，custom tool（C）是正确做法。核心原则一样：给 Claude 结构化的数据库存取，不要只靠 prompt 里的 schema 知识。

> [!IMPORTANT]
> **PM 重点**：工程师的「就跟 Claude 说」做法（A）是典型的 prompt-over-architecture 反模式。永远优先给 Claude 真正的工具，而非在 prompt 里描述能力。

</details>
