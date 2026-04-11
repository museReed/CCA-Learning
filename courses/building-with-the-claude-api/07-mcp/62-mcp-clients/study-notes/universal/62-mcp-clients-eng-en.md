# MCP Clients — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.3 (MCP primitives and protocol), 2.4 (multi-turn tool loops), 1.2 (agent loop integration) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 62 |

---

## One-Liner

The MCP client is the communication bridge inside your server that speaks the MCP protocol to MCP servers — it abstracts transport, discovery (`ListTools`), and invocation (`CallTool`) so your app code can treat remote tools almost identically to local ones.

---

## The Role of the Client

Where Lesson 61 introduced MCP at an architectural level, Lesson 62 zooms into the client half of the picture. Your application has a piece that:

1. Establishes a connection to an MCP server over some transport.
2. Asks that server "what tools do you provide?"
3. Forwards Claude's tool-use requests to the server when the time comes.
4. Returns the server's results back up to your agent loop.

That piece is the **MCP client**. It is a library inside your own server, not a separate service. If you have ever used an HTTP client (e.g. `requests.Session`) to talk to a REST API, the MCP client plays the same role for MCP servers.

---

## Transport Agnostic Communication

A core design property of MCP is that it is **transport agnostic** — the client and server can talk over whatever medium makes sense. The most common setup today is:

| Transport | Where it fits |
|-----------|---------------|
| **stdio** (standard input/output) | Both client and server on the same machine; server is a subprocess |
| **HTTP** | Client and server on different machines; network-accessible server |
| **WebSockets** | Bi-directional streaming over a network |
| **Other network protocols** | Custom deployments |

The important implication: **the same MCP protocol messages work regardless of transport**. Swapping from stdio (local dev) to HTTP (production) does not change the shape of `ListToolsRequest` or `CallToolRequest` — it only changes how the bytes get delivered.

---

## The Core Message Types

MCP defines a set of message types. The two you work with most often (and the ones Lesson 62 highlights) are:

### 1. List Tools

```
Client  ──▶  ListToolsRequest   ──▶  Server
Client  ◀──  ListToolsResult    ◀──  Server
```

The client asks the server "what tools do you provide?" and gets back a structured list of tool definitions. Each definition includes a name, a description, and an input schema — the same shape your Claude API `tools` array expects, which is not an accident.

### 2. Call Tool

```
Client  ──▶  CallToolRequest   ──▶  Server
Client  ◀──  CallToolResult    ◀──  Server
```

The client asks the server to run a specific tool with specific arguments. The server executes it and returns the result. Your server then forwards that result to Claude as a `tool_result` block.

These two message types cover the entire discovery-then-invocation cycle for tools. Later lessons introduce analogous messages for resources and prompts.

---

## The Complete Flow Example (Repository Question)

Lesson 62 walks through a worked example: a user asks "what repositories do I have?" Here is the full sequence that the lesson describes.

```
┌──────┐    1 query     ┌────────────┐    2 ListToolsReq ┌─────────┐
│ User │ ─────────────▶ │ Your server│ ────────────────▶ │  MCP    │
└──────┘                │ + MCP      │ ◀────────────────│ Server  │
                        │  client    │ 3 ListToolsResult│         │
                        │            │                   │         │
                        │            │  4 messages w/    ┌─────────┐
                        │            │ ──── tools ─────▶│ Claude  │
                        │            │ ◀──── tool_use ──│  API    │
                        │            │  5 tool_use      └─────────┘
                        │            │
                        │            │  6 CallToolReq   ┌─────────┐
                        │            │ ────────────────▶│  MCP    │
                        │            │                  │ Server  │
                        │            │                  │    │    │
                        │            │                  │    ▼    │
                        │            │                  │ GitHub  │
                        │            │                  │   API   │
                        │            │                  │    │    │
                        │            │  7 CallToolResult│ ◀──┘    │
                        │            │ ◀────────────────│         │
                        │            │                  └─────────┘
                        │            │  8 tool_result   ┌─────────┐
                        │            │ ────────────────▶│ Claude  │
                        │            │ ◀── final answer ┤  API    │
                        │            │  9               └─────────┘
                        └────────────┘
                             │  10 final answer
                             ▼
                        ┌──────┐
                        │ User │
                        └──────┘
```

Step-by-step:

