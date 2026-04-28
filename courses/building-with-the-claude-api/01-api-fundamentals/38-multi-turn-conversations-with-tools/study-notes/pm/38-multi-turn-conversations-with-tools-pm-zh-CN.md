# Multi-Turn Conversations with Tools — PM Perspective（简中）

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture (22%) / D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 1.3（multi-turn conversation management）、1.2（agentic loop 实现）、2.4（multi-turn tool loops） |
| 来源 | building-with-the-claude-api / 01-api-fundamentals / Lesson 38 |

---

## 一句话总结

Multi-turn tool 对话解锁了「Claude 可以帮我调用一个 API」和「Claude 可以规划、执行、串联多个动作解决真实用户问题」之间的差距——而工程成本是写一个 loop，不是整个重写。

---

## 心智模型：生产线上的工人

把 Claude 想成一个聪明的生产线工人，工作台上放着各种专门工具：

| 单回合 tool | Multi-turn tool |
|------------|-----------------|
| 工人拿一样工具、用完、放回去 | 工人拿工具 A、看结果、拿工具 B、看结果、一直到完成 |
| 主管（你的代码）交还一个结果 | 主管交还每一个结果，工人决定下一步 |
| 任务：「量这个零件」 | 任务：「确认这个零件尺寸对——量它、对规格、必要时调整」 |

工人不会事先规划每一次 tool 调用。他们看当前结果、决定下一步。你代码的工作就是每次工人要求新动作时，把正确的 tool 结果交回去——直到工人最后交出完成品。

---

## 为什么产品要在乎

Multi-turn tool 对话是 **agent 类功能** 的栖息地。没有它，Claude 基本上只是个装了一个函数的高级 autocomplete。有了它，Claude 变成能：

| 能力 | 示例 |
|------|------|
| 串联依赖操作 | 「订机票然后加进日历」 |
| 先看再做 | 「查天气，再决定要不要订户外餐厅」 |
| 迭代优化 | 「搜索产品、按评分筛、买评分最高的那个」 |
| 错误恢复 | 「如果那个 API 挂了，试备用 API」 |

每一个都是高杠杆的产品能力，单次 tool 调用做不到。Multi-turn loop 是从「AI 功能」走向「AI agent」的门槛。

---

## 产品应用场景

### 非要 Multi-Turn 不可的时候

| 场景 | 为什么要 Multi-Turn |
|------|---------------------|
| 「帮我规划京都旅行」 | 需要序列决策（日期 → 酒店 → 机票 → 活动） |
| 「Debug 这段代码的错误」 | 读文件 → 找问题 → 改 → 验证 |
| 「帮我总结最近 30 封邮件」 | 抓列表 → 抓每封邮件 → 综合 |
| 「找 500 万以下、学区好的房子」 | 搜索房源 → 抓学校评分 → 筛选 → 排序 |

### 单回合就够的时候

| 场景 | 为什么单回合 |
|------|--------------|
| 「今天几号？」 | 一次 tool 调用就结束 |
| 「翻译这段」 | 纯模型操作，根本不用 tool |
| 「给我一个优惠码」 | 单次查询 |

PM 的经验法则：**如果答案需要「先做 X，再根据结果做 Y」，就需要 multi-turn。**

---

## PM 决策框架

规划 multi-turn tool 功能之前，先回答这些：

| 问题 | 为什么重要 |
|------|-----------|
| 最多允许跑几次迭代？ | 延迟、成本、安全边界——用户不能无限等 |
| 迭代中间如何向用户显示进度？ | 好几秒的空白画面会毁掉感知质量 |
| 中途 tool 失败怎么办？ | 需要优雅降级策略 |
| Token 成本预算怎么算？ | 每个回合都会让历史变长，长 loop 很贵 |
| Loop 的观测性怎么做？ | 生产环境 debug 需要看到每个回合 |
| 用户可以打断 loop 吗？ | 没有取消按钮的长 loop 是敌意 UX |

---

## 常见 PM 错误

1. **以为 shipping 了第一个 tool 之后「agent」就免费**——从单回合变多回合需要真正的 loop 实现、错误处理、成本控制
2. **Loop 期间没有进度指示**——用户看到 spinner 会以为产品坏了；要把每一步显示出来
3. **没有 max_iterations 上限**——搞混的 Claude 或坏掉的 tool 会无限 loop；跳过这个的 PM 会 ship 一张失控 token 账单
4. **没预算更长的延迟**——multi-turn 一定比单回合慢，因为每次 tool 调用都是一趟 round trip
5. **忽略部分结果**——loop 撞到上限时，要显示「不完整」结果还是装没事？这是产品决策不是工程决策

---

> **Key Insight**
>
> Multi-turn tool 对话是产品层级对 agent 的定义。技术成本很小——一个 `while` loop 加更好的 helper function——但产品影响很大：延迟预算、进度 UX、取消、token 成本、观测性全部都变成一线议题。把「让这个功能支持 multi-turn」当成产品里程碑，不是一个 tech spike。

---

## CCA Exam Relevance

- **D1（Agentic Architecture）**：Multi-turn tool 对话是典型的 agentic loop。考题会问什么时候用、跟单回合调用怎么差。
- **D2（Tool Design & MCP Integration）**：记住 tool schema 必须在每次迭代都带上。
- 考题描述「依赖链的 tool 调用」的情境——答案几乎永远是「实现对话 loop」。

---

## Flashcards

| 题目 | 答案 |
|------|------|
| 用什么生产线比喻来理解 multi-turn tool 对话？ | 一个聪明的工人一次拿一样工具、看每个结果、决定下一步 |
| Agent 的产品层级定义是什么？ | 支持 multi-turn tool 对话的功能——串联、依赖推理 |
| 什么时候必须用 multi-turn 而不是单回合？ | 当答案需要「先做 X 再根据 X 的结果做 Y」——规划、迭代、错误恢复 |
| Multi-turn tool 功能最大的隐藏成本是什么？ | 延迟——每次 tool 调用多一趟 round trip，感觉比单回合慢 |
| Multi-turn 功能为什么需要 max_iterations 上限？ | 防止失控 loop 烧光 token、永远卡住 UI |
| Multi-turn loop 期间最重要的 UX 元素是什么？ | 进度指示——把每个步骤显示出来，否则用户会以为产品坏了 |
| Multi-turn 引入了哪些产品决策？ | 迭代上限、进度 UX、取消、token 预算、观测性 |
| 为什么不能直接 reuse 单回合 tool 实现？ | 单回合 tooling 不保留历史、不管理 stop_reason、不处理一个 response 多个 tool 调用 |
