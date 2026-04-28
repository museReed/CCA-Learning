# GitHub Integration — Engineering Deep Dive


![Github Workflows Two Actions](../../visuals/github-workflows-two-actions.svg)
*Figure: GitHub workflows — @claude mention + PR review.*

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Claude Code Configuration & Workflows (20%) |
| Task Statements | 3.6 ★★★ (CI/CD integration), 2.4 ★★ (MCP integration), 1.1 ★ (agentic loops) |
| Source | claude-code-in-action / 04-integrations / Lesson 13 |

---

## One-Liner

Claude Code's GitHub integration provides two automated workflows via GitHub Actions: `@claude` mention support for interactive tasks in issues/PRs, and automatic PR reviews. Both run Claude in non-interactive mode using the `-p` flag with explicit `allowed_tools` permissions.

---

## Two Default Workflows

The integration installs two GitHub Actions workflow files in `.github/workflows/`:

<!-- diagram: github-integration-workflows — /install-github-app → PR with 2 workflow files → Merge → (1) @claude Mention Action (issues + PRs) / (2) PR Review Action (automatic on PR create) -->
> Diagram produced by nanobanana

### 1. Mention Action (`@claude`)

Triggered when someone mentions `@claude` in an issue or pull request comment.

| Step | What Happens |
|------|-------------|
| 1. User mentions `@claude` | "Fix the toggle buttons" with a screenshot |
| 2. GitHub Action starts | Workflow spins up, sets up environment |
| 3. Claude analyzes | Creates a task checklist, plans approach |
| 4. Claude executes | Accesses codebase, runs tools, tests the app |
| 5. Claude responds | Posts findings/fix directly in the issue/PR |

### 2. PR Review Action

Triggered automatically when a pull request is created.

| Step | What Happens |
|------|-------------|
| 1. PR is opened | Developer pushes changes |
| 2. GitHub Action starts | Workflow runs automatically |
| 3. Claude reviews | Analyzes changes, checks for issues |
| 4. Claude reports | Posts detailed review on the PR |

> 🎬 **Instructor insight from the video**
>
> In the demo, the instructor created a fake bug report with a screenshot, mentioned `@claude`, and Claude autonomously navigated to the app via Playwright, tested the buttons, confirmed they worked fine, and posted its findings. Claude created a step-by-step checklist before executing — this is the **agentic loop** pattern (plan → execute → observe → report).

---

## Setup Process

```bash
# Inside Claude Code, run:
/install-github-app
```

This walks you through three steps:
1. Install the Claude Code app on GitHub
2. Add your API key
3. Auto-generate a PR with the workflow files

After merging the PR, the two workflow files appear in `.github/workflows/`.

---

## Customizing Workflows

### Adding Project Setup Steps

Before Claude runs, you can add environment preparation:

```yaml
- name: Project Setup
  run: |
    npm run setup
    npm run dev:daemon
```

### Custom Instructions

Provide Claude with context about the running environment:

```yaml
custom_instructions: |
  The project is already set up with all dependencies installed.
  The server is already running at localhost:3000. Logs from it
  are being written to logs.txt. If needed, you can query the
  db with the 'sqlite3' cli. If needed, use the mcp__playwright
  set of tools to launch a browser and interact with the app.
```

> 💡 **Key detail**
>
> Custom instructions tell Claude what is already available in the CI environment. Since Claude cannot interactively discover this (it runs non-interactively with `-p`), these instructions are critical for Claude to know what tools and services are accessible.

### MCP Server Configuration

Configure MCP servers for the GitHub Actions environment:

```yaml
mcp_config: |
  {
    "mcpServers": {
      "playwright": {
        "command": "npx",
        "args": [
          "@playwright/mcp@latest",
          "--allowed-origins",
          "localhost:3000;cdn.tailwindcss.com;esm.sh"
        ]
      }
    }
  }
```

---

## Tool Permissions: The `-p` Flag and `allowed_tools`


![Permission Model Local Vs Ci](../../visuals/permission-model-local-vs-ci.svg)
*Figure: Permission model — local interactive vs CI non-interactive.*

This is the **most exam-critical** concept in this unit.

When Claude runs in GitHub Actions, it uses the `-p` flag (non-interactive / "print" mode). In this mode, there is no human to approve permissions, so **every tool must be explicitly listed**:

```yaml
allowed_tools: "Bash(npm:*),Bash(sqlite3:*),mcp__playwright__browser_snapshot,mcp__playwright__browser_click,..."
```

> ⚠️ **Critical exam detail**
>
> Unlike local development where you can use `mcp__playwright` to allow all tools from a server, in GitHub Actions **each MCP tool must be individually listed**. There is no shortcut. The instructor explicitly says: "There is no shortcut for permissions like we saw previously."

| Context | Permission Style | Example |
|---------|-----------------|---------|
| Local development | Blanket server allow | `"allow": ["mcp__playwright"]` |
| GitHub Actions (CI) | Individual tool listing | `allowed_tools: "mcp__playwright__browser_click,mcp__playwright__browser_snapshot,..."` |

> 🎯 **Exam note**
>
> The `-p` flag is the key indicator that Claude is running in non-interactive CI mode. Exam questions about CI/CD scenarios (S5) will often include this flag as a signal. When you see `-p`, think: explicit permissions, no human approval, `allowed_tools` required.

