# CCA-F Exam — Preparation Strategy

> Compiled from: ai.cc, lowcode.agency, claudecertified.com (March 2026)

## Exam Facts

| Item | Detail |
|------|--------|
| Questions | 60 multiple-choice, scenario-based |
| Time | 120 minutes (no breaks, no external resources) |
| Passing | 720/1000 (aim 900+ on practice) |
| Proctoring | ProctorFree online |
| Results | 2 business days + digital badge |
| Cost | Free (first 5,000 partner org employees) / $99 per attempt |
| Access | Claude Partner Network → Anthropic Skilljar |

## Domain Weights

| # | Domain | Weight | Key Focus |
|---|--------|--------|-----------|
| D1 | Agentic Architecture & Orchestration | **27%** | Multi-agent, task decomposition, hub-and-spoke |
| D3 | Claude Code Configuration & Workflows | **20%** | CLAUDE.md, commands/skills, CI integration |
| D4 | Prompt Engineering & Structured Output | **20%** | Prompting, JSON mode, tool calling |
| D2 | Tool Design & MCP Integration | **18%** | MCP servers, tool boundaries |
| D5 | Context Management & Reliability | **15%** | Long-context, reliability patterns |

**D1 + D3 = 47%** of the exam. Master these two first.

## Recommended Study Path

### Phase 1: Foundation (Free Courses)
1. Claude 101 (baseline)
2. Building with the Claude API (8+ hours — covers D1, D2, D4)
3. Claude Code in Action (covers D3)
4. Introduction to MCP (covers D2)
5. Introduction to Agent Skills (covers D3)
6. Introduction to Subagents (covers D1, D3)

### Phase 2: Deep Dive (Official Materials)
1. Download & study the **Official Exam Guide PDF** (30 Task Statements, 12 sample questions)
2. Read **"Building Effective Agents"** guide (Anthropic Research)
3. Study **Claude Code Documentation** (72 pages, focus on memory/skills/hooks/subagents/headless)

### Phase 3: Practice
1. Complete the **4 Preparation Exercises** in the Exam Guide
2. Attempt the **Official Practice Exam** (available after registration)
3. Optional: 105-question pack from claudecertified.com ($11)

### Phase 4: Hands-On
Build real applications covering all 5 domains:
- RAG system with tool calls
- Support chatbot with external API
- Multi-step autonomous agent
- Structured data extraction pipeline
- CI/CD integration with Claude Code

## Key Preparation Tips

1. **Treat questions as production decisions** — distractors are "very plausible"
2. **Architecture > Prompt** — when both options exist, architecture wins
3. **Deterministic > Probabilistic** — programmatic enforcement > prompt instructions
4. **Tool descriptions are primary** — descriptions > few-shot for tool selection
5. **Master MCP boundaries** — common weak area
6. **Know CLAUDE.md hierarchy** — user/project/managed policy precedence
7. **Batch API has 24h latency** — unsuitable for blocking operations
8. **stop_reason meanings** — `end_turn` vs `max_tokens` vs `tool_use`

## 12 Core Exam Philosophies (from Official Guide)

1. Architecture > Prompt — prefer structural solutions
2. Deterministic > Probabilistic — programmatic enforcement
3. Structured error > Generic — typed errors with actionable fields
4. Description > Few-shot — tool descriptions primary mechanism
5. Hierarchy > Flat — CLAUDE.md scoping matters
6. Isolation > Shared — subagent context isolation
7. Validation > Trust — gates between pipeline steps
8. Explicit > Implicit — clear handoff protocols
9. Minimal scope > Kitchen sink — least privilege tools
10. Evaluation-driven — add complexity only when proven
11. Composability > Monolith — small focused tools
12. Observable > Opaque — structured provenance tracking

## Timeline Estimates

| Profile | Time |
|---------|------|
| Active Claude builder | 2-4 weeks (20-30 hours) |
| Experienced AI developer | 6-10 weeks |
| New to Claude | 2-4 months (including project building) |
