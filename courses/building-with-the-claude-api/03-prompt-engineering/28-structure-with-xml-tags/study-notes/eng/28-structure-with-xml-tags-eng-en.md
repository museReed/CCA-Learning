# Structure with XML Tags — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation & Iteration (20%) — primary; D2 — Tool Design (18%) — secondary |
| Task Statements | 3.1 (prompt design for reliability), 2.2 (structured content blocks) |
| Source | building-with-the-claude-api / 03-prompt-engineering / Lesson 28 |

---

## One-Liner

XML tags act as explicit delimiters inside a prompt string, letting Claude parse which bytes are instructions, which are data, and which are examples — the simplest and most reliable structural technique in prompt engineering.

---

## The Problem: Byte Soup

When you concatenate instructions, 20 pages of sales records, and a user question into a single prompt string, Claude sees one long undifferentiated sequence of tokens. Without boundaries, it must infer structure from prose cues alone. This inference is fragile:

- Instructions bleed into data
- Data bleeds into examples
- Claude may "follow" text that was meant to be analyzed, not executed

The source lesson frames this as a parsing problem: Claude "can sometimes struggle to understand which pieces of text belong together or what different sections are supposed to represent."

XML tags solve this by putting explicit markers in the token stream. `<sales_records>...</sales_records>` tells Claude: everything inside is one logical unit of a specific kind.

---

## The Canonical Example

From the lesson, the athlete meal-plan prompt:

```
<athlete_information>
- Height: 6'2"
- Weight: 180 lbs
- Goal: Build muscle
- Dietary restrictions: Vegetarian
</athlete_information>

Generate a meal plan based on the athlete information above.
```

Three things are happening:

1. **Semantic grouping** — height, weight, goal, and restrictions are bound together inside one container.
2. **Role separation** — the instruction ("Generate a meal plan...") sits outside the tag, so there is zero ambiguity about what is data and what is directive.
3. **Referability** — the instruction can literally say "the athlete information above," matching the tag name.

---

## Code vs Docs: The Dramatic Case

The source highlights a second example: asking Claude to debug code with provided documentation. Mixing both into one blob creates a "Not Great" version where it is nearly impossible for Claude to distinguish code tokens from prose tokens. The "Better" version wraps each section:

```
<my_code>
def calculate_total(items):
    return sum(item.price for item in items)
</my_code>

<docs>
The Item class has fields: name (str), price (float), quantity (int).
Prices are stored in cents as integers.
</docs>

Using the documentation above, find the bug in my_code.
```

Now Claude knows: parse `my_code` as Python, consult `docs` as ground truth, find the mismatch (the docs say price is an integer in cents, but the code treats it as if the sum is final).

---

## Custom Tag Names Matter

The lesson is explicit that you do not need "official" XML. The tag names are semantic hints, so more specific is better:

| Weak | Strong | Why |
|------|--------|-----|
| `<data>` | `<sales_records>` | Tells Claude what kind of data |
| `<info>` | `<athlete_information>` | Disambiguates from any other info |
| `<text>` | `<customer_review>` | Implies domain (sentiment, tone) |
| `<input>` | `<my_code>` / `<docs>` | Distinguishes co-located content |

Rule of thumb: if you can name the variable in your application code, use that exact name as the tag.

---

## When XML Tags Are Most Valuable

Straight from the source, XML is most useful when:

- Including large amounts of context or data
- Mixing different types of content (code, documentation, data)
- You want to be extra clear about content boundaries
- Working with complex prompts that interpolate multiple variables

For a one-line prompt ("Translate to French: hello"), tags are overkill. The payoff scales with prompt complexity.

---

## Python Pattern: String Interpolation Safely

```python
from anthropic import Anthropic

client = Anthropic()

athlete_info = """- Height: 6'2"
- Weight: 180 lbs
- Goal: Build muscle
- Dietary restrictions: Vegetarian"""

prompt = f"""<athlete_information>
{athlete_info}
</athlete_information>

Generate a meal plan based on the athlete information above."""

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}],
)
```

Notice the interpolation point is entirely inside the tag. User-supplied data cannot leak into the instruction region, which also helps limit prompt-injection surface area: an attacker who inserts text can contaminate `athlete_information`, but the directive outside the tag is fixed.

---

## Common Mistakes

1. **Vague tag names** — using `<data>` or `<text>` instead of something descriptive like `<sales_records>`. Claude cannot exploit a hint that is not there.
2. **Forgetting closing tags** — an unclosed `<my_code>` may cause Claude to treat the rest of the prompt as code.
3. **Mixing multiple sections without tags** — co-locating code and docs with no delimiters is the exact failure case the lesson warns about.
4. **Over-tagging trivial prompts** — wrapping a one-sentence request in XML adds noise without benefit.
5. **Assuming XML changes output format** — tags structure the input; they do not automatically make Claude reply in XML. That requires a separate instruction.

> **Key Insight**
>
> XML tags are the cheapest reliability upgrade in prompt engineering. They do not change what Claude can do; they change how confidently it can tell your instructions apart from your data. On the CCA exam, any scenario involving "large context," "multiple data types," or "Claude is confusing instructions with content" points to XML structuring as the answer.

---

## CCA Exam Relevance

- **D3 (Evaluation & Iteration)**: XML tagging is a first-line iteration move when evals show Claude misinterpreting input. Expect scenario questions where a prompt fails because of ambiguous boundaries.
- **D2 (Tool Design)**: the same delimiting principle applies to `tool_use` / `tool_result` content blocks — structured channels beat free-form strings.
- Watch for the word "interpolating" or "mixing" in questions; the canonical answer is "use XML tags to delimit each section."

---

## Flashcards

| Front | Back |
|-------|------|
| What problem do XML tags solve in prompts? | They mark explicit boundaries so Claude can distinguish instructions from data and from examples. |
| Do XML tag names have to be from a standard? | No — descriptive custom names like `<sales_records>` or `<athlete_information>` are preferred. |
| When are XML tags most valuable? | Large context, multiple content types, complex prompts with interpolated variables. |
| Give a weak vs strong tag name pair. | Weak: `<data>`; Strong: `<sales_records>`. |
| What is the canonical code-vs-docs example? | Wrap code in `<my_code>` and documentation in `<docs>`, then ask Claude to debug using the docs. |
| Do XML tags change the output format of the response? | No — they structure the input only. Output format requires its own instruction. |
| What is the prompt-injection benefit of XML tags? | User-supplied data stays inside a tag region, so directives outside the tag are harder to override. |
| Is XML necessary for trivial prompts? | No — the payoff scales with prompt complexity; for one-line prompts it adds noise. |
