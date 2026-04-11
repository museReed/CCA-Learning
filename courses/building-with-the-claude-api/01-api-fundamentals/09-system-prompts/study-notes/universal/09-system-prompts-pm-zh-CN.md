# System Prompts — PM 视角

| 项目 | 细节 |
|------|------|
| 考试领域 | D5 — Enterprise Deployment (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 5.1（模型选择与配置）、5.3（production 模式）、1.2（agentic loop 基础） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 09 |

---

## 一句话总结

System prompt 是你在每段对话开始时交给 Claude 的「岗位说明」——它把通用 AI 变成你产品的专属 persona，是 PM 对输出质量与品牌一致性最有杠杆的单一控制点。

---

## 为什么 PM 要在乎

没有 system prompt，你产品里的每个用户都在和同一个通用 Claude 对话——任何人在 Claude.ai 都拿得到。这不是产品，这是一层薄薄的 wrapper。System prompt 才是你差异化的所在。

| 没有 system prompt | 有精心设计的 system prompt |
|--------------------|----------------------------|
| 通用、有帮助但不具体的响应 | 品牌语气、一致的 tone |
| 直接给答案，跳过用户旅程 | 围绕用户目标设计的体验 |
| 跟其他 Claude 集成行为一模一样 | 差异化的产品行为 |
| 没有 guardrails——无关问题照答 | 有范围限制、优雅拒绝 |
| 格式不可预测 | 可靠、可解析的结构 |

数学家教的例子很说明问题。没有引导的话，Claude 对「5x + 2 = 3」会直接给答案。真正的家教产品不要这样——它要的是**教学体验**，不是答案。System prompt 就是你编码「这是家教，不是计算器」的地方。

---

## 心智模型：新人 Onboarding 简报

想象你聘了一位世界级顾问。他很聪明，但第一天对你公司、客户、品牌语气一无所知。你会怎么做？你会给他一份 onboarding 简报：

- 「你是一家企业 SaaS 公司的 lead customer success manager」
- 「我们的 tone 是友善但专业——绝不用 emoji，永远用客户名字署名」
- 「绝不承诺无法验证的时间点」
- 「这是我们最强 CSM 写的三封范例信——照这个风格」

那份简报就是 system prompt。Claude 收到的每个用户查询都是一封新的客户信——简报塑造每封回复的样子。

---

## 产品使用场景

### 什么时候 System Prompt 是关键

| 场景 | 为什么 system prompt 重要 |
|------|---------------------------|
| 客服 chatbot | 品牌语气、升级规则、知识边界 |
| 数学 / 语言家教 | 教学立场（引导而非直接解答） |
| 法律 / 医疗助理 | 硬 guardrails、免责声明、范围限制 |
| Code review 工具 | 技术 persona、严重度标准、输出 schema |
| 内部 HR bot | 以公司政策为真相来源、隐私规则 |

### 什么时候 System Prompt 没那么重要

| 场景 | 原因 |
|------|------|
| 通用 ChatGPT 式 playground | 用户预期看到原味 assistant 行为 |
| 一次性研究查询 | 没有可重复的 workflow 要编码 |
| PMF 前的原型 | 迭代速度胜过 persona 打磨 |

---

## 每个 Production System Prompt 都需要的五件事

1. **身份**——「You are ...」Claude 要扮演谁？
2. **任务范围**——什么在范围内？什么在范围外？
3. **语气 & 格式**——Tone、长度、结构、是否用 markdown
4. **Guardrails**——安全、隐私、法律、品牌的硬规则
5. **示例**——一两个黄金标准输出，锚定风格

如果你的 system prompt 缺了这五个其中任何一个，就有一个质量 bug 在等着发生。

---

## PM 决策框架

在规划新的 AI 功能时，问这些问题：

| 问题 | 如果答 Yes | 含义 |
|------|-----------|------|
| 这个功能有特定 persona 或 role 吗？ | Yes | System prompt——明确定义 |
| 有 Claude 该拒绝的话题吗？ | Yes | System prompt——编码拒绝规则 |
| 有必须的输出格式（JSON、markdown、条列）吗？ | Yes | System prompt——指定结构 |
| 需要品牌语气一致性吗？ | Yes | System prompt——锁定 tone |
| 多轮对话中行为要保持稳定吗？ | Yes | System prompt——持续性 context |
| Context 每个用户 / 每个查询都不同吗？ | Yes | **不是** system prompt——放在 `messages` |

最后一行是大多数 PM 会踩的陷阱：把每位用户的数据塞进 system prompt，因为「指令应该放那」。动态 context 属于 `messages`，不是 `system`——否则你会破坏 prompt caching 并浪费钱。

---

## 常见 PM 错误

1. **把 system prompt 当作一次性产出**——它是产品。版本化、A/B 测试、量化回归。质量下降时，第一个要看的就是 system prompt
2. **写模糊的指令**——「要有帮助又友善」没用。「永远用三个条列回复、总字数不超过 40 字、绝不用惊叹号」才可执行
3. **把动态数据塞进 system prompt**——每位用户的 context 要放 messages，caching 才能生效
4. **没在 PRD 指定 system prompt**——工程师会写一个默认的，而且一定跟你想象的不一样。把 system prompt 列为验收标准
5. **把用户请求复制进「system message」**——system prompt 是环境规则，不是当前任务。混了就不可预测

> **Key Insight**
>
> System prompt 是你唯一能确保 Claude 表现得像*你的*产品，而不是通用 assistant 的地方。它是 PM 在 AI 功能上能拥有的最高杠杆制品——杠杆比 model 选择、temperature、甚至 tool 选择都还大。如果你把它外包给没有产品 context 的工程师写，你的功能就会感觉像 Claude 的 wrapper，而不是产品。

---

## CCA 考试重点

- **D5 (Enterprise Deployment)**：system prompt 是在企业部署中强制行为一致性的标准 production 机制
- **D1 (Agentic Architecture)**：system prompt 是每个 agent 稳定的身份层，贯穿 tool-use loops
- 注意「如何强制品牌语气 / 拒绝规则 / 输出格式？」这种场景——考试答案一定是 system prompt，不是逐条 message engineering

---

## Flashcards

| 题目 | 答案 |
|------|------|
| System prompt 的 PM 级定义是什么？ | 你交给 Claude 的「岗位说明」或 onboarding 简报——定义整段对话的 persona、范围、语气、guardrails |
| Production system prompt 的五个核心元素？ | 身份、任务范围、语气 & 格式、guardrails、示例 |
| 为什么每位用户的数据不该放 system prompt？ | 因为 system prompt 应该稳定且可 cache；每位用户的数据要放 `messages`，caching 才有效且 context 可随 turn 演化 |
| 没写 system prompt 最大的产品风险是什么？ | 你的功能会变成通用 Claude 的薄 wrapper——没有差异化、语气不一致、没有 guardrails |
| 在数学家教产品中，system prompt 防止什么？ | 防止 Claude 直接给答案，强制逐步 Socratic 引导 |
| 「要有帮助」该放进 system prompt 吗？ | 不该——它模糊且没有实际约束。具体、可测试的规则（「永远最多三个条列」）才是能提升质量的 |
| 团队里谁该拥有 system prompt？ | PM——它编码的是产品意图。工程师实现；PM 定义契约、版本化、A/B 测试 |
| System prompt 设计最直接对应 CCA 哪个 domain？ | D5 Enterprise Deployment——它是在规模下强制 production 级一致性的方式 |
