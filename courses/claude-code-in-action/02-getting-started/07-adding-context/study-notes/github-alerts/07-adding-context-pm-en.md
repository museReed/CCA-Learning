# Adding Context — PM Perspective

| Item | Details |
|------|---------|
| Exam Coverage | D3 — Effective Claude Code Usage (30%), D5 — Performance Optimization (12%) |
| Task Statements | 3.1 ★★★ (CLAUDE.md hierarchy), 5.1 ★★ (context preservation), 5.4 ★★ (large codebase context) |
| Exam Scenarios | S2 (Code Gen), S4 (Developer Productivity) |
| Course Source | claude-code-in-action / 02-getting-started / Lesson 07 (video + text) |

---

## TL;DR

Claude Code manages project context through a three-tier configuration file system (CLAUDE.md). `/init` generates the initial file by analyzing the codebase. Three levels exist — global (all projects), project (shared via repo), and local (personal overrides). The `@` syntax lets developers point Claude at specific files. For PMs: this is how teams standardize AI-assisted development across an organization, and how context window budget is managed.

---

## Why PMs Must Understand This

1. **Team standardization** — CLAUDE.md committed to source control means every developer gets the same AI behavior. This is your lever for consistent code quality.
2. **Onboarding acceleration** — `/init` + CLAUDE.md means new team members' AI assistant already knows the project architecture from day one.
3. **Performance tuning** — Too much context in CLAUDE.md degrades performance. PMs should understand this trade-off when teams report "Claude is slow."
4. **Security consideration** — CLAUDE.local.md is not committed to source control, making it safe for personal API keys or experimental directives.

---

## Business Analogies

| Concept | Business Analogy |
|---------|-----------------|
| CLAUDE.md hierarchy | Company policy levels: corporate policy (global) < department policy (project) < individual exceptions (local). More specific overrides more general. |
| `/init` command | Employee onboarding — read all documentation, understand the org, summarize key processes |
| `@` file mentions in CLAUDE.md | Standing meeting agenda items — always on the table, always discussed |
| Interactive `@` mentions | Ad-hoc meeting topics — brought up only when relevant |
| `#` memory command | Updating the team wiki — persistent knowledge that survives personnel changes |

---

## Scenario Walkthrough: Rolling Out Claude Code to a 20-Person Team


![Claude Md Hierarchy Priority Stack](../../visuals/claude-md-hierarchy-priority-stack.svg)
*Figure: CLAUDE.md hierarchy — local overrides project overrides global.*

| Phase | Action | CLAUDE.md Lever |
|-------|--------|-----------------|
| 1. Initial setup | Tech lead runs `/init` on the main repo | Generates baseline CLAUDE.md with project architecture |
| 2. Standardize | Tech lead adds coding standards, PR conventions, test requirements to CLAUDE.md | All developers inherit same rules via source control |
| 3. Personalize | Individual developers create CLAUDE.local.md for personal preferences | Personal style without affecting team standards |
| 4. Optimize | Team removes low-value `@` references from CLAUDE.md after monitoring context usage | Better performance, lower token costs |

> [!NOTE] **Instructor insight from the video**
>
> The instructor shows that CLAUDE.md is "included in every request" — making it essentially a persistent system prompt. For PMs, this means the CLAUDE.md is the single most impactful configuration for controlling AI behavior across the team.

---

## Decision Framework: What Goes Where?

| Content Type | Where to Put It | Why |
|-------------|----------------|-----|
| Project architecture, build commands | `./CLAUDE.md` (project) | Every developer needs this; version-controlled |
| Coding standards, PR conventions | `./CLAUDE.md` (project) | Team consistency; changes tracked in git |
| Personal coding style preferences | `~/.claude/CLAUDE.md` (global) | Applies to all your projects; not shared |
| Experimental directives, personal API keys | `./CLAUDE.local.md` (local) | Per-project overrides; not committed |
| Schema files, API contracts | `@` reference in `./CLAUDE.md` | Cross-cutting context needed on most requests |
| Task-specific files | Interactive `@` in chat | One-time context; does not waste context window |

