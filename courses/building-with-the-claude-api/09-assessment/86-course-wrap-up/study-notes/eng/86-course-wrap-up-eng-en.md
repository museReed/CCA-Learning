# Course Wrap Up — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D1 (22%) + D2 (18%) + D4 (20%) + D5 (20%) — Cross-cutting review |
| Task Statements | All — comprehensive course recap |
| Source | building-with-the-claude-api / 09-assessment / Lesson 86 |

---

## One-Liner

This wrap-up recaps every major topic covered in the course — from model selection and API parameters through prompt evaluation, tool use, MCP, and agent architectures — and highlights the follow-up topics you should research independently: agent orchestration, agent evaluation, agentic RAG, and tool evaluation.

---

## Course Recap

### Models and API Access (D5)

Anthropic offers multiple models with different trade-offs:
- **Haiku** — fast, cost-efficient, best for smaller requests
- **Sonnet** — higher intelligence, best for complex tasks

The API accepts parameters that shape Claude's behavior: **temperature** (creativity control), **stop sequences** (output termination), and **message prefilling** (guiding response format).

### Prompt Evaluation (D5)

The instructor emphasizes this as **the single most important practice** for production applications. Running a prompt 10 times locally may look fine, but production users will surface edge cases. Key principles:

- Evaluations don't require fancy frameworks — Claude can generate eval frameworks
- Systematic evaluation catches failures that manual testing misses
- The course's own eval framework was largely Claude-authored

### Prompt Engineering (D4, D5)

Core technique: **be clear and direct**. Tell Claude exactly what you expect. Additional techniques covered in the course build on this foundation but clarity is always the primary lever.

### Tool Use (D2)

Tool use dramatically expands Claude's capabilities. It was one of the most complex sections because it involves:
- Tool schema definition
- Handling message blocks (tool_use, tool_result)
- Multi-turn tool conversations
- Multiple simultaneous tools

### Claude Code and Computer Use (D3)

Two Anthropic applications with hands-on coverage. The instructor specifically notes he uses Claude Code at the terminal as his primary coding workflow — not an in-editor assistant.

### Workflows vs Agents (D1)

Critical distinction: **workflows often deliver better results and higher accuracy than agents**. Agents are exciting but workflows should be your default choice for structured, predictable tasks.

---

## Recommended Follow-Up Topics

The instructor identifies these as important topics not fully covered:

| Topic | Why It Matters |
|-------|---------------|
| **Agent Orchestration** | Getting multiple agents to work together |
| **Agent Evaluation & Monitoring** | Measuring agent performance in production |
| **Agentic RAG** | RAG variation where agents actively search and reason |
| **RAG Evaluation** | Measuring retrieval quality systematically |
| **Tool Evaluation** | Ensuring tool descriptions help Claude correctly (analogous to prompt evals) |

---

## CCA Exam Relevance

This lesson is a meta-review — it maps the entire course to exam domains. Use it as a checklist:
- D1: Agents vs workflows distinction, agentic loop
- D2: Tool use, MCP primitives
- D4: Prompt engineering, safety
- D5: Model selection, prompt evaluation, production patterns

---

## Flashcards

| Front | Back |
|-------|------|
| Which model is best for fast, cost-efficient requests? | Haiku. |
| What does the instructor call the most important practice for production AI apps? | Prompt evaluation. |
| What is the primary prompt engineering technique? | Being clear and direct — tell Claude exactly what you expect. |
| Should you default to agents or workflows for structured tasks? | Workflows — they often deliver better results and higher accuracy than agents. |
| What is tool evaluation? | Ensuring tool descriptions help Claude use tools correctly — analogous to prompt evals. |
| What is agentic RAG? | A RAG variation where agents actively search and reason, rather than simple retrieve-then-generate. |
| What follow-up topics does the instructor recommend? | Agent orchestration, agent evaluation/monitoring, agentic RAG, RAG evaluation, tool evaluation. |
