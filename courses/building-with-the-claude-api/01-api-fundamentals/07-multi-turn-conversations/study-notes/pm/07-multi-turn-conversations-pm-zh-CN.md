# Multi-Turn Conversations — PM Perspective（简体中文）

| 项目 | 内容 |
|------|------|
| Exam Domain | D1 — Agentic Architecture (22%) 主要；D5 — Enterprise Deployment (20%) 次要 |
| Task Statements | 1.2（agentic loop 基础）、1.1（对话状态管理）、5.3（生产 pattern） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 07 |

---

## One-Liner

Claude 在调用之间没有记忆——每一轮你的产品都要提供对话历史——这让"用户感觉 AI 记得什么"变成 PM 没办法丢给工程师的产品决策。

---

## Mental Model：金鱼顾问

想象你请了一位非常聪明但同时是金鱼的顾问：每次你走进会议室，他都对上次会议没有记忆。要持续对话，你每次会议开始都要递上所有过去会议的打印逐字稿。

| 金鱼顾问 | Claude API |
|---------|-----------|
| 会议之间会忘记 | API 调用之间 stateless |
| 读逐字稿追上进度 | 每次调用读 `messages` list |
| 逐字稿每次变厚 | `messages` list 每轮变长 |
| 厚逐字稿读起来久 | 历史越长，input token 越贵 |

PM 的工作是决定：逐字稿要放什么、保留多久、每次会议你愿意付多少钱。

---

## 为什么 PM 该关心 Statelessness

这一个技术细节对产品的影响超乎想象：

| 产品考量 | Statelessness 的影响 |
|---------|---------------------|
| 聊天感 | 记忆必须刻意设计，不会免费出现 |
| 成本曲线 | 长聊天很快变贵（线性 token 增长） |
| 隐私 | 你决定留什么、丢什么 |
| Session 超时 | 对话什么时候"结束"你决定，不是 API |
| 跨设备延续 | 历史必须放在持久存储，不只是 in-memory |
| Per-user 隔离 | 绝不能把一个用户的历史混进另一个 |

这每一项都是产品决策。工程师可以实现任何一种，但需要 PM 指引产品该有哪种行为。

---

## Product Use Cases

### 需要多轮的时候

| Feature | 为什么必须多轮 |
|---------|-------------|
| 客服聊天 | 用户会指涉对话前面的东西 |
| 辅导 / coaching agent | 学习进度依赖前几轮的 context |
| 长期写作助理 | 草稿会跨多个 prompt 迭代 |
| 研究 agent | 某一步的发现会喂到下一步 |

### 单轮就够的时候

| Feature | 为什么单轮可以 |
|---------|-------------|
| "摘要这封信"按钮 | 每次点击独立 |
| 文档分类 | 不需要对话 |
| 翻译 | 无状态转换 |
| 自动完成建议 | 发射后不管 |

PM 经验法则：如果用户会期待 AI"记得之前"，那就是多轮情境，你必须明确为它设计。

---

## 成本曲线：PM 必须看得懂的一张图

因为历史每轮都重放，input token 线性增长：

```
   Input tokens
        │
20,000  │                                    ●
        │                               ●
        │                          ●
10,000  │                     ●
        │                ●
        │           ●
 5,000  │      ●
        │  ●
        └──────────────────────────────────────── Turns
          1    5    10   20   30    40    50
```

这有三个产品后果：

1. **单位经济随聊天长度变动。** 50 轮的 chat 大约是 10 轮的 25 倍 input token 成本。
2. **最终会撞 context window。** 每个 model 有历史长度上限；长 chat 撞墙前需要策略（摘要、截断、prompt cache）。
3. **没有聊天长度分布就没办法预估成本。** 需要真实埋点数据，不是凭感觉。

---

## PM Decision Framework：记忆策略

Launch 前，每个 feature 挑一个记忆策略：

| 策略 | 做法 | 什么时候用 |
|------|------|----------|
| **完整历史** | messages list 永远保留每一轮 | 短对话（< 20 轮）且 context 重要 |
| **Sliding window** | 只留最近 N 轮 | 长对话但最近 context 就够 |
| **摘要** | 把旧轮压成滚动摘要 | 长对话但早期 context 还是重要 |
| **Session reset** | 闲置或动作时明确结束并清空 | 以任务为单位、有明确完成的 chat |
| **Prompt caching** | 没变的 prefix 便宜重用 | 长而稳定的 system prompt + 变动的尾巴 |

PRD 应该指定用哪个策略、用户看起来会是怎样。"用户会记住几轮"是 PM 能回答的问题，不是工程细节。

---

## Common PM Mistakes

1. **以为 Claude 默认会记得** —— 它不会；跳过这一课，你第一个 chat feature 会让用户觉得"笨笨的"。
2. **没有聊天长度或预算上限** —— 一个 power user 200 轮的对话会花你真金白银，要设限。
3. **混淆跨用户 session** —— 后端 bug 让两个用户共用 `messages` list 就是隐私事故；PM 的验收条件必须要求隔离。
4. **忘记 reset 流程** —— 用户需要"新对话"按钮；没有它，成本爬升 context 变陈旧。
5. **没埋点聊天长度分布** —— 没真实 chat 长度分布就没办法规划预算或 eval prompt。

> **Key Insight**
>
> Statelessness 是伪装起来的产品决策。API 给你一张白纸；你的产品定义"记忆"是什么意思。感觉像魔法的 chat 产品都是刻意这么做——他们决定哪些轮次重要、session 多久、成本怎么 scale、chat"重置"时用户看到什么。忽略这件事的产品会做出慢、贵、健忘的 chat，然后怪 model。**在 PRD 里拥有记忆策略，你就会出 feel smart 而且可预测的 feature。**

---

## CCA Exam Relevance

- **D1（Agentic Architecture）**：多轮就是 agent loop 的基础。情境："Claude 怎么记住之前消息？"→ client 每轮都重发。
- **D5（Enterprise Deployment）**：线性 token 增长对成本与 scale 的启示。
- 情境触发："用户反映 chatbot 会忘"→ 检查 app 有没有追加 assistant 回复并发完整历史，不是改 prompt。

---

## Flashcards

| Front | Back |
|-------|------|
| Claude 在同一个 chat 里会自动记得之前交流吗？ | 不会——API 是 stateless；你的 app 每轮都要重放历史 |
| "金鱼顾问"比喻是什么？ | Claude 调用之间会忘，所以你每次新会议都要递一份完整的过去会议逐字稿 |
| 为什么长聊天成本比例失衡？ | Input token 随历史重放线性增长；50 轮 chat 大约是 10 轮的 25 倍 input token |
| PM 可以挑的记忆策略有哪些？ | 完整历史、sliding window、摘要、session reset、prompt caching |
| Statelessness 对多用户 app 引发什么产品考量？ | Per-user 隔离——一个用户的历史绝不能泄漏到另一个 |
| 什么时候单轮就够？ | 每次交互独立（摘要、翻译、分类）、用户不期待"记忆" |
| Chatbot"会忘"时第一个该检查什么？ | App 有没有追加 assistant 回复并每次调用发完整历史 |
| PRD 该指定哪些记忆相关事项？ | 用哪个记忆策略、轮数/成本上限、"新对话"/session reset 怎么运作 |
