# Getting an API Key — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3 — Claude Code Configuration (20%) — primary; D5 — Enterprise Deployment (20%) — secondary |
| Task Statements | 3.1 (API key lifecycle), 3.2 (workspace & key naming), 5.3 (secret hygiene in production) |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 05 |

---

## One-Liner

An Anthropic API key is a write-once, bearer credential created through the Console under a named workspace — you must copy it the moment it appears, because it will never be shown again.

---

## The Five-Step Creation Flow

```
Console login  ─▶  Get API Keys  ─▶  Create Key  ─▶  Workspace + Name  ─▶  Copy Once
     1                  2                3                  4                  5
```

| Step | Action | Notes |
|------|--------|-------|
| 1 | Navigate to `https://console.anthropic.com/` and log in | Use the account that should own billing & auditing |
| 2 | Click **Get API Keys** (top right of the dashboard) | Lands on the keys management page |
| 3 | Click **Create Key** (top right of the keys page) | Opens the creation dialog |
| 4 | Pick a workspace (e.g. `Default`) and give the key a name (e.g. `Anthropic Course`) | Name is identification only; workspace is the billing/audit boundary |
| 5 | Copy the key immediately | **The value is shown exactly once**; if you close the dialog, you must delete and recreate |

The "copy once" rule is not a UX quirk — it's a security design. Anthropic never stores the plaintext key on its side after creation, only a hash. If you lose it, nobody can recover it, which is also why nobody can steal it from a support ticket.

---

## Workspace: The Unit of Isolation

A workspace is the boundary where billing, rate limits, and usage reporting live. Choosing the right workspace for a key is a production decision, not cosmetic.

| Workspace strategy | Good for | Tradeoff |
|---------------------|----------|----------|
| One workspace per product | Clean per-product billing and quotas | Requires workspace switching for devs |
| One workspace per environment (dev/staging/prod) | Env isolation, incident containment | More keys to manage |
| Shared `Default` workspace | Prototyping / courses | No cost attribution between projects |

For any serious production app, treat workspaces the way you treat AWS accounts: at least a prod/non-prod split.

---

## Key Naming: A Small Habit With Big Payoff

The name field is free-form and exists only to help humans identify which key is which. Adopt a naming convention early:

```
<env>-<service>-<owner>-<date>
prod-chatbot-backend-2025-04-11
dev-ingest-worker-2025-04-11
```

When you see a suspicious charge or need to rotate, the name is your only lookup key inside the console. "My Key 3" will cost you hours during an incident.

---

## Handling the Key in Code

Anthropic's SDK auto-reads from the environment variable `ANTHROPIC_API_KEY`. This is the pattern Lesson 06 will rely on, and the only acceptable starting pattern:

```bash
# .env (never commit this file)
ANTHROPIC_API_KEY="sk-ant-api03-...your-key..."
```

```python
# Python — the SDK picks up the env var automatically
from dotenv import load_dotenv
load_dotenv()

from anthropic import Anthropic

client = Anthropic()  # no explicit key argument needed
```

Rules for the key in code:

| Rule | Reason |
|------|--------|
| Never commit `.env` | Public repos trigger auto-revocation, private repos still leak via forks |
| Always add `.env` to `.gitignore` | Belt + suspenders against accidental commits |
| Use a secret manager in production (AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault) | Env vars on bare servers are fine for POCs but not auditable |
| Rotate on any suspicion of leak | Delete in console → create new → redeploy |
| Never share via chat/email/screenshot | If you must share, use a password manager's secure share |

---

## The "Lost Key" Workflow

Because the value is shown only once, the recovery path is explicit: you cannot recover, you must rotate.

```
                ┌──────────────────┐
                │  Lost the key?   │
                └────────┬─────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
    Console: find                 Console: delete
    the key by name               the lost key
         │                               │
         └───────────────┬───────────────┘
                         ▼
                 Console: Create Key
                 (new value, new copy-once window)
                         ▼
                 Update .env / secret
                 manager / deploy
```

This is also the exact workflow for scheduled rotation — there is no "get existing key value" endpoint.

---

## Code Example: SDK With Explicit Key (for testing only)

The SDK allows passing the key directly, but you should only do this in throwaway scripts:

```python
from anthropic import Anthropic

# Only acceptable in a one-off notebook or test; never in production
client = Anthropic(api_key="sk-ant-api03-...")

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=256,
    messages=[{"role": "user", "content": "ping"}],
)
print(response.content[0].text)
```

The moment this pattern leaves a notebook it becomes a landmine — a stray `git add .` will ship the key to the remote.

---

## Common Mistakes

1. **Closing the creation dialog before copying** — the value cannot be recovered; you must delete and recreate.
2. **Committing the key to git** — even private repos can leak via forks, backups, or future open-sourcing. Always use env vars.
3. **Using "My Key" or "Test" as the name** — during an incident you won't know which service owns which key.
4. **Sharing one workspace across dev and prod** — a runaway dev job can then drain your production quota.
5. **Never rotating** — keys should expire on a schedule (quarterly is a reasonable default); unused keys should be deleted.

> **Key Insight**
>
> The copy-once dialog is not an inconvenience — it's the reason API keys stay secure. If Anthropic could show you the key later, so could an attacker who compromised your account. Internalize the "copy once, store in a secret manager, rotate on any doubt" loop and you've already passed the D3 secret-hygiene questions on the CCA.

---

## CCA Exam Relevance

- **D3 (Claude Code Configuration)**: creation flow, where keys live, how to recover (you can't — you rotate), and why.
- **D5 (Enterprise Deployment)**: workspace strategy as a production concern — billing, auditing, rate-limit isolation.
- Exam trigger: "A developer lost an API key" → the correct answer is always "delete in console and create a new one," never "contact Anthropic support to recover it."

---

## Flashcards

| Front | Back |
|-------|------|
| How many times can you view the plaintext value of an Anthropic API key? | Exactly once, at creation time — it is never shown again |
| If you lose a key, how do you recover it? | You cannot recover it; you must delete it in the console and create a new one |
| What are the five steps to create an API key? | 1) Log in to console.anthropic.com, 2) Get API Keys, 3) Create Key, 4) Choose workspace + name, 5) Copy the value once |
| What environment variable does the `anthropic` SDK auto-read? | `ANTHROPIC_API_KEY` |
| What must you add to `.gitignore` to protect keys? | `.env` (and any other file where keys might land) |
| Why does Anthropic not store the plaintext key server-side after creation? | So nobody — including Anthropic support or attackers — can retrieve it later |
| What is a workspace used for in key management? | It's the boundary for billing, quotas, and usage reporting; choose per-env or per-product |
| What is a safe naming convention for keys? | `<env>-<service>-<owner>-<date>`, e.g. `prod-chatbot-backend-2025-04-11` |
