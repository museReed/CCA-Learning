# 项目概览：提醒应用 — Engineering Deep Dive

| 项目 | 内容 |
|------|------|
| 考试 Domain | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.1（tool schema 设计）、1.2（agentic loop 基础）、1.1（把功能拆成 tool 组合） |
| 来源 | building-with-the-claude-api / 04-tool-use / Lesson 33 |

---

## 一句话总结

提醒应用项目示范 tool use 的核心设计原则：把模型能力的缺口拆成**一个个小型、单一职责的 tool**，让 Claude 在推理时自行组合，而不是硬写一个「什么都包」的大函数。

---

## 目标用户体验

```
用户：「帮我设一个提醒，我要看医生。是下下个星期四。」

Claude：「好，我会提醒你。」
```

表面上超简单 — 但底下藏了三个 base model 解不了的能力缺口。

---

## Claude 与目标之间的三个缺口

| 缺口 | 为什么重要 | 对应的 tool |
|------|------------|-------------|
| **时间感知有限** | Claude 大概知道今天日期，但不知道此刻精确时间 | `get_current_datetime` |
| **日期运算容易算错** | 「下下个星期四」需要日期相加；LLM 常会算错星期几、跨月处理也会出问题 | `add_duration_to_datetime` |
| **没有提醒能力** | Claude 本身没办法把排期提醒写到任何系统里 | `set_reminder` |

每个缺口恰好对应一个 tool。这不是巧合 — 就是设计原则本身。

---

## 设计原则：一个缺口 = 一个 tool

```
┌────────────────────────────────────────┐
│         用户目标：设定提醒               │
└────────────────────────────────────────┘
             │
   拆成原子步骤
             │
 ┌───────────┼────────────┐
 ▼           ▼            ▼
get_current_  add_duration_  set_reminder
datetime      to_datetime
(现在)        (现在 + 7 天)  (写入)
```

为什么原子 tool 胜过一个「parse_and_set_reminder」大函数：

1. **可组合** — `add_duration_to_datetime` 可以被其他日期运算需求（生日、截止日、续约）复用。
2. **可测试** — 每个 tool 只做一件事，单元测试很简单。
3. **可观测** — log 能清楚看到哪一步挂掉，而不是「大函数返回了错东西」。
4. **发挥模型强项** — Claude 擅长规划序列。如果你把顺序预先写死在一个函数，就浪费了这个能力。
5. **优雅降级** — `set_reminder` 失败时，已经算好的时间戳不会连带丢失。

---

## 这个项目隐含的 Agent Loop

虽然每个 tool 都很简单，三个 tool 组合起来代表对话可能要**三轮** tool-use turn，Claude 才会输出最终答案：

```
Turn 1: user → "帮我下星期四提醒"
Turn 2: Claude → tool_use get_current_datetime
Turn 3: app   → tool_result "2026-04-11 14:30:00"
Turn 4: Claude → tool_use add_duration_to_datetime(now, +7 days)
Turn 5: app   → tool_result "2026-04-18 14:30:00"
Turn 6: Claude → tool_use set_reminder(when="2026-04-18 14:30:00", ...)
Turn 7: app   → tool_result "ok, reminder created"
Turn 8: Claude → "好，我会提醒你。"  (stop_reason=end_turn)
```

这就是最小可行的 **agent loop** 示例：Claude 自行规划 tool call 的顺序，完全由用户的自然语言输入驱动。你的代码不会写死顺序 — 只是重复执行 Claude 下一步要求的任何 tool，直到 `stop_reason != "tool_use"`。

---

## 渐进式构建顺序

课程一次建一个 tool，最简单的先做。这与任何 tool-use 项目的 best practice 一致：

1. **先做 read-only 的 tool**（`get_current_datetime`）— 无副作用，最容易测。
2. **接着做 pure-function 的 tool**（`add_duration_to_datetime`）— 确定性，仍然无外部副作用。
3. **最后才做有副作用的 tool**（`set_reminder`）— 持久化、失败模式、审计轨迹。

这个顺序也是安全梯度。Read-only tool 出错风险低；写入 tool 需要更多验证与测试。

---

## 这个项目教我们如何 Scoping AI 功能

底层功课是**AI 功能的 scoping**。一个 naive 的工程师可能会写：

```python
def handle_reminder_request(user_text: str) -> str:
    # 解析文字、做所有事、返回一句确认
    ...
```

...然后试着 prompt Claude 去调这个巨型函数。会失败因为：

- 你把所有苦工（解析、日期运算、持久化）又搬回命令式代码里。
- Claude 没机会推理，变成「文字转 function call」的分类器。
- 你失去在其他功能复用这些能力的机会。

Tool use 范式把这个**反过来**：给 Claude 小的 primitive，让它去编排。这是从「LLM 只是个聪明的字符串函数」过渡到「LLM 是个 planner」的桥梁。

---

## 常见错误

1. **把多个能力塞进一个 tool** — 例如一个 `schedule_reminder(natural_language_time)` 内部解析字符串。请拆开。
2. **写死 tool 调用顺序** — 让 Claude 决定。你的代码只负责派发它下一步要什么。
3. **从写入 tool 开始做** — 先做 read-only tool，比较安全可以反复迭代。
4. **跳过玩具项目阶段** — 直接跳进生产代码，会让失败模式在真实用户上爆炸。
5. **没规划 multi-turn loop** — 即便是简单功能都可能要 3+ 次 tool call；你的 message loop 必须能处理任意轮数。

> **Key Insight**
>
> 提醒项目是**能力拆解**（capability decomposition）的案例研究：模型的每个原生限制恰好对应一个原子 tool，由 Claude 在推理时组合起来。这个反转 — 「给模型 primitive，让它规划」 — 正是 CCA 考试 D1（agentic architecture）反复测验的心智转换。看到多步骤的自然语言目标就该想到它。

---

## CCA 考试重点

- **D1（Agentic Architecture）**：理解单一用户请求可能需要多轮 tool call 的 loop，全部由模型规划。
- **D2（Tool Design & MCP Integration）**：拆解原则 — 一个能力缺口 = 一个 tool。
- 考题常见模式：题目描述一个功能（「下星期提醒我」）然后问该设计几个 tool 或哪种 tool — 答案会强调原子 tool 让 Claude 组合。

---

## Flashcards

| Front | Back |
|-------|------|
| 提醒项目的目标用户交互是什么？ | 「帮我设一个提醒，我要看医生。是下下个星期四。」→「好，我会提醒你。」 |
| 提醒项目识别出哪三个能力缺口？ | 时间感知有限、日期运算不可靠、没有内建提醒机制。 |
| 项目里建了哪三个 tool？ | `get_current_datetime`、`add_duration_to_datetime`、`set_reminder`。 |
| 为什么要做三个小 tool 而非一个大 tool？ | 可组合、可测试、可观测、发挥模型推理强项、优雅降级。 |
| Tool 是以什么顺序引入，为什么？ | 最简单、read-only 的先（`get_current_datetime`）、再 pure function、最后才是有副作用的（`set_reminder`）— 安全梯度。 |
| 一次提醒请求可能要几轮 tool-use turn？ | 最多三轮 — 每个 tool 一轮 — 才会让 Claude 输出最终自然语言确认。 |
| 这个项目示范的设计原则是？ | 一个能力缺口 = 一个原子 tool；让 Claude 规划组合。 |
| 「LLM as planner」是什么意思？ | 不把 LLM 当作把文字分类到一个大函数的东西，而是给它小 primitive 让它去编排。 |
