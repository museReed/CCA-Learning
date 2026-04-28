# Making a Request — Engineering Deep Dive（繁體中文）

| 項目 | 內容 |
|------|------|
| Exam Domain | D5 — Enterprise Deployment (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 5.1（model selection）、5.3（production patterns）、1.2（agentic loop 基礎） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 06 |

---

## One-Liner

`client.messages.create()` 是 Anthropic API 的原子單位——三個必要參數（`model`、`max_tokens`、`messages`）產生一個 response，文字在 `response.content[0].text`。這個呼叫就是 agents、tool use、streaming 等所有上層 feature 的基礎。

---

## 環境設定：最小可行 Stack

在呼叫任何 API 前，兩個套件是必要的：

```bash
%pip install anthropic python-dotenv
```

- **`anthropic`** —— 官方 Python SDK。包住 REST API，處理認證、重試、pagination。
- **`python-dotenv`** —— 把本地 `.env` 載進 `os.environ`，讓 SDK 能自動讀 `ANTHROPIC_API_KEY`。

`.env` 放在 notebook 或 entry point 旁邊：

```
ANTHROPIC_API_KEY="sk-ant-api03-...your-key..."
```

兩條規則救你免於意外洩漏憑證：

| 規則 | 原因 |
|------|------|
| `.env` 加進 `.gitignore` | 防止 commit |
| 絕不用字串 literal 把 key 寫進程式碼 | 防止它出現在 notebook、log、Slack |

---

## Client 物件

一個 process 一個 instance，每次呼叫都重用：

```python
from dotenv import load_dotenv
load_dotenv()

from anthropic import Anthropic

client = Anthropic()           # 從環境變數自動讀 ANTHROPIC_API_KEY
model = "claude-sonnet-4-5"    # 把 model 名字釘在一個地方
```

把 model 名字釘在變數裡（而不是四處撒字串 literal）是一個小習慣，但回報很大：未來要升級 model，只要改一行。

---

## 三個必要參數

```python
message = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "What is quantum computing? Answer in one sentence"}
    ],
)
```

| 參數 | 型別 | 用途 |
|------|------|------|
| `model` | string | 用哪個 model，例如 `"claude-sonnet-4-5"` |
| `max_tokens` | int | 輸出長度上限（不是目標） |
| `messages` | list[dict] | 對話歷史（見下一節） |

### `max_tokens` 是上限不是目標

這是新手最常見的誤解。`max_tokens=1000` **不是**告訴 Claude 「寫 1000 個 token 的輸出」，而是告訴 Claude 「你最多可以寫 1000 個 token；遇到自然結束或寫到 1000，看哪個先到」。

| 行為 | 正確理解 |
|------|---------|
| 設預算？ | 是 |
| 設目標？ | 不是 |
| 強迫輸出變長？ | 不能（要用 prompt 措辭去引導） |
| 打到上限時 `stop_reason == "max_tokens"`？ | 是 |

實務規則：把 `max_tokens` 設成你預期最長合理回應的 1.5 倍。太低會真的截斷；太高不會浪費（你只為實際生成的 token 付錢），但會掩蓋 prompt bug。

---

## `messages` List

`messages` 是一個有序的 dict list，每個 dict 有 `role` 和 `content`：

```python
messages = [
    {"role": "user",      "content": "Define quantum computing"},
    {"role": "assistant", "content": "Quantum computing uses qubits..."},
    {"role": "user",      "content": "Give me a concrete example"},
]
```

| Role | 誰寫的 | 何時 |
|------|-------|------|
| `user` | 人（或你的後端代寫） | 永遠是第一個和最後一個 |
| `assistant` | 之前 Claude 的回應你重播回來 | 在 user turn 之間，提供上下文 |

兩個不變式必須成立：

1. **第一個 message 必須是 `user`**。忘了從 `assistant` 開始，API 會拒絕。
2. **Turn 必須交替**。連續兩個 `user` message 不允許；要合併或塞一個 assistant turn。

這就是 Lesson 07 用來建立多輪對話的形狀——每次追問都追加兩個 entry（前一次的 assistant 回應 + 新的 user 問題）。

---

## 取出 response 文字

Response 物件是結構化的（帶 usage、stop_reason、metadata），所以拉出文字要一行：

```python
message = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[{"role": "user", "content": "What is quantum computing? Answer in one sentence"}],
)

print(message.content[0].text)
```

為什麼是 `content[0].text` 而不只是 `content`？

- `content` 是一個 **content block 的 list**，不是字串。
- 單純文字回應時，list 只有一個 `TextBlock` 在 index 0。
- 有 tool use 時（Lesson 32 之後），同一個 list 可能交錯出現 `tool_use` 和 text block。
- 索引 `[0]` 在最簡單情況可以用，但是壞習慣——生產環境要 iterate 並 pattern-match block type。

```python
# 生產環境更安全的 pattern
for block in message.content:
    if block.type == "text":
        print(block.text)
    elif block.type == "tool_use":
        handle_tool_use(block)
```

---

## 完整 End-to-End 範例

```python
from dotenv import load_dotenv
load_dotenv()

from anthropic import Anthropic

client = Anthropic()
model = "claude-sonnet-4-5"

def ask(question: str, max_tokens: int = 1024) -> str:
    """Single-turn 問答 helper。"""
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": question}],
    )
    # 生產環境 iterate；demo 可以用 index。
    return response.content[0].text

print(ask("What is quantum computing? Answer in one sentence."))
```

差不多 15 行程式碼，就是完整最小可行 Claude 整合。課程後面所有東西——多輪、streaming、tool use、agents——都是疊在這個骨架上面。

---

## Common Mistakes

1. **把 `max_tokens` 當目標** —— Claude 遇到 `end_turn` 就停，這個參數是 cap 不是配額。
2. **`messages` 從 `assistant` 開始** —— 無效請求；第一個 turn 必須是 `user`。
3. **連續兩個 `user` message** —— 無效；要合併或中間塞 assistant turn。
4. **把 `response.content` 當字串用** —— 它是 content block 的 list；用 `response.content[0].text` 或 iterate。
5. **Model 名字到處硬編碼** —— 釘在一個變數，升級 model 才會是一行改動。

> **Key Insight**
>
> `client.messages.create()` 看起來小得嚇人——三個參數、一個 response——但它是你未來會出的每個 Claude feature 的 **原子**。多輪是這個呼叫跑 loop；tool use 是這個呼叫跑兩次；agents 是這個呼叫跑 loop 加分支；streaming 是這個呼叫加 flag。把三個必要參數和 `content[0].text` 提取方法深度內化，你就能推理所有上層 pattern。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）**：考題會問 `max_tokens` 語意、必要參數集、怎麼讀 response envelope。
- **D1（Agentic Architecture）**：每個 agent loop 都是 `messages.create()` 的 for-loop；熟悉原子呼叫是所有 D1 內容的前置。
- 情境觸發：「`max_tokens` 是什麼意思？」→ 永遠是「輸出長度的上限，不是目標」。

---

## Flashcards

| Front | Back |
|-------|------|
| `client.messages.create()` 三個必要參數是什麼？ | `model`、`max_tokens`、`messages` |
| `max_tokens` 設的是目標長度還是上限？ | 上限——Claude 自然遇到 `end_turn` 就停，或打到 `max_tokens` 被截 |
| `messages` 第一個訊息 role 必須是什麼？ | `user`——從 `assistant` 開始是無效的 |
| 怎麼取簡單回應的純文字？ | `response.content[0].text` |
| 為什麼 `response.content` 是 list 不是字串？ | 它是有序的 content block list；tool use 時 `text` 和 `tool_use` 類型可以交錯 |
| Lesson 06 安裝哪兩個套件？ | `anthropic`（SDK）和 `python-dotenv`（載 `.env`） |
| 為什麼 model 名字要釘在單一變數？ | 這樣升級 model 只改一行，不用 find-and-replace |
| SDK 會自動讀哪個環境變數？ | `ANTHROPIC_API_KEY` |
