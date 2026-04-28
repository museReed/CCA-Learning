# Prompts in the Client — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP client implementation), 2.6 (prompt consumption patterns), 1.3 (prompt orchestration) |
| Source | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 13 |

---

## One-Liner

Client-side prompt integration is like installing a "Quick Actions" menu in your product — users see a curated list of expert workflows, pick one, fill in the details, and get consistent results every time.

---

## Why PMs Need to Understand Client-Side Prompts

This lesson completes the picture of how prompts work end-to-end. As a PM, you need to know:

1. **How users discover prompts** — through slash commands, buttons, or menus
2. **How users parameterize prompts** — what inputs they need to provide
3. **How prompts orchestrate tools** — prompts give instructions, tools do the work
4. **The three-way control model** — the foundation of all MCP architecture decisions

---

## Mental Model: The Self-Service Kiosk

Think of the three MCP primitives as different ordering experiences at a fast-food restaurant:

| Experience | MCP Primitive | Who Decides | Kiosk Analogy |
|------------|---------------|-------------|---------------|
| Kitchen decides what to cook | **Tool** | Chef (Claude) | The kitchen makes whatever they think you need |
| Drink dispenser pre-fills | **Resource** | Restaurant system (app) | Water automatically appears at your table |
| Self-service kiosk ordering | **Prompt** | Customer (user) | You tap "Combo #3," customize toppings, confirm |

The slash command experience is the self-service kiosk. The menu has been carefully designed, the combos are tested, and the user just makes selections.

---

## The End-to-End User Journey

Here is what a user experiences when using prompts in a product:

### Step 1: Discovery
User types `/` in the chat. A dropdown appears showing available workflows:
- `/format` — Rewrite a document in Markdown
- `/summarize` — Create a summary of a document
- `/analyze` — Generate an analysis report

This is powered by `list_prompts()` behind the scenes.

### Step 2: Selection and Parameters
User selects `/format`. The system asks for required information:
- "Which document?" — shows a document picker

This is the parameter collection phase. Each prompt defines what inputs it needs.

### Step 3: Execution
User confirms. Behind the scenes:
1. The prompt template is filled with the user's parameters
2. The instructions are sent to Claude
3. Claude reads the document (using tools) and reformats it
4. The result appears in the chat

### Step 4: Result
User sees a professionally formatted markdown document. The same quality every time, regardless of the user's prompt engineering skill.

---

## The Three-Way Control Model — The Master Framework

This is the single most important concept from Chapters 2-3 and a cornerstone of the CCA exam:

| Primitive | Controller | Exam Keyword | Product Example |
|-----------|-----------|-------------|-----------------|
| **Tools** | Claude (model-controlled) | "Claude decides," "autonomously" | Claude runs a calculation behind the scenes |
| **Resources** | Application (app-controlled) | "Pre-loaded," "UI context" | Google Drive document injected into chat |
| **Prompts** | User (user-controlled) | "Slash command," "workflow button" | User clicks "Summarize" workflow button |

### PM Decision Flowchart

When designing a feature, ask:

1. "Who should decide when this happens?"
   - **User explicitly triggers** → Prompt
   - **Claude decides during reasoning** → Tool
   - **App pre-loads automatically** → Resource

2. "Is this a repeatable workflow with known steps?"
   - **Yes** → Prompt (package the workflow as a slash command)
   - **No, it is ad-hoc** → Let Claude handle it with tools

3. "Does this need data before Claude starts thinking?"
   - **Yes** → Resource (inject context into prompt)
   - **No, Claude fetches as needed** → Tool

---

## Prompts + Tools: The Orchestration Pattern

A critical insight for PMs: **prompts do not replace tools — they orchestrate them**.

| What Prompts Do | What Tools Do |
|-----------------|---------------|
| Provide expert instructions | Execute specific actions |
| Define the "what" | Handle the "how" |
| User-controlled trigger | Model-controlled execution |

Example: The `/format` prompt tells Claude "reformat this document using markdown." Claude then uses the `edit_document` tool to make the actual changes. Both primitives are needed.

**PM implication**: When writing a PRD for a prompt-powered feature, you need to ensure the required tools are also available. A prompt without the necessary tools is like a recipe without ingredients.

---

## Product Design Considerations

### Prompt Discoverability
- How do users find available prompts? (Slash menu, toolbar, onboarding)
- Should prompts be categorized? (By task type, frequency of use)
- How prominent should the `/` hint be for new users?

### Parameter Experience
- What parameters does each prompt need?
- Can parameters be auto-filled from context? (Current document, selected text)
- What happens if a required parameter is missing?

### Result Presentation
- How is the prompt result displayed? (Inline, new panel, notification)
- Can the user undo or retry with different parameters?
- Should the system show what prompt was used? (Transparency)

---

## Common PM Mistakes

1. **Designing prompts as tools** — if the user triggers it, it is a prompt; if Claude decides, it is a tool
2. **Forgetting tool dependencies** — prompts often need tools to fulfill their instructions; ensure both are available
3. **Overwhelming users with choices** — curate 5-10 high-value prompts, not 50 rarely-used ones
4. **No parameter defaults** — reduce friction by pre-filling parameters from context (current document, selected text)

> **Key Insight**
>
> The three-way control model is the master framework for all MCP architecture decisions: Tools = model-controlled, Resources = app-controlled, Prompts = user-controlled. For PMs, this translates directly to product design: "Who initiates this action?" determines which primitive to use. On the CCA exam, this distinction appears in nearly every D1 and D2 scenario question.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: Know the two client methods (`list_prompts` and `get_prompt`) and the slash command UX pattern.
- **D1 (Agentic Architecture)**: The three-way control model is the most-tested concept. Expect scenarios asking "which primitive should be used for X?"
- **Key exam signal words**: "slash command" / "workflow button" / "user triggers" → Prompt. "Claude decides" / "autonomously" → Tool. "Pre-loaded context" / "UI data" → Resource.

---

## Flashcards

| Front | Back |
|-------|------|
| What are the three MCP control models? | Tools = model-controlled (Claude decides), Resources = app-controlled (app code decides), Prompts = user-controlled (user decides) |
| What is the slash command pattern for prompts? | User types `/`, sees available prompts, selects one, provides parameters, system sends interpolated messages to Claude |
| How do prompts and tools work together? | Prompts provide the "what" (instructions), tools provide the "how" (capabilities) — Claude uses tools to fulfill prompt instructions |
| What is the self-service kiosk analogy for prompts? | User selects from a curated menu (prompts), customizes options (parameters), and gets a consistent result — just like ordering at a kiosk |
| What should a PM ensure when designing a prompt-powered feature? | That the required tools are also available — a prompt without necessary tools is like a recipe without ingredients |
| How should a PM decide between prompt, tool, and resource? | Ask "Who should decide when this happens?" — User triggers = Prompt, Claude decides = Tool, App pre-loads = Resource |
| What exam signal words indicate a prompt is the answer? | "Slash command," "workflow button," "user triggers," "predefined workflow" |
| In Claude's interface, what are examples of all three primitives? | Prompts = workflow buttons below chat, Resources = "Add from Google Drive," Tools = code execution behind the scenes |
