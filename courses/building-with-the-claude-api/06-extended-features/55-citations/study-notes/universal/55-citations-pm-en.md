# Citations — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D4 — AI Safety & Alignment (20%) — primary; D2 — Tool Design & MCP Integration (18%) — secondary |
| Task Statements | 4.2 (grounded outputs), 2.2 (content blocks), 5.4 (trust and verifiability) |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 55 |

---

## One-Liner

Citations are the trust layer for any Claude feature where users need to know "where did this answer come from?" — they turn Claude from a black box into a research assistant that shows its work.

---

## Mental Model: The Research Assistant With Receipts

Imagine hiring a research assistant to read a stack of contracts and summarize them. Two scenarios:

- **Without citations**: the assistant hands you a summary and says "trust me." You have no way to verify it, and if the summary is wrong you cannot tell which document misled them.
- **With citations**: every sentence in the summary has a footnote pointing at the exact clause in the exact contract. You can spot-check any claim in seconds.

Citations are footnotes for Claude. The cost is slightly more complex response handling; the payoff is a feature users are willing to trust with real decisions.

---

## Why PMs Should Care

Citations are the single feature that makes high-stakes document features shippable. Without them:

- Legal teams will not use an AI contract reviewer.
- Compliance will not approve a policy-QA tool.
- Doctors will not rely on a clinical reference assistant.
- Financial analysts will not trust extraction from a 10-K.

With them, all of those features suddenly clear the bar. Users can verify any claim before acting on it. Auditors have a traceable trail. Customer-facing products can say "here is the source" instead of "please trust our AI."

If your product exists in a regulated, high-stakes, or enterprise setting, citations are almost never optional.

---

## Product Use Cases

### When Citations Are Required

| Product Context | Why Citations Are Mandatory |
|-----------------|-----------------------------|
| Legal research, contract review | Lawyers must cite source clauses for any assertion |
| Clinical decision support | Clinicians need to verify the source guideline before acting |
| Financial analysis | Auditors demand a traceable evidence chain |
| Regulatory / compliance QA | Regulators require proof the answer came from the policy text |
| Enterprise knowledge search | Internal users want to jump from answer to source document |
| Academic or research tools | Researchers cannot cite a source they cannot point at |

### When Citations Are Optional

| Product Context | Why |
|-----------------|-----|
| Casual chat / creative writing | No grounded source is involved |
| Brainstorming with Claude's general knowledge | The source would be the training data, which is not citable |
| Summaries of content the user provided verbally | No written document to cite |
| Internal prototypes without shipping commitments | Pay the complexity cost only when trust is a requirement |

---

## PM Decision Framework

When designing a document-grounded feature, ask:

| Question | If Yes | Implication |
|----------|--------|-------------|
| Will users make decisions based on Claude's answer? | Yes | Citations are almost certainly required. |
| Is the workflow regulated (legal, medical, financial, compliance)? | Yes | Citations are mandatory — ship them with the first release. |
| Will internal auditors or external reviewers see Claude's output? | Yes | Citations produce the trail they need. |
| Can users tolerate the slight UI complexity of citation markers? | Yes | Build a hover-to-verify pattern. |
| Does the feature use multiple documents per request? | Yes | `document_index` and `document_title` matter; track them in the UI. |
| Are we working with plain-text RAG chunks instead of PDFs? | Yes | Citations still work — they return character positions instead of pages. |

---

## Cost, Complexity, and UX Trade-offs

Citations are one of the cheapest high-impact features in the API. The costs:

- **Slightly more complex response handling.** Engineering must iterate over content blocks and surface citation metadata to the UI.
- **A modest token overhead** per call, because Claude emits citation metadata alongside text.
- **UX design work** to create the hover-and-verify pattern.

The benefits:

- **Trust.** Users will actually rely on the output.
- **Regulatory clearance.** Legal and compliance teams can approve features they would otherwise block.
- **Fewer hallucination incidents.** Citations surface when Claude is drawing from the document vs. reaching outside it — a natural sanity check.
- **Better UX for drill-down.** Users who want more context can jump to the source paragraph or page.

