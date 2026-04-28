# Parallelization Workflows — 工程深度解析

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture(22%)— 主要 |
| 任务陈述 | 1.2(agentic 模式 — parallelization)、5.2(production workflow 部署)|
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 78 |

---

## 一句话总结

Parallelization workflow 把一个复杂任务拆成多个独立子任务并行执行(通常用 `asyncio.gather`),再用最后一次 LLM 调用汇总结果 — 这是 LLM 推理版的 "fan-out / fan-in" 模式。

---

## 这个模式解决什么问题

单一 prompt 处理复杂决策时,会逼 Claude 同时兼顾很多标准。课程的标准示例: 材料推荐系统, 要从 metal、polymer、ceramic、composite、elastomer、wood 六种材料中挑一个适合某零件图片的。

朴素做法(一个 prompt):
```
"看这个零件, 从以下材料挑最好的: metal、polymer、ceramic、composite、elastomer、wood。
考虑强度、重量、成本、可制造性、抗腐蚀……"
```

问题:
1. Claude 要把注意力分散到 6 种材料 × 5+ 个标准 = 30+ 个考量
2. 没有任何单一材料被深入分析
3. 难以优化 — 你没办法单独 A/B 测 "metal prompt"
4. 想加第 7 种材料得重写整个 prompt

---

## Parallelization 模式

出自 Anthropic "Building Effective Agents" 博客, parallelization 有两种变体:

| 变体 | 用途 | 示例 |
|------|------|------|
| **Sectioning** | 把任务拆成独立子任务, 每个聚焦一个方面 | 材料推荐(每种材料一个 LLM)|
| **Voting** | 跑*同一个*任务多次, 取多数决 | Moderation("这内容安全吗?") N 个投票者 |

两者都是并行跑 N 个 LLM 调用再汇总。区别在于每个子任务的输入/prompt 是*不同*(sectioning)还是*相同*(voting)。

---

## 标准结构

```
       ┌─→ 子任务 1 ──┐
input ─┼─→ 子任务 2 ──┼─→ aggregator ─→ 最终输出
       └─→ 子任务 N ──┘
```

1. **Split** — 把一个输入转成 N 个聚焦子任务
2. **Fan-out** — 并行跑 N 个子任务(`asyncio.gather`)
3. **Fan-in / Aggregate** — 把所有子任务结果喂给最后一次 LLM 调用做单一决策
4. **Return** — 把汇总结果返回给用户

---

## Python 实现(asyncio.gather)

```python
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

MATERIALS = ["metal", "polymer", "ceramic", "composite", "elastomer", "wood"]

async def evaluate_material(image_b64: str, material: str) -> dict:
    """每种材料一个专用的 LLM 调用。"""
    prompt = f"""
你是材料工程师, 评估 {material} 是否适合图中零件。
只聚焦在 {material} 的标准:

<criteria>
{MATERIAL_CRITERIA[material]}
</criteria>

返回 JSON: {{"material": "{material}", "score": 0-10, "rationale": "..."}}
"""
    resp = await client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64",
                                             "media_type": "image/jpeg",
                                             "data": image_b64}},
                {"type": "text", "text": prompt},
            ],
        }],
    )
    return parse_json(resp.content[0].text)

async def aggregate(evaluations: list[dict]) -> str:
    """Fan-in: 把所有专门评估合并成最终选择。"""
    prompt = f"""
以下是同一个零件的 6 份独立材料评估:

{json.dumps(evaluations, indent=2, ensure_ascii=False)}

挑出最佳材料并说明理由。
"""
    resp = await client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text

async def material_recommender(image_b64: str) -> str:
    # fan-out
    tasks = [evaluate_material(image_b64, m) for m in MATERIALS]
    evaluations = await asyncio.gather(*tasks)
    # fan-in
    return await aggregate(evaluations)
```

实现要点:
- 用 `AsyncAnthropic`(不是 `Anthropic`), 调用才能 await
- `asyncio.gather(*tasks)` 让 fan-out 阶段真正并行
- 每个子任务小、聚焦、可独立测试
- Aggregator 一次看到所有结构化结果

