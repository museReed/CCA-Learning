# Claude Code in Action — PM Strategic Overview

| Item | Detail |
|------|--------|
| Exam Domain | D2: Tool Design & MCP Integration (18%), D3: Claude Code Configuration & Workflows (20%) |
| Task Statements | 2.4 (MCP integration), 2.5 (built-in tools), 3.6 (CI/CD integration), 1.1 (agentic loops) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> 📝 All content in this section comes directly from official course materials.

## One-Liner / TL;DR

Claude Code delivers business value through autonomous multi-step task execution, extensible tooling via MCP, and automated quality gates in CI/CD — reducing engineering bottlenecks across performance, analysis, design, and compliance.

## Core Concepts

### Claude Code Is Extensible by Design

Claude is fundamentally an expert tool user. Claude Code ships with built-in tools for file I/O, execution, and search — but critically, it's designed to be **extensible**. New capabilities can be added through MCP servers without retraining or code changes.

### Built-in Tools — What PMs Need to Know

You don't need to provision special tooling for most tasks. Claude chains built-in tools intelligently:

| Capability | Business Impact |
|------------|----------------|
| File I/O (Read, Write, Edit) | Autonomous code changes without human handholding |
| Execution (Bash) | Run tests, benchmarks, builds automatically |
| Search (Grep, Glob) | Navigate large codebases to understand context |
| Notebooks (NotebookEdit) | Data analysis with execution, not just code generation |
| Web (WebFetch, WebSearch) | Research and verify against current information |

### Intelligent Tool Combination

What makes Claude Code truly powerful is how it **combines** these tools to tackle complex, multi-step problems. Think of it as a capable team member who can plan their own work, execute it, check results, and iterate — all without needing step-by-step instructions.

---

## 🎬 Demo Walkthrough: Performance Optimization — chalk Library

> Even widely-used infrastructure can have hidden performance gains — like finding a 3.9x efficiency improvement in a process your team uses daily.

**Business context**: chalk is the 5th most downloaded npm package (~429 million downloads/week). Performance optimization at this scale typically requires senior engineer time and is often deprioritized.

| Step | What Happens | Screenshot |
|------|-------------|------------|
| 1 | Instructor introduces chalk — 5th most downloaded npm package, fundamental infrastructure used across the ecosystem | ![chalk docs](../../visual-guide/frames/frame_016.jpg) |
| 2 | Shows the scale: 429 million downloads per week — improvements here ripple across the entire ecosystem | ![429M downloads](../../visual-guide/frames/frame_022.jpg) |
| 3 | Claude autonomously creates a todo list, runs benchmarks, and identifies the worst-performing cases | ![todo and benchmarks](../../visual-guide/frames/frame_027.jpg) |
| 4 | Claude writes targeted test files and uses CPU profiling to pinpoint the exact bottleneck | ![CPU profiling](../../visual-guide/frames/frame_030.jpg) |
| 5 | Claude implements the fix and verifies the improvement with benchmarks | ![3.9x improvement](../../visual-guide/frames/frame_032.jpg) |

**Result**: 🏆 **3.9x throughput improvement** — achieved autonomously without human intervention between steps.

**Business impact**:
- Senior engineer time freed from routine optimization work
- Performance improvements happen proactively, not reactively
- Measurable results (3.9x) with full audit trail

> 💡 **Why PMs Care**: Claude creates its own task list and tracks progress. This self-management capability means it handles complex multi-step work that would normally require task decomposition by a tech lead.

---

## 🎬 Demo Walkthrough: CSV Churn Analysis in Jupyter Notebook

> The difference between "write analysis code" and "write, execute, read results, refine" is the difference between a template and an actual insight.

**Business context**: Getting insights from data requires analysts or data scientists. When the data team is at capacity, product teams wait.

| Step | What Happens | Screenshot |
|------|-------------|------------|
| 1 | Instructor provides CSV of video streaming platform user data and asks Claude to analyze churn patterns | ![CSV dataset](../../visual-guide/frames/frame_037.jpg) |
| 2 | Claude writes analysis code, executes notebook cells, and reads the actual output | ![notebook execution](../../visual-guide/frames/frame_041.jpg) |
| 3 | Based on what it found, Claude customizes the next analysis step — iterating toward deeper insights | ![iterative analysis](../../visual-guide/frames/frame_044.jpg) |

**Result**: Complete churn analysis produced through iterative execution — not just code generation.

**Business impact**:
- Product teams get preliminary data insights without waiting for the data team
- Analysis quality is higher because Claude iterates based on actual results
- Reduces time-to-insight for product decisions

> 💡 **Why PMs Care**: Claude doesn't just generate code and hand it off. It executes, reads results, and adapts. This is the difference between getting a template and getting an actual answer.

---

## 🎬 Demo Walkthrough: UI Styling with Playwright MCP

> When stakeholders ask "can Claude do X?" the answer is often "yes, with the right MCP server." This is a capability you can plan around.

**Business context**: UI styling iterations create back-and-forth between developers and designers. Each cycle takes hours or days.

