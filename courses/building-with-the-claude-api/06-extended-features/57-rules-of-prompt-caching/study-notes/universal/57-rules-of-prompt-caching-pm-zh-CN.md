# Rules of Prompt Caching — PM Perspective（简体中文）

| 项目 | 详情 |
|------|------|
| 考试领域 | D5 — Enterprise Deployment (20%) |
| Task Statements | 5.1（成本／延迟优化）、5.2（生产性能） |
| 来源 | building-with-the-claude-api / 06-extended-features / Lesson 57 |

---

## One-Liner

Prompt caching 有一本规则书，必须照办才能拿到折扣：明确 opt in、cached 内容保持逐字节一致、达到 1,024 token 门槛、把四个 breakpoint 额度当稀缺资源来规划。

---

## PM 为什么要关心这些规则？

Engineering 可以把 caching 开关打开，但真正让 caching 发挥效果的，是产品层面的决策：**哪些内容要保持稳定不变**。如果你的产品每个 sprint 都在改 system prompt、让用户重排 tool definition、把用户问题塞进「模板」中间——cache 就会失效，省下来的钱全部蒸发。

换句话说：caching 的规则其实是「**你的 context 有多稳定**」的规则——这是产品决策，不是工程决策。

---

## Mental Model：仓库贴标流水线

想象一个物流仓库，箱子在传送带上被盖印刷上标签。每个箱子前三面都盖着同样的大公司 logo（稳定），只有第四面手写客户地址（可变）。

| 层 | 仓库比喻 | Caching 对应 |
|----|----------|----------------|
| 预先盖的 logo | 公司 logo 橡皮章 | Tools + system prompt + 稳定 context |
| 定制标签 | 手写的客户地址 | 用户当下的问题 |
| 规则 | Logo 必须完全一致——糊一个字就整面重印 | Cached 前缀必须逐字节相同 |
| 批量规则 | 不能预先盖微型出货单——只有大箱子行 | Breakpoint 前最少 1,024 tokens |
| 切线规则 | 流水线上只有四个印章站 | 每个请求最多 4 个 cache breakpoint |

印章只有在「左边的东西完全一样」时才省事。印章一换，整片就得重印。

---

## Product Use Cases

### 能符合规则的产品模式

| 模式 | 为什么符合 |
|------|------------|
| 带锁定 persona 的聊天产品 | 稳定前缀 → 每轮逐字节一致 |
| 带版控 tool schema 的编程助手 | Tool 只在 deploy 之间改，不会在 session 中途变 |
| 有标准 PDF 的文档问答 | 文档稳定；只有用户问题在变（且放在 breakpoint 之后） |
| 带固定工具箱的 agent loop | Tools + system prompt 每轮都是稳定的可缓存前缀 |

### 会打破规则的产品模式

| 模式 | 为什么会破 |
|------|------------|
| 在 prompt 顶端注入「个性化问候」 | 用户名是变量 → 每轮 cache miss |
| A/B 测试为不同用户改写 system prompt | 前缀不同 → 没人受益 |
| 短 prompt（< 1,024 tokens） | 低于门槛 → caching 是 no-op |
| 让用户重排 tool description | 字节顺序变化 → cache 失效 |

---

## PM Decision Framework

在把 caching 纳入某个功能之前，跑一遍这张检查表：

| 问题 | 为什么重要 |
|------|------------|
| 是否有一段至少 1,024 tokens 的稳定 context？ | 低于此，caching 什么都不做 |
| 能保证那段稳定内容放在请求的**开头**吗？ | Breakpoint 切的是前缀，变量必须放在**之后** |
| 使用的独立 caching 层少于 4 层吗？ | 4 是硬上限——预算要抓好 |
| 能承诺 release 之间保持那段前缀逐字节一致吗？ | 一个空白的 rewrite 就会打翻 cache |
| 那段 context 一小时内会被复用吗？ | TTL 是 1 小时——冷门功能浪费 cache write |
| 你知道什么时候会变吗——以便把 breakpoint 放在能最小化失效的位置？ | Cache 边界要对齐变动频率 |

前四题不能全答「是」，caching 就会表现不如预期——或静默什么都不做。

---

## Common PM Mistakes

1. **把 caching 当成工程开关** — 它其实是**context 稳定性契约**。产品决策决定 cache 会不会命中。
2. **把变量内容注入前缀** — 把用户名、时间戳、session ID 放在 system prompt 顶端，等于每次调用都毁掉 cache 命中。变量移到尾巴。
3. **随手改 system prompt** — 每次小编辑都让 cache 失效。把 cached system prompt 当成有版本、有 changelog 的 asset 对待。
4. **在小功能上忽略 1,024 token 门槛** — 「我们开了 caching 但成本没降」通常是前缀太短不合格。
5. **太早把 4 个 breakpoint 用光** — 把 budget 用光就没空间做后续优化。留一个保留位。
6. **没通知 cache 失效事件** — 一次 system prompt 「润色」就可能让整个舰队一小时的 cache 节省归零。所有人要知道这事何时发生。

---

> **Key Insight**
>
> Prompt caching 的规则其实是一份「**你的产品承诺保持什么稳定**」的契约。好的 PM 读完这堂课会问：「我的 prompt、tools、context 哪些部分能真的冻结？」那个答案——不是工程开关——才决定 caching 能不能兑现广告上的节省。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）** — 考题会测这些机械规则：手动 opt in、逐字节比对、1,024 token 底线、4 个 breakpoint 上限、1 小时 TTL、tools → system → messages 顺序。
- 题目若出现 PM 被告知「caching 开了但没看到省」——答案几乎总是某条规则被违反（前缀里有变量、内容低于门槛、或 system prompt 被随手改过）。
- 记住 system prompt 与 tool definition 是**最佳**缓存目标，因为它们在处理顺序上排最前面，而且很少变动。

---

## Flashcards

| Front | Back |
|-------|------|
| 从 PM 角度看 prompt caching 是自动的吗？ | 不是——engineering 要逐 block 明确 opt in，产品要承诺内容稳定才会赚。 |
| 什么长度门槛才能启动 caching？ | Breakpoint 之前累积至少 1,024 tokens。 |
| 单个请求最多可以用几个 breakpoint？ | 最多 4 个。 |
| 为什么用户的问题应该放在 breakpoint **之后**？ | 因为 cached 前缀必须逐字节相同；把变量放进前缀等于保证 miss。 |
| 最好的 caching 目标是哪些层？ | System prompt 和 tool definition——体积大、稳定、处理顺序最前。 |
| 什么改动会打翻 cache 即使「没实质变化」？ | 任何空白编辑、错字修正、加「please」、或重排 tool——caching 是逐字节精确。 |
| PM 为什么要关心 1 小时 TTL？ | 低频功能的 cache entry 会在被复用前过期，等于什么都没省到。 |
| PM 在 prompt caching 上真正的任务是什么？ | 保证 context 稳定性——规则只有在产品承诺把 cached 前缀冻结时才会兑现。 |
