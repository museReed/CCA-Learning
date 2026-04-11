# Chaining Workflows — 工程深度解析

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture(22%)— 主要 |
| 任务陈述 | 1.2(agentic 模式 — chaining)、5.2(production workflow 部署)|
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 79 |

---

## 一句话总结

Chaining 是最简单也最实用的 workflow 模式: 把复杂任务拆成顺序的 LLM 调用序列, 每一步的输出喂给下一步 — 与 parallelization 相反, 用在后续步骤*依赖*前面步骤的场景。

---

## 什么是 Prompt Chaining

出自 Anthropic "Building Effective Agents" 博客, **prompt chaining** 把任务拆成一系列步骤, 每次 LLM 调用处理前一次的输出。当你能干净地拆解任务, 而且每一步都依赖前一步的结果时, 这个模式最适合。

你需要 chaining 的关键信号: 步骤可以按顺序列出, 而且步骤 N+1 真的需要步骤 N 的输出。

---

## 课程中的社交媒体示例

课程演示一个自动生成并发布视频的社交媒体营销工具:

```
1. 从 Twitter 找相关热门话题       (非 LLM)
2. 选出最吸引人的话题                (Claude)
3. 研究该话题                        (Claude)
4. 写短视频脚本                      (Claude)
5. 用 AI 虚拟人 + TTS 生成视频       (非 LLM)
6. 发布到社交媒体                    (非 LLM)
```

重点观察:
- **不是每步都是 LLM 调用。** Chain 可以混搭 LLM 与非 LLM 处理(步骤 1 是 Twitter API、步骤 5 是视频 pipeline、步骤 6 是发布 API)。
- **每个 LLM 步骤都聚焦。** Claude 在步骤 2 挑话题、步骤 3 研究、步骤 4 写脚本 — 从不在同一 prompt 里做三件事。
- **输出向后传。** 选好的话题变成研究步骤的输入; 研究结果变成脚本步骤的输入。

---

## 为什么要 chain 而不是一个大 prompt

Chaining 给你:

1. **每步都聚焦。** Claude 专心做好一件事, 而不是同时应付全部。
2. **非 LLM 处理的 hook。** 步骤之间, 你的代码可以验证、转换、抓数据、或短路流程。
3. **可测试。** 每一步有干净的 input/output contract, 容易 unit test 和 eval。
4. **可观测。** 失败被定位到特定步骤, 而不是埋在巨型 prompt 里。
5. **部分重跑。** 5 步里第 3 步失败时, 可以从第 3 步重跑, 不用整个重来。

---

## 长 Prompt 问题(课程的核心动机)

即便你的限制写得很清楚, Claude 有时还是会在长 prompt 中忽略规则。课程示例是写一篇技术文章, 要:

- 不能提到是 AI 写的
- 不能用 emoji
- 不能有过时或过于随意的语言
- 要专业、技术语气

单一 prompt 想一边生好内容、一边满足四个限制, 常常产出违反其中一个以上的结果。

### Chaining 解法

拆成两步:

**步骤 1 — 初稿**
```python
draft = claude.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=2048,
    messages=[{"role": "user",
               "content": f"写一篇关于 {topic} 的技术文章。"}]
).content[0].text
```

**步骤 2 — 聚焦修订**
```python
final = claude.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=2048,
    messages=[{"role": "user", "content": f"""
请修订下方文章。

按照以下步骤重写:
1. 找出任何指明作者是 AI 的地方, 删除
2. 找出并删除所有 emoji
3. 找出任何尴尬用语, 替换为技术写作者会用的语气

<article>
{draft}
</article>
"""}]
).content[0].text
```

步骤 2 中, Claude 不是同时在*创建*好文章*并*满足限制 — 它只是在已写好的文章上执行限制。聚焦任务能完成组合任务失败的事。

---

## 标准 Python 实现

```python
from anthropic import Anthropic

client = Anthropic()

def call_claude(system: str, user: str) -> str:
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return resp.content[0].text

def social_media_chain(keyword: str) -> str:
    # Step 1: 非 LLM — 抓趋势
    trends = twitter_api.fetch_trends(keyword)

    # Step 2: LLM — 挑最佳话题
    topic = call_claude(
        system="你负责挑选最吸引人的趋势。",
        user=f"趋势:\n{trends}\n\n返回单一最佳话题。",
    )

    # Step 3: LLM — 研究话题(带错误检查)
    research = call_claude(
        system="你是精简的研究员。",
        user=f"研究这个话题: {topic}",
    )
    if len(research) < 100:
        raise RuntimeError("研究步骤返回内容过少")

    # Step 4: LLM — 用研究内容写脚本
    script = call_claude(
        system="你写 60 秒视频脚本。",
        user=f"用这份研究写脚本:\n{research}",
    )

    # Step 5: 非 LLM — 合成视频
    video = video_pipeline.synthesize(script)

    # Step 6: 非 LLM — 发布
    return social_media.post(video)
```

