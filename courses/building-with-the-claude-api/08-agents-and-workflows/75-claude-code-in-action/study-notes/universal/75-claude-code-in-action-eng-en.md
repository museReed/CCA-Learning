# Claude Code in Action — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Claude Code Configuration (20%) |
| Task Statements | 3.1 (Claude Code setup & commands), 3.3 (CLAUDE.md memory), 1.2 (agentic workflow patterns) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 75 |

---

## One-Liner

Claude Code's most effective workflow is "context → plan → implement": load relevant files, ask for a plan without code, then request implementation — with `/init` producing a `CLAUDE.md` memory file that persists project context across sessions.

---

## The `/init` Command and CLAUDE.md

When you start a new project, run `/init` first. This triggers Claude Code to:

1. Scan the entire codebase
2. Infer project structure, dependencies, coding style, and architecture
3. Write a summary into a special file named `CLAUDE.md`

`CLAUDE.md` is automatically included as context in every subsequent conversation in that project. It is the persistent memory that makes the agent "remember" your project between sessions.

### Three scopes of CLAUDE.md

| Scope | Purpose | Checked into git? |
|-------|---------|-------------------|
| **Project** | Shared across all engineers on the project | Yes |
| **Local** | Your personal notes for this project | No |
| **User** | Applied across all your projects | No (user-global) |

When running `/init` you can also pass special directions telling Claude what areas to focus on. The generated file typically contains build commands, coding guidelines, and project-specific patterns.

### The `#` shortcut for adding notes

You can append notes to any `CLAUDE.md` without opening the file. Typing:

```
# Always use descriptive variable names
```

…prompts Claude Code to ask which scope (project / local / user) to add the note to, then appends it automatically.

---

## The Canonical Workflow: Context → Plan → Implement

The lesson's central claim is that Claude Code is an "effort multiplier" only when you give it enough context and structure. The recommended three-step workflow:

### Step 1 — Feed context into Claude

Before asking for any code, identify the existing files that show your patterns and ask Claude to read them. This gives the agent examples of your coding style and existing functionality to build on.

```
> Read the math.py and document.py files
```

### Step 2 — Tell Claude to plan a solution (explicitly, no code)

Ask Claude to think through the problem and write a plan. **Say explicitly not to write code yet** — just the approach and steps.

```
> Plan to implement document_path_to_markdown tool:
1. Create a function that:
   - Takes a file path parameter
   - Validates the file exists
   - Determines file type from extension
   - Reads binary data from file
   - Leverages existing binary_document_to_markdown function
   - Returns markdown string
2. Add appropriate documentation
3. Register the tool with MCP server
4. Add tests
```

### Step 3 — Ask Claude to implement the plan

Only after the plan is agreed, ask for the implementation:

```
> Implement the plan
```

Claude will write code based on the shared context and planning work, update relevant files, add tests, and run the suite to verify.

This three-step pattern mirrors the "think then act" principle that the exam tests for agent design — it is not a Claude Code–only idiom, it is the general agent best practice.

---

## Test-Driven Development Workflow

The lesson describes a TDD variant of the workflow that produces more robust code:

1. **Feed context** — same as above
2. **Ask Claude to brainstorm test cases** — what would validate this feature?
3. **Ask Claude to implement the tests** — select the most relevant cases and have Claude write them
4. **Ask Claude to write code that passes the tests** — it will iterate until all tests pass

This works because tests give Claude a concrete success criterion. Instead of "write a function that does X", the agent now has a verifiable goal — green tests — and will iterate until it achieves it.

---

## The Additional Command Set

Beyond the workflow, memorize these commands for the exam:

| Command | What it does |
|---------|--------------|
| `/init` | Scans the codebase and generates `CLAUDE.md` |
| `/clear` | Clears conversation history and resets context |
| `#` | Adds a note to a `CLAUDE.md` (prompts for scope) |

That is the full command surface taught in this lesson. `/init`, `/clear`, and `#` — expect direct recall questions.

---

## Routine Tasks Claude Code Handles

Once in a session, Claude can also handle routine development tasks that would otherwise require switching between editor and terminal:

- Staging and committing changes to git
- Running tests
- Managing dependencies
- Executing ad-hoc shell commands

The design goal: you focus on the bigger picture (what to build, what the spec is) while Claude handles the glue work.

---

## Why Planning Before Coding Works

This section is the "WHY" that goes beyond the source:

- **Attention budget** — asking for a plan first keeps the model's reasoning focused on architecture, not syntax. When it later implements, both the architecture and the syntax get model attention.
- **Error cost** — plans are cheap to revise; code is expensive. Catching a wrong approach at the plan stage is 10x cheaper than rewriting.
- **Human review** — plans are short; code diffs are long. Reviewing a plan takes seconds, reviewing a diff takes minutes.
- **Context anchoring** — a plan agreed on in the conversation becomes a reference the agent returns to when generating code.

This is why the exam treats "context → plan → implement" as the canonical agent workflow, not just a Claude Code tip.

---

## Common Mistakes

1. **Skipping `/init` at the start of a project** — you lose persistent context and the agent re-learns your project every session.
2. **Asking for code before asking for a plan** — removes the cheapest error-correction step.
3. **Forgetting to feed context** — Claude will guess at your conventions and produce code that fights the codebase.
4. **Confusing `#` with Markdown heading syntax** — inside Claude Code, `#` at the start of a message is a memory-append shortcut, not Markdown formatting.
5. **Using `/clear` when you meant `/init`** — `/clear` wipes current conversation, `/init` builds project memory. Opposite effects.

> **Key Insight**
>
> The core workflow — **context → plan → implement** — is the one pattern that unlocks 10x value from Claude Code (and from agents in general). Skipping any step degrades output quality dramatically. The exam may phrase this as "what is the recommended Claude Code workflow" or may present a scenario and ask which step is missing.

---

## CCA Exam Relevance

- **D3 (Claude Code Configuration)**: Direct recall of `/init`, `/clear`, `#`, and `CLAUDE.md` scopes is very likely.
- **D1 (Agentic Coding & Architecture)**: The "context → plan → implement" workflow maps to general agent best practices.
- Expect at least one question about the three CLAUDE.md scopes (project / local / user).
- Expect a question contrasting `/init` vs `/clear` — they are easily confused.

---

## Flashcards

| Front | Back |
|-------|------|
| What does the `/init` command do in Claude Code? | Scans the codebase to understand structure, dependencies, style, and architecture, then writes a summary into a `CLAUDE.md` file |
| What is `CLAUDE.md`? | A memory file automatically included as context in future Claude Code conversations, holding project-specific information |
| What are the three scopes of `CLAUDE.md`? | Project (shared, in git), Local (personal, not in git), and User (across all your projects) |
| What does the `#` command do inside Claude Code? | Adds a note to a `CLAUDE.md` file, prompting you to choose project, local, or user scope |
| What are the three steps of the canonical Claude Code workflow? | 1) Feed context by reading relevant files, 2) Ask for a plan without code, 3) Ask Claude to implement the plan |
| What does `/clear` do? | Clears conversation history and resets context in the current session |
| What is the TDD variant of the Claude Code workflow? | Feed context → ask Claude to brainstorm test cases → implement the tests → write code that passes the tests |
| Why ask for a plan before implementation? | Plans are cheap to revise, easier to review, and keep the model's attention on architecture before syntax — catching mistakes early |
