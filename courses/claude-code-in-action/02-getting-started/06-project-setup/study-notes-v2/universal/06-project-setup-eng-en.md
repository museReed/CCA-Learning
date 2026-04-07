# Project Setup — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows |
| Task Statements | 3.1 (project context prerequisite) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> 📝 All content in this section comes directly from official course materials.

## One-Liner / TL;DR

Set up a sample Node.js + SQLite UI generation project so you have a real codebase to explore with Claude Code throughout the rest of the course.

## Core Concepts

### Why a Project Matters

Working with Claude Code is more interesting if you have a project to work with. The course provides a sample UI generation app (the same one shown in a previous video). You do not have to run this project — you can follow along with your own codebase if you prefer.

### Prerequisites

- **Node.js** must be installed locally
- Installation directions: https://nodejs.org/en/download

### Setup Steps

| Step | Command / Action | What It Does |
|------|-----------------|--------------|
| 1 | Install Node.js | Runtime prerequisite |
| 2 | Download and extract `uigen.zip` (attached to the lecture) | Provides the sample project files |
| 3 | `npm run setup` | Installs dependencies and sets up a local SQLite database |
| 4 | *(Optional)* Place an Anthropic API key in the `.env` file | Enables live Claude API calls for UI generation |
| 5 | `npm run dev` | Starts the development server |

> 📝
> Step 4 is optional. If no API key is provided, the app will still generate some static fake code. Get an API key at https://console.anthropic.com/ if you want to fully test the app.

### Project Architecture (from context)

- **Frontend + Backend**: Node.js project with a dev server (`npm run dev`)
- **Database**: Local SQLite (provisioned by `npm run setup`)
- **AI Integration**: Uses Claude through the Anthropic API to generate UI components
- **Graceful Degradation**: Falls back to static fake code when no API key is present

## Key Takeaways

1. The sample project is optional — you can use your own codebase instead
2. `npm run setup` handles both dependency installation and database provisioning in one command
3. The Anthropic API key is optional; the app degrades gracefully without it
4. The project gives you a realistic multi-file codebase to practice Claude Code interactions against
5. The `.env` file is where secrets (API key) are stored — a common Node.js pattern

---

# PART 2: Study Aids

> 💡 Supplementary learning materials, not from official course.

## Familiar Analogies

- **`npm run setup`** — Like `rails db:setup` in Ruby on Rails or `python manage.py migrate` in Django. A single command bootstraps both dependencies and the database.
- **`.env` file for API key** — The same pattern used by Next.js, Vite, and most modern Node.js frameworks. Environment variables keep secrets out of source code.
- **Graceful degradation** — Like a weather app that shows cached data when the network is down. The app still works without the API key, just with static content.
- **SQLite for local dev** — Like using H2 in Java or sqlite3 in Python. A file-based database that requires zero server setup.

## CCA Exam Connection

> 💡
> This unit establishes the project context used for the remainder of the course. Expect questions that test:
> - Understanding that Claude Code works on existing codebases (not just new projects)
> - Knowledge that `npm run setup` is a project-specific script (not a Claude Code command)
> - The distinction between Claude Code (the CLI tool) and the Anthropic API (used by the sample app)

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|-------------|---------------|-----------------|
| Committing the `.env` file with your API key | Exposes secrets in version control | Add `.env` to `.gitignore`; the project likely already does this |
| Running `npm run dev` before `npm run setup` | The database won't exist yet; the app will crash | Always run `npm run setup` first |
| Thinking the API key is required | The course explicitly states it is optional | The app generates static fake code as a fallback |
| Confusing the project's Anthropic API usage with Claude Code itself | They are separate: the project calls the API; Claude Code is the CLI you use to work on the project | Understand that Claude Code analyzes code, while the project uses Claude's API at runtime |

## Practice Questions

**Q1.** After downloading and extracting the sample project, what is the first command you should run?

- A) `npm install`
- B) `npm run dev`
- C) `npm run setup`
- D) `node setup.js`

> 📝
> **Answer: C.** `npm run setup` installs dependencies and sets up the local SQLite database. Running `npm run dev` before setup would fail because the database has not been provisioned.

**Q2.** A student does not have an Anthropic API key. What happens when they run the sample project?

- A) The app will not start at all
- B) The app starts but crashes when generating UI components
- C) The app starts and generates static fake code instead of calling Claude
- D) The app prompts for an API key on startup

> 📝
> **Answer: C.** The course explicitly states that if no API key is provided, the app will still generate some static fake code. The API key is optional for following along with the course.

**Q3.** Where should the Anthropic API key be placed in the sample project?

- A) In a `config.json` file
- B) In the `.env` file
- C) As a command-line argument to `npm run dev`
- D) In the `package.json` under `scripts`

> 📝
> **Answer: B.** The course instructs you to place the API key in the `.env` file, which is the standard Node.js pattern for environment-specific configuration.
