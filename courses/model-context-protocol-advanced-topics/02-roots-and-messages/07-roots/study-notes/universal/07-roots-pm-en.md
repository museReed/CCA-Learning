# Roots — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.2 (MCP security model), 2.3 (MCP server capabilities) |
| Source | model-context-protocol-advanced-topics / 02-roots-and-messages / Lesson 07 |

---

## One-Liner

Roots are MCP's way of telling a server "you may look here, and only here" — solving both the usability problem of file discovery and the security problem of unrestricted access.

---

![Roots Access](../../visuals/roots-access.svg)


## Mental Model: Building Security Badges

Think of roots like security badges in an office building:

| Concept | Office Analogy | MCP Equivalent |
|---------|---------------|----------------|
| Root | Badge grants access to Floor 3 and Floor 7 | Client says "you can access /projects and /data" |
| Server with roots | Employee with badge | Server knows which directories to search |
| Server without roots | Visitor with no badge | Must ask for exact room numbers (full file paths) |
| Enforcement | Turnstile at each floor | `is_path_allowed()` function (must be built) |

Key insight: **the badge itself does not lock the doors** — the turnstile does. Similarly, roots tell the server where it should go, but enforcement must be implemented separately.

---

## The Two Problems Roots Solve

### Problem 1: Usability

Without roots, users must provide exact file paths:
- "Read `/Users/reed/Documents/projects/my-app/src/components/Header.tsx`"

With roots, users just say:
- "Read Header.tsx"

The server knows to search within the approved directories.

### Problem 2: Security

Without roots, an MCP server could potentially access any file on the system:
- Personal documents, SSH keys, environment files with secrets

With roots, the server's scope is limited to approved directories.

> **Key Insight**
> Roots solve the same problem that "folder permissions" solve in Google Drive or Dropbox — they define the boundary of what a tool can see. As a PM, if your product handles files, roots are the mechanism for implementing least-privilege access.

---

## How the Flow Works (No Code)

1. **Client declares roots**: "This server can access my project folder and my data folder"
2. **Server discovers roots**: "I have access to two directories — let me search there"
3. **User makes a request**: "Find the config file"
4. **Server searches within roots**: Looks in project folder, then data folder
5. **Server finds and uses file**: Returns the config file contents

The user never types a full path. The server never looks outside approved directories.

---

## The Critical Security Gap

This is the most important detail for PMs to communicate to engineering:

**The MCP SDK does NOT automatically enforce root boundaries.**

The SDK provides the list of approved roots. But nothing technically prevents the server from ignoring that list and accessing other files. Your engineering team must build enforcement.

| What SDK Provides | What Your Team Must Build |
|-------------------|--------------------------|
| Root discovery mechanism | Access control validation |
| List of approved directories | Path traversal prevention |
| Standard URI format | Symlink resolution |

**PM Action Item**: In your PRD, explicitly require that file-accessing tools implement path validation. Do not assume the SDK handles it.

---

## Product Scenarios

### Scenario 1: Code Review Tool

A code review MCP server needs to read source files. Without roots:
- User must paste full file paths for every file
- Server might accidentally read `.env` files with API keys

With roots:
- Client points the server at the repository root
- Server searches naturally within the repo
- Files outside the repo are inaccessible (when enforced)

### Scenario 2: Multi-Project Workspace

A developer works on three projects. The client configures three roots:
- `/projects/frontend` (React app)
- `/projects/backend` (Python API)
- `/projects/shared` (shared libraries)

The server can search across all three without the user switching context.

---

## Security Checklist for PMs

When reviewing MCP tool designs that access files, verify:

- [ ] Server calls `list_roots()` before accessing files
- [ ] Path validation function exists (`is_path_allowed()`)
- [ ] Path traversal attacks are handled (resolving `..` and symlinks)
- [ ] Rejected access attempts are logged
- [ ] Users can see and modify their root configuration

---

## CCA Exam Relevance

- **D2 Task 2.2**: MCP security model — roots are the filesystem security mechanism
- **D2 Task 2.3**: Server capabilities — understanding how `list_roots()` enables file discovery
- Expect scenario questions: "A server accesses files outside approved roots. What went wrong?" Answer: enforcement was not implemented
- Key exam philosophy: **Validation > Trust** — the SDK trusts the server by default; your code must add validation

---

## Flashcards

| Front | Back |
|-------|------|
| What two problems do MCP roots solve? | Usability (no need for full file paths) and Security (limits server access to approved directories) |
| Does the MCP SDK automatically prevent servers from accessing files outside roots? | No — the SDK provides the root list but does not enforce boundaries; developers must implement validation |
| What is the PM's key action item regarding roots? | Explicitly require path validation in the PRD — do not assume the SDK handles it |
| What is the security analogy for roots? | Building security badges — they tell you where you can go, but the turnstile (enforcement code) must be built separately |
| How do roots improve user experience? | Users say "find config file" instead of typing full paths — the server searches within approved directories |
| Can a client configure multiple roots? | Yes — for example, pointing at multiple project directories simultaneously |
| What is the biggest security risk with roots? | A server that receives roots but does not validate paths against them — path traversal attacks can escape the root boundary |
| What exam philosophy applies to roots? | Validation > Trust — never assume the server will self-restrict; add programmatic enforcement |
