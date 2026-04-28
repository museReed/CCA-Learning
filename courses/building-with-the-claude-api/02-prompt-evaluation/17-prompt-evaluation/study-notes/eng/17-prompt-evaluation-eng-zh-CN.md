# Prompt Evaluation — Engineering Deep Dive（简体中文）

| 项目 | 内容 |
|------|------|
| Exam Domain | D3 — Evaluation & Iteration（20%，主要）；D5 — Enterprise Deployment（20%，次要） |
| Task Statements | 3.1（eval 设计）、3.2（测试数据集）、3.3（eval 执行） |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 17 |

---

## 一句话摘要

Prompt engineering 教你"如何写"prompt；prompt evaluation 则是自动化度量手段，告诉你"这些 prompt 在真实输入分布下到底表现如何"。

---

## 两种不同的学科：工程 vs. 评估

使用 Claude 的工作可以清晰地分成两块。大多数初学者只掌握第一块就把东西推到生产环境，对 prompt 在真实流量下的表现毫无可见性。

| 学科 | 核心关注 | 产物 |
|------|----------|------|
| Prompt engineering | *如何*写出有效的 prompt | Multishot 示例、XML 标签、系统提示、结构化输出指令 |
| Prompt evaluation | Prompt *到底*表现多好 | 测试数据集、grader、数值分数、版本比较 |

Prompt engineering 是手艺；prompt evaluation 是闭合反馈循环的度量系统。

---

## 写完 Prompt 之后的三条路

写完第一版 prompt 后通常面临三个选择，但只有一个能扩展到生产环境。

**选项 1 — 测一次就上线。** 跑一两个输入看起来没问题就直接上线。风险：真实用户会立即送来你没测过的输入，prompt 悄无声息地崩掉。

**选项 2 — 测几次，零散地处理边角情况。** 比选项 1 好一点。你针对自己能想到的几个边角情况迭代。风险：人类的想象力代替不了真实的输入分布，用户还是会让你意外。

**选项 3 — 把 prompt 丢进 evaluation pipeline。** 建数据集，用客观 grader 打分，基于指标迭代。代价：前期工作量和 API 开销更大。收益：带着"度量出来的信心"而非"乐观"上线。

课程说得很直白：选项 3 是唯一能产出可靠 AI 应用的路径。选项 1 和 2 是"所有工程师都会掉进去的常见陷阱"。

---

## 为什么测试陷阱如此诱人

选项 1 和 2 感觉"很有生产力"，因为每一次 prompt 调整都会立刻让 Claude 在你刚跑的那个例子上输出更好的答案 — 立即的多巴胺反馈。但这种"轶事式验证"极具误导性。生产流量有两个手动测试无法重现的特性：

1. **量** — 真实用户每天生成数千条输入，分布的尾部正是 prompt 崩溃的地方。
2. **不可预测性** — 用户会用开发者从未想过的方式提问、注入边角情况、串联上下文。

一个在三个手挑输入上看起来"还不错"的 prompt，在生产环境可能有 30% 的失败率，而你只会从一堆愤怒的客服工单里得知这件事。

---

## Evaluation-First 的方法论

系统化的替代方案是：在打磨 prompt 之前先投资一条 evaluation pipeline。回报是四项具体能力：

- **在生产之前发现弱点** — 失败案例出现在你的笔记本上，而不是客户工单里。
- **客观比较 prompt 版本** — 两个 prompt 产出两个数字，你选分数高的那个，没有争论空间。
- **带信心迭代** — 每次改动都对数据集验证，你知道这是真正的改进而不是运气。
- **建造可靠的应用** — 质量成为系统的可度量属性，不再靠感觉。

代价是前期要花力气搭建 eval harness，但这会复利累积：未来每一次 prompt 改动都走同一条 pipeline，边际成本几乎为零。

---

## 在 CCA 课纲中的位置

Prompt evaluation 正好落在两个 domain 的交界：

- **D3 Evaluation & Iteration（20%）** — 本节课定义了这门学科本身：度量、数据集驱动的迭代、客观比较。
- **D5 Enterprise Deployment（20%）** — Eval 是生产发布前的质量闸门。没有 eval pipeline 的 LLM 功能不应上线。

后面几节课把这个流程 operationalize：18 讲典型工作流、19 讲数据集生成、20 搭建 eval runner、21–22 讲 model-based 与 code-based grading。

---

## 常见错误

1. **把 prompt engineering 和 prompt evaluation 混为一谈** — 以为只靠写 prompt 的技巧就够，没有度量层。
2. **只在一个 happy-path 例子上测试** — 掉进选项 1 然后宣告完工。
3. **相信自己手挑的边角情况涵盖真实使用** — 选项 2 给你假信心，因为开发者的想象力不是生产流量的随机抽样。
4. **因为"太贵"而跳过 eval** — Prompt 在生产崩溃的代价（客服负担、品牌损伤、流失）远远超过跑一次 eval 的开销。
5. **把 eval 分数当成最终答案而非反馈信号** — 目标是迭代，不是一次性的数字。

---

> **Key Insight**
>
> Prompt evaluation 是把 prompt engineering 从手艺变成工程学科的关键。没有 eval，每次改 prompt 都是猜测；有了 eval，每次改 prompt 都是可度量的改进。CCA 考试中凡是提到 "reliability"、"iteration"、"version comparison" 的题目都指向 D3，答案永远是：把 prompt 跑进 eval pipeline。

---

## CCA 考试相关性

- **D3（Evaluation & Iteration）**：要能区分 prompt engineering 与 prompt evaluation；要能辨认三条路并理解为什么选项 3 才正确。
- **D5（Enterprise Deployment）**：Eval 是生产就绪的前提条件；要能说明为什么 ad-hoc 测试不够。
- 考题关键词："reliable"、"measure"、"objective"、"iterate"、"compare versions" → 答案是 eval pipeline，而不是再多调几次 prompt。

---

## Flashcards

| Front | Back |
|-------|------|
| Prompt engineering 和 prompt evaluation 有什么区别？ | Prompt engineering 是写有效 prompt 的技巧集合；prompt evaluation 是自动化度量 prompt 表现的方法。 |
| 写完 prompt 之后有哪三条路？ | 1) 测一次就上线、2) 测几次补边角情况、3) 跑进 eval pipeline 并基于客观指标迭代。 |
| 为什么选项 1 和 2 在生产会失败？ | 真实用户会送来开发者从未想过的输入；手动测试无法重现生产的量和不可预测性。 |
| 选项 3 的成本和收益？ | 前期工作量和 API 开销较高，但能产出可度量的信心，在部署前抓出失败案例。 |
| Evaluation-first 解锁哪四项能力？ | 提前识别弱点、客观比较版本、带信心迭代、建造可靠应用。 |
| Prompt evaluation 主要对应哪个 CCA domain？ | D3 — Evaluation & Iteration（20%）。 |
| 课程中提到 prompt engineering 包含哪些技巧？ | Multishot prompting、XML 标签结构化，以及其他 best practices。 |
| 考题看到 "reliability" 要怎么答？ | 要保证 prompt 可靠，答案是 evaluation pipeline，而不是更多 prompt 调整。 |
