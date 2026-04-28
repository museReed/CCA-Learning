# The Web Search Tool — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%), D4 — AI Safety & Alignment (20%) |
| Task Statements | 2.3 (built-in server tools), 4.2 (grounding & citations) |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 43 |

---

## One-Liner

Adding web search to your product is now a one-config-line decision: Anthropic handles the searching, the parsing, and the citations — your team only has to render the result blocks in your UI.

---

## Mental Model: Research Assistant With a Library Card

Before server tools, giving an AI access to the web meant building a search pipeline, scraping, cleaning, ranking, and citation extraction — like hiring a researcher and also setting up their entire library. The web search tool is like handing your research assistant a library card: they know how to use it, they bring back sources, and every claim has a footnote.

| Capability | Build It Yourself | Use Web Search Tool |
|------------|-------------------|---------------------|
| Search infrastructure | Weeks of engineering | Ships today |
| Content parsing | Custom per source | Handled |
| Citation formatting | Custom logic | Built-in blocks |
| Domain restriction | Custom allowlists | `allowed_domains` field |
| Ongoing maintenance | Your team forever | Anthropic |

The speed-to-market is typically 10-100x faster.

---

## Why Citations Are a Product Feature

The web search tool does not just return search results — it returns **citations** that quote the exact source text supporting each statement. For product, this changes everything:

- **Trust**: users see where answers come from, not just raw generation
- **Compliance**: regulated industries require source traceability
- **Auditing**: internal users can verify Claude's reasoning
- **Liability reduction**: "Claude said so" becomes "this verifiable source said so"

Ungrounded LLM output is a hard sell in healthcare, legal, finance, and government. Grounded output with citations unlocks these markets.

---

## Product Use Cases

### Clear Wins for Web Search Tool

| Product | Value |
|---------|-------|
| News-aware assistant | Fresh information after model cutoff |
| Medical info product | NIH/PubMed restriction + citations for safety |
| Legal research copilot | `.gov` / `.edu` restriction + verifiable quotes |
| Competitive intelligence | Current market data, not stale training data |
| Financial analyst assistant | Real-time stock / macro data with sources |
| Customer support for rapidly changing docs | Always-fresh answers |

### When to Not Use It

| Scenario | Better Alternative |
|----------|-------------------|
| Questions fully answerable from training data | Skip the tool — save cost & latency |
| Private / proprietary information | Use a custom retrieval tool against your own docs |
| Offline / air-gapped environments | Web search requires Anthropic backend connectivity |
| High-volume, latency-sensitive endpoints | Every search adds time; budget carefully |

---

## Key Configuration Levers for PMs

### 1. `max_uses` — Cost and Latency Ceiling

Claude may run follow-up searches to refine answers. `max_uses` caps this.

- **1-2**: Cheap, fast, may miss nuance
- **3-5**: Standard range for research use cases
- **10+**: Deep research; budget carefully

### 2. `allowed_domains` — Content Quality Lever

This is the most under-appreciated PM control:

- Restricting to PubMed turns a generic health bot into an evidence-based medical assistant
- Restricting to SEC filings turns a chatbot into a compliant financial info tool
- Restricting to your own docs turns it into a grounded internal knowledge base

Domain restriction is how you build **trust** into the product.

### 3. Console Privacy Setting

Web search must be enabled at the organization level in the Anthropic console under privacy settings. PMs should add this to environment setup checklists.

---

## PM Decision Framework

| Question | If Yes | Action |
|----------|--------|--------|
| Do users ask about current events / fresh info? | Yes | Enable web search |
| Is content quality and trust critical? | Yes | Set `allowed_domains` tightly |
| Do answers need citations for compliance? | Yes | Render citation blocks prominently |
| Is this a latency-sensitive endpoint? | Yes | Lower `max_uses`; consider caching |
| Is the data private / internal? | Yes | Build a custom retrieval tool instead |

---

## Rendering Matters

The response returns several block types — text, search results, citations. These are not interchangeable:

1. Show **web search results** as a "Sources" list (trust signal, visible at a glance)
2. Show **citation blocks** as inline links within the answer (proof for each claim)
3. Show **text blocks** as the main answer content

Products that merge everything into raw text lose the trust advantage. Products that render the blocks distinctly gain measurable trust and click-through.

---

## Common PM Mistakes

1. **Treating web search as a backend concern** — the citation rendering is a core UX decision; own it.
2. **Leaving `allowed_domains` empty for sensitive topics** — medical, legal, and financial products need domain restriction from day one.
3. **Not measuring citation click-through** — it is the key trust metric; instrument it.
4. **Setting `max_uses` too high "just in case"** — cost and latency compound with every follow-up search.
5. **Forgetting the console privacy toggle** — your staging / production environments silently fail if the org setting is off.

> **Key Insight**
>
> Web search is a fully managed server tool: Anthropic owns the execution, you own the rendering. The product value is **grounded, cited, fresh answers** with almost no engineering investment. Invest the saved time in great citation UI, because that is where trust is earned.

---

## CCA Exam Relevance

- **D2 (Tool Design)**: Web search is the canonical "server tool" — fully executed by Anthropic. Know the contrast with text editor (local execution).
- **D4 (AI Safety & Alignment)**: Citations and grounding are trust mechanisms; questions may ask which tool provides built-in citations.
- Watch for scenario questions comparing self-built search vs. server tool — the server tool is almost always the right answer unless the data is private.

---

## Flashcards

| Front | Back |
|-------|------|
| Who executes the web search tool? | Anthropic — it is a fully managed server tool; you write no local code |
| What field caps the number of searches per request? | `max_uses` |
| What field restricts searches to specific domains? | `allowed_domains` |
| What product value comes from citation blocks? | Grounded, verifiable answers — users can click through to the source of each statement |
| What must be enabled in the Anthropic console before using web search? | The web search tool under organization privacy settings |
| Why is `allowed_domains` important for regulated industries? | It constrains Claude to authoritative sources (e.g., NIH for medical, `.gov` for legal), improving trust and compliance |
| Name two product scenarios where web search is the wrong choice. | Private / proprietary data; offline environments |
| What is the main UX lever for trust when using web search? | Rendering citation blocks prominently — inline with answers and as a sources list |
