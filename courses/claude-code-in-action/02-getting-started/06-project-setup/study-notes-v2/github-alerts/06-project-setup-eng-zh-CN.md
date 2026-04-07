# Project Setup — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows |
| Task Statements | 3.1 (project context prerequisite) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> 📝 本节所有内容均直接来自官方课程教材。

## One-Liner / TL;DR

设置一个示例 Node.js + SQLite UI 生成项目，让你在后续课程中有真实的 codebase 可以搭配 Claude Code 一起探索。

## Core Concepts

### 为什么需要一个项目

搭配项目使用 Claude Code 会更有趣。课程提供了一个示例 UI 生成应用（与之前视频中展示的相同）。你不一定要运行这个项目 — 如果你愿意，可以用自己的 codebase 跟着做。

### 前置需求

- 本机必须安装 **Node.js**
- 安装指引：https://nodejs.org/en/download

### 设置步骤

| 步骤 | 命令 / 操作 | 功能说明 |
|------|------------|---------|
| 1 | 安装 Node.js | 运行环境前置需求 |
| 2 | 下载并解压 `uigen.zip`（附在该课程单元中） | 获取示例项目文件 |
| 3 | `npm run setup` | 安装依赖并创建本地 SQLite 数据库 |
| 4 | *（可选）* 将 Anthropic API key 放入 `.env` 文件 | 启用实时 Claude API 调用以生成 UI |
| 5 | `npm run dev` | 启动开发服务器 |

> [!NOTE]
> 步骤 4 是可选的。如果没有提供 API key，应用仍会生成一些静态假数据。若要完整测试，可在 https://console.anthropic.com/ 获取 API key。

### 项目架构（从上下文推断）

- **Frontend + Backend**：Node.js 项目，带有 dev server（`npm run dev`）
- **Database**：本地 SQLite（由 `npm run setup` 创建）
- **AI Integration**：通过 Anthropic API 使用 Claude 生成 UI 组件
- **Graceful Degradation**：无 API key 时降级为静态假数据

## Key Takeaways

1. 示例项目是可选的 — 你可以改用自己的 codebase
2. `npm run setup` 一个命令同时处理依赖安装与数据库创建
3. Anthropic API key 是可选的；应用在没有 key 的情况下仍可正常降级运行
4. 这个项目提供一个真实的多文件 codebase，让你练习 Claude Code 交互
5. `.env` 文件用来存放密钥（API key）— 这是常见的 Node.js 模式

---

# PART 2: Study Aids

> 💡 补充学习材料，非官方课程内容。

## Familiar Analogies

- **`npm run setup`** — 类似 Rails 的 `rails db:setup` 或 Django 的 `python manage.py migrate`。一个命令同时搞定依赖和数据库。
- **`.env` 文件放 API key** — 与 Next.js、Vite 及大多数现代 Node.js 框架相同的模式。环境变量让密钥不进版本控制。
- **Graceful degradation** — 就像天气 app 在断网时显示缓存数据。没有 API key 应用仍能运行，只是内容是静态的。
- **SQLite 做本地开发** — 类似 Java 的 H2 或 Python 的 sqlite3。文件型数据库，零服务器配置。

## CCA Exam Connection

> [!TIP]
> 这个单元建立了后续课程使用的项目背景。预期考试会测试：
> - 理解 Claude Code 可以在现有 codebase 上工作（不只是新项目）
> - 知道 `npm run setup` 是项目特有的 script（不是 Claude Code 的命令）
> - 区分 Claude Code（CLI 工具）与 Anthropic API（示例 app 使用的服务）

## Anti-Patterns

| Anti-Pattern | 为什么是错的 | 正确做法 |
|-------------|------------|---------|
| 将含有 API key 的 `.env` 文件 commit 进版本控制 | 在版本控制中暴露密钥 | 将 `.env` 加入 `.gitignore`；项目应该已经这样做了 |
| 在 `npm run setup` 之前就跑 `npm run dev` | 数据库还不存在，app 会 crash | 一定要先跑 `npm run setup` |
| 以为 API key 是必需的 | 课程明确说明这是可选的 | 没有 key 时 app 会生成静态假数据作为 fallback |
| 混淆项目的 Anthropic API 使用与 Claude Code 本身 | 两者是分开的：项目调用 API；Claude Code 是你用来开发项目的 CLI | 理解 Claude Code 分析代码，而项目在 runtime 使用 Claude API |

## Practice Questions

**Q1.** 下载并解压示例项目后，应该先执行什么命令？

- A) `npm install`
- B) `npm run dev`
- C) `npm run setup`
- D) `node setup.js`

> [!NOTE]
> **答案：C。** `npm run setup` 会安装依赖并创建本地 SQLite 数据库。在 setup 之前就跑 `npm run dev` 会失败，因为数据库尚未创建。

**Q2.** 学生没有 Anthropic API key。运行示例项目时会发生什么？

- A) 应用完全无法启动
- B) 应用启动但在生成 UI 组件时 crash
- C) 应用启动并生成静态假数据，而非调用 Claude
- D) 应用启动时提示输入 API key

> [!NOTE]
> **答案：C。** 课程明确说明如果没有提供 API key，app 仍会生成一些静态假数据。API key 对于跟着课程学习来说是可选的。

**Q3.** Anthropic API key 应该放在示例项目的哪里？

- A) `config.json` 文件中
- B) `.env` 文件中
- C) 作为 `npm run dev` 的命令行参数
- D) 在 `package.json` 的 `scripts` 区块中

> [!NOTE]
> **答案：B。** 课程指示将 API key 放入 `.env` 文件，这是 Node.js 中环境特定配置的标准模式。
