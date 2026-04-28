# Claude Code Setup — Engineering Deep Dive（简体中文）

| 项目 | 内容 |
|------|------|
| 考试 Domain | D3 — Claude Code Configuration (20%) |
| Task Statements | 3.1（Claude Code 安装与配置）、3.2（认证）、1.1（Claude Code 概览） |
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 74 |

---

## 一句话总结

Claude Code 是终端原生的 coding agent，用 `npm install -g @anthropic-ai/claude-code` 安装，用 `claude` 命令启动，可通过 MCP 扩展 —— 从全新机器到可用 agent 总共三条命令。

---

## Claude Code 开箱自带什么

安装前先记住 agent 默认带了什么，这样"下列哪项 Claude Code 支持？"的题目才能答对：

| 工具类别 | 功能 |
|---------|------|
| **文件操作** | 搜索、读取、编辑项目中任意文件 |
| **终端访问** | 在对话中直接执行 shell 命令 |
| **Web 访问** | 抓取文档页、搜索网络、拉取代码示例 |
| **MCP server 支持** | 通过注册 MCP server 扩展工具 |

MCP 集成是考试最重要的类别 —— 它是官方扩展点。心智模型就是"内置工具 + MCP"。

---

## 支持平台

Claude Code 是跨平台 CLI，lesson 明确支持：

- **macOS** —— 原生
- **Windows** —— 通过 WSL（Windows Subsystem for Linux）
- **Linux** —— 原生

在 Windows 上，原生 PowerShell/cmd **不是**受支持的路径，必须在 WSL 里跑。考题至少会有一题把 Windows 丢进安装场景。

---

## 三步安装流程

整个流程就三步，按顺序背下来：

### Step 1 —— 安装 Node.js

Claude Code 以 npm 包形式发布，所以需要 Node 与 npm。Lesson 建议先检查：

```bash
npm help
```

能跑就说明已装；没装就去 `nodejs.org/en/download` 下载。

### Step 2 —— 全局安装 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

这条命令常见的考试陷阱：

- `-g` flag（global）—— 必要，因为 `claude` 要在 PATH 上。
- 包名是 `@anthropic-ai/claude-code`（在 `@anthropic-ai` 组织 scope 下）—— 不是 `claude`，也不是 `anthropic-claude-code`。
- 它是 npm 包，不是 `pip install`，也不是独立二进制。

### Step 3 —— 启动并认证

```bash
claude
```

第一次启动时 Claude Code 会要求登录 Anthropic 账号。登录后直接进入当前工作目录的交互式 agent session。

---

## 认证模型

Lesson 描述的是类似浏览器的登录流程，绑定 Anthropic 账号。重点：

- 登录绑的是 **Anthropic 账号**，不是贴在 config 文件里的 API key。
- 第一次跑 `claude` 会触发登录流程。
- 认证完后后续 session 自动复用凭证。
- 计费与用量走你的账号 —— 这跟直接用 `ANTHROPIC_API_KEY` 环境变量调 Anthropic API 不同。

考试重点差异：**Anthropic API 计费用 API key；Claude Code 用账号登录**。

---

## 全新 Mac 的完整安装 Session

```bash
# 1. 检查是否已有 Node
npm help
# 若未安装，到 nodejs.org/en/download 下载并安装

# 2. 全局安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 3. 验证已在 PATH 上
which claude
# /usr/local/bin/claude  （或类似）

# 4. 启动、认证、进入项目
cd ~/projects/my-app
claude
# 首次执行：打开登录流程
# 登录后：进入交互式 agent prompt
```

四条命令跑完就得到一个以当前目录为默认 project root 的终端 agent。

---

## 装完立即能做什么

`claude` 跑起来后，就可以直接用自然语言下命令，agent 会自动使用内置工具。第一个 session 可以试：

- `读 README.md 并总结这个项目`
- `找出所有引用旧 API endpoint 的文件`
- `跑测试套件并汇报失败项`

这些命令直接可用，不需额外配置。进阶配置（CLAUDE.md、MCP server、自定义命令）会在后续 lesson 讲。

---

## 常见错误

1. **漏掉 `-g` flag** —— 本地安装不会把 `claude` 放到 PATH 上。
2. **包名写错** —— 正确的 scoped 名称是 `@anthropic-ai/claude-code`。
3. **Windows 上没装 WSL 就直接跑** —— Lesson 明确 Windows 需要 WSL，不是原生 PowerShell。
4. **试图设置 `ANTHROPIC_API_KEY` 而不是登录** —— Claude Code 用账号登录，不用 raw API key。
5. **跳过 `npm help` 检查** —— 没装 Node 的机器会安装失败。

> **关键洞察**
>
> CCA 考试把 Claude Code 的安装流程当成"常识题"，必须一字不差背下来：**Node.js → `npm install -g @anthropic-ai/claude-code` → `claude` → 账号登录**。没有可选步骤，Windows 明确指 WSL。背熟这句话就是稳拿分。

---

## CCA 考试重点

- **D3（Claude Code Configuration）**：这 lesson 是约 20% 考题的基础，会出直接问安装命令和平台支持的题。
- **D1（Agentic Coding & Architecture）**：要知道 Claude Code 是 agent application，不是 chat app，MCP 是它的扩展机制。
- 预期至少一题问 npm 包的精确名称 —— `@anthropic-ai/claude-code`。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Claude Code 的三个安装步骤是什么？ | 1) 安装 Node.js、2) `npm install -g @anthropic-ai/claude-code`、3) 跑 `claude` 并登录 |
| Claude Code 的精确 npm 包名是什么？ | `@anthropic-ai/claude-code` |
| 为什么安装命令要用 `-g` flag？ | 全局安装会把 `claude` 可执行文件放到 PATH 上，任何目录都能启动 |
| Claude Code 支持哪些操作系统？ | macOS、Windows（通过 WSL）、Linux |
| Claude Code 的认证模型是什么？ | 通过 Anthropic 账号做账号登录，不是 raw `ANTHROPIC_API_KEY` |
| Claude Code 内置的四类工具是什么？ | 文件操作、终端访问、Web 访问、MCP server 支持 |
| 如何检查 Node.js 是否已安装？ | 跑 `npm help` |
| 首次启动 Claude Code 的命令是什么？ | `claude` —— 会触发登录流程 |
