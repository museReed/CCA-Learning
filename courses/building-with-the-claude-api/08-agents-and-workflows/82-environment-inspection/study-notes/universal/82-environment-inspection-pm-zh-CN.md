# Environment Inspection — PM 视角

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture (22%) |
| Task Statements | 1.1 (agent 架构)、1.2 (agentic loop)、1.3 (agent 中的 tool use)、5.1 (production pattern 选型) |
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 82 |

---

## 一句话总结

AI agent 默认是盲的——它需要明确的"眼睛"去看你 App 的 state 才能可靠地交付结果。PM 必须从第一天就把 inspection 能力写进预算,不能当成 nice-to-have。

---

## PM 为什么该关心

Production AI 功能大部分的失败不是 model"幻觉"——是 model 在它实际看不到的 state 上做动作。用户的文件因为错误假设被改掉、按钮被宣告点击成功但其实什么都没发生、数据库 row 用过时 context 被更新。

解法不是"用更聪明的 model",而是给 agent **观察能力**,并且强制它在每个动作前后都用。这是 PM 的决策,因为它会出现在你的 PRD 里:tool 需求、成本预算、可靠度 SLO。

| 没有 Inspection | 有 Inspection |
|----------------|--------------|
| Agent 凭空猜现实 | Agent 每个决策都接地在观察到的 state |
| 静默失败传到用户 | 失败在同一轮就被抓到并修正 |
| "AI 看起来不太可靠" | "AI 稳定地交付它承诺的东西" |
| 错误编辑引发客服 ticket | 用户信任随时间累积 |

---

## 心智模型:没看 X 光就动刀的外科医生

想象一个外科医生,靠教科书背下人体解剖,但拒绝在开刀前看你实际的 X 光片。每个病人都略有不同——器官位置会偏、血管分支不尽相同——教科书的平均值不是你的身体。

没有 environment inspection 的 agent 就是那个医生。他们知道代码、文件、数据库、UI"通常"长什么样,然后根据平均值动作。Environment inspection 就是 X 光:它让 Claude 看到面前这个 **特定的** 病人,不是教科书。

产品版本的心法:**agent 动刀前要先看,缝合后要再看一次。**

---

## 产品使用场景

### 什么时候 Inspection 是关键

| 情境 | Inspection 给你什么 |
|------|---------------------|
| AI 编码助手编辑用户文件 | 防止覆盖"上次读取之后"才发生的变更 |
| Agent 操作网页 UI(Computer Use) | 每次点击后的 screenshot 确认点击成功 |
| AI 客服 agent 更新 CRM 记录 | Read-back 确认更新有存进去 |
| AI 内容生成器产出多媒体 | 抽 frame/字幕验证输出符合 brief |
| AI 操作团队共享数据 | 抓出 race condition 和 stale-state bug |

### 什么时候 Inspection 是过度工程

| 情境 | 为什么可以跳过 |
|------|---------------|
| 一次性文字摘要 | 没有 state 被变更——没东西可 inspect |
| 固定输入的翻译 | 输出就是唯一 artifact;没有下游 state |
| 分类或评分 | Pure function——没有环境可 inspect |

**Rule**:任何会写入东西(文件、DB、API、UI)的功能都该有 inspection。只读取并返回文字的功能通常不需要。

---

## "不做 Inspection"的隐藏成本

团队跳过 inspection 是因为感觉像工程 overhead。这个省法实际上买到什么:

| 跳过省下 | 后来付的代价 |
|----------|-------------|
| 每个动作少 2 次 tool call | 客服 ticket 变 10 倍 |
| 每次请求 cost 少 ~20% | 一次错误编辑就失去用户信任 |
| 响应稍快 | 工程团队好几个月在救 edge case |
| PRD 比较简单 | Production 有不可知的失败模式 |

这是典型的短期 vs 长期 trade-off。为了赶 demo date 跳过 inspection 的 PM 通常会付 5 倍回去补客服负担。

---

## PM 决策框架

对每个 AI 功能问:

| 问题 | 为什么重要 |
|------|-----------|
| Agent 变更了什么 state? | 任何变更的东西都必须可观察 |
| Agent 怎么知道动作成功? | 答不出来 = 你有个盲 agent |
| 静默失败长什么样? | Inspection 是你实时抓静默失败的方法 |
| 如果 state 在 agent 上次读取后变了会怎样? | 答案是"数据丢失" = 写入前强制重新 inspect |
| 怎么衡量结果符合意图? | 动作后的 inspection 是你的 in-band quality gate |

如果团队说"直接相信 tool result 就好",推回去。Claude 分不出"我做了"跟"我以为我做了"的差别,没有证据它真的不知道。

---

## PM 常见错误

1. **把 inspection 当成要优化掉的 cost** — 每次 inspection 省下的客服和恢复成本是它自己的好几倍。
2. **PRD 里没列 inspection tool** — 你不写,工程团队就会做 write-only 版本。
3. **Computer Use 为了"省钱"关掉 screenshot** — 这会让下游每个 agent 决策都静默劣化。
4. **说"model 应该自己知道"** — Environment inspection 关心的是 model 面前的 **具体** state,训练数据给不了这个。
5. **用"tool call 次数"当成功指标** — 你要的是"verified success rate"不是"tool call success rate"。

> **Key Insight**
>
> Environment inspection 是任何 agentic 产品里单一杠杆最高的可靠度功能。把它写进 PRD、把它列进 acceptance criteria——这就分开了"用户信任的 AI 产品"跟"制造客服 ticket 的 AI 产品"。心法:"Agent 动作前看到什么?动作后怎么确认成功?"

---

## CCA 考试关联

- **D1 (Agentic Coding & Architecture)**:会出情境题"agent 改错文件,哪里出问题?"答案通常是"没先检视当前 state"。
- **D5 (Enterprise Deployment)**:Production agent 的可靠度、error handling、用户信任都是 inspection 的下游。
- 考题关键字:"grounding""observe environment""verify output""read before write"。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Environment inspection 为什么对 agent 很关键? | Claude 默认是盲的——它需要 tool 来观察真实 state,否则只能根据假设行动。 |
| Environment inspection 的外科医生类比是什么? | 一个拒绝看你 X 光的医生——他懂一般解剖但不懂你这个病人;inspection 就是 X 光。 |
| PM 什么时候该在 PRD 里要求 environment inspection? | 只要 agent 会变更任何 state 就要——文件、数据库、UI、API。 |
| 列出三个 inspection 很关键的产品情境。 | AI 代码编辑器、Computer Use agent、CRM 更新 agent、内容生成器、共享数据 agent(任三)。 |
| 跳过 inspection 的隐藏成本是什么? | 静默失败传到用户、客服 ticket 爆掉、用户信任崩盘——通常比 inspection 本身的 cost 贵 5 倍。 |
| PM 在 PRD 里对每个 AI 动作该问的单一问题是什么? | "Agent 怎么知道这个动作成功了?" |
| 为什么"model 应该自己知道"是错的 PM 直觉? | 训练数据给的是平均值,inspection 关心的是此刻 model 面前的具体 state。 |
| 比"tool call 成功率"更重要的 success metric 是什么? | Verified outcome success rate——观察到的 state 是否真的符合用户意图。 |
