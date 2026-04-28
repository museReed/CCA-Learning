# BM25 Lexical Search — PM Perspective（产品视角）

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Architecture（22%）主领域；D5 — Enterprise Deployment（20%）次领域；D2 — Tool Design（18%）也相关 |
| Task Statements | 1.3（context management）、5.2（production search infrastructure） |
| 来源 | building-with-the-claude-api / 05-rag / Lesson 50 |

---

## 一句话总结

BM25 是一个不起眼、已有数十年历史的搜索技术，却悄悄拯救了你的 RAG 产品——在用户输入精确 order ID 而你的 AI 助理很有自信地返回错的 ticket 的那天。

---

## Mental Model：聪明实习生 vs Ctrl-F 高手

想象两位助理帮你在一份 500 页报告里找资料：

- **聪明实习生（语义搜索）**：把报告读完，归纳主题。问"上一季发生什么事？"他答得很好。问"incident INC-2023-Q4-011 怎样？"他很有自信地描述另一个 incident，因为他记得"那个是资安相关"，没去检查编号。
- **Ctrl-F 高手（BM25）**：任何字面 string 都能瞬间找到，但零理解力。问"上一季发生什么事？"他耸肩。问"INC-2023-Q4-011"他立刻指出提到这个 ID 的那三页。

好的研究团队两种都要。这就是 hybrid retrieval 对 RAG 产品做的事。

---

## PM 为什么要在意

纯语义 RAG 是 AI 功能最常见的早期失败模式。产品在 demo 时很漂亮（概念问题答得很好），但实际使用就崩了，因为真实用户常常输入：

- Order ID："查订单 #78921 状态"
- SKU："SKU-GX-42B 还有货吗？"
- Error code："ERR_UNAUTHORIZED_10031 是什么？"
- Ticket 编号、CVE ID、invoice 编号、员工编号、合同代码。

这些都可能被纯语义搜索漏掉，返回一个很自信但错误的答案。BM25（或任何 lexical search）是便宜又可靠的 safety net。

---

## Product Use Cases

### BM25 / Hybrid 是对的选择

| User Need | 为什么 BM25 有帮助 |
|-----------|---------------------|
| 精确 ticket / order / incident 查询 | ID 必须字面符合 |
| 技术文档的 error code 搜索 | Code 是罕见 token，BM25 一击命中 |
| 法律合同条款搜索 | 字面 phrase 关键 |
| 产品 SKU / barcode 查询 | 精确 token，没语义代理 |
| 合规 / 政策关键字审计 | 需要字面匹配，不是 paraphrase |

### 单靠 BM25 不够

| User Need | 为什么还是需要语义搜索 |
|-----------|------------------------|
| "怎么退款？" | 用户绝不会打"refund policy section 4" |
| "上一季有什么重点发现？" | 纯概念，没字面关键字 |
| 多语言或改述的 query | BM25 只看字面，太浅 |
| 容错的产品搜索 | Lexical match 对拼错就失效 |

**真正的答案是 hybrid**——两种并行——不是选边站。

---

## 四步骤（大白话）

1. **把问题拆成字**——"a INC-2023-Q4-011"变 `["a", "INC-2023-Q4-011"]`。
2. **算每个字有多常见**——"a"到处都是，ID 只出现一次。
3. **罕见字多给分**——ID 被当作强 signal；"a"被当作 noise。
4. **按总分排序文档**——提到罕见字的文档胜出。

注意这里没有模型、没有 embedding API、没有 GPU。BM25 纯粹是文字计数。这就是为什么它又便宜又快。

---

## PM 决策框架

| 问题 | 如果答 Yes | 含义 |
|------|-----------|------|
| 用户会输入字面识别码（ID、code、SKU）？ | Yes | 组合里要加 BM25。 |
| 语料是技术类（docs、reports、policies）？ | Yes | Hybrid 几乎都是赢家。 |
| Latency budget 紧？ | Yes | BM25 latency 是免费的——不调用 embedding。 |
| Embedding API 账单是痛点？ | Yes | BM25 能抵销成本——query 时不跑 embedding。 |
| 用户主要问概念问题？ | Yes | 语义搜索为主，BM25 当安全网。 |

---

## 成本与延迟现实检查

BM25 是你能加到 RAG 产品上最便宜的检索：

- **Query 时不调用 embedding API**——BM25 完全在你自己的 process 中对 indexed text 跑。
- **Index 建得快**——文字 tokenization 与计数，不用 GPU 数学。
- **内存占用小**——稀疏的 term-document matrix 压缩效率很好。

不加 BM25 的代价很隐微但严重：用户看到那些他们知道存在的 ID 被"很有自信地答错"时，信任会悄悄流失。Hybrid search 是便宜的信任保险。

---

## PM 常见错误

1. **相信"向量搜索解决一切"**——不会。用户一打 ID，纯向量 RAG 就破功。
2. **把 BM25 延后当 optimization**——它不是 optimization，它是精确查询的 correctness feature。
3. **没有字面 query 的 eval set**——eval 要混概念题跟 ID 题。少一种，regression 就躲起来。
4. **只把一种搜索的结果拿出来**——hybrid 是合并，不是择一。下一课讲合并策略。
5. **低估用户信任冲击**——一个 ID 答错失去的信任，比十个好答案累积的还多。

> **核心洞见**
>
> Hybrid retrieval 不是进阶升级——它是**任何会有用户输入精确识别码的 RAG 产品的基线**。语义搜索给你"看起来厉害"的答案；BM25 给你字面 query 上"正确"的答案。认真的产品两个都要。

---

## CCA 考试关联

- **D1（Agentic Architecture）**：了解 hybrid retrieval 是两种互补搜索方法的组合。
- **D5（Enterprise Deployment）**：BM25 在运维上便宜——它是流量放大时不会让 embedding 成本复利上升的检索层。
- **D2（Tool Design）**：如果把 retrieval 暴露成 tool，BM25 / 语义 / hybrid 的选择会形塑 tool description。
- 题目 pattern："纯语义搜索对含特定 code 的 query 返回不相关结果——怎么修？"→ 加 BM25 / hybrid search。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 实习生 vs Ctrl-F analogy 怎么对应 BM25？ | 语义搜索像聪明实习生，理解主题；BM25 像 Ctrl-F 高手，找字面 string。团队两个都要。 |
| 纯语义 RAG 产品什么时候在 production 崩掉？ | 用户第一次输入精确 ID、SKU 或 error code 的时候——语义搜索经常很自信地返回错文档。 |
| BM25 query time 需要调用 embedding API 吗？ | 不用。它对 indexed text 跑，不调用模型，所以便宜又低延迟。 |
| BM25 四个打分步骤（大白话）？ | 1) 把 query 拆成字、2) 算每个字多常见、3) 罕见字多给分、4) 按总分排 document。 |
| RAG 产品应该用 BM25 取代语义搜索吗？ | 不——两个并行跑（hybrid）。互相补漏。 |
| RAG eval set 应该长什么样？ | 概念题和字面识别码题混搭，才能量化 hybrid 品质。 |
| 忽略 BM25 的 PM 最大风险是什么？ | 用户信任崩盘——一个 ID 答错侵蚀的信任，比很多好的概念答案累积的还多。 |
| 哪类 token 最受益于 BM25？ | 罕见、技术性的字面 token：ID、SKU、error code、ticket 编号、CVE 编号、合同代码。 |
