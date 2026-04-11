# The Server Inspector — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.3 (MCP primitives), 2.1 (tool schema design), 1.2 (agent loop integration) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 65 |

---

## One-Liner

The MCP Inspector is a browser-based development tool — shipped with the Python MCP SDK as `mcp dev` — that lets you `list` and `call` your server's tools, resources, and prompts directly, without wiring the server up to Claude or a real application first.

---

## The Problem: Debugging Feedback Loops

When you build an MCP server, you have two ways to exercise its tools:

| Path | Feedback loop |
|------|---------------|
| Wire it into a full Claude-based application | Slow, noisy, mixes MCP bugs with prompt/agent bugs |
| Exercise it directly via the MCP protocol | Fast, isolated, reveals MCP bugs in seconds |

The first path is what you eventually need, but it is the worst place to debug. You don't know if a failure came from your tool, your prompt, Claude's choice of tool, or your agent loop. The **Inspector** collapses the feedback loop by giving you the second path out of the box.

---

## Starting the Inspector

From an activated Python environment (check your project's README for the exact command), run:

```bash
mcp dev mcp_server.py
```

This command:

1. Starts a development server on **port 6277**.
2. Prints a local URL for the Inspector UI.
3. Loads your MCP server code so its tools, resources, and prompts are discoverable.

You then open the URL in your browser and land on the **MCP Inspector dashboard**.

> Note: the lesson explicitly says the Inspector is "actively being developed", so the exact UI may differ from the course screenshots. The **capabilities** — list tools, call tools, view results — remain the same.

---

## Connecting and Discovering Tools

The Inspector workflow is driven from the left-hand sidebar. The core steps:

1. **Click "Connect"** — establishes the MCP protocol session with your server.
2. **Navigate to "Tools"** — switches to the tools view in the navigation bar.
3. **Click "List Tools"** — sends a `ListToolsRequest` and renders the response.
4. **Select a tool** — opens a form view for that tool's input schema.
5. **Fill in parameters** — the form is generated from your Python type hints + `Field(description=...)`.
6. **Click "Run Tool"** — sends a `CallToolRequest` and shows the result inline.

Every interaction maps 1:1 to a real MCP protocol message, so what you test in the Inspector is exactly what a real MCP client would see.

Besides Tools, the navigation bar also exposes sections for **Resources** and **Prompts** (covered in later lessons), letting you test all three primitives from one UI.

---

## A Worked Example: Exercising the Document Tools

Using the server from Lesson 64, here is how you would verify both tools from the Inspector without ever booting the chatbot:

### 1. Read a Document

- Tool: `read_doc_contents`
- Parameters: `doc_id = "deposition.md"`
- Expected result: `"This deposition covers the testimony of Angela Smith, P.E."`

### 2. Edit and Re-Read

- Tool: `edit_document`
- Parameters: `doc_id = "deposition.md"`, `old_str = "Angela Smith"`, `new_str = "Jane Doe"`
- Inspector confirms the call completed.

Immediately after the edit, re-run `read_doc_contents` with the same ID — you should see the text has been replaced. This **chained verification** pattern is a low-cost way to check that mutation tools actually work.

Because documents live in an in-memory dict, restarting the server wipes the changes. That's a feature during debugging — every session starts from a clean state.

---

## The Development Loop Enabled

The Inspector creates a tight, repeatable loop:

```
┌─────────────────────────┐
│ 1. Edit mcp_server.py   │
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 2. Restart `mcp dev`    │   (or rely on auto-reload)
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 3. List Tools in UI     │
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 4. Run Tool with inputs │
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 5. Inspect results      │
└───────────┬─────────────┘
            ▼
         (repeat)
```

Each iteration touches only the MCP server — no Claude API calls, no prompt engineering, no chat loop. That isolation is precisely what makes the Inspector valuable.

---

## Why This Matters Architecturally

The Inspector is an admission that **MCP is a protocol**, not a Claude-specific feature. A protocol needs a generic client for debugging, independent of the specific consumer (Claude, other LLMs, or automation). `mcp dev` is that generic client.

Concretely:

| Without Inspector | With Inspector |
|-------------------|----------------|
| Every test requires a Claude API key | Works offline from Claude |
| Tool bugs mask prompt bugs | Tool bugs isolated |
| Feedback loop: minutes | Feedback loop: seconds |
| You can't validate tool schemas without a chatbot | Schemas render as forms instantly |

---

## What the Inspector Does NOT Do

It is important to be clear about the boundaries:

| Capability | In the Inspector? |
|------------|-------------------|
| Exercise tools, resources, prompts | Yes |
| Render auto-generated schemas as forms | Yes |
| Call Claude with the resulting tool | No — use the full chatbot for that |
| Replace end-to-end testing | No — still run integration tests |
| Deploy your server | No — `mcp dev` is dev-only |

The Inspector's value is in **isolating MCP behavior** from LLM behavior. Once your tools pass in the Inspector, you move on to wiring them into your agent.

---

## Common Mistakes

1. **Skipping the Inspector and going straight to chatbot integration.** You lose the isolated feedback loop and end up debugging two layers at once.
2. **Not clicking "Connect" first.** The left-side Connect button actually starts the session; without it, "List Tools" returns nothing.
3. **Assuming UI stability.** The lesson warns the Inspector UI is "actively being developed" — learn the concepts (list, call, chain), not the exact pixels.
4. **Forgetting the port.** Default is `6277`; if it's taken, the command will tell you.
5. **Testing only the happy path.** Put in a bogus `doc_id` too — verify your `ValueError` surfaces cleanly.

> **Key Insight**
>
> The Inspector is a **protocol debugger**. It separates "does my tool work?" from "does Claude use my tool well?" — two very different questions that get conflated when you only test end-to-end. Build the habit of hitting the Inspector first on every new tool and every change to an existing one. It will save you hours of tangled debugging across the rest of Ch07.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: Know that the Python MCP SDK ships a browser-based Inspector launched with `mcp dev mcp_server.py`, and that the Inspector exposes Tools, Resources, and Prompts.
- **D1 (Agentic Architecture)**: Recognize the Inspector as the isolated test surface for MCP, distinct from full agent testing.
- Scenario question to expect: "your tool works in the Inspector but fails from your chatbot — what category of bug is it?" — answer: not an MCP bug; likely a prompt, schema description, or agent-loop bug.

---

## Flashcards

| Front | Back |
|-------|------|
| How do you start the MCP Inspector? | `mcp dev mcp_server.py` from an activated Python environment. |
| What port does the Inspector run on by default? | `6277` |
| What is the first button to click in the Inspector sidebar? | "Connect" — it starts the session with your MCP server. |
| What three primitives does the Inspector let you exercise? | Tools, Resources, and Prompts. |
| What does clicking "List Tools" do at the protocol level? | Sends a `ListToolsRequest` and renders the returned `ListToolsResult`. |
| What does "Run Tool" do at the protocol level? | Sends a `CallToolRequest` with the form inputs and displays the `CallToolResult`. |
| What is the chained verification pattern shown in the lesson? | Call `edit_document` then immediately call `read_doc_contents` to confirm the edit. |
| What is the Inspector's biggest value for debugging? | It isolates MCP behavior from LLM behavior — tool bugs stop masking prompt bugs. |
