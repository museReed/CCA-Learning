# Implementing Multiple Turns — Engineering Deep Dive（繁中）

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture (22%) / D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 1.2（agentic loop 實作）、2.4（multi-turn tool loops）、1.3（multi-turn 對話管理） |
| 來源 | building-with-the-claude-api / 04-tool-use / Lesson 39 |

---

## 一句話總結

Agentic loop 就是一個 `while True`：呼叫 Claude、檢查 `response.stop_reason != "tool_use"` 就 break，否則執行每一個 `tool_use` block、把每個結果包成 `tool_result` block、再 loop 一次。

---

## 標準 Agentic Loop

這就是整個 agentic 生態系建立其上的那個 pattern：

```python
def run_conversation(messages):
    while True:
        response = chat(messages, tools=[get_current_datetime_schema])
        add_assistant_message(messages, response)
        print(text_from_message(response))

        if response.stop_reason != "tool_use":
            break

        tool_results = run_tools(response)
        add_user_message(messages, tool_results)

    return messages
```

**每次迭代五個步驟：**

1. 用目前的歷史和 tool schema 呼叫 Claude
2. 把完整的 assistant message append 到歷史
3. 把 text block 秀給使用者（進度指示）
4. 檢查 `stop_reason`——不是 `"tool_use"` 就 break
5. 執行所有 tool-use block，把結果以 user message 的形式 append 回去

Loop 會在 `stop_reason` 不是 `"tool_use"` 時結束——通常是 `"end_turn"`，但也可能是 `"max_tokens"` 或 `"stop_sequence"`。

---

## `stop_reason` 是權威信號

Response 上的 `stop_reason` 是**唯一**可靠的信號，用來判斷 Claude 還想不想用 tool：

| `stop_reason` 值 | 意思 | Loop 動作 |
|-----------------|------|-----------|
| `"tool_use"` | Claude 想跑一或多個 tool | 執行並 loop |
| `"end_turn"` | Claude 已經完成答案 | Break，回傳最終回應 |
| `"max_tokens"` | 撞到輸出長度上限 | Break，警告使用者，可能要加 token 重試 |
| `"stop_sequence"` | 比對到 stop sequence | Break |

不要試著從 block 內容推斷。Claude 可以同一回合送出 text block **和** tool-use block；靠「response 裡有 text 所以應該結束了」是經典 bug。

---

## `run_tools`——過濾再執行

`run_tools` 走訪 response content，挑出 `tool_use` block，執行每一個，並回傳一個 `tool_result` block 的 list：

```python
import json

def run_tools(message):
    tool_requests = [
        block for block in message.content if block.type == "tool_use"
    ]
    tool_result_blocks = []

    for tool_request in tool_requests:
        try:
            tool_output = run_tool(tool_request.name, tool_request.input)
            tool_result_blocks.append({
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": json.dumps(tool_output),
                "is_error": False
            })
        except Exception as e:
            tool_result_blocks.append({
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": f"Error: {e}",
                "is_error": True
            })

    return tool_result_blocks
```

這個 function 保留兩個不變式：

1. **每個 tool-use block 都有對應的 result block**（即使失敗也有）
2. **`tool_use_id` 精準回填**，讓 API 能配對請求和回應

---

## `run_tool`——可擴充的 Tool Routing

`run_tool` 把 tool name 對應到實際 function。最簡單是 `if/elif`，但 production 系統通常用 dict-based registry：

```python
TOOL_REGISTRY = {
    "get_current_datetime": get_current_datetime,
    "add_duration_to_datetime": add_duration_to_datetime,
    # 這裡註冊更多 tool
}

def run_tool(tool_name, tool_input):
    if tool_name not in TOOL_REGISTRY:
        raise ValueError(f"Unknown tool: {tool_name}")
    return TOOL_REGISTRY[tool_name](**tool_input)
```

Registry pattern 讓「加新 tool」變成純資料改動——不用動 loop 邏輯本身。搭配 `run_tools`，你就有一個能擴展到幾十個 tool 而不用重寫結構的 agent。

---

## Loop 內的錯誤處理

Lesson 強調**tool 層**要做好錯誤處理，而不是 loop 層。當 tool 噴例外：

1. 在 `run_tools` 裡面 catch 住
2. 建一個 `tool_result` block，`is_error=True`，錯誤字串放 `content`
3. 繼續 loop——讓 Claude 決定下一步

