# Gotchas Around Hooks — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Claude Code Configuration & Workflows (20%) |
| Task Statements | 3.2 (custom commands & hooks), 1.5 (Agent SDK hooks for tool call interception) |
| Source | claude-code-in-action / 05-hooks / Lesson 17 (text-only) |

---

## One-Liner

Hook scripts should use **absolute paths** for security (preventing path interception and binary planting attacks), but absolute paths break portability — solve this with a `settings.example.json` + init script pattern that replaces `$PWD` placeholders with machine-specific absolute paths.

---

## Context: The Security-Portability Trade-Off

You know how to define and implement hooks (Lessons 15-16). This lesson addresses a real-world deployment problem: the tension between security best practices (absolute paths) and team collaboration (sharing settings files).

> [!TIP]
> **iOS/Swift analogy**
>
> This is like the tension between hardcoding a certificate pinning hash (secure but breaks when the cert rotates) vs. loading it from a config (flexible but requires a secure distribution mechanism). The solution is an automated setup step.

---

## The Core Problem

### Why Absolute Paths?

```json
// ❌ Relative path (security risk)
"command": "node ./hooks/read_hook.js"

// ✅ Absolute path (secure)
"command": "node /Users/alice/projects/queries/hooks/read_hook.js"
```

Absolute paths mitigate two attack vectors:

| Attack | Description | How Absolute Paths Help |
|--------|-------------|------------------------|
| **Path interception** ([MITRE T1574.007](https://attack.mitre.org/techniques/T1574/007/)) | Attacker places a malicious script in a directory that appears earlier in `$PATH` | Absolute path bypasses `$PATH` resolution entirely |
| **Binary planting** ([OWASP](https://owasp.org/www-community/attacks/Binary_planting)) | Attacker places a malicious file with the same name in the working directory | Absolute path points to the exact file |

> [!CAUTION]
> **Security is non-negotiable**
>
> The CCA exam treats security best practices as the correct answer. If a question asks about hook command paths, absolute paths are always preferred.

### Why This Breaks Portability

Absolute paths are machine-specific:

```
Alice's machine: /Users/alice/projects/queries/hooks/read_hook.js
Bob's machine:   /home/bob/dev/queries/hooks/read_hook.js
CI server:       /workspace/queries/hooks/read_hook.js
```

---

## The Solution: Template + Init Script


![Template Init Pattern](../../visuals/template-init-pattern.svg)
*Figure: Template → Init → Local pattern — committed template with $PWD placeholders, one-time init generates machine-specific config.*

### 1. `settings.example.json` (committed to git)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read|Grep",
        "hooks": [
          {
            "type": "command",
            "command": "node $PWD/hooks/read_hook.js"
          }
        ]
      }
    ]
  }
}
```

### 2. `scripts/init-claude.js` (committed to git)

Reads template → replaces `$PWD` → writes `settings.local.json`

### 3. `settings.local.json` (gitignored, generated)

Machine-specific absolute paths. **Never committed**.

> [!NOTE]
> **Why this matters for teams**
>
> This pattern ensures: Security (absolute paths) + Portability (template works on any machine) + Automation (no manual path editing) + Version control (template tracked; generated file not)

---

## Two Settings Files Explained

| File | Purpose | In Git? |
|------|---------|---------|
| `settings.json` | Team-shared settings | Yes |
| `settings.local.json` | Generated file with machine-specific absolute paths | No (gitignored) |

---

## Anti-Patterns (Exam Frequently Tested)

| ❌ Wrong Approach | ✅ Correct Approach | Why |
|-------------------|---------------------|-----|
| Use relative paths in hook commands | Use absolute paths | Relative paths are vulnerable to path interception and binary planting |
| Commit `settings.local.json` with absolute paths | Commit `settings.example.json` with `$PWD` placeholders | Absolute paths are machine-specific |
| Manually edit paths for each developer | Use an init script to auto-generate | Manual editing is error-prone |
| Skip the security recommendation | Always use absolute paths | CCA exam expects security best practices |

---

## Practice Questions

### Q1: Developer Productivity Scenario (S4)

Your team wants to share a PreToolUse hook configuration across all developers. The hook script is in the project's `hooks/` directory. What is the recommended approach?

- A. Commit `settings.local.json` with relative paths
- B. Commit `settings.json` with absolute paths
- C. Commit a `settings.example.json` with `$PWD` placeholders and an init script that generates `settings.local.json`
- D. Have each developer manually create their own `settings.local.json`

<details><summary>Answer</summary>

**C** — Provides both security (absolute paths) and portability (template works on any machine).

- A: Relative paths are a security risk
- B: Absolute paths in shared settings break on other machines
- D: Manual setup is error-prone

> [!IMPORTANT]
> Key principle: Template + init script = security + portability
</details>

### Q2: CI/CD Integration Scenario (S5)

Your CI pipeline uses hooks with relative paths. A security audit flags this. The CI runs on different runners with different workspace directories. What is the correct fix?

- A. Add hooks directory to the CI runner's `$PATH`
- B. Use a setup step that generates `settings.local.json` with absolute paths based on the runner's workspace
- C. Disable hooks in CI
- D. Hardcode a common CI workspace path in `settings.json`

<details><summary>Answer</summary>

**B** — The setup step mirrors the init script pattern for CI environments.

- A: Does not fix the relative script path vulnerability
- C: Hooks may be needed for compliance
- D: Dynamic runners have different paths

> [!IMPORTANT]
> CI/CD environments need the same security posture as developer machines.
</details>

### Q3: Code Generation Scenario (S2)

A new developer clones the project. Hooks are not working. They see `settings.example.json` but no `settings.local.json`. What is the cause and fix?

- A. Hooks feature is disabled by default
- B. They need to run the setup script (`npm run setup`) to generate `settings.local.json`
- C. They need to copy `settings.example.json` to `settings.json`
- D. Hooks are not supported on their OS

<details><summary>Answer</summary>

**B** — `settings.local.json` is gitignored and must be generated by the init script.

- A: Hooks are available by default
- C: Copying without replacing `$PWD` leaves broken placeholders
- D: Hooks are platform-independent
</details>
