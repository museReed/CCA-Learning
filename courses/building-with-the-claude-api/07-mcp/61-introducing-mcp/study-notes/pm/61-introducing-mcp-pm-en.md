# Introducing MCP — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — primary; D1 — Agentic Architecture (22%) — secondary |
| Task Statements | 2.3 (MCP primitives), 2.1 (tool schemas), 1.2 (agent loop integration) |
| Source | building-with-the-claude-api / 07-mcp / Lesson 61 |

---

## One-Liner

MCP is the "don't reinvent the wheel" layer for Claude integrations: instead of your team authoring, testing, and maintaining tool definitions for every SaaS service you want to use, you plug in a pre-built MCP server and inherit its entire tool catalog for free.

---

## Mental Model: The App Store for Claude

Think of tool use (Ch04) as having Claude learn how to use a single custom-built device. Think of MCP as the **app store** that device connects to:

| Without MCP | With MCP |
|-------------|----------|
| Every integration is a custom build | Integrations are installable |
| Your eng team owns every tool schema | The service provider or community owns it |
| Adding GitHub means writing dozens of schemas | Adding GitHub means installing a server |
| Every API change is your maintenance problem | Upstream publishes a new server version |

The "app store" mental model is not official — it's a PM shortcut. But it captures the most important product truth: MCP changes the economics of integration work.

---

## Why This Lesson Matters for PMs

For a product team evaluating "can we build an AI assistant that answers questions from our GitHub / Jira / Sentry / Notion data?", the answer has historically been:

> "Yes, but it will cost 3–6 months of engineering to write and maintain all the tool integrations."

MCP collapses that timeline dramatically. Roughly:

| Integration source | Rough time to "Claude can use it" |
|--------------------|-----------------------------------|
| Custom-built tools for a single SaaS | Weeks to months |
| Install an official MCP server | Hours |
| Install a community MCP server | Hours (plus due diligence) |
| No MCP server exists yet | Back to the original timeline |

The first product question a PM should ask when scoping an AI feature that touches external systems: "does an MCP server already exist for this?"

---

## The GitHub Example in PM Language

The lesson uses GitHub as the motivating example. A PM should internalize it this way:

> "What would it cost to let Claude answer *any* GitHub question?"

Without MCP, "any GitHub question" means committing to author, test, and maintain a tool for every feature the user might reference: repos, PRs, issues, projects, releases, actions, reviews, members, permissions, search, notifications. That's a multi-quarter project — before you even get to Jira or Slack.

With MCP, "any GitHub question" means connecting to a GitHub MCP server — the tools are already authored, and the service-provider (or a trusted community) keeps them current.

---

## Product Use Cases

### When MCP is the right answer

| Scenario | Why MCP fits |
|----------|-------------|
| AI assistant that spans multiple SaaS tools | MCP gives you N ecosystems for the price of N `install` commands |
| Long-tail integration requests from stakeholders | You can add integrations incrementally, without re-architecting |
| Internal "AI for the company data" pilots | Wrap internal APIs in one MCP server; every Claude-based product gets access |
| Agent workflows that need many small actions | Each action is a prebuilt MCP tool, not a new schema |

### When MCP is overkill

| Scenario | What to do instead |
|----------|--------------------|
| One-shot lookup against a simple internal endpoint | Write a direct tool; it's faster than pulling in a server |
| You only need read access to one static doc | Use a resource or plain context, not MCP |
| Prototype to test whether users even want the feature | Hard-code the tool until the signal is clear |

---

## PM Decision Framework

When someone proposes "let's add X integration", ask:

1. **Is there an official MCP server from the vendor?** Start here — it's the highest quality source.
2. **Is there a community MCP server?** Good, but do security and maintenance due diligence.
3. **If not, does the feature justify writing one?** Use the "weekly use or safety-critical" heuristic.
4. **What subset of the vendor's API do we actually need?** Prevent scope creep — don't install 80 tools if users only need 3.
5. **What is our fallback when the MCP server goes down?** MCP servers are separate processes; plan for failure.

---

## The Hidden PM Wins

The three-primitive model (tools, prompts, resources) is also a PM lever:

| Primitive | What the PM is really buying |
|-----------|-----------------------------|
| Tools | Actions the assistant can take on the user's behalf |
| Prompts | Pre-authored workflows that load with one click |
| Resources | Curated data surfaces the assistant can read |

A PM can scope an MCP adoption as "install this server for the tools, and also expose these prompts to power-users" — the same server delivers multiple layers of value.

---

## Ecosystem Positioning

A PM should also know:

| Fact | Product implication |
|------|---------------------|
| MCP is an open protocol | You are not locked to Anthropic; your integrations travel to other model hosts |
| Anyone can author a server | Vendors, community, your own internal platform team |
| Service providers often ship official servers | First place to check when scoping a feature |
| The ecosystem grows rapidly | The "no MCP server yet" answer has a short half-life |

---

## Common PM Mistakes

1. **Treating MCP as a technical detail** — it is a *buy vs build* decision at every integration.
2. **Installing servers without asking what tools users actually need** — tool sprawl bloats context and slows responses.
3. **Assuming MCP solves auth** — credential handling, rate limits, and permissions are still your product's problem.
4. **Forgetting to budget for server updates** — MCP servers get versioned; stale versions break silently.
5. **Confusing MCP with tool use** — tool use is the Claude protocol that MCP tools still ride on. You can't skip learning tool use.

> **Key Insight**
>
> MCP is not a technical upgrade — it's an **economic** one. It takes the dominant cost of shipping AI features that touch real systems (writing and maintaining tool integrations) and hands it to someone else. The PM job is to notice when the answer to "should we build this integration?" has changed from "months of work" to "install command" — and reprioritize accordingly.

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**: Know what MCP is, who writes MCP servers, and the three primitives.
- **D1 (Agentic Architecture)**: Understand MCP as the reusable integration layer agents plug into.
- Exam questions often ask "what problem does MCP solve?" — the answer is *the burden of authoring/maintaining tool integrations*.

---

## Flashcards

| Front | Back |
|-------|------|
| What is MCP's one-sentence pitch? | A protocol that lets you install pre-built tool integrations into Claude instead of writing them yourself. |
| What is the PM's first question when scoping a new Claude integration? | "Does an official or community MCP server already exist for this service?" |
| What are MCP's three primitives? | Tools, Prompts, Resources |
| Does MCP replace tool use? | No — it rides on top of tool use as a distribution layer. |
| Who typically authors an MCP server? | Service providers (official), community maintainers, or your own internal team |
| What should a PM budget for when adopting MCP servers? | Token cost, latency, failure surface, security review, version maintenance |
| Is MCP Anthropic-proprietary? | No — it is an open protocol; any model host or application can speak it. |
| What was the primary problem shown in the GitHub example? | Having to author and maintain dozens of custom tools for a single service's API. |
