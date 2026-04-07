# Log and Progress Notifications — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server capabilities), 2.5 (server-to-client communication) |
| Source | model-context-protocol-advanced-topics / 01-sampling-and-notifications / Lesson 05 |

---

## One-Liner

MCP servers can send real-time status updates and progress indicators to clients during long operations, turning silent black-box processing into transparent, user-friendly experiences.

---

## Mental Model: Restaurant Kitchen

Think of an MCP tool as a restaurant kitchen:

| Without Notifications | With Notifications |
|----------------------|-------------------|
| You order food and wait in silence | Waiter says "Your appetizer is being prepared" |
| 20 minutes pass — is it coming? | "Main course is in the oven, 10 minutes left" |
| You consider leaving | "Plating now — almost ready!" |
| Food arrives (or doesn't) | Food arrives, and you felt informed the whole time |

Notifications do not change the food. They change the **dining experience**.

---

## Two Types of Real-Time Feedback

| Type | What It Does | Analogy |
|------|-------------|---------|
| **Logging** | Status messages during processing ("Searching databases...", "Found 42 results") | Waiter giving verbal updates |
| **Progress** | Completion percentage (30%, 60%, 90%) | Progress bar on a delivery tracking page |

Both are **optional** — the tool works without them. But they dramatically improve perceived performance and user trust.

---

## Why PMs Should Care

### 1. User Perception of Speed

Research consistently shows that tasks with progress indicators feel faster than identical tasks without them, even when they take the same time. For AI tools that may run 10-60 seconds, this is critical.

### 2. Reduced Abandonment

Users who see no feedback during a long operation will:
- Assume the tool is broken
- Retry (creating duplicate work)
- Abandon the workflow entirely

### 3. Debugging and Support

Logging gives your support team visibility into what happened during a failed operation, without asking the user to reproduce the issue.

---

## Product Design Implications

When writing requirements for MCP tools, consider:

| Tool Duration | Recommended UX |
|--------------|----------------|
| < 2 seconds | No notifications needed |
| 2-10 seconds | Logging messages ("Searching...", "Processing...") |
| 10-60 seconds | Logging + Progress bar |
| > 60 seconds | Logging + Progress + Consider breaking into smaller steps |

---

## Client Presentation Flexibility

The server sends raw data. Different clients present it differently:

| Client Type | How Logging Shows Up | How Progress Shows Up |
|-------------|---------------------|----------------------|
| Terminal/CLI | Text lines printed to stdout | ASCII progress bar |
| Web application | Toast notifications or log panel | HTML/CSS progress bar |
| Desktop app | System notification area | Native OS progress ring |
| Chat interface | Inline status messages | Animated loading indicator |

> **Key Insight**
> As a PM, you specify **what information** to communicate (steps, percentages, warnings). You do NOT need to specify **how** it is displayed — that is the client's responsibility. This separation of concerns means one well-designed server works beautifully across all client types.

---

## Notifications Are Fire-and-Forget

A critical architectural detail for PMs to understand:

- Notifications are **one-way**: server sends, does not wait for acknowledgment
- If the client ignores them, nothing breaks
- They do NOT affect the tool's actual output
- They add minimal overhead to processing time

This means you can always recommend adding notifications — there is no downside.

---

## Error Communication Strategy

Logging levels map to user-facing communication tiers:

| Level | When to Use | User Experience |
|-------|------------|-----------------|
| Debug | Internal details (URLs, record counts) | Usually hidden from end users |
| Info | Major milestones ("Step 2 of 4 complete") | Shown to users as status |
| Warning | Degraded performance ("Large dataset, may be slow") | Alert — user can decide to wait |
| Error | Failure ("Database connection lost") | Error message — user takes action |

---

## Acceptance Criteria Template

For any tool that takes > 2 seconds, include in your PRD:

```
Given: User initiates [tool name]
When: Processing takes longer than 2 seconds
Then: Client receives logging notifications for each major step
And: Client receives progress updates at least every 5 seconds
And: Final notification confirms completion or reports failure
```

---

## CCA Exam Relevance

- **D2 Task 2.3**: Server capabilities — notifications are optional but expected in well-designed servers
- **D2 Task 2.5**: Server-to-client communication — logging and progress are primary examples
- Exam tests understanding that notifications are one-way (not request-response)
- Key philosophy: **Good UX is not optional** — even infrastructure tools should communicate status

---

## Flashcards

| Front | Back |
|-------|------|
| What two types of real-time feedback can MCP servers send? | Logging (status messages) and Progress (completion percentage) |
| Are MCP notifications required for tool functionality? | No — they are optional but highly recommended for UX |
| What happens if a client ignores notifications? | Nothing breaks — notifications are fire-and-forget |
| Why do progress indicators matter for AI tools? | Users perceive tasks with progress feedback as faster and are less likely to abandon |
| Who decides how notifications are displayed? | The client — the server sends raw data, each client renders it appropriately |
| At what tool duration should a PM recommend adding notifications? | For any operation exceeding 2 seconds |
| What are the four logging levels? | Debug (internal), Info (milestones), Warning (degraded), Error (failure) |
| Can notifications change a tool's return value? | No — they are purely informational side-channel communication |
