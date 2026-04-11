# Generating Test Datasets — Engineering Deep Dive（繁體中文）

| 項目 | 內容 |
|------|------|
| Exam Domain | D3 — Evaluation & Iteration（20%，主要）；D5 — Enterprise Deployment（20%，次要） |
| Task Statements | 3.2（測試資料集）、3.1（eval 設計）、3.3（eval 執行） |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 19 |

---

## 一句話摘要

你可以在幾分鐘內用 Claude 幫自己產出 eval 資料集 — 用 Haiku 這種較快的模型、JSON prefilling 技巧、配合 stop sequences，一次就能拿到可 parse 的乾淨輸出。

---

## 情境：AWS Code Assistant

課程建構的 eval 系統是給一個幫用戶寫 **AWS 專屬程式碼**的 prompt，輸出格式有三種：

- Python 程式碼
- JSON 設定檔
- 正規表示式（regex）

核心需求：輸出必須**乾淨** — 不能有多餘的解釋、前言、後記。這個「乾淨輸出」需求，正是 eval 資料集要壓力測試的屬性。

起始版（v1）prompt：

```python
prompt = f"""
Please provide a solution to the following task:
{task}
"""
```

---

## 資料集格式：Task 陣列

資料集是一個 JSON 物件陣列，每個物件有一個 `task` 欄位描述要 Claude 完成什麼：

```json
[
  { "task": "Description of task" },
  ...additional
]
```

這種最小結構是刻意的。執行 eval 時你會走過整個陣列，把每個 `task` 內插進 prompt template 後送進 Claude。之後要加欄位（expected output、分類、難度）很容易；從簡單開始更快。

---

## 為什麼用 Haiku 產資料集

課程明確建議用 **Haiku** 而不是完整版 Claude 來產資料集。理由是經濟考量：

- 資料集生成是批次、創意性任務，不需要 frontier-model 的推理能力。
- Haiku 每次呼叫更快、更便宜。
- 一百筆資料集在 Sonnet 上很貴，在 Haiku 上幾乎免費。

這是 CCA 課綱的通用模式：**批次工作用快模型，被評估的任務本身才用 frontier 模型。**

---

## 與 Claude 互動的輔助函式

課程介紹三個會在整章重複使用的輔助函式：

```python
def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, system=None, temperature=1.0, stop_sequences=[]):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature
    }
    if system:
        params["system"] = system
    if stop_sequences:
        params["stop_sequences"] = stop_sequences

    response = client.messages.create(**params)
    return response.content[0].text
```

三個觀察點：

1. **`temperature=1.0` 為預設** — 資料集生成需要高熵產出多樣的測試案例，不是重複的清單。
2. **`stop_sequences` 已預接好** — 這就是讓 prefilling 技巧能乾淨運作的關鍵（下面說明）。
3. **`chat()` 回傳 `.content[0].text`** — 幫呼叫端抽象掉 content-block 結構，直接拿到純文字。

---

## 資料集生成函式

課程主函式：

```python
def generate_dataset():
    prompt = """
Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects, each representing task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
  {
    "task": "Description of task",
  },
  ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
* Focus on tasks that do not require writing much code

Please generate 3 objects.
"""
```

三個值得注意的 prompt engineering 決策：

- **Example output 放在圍籬碼區塊裡** — Claude 得到具體的形狀範本，而不是抽象描述。
- **兩個明確約束** — 「單一 function / object / regex」和「不用寫太多程式碼」。這兩條把生成空間收窄，讓資料集保持聚焦。
- **明確數量** — 「Please generate 3 objects」給出確定的輸出大小。

---

## JSON Prefilling + Stop Sequence 技巧

本課最重要的技術：

```python
messages = []
add_user_message(messages, prompt)
add_assistant_message(messages, "```json")
text = chat(messages, stop_sequences=["```"])
return json.loads(text)
```

這是從 Claude 取得可 parse JSON 的經典模式。運作方式：

1. **加一則 assistant message 內容為 ` ```json `** — 等於告訴 Claude「你已經開始寫一個 JSON code block 了，繼續寫下去」。
2. **設定 `stop_sequences=["```"]`** — Claude 一旦要關閉 code fence 就會立刻停下。
3. **用 `json.loads` 解析原始文字** — 拿回來的就是純 JSON，沒有前言後語，沒有收尾圍籬。

