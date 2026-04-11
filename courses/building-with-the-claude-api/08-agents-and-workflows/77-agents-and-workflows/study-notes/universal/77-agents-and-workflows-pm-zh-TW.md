# Agents 與 Workflows — PM 觀點

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture(22%)— 主要 |
| 任務陳述 | 1.1(agent 與 workflow 定義)、1.2(agentic 模式)、5.2(production workflow 部署)|
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 77 |

---

## 一句話總結

身為 PM,你在 AI 功能架構上最關鍵的一次決定就是 **workflow vs agent** — workflow 給你可預測、能上線的功能;agent 解鎖開放式能力,但代價是測試成本、成本變動、以及 eval 複雜度。

---

## 心智模型:生產線 vs 偵探

| | 生產線(Workflow)| 偵探(Agent)|
|---|--------------------------|-------------------|
| **招聘需求** | 「每一件都做 A → B → C」| 「破案吧。這是你的工具:警徽、手機、車。」|
| **可預測性** | 每件產出都一樣 | 每個案件都不同 |
| **失敗形態** | 輸送帶壞掉(修你的程式碼)| 判斷失誤(重新訓練偵探)|
| **錄用標準** | 你畫得出流程圖 | 你信任偵探的推理 |
| **成本** | 每件可預測 | 每案差異巨大 |
| **規模化** | 加更多生產線 | 招更好的偵探 |

大部分 production AI 產品是生產線(workflow),偶爾加幾個偵探站(agent)處理生產線搞不定的案件。Anthropic 的建議:**先從生產線開始**。

---

## 產品場景

### 適合 Workflow 的情境

| 場景 | 為什麼 Workflow |
|------|---------------|
| PDF 發票 → 結構化資料 | 固定的輸入與輸出,已知的欄位 |
| 客服票券 → 草稿回覆 | 預先定義步驟:分類 → 檢索 → 草稿 → 審閱 |
| 零件圖片 → 3D CAD 檔 | 循序的確定性 pipeline(課程範例)|
| 保留格式翻譯文件 | 已知的轉換,每步都可測 |
| SaaS metric 每日報表 | 可重複的排程,固定資料源 |

### 適合 Agent 的情境

| 場景 | 為什麼 Agent |
|------|-------------|
| 能讀寫檔案的 coding assistant | 無法預測使用者需要哪些檔案 |
| 瀏覽並引用來源的 research helper | 搜尋路徑依找到的東西而定 |
| DevOps 事件回應 | 下一步依即時系統狀態而定 |
| 自訂資料分析 chatbot | 使用者問開放式問題 |

### 兩者都不用(單次 Claude 呼叫就夠)

- 任務一個 prompt 就裝得下
- 不需要 tool use
- 輸出短且終結

不是什麼任務都需要 orchestration。把單次任務過度工程化成 workflow 是 PM 常見錯誤。

---

## PM 決策框架

*依序*問這些問題:

1. **你畫得出流程圖嗎?** 可以 → workflow。
2. **你有端到端的 eval 嗎?** 沒有 → workflow(沒有 eval 不能上 agent)。
3. **財務能接受每次請求成本浮動嗎?** 不能 → workflow(agent 會迴圈)。
4. **Ops 能 debug 長度變動的 trace 嗎?** 不能 → workflow(trace 很快變亂)。
5. **只有走到這一步?** 你可能真的有 agent 用例。時程抓 workflow 的 2-3 倍。

---

## 「就做個 Agent」的四個隱形成本

PM 常常低估 agent 比 workflow 難出貨多少:

1. **Eval 成本** — workflow 可以用小資料集 per-step 測試;agent 需要端到端軌跡涵蓋多樣化輸入。
2. **成本變動** — workflow 每次 run 的 token 帳單可預測;agent 會迴圈、爆衝、爆預算。
3. **可觀測性成本** — workflow 對應乾淨的 span;agent 需要 replayable trajectory,很貴才能蓋出來。
4. **支援成本** — workflow 壞了工程師修程式;agent 判斷失誤時 PM 要決定這是 prompt 問題、tool 問題還是 model 問題。

這些成本在上線*之後*才出現,這就是為什麼 Anthropic 建議從 workflow 開始。

---

## Evaluator-Optimizer 模式(PM 最愛)

課程的 CAD 範例介紹了 **evaluator-optimizer** 模式: producer 產出,grader 評估,feedback loop 重複直到 grader 接受。

從 PM 角度看,這個模式給你:

- **功能內建品管** — grader 就是你的自動 QA
- **有界限的迭代** — 你設上限,成本可預測
- **自我修正但不交出控制權** — 仍然是 workflow

適用於「草稿」可接受輸入,但需要「可發佈版本」輸出的功能:自動生成行銷文案、自動修圖、自動寫 SQL。

---

## PM 常見錯誤

1. **把多步 prompt chain 叫做「我們的 agent」。** 那是 workflow。用錯詞會讓 stakeholder 和投資人期待失準。
2. **沒 eval 就上 agent。** Agent 可靠度取決於你建的 eval。沒 eval = 不能上。
3. **Agent 功能承諾固定費率。** 沒有 guardrail 時,一個爛 query 可以花 50 倍平均成本。要嘛分 tier,要嘛強制步驟上限。
4. **以為「agent」就是「聰明」。** Agent 是*自主*,不見得*更有能力*。設計良好的 workflow 常常勝過天真的 agent。
5. **沒規劃 evaluator-optimizer 模式。** 很多產品需求(「草稿要可發佈,不能只是堪用」)被這個模式優雅解決 — 但要明確設計才行。

---

> **關鍵洞察**
>
> Workflow vs agent 的決定,是 PM 在 AI 功能上最大的架構決定。Workflow 給你可預測、可出貨、可控成本 — 但你要事先知道流程。Agent 給你彈性 — 但代價是 eval 工作量、成本變動、debug 難度。Anthropic 自己的建議是:**先做 workflow**,只有在任務真的無法寫成流程圖時才升級成 agent。大部分「我們需要 agent」的對話最後都會變成「其實 workflow 就行」。

---

## CCA 考試關聯

- **D1(22%)主要**: 這是考最多的領域。預期要你分類情境 — 把流程圖捷思背起來。
- **D5(20%)次要**: 這個區別重要的原因是 production — 可觀測性、成本、eval。
- Workflow 的考試訊號字:「predefined steps」、「predetermined series」、「orchestrated」、「pipeline」。
- Agent 的考試訊號字:「given a goal」、「Claude decides」、「autonomous」、「open-ended」。

---

## Flashcards

| 題目 | 答案 |
|------|------|
| PM 判斷 workflow vs agent 的核心問題? | 執行前你畫得出流程圖嗎? |
| 為什麼 Anthropic 建議先從 workflow 開始? | 更便宜、更可預測、更好測、上線更快 |
| Workflow 的生產線類比? | 每一件都是已知步驟,壞掉就修程式碼 |
| Agent 的偵探類比? | 給目標和工具,自己想辦法下一步,失敗在判斷上 |
| 列出 agent 比 workflow 多出的四個隱形成本。 | Eval 成本、成本變動、可觀測性成本、支援成本 |
| Evaluator-optimizer 模式的 PM 定義? | 自動品管 — producer 草稿,grader 審閱,迴圈直到接受 |
| 什麼時候 workflow 和 agent 都不該用? | 任務單一 prompt 就能完成且不需 tool use 時 |
| PM 處理 agent 最大的錯誤? | 沒有端到端 eval 就上線,且沒設步驟上限 |
