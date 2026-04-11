# Agents and Tools — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) |
| Task Statements | 1.1 (agent architecture), 1.2 (agentic loop), 1.3 (tool use in agents), 5.1 (production pattern selection) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 81 |

---

## One-Liner

Agents let you ship one feature that handles many unpredictable user requests — you hand Claude a goal plus a simple toolbox, and Claude figures out the rest instead of your team hard-coding every user flow in advance.

---

## Why PMs Should Care

As a PM, the agent-vs-workflow decision is really a product strategy question: "Are user requests narrow and predictable, or wide and open-ended?"

| Situation | What Workflows Give You | What Agents Give You |
|-----------|------------------------|---------------------|
| Bounded, repeat use cases | Highest reliability | Unnecessary complexity |
| Creative, open-ended requests | Brittle, frustrating UX | Flexibility, delight |
| "We know the 5 things users will ask" | Workflow wins | Over-engineering |
| "Users ask things we never imagined" | Endless PM backlog patching | Agent wins |

Agents let you ship **one coherent capability** instead of N feature flags.

---

## Mental Model: The Swiss Army Knife vs the Kitchen Gadget Drawer

A specialized workflow is like the kitchen drawer of single-purpose gadgets:

- Avocado slicer — works great for avocados, useless for apples
- Egg separator — works great for eggs, useless for anything else
- Garlic press — works great for garlic, useless for ginger

An agent is the Swiss Army knife:

- Knife, scissors, screwdriver, can opener — each tool is simple
- The **user's creativity** decides what to do with them
- One tool covers scenarios the manufacturer never imagined

In product terms: if your PRD has a long list of "feature X, feature Y, feature Z" all solving related problems, you might actually be shipping the gadget drawer when a Swiss Army knife would be better.

---

## Product Use Cases

### When to Choose an Agent

| Scenario | Why an Agent Wins |
|----------|-------------------|
| "Help me with my taxes" assistant | Users will ask wildly different questions you cannot enumerate in advance |
| AI coding assistant (Claude Code) | Any codebase in any language — impossible to pre-build a workflow per case |
| Creative content studio | "Make me a promo video" can mean a thousand different things |
| Support copilot over messy internal data | Different customers have different questions about different systems |

### When to Choose a Workflow Instead

| Scenario | Why a Workflow Wins |
|----------|--------------------|
| "Summarize this meeting transcript" | One known input, one known output |
| "Translate this product description" | Deterministic, measurable, cheap to evaluate |
| "Extract invoice fields" | Compliance/audit requires predictable behavior |
| Regulated workflows (legal, medical) | You need to certify each step |

---

## The "Combinable Tools" Principle (for PMs)

Your engineers will ask: "Should I build tools like `refactor_function` or like `edit_file`?" The right answer is almost always the more generic one. Here is why it matters for your roadmap:

1. **Scope expands for free** — one generic tool covers dozens of user requests you would otherwise each ticket separately.
2. **Roadmap survives surprise** — when users ask for something unexpected (they will), the agent already handles it.
3. **Fewer features to maintain** — every narrow tool is a feature you have to eval, monitor, and deprecate.
4. **Ships faster** — five primitives beat fifty specialists to first release.

**Red flag in specs**: if your PRD lists 20 narrowly scoped AI actions, your engineering team will probably spend 6 months and still miss user requests. Re-frame as "what is the smallest toolbox that covers 80 percent of these?"

---

## PM Decision Framework

When scoping an AI feature, walk through these questions:

| Question | If Yes | Points To |
|----------|--------|-----------|
| Can you list every user flow in advance? | Yes | Workflow |
| Do users phrase requests in varied, unpredictable ways? | Yes | Agent |
| Is "wrong answer" a compliance or safety risk? | Yes | Workflow (predictable) |
| Do you need to handle creative combinations? | Yes | Agent |
| Does each extra scenario cost you another sprint? | Yes | Probably agent — you are fighting the wrong pattern |
| Is cost per request extremely sensitive? | Yes | Workflow (cheaper, fewer tokens) |

---

## Common PM Mistakes

1. **Specifying the flow instead of the goal** — writing PRDs that say "call tool A then tool B" forces engineering into workflow mode even when an agent would serve users better.
2. **Adding tools to an agent every time a user complains** — you should be improving system prompts and tool descriptions, not bolting on `handle_edge_case_47`.
3. **Picking agents for a narrow problem** — "Summarize this article" does not need an agent. You pay 3x the cost for zero flexibility benefit.
4. **Not budgeting for eval complexity** — agents are 3-10x harder to evaluate than workflows. Plan for it or your release cycle will stall.
5. **Ignoring latency impact** — each agent loop iteration is another round trip. Chatty agents feel slow to users.

> **Key Insight**
>
> Pick an agent when you cannot enumerate the user flows in advance — and pick a workflow the rest of the time. Most production AI features are workflows masquerading as agents, or agents drowning under a workflow-style PRD. Matching the pattern to the problem is the highest-leverage PM decision in any agentic product.

---

## CCA Exam Relevance

- **D1 (Agentic Coding & Architecture)**: Expect questions framed as "a user wants to do X — should you build a workflow or an agent?" The pattern is unpredictability = agent, predictability = workflow.
- **D5 (Enterprise Deployment)**: Know that agents are more expensive and harder to evaluate. This is the main production trade-off.
- Exam flag words: "varied requests" or "novel combinations" -> agent; "well-defined steps" or "known sequence" -> workflow.

---

## Flashcards

| Front | Back |
|-------|------|
| When should a PM choose an agent over a workflow? | When user requests are varied, unpredictable, and cannot be enumerated in advance. |
| What is the product analogy for abstract tools vs specialized tools? | Swiss Army knife (general primitives) vs kitchen gadget drawer (one tool per use case). |
| Give two product scenarios where a workflow beats an agent. | Summarizing transcripts, extracting invoice fields, translating descriptions, regulated legal flows (any two). |
| Why are agents more expensive to run than workflows? | Each loop iteration is another API call and more tokens; open-ended reasoning uses more compute per task. |
| What is the red flag in a PRD that hints you should build an agent instead? | A long list of narrowly scoped AI actions all solving related problems. |
| Name three downsides of agents PMs must plan for. | Higher cost, lower reliability, harder to evaluate, slower latency, less predictable behavior (any three). |
| Why should PMs avoid over-specifying the tool sequence in PRDs? | It forces engineering into workflow mode even when agents would serve users better, eliminating the flexibility benefit. |
| What is the most important PM trade-off in agent design? | Flexibility vs predictability — agents handle novel requests but are harder to test, eval, and control. |
