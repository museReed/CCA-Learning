# Extended Thinking — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 1.1 (reasoning depth and agent decision quality), 1.2 (agentic loop), 5.2 (latency/cost trade-offs) |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 52 |

---

## One-Liner

Extended thinking gives Claude dedicated "scratch paper" tokens to reason through a hard problem before emitting its final answer, trading higher cost and latency for improved accuracy on tasks that ordinary prompting cannot reliably solve.

---

## The Problem: When Prompt Engineering Stops Working

Every serious Claude deployment eventually hits a class of prompts where iteration on instructions, examples, and guardrails stops moving the accuracy needle. The model produces a plausible answer, but on hard reasoning problems that answer is not consistently right. Extended thinking exists for exactly this moment — it is the feature you turn on **after** you have optimized your prompt and eval suite and still need more headroom.

Think of it as Claude's scratch paper: the model writes its reasoning to an internal working area, and only after that work is done does it produce the final response. You pay for the scratch paper in tokens, and you wait longer for the answer, but the final answer is informed by a much longer internal deliberation.

---

## Response Structure: Two Blocks Instead of One

With extended thinking disabled, a Claude response is a simple text block. With extended thinking enabled, the response becomes structured — you get back both a **thinking block** (the reasoning trace) and a **text block** (the final answer).

This changes how your application handles responses. Code that assumes `response.content[0].text` now has to iterate through content blocks and distinguish thinking content from user-facing text. If you render Claude's output directly to a user, you must decide whether to show the thinking process, hide it, or collapse it behind a "show reasoning" toggle.

---

## Enabling Thinking in Code

The course teaches a minimal wrapper that exposes two new parameters on your chat function: `thinking` (boolean switch) and `thinking_budget` (max tokens Claude may spend on reasoning).

```python
def chat(
    messages,
    system=None,
    temperature=1.0,
    stop_sequences=[],
    tools=None,
    thinking=False,
    thinking_budget=1024,
):
    ...
```

Inside the function, when `thinking` is on you inject a `thinking` config block into the API parameters:

```python
if thinking:
    params["thinking"] = {
        "type": "enabled",
        "budget": thinking_budget,
    }
```

Then you call it:

```python
chat(messages, thinking=True)
```

Two hard constraints apply:

- **Minimum budget is 1024 tokens.** You cannot ask for a smaller scratch pad.
- **`max_tokens` must be greater than `thinking_budget`.** The thinking budget is *part of* the token budget Claude is allowed to spend, so `max_tokens` must leave room for both the reasoning trace and the final answer.

---

## The Signature System

Extended thinking responses carry a cryptographic **signature** over the thinking content. The signature is how Anthropic detects tampering: if a developer modifies the thinking text and passes it back into a later turn, the signature will no longer validate and the model will reject it.

The reason this matters is a safety guarantee. Claude's reasoning is part of how Anthropic's alignment training works — if developers could edit the reasoning text between turns, they could steer the model into unsafe territory by forging a "chain of thought" that justifies dangerous outputs. The signature prevents that attack vector.

Practical implication: **never mutate thinking blocks.** When you carry conversation history forward to the next turn, round-trip thinking blocks byte-for-byte, signature included.

---

## Redacted Thinking Blocks

Sometimes Claude's internal safety systems flag the reasoning trace itself. When that happens you do not receive the raw reasoning text — you receive a **redacted thinking block** containing an encrypted payload in place of readable text.

Two things matter here:

1. **Do not crash on redacted blocks.** Your content-block handler must treat redacted thinking as a valid variant alongside regular thinking and text blocks.
2. **Pass them back intact.** Even though your code cannot read the redacted content, Claude can decrypt it on the next turn, so passing the encrypted payload preserves context. Dropping it silently truncates Claude's memory.

The course mentions that for testing purposes there is a special trigger string you can send to force a redacted response. Use it to exercise your handler and confirm nothing downstream assumes every thinking block is readable.

---

## Cost and Latency Trade-offs

Extended thinking is not free:

- **Higher cost.** Thinking tokens are billed. A 1024-token thinking budget on every call is real money at scale.
- **Higher latency.** The model literally spends more wall-clock time before emitting its first text token.
- **More complex client code.** Content-block iteration, signature handling, redacted-block fallback.

