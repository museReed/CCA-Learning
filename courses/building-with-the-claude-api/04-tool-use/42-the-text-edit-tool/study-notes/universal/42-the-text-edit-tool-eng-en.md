# The Text Editor Tool — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%), D1 — Agentic Architecture (22%) |
| Task Statements | 2.3 (built-in / server tools), 2.1 (tool schema & selection), 1.2 (tool orchestration) |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 42 |

---

## One-Liner

The text editor tool is a built-in Anthropic tool where Claude already knows the full schema — you only declare a tiny stub (`type` + `name`) and provide the local file-operation implementations that execute Claude's commands.

---

## What Makes It a "Built-In" Tool

Most tools require you to author two things:

1. A full JSON schema describing every parameter
2. The Python function that executes the tool

The text editor tool is different. Anthropic ships a **predefined tool schema** inside the model, covering all the file operations Claude supports. You:

- Do **not** define parameters like `path`, `command`, `old_str`, `new_str`
- Do **not** write the full JSON schema
- **Do** declare a small stub telling Claude "enable this built-in tool"
- **Do** write the local functions that actually manipulate files when Claude invokes a command

Claude's side is hidden; your side still matters.

---

## Supported Operations

The text editor tool gives Claude the ability to behave like a local software engineer with a real editor:

| Operation | What It Does |
|-----------|--------------|
| **view** | Read a file or list a directory; can view specific line ranges |
| **create** | Create a new file with initial contents |
| **str_replace** | Replace one string in a file with another (the most common edit) |
| **insert** | Insert text at a specific line number |
| **undo_edit** | Undo the most recent edit to a file |

Together these cover the core editing vocabulary — read, write, create, modify, revert.

---

## Declaring the Stub

The exact stub depends on the Claude model family you are using. The lesson shows a helper:

```python
def get_text_edit_schema(model: str) -> dict:
    if model.startswith("claude-3-7-sonnet"):
        return {
            "type": "text_editor_20250124",
            "name": "str_replace_editor",
        }
    elif model.startswith("claude-3-5-sonnet"):
        return {
            "type": "text_editor_20241022",
            "name": "str_replace_editor",
        }
    # Check Anthropic docs for the latest version string for your model
```

Important notes:

- `type` is **versioned** per model family. The version string must match your model. Anthropic publishes the mapping at `docs.anthropic.com/en/docs/agents-and-tools/tool-use/text-editor-tool`.
- `name` is fixed per version (e.g., `str_replace_editor` for the above versions).
- Claude expands this stub internally into the full schema — you never see the parameter definitions.

---

## Pass It Like Any Other Tool

```python
import anthropic

client = anthropic.Anthropic()
model = "claude-3-5-sonnet-20241022"

response = client.messages.create(
    model=model,
    max_tokens=2048,
    tools=[get_text_edit_schema(model)],
    messages=[
        {"role": "user", "content": "Open ./main.py and summarize its contents"},
    ],
)
```

Claude will respond with a `tool_use` block whose `name` is `str_replace_editor` and whose `input` contains the command Claude wants to run (e.g., `{"command": "view", "path": "./main.py"}`). Your code must dispatch on `input["command"]` and perform the operation.

---

## Providing the Implementation

You are responsible for actually touching the filesystem. A minimal dispatcher:

```python
def run_text_editor(tool_input: dict) -> str:
    command = tool_input["command"]
    path = tool_input["path"]

    if command == "view":
        with open(path) as f:
            return f.read()

    elif command == "create":
        with open(path, "w") as f:
            f.write(tool_input["file_text"])
        return f"Created {path}"

    elif command == "str_replace":
        with open(path) as f:
            content = f.read()
        new_content = content.replace(
            tool_input["old_str"],
            tool_input["new_str"],
            1,
        )
        with open(path, "w") as f:
            f.write(new_content)
        return "Replacement complete"

    elif command == "insert":
        # Insert text at tool_input["insert_line"]
        ...

    elif command == "undo_edit":
        # Restore the previous version
        ...

    else:
        return f"Unknown command: {command}"
```

You decide:

- What filesystem counts as Claude's sandbox
- Whether to allow writes, reads only, or restricted paths
- Whether to keep an undo stack for `undo_edit`

---

## Example Workflow

Prompt: *"Open ./main.py, add a function to compute pi to the 5th digit, then create ./test.py with unit tests."*

Claude's turn sequence:

1. `tool_use`: `view ./main.py`
2. Your code returns the file contents
3. `tool_use`: `str_replace` to inject the new function
4. Your code applies the replacement and confirms
5. `tool_use`: `create ./test.py` with unit test contents
6. Your code creates the file and confirms
7. Final assistant text: "Done — added `compute_pi` and wrote tests."

Each `tool_use` is a separate round trip through your agentic loop.

---

## Why the Text Editor Tool Exists

Given that modern editors already have AI assistants built in, why expose this from the API? Because it enables:

- **Applications** that need to programmatically edit files (e.g., codemod services, migration bots)
- **Agent environments** without access to a full-featured editor
- **Claude-powered applications** that want to embed file editing capabilities natively
- **Headless automation** in CI pipelines

In short, it lets you replicate "AI code editor" functionality inside your own product, with fine-grained control over the file system surface.

---

## Common Mistakes

1. **Using the wrong version string for your model** — `text_editor_20241022` with a 3.7 Sonnet model, or vice versa. Always look up the current mapping in Anthropic's docs.
2. **Trying to write a full JSON schema** — you only provide the stub; Claude already knows the parameters.
3. **Not implementing `undo_edit`** — if Claude tries to revert and your handler ignores it, the workflow breaks.
4. **Running the tool without a sandbox** — the text editor lets Claude write arbitrary files on disk. Scope it to a directory and validate paths.
5. **Forgetting that `view` can target directories** — you must support listing directories, not only reading files.

> **Key Insight**
>
> "Built-in" describes the **schema**, not the **execution**. Anthropic provides the schema knowledge inside the model, but you still write the Python code that actually touches the filesystem. The text editor tool is a hybrid: Anthropic knows the API; you own the runtime.

---

## CCA Exam Relevance

- **D2 (Tool Design)**: The text editor tool is the canonical example of a built-in (schema-provided) tool where the developer supplies execution logic.
- **D1 (Agentic Architecture)**: Chain of file operations (view → edit → create → test) is a typical multi-turn agentic pattern.
- Expect questions contrasting built-in tools (like text editor) with server tools (like web search) where Anthropic handles execution entirely.

---

## Flashcards

| Front | Back |
|-------|------|
| What must you declare to use the text editor tool? | A small stub with `type` (versioned) and `name` (e.g., `str_replace_editor`) |
| Who provides the schema for the text editor tool? | Anthropic — Claude already knows the parameters; you do not define them |
| Who provides the implementation for the text editor tool? | The developer — you write the filesystem-manipulating functions that execute Claude's commands |
| What operations does the text editor tool support? | view, create, str_replace, insert, undo_edit |
| Why does the `type` string contain a date (e.g., `text_editor_20241022`)? | Because the schema is versioned per Claude model family; the version must match your model |
| Can Claude request to view a directory with this tool? | Yes — `view` works on both files and directories |
| What is the main risk of running the text editor tool unsandboxed? | Claude can write arbitrary files; path validation and a sandbox directory are essential |
| Why does this tool exist when editors already have AI built in? | To let Claude-powered applications embed programmatic file editing, useful for codemods, agents, and headless automation |
