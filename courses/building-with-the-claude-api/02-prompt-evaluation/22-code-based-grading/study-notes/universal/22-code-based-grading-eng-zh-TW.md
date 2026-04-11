# 程式碼評分 Code-Based Grading — 工程深入

| 項目 | 說明 |
|------|------|
| 考試領域 | D3 — Evaluation（20%）主要；D5 — Enterprise Deployment（20%）次要 |
| 任務聲明 | 3.4（deterministic 評分）、3.3（test runner 整合）、5.4（綜合 eval 指標） |
| 來源 | building-with-the-claude-api / 02-prompt-evaluation / Lesson 22 |

---

## 一句話重點

Code-based grading 把 model 輸出丟進 deterministic parser —— JSON、Python AST、regex —— 每個 test case 回傳 10 或 0，給你一個便宜可靠的 eval 品質底線，與較模糊的 model grader 互補。

---

## 為什麼需要 Code Grader

評估會產生程式碼的 AI model 時，「答案看起來對嗎？」還不夠。你需要驗證產出的程式碼**有合法 syntax 且符合正確格式**。用 model grader 做這件事又慢又貴 —— 而且這問題根本不需要判斷，需要的是 parser。

Code grading 驗證 AI 回應的兩個面向：

| 面向 | 檢查 |
|------|------|
| **Format** | 回應只能回傳指定的 code 類型（Python、JSON 或 Regex），不可有解釋 |
| **Valid Syntax** | 產出的程式碼必須能被正確 parse |
| **Task Following** | （由 model grader 處理 —— 不是 code grader） |

這個分工是故意的：便宜/deterministic 的東西交給 code grader，主觀的東西交給 model grader。兩者合起來提供完整評估。

---

## 三個 Validator

來源的三個 syntax validator 都走同一模式 —— 嘗試 parse、成功回 10、失敗回 0：

```python
def validate_json(text):
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
        return 0

def validate_python(text):
    try:
        ast.parse(text.strip())
        return 10
    except SyntaxError:
        return 0

def validate_regex(text):
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0
```

三個工程要點：

1. **先 `.strip()`** —— 不然前後空白會讓合法 payload 被誤判為 false negative。
2. **binary 10 或 0 的輸出** —— 讓分數尺度與 model grader 一致，後面才能平均。
3. **catch 特定 exception** —— `json.JSONDecodeError`、`SyntaxError`、`re.error`。裸 `except:` 會遮蔽 grader 本身的 bug。

三個 validator 都用標準函式庫 —— 沒有外部依賴、沒有 API 成本、延遲以微秒計。

---

## Dataset 格式要求

為了讓 code grader 知道**該跑哪個** validator，每個 test case 必須宣告它期待的格式：

```python
{
    "task": "Create a Python function to validate an AWS IAM username",
    "format": "python"
}
```

來源建議更新你的 dataset 生成 prompt，讓它自動把這個 `format` 欄位加進範例輸出結構，這樣新 test case 永遠帶有 routing 所需的提示。

---

## 改善 Prompt 清晰度

Code grader 也反過來逼你把底層 prompt engineering 寫得更嚴謹。為了提升通過率，來源建議在 prompt 層面做兩件事：

```
* Respond only with Python, JSON, or a plain Regex
* Do not add any comments or commentary or explanation
```

還有一個聰明的 pre-fill 技巧 —— 用不指定語言的通用 code fence 作為 assistant 訊息開頭：

```python
add_assistant_message(messages, "```code")
```

這告訴 Claude 直接開始吐 code content，runner 不必事先知道輸出是 Python、JSON 還是 Regex。後面要呼叫哪個 validator 靠 test case 的 `format` 欄位決定，不是靠這個 fence。

---

## 合併 Model + Code 分數

最後一步是把 model grader 分數和 code grader 分數合起來。來源的簡單預設是非加權平均：

```python
model_grade = grade_by_model(test_case, output)
model_score = model_grade["score"]
syntax_score = grade_syntax(output, test_case)

score = (model_score + syntax_score) / 2
```

這給內容品質（model grader）和技術正確性（code grader）同等權重。來源也直說：依產品需求不同可調整權重 —— 例如 code-generation 產品，syntax 正確性可能占 70% 權重。

---

## Code Grader 的真正價值

來源收尾給出最關鍵的定位：分數本身無所謂好壞 —— **重要的是你能不能靠調整 prompt 讓它提升**。Code grader 給你量化的方式衡量 prompt engineering 進展，不再靠主觀感覺。它們是 prompt 迭代的量化骨幹。

兩個實務屬性要內化：

- **Deterministic** —— 同一輸入永遠得到同一分數。沒有 model grader 那種隨機性。
- **便宜** —— 微秒延遲、無 API 成本。每次改 prompt 都能跑全 dataset。

合起來就代表 code grader 是任何 eval pipeline 的第一道防線。code grader 沒過？連呼叫 model grader 都不用浪費。

---

## 常見錯誤

1. **只用 model grader 驗 syntax** —— 浪費 token，還給一個本該 deterministic 的問題引入 variance。
2. **沒呼叫 `.strip()`** —— 前後有空白的合法 payload 會 fail，false negative 污染指標。
3. **test case 缺 `format` 欄位** —— runner 無法 route 到正確的 validator。
4. **catch 裸 `Exception`** —— 遮蔽 grader 程式碼本身的 bug；一律 catch 特定 parser exception。
5. **沒跟 model grader 平均** —— 程式碼正確性必要但不充分，還需要內容品質。
6. **一組權重用到底** —— 不同產品看重 syntax vs 品質的比例不同；權重要調。

> **關鍵洞察**
>
> Code graders 是 prompt evaluation 的便宜、deterministic 骨幹。它們不能評「味道」，但能用微秒的時間免費抓出每一個壞 payload。搭 model grader（評味道）取平均 —— 你就擁有一個可以在每次 prompt 改動上跑、而不會燒錢的綜合指標。

---

## CCA 考試相關性

- **D3（Evaluation）**：Code graders 是混合 eval pipeline 的 deterministic 那一半。會考何時用 code vs model grader、以及如何合併分數。
- **D5（Enterprise Deployment）**：Deterministic 評分適合塞進 prompt 的 CI/CD —— 便宜、快、夠可靠，每個 PR 都能跑。
- 注意：「你要驗證 AI 產生的 JSON / Python / Regex」→ 永遠是 code grader，絕對不是 model grader。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Code grading 驗證哪兩個面向？ | Format（只能回指定 code 類型）和 Valid Syntax（能實際 parse）。 |
| 成功的 `validate_json` 回傳什麼分數？ | 10 |
| 失敗的 `validate_python` 回傳什麼分數？ | 0 |
| 哪個 Python 模組用來 parse Python code？ | `ast` —— 具體是 `ast.parse(text.strip())`。 |
| `validate_regex` 捕捉哪個 exception？ | `re.error` |
| Dataset 必須帶哪個欄位讓 runner 知道用哪個 validator？ | `format` —— 值像 `"python"`、`"json"`、`"regex"`。 |
| 哪個 assistant prefill 技巧能鼓勵輸出純 code 又不指定語言？ | `` add_assistant_message(messages, "```code") `` |
| 來源如何合併 model grader 和 code grader 分數？ | 非加權平均：`(model_score + syntax_score) / 2`。 |
| 為什麼絕對 code-grader 分數無所謂好壞？ | 因為重要的是能不能靠 prompt 調整讓它提升 —— 看方向不看絕對值。 |
| Code grader 相對 model grader 的兩大優勢？ | Deterministic（同輸入同分數）和極便宜（微秒、無 API 成本）。 |
