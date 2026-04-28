# Workflows vs Agents — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%); D5 — Enterprise Deployment (20%) |
| Task Statements | 1.1 (agent vs workflow architecture), 1.2 (agentic loop), 5.1 (production pattern selection) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 83 |

---

## One-Liner

Workflows are the reliable, cheap, predictable architecture for AI features you can fully specify; agents are the flexible, expensive, less predictable architecture for ones you cannot — and the PM's job is to match the pattern to the problem instead of picking whichever sounds cooler in a roadmap review.

---

## Why PMs Should Care

Every AI feature PRD implicitly chooses between these two architectures. If you do not make the choice consciously, engineering will make it for you — usually by building whichever they find more interesting, which is usually an agent. Six months later you will be debating why cost per ticket is 10x the workflow alternative that would have shipped in a third of the time.

This is one of those decisions where the right answer for the user is almost always the less glamorous one.

---

## Mental Model: The Assembly Line vs the Workshop

**Workflow = assembly line**. Each station does one job. Inputs come in at the start, products come out at the end. Quality is high, throughput is high, cost is low, and you can measure each station independently. The downside: the line only makes one product. Change the product and you have to retool the line.

**Agent = craftsman's workshop**. The craftsman has tools on the wall and a goal from the customer ("make me a table"). They pick which tool to use and in what order based on the specific request. The output is more flexible — "make me a table with an extra drawer" works the same way. The downside: slower, more expensive per item, harder to measure because each build is different.

Most products should have an assembly line doing 80 percent of the volume and a workshop handling the 20 percent of requests that need hand-crafting.

---

## The Full Comparison Table (PM View)

| Dimension | Workflow | Agent |
|-----------|----------|-------|
| **Reliability** | High — same result every time | Lower — occasional off-the-rails behavior |
| **Cost per task** | Low, predictable | High, variable (1x-10x workflow cost) |
| **Latency** | Low, predictable | Higher, variable |
| **Eval complexity** | Moderate — test each step | Hard — must test emergent behavior |
| **Flexibility** | Low — only what you specified | High — handles novel requests |
| **Time to first ship** | Longer upfront (you must design the flow) | Shorter upfront (design the toolbox) |
| **Time to handle a new user request** | New ticket + new branch | Often zero — agent just handles it |
| **Support tickets for unexpected failures** | Low | Higher, harder to diagnose |
| **User trust** | Builds steadily on predictability | Depends heavily on inspection and guardrails |

---

## Product Use Cases

### Pick Workflow When

| Scenario | Why |
|----------|-----|
| "Summarize this article in 3 bullets" | Pure transformation, one known input |
| "Extract invoice totals" | Compliance demands deterministic behavior |
| "Translate product description" | Measurable, cacheable, cheap |
| "Categorize support tickets" | Narrow, repeatable, eval-friendly |
| Any regulated or audited flow | Predictability is non-negotiable |

### Pick Agent When

| Scenario | Why |
|----------|-----|
| Coding assistant over unknown codebases | Cannot enumerate what users will ask |
| "Help me with my taxes" conversational tool | Every user's question path is different |
| Creative content generation | Creativity requires tool recombination |
| Open-ended debugging helper | Cannot predict the bug in advance |
| Internal "data analyst" across messy schemas | Each question requires fresh exploration |

---

## Cost and Latency — The Business Math

For a typical 3-step task:

| Metric | Workflow | Agent |
|--------|----------|-------|
| Tokens per task | ~3,000 (fixed) | ~3,000 - 30,000 (variable) |
| Latency per task | ~3-6 seconds | ~5-30 seconds |
| Cost multiplier | 1x (baseline) | 1x to 10x |
| Support tickets | 1x (baseline) | 1.5x to 3x (debuggability cost) |

**PM rule of thumb**: if a workflow hits 95 percent accuracy and an agent hits 96 percent, the workflow wins. You are paying a 5-10x cost multiplier for a 1-point accuracy bump you can probably eat with better evals or a retry on the workflow.

---

## PM Decision Framework

Run every AI feature through this sequence:

| Step | Question | If Yes Go To | If No Go To |
|------|----------|--------------|-------------|
| 1 | Can I fully list the user flows in advance? | Workflow | Step 2 |
| 2 | Is the task a pure transformation (A -> B)? | Workflow | Step 3 |
| 3 | Are requests varied and unpredictable? | Step 4 | Workflow |
| 4 | Does the action depend on live environment state? | Agent with inspection | Step 5 |
| 5 | Can we afford 5-10x cost and eval complexity? | Agent | Decompose into smaller workflows |

And always ask a final sanity-check: **would the user notice if we built this as a workflow instead?** If the answer is "no," ship the workflow.

---

## Common PM Mistakes

1. **Choosing agents because they sound modern** — "agentic" sells well in roadmap reviews, but most features should be workflows. Ship reliability first.
2. **Not budgeting for the agent cost multiplier** — cost per request can jump 5-10x with no one forecasting it. Forecast agent cost before committing.
3. **Forgetting eval complexity in the timeline** — agents need 3-10x more eval cases than workflows. Add that to your estimates, not hope it is free.
4. **Writing PRDs that hard-code tool sequences** — this forces engineering into workflow mode even when an agent would serve users better. Write goals, not sequences.
5. **Missing the hybrid option** — production systems are rarely pure agents or pure workflows. A classifier + router is usually the best of both worlds.

> **Key Insight**
>
> The default answer is workflow. Pick an agent only when your user problem genuinely requires it — and when you accept the cost, latency, and eval overhead. Users do not care about your architecture; they care that the feature works reliably, affordably, and predictably. Matching the pattern to the problem is the highest-leverage PM decision in any agentic product.

---

## CCA Exam Relevance

- **D1 (Agentic Coding & Architecture)**: Expect direct "workflow vs agent" scenario questions. The formula: predictable and narrow -> workflow; unpredictable and broad -> agent; always default to workflow.
- **D5 (Enterprise Deployment)**: Production trade-offs — cost, latency, eval, reliability — all favor workflows for most features. This is directly tested.
- Exam cues: "compliance," "predictable," "cheapest" -> workflow; "varied requests," "creative combinations," "novel situations" -> agent.

---

## Flashcards

| Front | Back |
|-------|------|
| What is Anthropic's default recommendation for workflow vs agent? | Default to workflow; use agents only when workflows cannot solve the problem. |
| What is the assembly line vs workshop analogy? | Workflow = assembly line (one product, high throughput, cheap, predictable). Agent = workshop (craftsman with tools, flexible but slow and expensive). |
| Name three dimensions where workflows beat agents in production. | Reliability, cost, latency, debuggability, predictability, eval simplicity (any three). |
| When should a PM pick an agent over a workflow? | When user requests are varied, unpredictable, require creative tool combinations, and workflow accuracy is not acceptable. |
| What is the typical cost multiplier of an agent over a workflow for the same task? | 1x to 10x, depending on how many loop iterations the agent takes. |
| What PRD mistake forces engineering into the wrong architecture? | Writing hard-coded tool sequences instead of stating the user goal — forces workflow mode even when an agent fits better. |
| What is the hybrid pattern most production systems use? | A workflow router sending simple cases through workflow branches and hard cases to an agent. |
| What is the final sanity-check question before picking an agent? | Would the user notice if we built this as a workflow instead? If no, ship the workflow. |
