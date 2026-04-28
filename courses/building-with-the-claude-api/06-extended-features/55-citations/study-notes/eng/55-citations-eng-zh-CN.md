# Citations — Engineering Deep Dive

| 项目 | 内容 |
|------|------|
| Exam Domain | D4 — AI Safety & Alignment (20%) — 主要；D2 — Tool Design & MCP Integration (18%) — 次要 |
| Task Statements | 4.2（grounded outputs）、2.2（content blocks）、5.4（信任与可验证性） |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 55 |

---

## One-Liner

Citations 把 Claude 基于文档的答案从不透明文字变成可验证的轨迹——对每一个陈述，你都能拿到支撑它的原文、出自哪份文档、以及在文档里的位置。

---

## Citations 解决的信任问题

当 Claude 对着你提供的文档回答问题时，用户光看文字没办法分辨答案是来自你的文档还是模型的训练数据。这个暧昧性对任何"来源很重要"的功能都是信任杀手：法律研究、金融分析、医疗信息、合规 QA。

Citations 的修法是为 Claude 响应里的每一个陈述建立一条明确、机器可读的轨迹，指回支撑它的原文。模型不只回答——它把收据一起拿出来。

---

## 启用 Citations

启用 citations 需要在 `document` content block 上加两件事：一个人类可读的 `title` 和一个 `citations.enabled` 标志。

```python
{
    "type": "document",
    "source": {
        "type": "base64",
        "media_type": "application/pdf",
        "data": file_bytes,
    },
    "title": "earth.pdf",
    "citations": { "enabled": True }
}
```

两个字段很重要：

- **`title`**——文档的可读名称。这是用户在 UI 上看到 citation 时显示的名字；Claude 也用它在同一个 request 的多份文档之间做区分。
- **`citations.enabled`**——告诉 Claude 为每一个陈述追踪来源的开关。

Document block 的其他部分和 PDF support 的 pattern 完全一样。

---

## 开启 Citations 后的响应结构

关闭 citations 时，Claude 的响应是一个简单的 text block。开启后，Claude 返回一个更丰富的结构，文字片段附带 citation metadata。每个 citation 包含：

- **`cited_text`**——文档里支撑该陈述的原文，逐字符对应。这是模型指向的 ground truth。
- **`document_index`**——Claude 参考的是哪一份文档，单一 request 里有多份文档时很有用。
- **`document_title`**——你指给文档的 title（和 document block 里那个字符串一样）。
- **`start_page_number`**——被引用文字的起始位置。
- **`end_page_number`**——被引用文字的结束位置。

PDF 的 `start_page_number` / `end_page_number` 是页码。纯文字来源则把这两个字段换成**字符位置**，精确指向文字里的某个 span。

---

## 对纯文字来源的 Citations

Citations 不是 PDF 独享。对纯文字文档开 citations 的方式是换 `source` block：

```python
{
    "type": "document",
    "source": {
        "type": "text",
        "media_type": "text/plain",
        "data": article_text,
    },
    "title": "earth_article",
    "citations": { "enabled": True }
}
```

和 PDF 情况的差别：

- `source.type` 是 `"text"` 而不是 `"base64"`。
- `source.media_type` 是 `"text/plain"`。
- `source.data` 放原始文章文字，不是 base64 bytes。
- 返回的 citations 用**字符位置**（start_index / end_index）而不是页码。

这对 RAG 管线意义很大：当你的检索步骤抓出一段纯文字 chunk，你可以把它当成一份可引用的文档发送进去，拿回精确的字符 span，用来做 hover-over UI 或 highlight 工具非常干净。

---

## 用 Citations 做 UI

Citations 的真正产品杠杆在 UI 层。典型 pattern：

1. Claude 的响应带着 citation 注解的片段返回来。
2. UI 照常渲染答案文字，但每个被引用的 span 加上标记（一个小数字、反白背景、或内嵌 icon）。
3. Hover 或点击标记会打开一个 popover，显示 `cited_text`、`document_title`，并提供跳到某页或某字符位置的动作。
4. 用户可以就地验证陈述，不用离开答案画面。

