# Prompt Engineering — PM 视角

| 项目 | 内容 |
|------|------|
| 考试领域 | D3 — Evaluation & Iteration (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 3.1（prompt 设计与迭代）、1.1（指令遵循） |
| 来源 | building-with-the-claude-api / 03-prompt-engineering / Lesson 25 |

---

## 一句话总结

Prompt engineering 是有计分板的产品迭代——建 baseline、打分、改一件事、再打分——让每次发版都靠数据，不是靠感觉。

---

## PM 为什么该在乎

大多数 AI 功能上线后就把 prompt 丢着不再度量。这等同于你上线一个 landing page 却从来不看转化率。这堂课把 prompt 视为**一个值得自己的 CI、自己的 regression test、自己的 KPI 的产品工件**——evaluator 字面上就是一个 10 分制的分数。

没有 eval loop 会发生：

- **漂移**——模型升级悄悄让输出质量退步。
- **各说各话**——RD 说「有用」，客服说「用户在抱怨」，没人指得出一个数字。
- **不敢动**——没人敢碰 prompt，因为没人能证明改动是安全的。

有了 eval loop，prompt 改动就跟其他产品改动一样：看得到 delta、胜的就上、退步就 roll back。

---

## 心智模型：健身追踪器

把 prompt engineering 当成用健身追踪器训练：

| 活动 | 没追踪器 | 有追踪器 |
|------|----------|----------|
| 开始新计划 | 「感觉有变强」 | Baseline 卧推 = 60 kg |
| 试新技巧 | 「比较累应该有用」 | 技巧 A → 62 kg (+2) |
| 再试另一招 | 「刚刚哪一招比较好？」 | 技巧 B → 70 kg (+10)，采用 |

Evaluator 就是追踪器，prompt 是训练计划，各种技巧是不同运动。你只有在每次单独量体重后才知道哪个动作真的有效。

---

## 五步骤循环（翻译成 PM 语言）

| 步骤 | 做什么 | PM 翻译 |
|------|--------|---------|
| 1 | 设目标 | 「好」长什么样？定 acceptance criteria。 |
| 2 | 写初版 prompt | 就算知道很烂也先出 v0。 |
| 3 | 评估 | 跑测试、拿一个分数。 |
| 4 | 套用一个技巧 | 只改一件事。一件。 |
| 5 | 重新评估 | 分数上去？留下。下去？回滚。 |

这就是 Lean Startup 的 build-measure-learn 套用在 prompt 粒度上。

---

## 产品应用场景

### 什么时候值得建 eval loop

| 场景 | 为什么重要 |
|------|------------|
| 质量主观的用户功能（摘要、推荐） | 人对「质量」看法不同，你需要共同计分板 |
| 受监管或高风险领域（医疗、金融、法务） | 必须能证明 prompt 行为一致 |
| 会被多位工程师在几个月内修改的 prompt | Regression safety，改动得可证明无害 |
| 喂给下游 pipeline 的 prompt（prompt → tool call → DB 写入） | 上游质量退步在没有分数时很难察觉 |

### 什么时候是 overkill

| 场景 | 更好的做法 |
|------|------------|
| 一次性内部脚本 | 手动 spot-check 就好 |
| PMF 前的丢弃型 prototype | 优先迭代速度，不是 prompt 质量 |
| 只上给五个内部用户的 prompt | 用户本身就是 eval |

---

## 计分板思维

课程给了具体数字：baseline 2.3/10 很正常。PM 该内化几个锚点：

| 分数 (/10) | 代表什么 | 可以发吗 |
|-----------|----------|----------|
| 2-3 | 初版 baseline | 绝对不行 |
| 5-6 | 套了 clarity + specificity | 内部试吃 |
| 7-8 | 加了 examples + 结构 | Beta |
| 9+ | Edge case 都硬化了 | 正式上 |

这是有立场的——课程示范 2.3 → 3.92 → 7.86 连跳两个技巧。PM 的重点是：**把分数门槛绑到每个发版 gate**，不是模糊的「看起来 OK」。

---

## PM 决策框架

准备发 AI 功能时问：

| 问题 | 如果是，你需要 |
|------|---------------|
| 这个 prompt 上线后会被改超过一次吗？ | Eval loop + regression tracking |
| 不同利害关系人对质量有分歧吗？ | 用 `extra_criteria` 把 rubric 写死 |
| 质量是主观的（tone、格式、完整度）吗？ | Model-graded evaluator，不是只跑 unit test |
| 未来模型升级会影响这个功能吗？ | 固定 baseline 分数，让升级自己证明 |
| 我们在乎 p95 质量还是只在乎平均值？ | 最终验证跑大一点的数据集 |

---

## 常见 PM 错误

1. **「在我的示例上有用」** — 一个 happy path 不是 eval，那是 demo。
2. **跳过 baseline** — 上线时就用一个「好」prompt，结果你永远无法证明下一版更好。
3. **改动 rubric** — 在迭代中途改 `extra_criteria`，前后分数失去可比性。Rubric 冻结、迭代 prompt。
4. **太早投资** — 还没发 baseline 就去盖 500 case 的 eval harness 是烧 runway。先从 2-3 case 开始。
5. **只看分数不看报告** — PM 只盯数字就错过 grader 的推理，那才是产品洞察的来源。

> **Key Insight**
>
> Prompt engineering 把一个主观的产品工件变成可度量的。对 PM 来说这就是「靠感觉发版」和「靠数据发版」的差距。一旦有分数，你就能拥有它、保卫它、回滚退步、推动改进——这会把 AI 功能从魔法变成工程。

---

## CCA 考试相关性

- **D3 (Evaluation & Iteration)**：要认得出 eval-driven loop 是「怎么改善一个 prompt？」的标准答案。
- **D1 (Agentic Architecture)**：同一套 loop 也用来调 agent system prompt。题目可能把 agent 行为错误包装成 prompt 调校问题。
- 题目会问：「团队 prompt 得 2.3/10，下一步？」答案永远是「套一个技巧再评估」，不是「重写」。
- 要知道迭代早期用小数据集（2-3 case）是故意设计，不是缺陷。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 这堂课 prompt engineering 的核心概念？ | 可迭代的 loop：baseline → 评估 → 套技巧 → 重新评估。可度量，不是靠感觉。 |
| PM 为什么要帮每次 prompt 发版绑分数？ | 没分数就不知道改动是进步还是退步，分数把 prompt 变成可管理的产品工件。 |
| 典型 baseline 分数是多少？PM 该怎么反应？ | 约 2.3/10，把它当起点不是警报。 |
| 为什么每次迭代只套一个技巧？ | 才能归因分数变化，建立可靠的未来 playbook。 |
| `extra_criteria` 翻译成 PM 语言？ | Rubric，grader 要评分的必备项清单，是把业务需求编码进 eval 的方式。 |
| 「健身追踪器」类比是什么？ | Evaluator 是体重计/追踪器，prompt 是训练计划，每个技巧是一个动作，每次单独量。 |
| 什么时候建 eval loop 是 overkill？ | 一次性脚本、PMF 前 prototype、只上给少数内部用户的 prompt。 |
| 这堂课支持什么样的发版 gate 模式？ | 把每个发版阶段（内部、beta、GA）绑到最低分数门槛。 |