1. **User** submits a query to your server.
2. **Your server** realizes it needs to tell Claude what tools are available, so it asks the MCP client for them.
3. The **MCP client** sends `ListToolsRequest` to the MCP server and gets `ListToolsResult` back.
4. Your server calls Claude with the user's question *and* the tool list.
5. Claude returns a `tool_use` block.
6. Your server hands the tool-use details to the MCP client, which sends `CallToolRequest` to the MCP server. The MCP server performs the GitHub API call.
7. GitHub responds → MCP server packages the result → `CallToolResult` flows back to the MCP client.
8. Your server appends the result to the message list and calls Claude again.
9. Claude formats the final answer.
10. Your server returns the final answer to the user.

This is the same agentic loop from Ch04 tool use — the only difference is that tool listing and tool execution are delegated through the MCP client rather than implemented inside your server.

---

## What the MCP Client Abstracts Away

A well-written MCP client hides:

| Concern | What the client does for you |
|---------|-----------------------------|
| Transport negotiation | Chooses stdio, HTTP, etc., based on how you configured the connection |
| Message framing | Serializes/deserializes JSON-RPC-style messages on the wire |
| Request/response correlation | Matches responses to their in-flight requests |
| Error envelopes | Surfaces protocol-level errors vs tool-level errors |
| Lifecycle | Starts/stops the server subprocess where applicable |

Your application code typically sees `client.list_tools()` and `client.call_tool(name, args)` — simple async methods that return data, not a pile of JSON-RPC plumbing.

---

## Why Transport Agnosticism Matters

There are two engineering reasons this property is important:

1. **Local dev vs production parity.** You write the same code against stdio in dev and switch to HTTP in production without changing your agent logic.
2. **Process isolation and security.** An MCP server over stdio runs as a subprocess — crashes are contained. An MCP server over HTTP runs on a different host — blast radius is even smaller. Your agent code does not have to know which.

It also explains why MCP servers are safe to compose: each one is independent, they don't share memory, and the protocol handles the handshake.

---

## Common Mistakes

1. **Treating the MCP client as "the thing that talks to Claude."** It is not — the client talks to MCP servers. Your application code still talks to the Claude API separately.
2. **Forgetting to call `list_tools` before the first Claude call.** Claude needs the tool definitions up front; without them it cannot select a tool.
3. **Thinking stdio is a toy transport.** Most real MCP integrations run over stdio; it is the primary local-dev path and perfectly production-capable.
4. **Mixing up `CallToolResult` with `tool_result`.** `CallToolResult` is the MCP-layer reply; `tool_result` is the Claude-API content block you build from it before calling Claude again.
5. **Assuming one tool call returns immediately.** Tool execution can include external API latency (GitHub, DB, etc.) — clients are async-first.

> **Key Insight**
>
> The MCP client turns "can my agent call a remote tool?" into the same shape as "can my agent call a local function?" — and does so without committing you to any specific transport. Mastering the list-tools + call-tool cycle is what lets Lessons 63-65 make sense. Everything later is more primitives riding on the same two patterns.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: Know what the MCP client is, the difference between `ListTools` and `CallTool`, and the concept of transport agnosticism.
- **D1 (Agentic Architecture)**: The lesson's 10-step diagram is the canonical "agent + MCP" flow that can be invoked in scenario questions.
- Exam pitfall: expect questions about *where* each message type lives in the flow (client↔server, server↔Claude).

---

## Flashcards

| Front | Back |
|-------|------|
| What role does the MCP client play? | It is a library inside your server that speaks the MCP protocol to MCP servers, handling transport, discovery, and invocation. |
| What does "transport agnostic" mean for MCP? | The client and server can communicate over stdio, HTTP, WebSockets, or other transports — the same message types work regardless. |
| Which MCP message type does the client use to discover available tools? | `ListToolsRequest`, to which the server replies with `ListToolsResult`. |
| Which MCP message type does the client use to execute a tool? | `CallToolRequest`, to which the server replies with `CallToolResult`. |
| In the 10-step flow, does the MCP client talk directly to Claude? | No — your server talks to Claude; the MCP client only talks to MCP servers. |
| What is the most common local transport for MCP? | stdio (standard input/output) — usually with the server running as a subprocess. |
| How does `CallToolResult` differ from the `tool_result` block Claude expects? | `CallToolResult` is the MCP-layer response; your server wraps it into a `tool_result` content block before the next Claude API call. |
| How many round trips are involved in answering the "what repositories do I have?" example? | Two with Claude (initial + final) and two with the MCP server (list_tools + call_tool). |
