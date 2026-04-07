# Defining Hooks — PM Perspective

| Item | Details |
|------|---------|
| Exam Coverage | D3 — Claude Code Configuration & Workflows (20% of exam) |
| Task Statements | 3.2 (custom commands & hooks), 1.5 (Agent SDK hooks) |
| Course Source | claude-code-in-action / 05-hooks / Lesson 15 |

---

## TL;DR

Defining a hook follows four steps that mirror setting up a quality checkpoint in a factory: (1) decide whether to inspect *before* or *after* the work is done, (2) choose which production lines to monitor, (3) write the inspection procedure, and (4) decide whether to approve or reject the output. PMs must understand this process to write correct acceptance criteria and communicate with engineers about what can be *guaranteed* vs. what is *best-effort*.

---

## Why PMs Need to Understand Hook Definition

When you write a PRD, you specify requirements. Some requirements *must* be met 100% of the time (compliance, security), while others are *best-effort* (tone, formatting). Understanding the four-step hook definition process helps you:

1. **Specify the enforcement mechanism** — not just "what" but "how"
2. **Estimate engineering effort** — hooks require a script, not just a prompt edit
3. **Set realistic expectations** — hooks are deterministic; prompts are probabilistic

---

## Mental Model: Factory Quality Checkpoint

Think of Claude Code as a factory assembly line. Tools are the machines (drilling, welding, painting). Hooks are the quality checkpoints you install:

| Step | Factory Analogy | Hook Definition |
|------|----------------|-----------------|
| 1. Pre or Post? | Inspect raw materials before drilling, or inspect finished parts after welding? | PreToolUse blocks before action; PostToolUse inspects after action |
| 2. Which line? | Monitor the paint booth and the welding station | `matcher`: `"Read|Grep"` selects which tools |
| 3. Inspection procedure | Quality inspector follows a checklist | Command script reads tool call data (JSON) and applies rules |
| 4. Pass or fail? | Green light (continue) or red light (stop the line) | Exit code 0 (allow) or 2 (block) |

> [!TIP]
> **PM Decision Framework**
>
> When writing acceptance criteria, ask: "Is this a green-light/red-light requirement (hook), or a guideline (prompt)?"
> - **Red light**: "The system MUST prevent reading credentials" → Hook
> - **Guideline**: "The system SHOULD respond in a friendly tone" → Prompt

---

## The Four Steps in Business Terms

### Step 1: Before or After?

| Requirement Type | Hook Type | Business Example |
|-----------------|-----------|-----------------|
| Prevention / Compliance | **PreToolUse** | Block refunds > $500 without manager approval |
| Logging / Quality Check | **PostToolUse** | Log every customer interaction to CRM |
| Auto-correction | **PostToolUse** | Run spell-check after every document edit |

> [!WARNING]
> **Critical for PMs**
>
> If your requirement says "must never" or "must always prevent," specify PreToolUse in your acceptance criteria. PostToolUse cannot prevent — it only reacts after the fact.

### Step 2: Which Operations to Monitor?

The `matcher` field selects which AI tools trigger the checkpoint. Common scenarios:

| PM Requirement | Engineer Translates To |
|---------------|----------------------|
| "Claude must not read credential files" | `matcher: "Read|Grep"` |
| "Auto-format every file Claude writes" | `matcher: "Write|Edit|MultiEdit"` |
| "Log all shell commands" | `matcher: "Bash"` |
| "Monitor everything" | `matcher: ".*"` |

> [!TIP]
> **Common PM Oversight**
>
> PMs often forget that `Grep` (search) can also expose file contents, not just `Read`. Always ask your engineer: "Are there other tools that could access this data?"

### Step 3: The Inspection Logic

The hook command receives detailed information about what Claude is trying to do — not just "Claude wants to read a file" but specifically "Claude wants to read `/src/config/.env` using the Read tool."

This granularity means hooks can make very precise decisions based on file paths, command content, or any other parameter.

### Step 4: The Verdict

| Verdict | Exit Code | What Happens Next |
|---------|-----------|-------------------|
| Approved | 0 | Tool call proceeds normally |
| Rejected | 2 | Tool call is blocked; Claude receives the rejection reason and adjusts |

The rejection feedback creates a self-correcting loop — Claude does not just fail silently; it understands *why* and tries an alternative approach.

---

## Instructor Insights (From the Video)

