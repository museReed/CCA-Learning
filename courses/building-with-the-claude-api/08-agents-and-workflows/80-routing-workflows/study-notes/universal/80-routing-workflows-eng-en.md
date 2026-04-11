# Routing Workflows — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) — PRIMARY |
| Task Statements | 1.2 (agentic patterns — routing), 5.2 (production workflow deployment) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 80 |

---

## One-Liner

Routing workflows use a classifier LLM call (often with `tool_choice="tool"` for forced tool use) to categorize incoming requests, then dispatch them to specialized downstream pipelines — it's the "switch statement" of LLM workflows.

---

## The Problem Routing Solves

A generic prompt is bad at handling diverse inputs. The lesson's example: a social-media script generator that must handle both "Python functions" (educational) and "surfing" (entertainment). A one-size-fits-all script prompt produces mediocre output for both. The fix is to classify first, then dispatch to a category-specific prompt.

Anthropic describes routing in "Building Effective Agents" as: use it when complex tasks have distinct categories that each benefit from specialized handling, *and* the classification can be performed accurately by an LLM or deterministic algorithm.

---

## Canonical Two-Step Structure

```
user input ──→ [classifier LLM call] ──→ category ──→ [specialized pipeline] ──→ output
```

1. **Categorize** — send the user's request to Claude with a list of predefined categories, ask for one category label
2. **Specialized Processing** — use the returned category to look up the appropriate prompt template / tool set / sub-workflow, then generate the final output

The key insight: user input only goes to *one* specialized pipeline, not all of them. Each pipeline can be optimized independently for its use case.

---

## Example Categories (from the lesson)

| Category | Style |
|----------|-------|
| Entertainment | High-energy, culturally relevant, trendy language |
| Educational | Clear, engaging explanations with relatable examples |
| Comedy | Sharp, unexpected content with clever observations and timing |
| Personal vlog | Authentic, intimate content with conversational storytelling |
| Reviews | Decisive, experience-based content highlighting strengths and weaknesses |
| Storytelling | Immersive content using vivid details and emotional connection |

Each category has its own specialized prompt. Routing picks the right one.

---

## The Lesson's Categorization Prompt

```
Categorize the topic of a video into one of the listed categories:
<topic>Python functions</topic>

<categories>
- Educational
- Entertainment
- Comedy
- Personal vlog
- Reviews
- Storytelling
</categories>
```

Claude responds with "Educational", and your code then picks the educational prompt template.

---

## Forced-Tool Routing with `tool_choice="tool"`

For production, the classifier should return a *structured* category, not a free-form string that you then parse. The CCA-critical technique is to use tool use with `tool_choice` set to force a specific tool call:

```python
from anthropic import Anthropic

client = Anthropic()

ROUTE_TOOL = {
    "name": "route_request",
    "description": "Route the user request to a specialized content pipeline.",
    "input_schema": {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "enum": ["Educational", "Entertainment", "Comedy",
                         "Personal vlog", "Reviews", "Storytelling"],
                "description": "The content category for this topic."
            },
            "confidence": {
                "type": "number",
                "description": "Classifier confidence, 0.0 to 1.0."
            }
        },
        "required": ["category", "confidence"]
    }
}

def classify(topic: str) -> dict:
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        tools=[ROUTE_TOOL],
        tool_choice={"type": "tool", "name": "route_request"},  # forced
        messages=[{"role": "user",
                   "content": f"Categorize the topic: {topic}"}],
    )
    for block in resp.content:
        if block.type == "tool_use" and block.name == "route_request":
            return block.input  # {"category": "...", "confidence": ...}
    raise RuntimeError("Classifier did not call the route_request tool")
```

Why `tool_choice={"type": "tool", "name": "..."}` matters:

- **Forces** Claude to emit the route_request tool call (no free text)
- Guarantees the response shape via `input_schema`
- The `enum` constraint prevents hallucinated categories
- The classifier cannot "chat back" or explain — it MUST categorize

`tool_choice` options:

| Option | Behavior |
|--------|----------|
| `{"type": "auto"}` | Default — Claude decides if it wants to use a tool |
| `{"type": "any"}` | Claude must call *some* tool, but picks which |
| `{"type": "tool", "name": "X"}` | Claude must call exactly tool X |

