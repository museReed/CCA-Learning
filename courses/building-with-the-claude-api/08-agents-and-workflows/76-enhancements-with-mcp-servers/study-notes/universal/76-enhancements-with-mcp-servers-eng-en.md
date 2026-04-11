# Enhancements with MCP Servers — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Claude Code Configuration (20%) / D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 3.2 (MCP integration in Claude Code), 2.3 (MCP primitives), 1.1 (Claude Code extension model) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 76 |

---

## One-Liner

Claude Code ships with a built-in MCP client, letting you extend its capabilities by registering any MCP server via `claude mcp add [server-name] [command-to-start-server]` — this is the official extension point and the reason Claude Code can grow with your workflow.

---

## The MCP Extension Model

Claude Code's default toolset covers file operations, terminal, and web access. Everything else — your databases, your internal APIs, your third-party SaaS — comes in through MCP servers. The architecture:

```
┌────────────────────────────────────────┐
│          Claude Code (CLI)             │
│  ┌──────────────────────────────────┐  │
│  │      Built-in tools              │  │
│  │  File / Bash / Web / To-do       │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │      MCP Client (built in)       │  │
│  └────────┬─────────┬──────────┬────┘  │
└───────────┼─────────┼──────────┼───────┘
            │         │          │
       ┌────▼──┐ ┌────▼──┐  ┌────▼──┐
       │Sentry │ │Jira   │  │Custom │
       │MCP    │ │MCP    │  │MCP    │
       │Server │ │Server │  │Server │
       └───────┘ └───────┘  └───────┘
```

Each MCP server can expose three types of primitives:

| Primitive | Purpose | Example |
|-----------|---------|---------|
| **Tools** | Take actions | `document_path_to_markdown(path)` |
| **Prompts** | Reusable templates | A `/summarize` slash command |
| **Resources** | Access data | A fixture file or a DB row |

This matches the general MCP control model you already know from the MCP course: tools are model-controlled, prompts are user-controlled, resources are app-controlled.

---

## The `claude mcp add` Command

The entire registration syntax is one line:

```bash
claude mcp add [server-name] [command-to-start-server]
```

### Arguments

- **`server-name`** — a short identifier you choose (e.g., `documents`). This is the name Claude Code uses internally.
- **`command-to-start-server`** — the exact shell command that starts the MCP server process. Claude Code runs it as a child process and talks to it over stdio.

### Concrete example

If your document-processing server is started by running `uv run main.py` in its project directory, registration is:

```bash
claude mcp add documents uv run main.py
```

After this, the next time Claude Code starts, it automatically spawns the server and connects to it. The tools, prompts, and resources that server exposes become available to the agent.

Key fact for the exam: registration is a one-time operation — after `claude mcp add`, Claude Code remembers the server and reconnects on every subsequent launch.

---

## Practical Example: Document Processing

A canonical example the lesson builds: a custom MCP server exposing a `document_path_to_markdown` tool that reads PDF and Word documents and returns markdown.

Workflow:

1. Write the MCP server with the `document_path_to_markdown` tool.
2. Register it: `claude mcp add documents uv run main.py`.
3. In a Claude Code session, ask: "Convert the tests/fixtures/mcp_docs.docx file to markdown."
4. Claude Code recognizes the intent, picks the custom tool, invokes it, and receives the markdown text.

The user never explicitly names the tool. Claude infers which tool to use from the request, demonstrating the model-controlled nature of MCP tools.

---

## Popular MCP Integrations (Exam-Relevant Catalog)

The lesson names these servers explicitly — expect recognition questions:

| Server | What it unlocks |
|--------|-----------------|
| **sentry-mcp** | Automatically discover and fix bugs logged in Sentry |
| **playwright-mcp** | Gives Claude browser automation capabilities for testing and troubleshooting |
| **figma-context-mcp** | Exposes Figma designs to Claude |
| **mcp-atlassian** | Allows Claude to access Confluence and Jira |
| **firecrawl-mcp-server** | Adds web scraping capabilities to Claude |
| **slack-mcp** | Allows Claude to post messages or reply to specific threads |

