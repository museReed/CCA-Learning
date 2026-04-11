# Text Embeddings — 工程深度解析

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Architecture (22%) 主要；D4 — Safety & Alignment (20%) 次要 |
| Task Statements | 1.3（context management）、4.1（grounded responses） |
| 来源 | building-with-the-claude-api / 05-rag / Lesson 47 |

---

## 一句话总结

Text embedding 是一个捕捉文字意义的数值向量；RAG retrieval 的做法就是把 user query 和存储的 chunks 都转成 embedding，再找出向量与 query 最接近的 chunks。

---

## Retrieval 问题

切完 chunk 之后，你手上有一堆文字片段。用户提问时，你要找出哪些 chunks 与问题相关。这本质上是**搜索问题** — 「扫所有 chunks，找出与 query 相关的」。

两种做法：

- **Keyword search** — 找完全匹配的字。快、简单，但遇到同义词、改写、共享概念但无共享字词的情况会失败。
- **Semantic search** — 找*意义*最接近 query 的 chunks，不管确切字词。这是 RAG 默认，由 embeddings 支撑。

用户用自然语言问问题、且不一定鹦鹉学舌文档用语时，semantic search 是对的工具。「这家公司赚了多少？」应该要能匹配到标题为「Revenue」的 chunk，即使没有共享关键词。

---

## 什么是 text embedding？

Text embedding 是某段文字**意义的数值表示**。想象成把字和句子转换成电脑可以用数学比较的格式。

流程：

- 你把文字喂进 **embedding model**
- 模型输出一个很长的**数字 list**（embedding 向量）
- 每个数字范围 **-1 到 +1**
- 每个数字代表输入文字的某种学到的特征或质量

---

## 理解这些数字

embedding 里每个数字本质上是某种输入质量的「分数」。重点警告：**我们无法精确知道每个数字代表什么**。

会很想说「第 42 维代表文字有多快乐」或「第 17 维代表文字多谈海洋」，但这些只是概念示意。每个维度的实际语义是模型在训练时学到的，人类无法直接解读。

对 RAG 重要的不是每个维度*代表什么*，而是意义相似的文字会产生相似的向量。模型保证**几何**，我们不需要解读轴。

---

## 用 VoyageAI 做 embeddings

Anthropic 目前不提供 embedding 生成。推荐 provider 是 **VoyageAI**。

设定步骤：

1. 申请 VoyageAI 账号（与 Anthropic 分开）
2. 取得 API key（免费起步）
3. 把 key 加到环境变量

在 `.env` 加：

```
VOYAGE_API_KEY="your_key_here"
```

这是部署时要注意的 D5 相关重点：RAG pipeline 引入**第二个 vendor**到你的 stack，有自己的 key、rate limit、定价、SLO。

---

## 实现

安装 library：

```
%pip install voyageai
```

设定 client 与 helper function：

```python
from dotenv import load_dotenv
import voyageai

load_dotenv()
client = voyageai.Client()

def generate_embedding(text, model="voyage-3-large", input_type="query"):
    result = client.embed([text], model=model, input_type=input_type)
    return result.embeddings[0]
```

要注意：

- `client.embed` 吃的是**文字 list**，不是单一字符串 — API 是 batched。embedding 所有 chunks 时可以（也应该）一次传多笔。
- `result.embeddings` 是跟输入 list 对齐的 list；单笔情况取 `[0]`。
- `input_type` 有差：「query」vs.「document」。许多 embedding 模型有非对称调校，即使同一段文字，query 和 document 产出的向量会略有不同。
- `model="voyage-3-large"` 是 lesson 的例子 — 依质量／成本／延迟目标挑模型大小。

对 chunk 跑这个 function 会返回一个 floating-point 数字 list — 就是 embedding。流程本身简单；真正挑战在**有效率地**用 embedding 做 retrieval。

---

## Embeddings 在 RAG pipeline 的位置

