# 使用多個 Tools — Engineering Deep Dive

| 項目 | 內容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%)、D1 — Agentic Architecture (22%) |
| Task Statements | 2.1（tool schema 與選擇）、1.2（tool 編排）、2.4（多輪 tool loop） |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 40 |

---

## One-Liner

Claude 可以在單一對話中自行選擇並串接多個 tools；只要已經建立好核心的 tool-handling 基礎架構（schema 列表 + router 函式），新增 tool 就是一個簡單的四步驟模式，成本隨 tool 數量線性成長。

---

## 核心模式

從單一 tool 擴展到多個 tools，只需要每個新 tool 做四件事：

1. 實作 Python 函式
2. 定義 JSON schema
3. 將 schema 加入 `tools=[...]` 列表
4. 在 tool router 加上 `elif` 分支

外層的 agentic loop 完全不需要改動。既有的 `stop_reason == "tool_use"` 判斷與 message 累積邏輯都繼續有效。

---

## 範例：三個 tool 的提醒 Agent

```python
tools = [
    get_current_datetime_schema,
    add_duration_to_datetime_schema,
    set_reminder_schema,
]

def run_tool(tool_name: str, tool_input: dict):
    if tool_name == "get_current_datetime":
        return get_current_datetime(**tool_input)
    elif tool_name == "add_duration_to_datetime":
        return add_duration_to_datetime(**tool_input)
    elif tool_name == "set_reminder":
        return set_reminder(**tool_input)
    else:
        raise ValueError(f"未知的 tool: {tool_name}")

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    messages=messages,
)
```

Router 本質上是一個 dispatch table；當 tool 數量超過 5 個時，建議改用 dict registry：

```python
TOOL_REGISTRY = {
    "get_current_datetime": get_current_datetime,
    "add_duration_to_datetime": add_duration_to_datetime,
    "set_reminder": set_reminder,
}

def run_tool(tool_name, tool_input):
    return TOOL_REGISTRY[tool_name](**tool_input)
```

---

## Claude 如何選擇 Tool

當列表中有多個 tools 時，Claude 會讀取每個 schema 的 `name` 與 `description`，並依據對話脈絡判斷要呼叫哪個（或不呼叫）。選擇因素包括：

- **Description 品質** — 清晰、動作導向的描述勝過模糊描述
- **輸入參數名稱** — 命名清楚的參數降低歧義
- **使用者請求的用字** — 「提醒我」明顯對應到 `set_reminder`
- **鏈式依賴** — 如果某 tool 需要的資料還沒有，Claude 可能會先呼叫另一個 tool 取得

這就是為什麼 tool description 的重要性跟實作本身一樣高。

---

## 串接呼叫與 Agentic Loop

範例 prompt：*「幫我設定看醫生的提醒，在 2050 年 1 月 1 日之後的第 177 天。」*

Claude 通常會跨多輪產生多個 tool_use block：

1. **Turn 1** — Claude 發出 `add_duration_to_datetime(start="2050-01-01", days=177)` 的 `tool_use`
2. **你的程式碼**執行函式、回傳 `"2050-06-27"` 為 `tool_result`
3. **Turn 2** — Claude 收到結果，發出 `set_reminder(date="2050-06-27", description="doctor appointment")`
4. **你的程式碼**執行函式、回傳確認訊息
5. **Turn 3** — Claude 發出最後的 `text` block，總結執行內容

Agent loop 會持續呼叫 API，直到 `stop_reason != "tool_use"`。

---

## Parallel vs. Sequential Tool Calls

單一 assistant message **可以同時包含多個 tool_use block（parallel）**，只要這些 tool 彼此獨立。例如使用者問「東京天氣是多少，還有 AAPL 現在股價？」，Claude 可能在同一個 response 中同時發出 `get_weather` 與 `get_stock_price`。你必須執行每一個，並在**單一 user message** 中一次回傳**所有** `tool_result` block。