| Step | What Happens | Screenshot |
|------|-------------|------------|
| 1 | Instructor shows a UI generation app — the chat interface and header need styling work | ![unstyled UI](../../visual-guide/frames/frame_049.jpg) |
| 2 | Claude Code is given access to Playwright MCP server — browser control tools added via configuration | ![Playwright MCP](../../visual-guide/frames/frame_054.jpg) |
| 3 | Claude opens the browser, navigates to the app, takes a screenshot to assess current state | ![browser screenshot](../../visual-guide/frames/frame_058.jpg) |
| 4 | Claude updates styling, re-screenshots to verify, and iterates until the result is polished | ![improved styling](../../visual-guide/frames/frame_061.jpg) |

**Result**: Polished, professional interface achieved through visual feedback loops — in minutes, not hours.

**Business impact**:
- Faster design iteration cycles (minutes instead of hours)
- Developers handle styling refinements autonomously
- MCP extensibility means new capabilities without retraining — plan around it

> 💡 **Why PMs Care**: MCP is the extensibility story. New capabilities are added through configuration, not engineering work. This means you can scope Claude Code's capability growth into your roadmap.

---

## 🎬 Demo Walkthrough: GitHub PR Review — Catching PII Exposure

> Compliance risks caught before merge, not in production. Scales review capacity without hiring more senior engineers.

**Business context**: Manual code review misses cross-cutting concerns like PII exposure, especially in infrastructure-as-code where data flows span multiple files and resources.

**Scenario**: An AWS infrastructure with DynamoDB → Lambda → S3 bucket. The S3 bucket is shared with an external marketing partner. Months later, a developer adds user email to the Lambda export — forgetting the bucket is externally shared. This exposes PII to an external partner.

| Step | What Happens | Screenshot |
|------|-------------|------------|
| 1 | Claude Code runs in GitHub Actions — triggered automatically by PRs or `@claude` mentions | ![GitHub Actions](../../visual-guide/frames/frame_066.jpg) |
| 2 | AWS scenario: DynamoDB → Lambda → S3 bucket shared with external partner | ![AWS architecture](../../visual-guide/frames/frame_072.jpg) |
| 3 | Developer adds one line to Lambda — user email now flows to the shared S3 bucket | ![one-line change](../../visual-guide/frames/frame_083.jpg) |
| 4 | Pull request is created with the email addition | ![PR created](../../visual-guide/frames/frame_094.jpg) |
| 5 | Claude Code catches the PII exposure — traces the full data flow and explains the external partner risk | ![PII caught](../../visual-guide/frames/frame_098.jpg) |

**Result**: PII exposure caught before merge. Claude traces data from DynamoDB through Lambda to the shared S3 bucket — understanding infrastructure, not just scanning for keywords.

**Business impact**:
- Compliance risks caught pre-merge, not in production
- Scales review capacity without hiring more senior engineers
- Understands infrastructure context, not just code syntax
- Consistent review quality regardless of reviewer availability

> 🎯 **Critical for PMs**: Claude caught this not because someone wrote a rule saying "check for PII." It understood the Terraform infrastructure flow and recognized the risk. This is **Architecture > Prompt** — Claude reasons about systems structurally.

---

## Instructor Tips

1. **Claude self-manages complex tasks** — It creates todo lists and tracks progress, handling work that would normally require a tech lead to decompose
2. **Start with built-in tools** — No special setup needed for most tasks; add MCP only when genuinely needed
3. **Execute, don't just generate** — The execute-observe-refine loop produces dramatically better results
4. **MCP is configuration, not engineering** — Adding capabilities is a configuration change, not a development project
5. **CI/CD automation catches what humans miss** — Especially valuable for cross-file data flows and compliance

## Key Takeaways

1. 🔧 **Built-in tools handle most tasks** — No special provisioning needed to start getting value
2. 🤖 **Autonomous multi-step execution** — Claude plans, executes, observes, and refines without step-by-step guidance
3. 🔌 **MCP = planned extensibility** — New capabilities via configuration, scope it into your roadmap
4. 🏗️ **CI/CD integration delivers compliance value** — Automated review catches architectural risks, not just syntax errors
5. 📊 **Measurable results** — 3.9x performance improvement, PII caught pre-merge, faster iteration cycles

---

# PART 2: Study Aids

> 💡 Supplementary learning materials, not from official course.

## Familiar Analogies

- **Tool chaining = assembly line** — Each station (tool) does one thing well; the sequence creates the finished product. Claude is the floor manager who decides what goes where and in what order.
- **MCP = app store for Claude** — Built-in tools are the pre-installed apps. MCP servers are additional apps you install for specific needs (browser control, API access). No need to install everything — just what you need.
- **CI/CD review = automated quality inspection** — Like quality control checkpoints on a manufacturing line. Every PR passes through, issues are caught before they ship, and it scales without adding headcount.
- **Execute-observe-refine = scientific method** — Hypothesis (write code), experiment (execute), observe (read results), refine (adjust approach). Claude does data science the way data scientists actually work.

## CCA Exam Connection

