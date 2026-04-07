# Making Changes — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows |
| Task Statements | 3.4 (plan mode vs direct), 3.5 (iterative refinement) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> All content in this section comes directly from official course materials.

## One-Liner / TL;DR

Claude Code offers three operational modes for different complexity levels: screenshot-based visual communication for precise UI changes, Planning Mode for broad multi-file exploration, and Thinking Modes for deep reasoning — each consuming progressively more tokens.

## Core Concepts

### Screenshots for Precise Communication

The most effective way to communicate UI changes is to show Claude exactly what you see:

1. Take a screenshot of the element you want to modify
2. Paste with **Ctrl+V** (not Cmd+V on macOS) into the Claude Code chat
3. Describe the change you want relative to the screenshot

Claude processes both the image and your text instruction (multimodal input) to understand exactly which element to change and how. This eliminates the ambiguity of text-only descriptions like "the placeholder on the left panel."

### Planning Mode

Planning Mode separates planning from execution, giving Claude time to explore your codebase before acting.

**How to enable:** Press **Shift+Tab twice** (once if already auto-accepting edits).

In Planning Mode, Claude will:

1. **Read more files** — explores your codebase more broadly to understand the full picture
2. **Create a detailed implementation plan** — shows exactly what it intends to do
3. **Show what it intends to do** — presents the plan for your review
4. **Wait for approval** — gives you the opportunity to review and redirect before any changes are made

This is fundamentally different from direct execution. The extra file reading in the planning phase often catches dependencies and edge cases that direct execution would miss.

### Thinking Modes

Thinking modes give Claude progressively more tokens for internal reasoning before generating a response. Include the keyword in your prompt:

| Mode | Reasoning Depth | Best For |
|------|----------------|----------|
| "Think" | Basic extended | Moderate complexity |
| "Think more" | Extended | Complex logic |
| "Think a lot" | Comprehensive | Multi-step algorithms |
| "Think longer" | Extended time | Deep analysis |
| "Ultrathink" | Maximum | Hardest problems, ambiguous requirements |

Each level gives Claude progressively more tokens for deeper analysis before it responds.

### Planning vs Thinking — Breadth vs Depth

These two features solve different problems and can be combined:

| Dimension | Planning Mode | Thinking Mode |
|-----------|--------------|---------------|
| **What it does** | Reads more files, creates an action plan | Reasons more deeply about the problem |
| **Type of complexity** | Breadth — many files, many components | Depth — complex logic, ambiguous requirements |
| **Activation** | Shift+Tab twice (toggle) | Keyword in prompt ("think", "ultrathink") |
| **User interaction** | Review-approve cycle | No extra interaction needed |
| **Cost driver** | More file reads (tool calls) | More reasoning tokens |

**When to use Planning Mode:** Broad codebase understanding, multi-step implementation, changes spanning multiple files, unfamiliar codebases.

**When to use Thinking Mode:** Complex logic, debugging difficult issues, algorithmic challenges, ambiguous requirements.

**Combining both:** For tasks that need both breadth (many files) and depth (complex reasoning), enable Planning Mode and add "ultrathink" to your prompt. Both consume additional tokens — use proportionately.

### Git Integration

Claude Code also serves as a solid Git assistant. After completing changes, you can ask Claude to stage and commit with descriptive messages — streamlining the development-to-commit workflow without leaving the terminal.

## Demo Walkthrough: Screenshot Paste — Centering a Placeholder

| Step | What Happens | Frame |
|------|-------------|-------|
| 1. Start dev server | Instructor runs `npm run dev` and opens the app at localhost:3000 | ![frame_003](../../visual-guide/frames/frame_003.jpg) |
| 2. Identify the problem | Placeholder text sits on the left panel but is not centered | ![frame_006](../../visual-guide/frames/frame_006.jpg) |
| 3. Screenshot + paste | Takes a screenshot of the placeholder, pastes into Claude Code with Ctrl+V | ![frame_009](../../visual-guide/frames/frame_009.jpg) |
| 4. Result | Claude searches the codebase, updates styling — placeholder is now centered | ![frame_012](../../visual-guide/frames/frame_012.jpg) |

