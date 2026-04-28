# Welcome to the Course — PM Quick-Scan

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding Fundamentals (22%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 1.1 (foundational understanding of Claude capabilities), 5.1 (model selection and deployment readiness) |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 02 |

---

## One-Liner

This orientation lesson lays out the course roadmap — from API basics through agentic workflows — giving PMs a clear view of every Claude capability they will need to scope, prioritize, and ship AI-powered features.

---

## The Product Capability Map

Think of each course module as a capability your product team can unlock:

| Module | Capability for Your Product | PM Decision |
|--------|----------------------------|-------------|
| API Fundamentals | Basic AI text generation | "Can we call Claude at all?" — table stakes |
| Prompt Evaluation | Quality assurance for AI outputs | "How do we know the AI is working?" — the most important module |
| Prompt Engineering | Controlling AI tone, format, accuracy | "How do we make the AI do what we want?" |
| Tool Use | Claude calling external functions | "Can Claude look up data, book flights, etc.?" |
| RAG | Grounding AI in your company's documents | "Can Claude answer questions about our product?" |
| MCP | Standardized integrations with external services | "How do we connect Claude to Slack, databases, etc.?" |
| Claude Code / Computer Use | AI that operates software autonomously | "Can AI write code or browse the web for us?" |
| Workflows & Agents | Multi-step AI processes | "Can we automate entire workflows, not just single queries?" |

---

## Why PMs Should Care About This Roadmap

The course follows a deliberate dependency chain. This matters for product planning because:

1. **You cannot ship agents without tool use** — if your roadmap puts "AI agent" in Q1 but "tool integration" in Q2, the plan is broken.
2. **Prompt evaluation gates quality** — the instructor calls it the single most important practice. PMs who skip eval planning get AI features that demo well but fail in production.
3. **RAG unlocks enterprise value** — most enterprise deals require the AI to know about the customer's data. RAG is where that happens.

---

## PM Decision Framework

| Question to Ask Your Team | Why It Matters |
|---------------------------|---------------|
| Do we have API access and keys set up? | Blocked on this = zero engineering velocity |
| Have we planned prompt evaluation before launch? | No eval = no quality guarantee; the instructor stresses this above all else |
| Which module maps to our next feature? | Prioritize learning the module your roadmap needs first |
| Are we building tools or agents? | Tools are deterministic and testable; agents are flexible but harder to evaluate |
| Do we need RAG for our use case? | If users ask questions about proprietary data, the answer is yes |

---

## Common PM Mistakes

1. **Planning AI agents without understanding prerequisites** — agents require prompt engineering + tool use + evaluation. Skipping any of these leads to unreliable features.
2. **Treating prompt engineering as "engineering's problem"** — prompt design decisions are product decisions (tone, format, accuracy targets).
3. **Ignoring prompt evaluation** — the instructor explicitly says: if you deploy without evaluation, your users will not get the results you expect.
4. **Scoping too many capabilities at once** — the dependency chain means you should ship API basics before tools, tools before agents.
5. **Not budgeting for iteration** — the course emphasizes expanding, altering, and breaking notebooks. Your sprint plan needs room for prompt iteration.

> **Key Insight**
>
> This roadmap is not just a course outline — it is a product maturity model for AI features. Companies progress through these stages: basic API calls, then evaluation, then prompt engineering, then tool use, then RAG, then MCP, then agents. Trying to skip stages is how AI features fail in production.

---

## CCA Exam Relevance

- **D1 (Agentic Coding Fundamentals)**: the course arc maps directly to the CCA skill progression — exam questions assume familiarity with every module.
- **D5 (Enterprise Deployment)**: prerequisites (API key setup, environment readiness) are enterprise deployment basics.
- The exam expects you to understand the dependency chain: you cannot answer agent questions without understanding tool use fundamentals.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the course module dependency chain? | API → Prompt Eval → Prompt Engineering → Tool Use → RAG → MCP → Claude Code → Workflows & Agents |
| Which practice does the instructor call "the most important"? | Prompt evaluation — the only way to verify prompts work at scale, not just on the developer's machine |
| Why can't you plan an AI agent feature before tool use? | Agents depend on tools to act on the world; without tool integration, agents can only generate text |
| What are the three course prerequisites? | Basic Python knowledge, a notebook environment, and an Anthropic API key |
| What two Anthropic-built agents does the course cover? | Claude Code (terminal-based coding agent) and Computer Use (browser-based agent) |
| Why should PMs treat the course arc as a product maturity model? | Each capability builds on the previous; skipping stages leads to unreliable features in production |
| What is the instructor's top success tip? | Write code alongside the videos — passive watching has near-zero retention |
