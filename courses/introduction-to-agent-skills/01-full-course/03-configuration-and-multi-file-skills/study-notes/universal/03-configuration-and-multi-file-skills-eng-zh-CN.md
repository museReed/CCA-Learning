# Configuration and multi-file skills — 工程师深度解析

| 项目 | 细节 |
|------|--------|
| 考试领域 | D3 — Claude Code 设定与工作流程 (20%) |
| 任务陈述 | 3.1 (CLAUDE.md)、3.3 (自订指令/skill)、3.5 (权限模型) |
| 来源 | introduction-to-agent-skills / 第 03 课 |

---

## 一句话摘要

本影片涵盖让 skill 更强大的进阶技巧：完整的 metadata 栏位集、如何撰写能可靠触发的描述、为安全敏感的工作流程限制工具存取权限，以及使用渐进式揭露（progressive disclosure）跨多个档案组织较大的 skill。你将学会如何在支援复杂使用情境的同时保持 skill 的效率。

---

## 核心概念

### 学习目标

- 设定进阶 skill metadata 栏位，包括 allowed-tools 和 model
- 撰写能在正确请求时可靠触发的有效 skill 描述
- 使用 allowed-tools 来限制 skill 启用时 Claude 可以使用的工具
- 使用渐进式揭露和多档案结构来组织复杂的 skill

### 重点摘要

name 和 description 是必填栏位 — allowed-tools 和 model 是选填但功能强大的附加项目。
好的 description 要回答两个问题：这个 skill 做什么？Claude 应该在什么时候使用它？
allowed-tools 限制 skill 启用时 Claude 可以使用的工具 — 适用于唯读或安全敏感的工作流程。

---

## 记忆卡

**Q1：** name 和 description 是必填栏位 — allowed-tools 和 model…？
**A1：** name 和 description 是必填栏位 — allowed-tools 和 model 是选填但功能强大的附加项目。

**Q2：** 好的 description 要回答两个问题：这个 skill 做什么…？
**A2：** 好的 description 要回答两个问题：这个 skill 做什么？Claude 应该在什么时候使用它？

**Q3：** allowed-tools 限制 skill 启用时 Claude 可以使用…？
**A3：** allowed-tools 限制 skill 启用时 Claude 可以使用的工具 — 适用于唯读或安全敏感的工作流程。

---

*来源：introduction-to-agent-skills — Configuration and multi-file skills*
