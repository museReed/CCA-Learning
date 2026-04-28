# Accessing Resources — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.3 (MCP primitives: client-side resource access), 2.2 (content block types), 1.2 (context injection into agent loop) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 68 |

---

## One-Liner

Accessing resources is the client-side counterpart to defining them — you add a `read_resource(uri)` method to the MCP client, parse the returned `contents` list by MIME type, and hand the result to your app so it can be injected into the prompt before Claude ever sees it.

---

## Why Resources Beat Tool Calls for Context Injection

The lesson's opening framing is key: resources let the server expose data that can be **directly included in prompts**, rather than requiring tool calls. The advantage is efficiency:

- **No second round trip** — no `tool_use` / `tool_result` loop just to fetch context
- **Deterministic** — the data is always present, not contingent on Claude deciding to call a tool
- **Simpler trace** — fewer content blocks to reason about when debugging

When a user types `@report.pdf` and sends a message, your app uses the MCP client to fetch the resource and inlines its text into the prompt. Claude receives the full document in the first API call.

---

## Implementing `read_resource`

Extend the MCP client with a new method:

```python
async def read_resource(self, uri: str) -> Any:
    result = await self.session().read_resource(AnyUrl(uri))
    resource = result.contents[0]
    # ... parse based on MIME type (see next section)
```

Points to notice:

- The URI is wrapped in `AnyUrl` (from pydantic) before being passed to the SDK. This ensures proper type handling.
- `session().read_resource(...)` is the underlying SDK call.
- The response's `contents` is a **list**. You typically take the first element — it contains the actual data plus metadata (including the MIME type).

The return type is annotated `Any` because different resources return different Python types (strings, dicts, lists, binary) depending on their MIME type.

---

## Parsing by MIME Type

Because resources can return heterogeneous data, the client must branch on MIME type:

```python
if isinstance(resource, types.TextResourceContents):
    if resource.mimeType == "application/json":
        return json.loads(resource.text)

    return resource.text
```

Two cases are covered in the lesson:

1. **`application/json`** — the server returned structured data. Parse `resource.text` with `json.loads` and return a Python object (dict or list).
2. **`text/plain`** (and other text types) — return `resource.text` as-is.

The MIME type is the hint the server gave you via `@mcp.resource(mime_type=...)`. It is the contract that lets the client parse correctly without guessing.

For other content types (binary, images), you would add more branches — but the lesson focuses on text and JSON, which covers the document-mention use case.

---

## Required Imports

Two imports are needed to make this work:

```python
import json
from pydantic import AnyUrl
```

- `json` — parsing JSON bodies
- `AnyUrl` — pydantic's URL type; `read_resource` expects a typed URL, not a raw string

Missing either will surface as a type error or runtime exception.

---

## Testing Resource Access via CLI

The end-to-end test is through the CLI application. When the user types something like "What's in the @report.pdf document?", the system:

1. Shows available resources in an autocomplete list (powered by `list_resources` or similar).
2. Lets the user pick one.
3. Fetches the resource content automatically (via `read_resource`).
4. Includes that content in the prompt sent to Claude.

Claude then answers the question with the document already in context — no tool call needed.

---

## Integration Into the Application

A crucial design point: the MCP client code you write gets consumed by **other parts of the app**. `read_resource` becomes a building block. Higher-level components call it to:

- Fetch document contents for prompt injection
- Populate @mention autocomplete
- Integrate resource data into prompts

This separation of concerns matters:

| Layer | Responsibility |
|-------|---------------|
| MCP client | Talk to MCP server, parse responses |
| Application | Decide when to fetch, where to inject |
| Prompt builder | Format the final message to Claude |

The client is intentionally dumb — it just reads. Business logic stays in the application layer.

---

## Why This Is More Efficient Than a Tool Call

Compare two approaches for the same user intent ("read report.pdf"):

| Approach | Round trips | Content blocks | Determinism |
|----------|-------------|----------------|-------------|
| Tool call (`read_doc_contents`) | 2 (tool_use + tool_result) | tool_use, tool_result, final text | Claude decides whether to call |
| Resource fetch (`read_resource`) | 1 | prompt text only | App guarantees the fetch happens |

For explicit user-driven context ("I am @mentioning this document"), the resource path is strictly better: fewer API calls, fewer tokens, faster response.

---

## Common Mistakes

1. **Passing a raw string URI** — `read_resource` requires an `AnyUrl`. Skipping `AnyUrl(uri)` causes type errors inside the SDK.
2. **Forgetting to branch on MIME type** — returning `resource.text` unconditionally turns JSON into a raw string, breaking downstream parsing.
3. **Assuming `contents` has exactly one element** — the SDK returns a list. The first element is typical but not guaranteed — document this assumption.
4. **Double-parsing JSON** — if the server already serialized via `mime_type="application/json"`, the text is JSON; calling `json.loads` is correct. Do not wrap it again on the server side.
5. **Putting business logic in `read_resource`** — keep the client thin. "When to fetch" belongs in the app layer.

> **Key Insight**
>
> `read_resource` is the symmetric mirror of `@mcp.resource()` — what one side serializes, the other side deserializes. MIME type is the glue. Understanding this symmetry is what makes resource-backed features feel like a clean data channel instead of a makeshift tool call. Every MCP client you build will have this same three-line pattern: call `read_resource`, take `contents[0]`, branch on `mimeType`.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: `read_resource` is the client-side complement to `@mcp.resource()`; know the method signature, the use of `AnyUrl`, and the MIME-type branching pattern.
- **D1 (Agentic Architecture)**: resources inject context into the agent loop without costing a tool call — they shorten the loop and increase determinism.
- Exam pattern: "What type must you pass to `session.read_resource()`?" → `AnyUrl` (from pydantic), not a raw string.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the core client method for reading a resource? | `async def read_resource(self, uri: str)` which calls `self.session().read_resource(AnyUrl(uri))`. |
| What type must the URI be wrapped in before passing to the SDK? | `AnyUrl` from `pydantic`. |
| What does the response's `contents` field contain? | A list of resource content objects; you typically use `result.contents[0]`. |
| How do you parse a JSON-typed resource response? | Check `resource.mimeType == "application/json"` and return `json.loads(resource.text)`. |
| How do you parse a text-typed resource response? | Return `resource.text` as-is. |
| What two imports does the client need for resource access? | `import json` and `from pydantic import AnyUrl`. |
| Why are resources more efficient than tool calls for explicit context injection? | One API round trip instead of two — the data is inlined in the initial prompt, skipping the tool_use / tool_result loop. |
| Who decides to call `read_resource`? | The application (based on user action or policy), not Claude — Claude never sees the URI, only the resulting text. |
