# Claude Code Setup — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Claude Code Configuration (20%) |
| Task Statements | 3.1 (Claude Code installation & setup), 3.2 (authentication), 1.1 (Claude Code overview) |
| Source | building-with-the-claude-api / 08-agents-and-workflows / Lesson 74 |

---

## One-Liner

Claude Code's setup is intentionally a three-step frictionless flow — the low activation energy is a deliberate product choice that drives developer adoption and determines which personas you can realistically target.

---

## Mental Model: The Installable Coworker

Onboarding Claude Code is less like installing an app and more like hiring a coworker. The three steps map to:

| Step | Hiring analogy |
|------|----------------|
| Install Node.js | Making sure the office has power outlets the new hire needs |
| `npm install -g @anthropic-ai/claude-code` | The new hire arrives with their own laptop (the CLI binary) |
| `claude` + account login | The new hire signs their employment agreement (your Anthropic account) |

After 60 seconds of setup, the "coworker" is ready to pair with you. This is the fastest path to a real agent that exists — most agent products require far more configuration.

---

## Why Setup Friction Matters

Every step of setup loses some users. Claude Code's three-step flow is near the theoretical minimum:

| Setup complexity | Typical product | Claude Code |
|------------------|-----------------|-------------|
| 0 steps | Web app — visit URL | — |
| 1 step | Browser extension — single install | — |
| **3 steps** | CLI tool with dependency | **Claude Code** |
| 5+ steps | Desktop app + API keys + config | Most enterprise agents |

The product decision the Claude Code team made: keep the bar at "any developer comfortable with a terminal." That defines the addressable audience.

---

## Product Use Cases

### When "Install Claude Code" is the right recommendation

| Scenario | Why it fits |
|----------|-------------|
| Your team is already npm-comfortable | Zero new tooling to adopt |
| You need filesystem + git + shell access | Built-in tools cover it |
| You want to extend with MCP servers later | Extension point exists from day one |
| You want account-based billing, not raw keys | Login model handles it |

### When Claude Code is the wrong recommendation

| Scenario | Better alternative |
|----------|--------------------|
| Non-technical users | Use Claude.ai or an in-app chat widget |
| Strict corporate environments with no npm | Build a web-based tool or use Claude.ai for business |
| Windows-only shop with no WSL | Evaluate Claude.ai or Anthropic API-based tools |
| Feature needs a GUI, not a CLI | Use the API and build your own UI |

---

## PM Decision Framework

If you are asking "should my team adopt Claude Code?", check:

1. **Do our developers already live in the terminal?** If yes, adoption cost is near zero.
2. **Do we have npm or WSL available on every developer's machine?** Those are hard prerequisites.
3. **Do we need account-based auth, or is API-key provisioning already in place?** Claude Code expects account login.
4. **Will we need MCP extensions in year one?** If yes, Claude Code is ideal; otherwise raw API may be simpler.
5. **Who owns support when setup breaks?** Three steps rarely break, but someone still has to answer "why does `claude` say command not found?"

---

## The Four Built-in Capabilities (What Users Get For Free)

From a PM standpoint, these are the features you inherit the moment a developer finishes setup:

| Capability | Business value |
|------------|----------------|
| File operations | Agent can read/modify the codebase — enables real work, not just chat |
| Terminal access | Agent can run tests, linters, scripts — closes the verification loop |
| Web access | Agent can fetch docs — always current, no stale training data excuse |
| MCP server support | Anything you add later extends the agent without redeploying it |

Understanding this inventory is important because when someone asks "what does Claude Code do?", these four bullet points are the core answer.

---

## The Authentication Decision

Claude Code uses **account-based login**, not raw API keys. This has product implications:

| Aspect | Account login (Claude Code) | Raw API key |
|--------|----------------------------|-------------|
| User experience | One-time login, auto-reused | Copy-paste, often leaks into git |
| Security | Anthropic-managed session | User-managed secret |
| Billing | Tied to user's subscription | Tied to your API org |
| Compliance | Easier — no secret in your infra | Harder — key management burden |
| Revocation | Users log out or Anthropic revokes | You rotate keys manually |

For PMs running a "recommend a coding agent to our engineers" project, the account-login model is usually a win. For "ship a product that *uses* Claude under the hood", API keys are the right model.

---

## Common PM Mistakes

1. **Assuming Windows support means any Windows** — it means WSL only; warn Windows users early.
2. **Treating setup as an afterthought in a rollout plan** — even three steps trip up someone; document them.
3. **Confusing Claude Code login with Anthropic API keys** — they are separate billing paths with different operational models.
4. **Overlooking the four built-in capabilities** — "file + terminal + web + MCP" is the minimum viable feature list to communicate to stakeholders.
5. **Skipping a rollback plan** — if `claude` misbehaves on a team member's machine, `npm uninstall -g @anthropic-ai/claude-code` must be documented as the escape hatch.

> **Key Insight**
>
> Setup friction is a **product lever**, not a technical chore. Claude Code's three-step install is deliberate: it widens the audience to any npm-comfortable developer while still enabling a full agent. For any PM comparing agent platforms, the activation energy comparison is the single most important question.

---

## CCA Exam Relevance

- **D3 (Claude Code Configuration)**: Expect questions on the installation steps, platform support, and authentication model.
- **D1 (Agentic Coding & Architecture)**: Know why an agent product like Claude Code benefits from a lightweight install path.
- Watch for Windows/WSL trap questions and exact package-name questions.

---

## Flashcards

| Front | Back |
|-------|------|
| How many setup steps does Claude Code require? | Three: install Node.js, `npm install -g @anthropic-ai/claude-code`, then run `claude` and log in |
| What authentication model does Claude Code use? | Account-based login through your Anthropic account, not raw API keys |
| Which operating systems does Claude Code support out of the box? | macOS, Windows via WSL, and Linux |
| What are the four built-in capabilities a user gets after setup? | File operations, terminal access, web access, and MCP server support |
| Why does setup friction matter for a PM evaluating adoption? | Every setup step loses users — Claude Code's three-step flow sets the addressable audience at "any developer comfortable with a terminal" |
| When should a PM NOT recommend Claude Code? | When users are non-technical, Windows without WSL, or need a GUI rather than a CLI |
| How does Claude Code billing differ from direct Anthropic API usage? | Claude Code is tied to the user's Anthropic account subscription; the API uses organization-owned API keys |
| What is the PM-level case for preferring account login over API keys? | Better UX, no secret leakage risk, Anthropic-managed session, and easier compliance |
