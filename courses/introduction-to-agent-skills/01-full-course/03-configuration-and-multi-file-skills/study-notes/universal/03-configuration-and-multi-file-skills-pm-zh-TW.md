# Configuration and multi-file skills — PM Perspective

| 項目 | 細節 |
|------|---------|
| 考試覆蓋 | D3 — Claude Code Configuration & Workflows (20%) |
| 任務陳述 | 3.1 (CLAUDE.md), 3.3 (custom commands/skills), 3.5 (permission model) |
| 課程來源 | introduction-to-agent-skills / Lesson 03 |

---

## 一句話摘要

This video covers the advanced techniques that make skills more powerful: the full set of metadata fields, how to write descriptions that trigger reliably, restricting tool access for security-sensitive workflows, and organizing larger skills across multiple files using progressive disclosure. You'll learn how to keep your skills efficient while still supporting complex use cases.

---

## 為什麼 PM 需要知道

### 課後你會理解

- Configure advanced skill metadata fields including allowed-tools and model
- Write effective skill descriptions that reliably trigger on the right requests
- Use allowed-tools to restrict what Claude can do when a skill is active
- Organize complex skills using progressive disclosure and multi-file structures

### 重點摘要 (Business Impact)

name and description are required — allowed-tools and model are optional but powerful additions
A good description answers two questions: What does the skill do? When should Claude use it?
allowed-tools restricts which tools Claude can use when the skill is active — useful for read-only or security-sensitive workflows

---

## PRD 檢查清單

- [ ] Does the team understand configuration and multi-file skills?
- [ ] Are the relevant features documented?
- [ ] Have edge cases been considered?

---

*Source: introduction-to-agent-skills — Configuration and multi-file skills*