每一步都有清楚的 contract、错误处理 hook, 可以独立替换。

---

## Chain 中的错误传递

因为每一步依赖前一步, chain 必须刻意处理错误:

| 策略 | 说明 | 使用时机 |
|------|------|---------|
| **Fail fast** | 一失败就抛异常 | 早期 prototype、简单流程 |
| **Retry step** | 失败步骤用 backoff 重试 | 短暂 API 错误 |
| **Validate then branch** | 检查步骤输出, 选下一步 | 输出质量有变动(例如空研究)|
| **Graceful degradation** | 跳过非关键步骤 | 选用的丰富化步骤 |
| **Replay from checkpoint** | 持久化步骤输出, 重试时接续 | 长 chain、昂贵调用 |

Production chain 通常五种都混用, 每一步都包 retry + validation。

---

## Chaining vs Parallelization vs Agent

| 方面 | Chaining | Parallelization | Agent |
|------|----------|-----------------|-------|
| 步骤依赖 | 有(顺序)| 无(独立)| 运行期决定 |
| Control flow | 代码 | 代码 | LLM |
| 延迟 | 步骤延迟总和 | 步骤延迟最大值 | 变动 |
| 成本 | 步骤成本总和 | 步骤成本总和 | 变动 |
| 最适合 | 有依赖的多步复杂任务 | 跨独立标准的复杂决策 | 开放式任务 |

---

## 常见错误

1. **该 chain 却做成 agent。** 如果你能列出步骤, chain 比把流程交给 Claude 更简单可靠。
2. **Chain 太长。** 每步都是失败点。如果 LLM 调用超过 10 次, 考虑拆成多个 chain 加 checkpoint。
3. **忘了在步骤间传递 context。** 步骤 4 需要步骤 3 的输出 — 不要以为 Claude 会记得, 要明确注入。
4. **步骤间没错误处理。** 一个坏步骤可以把垃圾传到最后。要在步骤间验证。
5. **把该用单一调用的任务做成 chain。** 不是每个任务都该 chain。如果一个 prompt 可靠就用一个 prompt。

---

> **关键洞察**
>
> Chaining 是 "长 prompt 问题" 的解法模式。当 Claude 在巨型 prompt 中忽略限制时, 拆开任务: 一个调用负责生, 另一个负责执行限制。这个 "聚焦注意力" 原则延伸到任何下一步需要前一步输出的多步任务。考试记住: **chaining 有序列依赖, parallelization 没有。**

---

## CCA 考试关联

- **D1(22%)主要**: Chaining 是四大 workflow 模式之一, 预期有场景题要你与 parallelization 和 routing 区分。
- **D5(20%)次要**: Production chain 需要错误处理、checkpoint、步骤间验证。
- Chaining 信号词: "sequential"、"output of step N feeds step N+1"、"focus on one aspect at a time"、"break down into steps"。
- 关键区分: chaining = 序列依赖; parallelization = 独立子任务。

---

## Flashcards

| 题目 | 答案 |
|------|------|
| 什么是 prompt chaining? | 把任务拆成顺序 LLM 调用, 每一步输出喂下一步 |
| Chaining 和 parallelization 的区别? | Chaining 有序列依赖; parallelization 是并行独立子任务 |
| Chaining 解决的 "长 prompt 问题" 是什么? | Claude 在巨型 prompt 中忽略限制; 拆成 "生成 + 修订" 步骤可靠地强制执行 |
| Chain 可以包含非 LLM 步骤吗? | 可以 — chain 常常混搭 LLM 调用与 API、验证、数据转换 |
| 强制限制的两步 chaining 解法? | 步骤 1: 生初稿。步骤 2: 专门修订执行每条规则 |
| 列出 chain 的四种错误处理策略。 | Fail-fast、retry-step、validate-then-branch、graceful degradation、replay-from-checkpoint |
| Chaining 和 parallelization 的权衡? | Chaining 延迟总和(较慢)但支持依赖; parallelization 延迟最大值但需独立 |
| 什么时候*不*该用 chaining? | 当单一 prompt 可靠或子任务可独立执行时(改用 parallelization)|
