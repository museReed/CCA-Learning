# Response Streaming — PM 视角

| 项目 | 细节 |
|------|------|
| 考试领域 | D5 — Enterprise Deployment (20%) |
| Task Statements | 5.2（streaming 与响应速度）、5.3（production 模式） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 13 |

---

## 一句话总结

Streaming 是把 20 秒等待变成 200 毫秒「Claude is writing…」体验的产品 feature——它是所有面向用户的 AI chat 产品最重要的单一延迟优化，也是 demo 和真正产品的定义性差别。

---

## 心智模型：餐厅厨房

想象两家餐厅供应同一道菜：

| 餐厅 | 体验 | 食客反应 |
|------|------|---------|
| **Blocking** | 你点餐，主厨沉默地煮 20 分钟，侍者把完成的盘子放到你面前 | 「他们忘了我的餐点吗？」→ 焦虑、差评 |
| **Streaming** | 你点餐，跑堂立刻送面包，接着前菜，然后主菜一盘一盘上 | 「一切都在流动」→ 平静、好评 |

总烹饪时间一样。体验完全不同。Streaming 就是 LLM UX 的跑堂侍者。

---

## 为什么 PM 要在乎

AI chat app 的用户研究一致显示**感受延迟主导满意度**。用户愿意原谅慢响应，只要能看到进度。他们会放弃快响应，只要看到转圈超过 2-3 秒没有反馈。

Streaming 直接解决：

- **放弃率**——在响应到之前关掉标签页的用户
- **感受质量**——「这 app 很顺」vs「这 app 坏了」
- **信任**——可见的进度信号传达「系统活着」
- **与期望的比较**——用户已经被 ChatGPT / Claude.ai 训练成预期 streaming。Blocking 响应感觉过时

如果你的产品有 chat 界面而且不 streaming，不管底层 model 多好，都会感觉比每个竞争对手都差。

---

## 产品使用场景

### 永远要 Stream

| 产品 | 原因 |
|------|------|
| 对话式 chat UI | 用户预期实时生成——ChatGPT 基准线 |
| 长文内容生成器（博客、文章） | 几秒等待扼杀 engagement |
| Code 助手 | 用户想立刻开始读 fix |
| 家教 / 解说工具 | 渐进式解说教学更好 |
| 任何「Claude 在思考…」UX | Streaming 就是思考指示 |

### Streaming 较不关键

| 产品 | 原因 |
|------|------|
| 异步后台作业（晚点寄出的 email summary） | 没有用户在等 |
| 短分类输出（1-token label） | 生成已经够快 |
| Webhook 驱动的集成 | 接收端没有人 |
| Analytics pipelines | 批处理，延迟无关 |

---

## 用户感受延迟公式

每个 chat feature 的 PM 都该追踪三个数字：

1. **Time to first token (TTFT)**——用户看到任何东西前的时间。这是用户感受的数字。目标：< 1 秒
2. **Tokens per second (TPS)**——streaming 开始后文字出现的速度。目标：匹配阅读速度（~15 tokens/sec 就行）
3. **Total time to completion**——完整响应时间。如果 TTFT 低，用户对这个不敏感

Streaming 把用户注意力从第三个数字（Claude 控制有限）挪到第一个（streaming 几乎给你即时 TTFT）。这是 streaming 胜出的数学原因。

---

## PM 决策框架

规划 chat feature 时问这些问题：

| 问题 | 如果 Yes | 含义 |
|------|---------|------|
| 有人类在等响应吗？ | Yes | Stream |
| 响应可能超过 2 秒吗？ | Yes | Stream |
| 产品跟 ChatGPT 式 UI 竞争吗？ | Yes | Stream——不 stream 感觉过时 |
| 用户会边看边读输出吗？ | Yes | Stream |
| 输出很短（单次分类、yes/no）吗？ | No | Streaming 增加复杂度但 UX 收益很少 |

默认应该是「有人在等的都 stream」。不 streaming 是例外。

---

## UX 考量

Streaming 引入 blocking 没有的新 UX 问题：

- **光标 / 箭头指示**——streaming 时显示闪烁光标让用户知道生成中
- **停止按钮**——streaming 让用户能取消长响应；这是预期的 affordance
- **Stream 中途错误**——连接半途断掉怎么显示？设计「从这里重试」模式
- **Code block 渲染**——逐 token stream 的 markdown code block 需要小心渲染，避免中途看起来坏掉
- **Scroll 行为**——UI 要自动跟着 streamed 文字 scroll 吗？通常要，但要允许用户跳出

这些在 blocking 响应都不存在。加进验收标准。

---

## 常见 PM 错误

1. **没在 PRD 指定 streaming**——工程师默认选最容易的，你继承糟糕 UX
2. **测总延迟而不是 TTFT**——对 streaming UX 总时间是错的 metric
3. **没设计停止 / 取消按钮**——用户预期有；没有的话他们会关标签页
4. **只测短响应**——streaming 对长输出最重要。测 1000-token 响应
5. **假设 streaming 纯粹是工程工作**——streaming 是有 UX、错误处理、取消语义的面向用户 feature。需要 PM 设计

> **Key Insight**
>
> Streaming 不是性能优化——它是现代 AI chat 产品的核心 UX 模式。用户已经被 ChatGPT 训练成预期渐进渲染，blocking 响应立刻读成「旧的」或「坏的」。对任何做 AI feature 的 PM，指定 streaming（加上相关 UX——光标、停止按钮、stream 中错误优雅处理）是入场门槛。

---

## CCA 考试重点

- **D5.2（streaming 与响应速度）**：预期考 streaming 何时适当、它解决什么问题（感受延迟，不是总延迟）、以及它在 production chat 系统的角色
- **D5.3（production 模式）**：streaming 是面向用户 chat 的标准 production 模式——注意场景题
- 记住：streaming 不降低总生成时间；它降低 time-to-first-token

---

## Flashcards

| 题目 | 答案 |
|------|------|
| Streaming 解决什么产品问题？ | Chat UI 的高用户感受延迟——「我在盯着坏掉的转圈吗？」问题 |
| Streaming 会让 Claude 更快吗？ | 不会——它让 Claude 感觉更快，边生成边显示。总时间不变 |
| 「time to first token」是什么，为什么重要？ | 用户看到第一块文字前的延迟。它主导用户满意度，胜过总延迟 |
| Streaming 的餐厅类比是什么？ | 跑堂侍者——面包、前菜、主菜渐进出现，而不是等 20 分钟一个放下的盘子 |
| Streaming 需要哪些 UX affordance？ | 闪烁光标、停止 / 取消按钮、stream 中错误处理、auto-scroll 行为 |
| 什么时候 streaming 不重要？ | 异步后台作业、很短的分类输出、webhook 驱动集成——任何没有人实时在等的 |
| PM 该为 streaming feature 追踪哪些 metric？ | Time to first token (TTFT)、tokens per second (TPS)、total time——按 UX 重要性依序 |
| 为什么 blocking UX 现在对用户感觉「过时」？ | ChatGPT 和 Claude.ai 已把用户训练成预期渐进渲染；blocking 响应读起来像坏掉或慢 |