The guidance is to treat thinking as an accuracy lever you pull **after** standard prompting. The decision process is:

1. Write the prompt.
2. Build an eval set.
3. Iterate on the prompt until accuracy plateaus.
4. If accuracy is still below your bar, enable thinking and re-run the eval.

If thinking fixes it, ship. If it does not, the problem is not a reasoning-depth problem and you need a different approach (tools, RAG, better prompt structure).

---

## Feature Compatibility Caveat

The course explicitly notes that extended thinking is **not compatible** with certain other features, notably **assistant message pre-filling** and custom **temperature**. This matters in production: if your existing prompt strategy relies on pre-filled assistant messages to steer output format, you cannot simply layer thinking on top. You have to redesign that part of the prompt.

The full incompatibility list is maintained in the Anthropic docs; the lesson points at that reference rather than embedding the list, because it evolves with new models.

---

## Common Mistakes

1. **Enabling thinking before optimizing the prompt.** Thinking costs money and latency. If your prompt is simply wrong, thinking will not fix it — you will just pay more for the same wrong answer.
2. **Setting `max_tokens` ≤ `thinking_budget`.** The API will reject the call. `max_tokens` must accommodate both the thinking trace and the final answer.
3. **Mutating thinking blocks between turns.** Any modification breaks the signature and Claude will reject the history.
4. **Crashing on redacted thinking blocks.** Treat redacted as a first-class variant; do not assume thinking content is always readable text.
5. **Showing raw thinking to end users without a toggle.** The reasoning trace is verbose and internal. Surface it intentionally or hide it by default.
6. **Combining thinking with pre-filled assistant messages or custom temperature without checking compatibility.** The call will fail or behave unexpectedly.

---

> **Key Insight**
>
> Extended thinking is an accuracy lever, not a default. The right workflow is: optimize the prompt first, build evals, and only then enable thinking when the eval gap is clearly a reasoning-depth problem. The signature system and redacted blocks are safety features — treat thinking blocks as opaque, pass them through untouched, and never assume they are readable text.

---

## CCA Exam Relevance

- **D1 (Agentic Coding & Architecture)**: extended thinking is the canonical way to deepen Claude's reasoning inside an agentic loop. Expect questions on when thinking helps (hard reasoning) vs. when it is wasted spend (simple transformations).
- **D5 (Enterprise Deployment)**: cost/latency trade-offs, `thinking_budget` vs `max_tokens` constraint, and feature-compatibility caveats are exam-ready facts.
- Watch for exam questions framed as: "Prompt engineering has plateaued — what is the next lever?" The answer is extended thinking with an eval-driven decision.
- Remember the two safety mechanisms: **signature** (tamper detection) and **redacted blocks** (internal safety flagging), and that both must be passed back untouched.

---

## Flashcards

| Front | Back |
|-------|------|
| What problem does extended thinking solve? | Hard reasoning problems where ordinary prompt engineering has plateaued — it gives Claude scratch-paper tokens to deliberate before answering. |
| What is the minimum `thinking_budget`? | 1024 tokens. |
| What is the relationship between `max_tokens` and `thinking_budget`? | `max_tokens` must be strictly greater than `thinking_budget`, because the budget is spent from within the max. |
| What are the two content block types you get back when thinking is enabled? | A thinking block (the reasoning trace) and a text block (the final answer). |
| What is the signature on a thinking block and why does it exist? | A cryptographic token that proves the thinking content has not been modified; it prevents developers from forging reasoning to steer the model unsafely. |
| What is a redacted thinking block? | A thinking block whose reasoning has been flagged by internal safety systems and is returned in encrypted form. Your code must handle it and pass it back untouched. |
| When should you enable extended thinking? | Only after you have optimized the prompt, built evals, and confirmed accuracy is still below your bar due to reasoning depth. |
| Name two features extended thinking is NOT compatible with. | Assistant message pre-filling and custom temperature. |
| What are the three trade-offs of enabling extended thinking? | Higher cost (thinking tokens are billed), higher latency (more wall-clock time), and more complex client code (block iteration, signatures, redaction). |
