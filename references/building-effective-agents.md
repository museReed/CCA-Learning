# Building Effective Agents — Anthropic Official Guide

> Source: https://www.anthropic.com/research/building-effective-agents
> CCA Relevance: D1 Agentic Architecture & Orchestration (27%)

## Core Philosophy

**Start simple, add complexity only when evaluation metrics prove improvement.**

Anthropic distinguishes:
- **Workflows**: Predetermined execution paths; LLMs follow scripted sequences
- **Agents**: Model itself determines task decomposition and tool usage dynamically

Trade-off: Agentic systems exchange latency and cost for better task performance.

---

## Foundation: Augmented LLM

Base component combining LLM with:
- Retrieval capabilities
- Tool access
- Memory systems

Modern models can generate search queries, select tools, and determine what to retain. MCP offers one standardized approach for tool ecosystem integration.

---

## Workflow Patterns

### 1. Prompt Chaining
**Sequential steps** where each LLM call processes previous outputs.

- **When**: Tasks with fixed, cleanly separable subtasks; accuracy gains justify latency
- **Examples**: Marketing copy → translation; Document outline → draft
- **Key**: Add programmatic validation ("gates") between steps

### 2. Routing
**Classify inputs** and direct to specialized handlers.

- **When**: Distinct categories better handled separately; classification is accurate
- **Examples**: Customer service routing (general/refund/technical); Cost optimization (Haiku for easy, Sonnet for hard)
- **Implementation**: LLM or traditional classification

### 3. Parallelization
**Execute multiple LLM operations simultaneously** with aggregated outputs.

Two variations:
- **Sectioning**: Break independent subtasks into parallel tracks
- **Voting**: Run identical tasks multiple times for consensus

- **When**: Parallel execution improves speed or multiple perspectives needed
- **Sectioning examples**: Guardrails (screening + response); Evaluation (specialized dimensions)
- **Voting examples**: Code security reviews; Content appropriateness with threshold

### 4. Orchestrator-Workers
**Central LLM dynamically decomposes tasks**, delegates to workers, synthesizes.

- **When**: Open-ended problems where subtask structure can't be predetermined
- **Key difference from parallelization**: Flexibility — subtasks emerge from specific inputs
- **Examples**: Coding tasks (variable files/changes), information gathering

### 5. Evaluator-Optimizer
**Iterative refinement loop**: one instance generates, another provides feedback.

- **When**: Clear evaluation criteria; iterative improvement demonstrably helps
- **Examples**: Literary translation, multi-round research

---

## Autonomous Agents

Operate in continuous loops: receive task → plan → execute tools → evaluate → iterate.

**Requirements**: Complex input understanding, reasoning, reliable tool usage, error recovery.

**Lifecycle**:
1. Initial command or discussion
2. Independent execution with environment feedback
3. Pauses for human input at checkpoints/obstacles
4. Completion or stopping conditions

**Critical design**: Tool documentation quality determines agent effectiveness. ACI ≈ HCI effort.

**Risk management**: Higher costs, compounding errors → sandboxed testing + robust guardrails.

---

## Tool Optimization (ACI Design)

Consider:
- Format that matches LLM writing difficulty (diffs require line count knowledge; JSON needs escape handling)
- Optimal formats: provide thinking space, match internet patterns, eliminate formatting overhead
- Treat tool definitions with same rigor as prompts: include examples, edge cases, input specs, boundaries
- **Poka-yoke principle**: Restructure arguments to make mistakes harder (absolute paths > relative; required params > optional)

---

## Core Success Principles

1. **Simplicity**: Minimal agent design complexity
2. **Transparency**: Explicit visualization of planning steps
3. **Documentation**: Thorough tool definition and rigorous testing

---

## Key Exam Takeaways

| Principle | Exam Application |
|-----------|-----------------|
| Simplest solution first | Don't over-architect when a simple chain suffices |
| Programmatic gates between steps | Architecture > Prompt for enforcement |
| Orchestrator-Workers for dynamic tasks | Distinguish from parallelization (fixed vs dynamic) |
| Tool description quality = tool selection quality | D2 core concept |
| ACI design rigor = HCI rigor | Tool interface design matters |
| Evaluation-driven complexity | Only add agents when metrics prove improvement |
