# Agents 與 Tools — Engineering 深度解析

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture (22%) |
| Task Statements | 1.1 (agent 架構)、1.2 (agentic loop)、1.3 (agent 中的 tool use)、5.1 (production pattern 選型) |
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 81 |

---

## 一句話總結

Agent = Claude + 一組抽象、可組合的 tools,跑在 agentic loop 裡面;相較於 workflow 預先寫死的步驟順序,agent 讓 Claude 自己在執行時決定該呼叫哪些 tool、以什麼順序呼叫,以完成使用者給的目標。

---

## Workflow vs Agent:核心差異

Workflow 裡面,開發者把 tool 呼叫順序寫死在程式碼中:「先 A,再 B,再 C」。控制流是開發者擁有的。

Agent 裡面,你只給 Claude 一個目標 + 一個工具箱,控制流由 Claude 決定。同一份 agent 程式可以處理「現在幾點?」和「下週三早上七點提醒我去健身房」,你的 Python 程式碼裡完全沒有 if/else 分支。

```python
# Workflow:由開發者控制順序
def schedule_reminder(task, when):
    now = get_current_datetime()
    target = add_duration_to_datetime(now, when)
    return set_reminder(task, target)

# Agent:由 Claude 控制順序
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[get_current_datetime, add_duration_to_datetime, set_reminder],
    messages=[{"role": "user", "content": "下週三提醒我去健身房"}]
)
# Claude 自己決定:get_current_datetime -> add_duration_to_datetime -> set_reminder
```

---

## Datetime 範例 — Emergent Tool Chaining

三個簡單的 tools:

- `get_current_datetime` — 回傳目前日期時間
- `add_duration_to_datetime` — 回傳 `datetime + duration`
- `set_reminder` — 在指定時間建立提醒

看 Claude 怎麼把這三個 tool 組合成不同行為:

| 使用者要求 | Tool 序列 |
|------------|-----------|
| 「現在幾點?」 | `get_current_datetime` |
| 「11 天後是星期幾?」 | `get_current_datetime` -> `add_duration_to_datetime` |
| 「下週三提醒我去健身房」 | `get_current_datetime` -> `add_duration_to_datetime` -> `set_reminder` |
| 「我的 90 天保固什麼時候到期?」 | 先問使用者購買日期,再串接 tools |

這個 agent 並沒有被明確寫程式去辨認「下週三」或「90 天保固」——是 Claude 的推理能力把自然語言轉成正確的 tool 鏈。這叫做 **emergent composition**,也是 agent 存在的全部理由。

---

## 設計原則:抽象的 Tool 勝過專用的 Tool

在 agent 系統中,tool 設計的首要原則是:**選擇 primitive、抽象的 tool,不要選窄、專門的 tool**。Claude Code 是最佳示範:

| 有的 tool | 沒有的 tool |
|-----------|-------------|
| `bash`(執行任何 shell 指令) | `install_npm_dependency` |
| `read`(讀任何檔案) | `read_python_imports` |
| `write`(寫任何檔案) | `create_react_component` |
| `edit`(修改檔案) | `refactor_function` |
| `glob` / `grep` | `find_unused_variables` |

六個 primitive 讓 Claude 可以重構程式碼、安裝相依套件、跑測試、寫 migration、做 security audit——這些是 Claude Code 開發團隊從來沒明確規劃過的情境。如果換成 `refactor_function` 這種專用 tool,只能處理一種窄情境,其他場景全部失效。

**心法**:如果一個 tool 可以用 Unix 動詞描述,那它大概就在對的抽象層級。

---

## 設計可組合的 Tool Set

一個設計良好的 agent tool set,是少量可以 **組合** 的 primitive。舉例:social media video agent。

```python
tools = [
    {
        "name": "bash",
        "description": "執行 shell 指令,包括 FFMPEG 影片處理",
        "input_schema": {"type": "object", "properties": {"command": {"type": "string"}}}
    },
    {
        "name": "generate_image",
        "description": "從 text prompt 生成圖片",
        "input_schema": {"type": "object", "properties": {"prompt": {"type": "string"}}}
    },
    {
        "name": "text_to_speech",
        "description": "把文字轉成音訊檔",
        "input_schema": {"type": "object", "properties": {"text": {"type": "string"}, "voice": {"type": "string"}}}
    },
    {
        "name": "post_media",
        "description": "把媒體檔案上傳到社群平台",
        "input_schema": {"type": "object", "properties": {"file_path": {"type": "string"}, "platform": {"type": "string"}}}
    }
]
```

