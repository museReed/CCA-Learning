# Project Overview: Reminder App — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.1 (tool schema design), 1.2 (agentic loop foundation), 1.1 (feature decomposition) |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 33 |

---

## One-Liner

A three-word user request ("remind me Thursday") hides three distinct product capability gaps — and the correct AI product architecture is to build one tool per gap, not one giant "magic" function.

---

## The Deceptive Simplicity of "Remind Me"

The PRD line reads:

> *As a user, I can say "remind me of X a week from Thursday" and the assistant will set the reminder.*

Every stakeholder nods. Two-sentence story. Must be a two-day ticket, right?

No. Underneath, the base model cannot:

1. Know the exact current time (just the rough date)
2. Reliably do date arithmetic (LLMs mis-count weekdays surprisingly often)
3. Persist a reminder anywhere

Each bullet is a different problem. Each needs its own component. This is the single most common trap when PMs scope AI features: the surface is a one-liner, the underlying capability graph is a tree.

---

## Mental Model: The LEGO Set vs. the Action Figure

| Approach | Analogy | Shipping velocity | Long-term leverage |
|----------|---------|-------------------|--------------------|
| One big "do the whole thing" function | Action figure — molded for one pose | Fast for v1 | Zero reuse, hard to fix |
| Small atomic tools, composed by Claude | LEGO set — snap-together pieces | Slightly slower v1 | Any future feature reuses the bricks |

Tool use rewards the LEGO approach. The first time you build `add_duration_to_datetime`, you pay the cost. Every future feature that touches "remind me in N days", "set deadline for N weeks", "rebook for next quarter" gets to reuse the same brick — for free.

---

## The Three Gaps → Three Tools

| User Signal | Gap It Exposes | Tool to Build |
|-------------|----------------|---------------|
| "right now" | Claude does not know precise time | Get current datetime |
| "a week from Thursday" | Claude cannot do date math reliably | Add duration to datetime |
| "remind me" | Claude has no reminder system | Set reminder |

Each row is a decision point in the PRD. Each tool has its own acceptance criteria, its own failure modes, its own telemetry needs.

---

## Why This Matters for Roadmap Planning

Because the tools are reusable, scoping the reminder feature **simultaneously scopes** a half-dozen future features:

- Birthday reminders (reuses all three tools)
- Deadline tracking (reuses two of three)
- Recurring meetings (reuses two of three)
- Vacation countdowns (reuses two of three)
- "What day is it in N weeks" answers (reuses two of three)

A PM who recognizes this pattern can sell the feature to stakeholders as "we are building the foundation for the scheduling stack", not "we are building a toy reminder app." The ROI calculation flips completely.

---

## Build Order as a Risk-Management Tool

The course builds the tools simplest-first:

1. Read-only first (get current datetime) — lowest blast radius if it breaks.
2. Pure-function second (add duration) — deterministic, unit-testable.
3. Write operation last (set reminder) — real-world side effects, real-world risk.

For a PM, this is also the dogfood order. Ship the first tool internally, then the second, and only ship the write tool once both dependencies are stable. Each phase is releaseable.

---

## PM Decision Framework

When a user story looks "simple", ask:

| Question | If Yes | Action |
|----------|--------|--------|
| Does the request need the current moment's data? | Yes | Plan a tool for it. |
| Does the request need math the LLM is bad at (dates, money, distance)? | Yes | Plan a tool for it. |
| Does the request need to persist state anywhere? | Yes | Plan a tool for it. |
| Can any of these be reused in other features? | Yes | Upgrade the priority — it is foundational. |
| Does stakeholder think "this is simple, it's just one call"? | Yes | Run this gap analysis with them. |

---

## Common PM Mistakes

1. **Misreading the scope** — "remind me" sounds like a two-day ticket but is actually three tools and an agent loop. Budget accordingly.
2. **Bundling under pressure** — stakeholders will ask for "just one function that does it all". Resist. The long-term cost is far worse.
3. **Not marketing the reuse value** — if you don't sell the foundational work, it looks like over-engineering a trivial feature.
4. **Skipping the toy project** — building this pattern on a real, high-stakes feature means the learning curve happens in production.
5. **No loading state for multi-turn loops** — three tool calls plus three API calls means several seconds of latency. Design for it.

> **Key Insight**
>
> The reminder app is the clearest illustration of the "iceberg" problem in AI product management: a trivial-sounding user story sits on top of multiple distinct capability gaps. The correct response is to map one tool to each gap, because each tool you build becomes a reusable asset for future features. In the CCA exam, this shows up as questions asking how to decompose a natural-language feature into tools.

---

## CCA Exam Relevance

- **D1 (Agentic Architecture)**: recognize that one user turn may trigger many tool calls — Claude plans the sequence.
- **D2 (Tool Design & MCP Integration)**: the "one gap per tool" design rule is tested explicitly.
- Exam pattern: given a feature like "remind me / summarize my day / book the meeting", identify the minimum set of tools required.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the iceberg trap in AI product scoping? | A one-line user story (like "remind me Thursday") hides multiple distinct capability gaps; correct scoping requires mapping one tool to each gap. |
| Why is the reminder app a good first project? | It shows a realistic multi-tool composition with escalating risk (read-only → pure-function → write) inside a user-friendly story. |
| What is the LEGO-vs-action-figure analogy? | Atomic tools are LEGO bricks (reusable across features); monolithic functions are action figures (one use, zero reuse). |
| What future features reuse tools built for the reminder app? | Birthday reminders, deadline tracking, recurring meetings, vacation countdowns, "what day is it" answers. |
| What is the recommended build order for tools in this project? | Read-only first, pure function second, write/side-effect last — a risk gradient. |
| What is the first PM mistake when scoping "remind me"-style features? | Mis-sizing it — assuming it is a simple ticket instead of three tools plus a multi-turn loop. |
| Why budget loading state for this feature? | Multiple tool calls and API round trips easily reach several seconds of latency. |
| How do you sell foundational tool work to stakeholders? | Frame it as enabling a whole family of future features, not as a toy reminder app. |
