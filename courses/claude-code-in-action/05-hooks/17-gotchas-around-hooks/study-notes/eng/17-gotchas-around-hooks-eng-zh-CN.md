# Hooks 的注意事项 — 工程师深入解析

| 项目 | 细节 |
|------|--------|
| 考试领域 | D3 — Claude Code Configuration & Workflows (20%) |
| Task Statements | 3.2 (custom commands & hooks), 1.5 (Agent SDK hooks for tool call interception) |
| 来源 | claude-code-in-action / 05-hooks / Lesson 17（纯文字课） |

---

## 一句话摘要

Hook 脚本应使用**绝对路径**以确保安全性（防止 path interception 和 binary planting 攻击），但绝对路径破坏跨机器的可移植性 — 解法是 `settings.example.json` + init script 模式，用 `$PWD` 占位符替换为机器特定的绝对路径。

---

## 背景：安全性与可移植性的取舍

你已经知道如何定义和实现 hook（Lesson 15-16）。这堂课解决一个真实世界的部署问题：安全最佳实践（绝对路径）与团队协作（共享设置文件）之间的紧张关系。

> 💡 **iOS/Swift 类比**
>
> 这就像 certificate pinning 的取舍：硬编码 hash（安全但证书轮换时坏掉）vs 从 config 加载（灵活但需要安全的分发机制）。你两者都需要 — 解法是自动化的 setup 步骤。

---

## 核心问题

### 为什么要绝对路径？

```json
// ❌ 相对路径（安全风险）
"command": "node ./hooks/read_hook.js"

// ✅ 绝对路径（安全）
"command": "node /Users/alice/projects/queries/hooks/read_hook.js"
```

绝对路径缓解两种攻击向量：

| 攻击 | 描述 | 绝对路径如何帮助 |
|--------|-------------|------------------------|
| **Path interception** | 攻击者在 `$PATH` 中较早出现的目录放入恶意脚本 | 绝对路径完全绕过 `$PATH` 解析 |
| **Binary planting** | 攻击者在工作目录放入同名恶意文件 | 绝对路径指向确切的文件 |

> ⚠️ **安全性不可妥协**
>

![Security vs Portability](../../visuals/security-portability-tradeoff-zh-TW.svg)
*圖：安全性與可攜性的取捨 — 絕對路徑安全但綁定機器；Template + init script 可兩全其美。*

> CCA 考试将安全最佳实践视为正确答案。

---

## 解法：模板 + Init Script


![Template Init Pattern](../../visuals/template-init-pattern-zh-TW.svg)
*圖：Template → Init → Local 模式 — 提交含 $PWD 佔位符的 template，一次性 init 產生機器專屬設定。*

### 1. `settings.example.json`（commit 到 git）

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read|Grep",
        "hooks": [
          {
            "type": "command",
            "command": "node $PWD/hooks/read_hook.js"
          }
        ]
      }
    ]
  }
}
```

### 2. `scripts/init-claude.js`（commit 到 git）

读取模板 → 替换 `$PWD` → 写入 `settings.local.json`

### 3. `settings.local.json`（gitignored，自动生成）

带有机器特定绝对路径的输出文件。**永远不 commit**。

> 📝 **为何对团队很重要**
>
> 此模式确保：安全（绝对路径）+ 可移植（模板适用任何机器）+ 自动化（不需手动编辑路径）+ 版本控制（模板追踪；生成文件不追踪）

---

## 两个 Settings 文件解释

| 文件 | 用途 | 在 Git？ |
|------|---------|---------|
| `settings.json` | 团队共用设置 | 是 |
| `settings.local.json` | 带机器特定绝对路径的生成文件 | 否（gitignored） |

---

## 反模式（考试常考）

| ❌ 错误做法 | ✅ 正确做法 | 为什么 |
|-------------------|---------------------|-----|
| Hook command 用相对路径 | 用绝对路径 | 相对路径易受攻击 |
| Commit 带绝对路径的 `settings.local.json` | Commit 带 `$PWD` 占位符的 `settings.example.json` | 绝对路径是机器特定的 |
| 每个开发者手动编辑路径 | 用 init script 自动生成 | 手动编辑容易出错 |
| 跳过安全建议 | 永远用绝对路径 | CCA 考试期望安全最佳实践 |

---

## 练习题

### Q1：开发者生产力场景（S4）

团队想在所有开发者之间共享 PreToolUse hook 配置。推荐方法是？

- A. Commit 带相对路径的 `settings.local.json`
- B. Commit 带绝对路径的 `settings.json`
- C. Commit 带 `$PWD` 占位符的 `settings.example.json` 和生成 `settings.local.json` 的 init script
- D. 每个开发者手动创建自己的 `settings.local.json`

<details><summary>答案</summary>

**C** — 此模式提供安全性和可移植性。

- A：相对路径是安全风险
- B：共享设置中的绝对路径在其他机器上会坏
- D：手动设置不可扩展
</details>

### Q2：CI/CD 集成场景（S5）

CI pipeline 的 hook 配置用相对路径。安全审计标记为漏洞。正确修正？

- A. 将 hooks 目录加到 CI runner 的 `$PATH`
- B. 在 CI 加入 setup 步骤，根据 runner 的 workspace 目录生成带绝对路径的 `settings.local.json`
- C. 在 CI 停用 hook
- D. 用 `settings.json` 加硬编码的路径

<details><summary>答案</summary>

**B** — Setup 步骤反映 init script 模式。

- A：不修复相对脚本路径漏洞
- C：CI 中可能需要 hook
- D：CI runner 有不同 workspace 路径
</details>

### Q3：代码生成场景（S2）

新开发者 clone 项目后 hook 不工作。有 `settings.example.json` 但没有 `settings.local.json`。原因？

- A. Hook 功能默认停用
- B. 需要执行 `npm run setup` 从模板生成 `settings.local.json`
- C. 需手动复制 `settings.example.json`
- D. 操作系统不支持 hook

<details><summary>答案</summary>

**B** — `settings.local.json` 被 gitignore，必须由 init script 生成。

- A：Hook 默认可用
- C：直接复制不替换 `$PWD` 会留下坏掉的占位符
- D：Hook 是跨平台的
</details>
