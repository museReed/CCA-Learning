# Claude Code Setup — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows |
| Task Statements | 3.1 (setup is prerequisite) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> [!NOTE] All content in this section comes directly from official course materials.

## One-Liner / TL;DR

Claude Code installs with a single terminal command on every major platform — team members can self-serve without IT tickets.

## Core Concepts

### Installation Methods

Three platform-specific installation options — all are one-line commands requiring no admin intervention:

| Platform | Command | PM Takeaway |
|----------|---------|-------------|
| macOS (Homebrew) | `brew install --cask claude-code` | One command, team can self-serve without IT ticket |
| macOS, Linux, WSL | `curl -fsSL https://claude.ai/install.sh \| bash` | Universal fallback — works even without Homebrew |
| Windows CMD | `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd` | Windows team members covered — download, install, auto-cleanup |

> [!NOTE]
> macOS users have two paths (Homebrew or curl script). This means zero blockers for onboarding regardless of machine setup.

### First Run & Authentication

- After installation, running `claude` in the terminal triggers first-time authentication
- No separate setup step — the tool walks the user through auth on first launch

### Full Setup Reference

- Official quickstart documentation: https://code.claude.com/docs/en/quickstart

### Enterprise / Cloud Provider Options

For organizations with compliance or data residency requirements:

| Provider | Documentation | When to Consider |
|----------|--------------|-----------------|
| AWS Bedrock | https://code.claude.com/docs/en/amazon-bedrock | Team already on AWS, needs data in AWS region |
| Google Cloud Vertex AI | https://code.claude.com/docs/en/google-vertex-ai | Team already on GCP, needs data in GCP region |

## Key Takeaways

1. Zero-friction install: one command on macOS, Linux, WSL, and Windows
2. macOS offers two install paths — no single point of failure for onboarding
3. Windows uses a download-execute-cleanup pattern (`curl -o ... && ... && del ...`) — fully automated
4. Authentication is built into first launch — no separate credential provisioning step
5. Enterprise teams needing compliance controls can route through AWS Bedrock or Google Cloud Vertex AI

---

# PART 2: Study Aids

> [!TIP] Supplementary learning materials, not from official course.

## Familiar Analogies

- **One-command install** — Like installing Slack or Zoom from IT self-service portal, except it's a single terminal command. No download page, no drag-to-Applications.
- **First-run auth** — Like the first time you open a new SaaS tool and it asks you to log in. No pre-configuration needed.
- **Bedrock/Vertex options** — Like choosing whether your team's Slack data lives in US or EU regions. Same product, different hosting for compliance.
- **Three platform commands** — Like a vendor providing installer packages for Windows, Mac, and Linux — full platform coverage means no team member is blocked.

## CCA Exam Connection

> [!TIP]
> As a PM, you need to know:
> - That installation is self-serve (one command per platform) — impacts rollout planning
> - That auth happens automatically on first run — no IT provisioning step
> - That Bedrock/Vertex exist as enterprise options — relevant for procurement discussions
> - Which command goes with which OS — expect at least one question matching platform to command

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|-------------|---------------|-----------------|
| Planning a multi-step IT-assisted rollout | Installation is one command — over-engineering the rollout | Share the correct command per platform in a Slack message |
| Assuming Windows team members can't use Claude Code | Windows is fully supported via CMD | Share the Windows curl command |
| Requiring manual API key setup in onboarding docs | Auth is handled by the tool on first run | Just tell team to run `claude` after install |
| Ignoring Bedrock/Vertex during vendor evaluation | Enterprise teams may need these for compliance | Include cloud provider options in procurement checklist |

## Practice Questions

**Q1.** You are rolling out Claude Code to a cross-platform engineering team (macOS and Windows). A Windows developer reports they don't have Homebrew. What should you advise?

- A) Ask IT to install Homebrew on their Windows machine
- B) Tell them Claude Code is macOS-only
- C) Share the Windows CMD command: `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd`
- D) Ask them to switch to a Mac

> [!NOTE]
> **Answer: C.** Claude Code provides a dedicated Windows CMD installation command. Homebrew is a macOS package manager and is not available on Windows. Claude Code supports macOS, Linux, WSL, and Windows.

**Q2.** Your organization requires all AI tools to be routed through your existing AWS infrastructure for compliance. Which setup path should you recommend?

- A) Standard installation with direct Anthropic authentication
- B) AWS Bedrock integration as documented at https://code.claude.com/docs/en/amazon-bedrock
- C) Install via `pip install claude-code` for AWS compatibility
- D) Claude Code cannot be used with AWS infrastructure

> [!NOTE]
> **Answer: B.** AWS Bedrock is one of two enterprise cloud provider options (alongside Google Cloud Vertex AI) that allow routing Claude Code through existing cloud infrastructure for compliance requirements.
