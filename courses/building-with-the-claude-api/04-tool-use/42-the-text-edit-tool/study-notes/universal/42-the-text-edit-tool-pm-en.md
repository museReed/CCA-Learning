# The Text Editor Tool — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%), D1 — Agentic Architecture (22%) |
| Task Statements | 2.3 (built-in / server tools), 1.2 (tool orchestration) |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 42 |

---

## One-Liner

The text editor tool lets your product embed a "mini Claude Code" inside any workflow — Claude already knows how to edit files; you only have to provide the sandbox it writes into.

---

## Mental Model: The IKEA Furniture Kit

Buying tools from scratch is like building a custom chair from raw wood — you design every joint. The text editor tool is like an IKEA kit: Anthropic ships all the parts (schema + command vocabulary), and you only provide the workspace (your filesystem or sandbox).

| Item | Custom Tool | Text Editor Tool |
|------|-------------|------------------|
| Schema definition | You write it | Ships with Claude |
| Command vocabulary | You design it | Predefined (view, create, str_replace, insert, undo_edit) |
| Execution code | You write it | **You still write it** |
| Sandbox / safety model | Your responsibility | **Still your responsibility** |

The speed-up is real but the safety responsibility is unchanged.

---

## What Your Product Gets

The text editor tool immediately unlocks:

- **Read files** (any granularity — whole file or specific line ranges)
- **List directory contents**
- **Create new files**
- **Replace strings within files**
- **Insert text at specific line numbers**
- **Undo recent edits**

That is the full vocabulary of a code editor. You can build products like:

- A PR refactoring bot that takes a repo and a style guide, then rewrites code
- A content migration agent that rewrites Markdown files to a new schema
- A documentation auto-updater that keeps READMEs in sync with code changes
- An onboarding assistant that sets up config files in a user's sandbox

---

## Product Use Cases

### When the Text Editor Tool Shines

| Product | Fit | Why |
|---------|-----|-----|
| Code refactoring tool | Strong | Core loop is view → edit → save |
| Documentation generator | Strong | Claude can read code and create doc files |
| Template scaffolder | Strong | Claude creates multiple files in a standard structure |
| Internal developer agents | Strong | Focused on a controlled repo sandbox |
| Headless automation (CI) | Strong | Files are the universal interface |

### When to Look Elsewhere

| Product | Better Alternative |
|---------|--------------------|
| Structured data editing (DB records) | Build a custom tool with your DB schema |
| UI / visual editing | Use specialized design tools |
| Single atomic content edit | Direct text generation without file I/O |
| Collaborative real-time doc editing | Use a document-sync service instead |

---

## The Sandbox Question

Since your code runs Claude's file commands, you decide the blast radius. This is a critical PM decision:

| Sandbox Level | Risk | Use Case |
|---------------|------|----------|
| Whole filesystem | Very high — Claude could write anywhere | Never ship to production |
| Project directory | Medium — scoped but still substantial | Internal developer tools |
| Dedicated workspace directory | Low — clean boundary | User-facing products |
| Read-only | Minimal | Analysis / review agents |
| Virtual filesystem (in-memory) | Lowest | Preview-only experiences |

Start with the strictest sandbox that still delivers the product value, then widen only with explicit justification.

---

## PM Decision Framework

| Question | If Yes | Action |
|----------|--------|--------|
| Does the product edit files as a core workflow? | Yes | Text editor tool is a great fit |
| Can you define a tight sandbox directory? | Yes | Production-ready |
| Does Claude need to create multiple related files? | Yes | Text editor handles this naturally |
| Do users expect undo functionality? | Yes | Implement `undo_edit` in your handler |
| Does the product write to critical system paths? | Yes | **Stop** — re-architect around a sandbox |

---

## The Hybrid Responsibility Model

This is the most important PM insight for built-in tools: **Anthropic owns the schema; you own the runtime**. That means:

- You decide what "file" means (could be S3 objects, Git blobs, in-memory strings)
- You decide what `create` costs (e.g., charge per file for a metered product)
- You decide retention and undo behavior
- You decide logging, auditing, and compliance

PMs sometimes assume built-in = fully managed. It is not. Built-in means "schema is pre-wired"; you still ship all the operational concerns.

---

## Common PM Mistakes

1. **Assuming the text editor tool is fully managed** — Anthropic provides the schema; your team still builds the sandbox, safety, and file operations.
2. **Not implementing `undo_edit`** — users expect undo in editor-like products; skipping it breaks the mental model.
3. **Launching with a wide-open sandbox** — "internal only" expands into production; start strict.
4. **Ignoring audit logging** — Claude's edits should be traceable for debugging, compliance, and rollback.
5. **Forgetting about `view` on directories** — the tool is about navigation, not just editing; support listing as well as reading.

> **Key Insight**
>
> Built-in tools are a hybrid: Anthropic ships the schema, you ship the runtime and the safety model. The product value of the text editor tool is that it removes weeks of schema / command design work, but none of the operational work around sandboxing, auditing, and undo. Budget accordingly.

---

## CCA Exam Relevance

- **D2 (Tool Design)**: The text editor tool is a canonical example of a built-in (schema-provided) tool requiring developer execution.
- **D1 (Agentic Architecture)**: File operations are a natural multi-turn pattern — view, edit, verify, repeat.
- Exam questions often distinguish between "built-in with local execution" (text editor) and "built-in with managed execution" (web search).

---

## Flashcards

| Front | Back |
|-------|------|
| What does Anthropic provide with the text editor tool? | The schema and command vocabulary — Claude already knows how to use it |
| What must the developer still provide? | The execution code that actually reads, writes, creates, and undoes files on disk |
| What are the file operations the tool supports? | view, create, str_replace, insert, undo_edit |
| What is the critical PM decision when shipping this tool? | The sandbox — which directory, paths, or virtual filesystem Claude is allowed to touch |
| Why is this tool a "hybrid" responsibility model? | Schema is fully managed by Anthropic, runtime and safety are fully owned by the developer |
| Name three products where the text editor tool is a strong fit. | Refactoring bots, doc generators, template scaffolders |
| What must PMs budget for beyond the tool integration? | Sandboxing, audit logging, undo behavior, path validation |
| What happens if you skip `undo_edit` in your handler? | Claude's undo attempts fail silently and the user's mental model breaks |
