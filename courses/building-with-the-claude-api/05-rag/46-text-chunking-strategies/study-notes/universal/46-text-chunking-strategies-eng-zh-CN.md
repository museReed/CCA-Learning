# Text Chunking Strategies — 工程深度解析

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Architecture (22%) 主要；D4 — Safety & Alignment (20%) 次要 |
| Task Statements | 1.3（context management）、4.1（grounded responses） |
| 来源 | building-with-the-claude-api / 05-rag / Lesson 46 |

---

## 一句话总结

Chunking 是 RAG 里决定「可检索单位」长什么样子的步骤，烂的 chunking 策略会默默毒死所有下游 retrieval，把不相关内容塞进 prompt、产出很有信心的错答案。

---

## 为什么 chunking 是杠杆最大的一步

想象一份文档有两个 section：医疗研究和软件工程。用户问「How many bugs did engineers fix this year?」。如果 chunking 烂，医疗 section 里出现的「bug」（像是「XDR-47, a bug we have not seen before」）就会被抓进 context，结果 Claude 很开心地回答病毒的事，而不是软件缺陷。

这就是核心失败模式：**chunk 看起来相关只是因为共享关键词，但周围语义是不一样的**。chunking 决定语义相似度被评估的粒度。太粗，chunk 混主题；太细，chunk 失去 context。

---

## 策略 1：Size-Based Chunking

最简单的做法 — 把文字切成等长字符串。325 字符的文档可能变成三个 ~108 字符的 chunks。

**优点：**
- 实现超简单
- 适用任何文档类型（文字、code、log 任意内容）
- chunk 数量与大小可预测

**缺点：**
- 字会被切在句子中间
- chunk 失去周边文字的重要 context
- section header 可能被从内容中切开

### 解法：加上 Overlap

Overlap 代表每个 chunk 包含邻近 chunk 的部分字符 — 形成滑动窗口保留边界 context。

```python
def chunk_by_char(text, chunk_size=150, chunk_overlap=20):
    chunks = []
    start_idx = 0

    while start_idx < len(text):
        end_idx = min(start_idx + chunk_size, len(text))
        chunk_text = text[start_idx:end_idx]
        chunks.append(chunk_text)

        start_idx = (
            end_idx - chunk_overlap if end_idx < len(text) else len(text)
        )

    return chunks
```

两个要注意的点：
1. loop 实际上前进 `chunk_size - chunk_overlap` — overlap 缩小净步长。
2. 终点分支设 `start_idx = len(text)` 保证 loop 会结束，避免 off-by-one。

---

## 策略 2：Structure-Based Chunking

按文档自然结构切 — header、段落、section。最适合你控制格式的情况（Markdown、内部报告有保证的 heading 样式）。

```python
def chunk_by_section(document_text):
    pattern = r"\n## "
    return re.split(pattern, document_text)
```

**优点：**
- 最干净、语义最完整的 chunk — 每块都是完整语义单位
- 自然边界符合人类对文档的理解
- 「关于 risk factors」的 chunk 真的包含 Risk Factors section

**缺点：**
- 只在结构有保证时才能用 — 纯文字或扫描 PDF 没有 header 可切
- section 大小差异很大；一个 50 字、另一个可能 5000 字
- 一个巨大的 section 还是可能爆掉 token 预算

Structure-based 在格式配合时是**理想**，在不配合时是**错误工具**。

---

## 策略 3：Semantic-Based Chunking

先切成句子，用 NLP 衡量相邻句子之间的关联度，把相关句子组合成 chunks。

**优点：**
- 产生语义上最连贯的 chunks
- 边界依意义切，不依字符或 header

**缺点：**
- 运算成本高（预处理时要跑 semantic similarity 模型）
- 实现要做对很复杂
- 调参比 size 或 sentence 方法困难

chunk 质量很关键、而且你有 compute 预算支撑时才用 semantic chunking。

---

## 策略 4：Sentence-Based Chunking（实务中庸）

用 regex 切成句子，再把句子组成 chunk 并可选择句子层级 overlap。

```python
def chunk_by_sentence(text, max_sentences_per_chunk=5, overlap_sentences=1):
    sentences = re.split(r"(?<=[.!?])\s+", text)

    chunks = []
    start_idx = 0

    while start_idx < len(sentences):
        end_idx = min(start_idx + max_sentences_per_chunk, len(sentences))
        current_chunk = sentences[start_idx:end_idx]
        chunks.append(" ".join(current_chunk))

        start_idx += max_sentences_per_chunk - overlap_sentences

        if start_idx < 0:
            start_idx = 0

    return chunks
```

