# Claude Code Setup — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows |
| Task Statements | 3.1 (setup is prerequisite) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> [!NOTE] All content in this section comes directly from official course materials.

## One-Liner / TL;DR

Claude Code is installed via a single terminal command on macOS, Linux, WSL, or Windows, and authenticates on first run.

## Core Concepts

### Installation Methods

Three platform-specific installation commands are provided:

| Platform | Command |
|----------|---------|
| macOS (Homebrew) | `brew install --cask claude-code` |
| macOS, Linux, WSL | `curl -fsSL https://claude.ai/install.sh \| bash` |
| Windows CMD | `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd` |

> [!NOTE]
> The macOS universal script (`curl ... install.sh`) also works on macOS without Homebrew, giving two options for Mac users.

### First Run & Authentication

- After installation, run `claude` at your terminal
- First-time launch prompts an authentication flow

### Full Setup Reference

- Official quickstart documentation: https://code.claude.com/docs/en/quickstart

### Enterprise / Cloud Provider Options

Alternative authentication backends for enterprise deployments:

| Provider | Documentation |
|----------|--------------|
| AWS Bedrock | https://code.claude.com/docs/en/amazon-bedrock |
| Google Cloud Vertex AI | https://code.claude.com/docs/en/google-vertex-ai |

## Key Takeaways

1. Installation is a single command on every supported platform
2. macOS has two installation paths: Homebrew cask or the universal curl script
3. Windows uses a download-execute-cleanup pattern (`curl -o ... && ... && del ...`)
4. Authentication happens automatically on first `claude` invocation
5. Enterprise teams can route through AWS Bedrock or Google Cloud Vertex AI instead of direct Anthropic auth

---

# PART 2: Study Aids

> [!TIP] Supplementary learning materials, not from official course.

## Familiar Analogies

- **Homebrew cask install** — Same pattern as `brew install --cask visual-studio-code`. Cask = GUI/CLI app (not a library).
- **curl pipe to bash** — The universal Node.js/Rust installer pattern (`nvm`, `rustup`). Downloads a script and executes it in one shot.
- **Windows three-step** — Similar to downloading an `.exe` installer, running it, then deleting the installer. The `&&` chaining ensures each step succeeds before proceeding.
- **First-run auth** — Like `gh auth login` for GitHub CLI or `aws configure` — the tool bootstraps credentials on first use.

## CCA Exam Connection

> [!TIP]
> Setup is the prerequisite for every hands-on domain. Expect questions that test whether you know:
> - Which command is correct for a given OS
> - That authentication is triggered by running `claude` (not a separate `claude auth` step)
> - That Bedrock/Vertex are enterprise alternatives (not required for individual use)

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|-------------|---------------|-----------------|
| Running `npm install -g claude-code` | This is the old installation method, no longer the recommended path | Use `brew install --cask claude-code` or the official curl script |
| Using `sudo` with the curl install script | The official script handles permissions; `sudo` can cause ownership issues | Run the curl command as your normal user |
| Skipping authentication on first run | Claude Code won't function without auth | Run `claude` and complete the auth prompt |
| Confusing Bedrock/Vertex as mandatory | They are optional enterprise backends | Direct Anthropic auth is the default |

## Practice Questions

**Q1.** A developer on your team uses macOS but does not have Homebrew installed. Which command should they use to install Claude Code?

- A) `brew install --cask claude-code`
- B) `npm install -g @anthropic/claude-code`
- C) `curl -fsSL https://claude.ai/install.sh | bash`
- D) `pip install claude-code`

> [!NOTE]
> **Answer: C.** The universal curl script works on macOS, Linux, and WSL without requiring Homebrew. Option A requires Homebrew. Options B and D are not official installation methods.

**Q2.** After installing Claude Code, what is the next step to begin using it?

- A) Run `claude auth login` to configure credentials
- B) Run `claude` in the terminal — first launch triggers authentication
- C) Set the `ANTHROPIC_API_KEY` environment variable manually
- D) Open the Claude Code GUI application from the Applications folder

> [!NOTE]
> **Answer: B.** Simply running `claude` at the terminal triggers the first-time authentication flow. No separate auth command or manual API key configuration is needed for the standard setup.
