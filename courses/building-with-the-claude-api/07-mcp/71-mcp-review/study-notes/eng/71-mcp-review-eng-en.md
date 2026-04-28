# MCP Review — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.1 (MCP architecture), 2.2 (primitives), 2.3 (tool vs resource vs prompt) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 71 |

---

## One-Liner

MCP's three server primitives — tools, resources, and prompts — are each controlled by a different part of your application: **tools** are model-controlled, **resources** are app-controlled, and **prompts** are user-controlled, and this mapping tells you which primitive to reach for when adding new capabilities.

---

## The Three Primitives and Their Controllers

| Primitive | Controlled By | Purpose | Example |
|-----------|---------------|---------|---------|
| **Tools** | Model (Claude) | Extend Claude's capabilities | Claude decides to run JavaScript to calculate √3 |
| **Resources** | Application code | Provide data to the app/UI | Fetching Google Drive docs for autocomplete or context augmentation |
| **Prompts** | User | Predefined workflows | User clicks a button or types a slash command to start a workflow |

### Tools — Model Controlled

Claude alone decides when to invoke a tool. Your code defines the tool and its schema, but the model makes the runtime decision. If you need to **add capabilities to Claude** (execute code, query a database, call an API), implement a tool on your MCP server or consume tools from an existing server through your MCP client.

### Resources — App Controlled

Application code decides when to fetch a resource. Resources provide data — they don't perform actions. Two common patterns from the course project:

1. **UI enrichment** — fetch a resource to populate autocomplete suggestions
2. **Prompt augmentation** — fetch a resource to inject context into a prompt before sending to Claude

If you need to **get data into your app** for display or context, use a resource.

### Prompts — User Controlled

A user initiates a prompt by clicking a UI element or typing a slash command. Prompts are predefined, optimized workflows — think of the button row at the bottom of Claude.ai's chat input. Each button triggers a pre-authored prompt template.

If you need to **implement a predefined workflow** that the user starts, use a prompt.

---

## Decision Framework

```
Need to add capabilities to Claude?     → Tool
Need to get data into your app/UI?      → Resource
Need a predefined user-triggered flow?  → Prompt
```

These are high-level guidelines, not rigid rules. The key insight is that each primitive serves a different **audience**: the model, the application, or the user.

---

## Real-World Mapping: Claude.ai

The course maps all three primitives to features visible in Claude.ai:

- **Prompts** → The pre-built conversation starters (buttons below chat input)
- **Resources** → "Add from Google Drive" button (app fetches document list, injects content)
- **Tools** → Claude deciding to execute JavaScript when asked to calculate something

---

## CCA Exam Relevance

- **D2 (MCP Integration)**: Expect questions like "Which MCP primitive should you use when…?" — the answer maps directly to who controls the action (model/app/user).
- Watch for: "Tools are model-controlled" is the most-tested fact. Resources and prompts are commonly confused — remember resources are for data retrieval by app code, prompts are for user-initiated workflows.

---

## Flashcards

| Front | Back |
|-------|------|
| What are the three MCP server primitives? | Tools, Resources, and Prompts. |
| Who controls MCP tools at runtime? | The model (Claude) — it decides when to invoke a tool. |
| Who controls MCP resources at runtime? | Application code — your app decides when to fetch data. |
| Who controls MCP prompts at runtime? | The user — they trigger prompts via UI elements or slash commands. |
| When should you use a tool vs a resource? | Tool: add capabilities to Claude. Resource: get data into your app/UI. |
| What is an example of a resource in Claude.ai? | The "Add from Google Drive" button — app fetches and displays document list. |
| What is an example of a prompt in Claude.ai? | The pre-built conversation starter buttons below the chat input. |
| Are these primitive-controller mappings strict rules? | No — they are high-level guidelines that indicate the primary intended audience of each primitive. |
