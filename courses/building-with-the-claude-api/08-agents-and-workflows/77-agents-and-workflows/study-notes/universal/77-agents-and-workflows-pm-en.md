# Agents and Workflows — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) — PRIMARY |
| Task Statements | 1.1 (agent vs workflow definition), 1.2 (agentic patterns), 5.2 (production workflow deployment) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 77 |

---

## One-Liner

As a PM, your single most important AI architecture call is **workflow vs agent** — workflows give you predictable, shippable features, while agents unlock open-ended capabilities at the cost of testing effort, cost variance, and eval complexity.

---

## Mental Model: The Assembly Line vs The Detective

| | Assembly Line (Workflow) | Detective (Agent) |
|---|--------------------------|-------------------|
| **Job posting** | "Do step A, then B, then C on every unit" | "Solve the crime. Here are your tools: badge, phone, car." |
| **Predictability** | Every unit comes out the same | Every case is different |
| **Failure shape** | Broken conveyor belt (fix your code) | Bad judgment call (retrain the detective) |
| **Hiring criteria** | You know the flowchart | You trust the detective's reasoning |
| **Cost** | Predictable per unit | Varies wildly per case |
| **Scaling** | Add more lines | Hire better detectives |

Most production AI products are assembly lines (workflows) with occasional detective stations (agents) for the cases the line cannot handle. Anthropic's guidance: **start with the assembly line.**

---

## Product Use Cases

### When a Workflow Fits

| Scenario | Why Workflow |
|----------|--------------|
| PDF invoice → structured data | Fixed inputs and outputs, known fields |
| Customer ticket → draft reply | Predefined steps: classify → retrieve → draft → review |
| Image of a part → 3D CAD file | Sequential deterministic pipeline (the lesson example) |
| Translate doc preserving formatting | Known transformation, testable per step |
| Daily report from SaaS metrics | Repeatable schedule, fixed data sources |

### When an Agent Fits

| Scenario | Why Agent |
|----------|-----------|
| Coding assistant that reads/writes files | Cannot predict which files the user needs |
| Research helper that browses and cites | Search path depends on what it finds |
| DevOps incident responder | Next action depends on live system state |
| Custom data analyst chatbot | User asks open-ended questions |

### When to Avoid Both (Just Use Single-Turn Claude)

- The task fits in one prompt
- There's no tool use required
- The output is short and final

Not everything needs orchestration. Over-engineering a single-turn task into a workflow is a common PM mistake.

---

## PM Decision Framework

Ask these questions *in order*:

1. **Can you draw the flowchart?** If yes → workflow.
2. **Do you have evals for end-to-end behavior?** If not → workflow (you cannot ship an agent without evals).
3. **Is per-request cost variance acceptable to finance?** If not → workflow (agents can loop).
4. **Can ops teams debug a variable-length trace?** If not → workflow (traces get messy fast).
5. **Only reached here?** You may have a real agent use case. Budget for 2–3× the workflow timeline.

---

## The Four Hidden Costs of "Just Build an Agent"

PMs often underestimate how much harder an agent is to ship than a workflow:

1. **Eval cost** — workflows can be tested per-step with small datasets; agents need end-to-end trajectories across diverse inputs.
2. **Cost variance** — a workflow has a predictable token bill per run; an agent can loop, spike, and blow budgets.
3. **Observability cost** — workflows map to clean spans; agents need replayable trajectories that are expensive to build.
4. **Support cost** — when a workflow breaks, engineers fix code; when an agent makes a bad call, PMs debate whether it's a prompt issue, a tool issue, or a model issue.

These costs show up *after* launch, which is why Anthropic advises starting with workflows.

---

## The Evaluator-Optimizer Pattern (A PM Favorite)

The lesson's CAD example introduces the **evaluator-optimizer** pattern: a producer creates output, a grader evaluates it, and a feedback loop repeats until the grader accepts.

From a PM lens, this pattern gives you:

- **Quality control inside the feature** — the grader is your automated QA
- **Bounded iteration** — you cap attempts, so cost is predictable
- **Self-correction without handing control to Claude** — stays a workflow

Great candidate for features where "first draft" is acceptable input but "publishable version" is required output: generated marketing copy, auto-edited images, auto-written SQL.

---

## Common PM Mistakes

1. **Calling a multi-step prompt chain "our agent."** It's a workflow. Using the wrong word sets wrong expectations with stakeholders and investors.
2. **Shipping an agent without evals.** Agents are only as reliable as the evals you build to measure them. No evals = no ship.
3. **Promising flat-rate pricing on an agent feature.** Without guardrails, one bad query can cost 50× the average. Either gate by tier or enforce max-step budgets.
4. **Assuming "agent" means "smart."** Agents are *autonomous*, not necessarily more capable. A well-designed workflow often outperforms a naive agent.
5. **Not planning for the evaluator-optimizer pattern.** Many product requirements ("draft must be publishable, not just okay") are solved elegantly by this pattern — but only if you explicitly design it.

---

> **Key Insight**
>
> The workflow-vs-agent decision is the single biggest architecture call a PM makes on an AI feature. Workflows give you predictability, shippability, and cost control — but require you to know the flow upfront. Agents give you flexibility — but cost you eval work, cost variance, and debuggability. Anthropic's own advice is: **start with the workflow**, and only move to an agent when the task genuinely cannot be expressed as a flowchart. Most "we need an agent" conversations end up as "actually, a workflow works."

---

## CCA Exam Relevance

- **D1 (22%) PRIMARY**: This is the most-tested domain. Expect to classify scenarios — memorize the flowchart heuristic.
- **D5 (20%) SECONDARY**: The reason the distinction matters is production — observability, cost, eval.
- Exam signal words for workflow: "predefined steps", "predetermined series", "orchestrated", "pipeline".
- Exam signal words for agent: "given a goal", "Claude decides", "autonomous", "open-ended".

---

## Flashcards

| Front | Back |
|-------|------|
| What is the core PM question that decides workflow vs agent? | Can you draw the flowchart before runtime? |
| Why does Anthropic advise starting with workflows? | They are cheaper, more predictable, more testable, and faster to ship |
| What is the assembly-line analogy for workflows? | Known steps on every unit, breakdowns mean fix the code |
| What is the detective analogy for agents? | Given a goal and tools, figures out the next step, failures are judgment calls |
| Name four hidden costs of agents vs workflows. | Eval cost, cost variance, observability cost, support cost |
| What is the evaluator-optimizer pattern in PM terms? | Automated quality control — producer drafts, grader reviews, loop until accepted |
| When should you AVOID both a workflow and an agent? | When the task fits in a single prompt with no tool use |
| What is the biggest PM mistake with agents? | Shipping them without end-to-end evals and without capping step counts |
