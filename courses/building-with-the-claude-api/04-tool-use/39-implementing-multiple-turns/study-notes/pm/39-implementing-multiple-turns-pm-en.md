# Implementing Multiple Turns — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) / D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 1.2 (agentic loop implementation), 2.4 (multi-turn tool loops), 1.3 (multi-turn conversation management) |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 39 |

---

## One-Liner

The agentic loop is the 15-line engine that turns Claude from a chatbot into an agent — and once your team can ship it reliably, every agent-like product you dream up becomes feasible.

---

## Mental Model: The Barista and the Order Slip

Picture a coffee shop barista working from an order slip:

| Step | Coffee Shop | Agentic Loop |
|------|-------------|-------------|
| Read the order slip | User asks question | Call Claude with messages |
| "Do I need anything special?" | "Does Claude want a tool?" | Check `stop_reason` |
| Yes: grind beans, steam milk, etc. | Yes: run tools | Execute tool-use blocks |
| Hand step results back to barista | Add tool results to history | Loop back to Claude |
| No: plate the drink, done | No: return final text | Break the loop |

The barista keeps asking themselves "is there another step?" until the drink is ready. That is exactly what the loop does — it keeps asking Claude "do you need another action?" until Claude says "no, I'm done."

---

## Why This Unlocks Real Product Value

Without the loop, you can ship "Claude answers questions." With the loop, you can ship:

| Product | What It Does |
|---------|-------------|
| Coding assistant | Reads files, runs tests, writes patches, iterates |
| Travel planner | Checks flights, filters by price, books, confirms |
| Customer support agent | Reads ticket, queries CRM, checks knowledge base, drafts reply |
| Data analyst | Runs SQL, interprets results, generates charts, writes summary |

The loop is why "agent" is a category and not just a buzzword. Every real-world Claude agent — from Claude Code to MCP clients — is a variation of this 15-line pattern plus production hardening.

---

## Product Use Cases: When to Invest

### When The Loop Pays Off

| Signal | Product Implication |
|--------|---------------------|
| Users want "fire and forget" workflows | The loop lets Claude finish multi-step tasks autonomously |
| The answer depends on external data | Tool calls fetch the data, loop iterates until complete |
| Users accept latency in exchange for quality | Multi-turn loops trade speed for correctness |
| Features benefit from iterative refinement | Loop can retry, filter, compare, converge |

### When The Loop Is Overkill

| Signal | Simpler Alternative |
|--------|---------------------|
| Single lookup with immediate answer | One tool call, no loop |
| Pure Q&A on static knowledge | No tools at all |
| Real-time conversational UI | Streaming without the loop complexity |

---

## PM Decision Framework

Before scoping an agentic-loop feature, ask:

| Question | Why It Matters |
|----------|---------------|
| What is the iteration cap? | Unbounded loops can hang for minutes and burn tokens |
| How do we show progress between iterations? | Users need to see each step or they assume failure |
| Can the user cancel mid-loop? | Multi-step agents must be interruptible |
| What happens if the loop hits the cap with no final answer? | "Partial result" UX must be designed |
| How do we budget tokens per conversation? | Each iteration grows history; plan for the worst case |
| How do we audit what tools ran? | Essential for debugging and compliance |
| What is the retry policy for tool failures? | Let Claude handle it, or hard-retry at the app layer? |

---

## Common PM Mistakes

1. **Treating the loop as a tech detail** — it is a product feature surface with UX decisions at every turn (progress, cancel, partial results)
2. **Not setting a visible iteration cap** — runaway loops waste budget and hang users; caps must be tuned and documented
3. **Hiding tool errors from Claude** — if the tool failed, Claude needs to know via `is_error=True` so it can recover; hiding causes hallucinations
4. **No observability story** — production debugging of agent loops requires logging every iteration's tool calls and results
5. **Shipping before parallelizing** — tools that could run in parallel should not be serialized; doing so doubles or triples latency

---

## Cost and Latency Planning

Every extra loop iteration adds:

| Cost | Typical Magnitude |
|------|------------------|
| One API round trip | +300ms to +1s |
| Growing conversation history | +10% to +30% input tokens per iteration |
| Tool execution time | Depends on the tool (milliseconds to seconds) |
| Output tokens | +few hundred per turn |

A 5-iteration loop can easily cost 5x the input tokens of a single call, and take 3-10 seconds of wall time. Prompt caching (covered later) is the standard mitigation for the token cost, but the latency cost is fundamental to the pattern.

---

> **Key Insight**
>
> The agentic loop is the smallest unit that separates "Claude features" from "Claude agents." Fifteen lines of code unlock a new product category. But every line of that loop corresponds to a product decision: how long do we iterate, how do we show progress, how do we handle failures, how do we cap cost. PMs who treat the loop as "just backend" ship broken agents; PMs who treat it as "a product surface with five knobs" ship great ones.

---

## CCA Exam Relevance

- **D1 (Agentic Architecture)**: The agentic loop is the canonical agent pattern. Expect scenario questions on `stop_reason` handling and iteration control.
- **D2 (Tool Design & MCP Integration)**: Understand error propagation via `is_error=True` and why hiding errors breaks Claude's recovery behavior.
- Watch for exam questions that describe "Claude making multiple tool calls in sequence" — the answer is always a loop with stop_reason checking.

---

## Flashcards

| Front | Back |
|-------|------|
| What analogy captures the agentic loop? | A barista working from an order slip — keeps asking "is there another step?" until the drink is done |
| What single line of code signals the loop to exit? | `if response.stop_reason != "tool_use": break` |
| Why is the agentic loop a product surface, not just engineering? | Every iteration involves PM decisions: progress UX, cancellation, cost, retries, partial results |
| What is the biggest hidden cost of an agentic loop feature? | Growing conversation history — each iteration adds tokens to every subsequent call |
| What must a production agent loop include for safety? | A max-iterations cap, observability per iteration, and error propagation via `is_error=True` |
| Why hide errors from Claude backfire? | Claude cannot recover if it thinks the tool succeeded — it will hallucinate a result |
| What products become possible only with the agentic loop? | Coding assistants, travel planners, support agents, data analysts — anything requiring multi-step reasoning |
| What latency budget should PMs expect for a 5-iteration agentic loop? | 3 to 10 seconds of wall time plus token costs scaled by iteration depth |