---

## The Agentic Loop in CI

When Claude runs via `@claude` mention, it demonstrates the agentic loop pattern:

1. **Plan** — Claude creates a checklist of steps (visible in the GitHub comment)
2. **Execute** — Claude runs tools (Bash, Playwright, Read, Write)
3. **Observe** — Claude evaluates results
4. **Report** — Claude posts findings back to the issue/PR

This is Task Statement 1.1 (agentic loops) applied in a CI/CD context. The loop is autonomous — no human intervention between steps.

---

## Familiar Analogies

| Technology | GitHub Integration Equivalent | Behavior |
|-----------|------------------------------|----------|
| CI/CD bots (Dependabot, Renovate) | PR Review Action | Automated PR analysis |
| ChatOps (`/deploy` in Slack) | `@claude` mention | Trigger agent from a comment |
| Jenkins pipeline agent | Claude in GitHub Actions | Non-interactive tool execution |
| Code review tools (SonarQube) | PR Review Action | Automated quality gates |

---

## Configuration Hierarchy

| Layer | What It Configures | Where |
|-------|--------------------|-------|
| Workflow YAML | When Claude runs, env setup | `.github/workflows/*.yml` |
| `custom_instructions` | What Claude knows about the env | Inside workflow YAML |
| `mcp_config` | What tools Claude has access to | Inside workflow YAML |
| `allowed_tools` | What Claude is permitted to use | Inside workflow YAML |
| `CLAUDE.md` | Project-wide instructions | Repository root |

---

## Anti-Patterns

| Anti-Pattern | Why It Is Wrong | Correct Approach |
|-------------|----------------|-----------------|
| Not listing MCP tools individually in CI | Claude cannot use tools it is not explicitly allowed | List each tool in `allowed_tools` |
| Forgetting to set up the environment before Claude runs | Claude will fail to find running services | Add setup steps before the Claude action |
| Not providing `custom_instructions` about the CI environment | Claude will waste tokens discovering what is available | Tell Claude what is already running |
| Using interactive mode in CI | CI has no human to approve permissions | Use `-p` flag for non-interactive mode |

---

## Practice Questions

### Q1: CI/CD Pipeline Scenario

Your team wants to add Claude Code as an automated PR reviewer in GitHub Actions. Claude needs to access a PostgreSQL database to validate migration files. Which configuration is correct?

- A. Add `mcp__postgresql` to `.claude/settings.local.json` allow list
- B. Configure `mcp_config` with the PostgreSQL MCP server in the workflow YAML, and list each PostgreSQL tool individually in `allowed_tools`
- C. Add "you have access to PostgreSQL" in `custom_instructions` without configuring an MCP server
- D. Configure `mcp_config` with the PostgreSQL MCP server and use `mcp__postgresql` in `allowed_tools` to allow all tools

<details><summary>Answer</summary>

**B** — In GitHub Actions, you must configure the MCP server in `mcp_config` AND list each tool individually in `allowed_tools`. There is no shortcut for MCP tool permissions in CI.

- A configures local settings, not CI
- C tells Claude about PostgreSQL but does not give it actual access
- D uses blanket permission which is not available in GitHub Actions — each tool must be listed individually

Exam philosophy: **Explicit Permissions > Blanket Access** in CI/CD contexts.
</details>

### Q2: Developer Productivity Scenario

A developer wants Claude to automatically test UI changes when mentioned in a GitHub issue. The app runs on `localhost:3000`. What steps are needed in the workflow configuration?

- A. Just add `@claude` mention support — Claude will figure out the rest
- B. Add a setup step to start the dev server, configure Playwright MCP in `mcp_config`, list Playwright tools in `allowed_tools`, and add `custom_instructions` explaining the running server
- C. Add Playwright MCP to `.claude/settings.json` and deploy the app to a public URL
- D. Configure `custom_instructions` telling Claude to use `curl` to test the app

<details><summary>Answer</summary>

**B** — All four components are needed: environment setup (start the server), MCP configuration (give Claude browser tools), explicit permissions (list each Playwright tool), and custom instructions (tell Claude what is already running).

- A is insufficient — Claude needs explicit configuration in CI
- C mixes local and CI configuration approaches
- D does not give Claude actual browser interaction capability

Exam philosophy: **Architecture > Prompt** — give Claude the tools and environment, do not hope it can work with `curl` alone.
</details>

### Q3: CI/CD Automation Scenario

Your team has configured Claude Code in GitHub Actions for PR reviews. Engineers notice Claude is not using the Playwright MCP server despite it being configured in `mcp_config`. What is the most likely issue?

- A. The Playwright MCP server is not compatible with GitHub Actions
- B. The individual Playwright tools are not listed in `allowed_tools`
- C. Claude needs to be restarted after MCP configuration changes
- D. The `custom_instructions` do not mention Playwright

<details><summary>Answer</summary>

**B** — In GitHub Actions, configuring an MCP server in `mcp_config` is not enough. Each tool from that server must also be individually listed in `allowed_tools`. This is the most common misconfiguration.

- A is incorrect — Playwright works in GitHub Actions
- C is incorrect — Claude starts fresh for each action run
- D may be helpful but is not the root cause — tools need explicit permission, not just instructions

Key exam term: `allowed_tools` is the permission gate in CI/CD mode.
</details>
