# Project Setup — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.3 (MCP primitives), 1.2 (agent loop integration), 2.1 (tool schemas) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 63 |

---

## One-Liner

Lesson 63 bootstraps the hands-on MCP project — a CLI chatbot with both a custom MCP client and a custom MCP server in the same codebase — and establishes the directory layout, env vars, and "hello world" baseline you will build on in lessons 64 and 65.

---

## What We're Building

The project is a command-line chatbot that lets users interact with an in-memory document collection through Claude. It has two main components that will be implemented incrementally over the rest of Ch07:

| Component | Purpose |
|-----------|---------|
| **MCP client** | Handles the user chat loop and forwards tool use requests |
| **Custom MCP server** | Manages document operations (read and update) |

The MCP server will expose two essential tools (covered in detail in lesson 64):

1. A **read** tool that returns a document's contents.
2. An **update** tool that edits a document via find-and-replace.

Documents are stored in a plain Python dictionary — no database — to keep the focus on MCP mechanics rather than persistence plumbing.

---

## Important Architecture Note

The lesson calls out a design caveat: **in real-world projects you typically implement either an MCP client OR an MCP server, not both**. Common patterns:

| Role | Example |
|------|---------|
| MCP server author | You expose your internal service's functionality to other developers |
| MCP client author | You build an app that connects to existing MCP servers (e.g. GitHub, Sentry) |

The course builds both halves in the same repo **only for educational purposes** — so you can see how the two sides of the protocol talk to each other without switching codebases. Don't mistake this for the recommended production pattern.

---

## Project Layout

After extracting the `cli_project.zip` attached to the lesson, you will find at minimum:

| File | Role |
|------|------|
| `main.py` | Entry point; runs the CLI chat loop |
| `mcp_client.py` | The MCP client implementation (will be filled in later) |
| `mcp_server.py` | The custom MCP server (will be filled in later) |
| `.env` | Environment file — holds `ANTHROPIC_API_KEY` |
| `README.md` | Step-by-step setup instructions |

The `.env` file is the critical piece: without an Anthropic API key, the chatbot cannot call Claude at all. Both the `uv` and plain `pip` paths expect the key to be present before first run.

---

## Installing Dependencies

The README documents two supported install paths:

### Option 1 — UV (recommended)

```bash
# In the project directory
uv run main.py
```

`uv` is a Python package manager (from Astral, authors of ruff) that combines venv management and dependency install in one command. If the project ships a `pyproject.toml` or `uv.lock`, `uv run` will resolve and install dependencies automatically before executing.

### Option 2 — Standard Python + pip

```bash
# Create and activate a venv, then
pip install -r requirements.txt
python main.py
```

Either path should leave you with:

- The `anthropic` SDK installed
- The `mcp` (Python MCP SDK) installed
- A working Python interpreter that can run `main.py`

---

## "Hello World" Baseline

Before implementing any MCP features, the course asks you to verify the baseline by asking a trivial question:

```
> what's 1+1?
```

You should get a quick response from Claude. This sanity-check confirms three things:

1. Your `.env` is readable by `main.py`.
2. Your API key is valid (no 401).
3. The Claude SDK is correctly installed and callable.

If this fails, there is no point proceeding to lessons 64-65 — MCP will just add more moving parts to an already broken setup.

---

## Why This Lesson Matters

A running baseline is the precondition for any meaningful debugging later. The MCP inspector in lesson 65 and the tool implementations in lesson 64 both assume you can already hit Claude from `main.py`. The lesson is short because its job is not to teach a concept — it is to remove environment excuses for the rest of the chapter.

Concretely, Lesson 63 sets up:

| Setup item | Needed by |
|------------|-----------|
| `.env` with `ANTHROPIC_API_KEY` | Every lesson from here on |
| Working `main.py` CLI | 64, 65, 66, 68, 70 |
| Installed `mcp` Python SDK | 64 (`FastMCP`), 65 (`mcp dev`) |
| Installed `anthropic` Python SDK | Every Claude call |

---

## The Python MCP SDK Stack

Lesson 63 doesn't write MCP code yet, but it does install the runtime you will use next. The two relevant imports for the remaining lessons are:

```python
from mcp.server.fastmcp import FastMCP   # lesson 64
from anthropic import Anthropic          # every lesson
```

`FastMCP` is the high-level server builder (decorators + type hints); the `mcp` package also ships a client API and a CLI inspector (`mcp dev`, used in lesson 65).

---

## Common Mistakes

1. **Skipping the baseline test.** If `what's 1+1?` doesn't work, stop and fix setup — don't add MCP on top.
2. **Forgetting the `.env` file.** The Anthropic SDK reads `ANTHROPIC_API_KEY` from the environment; a missing key produces an unhelpful error at call time, not at import time.
3. **Using a global Python interpreter.** Both `uv` and venv isolate dependencies; a global install risks version conflicts with the `mcp` package.
4. **Assuming you must build both halves in production.** Re-read the Important Architecture Note: real projects usually build only one side.
5. **Ignoring the README.** The README carries exact setup steps; Anthropic course projects are tightly coupled to it.

> **Key Insight**
>
> This lesson's real point is **remove setup ambiguity**. MCP introduces more moving parts than plain tool use (subprocesses, transports, SDK versions). The only way to debug those later without pulling your hair out is to start from a known-good baseline. Getting `what's 1+1?` to work once is a 5-minute investment that pays back across the next four lessons.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: The scenario of "CLI chatbot with in-memory doc store + read/update tools" is the canonical MCP intro example — exam scenarios may echo it.
- **D1 (Agentic Architecture)**: Understand that `main.py` is the host, `mcp_client.py` is the client, `mcp_server.py` is the server — this triad recurs in subsequent questions.
- Recognize that "build both client and server" is an educational choice, not a production recommendation.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the demo project in Ch07? | A CLI chatbot that uses an MCP client plus a custom MCP server to read and update an in-memory document collection. |
| What two tools will the custom MCP server expose? | A read-document tool and an edit-document tool (find and replace). |
| Why does the course build both client and server in one repo? | Purely for educational purposes, so you can see both sides of the MCP protocol in one codebase. |
| What does real-world practice usually look like? | You build either a client OR a server — not both — exposing a service to others or consuming existing servers. |
| What must you add to `.env` before first run? | `ANTHROPIC_API_KEY` |
| What is the recommended Python tool to run the project? | `uv run main.py` |
| What is the baseline sanity check after setup? | Ask the chatbot `what's 1+1?` and verify Claude responds. |
| What files ship in the starter project? | `main.py`, `mcp_client.py`, `mcp_server.py`, `.env`, and a README. |
