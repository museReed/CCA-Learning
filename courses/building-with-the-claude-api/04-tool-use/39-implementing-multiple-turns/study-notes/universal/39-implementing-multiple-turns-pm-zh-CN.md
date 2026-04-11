# Implementing Multiple Turns — PM Perspective（简中）

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture (22%) / D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 1.2（agentic loop 实现）、2.4（multi-turn tool loops）、1.3（multi-turn 对话管理） |
| 来源 | building-with-the-claude-api / 04-tool-use / Lesson 39 |

---

## 一句话总结

Agentic loop 是那个把 Claude 从 chatbot 变成 agent 的 15 行引擎——一旦你的团队能可靠地 ship 它，所有你脑中想得到的 agent 产品就都可行了。

---

## 心智模型：咖啡师和点单

想象一个咖啡师看着点单做饮料：

| 步骤 | 咖啡店 | Agentic Loop |
|------|--------|--------------|
| 读点单 | 用户问问题 | 用 messages 调用 Claude |
| 「还需要做什么吗？」 | 「Claude 要 tool 吗？」 | 检查 `stop_reason` |
| 要：磨豆、打奶泡…… | 要：执行 tool | 执行 tool-use block |
| 把每个步骤的结果交回咖啡师 | 把 tool result 加到历史 | Loop 回 Claude |
| 不要：完成饮料、结束 | 不要：返回最终文字 | Break loop |

咖啡师会一直问自己「还有下一步吗？」直到饮料完成。Loop 做的就是这件事——一直问 Claude「你还要做什么动作吗？」直到 Claude 说「不用了，我做完了」。

---

## 为什么这解锁了真正的产品价值

没有 loop，你只能 ship「Claude 回答问题」。有了 loop，你可以 ship：

| 产品 | 做什么 |
|------|--------|
| Coding assistant | 读文件、跑测试、写 patch、迭代 |
| 旅行规划 | 查机票、筛价格、订、确认 |
| 客服 agent | 读 ticket、查 CRM、查知识库、草拟回复 |
| 数据分析师 | 跑 SQL、解读结果、生成图、写摘要 |

Loop 是「agent」之所以是一个类别而不只是 buzzword 的原因。所有真实世界的 Claude agent——从 Claude Code 到 MCP client——都是这 15 行 pattern 加上生产加固的变体。

---

## 产品应用场景：何时该投资

### Loop 会回报成本的时候

| 信号 | 产品含义 |
|------|---------|
| 用户想要「fire and forget」的工作流 | Loop 让 Claude 自主完成多步骤任务 |
| 答案依赖外部数据 | Tool 调用抓数据，loop 迭代直到完成 |
| 用户愿意用延迟换质量 | Multi-turn loop 用速度换正确性 |
| 功能受益于迭代优化 | Loop 可以重试、筛选、比较、收敛 |

### Loop 是大材小用的时候

| 信号 | 更简单的做法 |
|------|--------------|
| 单次查询立即答案 | 一次 tool call，不用 loop |
| 纯静态知识 Q&A | 完全不用 tool |
| 实时对话 UI | 直接 streaming，不用 loop 那么复杂 |

---

## PM 决策框架

规划 agentic loop 功能前问：

| 问题 | 为什么重要 |
|------|-----------|
| 迭代上限是多少？ | 无限 loop 会卡好几分钟、烧 token |
| 迭代之间怎么显示进度？ | 用户要看得到每一步，不然会以为坏了 |
| 用户可以中途取消吗？ | 多步骤 agent 必须可以被打断 |
| Loop 撞到上限但没有最终答案怎么办？ | 「部分结果」UX 要设计 |
| 单一对话的 token 预算怎么算？ | 每次迭代都让历史变长，要规划最糟情况 |
| 如何审计跑过哪些 tool？ | Debug 和 compliance 都需要 |
| Tool 失败的重试策略是什么？ | 交给 Claude 处理、还是应用层硬重试？ |

---

## 常见 PM 错误

1. **把 loop 当成技术细节**——它是产品功能界面，每一回合都有 UX 决策（进度、取消、部分结果）
2. **没设可见的迭代上限**——失控 loop 浪费预算、把用户卡住；上限要调参数并写进文档
3. **把 tool 错误藏起来不给 Claude 看**——tool 失败的话 Claude 要用 `is_error=True` 知道，这样才能恢复；藏起来会 hallucinate
4. **没有观测性计划**——生产 debug agent loop 需要 log 每次迭代的 tool call 和结果
5. **没并行化就上线**——能并行跑的 tool 不要串行，否则延迟翻倍或翻三倍

---

## 成本与延迟规划

每多一次迭代就增加：

| 成本 | 典型量级 |
|------|---------|
| 一趟 API round trip | +300ms 到 +1s |
| 历史变长 | 每次迭代 +10% 到 +30% input token |
| Tool 执行时间 | 看 tool 而定（毫秒到秒） |
| Output token | 每回合 +几百 |

一个 5 次迭代的 loop 很容易就用掉单次调用 5 倍的 input token，wall time 要 3-10 秒。Prompt caching（课程后面会讲）是 token 成本的标准缓解方式，但延迟成本是这个 pattern 的本质。

---

> **Key Insight**
>
> Agentic loop 是分开「Claude 功能」和「Claude agent」的最小单位。15 行代码解锁一个新的产品类别。但那 loop 的每一行都对应一个产品决策：要迭代多久、进度怎么显示、失败怎么处理、成本上限在哪。把 loop 当「后端的事」的 PM 会 ship 坏掉的 agent；把它当「有五个旋钮的产品界面」的 PM 会 ship 好的 agent。

---

## CCA Exam Relevance

- **D1（Agentic Architecture）**：Agentic loop 是标准的 agent pattern。考题会问 `stop_reason` 处理和迭代控制。
- **D2（Tool Design & MCP Integration）**：理解错误如何用 `is_error=True` 传递，以及藏错误为什么会破坏 Claude 的恢复能力。
- 考题描述「Claude 连续做多个 tool 调用」——答案永远是一个有 stop_reason 检查的 loop。

---

## Flashcards

| 题目 | 答案 |
|------|------|
| 用什么比喻来理解 agentic loop？ | 咖啡师看点单——一直问「还有下一步吗？」直到饮料完成 |
| 哪一行代码是 loop 退出的信号？ | `if response.stop_reason != "tool_use": break` |
| 为什么 agentic loop 是产品界面而不只是工程？ | 每次迭代都有 PM 决策：进度 UX、取消、成本、重试、部分结果 |
| Agentic loop 功能最大的隐藏成本是什么？ | 历史变长——每次迭代都加 token 到后续调用 |
| 生产 agent loop 必须包含哪些安全机制？ | Max iteration 上限、每次迭代的观测性、用 `is_error=True` 传递错误 |
| 为什么藏错误不给 Claude 看会适得其反？ | Claude 以为 tool 成功就无法恢复，会 hallucinate 出结果 |
| 哪些产品是靠 agentic loop 才有可能？ | Coding assistant、旅行规划、客服 agent、数据分析师——任何需要多步推理的功能 |
| PM 应该为 5 次迭代的 agentic loop 算多少延迟预算？ | 3 到 10 秒 wall time，加上随迭代深度放大的 token 成本 |
