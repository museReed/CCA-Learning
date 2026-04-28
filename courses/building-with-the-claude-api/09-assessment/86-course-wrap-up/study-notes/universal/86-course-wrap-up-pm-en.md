# Course Wrap Up — PM Quick-Scan

| Item | Detail |
|------|--------|
| Exam Domain | D1 (22%) + D2 (18%) + D4 (20%) + D5 (20%) — Cross-cutting review |
| Task Statements | All — comprehensive course recap |
| Source | building-with-the-claude-api / 09-assessment / Lesson 86 |

---

## One-Liner

This wrap-up provides a bird's-eye view of every major topic in the course and identifies the highest-priority follow-up areas for self-study: agent orchestration, agent monitoring, agentic RAG, and tool evaluation.

---

## Course Topics at a Glance

| Topic | Business Impact | Key Takeaway |
|-------|----------------|--------------|
| **Model Selection** | Cost vs capability trade-off | Haiku for speed/cost, Sonnet for intelligence |
| **API Parameters** | Control output quality | Temperature, stop sequences, prefilling |
| **Prompt Evaluation** | Production reliability | #1 most important practice — don't skip it |
| **Prompt Engineering** | Response quality | Clarity is the primary lever |
| **Tool Use** | Capability expansion | Lets Claude interact with external systems |
| **Claude Code** | Developer productivity | Terminal-based coding workflow |
| **Workflows vs Agents** | Architecture decisions | Workflows first — higher accuracy, more predictable |

### The Biggest Takeaway

**Prompt evaluation is the most important practice for any AI product.** A prompt that works 10 times in testing may fail at scale. Evaluations don't need complex frameworks — Claude can help build them.

### Workflows Over Agents

When planning product features: **default to workflows**, not agents. Agents are flexible but less predictable. Workflows deliver consistent, measurable results for structured tasks.

---

## Knowledge Gaps to Fill

| Follow-Up Topic | Product Relevance |
|------------------|-------------------|
| Agent Orchestration | Multi-agent product features |
| Agent Evaluation & Monitoring | Production observability |
| Agentic RAG | Advanced search and reasoning |
| Tool Evaluation | Ensuring tool descriptions drive correct AI behavior |

---

## CCA Exam Relevance

Use this as a final review checklist mapping topics to exam domains. The workflows-over-agents principle and prompt evaluation importance are likely exam topics.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the #1 most important practice for production AI apps? | Prompt evaluation. |
| Should product teams default to agents or workflows? | Workflows — they deliver higher accuracy and more predictable results. |
| What is tool evaluation? | Testing that tool descriptions help Claude use tools correctly. |
| What model trade-off should PMs understand? | Haiku = fast/cheap, Sonnet = more intelligent — choose based on use case requirements. |
| What follow-up topics should teams research? | Agent orchestration, agent monitoring, agentic RAG, tool evaluation. |
