# 介紹 Tool Use — Engineering Deep Dive

| 項目 | 內容 |
|------|------|
| 考試 Domain | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 1.2（agentic loop 基礎）、2.1（tool schema 設計）、2.4（multi-turn tool loop） |
| 來源 | building-with-the-claude-api / 04-tool-use / Lesson 32 |

---

## 一句話總結

Tool use 是一套結構化的 request/response 協定,讓 Claude 能主動請求你的應用程式去抓取外部資料或執行動作,補上訓練資料與即時世界之間的落差。

---

## 沒有 Tools 時的問題:靜態知識的邊界

沒有 tools,Claude 就被訓練截止日期綁死。使用者問「舊金山現在天氣如何?」時,只會得到:

> 「抱歉,我沒辦法取得最新的天氣資訊。」

這是能力的牆,不是 prompt 寫不好的問題。再怎麼調 prompt 也變不出訓練資料裡沒有的即時資訊。同樣的牆出現在:

- 即時股價、賽事比分、新聞頭條
- 公司內部資料庫與 CRM 記錄
- 使用者個人狀態(行事曆、檔案、偏好)
- 任何需要真實世界副作用的操作(寄信、寫檔案、觸發 workflow)

Tools 是架構面的答案:與其用 prompt 繞過限制,不如透過結構化的方式**擴展** Claude 的能力,讓它可以向你的程式碼求助。

---

## Tool Use 的四步驟流程

```
┌──────────┐   1. 使用者問題 + 工具定義           ┌─────────┐
│  Client  │ ─────────────────────────────────▶ │ Claude  │
│  (app)   │                                     │   API   │
│          │ ◀──────────────────────────────────│         │
│          │   2. tool_use request (name + args) └─────────┘
│          │
│          │   3. 本地執行 function
│          │
│          │   4. tool_result 帶回結果           ┌─────────┐
│          │ ─────────────────────────────────▶ │ Claude  │
│          │ ◀──────────────────────────────────│   API   │
│          │   5. 最終自然語言回覆                └─────────┘
└──────────┘
```

1. **初始請求** — 把使用者問題加上可用工具清單(name、description、input_schema)POST 到 `/v1/messages`。
2. **工具請求** — Claude 的 `stop_reason` 回 `"tool_use"`,`content` 裡會有 `tool_use` block,包含 `id`、`name`、`input`(JSON 參數)。
3. **本地執行** — 你的伺服器讀 tool_use block,呼叫對應的 Python function,拿到結果。
4. **最終回覆** — 把 assistant 訊息與一則新的 user 訊息(含 `tool_result` block,用 `tool_use_id` 對應)附加進去,再呼叫一次 API。Claude 綜合所有資訊產生最終答案。

---

## 最小可行 Python 範例

```python
from anthropic import Anthropic

client = Anthropic()

tools = [{
    "name": "get_weather",
    "description": "回傳指定城市的目前天氣。",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "城市名稱,例如 San Francisco"}
        },
        "required": ["city"]
    }
}]

messages = [{"role": "user", "content": "舊金山現在天氣怎樣?"}]

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    messages=messages,
)

if response.stop_reason == "tool_use":
    tool_use = next(b for b in response.content if b.type == "tool_use")
    result = fetch_weather(tool_use.input["city"])  # 你的 function

    messages.append({"role": "assistant", "content": response.content})
    messages.append({
        "role": "user",
        "content": [{
            "type": "tool_result",
            "tool_use_id": tool_use.id,
            "content": result,
        }],
    })

    final = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )
    print(final.content[0].text)
```

核心觀念:**tool use 是 multi-turn**。一個使用者問題通常會橫跨兩次(以上)API 呼叫。

---

## 為什麼 Tools 比 Fine-tune 更適合即時資料

| 方式 | 新鮮度 | 成本 | 維運 |
|------|--------|------|------|
| Fine-tune 最新資料 | 數小時到數天 stale | 高(retrain) | 持續 retrain |
| RAG(vector search) | 看 index 更新頻率 | 中(embedding + 儲存) | 需維護 index pipeline |
| **Tool use** | 即時 — 直接打 live source | 按次計費 | 零 — source of truth 在上游 |

Tools 是唯一一種讓 Claude 直接讀取系統真實來源的模式。不快取、不過期。

---

## 關鍵優勢

- **即時資訊** — 取得訓練資料裡沒有的最新資料
- **外部系統整合** — 串接資料庫、SaaS API、內部服務
- **動態回應** — 每次答案都奠基於最新狀態
- **結構化互動** — Claude 透過 `input_schema` 明確宣告它要什麼
- **可執行動作** — tools 不只讀取,還能寫入,這是 Claude 變成 agent 的關鍵

---

## 常見錯誤

1. **忘了第二次 API 呼叫** — 把 `tool_use` block 直接回給使用者,沒有實際執行並把結果送回 Claude。
2. **`tool_use_id` 對不上** — `tool_result` 必須引用原始 `tool_use` 的 `id`,否則 Claude 會斷開 context。
3. **用字串傳遞 assistant 訊息** — assistant message 的 `content` 必須保留完整陣列,不可壓成純文字。
4. **以為 tools 是可有可無** — 需要即時資料時,沒有 prompt engineering 的替代方案,只能用 tools。
5. **沒處理 `stop_reason`** — 要分支判斷是否進入下一輪 loop,或直接回最終答案。

> **Key Insight**
>
> Tool use 不是單次 API call,而是**一個 loop**。每一輪檢查 `stop_reason`,若是 `tool_use` 就本地執行、附上 `tool_result`,再呼叫一次 API。這個 loop 是 CCA 整個 agentic 章節的基礎。搞懂它就同時解鎖 D1(agents)與 D2(tool design)。

---

## CCA 考試重點

- **D2(Tool Design & MCP Integration)**:tool_use request/response 流程、`tool_use` 與 `tool_result` block 類型、`input_schema` 即為 JSON Schema。
- **D1(Agentic Architecture)**:tool use 這個 loop 就是最小的 agentic loop。Multi-turn tool call 就是更複雜 agent pattern 的起點。
- 考題常見情境:「Claude 需要即時天氣」→ 答案永遠是 tools,不是 prompt engineering。

---

## Flashcards

| Front | Back |
|-------|------|
| Tool use 解決什麼問題? | Claude 訓練截止的限制 — 讓它能取得即時資料與外部系統,補上模型原本不知道的資訊。 |
| 哪個 `stop_reason` 代表 Claude 想呼叫工具? | `"tool_use"` |
| Claude 要求工具時會回什麼 content block? | `tool_use` block,含 `id`、`name`、`input`(JSON 參數)。 |
| 你的 app 如何把工具結果回傳給 Claude? | 送一則新的 user message,裡面放 `tool_result` block,用 `tool_use_id` 對應原 tool_use。 |
| 一次 tool use round trip 最少要幾次 API call? | 至少兩次 — 一次收 tool_use 請求,一次送 tool_result 拿最終答案。 |
| Tool use 的四個步驟是? | 1) 初始請求帶 tools,2) Claude 回 tool_use,3) 本地執行,4) 回 tool_result,Claude 產出最終答案。 |
| 為何 prompt engineering 取代不了 tools 的即時資料需求? | 因為那些資料從來沒在訓練資料裡 — 再怎麼 prompt 都生不出來。 |
| Tools 能有副作用嗎? | 可以 — tools 能讀(天氣 API)也能寫(寄信、建立記錄),這正是 Claude 變成 agent 的關鍵。 |
