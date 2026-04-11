# Introducing MCP — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.3 (MCP primitives: tools/resources/prompts), 2.1 (tool schema design), 1.2 (agent loop integration) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 61 |

---

## One-Liner

Model Context Protocol (MCP) is a communication layer that lets you plug pre-built, externally-maintained tools into Claude without writing the schemas or implementations yourself — it shifts the burden of tool authorship from your server to specialized MCP servers.

---

## The Problem MCP Solves

Once you understand tool use (Ch04), the next wall you hit is **scale of authorship**. Imagine building a chat interface where users can ask Claude about their GitHub data:

> "What open pull requests are there across all my repositories?"

To answer this, Claude needs tools that hit GitHub's API. GitHub has massive surface area — repositories, pull requests, issues, projects, commits, reviews, actions. A "complete" GitHub chatbot means authoring **dozens** of tools, each with:

1. A JSON schema describing the input shape
2. A Python function implementing the call
3. Tests, error handling, auth, rate-limit handling
4. Ongoing maintenance as GitHub's API evolves

That is a lot of code for any one developer to write, test, and maintain — and it has to be repeated for every service you integrate with (Slack, Jira, Sentry, Figma, ...).

---

## How MCP Changes the Equation

MCP shifts the burden of tool **definitions** and **execution** from your application server to a dedicated **MCP server**. Instead of writing all the GitHub tools yourself, you connect to a GitHub MCP server that already contains them:

```
┌────────────────┐                      ┌──────────────────────┐
│  Your server   │                      │   GitHub MCP Server  │
│  (MCP client)  │ ◀─── MCP protocol ──▶│  - list_repos        │
│                │                      │  - list_prs          │
│  Claude API    │                      │  - create_issue      │
│  integration   │                      │  - ... (dozens more) │
└────────────────┘                      └──────────────────────┘
```

An MCP server is a wrapper around an outside service (GitHub, AWS, Jira, ...) that exposes ready-made tools, prompts, and resources. Any application that speaks MCP can connect and immediately use them.

---

## What an MCP Server Exposes

An MCP server exposes three primitive types (the full set becomes important in later lessons, but you should know them now):

| Primitive | Purpose |
|-----------|---------|
| **Tools** | Functions Claude can call to take action or fetch data |
| **Prompts** | Reusable prompt templates surfaced to the host application |
| **Resources** | Data payloads Claude can read (files, records, etc.) |

Lesson 61 focuses on tools; resources and prompts appear in later lessons of Ch07.

---

## Who Authors MCP Servers?

Anyone can write one. In practice the authorship breaks into three tiers:

| Author | Example |
|--------|---------|
| Service provider (official) | AWS releases an official MCP server with tools for EC2, S3, IAM, etc. |
| Community | Open-source `sentry-mcp`, `playwright-mcp`, `firecrawl-mcp-server`, etc. |
| You (internal) | A custom server exposing your company's internal APIs |

The common pattern: when you want to integrate with service X, **check if an MCP server already exists before writing tools from scratch**.

---

## MCP vs Direct Tool Use

A frequent misconception is that MCP and tool use are alternatives. They are not — they are complementary:

| Concept | What it is |
|---------|-----------|
| **Tool use** | The Claude API protocol: `tool_use` request block → `tool_result` reply block |
| **MCP** | A separate protocol for *packaging and distributing* tools so someone else defines and runs them |

When you use MCP, your server still makes normal tool-use calls to Claude. The difference is **who** wrote and executes the tool implementations:

| Direct tools | MCP tools |
|--------------|-----------|
| You author the schema | MCP server ships the schema |
| You implement the function | MCP server runs the function |
| You maintain the integration | Server author maintains it |
| You own the code | You consume the server |

Your server in both cases still receives a `tool_use` block from Claude, executes it (by asking the MCP client to forward the call), and returns a `tool_result`. The agent loop is unchanged.

---

## Mental Model: Tool Distribution Layer

If tool use is Claude's plug, MCP is the power grid. It standardizes:

- **Discovery**: "what tools are available from this server?"
- **Invocation**: "call this tool with these arguments"
- **Transport**: stdio today, HTTP/WebSockets in more complex setups (covered in lesson 62)

The payoff is composability. If you have an MCP client, you can connect to N different MCP servers and assemble a custom agent out of their combined tools — without ever writing a schema.

---

## Where This Lesson Sits in the Course

Lesson 61 is the conceptual introduction. The subsequent lessons in Ch07 build an actual client and server:

| Lesson | What it adds |
|--------|-------------|
| 61 (this) | Why MCP exists and what it solves |
| 62 | MCP client: transport agnosticism and message types |
| 63 | Project setup for a CLI MCP demo |
| 64 | Defining tools with the Python SDK |
| 65 | Debugging with the MCP inspector |

---

## Common Mistakes

1. **Conflating MCP with tool use** — MCP is a *distribution* layer on top of tool use, not a replacement.
2. **Writing custom tools when an ecosystem server exists** — always check for an official or community MCP server first; `sentry-mcp`, `playwright-mcp`, `mcp-atlassian`, etc. already exist.
3. **Assuming MCP servers run in your process** — they run as separate processes (usually subprocesses) and talk over a transport. Failure modes are network-shaped.
4. **Thinking MCP handles auth for you** — it doesn't. Credentials still flow through your environment; each server has its own auth story.
5. **Believing MCP is Anthropic-proprietary** — it is an open protocol, and any model provider or any application can speak it.

> **Key Insight**
>
> MCP is best understood as a **package manager for tools**. Tool use gives Claude the ability to call functions; MCP gives the ecosystem a way to ship those functions so you don't have to write them. Whenever you are about to write a tool schema, first ask: "has someone already published an MCP server for this?"

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: the definition of MCP, the three primitives (tools/prompts/resources), and the distinction between MCP and direct tool use.
- **D1 (Agentic Architecture)**: MCP as a building block for agents that span multiple systems.
- Watch for questions framed as "what problem does MCP solve?" — the answer is always *the burden of authoring and maintaining tool integrations*.

---

## Flashcards

| Front | Back |
|-------|------|
| What does MCP stand for? | Model Context Protocol |
| What is MCP's core value proposition? | It shifts the burden of writing and executing tool definitions from your server to specialized MCP servers. |
| What are the three MCP primitives? | Tools, Prompts, Resources |
| Who can author an MCP server? | Anyone — service providers often release official servers; community and internal teams also publish them. |
| Is MCP a replacement for tool use? | No — MCP is complementary. Tool use is the Claude API protocol; MCP is a distribution layer on top of it. |
| Why would a team write a GitHub MCP server instead of calling GitHub's API directly? | So every consumer gets ready-made tool schemas and implementations instead of each app re-authoring them. |
| What does an MCP server act as, conceptually? | A wrapper around an outside service that packages reusable tools, prompts, and resources. |
| If an ecosystem MCP server already exists for a service, what should you do? | Use it instead of hand-rolling your own tool definitions. |
