# Prompts in the Client — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.3 (client-side MCP prompt usage), 1.2 (agent loop seeding) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 70 |

---

## One-Liner

Wiring prompts into the client is what turns them from "server-side potential" into "user-visible buttons" — it is the last mile that lets your product ship slash-commands, quick actions, and template galleries that hide all the prompt engineering behind a single tap.

---

## Mental Model: The Remote Control With Named Buttons

Imagine your MCP server is a capable appliance — it can cook anything. Without prompts in the client, users stand in front of it with a manual typing raw instructions. With prompts in the client, you give them a remote control:

- `/format` button → reformats documents to markdown
- `/summarize` button → condenses content
- `/translate` button → converts languages

Each button is a pre-engineered recipe. The user taps it, maybe picks an argument (which document), and the appliance does its thing. The recipe lives on the server; the button lives in the client. This lesson is about how the button gets wired up.

---

## Why PMs Should Care

This is where prompts go from an engineering abstraction to a **product feature you can point at in a demo**. Without client-side wiring, prompts are invisible. With it:

- Users see a **discoverable menu** instead of a blank text box
- Onboarding flows can open with "try this prompt"
- Support can say "click `/format` to fix this document"
- Analytics can track which prompts get used
- Marketing can showcase specific commands

The two client methods (`list_prompts`, `get_prompt`) are small in code but large in product surface. Every prompt you want to ship lives and dies on whether the client exposes it well.

---

## What the Client Actually Shows the User

The canonical flow from the user's point of view:

1. User types `/` or clicks a "commands" button.
2. The client calls `list_prompts()` and renders a menu with names and descriptions.
3. User picks one (say `format`).
4. The client reads the argument metadata and prompts for required inputs (e.g., "Which document?").
5. The client calls `get_prompt("format", {"doc_id": "report.pdf"})` under the hood.
6. The server returns the full message list — the user does not see this step.
7. The client sends the messages to Claude and shows the streaming response.

From the user's point of view: "I picked an action and it just worked." From the PM's point of view: every step above is a design decision.

---

## Product Use Cases

### When Client-Side Prompt Wiring Shines

| Scenario | Why It Works |
|----------|--------------|
| Complex apps with many possible actions | A slash menu beats dumping everything into one free-form prompt |
| Onboarding new users | Curated prompts demo the product's capability immediately |
| Teams sharing best-practice workflows | Prompts become organizational knowledge |
| Reducing support load | "Click `/format`" is shorter than "copy this prompt text" |
| Brand-consistent outputs | Each prompt enforces a specific style/format |

### When It Is Overkill

| Scenario | Better Approach |
|----------|-----------------|
| Single-use prototype | Skip the plumbing; just hardcode text |
| Totally free-form chat product | Prompts limit more than they help |
| No MCP server yet | Build the server first (Lesson 69) |

---

## PM Decision Framework

When designing a prompt-powered feature, ask:

| Question | If Yes | Implication |
|----------|--------|-------------|
| Will users need to discover the prompt on their own? | Yes | Must ship client-side listing (`list_prompts`) |
| Does the prompt take arguments? | Yes | Design the argument picker UX (dropdown, autocomplete, form) |
| Will the prompt be invoked repeatedly? | Yes | Consider surfacing as a top-level button, not buried in a menu |
| Do you want telemetry on prompt usage? | Yes | Instrument the client side; server-side usage is invisible to the product team |
| Should the prompt name match a brand voice? | Yes | Name and description are marketing copy — treat them as such |

---

## UX Design Notes

Because prompts appear in the client, these are PM/design decisions:

- **Naming** — `/format` is better than `/do_format_thing_v2`. Short, verb-first, obvious.
- **Descriptions** — one line, outcome-focused ("Rewrite document in markdown"), not feature-focused ("Uses the MCP prompt `format_document` with doc_id parameter").
- **Argument collection** — most users will not read forms. Provide defaults, smart autocomplete, and sensible fallbacks.
- **Discoverability** — `/` menu, quick actions bar, onboarding callouts. Pick at least one.
- **Feedback** — show a loading state while `get_prompt` runs, then stream the Claude response.
- **Error handling** — if the server is unreachable or the prompt errors, show "this command is temporarily unavailable" instead of a raw stack trace.

---

## Common PM Mistakes

1. **Shipping prompts without a discovery affordance** — users will not find them, so they do not exist.
2. **Cryptic names and descriptions** — treat prompt metadata as microcopy; iterate on it as you would a button label.
3. **No argument UX** — users will bounce rather than type a raw `doc_id`. Provide a picker.
4. **No analytics** — if you cannot see which prompts get used, you cannot prune the losers.
5. **Fragile error paths** — server hiccups should degrade gracefully; the user should not see Python exceptions.

> **Key Insight**
>
> `list_prompts` and `get_prompt` are the cheapest investment a PM can demand for the highest product impact. They turn engineering-maintained recipes into product-visible actions without any per-prompt eng work after the first setup. A well-wired client means every new prompt the server author ships appears in your product automatically — roadmap on autopilot.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: know that the client exposes `list_prompts` and `get_prompt` to let users discover and invoke prompts.
- **D1 (Agentic Architecture)**: prompts seed the agent loop; the rest of the loop (tools, resources) proceeds normally.
- Exam pattern: "How are MCP server prompts surfaced to users?" → the client implements `list_prompts`/`get_prompt` and typically renders them as a slash menu.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the "remote control with named buttons" analogy? | The server is an appliance that can do anything; the client's prompt wiring is the remote whose buttons each correspond to a pre-engineered recipe. |
| What are the two client methods that expose prompts to users? | `list_prompts()` for discovery and `get_prompt(name, args)` for invocation. |
| Why do prompts need client-side wiring? | Without it, prompts are invisible — they exist on the server but users cannot find or trigger them. |
| What should a good prompt name look like? | Short, verb-first, obvious — e.g., `/format`, not `/do_format_thing_v2`. |
| Why is analytics instrumentation a PM responsibility? | Server-side prompt execution is invisible to product teams; analytics have to live in the client where users actually interact. |
| How should the UX collect arguments? | With pickers, autocomplete, and defaults — not by asking users to type raw argument keys. |
| What happens when the server errors on `get_prompt`? | The client should degrade gracefully — "this command is temporarily unavailable" — never show a stack trace. |
| Why is client-side prompt wiring the "last mile" of MCP? | Because tools, resources, and server-side prompts are all useless to users unless the client surfaces them as discoverable actions. |
