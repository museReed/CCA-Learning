# Tool Schemas — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.1 (tool schema design), 2.2 (tool function definition), 1.2 (agentic loop foundation) |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 35 |

---

## One-Liner

A tool schema is a JSON Schema document with three top-level fields (`name`, `description`, `input_schema`) — it is the public API contract your Python function exposes to Claude, and its prose quality determines whether Claude picks the right tool and calls it with the right arguments.

---

## The Three Required Fields

Every tool definition sent to the Anthropic API must include:

| Field | Type | Purpose |
|-------|------|---------|
| `name` | string | The identifier Claude uses to reference the tool. Must match the function registry key. |
| `description` | string | 3–4 sentences telling Claude what the tool does, when to use it, and what it returns. |
| `input_schema` | JSON Schema object | The JSON Schema describing the function's arguments. |

These three fields become the contract Claude reads every time it decides whether to call the tool.

---

## Complete Example: `get_current_datetime`

```python
from datetime import datetime
from anthropic.types import ToolParam

def get_current_datetime(date_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)

get_current_datetime_schema: ToolParam = {
    "name": "get_current_datetime",
    "description": (
        "Returns the current date and time formatted according to "
        "the specified format string. Use this whenever you need to "
        "know the current moment in time, for example when a user "
        "asks what time it is or you need to timestamp a reminder. "
        "Returns a string formatted per Python's strftime codes."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": (
                    "A strftime format string such as '%Y-%m-%d %H:%M:%S'. "
                    "Defaults to ISO-style date and time if not provided."
                ),
                "default": "%Y-%m-%d %H:%M:%S",
            }
        },
        "required": [],
    },
}
```

Notice the **naming convention**: the function is `get_current_datetime`, and the schema variable is `get_current_datetime_schema`. Mirror pairs make it trivial to match function implementations with their schemas.

---

## Anatomy of `input_schema`

`input_schema` is a standard JSON Schema fragment. Three pieces matter most:

### 1. `type: "object"`

Tool inputs must always be objects (key-value maps of named arguments). This is because the API passes `input` as a JSON object that your code will unpack with `**block.input`.

### 2. `properties`

Each key in `properties` is a parameter name. Each value is a sub-schema describing the parameter's type, constraints, and — most importantly — its **description**.

```python
"properties": {
    "date_format": {
        "type": "string",
        "description": "A strftime format string...",
        "default": "%Y-%m-%d %H:%M:%S"
    }
}
```

The `description` on each property is your chance to tell Claude exactly what kind of value to send. Treat it like a docstring aimed at an LLM.

### 3. `required`

An array listing which parameter names are required. Parameters not in this list are optional, and Claude may omit them. Because `date_format` has a default, it is optional, so `required` is an empty list.

```python
"required": []              # all parameters optional
"required": ["city"]         # city is required, others optional
"required": ["city", "date"] # both required
```

---

## Why Description Quality Dominates Everything Else

Two tools with identical code but different descriptions will perform radically differently:

| Description | Outcome |
|-------------|---------|
| "Gets the time" | Claude may confuse it with other time tools; inconsistent usage. |
| "Returns the current date and time formatted per strftime codes. Use when the user asks 'what time is it' or when you need to timestamp a new record. Returns a formatted string." | Claude picks this tool correctly, supplies the right format, and interprets the result sensibly. |

**Best practices for descriptions:**

- 3–4 sentences (enough context, not a novel).
- State **what** it does and **what** it returns.
- State **when** Claude should use it (the "when" sentence is the most often skipped and the most valuable).
- Mention related tools to avoid confusion (e.g., "for converting a date string to a timestamp, see `parse_datetime`").
- For parameters, describe valid values, units, and format with concrete examples.

---

## Generating Schemas: Let Claude Do It

Instead of writing schemas by hand, you can have Claude generate them for you:

1. Copy the tool function code.
2. Ask Claude something like: *"Write a valid JSON schema spec for the purposes of tool calling for this function. Follow the best practices listed in the attached documentation."*
3. Attach the Anthropic tool-use documentation as context.
4. Paste the generated schema into your code, using the `{function_name}_schema` naming convention.

This is a meta-application of the tool-use principle: use the AI to build the AI's own inputs.

---

## Type Safety with `ToolParam`

