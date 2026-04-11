# Prompts in the Client — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.3 (MCP primitives: client-side prompt access), 1.2 (seeding the agent loop), 2.2 (message content blocks) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 70 |

---

## One-Liner

Using prompts from the client is a two-method extension to your MCP client — `list_prompts()` to discover and `get_prompt(name, args)` to fetch a fully interpolated message list that you feed directly into Claude as the start of a new conversation.

---

## The Client-Side Contract

Prompts defined on the server via `@mcp.prompt()` become invocable only when the client exposes two methods:

1. **`list_prompts()`** — returns every prompt the server knows about, with names, descriptions, and argument metadata.
2. **`get_prompt(prompt_name, args)`** — runs the server's prompt function with the supplied arguments and returns the resulting message list.

With these in place, your application can build UIs like slash menus, show descriptions for each prompt, collect arguments from users, and then launch a fully formed Claude conversation.

---

## Implementing `list_prompts`

```python
async def list_prompts(self) -> list[types.Prompt]:
    result = await self.session().list_prompts()
    return result.prompts
```

This is a straight pass-through to the session:

- `self.session().list_prompts()` calls the MCP SDK, which asks the server for its registered prompts.
- The SDK returns a `ListPromptsResult`; you return `result.prompts` as the list of `types.Prompt` objects.

Each `types.Prompt` object carries:

- `name` — the string identifier (e.g., `"format"`)
- `description` — human-readable summary for UI
- Argument metadata — names, descriptions, required-ness

Your app uses this information to render a picker, validate input, or gate access.

---

## Implementing `get_prompt`

```python
async def get_prompt(self, prompt_name, args: dict[str, str]):
    result = await self.session().get_prompt(prompt_name, args)
    return result.messages
```

This method fetches a specific prompt with arguments interpolated:

- `prompt_name` — the name you saw from `list_prompts()`.
- `args` — a dict mapping argument names to string values (matching the server-side function parameters).
- The session's `get_prompt` sends the request to the server, which runs the prompt function with those args and returns the resulting `list[base.Message]`.
- You return `result.messages` — a conversation ready to send to Claude.

---

## How Prompt Arguments Work

The server-side prompt function expects parameters. For example:

```python
def format_document(doc_id: str):
    # doc_id gets interpolated into the prompt template
```

When the client calls `get_prompt("format", {"doc_id": "report.pdf"})`, the MCP SDK routes the dict as keyword arguments into `format_document(doc_id="report.pdf")`. The function runs, interpolates the arguments into its template, and returns the message list. The client never sees the intermediate template — only the final messages.

This parameterization is what makes prompts reusable: one server-side template serves infinitely many parameter combinations.

---

## Testing Prompts in the CLI

Once `list_prompts` and `get_prompt` are wired, the CLI exposes prompts as slash-commands. Typing `/` shows the available prompts as a menu. Selecting one might trigger a secondary picker (e.g., "which document do you want to format?") and then the completed prompt is sent to Claude.

The canonical workflow:

1. **User selects a prompt** (e.g., `/format`)
2. **System prompts for required arguments** (e.g., which document)
3. **Client calls `get_prompt(name, args)`** — receives interpolated messages
4. **Client sends the messages to Claude** — Claude begins the conversation with that seed
5. **Claude proceeds normally** — it may call tools, read resources, and compose its final answer

---

## The Full Prompt-Powered Agent Loop

From the server author's perspective, a prompt is a recipe. From the client's perspective, it is a prebuilt conversation starter. Put together:

```
┌──────────┐   list_prompts()       ┌────────────┐   list_prompts()       ┌────────────┐
│  User    │ ─────────────────────▶ │ Application│ ─────────────────────▶ │ MCP Server │
│          │                        │ (+ client) │                        │            │
│          │   picks "format"       │            │                        │            │
│          │ ─────────────────────▶ │            │                        │            │
│          │   doc_id="report.pdf"  │            │    get_prompt(...)     │            │
│          │ ─────────────────────▶ │            │ ─────────────────────▶ │            │
│          │                        │            │ ◀───────────────────── │            │
│          │                        │            │   messages=[...]       └────────────┘
│          │                        │            │                              │
│          │                        │            │   first Claude call          │
│          │                        │            │ ─────────────────────▶ ┌──────────┐
│          │                        │            │ ◀───────────────────── │  Claude  │
│          │                        │            │   tool_use(...)        │   API    │
│          │                        │            │                        └──────────┘
│          │                        │            │   loop continues...
└──────────┘                        └────────────┘
```

The prompt only seeds the conversation. Tool use, resource access, and multi-turn reasoning continue as usual afterward.

---

## Prompt Best Practices (From the Lesson)

- Make prompts relevant to your server's purpose
- Test thoroughly before deployment
- Use clear, specific instructions
- Design them to work well with your available tools
- Consider what arguments users will need to provide

These mirror the server-side best practices from Lesson 69 — the client is simply the consumer of them.

---

## Common Mistakes

1. **Treating `get_prompt` result as plain text** — it is a **message list**. You must send it via the Anthropic API's messages parameter, not as a single user string.
2. **Passing wrong argument names** — `args` keys must match the server prompt function's parameter names exactly. Mismatch → server-side error.
3. **Calling `get_prompt` without first calling `list_prompts`** — you can technically do it, but you lose the ability to present a UI and validate arguments.
4. **Caching prompt messages across sessions** — prompt results are effectively pure, but the conversation state they create is per-session. Re-fetch when needed.
5. **Ignoring the description metadata** — the whole point of prompts is discoverability; propagate descriptions into your UI.

> **Key Insight**
>
> `list_prompts` and `get_prompt` are tiny — two methods, half a dozen lines — yet they complete MCP's product surface. With them, your client gets a "menu of pre-engineered actions" that the server author maintains. Every time the server author improves a prompt, every client that uses it improves automatically. This is the asymmetric compounding that makes prompts the most PM-friendly of the three MCP primitives.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: know the two client-side methods (`list_prompts`, `get_prompt`), the dict-based arg passing, and the `list[base.Message]` return shape.
- **D1 (Agentic Architecture)**: prompts seed the agent loop with curated starting conversations; the loop proceeds normally afterward.
- Exam pattern: "How does the client fetch a prompt with arguments?" → `await self.session().get_prompt(prompt_name, args)` and return `result.messages`.

---

## Flashcards

| Front | Back |
|-------|------|
| What two client methods are needed to use prompts? | `list_prompts()` to discover and `get_prompt(prompt_name, args)` to fetch an interpolated message list. |
| What does `list_prompts()` return? | `result.prompts` — a list of `types.Prompt` objects containing name, description, and argument metadata. |
| What does `get_prompt` return? | `result.messages` — a `list[base.Message]` ready to send to Claude. |
| How are prompt arguments passed? | As a `dict[str, str]` whose keys match the server prompt function's parameter names. |
| What happens on the server when the client calls `get_prompt`? | The server runs the decorated prompt function with the args as keyword arguments and returns the resulting message list. |
| What does the client do with the returned messages? | Sends them to Claude as the start of a new conversation; the agent loop proceeds normally (tools, resources, multi-turn). |
| How do prompts appear to the user in a CLI? | As slash-commands (e.g., `/format`), optionally followed by argument pickers before the prompt is sent to Claude. |
| Why is caching `get_prompt` results across sessions risky? | Prompt outputs are templates for new conversations; the conversation state that follows is per-session, so cached messages can mislead the app's state model. |
