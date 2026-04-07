# Claude Code Setup — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows |
| Task Statements | 3.1 (setup is prerequisite) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> 📝 本节所有内容均直接来自官方课程教材。

## One-Liner / TL;DR

Claude Code 通过单一终端命令即可在 macOS、Linux、WSL 或 Windows 上安装，首次运行时自动触发身份验证。

## Core Concepts

### 安装方式

提供三种平台专属安装命令：

| 平台 | 命令 |
|------|------|
| macOS (Homebrew) | `brew install --cask claude-code` |
| macOS, Linux, WSL | `curl -fsSL https://claude.ai/install.sh \| bash` |
| Windows CMD | `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd` |

> 📝
> macOS 通用脚本（`curl ... install.sh`）在没有 Homebrew 的 macOS 上也能使用，因此 Mac 用户有两种安装选项。

### 首次运行与身份验证

- 安装完成后，在终端执行 `claude`
- 首次启动会自动触发身份验证流程

### 完整设置参考

- 官方 quickstart 文档：https://code.claude.com/docs/en/quickstart

### Enterprise / 云供应商选项

企业部署的替代验证后端：

| 供应商 | 文档链接 |
|--------|---------|
| AWS Bedrock | https://code.claude.com/docs/en/amazon-bedrock |
| Google Cloud Vertex AI | https://code.claude.com/docs/en/google-vertex-ai |

## Key Takeaways

1. 每个支持平台都只需一行命令即可安装
2. macOS 有两条安装路径：Homebrew cask 或通用 curl 脚本
3. Windows 使用下载-执行-清除的模式（`curl -o ... && ... && del ...`）
4. 身份验证在首次运行 `claude` 时自动触发
5. 企业团队可通过 AWS Bedrock 或 Google Cloud Vertex AI 替代直接的 Anthropic 验证

---

# PART 2: Study Aids

> 💡 补充学习资料，非官方课程内容。

## Familiar Analogies

- **Homebrew cask install** — 与 `brew install --cask visual-studio-code` 相同模式。Cask = GUI/CLI 应用程序（非 library）。
- **curl pipe to bash** — 通用的 Node.js/Rust 安装器模式（`nvm`、`rustup`）。下载脚本并一次执行完毕。
- **Windows 三步骤** — 类似下载 `.exe` 安装程序、运行后删除。`&&` 串接确保每个步骤成功后才执行下一步。
- **首次运行验证** — 类似 `gh auth login`（GitHub CLI）或 `aws configure`——工具在首次使用时引导完成凭证设置。

## CCA Exam Connection

> 💡
> Setup 是所有实操领域的先决条件。预期考题会测试：
> - 特定 OS 对应的正确安装命令
> - 身份验证是通过运行 `claude` 触发（不是独立的 `claude auth` 步骤）
> - Bedrock/Vertex 是企业替代方案（个人使用不需要）

## Anti-Patterns

| Anti-Pattern | 为何错误 | 正确做法 |
|-------------|---------|---------|
| 运行 `npm install -g claude-code` | 这是旧的安装方法，不再是推荐路径 | 使用 `brew install --cask claude-code` 或官方 curl 脚本 |
| 对 curl 安装脚本使用 `sudo` | 官方脚本已处理权限；`sudo` 可能导致文件所有者问题 | 以普通用户身份运行 curl 命令 |
| 首次运行时跳过身份验证 | Claude Code 未验证无法工作 | 运行 `claude` 并完成验证提示 |
| 误认 Bedrock/Vertex 为必要设置 | 它们是可选的企业后端 | 直接 Anthropic 验证是默认方式 |

## Practice Questions

**Q1.** 团队中有位开发者使用 macOS 但未安装 Homebrew。他应该使用哪个命令安装 Claude Code？

- A) `brew install --cask claude-code`
- B) `npm install -g @anthropic/claude-code`
- C) `curl -fsSL https://claude.ai/install.sh | bash`
- D) `pip install claude-code`

> 📝
> **答案：C。** 通用 curl 脚本适用于 macOS、Linux 和 WSL，不需要 Homebrew。选项 A 需要 Homebrew。选项 B 和 D 不是官方安装方式。

**Q2.** 安装 Claude Code 后，开始使用的下一步是什么？

- A) 运行 `claude auth login` 设置凭证
- B) 在终端运行 `claude`——首次启动会触发身份验证
- C) 手动设置 `ANTHROPIC_API_KEY` 环境变量
- D) 从 Applications 文件夹打开 Claude Code GUI 应用程序

> 📝
> **答案：B。** 在终端运行 `claude` 即可触发首次身份验证流程。标准设置不需要独立的 auth 命令或手动 API key 配置。
