# Routing Workflows — 工程深度解析

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture(22%)— 主要 |
| 任務陳述 | 1.2(agentic 模式 — routing)、5.2(production workflow 部署)|
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 80 |

---

## 一句話總結

Routing workflow 用一個分類器 LLM 呼叫(通常搭配 `tool_choice="tool"` 強制工具呼叫)把進來的請求分類,再分派到專用下游 pipeline — 它是 LLM workflow 版的「switch statement」。

---

## Routing 解決的問題

通用 prompt 處理多樣化輸入時表現不佳。課程範例:一個社群媒體腳本生成器,要同時處理「Python functions」(教育類)和「surfing」(娛樂類)。單一 script prompt 對兩者都產出普通結果。解法是先分類,再分派到特定類別的 prompt。

Anthropic 在「Building Effective Agents」中描述 routing 的適用時機:當複雜任務有明顯類別,每類都能因為專用處理而受益,*並且*分類可以被 LLM 或確定性演算法準確完成。

---

## 標準兩步結構

```
使用者輸入 ──→ [分類器 LLM 呼叫] ──→ 類別 ──→ [專用 pipeline] ──→ 輸出
```

1. **分類** — 把使用者請求送給 Claude,附帶預定義類別清單,要求回傳一個類別標籤
2. **專用處理** — 用回傳的類別查出對應的 prompt template / tool set / 子 workflow,再產出最終輸出

核心觀念:使用者輸入只會進*一個*專用 pipeline,不是全部。每個 pipeline 可以獨立最佳化。

---

## 範例類別(課程)

| 類別 | 風格 |
|------|------|
| Entertainment | 高能量、有文化梗、用流行語 |
| Educational | 清楚吸引人的解釋搭配易懂例子 |
| Comedy | 犀利意外的內容,聰明觀察與節奏 |
| Personal vlog | 真誠親密的對話式敘事 |
| Reviews | 果斷、基於體驗,強調優缺點 |
| Storytelling | 沉浸式,用鮮活細節與情感連結 |

每個類別有自己的專用 prompt,routing 挑對的那個。

---

## 課程的分類 Prompt

```
Categorize the topic of a video into one of the listed categories:
<topic>Python functions</topic>

<categories>
- Educational
- Entertainment
- Comedy
- Personal vlog
- Reviews
- Storytelling
</categories>
```

Claude 回 "Educational",你的程式碼就去挑教育類 prompt template。

---

## 用 `tool_choice="tool"` 強制分類

Production 場景中,分類器應該回*結構化*類別,而不是自由文字再自己 parse。CCA 會考的關鍵技巧是用 tool use 並設 `tool_choice` 強制呼叫特定 tool:

```python
from anthropic import Anthropic

client = Anthropic()

ROUTE_TOOL = {
    "name": "route_request",
    "description": "把使用者請求 route 到專用內容 pipeline。",
    "input_schema": {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "enum": ["Educational", "Entertainment", "Comedy",
                         "Personal vlog", "Reviews", "Storytelling"],
                "description": "這個主題的內容類別。"
            },
            "confidence": {
                "type": "number",
                "description": "分類器信心值,0.0 到 1.0。"
            }
        },
        "required": ["category", "confidence"]
    }
}

def classify(topic: str) -> dict:
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        tools=[ROUTE_TOOL],
        tool_choice={"type": "tool", "name": "route_request"},  # 強制
        messages=[{"role": "user",
                   "content": f"Categorize the topic: {topic}"}],
    )
    for block in resp.content:
        if block.type == "tool_use" and block.name == "route_request":
            return block.input  # {"category": "...", "confidence": ...}
    raise RuntimeError("分類器沒呼叫 route_request tool")
```

為什麼 `tool_choice={"type": "tool", "name": "..."}` 很重要:

- **強制** Claude 發出 route_request tool call(不允許自由文字)
- 透過 `input_schema` 保證回應 shape
- `enum` 限制防止幻覺類別
- 分類器不能「閒聊」或解釋 — 只能分類

`tool_choice` 的選項:

| 選項 | 行為 |
|------|------|
| `{"type": "auto"}` | 預設 — Claude 自己決定要不要用 tool |
| `{"type": "any"}` | Claude 必須呼叫*某個* tool,但選哪個 |
| `{"type": "tool", "name": "X"}` | Claude 必須呼叫指定的 tool X |

