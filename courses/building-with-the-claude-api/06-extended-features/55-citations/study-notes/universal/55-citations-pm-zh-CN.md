# Citations — PM Perspective

| 项目 | 内容 |
|------|------|
| Exam Domain | D4 — AI Safety & Alignment (20%) — 主要；D2 — Tool Design & MCP Integration (18%) — 次要 |
| Task Statements | 4.2（grounded outputs）、2.2（content blocks）、5.4（信任与可验证性） |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 55 |

---

## One-Liner

Citations 是任何用户需要知道"这个答案哪来的？"的 Claude 功能的信任层——它把 Claude 从黑盒变成会摊开工作过程的研究助理。

---

## Mental Model：会拿出收据的研究助理

想象你请一个研究助理读一叠合同、做摘要。两种情境：

- **没有 citations**：助理交给你一份摘要然后说"相信我"。你没办法验证，若摘要出错你也不知道是哪份文档误导了他。
- **有 citations**：摘要里每句话都有脚注，指向某份合同里某条具体条款。你可以在几秒内抽检任何一项。

Citations 就是 Claude 的脚注。代价是稍微复杂的响应处理；收益是用户愿意用这个功能做真实决策。

---

## PM 为什么该在意

Citations 是让高代价文档功能能够上线的关键功能。没有它：

- 法务团队不会用 AI 合同审查器。
- 合规不会批准政策 QA 工具。
- 医师不会依赖临床参考助理。
- 金融分析师不会信任从 10-K 抽取出的数据。

有了它，上述所有功能突然都能过关。用户可以在采取行动前验证任何陈述。审计员有可追溯轨迹。面向客户的产品可以说"这是来源"而不是"请相信我们的 AI"。

如果你的产品在受管制、高代价或企业环境里，citations 几乎从来不是可选项。

---

## Product Use Cases

### Citations 必备的情境

| 产品情境 | 为何强制要有 citations |
|---------|----------------------|
| 法律研究、合同审查 | 律师对每个主张都要引用原条款 |
| 临床决策支持 | 临床医师采取行动前需验证来源指引 |
| 金融分析 | 审计员要求可追溯的证据链 |
| 法规 / 合规 QA | 监管机构要求证明答案来自政策原文 |
| 企业知识搜索 | 内部用户想从答案跳到来源文档 |
| 学术或研究工具 | 研究者无法引用指不出的来源 |

### Citations 可选的情境

| 产品情境 | 原因 |
|---------|------|
| 闲聊 / 创意写作 | 没有依据型的来源 |
| 用 Claude 一般知识做 brainstorming | 来源是训练数据，不可引用 |
| 对用户口述内容做摘要 | 没有书面文档可引用 |
| 无发布承诺的内部原型 | 只在"信任是需求"时才付复杂度 |

---

## PM 决策框架

设计以文档为依据的功能时要问：

| 问题 | 若答 Yes | 含义 |
|------|---------|------|
| 用户会基于 Claude 的答案做决策吗？ | Yes | 几乎一定要有 citations。 |
| Workflow 是受管制的（法律、医疗、金融、合规）？ | Yes | Citations 强制要有——第一个 release 就要上。 |
| 内部审计或外部审查者会看到 Claude 的输出？ | Yes | Citations 会产生他们需要的轨迹。 |
| 用户能容忍 citation 标记带来的一点 UI 复杂度吗？ | Yes | 建 hover-to-verify pattern。 |
| 单一 request 用多份文档吗？ | Yes | `document_index` 和 `document_title` 很重要，UI 要追踪。 |
| 我们用的是纯文字 RAG chunks 而不是 PDF？ | Yes | Citations 仍然能用，只是回的是字符位置不是页码。 |

---

## Cost、Complexity、UX 权衡

Citations 是 API 里最便宜、最高影响力的功能之一。成本：

- **响应处理稍微复杂。** 工程端要迭代 content blocks 并把 citation metadata 拉到 UI。
- **每次调用有少许 token 开销**，因为 Claude 会在文字旁边吐 citation metadata。
- **UX 设计工作**，要做 hover-and-verify pattern。

效益：

