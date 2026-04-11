# Sending Tool Results — PM Perspective（简中）

| 项目 | 内容 |
|------|------|
| 考试领域 | D2 — Tool Design & MCP Integration (18%) / D1 — Agentic Architecture (22%) |
| Task Statements | 2.4（tool_result block 格式）、2.2（content block 处理）、1.2（收尾 tool-use loop） |
| 来源 | building-with-the-claude-api / 04-tool-use / Lesson 37 |

---

## 一句话总结

把 tool 结果送回 Claude 是「收件回执」的动作——一个格式严格的数据包，用来收掉「Claude 要了一个东西」和「Claude 有足够信息可以回答」之间的循环。

---

## 心智模型：餐厅点餐票系统

想象一间忙碌的餐厅厨房：

| 厨房流程 | Claude tool-use 流程 |
|----------|---------------------|
| 前厅写票 #47：「汉堡，五分熟」 | Claude 发出 `ToolUseBlock(id="toolu_47", name="cook", input={"item":"burger"})` |
| 厨师做汉堡 | 你的代码执行函数 |
| 厨师把票 #47 夹在盘子上 | 你送回 `tool_result` block，`tool_use_id="toolu_47"` |
| 盘子送到票 #47 对应的桌子 | Claude 用结果回答用户 |

票号（`tool_use_id`）是神圣的。厨师忘了夹票，没人知道汉堡要送哪一桌。一张票回两个汉堡、或两张票只回一个，整个出餐流程就会垮。Anthropic API 处理 tool result 的方式就是这样。

---

## 为什么 PM 要在乎

Tool result 是大多数 tool-use 功能在生产环境坏掉的故障面：

| 故障模式 | 用户看到的症状 |
|----------|---------------|
| 后端在 tool 执行到一半 crash、丢掉结果 | Claude 整个卡住或回「抱歉我无法协助」 |
| 后端忘了用 `is_error: True` 标错误 | Claude 自信地给出错误答案（hallucinate 成功） |
| 多个 tool call 但后端只回一个结果 | 用户看到 400，整段对话救不回来 |
| 后端直接塞 dict 而没 serialize | 对话坏在看不懂的 validation error |

每一个都是产品质量问题。懂 tool-result 契约的 PM 可以写出更好的 acceptance criteria，在 staging 就拦下来，不要等到上线日。

---

## 产品应用场景：错误可见度

Tool 失败不只是工程问题——它是 UX 决策：

| 策略 | 什么时候用 | UX 影响 |
|------|-----------|---------|
| 通过 `is_error: True` 把错误丢给 Claude | 大多数情况 | Claude 会自然解释问题（「我抓不到股价，API 好像挂了，要再试一次吗？」） |
| 在 Claude 看到前就拦下错误 | Rate limit、安全错误 | 自己做 UI toast，完全绕过 Claude |
| 静默指数退避重试 | 暂时性网络错误 | 用户看不到，但会增加延迟 |

默认模式——`is_error: True`——会给 Claude 足够信息优雅降级。跳过这个会让 Claude 幻觉出成功，这是最糟的用户体验。

---

## PM 决策框架

任何使用 tool 的功能，PRD 都应该回答：

| 问题 | 为什么重要 |
|------|-----------|
| 每个 tool 的 timeout 预算是多少？ | 慢 tool 会让 UX 出现死区，需要 progress event |
| 如何把 tool 错误传达给用户？ | 通过 Claude（`is_error: True`）还是通过自己的 UI？ |
| Claude 如果连调同一个 tool 两次怎么办？ | Cache？幂等性？权限升级？ |
| Claude 可以看到敏感的错误细节吗？ | 送进 Claude 前要剥掉内部 stack trace |
| 如何记录 tool_use_id 配对以便观测？ | Debug 生产对话时非常关键 |

---

## 常见 PM 错误

1. **PRD 没写错误处理**——工程默认「log 然后丢掉」，会默默坏掉对话
2. **以为 tool result 就是函数返回值**——它有严格格式（role=user、content block 有特定字段），会限制工程做法
3. **忽略多 tool 同时调用的情况**——「Claude 一次叫两个 tool 怎么办」是真的设计问题，不是 edge case
4. **没编观测性预算**——tool_use_id 跟踪对 debug 生产环境很重要，但通常一开始没排进 scope
5. **把 `is_error` 当工程细节**——它其实是产品决策：要让 Claude 解释失败，还是用自己的 UI 挡掉？

---

> **Key Insight**
>
> 每一个 `tool_result` 都是用 `tool_use_id` 做 key 的回执。PM 教训：tool 失败其实是伪装的产品功能。选「Claude 看到错误并解释」（`is_error: True`）还是「绕过 Claude 自己显示错误」是 UX 决策，直接影响用户信任和恢复率。不要随便上线——要刻意设计。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：记住 `tool_result` block 的字段，以及它住在 user role message 里。
- **D1（Agentic Architecture）**：理解 tool_result 是 agentic 请求/响应配对的后半段。
- 考题会描述 tool 失败的情境，问你如何告知 Claude——答案几乎永远是「送一个 `is_error: True` 的 `tool_result` block」。

---

## Flashcards

| 题目 | 答案 |
|------|------|
| 用什么比喻来理解 `tool_use_id` / `tool_result` 配对？ | 餐厅点餐票——每张票号都要从前厅送到厨房再送回桌子 |
| 为什么 `is_error: True` 是 PM 要在乎的事，不只是工程 flag？ | 它决定 Claude 要不要跟用户解释失败，或是 UI 自己挡掉——这是影响信任的 UX 决策 |
| Tool result 最糟的故障模式是什么？ | 静默成功——忘了填 `is_error: True`，让 Claude 幻觉出成功结果 |
| 任何使用 tool 的功能 PRD 必须写什么？ | Timeout 预算、错误处理策略、多 tool 行为、tool_use_id 的观测性 |
| 为什么 `content` 直接塞 dict 会坏？ | API 要求 `content` 是字符串（或 block list），dict 要 JSON serialize |
| Claude 一次叫两个 tool，要回几个结果？ | 恰好两个——每个 `ToolUseBlock` 都要在同回合有对应的 `tool_result` |
| `tool_result` block 放在 message 结构的哪里？ | 放在 user role message 的 `content` 数组里 |
| 生产中后端丢了一个 tool result 会怎样？ | 下一次 API 调用回 400，对话救不回来，用户会看到错误 |
