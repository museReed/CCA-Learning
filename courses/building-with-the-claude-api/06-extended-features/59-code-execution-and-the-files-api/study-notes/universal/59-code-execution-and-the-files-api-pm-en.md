# Code Execution and the Files API — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.4 (server-side tools), 2.1 (tool schema design) |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 59 |

---

## One-Liner

Together, the Files API and the Code Execution tool let your product ship "hand it to Claude" features — users upload a file, ask a question in plain English, and get back an analysis complete with plots — without your team having to build a data pipeline, a sandbox, or a chart renderer.

---

## Why PMs Should Care

Before this feature, shipping "upload a CSV and get an analysis" meant owning a whole pipeline: file storage, a sandboxed runtime, a charting library, a results UI, and an engineer on call when any of those broke. Code Execution collapses that into **declare a server-side tool, wire the Files API for uploads and downloads**. The analysis work, the plot generation, the iteration — all handled by Claude inside a sandbox Anthropic operates.

This is the "delegate computation to Claude" pattern, and it unlocks product features that would otherwise take quarters to build: data analysis, image manipulation, document transformation, mathematical modeling. If your roadmap has any "upload X and get Y" feature, this lesson is the shortest path to shipping it.

---

## Mental Model: A Trustworthy Contractor's Closed Workshop

Think of Code Execution as hiring a contractor who works inside a locked workshop:

| Contractor analogy | API mechanic |
|--------------------|--------------|
| You hand the contractor raw materials at the workshop door | You upload files via the Files API and pass them to the sandbox via `container_upload` |
| The workshop has no phone or internet — no outside distractions | The Docker container has no network access — safe, isolated |
| The contractor can build and iterate inside, trying different approaches | Claude can run Python multiple times in one response |
| You collect finished products at the door | You download generated files via the Files API |
| You do not need to supply tools — the contractor brings them | Code Execution is a server-side tool, no client implementation |

The closed workshop is not a limitation — it is the *reason* you can trust giving Claude a real runtime.

---

## Product Use Cases

### High-Value Patterns the Lesson Highlights

| Use case | What the user does | What Claude does |
|----------|-------------------|------------------|
| Data analysis (churn, sales, experiments) | Upload CSV, ask a natural-language question | Cleans, analyzes, plots, summarizes |
| Image processing | Upload image, describe the transformation | Runs image libs inside the container, returns processed image |
| Document parsing and transformation | Upload PDF, request a format or redaction | Extracts, transforms, re-emits the document |
| Mathematical modeling | Describe the problem, upload parameters | Builds and runs the model, returns plots and numbers |
| Custom report generation | Upload raw data, describe the report layout | Generates formatted HTML/PDF output |

### Where the Pattern Does NOT Fit

| Scenario | Why not |
|----------|---------|
| Features that need live external APIs | The sandbox has no network access. |
| Features that need persistent state across sessions | The container is ephemeral — state must go through the Files API. |
| Tiny one-off computations a user could do in a spreadsheet | The overhead is not worth it; Claude's native reasoning is cheaper. |
| High-security data that cannot leave your infra | The sandbox is Anthropic-hosted — run through your compliance review. |

---

## PM Decision Framework

When scoping a "Claude does the computation" feature:

| Question | Why it matters |
|----------|---------------|
| Does the feature need to crunch, plot, parse, or transform data? | If yes, code execution probably fits. |
| Is the input a file (CSV, PDF, image)? | If yes, the Files API is the natural upload path. |
| Does the output include generated artifacts (plots, reports)? | If yes, wire the download path via `code_execution_output` blocks. |
| Does the feature need external network access? | If yes, this tool does not fit — sandbox has no network. |
| Is the compute workload bounded (seconds to minutes)? | Expected for iterative analysis; plan UX around streaming or progress indicators. |
| Are there compliance concerns with files leaving your infra? | Review before shipping. |

If the first three are yes and the next three have acceptable answers, code execution is a strong product bet.

---

## User Experience Implications

Code execution changes what a "simple feature" can accomplish. A single prompt can produce:

- An analysis with multiple chart outputs.
- Multi-step reasoning (load → inspect → clean → plot → summarize) narrated by Claude.
- Iterated refinement without extra user effort.

For users, this feels like having a junior data analyst on call. For the product, it means you can promise results that used to require a services team or a complex UI — delivered through a single text box and a file upload.

---

## Common PM Mistakes

1. **Promising live-data analysis** — the sandbox has no network, so "get the latest stock data and graph it" will not work out of the box. Fetch the data in your own code first, upload the result, then invoke code execution.
2. **Building a custom pipeline instead** — teams often under-estimate what code execution delivers and build a homegrown sandbox that is slower, less reliable, and more expensive to maintain.
3. **Forgetting to expose generated artifacts** — if your UI never surfaces the files Claude produced, users see only text explanations and feel short-changed. Render the `code_execution_output` files in the UI.
4. **Underestimating iteration** — Claude may run code three or five times in a single response. UX and logs should handle that, not assume a single execution.
5. **Skipping compliance review** — any time files leave your infra, legal and security should weigh in. Do not ship without this step for enterprise customers.
6. **Not pairing with the Files API upfront** — code execution without the Files API is like a workshop with no delivery door. Plan both at the same time.

---

> **Key Insight**
>
> Code Execution + Files API is a **product shortcut**: it turns "we need to build a sandboxed computation pipeline" into "we need to declare a tool and wire a file upload/download." For any roadmap item of the form "user uploads X, we analyze and return Y," this pairing collapses months of engineering into a single sprint.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)** — know the distinction: server-side tools (like code execution) require no client implementation, whereas client-side tools do. Exam scenarios often ask when you need to implement a tool yourself vs. when Claude runs it on the server.
- Know the sandbox characteristics: isolated Docker container, no network access, Python.
- Know the Files API is how you get data in (`container_upload`) and out (`download_file(file_id)`).
- Expect scenarios framed as "delegate a computational task to Claude" where the right answer is the Code Execution + Files API pattern.

---

## Flashcards

| Front | Back |
|-------|------|
| What kind of product features does Code Execution + Files API unlock? | Features where users upload a file and ask in plain English for analysis, transformation, or report generation — without your team building a sandbox or pipeline. |
| What does the Files API do for a product? | It provides an upload-once, reference-by-ID pattern for files, and it serves as the in/out bridge for the Code Execution sandbox. |
| Is Code Execution a server-side or client-side tool? | Server-side — no client implementation; Claude runs Python for you in an isolated container. |
| Why does the sandbox have no network access? | It is an isolation/security feature — the container cannot make external API calls, which keeps the execution environment safe. |
| Name a feature this pattern is NOT suitable for. | Anything that requires live external API access (the sandbox has no network), or anything needing persistent state across sessions. |
| What mental model captures this pattern well? | A trustworthy contractor in a locked, offline workshop — you hand them materials at the door, they work inside, you collect the finished product at the door. |
| Why should a PM not build a custom sandbox instead? | Because the server-side tool collapses months of work into a tool declaration plus Files API wiring, and the team avoids maintaining a bespoke runtime. |
| What block type delivers a generated file back to you? | A `code_execution_output` block containing a file ID, which you then retrieve via the Files API. |
