# Workflows vs Agents — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%); D5 — Enterprise Deployment (20%) |
| Task Statements | 1.1 (agent vs workflow architecture), 1.2 (agentic loop), 5.1 (production pattern selection) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 83 |

---

## One-Liner

**Default to workflows, escalate to agents only when unavoidable** — workflows give reliability and predictability for known problems, agents give flexibility for open-ended ones, and the engineer's job is to pick the cheapest pattern that actually solves the user's problem.

---

## Definitions

### Workflow

A **predefined sequence of Claude calls** that solves a known problem. The developer writes the control flow explicitly: "call model A to classify, then call model B to draft, then call model C to review." Each call has a narrow job.

```python
def summarize_ticket(ticket):
    category = classify(ticket)               # Step 1
    summary = summarize(ticket, category)     # Step 2
    priority = score_priority(summary)        # Step 3
    return {"category": category, "summary": summary, "priority": priority}
```

### Agent

A **goal + tool set** handed to Claude, which decides at runtime what to call and in what order. No hard-coded sequence.

```python
messages = [{"role": "user", "content": user_goal}]
while True:
    response = client.messages.create(model="claude-sonnet-4-5", tools=tools, messages=messages)
    if response.stop_reason == "end_turn": break
    # handle tool_use, loop continues
```

The difference is **who owns the control flow**: developer (workflow) or Claude (agent).

---

## The Full Comparison Table

| Dimension | Workflow | Agent |
|-----------|----------|-------|
| **Flexibility** | Low — handles only the shapes you hard-coded | High — combines tools for novel requests |
| **Reliability** | High — each step is narrow and well-tested | Lower — open-ended planning can fail unexpectedly |
| **Cost per task** | Low — predictable token count, cacheable | High — multiple loop iterations, more tokens |
| **Latency** | Low — fixed number of sequential calls | Variable — depends on how many loops Claude takes |
| **Debuggability** | High — you know the step that failed | Low — non-deterministic trajectory, harder to reproduce |
| **Predictability** | High — same input, same sequence every time | Low — Claude may choose different tool chains for similar inputs |
| **Eval effort** | Moderate — test each step in isolation | Hard — must eval emergent behavior, more test cases |
| **Upfront design cost** | High — you must enumerate the flow | Lower — design the toolbox, not the flow |
| **Best use cases** | Summarization, classification, extraction, translation, compliance flows | Coding assistants, creative content, open Q&A over messy data |
| **Worst use cases** | Open-ended or varied user requests | Narrow repeatable tasks with a known sequence |

---

## Benefits and Downsides from the Source

### Workflow Benefits

- Claude focuses on one subtask at a time, generally leading to higher accuracy
- Far easier to evaluate and test — you know each step
- More predictable and reliable execution
- Better suited for well-defined problems

### Workflow Downsides

- Far less flexible — dedicated to specific task types
- More constrained UX — you need to know the exact inputs
- Requires more upfront planning and design

### Agent Benefits

- More flexible UX
- Can combine tools in unexpected ways
- Handles novel situations not anticipated at design time
- Can ask users for additional input when needed

### Agent Downsides

- Lower task completion rate vs workflows
- Harder to instrument, test, and evaluate
- Less predictable behavior

---

## The Decision Framework

The Anthropic guidance is explicit: **default to workflows. Reach for agents only when workflows genuinely cannot solve the problem.**

Walk through this checklist for every AI feature:

```
1. Can I enumerate every user flow in advance?
   YES -> workflow
   NO  -> continue

2. Is the task a pure transformation (input -> output) with no branching?
   YES -> workflow
   NO  -> continue

3. Does the user phrase requests in varied, unpredictable ways?
   YES -> continue evaluating agent
   NO  -> workflow

4. Does the correct action depend on the current environment state?
   YES -> agent (with environment inspection)
   NO  -> workflow

5. Can I afford the cost, latency, and eval complexity of an agent?
   YES -> agent
   NO  -> decompose into smaller workflows
```

This is not a purity test — hybrid systems exist. Common pattern: an outer workflow that routes to an inner agent for the flexible steps, with workflow guardrails on the rest.

