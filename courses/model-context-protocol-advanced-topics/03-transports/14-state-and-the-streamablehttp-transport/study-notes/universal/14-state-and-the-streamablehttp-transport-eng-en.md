# State and the StreamableHTTP Transport — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.1 (MCP transport selection), 2.4 (remote server configuration), 2.6 (horizontal scaling patterns) |
| Source | model-context-protocol-advanced-topics / 03-transports / Lesson 14 |

---

## One-Liner

Horizontal scaling creates a coordination problem — two SSE connections from the same client may hit different server instances, and `stateless_http=true` solves this by eliminating state entirely, at the cost of major MCP features.

---

![Scaling Tradeoff](../../visuals/scaling-tradeoff.svg)


## The Scaling Problem

When an MCP server becomes popular, you need to scale horizontally — multiple server instances behind a load balancer. This creates a fundamental coordination problem:

```
                    ┌─── Instance A
Client ──→ LB ─────┤
                    ├─── Instance B
                    └─── Instance C
```

Remember from Lesson 13: a client maintains **two connections**:
1. **GET SSE** (persistent, for server-initiated messages)
2. **POST requests** (per tool call)

The load balancer may route these to **different instances**:

```
Client ── GET /sse ──→ LB ──→ Instance A  (primary SSE here)
Client ── POST /tool ──→ LB ──→ Instance B  (tool call here)
```

Instance B processes the tool call but Instance A holds the SSE connection. How does Instance B send progress updates to the client?

> 💡 **Key Insight**
> The two-connection architecture that makes SSE work on a single server becomes a liability at scale. The load balancer has no awareness of MCP session semantics.

---

## Solution: `stateless_http=true`

The nuclear option: **eliminate all state**. When enabled:

| Feature | Status |
|---------|--------|
| Session IDs | Disabled — no tracking |
| Server → Client requests | Disabled — no CreateMessage, no ListRoots |
| Sampling | Disabled |
| Progress notifications | Disabled |
| Resource subscriptions | Disabled |
| Initialization handshake | **Not required** — any instance can handle any request |

```python
# Stateless server — no initialization needed
mcp_server = MCPServer(
    stateless_http=True,  # Each request is independent
    json_response=False,  # Can still stream per-request
)
```

### The Key Benefit

No initialization required. Any server instance can handle any request independently. The load balancer just round-robins — no sticky sessions, no session affinity needed.

---

## Solution: `json_response=true`

A complementary flag that eliminates streaming:

| With `json_response=false` (default) | With `json_response=true` |
|--------------------------------------|--------------------------|
| Server streams results via SSE | Server returns single JSON response |
| Client sees progress in real-time | Client waits for complete result |
| Requires keeping connection open | Standard HTTP request-response |

```python
# Maximum simplicity — stateless + JSON
mcp_server = MCPServer(
    stateless_http=True,
    json_response=True,   # Just return final JSON
)
```

---

## The Decision Matrix

| Need | `stateless_http` | `json_response` | Result |
|------|-----------------|-----------------|--------|
| Full MCP features, single server | `false` | `false` | All features via SSE |
| Horizontal scaling, some streaming | `true` | `false` | Per-request streaming, no server-initiated |
| Maximum scalability, simple API | `true` | `true` | Basic request-response only |
| Streaming but with sessions | `false` | `false` | Needs sticky sessions on LB |

### The Fundamental Trade-off

```
Functionality ◄─────────────────────► Scalability

Full MCP          SSE workaround       Stateless         Stateless + JSON
(Stdio)           (single server)      (scales out)      (simplest)
```

---

## What You Lose vs. What You Gain

### `stateless_http=true` Losses

- No session IDs
- No server → client requests (CreateMessage, ListRoots)
- No sampling capability
- No progress reports
- No resource subscriptions

### `stateless_http=true` Gains

- No initialization handshake required
- Any instance handles any request
- Standard load balancer works (no sticky sessions)
- Simpler server implementation
- Better fault tolerance (instance failure doesn't lose session)

---

## Architectural Patterns

### Pattern 1: Sticky Sessions (Keep State)

```
Client ──→ LB (session affinity) ──→ Always Instance A
```

Keeps full MCP features but limits scaling and fault tolerance.

### Pattern 2: Stateless (Scale Out)

```
Client ──→ LB (round robin) ──→ Any Instance
```

Maximum scalability but loses server-initiated features.

### Pattern 3: Hybrid (Advanced)

Use stateless for most requests, separate stateful service for sampling/subscriptions. Complex but gets the best of both worlds.

---

## CCA Exam Relevance

- **Scaling questions**: Know that the two-connection model breaks with load balancers → `stateless_http` is the standard solution.
- **Feature-loss matrix**: Memorize exactly what `stateless_http=true` disables — it's a frequent exam target.
- **No initialization benefit**: Stateless mode skips the three-message handshake entirely.
- **Combined flags**: Both `true` = simplest possible MCP server (basic HTTP request-response).
- Exam philosophy: **Scalability and functionality are inversely correlated** in MCP transport design.

---

## Flashcards

| Front | Back |
|-------|------|
| What scaling problem does StreamableHTTP face? | Two connections (GET SSE + POST) from one client may hit different server instances behind a load balancer |
| How does `stateless_http=true` solve the scaling problem? | Eliminates all state — no sessions, no SSE, any instance handles any request independently |
| What five features does `stateless_http=true` disable? | Session IDs, server→client requests, sampling, progress notifications, resource subscriptions |
| What is the key benefit of stateless mode? | No initialization required — any server instance can handle any request without prior handshake |
| What does `json_response=true` do? | Eliminates streaming — server returns a single final JSON response instead of SSE events |
| What is the simplest possible MCP server config? | Both `stateless_http=true` and `json_response=true` — basic HTTP request-response only |
| When would you keep both flags false? | Single server deployment where you need full MCP features including SSE, sampling, and progress |
| What load balancer strategy works with stateless MCP? | Round-robin — no sticky sessions or session affinity needed |
