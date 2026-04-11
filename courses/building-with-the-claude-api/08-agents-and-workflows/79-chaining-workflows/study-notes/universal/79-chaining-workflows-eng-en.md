# Chaining Workflows — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) — PRIMARY |
| Task Statements | 1.2 (agentic patterns — chaining), 5.2 (production workflow deployment) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 79 |

---

## One-Liner

Chaining is the simplest and most useful workflow pattern: break a complex task into a sequence of focused LLM calls where each step's output feeds the next — the opposite of parallelization, used when later steps *depend on* earlier ones.

---

## What Is Prompt Chaining

From Anthropic's "Building Effective Agents" blog post, **prompt chaining** decomposes a task into a sequence of steps, where each LLM call processes the output of the previous one. This pattern is ideal when you can cleanly decompose a task but each step depends on the prior step's results.

The key signal that you need chaining: you can list the steps in order, and step N+1 genuinely needs step N's output.

---

## The Social Media Example from the Lesson

The lesson walks through a social media marketing tool that auto-generates and posts videos:

```
1. Find related trending topics on Twitter       (non-LLM)
2. Select the most interesting topic              (Claude)
3. Research the topic                             (Claude)
4. Write a script for a short-form video          (Claude)
5. Generate video with AI avatar + text-to-speech (non-LLM)
6. Post to social media                           (non-LLM)
```

Key observations:
- **Not every step is an LLM call.** Chains can interleave LLM and non-LLM processing (step 1 is Twitter API, step 5 is a video pipeline, step 6 is a posting API).
- **Each LLM step is focused.** Claude picks a topic in step 2, researches in step 3, writes a script in step 4 — never all three in one prompt.
- **Outputs are passed forward.** The chosen topic becomes input to the research step; the research becomes input to the script.

---

## Why Chain Instead of One Big Prompt

Chaining gives you:

1. **Focused attention per step.** Claude does one thing well instead of juggling everything.
2. **Non-LLM processing hooks.** Between steps, your code can validate, transform, fetch data, or short-circuit.
3. **Testability.** Each step has a clean input/output contract — easy to unit-test and eval.
4. **Observability.** Failures are localized to a specific step, not buried in a single monolithic prompt.
5. **Partial reruns.** If step 3 of 5 fails, you can rerun from step 3 instead of starting over.

---

## The Long Prompt Problem (The Lesson's Core Motivation)

Even with carefully worded constraints, Claude sometimes ignores rules in long prompts. The lesson gives an example: writing a technical article that:

- must not mention AI authorship
- must avoid emojis
- must skip clichéd / casual language
- must be professional and technical

A single prompt trying to enforce all four constraints *and* generate a good article often produces output that violates one or more rules.

### The Chaining Solution

Split into two steps:

**Step 1 — First draft**
```python
draft = claude.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=2048,
    messages=[{"role": "user",
               "content": f"Write a technical article about {topic}."}]
).content[0].text
```

**Step 2 — Focused revision**
```python
final = claude.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=2048,
    messages=[{"role": "user", "content": f"""
Revise the article provided below.

Follow these steps to rewrite the article:
1. Identify any location where the text identifies the author as an AI and remove them
2. Find and remove all emojis
3. Locate any cringey writing and replace it with text that would be written by a technical writer

<article>
{draft}
</article>
"""}]
).content[0].text
```

In step 2, Claude is not trying to *create* a good article *and* satisfy constraints — it is only enforcing constraints on an already-written article. The focused task succeeds where the combined task fails.

---

## Canonical Python Implementation

```python
from anthropic import Anthropic

client = Anthropic()

def call_claude(system: str, user: str) -> str:
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return resp.content[0].text

def social_media_chain(keyword: str) -> str:
    # Step 1: non-LLM — fetch trends
    trends = twitter_api.fetch_trends(keyword)

    # Step 2: LLM — pick the best topic
    topic = call_claude(
        system="You pick the most engaging trend.",
        user=f"Trends:\n{trends}\n\nReturn the single best topic.",
    )

    # Step 3: LLM — research the topic (with error check)
    research = call_claude(
        system="You are a concise researcher.",
        user=f"Research the topic: {topic}",
    )
    if len(research) < 100:
        raise RuntimeError("Research step returned too little content")

    # Step 4: LLM — write a script using research
    script = call_claude(
        system="You write 60-second video scripts.",
        user=f"Write a script using this research:\n{research}",
    )

    # Step 5: non-LLM — synthesize video
    video = video_pipeline.synthesize(script)

    # Step 6: non-LLM — post
    return social_media.post(video)
```

