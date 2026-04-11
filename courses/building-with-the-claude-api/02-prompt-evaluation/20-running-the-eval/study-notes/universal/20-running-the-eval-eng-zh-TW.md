# Running the Eval — Engineering Deep Dive（繁體中文）

| 項目 | 內容 |
|------|------|
| Exam Domain | D3 — Evaluation & Iteration（20%，主要）；D5 — Enterprise Deployment（20%，次要） |
| Task Statements | 3.3（eval 執行）、3.1（eval 設計）、3.2（測試資料集） |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 20 |

---

## 一句話摘要

核心 eval pipeline 由三個小函式構成 — `run_prompt`、`run_test_case`、`run_eval` — 拿一份資料集，把每一筆推進 Claude，吐出一份可以交給 grader 的結構化結果清單。

---

## 三函式架構

課程把 eval runner 組成三個責任分離明確的可組合函式：

```
┌─────────────────────┐
│     run_eval        │  ← 載入資料集、走每一筆
│  (dataset)          │
└──────────┬──────────┘
           │ 對每個 test_case
           ▼
┌─────────────────────┐
│   run_test_case     │  ← 串接 prompt + grader
│  (test_case)        │
└──────────┬──────────┘
           │ 呼叫
           ▼
┌─────────────────────┐
│    run_prompt       │  ← 把 template 和輸入合併、呼叫 Claude
│  (test_case)        │
└─────────────────────┘
```

每個函式只做一件事。這是刻意的 — 當 eval 變複雜（平行執行、重試、model-based grading），你一次只改一個函式，不用重寫整條 pipeline。

---

## 函式 1：`run_prompt`

最底層的函式處理單次 prompt 執行：

```python
def run_prompt(test_case):
    """Merges the prompt and test case input, then returns the result"""
    prompt = f"""
Please solve the following task:

{test_case["task"]}
"""

    messages = []
    add_user_message(messages, prompt)
    output = chat(messages)
    return output
```

注意此時 prompt 的狀態 — 刻意極簡。沒有格式指令、沒有輸出約束。課程說：*「現在我們讓 prompt 極其簡單。沒有包含任何格式指令，所以 Claude 很可能回出比我們需要的更冗長的輸出。我們會在後面迭代 prompt 設計時改善這點。」*

那個冗長輸出的 baseline 正是重點 — 它就是你後面加結構時要量測的對照組。

---

## 函式 2：`run_test_case`

中間層負責跑一筆測試案例並評分：

```python
def run_test_case(test_case):
    """Calls run_prompt, then grades the result"""
    output = run_prompt(test_case)

    # TODO - Grading
    score = 10

    return {
        "output": output,
        "test_case": test_case,
        "score": score
    }
```

兩個重要觀察點：

1. **Score 寫死為 10。** 這是刻意的 placeholder。真正的 grading 邏輯在 Lesson 21（model-based）和 22（code-based）。寫死 10 讓 pipeline 在 grader 還沒準備好之前就能端對端跑 — 這是經典的「walking skeleton」技巧。
2. **回傳結構是個緊湊合約。** 每筆結果都帶 `output`、`test_case`、`score`。下游消費者（報表產生、regression 偵測、dashboards）都依賴這個形狀。

---

## 函式 3：`run_eval`

最上層驅動整個迴圈：

```python
def run_eval(dataset):
    """Loads the dataset and calls run_test_case with each case"""
    results = []

    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    return results
```

刻意寫得很瑣碎。就是迴圈、呼叫 `run_test_case`、收集結果。後面章節會把它升級成平行執行，但這個同步版已經足以示範模式。

---

## 驅動整條 Pipeline

載入並跑完整 eval 就是五行 script：

```python
with open("dataset.json", "r") as f:
    dataset = json.load(f)

results = run_eval(dataset)
```

Lesson 19 存下來的資料集被 `json.load` 讀進來，交給 `run_eval`，回來的是一串 result dict。

**時間注記：** 課程提醒即使用 Haiku，第一次跑完整資料集大概要 30 秒。Production 規模（幾百到幾千筆）下這會成為第一個瓶頸，這就是為什麼要引入平行化。

---

## 結果結構

每個 result dict 有三個 key：

| Key | 內容 | 用途 |
|-----|------|------|
| `output` | Claude 的完整文字回應 | 你要評分的對象 |
| `test_case` | 原始測試案例（`task` dict） | Grader 和報表的脈絡 |
| `score` | 數值分數（目前寫死 10） | 品質指標 |

檢查結果：

