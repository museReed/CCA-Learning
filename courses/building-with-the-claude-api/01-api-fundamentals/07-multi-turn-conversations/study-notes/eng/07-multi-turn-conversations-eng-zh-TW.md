# Multi-Turn Conversations — Engineering Deep Dive（繁體中文）

| 項目 | 內容 |
|------|------|
| Exam Domain | D1 — Agentic Architecture (22%) 主要；D5 — Enterprise Deployment (20%) 次要 |
| Task Statements | 1.2（agentic loop 基礎）、1.1（對話狀態管理）、5.3（狀態性的生產 pattern） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 07 |

---

## One-Liner

Anthropic API 是 **stateless** 的——Claude 在呼叫之間沒有記憶——所以 client 要完全負責維護對話歷史並在每次請求時重播。這就是你未來要做的每個 agent 跟 chat feature 的機械基礎。

---

## 核心原則：Statelessness

Claude 這個模型不儲存你的對話。每次 `messages.create()` 都是一個全新的請求，沒有任何之前交流的記憶。如果你呼叫：

```python
client.messages.create(model=model, max_tokens=1000, messages=[
    {"role": "user", "content": "What is quantum computing?"}
])
# → 很好的回答

client.messages.create(model=model, max_tokens=1000, messages=[
    {"role": "user", "content": "Write another sentence"}
])
# → Claude 根本不知道「another sentence」在指什麼；會寫完全不相關的句子
```

第二次呼叫沒有任何 context。Claude 會寫一個跟量子計算完全無關的句子，因為它從沒看過第一次交流。**這不是 bug，是根本設計。**

| 屬性 | Anthropic API |
|------|---------------|
| 伺服器端記得你的對話？ | 沒有 |
| 對話 ID？ | 沒有（API 層沒有） |
| 誰擁有歷史？ | 你的應用程式 |
| 歷史怎麼重播？ | 你的程式碼每次都送完整 `messages` list |

---

## 解法：Client 端歷史

要做多輪對話，你必須：

1. **在應用程式碼裡維護一個 messages list。**
2. **每次請求都送完整的歷史。**

流程：

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  Turn 1:                                        │
│   messages = [user: "Define quantum computing"] │
│   response = create(messages)                   │
│   messages.append(assistant: response.text)     │
│                                                 │
│  Turn 2:                                        │
│   messages.append(user: "Write another          │
│                         sentence")              │
│   response = create(messages)   ← 送完整歷史    │
│   messages.append(assistant: response.text)     │
│                                                 │
│  Turn N:                                        │
│   messages 無限長大；每次呼叫都重播整份。       │
│                                                 │
└─────────────────────────────────────────────────┘
```

每一輪都追加兩個 entry：前一次的 assistant 回應 + 新的 user 問題。

---

## Helper Functions：最小 Chat 骨架

這一課推薦三個一行 helper：

```python
def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
    )
    return message.content[0].text
```

這三個函式是讓呼叫點保持可讀、歷史變動規則保持一致的最乾淨做法。

---

## 組起來

```python
from dotenv import load_dotenv
load_dotenv()

from anthropic import Anthropic

client = Anthropic()
model = "claude-sonnet-4-5"

def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
    )
    return message.content[0].text

# 從空 list 開始
messages = []

# Turn 1
add_user_message(messages, "Define quantum computing in one sentence")
answer = chat(messages)
add_assistant_message(messages, answer)

# Turn 2 —— Claude 現在有完整 turn 1 的 context
add_user_message(messages, "Write another sentence")
final_answer = chat(messages)
add_assistant_message(messages, final_answer)

