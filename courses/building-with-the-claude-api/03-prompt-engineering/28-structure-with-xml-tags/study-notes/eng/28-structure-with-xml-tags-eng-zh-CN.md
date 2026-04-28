# 使用 XML 标签构建结构 — Engineering Deep Dive

| 项目 | 内容 |
|------|------|
| 考试领域 | D3 — Evaluation & Iteration（20%）主；D2 — Tool Design（18%）次 |
| 任务陈述 | 3.1（提升可靠性的 prompt 设计）、2.2（结构化内容块） |
| 来源 | building-with-the-claude-api / 03-prompt-engineering / Lesson 28 |

---

## 一句话总结

XML 标签是 prompt 字符串里的显式分隔符，让 Claude 能清楚区分哪些 token 是指令、哪些是数据、哪些是示例——是 prompt engineering 里最简单也最可靠的结构化技巧。

---

## 问题：一锅 Token 粥

当你把指令、20 页销售记录、以及用户问题全部拼接成一个 prompt 字符串时，Claude 看到的是一长串没有区分的 token 序列。没有边界，它只能从文字本身推断结构，而这种推断非常脆弱：

- 指令会渗进数据
- 数据会渗进示例
- Claude 可能会「执行」原本只是要分析的内容

课程原文的描述是：Claude「有时会难以判断哪些文字属于同一组、各段落又分别代表什么」。

XML 标签通过在 token 流里插入明确的标记解决这个问题。`<sales_records>...</sales_records>` 告诉 Claude：这里面的东西是同一个逻辑单位，而且是某种特定类型。

---

## 经典示例

课程中的运动员饮食计划 prompt：

```
<athlete_information>
- Height: 6'2"
- Weight: 180 lbs
- Goal: Build muscle
- Dietary restrictions: Vegetarian
</athlete_information>

Generate a meal plan based on the athlete information above.
```

这里有三件事同时发生：

1. **语义分组**——身高、体重、目标、饮食限制被绑在同一个容器内。
2. **角色分离**——指令（"Generate a meal plan..."）放在标签外，完全不会有「这是数据还是指令」的模糊地带。
3. **可指代性**——指令可以直接说「the athlete information above」，正好对应标签名称。

---

## 代码 vs 文档：最戏剧化的例子

课程里第二个例子：请 Claude 用提供的文档 debug 代码。如果把两者混成一坨（"Not Great" 版本），几乎无法让 Claude 分辨哪些是代码、哪些是散文。"Better" 版本用标签把两段内容包起来：

```
<my_code>
def calculate_total(items):
    return sum(item.price for item in items)
</my_code>

<docs>
Item class 有三个字段：name (str)、price (float)、quantity (int)。
价格以整数分（cents）存储。
</docs>

请使用上述文档，找出 my_code 中的 bug。
```

现在 Claude 知道：把 `my_code` 当 Python 解析，把 `docs` 当作 ground truth，找出不一致的地方（文档说 price 是整数分，但代码直接把总和当成最终价格）。

---

## 标签名称很重要

课程明确表示你不需要用「官方」XML。标签名称是语义提示，所以越具体越好：

| 弱 | 强 | 理由 |
|----|----|------|
| `<data>` | `<sales_records>` | 告诉 Claude 是什么类型的数据 |
| `<info>` | `<athlete_information>` | 避免与其他 info 混淆 |
| `<text>` | `<customer_review>` | 隐含领域（情感、语气） |
| `<input>` | `<my_code>` / `<docs>` | 区分并列的内容 |

原则：如果你能在代码里给这个变量起名，就用同一个名字当标签。

---

## 何时 XML 标签最有价值

直接引用课程内容，XML 最有用的场景是：

- 包含大量 context 或数据
- 混合不同类型的内容（代码、文档、数据）
- 你想特别清楚地标示内容边界
- 复杂 prompt 中插入多个变量

对于单行 prompt（「翻译成法文：hello」），加标签是杀鸡用牛刀。收益会随 prompt 复杂度放大。

---

## Python 模式：安全的字符串插入

```python
from anthropic import Anthropic

client = Anthropic()

athlete_info = """- Height: 6'2"
- Weight: 180 lbs
- Goal: Build muscle
- Dietary restrictions: Vegetarian"""

prompt = f"""<athlete_information>
{athlete_info}
</athlete_information>

Generate a meal plan based on the athlete information above."""

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}],
)
```

注意插入点完全在标签内。用户提供的数据没办法渗到指令区——这也能降低 prompt injection 的攻击面：攻击者塞进来的文字最多污染 `athlete_information`，标签外的指令仍然固定。

---

## 常见错误

1. **模糊的标签名称**——用 `<data>` 或 `<text>` 而不是 `<sales_records>`。Claude 无法利用没被给出的提示。
2. **忘记关闭标签**——没有关闭的 `<my_code>` 可能让 Claude 把后面全部都当成代码。
3. **多段内容不加标签**——把代码和文档并排放但没有分隔符，正是课程警告的失败场景。
4. **对简单 prompt 过度加标签**——为一句话的请求加 XML 只会增加噪声。
5. **以为 XML 会改变输出格式**——标签只管输入结构；要 Claude 回 XML 还需要另外的指令。

> **Key Insight**
>
> XML 标签是 prompt engineering 里最便宜的可靠性升级。它不会改变 Claude 能做什么，但会改变它「多有把握地」区分你的指令和你的数据。在 CCA 考试中，任何涉及「大量 context」「多种数据类型」或「Claude 把指令和内容搞混」的情境，都指向 XML 结构化这个答案。

---

## CCA 考试相关性

- **D3（Evaluation & Iteration）**：当 eval 显示 Claude 误判输入时，XML 加标签是第一道改进手段。预期会有情境题描述某个 prompt 失败，原因是边界模糊。
- **D2（Tool Design）**：同样的分隔原则也适用于 `tool_use` / `tool_result` 的 content blocks——结构化通道优于自由字符串。
- 注意题目中出现「interpolating」或「mixing」——标准答案是「用 XML 标签分隔每一段」。

---

## Flashcards

| 正面 | 反面 |
|------|------|
| XML 标签在 prompt 里解决什么问题？ | 用明确边界让 Claude 能区分指令、数据、示例。 |
| XML 标签名称必须符合某个标准吗？ | 不需要——偏好用 `<sales_records>`、`<athlete_information>` 这类描述性自定义名称。 |
| XML 标签何时最有价值？ | 大量 context、多种内容类型、插入多个变量的复杂 prompt。 |
| 举一组弱/强标签名称对比 | 弱：`<data>`；强：`<sales_records>`。 |
| 代码 vs 文档的经典示例长什么样？ | 用 `<my_code>` 包代码、`<docs>` 包文档，再请 Claude 依文档找 bug。 |
| XML 标签会改变响应的输出格式吗？ | 不会——它只管输入结构；输出格式需要另外指令。 |
| XML 标签对 prompt injection 有什么好处？ | 用户数据被关在标签内，标签外的指令较难被覆盖。 |
| 简单 prompt 也要用 XML 吗？ | 不一定——收益随复杂度放大；一行 prompt 加标签反而是噪声。 |