Routing 要用 `"tool"` — 你要每次都呼叫*特定*分類器 tool。

---

## 完整 Routing Pipeline

```python
PROMPTS = {
    "Educational": "寫一份清楚的教育腳本……",
    "Entertainment": "寫一份高能量的娛樂腳本……",
    "Comedy": "寫一份喜劇腳本……",
    "Personal vlog": "...",
    "Reviews": "...",
    "Storytelling": "...",
}

def generate_script(topic: str) -> str:
    classification = classify(topic)
    category = classification["category"]
    prompt_template = PROMPTS[category]

    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        messages=[{"role": "user",
                   "content": f"{prompt_template}\n\nTopic: {topic}"}],
    )
    return resp.content[0].text
```

每個分支可以獨立最佳化,新增類別只要在 `PROMPTS` 和 `ROUTE_TOOL` 的 enum 加一筆。

---

## 什麼時候 Routing 是對的模式

Anthropic 建議,routing 適用於:

1. **可以清楚定義類別** — 分支之間沒有模糊重疊
2. **信任分類器** — Claude(或更便宜的分類器)能可靠分類
3. **專用處理真的有好處** — 每分支最佳化優於通用 prompt
4. **分類開銷值得分攤** — 多一次 LLM 呼叫是值得的

如果第一次 LLM 呼叫無法可靠分類,routing 反而是錯誤 — 你會把請求送到錯的 pipeline,結果比單一通用 prompt 還糟。

---

## 常見錯誤

1. **分類器用自由文字。** 沒有 `tool_choice="tool"` + `enum`,Claude 可能回「應該是教育類?」 — 你就要 parse。強制 tool call。
2. **類別太多。** Routing 適合類別明顯時。20+ 類別又有重疊會讓分類器不可靠。控制在 10 以下。
3. **沒有誤分類的 fallback。** 信心值低時怎麼辦? 要有預設/通用 pipeline。
4. **忽略分類成本。** 每個請求都多付一次 LLM 呼叫。對低延遲 app,分類用更小/便宜的模型(例如 Haiku)。
5. **把 routing 和 agent 混淆。** Routing 是 *workflow* — 程式碼分派到特定 pipeline。Agent 則是讓 Claude 在推理時自由挑工具。不一樣。

---

> **關鍵洞察**
>
> Routing 是 LLM workflow 版的「switch statement」 — 先分類,再分派。Production 等級的版本用 `tool_choice={"type": "tool", "name": "..."}` 搭配 `enum` input schema,強制出結構化類別標籤。這是 CCA 關鍵重點:**強制 tool use 保證分類器回傳有效類別,且無法閒聊。**

---

## CCA 考試關聯

- **D1(22%)主要**: Routing 是四大 workflow 模式之一,預期有情境題。
- **D2(18%)次要**: `tool_choice` 選項被明確測試 — 記三個值(`auto`、`any`、`tool`)。
- **D5(20%)次要**: Production 模式 — 便宜分類器模型、fallback 分支、enum 限制。
- Routing 訊號字:「categorize」、「classifier」、「dispatch」、「specialized handling per category」。
- 考試陷阱: routing ≠ agent。Routing 是分類呼叫後由程式碼驅動分派。

---

## Flashcards

| 題目 | 答案 |
|------|------|
| 什麼是 routing workflow? | 分類器 LLM 呼叫分類請求,再由程式碼分派到專用 pipeline |
| 為什麼分類器要用 `tool_choice={"type": "tool", "name": "X"}`? | 強制 Claude 透過 tool 回傳結構化類別,不允許自由文字 |
| 列出 `tool_choice` 的三個選項。 | `auto`(預設)、`any`(任一 tool)、`tool`(強制特定 tool)|
| 如何防止分類器幻覺出新類別? | Tool input schema 用 `"enum": [...]` 列出有效類別 |
| 什麼時候*不*該用 routing? | 類別重疊、分類器不可靠、或單一 prompt 已經可靠時 |
| 分類器步驟的關鍵 production 最佳化? | 用更小/便宜的模型(例如 Haiku),因為分類比生成簡單 |
| Routing 是 workflow 還是 agent? | Workflow — 程式碼掌握分類呼叫後的分派 |
| 信心值低時分類器該回什麼? | Route 到預設/通用 pipeline 或要求人工審查(fallback 路徑)|