為什麼重要：沒有 prefilling 的話，Claude 常會包一句前言（"Here is your dataset:"）或忘記關圍籬。Prefilling + stop sequences 把「從 Claude 取 JSON」從 regex parsing 問題，變成一行 `json.loads`。

這同時是 **D5 production 模式**，也是 D3 技巧 — 任何你要從 Claude 取結構化輸出但又不想動用 tool use 的場景都可以用。

---

## 執行

```python
dataset = generate_dataset()
print(dataset)
```

這會回出三個涵蓋 Python、JSON config、regex 的 AWS 測試案例。

---

## 持久化資料集

```python
with open('dataset.json', 'w') as f:
    json.dump(dataset, f, indent=2)
```

把資料集存檔很重要，原因有三：

- **可重現性** — 同一份資料集必須在 prompt 迭代間重用（否則比較無效，見 Lesson 18）。
- **版本控制** — 你可以把 `dataset.json` commit 進 repo，每個工程師都對同一個正典輸入集打分。
- **解耦** — 生成和執行變成兩個獨立步驟；生成一次、eval 跑很多次。

檔案就放在 notebook 旁邊，讓 Lesson 20 的 eval runner 用 `open("dataset.json", "r")` 直接讀。

---

## 常見錯誤

1. **用 Sonnet 來產資料集** — 浪費錢；Haiku 才是批次創意工作的正確選擇。
2. **跳過 JSON prefilling 技巧** — parser 會被 Claude 的前言後語弄壞。
3. **忘了 `stop_sequences`** — 沒設定時，Claude 會關圍籬然後繼續寫，毀掉 parse。
4. **生成後在每次迭代重新生成** — 這會摧毀可比性；生成一次、存檔、重用。
5. **沒在 prompt 裡指定確切數量** — 「產一些測試案例」會給你不可預測的大小，搞壞批次處理假設。

---

> **Key Insight**
>
> Prefilling + stop-sequence 技巧是本課最值得重用的技術。它把「叫 Claude 輸出 JSON」從脆弱的 parse 問題變成一行程式。背起來 — 它會出現在 D3（資料集生成）、D5（production 結構化輸出），以及任何需要機器可讀輸出但又不想啟動完整 tool use 協定的地方。

---

## CCA 考試相關性

- **D3（Evaluation & Iteration）**：Dataset generation 是 eval 工作流的一個命名子步驟；要知道「用 Claude 產生」和「手工建」兩種選項。
- **D5（Enterprise Deployment）**：Prefilling + stop-sequence 模式是 production 系統取結構化輸出的首選做法。
- 準備好回答類似「如何為新 prompt bootstrap 一份 eval 資料集？」→ 用 Haiku 生成、prefill JSON 圍籬、用 stop sequence、`json.loads`、存檔。

---

## Flashcards

| Front | Back |
|-------|------|
| 課程建議用哪個模型產資料集？為什麼？ | Haiku — 對批次創意工作（如產生測試案例），它比完整版 Claude 更快、更便宜。 |
| AWS code assistant prompt 的三種輸出格式是？ | Python 程式碼、JSON 設定檔、正規表示式。 |
| 資料集的最小結構是什麼？ | 一個 JSON 物件陣列，每個物件有一個 `task` 欄位描述 Claude 要完成什麼。 |
| 如何從 Claude 取得乾淨 JSON 而不用 tool use？ | Prefill 一則 assistant message 為 ` ```json `、設 `stop_sequences=["```"]`、對結果呼叫 `json.loads(text)`。 |
| `stop_sequences=["```"]` 在這個模式中的作用是什麼？ | Claude 一寫下收尾的 code fence 就停止生成，所以回傳文字是純 JSON。 |
| 為什麼資料集要存檔？ | 這樣同一份資料集可以在 prompt 迭代間重用，這是分數可比較的前提。 |
| 生成 prompt 裡的兩個明確約束是什麼？ | 「單一 Python function / JSON object / regex」以及「不用寫太多程式碼」。 |
| `chat()` helper 的預設 temperature 為何？原因？ | `temperature=1.0` — 高熵產生更多樣的測試案例，這正是 eval 資料集所需要的。 |
