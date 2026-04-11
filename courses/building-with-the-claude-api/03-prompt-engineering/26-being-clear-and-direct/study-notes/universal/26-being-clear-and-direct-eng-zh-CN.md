# Being Clear and Direct — 工程深度解析

| 项目 | 内容 |
|------|------|
| 考试领域 | D3 — Evaluation & Iteration (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 3.1（prompt 设计与迭代）、1.1（指令遵循） |
| 来源 | building-with-the-claude-api / 03-prompt-engineering / Lesson 26 |

---

## 一句话总结

Prompt 的第一行是 heavy lifting 的关键——用祈使动词开头、直接描述任务，让 Claude 对你要什么完全没有模糊空间。

---

## 第一行原则

课程直接断言：prompt 的第一行是整个 request 最重要的部分。后面所有的东西——context、constraints、examples——都是环绕这个开头指令的脚手架。第一行写对，Claude 立刻对齐意图；第一行写错，后面再多 context 也救不完全。

管住第一行的两个原则：**clarity（清楚）** 和 **directness（直接）**。

---

## Clarity：prompt 怎么用字

「清楚」关于选字与明确性：

- 用任何人都看得懂的简单语言。
- 直接说你要什么，不要绕路、不要清嗓子。
- 开头就用一句直白描述 Claude 的任务。

像「我需要知道那种人家放在屋顶上、用太阳的东西——我想叫太阳能板的那种」这种模糊开头，逼 Claude 猜主题、格式、深度都要猜。清楚改写——「Write three paragraphs about how solar panels work.」——一句话锁定全部三项。

---

## Directness：prompt 怎么结构化

「直接」关于语法形式：

- **用指令，不要用问句**。
- 用 action verb 开头：Write、Create、Generate、Identify、Summarize、Extract、List。

像「我在看可再生能源，地热听起来很酷。有哪些国家在用？」这种问句会让 Claude 用对话语气回答、没有结构。直接改写——「Identify three countries that use geothermal energy. Include generation stats for each.」——指定了数量（3）、限制（用地热）、必要输出（每国附统计）。

语法从问句变命令是有实际作用的。问句引出回答，祈使句引出产出。

---

## 贯穿示例

套用到 Lesson 25 的餐单 prompt：

**弱 baseline：**

```
What should this person eat?
```

**Clear and direct 改写：**

```
Generate a one-day meal plan for an athlete that meets their dietary restrictions.
```

改写版一句话告诉 Claude 三件事：

| 元素 | 值 |
|------|-----|
| 动作 | Generate |
| 对象 | 一份餐单 |
| 限制 | 一日份、给运动员、符合饮食限制 |

问句版本这三个元素全都缺。

---

## 度量结果

课程给了跑 evaluator 的具体数字：

| 版本 | 分数 (/10) |
|------|-----------|
| "What should this person eat?" | 2.32 |
| "Generate a one-day meal plan for an athlete that meets their dietary restrictions." | 3.92 |

单单改一行就 **+1.60 的绝对进步**。这不是终点——后面的技巧（specificity、examples、structure）还会继续往上推——但证明了光第一行就值好几分。

---

## 为什么这在机制上有效

Claude 被训练成遵循指令。看到祈使句开头时，模型的 next-token 概率分布会往「服从、产出要求的 artifact」这类 response pattern 靠拢。看到模糊问句时，分布会散到多种可能的 response style：对话、澄清、推测、保留。祈使句把分布 collapse 到你要的模式。

所以课程提的「把 Claude 当成需要明确指引的能干助理」比「正在聊天的朋友」好用。前者把互动 framing 成任务执行，后者邀请闲聊。

---

## 常见错误

1. **开头先给 context** — 「我在看 X……」把指令延后又稀释。指令先、context 后。
2. **把任务写成问句** — 问句看起来礼貌但结构模糊。
3. **用模糊名词** — 「那些东西」「一些」「合理就好」都把诠释 push 给 Claude。
4. **以为后面指令会修好烂第一行** — 后文能 refine 但不能 retro-frame 一个糊的开头。
5. **叠加保留语** — 「如果可以的话，可不可以也许……」把祈使句弱化成选配。

> **Key Insight**
>
> 祈使句开头是 prompt engineering 里最便宜、最快的胜利。在加 examples、加结构、加 XML tag 之前，先把第一行重写成 action verb 开头的命令句。课程示例中这个改动在 10 分制上贡献 +1.6 分——每个字符的投报率比其他任何技巧都高。

---

## CCA 考试相关性

- **D3 (Evaluation & Iteration)**：「问句 → 祈使句」是 prompt 改进 playbook 的第一招，也是最便宜的一招。
- **D1 (Agentic Architecture)**：agent 的 system prompt 同一个原则——先写 agent 的核心祈使，不要先写前言。
- 题目可能给一个弱 prompt，要你选改进版——祈使句改写几乎永远是答案。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Prompt 哪一行最重要？ | 第一行。它为后续一切定调，决定 Claude 怎么 framing 回应。 |
| 写好第一行的两个原则？ | Clarity（简单无歧义）和 Directness（用指令不用问句、action verb 开头）。 |
| 太阳能板弱 vs 清楚开头各一例？ | 弱：「屋顶上那个用太阳的东西」；清楚：「Write three paragraphs about how solar panels work.」 |
| Prompt 该用什么语法形式？ | 祈使句（命令）用 Write、Create、Generate、Identify 这类 action verb 开头，不用问句。 |
| 课程量到光靠 clarity + directness 的分数进步？ | 2.32 → 3.92，改一行的 +1.6 分进步。 |
| 为什么祈使句比问句对 Claude 更有效？ | 它把 response 分布 collapse 到任务执行，而不是对话或澄清模式。 |
| 改写后餐单开头告诉 Claude 哪三件事？ | 动作（generate）、对象（meal plan）、限制（一日、运动员、符合饮食限制）。 |
