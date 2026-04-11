# PDF Support — PM Perspective

| 项目 | 内容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — 主要；D5 — Enterprise Deployment (20%) — 次要 |
| Task Statements | 2.2（content blocks）、2.1（多模态输入）、5.2（文档处理） |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 54 |

---

## One-Liner

PDF support 把"让 Claude 读公司文档"从一个多周的集成项目变成一种新 content block——把传统的 OCR 加 layout 管线收敛成单次 API 调用，让每一类以文档为核心的产品突然变得可行。

---

## Mental Model：取代文档录入团队

多数企业都有一个——无论正式或非正式——负责从 PDF 抽取结构化意义的团队。法务读合同、财务从财报抽取数字、合规部门把政策对规范做比对、运营部门读供应商规格书。

PDF support 就是把一条 Claude 驱动的录入管线交到这个团队手上：一次 API 调用就读整份文档、理解结构、读表格与图表、回答人类原本要手动处理的问题。人不会消失，他们的工作从"读并抽取"变成"审查 Claude 抽取出来的东西"。

---

## PM 为什么该在意

每个碰 PDF 的企业产品过去都苦于抽取可靠度。传统 stack 长这样：OCR 引擎 → layout parser → table detector → chunking 逻辑 → prompt 管线。每一阶都加 latency、成本与错误。升级其中一环很少能修另一环。

PDF support 用单次 Claude 调用取代整条 stack，原生读文字、表格、图表与结构。产品面的含义是：一堆"太难可靠上线"的功能变得一个 sprint 就能做：

- **合同 QA**——"这份 MSA 的免责条款是什么？"
- **财务抽取**——"从这份 10-Q 拉出所有营收项目。"
- **政策合规**——"这份政策文档有提到数据保存吗？引出章节。"
- **规格书摘要**——"给非技术买家一份产品规格摘要。"
- **研究消化**——"这篇论文对方法 X 的结论是什么？"

PM 的工作从"怎么盖 parsing 管线？"变成"我们要模型回答的精确问题是什么？"

---

## Product Use Cases

### PDF support 合适的情境

| 需求 | 为何可行 |
|------|---------|
| 单份文档的摘要或 QA | 单次 API 调用，原生读文字 + 表格 + 图表 |
| 从已知文档类型抽取特定字段 | 明确 prompt + rubric 产生可靠的结构化输出 |
| 把答案锚在权威文档上 | 完美搭配 citations 做可追溯的依据 |
| 取代脆弱的 OCR / layout 管线 | 原生能力一次移除好几个失败模式 |
| 分析 PDF 内的图表或表格 | 不需要额外的 vision 或抽取步骤 |

### PDF support 不够的情境

| 需求 | 更好的选择 |
|------|-----------|
| 在上千份文档中搜索 | 你还是需要 RAG——PDF support 取代抽取阶段，不取代检索阶段 |
| 即时扫描大量实时文档 | 大语料要先一次前处理并 cache / 建索引 |
| 低质量扫描件的像素级表单抽取 | 针对标准化表单，专门 OCR 工具在成本和准确度上可能更优 |
| 高敏感度文档搭配严格数据管控 | 先检视数据驻地和加密要求；document support 仍然要把 bytes 发到网络 |

---

## PM 决策框架

| 问题 | 若答 Yes | 含义 |
|------|---------|------|
| 用户 workflow 要读的 PDF 变异太大、传统 parser 搞不定吗？ | Yes | PDF support 是强力候选。 |
| 文档里有表格、图表或复杂 layout 吗？ | Yes | 原生 PDF 读取在这里相对 legacy 管线有巨大优势。 |
| 用户会需要验证答案来源吗？ | Yes | 把 PDF support 和 citations（课程 55）配对。 |
| 文档通常非常长或在多次调用里重复？ | Yes | 规划 chunking 与 prompt caching 控成本。 |
| 问题的类别明确（摘要、字段抽取、QA）？ | Yes | Prompt 写成精确问题，不要"跟我说一下这份"。 |
| 我们处理受管制或机密数据吗？ | Yes | 发布前审厂商的数据处理、logging 与保存政策。 |

---

## Cost、Latency、UX 权衡

PDF support 比看起来更贵。长 PDF 主导每次调用的输入 tokens。三个要预算的 pattern：

