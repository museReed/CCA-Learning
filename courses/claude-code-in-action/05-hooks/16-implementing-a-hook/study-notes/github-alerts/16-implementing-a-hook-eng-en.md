# Implementing a Hook — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Claude Code Configuration & Workflows (20%) |
| Task Statements | 3.2 (custom commands & hooks), 1.5 (Agent SDK hooks for tool call interception) |
| Source | claude-code-in-action / 05-hooks / Lesson 16 |

---

## One-Liner

Implementing a hook means wiring up the configuration in `settings.local.json` (matcher + command) and writing the script that reads stdin JSON, inspects `tool_input`, and exits with code 0 (allow) or 2 (block + stderr feedback).

---

## Context: From Theory to Practice

Lesson 15 taught you the four-step framework for *defining* a hook. This lesson walks through a complete, working implementation — a PreToolUse hook that prevents Claude from reading `.env` files.

> [!TIP]
> **iOS/Swift analogy**
>
> This is like going from understanding `URLProtocol` conceptually to actually subclassing it, registering it, and seeing your interceptor fire in the Xcode debugger.

---

## Step-by-Step Implementation

### 1. Configure `settings.local.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read|Grep",
        "hooks": [
          {
            "type": "command",
            "command": "node ./hooks/read_hook.js"
          }
        ]
      }
    ]
  }
}
```

> [!NOTE]
> **Why `settings.local.json`?**
>
> This file is gitignored — it is for your personal settings. Use `.claude/settings.json` (no `.local`) for team-shared hooks that should be committed to version control.

### 2. Write the Hook Script

```javascript
async function main() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }

  const toolArgs = JSON.parse(Buffer.concat(chunks).toString());

  const readPath =
    toolArgs.tool_input?.file_path || toolArgs.tool_input?.path || "";

  if (readPath.includes('.env')) {
    console.error("You cannot read the .env file");
    process.exit(2);
  }
}

main();
```

> [!WARNING]
> **Critical implementation details**
>
> 1. **Read from stdin, not argv** — Tool call data comes via standard input
> 2. **Use `console.error()`, not `console.log()`** — Feedback must go to stderr
> 3. **Check both `file_path` and `path`** — Different tools may use different field names
> 4. **Exit code 2, not 1** — Code 2 specifically signals "block this tool call"

### 3. Restart and Test

1. **Restart Claude Code** — Hook changes only take effect after restart
2. **Test with Read**: Ask Claude to read `.env` — should be blocked
3. **Test with Grep**: Ask Claude to grep `.env` — should also be blocked
4. **Test with allowed files**: Ask Claude to read other files — should work normally

> [!NOTE]
> **Instructor insight from the video**
>
> Claude recognizes the hook feedback in its response: "I was prevented by a read hook from accessing that file." This demonstrates the self-correcting feedback loop.

---

## Common Implementation Mistakes

| ❌ Mistake | ✅ Fix | Why |
|-----------|--------|-----|
| Use `console.log()` for feedback | Use `console.error()` | Only stderr is sent to Claude on exit code 2 |
| Exit with code 1 to block | Exit with code 2 | Code 1 = generic error; Code 2 = intentional block |
| Read tool_input.file_path only | Also check tool_input.path | Grep uses `path`, Read uses `file_path` |
| Forget to restart Claude Code | Always restart after hook changes | Hooks are loaded at startup |
| Use `process.argv` for input | Use `process.stdin` | Tool call data is piped via stdin |
| Exact match on `.env` | Use `.includes('.env')` | File path may be absolute |

---

## Anti-Patterns (Exam Frequently Tested)

| ❌ Wrong Approach | ✅ Correct Approach | Why |
|-------------------|---------------------|-----|
| Check tool_name in the script to filter tools | Use matcher in config for tool filtering | Separation of concerns |
| Write hook logic inline in settings.json | Use external script files | Maintainability, testability |
| Silently block without feedback | Always write to stderr when blocking | Claude needs to know *why* |
| Only protect against Read | Protect against Read AND Grep | Both tools can expose file contents |

---

## Practice Questions

### Q1: Developer Productivity Scenario (S4)

You have implemented a PreToolUse hook to prevent Claude from reading `.env` files. The hook script uses `console.log("Access denied")` and `process.exit(2)`. Claude successfully blocks the read but does not display the "Access denied" message. What is the issue?

- A. The exit code should be 1, not 2
- B. The feedback must be written to stderr (`console.error()`), not stdout (`console.log()`)
- C. The matcher should include `Write` in addition to `Read`
- D. The hook needs to return a JSON response instead of a plain text message

<details><summary>Answer</summary>

**B** — When a hook exits with code 2, only stderr output is forwarded to Claude as feedback.

- A: Code 1 is a generic error, not a blocking signal
- C: Write is irrelevant to read access feedback
- D: Plain text to stderr is the correct mechanism

> [!IMPORTANT]
> Key principle: stderr = Claude feedback; stdout = ignored on exit code 2
</details>

### Q2: CI/CD Integration Scenario (S5)

Your team wants to implement a hook that checks whether Claude is executing potentially dangerous Bash commands (like `rm -rf`). Which implementation approach is correct?

- A. PostToolUse hook that reverts dangerous command results after execution
- B. PreToolUse hook with matcher `Bash` that reads stdin JSON, inspects `tool_input.command`, and exits with code 2 if the command matches a blocklist
- C. PreToolUse hook with matcher `.*` that blocks all tool calls containing "rm"
- D. Add "never run rm -rf" to the system prompt

<details><summary>Answer</summary>

**B** — PreToolUse is needed to block before execution. The matcher targets `Bash` specifically. The script inspects `tool_input.command` and applies a blocklist check.

- A: PostToolUse is too late
- C: `.*` is too broad
- D: Prompt-based with non-zero failure rate

> [!IMPORTANT]
> Exam philosophy: **Deterministic > Probabilistic**
</details>

### Q3: Customer Support Agent Scenario (S1)

You are implementing a PreToolUse hook that must block the `process_refund` tool when the refund amount exceeds $500. During testing, the hook allows refunds of $600. What is the most likely cause?

- A. The exit code should be 1 instead of 2
- B. The script is checking `tool_input.refund_amount` instead of the actual field name used by the tool
- C. PostToolUse hooks should be used instead of PreToolUse
- D. The matcher should be `.*` to catch all tool calls

<details><summary>Answer</summary>

**B** — The most common implementation bug is mismatching field names in `tool_input`. Each tool defines its own input schema.

- A: Exit code 2 is correct for blocking
- C: PostToolUse cannot block
- D: The matcher should target the specific tool

> [!IMPORTANT]
> Exam philosophy: **Architecture > Prompt** — implementation correctness matters
</details>
