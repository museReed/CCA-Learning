# Image Support — PM Perspective

| 項目 | 內容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) — 主要；D5 — Enterprise Deployment (20%) — 次要 |
| Task Statements | 2.2（content blocks）、2.1（多模態輸入）、5.2（token 計價） |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 53 |

---

## One-Liner

Image support 讓同一個 Claude API 變成多模態端點，一口氣打開許多過去卡在人工視覺作業的產品類別——保險勘查、醫療分診、零售分析、現場作業自動化。

---

## Mental Model：把照片交給分析師

想像你公司最強的分析師。你問「這個辦公室怎麼了？」他能回答問題、發現異常、歸納模式。但今天你必須**用嘴**描述場景給他聽。Image support 就是把實體照片交到他手上。

你能問的問題沒變。變的是現在這些問題的答案是基於真實視覺證據，而不是你對場景的描述。而且因為 Claude 直接讀圖，分析師永遠不會漏掉「你描述中沒提到」的東西。

這是任何「答案要靠看、而不只是讀」的產品最大的一次解鎖。

---

## PM 為什麼該在意

過去難以或無法自動化的產品類別，現在變得可行：

- **保險勘查**：衛星或空拍影像搭配 rubric prompt 取代現場勘查員。
- **醫療分診**：皮膚科 app 請 Claude 分類可見病灶（需在醫師監督下）。
- **電商**：自動分類賣家上傳的商品照片。
- **無障礙**：即時為圖片生成豐富的 alt-text。
- **內容審查**：在大量圖像動態裡標記敏感內容。
- **零售分析**：從店內照片計算貨架、偵測缺貨、稽核陳列。

同一個 Messages API 全都吃。沒有另一個 vision 產品、沒有另一份定價、沒有另一個 SDK——就是在你現有的 request 裡多放一個 content block。

---

## Product Use Cases

### Image support 合適的情境

| 需求 | 為何可行 |
|------|---------|
| 回答基於真實圖片的問題（這張照片裡有什麼？） | 核心能力——Claude 直接看圖 |
| 從視覺內容中結構化擷取（計數、類別標籤） | 搭配良好 rubric 可行 |
| 依書面標準做品質管制或視覺稽核 | Rubric + 逐步 prompt 可產生穩定一致的評分 |
| 多張圖並排比較 | 每個 request 最多 100 張，適合前後對照或批次比對 |

### 不適合的情境

| 需求 | 更好的選擇 |
|------|-----------|
| 即時影片分析 | Vision API 是單張圖 one-shot，不是影片管線 |
| 像素級測量或小字 OCR | 專門的 OCR / CV 工具，必要時再和 Claude 組合做推理 |
| 醫療診斷（作為唯一決策者） | 永遠搭配醫師；不要出貨自動診斷 |
| 高吞吐量 + 低預算的批次處理 | 每張圖成本隨解析度增長，要早期算清 token 數學 |

---

## PM 決策框架

| 問題 | 若答 Yes | 意涵 |
|------|---------|------|
| 使用者 workflow 真的需要判讀圖像嗎？ | Yes | Image support 是合適候選。 |
| 答案可以從一張靜態影格導出嗎？ | Yes | 你在 Claude 的甜蜜區。 |
| 我們每次 request 會送超過 100 張圖嗎？ | Yes | 必須 batch——100 張是硬上限。 |
| 我們能把圖縮到最小可用尺寸嗎？ | Yes | 就做。Token 是 `(width × height) / 750`，大小直接影響錢。 |
| 我們需要像素級測量或小字 OCR 嗎？ | Yes | 先用專門前處理器。Claude 是對圖像推理，不是精密量測。 |
| 我們能寫一份 rubric 或方法論給模型跟嗎？ | Yes | 準確度會跳升。天真的 prompt 通常不達標。 |

---

## Cost、Accuracy、UX 權衡

這個 token 公式比表面看起來更重要。`(width × height) / 750` 對像素數呈線性，意思是**解析度翻倍，token 成本變四倍**。一張 1170×2532 的手機截圖每次呼叫約 3950 tokens。每天 10 萬次呼叫，月帳單上就是一條看得見的 line item。

