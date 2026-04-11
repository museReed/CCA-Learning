# CCA Study Note Generation — Agent Instructions

## Context

You are generating study notes for the CCA (Claude Certified Associate) certification exam. Source material comes from Anthropic's official course "Building with the Claude API". Each lesson produces 6 study note variants.

## Output Format: 6 Variants Per Lesson

For each source lesson, produce 6 files:

| File suffix | Audience | Language |
|-------------|----------|----------|
| `-eng-en.md` | Engineering Deep Dive | English |
| `-eng-zh-TW.md` | Engineering Deep Dive | 繁體中文（台灣） |
| `-eng-zh-CN.md` | Engineering Deep Dive | 简体中文 |
| `-pm-en.md` | PM Perspective | English |
| `-pm-zh-TW.md` | PM Perspective | 繁體中文（台灣） |
| `-pm-zh-CN.md` | PM Perspective | 简体中文 |

## Template Reference

**Read this file first to understand the format:**
- Engineering EN: `/Volumes/Muse_AI_Core/CCA-Learning/courses/introduction-to-model-context-protocol/03-resources-and-prompts/12-defining-prompts/study-notes/universal/12-defining-prompts-eng-en.md`
- PM EN: `/Volumes/Muse_AI_Core/CCA-Learning/courses/introduction-to-model-context-protocol/03-resources-and-prompts/12-defining-prompts/study-notes/universal/12-defining-prompts-pm-en.md`

## Required Sections (Engineering Deep Dive)

1. **Title** — `# {Lesson Title} — Engineering Deep Dive`
2. **Metadata table** — Exam Domain / Task Statements / Source
3. **One-Liner** — 1-2 sentence synthesis
4. **Main content** — 4-7 sections covering technical details, code examples, architecture
5. **Common Mistakes** — numbered list of 3-5 pitfalls
6. **Key Insight** — blockquote with the single most important takeaway
7. **CCA Exam Relevance** — bullet list mapping to CCA domains
8. **Flashcards** — table of 6-10 Q&A pairs for spaced repetition

## Required Sections (PM Perspective)

1. **Title** — `# {Lesson Title} — PM Perspective`
2. **Metadata table** — same as Engineering
3. **One-Liner** — PM-framed synthesis (business value, user impact)
4. **Mental Model / Analogy** — relatable framing (restaurant menu, factory line, etc.)
5. **Product Use Cases** — when to use / when NOT to use tables
6. **PM Decision Framework** — questions to ask when designing features
7. **Common PM Mistakes** — 3-5 PM-specific pitfalls
8. **Key Insight** — blockquote
9. **CCA Exam Relevance** — maps to CCA domains
10. **Flashcards** — table of 6-10 Q&A pairs

## CCA Domain Reference

| Domain | Weight | Topics |
|--------|--------|--------|
| D1 | 22% | Agentic Coding & Architecture — agents, workflows, tool use loop, multi-turn |
| D2 | 18% | Tool Design & MCP Integration — tool schemas, tool_choice, MCP primitives |
| D3 | 20% | Claude Code Configuration |
| D4 | 20% | AI Safety & Alignment |
| D5 | 20% | Enterprise Deployment — production patterns, eval, caching, streaming |

## Chapter → Domain Mapping

- **Ch04 Tool Use (lessons 32-43 + 38)** → Primary: D2 (18%), Secondary: D1 (22%)
  - Task statements: 2.1 (tool schemas), 2.2 (content blocks), 2.4 (multi-turn tool loops), 1.2 (agentic loop)
- **Ch08 Agents & Workflows (lessons 73-83)** → Primary: D1 (22%), Secondary: D5 (20%)
  - Task statements: 1.1 (agent vs workflow), 1.2 (agentic patterns), 5.3 (production deployment)

## Language Guidelines

- **English**: Direct, technical, active voice. Use American English spelling.
- **繁體中文（zh-TW）**: 台灣用語。技術名詞保留英文（tool use, schema, agent, workflow）。避免大陸用語如「服務器」「代碼」，用「伺服器」「程式碼」。
- **简体中文（zh-CN）**: 大陆用语。「服务器」「代码」「函数」。

## Content Guidelines

- **Fidelity to source**: extract the facts from the source .md, do not invent features or APIs not mentioned
- **Technical depth**: go beyond the source — explain WHY, not just WHAT. Include code snippets in Python that match Anthropic's API patterns
- **PM framing**: translate technical concepts into business value, user experience, product decisions
- **Flashcards**: must be testable — concrete answers, not vague concepts
- **Length**: aim for ~150-200 lines per variant (similar to reference template)

## File Naming

Target path pattern:
```
/Volumes/Muse_AI_Core/CCA-Learning/courses/building-with-the-claude-api/{chapter}/{lesson-dir}/study-notes/universal/{lesson-name}-{variant}.md
```

Where:
- `{chapter}` = `04-tool-use` or `08-agents-and-workflows` or `01-api-fundamentals`
- `{lesson-dir}` = full lesson directory name (e.g., `32-introducing-tool-use`)
- `{lesson-name}` = same as lesson-dir
- `{variant}` = `eng-en` | `eng-zh-TW` | `eng-zh-CN` | `pm-en` | `pm-zh-TW` | `pm-zh-CN`

Example:
```
/Volumes/Muse_AI_Core/CCA-Learning/courses/building-with-the-claude-api/04-tool-use/32-introducing-tool-use/study-notes/universal/32-introducing-tool-use-eng-en.md
```

## Execution Checklist

For each lesson in your assignment:
1. Read source .md
2. Write 6 variant files to the target path
3. Verify each file has all required sections
4. Do NOT commit (the orchestrator will handle git)

The target directories have been pre-created.
