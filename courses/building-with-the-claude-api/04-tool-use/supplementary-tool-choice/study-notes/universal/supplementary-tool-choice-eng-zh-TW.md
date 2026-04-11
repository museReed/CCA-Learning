# Tool Choice 參數 — 工程深度解析

| 項目 | 內容 |
|------|------|
| 考試範圍 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| 任務陳述 | 2.1（tool schema 設計）、2.2（content blocks）、1.2（agentic loop 控制） |
| 來源 | 補充教材 — 填補 building-with-the-claude-api / 04-tool-use 的課程空缺 |

---

## 一句話總結

`tool_choice` 是 Claude 工具呼叫行為的方向盤 — 讓你宣告 Claude 在這一輪「可以」、「必須」或「不可以」呼叫工具，並可選擇性指定要呼叫哪一個工具。

---

## 四種模式

| 模式 | 語法 | 行為 | `stop_reason` |
|------|------|------|---------------|
| `auto` | `{"type": "auto"}` | **預設值。** Claude 自行決定是否呼叫工具。回應可能是 TextBlock（對話）或 ToolUseBlock。 | `end_turn` 或 `tool_use` |
| `any` | `{"type": "any"}` | Claude 必須呼叫其中一個提供的工具，由它自己挑選。回應一定是 ToolUseBlock。 | `tool_use` |
| `tool` | `{"type": "tool", "name": "get_weather"}` | 強制 Claude 呼叫某個指定名稱的工具。 | `tool_use` |
| `none` | `{"type": "none"}` | 停用本輪的工具呼叫；Claude 只會以純文字回應。 | `end_turn` |

### `auto` — 讓 Claude 決定

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "auto"},  # 等同於省略 tool_choice
    messages=messages,
)
```

最適合通用 agent 與聊天介面。Claude 決定要呼叫工具時，會先產出自然的 chain-of-thought 推理文字，讓你看得到它的思路。

### `any` — Claude 必須呼叫某個工具

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "any"},
    messages=messages,
)
# response.content[0].type == "tool_use" — 保證成立
```

最適合每一輪都必須產出結構化動作的工作流。Claude 仍然會根據訊息自行挑工具，但無法逃逸到純文字回應。

### `tool` — 強制使用特定工具

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "tool", "name": "extract_invoice"},
    messages=messages,
)
```

最適合結構化資料抽取 — 該工具的 `input_schema` 就變成一份有型別的輸出契約。這是 Claude API 中最接近「JSON mode」的慣用做法。

### `none` — 本輪停用工具

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,  # 仍然宣告
    tool_choice={"type": "none"},
    messages=messages,
)
```

在 agent loop 裡面很好用 — 當你想讓 Claude 總結、反思，或在所有工具結果都蒐集完畢後產出最終給使用者看的文字時，用這個模式阻止它又去呼叫工具。

---

## 與 `stop_reason` 的交互

tool_choice 模式會直接決定你必須處理哪些 `stop_reason`：

| 模式 | 可能的 `stop_reason` | 你的程式碼必須處理的分支 |
|------|----------------------|--------------------------|
| `auto` | `end_turn`、`tool_use`、`max_tokens`、`stop_sequence` | 兩大分支：純文字回應 vs 工具呼叫 |
| `any` | `tool_use`（加上 `max_tokens` 邊界情況） | 單一分支：永遠執行工具 |
| `tool` | `tool_use`（加上 `max_tokens` 邊界情況） | 單一分支：永遠執行被強制的工具 |
| `none` | `end_turn`、`max_tokens`、`stop_sequence` | 單一分支：只有純文字回應 |

這對 loop 控制很重要。使用 `auto` 時，你的 agent loop 在 `end_turn` 時退出。使用 `any` 時，loop 只能透過切換到 `auto` 或 `none`，或是你的程式碼根據工具結果判定為終止狀態來中止。

---

## `disable_parallel_tool_use`

```python
tool_choice={"type": "any", "disable_parallel_tool_use": True}
```

預設情況下，Claude 在單次回應中可以發出多個 `tool_use` block（parallel tool use）。設為 `disable_parallel_tool_use: true` 會強制**每輪最多只能有一個** `tool_use` block。

- 與 `any` 或 `tool` 搭配，適合需要嚴格「一次一個動作」的場景（狀態機、交易型流程）。
- 與 `auto` 搭配也合法 — 當你的執行器無法安全地並行呼叫工具時很有用。
- 代價：失去了並行呼叫帶來的延遲優勢。

