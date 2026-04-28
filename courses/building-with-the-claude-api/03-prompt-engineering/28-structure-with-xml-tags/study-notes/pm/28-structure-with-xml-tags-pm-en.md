# Structure with XML Tags — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Evaluation & Iteration (20%) — primary; D2 — Tool Design (18%) — secondary |
| Task Statements | 3.1 (prompt design for reliability), 2.2 (structured content blocks) |
| Source | building-with-the-claude-api / 03-prompt-engineering / Lesson 28 |

---

## One-Liner

XML tags are the product-safe way to stitch user data into a prompt — they keep the AI focused on your instructions instead of accidentally reading the user's input as a new order.

---

## Why PMs Should Care

Every AI feature that interpolates user data into a prompt shares one failure mode: the user's content blurs into your instructions and Claude does the wrong thing. XML tags are the lowest-effort, highest-leverage fix.

| User Content Type | Without Tags | With Tags |
|-------------------|--------------|-----------|
| A long document | Claude treats the document as part of the instructions | Document is scoped inside `<document>` and analyzed as data |
| Code snippets | Claude confuses code syntax with natural-language directives | Code is scoped inside `<my_code>` and debugged as data |
| Forms with many fields | Field values blend into prose | All fields live in one `<athlete_information>` container |
| Mixed inputs (code + docs) | Claude cannot tell them apart | Each type gets its own tag |

This is essentially the same reason product forms have labels: telling the user (or the AI) what each field is for.

---

## Mental Model: Labelled Drawers in a Filing Cabinet

Imagine you drop 20 pages of sales records, 5 pages of company policy, and a question onto a colleague's desk in one pile. You will probably get back: "What am I looking at?"

Now imagine you drop the same material into a filing cabinet with three labelled drawers: **Sales Records**, **Company Policy**, **Question**. Your colleague opens the Question drawer, reads it, then pulls only the drawers they need.

XML tags are the drawer labels. `<sales_records>...</sales_records>` is literally a drawer in the prompt. The AI knows what to pull and what to leave.

---

## Product Use Cases

### When XML Tags Help the Most

| Scenario | Why Tags Matter |
|----------|----------------|
| Document summarizer | Raw document could be 20 pages — the instruction must not get lost inside it |
| Code review assistant | Code and documentation look different to humans but similar to a token stream |
| Meal-plan or workout generator | User profile has many fields that should be considered as one unit |
| Customer support triage | Ticket body and metadata need to stay distinct from the triage instructions |
| Multi-variable templates | Any slash command or template that interpolates 2+ variables |

### When XML Tags Are Overkill

| Scenario | Better Alternative |
|----------|--------------------|
| One-line translation or rewrite | Plain prompt — no structure needed |
| Freeform chat turn | Let the user's message be the user's message |
| Prompts that work fine in eval without tags | Don't add complexity without evidence |

---

## The Four Product Benefits

1. **Reliability** — the same template behaves consistently across very different user inputs, because the boundary between "what the user sent" and "what we told Claude to do" never shifts.
2. **Safer data handling** — user content is isolated inside a tagged region, giving you a natural place to sanitize, truncate, or log the interpolated block.
3. **Reduced prompt-injection surface** — instructions sit outside the tag; content sits inside. A malicious user who tries to inject new directives has to break out of the tag.
4. **Maintainability** — engineers reading the template can see exactly what variable goes where, just like a labelled form in a UI.

---

## PM Decision Framework

When reviewing a prompt template in a PRD or during design review, ask:

| Question | If Yes | Action |
|----------|--------|--------|
| Does the template interpolate user content? | Yes | Wrap it in a descriptive XML tag |
| Are there two or more types of input (code + docs, data + query)? | Yes | Each type gets its own tag |
| Can the interpolated content be large (a whole document)? | Yes | Tags are critical — the instruction must not get lost |
| Is the instruction short and the content long? | Yes | Tags make the instruction visible at the "top level" |
| Is the feature already passing evals without tags? | Yes | Don't over-engineer |

---

## Common PM Mistakes

1. **Treating XML as an engineer-only concern** — PMs should specify the tag structure in the PRD. The tag names are part of the product contract, not an implementation detail.
2. **Using generic tag names** — `<data>` tells Claude nothing. `<customer_review>` tells Claude "this is a review, apply sentiment reasoning." Push back on vague names.
3. **Forgetting tags when the prompt changes** — when a template adds a new interpolated field (e.g., `user_history`), it needs its own tag. This often regresses if the template grows without review.
4. **Not running evals before and after** — XML is a first-line reliability fix, but you still need eval data to prove it helped on your specific task.
5. **Confusing input tags with output format** — tags in the input do not automatically make Claude respond in XML. If you want XML output, that is a separate instruction.

> **Key Insight**
>
> XML tags are the "labelled form fields" of prompt engineering. For PMs, they turn a prompt from an opaque string into a structured template with named slots — something you can reason about, review, and evolve. On the CCA exam, the cue is "Claude is confusing instructions with content" or "the prompt interpolates large data"; the answer is always "add XML tags with descriptive names."

---

## CCA Exam Relevance

- **D3 (Evaluation & Iteration)**: XML tagging is a first-line iteration move when a prompt fails due to ambiguous boundaries.
- **D2 (Tool Design)**: the same "named channel" principle applies to tool inputs and tool results.
- Watch for scenario phrases like "large amount of context," "mixing code and documentation," or "interpolating multiple variables" — these all point to XML tags.

---

## Flashcards

| Front | Back |
|-------|------|
| In one sentence, what do XML tags do for a prompt? | They create labelled boundaries so Claude knows which tokens are data and which are instructions. |
| What is the filing-cabinet analogy for XML tags? | Tags are labelled drawers — Claude opens the drawer it needs instead of rifling through one big pile. |
| Name two product scenarios where XML tags are most valuable. | Document summarizers (large context) and code review assistants (mixed content types). |
| What makes a "good" XML tag name? | Descriptive and specific — `<sales_records>` or `<athlete_information>`, not `<data>`. |
| Why do XML tags reduce prompt-injection risk? | User content is isolated inside a tag region, so directives outside the tag are harder to override. |
| Do XML tags change the output format? | No — they structure the input; output format needs its own instruction. |
| When should a PM NOT insist on XML tags? | Trivial one-line prompts or features already passing evals cleanly without them. |
| Who should own the tag names in a PRD? | The PM — tag names are part of the product contract, not an implementation detail. |
