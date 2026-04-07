# Implementing a Hook — PM Perspective

| Item | Details |
|------|---------|
| Exam Coverage | D3 — Claude Code Configuration & Workflows (20% of exam) |
| Task Statements | 3.2 (custom commands & hooks), 1.5 (Agent SDK hooks) |
| Course Source | claude-code-in-action / 05-hooks / Lesson 16 |

---

## TL;DR


![Implementation Flow](../../visuals/env-guard-flow.svg)
*Figure: .env file guard data flow — PreToolUse intercepts Read calls and blocks access to sensitive files.*

This lesson demonstrates a complete, working hook implementation — from configuration to testing. PMs do not need to write hooks, but understanding the implementation flow helps you write better acceptance criteria, estimate engineering effort, and verify that security requirements are properly enforced.

---

## The Implementation Flow (No Code Required)

| Step | Building Security | Hook Implementation |
|------|------------------|---------------------|
| 1. Register the camera | Add to security panel | Add hook entry in `settings.local.json` |
| 2. Point at the right door | Set camera angle | Set `matcher` to target specific tools |
| 3. Program alert rules | "Alert if someone enters after 10pm" | Write script: "Block if file path contains .env" |
| 4. Test the system | Walk through to verify | Ask Claude to read .env — verify blocked |
| 5. Activate | Turn on system | Restart Claude Code |

> [!TIP]
> **PM Insight**
>
> Hooks require a **restart** to take effect. Deploying a new hook to a team is not instantaneous — factor this into your rollout plan.

---

## What PMs Should Verify

> [!IMPORTANT]
> **Acceptance Criteria Checklist**
>
> 1. **Coverage**: Does the hook cover all relevant tools? (Read AND Grep for file access)
> 2. **Feedback quality**: Does the blocking message explain the policy?
> 3. **Testing**: Both positive (blocked) and negative (allowed) tests pass
> 4. **Settings level**: Compliance hooks in team-shared settings, not personal

---

## The Self-Correcting Feedback Loop

1. Claude tries to read `.env`
2. Hook blocks and sends feedback: "You cannot read the .env file"
3. Claude acknowledges and adjusts — no human intervention needed

This creates **autonomous compliance** — the AI self-corrects without human intervention.

> [!WARNING]
> **PM Risk Alert**
>
> If a security hook is in `settings.local.json`, each developer must configure it individually. For compliance requirements, insist on `settings.json` (team-shared, version-controlled).

---

## Engineering Effort Estimation

| Hook Complexity | Effort | Example |
|----------------|--------|---------|
| Simple file guard | 1-2 hours | Block reading `.env`, `.credentials` |
| Pattern-based blocker | 2-4 hours | Block Bash commands matching a blocklist |
| Conditional logic | 4-8 hours | Block refunds > $500, allow if manager-approved |
| Multi-tool coordination | 1-2 days | Enforce workflow ordering across multiple tools |

---

## Anti-Patterns (Exam Frequently Tested)

| ❌ Wrong Approach | ✅ Correct Approach | Why |
|-------------------|---------------------|-----|
| Assume the hook "just works" after saving | Always restart Claude Code | Hooks load at startup only |
| Accept silent blocking | Require clear error messages | Claude needs feedback to self-correct |
| Put compliance hooks in personal settings | Put compliance hooks in team settings | Personal settings cannot be enforced |
| Test only the blocking case | Test both blocking and allowing | Overly aggressive hooks break workflows |

---

## Practice Questions

### Q1: Customer Support Scenario (S1)

Your team implemented a PreToolUse hook to block refunds over $500. The hook works but the agent says "I encountered an error" instead of explaining policy. What should you recommend?

- A. Add refund policy to system prompt
- B. Improve the hook's stderr message to include the policy explanation
- C. Switch to PostToolUse
- D. Remove the hook for better customer experience

<details><summary>Answer</summary>

**B** — The hook's stderr message is forwarded directly to Claude. A clear policy message helps Claude explain the situation to the customer.

- A: Does not fix the root cause
- C: PostToolUse cannot block
- D: Removing deterministic enforcement creates compliance risk

> [!IMPORTANT]
> **PM Takeaway**: Hook feedback quality directly affects customer experience. Acceptance criteria should include feedback message requirements.
</details>

### Q2: Developer Productivity Scenario (S4)

A PreToolUse hook to block migration file modification was not active on one engineer's machine. The hook was in `settings.local.json` on the team lead's machine only. What is the fix?

- A. Email all engineers to add the hook
- B. Move the hook to `.claude/settings.json` and commit to version control
- C. Add "do not modify migrations" to CLAUDE.md
- D. Configure at global level on all machines

<details><summary>Answer</summary>

**B** — Team-shared hooks belong in `.claude/settings.json` (committed to git).

- A: Manual distribution is error-prone
- C: CLAUDE.md is prompt-based
- D: Requires manual setup per machine

> [!IMPORTANT]
> **PM Takeaway**: Compliance hooks must be in version-controlled, team-shared settings.
</details>

### Q3: Multi-Agent Research Scenario (S3)

A PostToolUse hook validates data after API calls. The hook works but Claude does not use the validated data. What is the issue?

- A. Should be PreToolUse
- B. Feedback is written to stdout instead of stderr
- C. Matcher is wrong
- D. Context window too small

<details><summary>Answer</summary>

**B** — PostToolUse feedback must go to stderr to be included in Claude's context. stdout is not captured.

- A: PreToolUse runs before data exists
- C: Hook is running correctly, so matcher is fine
- D: Hook feedback is small

> [!IMPORTANT]
> **PM Takeaway**: Verify that hook output goes to stderr. This is a common silent failure.
</details>
