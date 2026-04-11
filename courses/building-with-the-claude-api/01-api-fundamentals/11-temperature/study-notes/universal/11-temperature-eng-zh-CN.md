# Temperature — 工程深度解析

| 项目 | 细节 |
|------|------|
| 考试领域 | D5 — Enterprise Deployment (20%) |
| Task Statements | 5.1（模型配置）、5.3（production 模式）、5.4（evaluation 与可靠度） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 11 |

---

## 一句话总结

Temperature 是一个 sampling 参数（0.0–1.0），控制 Claude 下一个 token 概率分布的锐利或平滑程度——低值让输出确定、事实取向，高值让输出多变、具创意。

---

## Claude 实际上怎么生成文本

理解 temperature 前，先看三步骤生成循环：

1. **Tokenization**——输入被切成 tokens（subword 单位）
2. **Prediction**——模型对所有可能的下一个 token 计算概率分布
3. **Sampling**——从这个分布抽一个 token 加到输出。重复，直到模型输出 stop token 或达到 `max_tokens`

对于以「What do you think?」结尾的 prompt，分布可能长这样：

| 候选下一个 token | 概率 |
|-----------------|------|
| " about" | 30% |
| " would" | 20% |
| " of" | 10% |
| ... | ... |

模型挑一个、接上去，再跑整个循环生成下一个 token。Temperature 就是调整步骤 3 的旋钮。

---

## Temperature 在数学上做什么

Temperature 在 softmax 前对 logits（pre-softmax 分数）做 rescale。

- **Temperature = 0** → 分布坍缩成 argmax。永远挑概率最高的 token。输出几乎确定性（实务上——不计 tie-break）
- **Temperature = 1** → 直接用原始分布。Claude 从完整概率质量采样，生成多变输出
- **介于 0 和 1 之间** → 中间锐化程度。高概率 token 仍然被偏好，但低概率的也有合理机会

把它想成「信心旋钮」。0 的时候你只信最好的那个猜测；1 的时候你让多样性进来。

---

## 三个 Temperature 区段

不同的产品行为需要不同区段。课程定义了三个：

### 低（0.0 – 0.3）——确定性任务

当答案范围窄、事实很重要时使用。

- 事实性 Q&A
- Coding 辅助
- 数据抽取 / 分类
- 内容审核
- 任何要喂给下游 parser 的场景

### 中（0.4 – 0.7）——结构化创意

当你要连贯、有用、带点自然变化的输出时使用。

- Summarization
- 教育内容
- 问题解决
- 有约束的创意写作

### 高（0.8 – 1.0）——发散式生成

当目标是多样性与新颖时使用。

- Brainstorming
- 营销文案
- 虚构 / 笑话生成
- 发想 session

把区段和任务对上。内容审核系统开 temperature 1.0 是 bug。Brainstorming 工具开 temperature 0.0 很无趣。

---

## 把 Temperature 加进 chat 函数

接着 Lesson 09 的 `chat()` helper，把 `temperature` 加成第一级参数：

```python
from anthropic import Anthropic

client = Anthropic()

def chat(messages, system=None, temperature=1.0):
    params = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
    }
    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text
```

和 Lesson 09 版本的唯一差别是新的 `temperature=1.0` kwarg 和对应的 `params` 条目。注意 `temperature` **永远**被传入——和 `system` 不同，它不需要条件处理，因为 API 直接接受 float 值。

---

## 观察效果

用两个极端生成电影点子：

```python
messages = [{"role": "user", "content": "Give me a one-sentence movie idea."}]

print(chat(messages, temperature=0.0))
# "A time-traveling archaeologist must prevent ancient artifacts from being stolen."

print(chat(messages, temperature=1.0))
# 每次执行差异很大——不同主题、角色、情节
```

在 `0.0` 你常常每次拿到一样的答案。在 `1.0` 每次调用都会拿到明显不同的答案。这就是为什么非确定性流程的集成测试必须把 `temperature=0` 钉住，或用 LLM-as-judge evals，不能用 exact-match assertion。

---

## Temperature 不是保证

两个关键警告：

1. **Temperature 0 在不同 API 版本或 infra 上不严格确定性**。Tie-break、KV-cache 效应、backend routing 都可能产生罕见变异。如果你需要精确确定性，把低 temperature 搭配确定性 evaluation（对多次抽样做 exact-match，不是单次调用）
2. **高 temperature 不保证新颖**。就算 1.0，Claude 可能还是会重复常见措辞，因为那些 token 在分布里还是主导。Temperature 改变概率；它不会发明新 token

---

## Temperature 和其他 Sampling 参数

Temperature 是几个 sampling 控制之一。Anthropic API 也支持 `top_p`（nucleus sampling），把分布在累积概率阈值处截断。课程聚焦 temperature 因为它最直觉；实务上，production 系统通常把 `top_p` 留在默认，只调 temperature。

**经验法则**：一次只调一个 sampling 参数。`temperature` 和 `top_p` 一起调，会让输出很难推理。

---

## 常见错误

1. **在抽取 pipeline 用高 temperature**——如果下游 code 预期结构化 JSON，temperature 1.0 是 parse error 温床
2. **在创意任务用 temperature 0**——输出变得重复无趣，用户立刻察觉
3. **假设 temperature 0 是 bit-exact 可重现**——不是的；infra 层级的 nondeterminism 可能导致罕见变异
4. **在调 prompt 之前先调 temperature**——质量最大的杠杆是 prompt + system prompt；temperature 是微调旋钮，不是第一层修复
5. **完全忘了设 temperature**——全部默认 1.0 会让结构化任务的测试不稳定、production 行为不一致

> **Key Insight**
>
> Temperature 是政策决策，不是性能决策。它编码的是你产品能接受多少变异。依用户期望选区段：用户要*那个*答案（低）、*一个好*答案（中）、还是*很多不同*答案（高）？然后每个 endpoint 或 feature 锁死——不要让它飘动。

---

## CCA 考试重点

- **D5 (Enterprise Deployment)**：temperature 是核心 production 配置参数。预期会考给定场景该用哪个 temperature 区段（抽取 vs brainstorming）
- **D5.3（evaluation 与可靠度）**：确定性 evaluation pipelines 需要钉住 temperature——考试可能问可重现性
- 注意「如何让 Claude 输出在数据抽取任务上保持一致？」这种场景——答案是低 temperature（加上结构化 prompting），不是重试

---

## Flashcards

| 题目 | 答案 |
|------|------|
| Claude `temperature` 参数的有效范围？ | 0.0 到 1.0，含端点 |
| Temperature 0 在机制上是什么意思？ | Claude 每一步都挑概率最高的下一个 token——实际是 argmax，生成近确定性输出 |
| Temperature 1 在机制上是什么意思？ | 直接从完整概率分布 sampling，生成多变且具创意的输出 |
| 数据抽取该用哪个 temperature 区段？ | 低（0.0–0.3）——确定性和事实忠实度很重要 |
| Brainstorming 该用哪个 temperature 区段？ | 高（0.8–1.0）——目标是多样性与新颖 |
| Summarization 该用哪个 temperature 区段？ | 中（0.4–0.7）——结构化但带自然变化 |
| Temperature 0 是 bit-exact 可重现吗？ | 不是——infra 层级 nondeterminism 会造成罕见变异；是近确定性，不是保证 |
| 文本生成的三个步骤是？ | Tokenization → Prediction（概率分布）→ Sampling（挑下一个 token）|
| 为什么不该在调 prompt 前先调 temperature？ | Prompt 是第一层质量杠杆；temperature 是微调旋钮，修不了坏 prompt |