這組 tool 可以支援:

- 「發一部料理影片」-> image + TTS + bash(FFMPEG) + post_media
- 「先生個範例圖給我看,等我確認再繼續」-> image, 暫停等 feedback, 再繼續
- 「再好笑一點」-> 用不同的 prompt 重新生成

這些流程都沒有被寫死。它們是 agent 針對同一組四個 tool 推理出來的結果。

---

## Agentic Loop(Runtime 視角)

```python
messages = [{"role": "user", "content": user_goal}]
while True:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        tools=tools,
        messages=messages
    )
    messages.append({"role": "assistant", "content": response.content})

    if response.stop_reason == "end_turn":
        break

    if response.stop_reason == "tool_use":
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })
        messages.append({"role": "user", "content": tool_results})
```

這個 loop 就是 agent 的全部。你不需要預先決定會跑幾輪—— Claude 透過 `stop_reason == "end_turn"` 自己決定何時結束。

---

## 常見錯誤

1. **Tool 過度專用化** — 寫 `refactor_python_class` 而不是 `edit`。你用一個 work case 換來幾十個 broken case。
2. **沒有 loop 終止保護** — 讓 agent 無限跑下去。永遠要設最大迭代數(例如 25)避免失控的 cost。
3. **把 agent 當偽裝的 workflow 使用** — 如果你發現自己在寫 `if tool_name == X: 強制呼叫 Y`,那你要的是 workflow,不是 agent。
4. **Tool 描述太含糊** — Claude 只能選它看得懂的 tool。把描述寫得像在 onboard 新工程師一樣清楚。
5. **忘記 tool_results 是 user role 的訊息** — Anthropic API 裡,tool result 是用 `role: "user"` 送回去的,不是獨立的 role。

> **Key Insight**
>
> Agent 適合在「你沒辦法事先列出步驟」的情境。給 Claude 小、抽象、可組合的 tool 加上清楚的目標,然後讓 agentic loop 去組合。開發者的工作從「寫控制流」變成「設計對的工具箱」。

---

## CCA 考試關聯

- **D1 (Agentic Coding & Architecture)**:會考「agent 跟 workflow 差在哪」、「哪個 tool 設計支援 agent」。答案幾乎永遠是比較抽象的 primitive。
- **D5 (Enterprise Deployment)**:Agent 比較難做 eval 而且每個任務成本較高——這些 trade-off 要記住。
- 題目裡看到這些關鍵字:「unpredictable requests」「varied tasks」「creative combination」-> agent;「known sequence」「repeatable」「reliable」-> workflow。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Agent 跟 workflow 最關鍵的差別是什麼? | Workflow 裡開發者把 tool 順序寫死;Agent 裡 Claude 在 runtime 根據目標決定 tool 順序。 |
| 為什麼 agent tool 要設計成抽象而不是專用? | 抽象 tool(bash、read、edit)可以組合出開發者從沒預期的情境;專用 tool(refactor_function)只對一種情境有效。 |
| 舉三個 Claude Code 的 primitive tool。 | bash、read、write、edit、glob、grep(任選三個)。 |
| Agent 收到「我的 90 天保固什麼時候到期?」會怎麼處理? | 它會辨識出缺少資訊,先問使用者購買日期,然後串接 get_current_datetime 和 add_duration_to_datetime。 |
| 哪個 stop_reason 表示 agent 想呼叫 tool? | `tool_use` |
| 哪個 stop_reason 表示 agentic loop 該結束? | `end_turn` |
| 在 Anthropic API 裡,tool_result content block 是用哪個 role 送回給 Claude? | `user` |
| 每個 production agent loop 都該有什麼保護? | 最大迭代數限制,避免失控的 cost 和無限迴圈。 |
