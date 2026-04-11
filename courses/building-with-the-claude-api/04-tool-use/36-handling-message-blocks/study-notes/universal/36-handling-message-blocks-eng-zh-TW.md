# Handling Message Blocks — Engineering Deep Dive（繁中）

| 項目 | 內容 |
|------|------|
| 考試領域 | D2 — Tool Design & MCP Integration (18%) / D1 — Agentic Architecture (22%) |
| Task Statements | 2.2（content block 處理）、2.1（tool schema 整合）、1.2（agentic loop 基礎） |
| 來源 | building-with-the-claude-api / 04-tool-use / Lesson 36 |

---

## 一句話總結

只要在 request 中帶入 `tools=[...]`，Claude 的回應 `content` 就不再是單一字串，而是一個由 `TextBlock`、`ToolUseBlock` 等 typed block 組成的 list；你的程式碼必須迭代這些 block、完整保留到對話歷史、並依 block type dispatch。

---

## 從純文字回應跨到 Multi-Block 回應

沒有 tools 時，`response.content` 實務上只是一個 `TextBlock`。一旦 request 帶 `tools=[...]`，Claude 就可能決定要呼叫 function，assistant message 就會變成**異質的 block list**：

```python
response = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    tools=[get_current_datetime_schema],
)

# response.content 現在是 block 的 list：
# [TextBlock(text="我可以幫你查現在的時間..."),
#  ToolUseBlock(id="toolu_01...", name="get_current_datetime", input={})]
```

關鍵轉變：`response.content` **永遠是一個 list**，單一回合可能同時包含說明文字與一個或多個 tool use 請求。

---

## `ToolUseBlock` 的結構

每個 tool-use block 有四個你必須處理的欄位：

| 欄位 | 用途 |
|------|------|
| `type` | 永遠是 `"tool_use"`——用它來過濾 block |
| `id` | 每次呼叫唯一 ID（如 `toolu_01A09q90qw...`）。你必須在對應的 `tool_result` 中回填這個 ID |
| `name` | 模型選擇的 function 名稱（必須對應你註冊的 schema） |
| `input` | 符合該 tool `input_schema` 的參數 dict |

```python
for block in response.content:
    if block.type == "tool_use":
        tool_id = block.id
        tool_name = block.name
        tool_args = block.input  # dict，用 ** 展開
```

---

## 在對話歷史中保留完整 Content

Claude 是 stateless 的——歷史記錄由**你**管理。當 assistant 回傳 multi-block content 時，必須把**整個 `response.content` list** append 回去，不可以只留 text：

```python
messages.append({
    "role": "assistant",
    "content": response.content   # 保留所有 block，包含 ToolUseBlock
})
```

如果把它攤平成字串、或把 tool-use block 丟掉，下一次 API 呼叫就會壞掉：因為下一則 user message 裡的 `tool_result` 會引用一個已經不存在於歷史中的 `tool_use_id`，API 對這個配對非常嚴格。

---

## `stop_reason` 作為 Loop 信號

每個 response 除了 content list，還有 `stop_reason`。當 Claude 輸出 tool-use block 時，`stop_reason == "tool_use"`。這就是標準的信號，告訴你程式碼必須先去跑 tool、把結果送回來，才能拿到最終回答。其他常見值：`"end_turn"`（Claude 說完了）、`"max_tokens"`、`"stop_sequence"`。

---

## 升級 Helper Function 處理 Multi-Block

如果你之前寫的 helper 預設只處理純文字：

```python
# 舊版（純文字）——加 tools 後會壞
def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})
```

升級成接受字串或完整 `Message` 物件：

```python
from anthropic.types import Message

def add_assistant_message(messages, message):
    content = message.content if isinstance(message, Message) else message
    messages.append({"role": "assistant", "content": content})
```

這種多型處理在引入 tool 後是必要的——原本傳字串的呼叫點現在都要能處理 typed block list。

---

## 完整 Tool-Use 流程（單一回合）

1. 送 user message + `tools=[...]` schema list
2. 收到 assistant message，`content = [TextBlock, ToolUseBlock]`，`stop_reason="tool_use"`
3. 迭代 `response.content`，找出 `ToolUseBlock`，取出 `id`、`name`、`input`
4. 在本地執行真正的 function
5. append 一則 user message，裡面放一個 `tool_result` block，`tool_use_id` 對應剛才的 `id`
6. 再打一次 API（**仍然要帶 `tools=[...]`**），拿到最終的自然語言回答

每一步都依賴完整保留 block 結構——漏掉任何一塊整條鏈路就會斷。

---

## 常見錯誤

1. **把 `response.content` 當字串用**——啟用 tools 後它是 typed block 的 list，要用 `response.content[0].text` 或 iterate。
2. **存歷史時把 `ToolUseBlock` 丟掉**——下一回合的 `tool_result` 會引用不存在的 `id`，API 直接噴 400。
3. **假設一個回應只有一個 block**——Claude 可能同一回合送說明文字 + 多個 tool-use block。
4. **follow-up 呼叫忘了帶 `tools=[...]`**——即使你已經有 tool 結果，Claude 還是需要 schema 才能解析歷史中的 tool 引用。
5. **用 index（`content[1]`）抓 tool-use block**——Claude 可能省略 text block 或調換順序，永遠要 filter `block.type == "tool_use"`。

---

> **Key Insight**
>
> 只要你在 request 裡加 `tools=[...]`，就跨過了一條契約邊界：回應變成異質 block list、歷史必須精準保留 block 身份（特別是 `tool_use_id`）。原本假設「assistant content 是字串」的程式碼會悄悄壞掉，而且錯誤會在後續回合以看不懂的 400 出現。從第一天就把 helper 寫成能吃 `Message` 物件。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：理解 `TextBlock` vs `ToolUseBlock` 的差別，以及 `input_schema` 如何對應到 `ToolUseBlock.input`。
- **D1（Agentic Architecture）**：這一課是 agentic loop 的基礎——`stop_reason == "tool_use"` 是正式的延續信號。
- 考題常會給一段把 `response.content` 當字串處理的程式碼，問你哪裡會出錯。

---

## Flashcards

| 題目 | 答案 |
|------|------|
| 啟用 tools 後 `response.content` 是什麼型別？ | 一個 typed content block 的 list（`TextBlock`、`ToolUseBlock` 等） |
| `ToolUseBlock` 有哪四個欄位？ | `type`、`id`、`name`、`input` |
| 哪個 `stop_reason` 值代表 Claude 要呼叫 tool？ | `"tool_use"` |
| 為什麼必須把完整的 `response.content` append 到歷史，而不能只存 text？ | 因為下一個 `tool_result` 會引用 `ToolUseBlock.id`，那個 ID 必須存在於對話歷史中 |
| 如何安全地在 response 中找出 tool-use block？ | 用 `block.type == "tool_use"` 過濾，不要用 index |
| follow-up API 呼叫送 tool_result 時還需要帶 `tools=[...]` 嗎？ | 要——Claude 需要 schema 才能解析歷史中的 tool 引用 |
| 把 `ToolUseBlock.input` 展開成 keyword arguments 的 Python 語法？ | `my_function(**block.input)` |
| 如果 helper 把 `response.content` 攤平成字串會怎樣？ | 後續回合會壞掉，因為 `tool_result` 裡的 `tool_use_id` 在歷史中找不到對應 |
