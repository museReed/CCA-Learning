# Defining Resources — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.3 (MCP primitives: tools vs resources vs prompts), 1.2 (context injection) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 67 |

---

## One-Liner

Resources are MCP's "data shelf" — a structured way for your server to expose read-only data (like documents, records, or lists) that the app can pull and inject directly into Claude's prompt, without a tool call and without letting Claude guess what to fetch.

---

## Mental Model: The Restaurant Menu vs the Kitchen

- **Resources** are the **menu**: a readable list of things the server can serve up on request. You (the app) pick from the menu, the server hands you the item, and you put it on Claude's plate.
- **Tools** are the **kitchen**: Claude orders "make me a sandwich" and the kitchen actually does the cooking (actions, side effects).

Both are offered by the same restaurant (MCP server). The choice of menu-vs-kitchen is the choice of resource-vs-tool.

---

## Why PMs Should Care

Most AI features that feel "context-aware" — "@mention a document," "pull this record," "show me the latest customer notes" — are really resource-backed under the hood. Getting the distinction right changes:

- **Who drives the fetch** — user/app (resource) vs Claude (tool)
- **Cost** — pulling a resource once vs giving Claude a tool it might call many times
- **Latency** — resources go into the first prompt; tools add a second API round trip
- **Predictability** — resources always inject the same data; tools let Claude decide, which is more flexible but less deterministic

A PM who confuses the two either pays for tool calls that should have been a straight pull, or ships an app where Claude hallucinates about data it could have been handed.

---

## Feature Example: `@document` Mentions

The course uses a concrete feature: in the CLI, the user types `@` and gets an autocomplete list of documents. Pick one, send the message, and the document's full text gets injected into the prompt.

This is two resources:

| Operation | Resource type | Why |
|-----------|---------------|-----|
| List all documents for autocomplete | Direct (static URI) | Fixed, no parameters, always the same call |
| Fetch one document by ID | Templated (URI with `{doc_id}`) | Parameterized, different output per call |

Zero tool calls. Zero Claude round trips for the fetch. The app just asks the server for the data and puts it straight into the prompt.

---

## Resources vs Tools — PM Cheat Sheet

| Product Scenario | Resource or Tool? | Why |
|------------------|-------------------|-----|
| Insert document content when user says @filename | Resource | Pure read, app-driven, no decision needed |
| Let Claude search the knowledge base mid-answer | Tool | Claude decides when to search |
| Populate a dropdown of customers | Resource | Static list fetch |
| Update a customer's phone number | Tool | Write / side effect |
| Show a dashboard of current KPIs | Resource | Pull-and-render |
| "Book me a meeting if my calendar is free" | Tool (agentic) | Claude reasons, decides, acts |

---

## Product Use Cases

### When to Use Resources

| Need | Why Resources Fit |
|------|-------------------|
| Users reference specific items (@mentions, /commands, file pickers) | App drives the fetch based on user selection |
| Always-inject context (company style guide, glossary, schema) | Pull once, include every conversation |
| Lists for UI affordances (autocomplete, dropdowns) | Direct resources map to static collections |
| Data-driven onboarding (show "your last order") | Fetch per user, inject into prompt |

### When to Use Tools Instead

| Need | Why Tools Fit |
|------|---------------|
| Claude should decide whether to fetch at all | Only tools give Claude the choice |
| The action has side effects | Resources are read-only |
| Parameters depend on reasoning | Tool inputs can be synthesized mid-turn |

---

## PM Decision Framework

Before spec'ing a fetch-style feature, ask:

| Question | If Yes | Implication |
|----------|--------|-------------|
| Does the user (not Claude) decide which item to fetch? | Yes | Resource |
| Is the fetch a pure read with no side effects? | Yes | Resource |
| Do we want the data in the prompt every time, deterministically? | Yes | Resource |
| Should Claude be able to skip the fetch if it seems unnecessary? | Yes | Tool |
| Does the operation modify data? | Yes | Tool |

---

## Common PM Mistakes

1. **Treating every MCP capability as a tool** — the cheapest and most predictable primitive is often a resource. Ask "who decides?" before spec'ing.
2. **Not thinking about the URI namespace** — URIs are the API. Bad ones (`docs://d1`, `docs://d2`) will haunt you. Treat URI design like REST API design.
3. **Assuming resources are free** — they still cost tokens because the fetched content goes into the prompt. Large documents can blow the context window.
4. **Mixing reads and writes in one primitive** — keep reads in resources and writes in tools. It makes security review and audit logs dramatically simpler.
5. **Skipping the Inspector for validation** — the MCP Inspector lets you prove the resource works before writing a line of client code. Using it is a best practice to demand from eng.

> **Key Insight**
>
> Resources are the primitive that lets your product say "Claude, here is the exact data you need" instead of "Claude, here are tools you could use to maybe fetch something useful." Every time you force Claude to choose, you pay for tokens and introduce variance. Resources are how a PM preserves determinism and cost control while still giving Claude fresh, relevant context.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: resources are one of three MCP primitives (tools, resources, prompts); know the direct vs templated distinction.
- **D1 (Agentic Architecture)**: resources are how context gets into the agent loop without a tool call — pulled by the client, injected into the prompt.
- Exam pattern: "The app needs to show document contents in the prompt based on a user selection. Is this a tool or a resource?" → resource.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the "menu vs kitchen" analogy for resources and tools? | Resources are the menu (readable data the app picks and serves to Claude). Tools are the kitchen (actions Claude chooses to perform). |
| What are the two kinds of resources? | Direct (static URI, fixed call) and templated (URI with parameters, parameterized call). |
| When should a feature be a resource instead of a tool? | When the app (not Claude) decides to fetch, the fetch has no side effects, and the data should always be present in the prompt. |
| Give a product example of a direct vs templated resource. | Direct: list all documents for autocomplete. Templated: fetch a specific document by `{doc_id}`. |
| What cost do resources still incur? | Token cost — fetched content goes into the prompt and counts against the context window. |
| Why should URI design be treated seriously? | URIs are the API contract of your server — bad URIs are as painful to fix as bad REST routes. |
| How do resources differ from tools in Claude's perspective? | Claude never "decides" to call a resource. Resources are pulled by the client and inserted into the prompt. Claude only sees the result. |
| What validation tool should you demand before launch? | The MCP Inspector — it lists direct and templated resources and lets you test each one end to end before the client is wired up. |
