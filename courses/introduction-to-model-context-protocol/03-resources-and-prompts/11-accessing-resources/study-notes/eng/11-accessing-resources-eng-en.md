# Accessing Resources — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP client implementation), 2.4 (resource consumption patterns), 2.5 (content type handling) |
| Source | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 11 |

---

## One-Liner

Client-side resource access uses `read_resource()` with `AnyUrl`, processes the `ReadResourceResult.contents` list, and branches on MIME type to parse JSON or return raw text.

---

## The Client-Side Resource Pattern

While Lesson 10 covered how to define resources on the server, this lesson focuses on the client code that consumes those resources. The key function is `read_resource()`.

### Core Implementation

```python
import json
from pydantic import AnyUrl

async def read_resource(self, uri: str) -> Any:
    result = await self.session().read_resource(AnyUrl(uri))
    resource = result.contents[0]

    if isinstance(resource, types.TextResourceContents):
        if resource.mimeType == "application/json":
            return json.loads(resource.text)

    return resource.text
```

### Line-by-Line Breakdown

1. **`AnyUrl(uri)`** — Pydantic's URL validator. Accepts any URI scheme (`docs://`, `file://`, custom schemes). Validates format at parse time.
2. **`result.contents[0]`** — The response has a `contents` list. We take the first element since a single resource request typically returns one item.
3. **`isinstance(resource, types.TextResourceContents)`** — Type check to confirm we have text content (vs. binary `BlobResourceContents`).
4. **MIME type branch** — If `application/json`, parse with `json.loads()`. Otherwise, return the raw `.text` string.

---

## Response Structure Deep Dive

The `ReadResourceResult` returned by the server has this shape:

```
ReadResourceResult
  └── contents: list[TextResourceContents | BlobResourceContents]
        └── [0]
              ├── uri: str
              ├── mimeType: str
              ├── text: str  (for TextResourceContents)
              └── blob: bytes (for BlobResourceContents)
```

Key design decisions:
- **`contents` is a list** — though typically one item, the protocol supports returning multiple content blocks
- **Two content types** — `TextResourceContents` for text-based data, `BlobResourceContents` for binary
- **MIME type lives on the content object** — not on the result wrapper, because each content block can have a different type

---

## MIME Type Handling Strategy

A production-ready client should handle more MIME types than the minimal example:

```python
async def read_resource(self, uri: str) -> Any:
    result = await self.session().read_resource(AnyUrl(uri))
    resource = result.contents[0]

    if isinstance(resource, types.TextResourceContents):
        mime = resource.mimeType or "text/plain"
        if mime == "application/json":
            return json.loads(resource.text)
        elif mime in ("text/plain", "text/markdown", "text/html"):
            return resource.text
        else:
            return resource.text  # fallback for unknown text types

    # BlobResourceContents for binary data
    return resource.blob
```

| MIME Type | Parse Strategy | Return Type |
|-----------|---------------|-------------|
| `application/json` | `json.loads(resource.text)` | `dict` or `list` |
| `text/plain` | `resource.text` | `str` |
| `text/markdown` | `resource.text` | `str` |
| Binary types | `resource.blob` | `bytes` |

---

## The `@` Autocomplete UX Pattern

From the user's perspective, resource access powers the `@mention` workflow:

1. **User types `@`** — client calls `list_resources()` to populate autocomplete dropdown
2. **User navigates with arrow keys** — selects desired resource from list
3. **User presses space to confirm** — client calls `read_resource(selected_uri)`
4. **Content injected into prompt** — resource content becomes part of the prompt context, no tool call required

This is fundamentally different from tools: the data is in the prompt **before** Claude starts reasoning, resulting in faster and more accurate responses.

---

## Testing Resource Access

In the MCP Inspector:
1. Navigate to the **Resources** tab
2. Click a direct resource to read it immediately
3. For templated resources, fill in parameter values
4. Inspect the response structure: URI, MIME type, content

In your CLI client:
1. Type `@` to trigger autocomplete
2. Select a resource
3. Verify the content appears in the prompt context
4. Confirm Claude can reference the content in its response

---

## Common Mistakes

1. **Forgetting `AnyUrl()` wrapper** — passing a raw string instead of wrapping it with Pydantic's `AnyUrl` will cause a type error
2. **Not handling the `contents` list** — accessing `result.text` directly instead of `result.contents[0].text`
3. **Missing JSON parsing** — treating `application/json` content as raw text, leading to string-encoded JSON in the prompt
4. **Ignoring binary resources** — not handling `BlobResourceContents` for non-text data

> **Key Insight**
>
> Resource content goes directly into the prompt — it is not processed through a tool call. This means the data is available to Claude as first-class context, reducing latency and avoiding the model needing to "ask" for information. For the CCA exam, remember: resources are **app-controlled** and inject context **before** model reasoning begins.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: Know the `read_resource()` pattern — `AnyUrl`, `contents[0]`, MIME type branching. This is testable implementation detail.
- **D1 (Agentic Architecture)**: Understand that resources inject context into prompts without tool calls, which is more efficient for known data needs.
- Scenario questions may describe a feature where data "appears in the chat" or "is available without Claude asking" — this is resource access, not tool invocation.

---

## Flashcards

| Front | Back |
|-------|------|
| What Pydantic type wraps the URI in `read_resource()`? | `AnyUrl` — it validates URI format and accepts any scheme (docs://, file://, etc.) |
| How do you access the actual content from a `ReadResourceResult`? | `result.contents[0]` — the contents field is a list, take the first element |
| How should a client handle `application/json` MIME type from a resource? | Call `json.loads(resource.text)` to parse the JSON string into a Python dict/list |
| What happens to resource content when a user selects an `@mention`? | It is injected directly into the prompt context — no tool call is triggered |
| What are the two content types in MCP resource responses? | `TextResourceContents` (for text/JSON data) and `BlobResourceContents` (for binary data) |
| Why is resource access faster than tool-based data fetching? | Resource data is in the prompt before Claude starts reasoning — no extra round-trip needed |
| What triggers the autocomplete list in the `@mention` pattern? | The client calls `list_resources()` when the user types `@` |
| What is the default fallback when MIME type is not `application/json`? | Return `resource.text` as a raw string |
