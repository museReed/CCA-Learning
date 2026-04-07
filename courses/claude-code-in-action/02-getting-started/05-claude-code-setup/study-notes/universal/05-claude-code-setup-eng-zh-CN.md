# Claude Code Setup — 工程深度笔记

| 项目 | 细节 |
|------|--------|
| 考试领域 | D3 — Effective Claude Code Usage (30%) |
| Task Statements | 3.1 (CLAUDE.md hierarchy — awareness level) |
| 来源 | claude-code-in-action / 02-getting-started / Lesson 05（纯文字课程） |

---


![Installation Methods Platform Grid](../../visuals/installation-methods-platform-grid-zh-TW.svg)
*圖：各平台安裝方式。*

## 一句话总结

Claude Code 通过单一 CLI 命令即可安装于 macOS、Linux 或 Windows/WSL，并可选择性设置 AWS Bedrock 和 Google Cloud Vertex 作为 API provider。

---

## 安装方式

Claude Code 依操作系统提供多种安装路径：

| 平台 | 命令 |
|----------|---------|
| macOS (Homebrew) | `brew install --cask claude-code` |
| macOS / Linux / WSL | `curl -fsSL https://claude.ai/install.sh \| bash` |
| Windows CMD | `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd` |

安装完成后，在终端执行 `claude`。首次启动会触发认证提示。

> 💡 **关键洞察**
>
> Claude Code 完全在终端中运行 — 没有 GUI 应用程序。这是刻意设计：它在开发者已经工作的地方（shell）运作。

---

## Cloud Provider 设置（可选）

如果你的组织通过云供应商路由 API 调用，而非直接使用 Anthropic API：

| Provider | 设置指南 |
|----------|-------------|
| AWS Bedrock | [code.claude.com/docs/en/amazon-bedrock](https://code.claude.com/docs/en/amazon-bedrock) |
| Google Cloud Vertex | [code.claude.com/docs/en/google-vertex-ai](https://code.claude.com/docs/en/google-vertex-ai) |

这些适用于有既有云合约或数据驻留需求的企业环境。

---

## 考试重点

| 考试概念 | 本课教了什么 |
|-------------|-------------------------|
| **CLAUDE.md hierarchy (3.1)** | 认识 Claude Code 是一个 CLI 工具，具有 project-level 设置（CLAUDE.md 在此介绍，Lesson 07 详述） |

---

## 反模式

| 反模式 | 为何失败 |
|-------------|-------------|
| 安装 Claude Code 后期待有 GUI | Claude Code 设计上就是 CLI-only；它集成进终端工作流 |
| 首次执行时跳过认证 | `claude` 命令在认证前无法使用任何功能 |
| 在企业环境忽略 cloud provider 设置 | 如果组织使用 Bedrock/Vertex，直接 API 调用可能被阻挡或不合规 |
