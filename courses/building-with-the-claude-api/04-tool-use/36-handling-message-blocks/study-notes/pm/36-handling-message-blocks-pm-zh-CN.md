# Handling Message Blocks — PM Perspective（简中）

| 项目 | 内容 |
|------|------|
| 考试领域 | D2 — Tool Design & MCP Integration (18%) / D1 — Agentic Architecture (22%) |
| Task Statements | 2.2（content block 处理）、2.1（tool schema 集成）、1.2（agentic loop 基础） |
| 来源 | building-with-the-claude-api / 04-tool-use / Lesson 36 |

---

## 一句话总结

一旦你的产品让 Claude 可以调用 tool，每一条 assistant 回复就会变成一个**结构化的数据包**——一部分是对用户讲的说明，一部分是给机器读的动作请求——系统的工作就是把每一块路由到正确的地方（UI vs 后端执行器）。

---

## 心智模型：无线电调度通信

把启用 tool 后的 Claude 回应想成**警用无线电调度**：

| 部分 | 无线电通话 | Claude 回应 |
|------|------------|-------------|
| 开场说明 | 「12 号车注意…」 | Text block——人类可读的上下文 |
| 可执行指令 | 「请前往 5 街和 Main 街口」 | ToolUseBlock——机器可读的函数调用 |
| 呼号 | 12 号车 | `tool_use_id`——配对请求与响应 |

调度员（你的后端）必须听完整段通信、把说明转述给用户、并把动作派给正确的单位。丢掉任何一块对话就断了。

---

## 为什么产品要在乎这件事

启用 tool 之前，Claude 回应「就是一句话」，可以直接塞进 UI。启用 tool 后，回应是一个**混合 payload**，需要解析：

- 有些部分是给用户看的文字（「我来帮你查时间…」）
- 有些部分是后端动作（「调用 `get_current_datetime` 并带这些参数」）
- 有些部分是看不见的 ID，必须来回送回 Claude

不懂这件事的 PM 会严重低估工程成本：看起来很简单的功能（例如「让 Claude 抓股价」）实际上需要新建一整套 block iteration、ID 跟踪、state 保留的管道。

---

## 产品应用场景

### Multi-Block 处理很重要的时候

| 场景 | 为什么 block 重要 |
|------|-------------------|
| 会查实时数据的助理（天气、股价、日历） | Text block = 用户看到的；ToolUseBlock = 后端调用 |
| 需要串联多个操作的 agentic workflow | 每一回合可能产生多个 ToolUseBlock，你得并行执行 |
| 会一边讲话一边动作的语音/视频助理 | Text block 驱动 TTS，tool-use block 触发实体动作 |
| Debug 或审计功能 | 要给用户看「Claude 正在做什么」就必须把 tool-use intent 暴露出来 |

### 可以保持简单的时候

| 场景 | 更简单的做法 |
|------|--------------|
| 纯静态知识问答 | 不用 tool——单一 text block 就好 |
| 分类／情感分析 | 不用 tool——用结构化 JSON 输出 |
| 创意写作 | 不用 tool——只要 text block |

---

## PM 决策框架

在承诺做一个使用 tool 的功能之前，确认团队能回答：

| 问题 | 为什么重要 |
|------|------------|
| 谁负责把 text-block 的说明露给用户？ | 跳过的话体感会是 Claude「沉默思考」 |
| 如何在回合之间保留完整的 block list？ | 丢 block 会在后续回合引发看不懂的 API 错误 |
| 谁负责 tool_use 和 tool_result 的 ID 配对？ | 必须有一个专职的 layer 来配对请求和响应 |
| 一次响应回来多个 tool call 怎么办？ | 可能要并行执行，不是顺序 |
| tool 执行中间的加载/进度状态如何呈现？ | 长时间工具会让 UX 出现空窗期，没有 progress event 很难收尾 |

---

## 常见 PM 错误

1. **把 tool-use 当成「另一个 API」规划**——它其实是一套新协议：multi-block message、ID 配对、stop_reason dispatch
2. **设计稿忽略说明 block**——设计师常常只画最终答案，漏掉「我正在查…」的前言
3. **假设一回合只会有一个 tool call**——一个问题可能产生 2、3 个 tool-use block，UI 和后端都要能处理并行执行
4. **把 tool-use ID 当成工程内部细节**——它们是与 Claude 的契约。丢了就会坏、会报 400，最后用户会看到
5. **没预算改 helper function**——旧的「加消息到历史」代码通常假设字符串，必须升级

---

> **Key Insight**
>
> 当你把 tool 加进一个由 Claude 驱动的功能，assistant 回复就不再是「一条消息」，而是「一个通信数据包」。产品现在需要一个调度员：能朗读说明、能把动作送给执行器、还能记住呼号。低估这个转变是 tool-use 项目最常见的 overrun 来源。Kickoff 就要跟工程讲清楚：「一旦启用 tool，每一条消息都会变成 typed block list。」

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：知道启用 tool 会把 response shape 从字符串变 block list；记得 ToolUseBlock 的四个字段。
- **D1（Agentic Architecture）**：`stop_reason == "tool_use"` 是 agentic 模式里标准的 loop 继续信号。
- 考题会给一段把 `response.content` 当字符串的代码，问你下一回合为什么会坏。

---

## Flashcards

| 题目 | 答案 |
|------|------|
| 启用 tool 后 Claude 回应的形状变成什么？ | 一个 typed block 的 list（TextBlock、ToolUseBlock），而不是单一字符串 |
| 用什么无线电比喻来理解 multi-block 消息？ | 警用调度通信——开场说明 + 动作指令 + 呼号（ID） |
| PM 规划 tool-use 功能时最大的风险是什么？ | 低估协议转变——multi-block 解析、ID 配对、历史保留 |
| 为什么一定要把说明 text block 显示给用户？ | 否则 Claude 推理时 UX 会沉默，前言上下文也会被丢掉 |
| 哪个 stop_reason 告诉后端要执行 tool 并继续 loop？ | `"tool_use"` |
| 一个 Claude 响应可以有多个 tool-use block 吗？ | 可以——一个问题可能需要多个 tool，系统要全部处理 |
| tool_use_id 为什么不只是工程细节？ | 它们跨 API 调用配对请求与响应，丢了会让后续回合坏掉 |
| 不升级旧 helper function 的产品代价是什么？ | 后续回合会出看不懂的 400，因为先前的 block 被扁平化成字符串 |