- **信任。** 用户真的会拿输出来用。
- **法规通过。** 法务与合规能批准原本会挡下来的功能。
- **幻觉事件更少。** Citations 会显示 Claude 在引文档还是在外推——是自然的 sanity check。
- **更好的深钻 UX。** 想要更多脉络的用户可以跳到来源段落或页面。

对任何企业文档功能，成本效益几乎是必赢的选择。对消费端的一般知识功能，citations 常常不适用。

---

## PDF + Citations 标准 stack

把课程 54（PDF support）和课程 55（citations）配对，就是标准的 Claude 企业文档 stack：

1. 启用 `citations.enabled: True` 并带可读 `title` 的 PDF content block。
2. 精准的抽取或 QA prompt。
3. 渲染答案并在行内放 citation 标记、提供 hover popover 的 UI。
4. 可选：对文档 bytes 做 prompt caching 以支持重复 query。

这是从"我们有一堆 PDF"到"我们有一个可发布、用户信任的企业功能"的最短路径。每一份文档 workflow 的 PRD 都应该明确引用这个配对。

---

## Common PM Mistakes

1. **对高代价功能把 citations 当可选项。** 它不是。受管制 workflow 里的用户没有它不会采用。
2. **在 API 打开 citations 却没在 UI 显示。** 付了成本、拿不到信任效益，还让工程团队困惑功能的意义。
3. **忘了 `title` 字段。** 多文档响应变得暧昧，用户无法分辨 citation 来自哪份文档。
4. **以为 citations 保证正确性。** Citation 证明来源文字存在，不证明 Claude 的改写忠实。高代价答案仍需人工审查解读错误。
5. **没处理纯文字 RAG chunks。** 若你的管线发送的是文字 chunk，citations 仍然能用，但返回的是字符位置不是页码，UI 必须依 source 类型分支。
6. **低估 UX 设计工作。** Citation 标记、hover popover、跳到来源、"无 citation"的 fallback 都需要明确设计。

---

> **Key Insight**
>
> Citations 是任何基于用户在意的文档的 Claude 功能的最小可行信任机制。启用便宜、跳过很贵：没有它，企业和受管制功能很少能过信任门槛，用户只好自己回去读原文。把 citations 和 PDF support 配对，一个 request 就能拿到标准的企业文档 stack。

---

## CCA Exam Relevance

- **D4 (AI Safety & Alignment)**：Citations 是 grounded、可验证输出的标准机制。预期考信任与来源透明度的题目。
- **D2 (Tool Design & MCP Integration)**：要会 API 形状——`title` 字段、`citations.enabled` 标志、citation metadata 结构（`cited_text`、`document_index`、`document_title`、页码或字符位置）。
- 情境题："用户需要验证 Claude 的文档答案。"答案是在 document block 启用 citations 并在 UI 显示 `cited_text`。

---

## Flashcards

| Front | Back |
|-------|------|
| Citations 的研究助理类比是什么？ | 没 citations 时助理说"相信我"；有 citations 时每句话都有脚注指向某个来源条款，你可以抽检。 |
| 什么时候 citations 是强制的？ | 受管制或高代价 workflow：法律、医疗、金融、合规、企业知识、学术或研究工具。 |
| 什么时候 citations 可选或不适用？ | 闲聊、创意写作、一般知识 brainstorming、或对用户口述内容做摘要。 |
| Citations UX 要设计什么？ | 行内标记、hover popover 显示 `cited_text` 与 `document_title`、跳到来源、以及无 citation 片段的 fallback。 |
| 最小可行的企业文档 stack 是什么？ | PDF content block + 启用 citations + 精准 prompt + 有 citation 标记的 UI +（可选）对重复 query 的 prompt caching。 |
| 为什么 citations 启用便宜、跳过很贵？ | 启用只要少许 token 开销与中等 UI 工作；跳过代表高代价功能过不了信任与合规门槛。 |
| Citations 保证 Claude 的答案正确吗？ | 不。它证明 Claude 读过某段来源原文，不证明 Claude 的解读准确。具后果的答案仍需人工审查。 |
| Citations PRD 该规格什么？ | 信任需求（谁要验证）、标记与 popover 的 UX pattern、多文档处理、纯文字 vs PDF source type、缺 citation 的 fallback。 |