这把 Claude 从"回答的黑盒"变成"会把工作过程摊开的研究助理"。需要信任输出的用户可以两下点击验证；不在意的用户可以忽略标记。

---

## 何时该用 Citations

课程点名四个 citations 值得花成本与复杂度的情境：

- **用户需要验证信息的正确性。** 高代价答案——法律、医疗、金融——需要证据。
- **你处理的是权威文档。** 若文档是 source of truth（合同、法规、临床指引），用户应该能指向它。
- **来源透明度对产品至关重要。** 有些产品——企业搜索、研究工具、知识库——靠来源透明度活着。
- **用户可能想探索特定事实周围的脉络。** Citations 是往下钻的 UX 钩子；用户可以从答案跳到周围段落再跳到整份文档。

---

## Common Mistakes

1. **忘了 `title` 字段。** Citations 在响应里用 title 当文档标识符。没写，用户看到空白或通用标签，无法区分文档。
2. **启用 citations 却没显示。** 标志打开却把答案渲染成纯文字，token 成本照付、信任效益为零。
3. **以为纯文字来源用页码。** 纯文字的 citations 返回字符位置，不是页码。你的 UI 必须依 source 类型分支。
4. **没处理更丰富的响应结构。** 开 citations 的响应比单一 text block 复杂。Content-block handler 必须迭代并正确拉出 citation metadata。
5. **在同一个 request 里混用有引用和没引用的文档却没追踪。** `document_index` 告诉你 citation 指向哪一份——要用它。
6. **以为 citations 等于正确性保证。** Citation 证明原文存在、Claude 读过它——不证明 Claude 的解读正确。Citations 是来源证据，不是准确度保证。

---

> **Key Insight**
>
> Citations 是把 Claude 的文档答案转成可验证陈述的依据层。API 表面很小——一个 `title` 字段加一个 `citations.enabled` 标志——但产品冲击巨大：对每一个高代价文档 workflow（法律、医疗、金融、合规），citations 就是"能发布"和"不能发布"的差别。把 citations 和 PDF support 搭配起来，就是企业文档 stack 的标准组合。

---

## CCA Exam Relevance

- **D4 (AI Safety & Alignment)**：Grounded outputs 与可验证响应是核心 safety 考量。Citations 是产生可验证、有来源链接答案的标准机制。
- **D2 (Tool Design & MCP Integration)**：Citations 延伸 `document` content block。要知道 `title` 和 `citations.enabled` 字段，以及 citation metadata 的形状（`cited_text`、`document_index`、`document_title`、页码或字符位置）。
- 情境题："用户需要验证 Claude 的答案来自某个特定来源。"答案是在 document block 上启用 citations，并在 UI 上显示 `cited_text` 和 `document_title`。

---

## Flashcards

| Front | Back |
|-------|------|
| 启用 citations 要在 document block 加哪两个字段？ | 一个 `title` 字段（可读文档名）加 `"citations": {"enabled": True}`。 |
| Citation 对象里有哪五项信息？ | `cited_text`、`document_index`、`document_title`、`start_page_number`、`end_page_number`。 |
| PDF 和纯文字来源的 citations 差在哪？ | PDF citations 返回页码；纯文字 citations 返回字符位置。 |
| 纯文字可引用文档用什么 `source.type` 和 `media_type`？ | `source.type: "text"` 和 `media_type: "text/plain"`，`data` 放原始文章文字。 |
| 什么时候该用 citations？ | 用户需要验证信息、处理权威文档、来源透明度关键、或用户可能想探索脉络时。 |
| 为什么启用 citations 时 `title` 字段是必要的？ | 它是每个 citation 返回的文档标识符，也是用户在 UI 看到的标签；没有它，多文档响应会暧昧。 |
| Citation 和正确性保证的差别？ | Citation 证明原文存在、Claude 读过它；不证明 Claude 的解读正确。 |
| Citations 的标准 UX pattern？ | 在被引用的 span 加行内标记，hover 显示 `cited_text` 与 `document_title`，并提供跳到来源的动作。 |
| 为什么 citations 对法律、医疗、金融产品至关重要？ | 这些领域的用户必须先验证来源才敢采取行动；citations 提供让这些功能能发布的可审计轨迹。 |
