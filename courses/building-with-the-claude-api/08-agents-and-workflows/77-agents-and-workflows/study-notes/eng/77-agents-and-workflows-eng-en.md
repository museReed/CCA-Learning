# Agents and Workflows — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) — PRIMARY |
| Task Statements | 1.1 (agent vs workflow definition), 1.2 (agentic patterns), 5.2 (production workflow deployment) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 77 |

---

## One-Liner

**Workflows** are orchestrated by *code* through a predefined sequence of LLM calls; **agents** are orchestrated by the *LLM itself*, which decides the next step given a goal and a set of tools. The choice between them comes down to how well you can specify the task flow in advance.

---

## The Fundamental Distinction (ALWAYS TESTED)

This distinction is from Anthropic's "Building Effective Agents" blog post (December 2024) and is the single most-tested concept in D1 of the CCA exam.

| Aspect | Workflow | Agent |
|--------|----------|-------|
| **Control flow** | Predefined in code | LLM decides dynamically |
| **Who orchestrates** | Your Python/TS code | Claude (via tool use loop) |
| **Task shape** | Known and repeatable | Open-ended |
| **Steps** | Fixed sequence (or fixed branching) | Emergent — depends on runtime context |
| **Predictability** | High — easy to test and trace | Lower — requires evals + guardrails |
| **Best when** | You can draw the flowchart | You cannot enumerate all paths |

**Canonical definition (memorize this):**

> Workflows are a series of calls to Claude meant to solve a specific problem through a *predetermined* series of steps. Agents give Claude a goal and a set of tools, expecting Claude to figure out how to complete the goal through the provided tools.

---

## Decision Heuristic

Ask yourself: **"Can I draw a flowchart of the solution before runtime?"**

- **Yes → workflow.** Encode the flowchart in code. You stay in control.
- **No → agent.** Give Claude tools and a goal, then run a tool-use loop.

A related test: if your app's UX constrains users to a known set of tasks (upload image → get STEP file), it's almost always a workflow. If users type freeform requests (a coding assistant, a research helper), it's almost always an agent.

---

## Worked Example: Image to CAD Workflow

The lesson walks through a web app where users drop an image of a metal part and receive a STEP file (3D CAD format):

```python
def image_to_cad_workflow(image_bytes: bytes) -> bytes:
    # Step 1: describe the object
    description = claude_describe_image(image_bytes)

    # Step 2: generate CadQuery code from description
    cad_code = claude_write_cadquery(description)

    # Step 3: execute code to produce a rendering
    rendering = run_cadquery(cad_code)

    # Step 4: grader loop (evaluator-optimizer)
    for attempt in range(MAX_ATTEMPTS):
        grade = claude_grade(image_bytes, rendering)
        if grade.accepted:
            return export_step(cad_code)
        cad_code = claude_fix(cad_code, grade.feedback)
        rendering = run_cadquery(cad_code)

    raise RuntimeError("Grader never accepted output")
```

The code owns the control flow. Claude is called as a *function* four times per iteration. This is the hallmark of a workflow.

---

## The Evaluator-Optimizer Pattern

The CAD example above is an instance of the **Evaluator-Optimizer** pattern from Anthropic's blog:

- **Producer** — takes input, creates output (the CadQuery modeler)
- **Grader / Evaluator** — scores the output against criteria
- **Feedback loop** — if not accepted, send feedback back to producer
- **Iteration** — repeat until accepted or max attempts

This pattern gives you self-correcting behavior *without* handing control to Claude. The code decides when to stop, when to retry, and how many attempts are allowed — all critical properties for production systems.

Other named workflow patterns from the same blog post:

| Pattern | Core Idea | Lesson Coverage |
|---------|-----------|-----------------|
| Prompt chaining | Sequential LLM calls, output feeds input | Lesson 79 |
| Parallelization | Split a task into parallel sub-tasks and aggregate | Lesson 78 |
| Routing | Classifier picks a specialized handler | Lesson 80 |
| Orchestrator-workers | Central LLM delegates to worker LLMs | Later lessons |
| Evaluator-optimizer | Producer + grader feedback loop | Lesson 77 |

---

## Why the Distinction Matters in Production

The workflow-vs-agent choice has direct consequences on:

1. **Observability** — workflow steps are trivial to log (one span per node); agent traces are variable-length and harder to compare across runs.
2. **Cost control** — workflows have known step counts; agents can loop unexpectedly (budget-exhaustion is a real production failure mode).
3. **Eval strategy** — workflows can be evaluated per-step; agents need end-to-end evals on diverse trajectories.
4. **Failure modes** — workflow failures are in *your code*; agent failures are in *Claude's decisions* and require prompt + tool redesign.
5. **Time to first success** — workflows are faster to ship; agents usually require iteration on the tool set and system prompt.

---

## Common Mistakes

1. **Reaching for an agent when a workflow would do.** If you can draw the flowchart, a workflow is cheaper, more reliable, and easier to debug. Anthropic explicitly recommends starting with workflows.
2. **Calling everything an "agent."** Multi-step prompt chains with no runtime LLM control flow are workflows, not agents. Precision matters on the exam.
3. **Forgetting the evaluator-optimizer loop has a max-attempts cap.** Without it, a bad grader can run forever and exhaust your budget.
4. **Assuming workflows cannot use tools.** Workflows can absolutely call tools — the distinction is about who decides the *sequence*, not whether tools exist.
5. **Treating workflow patterns as theory.** You still have to write the code. The patterns are recipes, not frameworks.

---

> **Key Insight**
>
> The difference between a workflow and an agent is **who owns the control flow**. In a workflow, your code owns it. In an agent, Claude owns it. Everything else — observability, cost, eval strategy, failure mode — flows from that one question. The CCA exam will often phrase this indirectly ("predetermined steps" = workflow, "Claude decides next action" = agent) — train yourself to spot the signal words.

---

## CCA Exam Relevance

- **D1 (22%) PRIMARY**: Lesson 77 is the foundational chapter for the most-tested domain. Expect at least one question that asks you to classify a scenario as agent vs workflow.
- **D5 (20%) SECONDARY**: Production deployment considerations (observability, cost, eval strategy) are tied to the choice.
- Signal words that point to a **workflow**: "predetermined series", "fixed steps", "orchestrated by code", "pipeline".
- Signal words that point to an **agent**: "given a goal and tools", "Claude decides", "autonomous", "open-ended task".

---

## Flashcards

| Front | Back |
|-------|------|
| What is the core difference between a workflow and an agent? | Who owns control flow — workflow = code; agent = Claude |
| Give the canonical one-line definition of a workflow. | A series of calls to Claude that solves a problem through a predetermined series of steps |
| Give the canonical one-line definition of an agent. | Give Claude a goal and a set of tools, and let Claude figure out how to complete the goal |
| What heuristic decides workflow vs agent? | Can you draw the flowchart before runtime? Yes → workflow, No → agent |
| What is the evaluator-optimizer pattern? | Producer creates output, grader evaluates it, feedback loops back until accepted |
| Name 4 workflow patterns from Anthropic's "Building Effective Agents". | Prompt chaining, parallelization, routing, evaluator-optimizer (also orchestrator-workers) |
| Why does Anthropic recommend starting with workflows? | They are cheaper, more observable, easier to test, and faster to ship than agents |
| What production risk is unique to agents vs workflows? | Unbounded step counts / budget exhaustion — agents can loop indefinitely if guardrails are missing |