注意 regex `(?<=[.!?])\s+` — 一个 lookbehind，把结尾标点留在前一句而不是丢掉。overlap 现在以**句子**为单位而不是字符，这更有意义。

Sentence-based 是你没有结构保证但又想要人类可读 chunk 边界时的合理默认。

---

## 如何选择策略

| 策略 | 最适合 | 避免 |
|------|--------|------|
| **Structure-based** | Markdown、有保证 header 的内部报告 | 纯文字、PDF、格式混杂 |
| **Sentence-based** | 大部分散文文档 | code（句子概念不适用） |
| **Size-based + overlap** | 任何内容类型、code、log、fallback | 有更好结构信号且想用的时候 |
| **Semantic** | retrieval 质量值得付出的高风险场景 | latency 或预算吃紧的预处理 |

**生产环境经验**：size-based + overlap 常是首选，因为简单可靠、适用任何东西。不会完美但不会坏你 pipeline。等有证据显示 retrieval 质量在伤害产品时再升级 sentence／structure／semantic。

**没有单一「最佳」策略**。对的选择要看你的文档、用例、以及你能承担的质量／复杂度取舍。

---

## CCA Task 对应

- **Task 1.3（Context Management）** — chunking 是你控制可检索 context 粒度的手段；chunk 大小决定系统中「一个知识单位」是什么。
- **Task 4.1（Grounded Responses）** — 好的 chunking 降低把离题文字抓进来、把错答案 grounded 的几率。

---

## 常见错误

1. **以为 chunking 是已解决的问题** — chunking library 的默认参数会一直可以用，直到它不行了，而你不知道为什么 retrieval 开始错。
2. **size-based 没有 overlap** — 字和句子被切在边界，chunk 失去让自己可被检索的 context。
3. **对非结构化文字用 structure-based** — 没有 header 时 regex 会返回整份文档当一个 chunk。
4. **不同文档类型用同一个策略** — code、散文、table 需要不同策略；不要强迫同一个 chunker 处理全部。
5. **生产没 log chunk ID** — retrieval 返回错 chunk 时，除非能追到是哪个 chunk 被挑，否则无法 debug。

> **关键洞察**
>
> Chunking 是 RAG pipeline 第一个会默默骗用户的地方。下游每个步骤 — embedding、retrieval、prompt 组装 — 都把 chunks 当成 given。chunk 若跨主题边界或切掉定义，retrieval 系统会很有信心地返回它，Claude 会很有信心地用它回答。投资在 chunking eval 要在投资 retrieval 调校之前。

---

## CCA 考试关联

- **D1（Agentic Architecture）**：chunking 是 RAG context-management pipeline 的第一个决策。熟悉四种策略、取舍、和何时用哪个。
- **D4（Safety & Alignment）**：烂 chunking 是错答案的默默来源 — lesson 里「bug」的例子是经典考题情境。
- 预期会看到「Markdown 文档有保证 header → 哪个策略？」（structure）、「纯文字 PDF → 哪个策略？」（size+overlap 或 sentence）。

---

## Flashcards

| Front | Back |
|-------|------|
| 列出课程涵盖的四种 chunking 策略。 | Size-based、structure-based、sentence-based、semantic-based。 |
| chunk overlap 解决什么问题？ | 边界 context 流失 — 确保完整字／句，并保留邻近 chunk 共享的 context。 |
| 何时选 structure-based chunking？ | 文档结构有保证时（Markdown header、模板化报告）。 |
| structure-based chunking 的缺点？ | 只在结构存在时有效；没 header 的纯文字或 PDF 无法使用。 |
| 为什么 semantic chunking 昂贵？ | 预处理时要跑 NLP／相似度模型衡量句子关联。 |
| 生产的 chunking fallback 策略？ | Size-based + overlap — 适用任何内容类型。 |
| 为什么「bug」的例子（医疗 vs. 工程）有启发性？ | 示范烂 chunking 如何单因关键词重叠就把不相关 chunk 抓进 prompt。 |
| `chunk_by_char` 里 `start_idx = end_idx - chunk_overlap` 做什么？ | 让窗口前进 `chunk_size - chunk_overlap`，保留相邻 chunk 的 overlap。 |