**Key takeaway:** A single screenshot + one-sentence instruction was enough for Claude to find the right file and fix the styling. No need to describe which component, which CSS file, or which class name.

## Demo Walkthrough: Plan Mode + Thinking — Complex Feature Implementation

| Step | What Happens | Frame |
|------|-------------|-------|
| 1. Discover the problem | After generating a card component, the instructor notices "String Replace Editor" — a technical tool name visible to users | ![frame_018](../../visual-guide/frames/frame_018.jpg) |
| 2. Screenshot the issue | Takes a screenshot of the technical text and pastes into Claude Code | ![frame_027](../../visual-guide/frames/frame_027.jpg) |
| 3. Enable Plan Mode | Presses Shift+Tab twice to enable Planning Mode — Claude will research and plan before acting | ![frame_035](../../visual-guide/frames/frame_035.jpg) |
| 4. Add ultrathink | Includes "ultrathink" for maximum reasoning depth; explains breadth (planning) vs depth (thinking) | ![frame_049](../../visual-guide/frames/frame_049.jpg) |
| 5. Combined execution | Plan Mode + ultrathink working together — Claude explores codebase broadly while reasoning deeply | ![frame_054](../../visual-guide/frames/frame_054.jpg) |
| 6. Feature complete | Technical tool names replaced with user-friendly messages: "Creating file:" and "Editing file:" | ![frame_069](../../visual-guide/frames/frame_069.jpg) |
| 7. Verification | Follow-up edit confirms the feature works — shows "Editing app.jsx" instead of tool names | ![frame_075](../../visual-guide/frames/frame_075.jpg) |

**Key takeaway:** This complex task touched multiple files and required understanding the rendering pipeline. Planning Mode found all the relevant files; ultrathink reasoned through the mapping logic. The combination took about two minutes for a feature that would require significant manual investigation.

## Instructor Tips

- Use **Ctrl+V** specifically for pasting screenshots — Cmd+V will not work in Claude Code on macOS
- Planning Mode is not just "slower execution" — it is a fundamentally different workflow that gathers more context
- Start with Planning Mode when you are unsure of the scope; drop back to direct execution for well-understood changes
- Ultrathink is the maximum reasoning level — use it when Claude is struggling with complex or ambiguous tasks
- Both Planning Mode and Thinking Modes cost extra tokens — match the tool to the task complexity
- Claude Code doubles as a Git assistant — use it to stage and commit after completing changes

## Key Takeaways

1. Screenshots eliminate ambiguity — show Claude exactly what you see with Ctrl+V
2. Planning Mode (Shift+Tab twice) = breadth — Claude reads more files and creates a plan before acting
3. Thinking Modes (think / think more / think a lot / think longer / ultrathink) = depth — more reasoning tokens for harder problems
4. Planning and Thinking can be combined for tasks needing both breadth and depth
5. Both features consume additional tokens — use proportionately to task complexity
6. Claude Code also handles Git operations — staging and committing with descriptive messages

---

# PART 2: Study Aids

> Supplementary learning materials, not from official course.

## Familiar Analogies

- **Screenshot paste** — Like pointing at a specific button on a monitor and saying "change this." Visual communication eliminates the ambiguity of describing UI elements in text.
- **Planning Mode** — Like an architect doing a site survey before drawing blueprints. You would not start construction without understanding the full layout. The extra exploration catches dependencies that a quick fix would miss.
- **Thinking Modes** — Like giving an engineer extra whiteboard time for a hard design problem. More time to reason does not mean more files to read — it means deeper analysis of the same problem.
- **Ultrathink** — Like a 3-hour design review session for a critical system component. Maximum reasoning resources for maximum complexity.
- **Planning + Thinking combined** — Like a cross-team sprint planning (breadth: who owns what) followed by a deep technical design session (depth: how to implement). Both are needed for complex features.
- **The five thinking levels** — Like a dimmer switch, not an on/off toggle. You dial up reasoning power gradually: think (25%), think more (50%), think a lot (75%), think longer (90%), ultrathink (100%).