Key points from the instructor that PMs should note:

1. **Tool discovery is dynamic** — The available tools change when MCP servers are added. Engineers can ask Claude "list your available tools" to discover what can be monitored.
2. **Matcher uses regex-like syntax** — The pipe symbol `|` means OR. This is a technical detail, but PMs should know that one hook can watch multiple tools.
3. **stderr feedback is critical** — When a hook blocks an action, the error message goes directly to Claude. Good error messages help Claude find alternatives; poor messages cause confusion.

---

## Anti-Patterns (Exam Frequently Tested)

| ❌ Wrong Approach | ✅ Correct Approach | Why |
|-------------------|---------------------|-----|
| Write "must prevent X" in PRD without specifying enforcement mechanism | Specify "enforce via PreToolUse hook" in acceptance criteria | Without specification, engineers may use prompt-based solutions |
| Assume PostToolUse can prevent actions | Use PreToolUse for prevention requirements | PostToolUse runs after the action — too late to prevent |
| Monitor only one tool when multiple tools can do the same thing | Ask engineers which tools can access the data | Grep can read file contents just like Read |
| Skip the rejection message | Require clear feedback messages in hook specs | Claude needs feedback to self-correct |

---

## Practice Questions

### Q1: Customer Support Scenario (S1)

You are writing a PRD for an AI customer support agent. One requirement states: "The agent must never access customer payment details stored in the `.credentials` directory." An engineer proposes adding this instruction to the system prompt. What should you recommend?

- A. Accept the engineer's proposal — prompt instructions are sufficient for access control
- B. Request a PreToolUse hook that blocks Read and Grep operations on `.credentials` paths
- C. Request a PostToolUse hook that logs when Claude accesses `.credentials` files
- D. Add the restriction to CLAUDE.md and set it as a team-shared project setting

<details><summary>Answer</summary>

**B** — "Must never access" is a compliance requirement that demands deterministic enforcement. PreToolUse hooks block the action before it occurs. Both Read and Grep must be covered because either tool can expose file contents.

- A is prompt-based with non-zero failure rate — unacceptable for compliance
- C is PostToolUse — too late, the file has already been read
- D is still a prompt-based instruction, not a programmatic enforcement

> [!IMPORTANT]
> **PM Takeaway**: When you write "must never" in a PRD, you are specifying a deterministic requirement. The enforcement mechanism must match — use a hook, not a prompt.

</details>

### Q2: Developer Productivity Scenario (S4)

Your team wants Claude Code to automatically run a code formatter after every file edit. The formatter should not block Claude's work — just clean up formatting. Which step-by-step approach would you specify in the requirements?

- A. PreToolUse hook on Write|Edit that runs the formatter before Claude writes the file
- B. PostToolUse hook on Write|Edit|MultiEdit that runs the formatter after Claude edits, exit code 0
- C. Add "always format your code" to the system prompt
- D. PostToolUse hook on Read that runs the formatter after Claude reads files

<details><summary>Answer</summary>

**B** — Formatting must happen after the file is edited (PostToolUse). The matcher should cover all edit operations (Write, Edit, MultiEdit). Exit code 0 means "proceed normally" — no blocking.

- A runs before the edit — there is nothing to format yet
- C is prompt-based and cannot guarantee consistent formatting
- D targets the wrong tool — Read does not modify files
</details>

### Q3: Code Generation Scenario (S2)

A team uses Claude Code to generate API endpoint code. They want to ensure all generated files follow the project's naming convention (`snake_case`). If a file does not follow the convention, the generation should be blocked. What hook configuration should you request?

- A. PostToolUse hook on Write that checks naming and logs a warning
- B. PreToolUse hook on Write that validates the file name and blocks with exit code 2 if non-compliant
- C. Add naming convention examples to CLAUDE.md
- D. PostToolUse hook on Write that renames the file after creation

<details><summary>Answer</summary>

**B** — "Should be blocked" means prevention, which requires PreToolUse. The hook checks the file name in the tool input before the Write operation executes.

- A is PostToolUse — the file is already written with the wrong name
- C is prompt-based and probabilistic
- D is reactive cleanup — more complex and error-prone than prevention

> [!IMPORTANT]
> **PM Takeaway**: "Block if non-compliant" is the key phrase. Blocking requires PreToolUse. If the requirement said "fix if non-compliant," PostToolUse would be appropriate.

</details>
