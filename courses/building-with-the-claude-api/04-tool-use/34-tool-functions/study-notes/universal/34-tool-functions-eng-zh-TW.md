# Tool Functions — Engineering Deep Dive

| 項目 | 內容 |
|------|------|
| 考試 Domain | D2 — Tool Design & MCP Integration (18%) 主要;D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.2(tool function 定義)、2.1(tool schema 設計)、1.2(agentic loop 基礎) |
| 來源 | building-with-the-claude-api / 04-tool-use / Lesson 34 |

---

## 一句話總結

Tool function 就是一個普通的 Python function — 但它的輸入、錯誤訊息、行為是刻意設計成**給 LLM 讀、給 LLM 自我修復**,而不只是給人類工程師看。

---

## 什麼是 Tool Function

Tool function 就是你的應用程式在 Claude 吐出 `tool_use` block 時會執行的一般 Python callable。Python 這端沒有魔法 — 魔法在於 function 與 LLM 之間的**契約**:

- 名字清楚 → Claude 挑得到正確的 function
- 參數名字清楚 → Claude 填得到正確的參數
- 驗證 + 描述性的錯誤 → Claude 下一輪可以自我修正
- 回傳型別可預測 → Claude 可以對結果推理

Tool function 是技術堆疊的底層。JSON schema(Lesson 35)是 Claude 讀的文件。Agentic loop 用 Claude 給的參數呼叫 function。

---

## 第一個 Tool:`get_current_datetime`

```python
from datetime import datetime

def get_current_datetime(date_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)
```

三個值得拆開來看的地方:

1. **預設引數**(`date_format="%Y-%m-%d %H:%M:%S"`)— 讓 Claude 在常見情境下不用傳參數就能呼叫。Schema 會標這個參數為 optional。
2. **使用前驗證** — `if not date_format: raise ValueError(...)` 擋掉 Python 原本會默默接受的退化值(空字串夠 falsy,`strftime("")` 會回空字串)。
3. **`strftime` 格式傳遞** — 把日期格式化丟給 Python 身經百戰的 `datetime` 模組,而不是自己重造輪子。

### 使用範例

```python
get_current_datetime()           # "2026-04-11 14:30:25"
get_current_datetime("%H:%M")     # "14:30"
get_current_datetime("%A")        # "Saturday"
```

---

## Tool Function 的 Best Practices

### 1. 描述性的名字

Function 名字:`get_current_datetime` — 人類一眼看懂意圖。對比 `gcdt` 或 `datetime_fn`。Claude 會把名字當成決定是否呼叫這個 function 的強先驗。

參數名字:`date_format`,不是 `fmt` 或 `d`。每個字元都是 Claude 會讀的文件。

### 2. 驗證輸入

```python
def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)
```

常見的驗證 pattern:

- 空字串(`if not s`)— LLM 意外頻繁會出這種。
- 型別錯(`if not isinstance(x, int)`)— 尤其是 JSON 反序列化之後。
- 超出範圍(`if not 0 <= p <= 100`)。
- 格式不符(regex、enum 成員)。

每個參數要問自己:「LLM 可能吐出什麼最糟糕的輸入,會讓我靜默產出錯答案?」針對那個驗證。

### 3. 有意義的錯誤訊息

**差**:`raise ValueError("invalid input")`
**好**:`raise ValueError("date_format cannot be empty")`
**更好**:`raise ValueError("date_format cannot be empty; use a valid strftime pattern like '%Y-%m-%d'")`

錯誤訊息是 Claude 唯一的回饋管道。每一則錯誤訊息都是一段迷你 prompt,告訴下一輪怎麼修正。如果你寫「invalid input」,Claude 可能用同樣的錯輸入再試一次。如果你寫「expected an ISO-8601 date like 2026-01-15, got 'next Friday'」,Claude 就知道該怎麼修。

這是與傳統錯誤訊息設計最大的轉變:**錯誤訊息不再只是給人看,而是 LLM 的修復訊號**。

---

## Tool Function 如何跟 Loop 整合

