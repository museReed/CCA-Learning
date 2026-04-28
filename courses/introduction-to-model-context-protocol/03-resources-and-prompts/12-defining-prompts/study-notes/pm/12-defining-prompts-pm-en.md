# Defining Prompts — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server primitives), 2.6 (prompt template design), 1.3 (prompt engineering for tools) |
| Source | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 12 |

---

## One-Liner

MCP prompts are like pre-written expert scripts that your team packages into the product — users get consistent, high-quality AI interactions without needing to become prompt engineers themselves.

---

## Why PMs Should Care About Prompts

Prompts solve a fundamental product problem: **the quality gap between expert and novice users**.

| User Type | Without MCP Prompts | With MCP Prompts |
|-----------|-------------------|-----------------|
| Expert user | Writes great prompts, gets great results | Same great results, slightly faster |
| Average user | Writes mediocre prompts, gets mediocre results | Gets expert-level results via pre-built templates |
| New user | Does not know what to ask, poor results | Discovers workflows through slash commands |

This is the same principle as email templates, Notion template galleries, or Figma component libraries — packaging expertise for reuse.

---

## Mental Model: The Restaurant Menu

Think of MCP primitives as different ways to interact with a restaurant:

| Interaction | MCP Primitive | Who Decides | Restaurant Analogy |
|-------------|---------------|-------------|-------------------|
| Chef improvises | **Tool** | Chef (Claude) | "Chef's choice — surprise me" |
| Waiter brings water | **Resource** | Restaurant (app) | Water appears on the table automatically |
| Customer orders from menu | **Prompt** | Customer (user) | "I'll have the #7 combo" |

Prompts are the menu. The kitchen (MCP server developer) has carefully designed each dish (prompt template). The customer (user) picks from tested options and gets a predictable, high-quality result.

---

## Product Use Cases

### When to Use Prompts

| Scenario | Why Prompts Work |
|----------|-----------------|
| "Reformat this document to markdown" | Tested template handles edge cases better than user's ad-hoc request |
| "Generate a weekly summary from my notes" | Complex instructions that users would struggle to write themselves |
| "Analyze this dataset and create a report" | Domain-specific workflow with multiple steps |
| "Translate this document preserving formatting" | Nuanced instructions that need careful prompt engineering |

### When NOT to Use Prompts

| Scenario | Better Alternative |
|----------|--------------------|
| User asks a freeform question | Let Claude handle it directly — no template needed |
| App needs to pre-load context | Use a **resource** — app-controlled |
| Claude needs to decide when to act | Use a **tool** — model-controlled |

---

## The Slash Command UX Pattern

Prompts naturally map to the slash command pattern familiar from tools like Slack, Notion, and Discord:

1. **User types `/`** — available prompts appear as a command menu
2. **User selects a command** (e.g., `/format`) — prompted for required parameters
3. **User provides parameters** (e.g., selects a document) — prompt template is filled in
4. **Template is sent to Claude** — Claude receives the expertly crafted instructions
5. **Claude executes** — using available tools to fulfill the prompt's instructions

From the user's perspective, this feels like a "workflow button" — one click (or command) to trigger a complex, reliable operation.

---

## The Four Benefits for Product

1. **Consistency** — every user gets the same quality of instructions, eliminating the "prompt lottery"
2. **Expertise encoding** — domain knowledge baked into templates by the developer
3. **Reusability** — multiple client applications can share the same prompts from one server
4. **Centralized maintenance** — update a prompt on the server, all clients automatically get the improvement

---

## PM Decision Framework

When designing an AI feature, ask these questions:

| Question | If Yes | Primitive |
|----------|--------|-----------|
| Does the user explicitly trigger this workflow? | Yes | **Prompt** |
| Does Claude need to decide when to act? | Yes | **Tool** |
| Does the app need data for UI or context? | Yes | **Resource** |
| Is this a predefined, repeatable workflow? | Yes | **Prompt** |
| Does this require specialized instructions? | Yes | **Prompt** |

---

## Common PM Mistakes

1. **Not investing in prompt quality** — treating prompts as simple strings instead of carefully tested templates that need iteration
2. **Too many prompts** — overwhelming users with choices; curate a focused set of high-value workflows
3. **Not specifying prompt parameters in PRD** — users need clear parameter descriptions; include them in acceptance criteria
4. **Confusing prompts with system instructions** — prompts are user-triggered workflows, not always-on behavior rules

> **Key Insight**
>
> Prompts are the **user-controlled** primitive. This means the user explicitly decides when to use them, unlike tools (Claude decides) or resources (app decides). For PMs, this maps directly to "workflow features" — features where the user initiates a structured, repeatable process. In the CCA exam, the control model distinction (model / app / user) is the most frequently tested concept across D1 and D2.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: Know when to recommend prompts vs. tools vs. resources. The trigger is: "predefined workflow" + "user initiates" = prompt.
- **D1 (Agentic Architecture)**: Prompts fit the user-controlled layer. Questions often present scenarios and ask which primitive to use.
- Watch for the word "workflow" or "slash command" in exam questions — these almost always point to prompts.

---

## Flashcards

| Front | Back |
|-------|------|
| Who controls when MCP prompts are triggered? | The user (user-controlled) — via slash commands, buttons, or menu selections |
| What product problem do MCP prompts solve? | The quality gap between expert and novice users — prompts package expertise into reusable templates |
| What is the restaurant analogy for MCP prompts? | The menu — the kitchen designs each dish (template), the customer (user) picks from tested options |
| When should a PM choose a prompt over a tool? | When the workflow is predefined, repeatable, and explicitly triggered by the user |
| What UX pattern do prompts naturally map to? | Slash commands (`/format`, `/summarize`) — familiar from Slack, Notion, Discord |
| What are the four product benefits of MCP prompts? | Consistency, expertise encoding, reusability, centralized maintenance |
| How do prompts differ from system instructions? | Prompts are user-triggered workflows; system instructions are always-on behavior rules |
| What happens after a user selects a prompt and provides parameters? | The template is filled in with parameters and sent to Claude as expertly crafted instructions |
