# Being Specific — 工程深度解析

| 項目 | 內容 |
|------|------|
| 考試領域 | D3 — Evaluation & Iteration (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 3.1（prompt 設計與迭代）、1.1（指令遵循） |
| 來源 | building-with-the-claude-api / 03-prompt-engineering / Lesson 27 |

---

## 一句話總結

Specificity 在收束 Claude 的 search space——output guidelines 鎖定「結果長什麼樣」，process steps 鎖定「Claude 該怎麼想」。

---

## 核心問題：沒有邊界的詮釋空間

Clear and direct 本身還不夠。例如「Write a short story about a character who discovers a hidden talent.」這個 prompt 清楚、直接、是祈使句——但 Claude 還是可以自由選：

- 長度（200 字或 2,000 字）
- 角色數量（一人或五人）
- 類型和場景
- 「hidden talent」是哪個、怎麼揭露

每一個自由軸都是 output 可能在跑多次時漂移的軸。Specificity 就是把這些軸關起來的方法。

---

## 兩種 Specificity

課程點出兩個互補的槓桿。實務 prompt 通常會同時用。

### 1. Output Quality Guidelines

一個列表，列出 output 必須具備的品質。這在控制 artifact 本身：

- **長度**
- **結構**和 format
- **必須包含的具體屬性或元素**
- **Tone** 或 style 要求

以短篇小說為例：「1,000 字以內、包含一個揭露才能的清楚動作、至少一個配角」。每一條都收掉一個自由軸。

### 2. Process Steps

給 Claude 在產出最終答案前要跑的動作序列。這在控制 reasoning path：

1. 腦力激盪三個會製造戲劇張力的才能。
2. 選最有趣的那個。
3. 勾勒出揭露才能的關鍵場景。
4. 腦力激盪能放大衝擊的配角類型。

Process steps 在任務受益於「先多角度思考再下筆」的情境特別有用，而不是一次到底生出答案。

---

## 貫穿範例：餐單 Guidelines

疊加在 Lesson 26 的 clear+direct prompt 上，課程示範的 output guidelines：

```
Guidelines:
1. Include accurate daily calorie amount
2. Show protein, fat, and carb amounts
3. Specify when to eat each meal
4. Use only foods that fit restrictions
5. List all portion sizes in grams
6. Keep budget-friendly if mentioned
```

每一條都可測。每一條都關掉前一版 prompt 沒關的品質自由軸。

---

## 量測結果

課程給了迭代 prompt 的 evaluator 分數：

| 版本 | 分數 (/10) |
|------|-----------|
| Baseline（「What should this person eat?」） | 2.32 |
| Clear and direct（「Generate a one-day meal plan...」） | 3.92 |
| **+ Specificity guidelines** | **7.86** |

加上 specificity **讓分數翻倍**——從 3.92 到 7.86，比 clarity/directness 的進步還大，也是課程把 specificity 列為「幾乎每次都要用」的原因。

---

## 何時用哪一招

| 技巧 | 什麼時候用 |
|------|-----------|
| **Output Quality Guidelines** | 幾乎每個 prompt。這是你保持一致性的安全網。 |
| **Process Steps** | 複雜問題——troubleshooting、決策、critical thinking，或任何你希望 Claude 在答前多角度思考的任務。 |

課程對 process steps 的範例：要 Claude 分析為什麼一個業務團隊業績下滑。沒有 process steps，Claude 可能會 fix 在某一個原因。用 process steps 引導它走過市場指標 → 產業變化 → 個人績效 → 組織變動 → 客戶回饋，分析變得周延而平衡。

---

## 同時用兩招

Professional prompt 通常兩個槓桿一起上：

- **Process steps** 放在上面，告訴 Claude 怎麼想。
- **Output guidelines** 放在下面，告訴 Claude 最終 artifact 必須含什麼。

這個組合同時給你 output 的一致性和 Claude 考慮過所有重要因素的信心。

---

## 為什麼 Specificity 是複利

Guidelines 裡每一條都像是 output 的一個 unit test。Grader（不管是人還是 model-based evaluator）可以獨立檢查每一項，這正是你的 eval `extra_criteria` 打分的方式。Prompt 的 guidelines 越對齊 evaluator 的 rubric，每次 eval 迭代就越能直接轉換成 prompt 改進。

所以資深 prompt engineer 常同時寫 rubric 和 guidelines——它們是同一份合約的兩個視圖。

---

## 常見錯誤

1. **停在 clear + direct** — 留給 Claude 自己猜長度、結構、要含的元素，把 eval 分數上限壓低。
2. **Specify 太少、太模糊** — 「include details」不是 guideline，「list all portion sizes in grams」才是。
3. **在瑣碎任務上用 process steps** — 簡單抽取或格式化用 steps 只是增加延遲、沒有品質收穫。
4. **Prompt guidelines 和 eval rubric 對不上** — prompt 要 X，evaluator 打 Y 的分。要對齊。
5. **Process steps 堆太多** — 超過約 5 步 Claude 可能會 drop 或 merge 步驟。保持 process sequence 聚焦。

> **Key Insight**
>
> Specificity 是課程 playbook 裡單點影響最大的技巧——把 eval 分數從 3.92 翻倍到 7.86。Guidelines 每一條都關掉一個 output 漂移軸，每關掉一個軸 prompt 就可量測地更可靠。Output guidelines 幾乎該出現在每個 prompt；process steps 在任務需要多角度推理時加入。

---

## CCA 考試相關性

- **D3 (Evaluation & Iteration)**：要認得 specificity 是 clarity/directness 之後最高槓桿的技巧，要知道兩個變體（output guidelines vs process steps）。
- **D1 (Agentic Architecture)**：agent system prompt 同樣靠這兩個槓桿——guidelines 約束 output，process steps 約束 reasoning。
- 考題會問「哪種任務該用哪招」。「多角度分析」→ process steps。「一致的 artifact format」→ output guidelines。「兩者都要」→ 組合。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Specificity 兩種 guidelines 是什麼？ | Output quality guidelines（結果該長什麼樣）和 process steps（Claude 該怎麼思考）。 |
| Output quality guidelines 控制什麼？ | 長度、結構、格式、必須包含的屬性/元素、tone 或 style。 |
| 什麼時候用 process steps？ | 複雜問題——troubleshooting、決策、critical thinking，或任何該在答前多角度考量的任務。 |
| 餐單範例中 specificity 帶來的分數進步？ | 3.92 → 7.86，光加具體 guidelines 就讓分數翻倍。 |
| Output guidelines 該每個 prompt 都加嗎？ | 幾乎是——課程把它稱為一致性的「safety net」。 |
| 課程的 process steps 範例序列？ | 1) 腦力激盪三個製造張力的才能 2) 選最有趣 3) 勾勒關鍵場景 4) 腦力激盪配角類型。 |
| Prompt guidelines 和 evaluator rubric 沒對齊會怎樣？ | 分數無法反映 prompt 真正在最佳化什麼——兩者必須保持對齊。 |
| 兩招一起用的 professional pattern？ | Process steps 放上面（怎麼想），output guidelines 放下面（最終 artifact 該含什麼）。 |