---

## The Cost and Latency Math

A workflow with 3 fixed model calls at ~1000 tokens each:

- **Tokens**: ~3000 per task (deterministic)
- **Latency**: 3 sequential calls, ~3-6 seconds total
- **Cost**: predictable, cacheable with prompt caching

An agent solving the same task with 3-10 loop iterations:

- **Tokens**: ~3000 to ~30000 per task (variable)
- **Latency**: 3-10 round trips, ~5-30 seconds total
- **Cost**: 1x to 10x the workflow cost for the same output quality

If your eval shows the workflow achieves 95 percent accuracy and the agent achieves 96 percent, the agent's flexibility is probably not worth the 5-10x cost multiplier. Pick the cheapest pattern that hits your quality bar.

---

## Hybrid Patterns in Practice

Real production systems rarely pick one or the other. Common hybrids:

| Pattern | How It Works | Example |
|---------|--------------|---------|
| **Workflow routing to agents** | A cheap classifier workflow decides if the request needs agent-level flexibility | Support ticket router: FAQ -> workflow, novel bug -> agent |
| **Agent with workflow sub-steps** | The agent calls a workflow as one of its tools | Coding agent that calls a deterministic "run_tests" workflow |
| **Agent with workflow safety gate** | The agent proposes actions, a workflow validates them before execution | AI trader proposes trades, workflow checks compliance rules |
| **Retry escalation** | Start with workflow, escalate to agent on failure | Extract structured data; fall back to agent when schema varies |

These patterns let you keep the reliability of workflows for 80 percent of traffic while reserving agent flexibility for the hard 20 percent.

---

## Common Mistakes

1. **Agent-washing** — building everything as an agent because it sounds modern, then fighting cost and eval for the rest of the project lifetime.
2. **Workflow rigidity** — forcing every variation into a branch of an if-tree, eventually producing unmaintainable spaghetti. This is when to escalate to an agent.
3. **Skipping eval on agents** — because agents have variable trajectories, you need larger, more diverse eval sets than workflows, not smaller.
4. **Ignoring the latency tax** — each agent loop is a round trip. Chatty agents feel sluggish even if each call is fast.
5. **Not measuring the cost per successful task** — "tokens per call" is the wrong metric; "cost per verified success" is what matters.

> **Key Insight**
>
> The Anthropic recommendation is crisp: default to workflows, pick agents only when you cannot predetermine the steps. Users do not care whether you built a clever agent — they care that the product works reliably. Matching the pattern to the problem (and being honest about which you actually have) is the highest-leverage architectural decision in any agentic product.

---

## CCA Exam Relevance

- **D1 (Agentic Coding & Architecture)**: Expect direct questions on "when to use an agent vs a workflow." Memorize the trade-off table.
- **D5 (Enterprise Deployment)**: Cost, latency, eval complexity, and debuggability are the production-facing trade-offs. Know which pattern wins on each axis.
- Exam phrasing cues: "varied requests," "unpredictable," "combine tools creatively" -> agent; "well-defined steps," "known flow," "compliance," "cheapest predictable" -> workflow.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the Anthropic default recommendation? | Default to workflows; reach for agents only when workflows cannot solve the problem. |
| Who owns the control flow in a workflow vs an agent? | Workflow: the developer hard-codes the sequence. Agent: Claude decides the sequence at runtime. |
| Name three dimensions where workflows beat agents. | Reliability, cost, latency, debuggability, predictability (any three). |
| Name three dimensions where agents beat workflows. | Flexibility, novel-case coverage, user-driven conversational UX, lower upfront design cost (any three). |
| Why are agents harder to evaluate than workflows? | Agents have non-deterministic trajectories — you cannot test each fixed step in isolation; you must test emergent behavior over many cases. |
| What is a hybrid pattern that combines both? | A workflow router that sends easy cases to workflow branches and hard cases to an agent. |
| What cost metric matters more than "tokens per call"? | Cost per verified successful task — agents may use more tokens but still be cheaper per success if they handle cases workflows cannot. |
| In the decision framework, what is the first question to ask? | Can I enumerate every user flow in advance? If yes -> workflow. |
