# Accessing Resources — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP client implementation), 2.4 (resource consumption patterns), 2.5 (content type handling) |
| Source | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 11 |

---

## One-Liner

Accessing resources is like your app pulling files from a shared drive and placing them on the meeting table before the discussion starts — Claude sees the data immediately without needing to ask for it.

---

## Why PMs Need to Understand Resource Access

Resource access is the client-side pattern that powers features like:
- **Document mentions** (`@plan.md` in a chat interface)
- **Context panels** (sidebar showing relevant data)
- **Autocomplete dropdowns** (selecting from available items)

As a PM, understanding this pattern helps you:
1. **Spec the right interaction model** — users see data instantly, not after Claude "looks it up"
2. **Set realistic performance expectations** — resource injection is faster than tool-based retrieval
3. **Design better UX flows** — the `@mention` pattern is a proven interaction paradigm

---

## Mental Model: The Meeting Briefing

Imagine you are organizing a meeting:

| Approach | Analogy | MCP Equivalent | User Experience |
|----------|---------|----------------|-----------------|
| **Pre-meeting briefing** | Assistant prints relevant reports and places them on the table before the meeting starts | **Resource access** | Fast — everyone can reference docs immediately |
| **Mid-meeting lookup** | Someone says "let me go check the filing room" and leaves to get a document | **Tool call** | Slower — meeting pauses while data is fetched |

Resources are the pre-meeting briefing. Your application gathers the data in advance and hands it to Claude as context. Claude never has to "leave the room" to get information.

---

## The `@Mention` User Journey

Here is the step-by-step UX flow that resource access enables:

1. **User types `@` in the chat input** — the app queries the server for available resources
2. **Autocomplete dropdown appears** — showing available documents, data sources, or references
3. **User selects an item** (arrow keys + space) — the app fetches the full content of that resource
4. **Content is silently injected into the prompt** — the user does not see the raw content; it becomes invisible context
5. **User presses Enter to send** — Claude receives both the user's question and the referenced document
6. **Claude responds with full context** — no "let me look that up" delay, no additional tool calls

This is the same pattern you see in Claude's official interface when using "Add from Google Drive."

---

## Product Implications

### Performance
Resource injection happens before Claude starts reasoning. This means:
- **No extra latency** from tool calls
- **No wasted tokens** from Claude describing what it is about to look up
- **First response is already informed** — no follow-up round-trips

### Data Format Awareness
Resources come with format hints (MIME types) that affect how your app handles them:

| Data Format | What the App Does | PM Consideration |
|-------------|-------------------|------------------|
| Structured data (JSON) | Parses into objects for rich display | Can power tables, charts, or filters in the UI |
| Plain text | Displays as-is or injects into chat | Simple to implement but limited visual options |
| Binary (PDF, images) | Needs special rendering | Requires viewer component in your UI spec |

### Error Handling
If a resource is not found or unavailable, the app should handle this gracefully. In your PRD, specify:
- What the user sees when a referenced document is unavailable
- Whether to show a warning or silently omit the resource
- Fallback behavior (e.g., Claude can still answer without the resource)

---

## Comparison: Resource Access vs. Tool-Based Retrieval

| Aspect | Resource Access | Tool-Based Retrieval |
|--------|----------------|---------------------|
| Trigger | User selects `@mention` or app pre-loads | Claude decides to call a tool |
| Timing | Before Claude responds | During Claude's reasoning |
| User perception | Instant context | "Let me look that up..." delay |
| Token efficiency | Data is already in prompt | Extra tokens for tool call + result |
| Control | App-controlled (deterministic) | Model-controlled (Claude decides) |

---

## Common PM Mistakes

1. **Designing tool-based UX when resources would work** — if the user explicitly selects what data to include, use resources (not tools)
2. **Not specifying the autocomplete experience** — resource-powered autocomplete needs design specs: search behavior, result ranking, display format
3. **Ignoring data size** — large resources (entire databases, huge documents) should be paginated or summarized before injection
4. **Assuming Claude controls resource access** — resources are app-controlled; Claude does not decide when to fetch them

> **Key Insight**
>
> The `@mention` pattern powered by resources creates a user experience where context is gathered **before** the AI starts thinking. This is fundamentally faster and more predictable than tool-based data retrieval. When writing PRDs, always ask: "Can this data be pre-loaded as a resource, or does Claude need to decide when to fetch it?"

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: Expect questions about the client-side resource pattern. Know that `read_resource()` returns a `contents` list and that MIME types determine parsing behavior.
- **D1 (Agentic Architecture)**: Resource access reduces latency by injecting data into the prompt before model reasoning. This is a key architecture trade-off.
- Watch for scenarios describing "data appears in the interface" or "context is pre-loaded" — these describe resource access, not tool calls.

---

## Flashcards

| Front | Back |
|-------|------|
| What triggers the autocomplete dropdown in the `@mention` pattern? | The client queries the server for available resources when the user types `@` |
| How is resource content delivered to Claude? | Injected directly into the prompt context — no tool call is required |
| What is the meeting room analogy for resource access? | Pre-meeting briefing: the assistant prints reports and places them on the table before the meeting starts |
| Why is resource access faster than tool-based retrieval for the user? | Data is already in the prompt before Claude starts reasoning — no extra round-trip or "let me look that up" delay |
| What determines how the client parses resource content? | The MIME type on the resource — `application/json` is parsed as JSON, `text/plain` is used as raw text |
| Who controls when resources are accessed — Claude, the app, or the user? | The application code (app-controlled), though the user may trigger it by typing `@` |
| What should a PM specify for resource error handling in a PRD? | What the user sees when a referenced document is unavailable, warning behavior, and fallback behavior |
| What real-world feature demonstrates the resource access pattern? | Claude's "Add from Google Drive" — the app fetches document content and injects it as prompt context |
