# 代码评分 Code-Based Grading — PM 视角

| 项目 | 说明 |
|------|------|
| 考试领域 | D3 — Evaluation（20%）主要；D5 — Enterprise Deployment（20%）次要 |
| 任务声明 | 3.4（deterministic 评分）、3.3（test runner 集成）、5.4（综合 eval 指标） |
| 来源 | building-with-the-claude-api / 02-prompt-evaluation / Lesson 22 |

---

## 一句话重点

Code-based grading 是你 AI 质量指标中便宜、deterministic 的底层 —— 用微秒时间自动挡下坏掉的输出，让团队不会再上线那些 demo 就能抓到的退化。

---

## 为什么 PM 要在意

想象一下：你上线了一个 code-generation feature，结果从用户推文才发现有一半输出 syntax 错。这种事不该发生。Code-based grading 让这类退化**无法上线** —— 每个 test case 在 prompt 改动正式发布前就自动被 parse 过。

Code grader 能抓、model grader 无法可靠抓的三件事：

- "这到底能不能 parse 成 JSON / Python / Regex？"
- "当我要求纯 code 时，model 有没有偷塞 commentary？"
- "这周我们是不是不小心在 format 纪律上退化了？"

这些退化人类 demo 可能 miss，但跑在每个 prompt PR 上的 CI pipeline 绝对会抓到。

---

## 心智模型：上编辑之前先拼写检查

把 code grader 和 model grader 想成两阶段编辑 pipeline：

| 阶段 | 角色 | 成本 | 抓什么 |
|------|------|------|--------|
| **拼写检查**（code grader） | 自动挡下 syntax 坏掉的输出 | 微秒、免费 | JSON parse 错误、Python syntax 错误、regex 错误 |
| **编辑**（model grader） | 判断清晰度、有用度、指令遵循 | 每个 case 一次 API | 主观质量问题 |

每一篇文字在交给真人编辑前都会先过拼写检查。AI 输出也一样 —— 便宜的 deterministic 检查先跑，过关的才进昂贵的判断环节。

---

## 产品使用场景

### 何时用 Code Graders

| 场景 | 为什么 code grader 适合 |
|------|-------------------------|
| 要上线 JSON API、AI 必须返回合法 JSON | Parseable 是不可协商的，而且检查免费 |
| Code-generation 功能（SQL、Python、regex） | 无效 syntax 会立刻让产品坏掉 |
| "只要 raw output、不要 commentary"的指令 | 用严格 parser 很好验 |
| 长度或格式限制 | 是布尔检查，不是判断题 |
| 每个 prompt PR 上 CI/CD eval gate | 微秒延迟让它可以到处跑 |

### 何时**不要**用 Code Graders

| 场景 | 更好的替代 |
|------|-----------|
| "这个响应有没有帮上忙？" | 用 model grader —— 这是主观题 |
| "输出符不符合品牌语气？" | 用 model grader |
| "答案对不对？" | 除非你有 ground-truth 字符串可比对，否则用 model grader |

---

## 综合分数才是 feature

来源最后一步是把 model grader 和 code grader 分数取平均：

```
score = (model_score + syntax_score) / 2
```

这个综合指标才是 PM 该追踪的。它奖励同时在形式（syntax）和内容（quality）都对的 prompt，并惩罚任一轴作弊的 prompt。

一个关键 PM 决策：**权重**。预设是 50/50。纯 code-generation 产品可能要把 syntax 拉到 70%。客服语气功能可能要把 quality 拉到 80%，code grader 只当硬底线。这个权重是**产品决策**，不是工程决策 —— 明确写在 PRD 里。

---

## PM 决策框架

| 问题 | 若答 Yes | 行动 |
|------|---------|------|
| 输出有 deterministic 结构（JSON、code、regex）吗？ | Yes | 加 code grader —— 免费又 deterministic |
| test case 有 `format: "python"` 这类格式字段吗？ | Yes | 很好 —— runner 可以自动 route |
| Eval pipeline 有 gate 在 CI 吗？ | Yes | Code graders 是最便宜、最适合每个 PR 跑的 gate |
| 我们也在乎内容质量吗？ | Yes | 和 model grader 合并取平均分数 |
| 有某个维度比另一个重要很多吗？ | Yes | 在 PRD 里调权重 —— 不要永远预设 50/50 |

---

## 常见 PM 错误

1. **因为"model grader 什么都能做"就跳过 code grader** —— 在 deterministic 检查上浪费 token，还引入不该有的 variance。
2. **CI 没 gate code grader** —— 坏掉的 JSON 退化会上线，没任何东西在 review 前挡它。
3. **永远预设 50/50 权重** —— 不是每个产品都平等看重 syntax 和质量。要刻意调。
4. **把 test case format 当成工程独占** —— `format` 字段是产品决策（我们对用户承诺什么？），该在 PRD 里拥有。
5. **把分数当目标** —— 来源讲得很清楚：分数本身无所谓好坏。重点是 prompt 迭代能不能把它往对的方向推。

> **关键洞察**
>
> Code graders 存在是因为某些质量属性是二元的：JSON 不是能 parse 就是不能，Python 不是能编译就是不能。花 model grader 去检查这些就像花钱请书籍编辑做拼写检查。便宜的 deterministic 检查放前面，model grader 的 token 只花在真的需要判断的地方。

---

## CCA 考试相关性

- **D3（Evaluation）**：Code graders 是混合 eval pipeline 的 deterministic 那一半。要知道哪些任务属 code grader（format、syntax、长度）vs model grader（质量、helpfulness）。
- **D5（Enterprise Deployment）**：Deterministic 评分让 eval 自动化便宜到可以 gate CI。
- 注意："你要验证 AI 产的 JSON / Python / Regex"→ 答案永远是 code grader。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Code graders 解决了 model graders 无法可靠处理的什么产品问题？ | 在上线前抓出坏掉的 deterministic 输出（无效 JSON、不能 parse 的 Python、坏 regex）。 |
| Code graders 的两大优势？ | Deterministic（同输入同分数）和极便宜（微秒、无 API 成本）。 |
| Code grader + model grader 的心智模型？ | 拼写检查（code grader）先跑，真人编辑（model grader）后跑。 |
| 合并 model 和 code grader 分数的预设方式？ | 非加权平均：`(model_score + syntax_score) / 2`。 |
| Model 和 code grader 分数的权重该由谁拥有？ | PM —— 这是关于功能"哪一轴更重要"的产品决策。 |
| test case 必须带哪个字段，runner 才能 route 到正确 validator？ | `format` —— 值像 `"python"`、`"json"`、`"regex"`。 |
| 为什么绝对分数无所谓好坏？ | 因为重点是 prompt 迭代能不能移动它 —— 看 delta，不看绝对值。 |
| 什么时候应完全跳过 code grader？ | 当输出没有 deterministic 结构可验（例如自由格式的有用响应）。 |