For any enterprise document feature, the cost-benefit is a near-slam-dunk. For consumer features on general knowledge, citations often do not apply.

---

## The PDF + Citations Canonical Stack

Pair lesson 54 (PDF support) with lesson 55 (citations) and you have the canonical Claude-based enterprise document stack:

1. PDF content block with `citations.enabled: True` and a readable `title`.
2. A precise extraction or QA prompt.
3. A UI that renders the answer with inline citation markers and hover popovers.
4. Optional: prompt caching on the document bytes for repeat queries.

This is the shortest path from "we have a pile of PDFs" to "we have a shippable enterprise feature users trust." Every document-workflow PRD should reference this pairing explicitly.

---

## Common PM Mistakes

1. **Treating citations as optional for high-stakes features.** They are not. Users in regulated workflows will not adopt the feature without them.
2. **Enabling citations in the API but not displaying them in the UI.** You pay the cost, get no trust benefit, and confuse the engineering team about why they exist.
3. **Forgetting the `title` field.** Multi-document responses become ambiguous and users cannot tell which document a citation came from.
4. **Assuming citations guarantee correctness.** A citation proves the source text exists; it does not prove Claude's paraphrase is faithful. Review for interpretation errors is still needed on high-stakes answers.
5. **Not handling plain-text RAG chunks.** If your pipeline surfaces text chunks, citations still work — but they return character positions instead of page numbers. Your UI has to branch on source type.
6. **Underestimating the UX design work.** Citation markers, hover popovers, jump-to-source, and "no citation available" fallback states all need explicit design.

---

> **Key Insight**
>
> Citations are the minimum viable trust mechanism for any Claude feature grounded in documents the user cares about. They are cheap to enable, expensive to skip: without them, enterprise and regulated features rarely clear the trust bar, and users fall back on reading the source themselves. Pair citations with PDF support and you get the canonical enterprise document stack in one request.

---

## CCA Exam Relevance

- **D4 (AI Safety & Alignment)**: citations are the standard mechanism for grounded, verifiable outputs. Expect questions framed around trust and source transparency.
- **D2 (Tool Design & MCP Integration)**: know the API shape — `title` field, `citations.enabled` flag, citation metadata structure (`cited_text`, `document_index`, `document_title`, page or character positions).
- Exam scenario pattern: "Users need to verify Claude's document answer." The answer is enabling citations on the document block and surfacing `cited_text` in the UI.

---

## Flashcards

| Front | Back |
|-------|------|
| What is the research assistant analogy for citations? | Without citations, the assistant says "trust me"; with citations, every sentence has a footnote pointing at the exact source clause so you can spot-check it. |
| When are citations mandatory? | In regulated or high-stakes workflows: legal, medical, financial, compliance, enterprise knowledge, academic or research tools. |
| When are citations optional or irrelevant? | Casual chat, creative writing, brainstorming on general knowledge, or summaries of content the user only provided verbally. |
| What does a PM need to design for a citations UX? | Inline markers, hover popovers with `cited_text` and `document_title`, jump-to-source actions, and fallback states for no-citation segments. |
| What is the minimum-viable enterprise document stack? | PDF content block + citations enabled + precise prompt + UI with citation markers + optional prompt caching for repeat queries. |
| Why are citations cheap to enable but expensive to skip? | Enabling costs a small token overhead and modest UI work; skipping means high-stakes features cannot clear trust and compliance bars. |
| Do citations guarantee Claude's answer is correct? | No. They prove Claude read a specific source passage, not that Claude's interpretation of that passage is accurate. Human review is still needed on consequential answers. |
| What should a citations PRD spec? | Trust requirements (who needs to verify), UX pattern for markers and popovers, handling of multiple documents, plain-text vs PDF source type, and a fallback for missing citations. |