print(final_answer)
```

這下「Write another sentence」如預期運作——Claude 看得到整段對話，理解代詞指涉的是量子計算。

---

## 隱藏成本：Token 線性成長

因為完整歷史每輪都重播，**input token 會隨對話長度線性成長**。第 N 輪時，你要再付一次 turn 1 到 turn N-1 的費用。

| Turn | Input tokens（約） | 累計 input 成本 |
|------|------------------|---------------|
| 1 | 50 | 50 |
| 2 | 150 | 200 |
| 3 | 300 | 500 |
| 10 | 2,000 | ~10,000 |
| 50 | 20,000 | ~500,000 |

兩個實務後果：

1. **長聊天的帳單由 input token 主宰。** Output 每輪可能就幾百 token；input 會爆炸。
2. **最終會打到 context window。** 每個 model 都有最大 context 長度；長對話在撞牆前要先截斷或摘要。

緩解策略（超出 Lesson 07 範圍但值得知道）：
- **Sliding window** —— 只留最近 N 輪。
- **Summarization** —— 把舊輪次壓成滾動摘要。
- **Prompt caching** —— Anthropic 的 caching feature 讓沒變的 prefix 便宜重用（課程後面會教）。

---

## 為什麼這對 agent 很重要

Lesson 07 教的是單職責多輪 chat，但完全一樣的 pattern 是每個 agent 的基礎：

```python
# Agent loop —— 就是多輪 chat 加 stop_reason 分支
while True:
    response = client.messages.create(model=model, max_tokens=1024, messages=messages, tools=tools)
    messages.append({"role": "assistant", "content": response.content})

    if response.stop_reason == "end_turn":
        break

    if response.stop_reason == "tool_use":
        tool_result = execute_tool(response)
        messages.append({"role": "user", "content": [tool_result]})
        continue
```

結構相似性就是重點：**多輪 chat + stop_reason 分支 = agent**。搞懂 Lesson 07，你就懂了每個 D1 agent 的骨架。

---

## Common Mistakes

1. **忘記追加 assistant 回應** —— 下一輪沒有 context，Claude 看起來像失憶。
2. **只追加 user message** —— API 拒絕連續兩個 user turn；必須交替。
3. **把 API 當有狀態的** —— 伺服器端沒有對話 ID；所有狀態都在你這邊。
4. **忽略 token 成長** —— 測試時好好的對話，在生產長 session 就爆掉。
5. **平行修改 `messages`** —— 多使用者 chat server 必須每個對話隔離；所有使用者共用一個 list 會把歷史搞爛。

> **Key Insight**
>
> API 的 statelessness 不是限制——它是 **刻意的設計**，把記憶的完整控制權交給你。你決定留什麼、丟什麼、摘要什麼、怎麼做 per-user 隔離。所有花俏 feature（agent、tool use、streaming、caching）都坐在「維護 list、每輪重播」這個基礎上。掌握這一課你就擁有整個 CCA 課綱每個上層 pattern 的心智模型。

---

## CCA Exam Relevance

- **D1（Agentic Architecture）**：多輪 loop 就是 agent loop。考題會用「Claude 怎麼記住 context？」的框架——答案永遠是「client 重播歷史；API 是 stateless」。
- **D5（Enterprise Deployment）**：成本（線性 token 成長）與 scale（per-user 隔離）的啟示。
- 情境觸發：「Claude 忘記我們在聊什麼」→ 是 app 沒有追加前一次交流；修復在 client，不是改 prompt。

---

## Flashcards

| Front | Back |
|-------|------|
| Claude 在 API 呼叫之間會儲存對話歷史嗎？ | 不會——API 完全 stateless，歷史由你的應用程式擁有 |
| 每一輪要做哪兩個動作才能保持 context？ | 把前一次的 assistant 回應和新的 user 問題追加到 `messages` list，然後送整份 list |
| 為什麼 input token 用量會隨對話長度線性成長？ | 每次請求都重播完整歷史，所以每次呼叫都把過去所有 turn 當 input 送 |
| Lesson 07 推薦的三個 helper 函式是什麼？ | `add_user_message`、`add_assistant_message`、`chat` |
| 只追加 user message（沒 assistant）會怎樣？ | API 拒絕連續 user turn；對話必須交替 |
| 多輪 chat 跟 agent loop 有什麼關係？ | Agent 就是多輪 chat 加 `stop_reason` 分支（tool_use vs end_turn） |
| 線性 token 成長有哪些緩解方法？ | Sliding window、舊 turn 摘要、prompt caching |
| 生產 chat app 的對話狀態住哪？ | 特定使用者的伺服器端 session——絕不跨使用者共用 |
