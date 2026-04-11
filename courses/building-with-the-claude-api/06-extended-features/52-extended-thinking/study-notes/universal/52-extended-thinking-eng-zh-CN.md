# Extended Thinking — Engineering Deep Dive

| 项目 | 内容 |
|------|------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) — 主要；D5 — Enterprise Deployment (20%) — 次要 |
| Task Statements | 1.1（推理深度与 agent 决策质量）、1.2（agentic loop）、5.2（latency/cost 权衡） |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 52 |

---

## One-Liner

Extended thinking 给 Claude 专属的"草稿纸"token，让模型在产出最终答案前先推理一遍；用更高的成本和延迟，换取单靠 prompt 无法稳定达成的准确度。

---

## 问题情境：prompt engineering 到达瓶颈时

每个严肃的 Claude 部署最终都会遇到一类 prompt——不论你怎么调整指令、example、guardrail，准确率就是上不去。模型给出的答案看起来合理，但对于较难的推理题，答案并不稳定正确。Extended thinking 就是为这个时刻设计的，它是你在**已经**优化过 prompt 和 eval 套件后，仍然需要更多余量时才打开的功能。

把它想成 Claude 的草稿纸：模型会把推理过程写在一块内部工作区，做完草稿才产出最终回应。你用 token 付草稿纸的钱，等更长时间，但最终答案基于更长的内部思考而来。

---

## 响应结构：从一块变两块

Extended thinking 关闭时，Claude 的响应就是一个简单的 text block。打开之后，响应结构化为两部分——一个 **thinking block**（推理轨迹）加一个 **text block**（最终答案）。

这会改变应用处理响应的方式。原本假设 `response.content[0].text` 的代码，现在必须迭代 content blocks 并区分 thinking 与用户可见的 text。如果你把 Claude 的输出直接渲染给用户，必须决定要显示推理过程、隐藏它、或收在"显示推理"按钮后面。

---

## 在代码里启用 thinking

课程教一个最小封装，在 chat 函数上多开两个参数：`thinking`（布尔开关）与 `thinking_budget`（Claude 可花在推理的最大 token 数）。

```python
def chat(
    messages,
    system=None,
    temperature=1.0,
    stop_sequences=[],
    tools=None,
    thinking=False,
    thinking_budget=1024,
):
    ...
```

函数内部，当 `thinking` 打开时把 thinking 配置注入 API 参数：

```python
if thinking:
    params["thinking"] = {
        "type": "enabled",
        "budget": thinking_budget,
    }
```

调用方式：

```python
chat(messages, thinking=True)
```

两条硬约束：

- **最小 budget 是 1024 tokens。** 不能再小。
- **`max_tokens` 必须大于 `thinking_budget`。** 因为 thinking 的预算是从 `max_tokens` 里面扣的，`max_tokens` 必须容纳推理轨迹和最终答案。

---

## 签名系统

Extended thinking 的响应会带上 thinking 内容的**加密签名**。签名是 Anthropic 检测篡改的机制：如果开发者改动了 thinking 文字再把它送回下一轮，签名就会验证失败，模型会拒绝这批 history。

这是一个 safety 保证。Claude 的推理是 alignment training 的一部分——如果开发者能在 turn 之间改动推理文字，就能伪造一串合理化危险输出的"chain of thought"，把模型引导到不安全的区域。签名就是为了堵上这个攻击面。

实务含义：**永远不要修改 thinking blocks**。把对话历史送到下一轮时，连同签名逐 byte 原样送回。

---

## Redacted thinking blocks

有时 Claude 的内部 safety 系统会对推理轨迹本身亮红灯。此时你拿到的不是可读的推理文字，而是一个 **redacted thinking block**，里面装的是加密的 payload。

两件事很重要：

1. **遇到 redacted block 不能崩溃。** 你的 content-block handler 必须把 redacted 当成一种合法变体，和普通 thinking block、text block 一样处理。
2. **原样送回。** 虽然你的代码读不出 redacted 的内容，Claude 在下一轮可以解密，所以把加密 payload 传回去就能保留上下文。若悄悄丢掉，等于截断了 Claude 的记忆。

课程提到测试时可以发一个特殊的 trigger 字符串强制 Claude 回传 redacted 响应，用来验证 handler 不会因为某些下游代码假设 thinking block 一定可读而掉链子。

---

## 成本与延迟的权衡

Extended thinking 不是免费的：

