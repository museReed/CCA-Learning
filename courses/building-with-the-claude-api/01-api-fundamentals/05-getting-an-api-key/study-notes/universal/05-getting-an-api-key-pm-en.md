# Getting an API Key — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Claude Code Configuration (20%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 3.1 (API key lifecycle), 3.2 (workspace strategy), 5.3 (secret hygiene in production) |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 05 |

---

## One-Liner

An Anthropic API key is the spending card for your Claude feature — treating key creation, workspace selection, and rotation as product concerns (not just devops) prevents 3am billing surprises and security incidents.

---

## Mental Model: The Physical Safe-Deposit Key

An Anthropic API key is like a safe-deposit box key at a bank:

| Property | Safe-Deposit Key | Anthropic API Key |
|----------|------------------|-------------------|
| Shown only once | You take the key home from the bank | Plaintext is displayed exactly once at creation |
| Not recoverable | If lost, you drill out the box and get a new one | If lost, you delete and create a new one |
| Bank can verify but not duplicate | Bank keeps a hash, not the key | Anthropic keeps a hash, not the plaintext |
| Whoever holds it can access | No ID check at the box | Whoever has the key can spend your budget |

The PM implication: treat keys like cash. You would not leave physical cash in a repository — don't leave API keys there either.

---

## Why PMs Should Care About Keys

| Concern | PM Impact |
|---------|-----------|
| Cost attribution | You cannot report "how much did Feature X cost?" without workspace discipline |
| Security incidents | A leaked key is a real-dollar exposure that shows up in next month's invoice |
| Launch blockers | Compliance teams will ask "where are keys stored?" before any enterprise launch |
| Team onboarding | New engineers need keys; the process must be documented and auditable |
| Vendor review | Enterprise customers will ask about your key management as part of procurement |

If you ship a Claude feature without a key management plan, you are shipping a cost and security liability disguised as a feature.

---

## Product Use Cases: Workspace Strategy as a Product Decision

### One Workspace Per Product Line

Use when you have multiple products sharing one Anthropic account and need clean per-product billing.

| Benefit | Cost |
|---------|------|
| Easy answer to "how much is Claude costing Product A?" | Engineers need to switch workspaces in the console |
| Per-product quotas prevent one product starving another | Slightly more admin overhead |

### One Workspace Per Environment

Use when operational safety matters (almost always for production).

| Benefit | Cost |
|---------|------|
| A dev runaway loop can't drain production quota | More keys to rotate |
| Clear blast radius during incidents | More audit surface to monitor |

### Shared Default Workspace

Use only for prototypes and courses.

| Benefit | Cost |
|---------|------|
| Zero setup | No cost attribution; any incident affects everything |

---

## The Key Lifecycle: A PM Checklist

```
     Create
        │
        ▼
     Copy once → store in secret manager
        │
        ▼
     Document: name, owner, purpose
        │
        ▼
     Use in service → monitor usage/cost
        │
        ▼
     Rotate on schedule (quarterly)
        │
        ▼
     Delete when service decommissioned
```

Each step is a product concern:

| Step | PM Responsibility |
|------|-------------------|
| Create | Ensure naming convention exists and is followed |
| Store | Require secret manager usage in the PRD |
| Document | Maintain a key inventory (who owns what) |
| Monitor | Dashboards for unusual spend |
| Rotate | Quarterly rotation as a scheduled engineering ticket |
| Delete | Decommission checklist when a feature sunsets |

---

## PM Decision Framework

When a new Claude feature is proposed, run this questionnaire:

| Question | Default Answer |
|----------|---------------|
| Which workspace will this key live in? | A dedicated per-feature or per-env workspace |
| Who is the human owner of this key? | Named engineer on the feature team, not "the team" |
| Where is the key stored in production? | Secret manager (never env vars on bare metal) |
| How will we rotate it? | Quarterly, as a scheduled ticket |
| How do we know if it leaks? | Billing anomaly alerts + GitHub secret scanning |
| What's the incident playbook? | Delete in console → create new → redeploy → post-mortem |

---

## Common PM Mistakes

1. **Treating key management as devops-only** — it is a product concern because it drives cost attribution, security posture, and launch readiness.
2. **Skipping the naming convention** — when the first incident hits, "My Key 3" costs hours of detective work.
3. **Not budgeting rotation work** — rotation never happens if it isn't on the roadmap; schedule it quarterly.
4. **Mixing dev and prod in one workspace** — saves ten minutes today, costs a runaway invoice later.
5. **No incident playbook** — when a key leaks, the team loses time improvising the rotation steps under pressure.

> **Key Insight**
>
> Key management is not below your pay grade — it's a product design decision disguised as plumbing. The PMs who lose sleep over Claude features are usually the ones who treated API keys as "engineering's problem" and then discovered a $40K dev runaway or a public-repo leak the hard way. Add "workspace + key plan" to your feature launch checklist, right next to "privacy review."

---

## CCA Exam Relevance

- **D3 (Claude Code Configuration)**: creation flow, storage patterns, recovery path (you can't — you rotate).
- **D5 (Enterprise Deployment)**: workspace as a billing/quota boundary; key hygiene as a production requirement.
- Scenario trigger: "A key leaked into a public repo" → delete in console, create new, redeploy, and review how it leaked.

---

## Flashcards

| Front | Back |
|-------|------|
| Why should a PM care about API key management? | It drives cost attribution, security incidents, and enterprise launch readiness |
| What is the mental model for an Anthropic API key? | A safe-deposit box key — shown once, not recoverable, bank keeps only a hash |
| What's the default PM answer to "which workspace?" | A dedicated per-feature or per-environment workspace, not shared Default |
| What goes in a key inventory? | Name, owner (named human), purpose, workspace, rotation date |
| What is the correct incident response to a leaked key? | Delete in console → create new → redeploy → post-mortem |
| Why does quarterly rotation need PM sponsorship? | Because rotation work only happens when it's on a roadmap with a scheduled ticket |
| What's wrong with mixing dev and prod in one workspace? | A dev runaway loop can drain production quota, causing a customer incident |
| What should a PM add to the feature launch checklist? | A workspace + key plan alongside privacy and security review |
