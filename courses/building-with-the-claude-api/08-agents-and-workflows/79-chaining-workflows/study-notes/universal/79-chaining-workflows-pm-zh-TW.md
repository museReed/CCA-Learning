# Chaining Workflows — PM 觀點

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture(22%)— 主要 |
| 任務陳述 | 1.2(agentic 模式 — chaining)、5.2(production workflow 部署)|
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 79 |

---

## 一句話總結

Chaining 是「一次只做一件事」的 workflow:只要 Claude 在單一 prompt 裡無法同時滿足多個限制,或任務有天然的循序階段,就把它拆成聚焦的步驟,輸出從一步流到下一步。

---

## 心智模型:編輯部

一篇雜誌文章不是一個人一次全做完:

| 角色 | 工作 | Chaining 對應 |
|------|------|--------------|
| **記者** | 蒐集素材 | 步驟 1:研究 LLM 呼叫 |
| **寫手** | 把素材寫成稿 | 步驟 2:撰稿 LLM 呼叫 |
| **文字編輯** | 執行家規、去除陳腔濫調 | 步驟 3:修訂 LLM 呼叫 |
| **事實查核** | 驗證 claim | 步驟 4:驗證(可以非 LLM)|
| **出版** | 發布成品 | 步驟 5:發布 API 呼叫 |

每個角色專注在自己最擅長的事,工作從一個桌子流到下一個。Chaining workflow 就是把同樣想法套在 Claude 上:與其讓一個 prompt 爛爛地演五個角色,不如讓五個聚焦呼叫各演好一個。

---

## 產品場景

### 適合 Chaining 的情境

| 場景 | 為什麼 Chaining |
|------|---------------|
| 有品牌語氣規則的行銷文案生成 | 步驟 1 草稿、步驟 2 執行語氣、步驟 3 縮短 |
| 語氣校準的自動回覆系統 | 分類意圖 → 草稿回覆 → 語氣修正 → 送出 |
| 保留結構的文件翻譯 | 擷取結構 → 翻譯文字 → 重組 |
| 資料到報表 pipeline | 抓資料 → 摘要 → 格式化 → 加視覺化 |
| 影片內容 pipeline(課程範例)| 熱門主題 → 研究 → 腳本 → 影片 → 發布 |
| 法律合約審查 | 逐章節分析餵給最終建議 |

### 不適合 Chaining 的情境

| 場景 | 更好的選擇 |
|------|-----------|
| 單一簡單任務 | 一次 Claude 呼叫就好 |
| 獨立子分析 | Parallelization(Lesson 78)|
| 開放式探索 | Agent(Lesson 77)|
| 延遲關鍵的即時功能 | 單一呼叫 — chaining 延遲會加總 |

---

## PM 熟悉的「長 Prompt 問題」

這是 chaining 解決的 PM 最常見痛點。你寫 PRD 說「AI 要產出 X、Y、Z,避免 A、B、C」 — 工程建了包含所有規則的大 prompt — 輸出還是不一致地違反規則。

**診斷**:你同時要求 Claude *創作*好內容*又*執行六條限制。把工作拆開:

1. **第一次呼叫** — 只專注創作好內容
2. **第二次呼叫** — 只專注執行限制(「刪掉 X、替換 Y、調整語氣 Z」)

第二次呼叫會成功,因為 Claude 不再是在創造力和合規之間取平衡 — 它只是在編輯。

這個模式適用於任何有「輸出要 X *而且* 避免 Y」需求的功能。

---

## PM 決策框架

問這些問題:

| 問題 | 是 | 行動 |
|------|----|------|
| 任務是否有天然的循序階段? | 是 | Chaining 候選 |
| Claude 在單一 prompt 中忽略某些規則? | 是 | Chaining(拆生成/執行)|
| 後續步驟需要前面步驟的輸出? | 是 | Chaining,不是 parallelization |
| 可以在步驟間驗證輸出? | 是 | Chaining(加品質 gate)|
| 單一 prompt 已可靠運作? | 是 | 不要 chain — 保持簡單 |

---

## 業務價值論述

為 chaining vs 單一大 prompt 提案時,翻成商業語言:

