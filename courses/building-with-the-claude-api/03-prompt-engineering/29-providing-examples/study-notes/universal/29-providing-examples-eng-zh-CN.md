# 提供示例 — Engineering Deep Dive

| 项目 | 内容 |
|------|------|
| 考试领域 | D3 — Evaluation & Iteration（20%）主；D2 — Tool Design（18%）次 |
| 任务陈述 | 3.1（提升可靠性的 prompt 设计）、2.2（结构化内容块） |
| 来源 | building-with-the-claude-api / 03-prompt-engineering / Lesson 29 |

---

## 一句话总结

Few-shot prompting（one-shot / multi-shot）是把「输入/输出」示例丢给 Claude，而不是用文字描述想要的行为——这是处理 corner case、格式和语气最有效的 prompt engineering 技巧。

---

## 为什么「示范」比「描述」更有效

指令是「告诉」，示例是「展示」。当任务的细微之处很难用文字精确表达——讽刺、特定 JSON 结构、公司风格——示范预期行为比描述它更可靠。课程原文称 few-shot 是「你最常用的 prompt engineering 技巧之一」。

课程里的经典失败案例是带有讽刺意味的情感分析。这则推文：

> "Yeah, sure, that was the best movie I've seen since 'Plan 9 from Outer Space'"

表面看起来像正面（best、since、sure），但实际上是讽刺、是负面。不管你写多短的「请检测讽刺」指令都难以稳定修好，但加一个讽刺示例就可以。

---

## 结构化的讽刺示例

课程中改进后的 prompt 包含：

- 一个明确的正面示例：`"Great game tonight!"` → `"Positive"`
- 一个讽刺示例：`"Oh yeah, I really needed a flight delay tonight! Excellent!"` → `"Negative"`
- 解释为什么讽刺要被小心处理的 context

关键是，这些示例都包在 XML 标签里：`<sample_input>` 和 `<ideal_output>`。这直接扣回 Lesson 28——XML 标签分隔示例输入、示例输出和真正的任务。没有结构的 few-shot 会让 Claude 猜哪段文字才是「答案」。

```
<example>
  <sample_input>Great game tonight!</sample_input>
  <ideal_output>Positive</ideal_output>
</example>

<example>
  <sample_input>Oh yeah, I really needed a flight delay tonight! Excellent!</sample_input>
  <ideal_output>Negative</ideal_output>
</example>

Classify the following tweet. Sarcasm should be treated as negative.

<tweet>
{user_tweet}
</tweet>
```

---

## One-Shot vs Multi-Shot

直接引用课程：

- **One-shot**——单一示例，足以建立模式
- **Multi-shot**——多个示例，涵盖不同情境和 edge case

当你需要处理多种 corner case、或示范多种有效的响应类型时用 multi-shot。原则：每多加一个示例，都应该「付清自己的成本」——也就是能覆盖前面示例没覆盖到的失败模式。

---

## 什么时候示例是对的工具

根据课程，示例对以下情况特别有用：

- 处理 corner case 或边缘情境（讽刺、模糊输入）
- 定义复杂的输出格式（如特定 JSON 结构）
- 展示精确的风格或语气
- 示范如何处理模糊输入

注意共通点：任何「给我看」比「精确描述我要什么」更快的场景。

---

## 从 Evaluations 收割示例

实务上最重要的一点：当你跑 prompt eval 时，看**得分最高的输出**，然后把它们升级成 prompt 里的示例。课程原文明确写：「找出得 10 分（或你最高分）的响应，把这些输入/输出对当作 prompt 的示例」。

这形成一个良性循环：

1. 用现有 prompt 跑 eval
2. 找出 Claude 已经产出理想输出的 case
3. 把那些（input, output）对复制到 prompt 里当 few-shot 示例
4. 重跑 eval——难 case 的分数应该会上升

这就是 Lesson 29 被放在本章「prompt engineering → evaluation」流程里的原因：示例和 eval 是同一个迭代循环。

---

## 不只是展示，还要解释

课程强调一个理想示例应该附上「为什么这是好的」的说明。原文：

