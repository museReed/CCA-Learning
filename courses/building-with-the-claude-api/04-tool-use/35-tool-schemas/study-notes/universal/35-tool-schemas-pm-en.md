# Tool Schemas — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.1 (tool schema design), 2.2 (tool function definition), 1.2 (agentic loop foundation) |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 35 |

---

## One-Liner

A tool schema is the product copy your AI reads before deciding how to help the user — treat its words like app-store descriptions, because Claude does.

---

## Mental Model: The Menu Item Description

Think of a restaurant menu:

- The menu item **name** ("Spicy Tuna Roll") — tells the customer this exists.
- The menu item **description** ("Fresh yellowfin tuna, sriracha aioli, scallions, 6 pieces") — tells them when to order it and what to expect.
- The **allergen / spice / price** annotations — constrain who should order it.

A tool schema is exactly this for Claude:

| Menu concept | Schema field |
|--------------|--------------|
| Item name | `name` |
| Item description | `description` |
| Ingredients / allergens / spice level | `input_schema.properties` with type, description, enum |
| Required choices (e.g., "pick a side") | `input_schema.required` |

A menu with vague descriptions ("Fish Thing, $12") gets fewer orders and more confused customers. A menu with rich descriptions gets the right dishes to the right people. Same for tool schemas.

---

## Why PMs Should Own the Description Copy

Most engineers will happily write a one-line description like "Gets current time" and move on. That line is *product copy Claude reads on every invocation*. The engineering time to write a good description is minutes; the reliability dividend is enormous.

PMs should:

1. **Review every tool's `description`** the same way they review app-store listings or onboarding copy.
2. **Provide the "when to use" sentence** — this is the single most valuable sentence in the description and engineers often skip it.
3. **List related tools** to help Claude disambiguate.
4. **Include concrete parameter examples** in the property descriptions.

---

## Product Use Cases: Where Schema Quality Moves the Needle

| Scenario | How schema quality helps |
|----------|--------------------------|
| Multiple similar tools (e.g., several calendar actions) | Descriptions let Claude pick the right one instead of guessing |
| Ambiguous user phrasing | "When to use" sentence guides Claude toward the right tool |
| Strict parameter formats (IDs, dates, SKUs) | Property descriptions and enums prevent malformed calls |
| Users in different languages | Rich descriptions let Claude map translations to correct tools |
| High-stakes actions (payments, deletions) | Explicit required fields avoid accidental omissions |

---

## The Three Fields in Plain English

| Field | What it means to a PM |
|-------|----------------------|
| `name` | The internal ID. Think of it like a slug. Short, unambiguous, snake_case. |
| `description` | The sales pitch. Tell Claude *what* it does, *when* to use it, and *what it returns*. 3–4 sentences. |
| `input_schema` | The order form. What fields are required, what values are allowed, what units, what format. |

Think of these three as the three columns of a product requirements doc: identity, value proposition, and configuration.

---

## The "When to Use" Sentence

The most frequently skipped piece of schema copy is the sentence that tells Claude **when** to pick this tool over others. Examples:

- Bad: "Returns the current date."
- Good: "Returns the current date. **Use this when the user asks about today, tomorrow, or any relative date reference.**"

In a PRD, literally include a line for each tool that reads:

> Claude should use this tool when: *(one sentence)*

This forces the PM and engineer to agree on the tool's purpose before writing code, and the sentence goes straight into the description.

---

## PM Decision Framework for Schema Design

For each tool in your feature, ask:

| Question | Output |
|----------|--------|
| What name will non-ambiguously identify this tool? | The `name` |
| What is the one-sentence "when to use" statement? | First sentence of `description` |
| What does this tool return and in what format? | Last sentence of `description` |
| Which parameters are strictly required? | `input_schema.required` |
| For each param, what values are legal? (enum? range? format?) | Property `type`, `enum`, examples in `description` |
| Are there related tools Claude might confuse this with? | Cross-reference in `description` |
| What happens if Claude sends malformed arguments? | Define recovery UX (ties to tool function error handling) |

---

## Common PM Mistakes

1. **Letting engineering ship one-line descriptions** — skipping copy review means Claude misroutes user requests.
2. **Describing implementation instead of intent** — "Calls the /v1/time endpoint" tells Claude nothing about when to use it.
3. **Forgetting to enumerate valid values** — "temperature unit" should be an `enum: ["celsius", "fahrenheit"]`, not a freeform string.
4. **Not cross-referencing similar tools** — in a system with many tools, Claude needs help disambiguating. "This tool returns the current time; to schedule something in the future, use `create_reminder`."
5. **Updating code without updating the schema** — parameter renames and new optional fields must be reflected in the schema, or Claude's priors go stale.

> **Key Insight**
>
> Tool schema descriptions are product copy that your AI reads and acts on. Treating them as an engineering afterthought is like shipping an app with a blank app-store listing: you'll get lower usage and worse user experiences. PMs who own schema copy as rigorously as they own UI copy ship features that feel dramatically more capable. On the CCA exam, this shows up under D2 questions about tool design and selection.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: three required fields of a tool definition, description best practices, `required` semantics, `enum` for constrained values.
- **D1 (Agentic Architecture)**: description quality is what drives Claude's tool selection in the agent loop.
- Expect product-framed questions: "A team has two similar tools and Claude often picks the wrong one. What is the most likely fix?" — answer: improve descriptions, add 'when to use' sentences, cross-reference between tools.

---

## Flashcards

| Front | Back |
|-------|------|
| What are the three required fields of a tool definition? | `name`, `description`, and `input_schema`. |
| What is the menu-item analogy for tool schemas? | Name is the dish name; description is the menu description; properties are the ingredients/constraints; required fields are the "must pick a side" choices. |
| What is the most frequently skipped sentence in a schema description? | The "when to use" sentence — it tells Claude which tool to pick when several are available. |
| Why should PMs review tool descriptions? | They are product copy Claude reads on every invocation; they directly influence feature reliability and user experience. |
| How do you prevent Claude from confusing two similar tools? | Cross-reference them in each description ("for X instead, use the `other_tool` tool"). |
| When should you use `enum` in a parameter description? | When there is a fixed set of valid values (e.g., units, statuses, categories) — it eliminates ambiguity. |
| What does `required` mean in a tool schema? | It lists the parameter names Claude must supply; anything not listed is optional. |
| What PRD line item captures the tool's purpose for Claude? | "Claude should use this tool when: *(one sentence)*" — goes straight into the description. |
