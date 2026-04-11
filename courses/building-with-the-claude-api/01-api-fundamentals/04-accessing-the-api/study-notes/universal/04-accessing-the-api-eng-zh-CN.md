# Accessing the API — Engineering Deep Dive（简体中文）

| 项目 | 内容 |
|------|------|
| Exam Domain | D5 — Enterprise Deployment (20%) 主要；D3 — Claude Code Configuration (20%) 次要；D1 — Agentic Architecture (22%) |
| Task Statements | 5.1（model selection）、5.3（production patterns）、3.1（API key 管理）、1.2（agentic loop 基础） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 04 |

---

## One-Liner

一个生产环境的 Claude 请求会经过五个跳点：client → 你的服务器 → Anthropic API → 模型 pipeline → response。搞懂每一跳，才能做好安全架构、调试与成本/延迟调优。

---

## 五步请求生命周期

```
┌────────┐ 1) HTTPS  ┌────────┐ 2) HTTPS+key ┌──────────┐ 3) 模型
│ Client │ ────────▶│  你的  │ ────────────▶│ Anthropic│   处理
│  (app) │          │服务器  │              │   API    │  (tokenize,
│        │ ◀────────│        │ ◀────────────│          │   embed,
└────────┘ 5) JSON  └────────┘ 4) Response  └──────────┘   contextualize,
                                                           generate)
```

| 步骤 | 跳点 | 传递内容 | 谁持有 secret |
|------|------|---------|--------------|
| 1 | Client → Server | 用户 prompt、session token | — |
| 2 | Server → Anthropic | Prompt + `x-api-key` header | 服务器 |
| 3 | Anthropic 内部 | Tokens → embeddings → logits → next token | Anthropic |
| 4 | Anthropic → Server | `message` JSON（`content`、`usage`、`stop_reason`） | — |
| 5 | Server → Client | 渲染后的文本或 streaming SSE | — |

每个生产事故都落在这五跳中的某一跳。**第一个要问的问题永远是：哪一跳坏了？** 这个问题能不能问出来，取决于你有没有把这张图背下来。

---

## 为什么必须有服务器

直接从 client 调用 Anthropic 在生产环境是绝对禁止的。原因只有一个：API key 是 **bearer credential**——任何持有它的东西都可以花你的钱、看你的回复。

| 错误做法 | 后果 |
|---------|------|
| API key 写进 mobile app binary | 用 `strings` 或反编译就能挖出来 → 被滥用 |
| API key 写进浏览器 JS | DevTools 直接可见 → credits 瞬间被抽干 |
| API key commit 到 public GitHub repo | Anthropic 几分钟内会自动 revoke，但账单已经打下去了 |

服务器这一层是唯一可以做到以下事情的地方：
1. 把 key 放在环境变量或 secret manager（绝不写进源代码）。
2. 做按用户的 rate limit 与 auth。
3. 在数据离开你的边界前做 logging、审计、PII 脱敏。
4. 加 retry、circuit breaker、cache 等逻辑。

---

## 模型内部：四个处理阶段

请求进到 Anthropic 之后，Claude 会跑完四个阶段才吐出第一个 output token：

1. **Tokenization**（分词）——输入文本被切成 tokens。粗略把一个英文单词想成一个 token，但长词会被切成片段。
2. **Embedding**（嵌入）——每个 token 变成一个高维向量，同时编码该词所有可能的语义（例如 "quantum" 同时带有物理、计算、"非常小"等含义）。
3. **Contextualization**（上下文化）——周围的 tokens 把每个 embedding 往句子实际需要的那个语义拉。
4. **Generation**（生成）——最后一层产生词表上的概率分布；下一个 token 是用带随机性的采样抽出来的（不是纯 argmax）。新 token 追加到序列后面，循环继续。

```python
# 生成循环的概念 pseudo-code
tokens = tokenize(prompt)
while True:
    embeddings = embed(tokens)
    contextual = contextualize(embeddings)
    logits = output_layer(contextual)
    next_token = sample(logits)  # 不是纯 argmax
    tokens.append(next_token)
    if should_stop(next_token, tokens):
        break
```

采样这一步就是为什么两个完全一样的请求会返回不同的文字——temperature 跟随机性是刻意设计，让回复自然。

