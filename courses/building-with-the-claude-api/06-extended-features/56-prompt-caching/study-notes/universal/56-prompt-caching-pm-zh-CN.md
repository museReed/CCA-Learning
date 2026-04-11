# Prompt Caching — PM Perspective（简体中文）

| 项目 | 详情 |
|------|------|
| 考试领域 | D5 — Enterprise Deployment (20%) |
| Task Statements | 5.1（成本／延迟优化）、5.2（生产性能） |
| 来源 | building-with-the-claude-api / 06-extended-features / Lesson 56 |

---

## One-Liner

Prompt caching 是 Claude API 的「批发折扣」——只要你的产品反复发送同一大段 context，开启之后每一次非首次调用都会更快、更便宜，而且用户完全感觉不到任何变化。

---

## PM 为什么要关心？

你的 app 每次调用 Claude，模型都要先做一堆昂贵的前置处理（tokenization、embeddings、上下文分析）才吐出第一个字——然后把这些结果全部丢弃。如果你的产品每次调用都发同一份 6,000 token 的 system prompt 或同一份长 PDF，你就是**每次都在重付这笔设置费，还要重等一遍**。

Prompt caching 改变了这个经济模型。这笔设置费只付一次，之后一小时内的后续调用就「免费」（更便宜、更快）地复用。对任何「在稳定 context 上反复交互」的产品，这是单位经济和体感速度上最大的一根杠杆。

---

## Mental Model：手冲咖啡店

想象一家每杯都现磨的手冲咖啡店：

| 步骤 | 没有 caching | 有 caching |
|------|--------------|------------|
| 第一位客人点埃塞俄比亚手冲 | 磨豆、烧水、冲煮 | 磨豆、烧水、冲煮（付全额） |
| 第二位客人点同样的 | 重新磨豆、重新烧水、再冲 | 复用已磨好的豆和热水（只付冲煮） |

磨豆与烧水 = preprocessing。冲煮 = 真正的生成。Prompt caching 就是「别再为同样的订单重复磨豆」。客人仍然拿到现做的咖啡——只是出杯更快，店铺毛利更高。

---

## Product Use Cases

### 适合开 caching 的场景

| 场景 | 为什么有用 |
|------|------------|
| 带长 persona／指南的聊天产品 | Persona 每轮都一样——cache 一次就够 |
| 文档问答（对同一份 PDF 问多个问题） | 文档稳定，只有问题在变 |
| 带大 repo context 的编程助手 | 每次请求都带同样的代码库 context |
| 带固定 tool 的 agent loop | Tool schema 每轮都一样 |
| 反复编辑同一份草稿 | Base content 固定，指令在变 |

### 不适合的场景

| 场景 | 为什么没用 |
|------|------------|
| 一次性 prompt（不会重复） | 白白付 cache-write 成本 |
| Prompt 每次都变 | Cache 永远 miss |
| 调用频率极低（间隔几小时） | Cache 一小时就过期 |
| Prompt 很短 | 节省的几乎可忽略 |

---

## PM Decision Framework

判断是否为某个功能开启 prompt caching：

| 问题 | 为什么重要 |
|------|------------|
| 每次请求是否都带一段「大而稳定」的 context？ | Caching 就是靠大而稳定的前缀在省 |
| 用户在一小时内是否频繁交互？ | 1 小时 TTL 奖励高频复用 |
| Input token 成本是否是单位经济中的显著部分？ | 如果是，caching 直接影响毛利 |
| 体感延迟是用户的主要抱怨吗？ | Caching 降低 time-to-first-token |
| Cached 内容是否真的每次一字不差？ | Cache 对任何改动都极度敏感 |

大多答案为是，就该排进 roadmap——通常应该排在其他模型端优化之前。

---

## 商业影响

| 指标 | Prompt caching 的典型影响 |
|------|---------------------------|
| **单次对话成本** | 下降——cached 前缀按显著折扣计费 |
| **延迟／time-to-first-token** | 下降——命中时跳过 preprocessing |
| **AI 功能毛利率** | 上升——热门 workflow 单位成本下降 |
| **留存率（间接）** | 可能上升——更快的响应让产品更「顺手」 |

这些全是生产收益，完全不需要改产品、也不增加用户摩擦。这种机会很稀有。

---

## Common PM Mistakes

1. **把 caching 当作「以后再做」的优化** — 等你注意到账单时，已经多付了好几个月。只要你的产品有任何重复 context 的模式，就应该排进 v1。
2. **把 caching 和 memory 或个性化混淆** — caching 是「复用计算」，不是「记住用户」。它不会改变 Claude 知道什么。
3. **算指标时忽略 1 小时 TTL** — 不看调用频率就估算「x% 调用被 cache」，低流量功能会高估节省。
4. **不投资 context 稳定性** — 如果团队每个 sprint 都在改 system prompt，cache 一直被打翻。稳定 context 是前提。
5. **没告诉 finance／ops caching 上线** — 成本曲线会突然变形。确保成本模型跟上。

---

> **Key Insight**
>
> Prompt caching 是**隐形的产品改善**：用户看不到，但感受得到。更低的单次成本保护毛利，更低的延迟让产品用起来更顺。对任何建立在「大而稳定 context」之上的 AI 功能，caching 是 PM 能推动的杠杆最大的优化——纯粹的上行，没有 UX 代价。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）** — caching 稳稳落在 task 5.1（成本与延迟）之下。考题会问如何优化重复 context 的 workflow。
- 记住 caching **同时**降低成本与延迟，不是只降一个。
- 记住 1 小时 TTL，以及只有在这时间窗内复用才有用。
- 题目若出现「对同一份长文档问多个问题」或「每轮都发同样 system prompt」的情境，答案通常是 prompt caching。

---

## Flashcards

| Front | Back |
|-------|------|
| 用最白话说，prompt caching 为产品做了什么？ | 把 Claude 昂贵的 preprocessing 结果存起来复用，让重复 context 的调用更快更便宜。 |
| PM 必记的 1 小时规则是什么？ | Cache 内容只存活一小时，过后就过期必须重建。 |
| Caching 影响哪两个商业指标？ | 每次调用成本（下降）以及延迟／time-to-first-token（下降）。 |
| 哪些产品模式最受益？ | 大型稳定 system prompt、文档问答、带 repo context 的编程助手、带固定 tool 的 agent loop、迭代编辑。 |
| 哪些产品不受益？ | 一次性 prompt、内容每次都变、低频使用（间隔超过一小时）、极短 prompt。 |
| Caching 是自动的吗？ | 不是——必须明确启用；不 opt-in Claude 就照常丢弃 preprocessing。 |
| Caching 会改变 Claude 对用户的「了解」吗？ | 不会——它只复用计算，不是 memory 或个性化。 |
| 为什么 caching 应排进 v1 而不是「以后再说」？ | 因为没有它的每一周都是在「重复 context 流量上重付两次」，省下的钱不会回补过去。 |
