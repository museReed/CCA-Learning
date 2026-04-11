# Multi-Turn Conversations with Tools — Engineering Deep Dive（繁中）

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture (22%) / D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 1.3（multi-turn conversation management）、1.2（agentic loop 實作）、2.4（multi-turn tool loops） |
| 來源 | building-with-the-claude-api / 01-api-fundamentals / Lesson 38 |

---

## 一句話總結

當 Claude 需要串連多個 tool call 才能回答一個使用者問題時，就會出現 multi-turn tool 對話；唯一的實作方式是一個**迴圈**，不斷往返打 API，直到 Claude 不再要求 tool 為止。

---

## 為什麼需要 Multi-Turn

有些問題沒辦法用一次 tool 呼叫回答。「103 天之後是幾號？」會拆解成：

1. `get_current_datetime()` → 今天日期
2. `add_duration_to_datetime(date, +103 days)` → 目標日期

Claude 沒辦法事先把兩次呼叫都打包好，因為第二次依賴第一次的輸出。每次呼叫都變成獨立回合，伺服器端（你的程式）負責推動這個迴圈。

```
使用者問題
  ↓
Claude → tool_use: get_current_datetime
  ↓
Server 執行 tool → tool_result
  ↓
Claude → tool_use: add_duration_to_datetime(date=..., days=103)
  ↓
Server 執行 tool → tool_result
  ↓
Claude → 最終文字答案（stop_reason="end_turn"）
```

---

## 對話 Loop 骨架

標準模式是一個 `while True` loop，當 Claude 不再要求 tool 時 break：

```python
def run_conversation(messages):
    while True:
        response = chat(messages)
        add_assistant_message(messages, response)

        # 虛擬碼——Lesson 39 會看到真正的 stop_reason 檢查
        if not response_is_asking_for_a_tool(response):
            break

        tool_result_blocks = run_tools(response)
        add_user_message(messages, tool_result_blocks)

    return messages
```

三個重點：

1. **`add_assistant_message` 保留完整 block list**（text + tool-use blocks）
2. **`run_tools` 執行每一個 tool-use block** 並一次回傳所有結果
3. **`add_user_message` 吃 tool result** 把結果包成單一則 user-role message 送回去

---

## 重構 Helper Function 支援 Multi-Block

Lesson 強調：實作 loop 之前，你的 helper 必須升級成能接 `Message` 物件，不只是字串。

### `add_user_message`——接字串、block list 或 Message

```python
from anthropic.types import Message

def add_user_message(messages, message):
    content = message.content if isinstance(message, Message) else message
    messages.append({"role": "user", "content": content})
```

這種多型讓你可以用這些方式呼叫：
- 純字串（`"現在幾點？"`）
- content block list（tool result blocks）
- API 回傳的完整 `Message` 物件

### `add_assistant_message`——同樣的多型

```python
def add_assistant_message(messages, message):
    content = message.content if isinstance(message, Message) else message
    messages.append({"role": "assistant", "content": content})
```

### `chat`——接受 tools、回傳完整 Message 物件

```python
def chat(messages, system=None, temperature=1.0, stop_sequences=[], tools=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }
    if tools:
        params["tools"] = tools
    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message
```

一旦有 tool 介入，回傳整個 `Message`（而不是 `.content[0].text`）是**必要的**——你需要 block list、`stop_reason` 和 usage data 來驅動 loop。

### `text_from_message`——需要時抽出顯示用的文字

```python
def text_from_message(message):
    return "\n".join(
        [block.text for block in message.content if block.type == "text"]
    )
```

用 `block.type == "text"` 過濾是從混合 block 回應中拉出使用者可見說明的標準做法。

---

## 對話累積的語意

每個回合至少會在歷史中多加一則訊息：

| 回合 | 加到 `messages` 的內容 |
|------|-----------------------|
| 0 | 使用者問題 |
| 1 | Assistant message：`text + tool_use_1` |
| 2 | User message：`tool_result_1` |
| 3 | Assistant message：`text + tool_use_2` |
| 4 | User message：`tool_result_2` |
| 5 | Assistant message：最終文字（`stop_reason=end_turn`） |

注意 assistant 和 user message **嚴格交替**——tool result 永遠是 user message 送回來，絕對不能是 assistant message。這保留了 API 強制的交替不變式。

---

## Context Window 考量

每次迭代會讓 `messages` 成長一條（有時兩條）訊息。長 tool 鏈會讓你撞到 context window 上限。緩解策略：

1. **用 `max_iterations` 計數器卡住 loop**，防止 agent 失控
2. **摘要中間 tool 結果**，如果裡面有不再需要的冗長資料
3. **用 prompt caching**（課程後面會講），分攤歷史成長的成本
4. **讓 tool 回應短一點**——回簡潔 JSON 的 tool 比回整個網頁的 tool 好太多

---

## 常見錯誤

1. **只 append `.content[0].text` 到歷史**——會掉 tool-use block，下一回合 `tool_use_id` 就配對不上
2. **忘了每次 loop 都要帶 `tools=[...]`**——Claude 每次都需要 schema，即使只是在回應 tool result
3. **用字串呼叫 `add_user_message` 來送 tool result**——tool result 必須是 content-block list
4. **沒有 loop 上限**——壞掉的 tool 或搞混的 Claude 會產生無限 tool-use loop，燒光 token
5. **用「有沒有 text content」當 break 條件**——Claude 可以同一回合吐 text 加 tool_use；永遠檢查 `stop_reason`

---

> **Key Insight**
>
> Multi-turn tool 對話不是特例——它是通例。單回合 tool use 只是「loop 跑完一次就結束」的情況。即使你第一個 tool-use 功能只需要單一 tool，也把它寫成標準 loop 形式，將來產品需要 tool 串接時就不用重寫。前期投資在 helper function 的多型處理，就是讓 loop 實作變輕鬆的關鍵。

---

## CCA Exam Relevance

- **D1（Agentic Architecture）**：這是核心的 agentic loop 問題。考題會問「什麼信號讓 loop 繼續」、「Claude 怎麼知道要串接 tool」。
- **D2（Tool Design & MCP Integration）**：理解 tool schema 必須在每次 loop 迭代都帶上。
- 考試提示：問 multi-turn tool 對話的題目幾乎都在考 loop 結構——把 `while` 模式背熟。

---

## Flashcards

| 題目 | 答案 |
|------|------|
| 為什麼有些問題需要 multi-turn tool 對話？ | 因為第二個 tool call 依賴第一個的輸出（例如「103 天後」要先知道今天） |
| 用什麼控制結構實作 multi-turn tool 對話？ | `while` loop，持續呼叫 API 直到 Claude 不再要 tool |
| `add_assistant_message` 除了字串還要接什麼？ | 完整 `Message` 物件——才能保留包含 tool-use block 的整個 block list |
| 為什麼 `chat` 要回傳整個 `Message` 而不只是 text？ | 因為你需要 `content`（block list）、`stop_reason` 和 usage data 來驅動 loop |
| 哪個 helper 從混合 block 訊息中抽出使用者可見文字？ | `text_from_message`——用 `block.type == "text"` 過濾再合併 |
| 為什麼要用 `max_iterations` 卡住 loop？ | 防止失控的 agent 或壞掉的 tool 產生無限 loop |
| Multi-turn tool 對話的交替不變式是什麼？ | Assistant 和 user message 必須嚴格交替；tool result 永遠放在 user message |
| 為什麼不能用「有 text 就 break」？ | Claude 可以同回合吐 text 加 tool_use——永遠改用 `stop_reason` 檢查 |
