# Being Specific — PM 視角

| 項目 | 內容 |
|------|------|
| 考試領域 | D3 — Evaluation & Iteration (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 3.1（prompt 設計與迭代）、1.1（指令遵循） |
| 來源 | building-with-the-claude-api / 03-prompt-engineering / Lesson 27 |

---

## 一句話總結

Specificity 就是一份 acceptance criteria——一條條告訴 Claude 「done」長什麼樣，把模糊要求變成可測試的合約。

---

## PM 為什麼該在乎

每個 PM 都寫過模糊的 ticket、然後看著它被做錯——不是工程師爛，是「done」沒定義。Prompt 的失敗方式一樣。沒有 specificity 的 prompt 就像沒有 acceptance criteria 的 feature ticket——你會拿到「某個東西」，但你無法預測是什麼，也無法證明它是對的。

課程量到的影響非常明顯：在 clear+direct prompt 上加一份 specificity 列表，eval 分數從 **3.92 跳到 7.86**——一次編輯讓品質翻倍有餘。這是整章 prompt engineering 裡最大的單點品質跳升。對 PM 來說，這是最高 ROI 的槓桿。

---

## 心智模型：Acceptance Criteria

| PM 產物 | Prompt 對應 |
|---------|-------------|
| User story | 第一行 clear+direct |
| Acceptance criteria | Output quality guidelines |
| Test plan / checklist | Eval rubric（`extra_criteria`） |
| Process doc / SOP | Process steps |

當你讀課程的餐單 guidelines（「包含準確的每日卡路里、蛋白質/脂肪/碳水量、指定用餐時間……」），你讀的就是一個 AI 功能的 acceptance criteria。每一條都可測，每一條都關掉一個模糊來源。

---

## 兩個槓桿

### Output Quality Guidelines — 「做什麼」

告訴 Claude 完成的 artifact 必須含什麼：

- 長度
- 結構和 format
- 具體元素或屬性
- Tone 或 style

課程建議**幾乎每個 prompt 都要用**。這是一致性的 safety net。

### Process Steps — 「怎麼做」

告訴 Claude 答前該怎麼想：

1. 腦力激盪選項
2. 選最好的
3. 勾勒細節
4. 考慮支援因素

當任務複雜到 Claude 可能只 fix 在一個角度，而你希望它考慮多個角度時使用。課程的經典範例是「分析為什麼業務團隊業績下滑」——跳到單一原因會給出膚淺答案的任務。

---

## 產品應用場景

### 一定要加 Output Guidelines

| 功能 | Guidelines 範例 |
|------|----------------|
| 會議摘要器 | 「包含與會者、決議、action item 和負責人、下次會議時間，200 字內。」 |
| Support ticket 分類器 | 「只回：category（billing/bug/feature/other 擇一）、priority（P0-P3）、一句話摘要。」 |
| 週報產生器 | 「包含 2 句 intro、3 則精選故事、一個數據表、一個 CTA 連結。上限 400 字。」 |

### 多角度分析時加 Process Steps

| 功能 | Process Steps 範例 |
|------|-------------------|
| Root-cause 分析助理 | 「1) 列可能原因 2) 依可能性排序 3) 指出每個要驗證的資料 4) 提出前 2 個假設」 |
| Design critique 工具 | 「1) 辨識主要用戶目標 2) 對照評估 3) 記優點 4) 記缺點 5) 提一個改進」 |
| Sales ops 的 deal review | 「1) 檢查 pipeline stage 2) 看近期活動 3) 標風險訊號 4) 推薦下一步」 |

### 不要過度工程

簡單抽取或格式化（「抽簽名檔裡的 email」）不需要 process steps。加了只是增加延遲、沒有品質收穫。

---

## PM 決策框架

設計 AI 功能的 prompt 時問：

