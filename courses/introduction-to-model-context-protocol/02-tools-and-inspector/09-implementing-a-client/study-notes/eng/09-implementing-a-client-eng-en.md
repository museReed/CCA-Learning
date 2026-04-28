# Implementing a Client — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | T2.2 Implement MCP client-server communication; T2.4 Handle tool discovery and execution flows |
| Source | introduction-to-model-context-protocol / 02-tools-and-inspector / Lesson 09 |

---

## One-Liner

Building the MCP client side requires the MCP Client class and ClientSession from the SDK, with two essential methods: `list_tools()` for discovery and `call_tool()` for execution.

---

## The Client Architecture

The MCP client is composed of two main SDK classes:

```python
from mcp import ClientSession
from mcp.client import Client
```

**Client** — Manages the connection lifecycle (connecting, disconnecting, transport management).

**ClientSession** — Provides the methods for interacting with the MCP server (`list_tools()`, `call_tool()`, etc.).

These two classes work together: the Client establishes the connection, and the ClientSession uses that connection to communicate.

```python
class MCPClient:
    def __init__(self):
        self.client = Client()
        self.session: ClientSession | None = None

    async def connect(self, server_script: str):
        """Connect to an MCP server."""
        server_params = StdioServerParameters(
            command="python",
            args=[server_script]
        )
        # Establish connection
        stdio_transport = await self.client.connect_stdio(server_params)
        self.session = ClientSession(*stdio_transport)
        await self.session.initialize()
```

> **Key Insight**
> The `initialize()` call is critical. It performs the MCP handshake where client and server negotiate capabilities. Without it, subsequent calls will fail.

---

## The Two Essential Methods

### list_tools() — Discovery

```python
async def discover_tools(self):
    """Discover available tools from the MCP server."""
    response = await self.session.list_tools()

    # response.tools is a list of Tool objects
    for tool in response.tools:
        print(f"Tool: {tool.name}")
        print(f"  Description: {tool.description}")
        print(f"  Schema: {tool.inputSchema}")

    return response.tools
```

`list_tools()` returns a `ListToolsResult` containing an array of tool definitions. Each tool has:

- `name` — The tool identifier (e.g., "read_doc_contents")
- `description` — What the tool does (from the server's docstring)
- `inputSchema` — JSON schema for the tool's parameters

This is what you pass to Claude so it knows what tools are available.

### call_tool() — Execution

```python
async def execute_tool(self, tool_name: str, tool_input: dict):
    """Execute a tool on the MCP server."""
    result = await self.session.call_tool(tool_name, tool_input)

    # result.content contains the tool output
    return result.content
```

`call_tool()` takes two arguments:

- `tool_name` — Which tool to call (string)
- `tool_input` — The arguments for the tool (dict matching the inputSchema)

It returns a `CallToolResult` containing the tool's output.

> **Key Insight**
> The tool_name and tool_input typically come directly from Claude's tool_use response. Claude decides which tool to call and with what arguments; your client just routes that decision to the MCP server.

---

## Complete Client-Side Flow

Here is how the client integrates with Claude in the full agentic loop:

```python
import anthropic
from mcp import ClientSession

class AgenticMCPClient:
    def __init__(self):
        self.claude = anthropic.Anthropic()
        self.session: ClientSession = None  # Set during connect

    async def handle_query(self, user_query: str) -> str:
        # Step 1: Discover tools
        tools_response = await self.session.list_tools()
        claude_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            }
            for tool in tools_response.tools
        ]

        # Step 2: Send query + tools to Claude
        messages = [{"role": "user", "content": user_query}]
        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=claude_tools,
            messages=messages
        )

        # Step 3: Check if Claude wants to use a tool
        if response.stop_reason == "tool_use":
            tool_block = next(
                b for b in response.content
                if b.type == "tool_use"
            )

            # Step 4: Execute the tool via MCP
            tool_result = await self.session.call_tool(
                tool_block.name,
                tool_block.input
            )

            # Step 5: Send result back to Claude
            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_block.id,
                    "content": str(tool_result.content)
                }]
            })

            final_response = self.claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                tools=claude_tools,
                messages=messages
            )
            return final_response.content[0].text

        return response.content[0].text
```

The five key steps:

1. **Discover** — `list_tools()` gets available tools
2. **Present** — Tool schemas sent to Claude with the user query
3. **Decide** — Claude returns a `tool_use` block (or answers directly)
4. **Execute** — `call_tool()` runs the tool on the MCP server
5. **Interpret** — Claude receives the result and generates a final response

---

## Running the Client

```bash
uv run mcp_client.py
```

The `uv` runner handles dependency resolution and virtual environment management. When run, the client:

1. Connects to the specified MCP server
2. Discovers available tools
3. Enters an interactive loop where users can ask questions
4. Routes tool calls through MCP and responses through Claude

---

## Error Handling in the Client

```python
async def safe_call_tool(self, tool_name: str, tool_input: dict):
    try:
        result = await self.session.call_tool(tool_name, tool_input)
        if result.isError:
            return f"Tool error: {result.content}"
        return result.content
    except Exception as e:
        return f"MCP communication error: {str(e)}"
```

Key error scenarios:

- **Tool not found** — The tool name does not match any registered tool
- **Invalid input** — The tool_input does not match the expected schema
- **Server error** — The MCP server encounters an internal error
- **Transport error** — Connection to the MCP server is lost

> **Key Insight**
> Always check `result.isError` after `call_tool()`. A successful MCP round-trip can still contain a tool-level error. The transport succeeded but the tool execution failed.

---

## CCA Exam Relevance

This lesson completes the **Domain 2 (18%)** client-server picture:

- **Two SDK classes**: Know that Client handles connection and ClientSession handles communication
- **Two essential methods**: `list_tools()` for discovery, `call_tool()` for execution
- **The agentic loop**: Understand the five-step flow from discovery through Claude decision to final response
- **`uv run`**: Know this is how MCP clients are typically executed
- **Error handling**: Understand that `result.isError` catches tool-level errors even when transport succeeds

---

## Flashcards

| Front | Back |
|-------|------|
| What are the two main SDK classes for building an MCP client? | Client (manages connection lifecycle) and ClientSession (provides list_tools and call_tool methods). |
| What does `list_tools()` return? | A ListToolsResult containing an array of tool definitions, each with name, description, and inputSchema. |
| What two arguments does `call_tool()` take? | tool_name (string identifying which tool to call) and tool_input (dict matching the tool's inputSchema). |
| Where do tool_name and tool_input typically come from? | From Claude's tool_use response block. Claude decides which tool to call and with what arguments. |
| What does `session.initialize()` do? | Performs the MCP handshake where client and server negotiate capabilities. Required before any other MCP calls. |
| What are the five steps in the complete client-side agentic flow? | 1) Discover tools, 2) Present tools + query to Claude, 3) Claude decides tool use, 4) Execute tool via MCP, 5) Send result to Claude for final response. |
| How do you run an MCP client? | `uv run mcp_client.py` — uv handles dependency resolution and virtual environment management. |
| Why should you check `result.isError` after call_tool()? | A successful MCP transport round-trip can still contain a tool-level error. The connection worked but the tool itself failed. |
