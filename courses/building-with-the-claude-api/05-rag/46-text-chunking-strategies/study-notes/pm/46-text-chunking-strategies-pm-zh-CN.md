# Text Chunking Strategies — PM 视角

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Architecture (22%) 主要；D4 — Safety & Alignment (20%) 次要 |
| Task Statements | 1.3（context management）、4.1（grounded responses） |
| 来源 | building-with-the-claude-api / 05-rag / Lesson 46 |

---

## 一句话总结

Chunking 是每个 RAG 功能看不见的产品质量旋钮 — 它决定「一个知识单位」长什么样子，做错了 AI 就会很有信心地引用错段落。

---

## 心智模型：在晚宴切蛋糕

想象一个多层蛋糕。客人点「巧克力那层」或「草莓那层」。怎么切很重要：

| 切法 | 每个客人拿到 | Chunking 策略 |
|------|--------------|---------------|
| 随机 5 公分立方块 | 有时纯巧克力，有时一半巧克力一半草莓 | Size-based、无 overlap |
| 同样的立方块，但沾到下一块的边 | 一样，但看得到旁边是什么层 | Size-based + overlap |
| 干净的水平切片，一层一片 | 他们点的那层，刚刚好 | Structure-based |
| 厨师按风味挑选分组 | 最小份量的纯风味 | Semantic |

切得随便，就会吃到跨层的那一口。点草莓的客人咬到一大块巧克力也不知道为什么。**这就是用户在 RAG 功能里遇到烂 chunking 的感觉**。

---

## 为什么这是 PM 问题（不只是工程问题）

Chunking 决策直接驱动用户看得到的行为：

- **「AI 给我不相关的答案」** → 通常是 chunking 烂
- **「AI 在 citation 里切在句子中间」** → 一定是 chunking 烂
- **「AI 用我没问的 section 回答」** → 本 lesson 经典的「bug」例子
- **「文档更新后答案没跟上」** → re-chunking pipeline 坏了

PM 如果觉得 chunking 是「工程搞定的事」，就会是 CEO demo 功能结果拿到错答案时那个道歉的人。

---

## 四种策略的 PM 白话

| 策略 | PM 白话 | 何时用 |
|------|---------|--------|
| **Size-based** | 「每 500 字切一次，加 overlap」 | 混合内容的默认 — 便宜、可靠、可预期 |
| **Structure-based** | 「按 Markdown header 切」 | 你控制内容格式时（内部文档、模板化报告） |
| **Sentence-based** | 「每 5 个句子一组」 | 散文为主的内容，句子是有意义的单位 |
| **Semantic** | 「用 NLP 把相关想法留在一起」 | 高风险 retrieval（法律、医疗）值得花 compute 时 |

PM 要内化的一件事：**没有哪个是通用「最佳」**。对的策略看内容类型、质量标准、工程预算。

---

## 「bug」例子 — 每个 PM 都该知道

Lesson 用一个很鲜明的例子：一份文档有医疗研究和软件工程两个 section。医疗 section 刚好写「XDR-47, a bug we have not seen before」。用户问「How many bugs did engineers fix this year?」。

烂的 chunker 可能因为有「bug」这个字就把医疗 chunk 捞出来。Claude 接着写一段流畅的关于病毒的答案 — 错的 section、错的领域、错的答案，但语气很有信心。

这就是**默默失败** pattern。没有错误消息。log 看起来健康。只有用户自己 QA 答案时才会发现。对 PM 而言，这种 bug 到第十次就会毁掉用户信任。

---

## 产品用例

### 何时用 Structure-Based

| 信号 | 理由 |
|------|------|
| 内容是 Markdown | header 是可靠边界 |
| 你拥有撰写模板（内部 wiki、PRD 模板） | 可以强制结构 |
| 每个 section 语义大致一致 | 语义对齐免费附送 |

### 何时用 Size-Based + Overlap

