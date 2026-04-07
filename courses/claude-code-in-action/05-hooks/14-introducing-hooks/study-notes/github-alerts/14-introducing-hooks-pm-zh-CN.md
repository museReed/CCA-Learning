# Introducing Hooks — PM Perspective

| 项目 | 内容 |
|------|------|
| 考试对应 | D3 — Claude Code Configuration & Workflows（占 20%） |
| Task Statements | 3.2（custom commands & hooks）、1.5（Agent SDK hooks） |
| 课程来源 | claude-code-in-action / 05-hooks / Lesson 14 |

---

## TL;DR


![Tool Execution Pipeline](../../visuals/tool-execution-pipeline-zh-TW.svg)
*圖：Claude Code 如何處理工具呼叫 — 模型提出請求，系統透過 Hook 攔截，再執行。*

Hooks 是 Claude Code 的「品管关卡」和「自动化触发器」。把它想成产品里的 business rule engine：在 AI 行动之前可以拦截审核（Pre），行动之后可以触发品质检查（Post）。PM 需要理解这个机制，因为它决定了「哪些 AI 行为是可以被保证的」vs「哪些只是尽力而为」。

---

## Why PMs Need to Understand Hooks

作为 PM，你不需要自己写 hook，但你需要知道：

1. **什么行为可以被 100% 保证** — Hook 能做到的事
2. **什么行为只能尽力而为** — Prompt instruction 能做到的事
3. **怎么跟工程师沟通需求** — 知道什么时候该要求用 hook

这直接影响你写 PRD 时的 acceptance criteria 和 risk assessment。

---

## Mental Model: 机场安检 vs 机上广播

| | PreToolUse Hook | PostToolUse Hook | Prompt Instruction |
|--|----------------|-----------------|-------------------|
| 类比 | 机场安检 — 不符合就不能登机 | 落地后海关 — 已入境但可补验 | 机上广播「请系安全带」 |
| 保证程度 | **100% 确定**会执行 | **100% 确定**会执行 | 95-99%（AI 可能忽略） |
| 能阻止吗？ | 可以阻止行动 | 不能（已发生），但可以善后 | 不能保证 |
| 适用场景 | 合规、安全、权限控制 | 品质检查、格式化、通知 | 风格偏好、语气建议 |

> [!IMPORTANT]
> **考试核心哲学（PM 必记）**
>
> - **Architecture > Prompt** — 能用结构解决的，不要靠提示
> - **Deterministic > Probabilistic** — 能用程序保证的，不要靠 AI 自觉

---

## Product Scenario Walkthrough

### Scenario: Customer Support Agent

你在规划一个 AI 客服系统，需求如下：

| 需求 | 实现方式 | 为什么 |
|------|----------|--------|
| 退款 > $500 必须人工审核 | **PreToolUse hook** — 拦截 `process_refund`，金额超标就 block 并转人工 | 合规需求，不能有任何漏网之鱼 |
| 回复语气要友善 | **Prompt instruction** | 偏好性需求，偶尔偏差可接受 |
| 每次回复后记录到 CRM | **PostToolUse hook** — 回复完自动写入 | 流程自动化，保证每次都执行 |
| 优先推荐自助方案 | **Prompt instruction** | 策略偏好，有弹性空间 |

> [!TIP]
> **PM 决策框架**
>
> 写 PRD 时问自己——「如果 AI 在这个行为上 100 次有 1 次出错，后果是什么？」
> - 后果严重（财务损失、合规违规）→ **必须用 hook**
> - 后果轻微（语气稍差、格式不一致）→ **prompt instruction 足够**

---

## Configuration: 谁控制什么

Hooks 有三层设定，这对 PM 来说很重要，因为它决定了**团队治理**：

| 层级 | 谁管 | 典型用途 | PM 关心的 |
|------|------|----------|-----------|
| Global (`~/.claude/settings.json`) | 个人开发者 | 个人偏好（自动 format） | 不可控，每人不同 |
| Project shared (`.claude/settings.json`) | Tech Lead / 团队 | 团队标准（lint、测试） | **可以要求团队统一** |
| Project local (`.claude/settings.local.json`) | 个人 | 个人覆写 | 无法强制 |

> [!TIP]
> **PM Takeaway**
>
> 如果你的 acceptance criteria 需要某个 hook 生效，确保它在 **Project shared** 层级，不是靠个人设定。

---

## Hooks in the Bigger Picture

Hooks 在考试中跨多个 Domain 出现：

