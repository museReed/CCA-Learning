# Notifications Walkthrough — PM Quick-Scan

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Model Context Protocol (23%) |
| Task Statements | 2.2 (MCP primitives — notifications) |
| Source | model-context-protocol-advanced-topics / 01-sampling-and-notifications / Lesson 06 |

---

## One-Liner

MCP notifications let server tools communicate real-time status (logging) and progress updates to clients during long-running operations -- like a delivery driver sending live GPS updates and status messages while completing your order.

---

## Why PMs Need to Know Notifications

Notifications solve a fundamental UX problem: **what happens during long-running AI operations?** Without notifications, users stare at a spinner. With them, you can build:

- Progress bars showing task completion percentage
- Status messages explaining what the AI is doing right now
- Warning indicators when operations encounter issues
- Debug logs for troubleshooting

---

## Mental Model: Package Delivery Tracking

| Delivery Stage | MCP Notification | What User Sees |
|---------------|-----------------|----------------|
| "Order received, preparing..." | `ctx.info("Preparing to process...")` | Status message in UI |
| "Package is 40% of the way there" | `ctx.report_progress(40, 100)` | Progress bar at 40% |
| "Traffic delay on route" | `ctx.warning("Processing slower than expected")` | Warning banner |
| "Delivered!" | Tool returns result | Completion state |

---

## Two Notification Types

| Type | What It Communicates | PM Use Case |
|------|---------------------|-------------|
| **Logging** | Textual status messages at different severity levels (info, warning, debug, error) | Building activity feeds, status indicators, error alerts |
| **Progress** | Numerical completion (e.g., 20/100, 80/100) | Building progress bars, estimated time remaining |

---

## Architecture: Where Things Connect

This matters for PMs writing requirements because it affects how engineers structure the code:

| Component | Responsibility | PM Implication |
|-----------|---------------|----------------|
| Server tool | Emits logs and progress during execution | Server team decides what to report |
| Logging callback (on session) | Handles all log messages for the entire connection | Session-level feature -- always active |
| Progress callback (on tool call) | Handles progress for a specific tool call | Per-operation feature -- must be explicitly attached each time |

Key takeaway: If your requirement says "show progress for file conversion," the progress callback must be explicitly passed when calling that specific tool. It is not automatic.

---

## Product Scenarios

### Scenario 1: Video Processing Dashboard

**Requirement**: Show users a progress bar while their video is being converted.

**Implementation**: The video conversion tool on the server calls `ctx.report_progress()` at milestones (encoding started, 50% done, finalizing). The client receives these via the progress callback and updates the UI.

### Scenario 2: Multi-Step Research Agent

**Requirement**: Show users what the agent is doing at each stage of a research task.

**Implementation**: The server tool calls `ctx.info("Searching academic databases...")`, `ctx.info("Found 12 relevant papers...")`, `ctx.info("Generating summary...")`. Each message appears in the client's activity feed.

### Scenario 3: Error Monitoring

**Requirement**: Alert operations team when tool execution encounters issues.

**Implementation**: The server tool calls `ctx.warning()` or `ctx.error()` for degraded performance. The logging callback routes warnings to a monitoring dashboard.

---

## Notifications vs Other Approaches

| Approach | When to Use | When NOT to Use |
|----------|------------|-----------------|
| MCP Notifications | Real-time status during long tool execution | Quick operations that finish instantly |
| Tool return value | Final result only | When users need intermediate feedback |
| Polling from client | When server cannot push updates | When server supports notifications (MCP does) |
| WebSocket streams | Real-time bidirectional communication outside MCP | When already using MCP (use notifications instead) |

---

## CCA Exam Relevance

- D2 tests understanding of **where callbacks are attached** (logging on session, progress on tool call)
- Notification primitives are **fire-and-forget** -- the server does not wait for the client to acknowledge
- Exam questions may present a UX scenario and ask which notification type is appropriate (logging for messages, progress for numerical tracking)
- The `Context` object is automatically injected into tool functions -- it is NOT manually constructed

---

## Flashcards

| # | Question | Answer |
|---|----------|--------|
| 1 | What two types of notifications does MCP support? | Logging (textual messages) and Progress (numerical completion updates) |
| 2 | Where is the logging callback attached in the client code? | To the `ClientSession` constructor |
| 3 | Where is the progress callback attached? | To the specific `call_tool()` invocation |
| 4 | Why are they attached at different levels? | Logging applies to the whole session; progress is specific to each tool call |
| 5 | Are MCP notifications blocking or fire-and-forget? | Fire-and-forget -- the server does not wait for the client |
| 6 | What logging severity levels are available? | info, warning, debug, error |
| 7 | How does the server access notification methods? | Through the `Context` object, automatically provided as the tool function's last argument |
| 8 | What product problem do notifications solve? | User experience during long-running operations -- replacing blank spinners with real-time status |
