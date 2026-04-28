# Claude Code Setup — PM 视角

| 项目 | 细节 |
|------|---------|
| 考试涵盖 | D3 — Effective Claude Code Usage（占考试 30%） |
| Task Statements | 3.1 (CLAUDE.md hierarchy — awareness level) |
| 课程来源 | claude-code-in-action / 02-getting-started / Lesson 05（纯文字课程） |

---


![Installation Methods Platform Grid](../../visuals/installation-methods-platform-grid-zh-TW.svg)
*圖：各平台安裝方式。*

## TL;DR

Claude Code 是一个命令行工具，开发者用一行命令即可安装。PM 需要知道它是 CLI-only（没有 GUI）、支持所有主流平台，且可设置通过企业云供应商（AWS Bedrock、Google Cloud Vertex）路由以满足合规要求。

---

## 为什么 PM 该关注

1. **部署规划** — 了解安装需求有助于评估工程团队的上手时间
2. **企业合规** — Cloud provider 选项（Bedrock、Vertex）决定 Claude Code 是否符合组织的数据驻留与安全策略
3. **无 GUI = 开发者原生** — 这不是你在浏览器中 demo 的产品；它活在终端里

---

## 商业类比

| 概念 | 商业类比 |
|---------|-----------------|
| CLI-only 工具 | 像 Slack 只有聊天没有 email 备选 — 它强制采用原生工作流 |
| Cloud provider 路由 | 像选择付款走 Stripe 直连还是通过银行的支付网关 |
| 首次启动认证 | 像访问任何企业 SaaS 前的 SSO 登录 |

---

## 决策框架：Cloud Provider 选择

| 因素 | 直接 Anthropic API | AWS Bedrock | Google Cloud Vertex |
|--------|---------------------|-------------|-------------------|
| 设置复杂度 | 最低 | 中等 | 中等 |
| 企业账单 | 独立 Anthropic 账单 | 合并至 AWS 账单 | 合并至 GCP 账单 |
| 数据驻留 | Anthropic 基础设施 | 你的 AWS 区域 | 你的 GCP 区域 |
| 最适合 | 个人开发者、小团队 | AWS 优先组织 | GCP 优先组织 |

---

## 练习题

### 场景：企业推广规划

你的工程主管问将 Claude Code 推广到 50 人团队需要多长时间。根据本课内容，哪个答案最准确？

- A. 数周 — 每个开发者需要定制化设置
- B. 每个开发者几分钟 — 就是一行 CLI 安装命令加认证
- C. 完全取决于 cloud provider 设置
- D. Claude Code 需要 IT 集中安装到所有机器上

<details><summary>答案</summary>

**B** — Claude Code 用一行命令安装，只需首次启动认证。安装本身微不足道。

然而，如果组织需要 Bedrock/Vertex 路由，IT 或 DevOps 需要一次性完成额外的云设置（不是每个开发者都需要）。这不会改变每个开发者的安装时间。

**PM 重点**：不要高估推广复杂度。瓶颈在于 cloud provider 设置（如果需要的话），而不是工具安装本身。
</details>
