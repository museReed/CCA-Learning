# Claude Code Documentation — CCA D3 Reference Summary

> Sources: https://code.claude.com/docs (72 pages)
> CCA Relevance: D3 Claude Code Configuration & Workflows (20%)

## 1. Memory System (CLAUDE.md + Auto Memory)

### CLAUDE.md Hierarchy (highest → lowest priority)
| Scope | Location | Shared With |
|-------|----------|-------------|
| Managed policy | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | All org users |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team (via VCS) |
| User | `~/.claude/CLAUDE.md` | Just you |

- Files walk UP directory tree from CWD
- Subdirectory CLAUDE.md files load **on demand** when Claude reads files there
- CLAUDE.md is a **user message** (not system prompt) → no strict compliance guarantee
- Target **< 200 lines** per file; longer = more context, less adherence

### @Import Syntax
```
@path/to/import          # Relative to containing file
@~/.claude/my-rules.md   # Absolute path
```
- Max depth: 5 hops
- First external import requires user approval dialog

### .claude/rules/ Directory
- Each `.md` file = one topic (e.g., `testing.md`, `api-design.md`)
- Without `paths` frontmatter → loaded at launch (same priority as .claude/CLAUDE.md)
- With `paths` frontmatter → loaded only when matching files opened

```yaml
---
paths:
  - "src/api/**/*.ts"
---
# API rules here
```

### Auto Memory
- Claude writes notes for itself: build commands, debugging insights, patterns
- Storage: `~/.claude/projects/<project>/memory/`
- `MEMORY.md` first 200 lines / 25KB loaded at startup
- Topic files loaded on demand
- Toggle: `/memory` or `autoMemoryEnabled` setting
- Survives compaction (re-read from disk)

### Key Exam Points
- CLAUDE.md **fully survives** `/compact` (re-read from disk)
- Instructions given only in conversation are **lost** after compaction
- HTML comments in CLAUDE.md are **stripped** before context injection
- `claudeMdExcludes` setting skips irrelevant files in monorepos
- Managed policy CLAUDE.md **cannot be excluded**

---

## 2. Skills System

