# Tool Schemas — Engineering Deep Dive

| 項目 | 內容 |
|------|------|
| 考試 Domain | D2 — Tool Design & MCP Integration (18%) 主要;D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.1(tool schema 設計)、2.2(tool function 定義)、1.2(agentic loop 基礎) |
| 來源 | building-with-the-claude-api / 04-tool-use / Lesson 35 |

---

## 一句話總結

Tool schema 是一份 JSON Schema 文件,包含三個頂層欄位(`name`、`description`、`input_schema`)— 它是你的 Python function 對 Claude 公開的 API contract,文字品質直接決定 Claude 會不會挑對 tool、會不會帶對參數。

---

## 三個必填欄位

每一個送到 Anthropic API 的 tool 定義都必須包含:

| 欄位 | 型別 | 用途 |
|------|------|------|
| `name` | string | Claude 引用 tool 的識別名稱,必須與 function registry 的 key 一致。 |
| `description` | string | 3-4 句,告訴 Claude tool 做什麼、何時用、回傳什麼。 |
| `input_schema` | JSON Schema object | 描述 function 參數的 JSON Schema。 |

這三個欄位組成 Claude 每次決定是否呼叫 tool 時會讀的 contract。

---

## 完整範例:`get_current_datetime`

```python
from datetime import datetime
from anthropic.types import ToolParam

def get_current_datetime(date_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)

get_current_datetime_schema: ToolParam = {
    "name": "get_current_datetime",
    "description": (
        "Returns the current date and time formatted according to "
        "the specified format string. Use this whenever you need to "
        "know the current moment in time, for example when a user "
        "asks what time it is or you need to timestamp a reminder. "
        "Returns a string formatted per Python's strftime codes."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": (
                    "A strftime format string such as '%Y-%m-%d %H:%M:%S'. "
                    "Defaults to ISO-style date and time if not provided."
                ),
                "default": "%Y-%m-%d %H:%M:%S",
            }
        },
        "required": [],
    },
}
```

注意**命名慣例**:function 叫 `get_current_datetime`,schema 變數叫 `get_current_datetime_schema`。鏡像命名讓你很容易把實作與 schema 對起來。

---

## `input_schema` 的結構解析

`input_schema` 就是標準的 JSON Schema 片段。三個最重要的部分:

### 1. `type: "object"`

Tool 的輸入永遠是 object(命名參數的 key-value map)。因為 API 會把 `input` 以 JSON object 傳入,你的程式碼用 `**block.input` 展開。

### 2. `properties`

`properties` 中的每個 key 是一個參數名。每個 value 是描述該參數型別、約束,以及**最重要的 description** 的子 schema。

```python
"properties": {
    "date_format": {
        "type": "string",
        "description": "A strftime format string...",
        "default": "%Y-%m-%d %H:%M:%S"
    }
}
```

每個屬性的 `description` 是你告訴 Claude「該傳什麼樣的值」的機會。把它當成寫給 LLM 看的 docstring。

### 3. `required`

一個陣列,列出哪些參數是必填的。沒列在這裡的就是 optional,Claude 可以省略不填。因為 `date_format` 有 default,所以是 optional,`required` 是空陣列。

```python
"required": []              # 全部 optional
"required": ["city"]         # city 必填,其他 optional
"required": ["city", "date"] # 都必填
```

---

## 為何描述品質決定一切

兩個 code 一模一樣但 description 不同的 tool,表現會天差地別:

| 描述 | 結果 |
|------|------|
| 「Gets the time」 | Claude 可能跟其他時間 tool 混淆;使用不穩定。 |
| 「Returns the current date and time formatted per strftime codes. Use when the user asks 'what time is it' or when you need to timestamp a new record. Returns a formatted string.」 | Claude 正確選中、帶對格式、合理解讀結果。 |

**描述的 best practices:**

- 3-4 句(足夠 context,不要寫小說)。
- 說明**做什麼**與**回傳什麼**。
- 說明 Claude **何時**該用它(「何時」這句最常被省略,但最有價值)。
- 提到相關 tool 避免混淆(例如「要把日期字串轉時間戳,請用 `parse_datetime`」)。
- 對參數,用具體範例描述合法值、單位、格式。

---

## 產生 Schema:讓 Claude 自己寫

與其手寫 schema,你可以叫 Claude 幫你產:

1. 複製 tool function 的程式碼。
2. 問 Claude 類似:「請為這個 function 寫一份合法的 JSON schema 用於 tool calling。遵循附件文件的 best practices。」
3. 把 Anthropic 的 tool-use 文件當作 context 附上。
4. 把產出的 schema 貼到程式碼,用 `{function_name}_schema` 命名慣例。

這本身就是 tool-use 原則的 meta 應用:用 AI 來打造 AI 自己的輸入。

---

## 用 `ToolParam` 做型別安全

