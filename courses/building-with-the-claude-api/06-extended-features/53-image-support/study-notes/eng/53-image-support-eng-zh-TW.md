# Image Support — Engineering Deep Dive

| 項目 | 內容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — 主要；D5 — Enterprise Deployment (20%) — 次要 |
| Task Statements | 2.2（content blocks）、2.1（多模態輸入結構）、5.2（token 計價） |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 53 |

---

## One-Liner

Claude 的 image support 讓你把 image content block 丟進 user message 與 text 並列，用同一個 Messages API 變成多模態端點——搭配明確的配額、token 計價、以及文字任務該有的 prompt engineering 紀律。

---

## 多模態訊息，同一個 API

沒有另一個「vision」端點。你呼叫 `/v1/messages` 的方式不變；差別是 user message 的 `content` 變成一個可以同時放 **image block** 與 **text block** 的 list。Claude 讀完整個多模態 payload 後回一個普通 text block。

這個設計是刻意的：既有的訊息處理程式大多照舊能用，唯一要多學的是怎麼組 image block、以及它的 token 成本怎麼算。

---

## 必記的硬限制

課程點名了一組每個 production 部署都要遵守的限制：

- **單次 request 最多 100 張圖**（所有 messages 合計）。
- **單張圖最大 5 MB。**
- **只傳一張圖時**：最大長寬 **8000 px**。
- **傳多張圖時**：每張最大長寬 **2000 px**。
- 圖可以用 **base64 編碼**或**圖片 URL** 送。
- Token 成本公式：`tokens = (width_px × height_px) / 750`。

這個 token 公式對成本模型很重要。一張 1920×1080 的圖光是丟進 prompt 就要 `2,764` tokens——還沒算 text 或回應 tokens。要積極縮圖：1024×1024 約 1400 tokens、512×512 約 350 tokens。不需要全解析度就不要傳全解析度。

---

## Image Block 結構

Image block 放在 user message 的 content list 裡，和 text block 並列：

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

重點：

- `type: "image"`——不是 `"image_url"` 或別的。
- `source.type: "base64"`——另一個選項是 URL。
- `source.media_type`——必須和真實檔案匹配（`image/png`、`image/jpeg` 等）。
- `source.data`——base64 字串，不是原始 bytes。

留意順序：先 image block，再 text block。課程範例把問題放在圖片**之後**，讀起來像「看這個，然後回答這個」。兩種順序都可以，但實務上把圖片先擺、問題緊接著最乾淨。

---

## Message flow 沒變

Request/response 流程完全和純文字對話一樣。你的伺服器送一個包含混合 block 的 user message，Claude 回一個 text block 分析結果。多輪對話、tool use、system prompt——圖像輸入之上全都照舊運作。迴圈裡沒有任何東西因為某一輪包含圖片而改變。

這是 content-block 導向 API 的隱藏好處：新增一個模態不需要新 endpoint 或新 handler。

---

## Prompting 技巧：同樣的規則

這堂課最大的要點：**你對文字用的 prompt engineering 技巧，對圖片同樣適用**。一個天真的問題「這張圖裡有幾顆彈珠？」常常會數錯；一個好設計的 prompt 則不會。

課程示範的三個技巧：

1. **詳細的指引與分析步驟。** 告訴 Claude 要用什麼方法，而不只是問問題。
2. **One-shot 或 multi-shot 範例。** 附一張你已經知道答案的參考圖、寫出正確答案，再問目標圖。Claude 會對著範例校準。
3. **把複雜任務拆成小步驟。** 與其直接要最終答案，先要中間觀察，再要最終判斷。

### 課程的逐步計數範例

```
Analyze this image of marbles and determine the exact count using this methodology:
1. Begin by identifying each unique marble one at a time. Assign each a number as you identify it.
2. Verify your result by counting with a different method. Start from the bottom-left corner and work row by row, from left to right.

What is the exact, verified number of marbles in this image?
```

