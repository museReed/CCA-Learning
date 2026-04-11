# Prompt Evaluation — PM Perspective（简体中文）

| 项目 | 内容 |
|------|------|
| Exam Domain | D3 — Evaluation & Iteration（20%，主要）；D5 — Enterprise Deployment（20%，次要） |
| Task Statements | 3.1（eval 设计）、3.2（测试数据集）、3.3（eval 执行） |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 17 |

---

## 一句话摘要

Prompt evaluation 是 AI 功能的"产品质量版 A/B 测试" — 它让团队改 prompt 时带着"度量出来的信心"上线，而不是祈祷上次那个小调整没把真实用户搞坏。

---

## PM 为什么要关心

每一个 AI 功能背后都有一个 prompt。没有 evaluation pipeline，"这个 prompt 好不好？"只是工程师的意见，不是产品的事实。这个落差会直接造成商业后果。

| 症状 | 根因 | 商业冲击 |
|------|------|----------|
| 客户反映"AI 回答错误" | Prompt 从未在真实流量上测过 | 客户流失、品牌信任受损 |
| 工程师争论哪版 prompt"更好" | 没有客观指标终结辩论 | 迭代变慢、变成政治决策 |
| 不敢改现有 prompt | 没有安全网抓 regression | 功能停滞、prompt 技术债 |
| 无法向高层汇报质量数字 | 根本没有 eval 分数 | 无法设定 AI 质量 OKR |

Prompt evaluation 把上面每一个"意见"和"恐惧"变成数字。PM 就是靠数字管产品的。

---

## 心智模型：餐厅厨房

把 prompt 想成食谱，prompt evaluation 想成试菜团队。

| 厨房概念 | Prompt 概念 |
|----------|-------------|
| 食谱卡 | Prompt 模板 |
| 主厨调整食谱 | Prompt engineer 调整 prompt |
| 主厨尝一次就出菜 | 选项 1 — 测一次就上 |
| 主厨尝五次、调一点调味 | 选项 2 — 测几次、补边角情况 |
| 试菜小组按评分表给 20 道菜打分，主厨据此迭代 | 选项 3 — 跑 eval pipeline |

选项 3 是唯一能让你拥有米其林级厨房的路。选项 1 和 2 感觉快，但做出的晚餐质量不稳定。

---

## 三条路 — PM 视角

| 选项 | 工程师实际做的事 | PM 可见的风险 |
|------|------------------|--------------|
| 1. 测一次 | 跑一个例子看起来没问题就上 | 高：任何不寻常的用户输入都可能成为事故 |
| 2. 测几次补洞 | 跑几个他能想到的边角情况 | 中：人类想象力抓不到真实长尾 |
| 3. Eval pipeline | 跑几百、几千个案例进自动化 scorer | 低：regression 在开发机就被抓到，而不是客服工单 |

工程师说"prompt 好了"，PM 的下一个问题永远应该是：*你刚才走的是三条路中的哪一条？*

---

## 产品场景

### Evaluation 不可省

| 场景 | 原因 |
|------|------|
| 面向客户的 AI 功能 | 失败对用户可见，事故代价高 |
| 涉及金钱、健康、法律、安全的 prompt | 正确性是合规与责任问题 |
| 计划每月迭代的功能 | 没有 eval，每次迭代都是 regression 风险 |
| 想比较两个模型的功能（Haiku vs. Sonnet） | Eval 提供 cost/quality 取舍所需的客观比较 |

### 可以短暂延后

| 场景 | 注意事项 |
|------|----------|
| 下周 demo 的内部原型 | 可延后，但没 eval 就不能正式上线 |
| 一次性抛弃脚本 | 可延后，但要知道你在欠技术债 |

---

## PM 决策框架

在批准任何 AI 功能 GA 之前问：

| 问题 | 如果"没有" |
|------|------------|
| 有反映真实用户输入的 eval 数据集吗？ | 阻止发布 — 你根本无法度量质量 |
| 能产出当前 prompt 版本的客观分数吗？ | 阻止发布 — 你没有 baseline |
| 下个月改 prompt 时 CI 会告诉你质量升降吗？ | 阻止发布 — 你没有 regression 安全网 |
| 能在发布文档的质量章节引用一个数字吗？ | 阻止发布 — 你的质量叙事全凭感觉 |

---

## PM 常见错误

1. **把"看起来还不错"当质量信号** — GA 前应该要求的是数字，不是感觉。
2. **因时间压力让工程师跳过 eval** — 每跳过一次 eval 就是未来要付出的生产事故。
3. **没把 eval 的 API 开销算进预算** — Eval 要钱，从第一天起就应纳入功能成本模型。
4. **把一次成功 demo 当成生产就绪** — 一次 demo 就是选项 1，而选项 1 是陷阱。
5. **没把 eval 数据集当作 PM 的产物** — 数据集编码了"什么才叫好"，那是 PM 的决策，不是 junior eng 的决定。

---

> **Key Insight**
>
> PM 的工作就是把"质量"变成一个数字。Prompt evaluation 就是那个机制，把 AI 质量从主观争论变成能写进 OKR、发布文档、事故复盘的客观指标。CCA 考题只要问"我们怎么知道这个 prompt 可以上生产了？"那就是 D3 题，答案永远是：跑 eval pipeline。

---

## CCA 考试相关性

- **D3（Evaluation & Iteration）**：区分 prompt engineering（怎么写）与 prompt evaluation（怎么量）；掌握三条路和为什么选项 3 胜出。
- **D5（Enterprise Deployment）**：Prompt eval 是生产发布的前置条件 — 没 eval 就不上线。
- 考题常见话术："怎么比较 prompt 版本""怎么抓 regression""怎么汇报质量"都是 D3/D5，都指向 eval pipeline。

---

## Flashcards

| Front | Back |
|-------|------|
| Prompt evaluation 解决的 PM 问题是什么？ | 把"这 prompt 好不好？"这种主观判断，变成能写进发布文档、OKR 和事故复盘的客观分数。 |
| Prompt evaluation 的餐厅比喻是什么？ | 试菜小组按评分表给菜打分，主厨带着信心迭代，而不是只靠一次试吃。 |
| Prompt 写好后 PM 该询问哪三条路？ | 1) 测一次、2) 测几个边角情况、3) 跑 eval pipeline — 只有 3 适合 GA。 |
| PM 批准 GA 前必须要求什么？ | 数据集、客观分数、regression 安全网，以及能写进发布文档的数字。 |
| 为什么"demo 看起来不错"不够？ | Demo 就是选项 1 — 一个例子不是生产流量的随机抽样，会隐藏失败模式。 |
| 什么情况下可以延后 eval pipeline？ | 只能是内部原型或一次性脚本 — 面向客户的功能绝对不行。 |
| Eval 数据集归谁拥有？ | 这是 PM 级别的产物，因为它编码了"什么才叫好"，不是纯工程决策。 |
| Prompt evaluation 对应哪个 CCA domain？ | D3 Evaluation & Iteration（主要）、D5 Enterprise Deployment（次要，作为生产闸门）。 |
