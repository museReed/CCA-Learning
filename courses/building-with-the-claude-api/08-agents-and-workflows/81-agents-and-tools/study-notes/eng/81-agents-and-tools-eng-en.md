# Agents and Tools — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) |
| Task Statements | 1.1 (agent architecture), 1.2 (agentic loop), 1.3 (tool use in agents), 5.1 (production pattern selection) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 81 |

---

## One-Liner

An agent is Claude + a set of abstract, combinable tools running in an agentic loop — instead of executing a predefined sequence, Claude decides which tools to call and in what order to achieve a goal it is given at runtime.

---

## Workflow vs Agent: The Core Shift

In a workflow, you hard-code the tool-calling sequence: "first call tool A, then tool B, then tool C." The developer owns the control flow.

In an agent, you hand Claude a goal plus a toolbox, and Claude owns the control flow. The same agent binary can handle "What time is it?" and "Set a gym reminder next Wednesday at 7am" without any conditional branching in your Python code.

```python
# Workflow: developer controls the sequence
def schedule_reminder(task, when):
    now = get_current_datetime()
    target = add_duration_to_datetime(now, when)
    return set_reminder(task, target)

# Agent: Claude controls the sequence
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[get_current_datetime, add_duration_to_datetime, set_reminder],
    messages=[{"role": "user", "content": "Remind me to go to the gym next Wednesday"}]
)
# Claude decides: call get_current_datetime -> add_duration_to_datetime -> set_reminder
```

---

## The Datetime Example — Emergent Tool Chaining

Three simple tools:

- `get_current_datetime` — returns current date/time
- `add_duration_to_datetime` — returns `datetime + duration`
- `set_reminder` — creates a reminder at a specific instant

Look how Claude combines them for different user requests:

| User Request | Tool Sequence |
|--------------|---------------|
| "What's the time?" | `get_current_datetime` |
| "What day of the week is it in 11 days?" | `get_current_datetime` -> `add_duration_to_datetime` |
| "Remind me to go to the gym next Wednesday" | `get_current_datetime` -> `add_duration_to_datetime` -> `set_reminder` |
| "When does my 90-day warranty expire?" | Asks user for purchase date first, then chains tools |

The agent is not explicitly programmed to recognize "next Wednesday" or "90-day warranty" — Claude's reasoning converts natural language into the right tool chain. This is **emergent composition**, and it is the whole reason agents exist.

---

## Design Principle: Abstract Tools Beat Specialized Tools

The most important rule for tool design in agent systems is to prefer primitive, abstract tools over narrow, task-specific ones. Claude Code is the canonical example:

| Has | Does NOT have |
|-----|---------------|
| `bash` (run any command) | `install_npm_dependency` |
| `read` (read any file) | `read_python_imports` |
| `write` (create any file) | `create_react_component` |
| `edit` (modify files) | `refactor_function` |
| `glob` / `grep` (find files / search content) | `find_unused_variables` |

With six primitives, Claude can refactor code, install dependencies, run tests, write migrations, audit security — scenarios the Claude Code team never explicitly planned for. A specialized tool like `refactor_function` would work for one narrow case and be useless everywhere else.

**Mental heuristic**: if you can describe a tool with a Unix verb, it is probably at the right level of abstraction.

---

## Designing Combinable Tool Sets

A well-designed agent tool set is a small number of primitives that **compose**. Example: a social media video agent.

```python
tools = [
    {
        "name": "bash",
        "description": "Run shell commands including FFMPEG for video processing",
        "input_schema": {"type": "object", "properties": {"command": {"type": "string"}}}
    },
    {
        "name": "generate_image",
        "description": "Create an image from a text prompt",
        "input_schema": {"type": "object", "properties": {"prompt": {"type": "string"}}}
    },
    {
        "name": "text_to_speech",
        "description": "Convert text to an audio file",
        "input_schema": {"type": "object", "properties": {"text": {"type": "string"}, "voice": {"type": "string"}}}
    },
    {
        "name": "post_media",
        "description": "Upload a media file to a social platform",
        "input_schema": {"type": "object", "properties": {"file_path": {"type": "string"}, "platform": {"type": "string"}}}
    }
]
```

This set supports:

- "Post a cooking video" -> image + TTS + bash(FFMPEG) + post_media
- "Generate a sample image first, wait for my approval" -> image, pause for feedback, then continue
- "Make it funnier" -> regenerate with a different prompt

None of those flows were hard-coded. They emerge from the agent's reasoning over the same four tools.

---

## The Agentic Loop (Runtime View)

```python
messages = [{"role": "user", "content": user_goal}]
while True:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        tools=tools,
        messages=messages
    )
    messages.append({"role": "assistant", "content": response.content})

    if response.stop_reason == "end_turn":
        break

    if response.stop_reason == "tool_use":
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })
        messages.append({"role": "user", "content": tool_results})
```

This loop is the entire agent. You do not predetermine the number of iterations — Claude decides when it is done by returning `stop_reason == "end_turn"`.

---

## Common Mistakes

1. **Over-specialized tools** — building `refactor_python_class` instead of `edit`. You trade one working case for dozens of broken ones.
2. **No loop termination guard** — letting the agent run forever. Always set a max iteration count (e.g., 25) to cap runaway costs.
3. **Treating the agent like a workflow in disguise** — if you find yourself writing `if tool_name == X: force call Y`, you want a workflow, not an agent.
4. **Vague tool descriptions** — Claude can only select tools it understands. Write descriptions as if you were onboarding a new engineer.
5. **Forgetting tool_results are user-role messages** — in the Anthropic API, tool results are sent back with `role: "user"`, not a separate role.

> **Key Insight**
>
> Agents win when you cannot enumerate the steps in advance. Give Claude small, abstract, combinable tools and a clear goal, then let the agentic loop do the composition. The developer's job shifts from writing control flow to designing the right toolbox.

---

## CCA Exam Relevance

- **D1 (Agentic Coding & Architecture)**: Expect questions on "what is an agent vs a workflow" and "which tool design supports an agent." The answer is almost always the more abstract primitive.
- **D5 (Enterprise Deployment)**: Agents are harder to evaluate and cost more per task — know these trade-offs.
- Flag words in questions: "unpredictable requests," "varied tasks," "creative combination" -> agent. "Known sequence," "repeatable," "reliable" -> workflow.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the defining difference between an agent and a workflow? | In a workflow the developer hard-codes the tool sequence; in an agent Claude decides the tool sequence at runtime based on the goal. |
| Why should agent tools be abstract rather than specialized? | Abstract tools (bash, read, edit) compose to cover cases the developer never anticipated; specialized tools (refactor_function) work for one case and nothing else. |
| Name three primitive tools Claude Code exposes. | bash, read, write, edit, glob, grep (any three). |
| How does Claude handle "When does my 90-day warranty expire?" in an agent? | It recognizes missing information, asks the user for the purchase date, then chains get_current_datetime and add_duration_to_datetime. |
| What stop_reason indicates the agent wants to call a tool? | `tool_use` |
| What stop_reason indicates the agentic loop should exit? | `end_turn` |
| In the Anthropic API, what role carries tool_result content blocks back to Claude? | `user` |
| What guard should every production agent loop have? | A maximum iteration count to prevent runaway cost and infinite loops. |
