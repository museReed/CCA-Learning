# Defining Tools with MCP — PM Strategic Overview

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | T2.1 Design and implement tool schemas; T2.5 Use MCP SDK to define tools with type safety |
| Source | introduction-to-model-context-protocol / 02-tools-and-inspector / Lesson 06 |

---

## One-Liner

The MCP SDK turns tool creation from a weeks-long specification project into a simple Python function with a good description — dramatically reducing the engineering effort to give Claude new capabilities.

---

![Tools Decorator](../../visuals/tools-decorator.svg)


## The Old Way: Specification-Driven Development

Before MCP SDKs, giving Claude access to a new tool required a multi-step process that felt a lot like writing legal contracts:

1. **Write a JSON schema** — A formal specification of every parameter, its type, constraints, and description
2. **Write the handler function** — The actual code that does the work
3. **Keep them in sync** — Any time the function changes, the schema must change too
4. **Test the schema** — Verify Claude correctly interprets the schema

This is like requiring every employee to write a formal job description before they can do any work, then updating that document every time their responsibilities change.

> **PM Takeaway**
> The old approach created a "tool bottleneck" — every new capability required schema specification work before any real functionality could be built. FastMCP removes this bottleneck entirely.

---

## The New Way: Just Write the Function

With FastMCP, the engineering workflow is dramatically simpler:

1. Write a Python function that does what you want
2. Add a decorator (`@mcp.tool()`)
3. Write a good docstring explaining what it does

That is it. The SDK automatically generates the formal specification from the code itself. The function IS the specification.

Think of it like the difference between:

- **Old way**: Writing a detailed 10-page RFP, getting it approved, then hiring a contractor to do the work
- **New way**: Describing what you need in a conversation, and the work starts immediately

The key insight for PMs is that the **quality of the tool description** (the docstring) directly affects how well Claude uses the tool. This is where product thinking matters — not in the technical schema, but in clearly articulating what the tool does, when to use it, and what it returns.

> **PM Takeaway**
> Tool descriptions are a product design decision, not just a technical detail. A well-written description means Claude picks the right tool at the right time. A vague one means Claude makes mistakes or ignores the tool entirely.

---

## Why Descriptions Are Product Decisions

When Claude receives a user query, it reads through all available tool descriptions and decides which tool (if any) to use. This is exactly like a customer reading product descriptions in a catalog.

Consider two descriptions for the same tool:

**Vague**: "Reads documents"

**Precise**: "Read and return the full text contents of a document at the specified file path. Use this when the user asks about document contents, needs to review a file, or wants to search within a document."

The precise description gives Claude clear signals about when and how to use the tool. The vague one leaves too much ambiguity.

This maps directly to product copy writing — the clearer your description, the better the user experience.

---

## Error Messages as User Experience

When tools fail, the error message Claude receives determines how gracefully it handles the situation. Good error messages are like good customer service training:

**Bad error**: "Operation failed"
- Claude tells user: "Something went wrong. Please try again."

**Good error**: "Document not found at /reports/q3.pdf. The reports directory contains: q1.pdf, q2.pdf, q4.pdf"
- Claude tells user: "I could not find q3.pdf, but I see q1, q2, and q4 reports available. Would you like me to read one of those instead?"

> **PM Takeaway**
> Error messages are part of the user experience, even though users never see them directly. They determine whether Claude recovers gracefully or gives a dead-end response. When reviewing tool specifications, always check the error handling design.

---

## The Validation Safety Net

FastMCP automatically validates inputs before tool code runs. This is like having a quality control checkpoint before a manufacturing line:

- If Claude sends a number where a text string was expected, the validation catches it
- If a required field is missing, the validation catches it
- If a value is outside allowed bounds, the validation catches it

This means tool authors can focus on the "happy path" — what happens when inputs are correct — and let the SDK handle input mistakes. Fewer bugs, less defensive coding, faster development.

---

## Strategic Implications for Product Teams

**Faster capability expansion**: Adding a new tool to your AI product takes hours instead of days. This means your product can respond to user feedback and market demands much faster.

**Lower engineering bar**: Junior developers can create MCP tools. The SDK handles the complex protocol details, so developers focus on business logic.

**Better tool quality**: Auto-validation catches bugs before they reach users. Schema-code synchronization eliminates a whole category of "it worked in testing but fails in production" issues.

**Description-driven design**: The most impactful thing a PM can do is ensure tool descriptions are clear, specific, and aligned with user intent. This is where product expertise directly improves AI performance.

---

## CCA Exam Relevance

This lesson covers **Domain 2 (18%)** with focus on:

- Understanding that `@mcp.tool()` auto-generates schemas from Python functions
- Knowing that docstrings become tool descriptions Claude uses for selection
- Recognizing that good descriptions improve tool selection accuracy
- Understanding the validation and error handling patterns

---

## Flashcards

| Front | Back |
|-------|------|
| What does the MCP SDK eliminate from the tool creation process? | Manual JSON schema writing. The SDK auto-generates schemas from Python function signatures and type hints. |
| Why are tool descriptions a product decision? | Because Claude reads descriptions to decide which tool to use. Clear, specific descriptions lead to better tool selection and better user experiences. |
| What is the difference between a good and bad tool error message? | Good errors include context (what went wrong, what alternatives exist). Bad errors are generic ("failed"). Good errors let Claude recover gracefully. |
| What does "auto-validation" mean in FastMCP? | The SDK automatically checks that Claude's tool inputs match the expected types and constraints before the tool code runs, catching errors early. |
| How does FastMCP affect development speed? | Adding a new tool drops from days (manual schema + handler + testing) to hours (write function + decorator + docstring). |
| What is the most impactful thing a PM can do for MCP tools? | Ensure tool descriptions are clear, specific, and aligned with user intent — this directly affects how well Claude selects and uses tools. |
| How does schema-code synchronization work in FastMCP? | The schema is generated from the code itself, so they can never drift apart. Changes to the function automatically update the schema. |
| What happens when Claude sends invalid input to a FastMCP tool? | Pydantic validation catches the type error before the tool function executes, returning a clear error message to Claude. |