這個簡單的轉換——從「幾顆？」變成「用這個方法數，然後用第二種方法驗證」——不換模型、不換圖片，準確度就大幅提升。

---

## 實務例：火災風險評估

課程走過一個用衛星影像自動化住家保險火災風險評估的例子。保險公司不再派人到現場，而是把衛星影像和一個結構化 prompt 一起送給 Claude。

Prompt 把任務拆成五個明確步驟：辨識主要住宅、樹冠懸伸分析、火災風險評估、防護空間辨識、最後給 1 到 4 的數字評級。每一步都精確告訴 Claude 要看什麼。

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

從這個 prompt 內化兩個 pattern：

1. **命名步驟加上明確子問題。** 不是「評估這個物件」而是「找最大的屋頂結構、規則幾何、與車道連接」。
2. **量化輸出用分類區間。** 不要只問一個分數，而是定義 1、2、3、4 各代表什麼，等於給一份 rubric，產出會穩定非常多。

---

## Common Mistakes

1. **對難的視覺任務用簡單問題。** 沒給方法論的「幾顆彈珠？」結果不可靠。把文字 prompt 紀律帶到圖像任務。
2. **忽略 token 公式。** `tokens = (w × h) / 750` 意味著全解析度圖會默默吃掉 token 預算。編碼前先縮圖。
3. **超過單張圖大小限制。** 5 MB、單圖 8000 px、多圖 2000 px 都是硬停，違規 API 會直接拒絕。
4. **忘記 100 張圖的 per-request 上限。** 大量視覺流程必須以 100 為單位 batch。
5. **`media_type` 和實際檔案不一致。** 對 JPEG 宣告 `image/png` 會讓解碼混亂。檢查檔案，不要猜。
6. **把 image block 當成 URL 欄位。** 它是一個結構化的 content block，有 `type`、`source.type`、`source.media_type`、`source.data`。單純的 URL 字串不能用。

---

> **Key Insight**
>
> Claude 的 image support 不是另一個產品——它只是 Messages API 裡的一種新 block 類型。API 表面不難；production 真正重要的是 **token 計價**（width × height / 750 公式）和 **prompt 紀律**（step-by-step 方法論、rubric、one-shot 範例對圖像和對文字一樣重要）。

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**：Image block 是 content-block 變體——記得 `type: "image"` 結構、`source.type: "base64"`、以及 `media_type` 欄位。
- **D5 (Enterprise Deployment)**：記住配額（100 張、5 MB、8000 px / 2000 px）與 token 公式 `(w × h) / 750` 用於成本規劃。
- 可能的題型：「為什麼我的圖像任務準確度很低？」預期答案通常是「對圖片套用和文字一樣的 prompt engineering：方法論、one-shot 範例、步驟拆解。」

---

## Flashcards

| Front | Back |
|-------|------|
| 單次 Claude API request 最多幾張圖？ | 全部 messages 合計 100 張。 |
| 單張圖檔案大小上限？ | 5 MB。 |
| 單圖 vs 多圖的最大長寬是多少？ | 單圖 8000 px，多圖每張 2000 px。 |
| 圖片 token 成本的公式是？ | `tokens = (width_px × height_px) / 750`。 |
| 送圖給 Claude 的兩種方式？ | Base64 編碼內嵌，或圖片 URL。 |
| 圖片用哪個 block type？資料放在哪個欄位？ | `type: "image"`，`source.type: "base64"`，`source.data` 放 base64 字串（加 `source.media_type`）。 |
| 為什麼「有幾顆彈珠？」在圖片任務上常失敗？ | 那是天真的 prompt。圖像任務需要和文字一樣的方法論、step-by-step 指令、one-shot 範例。 |
| 課程建議圖像任務用哪三個 prompting 技巧？ | 1) 詳細指引與方法論，2) one-shot 或 multi-shot 範例，3) 拆成小步驟。 |
| 加入圖片會改變 message flow 嗎？ | 不會——仍然是 user message 送到 `/v1/messages`、回一個 text block。迴圈沒變。 |
