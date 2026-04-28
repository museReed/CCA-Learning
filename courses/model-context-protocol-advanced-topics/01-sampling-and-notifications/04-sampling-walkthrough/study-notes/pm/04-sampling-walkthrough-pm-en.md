# Sampling Walkthrough — PM Quick-Scan

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Model Context Protocol (23%) |
| Task Statements | 2.2 (MCP primitives), 2.3 (sampling) |
| Source | model-context-protocol-advanced-topics / 01-sampling-and-notifications / Lesson 04 |

---

## One-Liner

Sampling is the mechanism that lets an MCP server ask the client to generate AI text on its behalf -- think of it as a "callback to headquarters" where the field agent (server) requests intelligence from command (client) during a mission.

---

## Why PMs Need to Know Sampling

Sampling changes the usual flow of MCP. Normally, clients ask servers to do things (run tools, read resources). With sampling, the direction reverses: the server asks the client to generate text. This matters for product design because:

1. **Server-side intelligence** -- Your server tools can incorporate AI reasoning mid-execution
2. **Client controls the LLM** -- The client decides which model to use and how to call it
3. **Human-in-the-loop potential** -- The client could insert approval steps before generating text

---

## Mental Model: Restaurant Kitchen

| Role | MCP Equivalent | What Happens |
|------|---------------|--------------|
| Kitchen (server) | MCP Server tool | Realizes it needs a recommendation for a dish pairing |
| Waiter running back to sommelier | Sampling request | Server sends a message asking for text generation |
| Sommelier (client + LLM) | Client's sampling callback | Generates the wine recommendation using expertise |
| Waiter returns with answer | `CreateMessageResult` | Server receives the generated text and continues |

The key insight: the kitchen (server) never talks to the sommelier (LLM) directly. It always goes through the waiter (client callback).

---

## The Six-Step Flow

1. **Server needs AI text** -- During a tool call, the server decides it needs LLM-generated content
2. **Server sends a request** -- Provides messages describing what it needs
3. **Client receives the request** -- Its pre-registered callback activates
4. **Client generates text** -- Uses whatever AI model and SDK it prefers
5. **Client sends back the result** -- Formatted as a standard MCP result
6. **Server continues** -- Uses the generated text to complete its task

---

## Product Design Implications

| Consideration | Impact |
|--------------|--------|
| **Model choice stays with the client** | Your server does not need to know which LLM is being used -- it just asks for text |
| **Cost control** | The client can enforce token limits, choose cheaper models, or cache responses |
| **Security** | API keys stay on the client side; the server never sees them |
| **Multi-step workflows** | A single tool call can make multiple sampling requests, enabling complex reasoning chains |
| **Format conversion required** | MCP message formats differ from LLM SDK formats -- engineering must handle this translation |

---

## When to Use Sampling in Your Product

| Scenario | Why Sampling | Alternative |
|----------|-------------|-------------|
| Server tool needs to summarize retrieved data | Server can request summarization mid-tool-execution | Return raw data and let client summarize (less elegant) |
| Multi-agent orchestration | Sub-agent (server) can ask for reasoning from the main agent (client) | Build all logic into one monolithic client |
| Content generation pipeline | Server handles workflow steps, delegates writing to LLM via client | Hard-code templates instead of AI generation |

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "The server calls the LLM directly" | No -- the server asks the client, which calls the LLM |
| "Sampling uses the same message format as Anthropic's API" | No -- MCP has its own message types that need conversion |
| "The server chooses the model" | No -- the client's callback determines the model |
| "Sampling is automatic" | No -- the client must explicitly register a callback |

---

## CCA Exam Relevance

- D2 frequently tests the **direction of the sampling flow** (server initiates, client executes)
- Expect scenario questions where a server tool needs intelligence -- the correct answer involves sampling
- The exam tests understanding that the client controls model selection and API keys
- Questions may present a scenario where sampling is missing and ask you to identify the root cause (missing callback registration)

---

## Flashcards

| # | Question | Answer |
|---|----------|--------|
| 1 | In MCP sampling, which component initiates the text generation request? | The server initiates it during a tool execution |
| 2 | Which component actually calls the LLM in sampling? | The client, via its sampling callback |
| 3 | Does the server know which LLM model the client uses? | No -- model selection is entirely the client's responsibility |
| 4 | Why is format conversion needed during sampling? | MCP uses its own message types that differ from LLM SDK formats (e.g., Anthropic) |
| 5 | Where do API keys for the LLM reside in the sampling flow? | On the client side only -- the server never sees them |
| 6 | What happens if the client does not register a sampling callback? | Sampling requests from the server will fail |
| 7 | Can a server make multiple sampling calls in one tool execution? | Yes -- it can chain multiple requests for complex workflows |
| 8 | How does sampling affect cost control? | The client controls token limits, model choice, and caching, giving full cost control |
