# A Typical Eval Workflow — Engineering Deep Dive（简体中文）

| 项目 | 内容 |
|------|------|
| Exam Domain | D3 — Evaluation & Iteration（20%，主要）；D5 — Enterprise Deployment（20%，次要） |
| Task Statements | 3.1（eval 设计）、3.2（测试数据集）、3.3（eval 执行） |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 18 |

---

## 一句话摘要

Prompt evaluation 工作流是一个五步循环 — draft、dataset、run、grade、iterate — 把主观的 prompt engineering 变成可度量、可复现、甚至可以放进 CI 的流程。

---

## 五步工作流

课程定义了"最小可行"的 eval 工作流。市面上每一个开源或付费 eval 工具本质上都是这五步的更精细实现。

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ 1. Draft     │ → │ 2. Dataset   │ → │ 3. Run       │ → │ 4. Grade     │ → │ 5. Iterate   │
│   a prompt   │   │              │   │   Claude     │   │   outputs    │   │   prompt     │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
        ▲                                                                             │
        └─────────────────────────────────────────────────────────────────────────────┘
                                  迭代直到分数进入平台期
```

---

## Step 1：起草 Prompt

从你本来就会写的 prompt 开始。课程刻意用了一个极简 baseline：

```python
prompt = f"""
Please answer the user's question:

{question}
"""
```

Baseline 的价值不在于它写得好，而在于它"可度量"。有了 baseline，你才能证明后续迭代真的是改进。

---

## Step 2：建立 Eval Dataset

数据集是一组能代表生产流量的示例输入。每一条都是要被插入 prompt 模板的槽位。

课程用的三个问题：

- "What's 2+2?"
- "How do I make oatmeal?"
- "How far away is the Moon?"

实际工作中你可能有几十、几百甚至上千条记录。两种建法：
- 手工构造（高保真、低产能）；
- 用 Claude 自动生成（较低保真、高产能 — 见 Lesson 19）。

最重要的特性是数据集要**反映真实输入分布**，不能只有 happy path。

---

## Step 3：喂进 Claude

对每一条数据集输入，把它内插进模板，然后把完整 prompt 送给 Claude。以第一题为例：

```
Please answer the user's question:
What's 2+2?
```

Claude 会返回诸如"2 + 2 = 4"、煮燕麦片的步骤、月球距离等。这就是 grader 要评分的原始输出。

Lesson 20 会把这一步包进 `run_prompt(test_case)` 函数。

---

## Step 4：喂进 Grader

Grader 才是把这个循环从"意见"变成"工程流程"的关键组件。它检视原始输入和 Claude 的输出，吐出一个数值分数 — 课程用 **1 到 10 分**，10 代表完美答案。

课程示例分数：

| 测试案例 | Grader 分数 |
|----------|------------|
| 数学："What's 2+2?" | 10（完美） |
| 燕麦："How do I make oatmeal?" | 4（需要改进） |
| 月球："How far away is the Moon?" | 9（非常好） |

汇总分数：`(10 + 4 + 9) / 3 = 7.66`。

Grader 本身可以是 code-based（regex、JSON schema 检查）或 model-based（用另一个 LLM 来评分），后面章节会介绍。

---

## Step 5：改 Prompt 并重跑

有了 7.66 的 baseline，你改 prompt 的某部分然后重跑整条 pipeline。课程示范了一个简单改进 — 加一行指引：

```python
prompt = f"""
Please answer the user's question:

{question}

Answer the question with ample detail
"""
```

同一个数据集跑 v2 prompt，新的平均分变成 **8.7**。因为差异是数值，没得争 — v2 在这个数据集上客观优于 v1。

一直迭代直到分数进入平台期，或者"足够生产"为止。

---

## 为什么这个工作流很重要

这个流程提供三项 ad-hoc 测试做不到的能力：

1. **Prompt 版本的数值比较** — 你挑分数高的那个，不是感觉顺的那个。
2. **挑出最佳版本** — 你能把客观最高分的 prompt 上线，而不是某个运气好的。
3. **持续迭代** — 每次改动都对同一个数据集度量，形成 regression 安全网。

这个工作流"把 prompt engineering 的猜测成分移除"，让你有信心说改动真的是改进而不是另一种变体。

---

## 规模化考量（超出课程范围）

五步是最小集。真实生产 eval pipeline 还会再叠加：

- **版本化数据集** — 每次数据集修订都存 checkpoint，可以复现旧分数。
- **并行执行** — 上千条数据集受益于并发 API 调用。
- **CI 集成** — 每个改动 prompt 的 PR 都跑 pipeline，挡 regression。
- **多个 grader** — 单一分数会隐藏维度上的取舍；生产会用多个 rubric（正确性、格式、语气）。
- **分层采样** — 数据集内有加权桶，让稀有类别不会被常见类别淹没。

这些都不改变核心循环，只是把它在规模上 operationalize。

---

## 常见错误

1. **没有 baseline 分数** — 没 baseline 的迭代等于无法验证改动是否真的改进。
2. **数据集只有 happy path** — 数据集的意义是暴露失败模式，不是证明容易的题目可以过。
3. **凭眼睛看输出、跳过 grader** — 没有数值 scorer，"迭代"只是意见洗牌。
4. **同时改 prompt 和 dataset** — 你不会知道分数变动来自 prompt 还是 dataset。
5. **分数一升就停** — 第一个改进很少是最佳改进；持续迭代直到进入平台期。

---

> **Key Insight**
>
> 五步工作流的全部威力在于"数据集保持不变、只变 prompt"。这让 prompt 被隔离成自变量，分数的每次变动都能归因到 prompt。若在两次跑之间同时动了 dataset，你就摧毁了这个实验。CCA 考试里，draft → dataset → run → grade → iterate 这个顺序是 D3 最可测的序列。

---

## CCA 考试相关性

- **D3（Evaluation & Iteration）**：记住五步顺序；知道 baseline 是为了启用数值比较；理解 "feed through grader" 输出 1-10 分。
- **D5（Enterprise Deployment）**：认识到这个工作流就是生产就绪的闸门 — 没 eval 循环就不能部署。
- 考题触发词："用客观数据改进 prompt 的流程是什么" → 答案就是这个五步循环。

---

## Flashcards

| Front | Back |
|-------|------|
| 典型 eval 工作流的五个步骤是什么？ | 1) 起草 prompt、2) 建立 eval 数据集、3) 喂进 Claude、4) 喂进 grader、5) 改 prompt 并重复。 |
| 课程用的 grader 分数尺度是什么？ | 1 到 10 分，10 为完美答案，分数越低代表越需要改进。 |
| 课程用的 baseline prompt 是什么？ | `Please answer the user's question: {question}` 内插入 f-string。 |
| 课程如何示范迭代？ | 在 prompt 里加一句 "Answer the question with ample detail"，平均分从 7.66 升到 8.7。 |
| 为什么数据集要在迭代之间保持不变？ | 这样分数差异才能归因于 prompt 改动，而不是输入改动。 |
| Step 3 做什么？ | 把每条数据集输入内插进 prompt 模板并送进 Claude；完整响应成为 grading 的原料。 |
| 这个工作流解锁哪三个好处？ | 版本的数值比较、客观挑出最佳版本、可持续度量的迭代。 |
| 建数据集的两种方式？ | 手工构造，或用 Claude 自动生成（Lesson 19 会介绍）。 |
