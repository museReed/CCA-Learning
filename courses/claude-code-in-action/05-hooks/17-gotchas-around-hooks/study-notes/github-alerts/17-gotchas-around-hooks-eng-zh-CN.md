# Hooks 的注意事项 — 工程师深入解析

| 项目 | 细节 |
|------|--------|
| 考试领域 | D3 — Claude Code Configuration & Workflows (20%) |
| Task Statements | 3.2 (custom commands & hooks), 1.5 (Agent SDK hooks for tool call interception) |
| 来源 | claude-code-in-action / 05-hooks / Lesson 17（纯文字课） |

---

## 一句话摘要

Hook 脚本应使用**绝对路径**以确保安全性（防止 path interception 和 binary planting 攻击），但绝对路径破坏可移植性 — 解法是 `settings.example.json` + init script 模式。

---

## 核心问题

### 为什么要绝对路径？

```json
// ❌ 相对路径（安全风险）
"command": "node ./hooks/read_hook.js"

// ✅ 绝对路径（安全）
"command": "node /Users/alice/projects/queries/hooks/read_hook.js"
```

| 攻击 | 描述 | 绝对路径如何帮助 |
|--------|-------------|------------------------|
| **Path interception** | 攻击者在 `$PATH` 中放入恶意脚本 | 绝对路径绕过 `$PATH` 解析 |
| **Binary planting** | 攻击者在工作目录放入同名恶意文件 | 绝对路径指向确切的文件 |

> [!CAUTION]
> **安全性不可妥协**
>
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

> [!NOTE]
> **为何对团队很重要**
>
> 此模式确保：安全（绝对路径）+ 可移植（模板适用任何机器）+ 自动化 + 版本控制

---

## 两个 Settings 文件

| 文件 | 用途 | 在 Git？ |
|------|---------|---------|
| `settings.json` | 团队共用设置 | 是 |
| `settings.local.json` | 生成的机器特定文件 | 否 |

---

## 反模式（考试常考）

| ❌ 错误做法 | ✅ 正确做法 | 为什么 |
|-------------------|---------------------|-----|
| Hook command 用相对路径 | 用绝对路径 | 安全风险 |
| Commit 带绝对路径的 `settings.local.json` | Commit 带 `$PWD` 占位符的模板 | 绝对路径是机器特定的 |
| 手动编辑路径 | 用 init script 自动生成 | 手动容易出错 |

---

## 练习题

### Q1：开发者生产力场景（S4）

团队想共享 PreToolUse hook 配置。推荐方法？

- A. Commit 带相对路径的 `settings.local.json`
- B. Commit 带绝对路径的 `settings.json`
- C. Commit 带 `$PWD` 占位符的 `settings.example.json` 和 init script
- D. 每个开发者手动创建

<details><summary>答案</summary>

**C** — 兼顾安全和可移植性。

> [!IMPORTANT]
> 关键原则：模板 + init script = 安全 + 可移植
</details>

### Q2：CI/CD 集成场景（S5）

CI pipeline 的 hook 用相对路径被安全审计标记。修正？

- A. 将 hooks 目录加到 `$PATH`
- B. CI 加 setup 步骤生成带绝对路径的 `settings.local.json`
- C. CI 停用 hook
- D. 硬编码路径

<details><summary>答案</summary>

**B** — Init script 模式在 CI 也适用。

> [!IMPORTANT]
> CI/CD 环境需要与开发者机器相同的安全态势。
</details>

### Q3：代码生成场景（S2）

新开发者 clone 后 hook 不工作。有 `settings.example.json` 但没有 `settings.local.json`。原因？

- A. Hook 默认停用
- B. 需执行 `npm run setup` 生成 `settings.local.json`
- C. 需手动复制模板
- D. OS 不支持

<details><summary>答案</summary>

**B** — `settings.local.json` 被 gitignore，必须由 script 生成。
</details>
