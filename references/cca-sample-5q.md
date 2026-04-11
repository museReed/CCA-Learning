CCA Foundations — Free Sample Questions

claudecertified.com

CLAUDE CERTIFIED ARCHITECT

Foundations (CCA-F) Certification

5 Domains

$99/Attempt

60 Questions

Pass Score: 720/1000

and style of the real exam.

Exam Domain Coverage

5 FREE Sample Questions

March 12, 2026. It validates your ability to design and ship production-grade Claude applications — covering

agentic architecture, MCP integration, Claude Code workflows, prompt engineering, and context management.

The  Claude  Certified  Architect  –  Foundations  is  Anthropic's  first  official  technical  certification,  launched

These 5 questions are drawn directly from the official exam scenarios to give you a feel for the format, difficulty,

claudecertified.com
claudecertified.com

H marks the correct answer for each question. Full explanation provided below each question.

Prompt Engineering & Structured Output

Claude Code Configuration & Workflows

Agentic Architecture & Orchestration

Context Management & Reliability

Tool Design & MCP Integration

Domain

Weight

27%

18%

20%

20%

15%

#

1

2

3

4

5

© 2026 claudecertified.com  |  Claude Certified Architect – Foundations

Page 1

CCA Foundations — Free Sample Questions

claudecertified.com

Sample Questions — One from Each Domain

Q
1

Domain 1 · Agentic Architecture & Orchestration · Scenario: Customer Support Resolution Agent

address this reliability issue?

Production data shows that in 12% of cases your agent skips get_customer entirely and

calls  lookup_order  using  only  the  customer's  stated  name,  occasionally  leading  to

misidentified  accounts  and  incorrect  refunds.  What  change  would  most  effectively

C) Add few-shot examples showing the agent always calling get_customer first, even when customers
volunteer order details.

B) Enhance the system prompt to state that customer verification via get_customer is mandatory before any
order operations.

D) Implement a routing classifier that analyzes each request and enables only the subset of tools appropriate
for that request type.

H A) Add a programmatic prerequisite that blocks lookup_order and process_refund calls until
get_customer has returned a verified customer ID.

claudecertified.com
claudecertified.com

A) Add few-shot examples to the system prompt demonstrating correct tool selection patterns, with 5–8
examples showing order-related queries routing to lookup_order.
H B) Expand each tool's description to include input formats, example queries, edge cases, and
boundaries explaining when to use it versus similar tools.

3 Correct: A | Programmatic enforcement provides deterministic guarantees. Prompt-based approaches (B, C)
have non-zero failure rates — unacceptable for financial operations. Option D addresses availability, not
ordering.

accept  similar  identifier  formats.  What  is  the  most  effective  first  step  to  improve  tool

orders (e.g., 'check my order #12345'), instead of calling lookup_order. Both tools have

Production  logs  show  the  agent  frequently  calls  get_customer  when  users  ask  about

minimal  descriptions  ('Retrieves  customer  information'  /  'Retrieves  order  details')  and

Domain 2 · Tool Design & MCP Integration · Scenario: Customer Support Resolution Agent

selection reliability?

Q
2

C) Implement a routing layer that parses user input before each turn and pre-selects the appropriate tool
based on detected keywords.

D) Consolidate both tools into a single lookup_entity tool that accepts any identifier and internally determines
which backend to query.

© 2026 claudecertified.com  |  Claude Certified Architect – Foundations

Page 2

CCA Foundations — Free Sample Questions

claudecertified.com

3 Correct: B | Tool descriptions are the primary mechanism LLMs use for tool selection. Minimal descriptions
leave models unable to differentiate similar tools. Option B fixes the root cause directly. Few-shot examples (A)
add overhead without fixing the description gap.

Q
3

D) In a .claude/config.json file with a commands array.

Domain 3 · Claude Code Configuration & Workflows · Scenario: Code Generation with Claude Code

C) In the CLAUDE.md file at the project root as a special command block.

clone or pull the repository. Where should you create this command file?