Claude 處理錯誤的能力很強：它可能用修正後的參數重試、換別的 tool、或把失敗回報給使用者。你程式的工作只是忠實地把「發生什麼事」傳達出來。

**不要**試著隱藏錯誤或跳過失敗的 block——那會破壞 `tool_use_id` 配對不變式，API 直接 400。

---

## 完整工作流程

```
┌────────────────────────────────┐
│ 使用者送出問題                    │
└──────────────┬─────────────────┘
               ▼
┌────────────────────────────────┐
│ chat(messages, tools=[...])    │◀───────────┐
└──────────────┬─────────────────┘            │
               ▼                              │
┌────────────────────────────────┐            │
│ add_assistant_message          │            │
│ print text_from_message        │            │
└──────────────┬─────────────────┘            │
               ▼                              │
         stop_reason                          │
        == "tool_use"?                        │
        /           \                         │
       否            是                       │
       ▼              ▼                       │
   ┌───────┐   ┌───────────────┐              │
   │ break │   │ run_tools     │              │
   └───────┘   │ (exec + wrap) │              │
               └──────┬────────┘              │
                      ▼                       │
               ┌──────────────────┐           │
               │ add_user_message │           │
               │ (tool_results)   │───────────┘
               └──────────────────┘
```

每次迭代嚴格交替 assistant/user message。歷史會一直成長，直到 Claude 收斂到最終答案。

---

## 常見錯誤

1. **用 `block.type == "tool_use"` 檢查取代 `stop_reason`**——平常會動，但如果 Claude 送了你不想執行的 tool_use block 就會壞
2. **執行 tool 前忘了 append assistant message**——會破壞歷史順序，下次 API 呼叫會被拒
3. **回傳錯誤數量的 `tool_result` block**——每個 `tool_use` 都要對應一個 result，失敗也要
4. **每次 loop 沒帶 `tools=[...]`**——Claude 需要 schema 才能解析歷史中的 tool 引用
5. **把可以平行的 tool 串行跑**——IO-bound 的 tool 用 `asyncio.gather` 或 thread pool 可以大幅降延遲
6. **沒有 max iterations**——搞混的 Claude 會無限 loop 燒 token，永遠要加上限

---

> **Key Insight**
>
> Agentic loop 出奇地小——大概 15 行 Python——但它是所有 agent framework（LangChain、AutoGPT、Claude Code、MCP client）的原子單位。掌握這個 pattern，你就懂所有 tool-using agent 的運作原理。信號永遠是 `stop_reason != "tool_use"`；動作永遠是「執行 tool 並 loop」。其他都是 production hardening：平行化、快取、觀測性、迭代上限。

---

## CCA Exam Relevance

- **D1（Agentic Architecture）**：這就是 THE agentic loop。`stop_reason` 檢查和 loop 結構一定會考好幾題。
- **D2（Tool Design & MCP Integration）**：理解 `run_tools` 如何過濾 block 並建 `tool_result` block。
- 主要考試情境：「怎麼知道何時停止 loop」、「tool 中途失敗怎麼辦」、「一個 response 多個 tool 呼叫怎麼處理」。

---

## Flashcards

| 題目 | 答案 |
|------|------|
| 退出 agentic loop 的確切條件是什麼？ | `response.stop_reason != "tool_use"`——不是 tool_use 就 break |
| `run_tools` 做什麼？ | 過濾 content 中的 `tool_use` block、用 `run_tool` 執行每一個、回傳 `tool_result` block 的 list |
| `run_tools` 怎麼處理例外？ | Catch 住、建一個 `is_error=True`、錯誤訊息在 `content` 的 `tool_result` block，繼續 loop |
| 為什麼要用 `TOOL_REGISTRY` dict 而不是 if/elif？ | 可擴充 routing——加新 tool 變成資料改動而非邏輯改動 |
| 把 `tool_input` dict 展開成 function keyword arguments 的 Python 語法？ | `tool_function(**tool_input)` |
| 如果 `tool_result` block 比 `tool_use` block 少會怎樣？ | API 會 400，說 `tool_use_id` 配對少了 |
| 為什麼 `add_assistant_message` 要在執行 tool 之前？ | 保持歷史順序——assistant message 必須先存在，user tool-result message 才能引用它 |
| Production agentic loop 必須加的最低限度安全機制是什麼？ | `max_iterations` 上限，防止 Claude 失控產生無限 loop |
