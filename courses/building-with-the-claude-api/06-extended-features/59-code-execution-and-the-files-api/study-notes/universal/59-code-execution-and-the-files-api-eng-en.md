# Code Execution and the Files API — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.4 (server-side tools), 2.1 (tool schema design), 1.2 (multi-turn tool loops) |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 59 |

---

## One-Liner

The Files API lets you upload files once and reference them by ID in future requests, and the Code Execution tool is a server-side Python sandbox (isolated Docker container, no network) that Claude can drive — combined, they let you hand off real computational work to Claude without wiring a custom execution environment.

---

## Files API — Upload Once, Reference Many Times

Normally you embed files in messages as base64 (for images or PDFs). The Files API is an alternative: upload the file separately, get back a file metadata object with a unique **file ID**, and then reference that ID in future messages.

The flow:

1. Upload your file (image, PDF, text, CSV, etc.) via a dedicated API call.
2. Receive a file metadata object containing a **file ID**.
3. Reference the file ID in future messages instead of inlining raw file bytes.

Why this matters:

- You do not have to resend the file on every request — one upload, many references.
- Large files become cheap to reuse — no base64 bloat in each request.
- It is the primary way to get data *into and out of* the Code Execution sandbox, because the sandbox has no network access.

---

## Code Execution Tool — Server-Side Python Sandbox

Code Execution is a **server-side tool**. Unlike a normal client-side tool, you do not implement it yourself — you just declare the predefined tool schema in your request, and Claude can optionally execute Python code in an isolated environment.

The execution environment has very deliberate properties:

| Property | Detail |
|----------|--------|
| **Runtime** | Python in an isolated Docker container. |
| **Network access** | **None.** The container cannot make external API calls. |
| **Iteration** | Claude can execute code multiple times during a single conversation, iterating as the analysis unfolds. |
| **Integration** | Results are captured and interpreted by Claude for the final response. |
| **Implementation required** | **None on your side** — it is a server-side tool provided by Anthropic. |

The isolation is a feature, not a limitation: it means you can let Claude run code safely without exposing your infrastructure, keys, or network.

---

## Combining Files API + Code Execution

Because the Docker container has **no network access**, the Files API is the natural bridge: it is the primary way to get data *in* and generated artifacts *out*.

A typical workflow:

1. Upload your data file (e.g., a CSV) using the Files API.
2. Include a `container_upload` block in your message with the file ID so the sandbox receives the file.
3. Ask Claude to analyze the data.
4. Claude writes and executes Python code inside the container to process the file.
5. Claude can generate outputs (plots, reports) and make them available for download via the Files API.

This is a clean delegation pattern: you control the inputs and outputs, Claude handles the code.

---

## Practical Example: Churn Analysis

The lesson walks through a streaming-service dataset (`streaming.csv`) containing user information — subscription tiers, viewing habits, and churn labels.

First, upload the file with a helper function:

```python
file_metadata = upload('streaming.csv')
```

Then create a message that pairs a text instruction with a `container_upload` block referencing the uploaded file, and enable the code execution tool:

```python
messages = []
add_user_message(
    messages,
    [
        {
            "type": "text",
            "text": """Run a detailed analysis to determine major drivers of churn.
            Your final output should include at least one detailed plot summarizing your findings."""
        },
        {"type": "container_upload", "file_id": file_metadata.id},
    ],
)

chat(
    messages,
    tools=[{"type": "code_execution_20250522", "name": "code_execution"}]
)
```

Key pieces:

- The `container_upload` block is how you inject the uploaded file into the sandbox.
- The `tools` list contains a single entry with `type: "code_execution_20250522"` — this is the predefined server-side tool schema; you do not implement it.
- Claude receives both the instruction and the file reference and can now run Python to analyze it.

---

## Understanding the Response Structure

When Claude uses code execution, the response contains multiple block types interleaved:

| Block type | What it holds |
|-----------|---------------|
| **Text blocks** | Claude's analysis, reasoning, and natural-language explanations. |
| **Server tool use blocks** | The actual Python code Claude decided to run. |
| **Code execution tool result blocks** | The output from running the code (stdout, errors, file handles). |

Claude might execute code **multiple times** during a single response, iteratively building up its analysis (load → inspect → clean → plot → summarize). Each execution cycle appears as a `server tool use` block followed by a `code execution tool result` block.