> 🎯 This lesson demonstrates four business-relevant patterns:

| Pattern | Demo | Business Value | Task Statement |
|---------|------|---------------|----------------|
| Autonomous task management | Demo 1 (chalk, 429M downloads) | Reduces senior engineer bottleneck for performance work | 1.1: Agentic loops |
| Execute-observe-refine | Demo 2 (Jupyter churn analysis) | Data insights without data team dependency | 3.5: Iterative refinement |
| Planned extensibility via MCP | Demo 3 (Playwright browser) | New capabilities via configuration, not engineering | 2.4: MCP integration |
| Automated compliance review | Demo 4 (GitHub Actions, PII) | Pre-merge risk detection, scales without headcount | 3.6: CI/CD pipelines |

## Decision Framework for PMs

| Question | Guidance |
|----------|----------|
| "Do we need MCP servers?" | Start without them. Add only when built-in tools can't cover a specific need (e.g., browser testing, API integration) |
| "Where does Claude Code fit?" | CI/CD for automated review (Demo 4), developer productivity for ad-hoc tasks (Demos 1-3) |
| "How do we measure ROI?" | Time saved per task, issues caught pre-merge, reduction in specialist bottlenecks |
| "What's the adoption risk?" | Low for built-in tools (no setup). Medium for MCP (requires config). Low for CI/CD (standard GitHub Actions) |
| "What's the rollout order?" | Phase 1: Built-in tools → Phase 2: CI/CD review → Phase 3: MCP extensions |

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|-------------|---------------|-----------------|
| Over-provisioning MCP servers upfront | Adds setup cost before proving value with built-in tools | Start simple, extend when specific needs arise |
| Treating Claude as generate-only | Misses the execute-observe-refine advantage (Demo 2) | Enable execution environments (notebooks, bash) |
| Manual-only code review for compliance | Humans miss cross-file data flows, doesn't scale | Automate first-pass review in CI/CD (Demo 4) |
| Expecting keyword-based PII detection | Misses architectural risks (data flowing to shared resources) | Leverage Claude's infrastructure understanding |
| Waiting for data team for all analysis | Creates bottleneck for product decisions | Use Claude for preliminary analysis, data team for validation |

## Practice Questions

**Q1.** Your engineering team wants to adopt Claude Code. The CTO asks for a phased rollout plan. Based on the demos, what is the most effective ordering?

- A) MCP extensions first, then CI/CD, then built-in tools
- B) Built-in tools for developer productivity, then CI/CD for automated review, then MCP for specialized workflows
- C) CI/CD first for immediate compliance value, then everything else
- D) Full deployment of all capabilities simultaneously

> 📝 **Answer: B.** Phase 1: Built-in tools (zero setup, immediate value — Demos 1-2). Phase 2: CI/CD integration (GitHub Actions config, organization-wide compliance — Demo 4). Phase 3: MCP extensions (only when specific needs arise — Demo 3). This follows the proportionate response principle.

**Q2.** A security-conscious VP asks: "How can we ensure Claude Code catches PII exposure in our infrastructure?" What is the best response?

- A) "We'll write explicit rules for every PII field type"
- B) "Claude Code in CI/CD reads infrastructure-as-code and traces data flows — it caught PII exposure in the demo by understanding architecture, not by being told what to look for"
- C) "We'll need a custom MCP server for PII scanning"
- D) "Claude Code can't reliably catch PII — we need a dedicated tool"

> 📝 **Answer: B.** Claude Code understands Terraform infrastructure and traces data flows (DynamoDB → Lambda → shared S3 bucket). It caught user email exposure to an external partner without being explicitly told to check for PII. This is Architecture > Prompt — Claude reasons about systems structurally.

**Q3.** Your team spends 20 hours/week on code review. How would you frame Claude Code's CI/CD integration to justify the setup investment?

- A) "It will replace all human code review"
- B) "It augments human review — automated first-pass catches structural and compliance issues, humans focus on business logic and architecture"
- C) "It only catches PII issues, so limited value"
- D) "It requires significant engineering investment to set up"

> 📝 **Answer: B.** Claude Code handles first-pass review (structural issues, security, compliance). Human reviewers focus on business logic and architecture decisions. Expected: 30-50% reduction in review cycle time, near-zero compliance escapes, consistent quality. Setup cost: standard GitHub Actions workflow — a few hours of engineering time.

**Q4.** A product manager on another team asks: "Can Claude Code help us analyze our user churn data without waiting for the data team?" What do you tell them?

- A) "No, Claude Code is only for writing code"
- B) "Yes — Claude can write analysis code in a Jupyter notebook, execute it, read the actual results, and iterate. It's like having a preliminary data analyst, though the data team should validate critical findings"
- C) "Yes, but only if we set up a special MCP server for data analysis"
- D) "No, data analysis requires specialized models"

> 📝 **Answer: B.** Demo 2 showed exactly this: Claude analyzed churn data by writing code, executing cells, reading output, and refining its analysis. The execute-observe-refine loop produces real insights, not just code templates. Use for preliminary analysis; data team validates critical findings.
