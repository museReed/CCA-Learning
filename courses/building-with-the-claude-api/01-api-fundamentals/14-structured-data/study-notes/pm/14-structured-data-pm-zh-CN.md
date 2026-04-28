# Structured Data — PM 视角

| 项目 | 细节 |
|------|------|
| 考试领域 | D5 — Enterprise Deployment (20%) 主要；D2 — Tool Design & MCP Integration (18%) 次要 |
| Task Statements | 5.3（production 模式）、1.3（prompt engineering）、2.1（结构化输出） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 14 |

---

## 一句话总结

当你的产品需要 raw data——一个 JSON object、code snippet、条列清单——不要闲聊前言时，你用两件一组的技巧（prefill + stop sequence）让 Claude 交回干净输出，用户可以直接 copy-paste 或下游系统可以直接 parse 而不用额外处理。

---

## 心智模型：贩卖机 vs 亲切咖啡师

想两种买咖啡的方式：

| 互动 | 类比 | 输出 |
|------|------|------|
| 亲切咖啡师 | 默认 Claude | 「来，你的拿铁！今天多加了一点奶泡，希望你喜欢。有需要随时说！」+ 咖啡 |
| 贩卖机 | Prefilled Claude | *click* → 咖啡 |

两者都交出咖啡。但如果你是把咖啡接进管线（下游系统）的产品，咖啡师的闲聊会堵住管线。结构化数据技巧把 Claude 变成贩卖机，用于闲聊是摩擦而非友善的场景。

---

## 产品问题

想象一个 AWS EventBridge 规则生成器：用户输入描述、按生成、预期按「复制」拿到干净 JSON，直接粘到 AWS console。如果 Claude 返回：

````
```json
{ ... }
```
This rule captures EC2 instance state changes when instances start running.
````

那「复制」按钮会：

1. 复制太多——用户把 markdown fences 和一句英文粘进 AWS，被拒绝
2. 需要 client 端 custom parsing 逻辑——当 Claude 用不同方式写解释就失败

两种结果都是产品质量 bug。结构化数据技巧完全消除这类 bug。

---

## 产品使用场景

### 什么时候需要结构化输出

| 产品 | 需要什么 |
|------|---------|
| API 响应生成器 | 纯 JSON body |
| Code 生成器 / snippet 工具 | 干净 code 无评论 |
| 配置文件构建器（YAML、JSON、TOML）| 可直接存档的文件内容 |
| 从非结构化文字抽数据 | 可 parse 的 JSON 进 database |
| CSV / 电子表格 row 生成器 | 可导入的 rows |
| SQL query 构建器 | 可执行的 SQL，别无其他 |

### 什么时候闲聊输出没问题

| 产品 | 原因 |
|------|------|
| 对话式 chat | 用户*想要* context 和友善 |
| 家教 app | 解释本身就是产品 |
| Summarizer | 散文就是输出 |
| 创意写作 | 评论可以是声音的一部分 |

测试：是人类要读这个输出，还是机器要 parse？如果是后者，你需要结构化输出。

---

## Copy-Paste 测试

这是简单的 PM 测试：如果你的 feature 有「复制」按钮，输出应该不用编辑就能粘。如果 Claude 生成的输出在可用前需要任何手动清理，你的产品就坏了。

设计评审时跑这个测试：

1. 用当前 prompt 从 Claude 生成真实响应
2. 按「复制」
3. 粘到目标环境（AWS console、code editor、电子表格）
4. 能用吗？不能的话，你需要结构化数据技巧

这是五分钟的测试，能在上线前抓住最常见的 AI 产品 bug 之一。

---

## PM 决策框架

| 问题 | 如果 Yes | 含义 |
|------|---------|------|
| 输出会喂给下游 parser 或自动 pipeline 吗？ | Yes | 必须用结构化输出 |
| UI 有「复制」按钮吗？ | Yes | 必须用结构化输出 |
| 用户会把响应跟规格（AWS rule、JSON schema）比对吗？ | Yes | 必须用结构化输出 |
| 输出只给人类阅读吗？ | No | 默认 Claude 可以 |
| 用户能忍受自己清理输出吗？ | No | 必须用结构化输出 |

任何「yes」条件成立时，把「输出必须是干净、可 parse 的 [格式]」写进 PRD 验收标准。

---

## 和 Tool Use 的权衡

课程后面，tool use 提供另一种获取结构化 JSON 的方式——Claude 返回一个 schema 验证过的 tool-call object。身为 PM，理解区别：

| 方法 | 优点 | 缺点 |
|------|------|------|
| Prefill + stop sequence | 简单，任何格式都行（code、CSV、YAML、XML），不需 schema | 无 type 验证；Claude 还是可能吐 malformed data |
| Tool use + `input_schema` | Schema 验证、type 安全、agent 式组合性 | 较复杂、只能 JSON |

**PM 经验法则：** 快速原型和非 JSON 格式用 prefill + stop sequence 就好。下游系统依赖的 production JSON 生成，坚持用有 schema 的 tool use。

---

## 常见 PM 错误

1. **假设 Claude「就会回 JSON」**——它默认回 JSON 加解释。结构化数据技巧是必要
2. **没在目标环境测试 copy-paste**——bug 只在真实用户尝试用输出时才出现
3. **在 system prompt 写「输出干净 JSON」就当作完成**——Claude 还是会加评论。你需要 prefill + stop sequence 或 tool use
4. **没编列 retry 逻辑预算**——就算有 prefill，Claude 偶尔还是会吐 malformed 输出。Production feature 需要 JSON parse retry
5. **在 API 响应用闲聊输出**——下游集成者假设契约；评论打破每个 consumer

> **Key Insight**
>
> 结构化数据不是 nice-to-have——它是用户能真的在下游 workflow 用起来的 AI feature 和「几乎可用」输出之间的区别。Prefill + stop sequence 模式是「让 Claude 闭嘴只回那个东西」最简单的 PM 面向配方。知道什么时候伸手用它；知道什么时候 tool use 才是更好的答案。

---

## CCA 考试重点

- **D5.3（production 模式）**：预期考场景题，问如何让 Claude 返回纯 JSON 给下游消费
- **D2 (Tool Design)**：tool use 是 production 级 JSON 的替代方案——考试可能要你在两者间选
- 注意「Claude 把输出包在 markdown fences 里并加解释」这种措辞——答案是 prefill + stop sequence（或 tool use）

---

## Flashcards

| 题目 | 答案 |
|------|------|
| 结构化数据技巧解决什么产品问题？ | Claude 默认把结构化输出包在 markdown fences 里并加英文评论，打破下游 parsing 和 copy-paste UX |
| PM 级的「copy-paste 测试」是什么？ | 生成真实响应、按复制、粘到目标环境。不能用的话，你的产品需要结构化输出 |
| 结合起来强制干净结构化输出的两个技巧是什么？ | Assistant message prefilling 和 stop sequences |
| 什么时候闲聊输出是对的选择？ | 对话式 chat、家教、summarization、创意写作——任何人类直接读输出的地方 |
| 什么时候结构化输出是必须？ | 任何输出喂给 parser、automation pipeline、copy 按钮或有 schema 契约的地方 |
| 和 tool use 的权衡是什么？ | Prefill 对任何格式有效不需 schema；tool use 只能 JSON 但提供 schema 验证和 type 安全 |
| 为什么在 system prompt 写「请只回 JSON」不够？ | Claude 的 helpful 行为还是会漏评论——你需要结构强制，不只是指令 |
| 贩卖机类比是什么？ | 默认 Claude 是加闲聊的亲切咖啡师；prefilled Claude 是只交出产品的贩卖机 |
