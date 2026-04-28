# What are skills? — 工程师深度解析

| 项目 | 细节 |
|------|--------|
| 考试领域 | D3 — Claude Code 设定与工作流程 (20%) |
| 任务陈述 | 3.1 (CLAUDE.md)、3.3 (自订指令/skill)、3.5 (权限模型) |
| 来源 | introduction-to-agent-skills / 第 01 课 |

---

## 一句话摘要

本影片介绍 skill — 可重复使用的 markdown 档案，用来教导 Claude Code 如何自动处理特定任务。你不需要每次请 Claude 審查 PR 或撰写 commit 讯息时都重复给出指示，只要撰写一次 skill，Claude 就会在该任务出现时自动套用。

---

## 核心概念

### 学习目标

- 定义 Claude Code skill 是什么以及它们如何运作
- 說明 skill 存放的位置（个人目录 vs. 專案目录）
- 区分 skill、CLAUDE.md 和 slash command 之间的差异
- 辨识适合使用 skill 作为自订工具的情境

### 重点摘要

skill 是一组指令资料夾，Claude Code 可以自动发现並使用它们来更准确地处理任务。每个 skill 都存放在一个 SKILL.md 档案中，其 frontmatter 包含名称和描述。

---

## 记忆卡

**Q1：** skill 是一组指令资料夾，Claude Code 可以自动发现並使用它们来…？
**A1：** skill 是一组指令资料夾，Claude Code 可以自动发现並使用它们来更准确地处理任务。每个 skill 都存放在一个 SKILL.md 档案中，其 frontmatter 包含名称和描述。

---

*来源：introduction-to-agent-skills — What are skills?*
