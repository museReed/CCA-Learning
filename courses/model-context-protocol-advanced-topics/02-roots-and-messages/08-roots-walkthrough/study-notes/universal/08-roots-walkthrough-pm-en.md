# Roots Walkthrough — PM Quick-Scan

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Model Context Protocol (23%), D4 — Security & Guardrails (15%) |
| Task Statements | 2.2 (MCP primitives — roots), 4.3 (access control) |
| Source | model-context-protocol-advanced-topics / 02-roots-and-messages / Lesson 08 |

---

## One-Liner

Roots are MCP's file system access control mechanism -- the user tells the client which directories a server can access, and the server must actively check those boundaries before touching any file. Think of it as a "visitor badge" system that limits which rooms a guest can enter.

---

## Why PMs Need to Know Roots

Roots directly impact **security requirements** and **user trust**:

1. **Access control is NOT automatic** -- The MCP SDK does not enforce boundaries. If your engineering team forgets to implement checks, the server can access any file.
2. **User-defined permissions** -- Users decide what directories to share. Your UX needs to communicate what they are granting access to.
3. **Compliance implications** -- If your product handles sensitive data, root validation is a security requirement, not a nice-to-have.

---

## Mental Model: Building Access Cards

| Building Security | MCP Roots |
|------------------|-----------|
| Visitor requests a badge | User specifies allowed directories via CLI |
| Reception creates the badge | Client creates `Root` objects with `file://` URIs |
| Guard checks badge at each door | Server calls `is_path_allowed()` before file access |
| Badge only works for specific floors | Root boundaries limit which directories are accessible |
| **No guard = anyone walks in** | **No authorization check = server accesses anything** |

The last row is the most important lesson: the badge (root) by itself does nothing. Without a guard (authorization check), it is just a piece of plastic.

---

## The Seven-Step Architecture

1. **User specifies directories** -- Via CLI arguments, config file, or UI
2. **Client creates Root objects** -- Converts paths to `file://` URIs
3. **Client registers a callback** -- Will return roots when asked
4. **Server requests roots** -- Calls back to the client when it needs to know allowed paths
5. **Server implements authorization** -- Checks every file access against roots
6. **Server provides roots to LLM** -- Via a tool or prompt so the AI knows what is available
7. **Server enforces boundaries** -- Blocks access to paths outside roots

---

## Product Design Implications

| Consideration | Impact |
|--------------|--------|
| **User awareness** | Users must understand what directories they are granting access to. Clear UX is critical. |
| **Default behavior** | Without roots, the server has no declared boundaries. Decide: deny-all-by-default, or require explicit configuration? |
| **Granularity** | Roots are directory-level. You cannot grant access to individual files via roots. |
| **Dynamic updates** | Roots can change during a session. Consider: should your product support adding/removing directories mid-session? |
| **Security is developer-enforced** | The MCP SDK provides no built-in enforcement. This MUST be in your engineering requirements. |

---

## Security Risk Matrix for PMs

| Risk | Likelihood without Roots | Impact | Mitigation |
|------|-------------------------|--------|------------|
| Server reads sensitive files (`.env`, credentials) | High | Critical | Mandatory root checks before all file reads |
| Server writes to system directories | Medium | Critical | Root validation on all write operations |
| User unknowingly grants broad access | Medium | High | Clear UX showing exactly which paths are shared |
| Developer forgets authorization check in new tool | High | Critical | Code review checklist, automated testing |

---

## Acceptance Criteria Template

For any feature involving MCP file access, your PRD should include:

- [ ] Server must validate all file paths against client-provided roots before access
- [ ] Access denied errors must return clear messages explaining the restriction
- [ ] UI must display which directories the user has granted access to
- [ ] New tools must include root validation (add to code review checklist)
- [ ] Test cases must verify that paths outside roots are rejected

---

## CCA Exam Relevance

- Roots span **D2** (MCP primitives) and **D4** (security/access control) -- expect cross-domain questions
- The most tested point: **MCP SDK does NOT auto-enforce roots**. If a question describes a security vulnerability in an MCP app, check whether authorization is missing.
- The callback pattern (on-demand root listing) is a D2 concept
- Path validation as a security requirement is a D4 concept
- Exam philosophy: **Validation > Trust** -- never assume the server will respect boundaries without explicit checks

---

## Flashcards

| # | Question | Answer |
|---|----------|--------|
| 1 | Who defines the roots in MCP? | The user/client -- not the server |
| 2 | Does the MCP SDK automatically prevent a server from accessing files outside roots? | No -- developers must implement authorization checks themselves |
| 3 | What URI scheme do roots use? | `file://` |
| 4 | At what granularity do roots operate? | Directory level -- not individual files |
| 5 | How does the server get the list of roots? | By making a request back to the client via a callback |
| 6 | What exam philosophy applies to root enforcement? | Validation > Trust -- always verify, never assume |
| 7 | What should a PM include in PRD acceptance criteria for file access features? | Mandatory root validation before all file operations |
| 8 | What is the biggest security risk if root validation is missing? | The server can read or write any file on the system, including credentials and sensitive data |
