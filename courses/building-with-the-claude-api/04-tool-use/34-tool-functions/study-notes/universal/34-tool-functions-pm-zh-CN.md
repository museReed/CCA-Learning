# Tool Functions — PM Perspective

| 项目 | 内容 |
|------|------|
| 考试 Domain | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.2（tool function 定义）、2.1（tool schema 设计）、1.2（agentic loop 基础） |
| 来源 | building-with-the-claude-api / 04-tool-use / Lesson 34 |

---

## 一句话总结

Tool function 是 Claude 实际执行的代码 — 你工程团队怎么写它（命名、验证、错误消息）直接决定你的 AI 功能对用户而言有多可靠。

---

## 心智模型：厨房出餐线

把你的 AI 产品想象成一间餐厅：

- **Claude** = 跟客人点餐、决定把每道任务丢给哪个灶台的服务员。
- **Tool function** = 真正做菜的线上厨师。
- **Schema** = 服务员读的食谱卡。
- **错误消息** = 厨师出事时喊回去的话（「香菇不够！」vs.「出事了！」）。

食谱卡清楚、厨师喊具体可执行内容的餐厅，运作顺畅。厨师只会对服务员哼哼的餐厅，一片混乱。Tool function 就是你的出餐厨师 — PM 的职责是确保他们讲话清楚。

---

## PM 为什么要关心 Tool Function 设计

Tool function 设计看起来像工程细节，却直接出现在用户体验上：

| Tool function 质量 | 用户会看到的症状 |
|-------------------|--------------------|
| 名字含糊 | Claude 挑错 tool — 功能做错事 |
| 没输入验证 | Tool 返回垃圾 — 用户看到自信的胡说八道 |
| 错误消息没用 | Claude 无法恢复 — 用户看到「抱歉，我做不到」 |
| 错误消息丰富可执行 | Claude 自我修正 — 用户只看到正确答案 |

第三、第四行是重点。AI 功能「感觉可靠」与「感觉坏了」的差别，常常就在你的错误消息能不能让 Claude 自己恢复。

---

## 设计好 Tool Function 的产品场景

### 投资会回本的场景

| 场景 | 为什么好设计很重要 |
|------|-----------------|
| 高流量的用户面向功能 | 微小的可靠度改善会在用户间复利叠加 |
| 多步骤 workflow | 链中每个 tool 都是潜在失败点 |
| 不可逆动作的功能 | 验证能避免真实世界的损害 |
| 复杂参数（日期、ID、金额） | LLM 在没有护栏时超容易出错 |

### 过度设计的场景

| 场景 | 原因 |
|------|------|
| 内部开发工具 | 工程师能忍受粗糙的边缘 |
| 一次性 prototype | 先出货再补强 |
| 只读 debug 工具 | Blast radius 小 |

---

## 验证 → 恢复的 Loop

这是本课最重要的产品概念：

```
Claude 用坏输入调用 tool
       ↓
Tool 抛出描述性错误
       ↓
错误变成 tool_result（is_error=True）
       ↓
Claude 下一轮读到错误
       ↓
Claude 带着修正后的输入重试
       ↓
成功 — 用户从未看到失败
```

从用户角度看，这个 loop 是隐形的。他们只看到「成功了」。但链上任何一环断掉（错误消息含糊、没有捕捉异常、静默失败），整段就会塌成可见的错误。

PM 应该把「tool 错误恢复」明确写进 AI 功能的 PRD acceptance criteria。

---

## PM 决策框架

规划 tool-using 功能时，文档上要写清楚：

| 项目 | 为什么重要 |
|------|----------|
| Tool 名称与清楚的用途描述 | 影响 Claude 选 tool 的准确度 |
| 每个参数的允许值与格式 | 避免默默的垃圾输出 |
| 非法输入会发生什么事 | 定义恢复 UX |
| 若恢复失败，会给用户看什么消息 | 用户面向的文案需要 PM 审核 |
| 副作用与 idempotency | 决定重试是否安全 |
| 可观测性 hook（log、metric） | 为生产 debug 做准备 |

---

## PM 常犯的错

1. **把 tool function 当成「纯工程」** — 跳过设计 review 导致命名、验证、错误消息不一致。
2. **没在 PRD 写错误消息** — 工程师最后写给开发者看的错误，Claude（与用户）都无法用来恢复。
3. **忽略 idempotency** — 若 Claude 因错误重试 create-reminder，你会多一笔提醒。PRD 应指定去重行为。
4. **低估名字的影响** — 「set_reminder」vs.「create_reminder」vs.「reminder」看似可互换，实际上会改变 Claude 选对 tool 的概率。
5. **没有可观测性** — 没 log tool call 与结果，生产失败无法 debug、功能可靠度也无从测量。

> **Key Insight**
>
> Tool function 质量不是实现细节 — 它直接决定你 AI 功能的可靠度与 UX。你工程团队写的错误消息，Claude 每次重试都会读到，所以实际上是你产品文案的一部分。把 tool function review 当成 PRD 等级的事情来处理的 PM，会做出明显更可靠的功能。CCA D2 直接测这一点。

---

## CCA 考试重点

- **D2（Tool Design & MCP Integration）**：Tool 命名、验证、错误处理作为恢复信号、idempotency 顾虑。
- **D1（Agentic Architecture）**：错误如何透过 agent loop 流回并让 Claude 自我修正。
- 预期会出「含糊错误」vs.「描述性错误」结果的对比题 — 描述性永远胜出。

---

## Flashcards

| Front | Back |
|-------|------|
| Tool function 的餐厅比喻是什么？ | Tool function 是线上厨师、Claude 是服务员、schema 是食谱卡、错误消息是厨师对服务员喊回去的话。 |
| 为什么错误消息对 PM 而不只是工程师重要？ | 因为 Claude 重试时会读它 — 错误消息的质量决定用户是看到可见失败还是无感恢复。 |
| Tool-using 功能的 PRD 应该写什么？ | Tool 名称与用途、参数验证规则、错误恢复 UX、用户面向的错误文案、副作用/idempotency 规则、可观测性 hook。 |
| 什么是验证-恢复 loop？ | 坏输入 → 描述性错误 → tool_result with is_error → Claude 重新规划 → 修正后重试 → 用户从未看到失败。 |
| 为什么写入型 tool 的 idempotency 是 PM 的事？ | Claude 可能在错误后重试；没有 idempotency 就会重复写入，例如一次请求产生两笔同样的提醒。 |
| 含糊的 tool 名字会造成什么用户可见症状？ | Claude 挑错 tool，功能做错事 — 用户看到自信的胡说八道。 |
| PM 在 tool function 设计 review 的角色是什么？ | 确保命名、验证、错误文案、恢复 UX 都在 PRD 里明确定义并于实现前 review。 |
| 什么时候投入大量 tool function 设计是过度设计？ | 内部开发工具、一次性 prototype、只读 debug 工具，blast radius 小。 |
