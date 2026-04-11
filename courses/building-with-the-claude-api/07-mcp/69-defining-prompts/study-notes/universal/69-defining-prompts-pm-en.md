# Defining Prompts — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.3 (MCP primitives: prompts), 1.2 (agent loop priming) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 69 |

---

## One-Liner

Prompts are MCP's "greatest hits playlist" — curated, expert-tuned instructions the server author ships so users get consistently high-quality results without having to learn prompt engineering themselves. They turn unreliable free-text requests into predictable, brand-consistent features.

---

## Mental Model: The Cookbook Recipe

- Users writing their own instructions are home cooks improvising. Sometimes they nail it; sometimes it is inedible.
- Prompts are the cookbook the restaurant author gives them. Follow the recipe, get the chef's version every time.
- Users still customize via parameters (the `doc_id` is the ingredient swap), but the method is locked in.

Good MCP servers ship recipes for their most common use cases. Users pick from a slash-menu; the server does the heavy prompt lifting.

---

## Why PMs Should Care

Free-form prompting is the AI product equivalent of "type a command in the terminal." Expert users love it. Everyone else bounces. Prompts convert expert knowledge into:

- **Consistent quality** — every user gets the same tested result
- **Discoverable features** — prompts become slash-commands, quick actions, buttons
- **Brand voice** — your writing style, your formatting, your tone, baked into the template
- **Onboarding shortcuts** — new users hit "run prompt" and see a great result immediately
- **Cost control** — tuned prompts are usually shorter and more focused than what users type

For a PM, prompts are the productization layer on top of tools and resources.

---

## Product Use Cases

### When Prompts Pay Off

| Scenario | Why Prompts Are the Right Layer |
|----------|---------------------------------|
| A task your users do repeatedly (reformat, summarize, translate) | Codify the best version once |
| A task where wording matters a lot (tone, structure, compliance) | Lock down the wording |
| Features you want to expose as slash-commands or quick actions | Prompts naturally map to UI affordances |
| Low-confidence users who want "just make it good" | Hide the prompt complexity behind a button |

### When Prompts Are Overkill

| Scenario | Better Pattern |
|----------|---------------|
| One-off tasks with no repeat users | Free-form input is fine |
| Highly variable tasks where constraints hurt | Let users write their own |
| Tasks that are really data lookups | Use a resource |
| Tasks that are really actions | Use a tool |

---

## How Users Experience a Prompt

From the user's side, a prompt usually appears as:

1. A slash-command (`/format`, `/summarize`) in a CLI or chat UI
2. A button or quick action in a graphical app
3. A template picker on first launch

They select it, fill in one or two parameters (like which document), and the system runs the full pre-engineered instruction. The user never sees — and never has to write — the underlying prompt text.

---

## PM Decision Framework

Before building a prompt, ask:

| Question | If Yes | Implication |
|----------|--------|-------------|
| Is the output quality highly sensitive to how the request is worded? | Yes | Ship a prompt |
| Is this a repeat task across many users? | Yes | Ship a prompt |
| Does the expertise to do this well live with your team? | Yes | Ship a prompt (externalize the knowledge) |
| Will users want to do the task in many different creative ways? | Yes | Do NOT ship a prompt; leave free-form |
| Does the prompt need live data? | Yes | Combine prompt with a resource or tool |

---

## Quality Bar: When Is a Prompt "Good Enough" to Ship?

The lesson's guidance is strict: only ship prompts that are demonstrably better than what users would write themselves. A rough checklist:

1. **Tested on 5+ realistic inputs** — does it produce good output every time?
2. **Clear parameter schema** — each argument has a description that the client can display.
3. **Works with your tools and resources** — the prompt references real server primitives, not imagined ones.
4. **Survives edge cases** — empty inputs, non-standard document IDs, edge lengths.
5. **Has a one-line description** — users choose from a menu based on that string.

If your prompt does not beat a 30-second ad-hoc attempt, do not ship it. You will train users to distrust prompts.

---

## Common PM Mistakes

1. **Shipping too many prompts** — more prompts than users can scan produce decision paralysis. Prune ruthlessly; 3–10 great prompts beats 50 mediocre ones.
2. **Vague descriptions** — if users cannot tell what a prompt does, they will not pick it. Write them like button labels.
3. **Treating prompts as static config** — they need versioning, eval, and iteration like any other model-facing code.
4. **Mixing prompts with data** — if you find yourself hardcoding the document content in the prompt, you actually want a resource.
5. **Not measuring prompt quality** — track which prompts get selected and which produce rework. Kill the losers.

> **Key Insight**
>
> Prompts are the primitive that turns MCP from "developer SDK" into "product surface." Tools and resources make the server capable; prompts make it usable. A PM who understands this ships small, crisp menus of high-quality actions — the AI-product equivalent of a well-organized slash-menu in Notion or Linear — and users feel they got a great tool without ever opening a text box.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: prompts are the third MCP primitive (after tools and resources); know that they are parameterized and return a sequence of messages.
- **D1 (Agentic Architecture)**: prompts seed the agent loop with a high-quality starting conversation.
- Exam pattern: "A server author wants to ship a reusable 'reformat to markdown' command. Which primitive?" → prompt.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the "cookbook recipe" analogy for prompts? | Users writing their own prompts are improvising cooks; prompts are the cookbook recipes the restaurant author ships — users fill in ingredients (parameters), get chef-quality results. |
| Why are prompts a productization layer? | They take expert prompt-engineering knowledge and expose it to users as simple slash-commands or quick actions. |
| When should a PM NOT ship a prompt? | When the task varies widely per user, is one-off, or is really a data lookup (resource) or action (tool). |
| What makes a prompt "shippable"? | Tested on realistic inputs, clear parameter schema, works with server tools/resources, handles edge cases, has a clear one-line description. |
| Why do vague descriptions kill prompts? | Users select prompts from a menu based on the description; vague ones never get picked and waste engineering effort. |
| Should you ship 50 mediocre prompts or 5 great ones? | 5 great ones — more prompts cause decision paralysis and dilute perceived quality. |
| How do prompts compose with tools and resources? | A prompt can reference a tool (e.g., "use `edit_document` to save the result") or a resource, acting as a recipe for a multi-step workflow. |
| What happens if a prompt hardcodes document content instead of a parameter? | You are using a prompt where you actually wanted a resource — prompts are templates, resources are data. |