### What Skills Are
- SKILL.md + optional supporting files in a directory
- Claude uses them when relevant OR you invoke with `/skill-name`
- Follow [Agent Skills](https://agentskills.io) open standard

### Skill Locations (priority order)
1. Enterprise (managed settings)
2. Personal (`~/.claude/skills/<name>/SKILL.md`)
3. Project (`.claude/skills/<name>/SKILL.md`)
4. Plugin (`<plugin>/skills/<name>/SKILL.md`)

### Key Frontmatter Fields
| Field | Purpose |
|-------|---------|
| `name` | Slash command name |
| `description` | When to use (250 char truncation in listing) |
| `disable-model-invocation` | true = only user can invoke |
| `user-invocable` | false = hidden from / menu |
| `allowed-tools` | Tools available without permission prompt |
| `context` | `fork` = run in subagent |
| `agent` | Which subagent type (with context: fork) |
| `paths` | Glob patterns for auto-activation |
| `model` | Model override |
| `hooks` | Scoped lifecycle hooks |

### String Substitutions
- `$ARGUMENTS` — all args passed to skill
- `$ARGUMENTS[N]` or `$N` — positional args
- `${CLAUDE_SESSION_ID}` — session ID
- `${CLAUDE_SKILL_DIR}` — skill directory path

### Dynamic Context Injection
`` !`command` `` runs shell commands BEFORE content sent to Claude.

### Bundled Skills
| Skill | Purpose |
|-------|---------|
| `/batch <instruction>` | Large-scale parallel changes in worktrees |
| `/claude-api` | Load API reference for current language |
| `/debug` | Enable debug logging + troubleshoot |
| `/loop [interval] <prompt>` | Repeat prompt on schedule |
| `/simplify` | Three parallel review agents for code quality |

### Key Exam Points
- Skills vs CLAUDE.md: Skills load **on demand**, CLAUDE.md loads **every session**
- `.claude/commands/` merged into skills system; same functionality
- Description truncated to 250 chars; budget = 1% of context window
- `context: fork` = skill content becomes subagent's task (not access to conversation history)

---

## 3. Hooks System

### Hook Types
1. **Command** (`type: "command"`): Shell scripts, receive JSON on stdin
2. **HTTP** (`type: "http"`): POST JSON to endpoints
3. **Prompt** (`type: "prompt"`): Send to Claude for evaluation
4. **Agent** (`type: "agent"`): Spawn subagents for complex validation

### Key Lifecycle Events
| Event | When | Can Block? |
|-------|------|-----------|
| PreToolUse | Before tool execution | Yes (allow/deny/ask) |
| PostToolUse | After successful execution | Yes (block = prompt Claude) |
| UserPromptSubmit | Before Claude processes prompt | Yes |
| Stop | Main agent finished | Yes (force continuation) |
| SessionStart | New/resumed session | No (can add context) |
| SubagentStart/Stop | Subagent lifecycle | No |
| InstructionsLoaded | CLAUDE.md/rules loaded | No (observability) |

### Exit Codes (Command Hooks)
- **0**: Success, stdout parsed for JSON
- **2**: Blocking error, stderr fed to Claude
- **Other**: Non-blocking error, continues

### PreToolUse Decision Fields
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "Why",
    "updatedInput": {}
  }
}
```

### Key Exam Points
- Hooks = **deterministic enforcement** (vs CLAUDE.md = behavioral guidance)
- PostToolUse can **block** but tool already ran (data normalization use case)
- `matcher` uses regex on tool names
- MCP tools: `mcp__<server>__<tool>` pattern
- Hooks in settings.json vs in skill/agent frontmatter (scoped to component lifetime)

---

## 4. Subagents

### Built-in Subagents
| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| Explore | Haiku | Read-only | Codebase search/analysis |
| Plan | Inherit | Read-only | Plan mode research |
| General-purpose | Inherit | All | Complex multi-step tasks |

### Custom Subagent Locations
1. `--agents` CLI flag (session only, highest priority)
2. `.claude/agents/` (project)
3. `~/.claude/agents/` (personal)
4. Plugin `agents/` (lowest priority)

### Key Frontmatter Fields
| Field | Purpose |
|-------|---------|
| `tools` | Allowlist of tools |
| `disallowedTools` | Denylist (applied first) |
| `model` | `sonnet`, `opus`, `haiku`, `inherit`, or full ID |
| `permissionMode` | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `skills` | Skills preloaded at startup (full content injected) |
| `mcpServers` | Scoped MCP servers |
| `hooks` | Lifecycle hooks for this subagent |
| `memory` | `user`, `project`, `local` for persistent learning |
| `background` | true = run concurrently |
| `isolation` | `worktree` = isolated git worktree |
| `maxTurns` | Max agentic turns |

### Key Exam Points
- Subagents **cannot spawn other subagents**
- Subagent receives its system prompt only (not full Claude Code system prompt)
- CLAUDE.md still loads through normal message flow
- Background subagents: permissions pre-approved, auto-deny unapproved
- `Agent(worker, researcher)` in tools field restricts which subagents can be spawned
- Skills in subagents: **full content injected** at startup, not just made available

---

## 5. Headless Mode / CI Integration

### Basic Usage
```bash
claude -p "prompt" --allowedTools "Read,Edit,Bash"
```

### Key Flags
| Flag | Purpose |
|------|---------|
| `-p` / `--print` | Non-interactive mode |
| `--bare` | Skip auto-discovery (hooks, skills, MCP, memory, CLAUDE.md) |
| `--output-format json` | Structured JSON output |
| `--json-schema '{...}'` | Enforce output schema |
| `--output-format stream-json` | Real-time streaming |
| `--allowedTools` | Auto-approve specific tools |
| `--continue` | Continue most recent conversation |
| `--resume <id>` | Continue specific session |
| `--append-system-prompt` | Add to system prompt |
| `--system-prompt` | Replace system prompt entirely |
| `--agents` | Define session-only agents as JSON |
| `--settings` | Load settings from file/JSON |
| `--mcp-config` | Load MCP config |

### Key Exam Points
- `--bare` = recommended for CI (deterministic, no local config interference)
- `--json-schema` + `--output-format json` → structured output in `structured_output` field
- Permission rule syntax: `Bash(git diff *)` (space before * = prefix match)
- User-invoked skills (e.g., `/commit`) NOT available in `-p` mode
- `-p` was previously called "headless mode"

---

## 6. Context Window

### Startup Load Order
1. System prompt (~4,200 tokens)
2. Auto memory / MEMORY.md (~680 tokens)
3. Environment info (~280 tokens)
4. MCP tools (deferred by default, ~120 tokens for names)
5. CLAUDE.md files (variable)
6. Rules files (variable)
7. Skill descriptions (~1% of context window budget)
8. Git status
9. User's first message

### Key Exam Points
- Default context: 200,000 tokens
- Auto-compaction at ~95% capacity (`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` to adjust)
- CLAUDE.md re-read from disk after compaction
- Conversation messages lost after compaction (only summary retained)
- MCP tool schemas deferred by default; loaded on demand via tool search
- `ENABLE_TOOL_SEARCH=auto` loads schemas upfront if < 10% of context
