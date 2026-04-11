# Prompt Caching in Action — PM Perspective（简体中文）

| 项目 | 详情 |
|------|------|
| 考试领域 | D5 — Enterprise Deployment (20%) |
| Task Statements | 5.1（成本／延迟优化）、5.2（生产性能） |
| 来源 | building-with-the-claude-api / 06-extended-features / Lesson 58 |

---

## One-Liner

在真实产品里开 caching 的意思是：和团队说好哪段 tool list 与 system prompt 保持冻结、接好 cache 标记，然后到生产监看 usage 计数器，验证 business case 里承诺的节省是否真的出现。

---

## PM 为什么要关心

Caching 是少数几个「产品层决策」能决定成败的优化：我们承诺这段 context 在每次调用间保持一致。Engineering 把 tool list 和 system prompt 转成可缓存形式之后，这项功能要么省钱，要么静默什么都不做。结果完全取决于：

1. **产品保证哪些东西稳定** — 大型稳定 system prompt？稳定 tool schema？两个都有？都没有？
2. **有没有人在看数字** — Cache 节省只有在有人盯着 dashboard 时才算数。

真的懂这堂课的 PM，走进 roadmap 会议可以说：「caching 开了，这三件事会把它打翻，这个指标我会盯着证明它有用。」

---

## Mental Model：会员杯折扣

想象星巴克的自带杯折扣。第一次买咖啡没什么特别。第二次如果你带着同一个杯子，就有折扣。忘记带杯子？原价。杯子太小？不给折扣。太久没用？优惠过期。

| 咖啡店比喻 | Caching 对应 |
|------------|----------------|
| 带同一个杯子 | 发同样的前缀 |
| 续杯折扣 | Cache read 便宜 |
| 第一次来付原价 | 第一次 `cache_creation_input_tokens` |
| 每次匹配都便宜 | 后续 `cache_read_input_tokens` |
| 杯子太小 → 没折扣 | 前缀 < 1,024 tokens → 不 cache |
| 忘记带一次 → 付原价 | 改一个字 → cache miss |

会员计划只有在顾客（你的 app）一直带同一个杯子（同样的前缀）时才有用。

---

## Product Use Cases

### 三个最高价值的目标

| 目标 | 典型大小 | 为什么是好候选 |
|------|----------|----------------|
| 大型 system prompt | ~6K tokens | 定义产品 persona；每次调用都稳定 |
| Tool schemas | ~1.7K tokens | Tool 定义不会在 session 中途改 |
| 重复的 message 内容 | 视情况 | 任何反复发送相同内容的 workflow（文档问答、滚动对话历史） |

### 部分命中是产品胜利

因为 tools、system prompt、messages 各自独立缓存，产品团队可以：

- **调整 system prompt**（可能是表现最差的一层）而不动 tools——tools 的 cache 节省不变。
- **新增一个 tool**——知道只有 tools 层被 cache write，system prompt 的 cache 保持热。
- **在 system prompt 层做 A/B 测试**——清楚知道成本影响：一组付新 prompt 的 cache write，另一组继续读 cached 版。

这种细粒度意味着 caching 不必是「全有全无」的实验闸门。

---

## PM Decision Framework

真实上线时 scope caching 的决策：

| 问题 | 为什么重要 |
|------|------------|
| 哪一层（tools／system／messages）占最大的稳定块？ | 那是你第一个 breakpoint 要放的位置；也是最大的省 |
| 我们能承诺那一层至少冻结一周吗？ | 不断编辑会毁掉节省；稳定就是契约 |
| 谁拥有「cache 真的在用吗」的 dashboard？ | 没人看 `cache_read_input_tokens`，节省就只是空口宣称 |
| 预期命中率是多少？ | 用来设目标（例：上线后 70% 的非首次调用要是 cache read） |
| 如何在 cache 失效前通知团队？ | 改 system prompt 前在 Slack 说一声，能避免成本图表上的惊喜尖峰 |

