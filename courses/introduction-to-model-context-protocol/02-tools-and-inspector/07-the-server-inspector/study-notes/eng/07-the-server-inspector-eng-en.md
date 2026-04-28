# The Server Inspector — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | T2.6 Test and debug MCP servers; T2.7 Validate tool behavior before deployment |
| Source | introduction-to-model-context-protocol / 02-tools-and-inspector / Lesson 07 |

---

## One-Liner

The MCP Inspector is a browser-based debugging tool that lets you test MCP servers interactively without building a full application, running at localhost:6274 via `mcp dev`.

---

## What Is the MCP Inspector?

The MCP Inspector is a development tool provided by the MCP SDK that gives you a browser-based UI for testing MCP servers. Instead of building a complete application with a client, Claude integration, and user interface just to test whether your tools work, you can use the Inspector to directly interact with your MCP server.

```bash
# Launch the Inspector against your MCP server
mcp dev mcp_server.py
```

This single command:

1. Starts your MCP server as a subprocess
2. Launches a web UI at `http://localhost:6274`
3. Establishes the MCP connection automatically

> **Key Insight**
> The Inspector eliminates the chicken-and-egg problem of MCP development. You do not need a working client to test your server, and you do not need a working server to understand what a server exposes. It decouples development of the two sides.

---

## The Inspector Interface

When you open `localhost:6274` in your browser, you see the Inspector UI with several key components:

### Connect Button

At the top of the interface is a **Connect** button. Clicking it establishes the MCP connection between the Inspector (acting as a client) and your server. The connection status indicator shows whether you are connected.

### Three Main Tabs

The Inspector organizes MCP server capabilities into three tabs:

| Tab | What It Shows |
|-----|--------------|
| **Resources** | Data sources the server exposes (files, databases, etc.) |
| **Tools** | Executable functions the server provides |
| **Prompts** | Reusable prompt templates the server offers |

For this lesson, the **Tools** tab is the primary focus.

### Tools Tab

Clicking the Tools tab shows a list of all tools your server exposes. Each tool entry displays:

- Tool name
- Tool description (from the docstring)
- Input parameters with their types and descriptions

You can select any tool, enter parameter values in the input fields, and click **Run Tool** to execute it.

---

## Testing Workflow

The standard development workflow with the Inspector follows this pattern:

### 1. Write Your Tool

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-tools")

@mcp.tool()
def calculate_total(prices: list[float], tax_rate: float = 0.1) -> float:
    """Calculate the total price including tax.

    Args:
        prices: List of individual item prices.
        tax_rate: Tax rate as a decimal (default 0.1 = 10%).
    """
    subtotal = sum(prices)
    return subtotal * (1 + tax_rate)
```

### 2. Launch the Inspector

```bash
mcp dev mcp_server.py
```

### 3. Connect and Test

1. Open `http://localhost:6274`
2. Click **Connect**
3. Navigate to the **Tools** tab
4. Select `calculate_total`
5. Enter test inputs: `prices: [10.0, 20.0, 30.0]`, `tax_rate: 0.08`
6. Click **Run Tool**
7. Verify the output: `64.8`

### 4. Iterate

If the output is wrong or the tool errors, fix your code and re-test. The Inspector maintains the connection, so you can test repeatedly without restarting.

> **Key Insight**
> State persists between tool calls in the Inspector. If your first tool call creates a file, a subsequent tool call can read that file. This lets you test multi-step workflows without resetting between each call.

---

## State Persistence Between Calls

One of the Inspector's most useful features is that state persists across tool calls within a session. This is critical for testing tools that have side effects:

```python
@mcp.tool()
def create_note(title: str, content: str) -> str:
    """Create a new note."""
    notes_db[title] = content
    return f"Note '{title}' created"

@mcp.tool()
def read_note(title: str) -> str:
    """Read an existing note."""
    return notes_db.get(title, "Note not found")
```

In the Inspector, you can:

1. Call `create_note(title="meeting", content="Discuss Q3 goals")`
2. Then call `read_note(title="meeting")`
3. Verify it returns "Discuss Q3 goals"

This sequential testing capability is essential for verifying tools that work together.

---

## Debugging with the Inspector

The Inspector is particularly valuable for debugging these common issues:

**Schema problems**: If your tool's input schema is wrong (missing fields, wrong types), you will see it immediately in the Tools tab. The Inspector displays exactly what schema your server exposes.

**Parameter descriptions**: You can verify that parameter descriptions are clear and helpful by reading them in the Inspector UI — the same descriptions Claude will see.

**Error handling**: Send invalid inputs deliberately to verify your error messages are informative and not just stack traces.

**Return values**: Verify that tool outputs are structured and informative enough for Claude to interpret.

---

## Essential Dev Workflow Position

The Inspector fits into the MCP development workflow as follows:

```
Write Tool Code  →  Test with Inspector  →  Fix Issues  →  Integrate with Client
                          ↑                       |
                          └───────────────────────┘
```

You should not move to client integration until all tools pass Inspector testing. This saves significant debugging time because Inspector issues (schema, parameters, errors) are much easier to diagnose than client-side issues where the problem could be in the client code, the transport layer, or the server.

> **Key Insight**
> The Inspector is not just a convenience — it is an essential quality gate. Skipping Inspector testing and going straight to client integration is like skipping unit tests and going straight to integration tests. You will spend more time debugging, not less.

---

## CCA Exam Relevance

This lesson covers **Domain 2 (18%)** testing and debugging:

- **`mcp dev` command**: Know that this launches the Inspector against an MCP server file
- **localhost:6274**: The default Inspector URL
- **Three tabs**: Resources, Tools, Prompts — know what each shows
- **State persistence**: Understand that tool state persists between calls within a session
- **Development workflow**: Inspector sits between writing code and client integration

---

## Flashcards

| Front | Back |
|-------|------|
| What command launches the MCP Inspector? | `mcp dev mcp_server.py` — it starts the server and opens a browser-based testing UI. |
| What URL does the MCP Inspector run on? | `http://localhost:6274` |
| What are the three tabs in the MCP Inspector? | Resources (data sources), Tools (executable functions), and Prompts (reusable templates). |
| Does state persist between tool calls in the Inspector? | Yes. If one tool call creates data, subsequent calls can access it within the same session. |
| Why should you test with the Inspector before integrating with a client? | Inspector issues (schema, parameters, errors) are much easier to diagnose than client-side issues where problems could be in multiple layers. |
| What can you verify by reading the Tools tab in the Inspector? | Tool names, descriptions, parameter types, parameter descriptions, and input schemas — exactly what Claude will see. |
| How do you test error handling with the Inspector? | Send deliberately invalid inputs and verify the error messages are informative and contextual rather than raw stack traces. |
| What is the standard MCP development workflow? | Write tool code → Test with Inspector → Fix issues → Integrate with client. Do not skip the Inspector step. |
