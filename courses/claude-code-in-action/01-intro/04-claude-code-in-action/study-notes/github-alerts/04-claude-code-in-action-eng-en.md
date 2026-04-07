# Claude Code in Action — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%), D3 — Claude Code Configuration & Workflows (20%) |
| Task Statements | 2.5 (built-in tools), 2.4 (MCP integration), 3.6 (CI/CD), 1.1 (agentic loops) |
| Source | claude-code-in-action / 01-intro / Lesson 04 |

---


![Builtin Vs Mcp Decision Tree](../../visuals/builtin-vs-mcp-decision-tree.svg)
*Figure: Decision tree — built-in tools vs MCP servers.*

## One-Liner

Claude Code's power comes from intelligent tool chaining across built-in capabilities, easy extensibility via MCP servers, and seamless CI/CD integration — not from any single tool in isolation.

---

## Built-in Tools Overview

Claude Code ships with a default set of tools that cover file I/O, execution, and search:

| Tool | Purpose | Category |
|------|---------|----------|
| Read | Read file contents (supports images, PDFs, notebooks) | File I/O |
| Write | Create or overwrite files | File I/O |
| Edit | Make targeted, surgical edits to existing files | File I/O |
| Bash | Execute shell commands | Execution |
| Grep | Search file contents with regex (powered by ripgrep) | Search |
| Glob | Find files by name/pattern | Search |
| NotebookEdit | Edit Jupyter notebook cells | Notebook |
| WebFetch | Fetch and analyze web content | Web |
| WebSearch | Search the web for current information | Web |

> [!TIP]
> **Key Insight**
> The power isn't in any single tool — it's in how Claude chains them intelligently. Each demo in this lesson showcases a different chaining pattern.

---

## Demo 1: Performance Optimization — Intelligent Tool Chaining

**Context**: chalk is the 5th most downloaded npm package (~429M downloads/week). Even small performance improvements have massive ecosystem impact.

**What Claude did** (tool chain):
1. **Plan** — Created a structured todo list to track multi-step work
2. **Search** — Used Grep/Glob to find performance-relevant code paths
3. **Benchmark** — Ran existing benchmarks via Bash to establish baseline
4. **Focus** — Wrote a targeted test file isolating the hot path
5. **Profile** — Ran CPU profiler via Bash, Read the output
6. **Fix** — Used Edit to implement the optimization
7. **Verify** — Re-ran benchmarks to confirm improvement

**Result**: 3.9x throughput improvement on the targeted operation.

> [!NOTE]
> **Instructor Insight**
> Claude builds a todo list to track its own progress through complex tasks. This self-management behavior emerges naturally — it's how agentic loops maintain coherence across many steps.

> [!IMPORTANT]
> **Exam Note**
> This is the canonical example of Task 1.1 (agentic loops): Claude autonomously plans, executes, observes, and refines without human intervention between steps.

---

## Demo 2: Data Analysis — Execute and Iterate

**Context**: CSV dataset of video streaming platform users. Goal: analyze user churn patterns.

**What Claude did**:
1. Read the CSV to understand schema
2. Wrote analysis code in Jupyter notebook cells
3. **Executed cells and read the output** — this is the critical differentiator
4. Based on actual results, customized the next analysis step
5. Iteratively refined visualizations and statistical tests

> [!TIP]
> **Key Insight**
> Claude doesn't just generate code and hope it works. It executes cells, observes results, and adapts. This execute-observe-refine loop produces dramatically better analysis than generate-only approaches.

**Why this matters for the exam**: This demonstrates Task 3.5 (iterative refinement). The quality difference between "write code" and "write code, run it, read output, adjust" is substantial.

---

## Demo 3: MCP Extensibility — Playwright Browser Control

**Context**: A small app that generates UI components from text descriptions. Claude needs to style the output visually.

**What Claude did**:
1. Was given access to Playwright MCP server (browser control tools)
2. Opened the browser, took a screenshot to see current state
3. Made CSS/style changes via Edit
4. Re-screenshotted to verify visual result
5. Iterated until the styling matched expectations

**Key technical points**:
- MCP tools are added via configuration — no retraining needed
- Claude adapts to new tools based on their descriptions alone
- Tool description quality determines how effectively Claude uses the tool

> [!TIP]
> **Exam Connection**
> This demonstrates Task 2.4: Integrate MCP servers into Claude Code and agent workflows. The exam philosophy here is **Tool description > Few-shot** — clear, well-written tool descriptions matter more than examples.

---

## Demo 4: CI/CD Integration — Automated PR Security Review

**Context**: Claude Code runs inside GitHub Actions, triggered by PR creation or `@claude` mentions in PR comments.

