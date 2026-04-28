# Implementing a Client — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.3 (MCP primitives: client/server integration), 1.2 (agentic loop), 2.2 (content block types) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 66 |

---

## One-Liner

The MCP client is the "adapter plug" that lets any Claude-powered product snap into an existing MCP server — teams that build one can immediately reuse every MCP server the ecosystem produces, turning tool integrations from custom engineering work into configuration.

---

## Mental Model: The Power Outlet Adapter

Imagine your product is a laptop and MCP servers are wall outlets around the world. Without an adapter, every trip (every integration) means a new power cable. **The MCP client is the universal travel adapter**: write it once, plug into any MCP server, and your laptop charges the same way.

- Your product = Claude-powered app
- MCP server = a capability bundle (read docs, query CRM, send email)
- MCP client = the standard interface that lets your app talk to any server

This matters because the client is **not custom per integration**. It is the same code shape for every MCP server your product ever uses.

---

## Why PMs Should Care

Before MCP, "add a new tool" meant engineering tickets: write the schema, write the dispatcher, test it, ship it. Every integration cost real time. After MCP, adding a new tool can be as cheap as pointing your client at a new server.

| Before MCP | With MCP Client |
|------------|-----------------|
| Each integration is bespoke code | Integrations are pluggable servers |
| Tool schemas live in your app | Tool schemas live in the server, discovered dynamically |
| Cleanup and lifecycle are your problem | Hidden inside the client wrapper |
| Hard to reuse across products | Any MCP-compatible app can reuse the server |

For product leadership, this is a **time-to-value lever**: your eng team ships the client once, then every new capability is a server-side project (often built by someone else in the ecosystem).

---

## What the Client Actually Does (No Code)

The client has exactly two jobs:

1. **Ask the server "what can you do?"** — the tool discovery step. The server answers with a menu of tools (name, description, inputs). Your app forwards that menu to Claude so Claude knows its options.
2. **Execute a tool on request** — when Claude says "I need to call `read_doc_contents` with this document ID," your client relays the request to the server and returns the answer.

Everything else — startup, cleanup, message framing, subprocess lifecycle — is handled inside the client. Your product team does not see it.

---

## Product Use Cases

### When to Invest in Building an MCP Client

| Scenario | Why MCP Client Pays Off |
|----------|-------------------------|
| You expect to integrate many tools over time | One client, unlimited servers |
| Multiple teams build tools inside your company | Each team can ship a server independently |
| You want to adopt community/open-source tool integrations | MCP is the standard; plug and play |
| You run several Claude-powered apps | All apps can share the same servers |

### When a Client Is Overkill

| Scenario | Simpler Alternative |
|----------|---------------------|
| One product with two or three hard-coded tools | Keep using local Python functions and skip MCP |
| Throwaway prototype | Inline tool definitions are faster |
| Security-sensitive flows that forbid subprocesses | Embed tools directly in your app |

---

## PM Decision Framework

Before committing to an MCP client, ask:

| Question | If Yes | Implication |
|----------|--------|-------------|
| Will we integrate at least three distinct tool surfaces in the next 6 months? | Yes | MCP client pays off |
| Do we want other teams to ship capabilities without touching our codebase? | Yes | MCP client is ideal |
| Is there already an MCP server for the system we need? | Yes | Building the client unlocks it for free |
| Will our product run in an environment that cannot spawn subprocesses? | Yes | Reconsider — local tools may be safer |

---

## Reliability, Latency, and Observability

Adopting an MCP client introduces a new failure surface: the server may not start, the handshake may fail, a tool call may time out. PMs need to budget for:

- **Startup checks** — if the server subprocess cannot launch, the app must degrade gracefully (e.g., hide tool-powered features)
- **Per-tool error handling** — each `call_tool` can fail; plan UX for "the data source is temporarily unavailable"
- **Logging and audit** — every tool call is a potential side effect. Log tool name, arguments, and result for compliance and debugging
- **Latency overhead** — the first call includes a handshake and a `list_tools` round trip. Subsequent calls are faster but still network-bound

Put these into your launch checklist.

---

## Common PM Mistakes

1. **Treating the client as "just plumbing"** — in practice it becomes the observability, reliability, and security chokepoint. Fund it accordingly.
2. **Expecting zero integration effort** — MCP makes integration dramatically cheaper, not free. You still need to decide which servers to trust, how to authenticate, and how to handle errors.
3. **Skipping the tool discovery UX** — `list_tools` returns dozens of tools once you scale. The product must have a strategy for which to expose to which user.
4. **Ignoring subprocess security** — spawning an MCP server is running code. If that code is supplied by a third party, treat it like any other dependency (sandbox, pin, review).
5. **Rolling your own client when the SDK already has one** — write the thin wrapper for ergonomics, not a new transport.

> **Key Insight**
>
> The MCP client is the smallest piece of MCP, but it is the piece that decides whether your product gets to participate in the ecosystem. Build one, and every MCP server on the planet becomes a potential feature. Skip it, and you are stuck hand-coding every integration forever. For a PM, "do we invest in MCP?" is really "do we want our product's roadmap to compound from community work or grow only as fast as we write code?"

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: recognize the role of `list_tools` and `call_tool` as the minimal contract between a client and a server.
- **D1 (Agentic Architecture)**: the agent loop is unchanged — MCP is a substitution for local dispatch, not a new paradigm.
- Exam pattern: "An app needs to use an MCP server. What two methods must the client expose?" → `list_tools()` and `call_tool()`.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the "power outlet adapter" analogy for an MCP client? | The client is the universal adapter that lets your product plug into any MCP server without custom wiring per integration. |
| What two things does an MCP client do? | 1) Discover the tools the server offers, 2) execute a tool on behalf of Claude. |
| When is building an MCP client NOT worth it? | When you only have a few hard-coded tools, a throwaway prototype, or an environment that cannot spawn subprocesses. |
| What hidden risk comes with MCP adoption? | Running third-party server code — treat MCP servers as dependencies that need review, sandboxing, and version pinning. |
| What should be in a PRD for an MCP-powered feature? | Startup/error handling, tool discovery UX, per-call logging, fallback when a server is down, and latency budget. |
| Why is MCP a "time-to-value lever" for PMs? | Once the client exists, each new integration can be a server written by someone else — compounding roadmap capacity. |
| Does MCP change how Claude processes tool calls? | No — the agent loop is identical. MCP only changes where the tool code lives and how it is invoked. |
| What is the minimum client contract? | `list_tools()` to discover, `call_tool(name, input)` to execute. |
