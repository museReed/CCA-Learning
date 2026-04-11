# Being Clear and Direct — PM 视角

| 项目 | 内容 |
|------|------|
| 考试领域 | D3 — Evaluation & Iteration (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 3.1（prompt 设计与迭代）、1.1（指令遵循） |
| 来源 | building-with-the-claude-api / 03-prompt-engineering / Lesson 26 |

---

## 一句话总结

写 prompt 就像写 design brief——用祈使动词开头、讲清楚要什么交付物，不要用客气的问句。

---

## PM 为什么该在乎

Prompt 的第一行就像 PRD 或 design brief 的第一句。如果工程师或设计师从第一句看不出要产什么，后面整份文件都在救火。Claude 也一样。这堂课显示：单一最高杠杆的 prompt 编辑——把第一行从问句改成祈使句——在 10 分制 eval 上带来可度量的分数跳升（2.32 → 3.92）。这个产品质量 delta 比大多数 A/B test 看得到的还大，而且只要改一句话。

---

## 心智模型：Design Brief

比较弱 vs 强 brief 对设计师的落地感：

| Brief 风格 | 设计师反应 | Claude 反应 |
|-----------|-----------|-------------|
| 「我们在想或许可以重做 onboarding flow，感觉怪怪的？」 | 「好……你到底想要什么？」 | 产出模糊回应，要求澄清或猜范围 |
| 「Redesign onboarding flow，目标降低 step 2 drop-off。交付物：3 个 Figma frame，周五前。」 | 「收到，开始了。」 | 产出对齐的结构化 artifact |

Prompt 就是 brief，Claude 是合作者。动词+交付物开头的 brief 永远赢过用 context 或问句开头的 brief。

---

## 两个原则翻成产品语言

| 原则 | 定义 | PM 翻译 |
|------|------|---------|
| **Clarity** | 简单语言、对要什么没有模糊 | User story：「As a X, I want Y so that Z」，没人要用猜的 |
| **Directness** | 指令而非问句、action verb 开头 | Acceptance criteria：「Given / When / Then」，祈使、可测 |

PM 如果已经会写好 Jira ticket，其实已经会写 clear and direct 的 prompt。能力可以 transfer。

---

## 产品应用场景

### 什么时候 clarity + directness 是第一个要改的

| 功能 | 症状 | 修法 |
|------|------|------|
| AI 摘要长度不一致 | Prompt 问「Can you summarize this?」 | 改：「Write a 3-sentence summary covering the main argument, supporting evidence, and conclusion.」 |
| AI 写手太话唠 | Prompt 用问句开头 | 改祈使：「Draft a professional email declining the meeting.」 |
| 内部文档抽取漏字段 | Prompt 说「Tell me about the contract」 | 改：「Extract the effective date, party names, and total value from the contract.」 |

### 什么时候这招不够

光靠 clarity and directness 有上限——课程只跑到 3.92/10。要再上去需要 specificity（Lesson 27）、examples、structure。把 clear+direct 当成**最小可用 prompt**，不是最终产品。

---

## PM 决策框架

在 PRD review 看团队的 AI prompt 时问：

| 问题 | 如果 No，就 flag |
|------|------------------|
| 第一行是动词开头吗？ | Flag——改祈使句 |
| 从第一句看得出 Claude 会产什么吗？ | Flag——brief 不清楚 |
| 有保留语吗（「maybe」「if possible」「could you」）？ | Flag——拿掉 |
| Prompt 有指定输出格式或长度吗？ | Flag——加 constraint |
| 新进同事看第一行不需 context 就懂吗？ | Flag——简化用字 |

本质上就是对 prompt 做一次 PRD lint。

---

## 隐藏的产品胜利

Clear + direct prompt 不只分数比较高——它**失败得更可预测**。模糊 prompt 可以用一百种方式失败（太长、太短、主题跑掉、格式错、太话唠、离品牌调性）。祈使 prompt 只用一种方式失败：要的 artifact 在某个具体、可 debug 的点错了。

可预测的失败是产品资产。QA 可以写针对性测试、on-call 看得出 bug 形状、eval rubric 也跟得上。

---

## 常见 PM 错误

1. **太客气的 prompt** — 「Could you please kindly...」PM 常把 AI prompt 当成写信给陌生人。Claude 不需要礼貌，它需要清楚。
2. **Context 前置** — 把指令埋在三句背景后面。指令先、context 后。
3. **用问不用命** — 把 Claude 当成可能拒绝你。它不会，直接下祈使句。
4. **觉得「太简单所以跳过」** — 课程测出一行改动 +1.6 分，不要跳过简单的胜利。
5. **以为 clear+direct 就结束了** — 这是地板不是天花板，上面还需要 specificity 和 examples。

> **Key Insight**
>
> AI 功能里最便宜的产品质量胜利，就是把每个 prompt 的第一行改写成动词开头的祈使句。零工程成本、可度量的分数提升、让功能失败模式变可预测。PM 在 review AI prompt 时第一个该 audit 的就是第一行。

---

## CCA 考试相关性

- **D3 (Evaluation & Iteration)**：「问句 → 祈使句」是 prompt 改进循环中最便宜的第一步。
- **D1 (Agentic Architecture)**：同一条规则套用到 agent system prompt——先祈使，再 preamble。
- 考题给弱 prompt 时，改写成祈使句的版本通常就是正解。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| PM 第一个该 audit 的是 prompt 哪部分？ | 第一行——它定调且影响回应质量比其他部分都大。 |
| 跟 clear-and-direct prompt 类比的 PM 产物是什么？ | 好的 design brief 或 Jira ticket——动词开头、有具体交付物、不保留。 |
| 光靠 clarity + directness 量到的分数进步？ | 2.32 → 3.92 的 +1.6 分，改一行来的。 |
| 为什么模糊 prompt 的产品风险不只是质量？ | 因为它失败模式不可预测，无法 debug、测试、预防。 |
| 「Design brief」类比？ | 模糊 brief 让设计师用猜的，动词+交付物 brief 可以立刻开工；Claude 一样。 |
| 列三个 PM 该从 prompt 移除的保留语？ | 「Maybe」「if possible」「could you」，任何让指令看起来选配的字。 |
| Clear and direct 够用吗？ | 不够，这是地板。还需要 specificity、examples、structure 才能拿高分。 |
