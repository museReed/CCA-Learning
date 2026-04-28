# Being Specific — PM 视角

| 项目 | 内容 |
|------|------|
| 考试领域 | D3 — Evaluation & Iteration (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 3.1（prompt 设计与迭代）、1.1（指令遵循） |
| 来源 | building-with-the-claude-api / 03-prompt-engineering / Lesson 27 |

---

## 一句话总结

Specificity 就是一份 acceptance criteria——一条条告诉 Claude「done」长什么样，把模糊要求变成可测试的合约。

---

## PM 为什么该在乎

每个 PM 都写过模糊的 ticket、然后看着它被做错——不是工程师烂，是「done」没定义。Prompt 的失败方式一样。没有 specificity 的 prompt 就像没有 acceptance criteria 的 feature ticket——你会拿到「某个东西」，但你无法预测是什么，也无法证明它是对的。

课程量到的影响非常明显：在 clear+direct prompt 上加一份 specificity 列表，eval 分数从 **3.92 跳到 7.86**——一次编辑让质量翻倍有余。这是整章 prompt engineering 里最大的单点质量跳升。对 PM 来说，这是最高 ROI 的杠杆。

---

## 心智模型：Acceptance Criteria

| PM 产物 | Prompt 对应 |
|---------|-------------|
| User story | 第一行 clear+direct |
| Acceptance criteria | Output quality guidelines |
| Test plan / checklist | Eval rubric（`extra_criteria`） |
| Process doc / SOP | Process steps |

当你读课程的餐单 guidelines（「包含准确的每日卡路里、蛋白质/脂肪/碳水量、指定用餐时间……」），你读的就是一个 AI 功能的 acceptance criteria。每一条都可测，每一条都关掉一个模糊来源。

---

## 两个杠杆

### Output Quality Guidelines — 「做什么」

告诉 Claude 完成的 artifact 必须含什么：

- 长度
- 结构和 format
- 具体元素或属性
- Tone 或 style

课程建议**几乎每个 prompt 都要用**。这是一致性的 safety net。

### Process Steps — 「怎么做」

告诉 Claude 答前该怎么想：

1. 头脑风暴选项
2. 选最好的
3. 勾勒细节
4. 考虑支援因素

当任务复杂到 Claude 可能只 fix 在一个角度，而你希望它考虑多个角度时使用。课程的经典示例是「分析为什么业务团队业绩下滑」——跳到单一原因会给出肤浅答案的任务。

---

## 产品应用场景

### 一定要加 Output Guidelines

| 功能 | Guidelines 示例 |
|------|----------------|
| 会议摘要器 | 「包含与会者、决议、action item 和负责人、下次会议时间，200 字内。」 |
| Support ticket 分类器 | 「只回：category（billing/bug/feature/other 择一）、priority（P0-P3）、一句话摘要。」 |
| 周报生成器 | 「包含 2 句 intro、3 则精选故事、一个数据表、一个 CTA 链接。上限 400 字。」 |

### 多角度分析时加 Process Steps

| 功能 | Process Steps 示例 |
|------|-------------------|
| Root-cause 分析助理 | 「1) 列可能原因 2) 依可能性排序 3) 指出每个要验证的资料 4) 提出前 2 个假设」 |
| Design critique 工具 | 「1) 识别主要用户目标 2) 对照评估 3) 记优点 4) 记缺点 5) 提一个改进」 |
| Sales ops 的 deal review | 「1) 检查 pipeline stage 2) 看近期活动 3) 标风险信号 4) 推荐下一步」 |

### 不要过度工程

简单抽取或格式化（「抽签名档里的 email」）不需要 process steps。加了只是增加延迟、没有质量收获。

---

## PM 决策框架

设计 AI 功能的 prompt 时问：

| 问题 | 动作 |
|------|------|
| 我能列出 output 必含的明确元素吗？ | 写 output guidelines 编号列表 |
| 有「正确答案」是需要考虑多因素的吗？ | 加 process steps |
| Claude 有可能忽略某个重要角度吗？ | 为那个角度加一个 process step |
| Eval rubric 能独立评分每个 guideline 吗？ | 能——保持 guidelines 和 rubric 对齐 |
| 所有 guidelines 都可测吗？ | 把模糊的换成可度量的 |

如果 PM 写不出一个功能的 acceptance criteria，prompt 就会失败。列 output guidelines 的练习常常会揭露 PRD 的漏洞。

---

## 复利效应

Specificity 有两层回报：

1. **直接** — eval 分数上升，因为 output 更贴近你要的。
2. **间接** — 因为每个 bullet 可测，你的 eval rubric 可以更紧，未来迭代改进更快。

这和强 PRD 的复利一样：清楚的 acceptance criteria 让 QA 更快、bug 更具体、regression 更容易预防。Prompt 也受益于同样的纪律。

---

## 常见 PM 错误

1. **模糊质量 bullet** — 「should be professional」不是 guideline，「avoid contractions, use third-person voice, max 300 words」才是。
2. **以为 clear+direct「有用」就跳过 specificity** — 3.92/10 不是可发版的质量。Specificity 才是把你推到 7.86+ 的杠杆。
3. **混淆 process steps 和 output structure** — process steps 控制*Claude 怎么想*，不是*答案怎么格式化*。是分开的杠杆。
4. **把所有东西塞进一条 bullet** — 每个 guideline 该可独立测试。过载 bullet 要拆。
5. **Guidelines 和 eval rubric 不对齐** — prompt 要 X、rubric 评 Y，你永远无法可靠地发改进版本。

> **Key Insight**
>
> Specificity 是 prompt engineering 从「选字游戏」变成 **产品规格写作** 的分水岭。Output guidelines 是 acceptance criteria，process steps 是 SOP，合起来把 prompt 从请求变成合约。课程的 3.92 → 7.86 跳升是整章最强的证据：这是 PM 在 AI 功能上能做的最高 ROI 动作。

---

## CCA 考试相关性

- **D3 (Evaluation & Iteration)**：要认得 specificity 是 clarity/directness 之后最高杠杆的技巧，并区分 output guidelines 和 process steps。
- **D1 (Agentic Architecture)**：agent system prompt 同样用这两个杠杆控制 agent 产什么、怎么想。
- 考题可能描述一个缺其中一个杠杆的 prompt，要你补。线索：「格式不一致」→ output guidelines；「跳到结论」→ process steps。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Specificity output guidelines 最直接对应哪个 PM 产物？ | Acceptance criteria——一份可测的 bullet list 描述「done」长什么样。 |
| 课程量到 specificity 带来的分数变化？ | 3.92 → 7.86，加 output guidelines 让 eval 分数翻倍有余。 |
| PM 什么时候该用 process steps 而不只是 output guidelines？ | 任务需要多角度考量时，如 root-cause 分析或决策——Claude 可能会 fix 在单一原因。 |
| 好的 output guideline 的检验？ | 每个 bullet 都能被 eval rubric 独立测试；「be professional」这类模糊 bullet 过不了关。 |
| Output guidelines 该出现在几乎每个 prompt 吗？ | 是——课程称它为一致性的「safety net」，该是默认而不是最优化。 |
| Deal-review 功能的 process step 序列示例？ | 1) 检查 pipeline stage 2) 看近期活动 3) 标风险信号 4) 推荐下一步。 |
| Guidelines 和 eval rubric 不对齐会怎样？ | 分数无法反映 prompt 在最优化什么，迭代无法转换成可发版的改进。 |
| Specificity 的两层复利？ | 直接（output 更贴近 spec、分数上升）和间接（更紧的 rubric 让未来迭代更快）。 |
