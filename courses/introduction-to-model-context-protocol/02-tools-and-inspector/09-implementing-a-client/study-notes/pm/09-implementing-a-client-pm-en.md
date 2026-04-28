# Implementing a Client — PM Strategic Overview

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | T2.2 Implement MCP client-server communication; T2.4 Handle tool discovery and execution flows |
| Source | introduction-to-model-context-protocol / 02-tools-and-inspector / Lesson 09 |

---

## One-Liner

The MCP client is the orchestration layer in your product that coordinates between the user, Claude, and external services — like a project manager who knows who to ask for what and when.

---

## The Client as Project Manager

Think of the MCP client as a project manager coordinating a complex request:

1. **Intake** — A stakeholder (user) submits a request
2. **Resource survey** — The PM checks which teams (MCP servers) are available and what services they offer
3. **Expert consultation** — The PM presents the request and available resources to a decision-maker (Claude)
4. **Delegation** — The decision-maker says "have the data team pull this report" — the PM routes the request
5. **Delivery** — The PM collects the results and brings them back to the decision-maker for a final recommendation
6. **Response** — The decision-maker crafts a polished answer for the stakeholder

This six-step pattern is the core of every MCP-powered product interaction.

> **PM Takeaway**
> The client is the coordination layer, not the intelligence layer. Claude provides the intelligence (deciding what to do). The MCP server provides the capabilities (doing the work). The client connects them. This separation of concerns is key to understanding the architecture.

---

## The Two Essential Operations

Every MCP client does exactly two things with MCP servers:

### "What Can You Do?" (Discovery)

Before any work happens, the client asks each MCP server what tools it offers. This is like a PM's first meeting with a new vendor — "Show me your service catalog."

The response is a structured list of capabilities: tool names, descriptions, and what inputs each tool needs. This catalog gets passed to Claude so it can make informed decisions.

### "Please Do This" (Execution)

When Claude decides to use a tool, the client takes Claude's specific request and sends it to the right MCP server. This is like the PM sending a detailed work order to the vendor: "Run analysis X on dataset Y with parameters Z."

The server does the work and returns results, which the client passes back to Claude for interpretation.

> **PM Takeaway**
> These two operations — discovery and execution — are the only things the client does with MCP. If someone on your team describes a more complex interaction, they are likely describing multiple rounds of these same two operations.

---

## The Five-Step Product Flow

From a product perspective, every user interaction with MCP-powered tools follows five steps:

**Step 1: Discover capabilities** — Your product checks what tools are available. This happens automatically and invisibly to the user.

**Step 2: Present context to Claude** — Your product sends the user's question along with the tool catalog to Claude. Claude sees both what the user wants and what tools it has to work with.

**Step 3: Claude makes a decision** — Claude either answers directly (if no tools are needed) or decides to call a specific tool with specific inputs. This is the "AI judgment" step.

**Step 4: Execute the action** — Your product sends Claude's tool request to the appropriate MCP server. The server does the work — queries a database, fetches a file, runs a calculation.

**Step 5: Deliver the answer** — Your product sends the tool results back to Claude, which crafts a natural language response for the user.

The user sees none of this complexity. They ask a question and get an answer. The five steps happen in milliseconds to seconds.

> **PM Takeaway**
> Step 3 is where product quality is won or lost. Claude's ability to choose the right tool depends on the quality of tool descriptions (from the server) and the clarity of the user's question. Both are product design concerns.

---

## The Double-Call Pattern

A subtle but important aspect: the product makes two separate calls to Claude for every tool-using interaction.

**First call**: "User asks X. Here are the available tools. What do you want to do?"
**Claude responds**: "I want to call tool Y with input Z."

**Second call**: "Tool Y returned these results. Now please answer the user's original question."
**Claude responds**: "Based on the data, here is the answer..."

This double-call pattern has product implications:

- **Latency**: Two API calls means longer response times when tools are involved
- **Cost**: Two Claude API calls per interaction (important for pricing models)
- **Quality**: The second call benefits from concrete data, often producing better responses than the first call alone could

> **PM Takeaway**
> When estimating response times and API costs for your product, remember that tool-using interactions require two Claude API calls. Non-tool interactions require only one. Your product's mix of these two types determines overall performance and cost.

---

## Error Scenarios Product Teams Should Understand

Four types of failures can occur, each with different user-facing implications:

1. **Tool not found** — The tool Claude requested does not exist. Usually a configuration issue.
2. **Invalid input** — Claude sent the wrong type of data to a tool. Usually a tool description clarity issue.
3. **Server error** — The MCP server or external service failed. Infrastructure issue.
4. **Transport error** — Connection between client and server was lost. Network issue.

Each requires different error handling and different user messaging.

---

## CCA Exam Relevance

This lesson completes **Domain 2 (18%)**:

- The client uses two SDK classes: Client (connection) and ClientSession (communication)
- Two essential methods: `list_tools()` and `call_tool()`
- The five-step agentic flow from discovery to final response
- The double-call pattern (two Claude API calls per tool-using interaction)
- Error handling: check `result.isError` for tool-level failures

---

## Flashcards

| Front | Back |
|-------|------|
| What is the MCP client's role in business terms? | It is the coordination layer — like a project manager who surveys available resources, presents options to a decision-maker (Claude), and routes execution requests. |
| What are the only two operations an MCP client performs with MCP servers? | Discovery (asking what tools are available) and Execution (calling a specific tool with specific inputs). |
| What are the five steps of the MCP product flow? | 1) Discover capabilities, 2) Present context to Claude, 3) Claude decides, 4) Execute the action, 5) Deliver the answer. |
| Why does tool-using interaction require two Claude API calls? | First call: Claude receives the query and tools, decides what to do. Second call: Claude receives the tool results and crafts a final response. |
| What are the cost implications of the double-call pattern? | Every tool-using interaction costs two Claude API calls instead of one, which affects pricing models and usage projections. |
| Which step in the five-step flow determines product quality? | Step 3 (Claude's decision) — it depends on tool description quality and user question clarity, both of which are product design concerns. |
| What are the four types of MCP client errors? | Tool not found (config), Invalid input (description clarity), Server error (infrastructure), Transport error (network). |
| What does the user experience during the five-step MCP flow? | Nothing. They ask a question and get an answer. All five steps happen transparently in milliseconds to seconds. |