```python
# agent loop 的 pseudo-code
while True:
    response = client.messages.create(..., tools=tool_schemas, messages=messages)

    if response.stop_reason != "tool_use":
        break  # 最終文字回應在 response.content 裡

    for block in response.content:
        if block.type != "tool_use":
            continue
        fn = TOOL_REGISTRY[block.name]
        try:
            result = fn(**block.input)
            tool_result_content = str(result)
            is_error = False
        except Exception as e:
            tool_result_content = f"Error: {e}"
            is_error = True

        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": tool_result_content,
                "is_error": is_error,
            }],
        })
```

關鍵觀察:

- 捕捉例外並以 `is_error: True` 的 `tool_result` 傳回。不要讓例外把 loop 打斷 — 告訴 Claude 它就能復原。
- `**block.input` 把 JSON 參數展開給 Python。型別不符會在 Python 呼叫點被擋下。
- `TOOL_REGISTRY` 就是個「tool 名字 → function pointer」的 dict。讓 dispatch 超簡單。

---

## Type Hint 對人與 Schema 都有幫助

Python type hint 在 runtime 是可有可無,但在設計階段極有價值:

```python
def get_current_datetime(date_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    ...
```

- 讓推導 schema(Lesson 35)變得超簡單。
- 在 runtime 前就抓到開發者 bug。
- 對 review code 的隊友傳達意圖。
- `inspect`、`pydantic` 之類的 library 可以從有 type hint 的 function 自動產生 JSON Schema。

---

## 常見錯誤

1. **名字曖昧的 function** — `process`、`run`、`do_it`。Claude 從含糊的名字推不出用途。
2. **輸入壞的也默默吃下去** — 接受 `None` 或空字串卻不驗證,產出垃圾結果。
3. **神祕的錯誤訊息** — 「error 42」告訴 Claude 什麼都沒有;「radius must be positive, got -3」告訴它要怎麼修。
4. **沒在 loop 層級捕捉例外** — 讓 tool 例外把整段對話炸掉,而不是包成 tool_result error 餵回去。
5. **隱藏的副作用** — 名字沒寫清楚就靜默寫 DB 的 tool 很危險;用 `create_reminder` 取代 `reminder`。
6. **回傳複雜物件沒 `str()`** — `tool_result.content` 必須是可序列化的文字;把物件顯式轉字串或 JSON。

> **Key Insight**
>
> Tool function 不是「內部工具」 — 它是你對 Claude 暴露的 **public API**。每個參數名、每個錯誤訊息、每個回傳型別都會被模型讀到。把 tool function 當成文件完整的 SDK 設計,因為 Claude 就是這樣看它的。CCA D2 常出這個角度的題目。

---

## CCA 考試重點

- **D2(Tool Design & MCP Integration)**:命名、驗證、錯誤訊息作為 LLM 可讀的修復訊號、預設引數。
- **D1(Agentic Architecture)**:Tool loop 內的例外處理;錯誤如何轉成 tool_result block。
- 預期會出:「為何 tool function 要 raise 描述性的錯誤?」— 答:讓 Claude 在下一輪能自我修正。

---

## Flashcards

| Front | Back |
|-------|------|
| Tool function 是什麼? | 一般的 Python callable,Claude 吐出 `tool_use` block 時會被呼叫;function 必須驗證輸入並回傳可序列化的結果。 |
| 為何 tool function 的錯誤訊息很重要? | 因為它是 Claude 唯一的回饋管道 — Claude 會讀它並用來自我修正下一次 `tool_use` 呼叫。 |
| 什麼是差的 tool function 名字? | 任何像 `process`、`run`、`do_it` 這類含糊的名字 — Claude 推不出用途。 |
| 若 tool function 在 agent loop 內丟例外會怎樣? | 呼叫方應該捕捉並以 `is_error: True` 的 `tool_result` 回傳 — 不要讓它炸掉 loop。 |
| 為何 tool function 要用預設引數? | 讓 Claude 在常見情境下能用最少的輸入呼叫,只在必要時才帶參數。 |
| `get_current_datetime` 驗證了什麼、為什麼? | 它拒絕空的 `date_format`,這樣 `strftime("")` 才不會默默回空字串。 |
| Tool function 要怎麼回傳複雜物件? | 轉成字串或 JSON — `tool_result.content` 必須是可序列化文字。 |
| Type hint 與 schema 有什麼關係? | Type hint 讓 JSON Schema 可以自動產生,並讓 Claude(透過 schema)與人類都看到清楚意圖。 |
