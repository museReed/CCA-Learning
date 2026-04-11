# Response Streaming — PM 視角

| 項目 | 細節 |
|------|------|
| 考試領域 | D5 — Enterprise Deployment (20%) |
| Task Statements | 5.2（streaming 與回應速度）、5.3（production 模式） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 13 |

---

## 一句話總結

Streaming 是把 20 秒等待變成 200 毫秒「Claude is writing…」體驗的產品 feature——它是所有面向使用者的 AI chat 產品最重要的單一延遲優化，也是 demo 和真正產品的定義性差別。

---

## 心智模型：餐廳廚房

想像兩家餐廳供應同一道菜：

| 餐廳 | 體驗 | 食客反應 |
|------|------|---------|
| **Blocking** | 你點餐，主廚沉默地煮 20 分鐘，侍者把完成的盤子放到你面前 | 「他們忘了我的餐點嗎？」→ 焦慮、差評 |
| **Streaming** | 你點餐，跑堂立刻送麵包，接著前菜，然後主菜一盤一盤上 | 「一切都在流動」→ 平靜、好評 |

總烹飪時間一樣。體驗完全不同。Streaming 就是 LLM UX 的跑堂侍者。

---

## 為什麼 PM 要在乎

AI chat app 的使用者研究一致顯示**感受延遲主導滿意度**。使用者願意原諒慢回應，只要能看到進度。他們會拋棄快回應，只要看到轉圈超過 2-3 秒沒有回饋。

Streaming 直接解決：

- **放棄率**——在回應到之前關掉分頁的使用者
- **感受品質**——「這 app 很順」vs「這 app 壞了」
- **信任**——可見的進度訊號傳達「系統活著」
- **與期望的比較**——使用者已經被 ChatGPT / Claude.ai 訓練成預期 streaming。Blocking 回應感覺過時

如果你的產品有 chat 介面而且不 streaming，不管底層 model 多好，都會感覺比每個競爭對手都差。

---

## 產品使用情境

### 永遠要 Stream

| 產品 | 原因 |
|------|------|
| 對話式 chat UI | 使用者預期即時生成——ChatGPT 基準線 |
| 長文內容生成器（部落格、文章） | 幾秒等待扼殺 engagement |
| Code 助手 | 使用者想立刻開始讀 fix |
| 家教 / 解說工具 | 漸進式解說教學更好 |
| 任何「Claude 在思考…」UX | Streaming 就是思考指示 |

### Streaming 較不關鍵

| 產品 | 原因 |
|------|------|
| 非同步背景工作（晚點寄出的 email summary） | 沒有使用者在等 |
| 短分類輸出（1-token label） | 生成已經夠快 |
| Webhook 驅動的整合 | 接收端沒有人 |
| Analytics pipelines | 批次處理，延遲無關 |

---

## 使用者感受延遲公式

每個 chat feature 的 PM 都該追蹤三個數字：

1. **Time to first token (TTFT)**——使用者看到任何東西前的時間。這是使用者感受的數字。目標：< 1 秒
2. **Tokens per second (TPS)**——streaming 開始後文字出現的速度。目標：匹配閱讀速度（~15 tokens/sec 就行）
3. **Total time to completion**——完整回應時間。如果 TTFT 低，使用者對這個不敏感

Streaming 把使用者注意力從第三個數字（Claude 控制有限）挪到第一個（streaming 幾乎給你即時 TTFT）。這是 streaming 勝出的數學原因。

---

## PM 決策框架

規劃 chat feature 時問這些問題：

| 問題 | 如果 Yes | 意涵 |
|------|---------|------|
| 有人類在等回應嗎？ | Yes | Stream |
| 回應可能超過 2 秒嗎？ | Yes | Stream |
| 產品跟 ChatGPT 式 UI 競爭嗎？ | Yes | Stream——不 stream 感覺過時 |
| 使用者會邊看邊讀輸出嗎？ | Yes | Stream |
| 輸出很短（單次分類、yes/no）嗎？ | No | Streaming 增加複雜度但 UX 收益很少 |

預設應該是「有人在等的都 stream」。不 streaming 是例外。

---

## UX 考量

Streaming 引入 blocking 沒有的新 UX 問題：

- **游標 / 箭頭指示**——streaming 時顯示閃爍游標讓使用者知道生成中
- **停止按鈕**——streaming 讓使用者能取消長回應；這是預期的 affordance
- **Stream 中途錯誤**——連線半途斷掉怎麼顯示？設計「從這裡重試」模式
- **Code block 渲染**——逐 token stream 的 markdown code block 需要小心渲染，避免中途看起來壞掉
- **Scroll 行為**——UI 要自動跟著 streamed 文字 scroll 嗎？通常要，但要允許使用者跳出

這些在 blocking 回應都不存在。加進驗收標準。

---

## 常見 PM 錯誤

1. **沒在 PRD 指定 streaming**——工程師預設選最容易的，你繼承糟糕 UX
2. **測總延遲而不是 TTFT**——對 streaming UX 總時間是錯的 metric
3. **沒設計停止 / 取消按鈕**——使用者預期有；沒有的話他們會關分頁
4. **只測短回應**——streaming 對長輸出最重要。測 1000-token 回應
5. **假設 streaming 純粹是工程工作**——streaming 是有 UX、錯誤處理、取消語意的面向使用者 feature。需要 PM 設計

> **Key Insight**
>
> Streaming 不是效能優化——它是現代 AI chat 產品的核心 UX 模式。使用者已經被 ChatGPT 訓練成預期漸進渲染，blocking 回應立刻讀成「舊的」或「壞的」。對任何做 AI feature 的 PM，指定 streaming（加上相關 UX——游標、停止按鈕、stream 中錯誤優雅處理）是入場門檻。

---

## CCA 考試重點

- **D5.2（streaming 與回應速度）**：預期考 streaming 何時適當、它解決什麼問題（感受延遲，不是總延遲）、以及它在 production chat 系統的角色
- **D5.3（production 模式）**：streaming 是面向使用者 chat 的標準 production 模式——注意情境題
- 記住：streaming 不降低總生成時間；它降低 time-to-first-token

---

## Flashcards

| 題目 | 答案 |
|------|------|
| Streaming 解決什麼產品問題？ | Chat UI 的高使用者感受延遲——「我在盯著壞掉的轉圈嗎？」問題 |
| Streaming 會讓 Claude 更快嗎？ | 不會——它讓 Claude 感覺更快，邊生成邊顯示。總時間不變 |
| 「time to first token」是什麼，為什麼重要？ | 使用者看到第一塊文字前的延遲。它主導使用者滿意度，勝過總延遲 |
| Streaming 的餐廳類比是什麼？ | 跑堂侍者——麵包、前菜、主菜漸進出現，而不是等 20 分鐘一個放下的盤子 |
| Streaming 需要哪些 UX affordance？ | 閃爍游標、停止 / 取消按鈕、stream 中錯誤處理、auto-scroll 行為 |
| 什麼時候 streaming 不重要？ | 非同步背景工作、很短的分類輸出、webhook 驅動整合——任何沒有人即時在等的 |
| PM 該為 streaming feature 追蹤哪些 metric？ | Time to first token (TTFT)、tokens per second (TPS)、total time——按 UX 重要性依序 |
| 為什麼 blocking UX 現在對使用者感覺「過時」？ | ChatGPT 和 Claude.ai 已把使用者訓練成預期漸進渲染；blocking 回應讀起來像壞掉或慢 |
