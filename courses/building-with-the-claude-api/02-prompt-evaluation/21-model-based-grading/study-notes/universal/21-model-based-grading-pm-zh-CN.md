# 模型评分 Model-Based Grading — PM 视角

| 项目 | 说明 |
|------|------|
| 考试领域 | D3 — Evaluation（20%）主要；D5 — Enterprise Deployment（20%）次要 |
| 任务声明 | 3.4（LLM-as-judge 评分）、3.3（测试案例执行）、5.4（eval 驱动迭代） |
| 来源 | building-with-the-claude-api / 02-prompt-evaluation / Lesson 21 |

---

## 一句话重点

Model-based grading 就是把"这个 AI 输出感觉不错吗？"变成 dashboard 上的一个数字 —— 让 prompt engineering 不再靠 vibes，而是变成可衡量的产品 workflow。

---

## 为什么 PM 要在意

没有评分 eval，每次改 prompt 都是信仰之跃。有人动一下 system prompt、看十笔输出、就上线。下列基本问题根本答不出来：

- 这周的 prompt 改动到底有没有提升 helpfulness？
- 新指令是不是搞坏了 completeness？
- 我们是不是在不知情的情况下退化了 safety？

Model-based grading 给你**每个 prompt 版本的质量指标** —— 一个可以像 DAU 或 conversion rate 一样随时间绘制的数字。它把 prompt engineering 从手艺变成工程。

---

## 心智模型：餐厅评论家

把三种 grader 想成三种餐厅评论系统：

| Grader 类型 | 餐厅比喻 | 优点 | 缺点 |
|-------------|----------|------|------|
| **Code grader** | 带检查表的卫生稽查员 | 快、便宜、100% 一致 | 只能检查规则、不能判断味道 |
| **Model grader** | 用 email 写评论的 freelance 美食评论家 | 能判断味道、可便宜扩展 | 每次造访意见略有不同 |
| **Human grader** | 亲自到场的米其林密探 | 最深入、最细腻 | 慢又贵 |

真正的连锁餐厅三种都用。PM 在打造 AI 功能时也该如此：code graders 做规则遵守、model graders 做体验质量、high stakes（安全、法务、品牌）时用 human graders。

---

## 产品使用场景

### 何时用 Model Graders

| 场景 | 为什么 model grader 适合 |
|------|-------------------------|
| "这个客服响应有没有帮上忙？" | Helpfulness 是代码无法判断的主观题 |
| "AI 有没有照我们的指令做？" | 指令遵循是语义层面的问题 |
| "这个摘要完整吗？" | Completeness 取决于意义，不是字数 |
| "这个响应感觉安全、符合品牌吗？" | 语气与安全需要 model 的判断 |

### 何时**不要**用 Model Graders

| 场景 | 更好的替代 |
|------|-----------|
| "输出是不是合法的 JSON？" | 用 code grader —— deterministic 且免费 |
| "响应是不是 200 字以内？" | 用 code grader —— 很琐碎 |
| "答案是不是跟已知正解相符？" | 用 code grader 做字符串比对 |
| "这个有没有违反我们最敏感的政策？" | 棘手 case 走 human graders |

---

## 每个 PM 该争取的那一招

来源的 grader prompt 依序要求 model 返回四件事：

1. Strengths（1-3 项）
2. Weaknesses（1-3 项）
3. Reasoning（简短解释）
4. Score（1-10）

这是**整课最重要的设计决策**。来源指出：没有 strengths 和 weaknesses，model graders 都会打 6 分 —— 追踪改善完全没用。

PM 应该坚持保留这个结构，即使工程端压力要求"简化 grader"。strengths 和 weaknesses 也直接可用作 PM 的产物：变成 prompt 修改 backlog，reasoning 也让 CS 和 QA 在退化时能追溯原因。

---

## PM 决策框架

当团队提议加 model-based grading，请问：

| 问题 | 若答 Yes | 行动 |
|------|---------|------|
| 我们有写下清楚的评分标准吗？ | Yes | 继续 —— grader 需要先有标准 |
| 要衡量的质量维度是主观的（helpfulness、completeness）？ | Yes | Model grader 是对的选择 |
| 要衡量的质量维度是 deterministic（valid JSON、长度）？ | Yes | 改用 code grader |
| 我们在乎**绝对**分数吗？ | No | 很好 —— 信 delta，不信绝对数字 |
| reasoning 字段有 log 而且可 review？ | Yes | 继续 —— 这是评分可追溯的关键 |

---

## 常见 PM 错误

1. **把 grader 分数当 ground truth** —— model graders 有随机性。要信 prompt 版本之间的 delta，不要信绝对数字。
2. **跳过标准定义** —— 跟工程说"直接评就好"会产出一个到处打 6 分的 grader。一定要先定 rubric。
3. **没预留 grader 迭代预算** —— grader 本身也是个 prompt，需要调。要排周期给它。
4. **该用 code grader 却用 model grader** —— 浪费 token、拖慢迭代。规则类检查一律优先 code grader。
5. **没记录 reasoning** —— 分数意外时，你需要辩护理由才能跟工程或 QA debug。

> **关键洞察**
>
> Model-based grading 把 prompt engineering 从手艺变成产品 workflow。Grader 本身不是 feature —— grader 是**测量仪器**，让你有信心改善真正的 feature。懂这点的 PM 能在几周内交付质量提升；跳过这步的 PM 只能交付 vibes 和希望。

---

## CCA 考试相关性

- **D3（Evaluation）**：Model-based grading 是 LLM-as-judge 的范式。要知道何时选 model vs code vs human，以及 grader prompt 必须包含什么（strengths、weaknesses、reasoning、score）。
- **D5（Enterprise Deployment）**：Graders 支撑 eval 驱动迭代 —— 考题会围绕生产环境测量 prompt 改善。
- 注意："你要衡量 helpfulness / instruction following / completeness"→ model grader。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Model-based grading 解决什么产品问题？ | 把主观的 AI 输出质量变成 PM 可绘制、可迭代的数字。 |
| 三种 grader 类型是什么？ | Code graders、model graders、human graders。 |
| PM 何时该选 model grader 而非 code grader？ | 当质量维度是主观的 —— helpfulness、completeness、instruction following、safety。 |
| 为什么 model grader 必须返回 strengths 和 weaknesses，而不只是分数？ | 没有它们，model 会退化到 6 分左右，指标失效。 |
| 三种 grader 的餐厅比喻？ | 卫生稽查员（code）、freelance 美食评论家（model）、米其林密探（human）。 |
| PM 该信哪种分数 —— 绝对或 delta？ | Prompt 版本之间的 delta —— model graders 绝对值有随机性。 |
| Model graders 擅长哪些维度？ | Response quality、instruction following、completeness、helpfulness、safety。 |
| grader 到底是 feature 还是测量仪器？ | 测量仪器 —— 它存在的目的是让你有信心改善真正的 feature。 |
