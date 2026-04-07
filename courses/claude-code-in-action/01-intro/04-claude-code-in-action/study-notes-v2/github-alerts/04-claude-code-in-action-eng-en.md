# Claude Code in Action — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2: Tool Design & MCP Integration (18%), D3: Claude Code Configuration & Workflows (20%) |
| Task Statements | 2.4 (MCP integration), 2.5 (built-in tools), 3.6 (CI/CD integration), 1.1 (agentic loops) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> [!NOTE]
> All content in this section comes directly from official course materials.

## One-Liner / TL;DR

Claude Code's power comes from intelligently chaining built-in tools, extending capabilities via MCP servers, and integrating into CI/CD pipelines — not from any single tool in isolation.

## Core Concepts

### Claude Is Expert at Tool Use

The course emphasizes that Claude is fundamentally an expert tool user. Claude Code is designed to be **extensible** — beyond its built-in tools, you can add new capabilities through MCP servers and custom integrations.

### Built-in Tools

Claude Code ships with a default set of tools for file I/O, execution, and search:

| Tool | Purpose |
|------|---------|
| Read | Read file contents (supports images, PDFs, notebooks) |
| Write | Create or overwrite files |
| Edit | Make targeted, surgical edits to existing files |
| Bash | Execute shell commands |
| Grep | Search file contents with regex (powered by ripgrep) |
| Glob | Find files by name/pattern |
| NotebookEdit | Edit Jupyter notebook cells |
| WebFetch | Fetch and analyze web content |
| WebSearch | Search the web for current information |

### Intelligent Tool Combination

What makes Claude Code truly powerful is how it **combines** these tools to tackle complex, multi-step problems. Each demo in this lesson showcases a different chaining pattern — from profiling and benchmarking to executing notebook cells and controlling browsers.

---

## Demo Walkthrough: Performance Optimization — chalk Library

> [!NOTE]
> Walkthrough of instructor demonstration. Screenshots from actual course video.

**Context**: chalk is the 5th most downloaded npm package with ~429 million downloads per week. Even small performance improvements have massive ecosystem impact.

| Step | What Happens | Screenshot |
|------|-------------|------------|
| 1 | Instructor introduces chalk — 5th most downloaded npm package, used for colored terminal text | ![chalk docs](../../visual-guide/frames/frame_016.jpg) |
| 2 | Shows download stats: 429 million downloads/week | ![429M downloads](../../visual-guide/frames/frame_022.jpg) |
| 3 | Asks Claude to find and optimize performance. Claude creates a todo list to track progress, then runs benchmarks to identify worst-performing cases | ![todo and benchmarks](../../visual-guide/frames/frame_027.jpg) |
| 4 | Claude writes a file to zoom in on one case, then uses CPU profiler to understand why it's slow | ![CPU profiling](../../visual-guide/frames/frame_030.jpg) |
| 5 | Claude implements the optimization and verifies the result | ![3.9x improvement](../../visual-guide/frames/frame_032.jpg) |

**Result**: **3.9x throughput improvement** on the targeted operation.

> [!TIP]
> Claude builds its own todo list and tracks progress through complex tasks. This self-management behavior is how agentic loops maintain coherence across many steps — Plan, Execute, Observe, Refine.

---

## Demo Walkthrough: CSV Churn Analysis in Jupyter Notebook

> [!NOTE]
> Claude doesn't just write code — it executes, reads results, and adapts.

**Context**: CSV dataset of video streaming platform users. Goal: analyze user churn patterns.

| Step | What Happens | Screenshot |
|------|-------------|------------|
| 1 | Instructor provides CSV file with video streaming platform user data, asks Claude to analyze churn in a Jupyter notebook | ![CSV dataset](../../visual-guide/frames/frame_037.jpg) |
| 2 | Claude writes analysis code into notebook cells, executes them, and views the output | ![notebook execution](../../visual-guide/frames/frame_041.jpg) |
| 3 | Claude customizes successive cells based on previous execution results — iterating toward deeper insights | ![iterative analysis](../../visual-guide/frames/frame_044.jpg) |

**Result**: Claude produces a complete churn analysis by executing, observing, and refining — not just generating code.

> [!TIP]
> The critical differentiator is the execute-observe-refine loop. Claude runs cells, reads actual output, then decides what to analyze next. This produces dramatically better analysis than generate-only approaches.

---

## Demo Walkthrough: UI Styling with Playwright MCP

> [!NOTE]
> Demonstrates how MCP servers extend Claude Code's capabilities beyond built-in tools.

**Context**: A UI generation app with a chat interface and header that need styling fixes.

