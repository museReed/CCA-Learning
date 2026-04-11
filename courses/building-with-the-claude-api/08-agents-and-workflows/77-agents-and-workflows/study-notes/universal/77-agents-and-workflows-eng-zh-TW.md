# Agents 與 Workflows — 工程深度解析

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture（22%）— 主要 |
| 任務陳述 | 1.1（agent 與 workflow 定義）、1.2（agentic 模式）、5.2（production workflow 部署）|
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 77 |

---

## 一句話總結

**Workflow** 是由*程式碼*透過預先定義的 LLM 呼叫序列來編排；**Agent** 是由 *LLM 自己*編排，給定目標與工具後由 Claude 決定下一步。選擇哪一種，取決於你能不能事先完整描述任務流程。

---

## 最關鍵的區別（考試必考）

此區別出自 Anthropic 的「Building Effective Agents」部落格文章（2024 年 12 月），是 CCA 考試 D1 領域最常被測的觀念。

| 面向 | Workflow | Agent |
|------|----------|-------|
| **Control flow** | 由程式碼事先定義 | 由 LLM 即時決定 |
| **誰在編排** | 你的 Python/TS 程式碼 | Claude（透過 tool use loop）|
| **任務形狀** | 已知、可重複 | 開放式 |
| **步驟數** | 固定序列（或固定分支）| 浮現式 — 依執行期 context 而定 |
| **可預測性** | 高 — 容易測試與追蹤 | 較低 — 需要 evals 與 guardrails |
| **適合時機** | 你畫得出流程圖 | 你無法列舉所有路徑 |

**標準定義（務必背熟）：**

> Workflow 是一系列對 Claude 的呼叫，透過*預先決定*的步驟來解決特定問題。Agent 則是給 Claude 一個目標與一組工具，期望 Claude 自己想辦法用這些工具完成目標。

---

## 決策捷思

問自己一個問題：**「我能不能在執行前就畫出這個解決方案的流程圖?」**

- **可以 → workflow。** 把流程圖寫在程式碼裡，你保有控制權。
- **不行 → agent。** 給 Claude 工具與目標，然後跑 tool use loop。

另一個判斷：如果你的 app UX 把使用者限制在一組已知的任務（上傳圖片 → 產出 STEP 檔），幾乎一定是 workflow。如果使用者輸入自由格式請求（coding assistant、research helper），幾乎一定是 agent。

---

## 實例：Image to CAD Workflow

課程示範一個 web app：使用者拖曳金屬零件照片，系統產出 STEP 檔（3D CAD 格式）：

```python
def image_to_cad_workflow(image_bytes: bytes) -> bytes:
    # Step 1: 描述物件
    description = claude_describe_image(image_bytes)

    # Step 2: 根據描述產生 CadQuery 程式碼
    cad_code = claude_write_cadquery(description)

    # Step 3: 執行 CadQuery 產生 rendering
    rendering = run_cadquery(cad_code)

    # Step 4: Grader 迴圈（evaluator-optimizer）
    for attempt in range(MAX_ATTEMPTS):
        grade = claude_grade(image_bytes, rendering)
        if grade.accepted:
            return export_step(cad_code)
        cad_code = claude_fix(cad_code, grade.feedback)
        rendering = run_cadquery(cad_code)

    raise RuntimeError("Grader 始終不接受輸出")
```

程式碼掌握 control flow,Claude 在每次迭代被當成*函式*呼叫四次。這就是 workflow 的特徵。

---

## Evaluator-Optimizer 模式

上面的 CAD 範例是 Anthropic 部落格中 **Evaluator-Optimizer** 模式的實例:

- **Producer** — 拿 input 產出 output(CadQuery 建模器)
- **Grader / Evaluator** — 依照準則替 output 打分
- **Feedback loop** — 如果沒過,把 feedback 回傳給 producer
- **Iteration** — 重複直到接受或達到最大次數

這個模式讓你取得「自我修正」行為,卻*不需要*把控制權交給 Claude。程式碼決定何時停、何時重試、最多試幾次 — 這些都是 production 系統的關鍵屬性。

Anthropic 部落格中其他 workflow 模式:

| 模式 | 核心概念 | 課程 Lesson |
|------|---------|------------|
| Prompt chaining | 循序 LLM 呼叫,前一步 output 餵下一步 | Lesson 79 |
| Parallelization | 把任務拆成平行子任務並匯總 | Lesson 78 |
| Routing | 分類器挑選專門處理器 | Lesson 80 |
| Orchestrator-workers | 中央 LLM 委派給 worker LLM | 後續 Lesson |
| Evaluator-optimizer | Producer + grader feedback loop | Lesson 77 |

---

## 為什麼這個區別在 production 很重要

Workflow vs agent 的選擇直接影響:

1. **可觀測性** — workflow 每一步都好記錄(每個節點一個 span);agent trace 長度變動,跨 run 比較困難。
2. **成本控制** — workflow 步驟數已知;agent 可能意外迴圈(budget 爆掉是真實的 production 失敗模式)。
3. **Eval 策略** — workflow 可以 per-step 評估;agent 需要端到端 eval,涵蓋多樣化軌跡。
4. **失敗模式** — workflow 失敗在*你的程式碼*;agent 失敗在 *Claude 的決策*,需要重新設計 prompt 與 tool set。
5. **上線速度** — workflow 較快能出貨;agent 通常要反覆調整工具組與 system prompt。

---

## 常見錯誤

1. **該用 workflow 卻用 agent。** 如果你畫得出流程圖,workflow 更便宜、更可靠、更好除錯。Anthropic 明確建議先從 workflow 開始。
2. **把什麼都叫「agent」。** 多步驟 prompt chain 但執行期沒有 LLM control flow 的,是 workflow 不是 agent。考試對精確度有要求。
3. **忘了 evaluator-optimizer loop 要有最大次數上限。** 否則一個爛的 grader 可以跑到地老天荒,把預算燒光。
4. **誤以為 workflow 不能用 tool。** Workflow 絕對可以呼叫 tool,區別在於*誰決定順序*,而不是有沒有 tool。
5. **把 workflow pattern 當成理論。** 你還是得自己寫 code,pattern 是 recipe 不是 framework。

---

> **關鍵洞察**
>
> Workflow 和 agent 的差異在於**誰掌握 control flow**。Workflow 由你的程式碼掌握,agent 由 Claude 掌握。其他一切 — 可觀測性、成本、eval 策略、失敗模式 — 都由這一個問題延伸而來。CCA 考試常常用間接方式問這個觀念(「預先決定的步驟」= workflow,「Claude 決定下一步」= agent)— 訓練自己抓出訊號字。

---

## CCA 考試關聯

- **D1(22%)主要**: Lesson 77 是最常被考的領域的基礎章節。至少會有一題要你分類某情境是 agent 還是 workflow。
- **D5(20%)次要**: production 部署考量(可觀測性、成本、eval 策略)都跟這個選擇綁在一起。
- 指向 **workflow** 的訊號字: 「predetermined series」、「fixed steps」、「orchestrated by code」、「pipeline」。
- 指向 **agent** 的訊號字: 「given a goal and tools」、「Claude decides」、「autonomous」、「open-ended task」。

---

## Flashcards

| 題目 | 答案 |
|------|------|
| Workflow 與 agent 的核心差別? | 誰掌握 control flow — workflow 是程式碼,agent 是 Claude |
| 寫出 workflow 的標準定義。 | 透過預先決定的步驟序列對 Claude 呼叫以解決特定問題的一系列呼叫 |
| 寫出 agent 的標準定義。 | 給 Claude 目標與工具,讓 Claude 自己想辦法完成目標 |
| 判斷 workflow vs agent 的捷思? | 執行前能不能畫出流程圖? 能 → workflow,不能 → agent |
| Evaluator-optimizer 模式是什麼? | Producer 產出結果,grader 評分,不過就回饋重做直到接受 |
| 列出 Anthropic「Building Effective Agents」中 4 個 workflow 模式。 | Prompt chaining、parallelization、routing、evaluator-optimizer(還有 orchestrator-workers) |
| 為什麼 Anthropic 建議先用 workflow? | 比 agent 更便宜、更可觀測、更好測、上線更快 |
| Agent 獨有的 production 風險? | 步驟數無上限 / budget 爆掉 — 沒有 guardrail 時會無限迴圈 |
