# Defining Resources — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server primitives), 2.4 (resource URI design), 2.5 (MIME type handling) |
| Source | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 10 |

---

## One-Liner

Resources are the "reference library" of an MCP server — they let your application pull in data for display or context, like a librarian fetching a book when someone asks for it by name.

---

![Resources Types](../../visuals/resources-types.svg)


## Why PMs Need to Understand Resources

As a PM, you shape product requirements that determine whether a feature should use a resource, a tool, or a prompt. Getting this wrong means:

1. **Wasted engineering cycles** — building a tool when a resource would be simpler
2. **Poor UX** — forcing users to wait for Claude to "look something up" when the data could be pre-loaded
3. **Incorrect acceptance criteria** — specifying the wrong interaction pattern in your PRD

---

## Mental Model: The Office Filing System

Think of an MCP server as an office building with three departments:

| Department | MCP Primitive | Who Decides to Use It | Office Analogy |
|------------|---------------|----------------------|----------------|
| Filing Cabinet | **Resource** | The receptionist (your app) | Receptionist pulls a file to hand to a visitor |
| Action Desk | **Tool** | The executive (Claude) | Executive decides to call accounting to process a refund |
| Workflow Manual | **Prompt** | The employee (user) | Employee follows a standard procedure checklist |

Resources are the filing cabinet. Your application code opens the drawer, pulls out the file, and either shows it in the UI or hands it to Claude as context. Claude never goes to the filing cabinet on its own — that distinction is critical.

---

## Two Types of Resources

### 1. Direct Resources — "Give Me the Whole Catalog"

Like asking a librarian: "Show me all available books." The request is always the same, the URI is fixed.

- **Product example**: An autocomplete dropdown showing all available documents
- **URI pattern**: `docs://documents` (no variables)

### 2. Templated Resources — "Give Me This Specific Book"

Like asking: "Show me the book with ID plan.md." The request includes a parameter.

- **Product example**: When a user types `@plan.md`, the system fetches that specific document
- **URI pattern**: `docs://documents/{doc_id}` (variable part in braces)

---

## The Document Mention Feature — A Product Walkthrough

Imagine you are designing a chat interface where users can reference documents:

1. **User types `@`** — your app calls the "list all documents" resource to populate an autocomplete menu
2. **User selects `plan.md`** — your app calls the "fetch specific document" resource with `doc_id=plan.md`
3. **Document content is injected into the prompt** — Claude sees the document contents immediately, no extra step needed
4. **Claude responds** — with full context about the document, instantly

This is faster and smoother than the alternative (Claude calling a tool to fetch the document), because the data is already in the prompt before Claude starts thinking.

---

## Product Decision Framework

When writing a PRD for an AI feature, ask:

| Question | If Yes... | If No... |
|----------|-----------|----------|
| Does the data need to appear in the UI (dropdown, sidebar)? | **Resource** | Maybe a tool |
| Should the data be pre-loaded as context before Claude responds? | **Resource** | Tool if Claude needs to decide |
| Does fetching this data have side effects (write, delete, charge)? | **Tool** (never a resource) | Resource is safe |
| Does Claude need to autonomously decide when to fetch this? | **Tool** | Resource |

---

## Data Format Hints (MIME Types)

Resources include a "format hint" that tells the client how to display the data:

| Format Hint | What It Means | Product Implication |
|-------------|---------------|---------------------|
| `application/json` | Structured data (lists, tables) | Can render as rich UI components |
| `text/plain` | Raw text | Display as-is or inject into chat |
| `application/pdf` | Binary document | May need special viewer |

This matters for your UI spec — knowing the data format helps you design the right display component.

---

## Common PM Mistakes

1. **Specifying a tool when a resource would suffice** — if the data is read-only and should appear in the UI, a resource is simpler and faster
2. **Assuming Claude fetches resources** — resources are app-controlled; your app fetches them, not Claude
3. **Ignoring the autocomplete pattern** — resources naturally support the `@mention` UX pattern that users find intuitive
4. **Not considering data freshness** — resources return data at the moment of request; if you need real-time updates, discuss caching strategy with engineering

> **Key Insight**
>
> The most important thing a PM needs to remember about resources: they are **app-controlled**. Your application code decides when to fetch the data. This means you can guarantee the data is available before Claude starts reasoning, which leads to faster response times and better UX.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: Scenario questions will describe a feature and ask which primitive to use. If the scenario involves displaying data in a UI or injecting context into a prompt, the answer is resources.
- **Control model is the key differentiator**: Tools = model-controlled, Resources = app-controlled, Prompts = user-controlled. This three-way distinction appears frequently.
- Watch for trick answers that suggest using a tool to "fetch data for the UI" — resources are the correct primitive for that use case.

---

## Flashcards

| Front | Back |
|-------|------|
| Who controls when MCP resources are accessed — Claude, the app, or the user? | The application code (app-controlled) |
| What are the two types of MCP resources? | Direct resources (fixed URI, no parameters) and Templated resources (URI with variable placeholders) |
| What is the product UX pattern that resources naturally support? | The `@mention` autocomplete pattern — type `@`, see available items, select one, content injected into prompt |
| When should a PM specify a resource instead of a tool in a PRD? | When data is read-only, needs to appear in UI, or should be pre-loaded as context before Claude responds |
| What does the MIME type hint do for resources? | Tells the client application how to interpret and display the returned data |
| Why are resources faster than tools for providing context? | Resource data is injected directly into the prompt before Claude starts reasoning, avoiding an extra round-trip |
| Can a resource have side effects (write, delete, charge)? | No — resources are read-only. If side effects are needed, use a tool instead |
| In the office analogy, what is a resource? | The filing cabinet — the receptionist (app) pulls files from it to hand to visitors or to add to meeting briefings |
