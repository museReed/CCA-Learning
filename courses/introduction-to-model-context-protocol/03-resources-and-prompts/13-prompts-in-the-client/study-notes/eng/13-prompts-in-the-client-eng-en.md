# Prompts in the Client — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP client implementation), 2.6 (prompt consumption patterns), 1.3 (prompt orchestration) |
| Source | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 13 |

---

## One-Liner

The client implements `list_prompts()` to discover available prompts and `get_prompt(name, args)` to retrieve interpolated messages, enabling the slash command (`/`) UX pattern where users trigger predefined workflows.

---

## Two Client-Side Methods

### 1. `list_prompts()` — Discovery

```python
async def list_prompts(self) -> list[types.Prompt]:
    result = await self.session().list_prompts()
    return result.prompts
```

This method queries the server for all available prompts. Each `types.Prompt` object contains:
- `name` — the identifier (used in slash commands)
- `description` — human-readable explanation
- `arguments` — list of required/optional parameters

### 2. `get_prompt()` — Retrieval with Interpolation

```python
async def get_prompt(self, prompt_name, args: dict[str, str]):
    result = await self.session().get_prompt(prompt_name, args)
    return result.messages
```

This method retrieves a specific prompt with variable interpolation:
- `prompt_name` — which prompt to retrieve (e.g., `"format"`)
- `args` — keyword arguments as a string-to-string dict (e.g., `{"doc_id": "plan.md"}`)
- Returns `result.messages` — the list of `base.Message` objects ready to send to Claude

The `args` dict maps directly to the prompt function's parameters. When the server receives `{"doc_id": "plan.md"}`, it calls `format_document(doc_id="plan.md")` and returns the interpolated messages.

---

## The Complete Prompt Workflow

Here is the end-to-end flow from user interaction to Claude response:

```
1. User types "/"
   └── Client calls list_prompts()
       └── Server returns available prompts

2. User selects "/format"
   └── Client shows parameter inputs
       └── User provides doc_id = "plan.md"

3. Client calls get_prompt("format", {"doc_id": "plan.md"})
   └── Server runs format_document(doc_id="plan.md")
       └── Returns interpolated messages

4. Client sends messages to Claude
   └── Claude receives expert-crafted instructions
       └── Claude uses tools (e.g., edit_document) to fulfill

5. Claude responds with formatted document
```

### Key Insight: Prompts Orchestrate Tools

When Claude receives the prompt messages, it often needs to use available **tools** to complete the task. In the format example:
1. The prompt tells Claude to reformat a document
2. Claude uses the `edit_document` tool to make changes
3. The result is a properly formatted document

This means prompts and tools work together — prompts provide the instructions, tools provide the capabilities.

---

## The Three-Way Control Model

This is the most important concept across Lessons 10-13 and a core CCA exam topic:

| Primitive | Controller | Trigger Mechanism | Analogy |
|-----------|-----------|-------------------|---------|
| **Tools** | Model-controlled | Claude decides during reasoning | Chef decides what ingredients to use |
| **Resources** | App-controlled | Your code calls `read_resource()` | Waiter brings water automatically |
| **Prompts** | User-controlled | User types `/` or clicks a button | Customer orders from the menu |

This maps to Claude's official interface:
- **Tools** — when Claude executes code or performs calculations behind the scenes
- **Resources** — the "Add from Google Drive" feature that injects document context
- **Prompts** — the workflow buttons below the chat input

---

## Slash Commands: The UX Pattern

Slash commands (`/`) are the primary UI pattern for prompts:

| Step | User Action | Client Behavior |
|------|-------------|-----------------|
| 1 | Types `/` | Calls `list_prompts()`, shows command menu |
| 2 | Selects command | Shows parameter form based on prompt arguments |
| 3 | Provides parameters | Validates input, prepares args dict |
| 4 | Confirms | Calls `get_prompt(name, args)`, gets messages |
| 5 | (Automatic) | Sends messages to Claude, displays response |

The `/` trigger is a convention, not a protocol requirement. Clients can also surface prompts as:
- Buttons in the UI
- Menu items in a sidebar
- Contextual actions on selected content

---

## Prompt Arguments: Variable Interpolation

The `args` parameter in `get_prompt()` is always `dict[str, str]` — all values are strings:

```python
# Client side
messages = await client.get_prompt("format", {"doc_id": "plan.md"})

# Server side (what happens internally)
def format_document(doc_id: str = Field(...)):
    # doc_id = "plan.md" — interpolated from args
    prompt = f"...{doc_id}..."
    return [base.UserMessage(prompt)]
```

Even if the parameter represents a number or boolean, it is passed as a string. The server function handles any necessary type conversion.

---

## Common Mistakes

1. **Confusing `list_prompts()` with `get_prompt()`** — `list_prompts()` returns metadata (names, descriptions), `get_prompt()` returns the actual interpolated messages
2. **Non-string args values** — the `args` dict must be `dict[str, str]`, not `dict[str, Any]`
3. **Sending prompt messages incorrectly** — the messages from `get_prompt()` go directly into the conversation as if the user typed them
4. **Forgetting that prompts use tools** — prompts provide instructions, but Claude often needs tools to fulfill them; both must be available

> **Key Insight**
>
> The three-way control model (Tools = model-controlled, Resources = app-controlled, Prompts = user-controlled) is the single most important MCP architecture concept for the CCA exam. Every primitive serves a different stakeholder: tools serve Claude, resources serve your application, prompts serve your users.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: Know both client methods — `list_prompts()` for discovery, `get_prompt(name, args)` for retrieval. The `args` dict is `dict[str, str]`.
- **D1 (Agentic Architecture)**: The three-way control model is a cornerstone concept. Expect scenario questions asking which primitive to use based on who should control the interaction.
- Questions with "slash command," "workflow button," or "user triggers" almost always point to prompts as the answer.

---

## Flashcards

| Front | Back |
|-------|------|
| What are the two client methods for working with MCP prompts? | `list_prompts()` for discovering available prompts, `get_prompt(name, args)` for retrieving interpolated messages |
| What type is the `args` parameter in `get_prompt()`? | `dict[str, str]` — all keys and values are strings |
| What does `get_prompt()` return? | `result.messages` — a list of `base.Message` objects (UserMessage/AssistantMessage) ready to send to Claude |
| What UI pattern do MCP prompts map to? | Slash commands (`/`) — user types `/`, sees available commands, selects one, provides parameters |
| How do prompts and tools work together? | Prompts provide instructions (what to do), tools provide capabilities (how to do it) — Claude uses tools to fulfill prompt instructions |
| What are the three MCP control models? | Tools = model-controlled (Claude decides), Resources = app-controlled (your code decides), Prompts = user-controlled (user decides) |
| What triggers `list_prompts()` in a typical client? | The user typing `/` in the chat input — the client queries the server for available prompts |
| In Claude's official interface, what demonstrates the prompt pattern? | Workflow buttons below the chat input — predefined, user-triggered workflows |
