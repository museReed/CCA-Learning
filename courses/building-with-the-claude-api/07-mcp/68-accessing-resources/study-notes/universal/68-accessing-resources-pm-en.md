# Accessing Resources — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.3 (client-side MCP resource usage), 1.2 (context injection) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 68 |

---

## One-Liner

Accessing resources is the part of MCP that turns "@mention" into a product feature: your app asks the server for the referenced data and hands it to Claude inside the prompt — zero tool calls, zero guessing, predictable latency and cost.

---

## Mental Model: Handing Claude a Folder Instead of a Map

- **Tool calls** are giving Claude a map and hoping it walks to the right building. Fast if it knows where to go, slow and error-prone if it doesn't.
- **Resource access** is handing Claude a folder with the exact document already opened. Claude starts reading immediately — no detour, no decision required.

When users explicitly point at a thing ("use this document", "look at this record"), resource access is almost always the right pattern.

---

## Why PMs Should Care

The difference between "@mention" built as a tool vs built as a resource is night-and-day in practice:

| Metric | Tool call path | Resource access path |
|--------|----------------|---------------------|
| API round trips per user message | 2+ | 1 |
| Latency overhead | ~1.5–3s per extra turn | ~0ms (happens before the Claude call) |
| Token cost | tool schema + tool_use + tool_result + final answer | just the injected content |
| Reliability | depends on Claude choosing correctly | deterministic |
| UX | "thinking..." spinner longer | snappier response |

A feature launched with resource access will feel faster and cost less — immediately, without any prompt tuning.

---

## Product Use Cases

### When to Use Resource Access

| User Experience | Why Resource Access Fits |
|-----------------|--------------------------|
| @mention a document / record / ticket | User explicitly chose what to include |
| Always-on context (company policies, glossary) | Must be there every time |
| "Summarize this page" with a page ID selector | Deterministic lookup, no Claude decision needed |
| File picker → inject | App knows which file, no ambiguity |

### When Resource Access Is Not Enough

| User Need | Better Pattern |
|-----------|---------------|
| Let Claude decide mid-conversation whether to look up more | Tool call |
| Search across many items | Tool call that takes a query |
| Conditional fetch based on reasoning | Tool call |
| Actions with side effects | Tool call (never a resource) |

---

## PM Decision Framework

For any "fetch and show" feature, ask:

| Question | If Yes | Implication |
|----------|--------|-------------|
| Does the user specify which thing to fetch? | Yes | Resource access |
| Is the set of candidates known at the time we build the UI? | Yes | Resource access (can be a dropdown / autocomplete) |
| Do we want the fetch to always happen for this intent? | Yes | Resource access |
| Should Claude be free to skip the fetch? | Yes | Tool call |
| Does the fetch need search / ranking? | Yes | Tool call (Claude passes the query) |

---

## UX Implications to Design

Because resource access happens **before** the Claude call, the UX burden sits in your own app:

- **Discovery** — how do users know a resource exists? (@ autocomplete, slash menu, file picker)
- **Selection affordance** — dropdown vs fuzzy search vs typed command
- **Progress indicator** — the resource fetch still has latency; show a subtle loader
- **Error states** — "that document is no longer available" when the URI fails
- **Preview** — show what will be injected before the user commits (optional but delightful)

This is pure product design, not prompt engineering. Your designers own it.

---

## Cost and Context-Window Implications

Resource access is cheap per API call but not free in tokens — the injected content occupies space in the prompt. PMs should plan for:

- **Large documents** — can the content fit in the context window? Plan truncation or chunking rules.
- **Many resources at once** — if users can @mention multiple items, the combined size can blow up. Set a limit.
- **Stale data** — the content is a point-in-time snapshot. Decide if you need to refetch per turn.
- **Sensitive data in logs** — injected content flows through your telemetry. Redact accordingly.

---

## Common PM Mistakes

1. **Building @mention as a tool call** — it works, but is twice as slow and twice as expensive for no user benefit.
2. **Letting resources grow unbounded** — a 50-page PDF injected into every turn will burn context and latency. Define limits.
3. **No UX for resource discovery** — a resource that users cannot find is a resource that does not exist.
4. **Forgetting error states** — resources can fail (missing, permissioned, too large). Your UI must handle it.
5. **Skipping preview affordance** — letting users see what is about to be injected increases trust and reduces "why did Claude say that?" escalations.

> **Key Insight**
>
> Resource access is the pattern that makes user-driven context feel invisible. From the user's perspective: "I mentioned a file, Claude read it." From the architecture: one API call instead of two, deterministic content, and a clean separation between "what the app fetched" and "what Claude reasoned about." For PMs, this is the single highest-leverage pattern to know when designing context-rich Claude features.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: know that resource access lives in the MCP client (e.g., `read_resource`) and runs before the Claude call, not during a tool loop.
- **D1 (Agentic Architecture)**: resources shorten the agent loop by injecting context up front.
- Exam pattern: "A user @mentions a document. How does the document content reach Claude?" → the client fetches the resource and inlines it into the prompt — no tool call.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the "folder vs map" analogy? | Tool calls give Claude a map to hopefully find data. Resource access hands Claude a folder with the document already opened. |
| Why is resource access cheaper than a tool call for @mention features? | One API round trip instead of two, fewer tokens overall, and no wait for Claude to decide whether to fetch. |
| Which team owns the UX for resource discovery? | Your product/design team — the user-facing @ autocomplete, file picker, or slash menu. |
| What cost does resource access still incur? | The injected content consumes prompt tokens and can push against the context window. |
| When is a tool call better than a resource? | When Claude should reason about whether to fetch, when the fetch needs search, or when the operation has side effects. |
| What should a PRD for an @mention feature include? | Limits on size/count of mentions, fallback UX on resource failure, preview affordance, latency budget, and privacy rules for injected content. |
| Why is resource access more deterministic than a tool call? | The app guarantees the fetch happens; Claude never decides and never skips it. |
| What happens before Claude is even called in a resource-based flow? | The app uses the MCP client to fetch the resource and inline it into the prompt being built. |
