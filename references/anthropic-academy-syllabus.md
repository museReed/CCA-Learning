# Anthropic Academy — Course Syllabus Index

> Source: https://anthropic.skilljar.com (March 2026)
> Note: Courses are interactive (video + quiz), not downloadable PDFs.

## CCA-Relevant Courses (7 of 15)

### 1. Claude Code in Action
**URL**: https://anthropic.skilljar.com/claude-code-in-action
**CCA Domain**: D3 Claude Code Configuration & Workflows (20%)

Topics:
1. **Coding Assistant Architecture** — How AI systems interact with codebases through tool integration
2. **Claude Code's Tool Use System** — Leveraging multiple tools for multi-step tasks
3. **Context Management Techniques** — Maintaining context, referencing project resources
4. **Visual Communication Workflows** — Using visual inputs, advanced planning features
5. **Custom Automation Creation** — Building reusable custom commands/automations
6. **MCP Server Integration** — Integrating external tools and services
7. **GitHub Workflow Integration** — Automated code review, version control
8. **Thinking and Planning Modes** — Different reasoning approaches for complexity levels

Prerequisites: CLI familiarity, basic Git

---

### 2. Building with the Claude API
**URL**: https://anthropic.skilljar.com/claude-with-the-anthropic-api
**CCA Domains**: D1 Agentic Architecture (27%), D4 Prompt Engineering (20%)

Topics:
1. **API Fundamentals** — Authentication, API key management, request config
2. **Conversation Management** — Single/multi-turn conversations, message formatting
3. **Model Control** — System prompts, temperature, streaming, structured outputs
4. **Prompt Evaluation** — Test dataset generation, automated grading
5. **Prompt Engineering** — XML structuring, example-based learning, directives
6. **Tool Integration** — Custom tools, batch operations, web search
7. **RAG Systems** — Text chunking, embeddings, BM25, contextual retrieval
8. **Extended Features** — Extended thinking, image analysis, PDF, citations
9. **Optimization** — Prompt caching strategies
10. **MCP Development** — Model Context Protocol servers and clients
11. **Anthropic Apps** — Claude Code and Computer Use deployment
12. **Agent Systems** — Parallelization, chaining, routing workflows

Prerequisites: Backend development experience

---

### 3. Introduction to Model Context Protocol
**URL**: https://anthropic.skilljar.com/introduction-to-model-context-protocol
**CCA Domain**: D2 Tool Design & MCP Integration (18%)

Topics:
1. **MCP Architecture** — How tool definition/execution delegates to specialized servers
2. **Transport System** — Transport-agnostic communication, message types
3. **Request-Response Flow** — User queries → MCP clients → external services → Claude
4. **Building MCP Servers** — Python SDK with decorators (no manual JSON schemas)
5. **Document Management** — Tools for reading and editing documents
6. **MCP Server Inspector** — Browser-based testing and debugging
7. **Resources** — Exposing read-only data (static and templated URIs)
8. **Resource Reading** — Proper MIME type handling
9. **Prompts** — Pre-crafted instructions for common workflows
10. **Primitives Decision** — Tools (model-controlled) vs Resources (app-controlled) vs Prompts (user-controlled)
11. **Integration Patterns** — Autocomplete, context injection

Prerequisites: Python, JSON/HTTP basics

---

### 4. Model Context Protocol: Advanced Topics
**URL**: https://anthropic.skilljar.com/model-context-protocol-advanced-topics
**CCA Domain**: D2 Tool Design & MCP Integration (18%)

Topics:
1. **Sampling** — Language model integration implementation
2. **Progress & Logging** — Notifications using context objects
3. **Roots** — File access with permission systems
4. **JSON Message Architecture** — MCP communication protocol
5. **Stdio Transport** — Mechanisms and initialization handshakes
6. **StreamableHTTP Transport** — Server-Sent Events (SSE)
7. **HTTP Transport Limitations** — Configuration flags
8. **Production Scaling** — Stateless vs stateful considerations
9. **Transport Selection** — Criteria for deployment requirements

Prerequisites: Python async, JSON, HTTP, basic SSE

---

### 5. Introduction to Agent Skills
**URL**: https://anthropic.skilljar.com/introduction-to-agent-skills
**CCA Domain**: D3 Claude Code Configuration & Workflows (20%)

Topics:
1. **Skill Fundamentals** — What Skills are vs CLAUDE.md, hooks, subagents
2. **Building Skills** — Creating SKILL.md, frontmatter, effective descriptions
3. **Configuration** — Directory organization, context window efficiency, progressive disclosure
4. **Advanced Options** — Restricting tool access (allowed-tools), scripts without context
5. **Distribution** — Team sharing via repos, plugins, org-wide deployment
6. **Integration** — Wiring Skills into custom subagents
7. **Troubleshooting** — Non-triggering skills, priority conflicts, runtime errors

---

### 6. Introduction to Subagents
**URL**: https://anthropic.skilljar.com/introduction-to-subagents
**CCA Domains**: D1 Agentic Architecture (27%), D3 Claude Code (20%)

Topics:
1. **How Sub-agents Work** — Separate context windows, input flow, summary return
2. **Creating Custom Sub-agents** — `/agents` command, code reviewers, doc generators
3. **Designing Effective Sub-agents** — Structured output, obstacle reporting, tool limits
4. **When to Use (and Not)** — Optimal use cases, common anti-patterns

---

### 7. Claude 101
**URL**: https://anthropic.skilljar.com/
**CCA Domain**: Foundation (assumed knowledge)

Topics: Claude usage patterns, capabilities, practical workflows


## Other Courses (not directly CCA-relevant)

| Course | Focus |
|--------|-------|
| Introduction to Claude Cowork | Collaborative Claude usage |
| AI Fluency: Framework & Foundations | General AI literacy |
| AI Fluency for Educators | Teaching with AI |
| AI Fluency for Students | Student AI usage |
| Claude with Amazon Bedrock | AWS integration |
| Claude with Google Cloud Vertex AI | GCP integration |
| Teaching AI Fluency | Instructor guide |
| AI Fluency for Nonprofits | Nonprofit AI adoption |