```
┌──────────────┐    chunk       ┌──────────────┐   每个 chunk 都 embed  ┌──────────────┐
│   Document   │ ─────────────▶ │    Chunks    │ ───────────────────▶ │   Vectors    │
└──────────────┘                └──────────────┘                      └──────────────┘
                                                                            │
                                                                            ▼
┌──────────────┐  embed query   ┌──────────────┐   比对向量              ┌──────────────┐
│  User query  │ ─────────────▶ │ Query vector │ ───────────────────▶ │  Top-k chunks│
└──────────────┘                └──────────────┘                      └──────────────┘
```

embedding 会被调用**两次**：

1. **预处理时** — corpus 里每个 chunk 都被 embed 并存储。
2. **查询时** — 每个进来的 user query 被 embed，那个向量拿去和存储的 chunk 向量比对。

比对两边必须用同一个 embedding model。混用模型产生的是不同几何空间的向量，similarity score 会变得毫无意义。

---

## Query vs. Document input type

VoyageAI 暴露 `input_type` 参数，有 `"query"` 和 `"document"` 这种值。lesson 的示例 function 用 `input_type="query"`。在完整 pipeline 里：

- embed **要存储的 chunks** 时传 `input_type="document"`
- embed **查询时的 user 问题**时传 `input_type="query"`

模型被调校过，让 query embedding 能和 document embedding 最好地对齐。这个小细节可以测得出 retrieval 质量差异。

---

## CCA Task 对应

- **Task 1.3（Context Management）** — embedding 是你挑选哪些 chunk 变成 context 的机制，是 context 挑选的「评分函数」。
- **Task 4.1（Grounded Responses）** — grounding 质量取决于 retrieve 到的 chunks 对不对；embedding 是第一个控制这件事的杠杆。

---

## 常见错误

1. **index 和 query 用不同 embedding model** — 向量在不同空间；相似度变胡说。
2. **`input_type` 没用对** — provider 支持时，document 和 query 要用各自对应的 input type。
3. **每次 query 都 re-embed chunks** — chunks 预处理时 embed 一次、存好向量、反复用。runtime 只 embed query。
4. **忘了预留 VoyageAI 的延迟与成本** — embedding API 调用是每次 query 的新 network hop；对 p99 延迟和每次查询成本有影响。
5. **以为维度可解读** — 你无法「看某个维度」来 debug retrieval 失败；debug 永远是比对整个向量。

> **关键洞察**
>
> Embedding 把「哪个 chunk 对这个 query 最相关」化约成「哪个向量对这个向量最接近」。这就是全部的 trick。你不需要理解个别维度代表什么 — 只需要相信模型把语义相似的文字放在向量空间中靠近的位置。RAG retrieval 的全部艺术在于挑一个好的 embedding model、并正确地比对向量。

---

## CCA 考试关联

- **D1（Agentic Architecture）**：embedding 是 RAG retrieval 的搜索骨干。熟悉它是什么、怎么产生、为什么能做 semantic search。
- **D4（Safety & Alignment）**：更好 retrieval → 更好 grounding → 更少幻觉。embedding 是 retrieval 质量的起点。
- 预期考题像「Anthropic 不提供 embeddings — 推荐的 provider 是？」（VoyageAI）、「embedding 值范围是？」（每个维度 -1 到 +1）。

---

## Flashcards

| Front | Back |
|-------|------|
| 什么是 text embedding？ | 一段文字意义的数值向量表示，用于 semantic search。 |
| embedding 里每个数字的范围是？ | -1 到 +1。 |
| Anthropic 提供 embedding 吗？ | 不 — lesson 推荐 VoyageAI 当 embedding provider。 |
| VoyageAI 用哪个环境变量？ | `.env` 里的 `VOYAGE_API_KEY`。 |
| Semantic search 和 keyword search 有何不同？ | Semantic search 通过向量相似度比对意义；keyword search 只比对确切字。 |
| `input_type` 参数做什么？ | 告诉 embedding model 输入是 query 还是 document；模型用非对称调校优化 retrieval 质量。 |
| RAG pipeline 里 embedding model 会被调用几次？ | 预处理时很多次（每个 chunk 一次），runtime 每个进来的 user query 一次。 |
| 为什么 index 和 query 混用不同 embedding model 是错的？ | 向量在不同空间，similarity 失去意义。 |
