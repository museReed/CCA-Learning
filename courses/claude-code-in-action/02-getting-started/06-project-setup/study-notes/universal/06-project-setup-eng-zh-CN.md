# Project Setup — 工程深度笔记

| 项目 | 细节 |
|------|--------|
| 考试领域 | D2 — Tool Design & MCP Integration (18%), D3 — Effective Claude Code Usage (30%) |
| Task Statements | 2.5 (built-in tools — awareness), 3.5 (iterative refinement — intro) |
| 来源 | claude-code-in-action / 02-getting-started / Lesson 06（纯文字课程） |

---

## 一句话总结

课程演示项目是一个以 Anthropic API 和 SQLite 为后端的 Node.js UI 生成应用 — 用来探索 Claude Code 的 built-in tools 和迭代工作流的实践沙箱。

---

## 项目架构

演示项目（`uigen`）通过 Anthropic API 使用 Claude 生成 UI 组件：

```
uigen/
├── package.json          # Node.js 项目设置
├── .env                  # Anthropic API key（可选）
├── prisma/
│   └── schema.prisma     # SQLite 数据库 schema
├── src/
│   ├── server/           # 后端 API 路由
│   └── client/           # 前端 UI
└── node_modules/         # 依赖（npm run setup 后生成）
```

**关键设置步骤：**
1. 安装 Node.js
2. 解压 `uigen.zip` 并执行 `npm run setup`（安装依赖 + 创建 SQLite DB）
3. 可选地在 `.env` 中加入 Anthropic API key
4. 以 `npm run dev` 启动

> 💡 **关键洞察**
>
> API key 是可选的。没有它，应用程序会生成静态假数据而非调用 Claude。这意味着即使没有 Anthropic API key 也能跟着课程学习。

---

## Built-in Tools 预览（Task 2.5）

本项目设置介绍了 Claude Code built-in tools 运作的场景。在后续课程中，你会使用：

| 工具 | 在此项目中的用途 |
|------|------------------------------|
| **Read** | 查看 `schema.prisma`、`package.json`、路由文件 |
| **Write / Edit** | 修改 UI 组件、添加 API 路由 |
| **Bash** | 执行 `npm run dev`、`npm run setup`、跑测试 |
| **Glob / Grep** | 在 `src/` 中搜索特定模式 |

Claude Code 会根据你的请求自动选择合适的工具。你不需要手动调用工具。

---

## Iterative Refinement 预览（Task 3.5）


![Iterative Refinement Cycle](../../visuals/iterative-refinement-cycle-zh-TW.svg)
*圖：迭代精煉循環 — 請求、建構、檢視、回饋。*

此项目旨在展示与 Claude Code 的迭代开发：

1. 请 Claude 生成一个 UI 组件
2. 在浏览器中查看结果
3. 提供反馈（截图、文字描述或两者皆有）
4. Claude 改进实现

这个引入-迭代-改进循环是高效使用 Claude Code 的基础，在 Lesson 07 和 08 中深入探讨。

---

## 考试重点

| 考试概念 | 本课教了什么 |
|-------------|-------------------------|
| **Built-in tool selection (2.5)** | 认识 Claude Code 有 Read、Write、Bash、Glob、Grep 等工具，且会自动选择 |
| **Iterative refinement (3.5)** | 介绍 generate-review-refine 循环 |

---

## 反模式

| 反模式 | 为何失败 |
|-------------|-------------|
| 跳过 `npm run setup` | SQLite 数据库不会存在，导致运行时错误 |
| 将含有 API key 的 `.env` commit 到版本控制 | 安全风险 — `.env` 应在 `.gitignore` 中 |
| 以为 API key 是必需的 | 应用程序在没有它的情况下使用静态备用数据正常运作 |
