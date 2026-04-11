# Being Specific — 工程深度解析

| 项目 | 内容 |
|------|------|
| 考试领域 | D3 — Evaluation & Iteration (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 3.1（prompt 设计与迭代）、1.1（指令遵循） |
| 来源 | building-with-the-claude-api / 03-prompt-engineering / Lesson 27 |

---

## 一句话总结

Specificity 在收束 Claude 的 search space——output guidelines 锁定「结果长什么样」，process steps 锁定「Claude 该怎么想」。

---

## 核心问题：没有边界的诠释空间

Clear and direct 本身还不够。例如「Write a short story about a character who discovers a hidden talent.」这个 prompt 清楚、直接、是祈使句——但 Claude 还是可以自由选：

- 长度（200 字或 2,000 字）
- 角色数量（一人或五人）
- 类型和场景
- 「hidden talent」是哪个、怎么揭露

每一个自由轴都是 output 可能在跑多次时漂移的轴。Specificity 就是把这些轴关起来的方法。

---

## 两种 Specificity

课程点出两个互补的杠杆。实务 prompt 通常会同时用。

### 1. Output Quality Guidelines

一个列表，列出 output 必须具备的质量。这在控制 artifact 本身：

- **长度**
- **结构**和 format
- **必须包含的具体属性或元素**
- **Tone** 或 style 要求

以短篇小说为例：「1,000 字以内、包含一个揭露才能的清楚动作、至少一个配角」。每一条都收掉一个自由轴。

### 2. Process Steps

给 Claude 在产出最终答案前要跑的动作序列。这在控制 reasoning path：

1. 头脑风暴三个会制造戏剧张力的才能。
2. 选最有趣的那个。
3. 勾勒出揭露才能的关键场景。
4. 头脑风暴能放大冲击的配角类型。

Process steps 在任务受益于「先多角度思考再下笔」的情境特别有用，而不是一次到底生出答案。

---

## 贯穿示例：餐单 Guidelines

叠加在 Lesson 26 的 clear+direct prompt 上，课程示范的 output guidelines：

```
Guidelines:
1. Include accurate daily calorie amount
2. Show protein, fat, and carb amounts
3. Specify when to eat each meal
4. Use only foods that fit restrictions
5. List all portion sizes in grams
6. Keep budget-friendly if mentioned
```

每一条都可测。每一条都关掉前一版 prompt 没关的质量自由轴。

---

## 度量结果

课程给了迭代 prompt 的 evaluator 分数：

| 版本 | 分数 (/10) |
|------|-----------|
| Baseline（「What should this person eat?」） | 2.32 |
| Clear and direct（「Generate a one-day meal plan...」） | 3.92 |
| **+ Specificity guidelines** | **7.86** |

加上 specificity **让分数翻倍**——从 3.92 到 7.86，比 clarity/directness 的进步还大，也是课程把 specificity 列为「几乎每次都要用」的原因。

---

## 何时用哪一招

| 技巧 | 什么时候用 |
|------|-----------|
| **Output Quality Guidelines** | 几乎每个 prompt。这是你保持一致性的安全网。 |
| **Process Steps** | 复杂问题——troubleshooting、决策、critical thinking，或任何你希望 Claude 在答前多角度思考的任务。 |

课程对 process steps 的示例：要 Claude 分析为什么一个业务团队业绩下滑。没有 process steps，Claude 可能会 fix 在某一个原因。用 process steps 引导它走过市场指标 → 行业变化 → 个人绩效 → 组织变动 → 客户反馈，分析变得周延而平衡。

---

## 同时用两招

Professional prompt 通常两个杠杆一起上：

- **Process steps** 放在上面，告诉 Claude 怎么想。
- **Output guidelines** 放在下面，告诉 Claude 最终 artifact 必须含什么。

这个组合同时给你 output 的一致性和 Claude 考虑过所有重要因素的信心。

---

## 为什么 Specificity 是复利

Guidelines 里每一条都像是 output 的一个 unit test。Grader（不管是人还是 model-based evaluator）可以独立检查每一项，这正是你的 eval `extra_criteria` 打分的方式。Prompt 的 guidelines 越对齐 evaluator 的 rubric，每次 eval 迭代就越能直接转换成 prompt 改进。

所以资深 prompt engineer 常同时写 rubric 和 guidelines——它们是同一份合约的两个视图。

---

## 常见错误

1. **停在 clear + direct** — 留给 Claude 自己猜长度、结构、要含的元素，把 eval 分数上限压低。
2. **Specify 太少、太模糊** — 「include details」不是 guideline，「list all portion sizes in grams」才是。
3. **在琐碎任务上用 process steps** — 简单抽取或格式化用 steps 只是增加延迟、没有质量收获。
4. **Prompt guidelines 和 eval rubric 对不上** — prompt 要 X，evaluator 打 Y 的分。要对齐。
5. **Process steps 堆太多** — 超过约 5 步 Claude 可能会 drop 或 merge 步骤。保持 process sequence 聚焦。

> **Key Insight**
>
> Specificity 是课程 playbook 里单点影响最大的技巧——把 eval 分数从 3.92 翻倍到 7.86。Guidelines 每一条都关掉一个 output 漂移轴，每关掉一个轴 prompt 就可度量地更可靠。Output guidelines 几乎该出现在每个 prompt；process steps 在任务需要多角度推理时加入。

---

## CCA 考试相关性

- **D3 (Evaluation & Iteration)**：要认得 specificity 是 clarity/directness 之后最高杠杆的技巧，要知道两个变体（output guidelines vs process steps）。
- **D1 (Agentic Architecture)**：agent system prompt 同样靠这两个杠杆——guidelines 约束 output，process steps 约束 reasoning。
- 考题会问「哪种任务该用哪招」。「多角度分析」→ process steps。「一致的 artifact format」→ output guidelines。「两者都要」→ 组合。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Specificity 两种 guidelines 是什么？ | Output quality guidelines（结果该长什么样）和 process steps（Claude 该怎么思考）。 |
| Output quality guidelines 控制什么？ | 长度、结构、格式、必须包含的属性/元素、tone 或 style。 |
| 什么时候用 process steps？ | 复杂问题——troubleshooting、决策、critical thinking，或任何该在答前多角度考量的任务。 |
| 餐单示例中 specificity 带来的分数进步？ | 3.92 → 7.86，光加具体 guidelines 就让分数翻倍。 |
| Output guidelines 该每个 prompt 都加吗？ | 几乎是——课程把它称为一致性的「safety net」。 |
| 课程的 process steps 示例序列？ | 1) 头脑风暴三个制造张力的才能 2) 选最有趣 3) 勾勒关键场景 4) 头脑风暴配角类型。 |
| Prompt guidelines 和 evaluator rubric 没对齐会怎样？ | 分数无法反映 prompt 真正在最优化什么——两者必须保持对齐。 |
| 两招一起用的 professional pattern？ | Process steps 放上面（怎么想），output guidelines 放下面（最终 artifact 该含什么）。 |
