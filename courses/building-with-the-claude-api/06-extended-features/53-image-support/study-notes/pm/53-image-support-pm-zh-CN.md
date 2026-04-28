# Image Support — PM Perspective

| 项目 | 内容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — 主要；D5 — Enterprise Deployment (20%) — 次要 |
| Task Statements | 2.2（content blocks）、2.1（多模态输入）、5.2（token 计费） |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 53 |

---

## One-Liner

Image support 让同一个 Claude API 变成多模态端点，一口气打开许多过去卡在人工视觉作业的产品类别——保险勘查、医疗分诊、零售分析、现场作业自动化。

---

## Mental Model：把照片交给分析师

想象你公司最强的分析师。你问"这个办公室怎么了？"他能回答问题、发现异常、归纳模式。但今天你必须**用嘴**描述场景给他听。Image support 就是把实体照片交到他手上。

你能问的问题没变。变的是现在这些问题的答案是基于真实视觉证据，而不是你对场景的描述。而且因为 Claude 直接读图，分析师永远不会漏掉"你描述中没提到"的东西。

这是任何"答案要靠看、而不只是读"的产品最大的一次解锁。

---

## PM 为什么该在意

过去难以或无法自动化的产品类别，现在变得可行：

- **保险勘查**：卫星或航拍影像搭配 rubric prompt 取代现场勘查员。
- **医疗分诊**：皮肤科 app 请 Claude 分类可见病灶（需在医师监督下）。
- **电商**：自动分类卖家上传的商品照片。
- **无障碍**：即时为图片生成丰富的 alt-text。
- **内容审查**：在大量图像动态里标记敏感内容。
- **零售分析**：从店内照片计算货架、检测缺货、审查陈列。

同一个 Messages API 全都吃。没有另一个 vision 产品、没有另一份定价、没有另一个 SDK——就是在你现有的 request 里多放一个 content block。

---

## Product Use Cases

### Image support 合适的情境

| 需求 | 为何可行 |
|------|---------|
| 回答基于真实图片的问题（这张照片里有什么？） | 核心能力——Claude 直接看图 |
| 从视觉内容中结构化抽取（计数、类别标签） | 搭配良好 rubric 可行 |
| 依书面标准做品质管制或视觉审查 | Rubric + 逐步 prompt 可产生稳定一致的评分 |
| 多张图并排比较 | 每个 request 最多 100 张，适合前后对照或批次比对 |

### 不适合的情境

| 需求 | 更好的选择 |
|------|-----------|
| 即时视频分析 | Vision API 是单张图 one-shot，不是视频管线 |
| 像素级测量或小字 OCR | 专门的 OCR / CV 工具，必要时再和 Claude 组合做推理 |
| 医疗诊断（作为唯一决策者） | 永远搭配医师；不要发布自动诊断 |
| 高吞吐量 + 低预算的批次处理 | 每张图成本随分辨率增长，要早期算清 token 数学 |

---

## PM 决策框架

| 问题 | 若答 Yes | 含义 |
|------|---------|------|
| 用户 workflow 真的需要判读图像吗？ | Yes | Image support 是合适候选。 |
| 答案可以从一张静态帧导出吗？ | Yes | 你在 Claude 的甜蜜区。 |
| 我们每次 request 会发送超过 100 张图吗？ | Yes | 必须 batch——100 张是硬上限。 |
| 我们能把图缩到最小可用尺寸吗？ | Yes | 就做。Token 是 `(width × height) / 750`，大小直接影响钱。 |
| 我们需要像素级测量或小字 OCR 吗？ | Yes | 先用专门前处理器。Claude 是对图像推理，不是精密量测。 |
| 我们能写一份 rubric 或方法论给模型跟吗？ | Yes | 准确度会跳升。天真的 prompt 通常不达标。 |

---

## Cost、Accuracy、UX 权衡

这个 token 公式比表面看起来更重要。`(width × height) / 750` 对像素数呈线性，意思是**分辨率翻倍，token 成本变四倍**。一张 1170×2532 的手机截图每次调用约 3950 tokens。每天 10 万次调用，月账单上就是一条看得见的 line item。

