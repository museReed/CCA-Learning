# 介绍 Tool Use — PM Perspective

| 项目 | 内容 |
|------|------|
| 考试 Domain | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 1.2（agentic loop 基础）、2.1（tool schema 设计）、2.4（multi-turn tool loop） |
| 来源 | building-with-the-claude-api / 04-tool-use / Lesson 32 |

---

## 一句话总结

Tool use 是让 Claude 从「博学的聊天机器人」变成「能干的队友」的功能 — 也是任何依赖实时数据或真实动作的产品，想把 AI 功能做成商业可行的关键。

---

## 心智模型：酒店礼宾

想象一位酒店礼宾读过所有旅游书，但被规定永远不能离开大厅。

- 问这座城市的历史 — 答得完美。
- 问「那家餐厅现在还开着吗？」— 礼宾只能耸肩。

Tool use 就像给这位礼宾一部**电话和一份可拨打的电话清单**。现在你问那家餐厅，他拿起电话打过去问，拿到答案再回你。从客人角度看，礼宾突然变得超级有用 — 可是他并没有变聪明，只是**能接触到外面的世界了**。

这是 Claude API 对 PM 最大的那一把钥匙。

---

## PM 为什么要关心

过去一年出货的 AI 功能，几乎没有哪个不依赖 tool use。下面这些需求都在暗示「你需要 tools」：

- 「显示这位客户最新的订单」
- 「帮我周二下午三点约个会」
- 「总结这张 Jira 工单目前的状态」
- 「发一封提醒邮件给团队」
- 「我用户要去的城市现在天气怎样？」

没有 tools，上面每一题的答案都是「我不知道」。有 tools 就能拿到实时、可信、可执行的答案。

---

## 产品使用场景

### 非用 Tool Use 不可的场景

| 用户需求 | 为什么只有 tools 能解 |
|----------|------------|
| 实时数据（股价、天气、比分） | 不在训练数据里 — 必须 live fetch |
| 私有/内部数据（CRM、内部 wiki） | 训练时从未看过 |
| 用户个人状态（我的日程、邮箱） | 因人而异 — 不可能 pre-train |
| 需要副作用的动作（发邮件、开工单） | 必须在现实世界真的发生 |
| 实时计算（查数据库、算实时数字） | 必须执行代码，不能幻觉 |

### Tool Use 过度设计的场景

| 用户需求 | 更好的替代方案 |
|----------|----------|
| 通用知识问答 | 基础模型就够 |
| 创意写作/头脑风暴 | 不需要外部数据 |
| 重写/总结用户粘贴的内容 | 文字已经在 prompt 里 |
| 解释概念 | 训练数据就足够 |

---

## 四步骤流程（白话版）

1. **App 问 Claude** — 「这是用户的问题，你可以用的工具在这。」
2. **Claude 举手** — 「我要旧金山的天气。帮我调用那个工具。」
3. **App 帮忙做** — 去调真正的天气 API，拿到真数据。
4. **App 回 Claude** — 「天气数据给你。」然后 Claude 综合所有东西，回给用户最终答案。

同一个用户问题会产生两次 API call。这有成本、延迟、可靠性的代价，排期时要考虑进去。

---

## PM 决策框架

规划 AI 功能时问自己：

| 问题 | 若是 | 意味着 |
|------|------|------|
| 答案依赖比模型训练日期更新的数据吗？ | 是 | 需要 tools |
| 这功能需要真的执行动作，不只是聊？ | 是 | 需要 tools |
| 这功能需要单个用户/租户的数据？ | 是 | 需要 tools |
| 用户会因为数据过期而抱怨？ | 是 | 需要 tools |
| 功能纯粹是语言处理（翻译、总结、改写）？ | 是 | 大概不需要 tools |

---

## 成本、延迟、可靠性的取舍

Tool use 强大但不是白吃的午餐。要先规划：

- **延迟加倍** — 每一轮 tool-using turn 至少两次 API round trip 加上工具本身的延迟。
- **Token 成本提高** — 对话历史每轮增长；tool 定义每次 call 都算 input token。
- **新的失败模式** — 上游 API 可能 fail、timeout、返回坏数据。app 必须优雅处理。
- **可观测性负担** — 必须 log 每次 tool call 的参数与结果，才能 debug 生产问题。

好的 PM 习惯：在 PRD 里加一条「tool reliability SLA」以及「tool 失败时的 fallback 行为」。

---

## PM 常犯的错

1. **相信 prompt engineering 能取代 tools** — 数据不在训练里，再神的 prompt 也变不出来。早点找工程师 escalate。
2. **低估延迟** — 两次 API call 加一次工具调用轻松吃掉 3 到 5 秒。记得设计 loading state。
3. **没预算处理 tool 错误** — 上游 API 会挂。要定义挂掉时用户看到什么。
4. **一次塞太多 tools** — 从一两个高价值工具开始。每多一个 tool 就多一条 bug 与模型混淆的路径。
5. **忘了 tool call 是可审计的** — 每一个 Claude 采取的动作都该被 log，尤其是写入操作。

> **Key Insight**
>
> Tool use 是决定你的 AI 产品是「花哨的 autocomplete」还是「真正助手」的那个功能。任何需要实时信息、个人数据或真实动作的产品需求，都暗示着要用 tool use。这个区别是 AI PM 的入门门槛，也是 CCA 考试 D1（agentic architecture）与 D2（tool design）重复出现的考点。

---

## CCA 考试重点

- **D2（Tool Design & MCP Integration）**：认识 tool_use request/response 模式；知道 `tool_result` 必须指回 `tool_use_id`。
- **D1（Agentic Architecture）**：tool use loop 是所有 agent pattern 的基础。Multi-turn reasoning with tools 是标准 agent 范例。
- 考题常见模式：场景问「Claude 该如何回答关于现在 X 的问题？」— 答案永远是「定义一个 tool 让 Claude 调用」。

---

## Flashcards

| Front | Back |
|-------|------|
| Tool use 的「酒店礼宾」比喻是什么？ | 礼宾读遍所有书但不能离开大厅。Tools 就是给他一部电话，让他可以打给外面的世界。 |
| 什么情况下 tool use 不是对的答案？ | 纯语言处理（翻译、总结、改写、头脑风暴）且不需要外部数据时。 |
| 加上 tool use 后延迟会怎样？ | 通常至少加倍 — 每个用户问题至少两次 API call 加上工具本身的延迟。 |
| 需要 tool use 的五大产品场景？ | 实时数据、私有/内部数据、用户个人状态、有副作用的动作、实时计算。 |
| 为什么 tool use 是 AI 产品的关键解锁？ | 它让 Claude 能获取实时数据、执行真实动作，从博学聊天机器人变成能干队友。 |
| 任何用 tool 的功能在 PRD 里一定要包含什么？ | Tool reliability SLA、tool 失败时的 fallback、loading state UX、log/审计需求。 |
| Prompt engineering 能替代 tools 抓实时数据吗？ | 不能 — 训练里没有的数据，再怎么巧妙的 prompt 也生不出来。 |
| 一次用到 tool 的用户问题要几次 API call？ | 至少两次 — 一次收 tool_use 请求，一次送 tool_result 拿最终答案。 |
