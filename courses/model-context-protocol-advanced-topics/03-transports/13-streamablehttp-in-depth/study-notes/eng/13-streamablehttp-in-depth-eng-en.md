# StreamableHTTP In Depth — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.1 (MCP transport selection), 2.4 (remote server configuration), 2.5 (SSE streaming patterns) |
| Source | model-context-protocol-advanced-topics / 03-transports / Lesson 13 |

---

## One-Liner

SSE (Server-Sent Events) is the workaround that partially restores server-to-client communication over HTTP, using dual connections — a primary SSE for server-initiated messages and per-tool SSE streams for call-specific results.

---

![Streamable Http Sse](../../visuals/streamable-http-sse.svg)


## The Problem SSE Solves

HTTP is client-initiated only. But MCP needs the server to push messages (progress, logs, sampling requests). **SSE** flips this: the client opens a persistent connection, and the server pushes events down that connection whenever it wants.

```
Traditional HTTP:
  Client ──request──→ Server
  Client ←──response── Server
  (server cannot initiate)

With SSE:
  Client ──GET /sse──→ Server
  Client ←──event 1─── Server  (server pushes anytime)
  Client ←──event 2─── Server
  Client ←──event 3─── Server
  ...
```

---

## Connection Setup Sequence

| Step | Action | Detail |
|------|--------|--------|
| 1 | Client sends Initialize Request | POST to server |
| 2 | Server returns Initialize Result + **session ID** | Session ID tracks this client |
| 3 | Client sends Initialized Notification | POST with session ID |
| 4 | Client opens SSE connection | **GET request** — stays open for server-initiated messages |

The session ID is critical — it links the GET SSE connection to the POST requests from the same client.

```python
# Step 1-3: Normal handshake
session_id = initialize_handshake(server_url)

# Step 4: Open persistent SSE connection
sse_stream = requests.get(f"{server_url}/sse",
    headers={"Mcp-Session-Id": session_id},
    stream=True
)
```

---

## Dual SSE Architecture

This is the key architectural concept. There are **two types** of SSE connections:

### 1. Primary SSE Connection (GET)

- Opened once after initialization
- **Stays open** for the entire session
- Carries **server-initiated messages**: sampling requests, root list requests
- Think of it as the "general notification channel"

### 2. Tool-Specific SSE Connections (POST)

- Created for **each tool call**
- **Auto-closes** when the tool call completes
- Carries **tool-specific messages**: progress updates, log entries, final result
- Think of it as a "per-task channel"

```
Client                          Server
  │                               │
  │──── GET /sse ────────────────→│  (Primary SSE — stays open)
  │←─── server-initiated msgs ───│
  │                               │
  │──── POST /tools/call ────────→│  (Tool SSE — auto-closes)
  │←─── progress, logs, result ──│
  │                               │
  │──── POST /tools/call ────────→│  (Another tool SSE)
  │←─── progress, logs, result ──│
```

> 💡 **Key Insight**
> The dual SSE design means the server can push progress for a specific tool call via the tool SSE, AND simultaneously push unrelated server-initiated requests via the primary SSE. They are independent channels.

---

## Message Routing Rules

Understanding which messages go where is exam-critical:

| Message Type | SSE Channel | Why |
|-------------|-------------|-----|
| Progress notifications | Tool-specific SSE | Tied to a specific tool call |
| Log messages | Tool-specific SSE | Generated during tool execution |
| Tool results | Tool-specific SSE | The final answer for that call |
| CreateMessage (sampling) | Primary SSE | Server-initiated, not tied to a tool call |
| ListRoots | Primary SSE | Server-initiated, not tied to a tool call |

---

## What Breaks the SSE Mechanism

The two configuration flags from Lesson 12 directly impact SSE:

| Flag | Effect on SSE |
|------|--------------|
| `stateless_http=true` | No session ID → no primary SSE connection → no server-initiated messages |
| `json_response=true` | No streaming at all → tool calls return final JSON only → no progress/logs mid-call |

Both flags enabled = SSE is completely disabled. You're back to basic HTTP request-response.

---

## CCA Exam Relevance

- **SSE architecture questions**: Know the dual connection model — primary (persistent, server-initiated) vs tool-specific (per-call, auto-close).
- **Message routing**: Progress and logs go to tool SSE. Sampling and roots go to primary SSE.
- **Flag impact**: `stateless_http` kills the primary SSE. `json_response` kills all streaming.
- **Session ID**: Links GET and POST connections. Without it, the server cannot correlate requests.
- Exam philosophy: **SSE is a workaround, not a full solution** — it partially restores server→client communication.

---

## Flashcards

| Front | Back |
|-------|------|
| What problem does SSE solve in MCP? | HTTP servers cannot initiate communication — SSE provides a persistent connection for server-pushed events |
| What are the two types of SSE connections? | Primary SSE (GET, stays open, server-initiated messages) and Tool-specific SSE (POST, per-call, auto-closes) |
| Where do progress notifications route? | Tool-specific SSE connection (tied to the specific tool call) |
| Where do sampling (CreateMessage) requests route? | Primary SSE connection (server-initiated, not tied to any tool call) |
| What does the session ID do? | Links the GET SSE connection to POST requests from the same client |
| What happens when `stateless_http=true`? | No session ID, no primary SSE connection, no server-initiated messages |
| What happens when `json_response=true`? | No SSE streaming at all — only final JSON results returned |
| What is the setup sequence for SSE? | Initialize Request → Initialize Result (get session ID) → Initialized Notification → GET request opens primary SSE |
