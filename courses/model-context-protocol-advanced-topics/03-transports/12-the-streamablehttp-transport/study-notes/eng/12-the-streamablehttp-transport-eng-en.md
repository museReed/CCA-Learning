# The StreamableHTTP Transport — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.1 (MCP transport selection), 2.4 (remote server configuration) |
| Source | model-context-protocol-advanced-topics / 03-transports / Lesson 12 |

---

## One-Liner

StreamableHTTP enables remote MCP servers over HTTP, but HTTP's request-response model means the server cannot initiate communication — trading full MCP capability for remote hosting.

---

## Why StreamableHTTP Exists

Stdio requires same-machine deployment. For production systems serving multiple users or running in the cloud, you need HTTP. StreamableHTTP bridges MCP to the web — but HTTP has a fundamental constraint:

**HTTP is client-initiated only.** The server can only respond to requests; it cannot spontaneously send messages to the client.

---

## Two Key Configuration Flags

StreamableHTTP behavior is controlled by two boolean settings on the server:

| Flag | Default | Purpose |
|------|---------|---------|
| `stateless_http` | `false` | When `true`, disables session tracking |
| `json_response` | `false` | When `true`, returns plain JSON instead of SSE streams |

Both default to `false` (least restrictive). Enabling either one **removes capabilities**.

```python
# Server configuration example
mcp_server = MCPServer(
    stateless_http=False,  # default: sessions enabled
    json_response=False,   # default: SSE streaming enabled
)
```

> 💡 **Key Insight**
> Think of these flags as **restriction toggles**. The more you enable, the simpler the server becomes — but the fewer MCP features you can use.

---

## What HTTP Breaks

The core limitation: **servers cannot initiate requests to clients** over plain HTTP.

### Affected Server-Initiated Features

| Feature | What It Does | Impact When Unavailable |
|---------|-------------|------------------------|
| `CreateMessage` (Sampling) | Server asks LLM to generate text | No server-side AI calls |
| `ListRoots` | Server queries client's workspace | No file system awareness |
| Progress Notifications | Server reports task progress | Client has no visibility into long operations |
| Logging Notifications | Server sends log messages | No real-time debugging info |

### What Still Works

All **client-initiated** features work normally:

- `tools/call` — client invokes server tools
- `resources/read` — client reads server resources
- `prompts/get` — client fetches prompt templates

---

## The Capability Spectrum

```
Full MCP (Stdio)
    │
    ▼
StreamableHTTP (defaults)     ← SSE workaround partially restores server→client
    │
    ▼
StreamableHTTP + stateless    ← No sessions, no server-initiated anything
    │
    ▼
StreamableHTTP + json_response ← No streaming at all
    │
    ▼
Both flags enabled            ← Maximum restriction, simplest server
```

Each step down **trades functionality for simplicity/scalability**.

---

## When to Use StreamableHTTP

| Scenario | Recommended Config |
|----------|--------------------|
| Remote server, need most features | Defaults (both `false`) |
| Horizontal scaling needed | `stateless_http=true` |
| Simple request-response API | Both `true` |
| Need sampling/progress | Defaults only — flags break these |
| Local development | Use Stdio instead |

---

## CCA Exam Relevance

- **Transport trade-off questions**: StreamableHTTP = remote hosting, reduced capabilities. Know exactly which features break.
- **Flag behavior**: `stateless_http` and `json_response` both default to `false`. Enabling either restricts functionality.
- **Server-initiated vs client-initiated**: HTTP only breaks server-initiated patterns. Client→server always works.
- Exam philosophy: **Remote access has a cost** — every networking constraint removes MCP features.

---

## Flashcards

| Front | Back |
|-------|------|
| What fundamental HTTP limitation affects MCP? | HTTP is client-initiated only — servers cannot spontaneously send messages to clients |
| What are the two StreamableHTTP configuration flags? | `stateless_http` and `json_response`, both defaulting to `false` |
| What happens when you enable `stateless_http`? | Disables session tracking — no server-initiated requests, no sampling, no progress notifications |
| What does `json_response=true` do? | Returns plain JSON instead of SSE streams — no streaming, just final results |
| Name two server-initiated features broken by HTTP | CreateMessage (sampling) and Progress Notifications |
| What client-initiated features still work over HTTP? | tools/call, resources/read, prompts/get — all client→server requests work normally |
| What is the capability trade-off of StreamableHTTP? | Remote hosting capability in exchange for reduced/lost server-initiated MCP features |
| When should you use StreamableHTTP defaults (both false)? | When you need remote hosting but still want maximum MCP capability including SSE workarounds |
