# Extended Thinking — PM Perspective

| 项目 | 内容 |
|------|------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) — 主要；D5 — Enterprise Deployment (20%) — 次要 |
| Task Statements | 1.1（推理深度）、1.2（agentic loop）、5.2（latency/cost 权衡） |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 52 |

---

## One-Liner

Extended thinking 是当 prompt engineering 在难推理任务上走到尽头时，产品经理可以拉的那根调节杆——多花钱、多等几秒，换一个更聪明的答案。

---

## Mental Model：国际象棋选手与时钟

想象一位国际象棋大师在两种不同赛制下下棋。

- **Bullet chess（超快棋）**：时钟只有三十秒。他靠直觉飞快落子，大多能赢，但有些该赢的会输。
- **Classical chess（慢棋）**：时钟有数小时。他靠在椅背上，在脑中推演各种变化、评估风险，下出明显更强的棋。

标准 Claude 就是 bullet chess——快、流畅、通常正确。Extended thinking 是 classical chess——你买的是模型在草稿纸上思考的时间。棋是同一盘棋，差别在选手有多少时间想。

没人会为了点一份咖啡用 classical chess。同样，也不该为了 prompt engineering 就能解决的问题付 extended thinking 的钱。

---

## PM 为什么该在意

Extended thinking 是少数能把**成本与延迟**直接换**准确度**的产品杠杆。这正是 PM 每天在处理的取舍：

- 用户抱怨 Claude 对某个难问题五次错一次。
- 工程团队已经调了两周 prompt，eval 分数停滞。
- CFO 在问为什么 AI 功能有延迟尖峰。
- 没人知道该拉哪根杆。

Extended thinking 给你一个有名字、可量测的选项带到那场对话里——测试成本很低（翻旗标重跑 eval），约束明确到可以写进 PRD。

---

## Product Use Cases

### Extended thinking 该打开的时机

| 用户需求 | 为什么 thinking 有帮助 |
|---------|---------------------|
| 难推理（数学、逻辑、多步规划） | 模型真的需要思考 token 来走完每一步 |
| 高代价的答案，准确度比延迟更重要 | 用户愿意多等几秒换一个正确答案 |
| 多约束的复杂文档分析 | 思考空间让模型能协调相互冲突的条件 |
| 需要"想清楚"而不是"查一下"的研究型问题 | 任务形状本身就是推导答案，不是检索 |

### 不该打开的时机

| 用户需求 | 更好的选择 |
|---------|-----------|
| 简单改写、摘要、翻译 | Base model；thinking 加成本但不加准确度 |
| 需要快速响应、延迟即 UX 的聊天 | Extended thinking 会明显拖慢 |
| 要抓实时数据 | 用 tools 而不是 thinking——再怎么深思熟虑也变不出训练数据里没有的事实 |
| 短结构化抽取 | 这是 prompt/格式问题，不是推理问题 |

---

## PM 决策框架

当团队有人说"我们来打开 extended thinking"时，要问：

| 问题 | 若答 Yes | 含义 |
|------|---------|------|
| 我们对着 eval set 优化过 prompt 了吗？ | No | 先做这件事。Thinking 修不了坏掉的 prompt。 |
| 准确度差距明显是推理深度问题吗？ | No | 问题可能在 tools、RAG 或结构——不是 thinking。 |
| 用户能容忍这个交互多等几秒吗？ | No | Thinking 会伤 UX。考虑异步或进度提示。 |
| 每次调用的成本增加在当前量级下可接受吗？ | No | Thinking tokens 规模化后是真金白银，先算清楚再决定。 |
| 这个 flow 依赖 assistant 预填或自定义 temperature 吗？ | Yes | 与 thinking 不兼容，必须重新设计 prompt 策略。 |

以上全绿就打开 thinking 跑 eval，看差距是否收敛。若收敛就发布，并在 PRD 里写下成本与延迟预算。

---

## Cost、Latency、UX 权衡

Extended thinking 不是无声升级。它改变三件用户会感觉到的事：

- **等待时间上升。** 模型真的会花更长的实际时间在思考。交互 UI 需要能容忍多几秒的 loading state。
- **每次调用成本上升。** Thinking tokens 要计费。每天 10 万次调用、budget 1024 token，月账单上看得到。
- **响应处理变复杂。** 工程端要迭代 content blocks，还要决定要不要把推理展示给用户看。这是设计决策，不只是代码决策。

PM 的卫生习惯：任何启用 thinking 的功能，PRD 里必含：

