# 使用多个 Tools — PM Perspective

| 项目 | 内容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%)、D1 — Agentic Architecture (22%) |
| Task Statements | 2.1（tool schema 与选择）、1.2（tool 编排） |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 40 |

---

## One-Liner

让 Claude 拥有多个 tools,就像请了一个通才,然后给他一条挂满专用工具的腰带——每新增一项能力都能立刻和已有能力组合,核心产品不用重写。

---

## Mental Model：瑞士军刀

单 tool 的 agent 是螺丝刀;多 tool 的 agent 是瑞士军刀。有趣的产品行为来自**组合**：

| 组件 | 单独使用 | 与其他组合 |
|------|---------|-----------|
| 查日程 | "我今天有什么安排？" | "把我下午 3 点的会议移到 4 点会议结束之后" |
| 日期运算 | "30 天后是几号？" | "合同签订后 2 周安排一次 follow-up" |
| 提醒 | "周五提醒我" | "护照到期前 3 天提醒我" |

用户很少只做单 tool 的动作,真实需求都是组合的——所以你的 tool catalog 也必须能组合。

---

## Product Use Cases

### 什么时候该加新 Tool

| 场景 | 为什么需要多个 tool |
|------|--------------------|
| 排程助手 | 需要日期运算 + 日历 + 提醒 + 通知一起工作 |
| 研究 copilot | 需要 web search + 文档检索 + 摘要 + 引用 |
| 客服 agent | 需要 ticket 查询 + 知识库搜索 + 升级 |
| DevOps 助手 | 需要 log 查询 + metric 查询 + runbook + incident 创建 |

### 什么时候该忍住不加

| 反模式 | 更好的做法 |
|--------|-----------|
| "以防万一"先加个 tool | 等到有具体用户需求再加;砍掉没用的 |
| 暴露 20+ 个窄的 tool,让 Claude 选 | 合并成较少、更丰富、带参数的 tool |
| 重复创建行为相似的 tool | 每个能力只保留一个标准 tool |

多一个 tool 的成本不是零:更多 tool 就是每个请求都要多塞 token、Claude 更容易选错、维护成本也更高。

---

## PM Decision Framework

规划 tool catalog 成长时,问以下问题：

| 问题 | 如果 Yes | 行动 |
|------|---------|------|
| 有真实用户需求需要串联 tool 吗？ | Yes | 补上缺的能力 |
| 现有的两个 tool description 有重叠吗？ | Yes | 合并或澄清 |
| 这个新 tool 单独使用也有价值吗？ | Yes | 上线 |
| 加进去会让总数超过 15-20 个吗？ | Yes | 考虑改用 MCP server 分组 |
| 能用改写现有 tool description 解决吗？ | Yes | 先改 description |

---

## 组合原则

Tool 能链式组合时,产品价值会复利增长：

- **1 个 tool** → 价值 = N
- **3 个 tool** → 价值 ≈ 3N + 组合数
- **10 个 tool** → 价值随着有用的组合数增长,而不是 tool 的总数

这就是 Slack、Zapier、IFTTT 成功的原因——平台在拥有足够多 primitive 可以组合出有意义的 workflow 时才变得有价值。你的 AI 产品也遵循相同的 S 曲线：前期慢、然后在组合能力达成时急速转折。

---

## Claude 如何选 Tool（PM 能怎么影响）

Claude 读取每个 tool 的 **description** 并挑最匹配的那个。PM 可以通过以下方式改善准确度：

1. **写动作导向的祈使句描述** — "Creates a reminder at a specific datetime" 胜过 "Reminder utility"
2. **标注使用限制** — "Use only for dates in the future" 可以防止误用
3. **避免重叠** — 两个 tool 能做类似的事,Claude 会随机选一个,应该合并
4. **用真实用户的说法测试** — 翻真实对话记录,确认正确的 tool 会被触发

Description 就是产品表面,请用跟按钮文字、empty state 一样的严谨度对待它。

---

## Common PM Mistakes

1. **把 tool description 当成随便写的 docstring** — 它是 Claude 选择的主要信号,请像 UX copy 一样投入。
2. **上线第一天就推出庞大的 tool catalog** — 从 2-3 个开始,观察使用情况,根据真实需求扩充。
3. **没有追踪 Claude 实际选了哪个 tool** — 没测量就无法优化,请记录 tool selection 事件。
4. **忽略 parallel vs. sequential 的成本差异** — parallel 调用是一次 API round-trip,sequential chain 是多次,延迟会累积。
5. **以为 tool 越多代表能力越强** — 能力来自"有用的组合",不是 catalog 大小。

> **Key Insight**
>
> Multi-tool agent 的产品价值来自**组合**,不是来自 tool 数量。每一个新 tool 都必须证明自己能解锁现有 tool 做不到的链式 workflow。CCA 考试的核心概念:tool 选择是 model-controlled 的,由 description 质量驱动,不是列表中的顺序。

---

## CCA Exam Relevance

- **D2 (Tool Design)**：理解 Claude 基于 schema name + description 选 tool,写得好的 description 是准确度的主要杠杆。
- **D1 (Agentic Architecture)**：理解 parallel vs. sequential tool execution 以及它们共用的 agentic loop。
- 场景题常给一个拥有 3-5 个 tool 的 agent,问某个用户请求会触发哪个——答案是由 description 的匹配度决定。

---

## Flashcards

| Front | Back |
|-------|------|
| Multi-tool agent 为什么比 single-tool 有价值？ | 组合——价值来自有用的 chain-workflow 数量,不是 tool 总数 |
| Claude 如何决定要调用哪个 tool？ | 将用户请求与每个 tool 的 name 和 description 做匹配 |
| PM 能改善 tool selection 准确度的主要杠杆？ | 写动作导向、祈使句形式的 description;避免 tool 之间重叠 |
| 为什么 PM 不该"以防万一"就加 tool？ | 多余的 tool 吃 token、让选择出错、增加维护成本;要有真实需求才加 |
| 暴露 20+ 个窄 tool 的风险是什么？ | Claude 要从更多选项中挑,准确度下降,token 成本升高 |
| parallel 何时比 sequential tool 调用便宜？ | 当 tool 彼此独立时——parallel 是一次 round-trip,sequential 是多次 |
| PM 要追踪什么信号来优化 tool catalog？ | 不同用户说法下 Claude 实际选了哪个 tool,以便调整 description |
| Multi-tool agent 的核心产品心智模型？ | 瑞士军刀——单个 tool 没那么重要,重要的是它们能组合出什么 |
