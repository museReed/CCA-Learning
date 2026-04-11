# Prompt Caching in Action — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D5 — Enterprise Deployment (20%) — primary; D2 — Tool Design (18%) — secondary |
| Task Statements | 5.1 (cost/latency optimization), 5.2 (production performance), 2.1 (tool schema design) |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 58 |

---

## One-Liner

Prompt caching in practice means converting your tools list and system prompt into cacheable longhand blocks with `cache_control`, then watching the `cache_creation_input_tokens` / `cache_read_input_tokens` usage fields to verify cache hits and misses.

---

## Where Caching Pays Off in Real Apps

The lesson highlights three high-value targets:

- **Large system prompts** — e.g., a ~6K-token coding assistant system prompt.
- **Complex tool schemas** — e.g., ~1.7K tokens for multiple tool definitions.
- **Repeated message content** — conversations or workflows that keep sending the same prefix.

The rule of thumb: caching only helps if you are repeatedly sending identical content — and in many real applications, this happens **extremely frequently**.

---

## Setting Up Tool Schema Caching

To cache tool schemas, add `cache_control` to **the last tool in the list**. Everything before and including that tool gets cached.

```python
if tools:
    tools_clone = tools.copy()
    last_tool = tools_clone[-1].copy()
    last_tool["cache_control"] = {"type": "ephemeral"}
    tools_clone[-1] = last_tool
    params["tools"] = tools_clone
```

Why the copy-then-mutate dance:

- `tools.copy()` creates a shallow copy of the tools list so the caller's list is not mutated.
- `tools_clone[-1].copy()` creates a shallow copy of the last tool dict so its original version stays clean.
- Only the copy gets the `cache_control` field.

You *could* write `tools[-1]["cache_control"] = ...` directly, but the copying approach prevents subtle bugs if you later reorder tools, reuse the list across calls, or share tool definitions between parts of the app.

The `cache_control` field is set to `{"type": "ephemeral"}` — the standard 1-hour cache type.

---

## Setting Up System Prompt Caching

For the system prompt, you need to convert it from a plain string into the longhand structured block form so you have somewhere to attach `cache_control`:

```python
if system:
    params["system"] = [
        {
            "type": "text",
            "text": system,
            "cache_control": {"type": "ephemeral"},
        }
    ]
```

The string-form system prompt has no field for `cache_control`; the block-form does. Once the system prompt is structured this way, the entire system prompt becomes part of the cached prefix.

---

## Understanding Cache Behavior in the Response

When you run requests with caching enabled, the API's `usage` block exposes new token counters that tell you whether you wrote to or read from the cache:

| Field | Meaning |
|-------|---------|
| `cache_creation_input_tokens` | Tokens Claude **wrote** into the cache on this request (first call or cache miss forcing a rewrite). |
| `cache_read_input_tokens` | Tokens Claude **read** from the cache on this request (cache hit — the savings event). |

Typical usage patterns:

- **First request**: `cache_creation_input_tokens=1772`, `cache_read_input_tokens=0` — Claude is writing to the cache.
- **Follow-up request, same content**: `cache_creation_input_tokens=0`, `cache_read_input_tokens=1772` — Claude is reading from the cache.
- **Changed content**: new `cache_creation_input_tokens` appear for the changed section, because it was not in the cache yet.

The cache is **extremely sensitive**: changing even a single character in your tools or system prompt invalidates the entire cache for that component.

---

## Cache Ordering and Partial Hits

You can set multiple cache breakpoints in a single request. The order Claude processes them is fixed:

1. **Tools** (if provided)
2. **System prompt** (if provided)
3. **Messages**

This ordering enables **partial cache hits**. Suppose you change the system prompt but leave the tools unchanged:

- The tools section is still byte-identical → **cache read** for tools.
- The system prompt differs → **cache write** for the new system prompt.
- The message section is processed normally.

You only pay for the parts that actually changed. This granular caching is one of the biggest wins of the feature: it degrades gracefully instead of all-or-nothing.

