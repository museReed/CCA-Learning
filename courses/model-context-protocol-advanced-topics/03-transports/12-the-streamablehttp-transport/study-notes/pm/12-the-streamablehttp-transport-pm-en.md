# The StreamableHTTP Transport — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.1 (MCP transport selection), 2.4 (remote server configuration) |
| Source | model-context-protocol-advanced-topics / 03-transports / Lesson 12 |

---

## One-Liner

StreamableHTTP puts your MCP server on the internet, but like moving from a private office to a public reception desk — you gain accessibility but lose the ability to walk over and tap someone on the shoulder.

---

## The Reception Desk Analogy

- **Stdio** = Private office. You and your colleague sit across from each other. Either person can start a conversation at any time.
- **StreamableHTTP** = Reception desk. Visitors (clients) can walk up and ask questions. But the receptionist (server) **cannot leave the desk** to find visitors — they must wait for someone to approach.

This is the fundamental HTTP limitation: **the server can only respond, never initiate**.

---

## What This Means for Your Product

### Features That Still Work (Client-Initiated)

| Feature | User Experience |
|---------|----------------|
| Tool calls | User asks AI, AI calls your server tools — works perfectly |
| Resource reads | AI fetches data from your server — works perfectly |
| Prompt templates | AI loads templates from server — works perfectly |

### Features At Risk (Server-Initiated)

| Feature | What's Lost | Product Impact |
|---------|------------|----------------|
| Sampling (CreateMessage) | Server can't ask the AI to generate text | No server-side AI reasoning |
| Progress notifications | Server can't report "50% done..." | Users see no progress on long tasks |
| Logging | Server can't push debug messages | Harder to troubleshoot in production |
| Root listing | Server can't ask "what files are open?" | No workspace-aware features |

> 💡 **Key Insight**
> If your product roadmap includes features where the **server needs to ask the client questions** (like "approve this action?" or "which file should I use?"), StreamableHTTP with restrictive settings will block those features.

---

## The Two Configuration Dials

Think of these as **restriction levels** your infrastructure team can set:

| Setting | Off (Default) | On | Business Impact |
|---------|--------------|-----|----------------|
| `stateless_http` | Server remembers each client session | Server treats every request independently | Easier to scale, but loses progress tracking and server-initiated features |
| `json_response` | Server can stream results gradually | Server sends one big response at the end | Simpler infrastructure, but users wait longer for results |

### The Restriction Spectrum

```
Most Features ◄──────────────────────────────► Simplest Infrastructure

Both OFF          stateless ON       json ON         Both ON
(default)         or json ON         or stateless    (most restricted)
```

---

## PM Decision Matrix

| Business Need | Recommended Setting |
|---------------|-------------------|
| "We need real-time progress bars" | Both flags OFF (defaults) |
| "We need to scale to 10K users" | `stateless_http=true` (accept feature loss) |
| "Simple webhook-style integration" | Both flags ON |
| "Server needs to call AI models" | Both flags OFF + SSE setup |
| "We just need basic tool access" | Either config works |

---

## The Core Trade-off for Stakeholders

| Dimension | Stdio | StreamableHTTP (defaults) | StreamableHTTP (restricted) |
|-----------|-------|--------------------------|---------------------------|
| Deployment | Local only | Remote/cloud | Remote/cloud |
| Scalability | Single user | Moderate | High |
| Feature coverage | 100% | ~80% (with SSE workarounds) | ~50% |
| Infrastructure complexity | Minimal | Moderate | Low |

---

## CCA Exam Relevance

- **Scenario questions**: "Remote MCP server for a web app" → StreamableHTTP. Then check which features the scenario needs to determine flag settings.
- **Trade-off questions**: Know the exact features lost at each restriction level.
- **Flag defaults**: Both `false` — this is frequently tested. Enabling restricts, not enables.
- **Never confuse direction**: Client→server always works. Only server→client is affected.

---

## Flashcards

| Front | Back |
|-------|------|
| In business terms, what does StreamableHTTP enable? | Remote MCP server hosting — your server can be in the cloud, serving users over the internet |
| What is the fundamental limitation of HTTP for MCP? | Server cannot initiate communication — it can only respond to client requests |
| What product feature requires server-initiated requests? | Progress bars, human-approval workflows, server-side AI reasoning (sampling) |
| What do the two flags default to? | Both `stateless_http` and `json_response` default to `false` (least restrictive) |
| What happens when you turn on `stateless_http`? | Server forgets sessions — easier to scale but loses progress tracking and server-initiated features |
| What happens when you turn on `json_response`? | No streaming — server sends one big response instead of gradual updates |
| When should a PM accept the feature trade-offs? | When scalability or infrastructure simplicity outweighs the need for server-initiated features |
| What features always work regardless of flag settings? | Client-initiated features: tool calls, resource reads, prompt template fetching |
