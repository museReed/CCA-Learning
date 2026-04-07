# Project Setup — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows |
| Task Statements | 3.1 (project context prerequisite) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> 📝 本节所有内容均直接来自官方课程教材。

## One-Liner / TL;DR

课程提供了一个示例项目，让你有一个真实运行的应用可以搭配 Claude Code 探索 — 把它想成后续课程的 sandbox 环境。

## Core Concepts

### 为什么需要一个项目

搭配项目使用 Claude Code 会更有趣。课程提供了一个示例 UI 生成应用（与之前视频中展示的相同）。你不一定要运行这个项目 — 如果你愿意，可以用自己的 codebase 跟着做。

### 这个项目做什么

示例 app 是一个 **UI 生成工具**，通过 Anthropic API 使用 Claude 来创建 UI 组件。把它想成一个接收请求、产出视觉结果的小产品 — 类似许多 AI 驱动的 SaaS 工具底层的运作方式。

### 设置步骤（你的工程团队会做的事）

| 步骤 | 命令 / 操作 | PM 翻译 |
|------|------------|---------|
| 1 | 从 https://nodejs.org/en/download 安装 Node.js | 安装运行环境 — 类似在开发者机器上安装 Java 或 Python |
| 2 | 下载并解压 `uigen.zip`（附在课程单元中） | 获取项目文件 — 类似从 GitHub clone 一个 repo |
| 3 | 运行 `npm run setup` | 一键设置 — 安装依赖并配置数据库，类似 SaaS 产品 onboarding 向导中点击「Setup」 |
| 4 | *（可选）* 将 Anthropic API key 放入 `.env` 文件 | 配置 AI 集成 — 类似在工具的设置页面输入 OpenAI key。在 https://console.anthropic.com/ 获取 |
| 5 | 运行 `npm run dev` | 启动应用 — 类似在 IDE 中点击「Run」或启动本地服务器 |

> [!NOTE]
> API key（步骤 4）是可选的。如果没有提供 API key，app 仍会生成一些静态假数据。这是 **graceful degradation** 模式 — 产品以降低功能的方式运行，而非完全崩溃。

### 关键架构决策（PM 视角）

- **本地 SQLite 数据库**：不需要云端数据库配置。开发环境零基础设施成本。
- **可选 API key**：降低准入门槛。新成员无需等待 API 访问权限即可上手。
- **单一设置命令**：`npm run setup` 将多个步骤打包。良好的开发者体验（DX）减少 onboarding 摩擦。

## Key Takeaways

1. 示例项目是可选的 — 团队可以用自己的 codebase
2. 一个命令（`npm run setup`）处理整个环境搭建
3. API key 是可选的，展示了产品设计中的 graceful degradation
4. 项目代表了典型的 AI 集成 web 应用架构
5. 密钥（API key）存储在 `.env` 文件中，不在代码里 — 这是安全最佳实践

---

# PART 2: Study Aids

> 💡 补充学习材料，非官方课程内容。

## Familiar Analogies

- **`npm run setup`** — 类似企业软件的「Quick Start」向导。一键（一个命令）环境就绪。降低开发者的「首次产生价值时间」。
- **`.env` 文件** — 类似 SaaS 产品中输入 API key 和配置的设置页面。将密钥与应用代码分离。
- **Graceful degradation（无 API key）** — 类似 Spotify 的离线模式：核心功能仍可使用，但高级功能（实时 AI 生成）需要认证。
- **SQLite** — 类似嵌入式数据库（想象现代版的 MS Access）。适合原型开发，因为不需要独立的数据库服务器。

## CCA Exam Connection

> [!TIP]
> 作为 PM，考试可能测试你对项目设置背景的理解，而非记住精确命令。专注于：
> - 为什么 Claude Code 需要一个项目（它分析现有代码）
> - Claude Code（开发工具）与 Anthropic API（示例 app 在 runtime 使用的服务）的区别
> - 理解设置命令是项目特有的，不是 Claude Code 的功能

## Anti-Patterns

| Anti-Pattern | 为什么是错的 | 正确做法 |
|-------------|------------|---------|
| 以为 Claude Code 只能用在示例项目 | Claude Code 可以用在任何 codebase | 示例项目只是一个方便的演示 |
| 以为 API key 是课程必须的 | 课程明确表示这是可选的 | 没有 key 时 app 会 graceful degradation |
| 混淆项目设置与 Claude Code 设置 | 这是两件不同的事：一个设置 app，另一个设置 AI 工具 | 第 05 单元涵盖 Claude Code 设置；第 06 单元涵盖示例项目 |
| 因为「PM 不写代码」就跳过这个单元 | 理解开发环境有助于与工程团队沟通 | 至少要理解每个设置步骤完成什么 |

## Practice Questions

**Q1.** `npm run setup` 在示例项目中完成什么？

- A) 在开发者机器上安装 Claude Code
- B) 安装项目依赖并创建本地 SQLite 数据库
- C) 将应用部署到云端服务器
- D) 配置 Anthropic API key

> [!NOTE]
> **答案：B。** `npm run setup` 是项目特有的 script，安装依赖并创建本地数据库。它与 Claude Code 安装无关（那是第 05 单元的内容）。

**Q2.** 为什么示例项目在没有 Anthropic API key 的情况下仍能运行？

- A) 它使用 Claude Code 内置的 API key
- B) SQLite 在本地提供 AI 功能
- C) app 降级为生成静态假数据
- D) Node.js 内置 AI 生成功能

> [!NOTE]
> **答案：C。** 课程说明没有 API key 时，app 会生成静态假数据。这是 graceful degradation 模式 — 产品提供降低但可用的输出，而非完全失败。

**Q3.** PM 正在评估团队应该用示例项目还是自己的 codebase 来上课。哪个说法正确？

- A) 认证考试要求必须使用示例项目
- B) 团队必须在前三个模块使用示例项目，之后才能切换
- C) 两种都可以 — 课程明确表示你可以用自己的 codebase 跟着做
- D) 只有示例项目具备 Claude Code 需要的正确结构

> [!NOTE]
> **答案：C。** 课程明确说明：「You can always follow along with the remainder of the course with your own code base if you wish.」Claude Code 可以用在任何 codebase。
