# Useful Hooks — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Claude Code Configuration & Workflows (20%), D1 — Agentic Architecture (27%) |
| Task Statements | 1.5 (Agent SDK hooks for tool call interception & data normalization), 3.2 (custom commands & hooks), 1.2 (multi-agent coordinator-subagent patterns) |
| Source | claude-code-in-action / 05-hooks / Lesson 18 |

---

## One-Liner

PostToolUse hooks can run compiler/linter checks after every edit (type-checking hook) or launch a separate Claude Code instance to review changes for code duplication (query deduplication hook) — both creating **self-correcting feedback loops** without human intervention.

---

## The Problem: Claude Breaks Things It Cannot See

When Claude modifies a function signature, it updates the definition file but often misses call sites in other files. This is analogous to an iOS developer changing a protocol method signature in one file — if you don't have the compiler checking all conformances, broken call sites slip through.

In a TypeScript project:
1. `schema.ts` defines `createSchema()`
2. `main.ts` calls `createSchema()`
3. You ask Claude to add a `verbose: boolean` parameter to `createSchema()`
4. Claude updates `schema.ts` but **does not update `main.ts`**
5. Result: type error at the call site that Claude never catches

> [!NOTE]
> **Instructor insight from the video**
>
> The instructor demonstrates this exact scenario live — Claude successfully edits the function definition but leaves `main.ts` broken. The key insight: Claude doesn't automatically run the TypeScript compiler, so it has no signal that something is wrong elsewhere in the project.

---

## Hook 1: TypeScript Type-Checking Hook

### How It Works

A PostToolUse hook that runs `tsc --noEmit` after every file edit:

```json
"PostToolUse": [
  {
    "matcher": "Write|Edit|MultiEdit",
    "hooks": [
      {
        "type": "command",
        "command": "node hooks/tsc.js"
      }
    ]
  }
]
```

The hook script:
1. Runs `tsc --noEmit` (type check without generating output files)
2. Captures any compiler errors
3. If errors exist, exits with code 2 and outputs the errors
4. Claude receives the errors as feedback and fixes them on the next turn

> [!TIP]
> **Engineering analogy**
>
> This is identical to how Xcode's build system works — after you edit a `.swift` file, the compiler incrementally checks all dependent files. The hook replicates this compiler feedback loop for Claude Code.

### Extending to Other Languages

| Language | Hook Command | What It Checks |
|----------|-------------|----------------|
| TypeScript | `tsc --noEmit` | Type errors across the project |
| Python | `mypy .` or `pyright` | Type annotation violations |
| Rust | `cargo check` | Borrow checker + type errors |
| Go | `go vet ./...` | Static analysis issues |
| Untyped JS/Python | `npm test` or `pytest` | Run tests as a proxy for type checking |

> [!WARNING]
> **Performance consideration**
>
> The TypeScript hook is relatively lightweight — `tsc --noEmit` on a medium project takes 2-5 seconds. For large projects, consider scoping the check to changed files only.

---

## The Second Problem: Code Duplication in Large Projects

When Claude receives a complex, multi-step task (e.g., "build a Slack integration that alerts about pending orders"), it may lose focus on existing code and write duplicate functionality.

### The Scenario

- `src/queries/orderQueries.ts` already has `getPendingOrders()`
- You ask Claude: "Create a Slack integration that alerts about orders pending longer than 3 days"
- **Focused task**: Claude finds and reuses `getPendingOrders()` — correct
- **Complex task** (after `/clear`): Claude writes a brand new `getOrdersPendingTooLong()` query — duplicate code

> [!NOTE]
> **Instructor insight from the video**
>
> The instructor shows that when the task is simple and focused ("print out pending orders"), Claude reuses the existing query. But when the same requirement is buried inside a larger task (Slack integration), Claude creates a duplicate. The context window and task complexity directly affect Claude's ability to discover existing code.

---

## Hook 2: Query Duplication Prevention Hook

### Architecture

This hook uses a **multi-agent review pattern** — one Claude instance reviews another's work:

```
Claude (primary) writes to queries/ directory
    ↓
PostToolUse hook triggers
    ↓
Hook launches a SECOND Claude Code instance (via TypeScript SDK)
    ↓
Second instance reviews the change against existing queries
    ↓
If duplicate found: exit code 2 + feedback → primary Claude removes duplicate
If no duplicate: exit code 0 → primary Claude continues
```

### Configuration

```json
"PostToolUse": [
  {
    "matcher": "Write|Edit|MultiEdit",
    "hooks": [
      {
        "type": "command",
        "command": "node hooks/query-hook.js"
      }
    ]
  }
]
```

The hook script:
1. Checks if the changed file is in the `./queries` directory (early exit if not)
2. Constructs a prompt asking Claude to review the change for duplicates
3. Launches a separate Claude Code instance using the **TypeScript SDK** (`@anthropic-ai/claude-code` package)
4. Parses the response — if duplicates found, exits with code 2 and feedback message
5. Primary Claude receives the feedback and refactors to use the existing query

