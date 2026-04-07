# Controlling Context — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D5 — Reliability & Performance (15%), D3 — Claude Code Configuration & Workflows (20%) |
| Task Statements | 5.1 ★★★ (context preservation), 5.4 ★★ (large codebase context), 3.5 ★★ (iterative refinement) |
| Source | claude-code-in-action / 03-context-and-commands / Lesson 10 |

---

## One-Liner

Context is a finite resource — Escape interrupts mid-generation, double-Escape rewinds conversation history, `/compact` summarizes to preserve learned knowledge, and `/clear` resets for a fresh start. Choosing the right tool at the right time keeps Claude focused and token-efficient.

---

## Why Context Management Matters

Claude Code operates within a fixed-size **context window**. Every message you send, every file Claude reads, every error it debugs — all of it consumes tokens from that window. When the window fills up, Claude loses access to earlier information, leading to:

- **Repeated mistakes** — Claude forgets corrections it already received
- **Drifting focus** — irrelevant debugging history distracts from the current task
- **Token waste** — paying for context that adds noise, not signal

Managing context is not just about convenience — it directly affects output quality.

---

## The Four Context Control Tools


![Context Control Tools Decision Tree](../../visuals/context-control-tools-decision-tree.svg)
*Figure: Decision tree for choosing context control tools.*

### 1. Escape (Single Press) — Interrupt

Stops Claude mid-generation. Use when:
- Claude is heading in the wrong direction
- You want to redirect before it wastes tokens on a bad approach
- You need to provide additional guidance before Claude finishes

> [!TIP]
> **Escape + Memory = Permanent Fix**
>
> When Claude makes a recurring mistake (e.g., trying to read a config file that does not exist), press Escape immediately, then use the `#` shortcut to save a memory about the correct behavior. This prevents the same mistake from recurring in future sessions — not just the current conversation.

### 2. Double-Escape — Rewind Conversation

Press Escape twice to see your full message history and jump back to any previous point. This **discards all messages after the selected point**, effectively rewinding the conversation.

Best used when:
- A debugging detour polluted the context with irrelevant back-and-forth
- You want to retry a task from a known-good state
- Claude successfully completed Task A, hit issues on Task B, and you want to go back to right after Task A

> [!NOTE]
> **Instructor insight from the video**
>
> The instructor demonstrates writing tests for four functions in `auth.ts`. After debugging a missing package issue for `createSession` tests, they rewind to before the debugging detour and update the prompt to "write tests for getSession." This preserves the useful context (Claude already read `auth.ts`) while dropping the noise (package debugging history).

### 3. `/compact` — Summarize and Continue

Compresses the entire conversation into a summary, then continues from that summary. The key distinction: Claude **retains learned knowledge** but in a condensed form.

Best used when:
- Claude has built up significant understanding of the codebase during the session
- You are transitioning between related subtasks (e.g., testing function 3 after finishing function 2)
- The context window is getting full but the accumulated knowledge is valuable

### 4. `/clear` — Fresh Start

Wipes the entire conversation history. Claude starts with zero context (except CLAUDE.md and memories).

Best used when:
- You are switching to a completely unrelated task
- The current conversation is so tangled that salvaging context would hurt more than help
- Starting a new coding session on a different feature

---

## Decision Framework: Which Tool When?

| Situation | Tool | Why |
|-----------|------|-----|
| Claude is generating bad output right now | **Escape** | Stop the bleed immediately |
| Claude made the same mistake again | **Escape + Memory** | Fix it permanently |
| Debugging detour polluted context | **Double-Escape** | Rewind to clean state, keep useful earlier context |
| Context is full but knowledge is valuable | **`/compact`** | Compress, do not discard |
| Switching to a completely different task | **`/clear`** | Fresh slate, no baggage |
| Long session, gradually losing coherence | **`/compact`** | Summarize to reclaim window space |

> [!IMPORTANT]
> **Exam note**
>
> The exam tests whether you understand the trade-off between context preservation and context pollution. The key insight: **more context is not always better**. Irrelevant context (debugging noise, failed approaches) actively degrades output quality.

---

## Analogies for Engineers

| Concept | Analogy |
|---------|---------|
| Context window | RAM — finite, shared across all running processes |
| Escape (interrupt) | `Ctrl+C` in terminal — kill the current process |
| Double-Escape (rewind) | `git reset --soft HEAD~3` — undo recent commits, keep the working tree |
| `/compact` | `git squash` — compress multiple commits into one, preserve the net result |
| `/clear` | `git init` in a new directory — start from nothing |
| Context pollution | Memory leaks — each debugging detour leaves residue that degrades performance |

