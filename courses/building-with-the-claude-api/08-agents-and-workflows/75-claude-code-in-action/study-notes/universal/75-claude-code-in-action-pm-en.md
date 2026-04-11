# Claude Code in Action — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Claude Code Configuration (20%) |
| Task Statements | 3.1 (Claude Code commands), 3.3 (CLAUDE.md memory), 1.2 (agentic workflow patterns) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 75 |

---

## One-Liner

Claude Code unlocks real value only when teams adopt the "context → plan → implement" workflow and commit a shared `CLAUDE.md` — these are product/process decisions the PM must champion, not engineering choices to leave to developers.

---

## Mental Model: The New Teammate's First Day

Think of onboarding Claude Code to a project like onboarding a new engineer:

| Onboarding step | Human engineer | Claude Code |
|-----------------|----------------|-------------|
| Tour of the codebase | Reads README + asks questions | `/init` scans and writes `CLAUDE.md` |
| Team conventions cheat sheet | Written in the wiki | `CLAUDE.md` (project scope) |
| Personal notes and preferences | Kept in a notebook | `CLAUDE.md` (local scope) |
| Universal working style | Shaped by career | `CLAUDE.md` (user scope) |
| How we work | "First plan, then code" | Context → plan → implement workflow |

A new engineer with no context writes mediocre code for weeks. So does Claude Code without `CLAUDE.md`. The memory file is not an optional feature — it is the onboarding document.

---

## Why This Lesson Matters for PMs

Most teams install Claude Code and then use it wrong — they treat it as autocomplete instead of an agent. This lesson is the product's workflow contract: follow it and you get 10x value, skip it and you get a glorified search-and-replace.

The PM's job:

1. **Make `/init` + `CLAUDE.md` a team policy** — not a suggestion.
2. **Codify the three-step workflow in team documentation** — context → plan → implement.
3. **Define what belongs in project-scope CLAUDE.md** — not every preference, only the shared ones.
4. **Treat the CLAUDE.md as a product artifact** — review it like a spec, update it like a spec.

---

## Product Use Cases

### Where Claude Code shines with the right workflow

| Scenario | Why it fits |
|----------|-------------|
| Adding a new feature on top of an existing codebase | Context-first workflow prevents the agent from reinventing your patterns |
| Refactoring with tests already in place | TDD variant shines — tests are the success criterion |
| New engineer ramping up on a legacy project | `CLAUDE.md` captures the tribal knowledge they need |
| Cross-team boundary work | Project `CLAUDE.md` carries conventions across contributors |

### When Claude Code alone is not enough

| Scenario | What to pair it with |
|----------|----------------------|
| Needs runtime data from prod | Add MCP server (lesson 76) |
| Needs UI design decisions | Product spec still required |
| Needs compliance approval | Human review in the loop |
| Needs cross-repo knowledge | `CLAUDE.md` at user scope + discipline |

---

## The Three Scopes of CLAUDE.md (PM Framing)

This is the most product-relevant concept in the lesson:

| Scope | Owner | What it should contain | What it should NOT contain |
|-------|-------|------------------------|----------------------------|
| **Project** | Team lead / PM | Build commands, team conventions, architectural rules | Personal shortcuts, machine-specific settings |
| **Local** | Individual engineer | Personal shortcuts, working notes, experimental flags | Team-wide conventions, rules others need |
| **User** | Individual engineer | Universal working style ("always explain before editing") | Project-specific patterns |

A PM should treat project-scope `CLAUDE.md` as a first-class deliverable — review it in code review, update it on every significant architectural change, and reference it in PR descriptions.

---

## PM Decision Framework

When rolling out Claude Code to a team, answer:

1. **Who owns the project `CLAUDE.md`?** Someone must curate it. Usually the tech lead or PM.
2. **What belongs in it?** Start with build commands, code style, testing requirements, and architecture overview.
3. **How do we review changes to `CLAUDE.md`?** In the same PR as the code that caused the change.
4. **How do we enforce the "plan first" workflow?** Team agreements, PR templates, or internal tooling.
5. **What do we measure?** Time-to-first-working-PR for new engineers; share of PRs with "Plan:" sections.

---

## The Workflow as a Product Standard

The "context → plan → implement" pattern is not a Claude Code quirk — it is the modern agent UX pattern. Other agent tools (Cursor, Windsurf, bespoke products) all converge on this same shape. As a PM:

| Workflow step | Product artifact you can request |
|---------------|----------------------------------|
| Context | File list, relevant docs, past PRs |
| Plan | Written plan posted in the PR before any code |
| Implement | The actual PR |

If you standardize on this, code review gets faster, onboarding gets cheaper, and the quality floor rises — all while using fewer senior engineering hours.

---

## Common PM Mistakes

1. **Treating `CLAUDE.md` as optional** — without it, every new session relearns the project. You lose the compounding advantage.
2. **Letting engineers put everything in user-scope** — shared conventions must live in project scope or they do not benefit the team.
3. **Skipping the plan step to "save time"** — you save minutes and lose hours fixing misdirected implementations.
4. **Not including `CLAUDE.md` in your code review checklist** — it is living documentation; stale entries cause bad output.
5. **Confusing `/clear` with `/init`** — this is the classic tutorial mistake. Document both so your team knows which to use when.

> **Key Insight**
>
> Claude Code is a **team protocol**, not just a developer tool. The PM's real deliverable is not "we installed it" — it is "we have a shared `CLAUDE.md`, we follow context → plan → implement, and we review changes to our agent memory like we review code." Teams that do this get the agent advantage. Teams that do not, do not.

---

## CCA Exam Relevance

- **D3 (Claude Code Configuration)**: Direct questions on `/init`, `/clear`, `#`, and `CLAUDE.md` scopes are very likely.
- **D1 (Agentic Coding & Architecture)**: The context → plan → implement workflow is the canonical agent pattern.
- Expect scenario questions like "a team installed Claude Code but reports low productivity — what is missing?" — the answer is usually `CLAUDE.md` + the workflow.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the canonical three-step Claude Code workflow PMs should enforce? | 1) Feed context by reading relevant files, 2) Ask for a written plan with no code, 3) Ask Claude to implement the plan |
| What are the three scopes of `CLAUDE.md` and who owns each? | Project (team/PM-owned, checked into git), Local (individual engineer, not in git), User (individual engineer, applies across all their projects) |
| Why should a PM treat project-scope `CLAUDE.md` as a first-class deliverable? | It is the onboarding document, style guide, and architecture summary that every future Claude Code session inherits — stale content produces bad output |
| What does `/init` do and when should a team run it? | It scans the codebase, writes a summary to `CLAUDE.md`, and should be run at project start and revisited after big architectural changes |
| What does the `#` shortcut do? | Appends a note to a `CLAUDE.md` file and prompts you to choose project, local, or user scope |
| What is the TDD variant of the Claude Code workflow? | Feed context → ask Claude to brainstorm test cases → implement the tests → write code until the tests pass |
| What is the #1 PM mistake when rolling out Claude Code? | Treating `CLAUDE.md` as optional — this eliminates the compounding advantage of persistent project memory |
| What metric shows whether the team is following the "plan first" rule? | Share of PRs that include a written plan (in description or attached comment) before the code diff |
