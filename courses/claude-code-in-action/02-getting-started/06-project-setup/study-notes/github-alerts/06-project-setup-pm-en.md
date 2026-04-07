# Project Setup — PM Perspective

| Item | Details |
|------|---------|
| Exam Coverage | D2 — Tool Design & MCP Integration (18%), D3 — Effective Claude Code Usage (30%) |
| Task Statements | 2.5 (built-in tools — awareness), 3.5 (iterative refinement — intro) |
| Course Source | claude-code-in-action / 02-getting-started / Lesson 06 (text-only) |

---


![Iterative Refinement Cycle](../../visuals/iterative-refinement-cycle.svg)
*Figure: The iterative refinement cycle — request, build, view, feedback.*

## TL;DR

The course uses a small Node.js app that generates UI components via Claude's API. PMs should understand: (1) the project demonstrates how Claude Code works with real codebases, (2) it has an optional API key — meaning the tool works even without external API access, and (3) the iterative generate-review-refine workflow it introduces is how teams actually use Claude Code in practice.

---

## Why PMs Should Care

1. **Product demo literacy** — Understanding the demo project helps you follow along and communicate what Claude Code does to stakeholders
2. **Iterative workflow introduction** — The generate-review-refine cycle is how engineering teams adopt Claude Code; this is the productivity story you will pitch
3. **API key optionality** — Demonstrates graceful degradation, a product design pattern worth noting

---

## Business Analogies

| Concept | Business Analogy |
|---------|-----------------|
| Demo project with optional API | Like a freemium SaaS — core features work without payment, premium features need a key |
| `npm run setup` one-time init | Like onboarding setup in an enterprise tool — run once, then start working |
| Iterative UI generation | Like design sprints — show prototype, get feedback, refine, repeat |

---

## Scenario Walkthrough: Explaining Claude Code to Stakeholders

Your VP of Engineering asks: "What does Claude Code actually do with our code?"

Using the demo project as a reference:

| Step | What Happens | Business Impact |
|------|-------------|----------------|
| 1. Developer asks Claude to build a feature | Claude reads the project structure and relevant files | No pre-indexing needed; works on any codebase from day one |
| 2. Claude generates implementation | Code is written directly in the project files | No copy-paste from a separate chat window |
| 3. Developer reviews in browser | The app reflects changes immediately | Feedback loop is seconds, not hours |
| 4. Developer provides refinement feedback | Claude iterates on the implementation | Converges on the right solution through dialogue |

---

## Practice Question

### Scenario: ROI Estimation

Your CFO asks whether the team needs Anthropic API keys for every developer to use Claude Code. Based on this lesson, what is the correct answer?

- A. Yes — Claude Code requires an API key to function at all
- B. No — Claude Code itself does not need an Anthropic API key; the demo project optionally uses one for its own features
- C. API keys are only needed for the first setup, then can be removed
- D. One shared API key is sufficient for the entire team

<details><summary>Answer</summary>

**B** — Claude Code authenticates through its own mechanism (Lesson 05). The Anthropic API key in this lesson is for the demo project's UI generation feature, not for Claude Code itself. The demo works without it using static fallback data.

**PM Takeaway**: Do not conflate the demo project's API key with Claude Code's authentication. These are separate systems. Claude Code's cost is through its own subscription/usage model, not through API keys in project `.env` files.
</details>