```
<ideal_output>
[Your example output here]
</ideal_output>

This example is well-structured, provides detailed information
on food choices and quantities, and aligns with the athlete's
goals and restrictions.
```

示例后面的短注解告诉 Claude 这个输出「好在哪里」，而不只是「长什么样子」。这有助于 generalization——Claude 学到的是判断标准，不只是表面形式。

---

## Python 模式

```python
from anthropic import Anthropic

client = Anthropic()

few_shot = """<example>
  <sample_input>Great game tonight!</sample_input>
  <ideal_output>Positive</ideal_output>
</example>

<example>
  <sample_input>Oh yeah, I really needed a flight delay tonight! Excellent!</sample_input>
  <ideal_output>Negative</ideal_output>
</example>

Sarcasm should be treated as negative."""

tweet = "Yeah, sure, that was the best movie I've seen since 'Plan 9 from Outer Space'"

prompt = f"""{few_shot}

Classify the following tweet as Positive or Negative.

<tweet>
{tweet}
</tweet>"""

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=64,
    messages=[{"role": "user", "content": prompt}],
)
```

两个重点：示例放在真实任务上方，而且示例和真实输入都用 XML 标签包起来。

---

## 课程的最佳实践

- 永远用 XML 标签结构化示例
- 明确说明你在展示什么（「Here is an example input with an ideal response」）
- 示例要针对最常见的失败 case
- 解释为什么示例输出是理想的
- 示例要跟你的实际任务相关

---

## 常见错误

1. **示例没用 XML 结构**——Claude 得猜哪段是输入、哪段是输出、哪段是真正的问题。
2. **挑选太容易的示例**——示范的全是 Claude 已经做得很好的 case，却忽略真正的失败模式。
3. **示例和任务漂移**——用的示例接近但不完全等同真实输入的形状。
4. **只展示不解释**——理想输出没有注解会让 Claude 只会「复制」而不是「推理」。
5. **Eval 后没重新收割示例**——eval set 变了但示例没更新，prompt 就不再对准难 case。

> **Key Insight**
>
> Few-shot prompting 是 Lesson 28（XML 结构）和 Chapter 04（tool use）之间的桥梁。CCA 考试预期会出现这类情境题：「prompt 能处理正常 case 但在讽刺／JSON 格式／特定语气上失败」。答案几乎都是：加 XML 标签的示例来覆盖那些失败模式，最好来自 eval 分数最高的输出。

---

## CCA 考试相关性

- **D3（Evaluation & Iteration）**：当 eval 暴露出系统性失败模式时，few-shot 是主要的迭代手段。「把高分 eval 输出升级成示例」的循环是考点。
- **D2（Tool Design）**：设计严格输出格式（包含 tool-like 行为的 JSON）时，示例比文字描述 schema 更可靠。
- 题目关键字：「sarcasm」「specific format」「corner case」「style or tone」——都指向 few-shot 示例。

---

## Flashcards

| 正面 | 反面 |
|------|------|
| 什么是 few-shot prompting？ | 在 prompt 里提供输入/输出示例对来引导 Claude 响应（one-shot = 1 个示例，multi-shot = 多个）。 |
| 为什么示例比指令更适合处理讽刺检测？ | 讽刺很难用文字描述；示范一个讽刺示例比叫 Claude「注意讽刺」更可靠。 |
| 课程为示例使用哪些 XML 标签？ | `<sample_input>` 和 `<ideal_output>`（实务上外层再包一个 `<example>`）。 |
| 什么时候该用 multi-shot 而非 one-shot？ | 需要覆盖多个 edge case 或示范不同有效响应类型时。 |
| 怎么从 eval 取得好示例？ | 找出得分最高（例如 10/10）的响应，把那些输入/输出对升级成 prompt 示例。 |
| 为什么要解释示例为什么是理想的？ | 帮助 Claude 学到背后的判断标准，而不只是复制表面形式。 |
| 列出四个示例特别有用的情境 | Corner case、复杂输出格式、特定风格/语气、模糊输入。 |
| Lesson 28 和 Lesson 29 的关系是什么？ | XML 标签（28）提供结构；示例（29）在结构里填入示范——设计上就是配套使用。 |
