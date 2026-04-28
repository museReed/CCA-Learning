# Summary and Next Steps — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | All 5 Domains (D1-D5) |
| Task Statements | Review: 1.1, 2.1, 2.4, 3.1, 3.2, 3.6 |
| Source | claude-code-in-action / 06-sdk-and-wrap-up / Lesson 22 |

---

## One-Liner

The course concludes with three actionable recommendations — stay updated, experiment with customization, and automate via GitHub integration — serving as a synthesis of all five CCA exam domains covered across the entire course.

---

![Course Review Map](../../visuals/course-review-map.svg)
*Figure: Course chapters mapped to CCA exam domains.*


## Instructor's Three Recommendations

| # | Recommendation | What It Means | Exam Domain |
|---|---------------|---------------|-------------|
| 1 | **Stay Updated** | Claude Code is in active development; new features, tools, and techniques are released frequently. Monitor the Claude Code homepage and changelog. | D1 — Agentic Architecture (understanding evolving capabilities) |
| 2 | **Experiment** | Author custom commands, enrich `CLAUDE.md`, try MCP servers beyond the course. Build muscle memory through experimentation. | D2 — Tool Use & MCP, D3 — Configuration |
| 3 | **Automate** | Use GitHub integration to delegate repetitive tasks. Think about what triggers (PR created, issue opened, `@claude` mention) can drive automation. | D3 — CI/CD, D5 — Developer Productivity |

---

## Course-to-Exam Domain Mapping

This is the most important review table for exam preparation. Each chapter maps to specific CCA domains:

| Chapter | Lessons | Primary Domain | Secondary Domain | Key Concepts |
|---------|---------|---------------|-----------------|--------------|
| 01 — Intro | 02-04 | D1 — Agentic Architecture (27%) | D5 — Developer Productivity (18%) | Agentic loops, plan-execute-observe cycle, coding assistant vs autocomplete |
| 02 — Getting Started | 05-08 | D3 — Configuration (20%) | D1 — Agentic Architecture (27%) | `CLAUDE.md`, project setup, context window, permission model, iterative changes |
| 03 — Context & Commands | 10-11 | D3 — Configuration (20%) | D2 — Tool Use & MCP (20%) | Context management, `@file` references, custom slash commands, `.claude/commands/` |
| 04 — Integrations | 12-13 | D2 — Tool Use & MCP (20%) | D3 — Configuration (20%) | MCP architecture (host/client/server), `settings.json`, GitHub Actions, `-p` flag, `allowed_tools` |
| 05 — Hooks | 14-19 | D3 — Configuration (20%) | D1 — Agentic Architecture (27%) | Hook lifecycle (9 types), PreToolUse/PostToolUse, blocking vs non-blocking, stdin/stdout protocol |
| 06 — SDK & Wrap Up | 20-22 | D1 — Agentic Architecture (27%) | D4 — Security (15%) | SDK programmatic access, `claudeClient.sendMessage()`, conversation turns array, synthesis |

---

## Key Concepts Revision Table

| Concept | Chapter | Domain | One-Sentence Definition |
|---------|---------|--------|------------------------|
| Agentic loop | 01 | D1 | Claude plans, executes tools, observes results, and iterates autonomously until the task is complete. |
| `CLAUDE.md` | 02 | D3 | Project-level instructions file that Claude reads automatically to understand project conventions and constraints. |
| Permission model | 02 | D4 | Three tiers — project (`settings.json`), user (`settings.local.json`), enterprise (`settings.enterprise.json`) — with allowlists and denylists. |
| Context window | 03 | D1 | Finite token budget; managed via `@file` references, `.claudeignore`, and compaction. |
| Custom commands | 03 | D3 | Markdown files in `.claude/commands/` that define reusable slash commands with `$ARGUMENTS` interpolation. |
| MCP architecture | 04 | D2 | Host (Claude Code) connects to MCP servers via stdio/SSE; servers expose tools, resources, and prompts. |
| `allowed_tools` in CI | 04 | D3/D4 | In non-interactive mode (`-p` flag), every tool must be individually listed — no blanket server permissions. |
| Hooks | 05 | D3 | Scripts that execute at specific lifecycle points; 9 types, 2 blocking (PreToolUse, UserPromptSubmit). |
| Hook stdin/stdout protocol | 05 | D3 | Hooks receive JSON on stdin, return JSON on stdout. Structure varies by hook type and tool matcher. |
| SDK (`@anthropic-ai/claude-code`) | 06 | D1 | Node.js package for programmatic Claude Code access; returns conversation turns array, supports streaming. |

