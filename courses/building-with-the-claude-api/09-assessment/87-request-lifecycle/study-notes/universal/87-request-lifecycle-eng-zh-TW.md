# 請求生命週期 Request Lifecycle — 工程深入

| 項目 | 說明 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture（22%）主要；D5 — Enterprise Deployment（20%）次要 |
| 任務聲明 | 1.1（API request flow）、5.1（secure architecture）、5.3（stop reasons 與 token 限制） |
| 來源 | building-with-the-claude-api / 09-assessment / Lesson 87 |

---

## 一句話重點

每次 Claude 互動都是一個五步驟來回：client → 你的 server → Anthropic API → Claude 內部 pipeline（tokenize、embed、contextualize、generate）→ 回到 client —— 看懂每一步，你才能設計安全架構、快速 debug 生產問題。

---

## 五步驟請求流程

每一次與 Claude 的互動都遵循可預測的五個階段：

1. **Request to server** —— client app 把使用者輸入送到你的 backend
2. **Request to Anthropic API** —— 你的 server 帶著 API key 轉發請求
3. **Model processing** —— Claude 執行 tokenize、embed、contextualize、generate
4. **Response to server** —— Anthropic 回傳結構化的 response，包含 message、usage、stop_reason
5. **Response to client** —— 你的 server 把產生的文字轉回 UI

不論你在打造 chatbot、IDE 整合、或 agentic workflow，這個形狀都一樣。CCA 課綱的每一個進階模式都是建在這個 loop 上。

---

## 為什麼一定要有 Server（不可直連）

來源立場明確：**絕對不要從 client-side 程式碼直接呼叫 Anthropic API**。理由：

- API request 需要 secret API key 做認證
- 把 key 放在 client code 中是嚴重的資安漏洞
- 任何人都可以把 key 挖出來做未授權的請求

正確做法：你的 web 或 mobile app 把請求送到**你自己的 server**，server 把 API key 保存在安全儲存中，再對上游發送經過清理的請求。這不是便利性建議 —— 這是唯一安全的架構。

這個分層也給你地方可以加 observability、rate limiting、per-user 額度、prompt template、audit logging。每一個生產環境的 Claude app 都有一層 server 介於使用者和 Anthropic 之間。

---

## 發出 API Request

Server 對 Anthropic API 發請求時，可以用官方 SDK（Python、TypeScript、JavaScript、Go、Ruby）或原生 HTTP。每個 request 都必須帶四個核心欄位：

| 欄位 | 用途 |
|------|------|
| **API Key** | 讓 Anthropic 辨識你的請求 |
| **Model** | 要用的 model 名稱（例如 `"claude-3-sonnet"`） |
| **Messages** | 含使用者輸入的 list |
| **Max Tokens** | Claude 可生成的 token 數上限 |

最小 Python 範例：

```python
from anthropic import Anthropic

client = Anthropic()  # 從環境變數讀 ANTHROPIC_API_KEY

response = client.messages.create(
    model="claude-3-sonnet",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
)
print(response.content[0].text)
```

API key 放在 server 的環境變數或 secret manager —— 永遠不要出現在 client 打包的程式碼中。

---

## Claude 內部處理

Anthropic 收到請求後，Claude 走四個內部階段：

### 1. Tokenization

Claude 先把輸入文字切成 token。token 可以是整個字、字的一部分、空格或符號。來源建議「一個字約等於一個 token」作為直覺。

### 2. Embedding

每個 token 被轉成 embedding —— 代表該字所有可能意義的長串數字。把 embedding 想成「數值化定義」，捕捉語義關係。重點是：一個 token 起初承載了**所有**可能意義，消歧義在下一步。

字常常有多重意義。來源以 "quantum" 為例：

- 物理學中的離散量
- 量子力學或量子物理概念
- 極小的、次原子層級的
- 量子計算應用

### 3. Contextualization

Claude 根據周圍字詞來調整每個 embedding，決定在當前情境下最可能的意義。這個過程調整數值表示以凸顯對的定義。這就是 model 如何為手上這句話挑出**這個**意義的 "quantum"。

### 4. Generation

Contextualized embeddings 通過 output layer，計算每個可能的下一個字的機率。Claude 不會永遠挑最高機率的字 —— 它混用機率和受控的隨機性，產生自然、多變的回應。選出一個字後，加進序列，對下一個字重複整個流程。

---

## Claude 何時停止生成

每產出一個 token，Claude 檢查幾個條件決定要不要繼續：

