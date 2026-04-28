# Using Multiple Tools — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%), D1 — Agentic Architecture (22%) |
| Task Statements | 2.1 (tool schema & selection), 1.2 (tool orchestration) |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 40 |

---

## One-Liner

Giving Claude multiple tools is like hiring a generalist and then handing them a belt full of specialized instruments — each new capability you add is instantly composable with everything already there, with no rewrite of the core product.

---

## Mental Model: The Swiss Army Knife

A single-tool agent is a screwdriver. A multi-tool agent is a Swiss Army knife. The interesting product behavior emerges from **combinations**:

| Component | Alone | Combined With Others |
|-----------|-------|---------------------|
| Calendar lookup | "What's on my calendar today?" | "Move my 3pm to after my 4pm ends" |
| Date math | "What date is 30 days from now?" | "Schedule a follow-up 2 weeks after the contract signing" |
| Reminder | "Remind me Friday" | "Remind me 3 days before my passport expires" |

Your users rarely ask for a single-tool action. Real requests compose — so your tool catalog must compose too.

---

## Product Use Cases

### When to Add More Tools

| Scenario | Why Multiple Tools Matter |
|----------|--------------------------|
| Scheduling assistant | Needs date math + calendar + reminders + notifications working together |
| Research copilot | Needs web search + document retrieval + summarization + citation |
| Customer support agent | Needs ticket lookup + knowledge base search + escalation |
| DevOps assistant | Needs log search + metric query + runbook retrieval + incident create |

### When to Resist Adding More

| Anti-Pattern | Better Approach |
|--------------|-----------------|
| Adding a tool "just in case" someone might need it | Wait for a concrete user request; prune unused tools |
| Exposing 20+ narrow tools Claude must choose between | Consolidate into fewer, richer tools with parameters |
| Duplicating tools with similar behavior | One canonical tool per capability |

The cost of an extra tool is not zero: more tools means more tokens in every request, more chances for Claude to choose the wrong one, and more maintenance.

---

## PM Decision Framework

When planning tool catalog growth, ask:

| Question | If Yes | Action |
|----------|--------|--------|
| Does any real user request require chaining tools? | Yes | Add the missing capability |
| Do two existing tools have overlapping descriptions? | Yes | Merge or clarify |
| Is the new tool independently valuable? | Yes | Ship it |
| Does adding this tool push the total above ~15-20? | Yes | Consider grouping under an MCP server instead |
| Can the request be satisfied by refining an existing tool's description? | Yes | Update description first |

---

## The Composition Principle

Product value compounds when tools can be chained:

- **1 tool** → Value = N
- **3 tools** → Value ≈ 3N + chain-combinations
- **10 tools** → Value grows with the number of useful compositions, not the raw count

This is why Slack, Zapier, and IFTTT thrive — the platform becomes valuable once enough primitives exist to compose meaningful workflows. Your AI product follows the same S-curve: slow at first, then a sharp inflection when composition becomes possible.

---

## How Claude Picks Tools (And What PMs Can Do About It)

Claude reads the **description** of each tool and picks the best match. PMs can improve accuracy by:

1. **Writing imperative, action-first descriptions** — "Creates a reminder at a specific datetime" beats "Reminder utility"
2. **Including constraints** — "Use only for dates in the future" prevents misuse
3. **Avoiding overlap** — if two tools can do similar things, Claude will randomly pick one; merge them
4. **Testing with real user phrasings** — look at real user transcripts and verify the right tool fires

The description is a product surface. Treat it with the same rigor as button labels or empty states.

---

## Common PM Mistakes

1. **Treating tool descriptions as throwaway docstrings** — they are the main signal Claude uses; invest in them like UX copy.
2. **Launching a broad tool catalog on day one** — start with 2-3 tools, observe usage, add more based on real requests.
3. **Not tracking which tools Claude actually picks** — you cannot optimize what you do not measure; log tool selection events.
4. **Ignoring parallel vs. sequential costs** — parallel tool calls are one API round-trip, sequential chains are many; latency compounds.
5. **Assuming more tools = more capability** — capability grows with *useful compositions*, not with catalog size.

> **Key Insight**
>
> A multi-tool agent's product value comes from **composition**, not from the raw tool count. Each new tool should earn its place by unlocking chain-workflows that previous tools could not accomplish. For the CCA exam, the core concept is: tool selection is model-controlled and driven by description quality, not by any explicit ordering in the tools list.

---

## CCA Exam Relevance

- **D2 (Tool Design)**: Know that Claude picks tools based on the schema name + description. Well-written descriptions are the primary lever for accuracy.
- **D1 (Agentic Architecture)**: Understand parallel vs. sequential tool execution and the shared agentic loop.
- Scenario questions often present an agent with 3-5 tools and ask which one Claude will call for a given user request — the answer is driven by description match.

---

## Flashcards

| Front | Back |
|-------|------|
| What makes multi-tool agents more valuable than single-tool ones? | Composition — value grows with the number of useful chain-workflows, not the raw tool count |
| How does Claude decide which tool to call? | By matching the user request against each tool's name and description |
| What is the main PM lever for tool selection accuracy? | Writing imperative, action-first tool descriptions; avoiding overlap between tools |
| Why should PMs resist adding tools "just in case"? | Extra tools cost tokens, increase selection errors, and add maintenance; add only when a real request demands it |
| What is the risk of exposing 20+ narrow tools? | Claude has to choose between more options, selection accuracy drops, and token cost rises |
| When are parallel tool calls cheaper than sequential? | When the tools are independent — parallel is one round-trip, sequential is many |
| What signal should PMs track to improve tool catalogs? | Which tools Claude actually picks for which user phrasings, so descriptions can be tuned |
| What is the core product mental model for multi-tool agents? | A Swiss Army knife — individual tools matter less than the combinations they enable |