Each step has a clear contract, an error-handling hook, and can be replaced independently.

---

## Error Propagation in Chains

Because each step depends on the previous one, chains must handle errors deliberately:

| Strategy | Description | Use When |
|----------|-------------|----------|
| **Fail fast** | Raise on first failure | Early prototype, simple flows |
| **Retry step** | Retry the failing step with backoff | Transient API errors |
| **Validate then branch** | Inspect step output, choose next step | Output quality varies (e.g., empty research) |
| **Graceful degradation** | Skip non-critical steps | Optional enrichment steps |
| **Replay from checkpoint** | Persist step outputs, resume on retry | Long chains, expensive calls |

A production chain typically combines all five, with each step wrapped in retry + validation.

---

## Chaining vs Parallelization vs Agents

| Aspect | Chaining | Parallelization | Agent |
|--------|----------|-----------------|-------|
| Step dependencies | Yes (sequential) | No (independent) | Decided at runtime |
| Control flow | Code | Code | LLM |
| Latency | Sum of step latencies | Max of step latencies | Variable |
| Cost | Sum of step costs | Sum of step costs | Variable |
| Best for | Complex multi-step tasks with dependencies | Complex decisions across independent criteria | Open-ended tasks |

---

## Common Mistakes

1. **Building an agent when chaining would do.** If you can list the steps, chaining is simpler and more reliable than handing the flow to Claude.
2. **Chains that are too long.** Each step is a potential failure point. If you have 10+ LLM calls in a chain, consider splitting into multiple chains with checkpoints.
3. **Forgetting to pass context between steps.** Step 4 needs step 3's output — do not assume Claude remembers; explicitly inject it.
4. **No error handling between steps.** A single bad step can propagate garbage all the way to the final output. Validate between steps.
5. **Chaining what should be a single call.** Not every task needs to be chained. If one prompt works reliably, use one prompt.

---

> **Key Insight**
>
> Chaining is the "break the long prompt problem" pattern. When Claude ignores constraints in a monolithic prompt, split the task: one call to create, another to enforce. This focused-attention principle extends to any multi-step task where the next step genuinely needs the previous step's output. For the exam, remember: **chaining has sequential dependencies, parallelization does not.**

---

## CCA Exam Relevance

- **D1 (22%) PRIMARY**: Chaining is one of the four core workflow patterns. Expect a scenario question distinguishing it from parallelization and routing.
- **D5 (20%) SECONDARY**: Production chains need error handling, checkpoints, and validation between steps.
- Signal words for chaining: "sequential", "output of step N feeds step N+1", "focus on one aspect at a time", "break down into steps".
- Key distinction: chaining = sequential dependencies; parallelization = independent sub-tasks.

---

## Flashcards

| Front | Back |
|-------|------|
| What is prompt chaining? | Break a task into sequential LLM calls where each step's output feeds the next |
| How does chaining differ from parallelization? | Chaining has sequential dependencies; parallelization runs independent sub-tasks concurrently |
| What is "the long prompt problem" that chaining solves? | Claude ignores constraints in monolithic prompts; splitting into create + revise steps enforces them reliably |
| Can chains include non-LLM steps? | Yes — chains often interleave LLM calls with API calls, validation, and data transforms |
| What is the two-step chaining solution for constraint enforcement? | Step 1: generate initial draft. Step 2: dedicated revision pass that enforces each rule |
| Name four error-handling strategies for chains. | Fail-fast, retry-step, validate-then-branch, graceful degradation, replay-from-checkpoint |
| What is the trade-off between chaining and parallelization? | Chaining sums latencies (slower) but supports dependencies; parallelization maxes latency but requires independence |
| When should you NOT use chaining? | When a single prompt works reliably, or when sub-tasks can run independently (use parallelization) |
