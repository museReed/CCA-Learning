# Anthropic Apps — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) |
| Task Statements | 1.1 (Claude Code overview), 1.2 (agentic patterns), 1.4 (Computer Use as agent case study) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 73 |

---

## One-Liner

Claude Code and Computer Use are Anthropic's two flagship "agent" products — they are your reference point for the user experience, trust model, and value proposition you should aim for when building your own AI-powered workflows.

---

## Mental Model: The Intern Analogy

Think of the three surfaces as three different kinds of helper:

| Surface | Helper equivalent | What you can ask for |
|---------|-------------------|----------------------|
| Claude.ai | A bright friend you text | Quick answers, drafts, brainstorming |
| Anthropic API | A toolbox on a workbench | Parts you assemble into something of your own |
| **Claude Code** | An engineering intern at your keyboard | "Fix this bug, run the tests, open the PR" |
| **Computer Use** | A virtual operator driving a PC | "Log into the dashboard, export the report, email it" |

PM takeaway: Claude.ai is a product, the API is infrastructure, and Claude Code + Computer Use are *agent products* — they do work, not just answer questions.

---

## Why PMs Should Care

Most AI features today are chat interfaces. The interesting product category — and the one the industry is moving toward — is agents. Claude Code and Computer Use are the best studied examples of each major agent archetype:

| Archetype | Example | Works best when |
|-----------|---------|----------------|
| Domain-native agent | Claude Code (terminal, file tools) | Target domain has clean, typed tools |
| GUI-driving agent | Computer Use (desktop via screenshots) | Target domain has no API, only a UI |

When you are scoping an AI feature, you should first decide which archetype applies. A native agent is cheaper, faster, and more reliable. A GUI-driving agent unlocks things that no other approach can reach.

---

## Product Use Cases

### When to Build a Domain-Native Agent (Claude Code archetype)

| Scenario | Why the archetype fits |
|----------|------------------------|
| Developer tooling inside your IDE or CLI | Clean tool integrations exist (filesystem, git, language servers) |
| Data analyst assistant over a SQL database | You can expose typed tools for query, schema, metric catalog |
| Customer support operator over your ticketing API | First-class APIs give reliable, auditable actions |

### When to Build a GUI-Driving Agent (Computer Use archetype)

| Scenario | Why the archetype fits |
|----------|------------------------|
| Automating a legacy desktop app without an API | Only UI exists — agent must see and click |
| QA testing across third-party web apps | Visual regression + interaction flows |
| Enterprise RPA replacing brittle macro scripts | Agent adapts to layout changes using vision |

### When NOT to Use Either

| Scenario | Better alternative |
|----------|--------------------|
| Simple Q&A inside an app | Plain chat with the API, not an agent |
| Fixed deterministic flow with no ambiguity | A classic workflow / RPA script, no LLM |
| Real-time ultra-low-latency requirement | Deterministic code path — agent loops are too slow |

---

## PM Decision Framework

When you see a proposal for a new "AI feature," ask:

1. **Is it really an agent?** Does it need multi-step tool execution, environmental interaction, and autonomous decision-making? If not, it is a chat feature — lower risk, lower ceiling.
2. **Which archetype fits?** Native tools (Claude Code style) or GUI driving (Computer Use style)?
3. **What is the trust boundary?** Agents act on your behalf. Where does the human approve?
4. **What is the failure mode?** File corruption, wrong click, irreversible action — design safeguards before building.
5. **What does the reference implementation teach us?** Both apps ship with permission prompts, memory (CLAUDE.md), and iterative workflows — lift those patterns.

---

## The Trust and Control Tradeoff

Agents are powerful because they act. That same property makes them risky. Claude Code and Computer Use both illustrate the spectrum:

| Control level | Claude Code behavior | User experience |
|---------------|---------------------|-----------------|
| Read-only | Show a plan, ask permission | Safe, slow |
| Confirm per action | Ask before each file edit or shell command | Balanced |
| Auto-approve | Run a batch of changes autonomously | Fast, risky |

As a PM, your job is to pick a default and expose the right escape hatches. The course is clear: good agents are **collaborative partners**, not autonomous actors.

---

## Common PM Mistakes

1. **Pitching "an agent" without defining which archetype** — "native-tool agent" and "GUI-driving agent" have very different cost and reliability curves.
2. **Assuming Claude.ai UX translates to agents** — agents need planning surfaces, permission prompts, and recovery affordances that a chat UI does not.
3. **Ignoring the context problem** — Claude Code invests heavily in CLAUDE.md because context management is half the battle. Ad-hoc prompting does not scale.
4. **Treating Computer Use as a cheap workaround for missing APIs** — it works, but it is slower, more fragile, and costs more tokens. Build an API first if you can.
5. **Skipping the human approval step to feel "more autonomous"** — for anything destructive, approval is not optional.

> **Key Insight**
>
> Claude Code and Computer Use are not just products — they are **PM reference designs** for the two dominant agent archetypes: native-tool agents and GUI-driving agents. Study their UX choices (permission prompts, persistent memory files, plan-then-execute workflows) and you have a template for your own agent feature.

---

## CCA Exam Relevance

- **D1 (Agentic Coding & Architecture)**: Be ready to identify "is this an agent?" scenarios by mapping onto the four properties.
- **D3 (Claude Code Configuration)**: This lesson sets up the Claude Code-heavy section of the exam; know the app-category vocabulary.
- Questions often contrast chat, API, and agent — know which role each plays.

---

## Flashcards

| Front | Back |
|-------|------|
| What are Anthropic's two flagship agent applications? | Claude Code and Computer Use |
| In the intern analogy, what is Claude Code equivalent to? | An engineering intern sitting at your keyboard, doing the actual work |
| What are the two dominant agent archetypes from this lesson? | Domain-native agents (Claude Code style) and GUI-driving agents (Computer Use style) |
| When should a PM prefer a native-tool agent over a GUI-driving one? | Whenever the target domain has clean APIs or typed tools — it is cheaper and more reliable |
| When is a GUI-driving agent the right call? | When the target app has no API, only a UI (legacy desktop apps, third-party dashboards) |
| What is the trust tradeoff PMs must manage with agents? | Agents act on behalf of the user — you must choose between read-only, confirm-per-action, and auto-approve defaults |
| Why is CLAUDE.md relevant to PMs? | It is the product pattern for persistent context — a reminder that agent UX includes memory, not just prompts |
| Is Computer Use a replacement for building proper APIs? | No — it is a fallback when no API exists; it is slower, more fragile, and more expensive |
