# MCP Clients — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.3 (MCP primitives & protocol), 2.4 (multi-turn loops), 1.2 (agent loop integration) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 62 |

---

## One-Liner

The MCP client is the "universal adapter" that sits inside your product's server and speaks MCP to any MCP server — the piece that lets your team swap stdio for HTTP and local-dev for production without re-architecting the agent.

---

## Mental Model: The Ticket Desk at a Theme Park

Think of your product's backend as a visitor service center and the MCP client as the ticket desk:

| Theme park analogy | Product/MCP reality |
|--------------------|---------------------|
| Visitor asks for a ride | User asks the AI assistant a question |
| Service center looks up which rides are open | Server calls `list_tools` to discover MCP tools |
| Service center hands the visitor a ticket | Server forwards the tool call via the MCP client |
| Visitor rides the ride | MCP server executes the real integration |
| Service center records the outcome | Server sends the result back to Claude |

The ticket desk doesn't run the rides — it connects visitors to them. That's exactly what an MCP client does for your agent.

---

## Why This Lesson Matters for PMs

Lesson 62 looks technical but it carries three product-shaping implications:

1. **The integration layer is replaceable.** Because MCP is transport-agnostic, your vendor choice (stdio dev, HTTP production, remote MCP in future) is a PM/ops decision rather than a rewrite.
2. **Your product's agent loop is bounded.** There is one identifiable component (the MCP client) through which all external system access flows — so governance, logging, rate limits, and policy can live in one place.
3. **Cross-SaaS workflows become a composition problem.** Once your client speaks MCP, every new integration is "add another server", not "add another code path."

---

## Product Use Cases

### When the MCP client abstraction shines

| Scenario | Why the client layer matters |
|----------|-----------------------------|
| Multi-tenant AI assistant | Each tenant can have its own set of MCP server connections, loaded through the same client |
| Evolving production infra | Start with stdio locally, move to HTTP when the server needs to be shared — no product code changes |
| Compliance / audit | All tool calls flow through a single point; easy to log and review |
| Gradual rollout of new tools | PMs can gate new MCP servers behind a feature flag at the client level |

### When the abstraction is less visible

| Scenario | What happens |
|----------|--------------|
| A product with only one integration | Overhead of client + server feels like ceremony |
| A product that never needs live actions | Tool use (and therefore MCP) is not required |
| Consumer apps with tight latency budgets | Each MCP layer adds milliseconds — measure carefully |

---

## The "10-Step Flow" in PM Terms

The lesson walks a detailed 10-step diagram for "user asks 'what repositories do I have?'". The PM-friendly summary is:

1. User asks.
2. Product server decides to consult the agent.
3. Server asks MCP client for the tool menu.
4. Server hands question + menu to Claude.
5. Claude says "call this tool".
6. Server forwards the call via MCP client → MCP server → GitHub.
7. GitHub answers → MCP server wraps → MCP client surfaces.
8. Server returns the result to Claude.
9. Claude formats a user-friendly answer.
10. User sees the answer.

For a PM, the important observation is **how many hops there are** — each hop has a cost (latency, failure risk, log surface) that your roadmap should price in. The MCP client is the one that abstracts away the worst of that complexity from your product code.

---

## PM Decision Framework

When reviewing an agent feature that uses MCP clients, ask:

1. **Which transport should we ship with?** stdio for local dev parity; HTTP for shared/remote servers. Product teams usually start with stdio.
2. **Who owns the MCP client instance lifecycle?** One global client or one per request? Affects concurrency and cost.
3. **What happens when the MCP server dies mid-call?** The user-visible failure mode is yours to design.
4. **How do we surface MCP server latency in our SLOs?** A slow MCP server looks like a slow assistant.
5. **Where do we log tool calls for audit?** Route them through a middleware at the client layer — don't scatter logging.

---

## The Cost Lens

The 10-step flow the lesson diagrams has real cost implications:

| Cost axis | Source |
|-----------|--------|
| API tokens | Every tool definition in `list_tools` is sent to Claude in every turn |
| Latency | Two round trips to Claude + two round trips to the MCP server + external API time |
| Failure surface | Five inter-process boundaries on the happy path; each can fail |
| Engineering time | Most of the complexity is hidden by the client library — that's the PM win |

A PM should reason about these costs whenever proposing "let's add more MCP servers". More servers = more tools in the `list_tools` response = more tokens every turn.

---

## Common PM Mistakes

1. **Treating the MCP client as infrastructure "for later"** — it is a product decision today; it shapes how your agent evolves.
2. **Not asking which transport the team picked** — stdio vs HTTP has ops, cost, and scaling consequences.
3. **Assuming tool listing is free** — every tool definition eats tokens on every turn.
4. **Conflating MCP client with Claude SDK** — the Claude SDK talks to Claude; the MCP client talks to MCP servers.
5. **Forgetting about error UX** — MCP server failures surface through your product UI; design the "tool failed" message.

> **Key Insight**
>
> The MCP client is your product's **single door** to external capabilities. Everything the agent can do in the real world walks through that door. That makes the client the single best place to enforce product policy — logging, rate limits, per-tenant access, feature flags, audit trails. Treat it as a platform surface, not just a library import.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: Know that the client issues `ListTools` and `CallTool` messages and that MCP is transport-agnostic.
- **D1 (Agentic Architecture)**: Be able to trace the 10-step flow — especially which hops involve the MCP client vs which involve the Claude API directly.
- Expect PM-flavoured scenario questions: "you need to add audit logging for all tool calls — where do you put it?" → at the MCP client layer.

---

## Flashcards

| Front | Back |
|-------|------|
| In PM terms, what is the MCP client? | The single door inside your server that all external tool calls pass through. |
| Why is transport-agnosticism a product win? | You can evolve from local stdio to networked HTTP without rewriting agent logic. |
| What are the two main message types the MCP client uses? | `ListToolsRequest/Result` for discovery and `CallToolRequest/Result` for execution. |
| Which component talks to the Claude API — the server, the client, or both? | The product server talks to Claude; the MCP client only talks to MCP servers. |
| What does adding more MCP tools cost your product? | Tokens on every turn, latency, and audit/ops surface. |
| Where should a PM put policy controls for tool use? | At the MCP client layer — the single chokepoint. |
| What does the "10-step flow" illustrate? | How a single user question becomes a coordinated sequence across user, server, MCP client, MCP server, and Claude. |
| Who owns MCP server uptime from a product standpoint? | Whoever authors/hosts the server — but the user-visible failure mode is yours to design. |
