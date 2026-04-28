# Defining Tools with MCP — 工程深度解析

| 項目 | 說明 |
|------|------|
| 考試領域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.1（tool schema 設計）、2.3（MCP primitives：tools）、1.2（agent loop 整合） |
| 來源 | building-with-the-claude-api / 07-mcp / Lesson 64 |

---

## 一句話總結

Lesson 64 示範 Python MCP SDK（`FastMCP`）如何把 tool 撰寫壓縮成「decorator + type hints」——SDK 會從你的 function signature 和 Pydantic `Field` 詮釋資料自動生出 JSON schema，讓你寫正常 Python 而不是手工 JSON Schema。

---

## 為什麼需要 SDK

Ch04 的 tool use 裡，每個 tool 定義都要寫一大段冗長的 JSON schema：

```python
tools = [{
    "name": "read_doc_contents",
    "description": "...",
    "input_schema": {
        "type": "object",
        "properties": {
            "doc_id": {"type": "string", "description": "..."}
        },
        "required": ["doc_id"]
    }
}]
```

一個 tool 還好，二十個 tool 就痛苦了。Python MCP SDK（`mcp.server.fastmcp.FastMCP`）用 decorator 驅動的模式：

- 拿一個普通的 Python function
- 讀取它的 type hints 和 `Field(description=...)` 註解
- 自動產出對應的 JSON schema
- 把 tool 註冊到 MCP server

結果是：tool 定義縮到幾行，看起來就像普通 Python 程式碼。

---

## 建立 Server