Memorize the pairings — you may be asked "which MCP server would let Claude Code fix bugs logged in a monitoring platform?" and the answer is `sentry-mcp`.

---

## Composing Multiple MCP Servers

The real power is combining servers to match your development process:

| Stage | MCP server | What Claude does |
|-------|-----------|------------------|
| Triage | sentry-mcp | Fetch production error details |
| Context | mcp-atlassian | Read the Jira ticket requirements |
| Implement | (built-in file tools) | Edit the code |
| Verify | playwright-mcp | Run browser tests |
| Notify | slack-mcp | Post completion message in the team channel |

Each server adds a vertical slice of capability. Stacking them turns Claude Code from a coding assistant into a workflow orchestrator that can span your entire toolchain.

This composition pattern — **specialized servers, each doing one thing, orchestrated by the agent** — is the MCP architectural ideal and shows up on the exam.

---

## Why MCP Instead of "Just Add More Built-In Tools"

Design rationale (beyond the source):

1. **Decoupling** — Anthropic does not need to ship and maintain every possible tool. The ecosystem handles long-tail needs.
2. **Security boundaries** — Each MCP server is a separate process with its own permissions and lifetime.
3. **Community contribution** — Anyone can publish an MCP server; ecosystem grows without Anthropic engineering bandwidth.
4. **Composition** — Stacking multiple small servers is cleaner than a monolithic agent with 200 built-in tools fighting for context window space.

---

## Common Mistakes

1. **Wrong command syntax** — it is `claude mcp add [name] [command]`, not `claude mcp install` or `claude add-server`.
2. **Forgetting that the server must be runnable** — Claude Code starts the MCP server as a subprocess; the command you pass must actually launch a valid MCP server.
3. **Confusing MCP with generic HTTP APIs** — MCP speaks a specific protocol over stdio or SSE, not raw REST.
4. **Assuming servers auto-install** — Claude Code does not fetch MCP servers from a registry; you must install them yourself first, then register.
5. **Re-running `claude mcp add` on every session** — registration persists; you only do it once per server per machine.

> **Key Insight**
>
> The MCP extension point is the single most important architectural fact about Claude Code: its power grows not through Anthropic adding features, but through you (or the community) plugging in MCP servers. The exam-critical sentence: **`claude mcp add [server-name] [command-to-start-server]`** — memorize the exact syntax. Questions frequently test both the command and the primitive triad (tools, prompts, resources).

---

## CCA Exam Relevance

- **D3 (Claude Code Configuration)**: Direct question likely on `claude mcp add` syntax and the fact that Claude Code has an MCP client built in.
- **D2 (Tool Design & MCP Integration)**: Know that MCP servers expose tools, prompts, and resources (the three primitives).
- **D1 (Agentic Coding & Architecture)**: Expect "compose multiple MCP servers into a workflow" scenario questions.
- Expect recognition questions for the named ecosystem servers (sentry-mcp, playwright-mcp, figma-context-mcp, mcp-atlassian, firecrawl-mcp-server, slack-mcp).

---

## Flashcards

| Front | Back |
|-------|------|
| What command registers an MCP server with Claude Code? | `claude mcp add [server-name] [command-to-start-server]` |
| What does Claude Code have built in that makes MCP extension possible? | An MCP client — it can connect to any MCP server you register |
| What are the three types of primitives an MCP server can expose to Claude Code? | Tools (actions), Prompts (templates), Resources (data) |
| How would you register a document-processing server started by `uv run main.py` and called `documents`? | `claude mcp add documents uv run main.py` |
| Does Claude Code reconnect to a registered MCP server automatically? | Yes — registration persists, so the server is spawned automatically on every Claude Code launch |
| Which MCP server would you use to let Claude automatically find and fix bugs from a monitoring platform? | `sentry-mcp` |
| Which MCP server gives Claude browser automation capabilities? | `playwright-mcp` |
| Which MCP server would you use to read Jira tickets or Confluence pages? | `mcp-atlassian` |
| Why does Claude Code use MCP instead of shipping every possible tool built in? | MCP decouples the ecosystem, enables community contributions, adds process-level security boundaries, and keeps Claude Code's built-in surface small |