**Scenario**:
- AWS infrastructure defined in Terraform
- Architecture: DynamoDB table -> Lambda function -> S3 bucket
- The S3 bucket is shared with an external partner
- A PR adds user email to the data flow
- Adding PII (email) to a bucket shared externally = **security/compliance risk**

**What Claude caught**: The PII exposure risk — not because it was told "check for PII," but because it understood the Terraform infrastructure flow and recognized that user email would end up in the shared S3 bucket.

> [!IMPORTANT]
> **Exam Note**
> This maps directly to Task 3.6 (CI/CD integration) and embodies the exam philosophy: **Architecture > Prompt**. Claude catches issues by understanding infrastructure code structurally, not by being told what to look for.

---

## Tool Chaining Patterns (Exam-Relevant)


![Tool Chaining Patterns Matrix](../../visuals/tool-chaining-patterns-matrix.svg)
*Figure: Tool chaining patterns across four demo use cases.*


![Tool Chain Pattern](../../visuals/tool-chain-pattern.svg)
*Figure: Three tool chaining patterns demonstrated in Claude Code.*

| Pattern | Example from Demos | Task Statement | When to Apply |
|---------|-------------------|----------------|---------------|
| Plan -> Execute -> Verify | chalk optimization (D1) | 1.1: Agentic loops | Complex multi-step tasks |
| Execute -> Observe -> Refine | Jupyter analysis (D2) | 3.5: Iterative refinement | Data analysis, debugging |
| New tool adoption via MCP | Playwright browser (D3) | 2.4: MCP integration | When built-in tools insufficient |
| Automated review in CI | GitHub PR review (D4) | 3.6: CI/CD pipelines | Code review, compliance |
| Proportionate tool selection | All demos | 2.5: Built-in tools | Start simple, extend when needed |

> [!TIP]
> **Exam Philosophy: Proportionate Response**
> Start with built-in tools. Only add MCP servers or custom tooling when built-in capabilities are genuinely insufficient. The exam tests whether you know WHEN to extend, not just HOW.

---

## Key Takeaways for the Exam

1. **Built-in tools are powerful** — most tasks don't need MCP extensions
2. **Tool chaining is the multiplier** — the sequence matters more than individual tools
3. **MCP extends, doesn't replace** — MCP servers add capabilities (browser, APIs) that built-in tools can't cover
4. **CI/CD integration is a first-class use case** — Claude Code in GitHub Actions for automated review
5. **Architecture understanding > explicit instructions** — Claude reasons about code structure, not just syntax

---

## Practice Questions

### Q1: CI/CD Security Review
Your team uses Terraform to manage AWS infrastructure. A junior developer submits a PR that adds a `user_phone` field to a Lambda function that writes to an S3 bucket shared with a third-party analytics partner. How should you configure Claude Code to catch this?

<details><summary>Answer</summary>

Configure Claude Code as a GitHub Actions workflow triggered on PR creation. Claude will read the Terraform files, understand the data flow (Lambda -> shared S3 bucket), and flag that `user_phone` is PII being sent to an external partner. The key insight is that you do NOT need to write a prompt saying "check for PII" — Claude understands infrastructure-as-code and can trace data flows. This is Architecture > Prompt in action (Task 3.6).
</details>

### Q2: Tool Selection
You need Claude Code to optimize a Python function's performance. Which sequence of built-in tools represents the best approach?

A) Edit the code directly with a known optimization pattern
B) Read the code -> Bash (run profiler) -> Read profiler output -> Edit (apply fix) -> Bash (re-run benchmark)
C) Write a completely new implementation from scratch
D) Grep for similar optimizations in the codebase and copy them

<details><summary>Answer</summary>

**B**. This follows the Plan -> Profile -> Fix -> Verify pattern from Demo 1. The key is that Claude should measure before optimizing (run profiler), then verify the improvement (re-run benchmark). Option A skips measurement. Option C is disproportionate. Option D doesn't address the specific bottleneck. This tests Task 2.5 (effective built-in tool use) and Task 1.1 (agentic loop design).
</details>

### Q3: MCP Extensibility
You want Claude Code to verify that your web application's login page renders correctly after CSS changes. Which approach is most appropriate?

A) Have Claude Read the CSS file and reason about visual appearance
B) Add a Playwright MCP server so Claude can screenshot and visually verify
C) Write unit tests for every CSS property
D) Use Bash to run a headless browser and save screenshots for manual review

<details><summary>Answer</summary>

**B**. This matches Demo 3 exactly. Playwright MCP gives Claude the ability to open a browser, take screenshots, and visually verify the result — creating a tight feedback loop. Option A can't verify visual rendering. Option C is brittle and doesn't test visual appearance. Option D requires manual review, losing the automation benefit. This tests Task 2.4 (MCP integration) and the principle that MCP extends Claude's capabilities when built-in tools are insufficient.
</details>
