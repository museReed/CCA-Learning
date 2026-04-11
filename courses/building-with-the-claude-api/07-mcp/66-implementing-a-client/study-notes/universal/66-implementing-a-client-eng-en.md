# Implementing a Client — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.3 (MCP primitives: client/server, list_tools, call_tool), 2.2 (content block types), 1.2 (agentic loop integration) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 66 |

---

## One-Liner

An MCP client is a thin wrapper around the MCP Python SDK's `ClientSession` that exposes two essential methods — `list_tools()` and `call_tool()` — so your application can discover and invoke server-side tools without worrying about transport, handshake, or resource cleanup.

---

## Why a Custom Client Class

In most real-world MCP projects you implement **either** a client **or** a server, not both. This course builds both so you can see how they fit together. The MCP client has two layers:

1. **`ClientSession`** — the underlying connection primitive provided by the MCP Python SDK. It handles the protocol handshake, message framing, and async lifecycle.
2. **`MCPClient`** — a custom class you write on top of `ClientSession` that:
   - Owns session lifecycle (startup + cleanup) via async context managers
   - Surfaces ergonomic methods (`list_tools`, `call_tool`, and later `read_resource`, `list_prompts`, `get_prompt`)
   - Hides the transport details (stdio subprocess, command + args) from the rest of your application

The critical reason for wrapping is **resource cleanup**: `ClientSession` requires proper async teardown. Bundling it in a context-managed class means callers never forget to close the subprocess.

---

## How the Client Fits the Agent Loop

Your CLI code needs two capabilities from the MCP server:

1. Get the list of available tools to forward to Claude (so Claude knows what it can call).
2. Execute a tool when Claude emits a `tool_use` block (so the result can be fed back into the agent loop).

```
┌────────────┐   list_tools()    ┌────────────┐
│ CLI / App  │ ────────────────▶ │ MCPClient  │
│            │ ◀──────────────── │            │
│            │     [tools]       └────────────┘
│            │                         │
│            │   ── call_tool() ──────▶│
│            │ ◀─── ToolResult ────────│
└────────────┘                         ▼
                                  MCP Server
                                  (subprocess)
```

The MCP client is the bridge: application logic on one side, MCP server on the other, agent loop wrapping both.

---

## The Two Core Methods

### `list_tools()`

```python
async def list_tools(self) -> list[types.Tool]:
    result = await self.session().list_tools()
    return result.tools
```

- Calls the session's built-in `list_tools()`.
- Returns a list of `types.Tool` objects — each contains `name`, `description`, and `inputSchema`.
- Your app converts these into the `tools` array that goes into `client.messages.create(..., tools=...)`.

### `call_tool()`

```python
async def call_tool(
    self, tool_name: str, tool_input: dict
) -> types.CallToolResult | None:
    return await self.session().call_tool(tool_name, tool_input)
```

- Takes the `name` and `input` fields that Claude emitted in the `tool_use` block.
- Delegates to the session's `call_tool()`, which sends the request over the MCP transport and awaits the server's response.
- Returns a `CallToolResult` whose `content` you plug into a `tool_result` block in the next API call.

Both methods are intentionally thin — the SDK does the real work. Your class exists to give callers a stable, friendly surface.

---

## Testing the Client Directly

The same file includes a testing harness that exercises the client in isolation (no Claude involved):

```python
async with MCPClient(
    command="uv", args=["run", "mcp_server.py"]
) as client:
    result = await client.list_tools()
    print(result)
```

Running it should print the tool definitions for `read_doc_contents` and `edit_document` — the tools registered on the server in earlier lessons. This is a smoke test: if the list comes back, the handshake, transport, and decoder are all healthy.

---

## End-to-End Flow (What Happens When a User Asks a Question)

1. **Startup** — CLI opens the `MCPClient` context manager, which spawns the `mcp_server.py` subprocess and performs the MCP handshake.
2. **Tool discovery** — CLI calls `client.list_tools()`. The result is stored or converted into the Anthropic tool schema.
3. **First Claude call** — user question + tool definitions go to `client.messages.create()`.
4. **Claude emits `tool_use`** — e.g., `read_doc_contents(doc_id="report.pdf")`.
5. **Dispatch** — CLI calls `client.call_tool("read_doc_contents", {"doc_id": "report.pdf"})`.
6. **Server executes** — returns a `CallToolResult` with the document text.
7. **Second Claude call** — CLI appends a `tool_result` block referencing the original `tool_use_id` and calls Claude again.
8. **Final answer** — Claude composes the user-facing response.

This is the same four-step tool use loop from Chapter 4 — MCP just replaces the local Python function dispatch with a protocol-based server call.

---

## Common Mistakes

1. **Calling `session()` without an active context** — the `ClientSession` must be initialized inside an `async with` block. Accessing it outside leaks the subprocess.
2. **Returning the raw `CallToolResult` to Claude** — you must still wrap it in a `tool_result` content block referencing the correct `tool_use_id`.
3. **Forgetting the subprocess command** — MCPClient is parameterized by `command` and `args` (e.g., `command="uv", args=["run", "mcp_server.py"]`). Wrong path = zero tools discovered.
4. **Treating `list_tools()` as cheap** — it involves an async round trip. Cache the result per session instead of calling on every user message.
5. **Mixing sync and async** — all MCP SDK calls are async. Calling them from sync code without an event loop will raise runtime errors.

> **Key Insight**
>
> An MCP client is not a rewrite of your agent loop — it is a **transport substitution**. Everywhere your old code called a local Python function, it now calls `client.call_tool(...)` instead. The agent loop, `tool_use` / `tool_result` protocol, and Anthropic API contract stay identical. MCP's power comes precisely from this separability: your servers become reusable across any Claude application without reshaping the agent loop.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: recognize that an MCP client wraps `ClientSession`, exposes `list_tools()` / `call_tool()`, and is the substitution point for local tool dispatch.
- **D1 (Agentic Architecture)**: the agent loop is unchanged by MCP — the client is just a different way to fetch tools and execute them.
- Exam pattern: "Where in an MCP-based app does the tool execution actually run?" → on the server, invoked via `call_tool()` on the client.

---

## Flashcards

| Front | Back |
|-------|------|
| What are the two layers of an MCP client? | `ClientSession` (SDK primitive handling transport + handshake) and a custom `MCPClient` class wrapping it for lifecycle and ergonomics. |
| Why wrap `ClientSession` in a custom class? | To guarantee async resource cleanup via context managers and to expose ergonomic methods to the rest of the app. |
| What two methods must an MCP client implement at minimum? | `list_tools()` and `call_tool(tool_name, tool_input)`. |
| What does `list_tools()` return? | A list of `types.Tool` objects with `name`, `description`, and `inputSchema` — ready to forward to Claude. |
| What does `call_tool()` accept and return? | Accepts `tool_name` and `tool_input` dict; returns a `CallToolResult | None`. |
| How do you test the MCP client in isolation? | Run the client file directly with a harness like `async with MCPClient(command="uv", args=["run", "mcp_server.py"]) as client: await client.list_tools()`. |
| How does MCP change the agent loop? | It does not — only the tool dispatch step is replaced by `client.call_tool(...)`. The loop, stop_reason logic, and tool_result protocol stay identical. |
| What is the typical `command`/`args` combination used in the course? | `command="uv"`, `args=["run", "mcp_server.py"]` — spawns the server as a subprocess over stdio. |
