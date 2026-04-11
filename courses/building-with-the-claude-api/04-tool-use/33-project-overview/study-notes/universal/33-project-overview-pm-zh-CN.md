# 项目概览：提醒应用 — PM Perspective

| 项目 | 内容 |
|------|------|
| 考试 Domain | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.1（tool schema 设计）、1.2（agentic loop 基础）、1.1（功能拆解） |
| 来源 | building-with-the-claude-api / 04-tool-use / Lesson 33 |

---

## 一句话总结

三个字的用户需求（「下周四提醒我」）底下藏着三个不同的产品能力缺口 — 正确的 AI 产品架构是**每个缺口配一个 tool**，而不是做一个「全能魔法函数」。

---

## 「提醒我」的假性简单

PRD 上可能这样写：

> *作为用户，我可以说「下下个星期四提醒我某件事」，助手会帮我设好提醒。*

所有 stakeholder 点头。两句话的 user story。两天的 ticket 吧？

不是。底层模型不会：

1. 知道此刻精确时间（只知道大概日期）
2. 可靠地做日期运算（LLM 算星期几出错频率超乎想象）
3. 把提醒存到任何地方

每一条都是不同的问题，都要自己的组件。这是 PM 在 scope AI 功能时最常踩的雷：表面是一句话，底下的能力图是一棵树。

---

## 心智模型：乐高 vs. 手办

| 方法 | 比喻 | v1 出货速度 | 长期杠杆 |
|------|------|-------------|----------|
| 一个「全做完」的大函数 | 手办 — 塑到固定的姿势 | 快 | 零复用、难修 |
| 小小的原子 tool，由 Claude 组合 | 乐高 — 积木 | 稍慢 | 未来任何功能都能复用 |

Tool use 奖励乐高派。第一次做 `add_duration_to_datetime` 时你付出成本。之后任何碰到「提醒我 N 天后」「N 周后截止」「下季再订」的功能都能免费复用同一块积木。

---

## 三个缺口 → 三个 Tool

| 用户信号 | 暴露的缺口 | 该做的 tool |
|-----------|------------|-------------|
| 「现在」 | Claude 不知道精确时间 | Get current datetime |
| 「下下个星期四」 | Claude 日期运算不可靠 | Add duration to datetime |
| 「提醒我」 | Claude 没有提醒系统 | Set reminder |

每一行都是 PRD 里的决策点。每个 tool 都有自己的 acceptance criteria、失败模式、遥测需求。

---

## 为什么这对 Roadmap 规划很重要

因为 tool 可以复用，所以帮提醒功能做 scoping 的同时，你也帮**未来好几个功能**做了 scoping：

- 生日提醒（三个 tool 全部复用）
- 截止日追踪（复用其中两个）
- 周期性会议（复用其中两个）
- 假期倒数（复用其中两个）
- 「N 周后是几号」类的问答（复用其中两个）

看到这个模式的 PM 可以把功能卖给 stakeholder 说「我们是在打排期系统的地基」，而不是「我们做了个玩具提醒 app」。ROI 算盘完全翻转。

---

## 把构建顺序当作风险管理工具

课程是最简单的先做：

1. Read-only 先做（get current datetime）— 坏了影响最小。
2. Pure function 第二（add duration）— 确定性、可单测。
3. Write operation 最后（set reminder）— 有真实世界副作用，有真实风险。

对 PM 而言，这也是 dogfood 的顺序。先内部出第一个 tool、再第二个，只有两个依赖都稳了才出写入型 tool。每个阶段都可上线。

---

## PM 决策框架

看到「听起来很简单」的 user story 就问：

| 问题 | 若是 | 行动 |
|------|------|------|
| 需要此刻的数据吗？ | 是 | 规划一个 tool。 |
| 需要 LLM 不擅长的运算（日期、金额、距离）吗？ | 是 | 规划一个 tool。 |
| 需要把状态持久化？ | 是 | 规划一个 tool。 |
| 这几个 tool 在其他功能用得到？ | 是 | 提升优先级 — 是地基。 |
| Stakeholder 以为「这很简单、一个 call 就够」？ | 是 | 跟他一起跑这个 gap 分析。 |

---

## PM 常犯的错

1. **误判 scope** — 「提醒我」听起来两天的 ticket，实际上是三个 tool 加一个 agent loop。排期要对应调整。
2. **在压力下 bundling** — stakeholder 会说「做一个全包函数就好」。抗住，长期成本远高。
3. **没营销复用价值** — 没把地基工作包装好，会让人觉得是过度工程一个小功能。
4. **跳过玩具项目** — 把这个 pattern 直接用在高风险功能上，等于把学习曲线推到生产环境。
5. **没为 multi-turn loop 设计 loading state** — 三次 tool call 加三次 API call 会叠出好几秒的延迟，得先设计好。

> **Key Insight**
>
> 提醒项目是 AI 产品管理「冰山」问题最清楚的范例：听起来琐碎的 user story 底下坐着多个截然不同的能力缺口。正确的回应是每个缺口配一个 tool — 因为每个 tool 都会变成未来功能的可复用资产。CCA 考试会出「如何把自然语言功能拆成 tool」类型的题目。

---

## CCA 考试重点

- **D1（Agentic Architecture）**：认知一次用户输入可能触发多次 tool call，顺序由 Claude 规划。
- **D2（Tool Design & MCP Integration）**：「一个缺口一个 tool」的设计原则会被直接测。
- 考题常见模式：给一个功能（「提醒我」「总结今天」「订会议」），要你辨认出最少需要的 tool 集合。

---

## Flashcards

| Front | Back |
|-------|------|
| AI 产品 scoping 的「冰山」陷阱是什么？ | 一句话的 user story（「下周四提醒我」）底下藏多个不同的能力缺口；正确 scope 是每个缺口配一个 tool。 |
| 为什么提醒 app 是好的首个项目？ | 它用一个友善的故事示范实际的多 tool 组合，风险逐步升级（read-only → pure function → write）。 |
| 乐高 vs. 手办的比喻是什么？ | 原子 tool 像乐高积木（跨功能复用）；大函数像手办（一次性、无复用）。 |
| 提醒 app 的 tool 可以在哪些未来功能被复用？ | 生日提醒、截止日追踪、周期性会议、假期倒数、「N 周后是几号」问答。 |
| 这个项目建议的 tool 构建顺序是？ | Read-only 先、pure function 第二、write/有副作用最后 — 风险梯度。 |
| Scoping「提醒我」类功能时 PM 第一个常犯的错是？ | 估错大小 — 以为是简单 ticket，实际上是三个 tool 加 multi-turn loop。 |
| 为什么要替这类功能预算 loading state？ | 多次 tool call 加 API round trip 很容易叠出好几秒延迟。 |
| 如何把地基 tool 工作卖给 stakeholder？ | 包装成「为一整家族的未来功能打地基」，而不是「做玩具提醒 app」。 |
