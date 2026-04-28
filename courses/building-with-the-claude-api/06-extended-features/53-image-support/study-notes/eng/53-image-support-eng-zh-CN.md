# Image Support — Engineering Deep Dive

| 项目 | 内容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — 主要；D5 — Enterprise Deployment (20%) — 次要 |
| Task Statements | 2.2（content blocks）、2.1（多模态输入结构）、5.2（token 计费） |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 53 |

---

## One-Liner

Claude 的 image support 让你把 image content block 塞进 user message 与 text 并列，用同一个 Messages API 变成多模态端点——搭配明确的配额、token 计费、以及文字任务该有的 prompt engineering 纪律。

---

## 多模态消息，同一个 API

没有另一个"vision"端点。你调用 `/v1/messages` 的方式不变；差别是 user message 的 `content` 变成一个可以同时放 **image block** 与 **text block** 的 list。Claude 读完整个多模态 payload 后回一个普通 text block。

这个设计是刻意的：既有的消息处理代码大多照旧能用，唯一要多学的是怎么组 image block、以及它的 token 成本怎么算。

---

## 必记的硬约束

课程点名了一组每个 production 部署都要遵守的限制：

- **单次 request 最多 100 张图**（所有 messages 合计）。
- **单张图最大 5 MB。**
- **只传一张图时**：最大长宽 **8000 px**。
- **传多张图时**：每张最大长宽 **2000 px**。
- 图可以用 **base64 编码**或**图片 URL** 发送。
- Token 成本公式：`tokens = (width_px × height_px) / 750`。

这个 token 公式对成本模型很重要。一张 1920×1080 的图光是塞进 prompt 就要 `2,764` tokens——还没算 text 或响应 tokens。要积极缩图：1024×1024 约 1400 tokens、512×512 约 350 tokens。不需要全分辨率就不要传全分辨率。

---

## Image Block 结构

Image block 放在 user message 的 content list 里，和 text block 并列：

```python
import base64

with open("image.png", "rb") as f:
    image_bytes = base64.standard_b64encode(f.read()).decode("utf-8")

add_user_message(messages, [
    # Image Block
    {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/png",
            "data": image_bytes,
        }
    },
    # Text Block
    {
        "type": "text",
        "text": "What do you see in this image?"
    }
])
```

要点：

- `type: "image"`——不是 `"image_url"` 或别的。
- `source.type: "base64"`——另一个选项是 URL。
- `source.media_type`——必须和真实文件匹配（`image/png`、`image/jpeg` 等）。
- `source.data`——base64 字符串，不是原始 bytes。

留意顺序：先 image block，再 text block。课程示例把问题放在图片**之后**，读起来像"看这个，然后回答这个"。两种顺序都可以，但实务上把图片先放、问题紧接着最干净。

---

## Message flow 没变

Request/response 流程完全和纯文字对话一样。你的服务器发送一个包含混合 block 的 user message，Claude 回一个 text block 分析结果。多轮对话、tool use、system prompt——图像输入之上全都照旧运作。循环里没有任何东西因为某一轮包含图片而改变。

这是 content-block 导向 API 的隐藏好处：新增一个模态不需要新 endpoint 或新 handler。

---

## Prompting 技巧：同样的规则

这堂课最大的要点：**你对文字用的 prompt engineering 技巧，对图片同样适用**。一个天真的问题"这张图里有几颗弹珠？"常常会数错；一个好设计的 prompt 则不会。

课程示范的三个技巧：

1. **详细的指引与分析步骤。** 告诉 Claude 要用什么方法，而不只是问问题。
2. **One-shot 或 multi-shot 示例。** 附一张你已经知道答案的参考图、写出正确答案，再问目标图。Claude 会对着示例校准。
3. **把复杂任务拆成小步骤。** 与其直接要最终答案，先要中间观察，再要最终判断。

### 课程的逐步计数示例

```
Analyze this image of marbles and determine the exact count using this methodology:
1. Begin by identifying each unique marble one at a time. Assign each a number as you identify it.
2. Verify your result by counting with a different method. Start from the bottom-left corner and work row by row, from left to right.

What is the exact, verified number of marbles in this image?
```

这个简单的转换——从"几颗？"变成"用这个方法数，然后用第二种方法验证"——不换模型、不换图片，准确度就大幅提升。

---

## 实务例：火灾风险评估

课程走过一个用卫星影像自动化住家保险火灾风险评估的例子。保险公司不再派人到现场，而是把卫星影像和一个结构化 prompt 一起发送给 Claude。

Prompt 把任务拆成五个明确步骤：识别主要住宅、树冠悬伸分析、火灾风险评估、防护空间识别、最后给 1 到 4 的数字评级。每一步都精确告诉 Claude 要看什么。

