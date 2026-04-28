# Enhancements with MCP Servers — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Claude Code Configuration (20%) / D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 3.2 (MCP integration in Claude Code), 2.3 (MCP primitives), 1.1 (Claude Code extension model) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 76 |

---

## One-Liner

MCP servers are the "app store" for Claude Code — they let a PM compose an agent from modular capabilities (Sentry, Jira, Slack, Figma, custom internal APIs) without asking Anthropic or engineering to build anything, using one command: `claude mcp add`.

---

## Mental Model: Plug-in Architecture for Agents

Think of Claude Code as a power strip and MCP servers as the devices you plug in:

| Power strip analogy | Claude Code reality |
|---------------------|---------------------|
| The strip (base device) | Claude Code with built-in file, shell, and web tools |
| Each socket | An MCP client connection |
| Devices you plug in | MCP servers (sentry-mcp, playwright-mcp, your internal server) |
| Adding a device | `claude mcp add [name] [command]` |

The key insight: the strip was designed so you could plug in anything. You do not need to return the strip to the factory to add a new device.

---

## Why This Lesson Matters for PMs

Up to lesson 75, Claude Code looks like a coding assistant. Lesson 76 reveals what it actually is — a **workflow orchestration platform**. With MCP servers, Claude Code can span your entire tool chain:

| Before MCP | After MCP |
|------------|-----------|
| Reads and edits code | Reads Jira tickets, edits code, checks Sentry, updates Slack |
| Terminal-scoped | Crosses your whole SaaS stack |
| Helps an individual | Can drive a full team workflow |

For a PM evaluating where Claude Code fits in the product org, this is the moment it graduates from "a nice dev tool" to "a platform choice."

---

## Product Use Cases

### When to invest in MCP servers

| Scenario | MCP servers to add |
|----------|--------------------|
| Production bug triage | sentry-mcp + mcp-atlassian + slack-mcp |
| Spec-driven feature development | mcp-atlassian + figma-context-mcp |
| QA automation | playwright-mcp + (internal fixture server) |
| Research and scraping | firecrawl-mcp-server |
| Internal system access | Custom MCP server for your APIs |

### When an MCP server is overkill

| Scenario | Alternative |
|----------|-------------|
| One-off script that calls your API | Have Claude write a Python script and run it |
| Read-only documentation | Use Claude Code's built-in web fetch |
| Action you only do once a month | Manual work still cheaper than the integration |

A good rule of thumb: build or install an MCP server only if the integration will be used weekly or is safety-critical.

---

## The Six Named Ecosystem Servers

PMs should memorize these so they can answer "does the ecosystem already have this?" questions fast:

| Server | Business use case | Decision framing |
|--------|-------------------|------------------|
| **sentry-mcp** | Automated bug discovery and fixes | "Connect Claude to our monitoring platform" |
| **playwright-mcp** | Browser automation for testing | "Let Claude run end-to-end tests" |
| **figma-context-mcp** | Claude reads design files | "Let Claude implement designs" |
| **mcp-atlassian** | Claude reads Jira/Confluence | "Let Claude see spec and tickets" |
| **firecrawl-mcp-server** | Claude scrapes the web | "Let Claude do competitive research" |
| **slack-mcp** | Claude posts to Slack | "Let Claude talk to the team" |

If a stakeholder asks "can Claude do X?", first check this list before scoping a custom build.

---

## PM Decision Framework

When a team proposes "let's add an MCP server", ask:

1. **Does an ecosystem server already exist?** Check the six named servers and the wider MCP ecosystem first.
2. **What primitive does the workflow actually need?** Tool (action), prompt (template), or resource (data)? Most times it is a tool.
3. **What is the trust boundary?** Each MCP server is a separate process — does the integration touch production? Require an approval step.
4. **Who owns the server?** Internal servers need an owner team. External servers need a version pin and update plan.
5. **What is the fallback if the server is down?** Claude Code's agent loop degrades — plan for it.

---

## The Composition Story: Stacking Servers Into Workflows

The biggest PM-relevant concept in this lesson is that you combine multiple MCP servers to cover an entire workflow. Example — production bug workflow:

| Step | What happens | MCP server used |
|------|--------------|-----------------|
| 1. New error lands | Claude is told: "fix the latest Sentry P1" | sentry-mcp |
| 2. Read ticket | Claude finds the linked Jira ticket | mcp-atlassian |
| 3. Read related code | Claude uses built-in file ops | (built-in) |
| 4. Implement fix | Claude edits files, runs tests | (built-in) |
| 5. Browser verify | Claude runs Playwright tests | playwright-mcp |
| 6. Notify team | Claude posts a summary in Slack | slack-mcp |

Four MCP servers plus Claude Code's built-in tools cover the entire production hotfix workflow. A PM's job is to notice which of these stacks is valuable to the org and approve the rollout.

---

## The Pricing and Operational Lens

Adding an MCP server has real operational costs. PMs should budget for:

| Cost | Description |
|------|-------------|
| Token cost | More tools = more context window used per turn |
| Latency | Each MCP server is a subprocess — slow servers slow the agent |
| Failure surface | Any server can crash and break the agent mid-workflow |
| Security review | Each integration is a new data path — review it |
| Updates | Servers get versioned; stale versions break silently |

None of these are deal-breakers; they are just items your rollout plan must account for.

---

## Common PM Mistakes

1. **Building custom when an ecosystem server exists** — check the six named servers first.
2. **Adding every server you can think of** — each server costs context and latency; curate.
3. **Not defining ownership** — internal MCP servers without owners rot fast.
4. **Ignoring the trust boundary** — an MCP server that can post to Slack can post the wrong thing. Add confirmation steps for destructive actions.
5. **Confusing MCP servers with API keys** — MCP is a protocol, not credentials. Auth is still your problem.

> **Key Insight**
>
> MCP turns Claude Code from a dev tool into a **workflow orchestration platform**. The command `claude mcp add` is the PM-visible moment where your agent graduates from "helps with code" to "runs a cross-system workflow." Treat MCP adoption as a platform decision, not a developer whim.

---

## CCA Exam Relevance

- **D3 (Claude Code Configuration)**: Know the `claude mcp add` command and that Claude Code has an MCP client built in.
- **D2 (Tool Design & MCP Integration)**: Know the three primitives (tools, prompts, resources).
- **D1 (Agentic Coding & Architecture)**: Be ready for scenario questions composing multiple servers into a workflow.
- Recognition questions for the named servers (sentry, playwright, figma, atlassian, firecrawl, slack) are very likely.

---

## Flashcards

| Front | Back |
|-------|------|
| What command does a PM need to authorize/document for adding MCP servers to Claude Code? | `claude mcp add [server-name] [command-to-start-server]` |
| What are the three MCP primitives that can be exposed through a server? | Tools (take action), Prompts (reusable templates), Resources (access data) |
| Which MCP server lets Claude automatically work on bugs logged in a monitoring platform? | `sentry-mcp` |
| Which MCP server lets Claude read Jira tickets and Confluence pages? | `mcp-atlassian` |
| Which MCP server lets Claude post messages to team channels? | `slack-mcp` |
| What is the PM test for whether to build a custom MCP server? | Will the integration be used weekly or is it safety-critical? If yes, build; otherwise defer |
| Name a four-server stack that covers a production hotfix workflow. | sentry-mcp (triage) + mcp-atlassian (ticket) + playwright-mcp (verify) + slack-mcp (notify), plus Claude Code built-in tools |
| What operational costs must a PM budget when adopting MCP servers? | Token cost, latency, failure surface, security review, and version/update maintenance |
