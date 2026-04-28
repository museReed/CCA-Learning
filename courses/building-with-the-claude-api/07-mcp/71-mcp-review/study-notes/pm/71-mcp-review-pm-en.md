# MCP Review — PM Quick-Scan

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.1 (MCP architecture), 2.2 (primitives), 2.3 (tool vs resource vs prompt) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 71 |

---

## One-Liner

MCP's three building blocks — tools, resources, and prompts — each serve a different stakeholder in your product: the AI model, the application itself, or the end user, and knowing which stakeholder each serves is the key to making the right architectural choice.

---

## The Stakeholder Map

Think of building a product with three departments, each needing different things:

| Building Block | Stakeholder | Business Analogy | When to Use |
|----------------|-------------|-------------------|-------------|
| **Tools** | AI Model | Giving an employee new skills | Claude needs to do something new (calculate, search, query) |
| **Resources** | Application | Accessing the company database | Your app needs data to display or use as context |
| **Prompts** | End User | Pre-built report templates | Users need one-click access to common workflows |

### Tools = New Skills for the AI

When your product needs Claude to do something beyond text generation — run code, search a database, call an external API — you provide a tool. The critical distinction: **Claude decides when to use it**, not your code and not the user.

**Product decision**: "Does our AI need a new capability?" → Add a tool.

### Resources = Data on Demand

When your application code needs data to display in the UI or to enrich a prompt, you use a resource. The application pulls the data — it's like a data feed your product subscribes to.

**Product decision**: "Does our app need to pull in external data?" → Add a resource.

### Prompts = User Workflows

When users need pre-built, optimized workflows they can trigger with one click, you create prompts. Think of them as templates that users activate.

**Product decision**: "Do users need a shortcut for a common task?" → Add a prompt.

---

## Decision Checklist for PRDs

When specifying a new MCP integration in a PRD:

- [ ] **Who initiates the action?** AI → Tool, App → Resource, User → Prompt
- [ ] **What's the outcome?** New capability → Tool, Data retrieval → Resource, Workflow → Prompt
- [ ] **Is it recurring or one-time?** Consider which primitive makes maintenance easiest

---

## CCA Exam Relevance

- **D2 (MCP Integration)**: The tool/resource/prompt decision framework is heavily tested. Memorize the controller mapping.
- Key formula: **Tools = model-controlled, Resources = app-controlled, Prompts = user-controlled**

---

## Flashcards

| Front | Back |
|-------|------|
| What are the three MCP server primitives? | Tools, Resources, and Prompts. |
| Which stakeholder do MCP tools serve? | The AI model — Claude decides when to invoke tools. |
| Which stakeholder do MCP resources serve? | The application — app code decides when to fetch data. |
| Which stakeholder do MCP prompts serve? | The end user — users trigger prompts via UI or commands. |
| If your product needs Claude to search a database, which primitive do you use? | A Tool — it adds a new capability that Claude can decide to use. |
| If your UI needs to display a list of documents, which primitive do you use? | A Resource — your app code fetches data for display. |
| If users need a one-click "Generate Report" button, which primitive? | A Prompt — it's a user-triggered predefined workflow. |