## CCA Exam Connection

> [!TIP]
> This unit covers two high-weight task statements. Expect questions that test:
> - **Planning Mode vs Thinking Mode** — The breadth-vs-depth distinction is the most testable concept. Planning = more files read; Thinking = more reasoning tokens.
> - **When to use which mode** — Given a scenario (multi-file refactor vs algorithmic challenge), identify the correct mode.
> - **Combining modes** — Know that both can be used simultaneously for tasks with both breadth and depth complexity.
> - **Activation methods** — Shift+Tab twice for Planning Mode; keyword in prompt for Thinking Modes.
> - **Cost awareness** — Both features increase token usage; proportionate usage is key.
> - **Screenshot input** — Ctrl+V (not Cmd+V) for pasting images into Claude Code.

## Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Approach |
|-------------|-------------|-----------------|
| Using Planning Mode for every task | Wastes tokens on simple changes; slower than necessary | Use direct execution for simple, well-scoped changes |
| Using ultrathink for trivial tasks | Burns reasoning tokens without benefit | Reserve thinking modes for genuinely complex problems |
| Never using Planning Mode | Misses dependencies in multi-file changes | Enable Planning Mode when scope is unclear or spans multiple files |
| Describing UI changes in text only | Ambiguous — "the button on the left" could mean many things | Paste a screenshot with Ctrl+V and point to the specific element |
| Using Cmd+V instead of Ctrl+V for screenshots | Image will not paste into Claude Code on macOS | Use Ctrl+V specifically |
| Skipping the review step in Planning Mode | Defeats the purpose; might execute a flawed plan | Always review the plan before approving execution |

## Practice Questions

**Q1.** A developer needs to rename a database column that is referenced across 15 files in a Node.js monorepo. Which approach is most appropriate?

- A) Direct execution — just ask Claude to rename it
- B) Planning Mode — let Claude explore the codebase and create a plan before making changes
- C) Ultrathink — ask Claude to reason deeply about the rename
- D) Start a new Claude session for each file

> [!NOTE]
> **Answer: B.** This is a classic Planning Mode scenario: a change spanning many files requires broad codebase exploration first. Planning Mode reads relevant files, identifies all references, and presents a comprehensive plan. Ultrathink (C) solves the wrong problem — this needs breadth, not depth.

**Q2.** A developer is designing a new caching strategy that involves modifying the data access layer, API routes, and configuration system. The optimal algorithm depends on specific access patterns. Which approach is best?

- A) Direct execution with a detailed prompt
- B) Planning Mode only
- C) Ultrathink only
- D) Planning Mode + ultrathink — Planning Mode for broad codebase understanding, ultrathink for reasoning about the optimal algorithm

> [!NOTE]
> **Answer: D.** This task has both breadth complexity (multiple components) and depth complexity (choosing the optimal algorithm). Combining Planning Mode and ultrathink addresses both dimensions.

**Q3.** How do you activate Planning Mode in Claude Code?

- A) Type "plan" in your prompt
- B) Press Shift+Tab twice (or once if already auto-accepting)
- C) Use the `--plan` flag when starting Claude
- D) Enable it in the settings file

> [!NOTE]
> **Answer: B.** Planning Mode is toggled with the Shift+Tab keyboard shortcut. Press it twice from the default state (once if already auto-accepting edits). It is not a prompt keyword — that is how Thinking Modes work.

**Q4.** A junior developer uses "ultrathink" for every request, including adding console.log statements. Token usage is up 5x. What guidance is appropriate?

- A) Ultrathink is free, so continue
- B) Reserve thinking modes for tasks with genuine complexity; use direct execution for simple changes
- C) Replace ultrathink with Planning Mode for everything
- D) Stop using Claude Code to reduce costs

> [!NOTE]
> **Answer: B.** Thinking modes consume additional tokens. For simple tasks, standard execution is sufficient. Ultrathink is for genuinely hard problems where more reasoning time produces better results. Match the tool to the task complexity.
