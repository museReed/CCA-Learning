# Project Setup — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.3 (MCP primitives), 1.2 (agent loop integration), 2.1 (tool schemas) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 63 |

---

## One-Liner

Lesson 63 is the "environment readiness" checkpoint: before your team writes any MCP code, verify the baseline CLI chatbot can talk to Claude — because every MCP feature that follows rides on top of that baseline.

---

## Mental Model: The IKEA Instructions Step Before Assembly

Think of this lesson as the IKEA instruction page that says *"open the box, lay out the parts, confirm all items are present."* You haven't built anything yet. You are checking that you **can** build.

| IKEA step | MCP project step |
|-----------|------------------|
| Unbox and lay out parts | Extract `cli_project.zip` |
| Check the parts list | Verify `main.py`, `mcp_client.py`, `mcp_server.py` present |
| Check the tools | Install `uv` or `pip` + venv |
| Check the connectors | Add `ANTHROPIC_API_KEY` to `.env` |
| Test move a single screw | Ask the bot `what's 1+1?` |

Skipping IKEA's setup page leads to a wobbly bookshelf. Skipping Lesson 63 leads to MCP bugs that are really setup bugs in disguise — and those cost the most engineering time to debug.

---

## Why This Lesson Matters for PMs

A PM may wonder why to bother with an "install the project" lesson at all. Three reasons:

1. **Environment is where AI features die.** "It worked on the demo" → "it failed in prod" is usually an env story, not a code story. MCP adds subprocesses and SDK versioning on top of normal Claude API use.
2. **The project shape is your feature shape.** The CLI chatbot in this lesson is the minimum viable reference architecture: host + client + server + env file. A PM who internalizes this triad can reason about any future MCP feature.
3. **Defining "done" for bootstrapping.** The lesson hands the team a crisp acceptance criterion for initial setup: `what's 1+1?` returns an answer. That's one less ambiguous "is it working yet?" conversation.

---

## The Product-Relevant Architecture Callout

The lesson explicitly flags that in real projects teams usually build **either** an MCP client **or** an MCP server, not both:

| Team intent | Build the... |
|-------------|--------------|
| "We want Claude-powered chat over our internal data" | MCP client + existing servers |
| "We want to expose our SaaS to every AI agent on the market" | MCP server that others consume |
| "We're building a platform layer" | Possibly both, but separate repos |

From a PM perspective this is a **scoping decision** you make once and live with:

- MCP server author = you are productizing your data/actions to agents.
- MCP client author = you are productizing an AI experience to end users.

The course builds both in one repo purely for education — don't let that blur your product's scope.

---

## Product Use Cases for the Bootstrapped Project

The lesson's CLI chatbot is a toy, but the shape is directly useful:

| Realistic product | How the shape maps |
|-------------------|--------------------|
| Internal docs assistant | In-memory docs → real knowledge base; CLI → web UI |
| Dev-tools CLI that edits config | find-and-replace tool → templated config edits |
| Ops runbook assistant | read + update tools → runbook read and amend |
| Compliance review bot | read tool → read policy docs; update tool → propose redlines |

Any PM scoping an AI feature that reads + writes a small bounded data set can treat this project as a working template.

---

## PM Decision Framework

Before your team starts down this lesson with a real product in mind, ask:

1. **Which side is our product?** Client (consume servers), server (publish tools), or rare-case both?
2. **Where will secrets live in prod?** `.env` is fine for dev; production needs a secret manager.
3. **What's our minimum viable data set?** In the demo it's a dict. In prod it's whatever you can safely let Claude read and edit.
4. **Who owns the CLI vs UI layer?** The lesson uses a CLI; your product will likely have a real front end. Plan that transition.
5. **What's the acceptance criterion for "setup works"?** Copy the lesson's approach — define a tiny, testable smoke check.

---

## Operational and Cost Notes

Even a blank-slate project has cost implications:

| Item | Why a PM should care |
|------|----------------------|
| API key | Billing starts the moment the baseline `what's 1+1?` runs |
| `uv` vs `pip` | Affects CI time and onboarding speed |
| `.env` policy | Secret sprawl risk — make sure it's gitignored from day 1 |
| Starter code vs completed code | Anthropic ships both `cli_project.zip` and `cli_project_COMPLETE.zip`; pick one for reference |

---

## Common PM Mistakes

1. **Treating Lesson 63 as skippable** — a broken baseline makes every later lesson harder to debug.
2. **Assuming a CLI is the final UX** — it is a course artifact; your product needs real UI.
3. **Blurring client/server ownership** — resist building "both in one service" just because the course did.
4. **Letting the API key live in `.env` forever** — plan the migration to a secret manager before go-live.
5. **Not defining a smoke test** — copy the `1+1?` pattern for your own product, scaled to your real data path.

> **Key Insight**
>
> This lesson looks like DevOps plumbing, but it quietly hands the PM an invaluable artifact: a **minimum viable MCP architecture** (host + client + server + env + baseline check). Any real product you scope can be reasoned about as a specialization of that shape. Memorize the shape; it recurs everywhere.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: Know that Ch07's working example is a CLI chatbot over in-memory documents with read and update tools.
- **D1 (Agentic Architecture)**: Recognize the host/client/server triad as the canonical MCP layout.
- Be ready for scenario questions that ask which half (client or server) a team should build given a product goal.

---

## Flashcards

| Front | Back |
|-------|------|
| What does Lesson 63 actually teach? | How to bootstrap the Ch07 project so the chatbot can talk to Claude before any MCP code exists. |
| What is the baseline smoke test? | Ask the bot `what's 1+1?` and confirm Claude responds. |
| In production, should a team build both an MCP client and server? | Usually only one — the course builds both for teaching purposes. |
| What does the demo store documents in? | An in-memory Python dictionary — no database. |
| Which two install paths does the README support? | `uv run main.py` (recommended) and standard Python + pip + `python main.py`. |
| What secret must be present before first run? | `ANTHROPIC_API_KEY` in `.env` |
| What is the PM takeaway from the "client or server, not both" note? | Your product usually picks one role; conflating them is a scoping smell. |
| What concrete artifact does this lesson hand the PM? | A reusable minimum viable MCP architecture template: host + client + server + env + baseline check. |