---

## 要监看的商业指标

| 指标 | 跟踪内容 |
|------|----------|
| **Cache 命中率** | `cache_read_input_tokens / (cache_read + cache_creation)`——越高越好 |
| **单次对话成本** | Caching 上线后应下降；与 baseline 期间比较 |
| **Time-to-first-token** | 命中时应下降；对任何延迟敏感 UX 很重要 |
| **Cache 失效事件** | 每周有几次 system prompt／tool 改动；太多就永远拿不到节省 |
| **TTL 过期 miss** | 如果闲置数小时后的首次调用大多显示 `cache_creation_input_tokens`，你的使用模式可能低于 1 小时频率门槛 |

---

## Common PM Mistakes

1. **上线 caching 却没 dashboard** — 看不到 `cache_read_input_tokens`，就无法向 finance 证明有省到钱。
2. **让文案团队每周编辑 system prompt 而不事先通知** — 每次改写就是 1 小时 cache 归零。要建变更流程。
3. **忽视部分命中** — 团队常误以为「改了 system prompt，caching 坏了」，其实 tools 那层还在命中。部分命中是正常且有价值的。
4. **为第一次调用节省庆祝** — 第一次永远是 cache *write*，那比平常**更贵**，不是更便宜。节省只在 1 小时窗口内后续调用累积。
5. **没告诉 ops／on-call 1 小时 TTL** — 夜间流量掉，早上第一批调用全是 cache write，成本图表看起来会很怪。
6. **把 caching 和 memory 混为一谈** — 有人听到「cache」就以为 Claude 在记东西。它不是。要澄清：caching 是成本／延迟，不是产品记忆。

---

> **Key Insight**
>
> 实战的 caching 重点不是「按开关」，而是**拥有一份稳定性契约**。产品团队决定什么冻结、平台写入 `cache_control` 标记、可观测层回报 `cache_read_input_tokens` 对 `cache_creation_input_tokens`。这三块缺一不可，否则上线就只是口头节省，没有真的省钱。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）** — 考题会给「caching 开了却没看到节省」的场景，答案通常是产品层原因（system prompt 被改、前缀有变量、把部分命中误判为全 miss）。
- 记住 `cache_read_input_tokens` 是证明命中的字段，`cache_creation_input_tokens` 是写入的字段。
- 记住部分命中是预期行为，因为 tools、system prompt、messages 各自独立缓存。
- 记住 1 小时 TTL 以及它与低频流量的交互。

---

## Flashcards

| Front | Back |
|-------|------|
| 开启 caching 时 PM 实际承诺什么？ | 某些 context 层（tool list、system prompt、稳定前缀）在调用间会保持逐字节相同。 |
| 哪个 usage 字段证明这次调用读取了 cache？ | `cache_read_input_tokens`——Claude 从 cache 复用的 tokens。 |
| 哪个 usage 字段证明这次调用写入了 cache？ | `cache_creation_input_tokens`——Claude 刚写入 cache 的 tokens。 |
| 什么是「部分命中」？为什么对 PM 是好事？ | 某一层（如 tools）命中、另一层（如 system prompt）写入。让你能调一层而不失去另一层的节省。 |
| 为什么 caching 上线后第一次调用更贵而不是更便宜？ | 因为那是 cache write（`cache_creation_input_tokens`），不是 read。节省从 1 小时窗口内的后续调用开始。 |
| 说出最受 caching 影响的三个产品层。 | 大型 system prompt（~6K tokens）、tool schema（~1.7K tokens）、重复的 message 内容。 |
| 团队星期五下午改写 system prompt 会发生什么？ | 所有 system prompt cache 都失效；接下来每次调用都付 cache write，直到新 prompt 稳定。 |
| 为什么「cache 命中率」dashboard 是 PM checklist 的一部分？ | 没有它 caching 的效益无法验证——没证据就无法向 finance 汇报节省。 |
