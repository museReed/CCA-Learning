# Welcome to the Course — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding Fundamentals (22%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 1.1 (foundational understanding of Claude capabilities), 5.1 (model selection and deployment readiness) |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 02 |

---

## One-Liner

This orientation lesson maps the full course arc — API access, prompt engineering, tool use, RAG, MCP, Claude Code, and agentic workflows — and sets the prerequisites: Python, notebooks, and an Anthropic API key.

---

## Course Topology

The course follows a deliberate dependency chain. Each module builds on the previous one:

```
API Basics → Prompt Evaluation → Prompt Engineering → Tool Use → RAG → MCP → Claude Code / Computer Use → Workflows & Agents
```

| Module | What You Build | Why It Matters for CCA |
|--------|---------------|----------------------|
| API Fundamentals | First request, multi-turn, streaming | D5: every production app starts here |
| Prompt Evaluation | Eval framework, test datasets | D1: you can't improve what you can't measure |
| Prompt Engineering | Clarity, specificity, XML structure | D1: prompt design is the core agentic skill |
| Tool Use | Tool schemas, multi-tool orchestration | D2: MCP and tool design live here |
| RAG | Chunking, embeddings, retrieval | D5: enterprise knowledge grounding |
| MCP | Servers, clients, resources, prompts | D2: the protocol that connects Claude to the world |
| Claude Code + Computer Use | Terminal agent, browser agent | D1/D3: agentic coding in practice |
| Workflows & Agents | Parallelization, chaining, routing | D1: agentic architecture patterns |

---

## Prerequisites Checklist

Before writing any code, confirm these are in place:

```bash
# 1. Python environment with notebook support
python3 --version          # 3.10+ recommended
pip install jupyter anthropic

# 2. Anthropic API key
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. Verify access
python3 -c "from anthropic import Anthropic; print(Anthropic().messages.create(model='claude-sonnet-4-5', max_tokens=50, messages=[{'role':'user','content':'ping'}]).content[0].text)"
```

If any of these fail, fix them before proceeding. The entire course runs through notebooks, so a broken environment means zero learning velocity.

---

## Success Strategies (Engineering Lens)

| Tip from Instructor | Engineering Translation |
|---------------------|----------------------|
| Write code alongside me | Type every snippet; muscle memory cements API patterns |
| Speed up playback | 1.5x–2x lets you scan for concepts, then pause for implementation |
| Expand / alter notebooks | The best learning happens when you break things on purpose |
| Ask Claude for help | Use Claude itself as a debugging partner — meta-learning |

The last tip is underrated: using Claude to debug Claude API code is a tight feedback loop that mirrors real agentic coding workflows.

---

## Common Mistakes

1. **Skipping environment setup** — half of all "stuck" moments in API courses are import errors and missing keys, not conceptual gaps.
2. **Watching without coding** — passive video consumption has near-zero retention for API patterns.
3. **Jumping ahead to agents** — the dependency chain is real; tool use without prompt engineering knowledge leads to fragile schemas.
4. **Ignoring prompt evaluation** — the instructor calls it "the most important practice." Engineers who skip evals build prompts that work on their machine but fail in production.

> **Key Insight**
>
> This is not a "watch and learn" course — it is a "build and break" course. The dependency chain means each module produces artifacts (notebooks, prompts, tool schemas) that feed the next module. Skipping a module means missing a dependency, not just missing content.

---

## CCA Exam Relevance

- **D1 (Agentic Coding Fundamentals)**: the course topology IS the CCA skill map — API → prompts → tools → agents mirrors the exam's expected progression.
- **D5 (Enterprise Deployment)**: prerequisites (API key management, environment setup) are day-one enterprise concerns.
- Expect the exam to assume you have hands-on experience with every module listed here; this lesson is the roadmap.

---

## Flashcards

| Front | Back |
|-------|------|
| What are the three prerequisites for this course? | Basic Python, a notebook environment, and an Anthropic API key |
| What is the course module order? | API Basics → Prompt Eval → Prompt Engineering → Tool Use → RAG → MCP → Claude Code/Computer Use → Workflows & Agents |
| Why does the instructor emphasize writing code alongside him? | Passive watching has near-zero retention for API patterns; typing cements muscle memory |
| Which module does the instructor call "the most important practice"? | Prompt evaluation — the only way to verify prompts work at scale |
| What two Anthropic-built agents does the course cover? | Claude Code (terminal agent) and Computer Use (browser agent) |
| Why is the module order a dependency chain? | Each module's output (notebooks, schemas, prompts) is input to the next module |
| What is the recommended strategy when stuck? | Ask Claude for help — using Claude to debug Claude API code is a meta-learning loop |