---

## Practical Considerations

Prompt caching is most effective when you have:

- **Consistent tool schemas across requests** — a production agent with a stable toolbox.
- **Stable system prompts** — locked personas, locked instructions.
- **Applications that make multiple requests with similar context** — chat, iterative workflows, batch evaluations.

Remember: the cache only lasts for one hour. This is designed for applications with **relatively frequent API usage**, not long-term storage. If your product makes a call every few hours, the cache will expire between calls and you will pay the cache-write fee repeatedly with no read benefit.

---

## Common Mistakes

1. **Mutating the caller's tool list in place** — writing `tools[-1]["cache_control"] = ...` directly can silently affect other parts of the app that share the same list. Use the copy-then-assign pattern.
2. **Leaving the system prompt as a plain string** — a string cannot carry `cache_control`. You must wrap it in a `{"type": "text", "text": ..., "cache_control": ...}` block.
3. **Assuming the whole request is one cache unit** — it is not. Tools, system prompt, and messages cache independently in processing order, so you can get partial hits.
4. **Forgetting to check `usage` fields in production** — without monitoring `cache_creation_input_tokens` vs. `cache_read_input_tokens`, you cannot tell whether the cache is actually being used.
5. **Making trivial edits to cached sections** — a single whitespace or punctuation change to a tool description or system prompt forces a cache rewrite. Treat cached sections as versioned, immutable assets.
6. **Caching for low-frequency workloads** — entries expire before they are reused, so you only pay the write penalty with no read savings.

---

> **Key Insight**
>
> Real-world caching is about three things: (1) wrap the last tool in `cache_control` to cache the full tool schema, (2) convert the system prompt to longhand block form so it can carry `cache_control`, and (3) inspect `cache_creation_input_tokens` / `cache_read_input_tokens` in the response to verify that cache hits are actually happening. The processing order (tools → system → messages) gives you partial hits for free.

---

## CCA Exam Relevance

- **D5 (Enterprise Deployment)** — expect questions about which API fields prove a cache hit (`cache_read_input_tokens`) vs. a cache write (`cache_creation_input_tokens`).
- **D2 (Tool Design)** — know that the `cache_control` field goes on the **last** tool in the list, which caches *all* tools before it thanks to the processing order.
- Know the partial-hit behavior: changing only the system prompt preserves the cache on tools and produces a split usage pattern (read for tools, create for system).
- The phrase "extremely sensitive" about byte-exact matching is an exam-style warning — any edit invalidates.

---

## Flashcards

| Front | Back |
|-------|------|
| Which API response field tells you the cache was written on this request? | `cache_creation_input_tokens` — the number of tokens Claude just wrote into the cache. |
| Which API response field tells you the cache was read on this request? | `cache_read_input_tokens` — the number of tokens Claude reused from the cache. |
| Where do you add `cache_control` to cache an entire tools list? | On the **last** tool in the list. Everything before and including it becomes part of the cached prefix because tools are processed first. |
| Why copy the tools list and the last tool before adding `cache_control`? | To avoid mutating the caller's original list or the original tool dict, which prevents bugs if tools are reordered or shared elsewhere. |
| How do you make a system prompt cacheable? | Convert it from a plain string to the longhand block form `[{"type": "text", "text": ..., "cache_control": {"type": "ephemeral"}}]`. |
| What is the value of `cache_control` you use for 1-hour caching? | `{"type": "ephemeral"}` |
| In what order are tools, system prompt, and messages processed for caching? | Tools first, then system prompt, then messages. |
| What happens to the cache when you change only the system prompt? | You get a partial hit: cache read on tools (unchanged) and cache write on the new system prompt. |
| What does "extremely sensitive" mean in the context of caching? | Any change — even a single character — to the cached section invalidates the cache and forces a rewrite. |
| Why is caching a bad fit for long-term, low-frequency workloads? | Because the cache only lives for one hour, so entries expire between calls and you pay cache-write without ever getting a cache read. |