1. **Chunking。** 若用户对长文档问的是狭窄问题，只把相关 section 发送给 Claude。PRD 要写清楚 chunk 的挑选方式（启发式、embedding 搜索、section 标题）。
2. **Caching。** 同一份文档被反复 query 时，prompt caching 让文档 bytes 在第一次调用之后几乎免费。这是 Claude API 里最干净的成本胜利之一。
3. **Latency。** Prompt 里放长 PDF 会拖慢第一个 token。交互功能要显示 loading state，描述模型正在做什么（"正在读合同…"）。

PDF 功能的 PRD 清单：

- 预期文档大小分布。
- Chunking 或 caching 计画。
- Prompt 精准度计画（功能问的是什么问题？）。
- 有标注的 eval set，涵盖你在乎的抽取。
- 若答案具后果，要有 human-in-the-loop 审核流程。

---

## 和 Citations 的配对

课程 55（Citations）是 PDF support 的天然搭档。Citations 把 Claude 的答案变成可验证的轨迹：用户能看到 PDF 里哪几句话支撑那个答案。任何用户需要信任答案的功能——法务、财务、医疗、合规——都应该把 PDF support 和 citations 配对。这是 API 里企业文档 workflow 杠杆最高的组合。

---

## Common PM Mistakes

1. **以为 PDF support 取代 RAG。** 它取代单份文档内的抽取阶段，不取代多份文档间的检索。语料有上千份，仍然需要检索。
2. **写含糊 prompt。** "跟我说这份合同"不达标。写精确的："用两句话摘要责任条款并列出上限金额。"
3. **忘记对重复 query 用 prompt caching。** 每次都发整份 50 页 PDF 而不 cache，财务会注意到这条 line item。
4. **没搭配 citations。** 以文档为依据的功能应该让用户能验证；citations 是那层信任的 UX。
5. **跳过数据处理审查。** PDF 常含机密信息。发布前确认厂商数据政策。
6. **没建 eval set。** 抽取功能 demo 漂亮、在 production 默默坏掉。一份小型标注集能早期抓到 regression。

---

> **Key Insight**
>
> PDF support 不是炫目的功能，但它是让严肃的企业文档 workflow 不用再盖 OCR 加 layout stack 的那个功能。真正的产品杠杆来自三个纪律：精准的 prompt、用 chunking 或 caching 控成本、以及搭配 citations 拿到可验证答案。把这三件事做对，一大类"太难上线"的文档功能就变成两周的工程。

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**：把 PDF 认成 `document` content block + `application/pdf` media type——和 image block 同一套 pattern。
- **D5 (Enterprise Deployment)**：文档处理管线、chunking、caching、以及和 citations 配对都是 production 考点。
- 情境题："你要 Claude 回答一份 PDF 合同的问题并显示来源。"预期答案是 `document` block + `application/pdf` + 启用 citations。

---

## Flashcards

| Front | Back |
|-------|------|
| PDF support 的文档录入团队类比是什么？ | PDF support 给企业一条 Claude 驱动的录入管线，像法务或财务团队那样读文档，取代脆弱的 OCR / layout stack。 |
| 什么时候 PDF support 是错的工具？ | 问题是大语料检索（仍需 RAG）、低质量扫描件的像素级表单抽取、或严格数据驻地管控下的文档处理。 |
| PDF 功能的三个 PM 权衡？ | 文档大小（token 随长度增长）、chunking vs 整份送、以及对同文档重复 query 的 prompt caching。 |
| 哪个 extended feature 是 PDF support 的天然搭档？ | Citations——把 Claude 的抽取变成 PDF 内可验证的来源指针。 |
| PDF 功能的 PRD 该包含什么？ | 预期文档大小、chunking / caching 计画、精准 prompt / 问题规格、有标注的 eval set、以及数据处理审查。 |
| 哪个常见 PM 错误把 PDF support 当全套 RAG？ | 以为它取代检索。它只取代单份文档内的抽取阶段；多份文档间的检索仍是另一个问题。 |
| 为什么企业文档功能应该把 PDF support 与 citations 配对？ | 让用户能验证答案来源——对法务、财务、医疗、合规这类信任不可妥协的工作流至关重要。 |
| PDF support 怎么改变 PM 的工作？ | 从"怎么盖 parsing 管线？"变成"模型该回答的精确问题是什么，以及我们怎么验证它？" |
