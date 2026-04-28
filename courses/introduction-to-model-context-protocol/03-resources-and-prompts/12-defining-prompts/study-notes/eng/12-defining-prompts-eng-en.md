# Defining Prompts — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server primitives), 2.6 (prompt template design), 1.3 (prompt engineering for tools) |
| Source | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 12 |

---

## One-Liner

MCP prompts are server-defined, parameterized message templates that return `list[base.Message]`, providing users with pre-built, tested instructions that outperform ad-hoc user prompts.

---

## Why Prompts Exist

Users can already ask Claude to do anything directly. The value of MCP prompts is **expertise packaging**:

| Approach | Quality | Consistency | Maintenance |
|----------|---------|-------------|-------------|
| User writes their own prompt | Variable — depends on user skill | Low — different every time | None — one-off |
| MCP server provides a prompt | High — tested by the developer | High — same template every time | Centralized — update once, all clients benefit |

As the MCP server author, you invest time crafting, testing, and evaluating prompts that handle edge cases. Users get expert-level results without prompt engineering knowledge.

---

## The `@mcp.prompt()` Decorator

Prompts follow the same decorator pattern as tools and resources:

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
<document_id>
{doc_id}
</document_id>

Add in headers, bullet points, tables, etc as necessary.
Feel free to add in structure.
Use the 'edit_document' tool to edit the document.
After the document has been reformatted...
"""
    return [
        base.UserMessage(prompt)
    ]
```

### Key Implementation Details

1. **`name` parameter** — becomes the slash command identifier (e.g., `/format`)
2. **`description` parameter** — shown to users in the prompt list
3. **`Field(description=...)`** — Pydantic Field for parameter documentation, displayed when user selects the prompt
4. **Return type `list[base.Message]`** — a list of messages (UserMessage, AssistantMessage) that get sent to Claude
5. **f-string interpolation** — `{doc_id}` is replaced with the actual parameter value at runtime

---

## Message Types in Prompts

Prompts return a list of messages, which can include:

```python
# Single user message (most common)
return [base.UserMessage(prompt_text)]

# Multi-turn conversation (for complex workflows)
return [
    base.UserMessage("Here is the task..."),
    base.AssistantMessage("I understand. Let me..."),
    base.UserMessage("Now proceed with step 2...")
]
```

Multi-turn prompts are powerful for:
- **Few-shot examples** — show Claude how to respond before the actual task
- **Complex workflows** — guide Claude through a multi-step process
- **Persona setup** — establish Claude's role before the task instruction

---

## Prompt vs. Tool vs. Resource: Control Model

| Primitive | Controller | Trigger | Example |
|-----------|-----------|---------|---------|
| **Tool** | Claude (model-controlled) | Claude decides during reasoning | `calculate_sqrt(3)` |
| **Resource** | Application code (app-controlled) | Your code calls `read_resource()` | `@plan.md` autocomplete |
| **Prompt** | User (user-controlled) | User types `/format` or clicks a button | `/format doc_id=plan.md` |

Prompts are the **user-controlled** primitive. The user explicitly triggers them through UI interactions (slash commands, buttons, menu selections).

---

## Testing Prompts with MCP Inspector

```bash
uv run mcp dev mcp_server.py
```

In the Inspector:
1. Navigate to the **Prompts** tab
2. Select a prompt from the list
3. Fill in parameter values (e.g., `doc_id = "plan.md"`)
4. Click "Get Prompt" to see the interpolated messages
5. Verify the f-string variables are correctly replaced

The Inspector shows you exactly what messages will be sent to Claude, making it essential for validating prompt templates before deployment.

---

## Design Best Practices

1. **Use XML tags for variable boundaries** — `<document_id>{doc_id}</document_id>` prevents prompt injection and helps Claude identify structured data
2. **Reference available tools in the prompt** — tell Claude which tools to use (e.g., "Use the 'edit_document' tool")
3. **Be specific about output format** — if you want markdown, say "written with markdown syntax"
4. **Test with edge cases** — empty strings, long documents, special characters
5. **Keep prompts domain-specific** — a document server has formatting prompts, a data server has analysis prompts

---

## Common Mistakes

1. **Returning a string instead of `list[base.Message]`** — prompts must return a list of Message objects, not raw strings
2. **Forgetting parameter documentation** — use `Field(description=...)` so users know what to provide
3. **Not referencing tools** — if your prompt expects Claude to use specific tools, mention them explicitly in the prompt text
4. **Overly generic prompts** — prompts should leverage your server's specific capabilities, not just be general instructions

> **Key Insight**
>
> Prompts are the **user-controlled** primitive in MCP. Unlike tools (where Claude decides when to act) or resources (where your app decides when to fetch), prompts give users explicit control through slash commands or UI buttons. For the CCA exam, the three-way control model (model / app / user) is a frequently tested concept.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: Know the `@mcp.prompt()` decorator pattern, the return type (`list[base.Message]`), and parameter handling via Pydantic `Field`.
- **D1 (Agentic Architecture)**: Prompts represent the user-controlled layer of the MCP control model. Questions may ask when to use prompts vs. tools vs. resources.
- The key exam differentiator: "predefined workflow triggered by user action" = prompt. "Claude decides to act" = tool. "App fetches data" = resource.

---

## Flashcards

| Front | Back |
|-------|------|
| What does an MCP prompt function return? | `list[base.Message]` — a list of UserMessage and/or AssistantMessage objects |
| Who controls when MCP prompts are triggered? | The user (user-controlled) — via slash commands, buttons, or menu selections |
| What decorator defines an MCP prompt? | `@mcp.prompt(name="...", description="...")` |
| How are prompt parameters documented for users? | Using Pydantic `Field(description="...")` on function parameters |
| Why use XML tags like `<document_id>` in prompt templates? | To clearly delimit variable boundaries, prevent prompt injection, and help Claude identify structured data |
| What is the difference between prompts and tools in MCP? | Prompts are user-controlled (user triggers explicitly), tools are model-controlled (Claude decides when to call) |
| Can MCP prompts include multi-turn conversations? | Yes — return multiple UserMessage and AssistantMessage objects for few-shot examples or complex workflows |
| How do you test prompts before deployment? | Use MCP Inspector — navigate to Prompts tab, fill in parameters, verify interpolated messages |
