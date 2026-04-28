# What are skills? — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Claude Code Configuration & Workflows (20%) |
| Task Statements | 3.1 (CLAUDE.md), 3.3 (custom commands/skills), 3.5 (permission model) |
| Source | introduction-to-agent-skills / Lesson 01 |

---

## One-Liner

What you'll learn Estimated time: 15 minutes By the end of this lesson you'll be able to: Define what Claude Code skills are and how they work Explain where skills live (personal vs. project directories) Distinguish between skills, CLAUDE.md, and slash commands Identify scenarios where skills are the right customization tool (3 minutes) This video introduces skills — reusable markdown files that teach Claude Code how to handle specific tasks automatically. Instead of repeating instructions every time you ask Claude to review a PR or write a commit message, you write a skill once and Claude applies it whenever the task comes up.

---

## Core Concepts

### Learning Objectives

Estimated time: 15 minutes
By the end of this lesson you'll be able to:

### Key Takeaways

Skills are folders of instructions that Claude Code can discover and use to handle tasks more accurately. Each skill lives in a SKILL.md file with a name and description in its frontmatter
Claude uses the description to match skills to requests. When you ask Claude to do something, it compares your request against available skill descriptions and activates the ones that match
Personal skills go in ~/.claude/skills and follow you across all projects. Project skills go in .claude/skills inside a repository and are shared with anyone who clones it
Skills load on demand — unlike CLAUDE.md (which loads into every conversation) or slash commands (which require explicit invocation), skills activate automatically when Claude recognizes the situation
If you find yourself explaining the same thing to Claude repeatedly, that's a skill waiting to be written

---

## Flashcards

**Q1:** Explain: Skills are folders of instructions that Claude Code can disc...
**A1:** Skills are folders of instructions that Claude Code can discover and use to handle tasks more accurately. Each skill lives in a SKILL.md file with a name and description in its frontmatter

**Q2:** Explain: Claude uses the description to match skills to requests. Whe...
**A2:** Claude uses the description to match skills to requests. When you ask Claude to do something, it compares your request against available skill descriptions and activates the ones that match

**Q3:** Explain: Personal skills go in ~/.claude/skills and follow you across...
**A3:** Personal skills go in ~/.claude/skills and follow you across all projects. Project skills go in .claude/skills inside a repository and are shared with anyone who clones it

---

*Source: introduction-to-agent-skills — What are skills?*