For routing, `"tool"` is the right choice — you want a *specific* classifier tool called every time.

---

## Full Routing Pipeline

```python
PROMPTS = {
    "Educational": "Write a clear educational script that ...",
    "Entertainment": "Write a high-energy entertainment script that ...",
    "Comedy": "Write a comedy script that ...",
    "Personal vlog": "...",
    "Reviews": "...",
    "Storytelling": "...",
}

def generate_script(topic: str) -> str:
    classification = classify(topic)
    category = classification["category"]
    prompt_template = PROMPTS[category]

    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        messages=[{"role": "user",
                   "content": f"{prompt_template}\n\nTopic: {topic}"}],
    )
    return resp.content[0].text
```

Each branch can be optimized independently, and new categories are added by appending a key-value pair to `PROMPTS` and the enum in `ROUTE_TOOL`.

---

## When Routing Is the Right Pattern

Anthropic's guidance: use routing when you can:

1. **Clearly define categories** — no fuzzy overlap between branches
2. **Trust the classifier** — Claude (or a cheaper classifier) can reliably categorize
3. **Benefit from specialized handling** — per-branch optimization beats a generic prompt
4. **Amortize the classification overhead** — one extra LLM call must be worth it

If the first LLM call cannot reliably categorize, routing is a mistake — you'll route requests to the wrong pipeline and get worse results than a single generic prompt.

---

## Common Mistakes

1. **Using free-form text for the classifier.** Without `tool_choice="tool"` + an `enum`, Claude can return "Maybe educational?" — now you need to parse. Force the tool call.
2. **Too many categories.** Routing works when categories are distinct. 20+ categories with overlap will make the classifier unreliable. Keep it under ~10.
3. **No fallback for misclassification.** What happens when confidence is low? Include a default/generic pipeline.
4. **Ignoring classification cost.** Every request pays an extra LLM call before the real work. For low-latency apps, use a smaller/cheaper model for classification (e.g., Haiku).
5. **Confusing routing with agents.** Routing is a *workflow* — the code dispatches to a specific pipeline. An agent would let Claude pick tools freely during reasoning. They are not the same.

---

> **Key Insight**
>
> Routing is the "switch statement" of LLM workflows — classify first, then dispatch. The production-grade version uses `tool_choice={"type": "tool", "name": "..."}` with an `enum` input schema to force a structured category label. This is the CCA-critical piece: **forced tool use guarantees the classifier returns a valid category and cannot chat back.**

---

## CCA Exam Relevance

- **D1 (22%) PRIMARY**: Routing is one of four core workflow patterns. Expect scenario questions.
- **D2 (18%) SECONDARY**: `tool_choice` options are explicitly tested — know the three values (`auto`, `any`, `tool`).
- **D5 (20%) SECONDARY**: Production patterns — cheap classifier model, fallback branches, enum constraints.
- Signal words for routing: "categorize", "classifier", "dispatch", "specialized handling per category".
- Exam trap: routing ≠ agent. Routing uses code-driven dispatch after a classification call.

---

## Flashcards

| Front | Back |
|-------|------|
| What is a routing workflow? | A classifier LLM call categorizes the request, then code dispatches to a specialized pipeline |
| Why use `tool_choice={"type": "tool", "name": "X"}` for the classifier? | To force Claude to emit a structured category via the tool, with no free-form text allowed |
| Name the three `tool_choice` options. | `auto` (default), `any` (any tool), `tool` (force a specific tool) |
| How do you prevent the classifier from hallucinating new categories? | Use a tool input schema with `"enum": [...]` listing the valid categories |
| When should you NOT use routing? | When categories overlap, when the classifier is unreliable, or when one prompt already works well |
| What is a key production optimization for the classifier step? | Use a smaller/cheaper model (e.g., Haiku) since categorization is simpler than generation |
| Is routing a workflow or an agent? | A workflow — code owns the dispatch after the classification call |
| What should the classifier return for low-confidence cases? | Route to a default/generic pipeline or request human review (fallback path) |
