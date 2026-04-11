# Tool Functions — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.2 (tool function definition), 2.1 (tool schema design), 1.2 (agentic loop foundation) |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 34 |

---

## One-Liner

A tool function is just a plain Python function — but one whose inputs, error messages, and behavior are intentionally designed to be read and recovered from by an LLM, not only by human developers.

---

## What Is a Tool Function?

A tool function is a normal Python callable that your application will invoke when Claude emits a `tool_use` block requesting it. There is nothing magical on the Python side — the magic is in the **contract** between the function and the LLM:

- Clear name → Claude picks the right function
- Clear parameter names → Claude fills the right arguments
- Validation + descriptive errors → Claude can self-correct on the next turn
- Predictable return types → Claude can reason about the result

The tool function is the bottom of the stack. The JSON schema (Lesson 35) is the documentation Claude reads. The agentic loop calls the function with the arguments Claude supplied.

---

## The First Tool: `get_current_datetime`

```python
from datetime import datetime

def get_current_datetime(date_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)
```

Three things worth unpacking:

1. **Default argument** (`date_format="%Y-%m-%d %H:%M:%S"`) — lets Claude call the function with zero arguments in the common case. The schema declares the parameter optional.
2. **Validation before use** — `if not date_format: raise ValueError(...)` protects against a degenerate value that Python would otherwise silently accept (empty string is "truthy" enough that `strftime("")` returns `""`).
3. **`strftime` format pass-through** — you delegate date formatting to Python's battle-tested `datetime` module rather than reimplementing.

### Usage examples

```python
get_current_datetime()           # "2026-04-11 14:30:25"
get_current_datetime("%H:%M")     # "14:30"
get_current_datetime("%A")        # "Saturday"
```

---

## Best Practices for Tool Functions

### 1. Descriptive Names

Function name: `get_current_datetime` — a human immediately understands the intent. Contrast with `gcdt` or `datetime_fn`. Claude uses the name as a strong prior when deciding whether to call this function.

Parameter names: `date_format` — not `fmt` or `d`. Every character is documentation that Claude reads.

### 2. Validate Inputs

```python
def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)
```

Common validation patterns:

- Empty strings (`if not s`) — surprisingly easy for an LLM to emit
- Wrong types (`if not isinstance(x, int)`) — especially after JSON deserialization
- Out-of-range values (`if not 0 <= p <= 100`)
- Format mismatches (regex, enum membership)

The key question to ask for each parameter: "what is the worst input an LLM might generate that would silently produce a wrong answer?" Validate against that.

### 3. Meaningful Error Messages

**Bad**: `raise ValueError("invalid input")`
**Good**: `raise ValueError("date_format cannot be empty")`
**Better**: `raise ValueError("date_format cannot be empty; use a valid strftime pattern like '%Y-%m-%d'")`

Error messages are Claude's only feedback channel. Every error message is a mini-prompt telling the next turn how to recover. If you write "invalid input", Claude might retry with the same invalid input. If you write "expected an ISO-8601 date like 2026-01-15, got 'next Friday'", Claude knows exactly how to fix it.

This is the biggest shift from traditional error-message design: your errors are no longer just for humans — they are LLM recovery signals.

---

## How Tool Functions Integrate with the Loop

```python
# pseudo-code for the agent loop
while True:
    response = client.messages.create(..., tools=tool_schemas, messages=messages)

    if response.stop_reason != "tool_use":
        break  # final text response is in response.content

    for block in response.content:
        if block.type != "tool_use":
            continue
        fn = TOOL_REGISTRY[block.name]
        try:
            result = fn(**block.input)
            tool_result_content = str(result)
            is_error = False
        except Exception as e:
            tool_result_content = f"Error: {e}"
            is_error = True

        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": tool_result_content,
                "is_error": is_error,
            }],
        })
```

Key observations:

- Catch exceptions and surface them as `tool_result` with `is_error: True`. Do not let exceptions break your loop — Claude can recover if told.
- `**block.input` unpacks the JSON arguments. Type mismatches get caught at the Python call site.
- The `TOOL_REGISTRY` is a simple dict from tool name to function pointer. Keeps dispatch trivial.

---

## Type Hints Help Both Humans and Schemas

Python type hints are optional at runtime but extremely useful at design time:

```python
def get_current_datetime(date_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    ...
```

- They make the schema (Lesson 35) trivial to derive.
- They catch developer bugs before runtime.
- They signal intent to teammates reviewing code.
- Libraries like `inspect` and `pydantic` can auto-generate JSON Schema from type-hinted functions.

---

## Common Mistakes

1. **Ambiguous function names** — `process`, `run`, `do_it`. Claude cannot infer purpose from a vague name.
2. **Silent failure on bad input** — accepting `None` or empty string without validating, producing garbage output.
3. **Cryptic error messages** — "error 42" tells Claude nothing; "radius must be positive, got -3" tells Claude exactly how to fix it.
4. **Not catching exceptions at the loop level** — letting a tool exception crash the entire conversation instead of feeding it back as a `tool_result` error.
5. **Hidden side effects** — a tool that silently writes to a database without making it clear in the name is dangerous; prefer `create_reminder` over `reminder`.
6. **Returning complex objects without `str()`** — `tool_result.content` must be serializable text; convert rich objects to strings or JSON explicitly.

> **Key Insight**
>
> Tool functions are not "internal helpers" — they are part of the public API you are exposing to Claude. Every parameter name, every error message, every return type is read by the model. Treat tool functions like a well-documented SDK, because that is how Claude sees them. This is a frequent exam angle for D2 on the CCA.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: naming, validation, error messages as LLM-readable recovery signals, default arguments.
- **D1 (Agentic Architecture)**: exception handling inside the tool loop; how errors turn into tool_result blocks.
- Expect questions like: "why should tool functions raise descriptive errors?" — answer: so Claude can self-correct on the next turn.

---

## Flashcards

| Front | Back |
|-------|------|
| What is a tool function? | A plain Python callable that Claude invokes when it emits a `tool_use` block; the function must validate inputs and return a serializable result. |
| Why do tool function error messages matter so much? | Because they are Claude's only feedback channel — Claude reads them and uses them to self-correct its next `tool_use` call. |
| What is a bad tool function name? | Anything vague like `process`, `run`, or `do_it` — Claude cannot infer the function's purpose. |
| What happens if a tool function raises an exception inside the agent loop? | The caller should catch it and return a `tool_result` with `is_error: True` — do not let it break the loop. |
| Why use default arguments in a tool function? | So Claude can call it with minimal input in the common case and only supply parameters when needed. |
| What does `get_current_datetime` validate and why? | It rejects empty `date_format` so `strftime("")` does not silently return an empty string. |
| How should a tool function return rich objects? | Convert them to strings or JSON — `tool_result.content` must be serializable text. |
| What is the relationship between type hints and schemas? | Type hints enable auto-generation of JSON Schema and give Claude (via the schema) and humans clear intent. |