- **Max tokens reached** —— 達到你指定的上限了嗎？
- **Natural ending** —— 產生了 end-of-sequence token？
- **Stop sequence** —— 碰到預設的停止片語？

這三種情況在 response 裡會產生不同的 `stop_reason`。在應用程式碼中區分處理，是「健壯整合」和「悄悄截斷答案」的差別。

---

## API Response

生成結束後，API 回傳結構化 response，內容包含：

| 欄位 | 意義 |
|------|------|
| **Message** | 產生的文字 |
| **Usage** | input/output token 數（用於計費和預算追蹤） |
| **Stop Reason** | 為什麼停止生成（`end_turn`、`max_tokens`、`stop_sequence`、`tool_use`） |

Server 收到後把產生的文字轉回 client 應用，最終出現在 UI 上。

---

## 實務上為什麼重要

來源列出看懂這個流程的四個好處：

- 設計保護 API key 的安全架構
- 為你的使用情境設適當的 token 上限
- 在程式碼中處理不同 stop reason
- 透過了解 pipeline 中問題可能發生的位置來 debug

換句話說，生命週期是「出事時你需要的那張地圖」。延遲飆高？你可以推斷是網路（1-2、4-5 步）還是 model（3 步）。輸出被截斷？看 stop_reason。帳單爆炸？看 usage。沒這張地圖，每一次故障都只能瞎猜。

---

## 常見錯誤

1. **從 client code 直接呼 Anthropic API** —— 洩漏 API key；來源明確說這絕對不行。
2. **不處理不同 stop reason** —— 把所有 response 當自然結束，會悄悄掩蓋 `max_tokens` 截斷。
3. **忽略 usage 欄位** —— 帳單爆炸是必然的，per-user 預算也壞掉。
4. **寫死 model 名稱** —— model 升級會很痛苦；應透過環境變數設定。
5. **忘了 max_tokens** —— 不設上限的請求會帶來未預期的成本和延遲。
6. **誤把 tokenization 當 word split** —— token 可能是子字、空白或符號；「一字 ≈ 一 token」是直覺，不是規則。

> **關鍵洞察**
>
> Request lifecycle 是讓 CCA 課綱中所有其他主題變得可理解的心智模型。Tool use、streaming、caching、agents —— 它們全都是這五步流程的變體。記熟一次，每個進階模式都變成「這一步，稍作修改」。跳過這步，每一種失敗模式都像魔法。

---

## CCA 考試相關性

- **D1（Agentic Architecture）**：生命週期是所有 agentic 模式的基礎。會考「X 發生在 request flow 的哪一步？」
- **D5（Enterprise Deployment）**：安全架構（server 介於 client 和 API）、token 預算、stop-reason 處理是生產部署必備。
- 注意：「為什麼 client 和 Anthropic 之間要有 server？」→ API key 安全性。「Claude 內部做什麼？」→ tokenize、embed、contextualize、generate。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Claude request lifecycle 的五個步驟是什麼？ | Request to server → request to Anthropic API → model processing → response to server → response to client。 |
| 為什麼 request 一定要走你自己的 server，不能從 client 直接發？ | Client-side 的 API key 可以被挖出來，造成嚴重資安漏洞，讓任何人發未授權請求。 |
| 每個 API request 必須包含哪四個核心欄位？ | API Key、Model、Messages、Max Tokens。 |
| Claude 內部處理的四個階段是什麼？ | Tokenization、embedding、contextualization、generation。 |
| 什麼是 tokenization？ | 把輸入文字切成更小的 chunk（整字、字的一部分、空格或符號），叫 token。 |
| 什麼是 embedding？ | 代表一個 token 所有可能意義的長串數字 —— 數值化的定義。 |
| Contextualization 做什麼？ | 根據周圍字詞調整每個 embedding，決定當前情境下最可能的意義。 |
| 為什麼 Claude 不永遠挑最高機率的下一個字？ | 它混用機率和受控的隨機性，產生自然、多變的回應。 |
| 哪三個條件讓 Claude 停止生成？ | 達到 max tokens、自然結束（end-of-sequence token）、或碰到預設的 stop sequence。 |
| API response 含哪三個欄位？ | Message（產生的文字）、Usage（input/output token 數）、Stop Reason（停止原因）。 |
| 為什麼懂生命週期有助於 debug？ | 讓你能定位故障發生在哪一環 —— 網路、認證、model 處理、或 response 處理。 |