---

## Downloading Generated Files

One of the most powerful features is Claude's ability to generate files (plots, reports, transformed CSVs) and make them downloadable. When Claude creates a visualization inside the container, it gets stored there and you can retrieve it via the Files API.

Look for blocks with `type: "code_execution_output"` in the response — these contain file IDs for the generated content. You then use a Files API call to download them:

```python
download_file("file_id_from_response")
```

This completes the round trip: CSV in (via Files API), plot out (via Files API), with Claude doing all the pandas/matplotlib work in between.

---

## Beyond Data Analysis

While churn analysis is the canonical example, the combination opens up many other delegation patterns:

- **Image processing and manipulation** — resize, convert, extract features.
- **Document parsing and transformation** — PDF extraction, format conversion, redaction.
- **Mathematical computations and modeling** — simulations, optimizations, statistical tests.
- **Report generation with custom formatting** — build HTML or PDF outputs from raw data.

The underlying pattern is the same: the Files API controls the *data boundary*, Code Execution handles the *computation*, and Claude orchestrates both through natural language.

---

## Common Mistakes

1. **Forgetting the sandbox has no network access** — writing code that tries to `requests.get(...)` will fail; data must come in via the Files API.
2. **Inlining large files when a file ID would do** — base64-embedding a big CSV on every request wastes tokens and cost; upload once and reference by ID.
3. **Assuming you must implement the code execution tool** — it is server-side. You only declare the schema; Anthropic runs the Python.
4. **Missing generated outputs** — failing to scan the response for `code_execution_output` blocks means you never see the plots and reports Claude produced.
5. **Expecting the sandbox to persist across sessions** — the container is ephemeral; file IDs from the Files API are the durable handle, not container state.
6. **Not iterating** — Claude is allowed to run code multiple times in a single response; designing your handler to only expect one execution block will miss data from the later ones.

---

> **Key Insight**
>
> Code Execution is a **server-side tool with zero client implementation** — you declare the schema, Claude runs Python in an isolated container, you read the result blocks. The Files API is the data boundary that replaces the container's missing network. Together they let you delegate entire computational workflows to Claude: upload data in, get analysis and artifacts out, without ever standing up your own execution infrastructure.

---

## CCA Exam Relevance

- **D2 (Tool Design)** — Code Execution is the canonical **server-side tool** example. Know that you do not implement it; you declare `{"type": "code_execution_20250522", "name": "code_execution"}` in the `tools` list and Claude runs Python for you.
- **D1 (Agentic Architecture)** — multi-turn code execution (Claude executes code multiple times in one response) is an agentic loop running entirely on the server side.
- Know the sandbox properties: isolated Docker container, no network access, Python runtime, ephemeral.
- Know that the Files API is the in/out bridge: files go in via `container_upload`, artifacts come out via `code_execution_output` → `download_file(file_id)`.

---

## Flashcards

| Front | Back |
|-------|------|
| What does the Files API let you do? | Upload a file once (image, PDF, CSV, etc.), receive a file ID, and reference that ID in future messages instead of inlining raw file data. |
| Is Code Execution a client-side or server-side tool? | Server-side — you do not implement it; you declare the predefined schema and Claude runs Python in an isolated container. |
| What runtime and environment does Code Execution use? | Python inside an isolated Docker container with **no network access**. |
| Why is the Files API essential when using Code Execution? | Because the sandbox has no network access, so the only way to get data in and artifacts out is to upload/download through the Files API. |
| What block type injects an uploaded file into the sandbox? | `container_upload` with the `file_id` from a Files API upload. |
| What tool schema entry enables code execution? | `{"type": "code_execution_20250522", "name": "code_execution"}` in the `tools` list. |
| Can Claude execute code multiple times in a single response? | Yes — iteratively, interleaving text, server tool use blocks, and code execution result blocks. |
| Which three block types appear in a code execution response? | Text blocks (Claude's explanations), server tool use blocks (the Python code), and code execution tool result blocks (the output). |
| How do you retrieve a file Claude generated inside the container? | Look for `code_execution_output` blocks containing file IDs, then call `download_file(file_id)` via the Files API. |
| Name three non-data-analysis use cases for Code Execution + Files API. | Image processing and manipulation, document parsing and transformation, mathematical computation and modeling, report generation with custom formatting. |
