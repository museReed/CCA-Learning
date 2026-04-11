# Defining Tools with MCP — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.1 (tool schema design), 2.3 (MCP primitives: tools), 1.2 (agent loop integration) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 64 |

---

## One-Liner

Lesson 64 shows how the Python MCP SDK (`FastMCP`) collapses tool authoring into decorators plus type hints — the SDK auto-generates the JSON schema from your function signature and Pydantic `Field` metadata, so you write normal Python instead of hand-rolled JSON Schema.

---

## Why the SDK Matters

In Ch04 tool use, every tool definition meant writing the same verbose JSON schema:

```python
tools = [{
    "name": "read_doc_contents",
    "description": "...",
    "input_schema": {
        "type": "object",
        "properties": {
            "doc_id": {"type": "string", "description": "..."}
        },
        "required": ["doc_id"]
    }
}]
```

That's fine for one tool and painful for twenty. The Python MCP SDK (`mcp.server.fastmcp.FastMCP`) uses a decorator-driven pattern that:

- Takes a plain Python function
- Reads its type hints and `Field(description=...)` annotations
- Generates the equivalent JSON schema automatically
- Registers the tool with the MCP server

The result: tool definition shrinks to a few lines that read like normal Python code.

---

## Setting Up the Server

Creating an MCP server is one import and one line:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")
```

- `"DocumentMCP"` is the server's name (identifier surfaced to clients).
- `log_level="ERROR"` silences noisy informational logs during development.

The `mcp` object is the registry onto which you attach tools (and, in later lessons, resources and prompts).

---

## The In-Memory Document Store

The lesson uses a plain Python dict as the "database":

```python
docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditure",
    "outlook.pdf": "This document presents the projected future performance of the",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment"
}
```

Keys are document IDs, values are the text contents. No persistence — documents live in process memory. This deliberately keeps the focus on MCP authoring rather than DB plumbing.

---

## Tool 1: `read_doc_contents`

The decorator-driven read tool:

```python
@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string."
)
def read_document(
    doc_id: str = Field(description="Id of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    return docs[doc_id]
```

What's happening under the hood:

| Source element | Becomes |
|----------------|---------|
| `@mcp.tool(name=..., description=...)` | Top-level tool metadata in the MCP schema |
| `doc_id: str` type hint | `{"type": "string"}` in the generated JSON Schema |
| `Field(description="...")` | The `description` for the `doc_id` property |
| Function body | The callable executed when Claude issues `CallToolRequest` |
| `raise ValueError(...)` | Surfaces as a tool error that Claude can read and potentially recover from |

Note that the function name (`read_document`) is independent from the MCP tool name (`read_doc_contents`); the decorator's `name=` argument is authoritative.

---

## Tool 2: `edit_document`

The second tool is a simple find-and-replace editor:

```python
@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string."
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace."),
    new_str: str = Field(description="The new text to insert in place of the old text.")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
```

Key engineering details:

- Three parameters, each annotated with `Field(description=...)` so Claude understands their roles.
- The `old_str` description explicitly notes "must match exactly, including whitespace" — this is Claude-facing documentation that reduces flaky edits.
- Implementation uses Python's built-in `str.replace`, which replaces **all** occurrences; if uniqueness matters in your real system, add a match-count check.
- The function has no explicit return; it mutates the dict in place.

---

## Error Handling via `ValueError`

Both tools raise `ValueError` when they receive a bad `doc_id`. The MCP SDK converts these into tool error responses that Claude receives in the next `tool_result` block, giving it a chance to:

- Apologize and ask the user for a valid ID
- Retry with a different ID if one looks similar
- Escalate to a "can't find this doc" final response

This is the **structured error** pattern: you give Claude a readable explanation instead of a silent failure, and the agent loop can incorporate the error into its reasoning.

---

## Key Benefits of the SDK Approach

The lesson highlights five wins over hand-written tool schemas:

1. **Automatic JSON Schema generation** from Python type hints.
2. **Clean, readable code** — the tool body looks like normal Python.
3. **Built-in parameter validation** via Pydantic `Field`.
4. **Reduced boilerplate** — no manual `{"type": "object", "properties": ...}` dictionaries.
5. **Type safety and IDE support** during development.

The meta-point: the SDK lets you focus on **business logic** (what the tool does) while the protocol (schema, serialization) is handled for you.

---

## Advanced Considerations Not Shown in the Lesson

The source is intentionally minimal, but real servers should also consider:

| Concern | Why |
|---------|-----|
| Return type hints | Fully typed returns let FastMCP describe the result shape |
| Optional parameters with defaults | Use `Field(default=..., description=...)` |
| Long descriptions | The `description` is Claude's instruction manual — invest in clarity |
| Side-effect logging | `edit_document` mutates state; in prod you'd audit-log every call |
| Concurrency safety | The dict is shared state; in prod use a lock or an async-safe store |

None of these are required to complete the course project, but they distinguish "works in demo" from "ships to users".

---

## Common Mistakes

1. **Forgetting `Field` descriptions.** Without them Claude only sees the parameter name — tool quality drops sharply.
2. **Using the function name instead of the MCP tool name.** The decorator's `name=` is what Claude sees; your function name is internal.
3. **Letting errors bubble as unhandled exceptions.** `ValueError` is converted into a readable tool error; arbitrary exceptions are noisier and less recoverable.
4. **Assuming tool names and schemas are stable.** If you rename or reshape a tool, clients (including the MCP inspector in lesson 65) need to re-list tools.
5. **Relying on the description doing prompt engineering.** Keep descriptions truthful; don't embed contradictory instructions that confuse Claude.

> **Key Insight**
>
> The Python MCP SDK turns tool authoring into normal Python code with two sprinkles of metadata (`@mcp.tool(...)` + `Field(description=...)`). That is the central productivity win of MCP: you trade hand-written JSON Schema for decorated functions, and the framework handles the protocol. Every tool you add later in the course follows this exact pattern.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: Know `FastMCP("Name", log_level=...)`, the `@mcp.tool(name, description)` decorator, and how `Field(description=...)` populates the schema.
- **D1 (Agentic Architecture)**: Understand how a `ValueError` is surfaced to Claude as a recoverable tool error in the agent loop.
- Scenario questions may ask: "how does the SDK know to require `doc_id`?" — answer: because it's a positional parameter with no default, the SDK marks it required in the schema.

---

## Flashcards

| Front | Back |
|-------|------|
| Which class initializes an MCP server in the Python SDK? | `FastMCP` from `mcp.server.fastmcp` |
| How do you declare a tool? | Decorate a function with `@mcp.tool(name=..., description=...)` |
| How do you document a parameter for Claude? | Use `Pydantic`'s `Field(description="...")` as the parameter default |
| What does the SDK generate from your type hints? | The JSON Schema (including `type`, `properties`, and `required`) |
| How do the two demo tools persist data? | They don't — documents live in a module-level Python dict (in-memory) |
| What happens if `read_doc_contents` is called with an unknown doc_id? | The tool raises `ValueError`, which is surfaced to Claude as a tool error |
| How many tools does the demo server expose? | Two — `read_doc_contents` and `edit_document` |
| What are the five benefits of the SDK approach listed in the lesson? | Auto JSON Schema, clean code, Pydantic validation, less boilerplate, type safety/IDE support |
