# Project Overview: Reminder App — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.1 (tool schema design), 1.2 (agentic loop foundation), 1.1 (breaking features into tool compositions) |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 33 |

---

## One-Liner

The reminder-app project demonstrates a core design principle of tool use: decompose capability gaps into small, single-purpose tools and let Claude compose them at reasoning time — rather than building one monolithic "do everything" function.

---

## The Target User Experience

```
User:  "Set a reminder for my doctor's appointment.
        It's a week from Thursday."

Claude: "OK, I will remind you."
```

Trivially simple on the surface — but hiding three distinct capability gaps that a base model cannot solve.

---

## Three Gaps Between Claude and the Goal

| Gap | Why It Matters | Tool That Fixes It |
|-----|---------------|---------------------|
| **Limited time awareness** | Claude may know the current date roughly but not the exact time at the moment of the call | `get_current_datetime` |
| **Date arithmetic is error-prone** | "A week from Thursday" requires adding durations to dates; LLMs regularly miscount weekdays and mis-handle month boundaries | `add_duration_to_datetime` |
| **No reminder capability** | Claude has no native way to persist a scheduled reminder in any system | `set_reminder` |

Each gap is addressed by exactly one tool. This is not accidental — it is the design principle.

---

## Design Principle: One Tool per Capability Gap

```
┌────────────────────────────────────────┐
│          User Goal: set reminder        │
└────────────────────────────────────────┘
             │
   decompose into atomic steps
             │
 ┌───────────┼────────────┐
 ▼           ▼            ▼
get_current_  add_duration_  set_reminder
datetime      to_datetime
(now)         (now + 1 week) (persist)
```

Why atomic tools beat a monolithic "parse_and_set_reminder":

1. **Composability** — Claude can reuse `add_duration_to_datetime` for other date-math tasks (birthdays, deadlines, renewals).
2. **Testability** — each tool has one job and is trivially unit-testable.
3. **Observability** — logs show exactly which step failed, not "the big function returned wrong thing".
4. **Model-side reasoning** — Claude's strength is planning sequences. If you pre-bake the sequence into one function, you waste that strength.
5. **Graceful degradation** — a failure in `set_reminder` doesn't lose the already-computed timestamp.

---

## The Agentic Loop Implicit in This Project

Even though each tool is simple, combining three tools means the conversation may need **three** tool-use turns before Claude emits the final answer:

```
Turn 1: user → "remind me next Thursday"
Turn 2: Claude → tool_use get_current_datetime
Turn 3: app   → tool_result "2026-04-11 14:30:00"
Turn 4: Claude → tool_use add_duration_to_datetime(now, +7 days)
Turn 5: app   → tool_result "2026-04-18 14:30:00"
Turn 6: Claude → tool_use set_reminder(when="2026-04-18 14:30:00", ...)
Turn 7: app   → tool_result "ok, reminder created"
Turn 8: Claude → "OK, I will remind you."  (stop_reason=end_turn)
```

This is the minimal working example of an **agent loop**: Claude plans the sequence of tool calls itself, based on the user's natural language request. Your code does not hard-code the order — it simply runs whatever tool Claude asks for next, until `stop_reason != "tool_use"`.

---

## Incremental Build Order

The course builds these tools one at a time, simplest first. This mirrors best practice for any new tool-use project:

1. **Start with the read-only tool** (`get_current_datetime`) — no side effects, easiest to test.
2. **Add the pure-function tool** (`add_duration_to_datetime`) — deterministic, still no external side effects.
3. **Add the side-effecting tool last** (`set_reminder`) — persistence, failure modes, audit trails.

This order is also the safety gradient. Read-only tools are low-risk to misuse; write tools demand more validation and testing.

---

## What This Project Teaches About Scoping

The underlying lesson is about **scoping AI features**. A naive engineer might write:

```python
def handle_reminder_request(user_text: str) -> str:
    # parse the text, do everything, return a confirmation
    ...
```

...and then try to prompt Claude to call that one giant function. This fails because:

- You have moved all the hard work (parsing, date math, persistence) back into imperative code.
- Claude never gets to reason; it becomes a text-to-function-call classifier.
- You lose the ability to reuse those capabilities in any other feature.

The tool-use paradigm **inverts** that: give Claude small primitives and let it orchestrate. This is the bridge from "LLM as a smart string function" to "LLM as a planner."

---

## Common Mistakes

1. **Bundling multiple capabilities into one tool** — e.g., a single `schedule_reminder(natural_language_time)` that parses strings internally. Decompose it.
2. **Hard-coding the tool call order** — let Claude decide. Your code's job is to dispatch whatever tool it asks for.
3. **Starting with the write tool** — build read-only tools first; they are safer to iterate on.
4. **Skipping the project phase** — jumping straight into production code without a toy project means you learn the failure modes on real users.
5. **Not planning for multi-turn loops** — even a simple feature can require 3+ tool calls; your message loop must handle an arbitrary number of turns.

> **Key Insight**
>
> The reminder project is a case study in **capability decomposition**: each native limitation of the model becomes exactly one atomic tool, and Claude composes them at reasoning time. This inversion — "give the model primitives, let it plan" — is the mental shift the CCA exam tests repeatedly under D1 (agentic architecture). Recognize it whenever you see a multi-step natural language goal.

---

## CCA Exam Relevance

- **D1 (Agentic Architecture)**: understanding that a single user request can require a loop of multiple tool calls, all planned by the model.
- **D2 (Tool Design & MCP Integration)**: the decomposition principle — one capability gap = one tool.
- Exam pattern: question describes a feature (e.g., "remind me in a week") and asks how many tools or what kind of tool design — answer emphasizes atomic tools Claude can compose.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the target user interaction in the reminder project? | `"Set a reminder for my doctor's appointment. It's a week from Thursday."` → `"OK, I will remind you."` |
| What three capability gaps does the reminder project identify? | Limited time awareness, unreliable date arithmetic, and no built-in reminder mechanism. |
| What are the three tools built in the project? | `get_current_datetime`, `add_duration_to_datetime`, `set_reminder`. |
| Why build three small tools instead of one big one? | Composability, testability, observability, model-side reasoning, and graceful degradation. |
| In what order are the tools introduced and why? | Simplest and read-only first (`get_current_datetime`), then pure function, then side-effecting (`set_reminder`) — a safety gradient. |
| How many tool-use turns may one reminder request take? | Up to three — one per tool invocation — before Claude emits the final natural-language confirmation. |
| What is the design principle this project illustrates? | One capability gap = one atomic tool; let Claude plan the composition. |
| What is the "LLM as planner" framing? | Instead of treating the LLM as a text classifier into one big function, give it small primitives and let it orchestrate them. |