```
Analyze the attached satellite image of a property with these specific steps:

1. Residence identification: Locate the primary residence on the property by looking for:
   - The largest roofed structure
   - Typical residential features (driveway connection, regular geometry)
   - Distinction from other structures (garages, sheds, pools)

2. Tree overhang analysis: Examine all trees near the primary residence:
   - Identify any trees whose canopy extends directly over any portion of the roof
   - Estimate the percentage of roof covered by overhanging branches (0-25%, 25-50%, 50-75%, 75%+)
   - Note particularly dense areas of overhang

3. Fire risk assessment: For any overhanging trees, evaluate:
   - Potential wildfire vulnerability (ember catch points, continuous fuel paths to structure)
   - Proximity to chimneys, vents, or other roof openings if visible
   - Areas where branches create a "bridge" between wildland vegetation and the structure

4. Defensible space identification: Assess the property's overall vegetative structure:
   - Identify if trees connect to form a continuous canopy over or near the home
   - Note any obvious fuel ladders (vegetation that can carry fire from ground to tree to roof)

5. Fire risk rating: Based on your analysis, assign a Fire Risk Rating from 1-4:
   - Rating 1 (Low Risk): No tree branches overhanging the roof, good defensible space around the home
   - Rating 2 (Moderate Risk): Minimal overhang (<25% of roof), some separation between tree canopies
   - Rating 3 (High Risk): Significant overhang (25-50% of roof), connected tree canopies, multiple vulnerability points
   - Rating 4 (Severe Risk): Extensive overhang (>50% of roof), dense vegetation against structure

For each item above (1-5), write one sentence summarizing your findings, with your final response being the numerical rating.
```

从这个 prompt 内化两个 pattern：

1. **命名步骤加上明确子问题。** 不是"评估这个物件"而是"找最大的屋顶结构、规则几何、与车道连接"。
2. **量化输出用分类区间。** 不要只问一个分数，而是定义 1、2、3、4 各代表什么，等于给一份 rubric，产出会稳定非常多。

---

## Common Mistakes

1. **对难的视觉任务用简单问题。** 没给方法论的"几颗弹珠？"结果不可靠。把文字 prompt 纪律带到图像任务。
2. **忽略 token 公式。** `tokens = (w × h) / 750` 意味着全分辨率图会默默吃掉 token 预算。编码前先缩图。
3. **超过单张图大小限制。** 5 MB、单图 8000 px、多图 2000 px 都是硬停，违规 API 会直接拒绝。
4. **忘记 100 张图的 per-request 上限。** 大量视觉流程必须以 100 为单位 batch。
5. **`media_type` 和实际文件不一致。** 对 JPEG 声明 `image/png` 会让解码混乱。检查文件，不要猜。
6. **把 image block 当成 URL 字段。** 它是一个结构化的 content block，有 `type`、`source.type`、`source.media_type`、`source.data`。单纯的 URL 字符串不能用。

---

> **Key Insight**
>
> Claude 的 image support 不是另一个产品——它只是 Messages API 里的一种新 block 类型。API 表面不难；production 真正重要的是 **token 计费**（width × height / 750 公式）和 **prompt 纪律**（step-by-step 方法论、rubric、one-shot 示例对图像和对文字一样重要）。

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**：Image block 是 content-block 变体——记得 `type: "image"` 结构、`source.type: "base64"`、以及 `media_type` 字段。
- **D5 (Enterprise Deployment)**：记住配额（100 张、5 MB、8000 px / 2000 px）与 token 公式 `(w × h) / 750` 用于成本规划。
- 可能的题型："为什么我的图像任务准确度很低？"预期答案通常是"对图片套用和文字一样的 prompt engineering：方法论、one-shot 示例、步骤拆解。"

---

## Flashcards

| Front | Back |
|-------|------|
| 单次 Claude API request 最多几张图？ | 全部 messages 合计 100 张。 |
| 单张图文件大小上限？ | 5 MB。 |
| 单图 vs 多图的最大长宽是多少？ | 单图 8000 px，多图每张 2000 px。 |
| 图片 token 成本的公式是？ | `tokens = (width_px × height_px) / 750`。 |
| 发送图给 Claude 的两种方式？ | Base64 编码内嵌，或图片 URL。 |
| 图片用哪个 block type？数据放在哪个字段？ | `type: "image"`，`source.type: "base64"`，`source.data` 放 base64 字符串（加 `source.media_type`）。 |
| 为什么"有几颗弹珠？"在图片任务上常失败？ | 那是天真的 prompt。图像任务需要和文字一样的方法论、step-by-step 指令、one-shot 示例。 |
| 课程建议图像任务用哪三个 prompting 技巧？ | 1) 详细指引与方法论，2) one-shot 或 multi-shot 示例，3) 拆成小步骤。 |
| 加入图片会改变 message flow 吗？ | 不会——仍然是 user message 发到 `/v1/messages`、回一个 text block。循环没变。 |