---

## 停止条件

每生成一个 token，Claude 都会检查三个退出条件：

| `stop_reason` | 含义 | 你该做什么 |
|---------------|------|----------|
| `end_turn` | 模型自己吐出 end-of-sequence token | 把文本返给用户 |
| `max_tokens` | 预算打满，被截断 | 调高 `max_tokens` 或显示截断 UI |
| `stop_sequence` | 撞到你在 `stop_sequences` 里给的字符串 | 预期行为——拿 sentinel 做切分 |

生产环境常见 bug：工程师把 `max_tokens` 设为 256，然后在 log 里写"Claude 截断了"当成模型 bug。这不是 bug，是你自己的预算。**一定要分支判断 `stop_reason`。**

---

## Response 结构

Anthropic 返回的 JSON 有一个稳定的形状，你的代码应该做 pattern match：

```python
from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "请解释五步请求流程。"}],
)

print(response.content[0].text)       # 生成的文本
print(response.usage.input_tokens)    # 成本指标 1
print(response.usage.output_tokens)   # 成本指标 2
print(response.stop_reason)           # "end_turn" | "max_tokens" | "stop_sequence" | "tool_use"
```

生产环境每个 app 都应该关心三个字段：
- `content` —— 模型吐出的文本或 tool_use block。
- `usage` —— input + output token 数；乘上价目表就是单次请求的真实成本。
- `stop_reason` —— 后端的分支信号，决定是"返给用户"、"继续 loop"还是"处理截断"。

---

## Common Mistakes

1. **从浏览器直接调用 Anthropic** —— key 秒被偷。一定要通过你的服务器代理。
2. **把 `max_tokens` 当成目标长度** —— 它是上限。模型遇到 `end_turn` 就停，不会刻意撑到那个数字。
3. **忽略 `stop_reason`** —— 代码永远假设 `end_turn`，结果 `max_tokens` 截断的时候静悄悄吞掉。
4. **把带 PII 的完整 prompt 写进 log** —— 服务器这一跳是唯一可以在数据离开边界前脱敏的地方。
5. **忘记生成是随机的** —— 断言字符串完全相等的测试会 flaky；要么断言结构，要么把 temperature 设低。

> **Key Insight**
>
> 五步流程不是考试冷知识，而是你调试每个生产事故时用的心智地图。请求失败时你第一个问题永远是"哪一跳？" 这个问题有没有答案，取决于你有没有把这张图内化。CCA 的 Enterprise Deployment domain 其他东西全部建在这张图上面。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）**：考题会丢情境问你 API key 该放哪、`max_tokens` 该设多少、生产代码怎么处理 `stop_reason`。
- **D3（Claude Code Configuration）**：API key 存储模式（env vars、secret manager，绝不写 client-side）。
- **D1（Agentic Architecture）**：request/response envelope 是每个 agent loop 的原子单位——所有 agent 都是跑这个流程的 for-loop。
- 题目里出现"API key 该放在哪"→ 答案永远是服务器，绝不是 client。

---

## Flashcards

| Front | Back |
|-------|------|
| Claude 请求生命周期的五个步骤是什么？ | Client → Server、Server → Anthropic API、模型处理、Anthropic → Server、Server → Client |
| 为什么 API key 必须放服务器不能放 client？ | Key 是 bearer credential，任何 client 持有都能被取出并滥用，把你的 credits 抽干 |
| 模型内部四个阶段是什么？ | Tokenization、embedding、contextualization、generation |
| `max_tokens` 的真正含义？ | 输出长度的上限——遇到 `end_turn` 会提前停，模型不会刻意撑到这个数字 |
| 这一课提到哪三个 `stop_reason`？ | `end_turn`（自然结束）、`max_tokens`（打到预算）、`stop_sequence`（撞到用户给的 sentinel） |
| 哪个 response 字段告诉你这一次花了多少钱？ | `response.usage.input_tokens` 与 `response.usage.output_tokens` |
| 为什么两个完全一样的请求会返回不同的文字？ | 生成是从概率分布做带随机性的采样，不是纯 argmax |
| 每个请求必须带的四个字段？ | API key、model 名称、messages list、max_tokens |
