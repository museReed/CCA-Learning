# Making Changes — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding Fundamentals (22%), D3 — Effective Claude Code Usage (30%) |
| Task Statements | 3.4 ★★★ (plan mode vs direct), 3.5 ★★★ (iterative refinement), 1.1 ★ (agentic loops) |
| Exam Scenarios | S2 (Code Gen), S4 (Developer Productivity) |
| Source | claude-code-in-action / 02-getting-started / Lesson 08 (video + text) |

---

## One-Liner

Claude Code offers three operational modes for different complexity levels: direct execution for simple changes, Planning Mode for complex multi-file restructuring, and Thinking Modes for deep reasoning on ambiguous problems.

---

## Screenshot-Based Communication

The most precise way to tell Claude what to change is to show it:

1. **Take a screenshot** of the UI element you want to modify
2. **Paste with Ctrl+V** (not Cmd+V on macOS) into the Claude Code chat
3. **Describe the change** you want relative to the screenshot

```
[paste screenshot of login form]
> Move the "Forgot Password" link below the submit button
> and make it a lighter gray color
```

> 🎬 **Instructor insight from the video**
>
> The instructor demonstrates pasting a screenshot of the uigen app and asking Claude to modify the UI. He emphasizes using Ctrl+V specifically — "it's Ctrl+V, not Cmd+V" — because this is the keybinding Claude Code uses for image pasting.

This is a form of **multimodal input** — Claude processes both the image and your text instruction to understand the change. Screenshots eliminate ambiguity about which element you mean.

---

## Planning Mode (Task 3.4 ★★★)


![Planning Mode Execution Flow](../../visuals/planning-mode-execution-flow.svg)
*Figure: Planning mode execution flow — explore, plan, review, execute.*

Planning Mode is Claude Code's mechanism for handling complex, multi-file changes. It separates **planning** from **execution**.

### How to Enable

Press `Shift+Tab` twice (or once if already auto-accepting edits):

```
Normal Mode:  Ask → Claude executes immediately
Plan Mode:    Ask → Claude plans → You review → Claude executes
```

### What Planning Mode Does

1. **Reads more files** — Claude explores your codebase more broadly
2. **Creates a detailed plan** — Shows you exactly what it intends to do
3. **Waits for approval** — You review and can redirect before any changes
4. **Executes the plan** — Only after your confirmation

<!-- diagram: plan-mode-flow — Ask → Claude Explores Codebase → Claude Creates Plan → User Reviews Plan → Approve/Redirect → Claude Executes -->

```
┌──────────┐    ┌─────────────────┐    ┌──────────────┐
│ You Ask  │───→│ Claude Explores │───→│ Claude Plans │
└──────────┘    │ (reads files,   │    │ (step-by-step│
                │  searches code) │    │  action list) │
                └─────────────────┘    └──────┬───────┘
                                              │
                                              ▼
                                       ┌──────────────┐
                                       │ You Review   │
                                       │ the Plan     │
                                       └──────┬───────┘
                                              │
                                    ┌─────────┴─────────┐
                                    ▼                   ▼
                              ┌──────────┐        ┌──────────┐
                              │ Approve  │        │ Redirect │
                              │ → Execute│        │ → Replan │
                              └──────────┘        └──────────┘
```

> 💡 **Key Insight**
>
> Planning Mode is not just "slower execution." It is a fundamentally different workflow that gathers more context before acting. The extra file reading in the planning phase often catches dependencies and edge cases that direct execution would miss.

### When to Use Planning Mode

| Use Planning Mode | Use Direct Execution |
|-------------------|---------------------|
| Multi-file refactoring | Single-file edits |
| Architectural changes | Simple bug fixes |
| New feature implementation across modules | Adding a CSS class |
| Tasks where you are not sure of the scope | Tasks where you know exactly what to change |
| Unfamiliar codebases | Well-understood code |

---

## Thinking Modes (Extended Thinking)


![Thinking Modes Token Spectrum](../../visuals/thinking-modes-token-spectrum.svg)
*Figure: Thinking modes spectrum — from standard to ultrathink.*

Thinking modes give Claude more tokens to reason internally before responding. This is orthogonal to Planning Mode — they solve different problems.

### The Spectrum