三条 PM playbook：

1. **积极前处理。** 把图缩到还能让 Claude 看出重点的最小尺寸。上线前要测出准确度下限。
2. **套用文字 prompt 的纪律。** 天真的"这张图里有什么？"会低效。给 Claude rubric、方法论、最好还有 one-shot 参考。
3. **为 100 张上限规划预算。** 若每个用户 session 要处理数百张图，batching 层必须明确设计。

---

## Prompt Engineering 的平行对应

PRD 要钉死的一件事：**你对文字用的 prompt engineering 技巧，对图片同样适用**。这是课程的重点，也是多数天真整合会失分的地方：

- 简单问题 → 不稳定答案（"几颗弹珠？"→ 数错）。
- 详细方法论 + one-shot 示例 + 步骤拆解 → 稳定答案。
- 分类 rubric（定义 1、2、3、4 代表什么）→ 量化输出稳定很多。

课程里的火灾风险评估就是 PM 模板：命名步骤、列每步要看什么、明确定义输出类别。任何 vision 功能的 PRD 都该长这样。

---

## Common PM Mistakes

1. **写"分析这张图"却没给方法论。** 模型会做些事，但不稳定。把 rubric 写进 PRD。
2. **忽略 token 数学。** 一张全分辨率手机截图可能相当于好几页文字的成本。选功能前要先建模。
3. **跳过图像上限的审视。** 有些流程默默需要超过 100 张，只有在 production 才发现。
4. **把 image support 当成另一个产品。** 它是同一个 Messages API 里的一种 content block，你现有的 retry、logging、auth 全都能用。
5. **没有准确度 eval set 就发布 image 功能。** 在没标过代表性样本前，你根本不知道功能够不够好。
6. **忘了对用户上传的图做 safety review。** 当用户能上传任意图片，内容审查和隐私策略就要升级。

---

> **Key Insight**
>
> Image support 是 Claude API 最大的多模态产品解锁，而且工程成本几乎为零——它只是在既有 request 里多一个 block。PM 真正的工作全在 **prompt rubric**（详细方法论、one-shot 示例、分类输出）和 **token 数学**（缩图、围绕 100 张上限做 batch）。把这两件事做对，整类原本要靠人工的视觉作业就能自动化。

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**：把 image block 认成同一个 Messages API 的 content-block 变体；没有另一个 endpoint。
- **D5 (Enterprise Deployment)**：记住配额（100 张、5 MB、单图 8000 px / 多图 2000 px）与 `(w × h) / 750` token 公式。
- 可能的情境题："图像分析结果不稳定——你建议怎么做？"预期答案是套用文字级的 prompt 纪律（方法论、one-shot、拆解）并把图缩到合适尺寸。

---

## Flashcards

| Front | Back |
|-------|------|
| Image support 的分析师类比是什么？ | 以前你得用嘴描述照片给分析师，现在你直接把照片交给他——问题一样，但依据是真的影像。 |
| Image support 解锁了哪些产品类别？ | 保险勘查、医疗分诊（需医师监督）、电商标签、无障碍 alt-text、内容审查、零售分析。 |
| 每次 request 图像的硬上限是几张？ | 所有 messages 合计 100 张。 |
| 单张图文件大小上限？ | 5 MB。 |
| 图片 token 公式是？ | `tokens = (width × height) / 750`。分辨率翻倍，成本变四倍。 |
| 为什么天真 prompt 在图像任务上表现不佳？ | 因为图像任务和文字一样需要方法论、rubric、one-shot 示例、步骤拆解。 |
| Vision 功能的 PRD 该包含什么？ | Rubric / 方法论、token 成本模型、100 张上限的 batching 计画、准确度 eval set、上传的 safety review。 |
| 什么时候不该用 image support？ | 即时视频、像素级量测、独立决策的医疗诊断、或高吞吐量 + 低预算批次处理。 |