> [!TIP] **PM Decision Rule**
>
> If it affects the whole team, it goes in project CLAUDE.md. If it is personal, it goes in local or global. If you are unsure, ask: "Would a new team member need this?" If yes, project CLAUDE.md.

---

## The Context Window Budget Problem


![Context Window Budget Allocation](../../visuals/context-window-budget-allocation.svg)
*Figure: Context window budget allocation across different sources.*

PMs should understand this trade-off because it affects both performance and cost:

| More context in CLAUDE.md | Less context in CLAUDE.md |
|--------------------------|--------------------------|
| Claude always knows project details | Claude may need to discover files each time |
| Higher token consumption per request | Lower token consumption per request |
| Risk of degraded response quality | Better reasoning with focused context |
| Faster for repeated questions | Slightly slower for first-time exploration |

The sweet spot: put **cross-cutting, frequently needed** files in CLAUDE.md `@` references. Let Claude discover everything else through its tools.

---

## Practice Questions

### Q1: Organizational Rollout

Your CTO asks: "How do we ensure all 50 developers using Claude Code follow our coding standards?" Which approach is correct?

- A. Send an email asking each developer to configure their Claude Code settings
- B. Add coding standards to the project CLAUDE.md and commit it to the repository
- C. Create a CLAUDE.local.md template and ask each developer to copy it
- D. Use the Anthropic dashboard to set organization-wide Claude Code rules

<details><summary>Answer</summary>

**B** — Project CLAUDE.md is committed to source control and automatically applied to all developers who clone the repo. This is the architectural solution — no manual setup per developer, no drift over time.

- A does not scale and creates drift
- C uses the wrong file type (local is gitignored, will not propagate)
- D does not exist as described

**PM Takeaway**: CLAUDE.md is your policy enforcement mechanism. Treat it like a team-wide configuration file, not a personal settings file.
</details>

### Q2: Performance Complaint

A developer reports: "Claude Code used to be fast but now it is slow and gives worse answers." Investigation reveals they added 12 `@` file references to CLAUDE.md last week. What do you recommend?

- A. Ask them to upgrade to a higher API tier for more context window
- B. Audit the `@` references and move non-essential ones to interactive `@` mentions; keep only cross-cutting files in CLAUDE.md
- C. Tell them to remove CLAUDE.md entirely and start over
- D. Suggest they switch to a simpler project structure

<details><summary>Answer</summary>

**B** — The lesson explicitly teaches that too much context degrades performance. The proportionate response is to audit and optimize, not to remove everything or throw money at the problem.

**PM Takeaway**: Context window is a finite resource. Treat `@` references in CLAUDE.md like database indexes — each one has a maintenance cost, so only keep the ones that provide cross-cutting value.
</details>

### Q3: New Hire Onboarding

A new developer joins your team. They have never used Claude Code. What is the fastest path to productive AI-assisted development on your project?

- A. Give them a 2-hour training on prompt engineering for Claude
- B. Have them install Claude Code, pull the repo (which includes CLAUDE.md), and start working — the CLAUDE.md provides project context automatically
- C. Ask them to run `/init` to generate a fresh CLAUDE.md
- D. Share your personal CLAUDE.local.md with them

<details><summary>Answer</summary>

**B** — If the team has already committed a well-maintained CLAUDE.md to the repo, the new developer inherits all project context automatically. No training needed for basic usage.

- A is disproportionate for getting started
- C would overwrite the team's existing CLAUDE.md
- D shares personal settings, not team standards (and local files are gitignored anyway)

**PM Takeaway**: A well-maintained CLAUDE.md is an onboarding accelerator. It is like having a senior engineer's brain available to every new hire from day one.
</details>