| Mode | Reasoning Depth | Best For |
|------|----------------|----------|
| (default) | Standard | Most tasks |
| "Think" | Basic extended | Moderate complexity |
| "Think more" | Extended | Complex logic |
| "Think a lot" | Comprehensive | Multi-step algorithms |
| "Think longer" | Extended time | Deep analysis |
| "Ultrathink" | Maximum | Hardest problems, ambiguous requirements |

Each level gives Claude progressively more tokens for internal reasoning before generating a response.

> 🎬 **Instructor insight from the video**
>
> The instructor explains that thinking modes give Claude "more tokens to reason about the problem." He positions ultrathink as the maximum reasoning capability, useful when Claude is struggling with a particularly complex or ambiguous task. He also notes the cost trade-off: "both features consume additional tokens."

### How to Invoke

Simply include the thinking keyword in your prompt:

```
> Think about how to refactor the authentication module
> Think more about the edge cases in the payment flow
> Ultrathink about the database migration strategy
```

---

## Planning Mode vs Thinking Mode (Critical Exam Distinction)

This is one of the most important distinctions for the exam:

| Dimension | Planning Mode | Thinking Mode |
|-----------|--------------|---------------|
| **What it does** | Reads more files, creates an action plan | Reasons more deeply about the problem |
| **Type of complexity** | Breadth — many files, many components | Depth — complex logic, ambiguous requirements |
| **Output** | A plan you review before execution | A more thoroughly reasoned response |
| **Activation** | Shift+Tab (toggle) | Keyword in prompt ("think", "ultrathink") |
| **User interaction** | Review-approve cycle | No extra interaction needed |
| **Cost driver** | More file reads (tool calls) | More reasoning tokens |

```
Complexity Matrix:
                        Low Reasoning    High Reasoning
                        Complexity       Complexity
                    ┌─────────────────┬─────────────────┐
Low Codebase        │   Direct        │   Think /       │
Complexity          │   Execution     │   Ultrathink    │
                    ├─────────────────┼─────────────────┤
High Codebase       │   Planning      │   Planning +    │
Complexity          │   Mode          │   Thinking Mode │
                    └─────────────────┴─────────────────┘
```

> 💡 **Key Insight**
>
> You can combine both modes. For a task that requires understanding many files (breadth) AND solving a complex algorithm (depth), use Planning Mode with a "think" or "ultrathink" keyword. This gives Claude both broad context and deep reasoning.

---

## Iterative Refinement Workflow (Task 3.5 ★★★)

The full iterative workflow combines all three techniques:

1. **Initial request** — Describe what you want (text + optional screenshot)
2. **Claude implements** — Direct execution or via Planning Mode
3. **You review** — Check the result in browser/IDE
4. **Provide feedback** — Screenshot of result + description of what to change
5. **Claude refines** — Iterates based on your feedback
6. **Repeat** until satisfied

This is the agentic loop (Task 1.1) applied to real development. Each iteration narrows the gap between current state and desired state.

> ⚠️ **Cost Consideration**
>
> Both Planning Mode and Thinking Modes consume additional tokens. Planning Mode reads more files (tool call tokens). Thinking modes use more reasoning tokens. Use them when the task complexity justifies the cost, not as a default for every request.

---

## Familiar Analogies

| Concept | Analogy | Why It Fits |
|---------|---------|-------------|
| Direct execution | Asking a senior dev to fix a typo — just do it | Simple task, no planning needed |
| Planning Mode | Architecture review before a sprint — plan first, build second | Complex task needs upfront exploration |
| Thinking modes | Giving someone extra time on an exam question | More time = better reasoning on hard problems |
| Ultrathink | Whiteboard session for a hard design problem | Maximum reasoning resources for maximum complexity |
| Planning + Thinking | Sprint planning + design review combined | Breadth (scope) + depth (reasoning) together |
| Screenshot input | Pointing at a specific button and saying "change this" | Visual communication eliminates ambiguity |

---

## Exam Focus

| Exam Concept | What This Lesson Teaches |
|-------------|-------------------------|
| **Plan mode vs direct (3.4) ★★★** | Planning Mode for multi-file/complex tasks; direct for simple edits. Planning reads more files and creates a reviewable plan. |
| **Iterative refinement (3.5) ★★★** | The ask → implement → review → feedback → refine cycle. Screenshots accelerate communication. |
| **Agentic loops (1.1) ★** | Iterative refinement is the agentic loop in practice — gather context, plan, act, evaluate, repeat. |

Key distinctions the exam tests:

- **Planning Mode vs Thinking Mode** — Breadth vs depth. Planning reads more files; thinking reasons more deeply. They are complementary, not alternatives.
- **When to use Planning Mode** — Multi-file changes, unfamiliar codebases, architectural refactoring. NOT for simple single-file edits.
- **Extended thinking is not a prompt trick** — It is an architectural feature that allocates more reasoning tokens. The exam philosophy "Architecture > Prompt" applies.
- **Cost awareness** — Both features have token costs. Proportionate usage is key.

> 🎯 **Exam note**
>
> When the exam presents a scenario with "complex multi-file restructuring," the answer almost always involves Planning Mode. When the scenario involves "ambiguous requirements" or "complex algorithm," the answer involves Thinking Modes. When both are present, combine them.

---

## Practice Questions

### Q1: Mode Selection

A developer needs to rename a database column that is referenced across 15 files in a Node.js monorepo. Which approach is most appropriate?

- A. Direct execution — just ask Claude to rename it
- B. Planning Mode — let Claude explore the codebase, identify all references, and create a plan before making changes
- C. Ultrathink — ask Claude to reason deeply about the rename
- D. Start a new Claude session for each file that needs changes

<details><summary>Answer</summary>

**B** — This is a classic Planning Mode scenario: a change that affects many files requires broad codebase exploration first. Planning Mode will read the relevant files, identify all references, and present a comprehensive plan.

- A risks missing references in some files
- C solves the wrong problem — this needs breadth (many files), not depth (complex reasoning)
- D defeats the purpose of an agentic coding assistant

Exam philosophy: **Architecture > Prompt** — Planning Mode is a structural approach to handling multi-file complexity.
</details>

### Q2: Combining Modes

A developer is tasked with designing a new caching strategy that involves modifying the data access layer, the API routes, and the configuration system. The optimal caching algorithm depends on the specific access patterns in the codebase. Which approach is best?

- A. Direct execution with a detailed prompt
- B. Planning Mode only — it will figure out the algorithm
- C. Ultrathink only — it will figure out the file changes
- D. Planning Mode + ultrathink — Planning Mode for broad codebase understanding, ultrathink for reasoning about the optimal caching algorithm

<details><summary>Answer</summary>

**D** — This task has both breadth complexity (multiple components across the codebase) and depth complexity (choosing the optimal caching algorithm). Combining Planning Mode and thinking mode addresses both dimensions.

- A does not give Claude enough structure for this complexity
- B handles the breadth but may not reason deeply enough about the algorithm
- C handles the depth but may miss file dependencies

Exam philosophy: **Proportionate response** — use the right combination of tools for the specific complexity profile.
</details>

### Q3: Cost-Effective Usage

A junior developer has started using "ultrathink" for every request, including simple tasks like "add a console.log statement." Their token usage has increased 5x. What guidance do you give?

- A. Ultrathink is free, so let them continue
- B. Reserve thinking modes for tasks with genuine complexity — ambiguous requirements, complex algorithms, or difficult debugging. Simple tasks do not benefit from extra reasoning tokens.
- C. They should use Planning Mode instead of ultrathink for everything
- D. They should never use ultrathink — it is experimental

<details><summary>Answer</summary>

**B** — Thinking modes consume additional tokens. For simple tasks like adding a log statement, standard execution is sufficient. Ultrathink is for genuinely hard problems where more reasoning time produces better results.

- A is wrong — ultrathink costs more tokens
- C replaces one mismatch with another
- D is wrong — ultrathink is a legitimate feature for complex tasks

Exam philosophy: **Proportionate response** — match the tool's power to the task's complexity. Do not use a sledgehammer to hang a picture frame.
</details>

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Approach |
|-------------|-------------|-----------------|
| Using Planning Mode for every task | Wastes tokens on simple changes; slower than necessary | Use direct execution for simple, well-scoped changes |
| Using ultrathink for trivial tasks | Burns reasoning tokens without benefit | Reserve thinking modes for genuinely complex problems |
| Never using Planning Mode | Misses dependencies in multi-file changes | Enable Planning Mode when scope is unclear or spans multiple files |
| Describing UI changes in text only | Ambiguous — "the button on the left" could mean many things | Paste a screenshot and point to the specific element |
| Skipping the review step in Planning Mode | Defeats the purpose; might execute a flawed plan | Always review the plan before approving execution |
| Using Cmd+V instead of Ctrl+V for screenshots | Image will not paste into Claude Code | Use Ctrl+V specifically for screenshot pasting |