三條 PM playbook：

1. **積極前處理。** 把圖縮到還能讓 Claude 看出重點的最小尺寸。上線前要測出準確度下限。
2. **套用文字 prompt 的紀律。** 天真的「這張圖裡有什麼？」會低效。給 Claude rubric、方法論、最好還有 one-shot 參考。
3. **為 100 張上限規劃預算。** 若每個使用者 session 要處理數百張圖，batching 層必須明確設計。

---

## Prompt Engineering 的平行對應

PRD 要釘死的一件事：**你對文字用的 prompt engineering 技巧，對圖片同樣適用**。這是課程的重點，也是多數天真整合會失分的地方：

- 簡單問題 → 不穩定答案（「幾顆彈珠？」→ 數錯）。
- 詳細方法論 + one-shot 範例 + 步驟拆解 → 穩定答案。
- 分類 rubric（定義 1、2、3、4 代表什麼）→ 量化輸出穩定很多。

課程裡的火災風險評估就是 PM 範本：命名步驟、列每步要看什麼、明確定義輸出類別。任何 vision 功能的 PRD 都該長這樣。

---

## Common PM Mistakes

1. **寫「分析這張圖」卻沒給方法論。** 模型會做些事，但不穩定。把 rubric 寫進 PRD。
2. **忽略 token 數學。** 一張全解析度手機截圖可能相當於好幾頁文字的成本。選功能前要先建模。
3. **跳過圖像上限的審視。** 有些流程默默需要超過 100 張，只有在 production 才發現。
4. **把 image support 當成另一個產品。** 它是同一個 Messages API 裡的一種 content block，你現有的 retry、logging、auth 全都能用。
5. **沒有準確度 eval set 就出貨 image 功能。** 在沒標過代表性樣本前，你根本不知道功能夠不夠好。
6. **忘了對使用者上傳的圖做 safety review。** 當使用者能上傳任意圖片，內容審查和隱私策略就要升級。

---

> **Key Insight**
>
> Image support 是 Claude API 最大的多模態產品解鎖，而且工程成本幾乎為零——它只是在既有 request 裡多一個 block。PM 真正的工作全在 **prompt rubric**（詳細方法論、one-shot 範例、分類輸出）和 **token 數學**（縮圖、圍繞 100 張上限做 batch）。把這兩件事做對，整類原本要靠人工的視覺作業就能自動化。

---

## CCA Exam Relevance

- **D2 (Tool Design & MCP Integration)**：把 image block 認成同一個 Messages API 的 content-block 變體；沒有另一個 endpoint。
- **D5 (Enterprise Deployment)**：記住配額（100 張、5 MB、單圖 8000 px / 多圖 2000 px）與 `(w × h) / 750` token 公式。
- 可能的情境題：「圖像分析結果不穩定——你建議怎麼做？」預期答案是套用文字等級的 prompt 紀律（方法論、one-shot、拆解）並把圖縮到合適尺寸。

---

## Flashcards

| Front | Back |
|-------|------|
| Image support 的分析師類比是什麼？ | 以前你得用嘴描述照片給分析師，現在你直接把照片交給他——問題一樣，但依據是真的影像。 |
| Image support 解鎖了哪些產品類別？ | 保險勘查、醫療分診（需醫師監督）、電商標籤、無障礙 alt-text、內容審查、零售分析。 |
| 每次 request 圖像的硬上限是幾張？ | 所有 messages 合計 100 張。 |
| 單張圖檔案大小上限？ | 5 MB。 |
| 圖片 token 公式是？ | `tokens = (width × height) / 750`。解析度翻倍，成本變四倍。 |
| 為什麼天真 prompt 在圖像任務上表現不佳？ | 因為圖像任務和文字一樣需要方法論、rubric、one-shot 範例、步驟拆解。 |
| Vision 功能的 PRD 該包含什麼？ | Rubric / 方法論、token 成本模型、100 張上限的 batching 計畫、準確度 eval set、上傳的 safety review。 |
| 什麼時候不該用 image support？ | 即時影片、像素級量測、獨立決策的醫療診斷、或高吞吐量 + 低預算批次處理。 |
