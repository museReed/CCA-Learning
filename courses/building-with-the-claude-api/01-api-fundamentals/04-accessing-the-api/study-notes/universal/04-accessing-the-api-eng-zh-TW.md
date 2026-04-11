# Accessing the API — Engineering Deep Dive（繁體中文）

| 項目 | 內容 |
|------|------|
| Exam Domain | D5 — Enterprise Deployment (20%) 主要；D3 — Claude Code Configuration (20%) 次要；D1 — Agentic Architecture (22%) |
| Task Statements | 5.1（model selection）、5.3（production patterns）、3.1（API key 管理）、1.2（agentic loop 基礎） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 04 |

---

## One-Liner

一個生產環境的 Claude 請求會經過五個跳點：client → 你的 server → Anthropic API → 模型 pipeline → response。搞懂每一跳，才能做好安全架構、除錯與成本/延遲調校。

---

## 五步驟請求生命週期

```
┌────────┐ 1) HTTPS  ┌────────┐ 2) HTTPS+key ┌──────────┐ 3) Model
│ Client │ ────────▶│  你的  │ ────────────▶│ Anthropic│  處理
│  (app) │          │ Server │              │   API    │  (tokenize,
│        │ ◀────────│        │ ◀────────────│          │   embed,
└────────┘ 5) JSON  └────────┘ 4) Response  └──────────┘   contextualize,
                                                           generate)
```

| 步驟 | 跳點 | 傳遞內容 | 誰持有 secret |
|------|------|---------|--------------|
| 1 | Client → Server | 使用者 prompt、session token | — |
| 2 | Server → Anthropic | Prompt + `x-api-key` header | Server |
| 3 | Anthropic 內部 | Tokens → embeddings → logits → next token | Anthropic |
| 4 | Anthropic → Server | `message` JSON（`content`、`usage`、`stop_reason`） | — |
| 5 | Server → Client | 渲染後的文字或 streaming SSE | — |

每個生產事故都發生在這五跳之中的某一跳。**第一個要問的問題永遠是：哪一跳壞了？** 這個問題能不能問出來，就看你有沒有把這張圖背起來。

---

## 為什麼一定要有伺服器

直接從 client 呼叫 Anthropic 在生產環境是絕對禁止的。原因只有一個：API key 是 **bearer credential**——任何持有它的東西都可以花你的錢、看你的回應。

| 錯誤做法 | 後果 |
|---------|------|
| API key 寫進 mobile app binary | 用 `strings` 或 decompile 就挖得出來 → 被濫用 |
| API key 寫進瀏覽器 JS | DevTools 直接看見 → credits 瞬間被抽乾 |
| API key commit 到 public GitHub repo | Anthropic 幾分鐘內會自動 revoke，但帳單已經打下去了 |

伺服器這一層是唯一可以做到下列事情的地方：
1. 把 key 放在環境變數或 secret manager（絕不寫進原始碼）。
2. 做每使用者的 rate limit 與 auth。
3. 在資料離開你的邊界前做 logging、稽核、PII 脫敏。
4. 加 retry、circuit breaker、cache 等邏輯。

---

## 模型內部：四個處理階段

請求進到 Anthropic 之後，Claude 會跑完四個階段才吐出第一個 output token：

1. **Tokenization**（斷詞）——輸入文字被切成 tokens。粗略把一個英文單字想成一個 token，但長字會被切成片段。
2. **Embedding**（嵌入）——每個 token 變成一個高維向量，同時編碼該字所有可能的語意（例如 "quantum" 同時帶有物理、計算、「非常小」等意義）。
3. **Contextualization**（上下文化）——周圍的 tokens 把每個 embedding 往句子實際需要的那個語意拉。
4. **Generation**（生成）——最後一層產生詞彙表上的機率分布；下一個 token 是用帶隨機性的取樣抽出來的（不是純 argmax）。新 token 附到序列後面，迴圈繼續。

```python
# 生成迴圈的概念 pseudo-code
tokens = tokenize(prompt)
while True:
    embeddings = embed(tokens)
    contextual = contextualize(embeddings)
    logits = output_layer(contextual)
    next_token = sample(logits)  # 不是純 argmax
    tokens.append(next_token)
    if should_stop(next_token, tokens):
        break
```

取樣這一步就是為什麼兩個一模一樣的請求會回不同的字——temperature 跟隨機性是刻意設計，讓回應自然。