建立一個 MCP server 只要一行 import + 一行初始化：

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")
```

- `"DocumentMCP"` 是 server 的名字（呈現給 clients 的識別名）。
- `log_level="ERROR"` 在開發時壓掉吵人的 info log。

`mcp` 物件是一個 registry，你把 tools（以及後面的 lessons 要加的 resources 和 prompts）掛在上面。

---

## 記憶體文件儲存

這節課把普通 Python dict 當「資料庫」用：

```python
docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditure",
    "outlook.pdf": "This document presents the projected future performance of the",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment"
}
```

Key 是 document ID，value 是文字內容。沒有 persistence——文件活在 process memory。這樣做是刻意的，讓焦點放在 MCP 撰寫而不是 DB 水管上。

---

## Tool 1：`read_doc_contents`

Decorator 驅動的讀取 tool：

```python
@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string."
)
def read_document(
    doc_id: str = Field(description="Id of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    return docs[doc_id]
```

底層發生的事：

| Source 元素 | 變成什麼 |
|------------|---------|
| `@mcp.tool(name=..., description=...)` | MCP schema 裡 tool 的頂層 metadata |
| `doc_id: str` type hint | 生出的 JSON Schema 裡的 `{"type": "string"}` |
| `Field(description="...")` | `doc_id` property 的 `description` |
| Function body | Claude 發 `CallToolRequest` 時執行的 callable |
| `raise ValueError(...)` | 會變成 Claude 能讀的 tool 錯誤，可能可以修正 |

注意 function 名（`read_document`）和 MCP tool 名（`read_doc_contents`）是獨立的；decorator 的 `name=` 才是權威。

---

## Tool 2：`edit_document`

第二個 tool 是簡單的 find-and-replace 編輯器：

```python
@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string."
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace."),
    new_str: str = Field(description="The new text to insert in place of the old text.")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
```

工程細節：

- 三個參數，每個都用 `Field(description=...)` 註解，讓 Claude 理解角色。
- `old_str` description 明寫「must match exactly, including whitespace」——這是面向 Claude 的文件，可減少不穩定的編輯。
- 實作用 Python 內建 `str.replace`，會替換**所有**出現位置；如果你真實系統需要唯一性，要加一個 match-count check。
- Function 沒有顯式 return；它直接 mutate dict。

---

## 用 `ValueError` 做錯誤處理

兩個 tools 收到無效 `doc_id` 時都 `raise ValueError`。MCP SDK 會把這些轉成 tool error response，Claude 在下一個 `tool_result` block 收到，讓它可以：

- 道歉並請使用者提供有效 ID
- 用看起來相似的 ID 重試
- 升級成「找不到這份文件」的最終回答

這是**結構化錯誤**模式：你給 Claude 一段可讀的解釋，而不是默默失敗；agent loop 就能把錯誤納入推理。

---

## SDK 方式的關鍵好處

這節課列了五個相較手寫 tool schema 的贏面：

1. **自動從 Python type hints 產出 JSON Schema**。
2. **乾淨、可讀的 code**——tool body 看起來像普通 Python。
3. **用 Pydantic `Field` 內建參數驗證**。
4. **減少樣板**——不用手寫 `{"type": "object", "properties": ...}` 的 dict。
5. **開發時的型別安全和 IDE 支援**。

Meta-point：SDK 讓你專注在**業務邏輯**（tool 做什麼），協定層（schema、序列化）自動處理。

---

## 課程沒示範的進階考量

Source 刻意簡化，但真實 server 還該考慮：

| 關注點 | 為什麼 |
|-------|-------|
| Return type hints | 完全型別化的 return 讓 FastMCP 能描述結果形狀 |
| 帶 default 的 optional 參數 | 用 `Field(default=..., description=...)` |
| 長描述 | `description` 是 Claude 的操作手冊——值得投資寫清楚 |
| Side-effect logging | `edit_document` 修改 state；prod 應每次呼叫都 audit-log |
| 並發安全 | dict 是共享 state；prod 要用 lock 或 async-safe store |

這些不是完成這門課專案的必要項目，但能區分「demo 能跑」和「能上線給使用者」。

---

## 常見錯誤

1. **忘了 `Field` description。** 沒有的話 Claude 只看到參數名字——tool 品質立刻下降。
2. **用 function 名當 MCP tool 名。** Claude 看到的是 decorator 的 `name=`；function 名是內部的。
3. **讓錯誤變未處理 exception 冒上來。** `ValueError` 會被轉成可讀的 tool error；其他 exception 比較吵且不好恢復。
4. **以為 tool name 和 schema 是穩定的。** 如果你改名或改形狀，clients（包括 lesson 65 的 MCP inspector）要重新 list tools。
5. **靠 description 做 prompt engineering。** Description 要誠實；不要塞相互矛盾的指示讓 Claude 混淆。

> **Key Insight**
>
> Python MCP SDK 把 tool 撰寫變成普通 Python code + 兩撮 metadata（`@mcp.tool(...)` + `Field(description=...)`）。這就是 MCP 的核心生產力贏面：你用「decorated function」換掉「手寫 JSON Schema」，framework 搞定協定。課程後面加的每個 tool 都是這個模式。

---

## CCA 考試重點

- **D2（Tool Design & MCP Integration）**：知道 `FastMCP("Name", log_level=...)`、`@mcp.tool(name, description)` decorator、以及 `Field(description=...)` 如何填入 schema。
- **D1（Agentic Architecture）**：理解 `ValueError` 如何在 agent loop 裡被呈現成 Claude 可恢復的 tool error。
- 情境題可能問：「SDK 怎麼知道要 require `doc_id`？」——答：因為它是沒有 default 的 positional 參數，SDK 把它標成 schema 中的 required。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Python MCP SDK 用哪個 class 初始化 server？ | `FastMCP`（來自 `mcp.server.fastmcp`） |
| 怎麼宣告一個 tool？ | 用 `@mcp.tool(name=..., description=...)` decorate 一個 function |
| 怎麼為 Claude 文件化一個參數？ | 用 Pydantic 的 `Field(description="...")` 當參數 default |
| SDK 從你的 type hints 產出什麼？ | JSON Schema（包含 `type`、`properties`、`required`） |
| 兩個 demo tools 的資料持久化方式？ | 沒有——文件活在 module-level 的 Python dict（記憶體） |
| `read_doc_contents` 收到不存在的 doc_id 會怎樣？ | Tool `raise ValueError`，變成送給 Claude 的 tool error |
| Demo server 對外提供幾個 tools？ | 兩個——`read_doc_contents` 和 `edit_document` |
| 這節課列出 SDK 方法的哪五個好處？ | 自動 JSON Schema、乾淨 code、Pydantic validation、減少樣板、型別安全/IDE 支援 |
