# Anthropic Apps — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) |
| Task Statements | 1.1 (Claude Code overview), 1.2 (agentic patterns), 1.4 (Computer Use as agent case study) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 73 |

---

## One-Liner

Anthropic ships two flagship agent applications — Claude Code (terminal coding assistant) and Computer Use (desktop-interaction tool suite) — both serve as canonical reference implementations of the agentic loop: tool integration, multi-step execution, environmental interaction, and autonomous problem-solving.

---

## The Anthropic Application Surfaces

Anthropic exposes Claude through several surfaces. The module focuses on two that exemplify agent design:

| Surface | Form Factor | Agentic? | Purpose |
|---------|-------------|----------|---------|
| Claude.ai | Web chat UI | Conversational, limited tools | Consumer assistant |
| Anthropic API | HTTP endpoint | Primitive — you build the agent | Developer platform |
| **Claude Code** | Terminal CLI | **Yes — full agent** | Agentic coding assistant |
| **Computer Use** | Desktop tool suite | **Yes — full agent** | GUI-interacting agent |

Claude Code and Computer Use are not just "products that happen to use Claude" — they are demonstrations of what a well-constructed agent looks like, and they map directly to patterns you will build yourself on the API.

---

## What Makes These Applications Agents

The course defines an agent as a system that exhibits four properties. Both Claude Code and Computer Use demonstrate all four:

| Property | Claude Code example | Computer Use example |
|----------|---------------------|----------------------|
| **Tool integration** | File edit, shell exec, web fetch, MCP | Screenshot, mouse click, keyboard input |
| **Multi-step task execution** | Plan → read → edit → test → commit | Open browser → navigate → fill form → submit |
| **Environmental interaction** | Reads and mutates the filesystem + shell | Reads and mutates the desktop GUI |
| **Autonomous problem-solving** | Debugs a failing test by iterating | Retries a click after a page reload |

Each cycle feeds the result of the tool call back into the next model turn — the canonical tool-use loop — until a natural stopping condition is reached (`end_turn` stop_reason, or a max-turns guard in the host application).

---

## Claude Code: Terminal-Native Agent

Claude Code runs as a persistent process in your terminal. Key characteristics:

- **Surface**: CLI, not a web chat
- **Tools available by default**: file read/write, grep/glob, bash execution, web fetch, to-do planning
- **Extension point**: MCP servers (we cover this in lesson 76)
- **Context window strategy**: project-scoped `CLAUDE.md` memory file for persistent context
- **Authentication**: `claude` command + Anthropic account login

It is useful to think of Claude Code as "an IDE where the human types English and Claude types code." The agent is responsible for:
1. Understanding the request
2. Reading enough of the codebase to form a plan
3. Editing files
4. Running tests/scripts to verify
5. Reporting back

This is the exact loop we will later replicate when we build our own agents on the raw API.

---

## Computer Use: GUI-Level Agent

Computer Use extends Claude beyond text-only environments. It provides tools that let the model drive a real desktop:

- Take a screenshot (vision input → reasoning)
- Move/click the mouse at pixel coordinates
- Type text with the keyboard
- Navigate the filesystem through GUI applications

Why this matters: most enterprise software does not expose a clean API. Computer Use lets Claude interact with whatever ships in the UI — legacy desktop apps, web dashboards, VDI environments — by treating the pixel plane as the interface.

The model receives screenshots back between actions, inspects them, and decides the next mouse/keyboard action. This is a concrete example of the multimodal tool-use loop.

---

## Why Use These as Case Studies

For agent builders, these apps are reference implementations. They answer:

- What does a good tool schema look like at scale? (Read their exposed tools.)
- How should I structure multi-turn context? (Watch CLAUDE.md behavior in Claude Code.)
- How do I bound autonomy without neutering the agent? (Observe permission prompts and confirmation steps.)
- What gets hard at the edges? (Error recovery, context management, tool choice under ambiguity.)

When you build on the API, you are essentially building your own Claude Code for your specific domain.

---

## Common Mistakes

1. **Treating Claude Code as a black box** — the exam expects you to know it is an *agent*, not a chat app, and to identify its loop structure.
2. **Confusing Claude.ai with Claude Code** — Claude.ai is a chat UI with limited tools; Claude Code is a terminal agent with full filesystem/shell access.
3. **Thinking Computer Use is a replacement for API-based agents** — it is one specific tool suite, not a general pattern. Most production agents use typed tools, not screenshots.
4. **Forgetting MCP extensibility** — the default toolset is only the starting point; both apps can be extended via MCP servers.

> **Key Insight**
>
> Claude Code and Computer Use are not "products" from an exam standpoint — they are **canonical agent implementations** demonstrating the four properties (tool integration, multi-step execution, environmental interaction, autonomous problem-solving). CCA questions frequently frame scenarios as "is this an agent?" and expect you to map the scenario onto these four properties.

---

## CCA Exam Relevance

- **D1 (Agentic Coding & Architecture)**: Know the definition of an agent and that Claude Code is Anthropic's reference agent. Expect questions asking "which of the following is a characteristic of an agent."
- **D3 (Claude Code Configuration)**: Lesson 73 is the gateway to the Claude Code-focused questions (~20% of the exam). Subsequent lessons drill into CLI commands and config.
- Watch for questions that contrast Claude.ai, the API, and Claude Code — know which is a chat, which is a primitive, and which is an agent.

---

## Flashcards

| Front | Back |
|-------|------|
| Which two Anthropic apps are highlighted as reference agent implementations? | Claude Code and Computer Use |
| What are the four properties that define an agent per this lesson? | Tool integration, multi-step task execution, environmental interaction, autonomous problem-solving |
| What surface does Claude Code run on? | The terminal / command line — a CLI-based agent |
| What does Computer Use let Claude interact with? | A full desktop environment via screenshots, mouse, and keyboard |
| Why are these apps used as case studies? | They demonstrate the key principles that make agents effective in real-world implementations |
| How does Claude Code differ from Claude.ai? | Claude.ai is a web chat with limited tools; Claude Code is a terminal agent with filesystem/shell access and MCP extensibility |
| What makes Computer Use valuable for enterprise use cases? | It can drive applications that do not expose APIs by interacting with the GUI directly |
| What is the relationship between Claude Code and MCP? | Claude Code has an MCP client built in, allowing users to extend its tool set with custom MCP servers |