---

## 停止條件

每產生一個 token，Claude 會檢查三個離開條件：

| `stop_reason` | 意義 | 你該做什麼 |
|---------------|------|----------|
| `end_turn` | 模型自己吐出 end-of-sequence token | 把文字回給使用者 |
| `max_tokens` | 預算打滿，被截斷 | 調高 `max_tokens` 或顯示截斷 UI |
| `stop_sequence` | 撞到你在 `stop_sequences` 給的字串 | 預期行為——拿 sentinel 做切割 |

生產環境常見 bug：工程師把 `max_tokens` 設 256，然後在 log 寫「Claude 截斷了」當成模型 bug。這不是 bug，是你自己的預算。**一定要分支判斷 `stop_reason`。**

---

## Response 結構

Anthropic 回傳的 JSON 有一個穩定的形狀，你的程式碼應該做 pattern match：

```python
from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "請解釋五步驟請求流程。"}],
)

print(response.content[0].text)       # 生成的文字
print(response.usage.input_tokens)    # 成本指標 1
print(response.usage.output_tokens)   # 成本指標 2
print(response.stop_reason)           # "end_turn" | "max_tokens" | "stop_sequence" | "tool_use"
```

生產環境每個 app 都應該關心三個欄位：
- `content` —— 模型吐出的文字或 tool_use block。
- `usage` —— input + output token 數；乘上價目表就是單次請求的真實成本。
- `stop_reason` —— 後端的分支訊號，決定是「回給使用者」、「繼續 loop」還是「處理截斷」。

---

## Common Mistakes

1. **從瀏覽器直接呼叫 Anthropic** —— key 秒被偷。一定要透過你的伺服器代理。
2. **把 `max_tokens` 當成目標長度** —— 它是上限。模型遇到 `end_turn` 就停，不會刻意撐到那個數字。
3. **忽略 `stop_reason`** —— 程式碼永遠假設 `end_turn`，結果 `max_tokens` 截斷的時候靜靜吞掉。
4. **把帶 PII 的完整 prompt 寫進 log** —— 伺服器這一跳是唯一可以在資料離開邊界前脫敏的地方。
5. **忘記生成是隨機的** —— 斷言字串完全相等的測試會 flaky；要嘛斷言結構，要嘛把 temperature 設低。

> **Key Insight**
>
> 五步驟流程不是考試小常識，而是你除錯每個生產事故時用的心智地圖。請求失敗時你第一個問題永遠是「哪一跳？」這個問題有沒有答案，取決於你有沒有把這張圖內化。CCA 的 Enterprise Deployment domain 其他東西全部建在這張圖上面。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）**：考題會丟情境問你 API key 該放哪、`max_tokens` 該設多少、生產程式碼怎麼處理 `stop_reason`。
- **D3（Claude Code Configuration）**：API key 儲存模式（env vars、secret manager，絕不寫 client-side）。
- **D1（Agentic Architecture）**：request/response envelope 是每個 agent loop 的原子單位——所有 agent 都是跑這個流程的 for-loop。
- 題目裡出現「API key 該放在哪」→ 答案永遠是伺服器，絕不是 client。

---

## Flashcards

| Front | Back |
|-------|------|
| Claude 請求生命週期的五個步驟是什麼？ | Client → Server、Server → Anthropic API、模型處理、Anthropic → Server、Server → Client |
| 為什麼 API key 必須放伺服器不能放 client？ | Key 是 bearer credential，任何 client 持有都能被取出並濫用，把你的 credits 抽乾 |
| 模型內部四個階段是什麼？ | Tokenization、embedding、contextualization、generation |
| `max_tokens` 的真正含義？ | 輸出長度的上限——遇到 `end_turn` 會提前停，模型不會刻意撐到這個數字 |
| 這一課提到哪三個 `stop_reason`？ | `end_turn`（自然結束）、`max_tokens`（打到預算）、`stop_sequence`（撞到使用者給的 sentinel） |
| 哪個 response 欄位告訴你這一次花了多少錢？ | `response.usage.input_tokens` 與 `response.usage.output_tokens` |
| 為什麼兩個一模一樣的請求會回不同的字？ | 生成是從機率分布做帶隨機性的取樣，不是純 argmax |
| 每個請求必須帶的四個欄位？ | API key、model 名稱、messages list、max_tokens |
