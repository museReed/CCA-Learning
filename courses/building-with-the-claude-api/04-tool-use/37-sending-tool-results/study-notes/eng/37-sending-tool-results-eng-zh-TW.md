# Sending Tool Results — Engineering Deep Dive（繁中）

| 項目 | 內容 |
|------|------|
| 考試領域 | D2 — Tool Design & MCP Integration (18%) / D1 — Agentic Architecture (22%) |
| Task Statements | 2.4（tool_result block 格式）、2.2（content block 處理）、1.2（收尾 tool-use loop） |
| 來源 | building-with-the-claude-api / 04-tool-use / Lesson 37 |

---

## 一句話總結

Tool 執行結果要透過 `tool_result` content block 包在一則 **user** message 裡送回 Claude，每個 result 都要用 `tool_use_id` 精準對應前面 `ToolUseBlock.id`。

---

## 從 Tool 請求到執行

當 Claude 送回一個 `ToolUseBlock` 後，你用 block 的 `input` dict 去呼叫本地 function。Python 的 `**` 展開會把 dict 變成 keyword arguments：

```python
tool_block = response.content[1]  # 例如 [TextBlock, ToolUseBlock]
result = get_current_datetime(**tool_block.input)
# 等同 get_current_datetime(format="HH:MM:SS")
```

`input` dict 保證符合 tool 的 `input_schema`（假設 Claude 有照規則），所以 unpacking 就是 JSON Schema 和你 function signature 之間的標準橋樑。

---

## `tool_result` Block 的結構

`tool_result` block 是 user role 底下的 content block，只有這幾個欄位：

| 欄位 | 型別 | 用途 |
|------|------|------|
| `type` | 字面值 `"tool_result"` | 告訴 API 這個 block 是 tool 回傳 |
| `tool_use_id` | 字串 | 必須對應前面 `ToolUseBlock` 的 `id` |
| `content` | 字串或 block list | 你 tool 的輸出，序列化後的內容 |
| `is_error` | 布林 | tool 失敗就填 `True`，Claude 會依此處理錯誤 |

```python
messages.append({
    "role": "user",
    "content": [{
        "type": "tool_result",
        "tool_use_id": response.content[1].id,
        "content": "15:04:22",
        "is_error": False
    }]
})
```

關鍵不變式：**前一則 assistant message 裡的每一個 `ToolUseBlock` 都必須在下一則 user message 中對應一個 `tool_result`**。API 會嚴格驗證這個配對，不符就 400。

---

## Content 序列化規則

`content` 欄位可以接字串或 block list。非 trivial 的資料請序列化成 JSON：

```python
import json

tool_output = {"time": "15:04:22", "timezone": "UTC", "epoch": 1762978180}
result_block = {
    "type": "tool_result",
    "tool_use_id": tool_block.id,
    "content": json.dumps(tool_output),
    "is_error": False
}
```

Claude 被訓練成能讀 tool result 裡的 JSON 字串，所以結構化資料就用 `json.dumps`。二進位資料（圖片、檔案）則要用 list-of-blocks 形式，內部放 image block。

---

## 同一回合處理多個 Tool Call

如果 Claude 在一次回應裡要了超過一個 tool（例如「10+10 是多少？30+30 是多少？」會產生兩個 `ToolUseBlock`），你必須在**單一一則 user message** 裡送回**所有**對應的 `tool_result` block：

```python
tool_use_blocks = [b for b in response.content if b.type == "tool_use"]

tool_results = []
for tub in tool_use_blocks:
    output = run_tool(tub.name, tub.input)
    tool_results.append({
        "type": "tool_result",
        "tool_use_id": tub.id,
        "content": json.dumps(output),
        "is_error": False
    })

messages.append({"role": "user", "content": tool_results})
```

Result 在 content list 裡的順序不重要——靠 `tool_use_id` 配對。但**不可以漏**：少一個就會 400。

---

## 用 `is_error` 處理錯誤

Tool 噴例外時，不可以省略 result block。改成填 `is_error: True`，把錯誤訊息放進 `content`：