`anthropic` SDK 暴露了一個 `ToolParam` TypedDict,可用於靜態分析:

```python
from anthropic.types import ToolParam

get_current_datetime_schema = ToolParam(
    name="get_current_datetime",
    description="Returns the current date and time...",
    input_schema={
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": "...",
                "default": "%Y-%m-%d %H:%M:%S",
            }
        },
        "required": [],
    },
)
```

好處:

- IDE 對三個必填欄位有自動補全。
- Mypy/pyright 可以在 runtime 前抓到像 `descripton` 這種拼錯。
- 程式碼自我文件化。

非強制 — API 也接受一般 dict — 但生產環境強烈建議用。

---

## Tool 定義常用的 JSON Schema 功能

| 功能 | 範例 | 用途 |
|------|------|------|
| `type` | `"string"`、`"integer"`、`"boolean"`、`"array"`、`"object"`、`"number"` | 宣告 JSON 型別 |
| `description` | 自由文字 | 給 LLM 讀的逐參數指引 |
| `default` | 字面值 | Claude 省略 optional 參數時使用 |
| `enum` | `["celsius", "fahrenheit"]` | 限制在固定允許值集合 |
| `items` | schema | 描述陣列元素型別 |
| `minimum` / `maximum` | 數值 | 數值範圍 |
| `pattern` | regex | 字串格式驗證 |
| `required` | 名稱陣列 | 必填屬性名 |

`enum` 特別強大:強迫 Claude 從定義好的集合裡挑,消除模糊性。

---

## 常見錯誤

1. **缺 `type: "object"`** — 每個 `input_schema` 都必須從 `type: "object"` 開始,不能只放 `properties`。
2. **空的或含糊的 description** — 「Gets data」對 Claude 等於沒說。要投資文字。
3. **忘了寫 `required`** — 省略不代表「全部必填」,代表「全部 optional」。要明確。
4. **Schema 與 function 不一致** — schema 寫 `city`,function 用 `location`。Claude 會傳 `city`,程式碼直接炸。
5. **Pattern 過度限制** — 正規表示式拒絕了你沒預期到的合法輸入,卡住正當使用。
6. **把實作細節放進 description** — Claude 不需要知道你打的是 SQLite;它需要知道 tool 在概念上做什麼。

> **Key Insight**
>
> Tool schema 不是接線 — 它是**LLM 可讀的 API contract**。描述裡的每個字、每個參數註解都會改變 Claude 呼叫 tool 的決策。你花在 schema 描述上的工程時間,會變成更少的誤選 tool、更少的錯誤參數、更少的挫折使用者。CCA 考試 D2 反覆出 `input_schema` 結構與 description best practice 的題目。

---

## CCA 考試重點

- **D2(Tool Design & MCP Integration)**:Tool 定義結構(`name`、`description`、`input_schema`)、JSON Schema 基礎、`required` 語意、enum 用法。
- **D1(Agentic Architecture)**:Schema 品質直接影響 Claude 在 agent loop 中選 tool。
- **D5(Enterprise Deployment)**:生產程式碼用 `ToolParam` 做型別安全。
- 預期題型:「Tool 定義的三個必填欄位是什麼?」或「兩個 tool 存在時 Claude 如何決定呼叫哪個?」— 答:description 品質與名稱清晰度。

---

## Flashcards

| Front | Back |
|-------|------|
| Tool 定義的三個必填欄位是什麼? | `name`、`description`、`input_schema`。 |
| `input_schema` 最上層的 `type` 永遠必須是什麼? | `"object"` — tool 輸入永遠是 JSON object。 |
| `input_schema` 裡的 `required` 是什麼意思? | 一個陣列列出必填的屬性名;沒列的就是 optional。 |
| 為何 tool schema 的 description 品質這麼關鍵? | Claude 讀 description 來決定何時呼叫 tool 與如何填參數 — 文字品質直接影響正確性。 |
| 課程建議 schema 用什麼命名慣例? | `{function_name}_schema` — 鏡像 function 名稱,讓實作與 schema 對得起來。 |
| `ToolParam` 是什麼、何時用? | `anthropic.types` 中的 TypedDict,讓 tool schema 可做靜態型別檢查;生產程式碼建議用,支援 IDE 與 mypy。 |
| 不手寫 JSON Schema 怎麼產 schema? | 叫 Claude 幫你產 — 貼 function 程式碼與 tool-use 文件,請它寫格式正確的 schema。 |
| 為何 property schema 要用 `enum`? | 把 Claude 限制在固定合法值集合(如 `["celsius", "fahrenheit"]`),消除模糊性。 |
| Schema 的參數名若與 Python function 的參數名不一致會怎樣? | Function 呼叫會失敗 — Claude 傳 schema 的名字、`**block.input` 展開到 function,Python 會丟 `TypeError`。 |
