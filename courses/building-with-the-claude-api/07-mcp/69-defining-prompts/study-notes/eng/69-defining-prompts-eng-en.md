# Defining Prompts — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.3 (MCP primitives: tools, resources, prompts), 1.2 (seeding the agent loop), 2.2 (base.Message content blocks) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 69 |

---

## One-Liner

Prompts are the third MCP primitive — pre-built, high-quality instruction templates that the server author has carefully developed so clients can invoke them by name instead of asking end users to write their own.

---

## The Problem Prompts Solve

Users technically can write their own instructions — "convert report.pdf to markdown" will work. But the result quality depends entirely on how good their prompt is, and most users are not prompt engineers. The core insight from the lesson:

> Users can accomplish these tasks on their own, but they'll get more consistent and higher-quality results when using prompts that have been carefully developed and tested by the MCP server authors.

Prompts externalize that expertise. A developer who knows exactly how to get a great markdown conversion bakes that knowledge into a reusable, server-side template.

---

## Where Prompts Sit Among MCP Primitives

| Primitive | Purpose | Example |
|-----------|---------|---------|
| Tool | Perform an action | `edit_document(doc_id, new_content)` |
| Resource | Expose data | `docs://documents/{doc_id}` |
| Prompt | Pre-built instruction template | `format(doc_id)` that reformats a document to markdown |

A prompt is not "text that Claude reads." It is a **callable template** the client can invoke, providing arguments, and receive back a list of messages ready to send to Claude.

---

## How Prompts Work

- Define prompts with the `@mcp.prompt()` decorator
- Give each prompt a `name` and `description`
- Return a list of messages (user + assistant) that form the complete conversation starter
- These prompts should be high quality, well-tested, and central to the server's purpose

When the client later requests a prompt by name, the server runs the decorated function with the client-supplied arguments and returns the resulting message list. The client forwards that list straight to Claude as the conversation.

---

## Building a Format Command — Imports

First, import the base message types from the MCP SDK:

```python
from mcp.server.fastmcp import base
```

`base` provides `UserMessage` and friends — the typed objects used to construct a prompt's message list.

---

## Building a Format Command — Definition

```python
@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format."
)
def format_document(
    doc_id: str = Field(description="Id of the document to format")
) -> list[base.Message]:
    prompt = f"""
Your goal is to reformat a document to be written with markdown syntax.

The id of the document you need to reformat is:

{doc_id}


Add in headers, bullet points, tables, etc as necessary. Feel free to add in extra formatting.
Use the 'edit_document' tool to edit the document. After the document has been reformatted...
"""

    return [
        base.UserMessage(prompt)
    ]
```

Breakdown:

- `@mcp.prompt(name=..., description=...)` registers the prompt with the server. Clients see these strings when listing available prompts.
- `doc_id: str = Field(description="...")` is a parameter with metadata — the description travels to the client so users know what to provide.
- The function body builds a multi-line template via f-string interpolation and returns a **list of messages**. In this case a single `UserMessage`.
- Notice how the prompt references the `edit_document` **tool** — prompts are designed to work in concert with the server's tools and resources. A prompt can be a recipe that uses the rest of the server's surface area.

---

## Why the Return Type Is `list[base.Message]`

Prompts can encode multi-turn conversations. For example, you could seed an assistant message as well:

- `base.UserMessage(...)` — what the user "says"
- `base.AssistantMessage(...)` — a pre-canned assistant turn (useful for few-shot conditioning)

By returning a list, the server author controls the exact conversation state that Claude sees when the prompt starts. The client just plays the messages back.

---

## Testing with the MCP Inspector

The MCP Inspector has a dedicated Prompts section. To test:

1. Run `uv run mcp dev mcp_server.py`
2. Open the Inspector in your browser
3. Navigate to Prompts, select your prompt, and fill in any parameters
4. The inspector displays the generated messages that would be sent to Claude

This lets you verify that your prompt interpolates variables correctly and produces the expected message structure **before** wiring it into the client.

---

## Best Practices

From the lesson:

1. **Focus on tasks central to your server's purpose** — a document server should ship prompts like `format`, `summarize`, `outline`.
2. **Write detailed, specific instructions** — vague prompts produce vague output.
3. **Test thoroughly with different inputs** — use the Inspector.
4. **Include clear descriptions** — users pick prompts based on the description string.
5. **Design prompts to work with your tools and resources** — a well-scoped prompt naturally chains into the server's tools (e.g., the format prompt ends by calling `edit_document`).

The framing is: **prompts are your expertise as a server author**, captured in a form clients can call. If a user could write it themselves in thirty seconds, it probably does not need to be a prompt. If it took you a week to dial in the wording, that is exactly the knowledge worth exposing.

---

## Common Mistakes

1. **Treating prompts as raw strings** — a prompt is a callable that returns a list of `base.Message` objects, not just a template string.
2. **Forgetting `Field(description=...)`** — without it, the client side cannot communicate to users what argument to supply.
3. **Hardcoding data the prompt should fetch** — if the prompt needs document text, reference the tool or resource that fetches it; do not bake data into the prompt.
4. **Writing low-effort prompts** — a prompt that is worse than what a user would type adds negative value. Only ship prompts that are demonstrably better than ad-hoc queries.
5. **Mixing prompts and resources** — a prompt is an instruction template; a resource is data. Do not return document text as a prompt.

> **Key Insight**
>
> Prompts are the missing primitive that most MCP discussions skip. Tools give Claude capabilities; resources give it context; prompts give it **direction**. A server with all three composes like a small product: the client discovers what can be done (tools), what data is available (resources), and which starting points are curated (prompts). In practice, prompts become the UX entry points users see as slash-commands or quick actions.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: prompts are the third MCP primitive alongside tools and resources; know the `@mcp.prompt()` decorator, `name`/`description`, the `list[base.Message]` return type, and `Field(description=...)` on parameters.
- **D1 (Agentic Architecture)**: prompts seed the agent loop with high-quality starting messages that the server author has pre-engineered.
- Exam pattern: "What MCP primitive should a server author use to ship a reusable, parameterized instruction to reformat documents?" → a prompt, defined via `@mcp.prompt()`.

---

## Flashcards

| Front | Back |
|-------|------|
| What are prompts in MCP? | Pre-built, parameterized instruction templates defined on the server that clients can invoke by name to get a high-quality starting conversation for Claude. |
| What decorator defines a prompt? | `@mcp.prompt(name=..., description=...)` |
| What does a prompt function return? | A `list[base.Message]` — the sequence of user/assistant messages that forms the conversation starter. |
| Where do the base message types come from? | `from mcp.server.fastmcp import base` — provides `base.UserMessage`, `base.AssistantMessage`, etc. |
| How do parameter descriptions reach the user? | Via `Field(description="...")` on the function parameter — the MCP SDK forwards them to the client. |
| Why ship prompts instead of letting users write their own? | Server authors have tested expert-level prompts; exposing them raises result quality without forcing every user to learn prompt engineering. |
| How do you test a prompt before wiring it into the client? | Run `uv run mcp dev mcp_server.py` and use the MCP Inspector's Prompts section to view the generated messages. |
| How does the `format` example connect to other MCP primitives? | It references the `edit_document` tool, showing prompts can orchestrate tools and resources to accomplish a task. |