1. 以 eval 为基础的理由（开启前后的准确度）。
2. 每次调用成本估算与月度预测。
3. Loading state 与可选的"显示推理"toggle 的 UX 规格。
4. 当 thinking 与其他依赖功能不兼容时的 fallback 路径。

---

## Safety 故事：Signatures 与 Redacted Blocks

Extended thinking 带两个 safety 特性。PM 应该知道它们存在，因为它们同时影响信任消息和技术设计。

- **Signatures**——每个 thinking block 都有加密签名。如果开发者（或攻击者）试图在对话中段改写推理、把 Claude 引到不安全的地方，签名验证会失败、history 会被拒绝。这是你可以对客户说"我们怎么知道推理没被篡改"时指得出来的保证。
- **Redacted blocks**——有时 Claude 自家的 safety 系统会对推理亮红灯，并以加密形式回传。你的 app 读不出 redacted 内容，但必须原样传回去以保留上下文。产品含义：你的"显示推理"UI 偶尔会在某一轮没东西可显示，必须准备一个优雅的 fallback，而不是丢错误画面。

---

## Common PM Mistakes

1. **Prompt 还没优化就先开 thinking。** 结果就是把推理杠杆叠在一个坏掉的 prompt 上，准确度几乎不动。
2. **把 thinking 当成"Claude 免费变聪明"。** 它是成本与延迟的权衡。假装不是，就会在上线时吓到财务与 UX。
3. **把原始推理文字直接渲染给用户。** 推理轨迹又长又偏内部，用户默认不会想看一整面墙的思考过程。
4. **忽略功能不兼容性。** 若你现在的 prompt 策略用了 assistant 预填或自定义 temperature，打开 thinking 会整个坏掉。
5. **忘记 thinking budget 必须严格小于 max_tokens。** API 会强制这条约束。第一次在 production 出故障，就是一次本来可以在 review 时拦截的事故。
6. **没为 redacted 情境更新"显示推理"UI。** 用户会看到空白面板，以为功能坏了。

---

> **Key Insight**
>
> Extended thinking 是 Claude API 第一个干净、可被产品经理管理的权衡——一边是准确度，另一边是成本加延迟。PM 的工作是知道什么时候拉它：在 prompt 优化之后、有 eval 证据支持、并且只用在那些用户宁愿等久一点也要正确答案的难推理任务上。

---

## CCA Exam Relevance

- **D1 (Agentic Coding & Architecture)**：把 extended thinking 认成 agentic loop 内推理深度的标准杠杆，并分辨它 vs. prompt / tools 各自的适用场景。
- **D5 (Enterprise Deployment)**：成本与延迟的权衡、以 eval 驱动的采用决策、以及 `thinking_budget` / `max_tokens` 的约束都是 production 级的考点。
- 可能的情境题："Prompt engineering 在一个难推理任务上碰到天花板——下一步该怎么做？"预期答案是 extended thinking，且要 eval-driven。

---

## Flashcards

| Front | Back |
|-------|------|
| Extended thinking 的国际象棋类比是什么？ | 标准 Claude 是 bullet chess——快、通常正确。Extended thinking 是 classical chess——买模型在草稿纸上思考的时间，在难题上给更强的答案。 |
| 什么时候 extended thinking 是错的工具？ | 快速简单任务（改写、翻译、闲聊）或真正问题是缺数据（该用 tools/RAG）而不是推理深度时。 |
| PM 在一个功能上打开 thinking 前必须先完成什么？ | 针对 eval set 的 prompt 优化，且证据显示剩下的差距是 prompt 单独解不掉的推理深度问题。 |
| Extended thinking 对用户体验改变哪三件事？ | 等待时间、每次调用成本、以及响应复杂度（推理轨迹出现在 content blocks）。 |
| 启用 thinking 的功能 PRD 该包含什么？ | 以 eval 为基础的准确度理由、成本预测、UX loading states、以及兼容性 fallback。 |
| Thinking signature 保证什么？ | 推理轨迹在对话 turn 之间没被篡改，防止开发者伪造 chain-of-thought 把模型引到不安全的地方。 |
| 什么是 redacted thinking block？app 该怎么处理？ | 因为内部 safety 系统标记而被加密的 thinking block。App 读不到内容但必须原样传回以保留上下文。 |
| 为什么 extended thinking 与某些功能不兼容？ | 出于模型设计原因——特别是 pre-filled assistant 消息与自定义 temperature 会和 thinking 机制冲突，启用 thinking 时那部分 prompt 策略必须重做。 |