The `anthropic` SDK exposes a `ToolParam` TypedDict you can use for compile-time (static analysis) checking:

```python
from anthropic.types import ToolParam

get_current_datetime_schema = ToolParam(
    name="get_current_datetime",
    description="Returns the current date and time...",
    input_schema={
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": "...",
                "default": "%Y-%m-%d %H:%M:%S",
            }
        },
        "required": [],
    },
)
```

Benefits:

- IDE autocomplete on the three required fields
- Mypy / pyright catches typos like `descripton` before runtime
- Self-documenting code for teammates

Not strictly required — the API accepts plain dicts — but strongly recommended for production code.

---

## JSON Schema Features Commonly Used in Tool Definitions

| Feature | Example | Purpose |
|---------|---------|---------|
| `type` | `"string"`, `"integer"`, `"boolean"`, `"array"`, `"object"`, `"number"` | Declare the JSON type |
| `description` | free text | LLM-readable per-parameter guidance |
| `default` | literal value | Used when Claude omits an optional param |
| `enum` | `["celsius", "fahrenheit"]` | Restrict to a fixed set of allowed values |
| `items` | schema | Describe array element types |
| `minimum` / `maximum` | numeric | Numeric ranges |
| `pattern` | regex | String format validation |
| `required` | array of names | Required property names |

`enum` is especially powerful: it takes ambiguity off the table by forcing Claude to pick from a defined set.

---

## Common Mistakes

1. **Missing `type: "object"`** — every `input_schema` must start with `type: "object"`, not just `properties`.
2. **Empty or vague descriptions** — "Gets data" gives Claude nothing to go on. Invest prose here.
3. **Forgetting `required`** — omitting it does not mean "all required"; it means "none required". Be explicit.
4. **Schema / function mismatch** — the schema says `city`, the function uses `location`. Claude will supply `city` and your code will crash.
5. **Over-constraining with patterns** — regex that rejects valid inputs you didn't anticipate blocks legitimate use.
6. **Putting implementation details in descriptions** — Claude does not need to know you call a SQLite DB; it needs to know what the tool does conceptually.

> **Key Insight**
>
> A tool schema is not mere wiring — it is an **LLM-readable API contract**. Every word in the description and every parameter annotation changes how Claude decides to call the tool. The engineering time you spend on schema descriptions pays off as fewer wrong tool picks, fewer malformed arguments, and fewer frustrated users. On the CCA exam, questions about `input_schema` structure and description best practices appear repeatedly under D2.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: structure of tool definitions (`name`, `description`, `input_schema`), JSON Schema basics, `required` semantics, enum usage.
- **D1 (Agentic Architecture)**: schema quality directly influences Claude's tool selection during the agent loop.
- **D5 (Enterprise Deployment)**: using `ToolParam` for type safety in production code.
- Expect questions like: "What are the three required fields in a tool definition?" or "How does Claude decide which tool to call when two tools exist?" — answer: description quality and name clarity.

---

## Flashcards

| Front | Back |
|-------|------|
| What are the three required fields in a tool definition? | `name`, `description`, and `input_schema`. |
| What must the top-level `type` of `input_schema` always be? | `"object"` — tool inputs are always JSON objects. |
| What does `required` mean in an `input_schema`? | An array of property names that must be supplied; parameters not listed are optional. |
| Why is description quality critical in a tool schema? | Claude reads the description to decide when to call the tool and how to fill its parameters — prose quality directly drives correctness. |
| What naming convention does the course recommend for schemas? | `{function_name}_schema` — mirror the function name so implementation and schema stay matched. |
| What is `ToolParam` and when should you use it? | A TypedDict from `anthropic.types` that adds static type checking to tool schemas; use it in production code for IDE and mypy support. |
| How can you generate a schema without writing JSON Schema by hand? | Ask Claude to generate one — paste the function code and the tool-use docs, and request a properly formatted schema. |
| Why use `enum` in a property schema? | To restrict Claude to a fixed set of valid values (e.g., `["celsius", "fahrenheit"]`), eliminating ambiguity. |
| What fails if the schema's parameter name does not match the Python function's parameter name? | The function call — Claude supplies the schema name, `**block.input` unpacks it into the function, and Python raises a `TypeError` for unexpected or missing arguments. |