You  want  to  create  a  custom  /review  slash  command  that  runs  your  team's  standard

code review checklist. This command should be available to every developer when they

H A) In the .claude/commands/ directory in the project repository.
B) In ~/.claude/commands/ in each developer's home directory.

3 Correct: A | Project-scoped commands in .claude/commands/ are version-controlled and automatically
available to all developers on clone/pull. ~/.claude/commands/ (B) is for personal commands not shared via
version control.

claudecertified.com
claudecertified.com

H A) Use batch processing for the technical debt reports only; keep real-time calls for pre-merge
checks.

next morning. A manager proposes switching both to the Message Batches API for its

Your team wants to reduce API costs for automated analysis. Currently real-time Claude

calls power two workflows: (1) a blocking pre-merge check that must complete before

developers can merge, and (2) a technical debt report generated overnight for review the

D) Switch both to batch processing with a timeout fallback to real-time if batches take too long.

B) Switch both workflows to batch processing with status polling to check for completion.

C) Keep real-time calls for both workflows to avoid batch result ordering issues.

Domain 4 · Prompt Engineering & Structured Output · Scenario: Claude Code for Continuous Integration

50% cost savings. How should you evaluate this proposal?

Q
4

3 Correct: A | The Message Batches API has up to 24-hour processing time with no guaranteed latency SLA
— unsuitable for blocking pre-merge checks. Overnight reports are latency-tolerant and benefit from the 50%
cost savings. Option C reflects a misconception: batch results are correlatable via custom_id.

Q
5

Domain 5 · Context Management & Reliability · Scenario: Multi-Agent Research System

© 2026 claudecertified.com  |  Claude Certified Architect – Foundations

Page 3

CCA Foundations — Free Sample Questions

claudecertified.com

After  running  your  multi-agent  research  system  on  the  topic  'impact  of  AI  on  creative

industries', you observe that each subagent completes successfully. However, the final

reports cover only visual arts, completely missing music, writing, and film production.

When you examine the coordinator's logs, you see it decomposed the topic into three

subtasks: 'AI in digital art creation', 'AI in graphic design', and 'AI in photography'. What

is the most likely root cause?

C) The web search agent's queries are not comprehensive enough and need to be expanded to cover more
creative industry sectors.

D) The document analysis agent is filtering out sources related to non-visual creative industries due to overly
restrictive relevance criteria.

3 Correct: B | The coordinator's logs reveal the root cause directly: only visual arts subtasks were assigned.
The subagents executed correctly within their scope. Options A, C, and D incorrectly blame downstream
agents that were working properly.

A) The synthesis agent lacks instructions for identifying coverage gaps in the findings it receives from other
agents.
H B) The coordinator agent's task decomposition is too narrow, resulting in subagent assignments
that don't cover all relevant domains of the topic.

claudecertified.com
claudecertified.com

© 2026 claudecertified.com  |  Claude Certified Architect – Foundations

Page 4

CCA Foundations — Free Sample Questions

claudecertified.com

Want All 105 Practice Questions?

3 105 Practice Questions

3 Official Sample Questions

What's Included in the Full Package

One question per task statement across all 5 domains and 6 scenarios

Full Question Bank · Domain Cheat Sheet · Exam Strategy Guide

n claudecertified.com

question with full explanations and a Quick Reference Cheat Sheet.

Get the complete CCA-F question bank — all 5 domains, all 6 scenarios, every

claudecertified.com
claudecertified.com

25 critical concepts — stop_reason, tool_choice, CLAUDE.md hierarchy,
Batch API rules and more

Get the full 105-question CCA-F practice pack at claudecertified.com and go into your

All 12 Anthropic official sample questions included and labelled

Every question includes why each option is right or wrong

The 7 most common exam traps and how to spot them

Understand where to focus your preparation time

3 Quick Reference Cheat Sheet

3 Domain Weight Breakdown

exam fully prepared.

3 Key Mental Models

3 Full Explanations

© 2026 claudecertified.com  |  Claude Certified Architect – Foundations

Page 5

