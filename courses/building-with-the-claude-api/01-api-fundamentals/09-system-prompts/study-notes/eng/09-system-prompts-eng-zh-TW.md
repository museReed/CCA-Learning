# System Prompts — 工程深度解析

| 項目 | 細節 |
|------|------|
| 考試領域 | D5 — Enterprise Deployment (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 5.1（模型選擇與設定）、5.3（production 模式）、1.2（agentic loop 基礎） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 09 |

---

## 一句話總結

System prompt 是一個獨立於 `messages` 的頂層指令通道，用來定義 Claude 在整個對話中的 persona、任務範圍與回應規則，是你在多輪互動中鎖定行為的決定性錨點。

---

## 為什麼 System Prompt 重要

沒有 system prompt，Claude 會用泛用的 helpful assistant 模式回應。這對隨意 Q&A 沒問題，但 production 應用幾乎都需要更窄、更有主見的行為設定。

以數學家教 chatbot 為例，學生問「How do I solve 5x + 2 = 3 for x?」。泛用 Claude 會直接給出完整解答——這就是**錯的產品行為**。好的家教應該：

- 給提示而不是完整答案
- 一步一步引導學生思考
- 用類似題目示範做法

而且明確不應該：

- 直接給答案
- 叫學生去用計算機

這是**行為規範**，不是知識落差。System prompt 就是你編碼這份規範的地方。

---

## API 介面

Anthropic Messages API 提供一個專屬的 `system` 參數，和 `messages` array 分開：

```python
from anthropic import Anthropic

client = Anthropic()

system_prompt = """
You are a patient math tutor.
Do not directly answer a student's questions.
Guide them to a solution step by step.
"""

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    system=system_prompt,
    messages=[{"role": "user", "content": "How do I solve 5x + 2 = 3 for x?"}],
)
print(response.content[0].text)
```

關鍵屬性：

- `system` 是純字串（若要用 prompt caching 則可以是 text block list）
- **不是** `messages` 的一部分。Anthropic API 裡沒有 `{"role": "system", ...}` 這種寫法
- Claude 把 system prompt 當作比 user message 更高優先級的 context
- 它持續整個 turn——你不必每條訊息重複注入，但每次 API 呼叫都要帶上它

---

## 前後對比

沒有 system prompt：

> To solve 5x + 2 = 3, subtract 2 from both sides: 5x = 1. Then divide by 5: x = 0.2.

帶上家教 system prompt：

> Great question! What do you think would be a good first step to isolate x? Consider what operation we might need to perform on both sides to start moving terms around.

同一個模型、同一個 user message——行為完全不同。差別全在 system prompt。

---

## 建立一個彈性的 chat 函式

把 system prompt 寫死在程式碼裡是錯誤的抽象。包一個輔助函式，讓 `system` 變成可選參數：

```python
def chat(messages, system=None):
    params = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 1000,
        "messages": messages,
    }
    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text
```

這個條件判斷很重要：**API 不接受 `system=None`**。你必須先組 kwargs dict，只在 `system` 是非空字串時才插入。這是 production 的真實地雷——傳 `None` 會觸發 validation error。

使用方式：

```python
# 通用行為
answer = chat(messages)

# 家教行為
tutor_system = """
You are a patient math tutor.
Do not directly answer a student's questions.
Guide them to a solution step by step.
"""
answer = chat(messages, system=tutor_system)
```

---

## System Prompt 該放什麼

一個強的 system prompt 通常結合：

1. **身份 / persona**——「You are a senior security engineer reviewing code for vulnerabilities.」
2. **任務範圍**——Claude 該處理什麼、不該處理什麼
3. **回應格式**——語氣、長度、結構、markdown 使用
4. **Guardrails**——硬規則（「永遠不揭露 API keys」「拒絕無關問題」）
5. **範例**——理想輸出的 few-shot 示範

要宣告式、要具體。「Be helpful」是雜訊。「永遠回傳含 `summary` 與 `action_items` keys 的 JSON」才是有用訊號。

---

## System Prompt 與 Agentic Loop

在 agentic 應用（D1）中，system prompt 定義了 agent 的**身份與運作規則**——也就是 tool-use loop 每一輪都不變的常數。Tools 在每輪可能進出，但 system prompt 是穩定的契約。這就是為什麼 CCA 考試常把 agent 設計題包成「這個約束該放哪？」——答案幾乎永遠是 system prompt，而不是逐條 user message 的指令。

---

## 常見錯誤

1. **把指令寫在 user message 而不是 `system`**——在多輪 context 中指令會被稀釋，Claude 會把它當成一次性請求處理
2. **傳 `system=None`**——SDK 會拒絕。要條件式組 kwargs
3. **用 `{"role": "system", ...}` message**——那是 OpenAI 的慣例，不是 Anthropic。會被當 user message，行為錯亂
4. **把動態資料塞進 system prompt**——system prompt 應該穩定；volatile context（使用者資料、當前文件）要放在第一條 user message 或獨立 content block，這樣 prompt caching 才能生效
5. **不迭代**——system prompt 是產品。版本化、A/B 測試、回歸要當回事

> **Key Insight**
>
> System prompt 是你和 Claude 之間的*行為契約*——唯一一個你可以鎖死身份、任務、guardrails 的地方。所有會變的東西（user input、retrieved context、tool results）走 `messages`；所有不會變的東西走 `system`。把這兩者搞混，你會不是把 persona 洩漏到每個 user turn，就是讓 prompt 的靜態部分無法被 cache。

---

## CCA 考試重點

- **D5 (Enterprise Deployment)**：production 應用需要一致的行為——system prompt 是在規模下強制這種一致性的標準機制
- **D1 (Agentic Architecture)**：system prompt 定義了 agent 在多輪 loop 中的持續身份。Tool-use agents 靠它保持專注
- 注意「如何確保 Claude 表現得像 {role}？」這種考題——答案一定是 system prompt，不是在 user message 做 prompt engineering

---

## Flashcards

| 題目 | 答案 |
|------|------|
| Anthropic API 用哪個參數設定 system prompt？ | `system`——`messages.create()` 的頂層字串參數，和 `messages` array 分開 |
| 可以傳 `system=None` 給 `messages.create()` 嗎？ | 不行——API 會拒絕。要條件式組 kwargs，只在有提供時才加入 `system` |
| `{"role": "system", ...}` message 在 Anthropic API 裡該放哪？ | 哪都不該放——那是 OpenAI 慣例。Anthropic 用獨立的頂層 `system` 參數 |
| 為什麼數學家教 chatbot 需要 system prompt？ | 為了覆蓋 Claude 直接給答案的預設行為，強制逐步 Socratic 引導 |
| System prompt 通常包含哪五樣東西？ | 身份/persona、任務範圍、回應格式、guardrails、可選的 few-shot 範例 |
| 在 agentic loop 中，system prompt 扮演什麼角色？ | 每一輪都不變的行為契約——tools 和 user messages 會變，但 system prompt 鎖住身份和規則 |
| Volatile 的使用者 context 應該放在 system prompt 嗎？ | 不應該——volatile context 要放在 `messages`，避免破壞 prompt caching 並可隨 turn 演化 |
| System prompt 和 user 指令的差別是什麼？ | System prompt 持續整個對話且優先級更高；user 指令是單輪輸入，被當成 request 層級 context |