| 信号 | 理由 |
|------|------|
| 你无法保证文档结构 | fallback 必须什么都能处理 |
| 内容混杂（docs + PDF + code + log） | 一个策略搞定全部 |
| 你在出 MVP 想要可预期的行为 | 最好推理 |

### 何时用 Sentence-Based

| 信号 | 理由 |
|------|------|
| 内容是散文、没结构 | 句子是自然单位 |
| 你要人类可读的 citation | citation 框里切掉的字看起来很坏 |

### 何时用 Semantic

| 信号 | 理由 |
|------|------|
| 领域高风险（法律、医疗、金融） | retrieval 错有实际后果 |
| retrieval 是验证过的产品瓶颈 | 有数据显示 chunk 质量重要 |
| 你有 compute 预算 | 预处理比较重 |

---

## PM 决策框架

规划 RAG 功能时，签核前回答这些：

| 问题 | 为什么重要 |
|------|------------|
| 我们的 canonical 内容格式是什么？ | 决定 structure-based 是否可行 |
| chunk 大小预算是多少？ | 直接关联 prompt 大小、成本、延迟 |
| 谁负责 chunk 质量 eval？ | 必须有具名 owner，不是「工程大家都负责」 |
| 用户怎么看到 citation？ | 如果 citation 可见，切掉的 chunk 看起来坏了 |
| 文档变更时怎么 re-chunk？ | 每次内容更新都有预处理成本 |

---

## 常见 PM 错误

1. **把 chunking 当工程实现细节** — 它是产品杠杆；chunk 大小直接影响用户看到的内容。
2. **没有 chunk 质量 eval** — 没 test set 就交付，代表你从愤怒用户那学到 chunking 烂。
3. **以为一个策略适合所有内容类型** — 有 docs、PDF、code 的平台需要不只一个 chunker。
4. **忽略 re-indexing 故事** — 每次内容更新都触发预处理；pipeline 脆弱的话，你的「AI 回答」功能会默默 stale。
5. **citation 不可审计** — 没有可见的来源链接，用户抓不到默默失败，信任崩塌。

> **关键洞察**
>
> Chunking 是 retrieval 的默默兄弟。当有人说「我们 RAG 系统答错了」，大约一半情况的 root cause 是 chunking — 好 chunk 根本没被产生，所以好 retrieval 不可能发生。对 PM 而言这代表 chunk 质量 day one 就是 eval target，不是「之后再迭代」的东西。

---

## CCA 考试关联

- **D1（Agentic Architecture）**：熟悉四种策略、取舍、情境题准备好（「Markdown 有保证 header → ？」、「PDF 混杂 → ？」）。
- **D4（Safety & Alignment）**：「bug」例子直接对应幻觉风险 — 错 chunk 导致很有信心的错答案。
- 注意考题环绕「overlap」的写法 — 问「怎么避免 chunk 被切在句子中间」答案永远是 overlap。

---

## Flashcards

| Front | Back |
|-------|------|
| PM 为什么要关心 chunking？ | 它是默默驱动产品质量的元素 — 烂 chunking 导致很有信心的错答案，用户无法 debug。 |
| 「bug」例子在教什么？ | 同一个关键词可以出现在不相关领域（医疗 vs. 软件），产生错但流畅的答案。 |
| 切蛋糕的类比是什么？ | 糟糕切法会跨层，让客人咬到错的口味 — 烂 chunking 跨主题边界。 |
| PM 何时选 structure-based chunking？ | 你控制内容格式时（Markdown、模板化报告），header 是可靠边界。 |
| 默认 fallback chunking 策略？ | Size-based + overlap — 适用任何内容类型、行为可预期。 |
| 为什么 chunk overlap 对用户看到的 citation 很重要？ | 没有 overlap，chunk 会切在句子中间，citation 看起来坏了。 |
| 谁该负责 chunk 质量 eval？ | 具名 PM／工程搭档 — 不是「工程大家」；这是产品指标。 |
| 烂 chunking 的默默失败模式是什么？ | 没错误、log 健康、用户拿到根据不相关 chunk 产出的自信错答案。 |
