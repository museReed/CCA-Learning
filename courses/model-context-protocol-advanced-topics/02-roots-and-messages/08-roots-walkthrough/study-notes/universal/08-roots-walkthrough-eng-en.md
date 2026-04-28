# Roots Walkthrough — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Model Context Protocol (23%), D4 — Security & Guardrails (15%) |
| Task Statements | 2.2 (MCP primitives — roots), 4.3 (access control) |
| Source | model-context-protocol-advanced-topics / 02-roots-and-messages / Lesson 08 |

---

## One-Liner

Roots are client-defined `file://` URIs that tell an MCP server which directories it is allowed to access. The client provides them via a callback, and the server must implement its own authorization logic to enforce access boundaries.

---

## What Are Roots?

Roots are the MCP mechanism for **file system access control**. They answer the question: "Which directories should this server be able to see?"

Key characteristics:
- Roots are **defined by the client** (typically from user input)
- They use `file://` URI format
- The server **requests** roots from the client at runtime (not hardcoded)
- The MCP SDK does **NOT** automatically enforce root boundaries -- you must implement that yourself

---

## Step 1: Defining Roots from User Input

```python
# main.py
import sys

async def main():
    # Get root directories from command line arguments
    root_paths = sys.argv[1:]
    if not root_paths:
        print("Usage: uv run main.py <root1> [root2] ...")
        sys.exit(1)

    # Pass roots to the MCP client
    doc_client = await stack.enter_async_context(
        MCPClient(
            command="uv", args=["run", "mcp_server.py"], roots=root_paths
        )
    )
```

Ideally, the user dictates which directories the server can access. The program accepts CLI arguments as paths and passes them to the `MCPClient`.

---

## Step 2: Creating Root Objects

```python
# mcp_client.py
from mcp.types import Root, ListRootsResult
from pydantic import FileUrl
from pathlib import Path

def _create_roots(self, root_paths: list[str]) -> list[Root]:
    """Convert path strings to Root objects."""
    roots = []
    for path in root_paths:
        p = Path(path).resolve()
        file_url = FileUrl(f"file://{p}")
        roots.append(Root(uri=file_url, name=p.name or "Root"))
    return roots
```

According to the MCP spec, all roots must have a URI beginning with `file://`. This function converts user-provided paths into proper `Root` objects.

---

## Step 3: Roots Callback

```python
# mcp_client.py
async def _handle_list_roots(
    self, context: RequestContext["ClientSession", None]
) -> ListRootsResult | ErrorData:
    """Callback for when server requests roots."""
    return ListRootsResult(roots=self._roots)
```

The client does not immediately send roots to the server. Instead, the server requests them at a future point. The callback returns roots inside a `ListRootsResult` object.

This callback is passed to `ClientSession`:

```python
self._session = await self._exit_stack.enter_async_context(
    ClientSession(
        _stdio,
        _write,
        list_roots_callback=self._handle_list_roots
        if self._roots
        else None,
    )
)
```

---

## Step 4: Server Accessing Roots

```python
# mcp_server.py
@mcp.tool()
async def list_roots(ctx: Context):
    """List all accessible root directories."""
    roots_result = await ctx.session.list_roots()
    client_roots = roots_result.roots
    return [file_url_to_path(root.uri) for root in client_roots]
```

Roots are accessed by calling `ctx.session.list_roots()`. This sends a request back to the client, which triggers the root-listing callback.

The server uses roots in two scenarios:
1. **Authorizing file access** -- Before a tool reads or writes a file
2. **Resolving paths for the LLM** -- When Claude needs to find where a file lives (e.g., "read todos.txt")

---

## Step 5: Implementing Access Control

**Critical**: The MCP SDK does NOT enforce root boundaries. You must implement that check yourself.

```python
# mcp_server.py
async def is_path_allowed(requested_path: Path, ctx: Context) -> bool:
    roots_result = await ctx.session.list_roots()
    client_roots = roots_result.roots

    if not requested_path.exists():
        return False

    if requested_path.is_file():
        requested_path = requested_path.parent

    for root in client_roots:
        root_path = file_url_to_path(root.uri)
        try:
            requested_path.relative_to(root_path)
            return True
        except ValueError:
            continue

    return False
```

The authorization function:
1. Gets the list of roots from the client
2. Checks if the requested path exists
3. For files, checks the parent directory
4. Uses `relative_to()` to verify the path is within an allowed root
5. Returns `False` if no root matches

---

## Step 6: Using Authorization in Tools

```python
@mcp.tool()
async def convert_video(input_path: str, format: str, *, ctx: Context):
    """Convert an MP4 video file to another format."""
    input_file = VideoConverter.validate_input(input_path)

    # Ensure the input file is contained in a root
    if not await is_path_allowed(input_file, ctx):
        raise ValueError(f"Access to path is not allowed: {input_path}")

    return await VideoConverter.convert(input_path, format)
```

Every tool that accesses the file system should call `is_path_allowed()` before proceeding.

---

## CCA Exam Relevance

- Roots are a **D2 primitive** (Task 2.2) and a **D4 security concern** (Task 4.3)
- The most critical exam point: **MCP SDK does NOT enforce root boundaries** -- you must implement authorization yourself
- The callback pattern (client provides roots on-demand via `list_roots_callback`) is frequently tested
- Root URIs must use the `file://` scheme
- Expect scenario questions where access control is missing and you must identify the vulnerability
- The `relative_to()` pattern for path validation is a common implementation detail tested in D4

---

## Flashcards

| # | Question | Answer |
|---|----------|--------|
| 1 | Who defines the roots in MCP? | The **client** defines roots, typically based on user input |
| 2 | What URI scheme must roots use? | `file://` |
| 3 | Does the MCP SDK automatically enforce root boundaries? | **No** -- you must implement authorization logic yourself |
| 4 | How does the server request roots from the client? | By calling `ctx.session.list_roots()`, which triggers the client's `list_roots_callback` |
| 5 | What does the roots callback return? | A `ListRootsResult` object containing the list of `Root` objects |
| 6 | What Python method is used to check if a path is within a root? | `Path.relative_to()` -- raises `ValueError` if the path is outside the root |
| 7 | In what two scenarios does the server use roots? | 1) Authorizing file/folder access, 2) Resolving paths for the LLM |
| 8 | Where is the `list_roots_callback` registered? | In the `ClientSession` constructor |