- **品質** — 「每步做好一件事,而不是做幾件都做得差」
- **可靠度** — 「限制由專門的修訂步驟執行,不是碰運氣」
- **可測試性** — 「每步有清楚的 input/output,可以獨立 unit test 與 eval」
- **可觀測性** — 「失敗出現在特定步驟,不藏在巨型 prompt 裡」
- **延遲取捨** — 「總時間是各步時間總和,預算大約是單一 prompt 的 2 倍」

---

## PM 要編進預算的隱形成本

1. **延遲會加總。** Chain 比單一 prompt 慢。如果步驟 1 是 2 秒、步驟 2 是 2 秒、步驟 3 是 2 秒,總共 6 秒。使用者感覺得到。必要時可以 streaming 中間輸出。
2. **Token 成本會加總。** 每一步都付自己的 prompt token + 輸出 token。早點算總成本。
3. **錯誤傳遞。** 步驟 2 輸出爛會讓步驟 3 更爛。要求工程在步驟間加驗證。
4. **Debug 複雜度。** 多步驟失敗需要 trace log — 把可觀測性寫進 spec。
5. **Eval 工作量放大。** 每步要自己的 eval 資料集*再加上*端到端 eval。

---

## PM 常見錯誤

1. **該用單一 prompt 卻 chain。** 過度工程化是真的。從最簡單解法開始,只有在單一 prompt 真的失敗時才 chain。
2. **Chain 太長。** 3-5 步是甜蜜點。10+ 步的 chain 變脆且慢。如果你需要 10+ 步,大概該拆成多個小 chain 加 checkpoint。
3. **漏了非 LLM hook。** Chain 可以在 LLM 呼叫間插入 code — PM 常忘記這點而要求「什麼都 AI」,錯過確定性驗證的機會。
4. **沒為 eval 編預算。** 每個 chain 步驟都需要 eval。Eval 預算常常比初建預算還大。
5. **PRD 沒寫錯誤處理。** 步驟 3 失敗會怎樣? 重試? Fallback? 降級? 整個請求失敗? 事先寫清楚。

---

> **關鍵洞察**
>
> Chaining 是「每個呼叫聚焦一個責任」的模式。產品需要 Claude 平衡多個目標時(創作 + 執行、擷取 + 重組、分類 + 回應),把工作拆成循序、單一目的的 LLM 呼叫。「長 prompt 問題」是這模式解決的 PM 第一大痛點。考試記得:**chaining 有序列依賴,parallelization 沒有。**

---

## CCA 考試關聯

- **D1(22%)主要**: Chaining 是四大 workflow 模式之一,預期有情境題要你區分 chaining、parallelization、routing。
- **D5(20%)次要**: Production 模式 — 錯誤處理、checkpointing、步驟間驗證。
- Chaining 訊號字:「sequential」、「output feeds next step」、「break into steps」、「focus on one aspect」。
- 最清楚的訊號:情境描述「Claude 寫 X,然後我們請 Claude 修訂 X」 — 就是 chaining。

---

## Flashcards

| 題目 | 答案 |
|------|------|
| Chaining 的產品定義? | 把任務拆成循序、聚焦的 LLM 呼叫,每一步輸出餵下一步 |
| Chaining 的編輯部類比? | 記者 → 寫手 → 文字編輯 → 事實查核 → 出版;每個角色聚焦,工作在桌子間流動 |
| Chaining 解決的「長 prompt 問題」是什麼? | Claude 在單一 prompt 同時創作內容與執行規則時會忽略限制 |
| Chaining 和 parallelization 的差別? | Chaining 有序列依賴;parallelization 是並行獨立子任務 |
| PM 什麼時候該避免 chaining? | 單一 prompt 可靠或延遲是首要限制時 |
| 列出三個 chaining 的 PM 錯誤。 | 不必要 chain、chain 太長、PRD 漏錯誤處理 |
| Chaining 功能要編哪些隱形成本? | 延遲總和、token 總和、每步 eval、錯誤處理、debug 複雜度 |
| Chaining 是 workflow 還是 agent? | Workflow — 程式碼掌握順序,Claude 不決定下一步 |
