# Defining Tools with MCP — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.1 (tool schemas), 2.3 (MCP primitives: tools), 1.2 (agent loop integration) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 64 |

---

## One-Liner

Lesson 64 is where tool authoring becomes **cheap**: the Python MCP SDK replaces hand-written JSON Schema with decorated functions, collapsing the time-to-first-tool from "a day of boilerplate" to "a paragraph of Python" — which changes how PMs should scope AI features.

---

## Mental Model: From Schematics to Business Cards

Before the SDK, adding a tool felt like drafting electrical schematics:

| Pre-SDK (hand-written JSON) | With SDK (decorators + type hints) |
|-----------------------------|-----------------------------------|
| Long JSON Schema docs | A decorated Python function |
| Easy to miss a `required` key | SDK fills it in from function signature |
| Hard for non-author devs to read | Reads like business logic |
| Docs live far from the code | Description sits on the parameter itself |

Think of MCP tools with the SDK as **business cards**: small, standardized, legible — a new tool fits on a few lines and is ready to hand out to Claude.

---

## Why This Lesson Matters for PMs

Three product-level consequences of the SDK's ergonomics:

1. **Tool count becomes cheap.** If adding a new tool costs minutes, PMs can safely ask for more granular capabilities — one tool per intent — instead of mega-tools that bundle behavior.
2. **Descriptions become product copy.** The `description` is Claude's instruction manual; writing it well is a PM/writer job, not just an engineering job. It is the tool's prompt engineering.
3. **Error handling is part of UX.** When a tool fails (`ValueError`), Claude surfaces the error to the user. That means tool error messages are **user-visible copy**. PMs should review them.

---

## Walkthrough of the Two Demo Tools

The lesson implements two tools against an in-memory document store:

| Tool | Business role |
|------|---------------|
| `read_doc_contents` | "Let Claude look up a specific document by ID" |
| `edit_document` | "Let Claude propose and apply a find/replace edit" |

The descriptions explicitly warn Claude about subtle gotchas — for example, `old_str` specifies "must match exactly, including whitespace". A PM reading this should treat tool descriptions as **the guardrail layer between Claude and real-world side effects**.

### The Find/Replace Caveat (Product Warning)

`edit_document` uses Python's `str.replace`, which replaces **every** occurrence in the document. That's fine for a demo; in a real product, it is a footgun:

> "Replace the word 'budget' with 'expenditure'" could silently change every mention of 'budget' across the document, not just the one the user intended.

A PM should flag this. Real products typically need:

- A uniqueness check on the match
- A preview-before-apply step
- An audit log of all edits
- User approval for destructive actions

---

## Product Use Cases

### Where lightweight tool authoring pays off

| Scenario | Why it fits |
|----------|-------------|
| Rapid feature iteration | A new tool is a ~10-line change; PMs can experiment |
| Domain-specific assistants | Author one tool per domain action (read policy, propose edit, post summary) |
| Internal platform teams | Standardize a library of company tools via a shared MCP server |
| Tool catalogs | Multiple tools with clear, single responsibilities; Claude picks at runtime |

### Where low friction is a risk

| Scenario | Caution |
|----------|---------|
| Mutating production systems | Low friction makes it easy to ship risky tools — require review |
| Ambiguous tool names | Claude's selection depends on description quality; sloppy copy = wrong tool chosen |
| Overlapping tools | Two tools doing similar things confuses Claude; PMs should deduplicate |
| Silent side effects | `edit_document` replaces all matches; real products need explicit confirmation |

---

## PM Decision Framework: Reviewing a Tool PR

When your team adds a new MCP tool, as a PM you should check:

1. **Is the tool's `name` clear and imperative?** (`read_doc_contents`, not `docs_tool_3`)
2. **Does the `description` tell Claude what it does AND what it won't do?** (e.g. "must match exactly, including whitespace")
3. **Does every parameter have a `Field(description=...)`?** Missing descriptions degrade tool quality.
4. **What happens on failure?** The tool should raise a user-readable error, not silently fail.
5. **Is the tool destructive?** If yes, is there approval/confirmation in the product flow?
6. **Is there overlap with existing tools?** If so, merge or rename to disambiguate.

---

## Descriptions as Copywriting

The MCP tool description is arguably the most underestimated piece of copy in a Claude product:

| Property | Implication |
|----------|-------------|
| Read by Claude, not users | No marketing fluff; plain declarative language wins |
| Used for tool selection | Ambiguous descriptions → wrong tool called |
| Constrains agent behavior | You can set expectations ("use only when you have an exact doc ID") |
| Invisible to eng reviewers | Code review doesn't catch weak copy — PM must review |

A PM rule of thumb: if a tool description wouldn't pass a technical writer's review, it probably wouldn't pass Claude's either.

---

## Common PM Mistakes

1. **Reviewing tool code but not tool descriptions** — the description is the API contract with Claude.
2. **Scoping mega-tools** — one tool that "does everything with a document" is harder for Claude than three focused tools.
3. **Ignoring destructive side effects** — `edit_document` silently replaces all matches; that needs product UX around it.
4. **Assuming error messages are internal** — `ValueError` text reaches the end user via Claude; make it clear.
5. **Treating SDK ergonomics as "engineering only"** — the productivity win changes how fast you can experiment at the PM level.

> **Key Insight**
>
> MCP tool definitions with the Python SDK are a PM surface, not just an engineering surface. The `name`, `description`, and parameter docs are product copy that shapes Claude's behavior and user-visible outputs. When tool authoring becomes this cheap, the bottleneck shifts from engineering effort to product judgment — and that's where PMs earn their keep.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: Know that the SDK pattern is `FastMCP` + `@mcp.tool(...)` + `Field(description=...)`.
- **D1 (Agentic Architecture)**: Understand that tool errors (raised exceptions) propagate through the agent loop and Claude can incorporate them in its next turn.
- Be ready for scenario questions about tool naming, description quality, and error surfacing.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the PM takeaway from the SDK-based tool pattern? | Tool authoring is now cheap enough that PMs can ask for more, narrower tools instead of mega-tools. |
| Who should review the `description` field on a tool? | The PM — it is product copy that shapes Claude's behavior. |
| What is the hidden risk of `edit_document` in the lesson? | It calls `str.replace`, replacing every occurrence; real products need uniqueness or confirmation. |
| Why do tool errors matter at the product level? | When a tool raises `ValueError`, Claude surfaces the message to the user — it is user-visible copy. |
| What happens when a parameter has no `Field` description? | Claude only sees the parameter name, so tool selection and usage quality drops. |
| How many tools does the demo server expose, and what do they do? | Two: `read_doc_contents` and `edit_document` (find-and-replace). |
| What is the PM rule for tool overlap? | Two tools doing similar things confuse Claude — dedupe or rename. |
| What's the one-sentence PM framing of tool descriptions? | They are Claude's instruction manual, and therefore product copy. |
