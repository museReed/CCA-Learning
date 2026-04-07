# Claude Code Setup — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows |
| Task Statements | 3.1 (setup is prerequisite) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> 📝 本节所有内容均直接来自官方课程教材。

## One-Liner / TL;DR

Claude Code 在每个主要平台上只需一行终端命令即可安装——团队成员可以自助完成，不需要 IT 工单。

## Core Concepts

### 安装方式

三种平台专属安装选项——全部都是一行命令，不需要管理员介入：

| 平台 | 命令 | PM 重点 |
|------|------|---------|
| macOS (Homebrew) | `brew install --cask claude-code` | 一行命令，团队可自助安装，无需 IT 工单 |
| macOS, Linux, WSL | `curl -fsSL https://claude.ai/install.sh \| bash` | 通用备案——即使没有 Homebrew 也能安装 |
| Windows CMD | `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd` | Windows 团队成员也支持——下载、安装、自动清除 |

> 📝
> macOS 用户有两条路径（Homebrew 或 curl 脚本）。这意味着无论机器配置如何，onboarding 都不会被阻塞。

### 首次运行与身份验证

- 安装完成后，在终端运行 `claude` 会触发首次身份验证
- 不需要额外设置步骤——工具会在首次启动时引导用户完成验证

### 完整设置参考

- 官方 quickstart 文档：https://code.claude.com/docs/en/quickstart

### Enterprise / 云供应商选项

适用于有合规或数据驻留需求的组织：

| 供应商 | 文档链接 | 何时考虑使用 |
|--------|---------|-------------|
| AWS Bedrock | https://code.claude.com/docs/en/amazon-bedrock | 团队已在 AWS 上，需要数据留在 AWS 区域 |
| Google Cloud Vertex AI | https://code.claude.com/docs/en/google-vertex-ai | 团队已在 GCP 上，需要数据留在 GCP 区域 |

## Key Takeaways

1. 零摩擦安装：macOS、Linux、WSL 和 Windows 各一行命令
2. macOS 提供两条安装路径——onboarding 不会有单点故障
3. Windows 使用下载-执行-清除模式（`curl -o ... && ... && del ...`）——完全自动化
4. 身份验证内建于首次启动——不需要额外的凭证配置步骤
5. 有合规需求的企业团队可通过 AWS Bedrock 或 Google Cloud Vertex AI 路由

---

# PART 2: Study Aids

> 💡 补充学习资料，非官方课程内容。

## Familiar Analogies

- **一行命令安装** — 类似从 IT 自助门户安装 Slack 或 Zoom，但只是一行终端命令。不需要下载页面，不用拖到 Applications。
- **首次运行验证** — 类似第一次打开新 SaaS 工具时要求登录。不需要预先配置。
- **Bedrock/Vertex 选项** — 类似选择团队的 Slack 数据存放在美国或欧洲区域。同样的产品，不同的托管方式以满足合规。
- **三平台命令** — 类似供应商同时提供 Windows、Mac 和 Linux 安装包——全平台覆盖代表没有团队成员会被阻塞。

## CCA Exam Connection

> 💡
> 作为 PM，你需要知道：
> - 安装是自助式的（每个平台一行命令）——影响推广规划
> - 验证在首次运行时自动发生——不需要 IT 配置步骤
> - Bedrock/Vertex 作为企业选项存在——与采购讨论相关
> - 哪个命令对应哪个 OS——预期至少有一题考平台与命令的配对

## Anti-Patterns

| Anti-Pattern | 为何错误 | 正确做法 |
|-------------|---------|---------|
| 规划多步骤 IT 协助的推广流程 | 安装只是一行命令——过度工程化推广流程 | 在 Slack 消息中分享每个平台的对应命令 |
| 假设 Windows 团队成员无法使用 Claude Code | Windows 通过 CMD 完全支持 | 分享 Windows curl 命令 |
| 在 onboarding 文档中要求手动设置 API key | 验证由工具在首次运行时处理 | 只需告知团队安装后运行 `claude` |
| 在供应商评估时忽略 Bedrock/Vertex | 企业团队可能因合规需要这些选项 | 在采购检查清单中纳入云供应商选项 |

## Practice Questions

**Q1.** 你正在将 Claude Code 推广到一个跨平台工程团队（macOS 和 Windows）。一位 Windows 开发者反馈他们没有 Homebrew。你应该如何建议？

- A) 请 IT 在他们的 Windows 机器上安装 Homebrew
- B) 告知他们 Claude Code 仅支持 macOS
- C) 分享 Windows CMD 命令：`curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd`
- D) 请他们换用 Mac

> 📝
> **答案：C。** Claude Code 提供专用的 Windows CMD 安装命令。Homebrew 是 macOS 包管理器，在 Windows 上不可用。Claude Code 支持 macOS、Linux、WSL 和 Windows。

**Q2.** 你的组织要求所有 AI 工具必须通过现有的 AWS 基础设施路由以满足合规。你应该推荐哪条设置路径？

- A) 使用直接 Anthropic 验证的标准安装
- B) 按照 https://code.claude.com/docs/en/amazon-bedrock 文档设置 AWS Bedrock 集成
- C) 通过 `pip install claude-code` 安装以获得 AWS 兼容性
- D) Claude Code 无法与 AWS 基础设施搭配使用

> 📝
> **答案：B。** AWS Bedrock 是两个企业云供应商选项之一（另一个是 Google Cloud Vertex AI），允许通过现有云基础设施路由 Claude Code 以满足合规需求。