```python
try:
    output = run_tool(tub.name, tub.input)
    block = {
        "type": "tool_result",
        "tool_use_id": tub.id,
        "content": json.dumps(output),
        "is_error": False
    }
except Exception as e:
    block = {
        "type": "tool_result",
        "tool_use_id": tub.id,
        "content": f"Error: {e}",
        "is_error": True
    }
```

Claude 會讀錯誤訊息，可能重試不同參數、把失敗回報給使用者、或選另一種策略。默默丟掉失敗的 tool 會破壞 ID 配對，直接 400。

---

## Follow-Up API 呼叫

後續 request 必須：

1. 帶完整的對話歷史（原始 user message + assistant tool-use message + 新的 user tool-result message）
2. 仍然要帶 `tools=[...]`——Claude 需要 schema 去解析 tool 引用
3. 用同一個 `model` 和 `max_tokens` 設定

```python
client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,  # 已經有 3 則以上的 message，包含 tool-result
    tools=[get_current_datetime_schema]
)
```

Claude 下一個回應會把 tool 輸出整合成自然語言。如果它還要呼叫別的 tool，就再 loop 一次。

---

## 常見錯誤

1. **把 `tool_result` 放在 assistant message**——必須放在 **user** role message，assistant role 的 tool result 會被拒絕。
2. **漏 `tool_use_id`** 或填錯值——API 會回 400「mismatched tool_use_id」。
3. **`content` 直接塞 dict/object** 而沒序列化——`content` 必須是字串（或 block list），結構化資料請 `json.dumps`。
4. **忘記填 `is_error`**——預設是 `False`，失敗時沒填就等於告訴 Claude 成功，會導致 hallucination。
5. **Claude 要多個 tool 但只回一個結果**——每個 `ToolUseBlock` 都要在同一回合有對應的 `tool_result`。
6. **follow-up 沒帶 `tools=[...]`**——Claude 會拒絕引用不存在 schema 的歷史。

---

> **Key Insight**
>
> `tool_use_id` 是你程式和 Claude 之間的契約。Assistant 送出的每一個 `ToolUseBlock` 都必須在下一則 **user** message 中有**剛好一個**對應 ID 的 `tool_result`。把它想成是 content block 層級的請求/回應配對，而不是 message 層級——而且即使是錯誤也要用 `is_error: True` 的 `tool_result` 送回去，不可以整個 block 不送。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：記住 `tool_result` block 的四個欄位，以及它在哪個 role（`user`）裡。
- **D1（Agentic Architecture）**：把請求/結果配對理解成 agentic loop 的基本單位。
- 考題會丟壞掉的 `tool_result`（錯 role、漏 ID、塞 dict）問你會出什麼錯。

---

## Flashcards

| 題目 | 答案 |
|------|------|
| `tool_result` block 要放在哪個 role 的 message 裡？ | `user` role——Claude 把 tool result 看成使用者提供的 context |
| `tool_result` block 哪個欄位用來配對前面的 tool-use 請求？ | `tool_use_id`——必須精準對應 `ToolUseBlock.id` |
| `tool_result` 的 `content` 欄位型別是什麼？ | 字串（或給圖片/檔案用的 block list）——結構化資料用 `json.dumps` |
| Tool 噴例外時 `is_error` 要設什麼？ | `True`——並把錯誤訊息放進 `content`，不要直接丟掉 block |
| 把 `ToolUseBlock.input` 展開成 keyword arguments 的 Python 語法？ | `my_function(**tool_block.input)` |
| Claude 要兩個 tool 但你只回一個 result 會怎樣？ | API 會 400，說 `tool_use_id` 配對失敗 |
| follow-up API 呼叫還需要帶 `tools=[...]` 嗎？ | 需要——Claude 要 schema 才能解析對話歷史中的 tool 引用 |
| 一回合有多個 tool call 怎麼處理？ | 全部執行、收集每個 `tool_result` block、用**單一**一則 user message 一起送回去 |
