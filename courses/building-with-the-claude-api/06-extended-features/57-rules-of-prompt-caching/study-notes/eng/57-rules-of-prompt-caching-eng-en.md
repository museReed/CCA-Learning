# Rules of Prompt Caching — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D5 — Enterprise Deployment (20%) — primary; D2 — Tool Design (18%) — secondary |
| Task Statements | 5.1 (cost/latency optimization), 5.2 (production performance), 2.1 (tool schema design) |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 57 |

---

## One-Liner

Prompt caching only works if you play by its rules: you opt in manually with cache breakpoints, the cached content must match byte-for-byte, a minimum of 1024 tokens must precede the breakpoint, and you get at most four breakpoints per request.

---

## Cache is Not Automatic — You Add Breakpoints

Caching is **not** enabled by default. You must explicitly mark where the cache should be taken by adding a **cache breakpoint** to a block in your request.

The mechanics:

- Work done on messages is **not cached automatically**.
- You manually add a `cache_control` field to a specific block.
- Everything **before and including** that breakpoint is cached.
- Follow-up requests can only read from the cache if the content up to and including the breakpoint is **identical**.

In other words, a breakpoint is a "cut line": everything above it is a cacheable prefix; everything below it is fresh and reprocessed every time.

---

## Longhand Block Form is Required

The shorthand message form (a plain string) has no place to attach `cache_control`. You must use the **longhand block form**:

```python
# Shorthand — cannot cache
messages = [{"role": "user", "content": "Here is a long document..."}]

# Longhand — can cache
messages = [{
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": "Here is a long document...",
            "cache_control": {"type": "ephemeral"},
        }
    ],
}]
```

The `cache_control` field is set to `{"type": "ephemeral"}`. "Ephemeral" is the currently supported cache type and maps to the 1-hour TTL from lesson 56.

---

## Byte-Exact Matching

The cache is extremely sensitive. The content up to and including the breakpoint must be **identical** in follow-up requests for the cache to be reused.

Even small changes invalidate the cache:

- Adding the word "please" → cache miss.
- Changing one whitespace character → cache miss.
- Reordering two sentences → cache miss.

If the prefix changes, Claude has to reprocess everything from the point of divergence, and you pay to re-create the cache entry.

**Design implication:** put stable content first, variable content last. The user's specific question belongs *after* the breakpoint, not in the cached prefix.

---

## Cross-Message Caching

Cache breakpoints can span across multiple messages and message types. If you place a breakpoint in a later message, **all previous messages** (user, assistant, etc.) are included in the cached content.

This is especially useful for conversational agents: you can cache the entire rolling history up to a stable point, then keep appending new turns after it.

---

## Cacheable Block Types

You are not limited to text blocks. Cache breakpoints can be added to:

- System prompts
- Tool definitions
- Image blocks
- Tool use blocks
- Tool result blocks

System prompts and tool definitions are the **best** candidates because they rarely change between requests. They are often where you get the biggest win from caching.

---

## Cache Ordering: Tools → System → Messages

Behind the scenes, Claude processes request components in a fixed order:

1. **Tools** (if provided)
2. **System prompt** (if provided)
3. **Messages**

This order dictates what is cached when. If your first breakpoint lives in the messages section, Claude still treats the tools and system prompt as part of the cached prefix because they come first.

You can place up to **four cache breakpoints total** in a single request. A common production layout is:

- Breakpoint 1 → end of tools (cache all tool schemas)
- Breakpoint 2 → end of system prompt (cache the system prompt)
- Breakpoint 3 → partway through message history (cache the stable conversation prefix)
- Breakpoint 4 → reserved for finer-grained caching if needed

Granular breakpoints let different parts of your request cache independently, so when one section changes you only lose the cache for that section — not for everything.

---

## Minimum Content Length: 1024 Tokens

There is a floor: **content must be at least 1024 tokens** (cumulative across everything before and including the breakpoint) to be cached.

- A short "Hi there!" message will not cross the threshold.
- You need genuinely large content — a long system prompt, a full document, or a verbose tool schema — to trigger caching.
- The 1024-token total is the **sum** of all the blocks being cached, not any single block.

If you are below the threshold, the cache_control field is a no-op: no cache is created, and no savings are realized.

---

## Common Mistakes

1. **Using the shorthand string form** — with no place to attach `cache_control`, nothing gets cached. Convert to the longhand block form first.
2. **Placing variable content before the breakpoint** — the user's fresh question should never live inside the cached prefix; it guarantees a miss on every call.
3. **Under-threshold caching** — trying to cache prompts smaller than 1024 tokens and expecting savings. It silently does nothing.
4. **Exceeding four breakpoints** — the request will be rejected. Plan the layout around the four-breakpoint budget.
5. **Not knowing the processing order** — placing a breakpoint on messages but mentally assuming the tools section is *not* cached. It is — tools and system prompt come before messages in the processing order and are always part of a message-level prefix.
6. **Relying on fuzzy matching** — caching is byte-exact. Normalize whitespace, punctuation, and ordering before you consider a prefix stable.

---

> **Key Insight**
>
> The four rules that define cache success: (1) opt in explicitly with a breakpoint, (2) match byte-for-byte, (3) hit the 1024-token floor, (4) respect the tools → system → messages ordering and the 4-breakpoint cap. Miss any one and the cache silently does nothing — or worse, you pay cache-write fees on content that never gets reused.

---

## CCA Exam Relevance

- **D5 (Enterprise Deployment)** — expect questions that test whether you know caching is manual, byte-exact, and floored at 1024 tokens.
- **D2 (Tool Design)** — tool definitions are a prime caching target because they are stable across requests; exam questions may ask where to put a breakpoint in a tool-heavy workflow.
- Remember the processing order: tools, then system prompt, then messages. This order maps directly to "what should I cache first?"
- Four breakpoints total, `{"type": "ephemeral"}`, 1024-token floor — these are frequently tested numbers.

---

## Flashcards

| Front | Back |
|-------|------|
| Is prompt caching automatic? | No — you must manually add a `cache_control` field to a block in your request (a cache breakpoint). |
| What value goes in `cache_control`? | `{"type": "ephemeral"}` — this is the currently supported cache type and maps to the 1-hour TTL. |
| Which message form supports cache breakpoints? | The longhand block form (`content` is a list of blocks). The shorthand string form cannot carry `cache_control`. |
| How much content does Claude cache when you place a breakpoint? | Everything before and including the breakpoint. |
| Does the cached content need to match exactly on follow-up calls? | Yes — byte-exact. Even adding "please" invalidates the cache. |
| What is the minimum token count for a cacheable prefix? | 1024 tokens (the sum of all blocks before and including the breakpoint). |
| How many cache breakpoints can you place in a single request? | Up to four. |
| In what order does Claude process request components for caching purposes? | Tools first, then system prompt, then messages. |
| What are the best candidates for caching and why? | System prompts and tool definitions — they rarely change between requests and often account for the largest stable input. |
| Can a breakpoint in a later message cache earlier messages too? | Yes — cross-message caching includes all previous messages (user, assistant, etc.) up to the breakpoint. |