---

## 何時用哪個模式 — 決策指南

```
有時需要即時資料、有時純聊天？              → auto
每一輪都必須產出結構化動作？                  → any
從非結構化輸入中抽取有型別資料？              → tool（指定名稱）
Agent loop 中的總結／反思輪？                 → none
嚴格一次一個動作的狀態機？                    → any + disable_parallel_tool_use
```

---

## 常見錯誤

1. **在聊天 agent 上用 `any`** — 會在每一輪都強制工具呼叫，包含「你好」「謝謝」這種閒聊，產出毫無意義的 tool_use block。
2. **預期 `tool` 或 `any` 模式會產出 chain-of-thought** — 當 Claude 被強制呼叫工具時，不會在 tool_use block 之前輸出推理文字，你會失去可觀察性。只有 `auto` 允許自然的 CoT。
3. **忘了 `none` 模式仍然需要宣告 `tools=`** — 工具清單還是要帶；`none` 只是停用本輪的呼叫行為。
4. **以為 `auto` 在有工具可用時一定會呼叫** — `auto` 代表 Claude 可以「選擇不呼叫」。如果你的使用情境一定要呼叫工具，請用 `any` 或 `tool`。
5. **執行器不支援並行時沒設 `disable_parallel_tool_use`** — Claude 可能同時發出兩個 tool_use block，你的序列式執行器會卡死或造成狀態重複套用。

---

> **關鍵洞察**
>
> `tool_choice` 是你把 Claude 從「對話助理」轉換成「確定性元件」的開關。`auto` 把方向盤交給 Claude（彈性、推理透明）；`any`/`tool` 把方向盤交回給你的程式碼（結構化、保證動作，但推理不透明）。選對模式是在「彈性」與「控制」之間做 trade-off — 而這個 trade-off 正是 CCA D1（agent 設計）與 D2（tool 設計）的核心。

---

## CCA 考試相關性

- **D2（Tool Design & MCP Integration）**：四種模式的語法、行為與使用時機都是直接可考的。預期會看到「哪個 `tool_choice` 設定能保證 Claude 會呼叫工具？」這類題目。
- **D1（Agentic Architecture）**：`tool_choice` 控制 loop 的終止與結構。用 `none` 做總結輪、用 `any` 做動作輪是核心的 agent pattern。
- **陷阱題**：考題可能描述一個「JSON 抽取」情境 — 正確答案是 `{"type": "tool", "name": "..."}`，不是 `any`，也不是靠 prompt 技巧。

---

## 快閃卡

| 正面 | 背面 |
|------|------|
| `tool_choice` 的預設值是什麼？ | `{"type": "auto"}` — Claude 自行決定是否呼叫工具。 |
| 哪個 `tool_choice` 模式能保證 Claude 會呼叫工具？ | `{"type": "any"}` — Claude 必須從提供的工具中挑一個。 |
| 如何強制 Claude 呼叫某個指定名稱的工具？ | `{"type": "tool", "name": "<tool_name>"}` |
| `{"type": "none"}` 的作用是什麼？ | 停用本輪的工具呼叫；Claude 只會以純文字回應，`stop_reason` 為 `end_turn`。 |
| 哪個模式會保留 Claude 在工具呼叫前的 chain-of-thought 推理？ | 只有 `auto`。`any` 與 `tool` 會抑制推理文字，直接輸出 tool_use block。 |
| `tool_choice: auto` 下可能的 `stop_reason` 有哪些？ | `end_turn`（文字回應）或 `tool_use`（工具呼叫）。 |
| `disable_parallel_tool_use: true` 強制了什麼？ | 每輪最多只能有一個 `tool_use` block，即使 Claude 本來可以並行呼叫多個工具。 |
| 什麼時候會在 agent loop 中使用 `tool_choice: none`？ | 在所有工具結果都收集完後的總結／反思輪，強制產出最終文字答案。 |
| 為什麼 `any` 不適合通用聊天 agent？ | 它會在每一輪都強制工具呼叫，連閒聊都會產出毫無意義的 tool_use block。 |
| Claude API 中最接近「JSON mode」的 `tool_choice` 模式是哪個？ | `{"type": "tool", "name": "..."}` — 工具的 `input_schema` 就是有型別的輸出契約。 |
