# Claude Code Setup — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Claude Code Configuration (20%) |
| Task Statements | 3.1 (Claude Code installation & setup), 3.2 (authentication), 1.1 (Claude Code overview) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 74 |

---

## One-Liner

Claude Code is a terminal-native coding agent installed via `npm install -g @anthropic-ai/claude-code`, launched with the `claude` command, and extensible through MCP — three commands total from clean machine to working agent.

---

## What Claude Code Provides Out of the Box

Before we touch the installer, know what the agent ships with so you can answer "which of these does Claude Code support?" exam questions:

| Tool category | What it does |
|---------------|-------------|
| **File operations** | Search, read, and edit files anywhere in your project |
| **Terminal access** | Run shell commands directly from the conversation |
| **Web access** | Fetch documentation pages, search the web, pull code examples |
| **MCP server support** | Extend tools with any MCP server you register |

The MCP integration is the most important category for the exam — it is the official extension point. "Built-in tools + MCP" is the mental model to carry in.

---

## Supported Platforms

Claude Code is a cross-platform CLI. Per the lesson it runs on:

- **macOS** — native
- **Windows** — via WSL (Windows Subsystem for Linux)
- **Linux** — native

On Windows, raw PowerShell/cmd is not the supported path; you must be inside WSL. Expect at least one exam question that drops "Windows" into a setup scenario.

---

## The Three-Step Installation

The entire flow is three steps. Memorize them in order:

### Step 1 — Install Node.js

Claude Code is distributed as an npm package, so you need Node + npm. The lesson suggests checking first:

```bash
npm help
```

If that works, you already have Node. Otherwise download from `nodejs.org/en/download`.

### Step 2 — Install Claude Code globally

```bash
npm install -g @anthropic-ai/claude-code
```

Key things to note about this command (common exam traps):

- The `-g` flag (global) — required, because `claude` needs to be on your PATH.
- The package name is `@anthropic-ai/claude-code` (scoped under the `@anthropic-ai` org) — not `claude` or `anthropic-claude-code`.
- It is an npm package, not a `pip install`, not a standalone binary download.

### Step 3 — Launch and authenticate

```bash
claude
```

On first launch Claude Code prompts you to log in to your Anthropic account. After login, you are dropped into the interactive agent session in the current working directory.

---

## Authentication Model

The lesson describes browser-style login tied to your Anthropic account. Important points:

- Login is tied to your **Anthropic account**, not a raw API key that you paste into a config file.
- The first `claude` invocation triggers the login flow.
- Once authenticated, subsequent sessions reuse credentials automatically.
- Billing and usage flow through your account — this is distinct from using the Anthropic API directly with an `ANTHROPIC_API_KEY` environment variable.

For the exam, remember the distinction: **Anthropic API billing uses an API key; Claude Code uses account-based login**.

---

## A Full Setup Session on a Fresh Mac

```bash
# 1. Check if Node exists
npm help
# If not installed, download from nodejs.org/en/download and install

# 2. Install Claude Code globally
npm install -g @anthropic-ai/claude-code

# 3. Verify it is on PATH
which claude
# /usr/local/bin/claude  (or similar)

# 4. Launch, authenticate, and enter project
cd ~/projects/my-app
claude
# First run: login flow opens
# After login: interactive agent prompt
```

After these four commands you have a working terminal agent scoped to the current working directory. The current directory becomes the agent's default project root.

---

## What You Can Do Immediately After Setup

Once `claude` is running you can issue natural language requests and the agent will use its built-in tools. Example first-session moves:

- `Read the README.md and summarize the project`
- `Find every file that references the old API endpoint`
- `Run the test suite and report failures`

These just work — no further configuration needed. Advanced setup (CLAUDE.md, MCP servers, custom commands) comes in the next lessons.

---

## Common Mistakes

1. **Omitting the `-g` flag** — a local-only install will not put `claude` on your PATH.
2. **Wrong package name** — the correct scoped name is `@anthropic-ai/claude-code`.
3. **Running on Windows without WSL** — the lesson specifies Windows WSL, not native PowerShell.
4. **Trying to set `ANTHROPIC_API_KEY` instead of logging in** — Claude Code uses account login, not raw API keys.
5. **Skipping the `npm help` check** — installs fail silently on machines without Node.

> **Key Insight**
>
> The CCA exam treats the Claude Code install path as a "trivia-level" fact you must memorize exactly: **Node.js → `npm install -g @anthropic-ai/claude-code` → `claude` → account login**. There are no optional steps, and Windows explicitly means WSL. Mastering this sentence is worth easy points.

---

## CCA Exam Relevance

- **D3 (Claude Code Configuration)**: This lesson is the foundation for ~20% of the exam. Expect direct questions on the install command and platform support.
- **D1 (Agentic Coding & Architecture)**: You must know that Claude Code is an agent application, not a chat app, and that MCP is its extension mechanism.
- Expect at least one question asking the exact npm package name — `@anthropic-ai/claude-code`.

---

## Flashcards

| Front | Back |
|-------|------|
| What are the three installation steps for Claude Code? | 1) Install Node.js, 2) `npm install -g @anthropic-ai/claude-code`, 3) run `claude` and log in |
| What is the exact npm package name for Claude Code? | `@anthropic-ai/claude-code` |
| Why does the install command use the `-g` flag? | Global install puts the `claude` executable on your PATH so it can be launched from any directory |
| Which operating systems does Claude Code support? | macOS, Windows (via WSL), and Linux |
| What authentication model does Claude Code use? | Account-based login through your Anthropic account, not a raw `ANTHROPIC_API_KEY` |
| What are the four built-in tool categories in Claude Code? | File operations, terminal access, web access, and MCP server support |
| What command can you run to check whether Node.js is already installed? | `npm help` |
| What command launches Claude Code for the first time? | `claude` — this triggers the login flow |