---

## CCA Exam Study Checklist

Use this checklist to verify you have covered every major topic from the course:

### D1 — Agentic Architecture (27%)
- [ ] Can explain the agentic loop (plan, execute, observe, iterate)
- [ ] Understand how Claude decides which tools to use
- [ ] Know the difference between agentic coding and autocomplete
- [ ] Can describe the SDK's programmatic interface (`sendMessage`, conversation turns)
- [ ] Understand subagent architecture (Task tool)

### D2 — Tool Use & MCP (20%)
- [ ] Can describe MCP architecture: host, client, server
- [ ] Know the three MCP primitives: tools, resources, prompts
- [ ] Understand transport mechanisms: stdio and SSE
- [ ] Can configure MCP servers in `settings.json`
- [ ] Know the difference between local and CI MCP permissions

### D3 — Configuration & Workflows (20%)
- [ ] Can create and structure `CLAUDE.md` files (root, nested, `~/.claude/CLAUDE.md`)
- [ ] Know how to build custom commands in `.claude/commands/`
- [ ] Understand the hook system: 9 types, blocking vs non-blocking
- [ ] Can configure GitHub Actions workflows for Claude Code
- [ ] Know the `custom_instructions`, `mcp_config`, `allowed_tools` configuration layers

### D4 — Security & Trust (15%)
- [ ] Understand the three-tier permission model (project/user/enterprise)
- [ ] Know allowlist vs denylist behavior
- [ ] Can explain why CI requires explicit per-tool permissions
- [ ] Understand hook security implications (PreToolUse as access control)

### D5 — Developer Productivity (18%)
- [ ] Can identify when to use Claude Code vs traditional tools
- [ ] Know how to structure prompts for effective agentic execution
- [ ] Understand how automation (GitHub integration) reduces manual work
- [ ] Can evaluate the right level of customization (CLAUDE.md, commands, hooks, SDK)

---

## Flashcards

### Card 1
**Q:** What are the three transport mechanisms for MCP servers?
**A:** stdio (local process) and SSE (HTTP streaming). The course primarily covers stdio for local MCP servers and the GitHub Actions environment.

### Card 2
**Q:** What is the `-p` flag and when is it used?
**A:** The `-p` (print/pipe) flag runs Claude Code in non-interactive mode. Used in CI/CD (GitHub Actions). Requires `allowed_tools` to explicitly list every permitted tool since no human is available to approve.

### Card 3
**Q:** Name the two blocking hook types.
**A:** `PreToolUse` and `UserPromptSubmit`. These can prevent Claude from proceeding by returning `{ "decision": "block" }`.

### Card 4
**Q:** What are the three levels of `CLAUDE.md` configuration?
**A:** (1) Project root `CLAUDE.md`, (2) Nested directory `CLAUDE.md` files (scoped to subtree), (3) User-global `~/.claude/CLAUDE.md`.

### Card 5
**Q:** How does the SDK differ from the CLI?
**A:** The SDK (`@anthropic-ai/claude-code`) provides programmatic access via Node.js. You call `claudeClient.sendMessage()` and receive a conversation turns array. The CLI is interactive terminal use.

### Card 6
**Q:** What file structure do custom commands use?
**A:** Markdown files in `.claude/commands/` (project-scoped) or `~/.claude/commands/` (user-scoped). Invoked with `/command-name`. Support `$ARGUMENTS` placeholder for parameterization.

### Card 7
**Q:** In GitHub Actions, why can you not use `mcp__playwright` as a blanket permission?
**A:** In non-interactive mode (`-p` flag), there is no human to approve tool use. Every individual tool must be explicitly listed in `allowed_tools`. The blanket server-level permission only works in interactive (local) mode.

### Card 8
**Q:** What is the hook stdin/stdout protocol?
**A:** Hooks receive JSON on stdin with context about the event. They return JSON on stdout. For PreToolUse: return `{ "decision": "allow" }` or `{ "decision": "block", "reason": "..." }`. Structure varies by hook type.

### Card 9
**Q:** What three recommendations does the instructor give for continued learning?
**A:** (1) Stay updated — Claude Code is actively evolving. (2) Experiment — try custom commands, CLAUDE.md customization, new MCP servers. (3) Automate — use GitHub integration for repetitive tasks triggered by events.

### Card 10
**Q:** Which exam domain has the highest weight?
**A:** D1 — Agentic Architecture at 27%. It covers agentic loops, tool selection, SDK, and the fundamental plan-execute-observe cycle.
