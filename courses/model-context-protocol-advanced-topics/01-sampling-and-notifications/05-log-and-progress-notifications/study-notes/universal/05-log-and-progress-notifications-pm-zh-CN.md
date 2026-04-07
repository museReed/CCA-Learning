# Log and Progress Notifications — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server capabilities), 2.5 (server-to-client communication) |
| Source | model-context-protocol-advanced-topics / 01-sampling-and-notifications / Lesson 05 |

---

## One-Liner

MCP server 可以在长时间操作中发送实时状态更新和进度指示器给 client，将沉默的黑箱处理转变为透明、友好的用户体验。

---

## 心智模型：餐厅厨房

把 MCP tool 想成餐厅厨房：

| 没有 Notification | 有 Notification |
|------------------|-----------------|
| 你点餐后沉默等待 | 服务员说「您的前菜正在准备」 |
| 过了 20 分钟 — 菜要来了吗？ | 「主菜正在烤箱里，还要 10 分钟」 |
| 你考虑离开 | 「正在摆盘 — 马上好！」 |
| 菜来了（或没来） | 菜来了，而且全程都有被告知 |

Notification 不改变食物，改变的是 **用餐体验**。

---

## 两种实时反馈类型

| 类型 | 功能 | 类比 |
|------|------|------|
| **Logging** | 处理中的状态消息（「搜索数据库中...」「找到 42 条结果」） | 服务员的口头更新 |
| **Progress** | 完成百分比（30%、60%、90%） | 外卖追踪页的进度条 |

两者都是 **可选的** — tool 没有它们也能运作。但它们大幅改善感知性能和用户信任。

---

## PM 为什么要关心

### 1. 用户的速度感知

研究一致显示，有进度指示器的任务感觉比没有的更快，即使花费相同时间。对于可能跑 10-60 秒的 AI 工具，这至关重要。

### 2. 降低放弃率

用户在长时间操作中没有看到反馈时会：
- 认为工具坏了
- 重试（产生重复工作）
- 完全放弃工作流程

### 3. 调试和支持

Logging 让你的支持团队能看到失败操作中发生了什么，不需要请用户重现问题。

---

## 产品设计考量

撰写 MCP tool 需求时，考虑：

| Tool 耗时 | 建议 UX |
|-----------|---------|
| < 2 秒 | 不需要 notification |
| 2-10 秒 | Logging 消息（「搜索中...」「处理中...」） |
| 10-60 秒 | Logging + 进度条 |
| > 60 秒 | Logging + 进度 + 考虑拆成更小步骤 |

---

## Client 呈现灵活性

Server 发送原始数据，不同 client 有不同呈现方式：

| Client 类型 | Logging 呈现 | Progress 呈现 |
|------------|-------------|--------------|
| Terminal/CLI | stdout 文字行 | ASCII 进度条 |
| Web app | Toast 通知或 log panel | HTML/CSS 进度条 |
| Desktop app | 系统通知区域 | 原生 OS 进度环 |
| 聊天界面 | 行内状态消息 | 动态加载指示器 |

> **Key Insight**
> 作为 PM，你指定 **沟通什么信息**（步骤、百分比、警告）。你 **不需要** 指定 **怎么显示** — 那是 client 的责任。这种关注点分离意味着一个设计良好的 server 在所有 client 类型上都能表现出色。

---

## Notification 是 Fire-and-Forget

PM 需要理解的关键架构细节：

- Notification 是 **单向的**：server 发送，不等待确认
- Client 忽略它们也不会坏
- **不影响** tool 的实际输出
- 对处理时间增加的额外开销极小

这意味着你永远可以建议加上 notification — 没有缺点。

---

## 错误沟通策略

Logging level 对应用户面向的沟通层级：

| Level | 何时使用 | 用户体验 |
|-------|---------|-----------|
| Debug | 内部细节（URL、记录数） | 通常不显示给终端用户 |
| Info | 主要里程碑（「步骤 2/4 完成」） | 作为状态显示给用户 |
| Warning | 性能降低（「大型数据集，可能较慢」） | 提醒 — 用户可决定是否等待 |
| Error | 失败（「数据库连接中断」） | 错误消息 — 用户采取行动 |

---

## CCA Exam Relevance

- **D2 Task 2.3**：Server capabilities — notification 在设计良好的 server 中是预期的
- **D2 Task 2.5**：Server-to-client communication — logging 和 progress 是主要范例
- 考试测试理解 notification 是单向的（非 request-response）
- 核心哲学：**好的 UX 不是可选项** — 即使基础设施 tool 也应沟通状态

---

## Flashcards

| Front | Back |
|-------|------|
| MCP server 可以发送哪两种实时反馈？ | Logging（状态消息）和 Progress（完成百分比） |
| MCP notification 是 tool 功能必需的吗？ | 不是 — 可选但强烈建议用于 UX |
| Client 忽略 notification 会怎样？ | 不会坏 — notification 是 fire-and-forget |
| 为什么进度指示器对 AI 工具很重要？ | 有进度反馈的任务用户感觉更快，也更不容易放弃 |
| 谁决定 notification 怎么显示？ | Client — server 发送原始数据，每个 client 适当渲染 |
| PM 在什么 tool 耗时下应建议加 notification？ | 超过 2 秒的操作 |
| 四个 logging level 是什么？ | Debug（内部）、Info（里程碑）、Warning（降级）、Error（失败） |
| Notification 可以改变 tool 的返回值吗？ | 不可以 — 纯粹是信息性的旁路沟通 |
