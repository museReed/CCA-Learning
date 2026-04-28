# The Web Search Tool — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%), D4 — AI Safety & Alignment (20%) |
| Task Statements | 2.3 (built-in server tools), 2.1 (tool schema), 4.2 (grounding & citations) |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 43 |

---

## One-Liner

The web search tool is a fully managed Anthropic server tool: you provide only a tiny schema stub, and Anthropic handles the search, result retrieval, and citation generation entirely on their infrastructure — no local implementation required.

---

## Key Distinction: Server Tool vs. Client-Executed Tool

Unlike custom tools (where you write both schema and implementation) or the text editor tool (where Claude knows the schema but you execute commands), the web search tool is a **server tool**:

| Tool Type | Who Defines Schema | Who Executes |
|-----------|---------------------|--------------|
| Custom tool | You | You |
| Text editor (built-in) | Anthropic | You |
| Web search (server tool) | Anthropic | **Anthropic** |

You do nothing at runtime. Claude calls out to Anthropic's web search backend and the results flow back through the API response.

---

## Prerequisite: Enable in Console

Before using web search, your Anthropic organization must enable it in the privacy settings:

```
https://console.anthropic.com/settings/privacy
```

This is an org-level opt-in. If the setting is off, requests including the web search tool will fail. PMs should treat this as a deployment checklist item for any environment that will use the tool.

---

## Declaring the Tool

The schema stub has three required fields:

```python
web_search_schema = {
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": 5,
}
```

| Field | Meaning |
|-------|---------|
| `type` | Versioned server tool identifier — must match the version for your model |
| `name` | Fixed: `web_search` |
| `max_uses` | Upper bound on the number of searches per request |

The `max_uses` cap matters because Claude may issue **follow-up searches** based on initial results. A single user question can turn into three or four queries as Claude refines its understanding. `max_uses` is your cost and latency ceiling.

---

## Restricting Search Domains

You can constrain which domains are searchable with `allowed_domains`:

```python
web_search_schema = {
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": 5,
    "allowed_domains": ["nih.gov"],
}
```

Use cases:

- **Medical advice** → restrict to PubMed / NIH for evidence-based sources
- **Legal research** → restrict to `.gov` or `.edu` domains
- **Company-specific data** → restrict to the company's official website
- **Academic** → restrict to peer-reviewed sources

Domain restriction is your primary lever for **content quality and trust**, not just search filtering.

---

## Response Block Types

A web-search-enabled response can contain several new block types alongside normal text:

| Block Type | Purpose |
|------------|---------|
| `text` | Claude's regular explanatory text |
| `ServerToolUseBlock` | Shows the exact search query Claude issued |
| `WebSearchToolResultBlock` | Contains the full search results returned |
| `WebSearchResultBlock` | An individual result (title + URL + snippet) |
| Citation blocks | Text quoted verbatim from sources, supporting Claude's statements |

Because the execution is server-side, the `ServerToolUseBlock` and `WebSearchToolResultBlock` are both returned in the same response — you do not do a second round trip.

```python
for block in response.content:
    if block.type == "text":
        render_text(block.text)
    elif block.type == "server_tool_use":
        log_query(block.input["query"])
    elif block.type == "web_search_tool_result":
        render_source_list(block.content)
```

---

## Citations and Grounding

Claude annotates its text output with **citation blocks** that include:

- The source domain and page title
- The source URL
- The specific quoted text supporting the claim

This enables true grounded generation: users can click through to the source and verify any statement. It also gives you a product surface — a "Sources" panel — that increases trust dramatically compared with ungrounded LLM responses.

---

## Rendering Pattern

The response block types are designed for specific UI elements:

1. **Text blocks** → regular content in the main answer area
2. **Web search result blocks** → a "Sources" list, typically above or beside the answer
3. **Citation blocks** → inline badges or footnotes, showing source domain and page title, linking out

Treat each block type as a different UI slot; do not merge them into a single string.

---

## When to Use the Web Search Tool

The lesson calls out four prime use cases:

- **Current events** — information after the model's training cutoff
- **Specialized information** not in Claude's training data
- **Fact-checking** and authoritative sourcing
- **Research tasks** requiring up-to-date information

When you include the schema in your tools array, Claude automatically decides whether a web search would help answer the question. You do not have to instruct Claude to use it; the model chooses based on the question content.

---

## Cost and Latency Considerations

- Each search adds latency (the server has to fetch, parse, and return results)
- `max_uses` bounds the number of searches per request — set it based on use case value
- Domain restriction can speed things up by narrowing the search surface
- Streaming still works; search blocks stream in the same event sequence as text

For high-volume production use, instrument:

- Average searches per request (watch for drift upward)
- Time to first text token with search enabled vs. disabled
- Citation click-through rate (a signal of user trust in sources)

---

## Common Mistakes

1. **Forgetting to enable web search in the console** — requests fail silently or return errors; check the org setting first.
2. **Setting `max_uses` too high** — runaway search chains on speculative questions can multiply cost and latency.
3. **Not rendering citations** — you lose the biggest product advantage of server tools: verifiable, grounded answers.
4. **Ignoring `allowed_domains` for sensitive topics** — medical, legal, and financial answers benefit massively from authoritative-source restriction.
5. **Trying to implement web search yourself when a server tool suffices** — re-implementing means more code, worse citations, and no built-in rendering blocks.

> **Key Insight**
>
> Server tools like web search are the fastest path to shipping production-grade AI features that need fresh or authoritative data. You ship a schema stub; Anthropic ships the entire execution, parsing, and citation pipeline. The only code you own is the UI that renders the response blocks.

---

## CCA Exam Relevance

- **D2 (Tool Design)**: Know that web search is a "server tool" where Anthropic executes the tool call; you never implement a function.
- **D4 (AI Safety & Alignment)**: Citations and grounding are key trust features; the exam tests the distinction between ungrounded LLM output and cited, sourced answers.
- Expect questions contrasting: custom tool (both), text editor (schema only), web search (neither — fully managed).

---

## Flashcards

| Front | Back |
|-------|------|
| What distinguishes a "server tool" from the text editor tool? | Server tools are executed entirely on Anthropic's infrastructure — you do not provide any local function |
| What fields does the web search schema stub require? | `type` (versioned), `name` (`web_search`), and `max_uses` |
| What does `max_uses` control? | The maximum number of searches Claude can run in a single request (for cost / latency control) |
| How do you restrict searches to specific domains? | Set `allowed_domains` in the schema, e.g. `["nih.gov"]` |
| What must you do in the Anthropic console before using web search? | Enable the web search tool under privacy settings |
| Name three new block types in a web-search response. | `ServerToolUseBlock`, `WebSearchToolResultBlock`, `WebSearchResultBlock`, plus citation blocks |
| What is the purpose of citation blocks? | They quote the specific source text supporting Claude's statements, enabling grounded, verifiable answers |
| When should PMs reach for the web search tool over a custom search integration? | When they need fresh / authoritative data and want automatic citation and grounding without building it themselves |
