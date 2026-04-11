# Defining Resources — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.3 (MCP primitives: tools vs resources vs prompts), 2.2 (content block types), 1.2 (context injection into agent loop) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 67 |

---

## One-Liner

Resources are the MCP primitive for **exposing data** — they behave like HTTP GET handlers addressed by URI, let the server decide how to serialize the response via MIME type, and come in two flavors: direct (static URI) and templated (URI with parameters).

---

## Resources vs Tools — The Mental Split

MCP gives servers three primitives: tools, resources, and prompts. The first decision when adding a new capability is whether it is a resource or a tool.

| Aspect | Resource | Tool |
|--------|----------|------|
| Purpose | Expose data (read) | Perform actions (read or write) |
| Analogy | HTTP GET handler | HTTP POST handler / RPC |
| Identification | URI (`docs://documents/{id}`) | Named function + JSON schema |
| Typical use | Fetch a document, list items | Edit, delete, send |
| Who decides to call it | Client/app inserts into prompt | Claude decides at inference time |

A rule of thumb: if the capability is a pure read that the user (or the app) wants to reference directly in a prompt, make it a resource. If the capability performs an action — especially one Claude should choose autonomously during an agent loop — make it a tool.

---

## Motivating Example: The `@document_name` Mention

The lesson anchors resources in a concrete product feature: users type `@` in the CLI and the app autocompletes available documents. When they pick one and submit, the app injects that document's content into the prompt.

Two operations are needed:

1. **List all documents** → for autocomplete
2. **Fetch a specific document's contents** → for injection

Both are pure reads. Both map cleanly to resources.

---

## Resource Request/Response Flow

Resources follow a request-response pattern. The client sends a `ReadResourceRequest` with a URI; the server responds with the data. The URI is the address of the resource.

```
Client ── ReadResourceRequest(uri="docs://documents/report.pdf") ──▶ Server
Client ◀──────── TextResourceContents(text=..., mimeType=...) ────── Server
```

This is deliberately simple: no schema negotiation, no tool loop, no second Claude call. Resources are pulled by URI and returned.

---

## Two Kinds of Resources

### Direct Resources

A fixed URI that never changes. Used for static data endpoints — "give me the list of all documents."

### Templated Resources

A URI with parameters embedded in curly braces. The Python SDK parses the URI, extracts the parameters, and passes them as keyword arguments to your function. Used for parameterized fetches — "give me document X."

The naming of URI parameters in the template must match the function signature exactly — the SDK pairs them by name.

---

## Implementing Resources with `@mcp.resource()`

### Direct Resource: List Documents

```python
@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    return list(docs.keys())
```

- URI `docs://documents` is static.
- Return value is a Python list of strings; the SDK serializes it to JSON automatically because `mime_type="application/json"`.
- No parameters — this is a pure directory listing.

### Templated Resource: Fetch One Document

```python
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]
```

- `{doc_id}` in the URI becomes a keyword argument in the function.
- `mime_type="text/plain"` because the return is raw document text.
- Errors surface as Python exceptions, which the SDK converts into proper error responses to the client.

---

## MIME Types

Resources can return any type of data — strings, JSON, binary. The `mime_type` parameter tells the client how to parse the response:

- `application/json` — structured JSON; SDK serializes return values automatically
- `text/plain` — raw text
- Any other valid MIME type for different formats

A critical convenience: **the SDK handles serialization for you**. You return a Python value (list, dict, str); the SDK converts it based on MIME type. You do not manually stringify JSON.

---

## Testing Resources with the MCP Inspector

Run the server in dev mode:

```bash
uv run mcp dev mcp_server.py
```

The inspector opens in your browser with two relevant sections:

- **Resources** — lists direct/static resources
- **Resource Templates** — lists templated resources and their parameter schemas

Clicking a resource runs it and shows the exact response structure the client will receive. This is the fastest way to validate your URI, MIME type, and return shape before wiring the client.

---

## Key Rules to Remember

- Resources expose data; tools perform actions.
- Direct resources = static URI; templated resources = URI with `{params}`.
- Parameter names in templated URIs become function arguments (matched by name).
- MIME type guides client parsing and enables automatic serialization.
- The Python SDK serializes return values — do not manually convert to JSON.

---

## Common Mistakes

1. **Using a resource for a side-effect operation** — writes, sends, deletes belong in tools, not resources.
2. **Mismatched URI parameter and function argument** — `{doc_id}` in the URI must match `doc_id: str` in the signature exactly.
3. **Manually JSON-stringifying the return value** — the SDK does this when `mime_type="application/json"`. Double serialization produces nested JSON strings.
4. **Forgetting to set `mime_type`** — the client uses it to decide how to parse; defaulting it can silently return text when you expected JSON.
5. **Building resources without the Inspector** — skipping MCP Inspector means your first real client call is the first test.

> **Key Insight**
>
> Resources are **data endpoints addressed by URI**. The URI is the whole API contract — picking good URIs (like `docs://documents/{doc_id}`) is analogous to designing a REST API. Good resource design means stable URIs, clear MIME types, and a clean split from tools: resources are what the client decides to pull; tools are what Claude decides to call.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: know that resources are one of three MCP primitives (tools, resources, prompts); recognize `@mcp.resource()` decorator with URI and `mime_type`; understand direct vs templated resources.
- **D1 (Agentic Architecture)**: resources are how an MCP server provides context to the agent loop without requiring a tool call — they are pulled and injected by the client.
- Exam pattern: "The server needs to expose document contents by ID to be injected into the prompt. Should this be a tool or a resource?" → resource.

---

## Flashcards

| Front | Back |
|-------|------|
| What are resources in MCP? | Server-side data endpoints addressed by URI, analogous to HTTP GET handlers, for exposing data rather than performing actions. |
| What are the two types of resources? | Direct (static URI like `docs://documents`) and templated (URI with parameters like `docs://documents/{doc_id}`). |
| What decorator defines a resource? | `@mcp.resource(uri, mime_type=...)` |
| How do templated URI parameters reach your function? | The SDK parses them from the URI and passes them as keyword arguments matched by name. |
| When should you use a resource vs a tool? | Resource for pure reads that the client pulls; tool for actions (especially ones Claude should choose autonomously). |
| What does the `mime_type` parameter do? | Tells the client how to parse the response and enables automatic SDK serialization (e.g., `application/json`). |
| How do you test resources locally? | `uv run mcp dev mcp_server.py` and use the MCP Inspector in the browser, which lists direct resources and resource templates. |
| Do you need to manually JSON-stringify return values? | No — the SDK handles serialization automatically based on the declared `mime_type`. |