| Domain | Hooks 怎么考 |
|--------|-------------|
| **D1 Agentic Architecture (27%)** | Agent SDK 的 hook 机制 — PostToolUse 做 data normalization、PreToolUse 做 policy enforcement |
| **D3 Claude Code Config (20%)** | Settings hierarchy、`/hooks` command、matcher syntax |
| **D5 Reliability (15%)** | Hook 作为 validation gate，确保 pipeline step 之间的品质 |

---

## Instructor Insights（影片补充）

讲师影片中有几个 PM 该注意的 nuance：

1. **Hook 拿到完整的 tool call details** — 不只是 "Claude 想写档案"，而是 "Claude 想用 Write tool 写 `/src/auth.ts`，内容是..."。这意味着 hook 可以做非常精细的判断
2. **PostToolUse 的 feedback loop** — Claude 收到 hook 的回馈后会自动修正。这不需要人工介入，是 **self-healing** 的设计
3. **讲师原话："Wrapping your head around hooks can be really challenging"** — 如果你的工程师需要时间理解这个概念，这是正常的

---

## Practice Questions

### 第一题：Customer Support 情境

你的 AI 客服 agent 处理退货和退款。公司政策规定：任何财务操作前必须验证身份。目前这个规则是透过 system prompt 指示来 enforce。有客户回报收到退款时没有被要求验证身份。建议的修正方式是什么？

- A. 加强 system prompt，用更强硬的语气要求验证
- B. 加入 few-shot examples 示范正确的验证流程
- C. 实作 PreToolUse hook，在 `get_customer` 回传已验证状态前，block `process_refund`
- D. 加入 PostToolUse hook，在退款处理后检查是否有做身份验证

<details><summary>答案与解析</summary>

**C** — 财务操作前的身份验证是合规需求。Prompt-based 方案（A、B）有非零失败率——客户回报已经证明了这点。PostToolUse（D）太迟——退款已经处理完。PreToolUse hook 的 prerequisite gate 是 deterministic 的。

> [!IMPORTANT]
> 考试哲学：**Deterministic > Probabilistic**、**Validation > Trust**

**PM 重点**：这就是为什么 PRD 里写 "must verify identity" 不够——你需要指定 enforcement mechanism 是 hook 而非 prompt。
</details>

### 第二题：Code Review CI 情境

你的团队把 Claude Code 整合到 CI pipeline 做自动化 PR review。工程师反映 Claude 有时候会修改 migration 档案，导致部署问题。你会建议什么？

- A. 在 CLAUDE.md 加上「不要修改 migration 档案」
- B. 设定 PreToolUse hook，block 对 `migrations/` 目录的 Write/Edit 操作
- C. 设定 PostToolUse hook，在 Claude 修改 migration 档案后 revert 变更
- D. 建立一个独立的 review pipeline，排除 migration 档案不给 Claude 看

<details><summary>答案与解析</summary>

**B** — PreToolUse hook 在问题发生前 deterministic 地阻止。A 是 prompt-based（对严重后果的场景不可靠）。C 是事后补救，增加复杂度。D 移除了有价值的 context，Claude 可能需要这些来 review migration 相关的 code。

**PM 重点**：「有时候会」（sometimes）= 你需要 deterministic solution。语气偶尔不够友善 → prompt 就够；会改到 migration 导致 deployment issue → 严重后果 → 用 hook。
</details>

### 第三题：Multi-Agent Research 情境

一个 coordinator agent 将研究任务分派给多个 subagent。不同的 backend API 回传不同格式的日期（Unix timestamp、ISO 8601、locale-specific string）。synthesis subagent 经常误解日期。最佳方案是什么？

- A. 在 synthesis subagent 的 prompt 里加入日期格式说明
- B. 在每个 backend tool 上实作 PostToolUse hook，在 agent 处理结果前把日期统一转成 ISO 8601
- C. 让 coordinator agent 在传给 synthesis subagent 前先转换日期
- D. 用 few-shot examples 示范不同的日期格式

<details><summary>答案与解析</summary>

**B** — PostToolUse hooks 在 tool boundary 做 data normalization，是最可靠且可维护的方案。A 和 D 是 probabilistic。C 增加了 coordinator 的复杂度，且要求它理解所有可能的日期格式。

> [!IMPORTANT]
> 考试哲学：**Architecture > Prompt**、**Deterministic > Probabilistic**

**PM 重点**：Data normalization 是 infra 层面的问题，不应该靠 AI 「理解」不同格式。就像你做 data pipeline 时不会靠前端自己转日期格式一样。
</details>