---

## 好处

1. **聚焦注意力** — 每次 Claude 调用专注一个方面, 准确度提升
2. **独立优化** — 改 metal prompt 不会影响其他; per-material A/B 测试
3. **可扩展** — 加第 7 种材料只要多加一个 prompt 文件, 其他六个零风险
4. **可靠性** — 每次调用认知负担低, 输出更一致
5. **延迟** — N 次并行调用 ≈ 最慢那一次的时间, 而不是 N × 平均

---

## 不该用 Parallelization 的时机

- 后续步骤*依赖*前面输出的任务(改用 chaining — Lesson 79)
- 子任务无法有意义地分开("总结这篇文章" 无法并行化)
- 成本比延迟更重要: parallelization 是*增加*调用次数, 不是减少, token 花费会乘以 N

---

## Voting 变体

同样的基础设施也能跑 voting: 让*同一个* prompt 跑 N 次, 用多数决汇总。适合安全关键决策:

```python
async def moderation_vote(text: str, n: int = 5) -> bool:
    tasks = [is_safe(text) for _ in range(n)]
    votes = await asyncio.gather(*tasks)
    return sum(votes) > n / 2  # 多数决
```

Voting 用成本换可靠度 — 经典的 ensemble 技术套到 LLM 上。

---

## 常见错误

1. **忘了 aggregation 步骤。** 并行子任务本身不会产生决策, 你还需要一个最后的 LLM(或规则)aggregator。
2. **让子任务互相依赖。** 如果子任务 2 需要子任务 1 的输出, 那是 chain 不是 parallel, `asyncio.gather` 会 race 或 deadlock。
3. **用 `Anthropic` 而不是 `AsyncAnthropic`。** Sync client 会 block, 结果变成串行而非并行。
4. **忽略每个任务的 timeout。** 一个慢调用会拖住整个 gather。用 `asyncio.wait_for` 或 `gather(return_exceptions=True)`。
5. **Token 成本爆炸。** 每个并行调用都是独立 API 账单。控制 N, 可以 cache 就 cache。

---

> **关键洞察**
>
> Parallelization 是 "聚焦注意力" 的 workflow — 每次 Claude 调用只负责一个窄责任, 单次分析更好, 总延迟也更低。代价是 N 倍 API 花费, 所以适用于质量比成本重要、或延迟是瓶颈时。考试记得两种变体: **sectioning**(不同子任务)与 **voting**(同一任务跑 N 次)。

---

## CCA 考试关联

- **D1(22%)主要**: 预期有场景题要你识别 parallelization(关键词: "split"、"run simultaneously"、"fan out"、"aggregate")。
- **D5(20%)次要**: Production 模式 — `asyncio.gather`、延迟/成本权衡。
- 信号词: "split into multiple independent evaluations"、"run simultaneously"、"aggregate results"、"fan-out / fan-in"。
- 两种变体都要懂(sectioning vs voting)。

---

## Flashcards

| 题目 | 答案 |
|------|------|
| 什么是 parallelization workflow? | 把一个任务拆成独立子任务并行执行, 再汇总结果 |
| Parallelization 的两种变体? | Sectioning(不同子任务同一输入)与 voting(同一任务跑 N 次)|
| 执行 fan-out 阶段的 Python 原语? | `asyncio.gather(*tasks)` 配 `AsyncAnthropic` client |
| 为什么 parallelization 比一个 mega-prompt 好? | 聚焦注意力、可独立优化、可扩展、更可靠 |
| Parallelization 的成本取舍? | N 倍 API 花费换取质量与延迟 |
| 什么时候*不*该用 parallelization? | 子任务互相依赖时(改用 chaining)、或成本比质量更重要时 |
| Voting 模式用来做什么? | 安全/共识决策 — 同一 prompt 跑 N 次取多数决(例如 moderation)|
| 能让 Anthropic 调用并行的 client class? | `AsyncAnthropic` — Anthropic SDK 的 async 版 client |