```python
# 從 assistant turn 收集所有 tool_use block
tool_uses = [b for b in response.content if b.type == "tool_use"]

# 執行並建立 tool_result block
tool_results = [
    {
        "type": "tool_result",
        "tool_use_id": tu.id,
        "content": str(run_tool(tu.name, tu.input)),
    }
    for tu in tool_uses
]

# 在單一 user message 中送出所有結果
messages.append({"role": "user", "content": tool_results})
```

相對地，Sequential chaining（Tool A 的結果餵給 Tool B）需要多次 API 來回，會以多個 turn 的形式累積在 `messages` 中。

---

## Multi-Tool 請求的 Message 結構

多 tool 請求的對話歷史如下：

```
user:      「177 天後設提醒」
assistant: [text「我得先算日期」] + [tool_use add_duration_to_datetime]
user:      [tool_result "2050-06-27"]
assistant: [text「現在設定提醒」] + [tool_use set_reminder]
user:      [tool_result "已設定"]
assistant: [text「完成，提醒排定在 2050 年 6 月 27 日」]
```

注意 assistant message 可以同時包含 text block 與 tool_use block。重播歷史時**不要把 text block 拿掉** — Claude 會將它們當作推理的脈絡。

---

## Common Mistakes

1. **忘記註冊 schema** — 函式與 router case 都寫好了，但忘了加進 `tools=[...]` 列表，Claude 永遠不知道這個 tool 存在。
2. **Router 對未知 tool 靜默忽略** — 遇到未知 name 應該直接 raise，讓 schema 拼字錯誤立刻浮現，而不是靜默回傳 `None`。
3. **Claude 同時發多個 parallel tool_use，但只回了一個 tool_result** — API 會回錯，因為 tool_use_id 集合對不上。
4. **把 assistant message 的 text block 丟掉** — assistant 的 content 是 block list，加入歷史時要保留所有 block。
5. **Tool description 太模糊** — 「helper tool」「utility」這類描述會讓 Claude 選錯 tool，應該寫動作導向的描述：「Adds a duration in days to a starting datetime」。

> **Key Insight**
>
> N 個 tool 的 agentic loop 與 1 個 tool 的 loop 完全相同。只要 `stop_reason == "tool_use"` 處理正確，擴展純粹就是註冊更多 schema 與 dispatch case。架構成本是固定的，唯一的變動成本是寫出高品質的 tool description。

---

## CCA Exam Relevance

- **D2 (Tool Design)**：理解 Claude 如何根據 schema 與 description 在多個 tool 之間做選擇，常出現 tool dispatch 的題型。
- **D1 (Agentic Architecture)**：辨識 parallel tool_use 的情境，並知道必須在單一 user turn 內回傳所有 tool_result。
- **Task 2.4（多輪 tool loop）**：追蹤鏈式 tool-use 序列並指出 loop 在哪裡終止，是常見的題目類型。

---

## Flashcards

| Front | Back |
|-------|------|
| 新增一個 tool 到 multi-tool agent 的四步驟？ | 1) 實作函式 2) 定義 schema 3) 加入 tools 列表 4) 加上 router case |
| Claude 如何在多個 tool 之間做選擇？ | 依據每個 tool 的 name、description、參數名稱以及當前對話脈絡 |
| 單一 assistant message 可以包含多個 tool_use block 嗎？ | 可以，parallel 呼叫會以多個 tool_use block 的形式出現在同一個 response，必須在單一 user message 中全部回覆 |
| 每個回傳的 tool_result 必須附帶什麼？ | 對應 assistant tool_use block 的 `tool_use_id` |
| Agentic loop 什麼時候停止？ | 當 `stop_reason` 不再是 `"tool_use"`（通常變成 `"end_turn"`） |
| 為什麼要保留 assistant turn 的 text block？ | Claude 會將它們當作推理的脈絡，刪掉會讓後續輪次變差 |
| 大型 `if/elif` router 的可擴展替代方案？ | 用 dict 建立 tool registry，將 name 對應到 callable |
| Tool description 過於模糊有什麼風險？ | Claude 可能選錯 tool 或誤用，導致錯誤的 tool 呼叫 |