---

## Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|-------------|---------|-----------------|
| Never using `/compact` in long sessions | Context window fills up, Claude forgets early instructions | Compact after completing each logical subtask |
| Using `/clear` when `/compact` would suffice | Throws away valuable learned context | Only `/clear` when switching to unrelated work |
| Letting Claude debug endlessly without interrupting | Wastes tokens, pollutes context with failed attempts | Escape early, provide guidance, rewind if needed |
| Not saving memories for recurring mistakes | Same error appears in every new session | Escape + `#` memory shortcut for permanent fixes |
| Starting a new task without any context management | Previous task's noise interferes with new task | `/compact` (related tasks) or `/clear` (unrelated tasks) |

---

## Exam Focus: Context Window as a Resource


![Context Window As Resource Analogy](../../visuals/context-window-as-resource-analogy.svg)
*Figure: Context window as a finite resource — analogy.*

This maps directly to Task Statement 5.1 (context preservation) and 5.4 (large codebase context):

| Exam Scenario | What They Test |
|--------------|----------------|
| S2 (Code Gen) | Should you compact or clear before generating code for a new module? |
| S4 (Developer Productivity) | How to maintain focus across a multi-step coding session? |

Core exam philosophies at play:
- **Context is a finite resource** — treat it like memory allocation, not an infinite log
- **Signal > Noise** — actively manage what stays in the window
- **Iterative refinement** (Task 3.5) — Escape + redirect is faster than letting Claude finish a bad approach

---

## Practice Questions

### Q1: Code Generation Scenario

You have been pair-programming with Claude Code for 30 minutes. Claude has read your project's database schema, understood your ORM patterns, and successfully implemented three API endpoints. You now need to implement a fourth endpoint that follows the same patterns. However, the context window is nearly full due to debugging output from the second endpoint. What should you do?

- A. Use `/clear` and start fresh with the fourth endpoint
- B. Use `/compact` to summarize the session, then ask for the fourth endpoint
- C. Continue without any context management and hope Claude remembers the patterns
- D. Close Claude Code entirely and start a new session

<details><summary>Answer</summary>

**B** — `/compact` preserves Claude's learned understanding of your schema, ORM patterns, and endpoint conventions while compressing the debugging noise. This is exactly the scenario `/compact` was designed for.

- A throws away 30 minutes of learned context unnecessarily
- C risks Claude losing earlier instructions as the context window overflows
- D is equivalent to A but with extra steps

> [!IMPORTANT]
> Key insight: Claude has **valuable accumulated knowledge** (schema, patterns) — do not discard it. Compress it.

</details>

### Q2: Developer Productivity Scenario

You asked Claude to refactor a utility file, but it started modifying the wrong file. Claude has already read the correct file earlier in the conversation. What is the fastest way to get back on track?

- A. Use `/clear` and start over
- B. Press Escape once to interrupt, then re-specify the correct file
- C. Let Claude finish, then ask it to undo its changes
- D. Press Escape twice to rewind to before the incorrect refactoring began

<details><summary>Answer</summary>

**D** — Double-Escape rewinds to the point before the mistake, preserving the earlier context where Claude read the correct file. You can then update your prompt to be more specific.

- A loses all context including Claude's knowledge of the correct file
- B stops generation but leaves the incorrect output in context, which may confuse subsequent attempts
- C wastes tokens and adds more noise to the context

> [!IMPORTANT]
> Exam philosophy: **Context preservation** — rewind to a clean state rather than layering corrections on top of mistakes.

</details>

### Q3: Iterative Refinement Scenario

Claude keeps trying to import a test helper from `utils/test-helpers.ts`, but in your project the file is actually at `test/helpers.ts`. This is the third time it has made this mistake across different sessions. What is the most effective long-term fix?

- A. Press Escape and tell Claude the correct path each time
- B. Press Escape, then use the `#` shortcut to save a memory about the correct file path
- C. Add the correct path to CLAUDE.md
- D. Both B and C are valid approaches, but B is faster for immediate effect

<details><summary>Answer</summary>

**D** — Both memories (B) and CLAUDE.md (C) can solve this, but the video specifically demonstrates the Escape + `#` memory pattern as the quick fix for recurring mistakes. CLAUDE.md is a heavier-weight solution that requires a file edit and is better for team-wide conventions.

- A is a temporary fix that does not persist across sessions
- B provides immediate, permanent personal-level correction
- C works but is overkill for a single file path correction and affects the whole team

> [!IMPORTANT]
> Exam philosophy: **Iterative refinement** — fix recurring errors at the right level of persistence.

</details>
