# Configuration and multi-file skills — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Claude Code Configuration & Workflows (20%) |
| Task Statements | 3.1 (CLAUDE.md), 3.3 (custom commands/skills), 3.5 (permission model) |
| Source | introduction-to-agent-skills / Lesson 03 |

---

## One-Liner

This video covers the advanced techniques that make skills more powerful: the full set of metadata fields, how to write descriptions that trigger reliably, restricting tool access for security-sensitive workflows, and organizing larger skills across multiple files using progressive disclosure. You'll learn how to keep your skills efficient while still supporting complex use cases.

---

## Core Concepts

### Learning Objectives

- Configure advanced skill metadata fields including allowed-tools and model
- Write effective skill descriptions that reliably trigger on the right requests
- Use allowed-tools to restrict what Claude can do when a skill is active
- Organize complex skills using progressive disclosure and multi-file structures

### Key Takeaways

name and description are required — allowed-tools and model are optional but powerful additions
A good description answers two questions: What does the skill do? When should Claude use it?
allowed-tools restricts which tools Claude can use when the skill is active — useful for read-only or security-sensitive workflows

---

## Flashcards

**Q1:** name and description are required — allowed-tools and model ?
**A1:** name and description are required — allowed-tools and model are optional but powerful additions

**Q2:** A good description answers two questions: What does the skil?
**A2:** A good description answers two questions: What does the skill do? When should Claude use it?

**Q3:** allowed-tools restricts which tools Claude can use when the ?
**A3:** allowed-tools restricts which tools Claude can use when the skill is active — useful for read-only or security-sensitive workflows

---

*Source: introduction-to-agent-skills — Configuration and multi-file skills*
