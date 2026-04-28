# Custom Commands — Engineering Deep Dive


![Custom Commands Scope Architecture](../../visuals/custom-commands-scope-architecture.svg)
*Figure: Custom commands scope — project vs user level.*


![Custom Command Mechanism](../../visuals/custom-command-mechanism.svg)
*Figure: Custom commands — markdown files become slash commands.*

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Claude Code Configuration & Workflows (20%) |
| Task Statements | 3.2 ★★★ (custom commands & skills), 3.1 ★★ (CLAUDE.md config) |
| Source | claude-code-in-action / 03-context-and-commands / Lesson 11 |

---

## One-Liner

Custom commands are reusable prompt templates stored as markdown files in `.claude/commands/`. They turn repeatable workflows into one-liner slash commands, with `$ARGUMENTS` as the injection point for dynamic input.

---

## How Custom Commands Work

Custom commands extend Claude Code's built-in `/` commands with your own project-specific shortcuts. The mechanism is simple:

1. Create a `.md` file inside `.claude/commands/`
2. The filename becomes the command name (e.g., `audit.md` → `/audit`)
3. The file contents become the prompt sent to Claude
4. Use `$ARGUMENTS` anywhere in the file as a placeholder for runtime input
5. Restart Claude Code to pick up new commands

> 💡 **Key mental model**
>
> Custom commands are **saved prompts with a trigger**, not scripts. They do not execute code directly — they instruct Claude what to do. Think of them as prompt templates, not shell scripts.

---

## Creating Your First Command

### Example 1: Dependency Audit

```
# File: .claude/commands/audit.md


![Claude Code Configuration Hierarchy](../../visuals/claude-code-configuration-hierarchy.svg)
*Figure: Claude Code configuration hierarchy.*

Review all dependencies installed in this project.
Check for known vulnerabilities and outdated packages.
If any vulnerabilities are found, update the affected packages.
After updating, run the test suite to verify nothing broke.
```

Usage: `/audit`

### Example 2: Write Tests (with Arguments)

```
# File: .claude/commands/write_tests.md

Write comprehensive tests for $ARGUMENTS.
Follow the existing test patterns in this project.
Run the tests after writing them to make sure they pass.
```

Usage: `/write_tests src/auth.ts` or `/write_tests the validation utilities in src/utils/`

> 🎬 **Instructor insight from the video**
>
> The instructor emphasizes that `$ARGUMENTS` is not limited to file paths. You can pass any string — a description, a feature name, or even natural language instructions. The placeholder is simply text substitution.

---

## Command Scope: Project vs User

| Scope | Path | Visible To | In Git? |
|-------|------|-----------|---------|
| Project | `.claude/commands/` | Whole team | **Yes** (committed) |
| User | `~/.claude/commands/` | Just you | No |

> 🎯 **Exam note**
>
> Project-scoped commands in `.claude/commands/` are the exam-relevant scope. They represent **team conventions codified as commands** — a key concept tested under D3. This follows the exam philosophy of **Architecture > Prompt** — rather than telling each developer how to audit dependencies, you create a command that encodes the process.

---

## Practical Command Ideas

| Command | Purpose | Arguments? |
|---------|---------|-----------|
| `/audit` | Check dependencies for vulnerabilities, update, run tests | No |
| `/write_tests` | Generate tests for a specific file or module | Yes — file path or description |
| `/review` | Review code changes for common issues | Yes — file path or PR number |
| `/doc` | Generate documentation for a module | Yes — module name |
| `/migrate` | Create a database migration for a schema change | Yes — description of change |
| `/refactor` | Refactor a file following project conventions | Yes — file path |

---

## Analogies for Engineers

| Concept | Analogy |
|---------|---------|
| Custom commands | Shell aliases or Makefile targets — shortcuts for common workflows |
| `.claude/commands/` directory | `.github/workflows/` — project-level automation config |
| `$ARGUMENTS` | `$1` in bash scripts — positional parameter substitution |
| Project-scoped commands | ESLint config committed to repo — team-wide conventions |
| Restarting Claude Code after adding | `source ~/.zshrc` — reload config to pick up changes |

---

## Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|-------------|---------|-----------------|
| Putting complex logic in commands | Commands are prompts, not scripts — Claude may interpret ambiguously | Keep commands focused; use hooks for deterministic logic |
| Not committing commands to the repo | Team members do not benefit from shared workflows | Store in `.claude/commands/` and commit |
| Hardcoding file paths in commands | Breaks when project structure changes | Use `$ARGUMENTS` for dynamic paths |
| Creating commands for one-off tasks | Adds clutter without reuse value | Commands are for **repeatable** workflows |
| Forgetting to restart Claude Code | New commands are not loaded until restart | Always restart after adding/modifying commands |

---

## Exam Focus: Commands vs Hooks vs CLAUDE.md

This is a frequently tested distinction in D3:

| Mechanism | What It Does | When to Use |
|-----------|-------------|-------------|
| **Custom Commands** | Reusable prompt templates triggered by `/name` | Repeatable workflows (audit, test, review) |
| **CLAUDE.md** | Always-loaded project instructions | Persistent conventions (coding style, project structure) |
| **Hooks** | Programmatic middleware on tool execution | Deterministic enforcement (block writes, auto-format) |
| **Memories** | Personal persistent notes | Individual preferences and corrections |

> 💡 **Decision rule**
>
> - "Every time I do X, I type the same long prompt" → **Custom command**
> - "Claude should always know Y about this project" → **CLAUDE.md**
> - "Z must never happen / must always happen" → **Hook**
> - "Claude keeps getting W wrong for me personally" → **Memory**

Core exam philosophy: **Architecture > Prompt** — custom commands codify team workflows into the project structure, making them discoverable, versionable, and consistent.

---

## Practice Questions

### Q1: Code Generation Scenario

Your team frequently asks Claude Code to generate API endpoint boilerplate. Each developer types a slightly different prompt, leading to inconsistent code patterns. What is the best way to standardize this workflow?

- A. Add boilerplate instructions to CLAUDE.md
- B. Create a custom command in `.claude/commands/endpoint.md` with `$ARGUMENTS` for the endpoint name
- C. Create a PreToolUse hook that enforces boilerplate structure
- D. Share a text file with the recommended prompt for all developers to copy-paste

<details><summary>Answer</summary>

**B** — A custom command standardizes the prompt across the team while allowing dynamic input via `$ARGUMENTS`. Since it lives in `.claude/commands/`, it is committed to the repo and available to all team members.

- A would work for always-on conventions but is too heavy for an on-demand workflow
- C is for deterministic enforcement, not prompt templating
- D is manual and error-prone — developers will modify it over time

Exam philosophy: **Architecture > Prompt** — encode the workflow in project structure, not in tribal knowledge.
</details>

### Q2: Developer Productivity Scenario

You created a new custom command file at `.claude/commands/lint_fix.md`, but when you type `/lint_fix` in Claude Code, the command does not appear. What is the most likely cause?

- A. The file must be named `lint-fix.md` with a hyphen instead of underscore
- B. You need to restart Claude Code to load new commands
- C. Custom commands only work with `$ARGUMENTS`
- D. The file must be in `~/.claude/commands/` instead

<details><summary>Answer</summary>

**B** — Custom commands are loaded at startup. After creating or modifying a command file, you must restart Claude Code for it to appear in the command list.

- A is incorrect — underscores work fine in command names
- C is incorrect — `$ARGUMENTS` is optional
- D is incorrect — `.claude/commands/` (project scope) is valid and is the recommended location for team-shared commands

This is a practical knowledge question — the video explicitly mentions the restart requirement.
</details>
