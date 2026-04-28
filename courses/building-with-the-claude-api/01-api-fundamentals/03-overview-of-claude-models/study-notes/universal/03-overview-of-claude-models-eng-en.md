# Overview of Claude Models — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D5 — Enterprise Deployment (20%) — primary |
| Task Statements | 5.1 (model selection for production workloads) |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 03 |

---

## One-Liner

Claude ships three model families — Opus (max intelligence), Sonnet (balanced), Haiku (fastest/cheapest) — and picking the right one per feature is the first architecture decision in any Claude-powered system.

---

## The Three Model Families

All three share the same core capabilities (text generation, coding, image analysis). The difference is optimization target:

```
Intelligence ◀─────────────────────────────────────▶ Speed / Cost

   Opus              Sonnet               Haiku
   ├── highest IQ    ├── balanced          ├── fastest
   ├── reasoning     ├── strong coding     ├── lowest cost
   ├── multi-hour    ├── precise edits     ├── no extended thinking
   │   autonomy      │   to codebases      │
   ├── higher cost   ├── moderate cost     ├── real-time UX
   └── higher latency└── moderate latency  └── lowest latency
```

### Opus — Maximum Intelligence

| Property | Detail |
|----------|--------|
| Optimization | Highest intelligence / reasoning |
| Best for | Complex multi-step tasks, long autonomous sessions (hours), deep planning |
| Reasoning | Supports extended thinking — can spend time on hard problems |
| Trade-off | Higher latency, higher cost per request |
| Use when | Quality matters more than speed; complex requirements need deep reasoning |

### Sonnet — The Sweet Spot

| Property | Detail |
|----------|--------|
| Optimization | Balance of intelligence, speed, and cost |
| Best for | Most practical use cases, coding tasks, precise codebase edits |
| Reasoning | Supports extended thinking |
| Trade-off | Neither the smartest nor the fastest, but the best default |
| Use when | General-purpose work; the course default model |

### Haiku — Speed Champion

| Property | Detail |
|----------|--------|
| Optimization | Fastest response time, lowest cost |
| Best for | User-facing real-time interactions, high-volume processing |
| Reasoning | Does NOT support extended thinking |
| Trade-off | Moderate intelligence compared to Opus/Sonnet |
| Use when | Latency-sensitive features, classification, simple extraction |

---

## Model Selection Framework

The decision tree is simple:

```python
def select_model(task):
    if task.requires_deep_reasoning or task.is_multi_step_complex:
        return "opus"
    elif task.requires_real_time or task.is_high_volume:
        return "haiku"
    else:
        return "sonnet"  # the default for most applications
```

**Critical insight**: production systems often use multiple models simultaneously:

| Layer | Model | Rationale |
|-------|-------|-----------|
| User-facing chat | Haiku | Speed matters for UX |
| Core business logic | Sonnet | Balance of quality and cost |
| Complex reasoning tasks | Opus | Quality over everything else |

This is not premature optimization — it is cost architecture. A system that routes everything through Opus will cost 5-10x more than one that uses Haiku for simple tasks.

---

## Reasoning Support Comparison

| Capability | Opus | Sonnet | Haiku |
|------------|------|--------|-------|
| Standard responses | Yes | Yes | Yes |
| Extended thinking | Yes | Yes | No |
| Adaptive (simple → fast, complex → think) | Yes | Yes | No |

Haiku's lack of extended thinking is the most important technical differentiator. If your feature needs chain-of-thought reasoning, Haiku is not an option.

---

## Common Mistakes

1. **Using Opus for everything** — wastes money and adds latency; most tasks don't need peak intelligence.
2. **Using Haiku for complex reasoning** — Haiku doesn't support extended thinking; it will give shallow answers on hard problems.
3. **Picking one model and never changing** — model selection should be per-feature, not per-application.
4. **Ignoring the cost multiplier** — the gap between Haiku and Opus pricing means model selection is a budget decision, not just a technical one.
5. **Assuming model names are stable** — always use the specific model string (e.g., `claude-sonnet-4-5`) rather than assuming "Sonnet" means the same version forever.

> **Key Insight**
>
> Model selection is not a one-time decision — it is a routing strategy. The best production systems treat model selection as a parameter, not a constant. They route simple tasks to Haiku, standard tasks to Sonnet, and complex tasks to Opus. This is the first architecture decision you make, and it directly controls your cost and latency budgets.

---

## CCA Exam Relevance

- **D5 (Enterprise Deployment)**: expect scenario questions like "which model should you use for a high-volume customer support bot?" (Haiku) or "which model for a multi-step research agent?" (Opus).
- Model selection questions will likely present trade-off scenarios and ask you to pick the appropriate model family.
- Know that Haiku does NOT support extended thinking — this is a likely exam differentiator.

---

## Flashcards

| Front | Back |
|-------|------|
| What are Claude's three model families? | Opus (max intelligence), Sonnet (balanced), Haiku (fastest/cheapest) |
| Which model should you use for real-time user-facing chat? | Haiku — optimized for speed and cost |
| Which model supports extended thinking? | Opus and Sonnet — Haiku does NOT |
| What is the recommended default model for most applications? | Sonnet — best balance of intelligence, speed, and cost |
| Why do production systems use multiple models? | Different features have different trade-offs; routing saves cost without sacrificing quality |
| When should you choose Opus over Sonnet? | When the task requires deep reasoning, multi-step planning, or long autonomous operation |
| What is the key limitation of Haiku? | No extended thinking / reasoning support; it gives shallow answers on complex problems |
| Which model does this course primarily use? | Sonnet — for its balance of quality, speed, and cost |
