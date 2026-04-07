# Hooks 的注意事项 — PM 视角

| 项目 | 细节 |
|------|---------|
| 考试范围 | D3 — Claude Code Configuration & Workflows（占考试 20%） |
| Task Statements | 3.2 (custom commands & hooks), 1.5 (Agent SDK hooks) |
| 课程来源 | claude-code-in-action / 05-hooks / Lesson 17（纯文字课） |

---

## 重点摘要

Hook 脚本应使用绝对路径以确保安全，但绝对路径是机器特定的。解法是模板文件搭配自动化 setup script。PM 需要理解这一点因为它影响入职、CI/CD 和安全合规。

---

## PM 为何需要关注

1. **安全审计** — 相对路径会被标记
2. **开发者入职** — 需要执行 setup 步骤
3. **CI/CD pipeline** — 需要机器特定配置
4. **团队一致性** — 没有模板模式 hook 可能静默失败

---

## 心智模型：办公大楼门禁卡

| 方面 | 门禁卡系统 | Hook 配置 |
|--------|----------------|-------------------|
| 安全需求 | 扫描器必须连到确切服务器 | Hook 必须指向确切脚本（绝对路径） |
| 可移植问题 | 每栋大楼地址不同 | 每台机器路径不同 |
| 解法 | 模板 + 大楼特定 setup | 模板设置 + 机器特定 init script |

> [!TIP]
> **PM 重点**
>
> 绝对路径 = 更高安全性，但需要自动化 setup 步骤。PRD 要求 hook 时，在部署计划中包含入职 setup。

---

## 两个文件

| 文件 | 在 Git？ | 包含 Hook？ |
|------|---------|----------------|
| `settings.json` | **是** | 一般设置 |
| `settings.local.json` | **否** | 带绝对路径的 Hook |

> [!WARNING]
> **PM 治理备注**
>
> 合规 hook 只在 `settings.local.json` 的话取决于每人是否执行 setup。包含在入职清单中。

---

## 反模式（考试常考）

| ❌ 错误做法 | ✅ 正确做法 | 为什么 |
|-------------------|---------------------|-----|
| 为方便允许相对路径 | 要求绝对路径 | 安全审计标记 |
| Commit 机器特定设置 | 用模板 + init script | 其他机器会坏 |
| 略过 setup 文档 | 入职清单包含 setup | 新人会有坏 hook |

---

## 练习题

### Q1：开发者生产力场景（S4）

新开发者加入后 Claude 可读取凭证文件。团队有 PreToolUse hook。原因？

- A. Claude Code bug
- B. 没执行 setup script，`settings.local.json` 未生成
- C. Hook 在全局层级
- D. PreToolUse 只对 Read 有效

<details><summary>答案</summary>

**B** — `settings.local.json` 被 gitignore，必须由 setup script 生成。

> [!IMPORTANT]
> **PM 重点**：Hook 激活是环境 setup 的一部分，必须在入职清单中。
</details>

### Q2：CI/CD 集成场景（S5）

安全团队要求绝对路径。CI 在动态 runner 上。如何配置？

- A. CI 中用相对路径
- B. 加 CI 步骤执行 init script 生成 `settings.local.json`
- C. 硬编码路径
- D. 停用 hook

<details><summary>答案</summary>

**B** — Init script 模式在 CI 也适用。

> [!IMPORTANT]
> CI/CD 环境需要与开发者机器相同的安全态势。
</details>

### Q3：客户支持场景（S1）

安全审计标记 hook 用相对路径。工程师说绝对路径难共享。解法？

- A. 接受风险
- B. 用带 `$PWD` 占位符的模板和 init script
- C. 移除 hook 用 prompt
- D. 用相对路径加 CLAUDE.md 警告

<details><summary>答案</summary>

**B** — 模板 + init script 同时满足安全和可移植。

> [!IMPORTANT]
> **PM 重点**：安全-便利取舍时寻找两者兼顾方案。
</details>
