# MCP Servers with Claude Code — PM Perspective


![Mcp Server Ecosystem Taxonomy](../../visuals/mcp-server-ecosystem-taxonomy.svg)
*Figure: MCP server ecosystem taxonomy.*

| Item | Details |
|------|---------|
| Exam Coverage | D2 — Tool Use & Integration (18% of exam) |
| Task Statements | 2.4 ★★★ (MCP integration), 2.1 ★★ (tool interfaces), 2.3 ★★ (tool distribution) |
| Course Source | claude-code-in-action / 04-integrations / Lesson 12 |

---


![Mcp Plugin Architecture Flow](../../visuals/mcp-plugin-architecture-flow.svg)
*Figure: MCP plugin architecture flow.*


![Mcp Architecture](../../visuals/mcp-architecture.svg)
*Figure: MCP server architecture — Claude Code ↔ Protocol ↔ Servers ↔ External Systems.*

## TL;DR

MCP servers are Claude Code's plugin system. They let you extend what Claude can do — browse the web, query databases, interact with APIs — without changing Claude Code itself. For PMs, the key insight is that MCP servers turn "Claude cannot do X" into "Claude can do X" at an architectural level. This is fundamentally different from prompt engineering, which only works within Claude's existing capabilities.

---

## Why PMs Need to Understand MCP Servers

1. **Scoping product capabilities** — Knowing what MCP servers exist tells you what Claude-powered features are feasible
2. **Build vs. configure decisions** — Many capabilities are available as MCP servers already; no custom development needed
3. **Security and permission governance** — MCP servers require explicit permission management, which affects your risk assessment
4. **CI/CD implications** — MCP servers in automated pipelines need different permission configurations than local development

---

## Mental Model: App Store for AI Tools

| Concept | App Store Analogy | MCP Server Reality |
|---------|-------------------|-------------------|
| Core product | iPhone out of the box | Claude Code's built-in tools (Read, Write, Bash, etc.) |
| Extension | Installing an app | Adding an MCP server |
| Permission | "Allow Camera access?" | "Allow mcp__playwright tools?" |
| Ecosystem | App Store catalog | MCP server registry |
| Configuration | App settings | `.claude/settings.local.json` |

> [!IMPORTANT]
> **Core Exam Philosophy (PMs must remember)**
>
> - **Architecture > Prompt** — If Claude needs a capability, give it a tool (MCP server). Do not try to prompt it into doing something it structurally cannot do.
> - **Explicit Permissions > Blanket Access** — Especially in CI/CD, each tool must be individually allowed.

---

## Product Scenario Walkthrough

### Scenario: Improving UI Component Generation

Your team uses an AI-powered component generator. The generated components look generic — lots of purple-to-blue gradients and standard Tailwind patterns. The product goal is to produce more creative, distinctive components.

| Approach | Implementation | Result |
|----------|---------------|--------|
| Prompt engineering only | Add "be more creative" to the generation prompt | Marginal improvement — Claude has no visual feedback |
| MCP + visual feedback loop | Install Playwright MCP → Claude generates component → Claude opens browser to see result → Claude updates prompt based on visual evaluation | Significant improvement — Claude iterates based on actual visual output |

> [!TIP]
> **PM Decision Framework**
>
> Ask yourself: "Does this require Claude to perceive or interact with something outside its context window?"
> - Yes → You need an MCP server (architectural solution)
> - No → Prompt engineering may suffice

---

## Business Impact of MCP Servers

| Impact Area | Without MCP | With MCP |
|-------------|-------------|----------|
| Visual QA | Manual review by humans | Claude verifies UI automatically via Playwright |
| Database operations | Copy-paste query results into Claude | Claude queries DB directly |
| API testing | Manual endpoint testing | Claude tests endpoints and validates responses |
| Development velocity | Claude generates code blindly | Claude generates, verifies, and iterates autonomously |

---

## Permission Governance

MCP servers have a permission model that PMs should understand for risk assessment:

| Setting | Location | Who Controls | Security Level |
|---------|----------|-------------|---------------|
| Local allow-all | `.claude/settings.local.json` | Individual developer | Low — convenient for dev |
| Project shared | `.claude/settings.json` | Team / Tech Lead | Medium — team standard |
| CI/CD explicit | GitHub Actions workflow file | DevOps / Team | **High — each tool listed individually** |

> [!TIP]
> **PM Takeaway**
>
> In production/CI contexts, MCP tool permissions must be explicitly listed one by one. There is no blanket "allow all tools from this server" shortcut. This is a deliberate security design — include it in your risk assessment.

---

## Instructor Insights (From the Video)

1. **Visual feedback changes everything** — The instructor was genuinely surprised by the quality improvement when Claude could see actual UI output. This suggests that visual verification capabilities should be a standard part of any UI-focused AI workflow.
2. **MCP servers are the extensibility story** — The instructor positions MCP as the primary way to extend Claude Code. If your product roadmap includes AI capabilities that Claude does not have out of the box, MCP servers are the answer.
3. **Ecosystem is growing rapidly** — The instructor recommends exploring MCP servers that align with your specific project needs, suggesting the ecosystem is mature enough for production use.

---

## Practice Questions

### Question 1: Developer Productivity Scenario

Your team wants Claude Code to verify that generated UI components match the design specification. Currently, developers manually compare screenshots. What would you recommend?

- A. Add the design specification to CLAUDE.md so Claude knows what to aim for
- B. Install the Playwright MCP server so Claude can open a browser and visually compare generated components against the spec
- C. Create a PostToolUse hook that runs visual regression tests after every file write
- D. Have developers paste screenshots into Claude Code conversations for review

<details><summary>Answer and Explanation</summary>

**B** — The Playwright MCP server gives Claude actual browser access to see and evaluate UI output. This creates an automated visual feedback loop.

- A gives Claude knowledge but no visual perception capability
- C could work for automated testing but requires pre-existing test infrastructure
- D works but is manual and breaks the automation benefit

> [!IMPORTANT]
> **PM Key Takeaway**: When the gap is "Claude cannot perceive something," the solution is an MCP server that gives it that perception — not a prompt that describes what it should perceive.

</details>

### Question 2: Code Generation Scenario

A PM is scoping an AI-powered feature that needs Claude to interact with a PostgreSQL database. The engineer says "we can just tell Claude the schema and have it write queries." What is the better approach?

- A. The engineer's approach is correct — providing schema context in the prompt is sufficient
- B. Install a PostgreSQL MCP server so Claude can directly query and validate against the live database
- C. Create a custom tool that wraps database queries and expose it via the Agent SDK
- D. Both B and C are valid, depending on whether this is Claude Code or an Agent SDK application

<details><summary>Answer and Explanation</summary>

**D** — For Claude Code workflows, a PostgreSQL MCP server (B) is the right approach. For Agent SDK applications, a custom tool (C) is the right approach. The key principle is the same: give Claude structural access to the database, do not rely on schema knowledge in prompts alone.

> [!IMPORTANT]
> **PM Key Takeaway**: The engineer's "just tell Claude" approach (A) is the classic prompt-over-architecture anti-pattern. Always prefer giving Claude real tools over describing capabilities in prompts.

</details>