| 問題 | 動作 |
|------|------|
| 我能列出 output 必含的明確元素嗎？ | 寫 output guidelines 編號列表 |
| 有「正確答案」是需要考慮多因素的嗎？ | 加 process steps |
| Claude 有可能忽略某個重要角度嗎？ | 為那個角度加一個 process step |
| Eval rubric 能獨立評分每個 guideline 嗎？ | 能——保持 guidelines 和 rubric 對齊 |
| 所有 guidelines 都可測嗎？ | 把模糊的換成可量測的 |

如果 PM 寫不出一個功能的 acceptance criteria，prompt 就會失敗。列 output guidelines 的練習常常會揭露 PRD 的漏洞。

---

## 複利效應

Specificity 有兩層回報：

1. **直接** — eval 分數上升，因為 output 更貼近你要的。
2. **間接** — 因為每個 bullet 可測，你的 eval rubric 可以更緊，未來迭代改進更快。

這和強 PRD 的複利一樣：清楚的 acceptance criteria 讓 QA 更快、bug 更具體、regression 更容易預防。Prompt 也受益於同樣的紀律。

---

## 常見 PM 錯誤

1. **模糊品質 bullet** — 「should be professional」不是 guideline，「avoid contractions, use third-person voice, max 300 words」才是。
2. **以為 clear+direct「有用」就跳過 specificity** — 3.92/10 不是可發版的品質。Specificity 才是把你推到 7.86+ 的槓桿。
3. **混淆 process steps 和 output structure** — process steps 控制*Claude 怎麼想*，不是*答案怎麼格式化*。是分開的槓桿。
4. **把所有東西塞進一條 bullet** — 每個 guideline 該可獨立測試。過載 bullet 要拆。
5. **Guidelines 和 eval rubric 不對齊** — prompt 要 X、rubric 評 Y，你永遠無法可靠地發改進版本。

> **Key Insight**
>
> Specificity 是 prompt engineering 從「選字遊戲」變成 **產品規格寫作** 的分水嶺。Output guidelines 是 acceptance criteria，process steps 是 SOP，合起來把 prompt 從請求變成合約。課程的 3.92 → 7.86 跳升是整章最強的證據：這是 PM 在 AI 功能上能做的最高 ROI 動作。

---

## CCA 考試相關性

- **D3 (Evaluation & Iteration)**：要認得 specificity 是 clarity/directness 之後最高槓桿的技巧，並區分 output guidelines 和 process steps。
- **D1 (Agentic Architecture)**：agent system prompt 同樣用這兩個槓桿控制 agent 產什麼、怎麼想。
- 考題可能描述一個缺其中一個槓桿的 prompt，要你補。線索：「格式不一致」→ output guidelines；「跳到結論」→ process steps。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Specificity output guidelines 最直接對應哪個 PM 產物？ | Acceptance criteria——一份可測的 bullet list 描述「done」長什麼樣。 |
| 課程量到 specificity 帶來的分數變化？ | 3.92 → 7.86，加 output guidelines 讓 eval 分數翻倍有餘。 |
| PM 什麼時候該用 process steps 而不只是 output guidelines？ | 任務需要多角度考量時，如 root-cause 分析或決策——Claude 可能會 fix 在單一原因。 |
| 好的 output guideline 的檢驗？ | 每個 bullet 都能被 eval rubric 獨立測試；「be professional」這類模糊 bullet 過不了關。 |
| Output guidelines 該出現在幾乎每個 prompt 嗎？ | 是——課程稱它為一致性的「safety net」，該是預設而不是最佳化。 |
| Deal-review 功能的 process step 序列範例？ | 1) 檢查 pipeline stage 2) 看近期活動 3) 標風險訊號 4) 推薦下一步。 |
| Guidelines 和 eval rubric 不對齊會怎樣？ | 分數無法反映 prompt 在最佳化什麼，迭代無法轉換成可發版的改進。 |
| Specificity 的兩層複利？ | 直接（output 更貼近 spec、分數上升）和間接（更緊的 rubric 讓未來迭代更快）。 |
