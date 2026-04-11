# Workflows vs Agents — Engineering 深度解析

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture (22%);D5 — Enterprise Deployment (20%) |
| Task Statements | 1.1 (agent vs workflow 架构)、1.2 (agentic loop)、5.1 (production pattern 选型) |
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 83 |

---

## 一句话总结

**默认选 workflow,真的不得已才升级到 agent** —— Workflow 对已知问题给你可靠度和可预测性,agent 对开放问题给你灵活性,工程师的工作就是挑能解决用户问题的最便宜 pattern。

---

## 定义

### Workflow

**一连串预先定义的 Claude 调用**,解决已知问题。开发者把控制流写死:"先用 model A 分类,再用 model B 起草,再用 model C review。"每个调用的工作都很窄。

```python
def summarize_ticket(ticket):
    category = classify(ticket)               # Step 1
    summary = summarize(ticket, category)     # Step 2
    priority = score_priority(summary)        # Step 3
    return {"category": category, "summary": summary, "priority": priority}
```

### Agent

**目标 + 工具集** 交给 Claude,runtime 由它决定调用什么、什么顺序。没有写死的序列。

```python
messages = [{"role": "user", "content": user_goal}]
while True:
    response = client.messages.create(model="claude-sonnet-4-5", tools=tools, messages=messages)
    if response.stop_reason == "end_turn": break
    # 处理 tool_use,loop 继续
```

差异在于 **控制流由谁拥有**:开发者(workflow)还是 Claude(agent)。

---

## 完整比较表

| 维度 | Workflow | Agent |
|------|----------|-------|
| **灵活性** | 低 — 只处理你写死的形状 | 高 — 组合 tools 处理新情境 |
| **可靠度** | 高 — 每步都窄、都经测试 | 较低 — 开放式规划可能出错 |
| **每任务成本** | 低 — token 数可预测、可 cache | 高 — 多次 loop 迭代、更多 token |
| **Latency** | 低 — 固定次数的顺序调用 | 变动 — 看 Claude 跑几次 loop |
| **Debuggability** | 高 — 你知道哪一步失败 | 低 — 轨迹不确定、难以重现 |
| **可预测性** | 高 — 相同输入永远相同序列 | 低 — Claude 对相似输入可能选不同 tool 链 |
| **Eval 成本** | 中等 — 逐步单元测试 | 高 — 必须 eval emergent 行为,需更多测试案例 |
| **Upfront design 成本** | 高 — 必须列出全部流程 | 较低 — 设计工具箱而非流程 |
| **最佳使用情境** | 摘要、分类、抽取、翻译、合规流程 | 编码助手、创意内容、混乱数据上的开放问答 |
| **最差使用情境** | 开放或多变的用户请求 | 有已知序列的窄重复任务 |

---

## 来源原文的优缺点

### Workflow 优点

- Claude 一次只关注一个子任务,通常准确度更高
- 更容易 eval 和测试——你知道每一步
- 执行更可预测、更可靠
- 适合解决定义良好的问题

### Workflow 缺点

- 灵活性低很多——只能解特定任务类型
- UX 较受限——你必须知道精确输入
- 需要更多前期规划和设计工作

### Agent 优点

- 更灵活的 UX
- 可以用没预期的方式组合 tool
- 能处理设计时没想到的新情境
- 需要时可以问用户补充信息

### Agent 缺点

- 任务完成率比 workflow 低
- 较难 instrument、测试、eval
- 行为较不可预测

---

## 决策框架

Anthropic 的建议很直白:**默认 workflow。只有 workflow 真的解不了的问题才用 agent。**

每个 AI 功能都走这个 checklist:

```
1. 我能事先列出所有用户流程吗?
   YES -> workflow
   NO  -> 继续

2. 这个任务是纯转换(input -> output)没有分支吗?
   YES -> workflow
   NO  -> 继续

3. 用户的请求会用多元、不可预测的方式表达吗?
   YES -> 继续评估 agent
   NO  -> workflow

4. 正确动作取决于当前环境 state 吗?
   YES -> agent(搭配 environment inspection)
   NO  -> workflow

5. 我负担得起 agent 的 cost、latency、eval 复杂度吗?
   YES -> agent
   NO  -> 拆成更小的 workflow
```

这不是纯粹主义测试——混合系统存在。常见 pattern:外层是 workflow,路由到内层 agent 处理灵活步骤,其余用 workflow 作护栏。

---