> [!TIP]
> **This is a multi-agent pattern inside a hook**
>
> The query hook is essentially a coordinator-subagent pattern (Task Statement 1.2) embedded within the hook system (Task Statement 1.5). The "reviewer" subagent has a scoped context — it only looks at the queries directory, not the entire project. This aligns with the exam philosophy: **Scoped context > Full history**.

### Trade-offs

| Benefit | Cost |
|---------|------|
| Cleaner codebase, less duplication | Additional time per edit (~10-30 seconds) |
| Consistent query organization | Additional API usage (second Claude instance) |
| Catches duplicates Claude would miss | Only practical for critical directories |

> [!WARNING]
> **Best practice: Scope your monitoring**
>
> The instructor explicitly recommends watching only "a handful of directories, like really important folders inside of your project, just to minimize the amount of extra work that is being done."

---

## Anti-Patterns (Exam Favorites)

| ❌ Wrong Approach | ✅ Correct Approach | Why |
|-------------------|---------------------|-----|
| Add "always run type checker" to system prompt | PostToolUse hook running `tsc --noEmit` | Prompt is probabilistic; hook is deterministic |
| Ask Claude to "check for duplicate code before writing" | PostToolUse hook with separate reviewer instance | Claude loses focus in complex tasks — demonstrated in the video |
| Monitor ALL directories with the duplication hook | Scope to critical directories only | Performance cost outweighs benefit for non-critical directories |
| Use PreToolUse to block duplicate writes | Use PostToolUse to review and provide feedback | You need to see what was written to determine if it's a duplicate |
| Rely on Claude to always find existing code | Automated review as a safety net | Claude's ability to find existing code degrades with task complexity |

---

## CCA Exam Connection

> [!IMPORTANT]
> **Exam scenarios where these concepts appear**
>
> - **S2 (Code Generation)**: TypeScript type-checking hook = ensuring code quality in generated code
> - **S4 (Developer Productivity)**: Both hooks improve developer workflow by catching issues automatically
> - **S5 (CI/CD)**: Hooks in CI pipelines for automated quality gates
>
> **Common exam pattern**: "Claude modified a function but broke call sites elsewhere. What is the best approach?"
> Answer direction: PostToolUse hook running the compiler/type checker — Architecture > Prompt.

---

## Practice Questions

### Q1: Code Generation Scenario

Your team uses Claude Code for a TypeScript project with 200+ files. Engineers report that when Claude modifies function signatures, it frequently breaks call sites in other files. What is the most effective solution?

- A. Add instructions to CLAUDE.md: "After modifying any function signature, search for and update all call sites"
- B. Configure a PostToolUse hook that runs `tsc --noEmit` after every file edit and feeds type errors back to Claude
- C. Switch to using the `--resume` flag so Claude maintains context of all files it has seen
- D. Implement a PreToolUse hook that prevents Claude from modifying function signatures

<details><summary>Answer</summary>

**B** — A PostToolUse hook running the TypeScript compiler provides deterministic feedback. Claude receives the type errors in its context and fixes them automatically.

- A is prompt-based and has a non-zero failure rate, especially in large projects
- C does not guarantee Claude will remember or re-check all call sites
- D prevents legitimate work — the goal is not to block signature changes, but to catch downstream effects

Exam philosophies: **Architecture > Prompt**, **Deterministic > Probabilistic**
</details>

### Q2: Developer Productivity Scenario

In a large project with many SQL query files, Claude sometimes creates duplicate queries instead of reusing existing ones. This happens most often when the query-related task is part of a larger, multi-step request. What is the best approach?

- A. Add few-shot examples showing Claude how to search for existing queries first
- B. Configure a PostToolUse hook that launches a separate Claude instance to review query changes for duplicates
- C. Consolidate all queries into a single file so Claude can see them all at once
- D. Always use `/clear` before giving Claude a new task to prevent context interference

<details><summary>Answer</summary>

**B** — A separate reviewer instance provides an independent check (exam philosophy: **Independent review > Self-review**). The hook catches duplicates that the primary instance missed due to task complexity.

- A is prompt-based and the video demonstrates this exact failure mode — Claude misses existing code when focused on complex tasks
- C creates a massive file that may exceed Claude's attention capacity and is poor code organization
- D removes useful context and doesn't address the root cause

Exam philosophies: **Architecture > Prompt**, **Independent review > Self-review**, **Scoped context > Full history**
</details>

### Q3: Multi-Agent Architecture Scenario

You are designing a PostToolUse hook that launches a separate Claude Code instance to review changes. What is the most important consideration for the reviewer instance?

- A. Give it the full project context so it can make comprehensive decisions
- B. Scope its context to only the relevant directory and the specific change being reviewed
- C. Have it run in the same session as the primary Claude instance
- D. Configure it as a PreToolUse hook instead so it can block changes before they happen

<details><summary>Answer</summary>

**B** — Scoped context is a core exam principle. The reviewer subagent should only see what it needs — the relevant directory and the change. Full project context (A) wastes tokens and may dilute focus. Same session (C) is not how the hook architecture works — hooks launch separate processes. PreToolUse (D) cannot review a change that hasn't been made yet.

Exam philosophy: **Scoped context > Full history**
</details>