| Step | What Happens | Screenshot |
|------|-------------|------------|
| 1 | Instructor shows the UI app — chat interface and header look unstyled and rough | ![unstyled UI](../../visual-guide/frames/frame_049.jpg) |
| 2 | Gives Claude Code access to Playwright MCP server — adding browser control tools | ![Playwright MCP](../../visual-guide/frames/frame_054.jpg) |
| 3 | Claude opens the browser, navigates to the app, takes a screenshot to see current state | ![browser screenshot](../../visual-guide/frames/frame_058.jpg) |
| 4 | Claude updates styling, takes another screenshot, and iterates until the result looks polished | ![improved styling](../../visual-guide/frames/frame_061.jpg) |

**Result**: A polished, professional-looking interface achieved through visual feedback loops.

> [!TIP]
> MCP tools are added via configuration — no retraining or code changes needed. Claude adapts to new tools based on their descriptions alone. This is the extensibility story: when built-in tools aren't enough, MCP fills the gap.

---

## Demo Walkthrough: GitHub PR Review — Catching PII Exposure

> [!IMPORTANT]
> The longest demo in the lesson. Shows Claude Code running in CI/CD to catch security issues that human reviewers miss.

**Context**: Claude Code runs inside GitHub Actions, triggered by PR creation or `@claude` mentions in comments.

**Scenario setup**:
- AWS infrastructure: **DynamoDB** table → **Lambda** function → **S3 bucket**
- The S3 bucket is shared with an **external marketing partner**
- Months later, internal team requests adding user email to the export
- Developer adds one line to the Lambda function — forgets the bucket is shared externally
- This exposes **PII (user email)** to an external partner — a serious security/compliance risk

| Step | What Happens | Screenshot |
|------|-------------|------------|
| 1 | Instructor explains Claude Code can run in GitHub Actions — triggered by PRs or `@claude` mentions | ![GitHub Actions integration](../../visual-guide/frames/frame_066.jpg) |
| 2 | Sets up the AWS scenario: DynamoDB → Lambda → S3 bucket shared with external partner | ![AWS architecture](../../visual-guide/frames/frame_072.jpg) |
| 3 | Developer adds one line — user email now included in Lambda export to shared S3 bucket | ![one-line change](../../visual-guide/frames/frame_083.jpg) |
| 4 | Pull request is created with the email addition change | ![PR created](../../visual-guide/frames/frame_094.jpg) |
| 5 | Claude Code automated review catches the PII exposure — shows exact data flow and explains the external partner risk | ![PII review caught](../../visual-guide/frames/frame_098.jpg) |

**Result**: Claude catches PII exposure by understanding the infrastructure flow — not because it was told "check for PII," but because it traced the data from DynamoDB through Lambda to the shared S3 bucket.

> [!WARNING]
> This maps directly to Task 3.6 (CI/CD integration). Claude understands infrastructure-as-code structurally, catching issues that rule-based scanners would miss. This embodies the **Architecture > Prompt** philosophy.

---

## Instructor Tips

1. **Self-management via todo lists** — Claude creates structured task lists for complex work, tracking its own progress without being asked
2. **Start with built-in tools** — Most tasks don't need MCP extensions; add them only when built-in capabilities are genuinely insufficient
3. **Execute, don't just generate** — The quality difference between "write code" and "write, run, read output, adjust" is substantial
4. **MCP is configuration, not code** — Adding new tool capabilities requires configuration changes, not retraining
5. **CI/CD catches what humans miss** — Automated review understands cross-file data flows that are easy to overlook in manual review

## Key Takeaways

1. **Built-in tools are powerful** — Read, Write, Edit, Bash, Grep, Glob cover most development tasks
2. **Tool chaining is the multiplier** — The sequence and combination matter more than individual tools
3. **MCP extends, doesn't replace** — MCP servers add capabilities (browser, APIs) that built-in tools can't cover
4. **CI/CD integration is first-class** — Claude Code in GitHub Actions for automated review is a production use case
5. **Architecture understanding > explicit instructions** — Claude reasons about code structure, data flows, and infrastructure

---

# PART 2: Study Aids

> [!NOTE]
> Supplementary learning materials, not from official course.

## Familiar Analogies

- **Tool chaining = Unix pipes** — Just like `cat file | grep pattern | sort | uniq`, Claude chains Read → Bash (profile) → Edit (fix) → Bash (verify). Each tool does one thing well; the chain creates the value.
- **MCP = USB ports** — Your laptop has built-in capabilities (screen, keyboard). USB ports let you plug in new devices (camera, external drive). MCP servers are Claude Code's USB ports — plug in browser control, API access, database tools as needed.
- **Claude's todo list = senior engineer's scratch pad** — When a senior engineer tackles a complex problem, they write down steps first. Claude does the same, but in a structured format it can track and check off.
- **CI/CD review = airport security X-ray** — It scans everything going through (every PR), catches things humans might miss (PII in data flows), and doesn't get tired or distracted.

