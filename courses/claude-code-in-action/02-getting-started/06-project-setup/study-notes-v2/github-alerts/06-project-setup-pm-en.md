# Project Setup — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows |
| Task Statements | 3.1 (project context prerequisite) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> 📝 All content in this section comes directly from official course materials.

## One-Liner / TL;DR

A sample project is provided so you have a real working application to explore with Claude Code — think of it as a sandbox environment for the rest of the course.

## Core Concepts

### Why You Need a Project

Working with Claude Code is more interesting if you have a project to work with. The course provides a sample UI generation app (the same one shown in a previous video). You do not have to run this project — you can follow along with your own codebase if you prefer.

### What the Project Does

The sample app is a **UI generation tool** that uses Claude through the Anthropic API to create UI components. Think of it as a small product that takes a request and produces a visual output — similar to how many AI-powered SaaS tools work under the hood.

### Setup Steps (What Your Engineering Team Would Do)

| Step | Command / Action | PM Translation |
|------|-----------------|----------------|
| 1 | Install Node.js from https://nodejs.org/en/download | Install the runtime — like installing Java or Python on a developer's machine |
| 2 | Download and extract `uigen.zip` (attached to the lecture) | Get the project files — like cloning a repo from GitHub |
| 3 | Run `npm run setup` | One-click setup — installs dependencies and configures the database, similar to clicking "Setup" in a SaaS onboarding wizard |
| 4 | *(Optional)* Place an Anthropic API key in the `.env` file | Configure the AI integration — like entering your OpenAI key in a tool's settings page. Get one at https://console.anthropic.com/ |
| 5 | Run `npm run dev` | Start the application — like clicking "Run" in an IDE or launching a local server |

> [!NOTE]
> The API key (step 4) is optional. If no API key is provided, the app will still generate some static fake code. This is a **graceful degradation** pattern — the product works with reduced functionality rather than breaking entirely.

### Key Architecture Decisions (PM Lens)

- **Local SQLite database**: No cloud database setup needed. Zero infrastructure cost for development.
- **Optional API key**: Lowers the barrier to entry. New team members can onboard without waiting for API access.
- **Single setup command**: `npm run setup` bundles multiple steps. Good developer experience (DX) reduces onboarding friction.

## Key Takeaways

1. The sample project is optional — teams can use their own codebase
2. One command (`npm run setup`) handles the entire environment bootstrap
3. The API key is optional, demonstrating graceful degradation in product design
4. The project represents a typical AI-integrated web application architecture
5. Secrets (API keys) are stored in `.env` files, not in code — a security best practice

---

# PART 2: Study Aids

> 💡 Supplementary learning materials, not from official course.

## Familiar Analogies

- **`npm run setup`** — Like a "Quick Start" wizard in enterprise software. One click (one command) and the environment is ready. Reduces the "time to first value" for developers.
- **`.env` file** — Like a settings page in a SaaS product where you enter API keys and configuration. It separates secrets from the application code.
- **Graceful degradation (no API key)** — Like Spotify's offline mode: core features still work, but premium features (live AI generation) require authentication.
- **SQLite** — Like an embedded database (think MS Access but modern). Perfect for prototyping because it requires no separate database server.

## CCA Exam Connection

> [!TIP]
> As a PM, you may be tested on understanding the project setup context rather than memorizing exact commands. Focus on:
> - Why Claude Code needs a project to work with (it analyzes existing code)
> - The difference between Claude Code (the development tool) and the Anthropic API (what the sample app uses at runtime)
> - Understanding that setup commands are project-specific, not Claude Code features

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|-------------|---------------|-----------------|
| Assuming Claude Code only works with the sample project | Claude Code works with any codebase | The sample project is just a convenient example |
| Thinking the API key is mandatory for the course | The course explicitly makes it optional | The app gracefully degrades without it |
| Confusing project setup with Claude Code setup | They are separate concerns: one sets up the app, the other sets up the AI tool | Unit 05 covers Claude Code setup; Unit 06 covers the sample project |
| Skipping this unit because "PMs don't code" | Understanding the dev environment helps you communicate with engineering | At minimum, understand what the setup steps accomplish |

## Practice Questions

**Q1.** What does `npm run setup` accomplish in the sample project?

- A) Installs Claude Code on the developer's machine
- B) Installs project dependencies and sets up a local SQLite database
- C) Deploys the application to a cloud server
- D) Configures the Anthropic API key

> [!NOTE]
> **Answer: B.** `npm run setup` is a project-specific script that installs dependencies and provisions the local database. It has nothing to do with Claude Code installation (that was covered in Unit 05).

**Q2.** Why does the sample project work without an Anthropic API key?

- A) It uses Claude Code's built-in API key
- B) SQLite provides the AI capabilities locally
- C) The app falls back to generating static fake code
- D) Node.js includes AI generation features

> [!NOTE]
> **Answer: C.** The course states that without an API key, the app generates static fake code. This is a graceful degradation pattern — the product provides reduced but functional output rather than failing entirely.

**Q3.** A PM is evaluating whether their team should use the sample project or their own codebase for the course. Which statement is correct?

- A) The sample project is required for certification
- B) Teams must use the sample project for the first three modules, then can switch
- C) Either option works — the course explicitly says you can follow along with your own codebase
- D) Only the sample project has the correct structure for Claude Code

> [!NOTE]
> **Answer: C.** The course explicitly states: "You can always follow along with the remainder of the course with your own code base if you wish." Claude Code works with any codebase.
