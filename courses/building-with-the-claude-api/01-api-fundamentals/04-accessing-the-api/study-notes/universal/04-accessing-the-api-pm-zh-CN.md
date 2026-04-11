# Accessing the API — PM Perspective（简体中文）

| 项目 | 内容 |
|------|------|
| Exam Domain | D5 — Enterprise Deployment (20%) 主要；D3 — Claude Code Configuration (20%) 次要；D1 — Agentic Architecture (22%) |
| Task Statements | 5.1（model selection）、5.3（production patterns）、3.1（API key 管理）、1.2（agentic loop 基础） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 04 |

---

## One-Liner

产品里每个 Claude feature 其实都是一趟五跳旅程——client、服务器、API、model、回来。搞懂这五跳的 PM 才能在延迟、成本、安全、失败 UX 之间做出聪明的权衡。

---

## Mental Model：机场转机

把 Claude 请求想成乘客从手机飞到模型再飞回来：

| 跳点 | 机场比喻 | PM 该关心什么 |
|------|---------|--------------|
| 1. Client → 你的服务器 | 上国内航班 | UX 延迟预算开始倒数 |
| 2. 服务器 → Anthropic | 国际转机（护照＝API key） | 安全、rate limit、logging |
| 3. Claude 内部 | 海关 / 行李处理 | 看不见内部，但花时间和钱 |
| 4. Anthropic → 服务器 | 飞机降落、拿行李 | 拿到 `stop_reason` 与 `usage` metadata |
| 5. 服务器 → Client | 乘客打车回家 | 渲染 streaming、必要时把成本显示给用户 |

每一跳都加延迟，每一跳都可能出错。PM 的工作就是围绕这个事实设计：这整段过程既不即时也不免费。

---

## 为什么"必须有服务器"是产品规格的硬需求

PM 常被问"能不能直接从 mobile app 调用 API？"答案永远是不行，而且理由是商业的，不只是技术的：

| Client-side 调用的风险 | 商业影响 |
|---------------------|---------|
| API key 被从 app binary 挖出来 | Credits 一夜被抽干，账单爆表 |
| Key commit 到 public repo | 被自动 revoke，feature 坏掉，丢人事件 |
| Client 没有 rate limit | 滥用的用户花你的钱比他付的还多 |
| 没有 audit log | 无法满足企业合规需求（SOC2、HIPAA） |

服务器是你未来要应付法务、财务、安全部门所有要求的地方。**Day 1 就要有，不是等出事才补。**

---

## Product Use Cases

### 五步流程最关键的场景

| 场景 | PM 为什么该懂这条流程 |
|------|--------------------|
| 给企业客户的 chatbot | Audit log 跟 PII 脱敏都要在服务器那跳做 |
| 有 AI feature 的 mobile app | Key 不能打包进 binary，需要 BFF 层 |
| 成本敏感的免费方案 | `usage` 让你不用再拉计费系统就能按用户计费 |
| 监管行业（医疗、金融） | 服务器是唯一可以管控数据驻留的地方 |
| 长篇生成 feature | `stop_reason == max_tokens` 要有"继续"的 UX pattern |

### 没那么关键的场景（但还是要注意）

| 场景 | 为什么 |
|------|-------|
| 只给 10 个工程师用的内部工具 | 安全还是重要，但成本/延迟调优可以晚点做 |
| 一次性实验 | 流程一样，只是省略生产硬化 |

---

## PM Decision Framework

设计 Claude feature 时走一遍这些问题：

| 问题 | 为什么重要 |
|------|----------|
| API key 放哪？ | 答案必须是服务器。工程师说"client"就要立刻举红旗。 |
| 这个 feature 的 `max_tokens` 预算是多少？ | 决定成本上限和截断 UX。 |
| `stop_reason == max_tokens` 怎么处理？ | 自动续写？显示"查看更多"？默默截断？ |
| 每个用户的用量怎么计？ | `response.usage` 是免费的，另开一个计费系统不是。 |
| Prompt log 写在哪？ | 必须是服务器，且要做 PII 脱敏。 |
| 等待时给用户看什么？ | 五跳总共好几秒，streaming UX 或 loader 必备。 |

---

## 成本透明化的优势

Anthropic 每个 response 都会回 `usage.input_tokens` 与 `usage.output_tokens`。这是 PM 的隐藏超能力：

- 可以让企业用户看到每次交互的成本。
- 可以不用叫工程师埋点就做按用户配额。
- 可以立刻 A/B 测试 prompt 变更的成本差异。
- 可以建 dashboard 看哪个 feature 最贵。

在其他 SaaS 产品里，这些都需要另开计费 pipeline。Anthropic 直接塞在每个 response 里。

---

## Common PM Mistakes

1. **以为 AI feature 是即时的** —— 五跳真的要花时间，loading state、streaming、optimistic UI 第一天就要设计。
2. **scope 时没决定 `max_tokens`** —— 工程师会随便给一个数字，悄悄盖住 feature 质量上限。
3. **忘了截断 UX** —— `stop_reason == max_tokens` 生产环境一定会遇到，PRD 必须写明用户看到什么。
4. **V1 不做成本计量** —— 之后补比一开始就用 `usage` 难十倍。
5. **以为 client 可以直接调 Anthropic** —— 会卡住 mobile 和 web launch，直到 security 审 BFF 为止。

> **Key Insight**
>
> PM 的角度看，五步流程就是你未来面对每个事故、成本审查、安全审计的地图。工程师说"AI 很慢"或"AI 坏了"，你第一个问题永远应该是"哪一跳？"这一句话能强迫团队把 client、服务器、Anthropic、model 区分开，比任何其他 post-mortem framing 都更快解锁问题。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）**：情境题会问 API key 放哪、`max_tokens` 怎么设、生产代码怎么处理 `stop_reason`。
- **D3（Claude Code Configuration）**：API key 管理模式——答案永远是服务器存储。
- **D1（Agentic Architecture）**：每个 agent loop 都是在这个五步 envelope 上跑 for-loop。
- 触发条件：题目说"工程师把 key 放进 mobile app"→ 正确答案永远是"搬到后端 service"。

---

## Flashcards

| Front | Back |
|-------|------|
| 用 PM 语言讲五步 Claude 请求流程？ | Client → 服务器 → Anthropic API → Model → 回服务器 → Client |
| 为什么 mobile app 不能直接调 Anthropic？ | API key 会被从 binary 抽走，谁都能抽干你的 credits |
| PII 脱敏唯一能做的位置是哪一跳？ | 服务器那一跳（在数据离开你的边界之前） |
| 每个 response 都会给哪些 PM 相关的 metadata？ | `usage.input_tokens`、`usage.output_tokens`、`stop_reason` |
| `stop_reason == max_tokens` 对 UX 意味着什么？ | Claude 被中途截断；PRD 要描述截断 UI（例如"继续"按钮） |
| 为什么 response 里的 `usage` 是 PM 超能力？ | 不用额外加 infra 就能做按用户计费和 prompt A/B 成本比较 |
| scope AI feature 时第一个该问的安全问题？ | "API key 放哪？"——唯一正确答案是服务器 |
| 假设 AI 回复是即时的会失去什么？ | 会省略 loading / streaming UX，用户在 2–5 秒 round trip 里觉得 feature 坏掉 |
