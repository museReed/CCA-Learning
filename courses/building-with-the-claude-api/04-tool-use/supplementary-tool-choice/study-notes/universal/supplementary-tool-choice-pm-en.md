# Tool Choice Parameter — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.1 (tool schema design), 2.2 (content blocks), 1.2 (agentic loop control) |
| Source | Supplementary — fills curriculum gap in building-with-the-claude-api / 04-tool-use |

---

## One-Liner

`tool_choice` is the product lever that decides how much freedom Claude gets to pick its next action — use it to trade conversational flexibility for workflow reliability.

---

## Mental Model — Ordering at a Restaurant

Think of `tool_choice` as how you order food at a restaurant:

| Mode | Restaurant Analogy | Product Meaning |
|------|-------------------|-----------------|
| `auto` | "Surprise me — maybe chat, maybe food" | Claude decides whether this turn needs a tool or just a friendly reply |
| `any` | "I must order from your menu — you pick which dish" | Every turn must produce a tool call; Claude chooses which |
| `tool` | "I want the lasagna, specifically" | Force a specific tool — guaranteed structured output |
| `none` | "Just tell me what's good today — no ordering" | Claude replies with text only; tools are off for this turn |

The tension: `auto` is the most natural user experience, but the least predictable. `tool` is the most predictable, but kills the conversation feel. Your product needs both, at different moments.

---

## Product Use Cases

### When to use `auto` — Conversational Agents

- Customer support chatbots that sometimes need to look up an order and sometimes just need to chat.
- Coding assistants that answer general questions directly and only call tools when the user asks for file operations.
- **Why**: users expect natural conversation. Forcing a tool call on "thanks!" feels broken.

### When to use `any` — Action-Oriented Workflows

- Agentic task runners ("book me a flight, then a hotel, then a car") where every turn must advance the plan.
- Back-office automation where human chat is out of scope — every Claude turn should be an API call.
- **Why**: removes the risk that Claude stops mid-workflow to "explain" instead of acting.

### When to use `tool` — Structured Data Extraction

- Resume parsing, invoice OCR, form-fill from unstructured emails, classification into a taxonomy.
- Anywhere you previously would have used "JSON mode" or a strict output schema.
- **Why**: the tool's `input_schema` becomes a typed output contract. No prompt brittleness, no "please respond in JSON" hack.

### When to use `none` — Summary & Reflection Turns

- After a multi-step agent has gathered all the data it needs, use `none` for the final user-facing message to prevent Claude from triggering yet another tool call.
- In evaluation harnesses where you want Claude to grade a response without calling anything.
- **Why**: gives your agent a clean "stop and talk" signal.

---

## PM Decision Framework

Ask these four questions in order:

1. **Does this turn ever need to be pure conversation?**
   - Yes → start with `auto`.
   - No → continue.
2. **Does this turn need to produce exactly one named output shape?**
   - Yes → `tool` with that tool's name.
   - No → continue.
3. **Does this turn need to pick from a menu of actions, but definitely take one?**
   - Yes → `any`.
   - No → continue.
4. **Is this a reflection, summary, or final user-facing reply turn?**
   - Yes → `none`.

In agent products, different turns in the same loop will use different modes. A common pattern: start with `auto`, switch to `any` when entering an execution phase, switch to `none` for the final summary.

---

## Common PM Mistakes

1. **Forcing `any` when users expect conversation** — your chatbot starts replying to "hello" with a weird tool call. Users think the product is broken.
2. **Forgetting that `tool` and `any` kill reasoning transparency** — when Claude is forced, it does not "think out loud" before acting. You lose the explainability that the `auto` mode gives you for free. This matters for regulated industries (finance, healthcare) where audit trails need to show *why* an action was taken.
3. **Using `auto` for structured data extraction** — Claude might reply with chatty text ("Sure! Here's the data you asked for...") instead of a clean tool call, breaking your downstream parser. Use `tool` instead.
4. **Treating `tool_choice` as a global setting** — it is per API call. Smart agent products switch modes turn-by-turn based on what phase the agent is in.
5. **Not setting `disable_parallel_tool_use` when your backend can't handle parallel actions** — Claude may fire two tool calls at once and your single-threaded executor will misbehave. If your backend is not parallel-safe, enforce serial execution explicitly.

---

> **Key Insight**
>
> `tool_choice` is the dial between **user delight** and **product reliability**. `auto` maximizes delight (natural conversation, transparent reasoning) but sacrifices guarantees. `any` and `tool` maximize reliability (guaranteed structured action) but sacrifice conversational feel and reasoning transparency. The best agent products do not pick one — they switch modes *within a single user session*, using `auto` for chat, `any` for execution, and `none` for summaries.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: PM-style questions may ask "which setting should you choose to guarantee the model returns structured data?" — the answer is `{"type": "tool", "name": "..."}`.
- **D1 (Agentic Architecture)**: expect scenario questions about agent loops where the right answer is switching `tool_choice` between turns.
- **Trap to watch for**: the exam may describe a chat assistant that "sometimes needs to look up data". The correct answer is `auto`, not `any`.

---

## Flashcards

| Front | Back |
|-------|------|
| Which `tool_choice` mode feels most like a normal conversation? | `auto` — Claude decides whether to chat or call a tool, so small talk still works naturally. |
| Which mode should you pick if every turn in your workflow must produce a structured action? | `any` — Claude must call one of the provided tools, but picks which. |
| Which mode is the best fit for structured data extraction (the "JSON mode" use case)? | `tool` with a specific name — the tool's schema is the typed output contract. |
| What does `none` do, and when is it useful? | Disables tools for this turn; useful for summary/reflection turns at the end of an agent loop. |
| What reasoning behavior do you lose when you use `any` or `tool`? | Chain-of-thought text before the tool call — Claude emits the tool_use block directly, so you lose explainability. |
| Why is `any` a bad default for a customer-support chatbot? | It forces a tool call on every turn, so "hello" or "thanks" will trigger nonsensical tool calls. |
| When would a well-designed agent product switch `tool_choice` mid-session? | Use `auto` for chat, `any` for execution phases, and `none` for final summaries — different phases, different modes. |
| What product risk does `disable_parallel_tool_use` mitigate? | Prevents Claude from firing multiple simultaneous actions when your backend cannot safely execute tools in parallel. |
| Your legal team needs to audit *why* Claude took an action. Which mode preserves reasoning? | `auto` — only `auto` lets Claude emit natural chain-of-thought text before the tool call. |
| Does `tool_choice: none` mean you should omit `tools=` from the request? | No — still declare the tools; `none` only disables calling them on this specific turn. |