```python
print(json.dumps(results, indent=2))
```

課程說輸出「相當冗長」，因為 prompt 沒有格式指令 — 這就是整章後半要改進的 baseline 條件。

---

## 你蓋了什麼 vs. 還缺什麼

課程講得很明白：*「你剛剛蓋好的幾乎就是 eval pipeline 實際會做的大部分事情。」* 骨架可以跑 — 資料集進、結果出。剩下的是三層深化：

| 面向 | 目前狀態 | 後續課程 |
|------|----------|----------|
| Grading | 寫死 10 | Lesson 21（model-based）與 22（code-based） |
| Prompt 品質 | 冗長 baseline | 依 eval 分數迭代 |
| 效能 | 序列、~30 秒 | 平行 batching |

關鍵 insight 是：*pipeline* 本身很簡單 — 複雜度在每一階段的細節裡，不在階段間的連接方式。

---

## 為什麼這個最小 pipeline 是正確起點

「Walking skeleton」有三個完整版 runner 沒有的特性：

1. **端對端證明** — 你可以在任何 grader 實作前就展示整個迴圈能跑，早期抓到整合 bug。
2. **隔離升級** — 你可以把寫死 grader 換成真的，而不碰到 `run_prompt` 或 `run_eval`。
3. **穩定合約** — 下游工具（dashboards、regression CI、報表）從第一天起就能依賴結果結構。

這正是 production AI 系統想要的模式：先上最簡 pipeline，隨著產品成熟再一個一個函式替換成精緻版。

---

## 常見錯誤

1. **跳過 walking skeleton** — 想一次蓋完 grader、平行、dashboard，會陷入 debugging 地獄。
2. **把 grading 混進 `run_prompt`** — 責任分離才讓你能獨立升級 grader。
3. **沒把 `results` 存檔** — Production 裡你會想把結果存檔，方便跨跑比對 diff。
4. **Production 規模下還用同步迴圈** — 3 筆沒問題，3,000 筆致命；早點規劃 `asyncio` 或 thread pool。
5. **忘了修掉 grader placeholder** — 把 `score = 10` 上 CI 會讓 eval 失去意義；這只是教學用。

---

> **Key Insight**
>
> 三函式架構的力量不在於複雜，而在於責任分離。`run_prompt` 管 Claude 呼叫、`run_test_case` 管評分、`run_eval` 管迭代。每個函式都能獨立替換，這正是從 notebook demo 邁向 production eval pipeline 所需要的性質。CCA 考試會測結構化結果形狀（`output` / `test_case` / `score`）這個 D3 task 3.3 的細節。

---

## CCA 考試相關性

- **D3（Evaluation & Iteration）**：知道三函式分解和固定的結果形狀；理解寫死 grader 是跳板不是終點。
- **D5（Enterprise Deployment）**：這個 pipeline 就是每一個 production prompt eval 的運作基底；要認知到 walking-skeleton 模式可以透過逐一替換函式的方式擴展到真實系統。
- 考題觸發詞：任何問「你實際怎麼對資料集跑 eval」都指向 `run_eval → run_test_case → run_prompt` 的分層。

---

## Flashcards

| Front | Back |
|-------|------|
| Eval runner 的三個函式由外到內是什麼？ | `run_eval`（走資料集）→ `run_test_case`（串 prompt 和 grader）→ `run_prompt`（呼叫 Claude）。 |
| `run_prompt` 做什麼？ | 把 prompt template 跟測試案例的 `task` 輸入合併，用 `chat()` 送進 Claude，回傳輸出文字。 |
| `run_test_case` 回傳什麼？ | 一個三鍵 dict：`output`（Claude 回應）、`test_case`（原始輸入）、`score`（數值分數，目前寫死 10）。 |
| 為什麼這課的 grading score 寫死 10？ | 為了在真正的 grader（lesson 21-22）實作前讓 walking-skeleton pipeline 能跑。 |
| 執行時如何載入資料集？ | `with open("dataset.json", "r") as f: dataset = json.load(f)` — 就是 Lesson 19 產的檔案。 |
| 用 Haiku 第一次跑 eval 大概多久？ | 課程說完整（小）資料集大約 30 秒。 |
| 為什麼 baseline prompt 產出冗長回應？ | 因為沒有格式指令 — 這是刻意的，讓後續 prompt 迭代能示範可量測的改善。 |
| 本課示範的「walking skeleton」模式是什麼？ | 先用 placeholder 把整條 pipeline 搭起來，再把每個函式換成 production 版，但合約不變。 |
