# Introducing Hooks — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Claude Code Configuration & Workflows (20%) |
| Task Statements | 3.2 (custom commands & hooks), 1.5 (Agent SDK hooks for tool call interception) |
| Source | claude-code-in-action / 05-hooks / Lesson 14 |

---

## One-Liner

Hooks are middleware for Claude Code's tool execution pipeline. PreToolUse intercepts before execution (can block). PostToolUse runs after execution (can't block, but can transform and provide feedback).

---

## Tool Execution Pipeline

Here's what happens under the hood when you interact with Claude Code:

![Tool Execution Pipeline](../../visuals/tool-execution-pipeline.svg)
*Figure: How Claude Code processes tool calls — the model proposes, the system intercepts via hooks, then executes.*

Key insight: Hooks wrap the **tool execution**, not Claude's reasoning.

---

## Familiar Analogies

If you've worked with any of these, you already understand hooks:

| Technology | Corresponding Hook Concept | Behavior |
|-----------|---------------------------|----------|
| Express `app.use()` middleware | PreToolUse | Validate before handler executes |
| Git `pre-commit` hook | PreToolUse | Block commit if lint fails |
| Git `post-commit` hook | PostToolUse | Trigger CI/notifications after commit |
| Network request interceptor | PreToolUse | Inspect request, allow or deny |
| Response transformer | PostToolUse | Normalize data after response |

---

## Two Hook Types

### 1. PreToolUse — The Gatekeeper

Runs **before** tool execution. **Can block** the operation.

![PreToolUse Flow](../../../16-implementing-a-hook/visuals/env-guard-flow.svg)
*Figure: .env file guard data flow — PreToolUse intercepts Read calls and blocks access to sensitive files.*

Configuration:

```json
"PreToolUse": [
  {
    "matcher": "Read",
    "hooks": [
      {
        "type": "command",
        "command": "node /home/hooks/read_hook.ts"
      }
    ]
  }
]
```

The `matcher` field specifies which tool to intercept — in this case, only `Read`.

> 💡 **When to use PreToolUse**
>
> When an action **must never happen**. Examples:
> - Prevent Claude from reading `.env` or credential files
> - Block modifications to `migrations/` directory
> - Enforce refund limits before processing

### 2. PostToolUse — The Observer

Runs **after** tool execution. **Cannot block** (already happened), but can:

![PostToolUse Feedback Loop](../../../16-implementing-a-hook/visuals/self-correcting-loop.svg)
*Figure: Self-correcting feedback loop — Claude tries, hook blocks with explanation, Claude adjusts automatically.*

Configuration:

```json
"PostToolUse": [
  {
    "matcher": "Write|Edit|MultiEdit",
    "hooks": [
      {
        "type": "command",
        "command": "node /home/hooks/edit_hook.ts"
      }
    ]
  }
]
```

The `|` in matcher works like regex OR — matches Write, Edit, or MultiEdit.

> 🎬 **Instructor insight from the video**
>
> PostToolUse feedback goes **directly into Claude's context**. If your hook runs a linter and returns "Line 42: unused variable", Claude will fix it on the next turn automatically. This creates a **self-correcting feedback loop** with zero human intervention.

---

## Settings Hierarchy

Hooks are defined in Claude settings files at three levels:

| Level | Path | Scope | In Git? |
|-------|------|-------|---------|
| Global | `~/.claude/settings.json` | All projects on this machine | No |
| Project (shared) | `.claude/settings.json` | Whole team | **Yes** |
| Project (local) | `.claude/settings.local.json` | Just you | No (gitignored) |

You can also use the `/hooks` command inside Claude Code to configure hooks interactively.

> 🎯 **Exam note**
>
> The settings hierarchy follows the same precedence logic as git config — more local = higher priority. This is a frequently tested concept in D3.

---

## Practical Applications

| Use Case | Hook Type | What It Does |
|----------|----------|--------------|
| Auto-format | PostToolUse on Write/Edit | Run `prettier` after every file change |
| Auto-test | PostToolUse on Write/Edit | Run `npm test` after edits |
| Access control | PreToolUse on Read | Block reading sensitive files |
| Code quality | PostToolUse on Write/Edit | Run linter → feed results to Claude → auto-fix |
| Audit logging | PostToolUse on all | Track which files Claude accessed or modified |
| Naming conventions | PostToolUse on Write | Validate new files follow naming rules |

---

## Exam Focus: Hook vs Prompt

This is the most commonly tested trade-off across D1 and D3:

| Scenario | Hook | Prompt | Decision Factor |
|----------|------|--------|----------------|
| Refunds over $500 must escalate | ✅ | ❌ | "must" = deterministic |
| Friendly response tone | ❌ | ✅ | Preference = probabilistic OK |
| Identity verification before financial ops | ✅ | ❌ | Compliance = no exceptions |
| Prefer shorter responses | ❌ | ✅ | "prefer" = best effort |
| Auto-format after every edit | ✅ | ❌ | Consistency = can't miss |

> 💡 **Decision rule**
>
> If the question says "must / always / guaranteed / compliance" → Hook. If it says "prefer / usually / best practice" → Prompt.

Core exam philosophies at play:
- **Architecture > Prompt** — structural solutions over instructional ones
- **Deterministic > Probabilistic** — programmatic enforcement over AI self-regulation

---

## Practice Questions

### Q1: CI/CD Pipeline Scenario

Your team uses Claude Code in CI for automated PR reviews. You need to ensure Claude **never** modifies files in the `migrations/` directory. What is the most reliable approach?

- A. Add instructions to the system prompt: "Never modify files in migrations/"
- B. Configure a PreToolUse hook that blocks Write/Edit operations targeting `migrations/` paths
- C. Set file permissions to read-only on the `migrations/` directory
- D. Configure a PostToolUse hook to revert any changes to `migrations/` files

<details><summary>Answer</summary>

**B** — PreToolUse hook deterministically blocks the operation before it occurs.

- A is prompt-based with non-zero failure rate
- C works at OS level but produces unclear errors for Claude and wastes tokens on failed attempts
- D is reactive — the modification already happened, and reverting adds complexity

Exam philosophies: **Deterministic > Probabilistic**, **Validation > Trust**
</details>

### Q2: Developer Productivity Scenario

You want Claude Code to automatically run `prettier` on any file it creates or edits. Which configuration is correct?

- A. PreToolUse hook with matcher `Write|Edit`, running prettier
- B. PostToolUse hook with matcher `Write|Edit|MultiEdit`, running prettier
- C. PostToolUse hook with matcher `Read`, running prettier
- D. PreToolUse hook with matcher `Bash`, running prettier

<details><summary>Answer</summary>

**B** — Formatting must happen after the file is written/edited (PostToolUse), and should cover all edit-type operations including MultiEdit.

- A runs before the file exists — nothing to format
- C targets the wrong tool
- D is unrelated to file editing
</details>

### Q3: Customer Support Agent Scenario

An Agent SDK application processes customer refunds. Business policy requires refunds exceeding $500 to be escalated to a human agent. How should this be enforced?

- A. Include the $500 limit in the agent's system prompt
- B. Implement a PostToolUse hook to check refund amounts after processing
- C. Implement a tool call interception hook that blocks `process_refund` calls exceeding $500 and redirects to `escalate_to_human`
- D. Add few-shot examples demonstrating the $500 threshold

<details><summary>Answer</summary>

**C** — PreToolUse interception provides deterministic compliance.

- A is probabilistic (prompts have non-zero failure rate)
- B is too late (refund already processed)
- D also cannot guarantee compliance

Exam philosophies: **Deterministic > Probabilistic**, **Architecture > Prompt**
</details>
