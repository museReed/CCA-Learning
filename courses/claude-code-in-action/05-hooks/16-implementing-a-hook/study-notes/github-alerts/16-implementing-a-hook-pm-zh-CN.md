# 实现一个 Hook — PM 视角

| 项目 | 细节 |
|------|---------|
| 考试范围 | D3 — Claude Code Configuration & Workflows（占考试 20%） |
| Task Statements | 3.2 (custom commands & hooks), 1.5 (Agent SDK hooks) |
| 课程来源 | claude-code-in-action / 05-hooks / Lesson 16 |

---

## 重点摘要


![Implementation Flow](../../visuals/env-guard-flow-zh-TW.svg)
*圖：.env 檔案守衛資料流 — PreToolUse 攔截 Read 呼叫，阻擋敏感檔案存取。*

这堂课展示了完整可运行的 hook 实现。PM 不需要写 hook，但理解实现流程帮助你撰写更好的验收标准。

---

## 实现流程

| 步骤 | 建筑安保 | Hook 实现 |
|------|------------------|---------------------|
| 1. 登记摄像头 | 加到控制面板 | 在 `settings.local.json` 加入 hook |
| 2. 对准正确的门 | 设置角度 | 设置 `matcher` |
| 3. 设置警报规则 | "10 点后有人就警报" | 写脚本逻辑 |
| 4. 测试 | 走过门口验证 | 请 Claude 读取 .env |
| 5. 启用 | 启动系统 | 重启 Claude Code |

> [!TIP]
> **PM 洞察**
>
> Hook 需要**重启**才会生效。向团队部署新 hook 不是即时的 — 在推出计划中考虑这一点。

---

## PM 验收检查清单

> [!IMPORTANT]
> **验收标准**
>
> 1. **覆盖**：Hook 涵盖所有相关工具了吗？
> 2. **反馈质量**：封锁信息有解释政策吗？
> 3. **测试**：正面（封锁）和负面（允许）测试都通过
> 4. **设置层级**：合规 hook 在团队共用设置中

---

## 自我修正反馈回路

1. Claude 尝试读取 `.env`
2. Hook 封锁并发送反馈
3. Claude 确认并调整方法 — 不需人工介入

> [!WARNING]
> **PM 风险警示**
>
> 安全 hook 在 `settings.local.json` 的话，每个开发者必须个别配置。合规需求应坚持用 `settings.json`（团队共用、版本控制）。

---

## 反模式（考试常考）

| ❌ 错误做法 | ✅ 正确做法 | 为什么 |
|-------------------|---------------------|-----|
| 假设保存后就生效 | 一定重启 Claude Code | Hook 只在启动时加载 |
| 接受静默封锁 | 要求清楚的错误信息 | Claude 需要反馈 |
| 合规 hook 放个人设置 | 放团队共用设置 | 个人设置无法跨团队强制 |

---

## 练习题

### Q1：客户支持场景（S1）

团队实现了封锁 > $500 退款的 hook。Hook 运行但代理回复"I encountered an error"而非政策说明。你的建议？

- A. 在 system prompt 加退款政策
- B. 改善 hook 的 stderr 信息，包含政策说明
- C. 改用 PostToolUse
- D. 移除 hook

<details><summary>答案</summary>

**B** — Hook 的 stderr 信息直接转发给 Claude。

> [!IMPORTANT]
> **PM 重点**：Hook 反馈质量直接影响客户体验。
</details>

### Q2：开发者生产力场景（S4）

PreToolUse hook 在一位工程师的机器上未启用。Hook 只在 team lead 的 `settings.local.json`。修正方式？

- A. 发邮件给所有工程师
- B. 移到 `.claude/settings.json` 并 commit
- C. 在 CLAUDE.md 加入限制
- D. 在所有机器全局设置

<details><summary>答案</summary>

**B** — 团队共用 hook 属于 `.claude/settings.json`。

> [!IMPORTANT]
> **PM 重点**：合规 hook 必须在版本控制的团队设置中。
</details>

### Q3：多代理研究场景（S3）

PostToolUse hook 验证数据但 Claude 没使用验证后的数据。问题？

- A. 应改为 PreToolUse
- B. 反馈写到 stdout 而非 stderr
- C. Matcher 不对
- D. Context window 太小

<details><summary>答案</summary>

**B** — PostToolUse 反馈必须写到 stderr 才会进入 Claude 的 context。

> [!IMPORTANT]
> **PM 重点**：确认 hook 输出到 stderr 而非 stdout。
</details>