## Cost 和 Latency 数学

一个 workflow 有 3 个固定 model 调用,每个 ~1000 tokens:

- **Tokens**:每任务 ~3000(deterministic)
- **Latency**:3 次顺序调用,总共 ~3-6 秒
- **Cost**:可预测、可用 prompt caching cache

同样任务用 agent 解,3-10 次 loop 迭代:

- **Tokens**:每任务 ~3000 到 ~30000(变动)
- **Latency**:3-10 次 round trip,总共 ~5-30 秒
- **Cost**:同样输出质量下是 workflow 的 1x 到 10x

如果 eval 显示 workflow 95% 准确、agent 96% 准确,agent 的灵活性大概不值那 5-10x 的 cost 倍数。挑能达到质量门槛的最便宜 pattern。

---

## Production 里的混合 Pattern

真实 production 系统很少只选一种。常见混合:

| Pattern | 运作方式 | 例子 |
|---------|---------|------|
| **Workflow 路由到 agent** | 便宜的分类 workflow 决定请求是否需要 agent 级别灵活性 | Support ticket router:FAQ -> workflow,新 bug -> agent |
| **Agent 带 workflow sub-step** | Agent 把 workflow 当成一个 tool 调用 | 编码 agent 调用 deterministic "run_tests" workflow |
| **Agent 带 workflow 安全闸门** | Agent 提出动作,workflow 执行前验证 | AI 交易员提案,workflow 检查合规规则 |
| **失败升级** | 先 workflow 失败再 agent | 结构化数据抽取,schema 变动时回退到 agent |

这些 pattern 让你对 80% 流量保持 workflow 的可靠度,同时保留 agent 灵活性给难搞的 20%。

---

## 常见错误

1. **Agent-washing** — 因为 agent 听起来潮就把所有东西做成 agent,然后接下来整个项目周期都在跟 cost 和 eval 打架。
2. **Workflow 僵化** — 把每个变异都塞成 if-tree 的一条分支,最后变成无法维护的意大利面。这就是该升级到 agent 的时候。
3. **Agent 跳过 eval** — 因为 agent 轨迹变动,你需要 **更大更多元** 的 eval set,不是更小。
4. **忽略 latency 税** — 每次 agent loop 都是一次 round trip。话多的 agent 即使每个调用都很快,整体感觉就是慢。
5. **没量每成功任务的 cost** — "每次调用的 token 数"是错的 metric;"每次验证成功的 cost"才是重点。

> **Key Insight**
>
> Anthropic 的建议很利落:默认 workflow,只有无法事先决定步骤时才选 agent。用户不在乎你做了个聪明的 agent,他们只在乎产品稳定好用。把 pattern 对齐到问题(而且诚实面对你实际有的是哪种)是 agentic 产品里最高杠杆的架构决策。

---

## CCA 考试关联

- **D1 (Agentic Coding & Architecture)**:会考"什么时候用 agent vs workflow"。背熟 trade-off 表。
- **D5 (Enterprise Deployment)**:Cost、latency、eval 复杂度、debuggability 是面对 production 的 trade-off。每个轴该知道哪个 pattern 胜出。
- 考题提示字:"varied requests""unpredictable""combine tools creatively" -> agent;"well-defined steps""known flow""compliance""cheapest predictable" -> workflow。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Anthropic 的默认建议是什么? | 默认用 workflow;只有 workflow 解不了的问题才用 agent。 |
| Workflow 跟 agent 的控制流由谁拥有? | Workflow:开发者写死序列。Agent:Claude 在 runtime 决定序列。 |
| 列出三个 workflow 胜 agent 的维度。 | 可靠度、cost、latency、debuggability、可预测性(任三)。 |
| 列出三个 agent 胜 workflow 的维度。 | 灵活性、新情境覆盖、用户驱动对话 UX、较低 upfront design cost(任三)。 |
| 为什么 agent 比 workflow 难 eval? | Agent 轨迹不确定——你不能单步测试;必须对大量案例测 emergent 行为。 |
| 举一个混合 pattern 把两者结合。 | Workflow router 把简单案例送到 workflow 分支,难案例送到 agent。 |
| 比"每次调用 token 数"更重要的 cost metric 是什么? | 每次验证成功的 cost——agent 用更多 token 但若能解 workflow 解不了的案例,每成功 cost 反而可能更低。 |
| 决策框架的第一个问题是什么? | 我能事先列出所有用户流程吗?能 -> workflow。 |