## CCA Exam Connection

> [!TIP]
> This lesson covers **four exam-relevant patterns** across three domains:

| Pattern | Demo | Task Statement | Exam Relevance |
|---------|------|----------------|----------------|
| Plan → Execute → Verify | Demo 1 (chalk) | 1.1: Agentic loops | How Claude autonomously manages multi-step tasks |
| Execute → Observe → Refine | Demo 2 (Jupyter) | 3.5: Iterative refinement | Quality difference between generate-only and execute-iterate |
| MCP tool adoption | Demo 3 (Playwright) | 2.4: MCP integration | When and how to extend Claude Code's capabilities |
| Automated CI/CD review | Demo 4 (GitHub Actions) | 3.6: CI/CD pipelines | Infrastructure-aware automated review |

> [!TIP]
> **Exam Philosophy: Proportionate Response** — Start with built-in tools. Only add MCP or custom tooling when built-in capabilities are genuinely insufficient. The exam tests whether you know WHEN to extend, not just HOW.

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|-------------|---------------|-----------------|
| Adding MCP servers before trying built-in tools | Over-engineering; built-in tools handle most tasks | Start with Read/Write/Edit/Bash/Grep, extend only when needed |
| Writing code without executing it | Generate-only approach misses runtime errors and data-dependent issues | Execute, observe output, refine (Demo 2 pattern) |
| Relying solely on manual PR review for security | Humans miss cross-file data flow issues, especially in infra-as-code | Automate first-pass review with Claude Code in CI/CD (Demo 4) |
| Expecting Claude to catch issues via keyword matching | Rule-based scanning misses architectural concerns | Claude understands infrastructure structurally — Architecture > Prompt |
| Giving Claude a single monolithic prompt for complex tasks | Overwhelms context, reduces quality | Let Claude decompose into steps with its own todo list (Demo 1) |

## Practice Questions

**Q1.** Your team uses Terraform to manage AWS infrastructure. A developer submits a PR that adds `user_phone` to a Lambda function writing to an S3 bucket shared with a third-party analytics partner. How should Claude Code be configured to catch this?

- A) Add a regex rule to scan for PII field names in PRs
- B) Configure Claude Code as a GitHub Actions workflow triggered on PR creation
- C) Write a custom MCP server that scans for PII patterns
- D) Add a CLAUDE.md instruction listing all PII fields to watch for

> [!NOTE]
> **Answer: B.** Configure Claude Code in GitHub Actions (Task 3.6). Claude reads Terraform files, traces the data flow (Lambda → shared S3 bucket), and flags PII exposure to the external partner. No explicit "check for PII" prompt is needed — Claude understands infrastructure structurally. This is Architecture > Prompt in action.

**Q2.** You need Claude Code to optimize a Python function's performance. Which tool sequence represents the best approach?

- A) Edit the code directly with a known optimization pattern
- B) Read → Bash (run profiler) → Read profiler output → Edit (apply fix) → Bash (re-run benchmark)
- C) Write a completely new implementation from scratch
- D) Grep for similar optimizations in the codebase and copy them

> [!NOTE]
> **Answer: B.** This follows Demo 1's Plan → Profile → Fix → Verify pattern. Claude should measure before optimizing, then verify the improvement. Option A skips measurement. Option C is disproportionate. Option D doesn't address the specific bottleneck. Tests Task 2.5 (built-in tools) and 1.1 (agentic loops).

**Q3.** You want Claude Code to verify that your web app's login page renders correctly after CSS changes. Which approach is most appropriate?

- A) Have Claude Read the CSS file and reason about visual appearance
- B) Add a Playwright MCP server so Claude can screenshot and visually verify
- C) Write unit tests for every CSS property
- D) Use Bash to run a headless browser and save screenshots for manual review

> [!NOTE]
> **Answer: B.** Matches Demo 3. Playwright MCP gives Claude browser control to screenshot and visually verify — creating a tight feedback loop. Option A can't verify visual rendering. Option C is brittle. Option D requires manual review. Tests Task 2.4 (MCP integration).

**Q4.** What distinguishes Claude Code's Jupyter notebook analysis (Demo 2) from a standard code-generation approach?

- A) Claude uses a specialized data science model
- B) Claude writes code, executes cells, reads actual output, and customizes the next step based on results
- C) Claude has access to pre-built analysis templates
- D) Claude connects directly to the data source via API

> [!NOTE]
> **Answer: B.** The execute-observe-refine loop is the critical differentiator. Claude doesn't just generate code — it runs cells, reads results, and adapts its analysis. This produces dramatically better insights than generate-only approaches. Tests Task 3.5 (iterative refinement).
