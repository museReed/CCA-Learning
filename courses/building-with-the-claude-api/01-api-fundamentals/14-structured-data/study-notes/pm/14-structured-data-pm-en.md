# Structured Data — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D5 — Enterprise Deployment (20%) — primary; D2 — Tool Design & MCP Integration (18%) — secondary |
| Task Statements | 5.3 (production patterns), 1.3 (prompt engineering), 2.1 (structured output) |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 14 |

---

## One-Liner

When your product needs raw data — a JSON object, a code snippet, a bullet list — with no chatty preamble, you use a two-part trick (prefill + stop sequence) to make Claude hand back clean output that users can copy-paste or that downstream systems can parse without extra work.

---

## Mental Model: The Vending Machine vs. the Friendly Barista

Think about two ways to get coffee:

| Interaction | Analogy | Output |
|-------------|---------|--------|
| Friendly barista | Default Claude | "Here's your latte! I added a little extra foam today, hope you love it. Let me know if you need anything else!" + coffee |
| Vending machine | Prefilled Claude | *click* → coffee |

Both deliver the coffee. But if you are a product that feeds the coffee into a pipe (downstream system), the barista's chatter clogs the pipe. Structured data techniques turn Claude into a vending machine for exactly the cases where chatter is friction instead of friendliness.

---

## The Product Problem

Imagine an AWS EventBridge rule generator: users type a description, click generate, and expect to click "copy" on clean JSON to paste straight into the AWS console. If Claude returns:

````
```json
{ ... }
```
This rule captures EC2 instance state changes when instances start running.
````

…then the "copy" button either:

1. Copies too much — user pastes markdown fences and an English sentence into AWS, which rejects it.
2. Requires custom parsing logic on the client — which fails when Claude phrases its explanation differently.

Both outcomes are a product quality bug. The structured-data technique removes this class of bug entirely.

---

## Product Use Cases

### When You Need Structured Output

| Product | What you need |
|---------|--------------|
| API response generator | Pure JSON body |
| Code generator / snippet tool | Clean code with no commentary |
| Config file builder (YAML, JSON, TOML) | Ready-to-save file content |
| Data extraction from unstructured text | Parseable JSON for a database |
| CSV / spreadsheet row generator | Rows ready for import |
| SQL query builder | Executable SQL, nothing else |

### When Chatty Output Is Fine

| Product | Why |
|---------|-----|
| Conversational chat | Users *want* context and friendliness |
| Tutoring app | The explanation IS the product |
| Summarizer | Prose is the output |
| Creative writing | Commentary can be part of the voice |

The test: will a human read the output, or will a machine parse it? If the latter, you need structured output.

---

## The Copy-Paste Test

Here's a simple PM test: if your feature has a "Copy" button, the output should be pasteable without editing. If the output Claude produces needs any manual cleanup before it's usable, your product is broken.

Apply this test during design review:

1. Generate a real response from Claude with your current prompt
2. Click "Copy"
3. Paste it into the target environment (AWS console, code editor, spreadsheet)
4. Does it work? If no, you need structured-data techniques.

This is a five-minute test that catches one of the most common AI product bugs before launch.

---

## PM Decision Framework

| Question | If "Yes" | Implication |
|----------|----------|-------------|
| Does the output feed a downstream parser or automated pipeline? | Yes | Must use structured output |
| Does the UI have a "copy" button? | Yes | Must use structured output |
| Will users compare responses to a specification (AWS rule, JSON schema)? | Yes | Must use structured output |
| Is the output meant for human reading only? | No | Default Claude is fine |
| Can users tolerate cleaning up the output themselves? | No | Must use structured output |

If any of the "yes" conditions apply, include "output must be clean, parseable [format]" as an acceptance criterion in the PRD.

---

## Trade-offs vs. Tool Use

Later in the course, tool use gives an alternative way to get structured JSON — Claude returns a tool-call object with schema-validated input. As a PM, understand the difference:

| Approach | Pros | Cons |
|----------|------|------|
| Prefill + stop sequence | Simple, works for any format (code, CSV, YAML, XML), no schema needed | No type validation; Claude can still emit malformed data |
| Tool use with `input_schema` | Schema validation, type safety, agent-style composability | More complex, JSON-only |

**PM rule of thumb:** For quick prototypes and non-JSON formats, prefill + stop sequence is fine. For production JSON generation that downstream systems depend on, insist on tool use with a schema.

---

## Common PM Mistakes

1. **Assuming Claude "just returns JSON"** — it returns JSON plus explanation by default. Structured-data techniques are required.
2. **Not testing copy-paste in the target environment** — the bug only appears when a real user tries to use the output.
3. **Putting "output clean JSON" in the system prompt and calling it done** — Claude still adds commentary. You need prefill + stop sequence or tool use.
4. **Not budgeting for retry logic** — even with prefill, Claude can occasionally emit malformed output. Production features need JSON parse retry.
5. **Using chatty output in an API response** — downstream integrators assume a contract; commentary breaks every consumer.

> **Key Insight**
>
> Structured data is not a nice-to-have — it is the difference between an AI feature that users can actually use in a downstream workflow and one that produces "almost usable" output. The prefill + stop sequence pattern is the simplest PM-facing recipe for "make Claude shut up and return just the thing." Know when to reach for it; know when tool use is the better answer.

---

## CCA Exam Relevance

- **D5.3 (production patterns)**: expect scenario questions asking how to get Claude to return pure JSON for downstream consumption.
- **D2 (Tool Design)**: tool use is the production-grade alternative for JSON — the exam may ask you to pick between them.
- Watch for phrasing like "Claude wraps output in markdown fences with explanation" — the answer is prefill + stop sequence (or tool use).

---

## Flashcards

| Front | Back |
|-------|------|
| What product problem do structured-data techniques solve? | Claude's default tendency to wrap structured output in markdown fences and add English commentary, which breaks downstream parsing and copy-paste UX. |
| What is the PM-level "copy-paste test"? | Generate a real response, click copy, paste into the target environment. If it doesn't work, your product needs structured output. |
| What are the two techniques combined to force clean structured output? | Assistant message prefilling and stop sequences. |
| When is chatty output the right choice? | Conversational chat, tutoring, summarization, creative writing — anywhere a human reads the output directly. |
| When is structured output mandatory? | Anywhere the output feeds a parser, automation pipeline, copy button, or has a schema contract. |
| What is the tradeoff vs. tool use? | Prefill works for any format without a schema; tool use only works for JSON but provides schema validation and type safety. |
| Why isn't "please return only JSON" in the system prompt enough? | Claude's helpful behavior still leaks commentary — you need structural enforcement, not just instructions. |
| What is the vending machine analogy? | Default Claude is a friendly barista who adds chat; prefilled Claude is a vending machine that hands over just the product. |
