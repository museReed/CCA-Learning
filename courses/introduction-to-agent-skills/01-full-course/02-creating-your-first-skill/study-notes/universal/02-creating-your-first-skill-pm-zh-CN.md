# Creating your first skill — PM Perspective

| 项目 | 細节 |
|------|---------|
| 考试覆蓋 | D3 — Claude Code Configuration & Workflows (20%) |
| 任務陳述 | 3.1 (CLAUDE.md), 3.3 (custom commands/skills), 3.5 (permission model) |
| 課程来源 | introduction-to-agent-skills / Lesson 02 |

---

## 一句话摘要

What you'll learn Estimated time: 20 minutes By the end of this lesson you'll be able to: Create a skill from scratch with proper frontmatter structure Test and verify that a skill loads correctly in Claude Code Explain how Claude Code matches incoming requests to available skills Describe the skill priority hierarchy (Enterprise, Personal, Project, Plugins) (4 minutes) This video walks through building a skill from scratch — a personal PR description skill that works across all your projects. You'll see exactly how to structure the SKILL.md file, test it, and understand how Claude Code discovers and matches skills to your requests. The video also covers the priority hierarchy that determines which skill wins when names conflict.

---

## 为什麼 PM 需要知道

### 課後你会理解

Estimated time: 20 minutes
By the end of this lesson you'll be able to:

### 重点摘要 (Business Impact)

A skill is a directory containing a SKILL.md file with metadata (name, description) in frontmatter and instructions below
Claude loads only skill names and descriptions at startup, then matches incoming requests against those descriptions using semantic matching
You get a confirmation prompt before Claude loads the full skill content into context
Priority for name conflicts: Enterprise → Personal → Project → Plugins
To update a skill, edit its SKILL.md. To remove one, delete its directory. Always restart Claude Code for changes to take effect

Let's walk through creating a skill from scratch, then look at how Claude Code actually loads and matches skills behind the scenes.
Creating a Skill
We'll build a personal skill that teaches Claude how to write PR descriptions in a consistent format. Since it's a personal skill, it lives in your home directory and works across all your projects.
First, create a directory for your skill inside the skills folder. The directory name should match your skill name:
mkdir -p ~/.claude/skills/pr-description
Then create a SKILL.md file inside that directory. The file has two parts separated by frontmatter dashes:
---
name: pr-description
description: Writes pull request descriptions. Use when creating a PR, writing a PR, or when the user asks to summarize changes for a pull request.
---

When writing a PR description:

1. Run `git diff main...HEAD` to see all changes on this branch
2. Write a description following this format:

### 需要了解的概念

- Bullet points of specific changes made
- Group related changes together
- Mention any files deleted or renamed

---

## PRD 检查清单

- [ ] Does the team understand creating your first skill?
- [ ] Are the relevant features documented?
- [ ] Have edge cases been considered?

---

*Source: introduction-to-agent-skills — Creating your first skill*