- **成本更高。** Thinking tokens 要计费，每次调用都吃 1024-token 的 thinking budget，规模化后就是真金白银。
- **延迟更高。** 模型在吐出第一个 text token 之前要花更多实际时间。
- **客户端代码更复杂。** Content-block 迭代、签名处理、redacted 的 fallback。

指导原则：把 thinking 当成**准确度的调节杆**，在标准 prompt engineering 之后才拉。决策流程：

1. 写好 prompt。
2. 建立 eval set。
3. 反复优化 prompt 直到准确率停滞。
4. 如果仍低于门槛，开 thinking 再跑一次 eval。

Thinking 解决了就发布。若没解决，代表问题不是推理深度的问题，需要换别的方案（tools、RAG、更好的 prompt 结构）。

---

## 功能兼容性注意事项

课程明确点名 extended thinking 与某些其他功能**不兼容**，特别是 **assistant message pre-filling** 与自定义 **temperature**。这在 production 里很重要：如果你现有的 prompt 策略靠 pre-fill 的 assistant 消息来引导输出格式，就不能直接把 thinking 叠上去，必须重新设计那部分的 prompt。

完整的不兼容清单放在 Anthropic docs，课程指向那份文档而不在此列出，因为清单会随新模型演进。

---

## Common Mistakes

1. **在优化 prompt 之前就开 thinking。** Thinking 花钱又花时间。如果你的 prompt 根本写错，thinking 不会把它变对，你只是花更多钱得到同样错的答案。
2. **`max_tokens` ≤ `thinking_budget`。** API 会拒绝调用。`max_tokens` 必须能同时容纳推理轨迹和最终答案。
3. **在 turn 之间修改 thinking blocks。** 任何修改都会破坏签名，Claude 会拒绝 history。
4. **遇到 redacted thinking 就崩溃。** 把 redacted 当一等公民处理，不要假设 thinking 内容永远是可读文字。
5. **把原始 thinking 直接丢给用户看却没给 toggle。** 推理轨迹又长又偏内部，要么刻意呈现，要么默认隐藏。
6. **没检查兼容性就把 thinking 和 assistant 预填或自定义 temperature 混用。** 调用会失败或行为异常。

---

> **Key Insight**
>
> Extended thinking 是准确度的调节杆，不是默认值。正确的流程是：先优化 prompt，再建 eval，最后当 eval gap 明显是推理深度问题时才开 thinking。签名系统和 redacted blocks 是 safety 机制——把 thinking blocks 当成不透明对象，原样传递，不要假设它永远是可读文字。

---

## CCA Exam Relevance

- **D1 (Agentic Coding & Architecture)**：Extended thinking 是在 agentic loop 内加深 Claude 推理的标准做法。预期会考"什么时候 thinking 有帮助（难推理题）vs 什么时候是浪费（简单转换）"。
- **D5 (Enterprise Deployment)**：成本/延迟权衡、`thinking_budget` vs `max_tokens` 的约束、以及兼容性警告都是可直接出题的事实。
- 可能的题型："Prompt engineering 已到瓶颈——下一个手段是什么？"答案是 extended thinking，且需 eval-driven 决策。
- 记住两个 safety 机制：**signature**（篡改检测）和 **redacted blocks**（内部安全标记），两者都必须原样传回。

---

## Flashcards

| Front | Back |
|-------|------|
| Extended thinking 解决什么问题？ | Prompt engineering 已到瓶颈的难推理题——它给 Claude 草稿纸 token，让它在回答前深思熟虑。 |
| `thinking_budget` 的最小值是？ | 1024 tokens。 |
| `max_tokens` 和 `thinking_budget` 的关系？ | `max_tokens` 必须严格大于 `thinking_budget`，因为 budget 是从 max 里扣的。 |
| 启用 thinking 后会拿回哪两种 content block？ | 一个 thinking block（推理轨迹）和一个 text block（最终答案）。 |
| Thinking block 上的 signature 是什么？为何存在？ | 加密 token，用来证明 thinking 内容未被修改；防止开发者伪造 reasoning 把模型引导到危险区。 |
| 什么是 redacted thinking block？ | 推理被内部 safety 系统标记、以加密形式回传的 thinking block。代码必须能处理并原样传回。 |
| 何时应该启用 extended thinking？ | 只在优化 prompt、建好 eval、确认准确度仍因推理深度不足而低于门槛时才开。 |
| 举两个 extended thinking **不**兼容的功能。 | Assistant message pre-filling 与自定义 temperature。 |
| 启用 extended thinking 的三个代价？ | 成本更高（thinking tokens 计费）、延迟更高、客户端代码更复杂（block 迭代、签名、redaction）。 |
