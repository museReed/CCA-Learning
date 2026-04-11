# Web Search Tool — PM Perspective

| 项目 | 内容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%)、D4 — AI Safety & Alignment (20%) |
| Task Statements | 2.3（built-in server tools）、4.2（grounding 与 citation） |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 43 |

---

## One-Liner

给产品加上 web search 现在是一行配置的决策:Anthropic 处理搜索、解析、citation,你的团队只要把 result block 渲染到 UI。

---

## Mental Model：拥有图书证的研究助理

Server tool 出现前,要给 AI 搜索网络能力意味着建 search pipeline、scrape、清数据、排序、citation 抽取——就像雇一个研究员还要帮他搭一整间图书馆。Web search tool 就像发给研究助理一张图书证:他知道怎么用、会带来源回来、每一个论点都有 footnote。

| 能力 | 自己做 | 用 Web Search Tool |
|------|------|--------------------|
| 搜索基础设施 | 几周工程 | 今天就上 |
| 内容解析 | 依来源自定义 | 已处理 |
| Citation 格式化 | 自定义逻辑 | 内置 block |
| Domain 限制 | 自定义 allowlist | `allowed_domains` 字段 |
| 持续维护 | 你的团队一直扛 | Anthropic |

上市时间通常快 10-100 倍。

---

## 为什么 Citation 是产品功能

Web search tool 不只是返回搜索结果——它还返回**引用支撑每个陈述的具体来源文字**。对产品而言,这改变一切：

- **信任**:用户看到答案出处,不只是原生生成
- **合规**:受监管行业要求来源可追溯
- **审计**:内部用户可验证 Claude 的推理
- **责任降低**:"Claude 说的"变成"这个可验证来源说的"

没 grounding 的 LLM 输出在医疗、法律、金融、政府很难卖。带 citation 的 grounded 输出能解锁这些市场。

---

## Product Use Cases

### Web Search Tool 的明显胜面

| 产品 | 价值 |
|------|-----|
| 时事型助手 | 模型 cutoff 之后的新信息 |
| 医疗信息产品 | NIH/PubMed 限制 + citation 保证安全 |
| 法律研究 copilot | `.gov` / `.edu` 限制 + 可验证引用 |
| 竞争情报 | 当前市场数据而非训练旧数据 |
| 金融分析助手 | 实时股票 / 宏观数据带来源 |
| 快速变动文档的客服 | 永远最新的答案 |

### 什么时候不用

| 场景 | 更好的替代 |
|------|-----------|
| 训练数据就能完全回答的问题 | 跳过这个 tool——省成本与延迟 |
| 私有 / 专属信息 | 用你自己的 document 建自定义检索 tool |
| 离线 / 无网络环境 | Web search 需要连到 Anthropic 后端 |
| 高流量、对延迟敏感的 endpoint | 每次搜索都加时间,请算好预算 |

---

## PM 的关键配置杠杆

### 1. `max_uses`——成本与延迟的天花板

Claude 可能会发追踪搜索以精炼答案,`max_uses` 就是上限。

- **1-2**：便宜、快,可能漏细节
- **3-5**：研究类场景的标准区间
- **10+**：深度研究;预算要抓好

### 2. `allowed_domains`——内容质量的杠杆

这是 PM 最被低估的控制：

- 限定 PubMed 会把泛用健康 bot 变成循证医疗助手
- 限定 SEC filings 会把 chatbot 变成合规的金融工具
- 限定自家文档会变成有 grounding 的内部知识库

Domain 限制就是你把**信任**建进产品的方式。

### 3. Console Privacy 设置

Web search 必须在 Anthropic console 的 privacy 设置中以 organization 层级启用。PM 要把它放进环境 setup checklist。

---

## PM Decision Framework

| 问题 | 如果 Yes | 行动 |
|------|---------|------|
| 用户会问时事 / 最新信息吗？ | Yes | 启用 web search |
| 内容质量与信任很关键吗？ | Yes | `allowed_domains` 抓紧 |
| 答案需要 citation 符合合规吗？ | Yes | 突出渲染 citation block |
| 这是对延迟敏感的 endpoint 吗？ | Yes | 降 `max_uses`;考虑 cache |
| 数据是私有 / 内部吗？ | Yes | 改建自定义检索 tool |

---

## 渲染很重要

Response 会返回几种 block——text、search result、citation。这些不能互换：

1. **Web search result** 以"来源"列表呈现（信任信号、一眼可见）
2. **Citation block** 以行内链接嵌入答案（每个论点的佐证）
3. **Text block** 作为主答案内容

把一切合并成纯字符串的产品会失去信任优势。区分渲染的产品可测量到真实的信任与点击提升。

---

## Common PM Mistakes

1. **把 web search 当成后端问题** — Citation 渲染是核心 UX 决策,请自己掌握。
2. **敏感主题把 `allowed_domains` 留空** — 医疗、法律、金融产品从第一天就需要 domain 限制。
3. **没测量 citation 点击率** — 这是关键信任指标,请埋点。
4. **"以防万一"把 `max_uses` 设太高** — 成本与延迟会随每次追踪搜索累积。
5. **忘了 console privacy 开关** — 如果 org 设置是关的,staging / production 会静默失败。

> **Key Insight**
>
> Web search 是完全托管的 server tool：Anthropic 拥有执行,你拥有渲染。产品价值是**grounded、有 citation、新鲜的答案**,几乎不需要工程投入。把省下来的时间投在优秀的 citation UI,因为那里才是信任真正赢来的地方。

---

## CCA Exam Relevance

- **D2 (Tool Design)**：Web search 是典型的"server tool"——由 Anthropic 完全执行。要知道它与 text editor（本地执行）的对比。
- **D4 (AI Safety & Alignment)**：Citation 与 grounding 是信任机制;题目可能问哪个 tool 内置 citation。
- 场景题常比较自建搜索 vs. server tool——除非数据是私有,server tool 几乎永远是正解。

---

## Flashcards

| Front | Back |
|-------|------|
| 谁执行 web search tool？ | Anthropic——是完全托管的 server tool,你不用写任何本地代码 |
| 哪个字段限制每请求的搜索次数？ | `max_uses` |
| 哪个字段限定搜索到特定域名？ | `allowed_domains` |
| Citation block 带来什么产品价值？ | Grounded、可验证的答案——用户可以点到每个陈述的来源 |
| 使用 web search 前必须在 Anthropic console 启用什么？ | Organization privacy 设置中的 web search tool |
| 为什么 `allowed_domains` 对受监管行业重要？ | 它把 Claude 限制到权威来源（医疗限 NIH、法律限 `.gov`）,提升信任与合规 |
| 列出两个不该用 web search 的产品场景。 | 私有 / 专属数据;离线环境 |
| 使用 web search 时信任的主要 UX 杠杆是什么？ | 突出渲染 citation block——行内与来源列表并用 |
