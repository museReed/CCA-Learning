# Temperature — PM 视角

| 项目 | 细节 |
|------|------|
| 考试领域 | D5 — Enterprise Deployment (20%) |
| Task Statements | 5.1（模型配置）、5.3（production 模式）、5.4（evaluation 与可靠度） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 11 |

---

## 一句话总结

Temperature 是 Claude 的「创意旋钮」——它控制用户看到响应的变异程度。身为 PM，为每个 feature 选对 temperature，就是你把输出行为对齐用户期望的方式：事实任务用可预测的，创意任务用多变的。

---

## 心智模型：厨师类比

想象在餐厅点餐：

| Temperature | 厨师行为 | 食客期望 |
|-------------|---------|---------|
| 0.0 | 每次都照菜谱做出完全一样的菜 | 「我要招牌牛排——和上次一模一样」 |
| 0.5 | 照菜谱做但加入小而有品位的变化 | 「按你的风格来，但保持招牌味」 |
| 1.0 | 自由即兴——每盘都是新创作 | 「惊喜我——主厨选择，永远不一样」 |

如果食客点的是医疗处方却拿到「主厨选择」，那是灾难。如果食客点的是 tasting menu 却每晚拿到同一道菜，那很无趣。Temperature 是这个 feature 要给用户哪种体验的产品决策。

---

## 为什么 PM 要在乎

Temperature 是少数几个**直接塑造用户体验**的 Claude 参数。它不是技术细节——它是产品政策。

- **低 temperature** = 产品承诺*一致性与可靠*
- **高 temperature** = 产品承诺*多样与惊喜*
- **中 temperature** = 产品承诺*质量带点人味*

如果你的数据抽取功能每次返回不同 JSON 结构，用户会失去信任。如果你的 brainstorming 工具每次访问都返回同样三个点子，用户会不再打开它。Temperature 是修复这两者最简单的杠杆。

---

## 产品使用场景

### 低 Temperature (0.0 – 0.3)

| 产品 | 为什么低？ |
|------|-----------|
| 支持工单分类 | 同输入必须得到同 label |
| 发票数据抽取 | 下游系统预期确定性字段 |
| 医疗 / 法律说明 | 措辞变异可能有法律风险 |
| Code 助手 | 用户预期同 bug 拿到同 fix |
| 内容审核 | 一致性是公平性要求 |

### 中 Temperature (0.4 – 0.7)

| 产品 | 为什么中？ |
|------|-----------|
| 会议摘要 | 连贯结构 + 自然措辞 |
| 家教解说 | 一致教学法带人声 |
| Email 草稿助手 | 事实为根但不机械 |
| 知识库回答 | 可靠事实加可读变化 |

### 高 Temperature (0.8 – 1.0)

| 产品 | 为什么高？ |
|------|-----------|
| Brainstorming / 发想工具 | 用户要很多不同点子 |
| 营销文案生成器 | 新颖就是全部意义 |
| 命名 / slogan 生成器 | 多样性 > 精确 |
| 虚构 / 游戏对白 | 惊喜驱动 engagement |

---

## PM 决策框架

规划 AI feature 时问四个问题：

1. **同样输入需要产生同样输出吗？** → 低 temperature。没有例外
2. **下游 parser 或 automation 会消费这个输出吗？** → 低 temperature。变异会打破 pipeline
3. **用户会把两次执行并列比较吗？** → 低或中。不一致会被当成 bug
4. **多样性是价值主张的一部分吗？** → 高。锁死

把答案写进 PRD，当作验收标准的一部分。「Temperature: 0.2, fixed」是真实的产品需求，不是调校细节。

---

## Temperature 修不了什么

Temperature 是 sampling 旋钮，不是质量修复。当真正的问题是下列时，不要伸手抓它：

- **坏 prompt** → 先改 prompt；temperature 是第二层
- **缺少 context** → 加 retrieved data 或 tools；temperature 无法捏造事实
- **模型尺寸不对** → 输出真的不够聪明就升级 model 阶层
- **Persona 不一致** → 那是 system prompt 的工作，不是 temperature

常见失败模式：PM 在 production 看到「hallucination」，把 temperature 降到 0 上线。Hallucination 是坏 prompt 造成的，不是 temperature。这个 fix 毫无作用。

---

## 常见 PM 错误

1. **所有功能都让 temperature 停在默认 1.0**——对 chat 很好，对抽取很糟。每个 feature 要选
2. **把低 temperature 和高准确度搞混**——它只代表低变异。一致的错答案还是错
3. **没在 PRD 指定 temperature**——工程师会选一个他们觉得顺手的，你会在上线后继承这个不一致
4. **没改 prompt 就做 temperature 高 vs 低的 A/B test**——你可能在测错的变量
5. **在法律敏感文案用高 temperature**——它总有一天会生成 off-brand 的东西，你会在会议室里被约谈

> **Key Insight**
>
> Temperature 是产品政策决策，不是工程调校旋钮。它编码的是你和用户关于「能预期多少变异」的契约。刻意决定它、写进 PRD、每个 feature 锁死。最糟的结果是因为 temperature 由「第一个写 code 的人」决定而产品不一致。

---

## CCA 考试重点

- **D5 (Enterprise Deployment)**：temperature 是标准 production 配置参数。预期会考场景题，问给定产品该用哪个区段
- 注意「如何确保分类输出一致？」这种问法——答案是低 temperature
- 注意「如何生成多样的营销文案变体？」这种问法——答案是高 temperature

---

## Flashcards

| 题目 | 答案 |
|------|------|
| 在产品层面，temperature 控制什么？ | 用户看到响应的变异程度——低 = 一致，高 = 多变 |
| 数据抽取工具该用哪个 temperature 区段？ | 低（0.0–0.3）——确定性是产品需求 |
| Brainstorming 工具该用哪个 temperature 区段？ | 高（0.8–1.0）——多样性就是价值主张 |
| 会议摘要该用哪个 temperature 区段？ | 中（0.4–0.7）——连贯但自然 |
| 低 temperature 等于高准确度吗？ | 不等于——它只代表低变异。可重复的错答还是错 |
| Temperature 该写进 PRD 吗？ | 应该——它是产品政策，不是工程调校细节 |
| Temperature 0 vs 1 的厨师类比是什么？ | 0 = 招牌菜每次完全一样；1 = 主厨选择，从不相同 |
| Temperature 修不了哪些产品问题？ | 坏 prompt、缺 context、错 model、persona drift。Temperature 是第二层 |
| 为什么法律 / 医疗文案用 temperature 1.0 危险？ | 罕见不寻常措辞可能有法律风险；你要的是一致性，不是创意 |
