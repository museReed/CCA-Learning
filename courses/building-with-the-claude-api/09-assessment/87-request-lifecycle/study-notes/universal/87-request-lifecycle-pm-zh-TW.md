# 請求生命週期 Request Lifecycle — PM 視角

| 項目 | 說明 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture（22%）主要；D5 — Enterprise Deployment（20%）次要 |
| 任務聲明 | 1.1（API request flow）、5.1（secure architecture）、5.3（stop reasons 與 token 限制） |
| 來源 | building-with-the-claude-api / 09-assessment / Lesson 87 |

---

## 一句話重點

Claude request lifecycle 是你產品裡每一次 AI 互動的解剖圖 —— 看懂它，PM 就能在第一行 code 被寫之前，把安全性、延遲預算、成本、事故應對的決策做對。

---

## 為什麼 PM 要在意

PM 不需要寫 `ast.parse` 也不需要實作 tokenization —— 但 PM **需要**決定架構、審 security、設 token 預算、owning 事故處理。上述每一個決策都藏在這五步流程裡：

| PM 決策 | 對應生命週期步驟 |
|---------|------------------|
| 「API key 放在哪？」 | 步驟 1-2（絕不能在 client） |
| 「最壞延遲是多少？」 | 步驟 3（model）+ 1-2、4-5 的網路 |
| 「每次請求的成本上限？」 | 步驟 2（max_tokens）+ 步驟 4（usage） |
| 「答案被截斷時 UX 怎麼處理？」 | 步驟 4（stop_reason） |
| 「事故 triage 流程？」 | 每一步 —— 生命週期就是那張地圖 |

跳過這個知識，團隊會在沒有你的情況下做這些決策，而且通常做錯。

---

## 心智模型：餐廳點餐

把每個 Claude request 想成在廚房講不同語言的餐廳點餐：

| 步驟 | 餐廳比喻 | 生命週期步驟 |
|------|----------|--------------|
| 客人告訴服務生要什麼 | 用戶跟你的 app 對話 | Request to server |
| 服務生把點單翻成廚房聽得懂的語言 | 你的 server 呼叫 Anthropic API | Request to API |
| 廚房做菜 | Claude 執行 tokenize、embed、contextualize、generate | Model processing |
| 服務生把菜端出來 | API 回 message、usage、stop_reason | Response to server |
| 把菜放到客人面前 | 你的 server 把文字轉回 UI | Response to client |

服務生（你的 server）是不可協商的。你不會讓客人自己走進廚房 —— 也絕不讓 client 直接呼 Anthropic API，同樣原因：會破壞廚房的安全和速度保證。

---

## 產品使用情境：每一步為什麼重要

### 安全（步驟 1-2）

來源立場明確：**絕不從 client-side 程式碼呼叫 Anthropic API**。Client 裡的 API key 可以被挖出來做未授權請求。對 PM 而言，這在每個 AI feature 的 PRD 中都是不可協商的安全要求：

- API key 放在 server 的安全儲存
- Client 只跟你的 server 講話，絕不碰 Anthropic
- Server 加 authentication、rate limiting、audit logging

### 成本與延遲（步驟 2-3）

每個 request 都必須含 `max_tokens`。這是 PM 手上最重要的成本槓桿。設太高，脫韁的生成會毀掉 unit economics。設太低，Claude 會講到一半被截斷，用戶沮喪。PM 常見作法是按 feature 分層：短回覆 256、長解釋 2048、文件草稿 8192。

### Response 處理（步驟 4）

API response 有三個 PM 該在乎的欄位：

| 欄位 | PM 關注點 |
|------|-----------|
| Message | 用戶實際看到的內容 |
| Usage | 驅動計費、預算追蹤、per-user 額度 |
| Stop Reason | 決定 feature 是正常工作還是被悄悄截斷 |

stop_reason 是三者中最陰險的。如果 app 忽略它，`max_tokens` 截斷看起來就跟完整答案一樣 —— 只差一段文字不見了。永遠在 UX 中明確處理 stop reason（例如「回應被切斷 —— 要繼續嗎？」）。

---

## 四個內部階段 —— PM 為什麼要懂

Claude 內部處理有四階段：**tokenization、embedding、contextualization、generation**。PM 不需要實作，但在概念層面懂它們能解鎖更好的產品直覺：

| 階段 | PM 洞察 |
|------|--------|
| **Tokenization** | 成本和長度以 token 計，不是以字。含大量 code 或非英文的輸入比你預想的貴。 |
| **Embedding** | 每個 token 起初承載**所有**可能意義 —— 所以短而有歧義的輸入會產出不可靠的結果。 |
| **Contextualization** | 周圍字詞消歧義 —— 所以框架好的 prompt 勝過裸指令。 |
| **Generation** | Claude 用受控隨機性，不是純最高機率 —— 所以同輸入有時產不同輸出，「deterministic」不是預設。 |

---

## PM 決策框架

| 問題 | 若答 Yes | 行動 |
|------|---------|------|
| 我們的架構有 server 介於 client 和 Anthropic 之間嗎？ | Yes | 通過安全審查 |
| 每個 request 有合理的 `max_tokens` 嗎？ | Yes | 通過成本審查 |
| App 有區分 `end_turn` 和 `max_tokens` 這些 stop reason 嗎？ | Yes | 通過 UX 審查 |
| Per-user token usage 有 log 且有預算嗎？ | Yes | 通過財務審查 |
| 事故發生時團隊知道是哪一步壞掉嗎？ | Yes | 通過事故審查 |

---

## 常見 PM 錯誤

1. **放任工程 ship client 直連 API** —— 即將發生的資安事故。這該在每個安全審查被擋下。
2. **不 own max_tokens** —— 留給工程 default，成本就會隨使用線性擴張，沒有產品輸入。
3. **UX spec 裡忽略 stop_reason** —— 答案悄悄截斷，用戶覺得 AI 很笨。
4. **PRD 裡把 words 和 tokens 搞混** —— 「200 字上限」不等於 `max_tokens=200`；token 可以是子字。
5. **期待 deterministic 輸出** —— generation 步驟用受控隨機性；同輸入可能產不同輸出，acceptance test 必須考慮這點。

> **關鍵洞察**
>
> 每一個高深的 Claude 模式 —— tool use、streaming、caching、agents —— 都是這同一個五步生命週期的變體。把這個模型裝在腦裡的 PM，拿到任何 AI feature 提案都能立刻問出對的問題：安全、成本、延遲、失敗處理。跳過的 PM 只能猜，而且通常在最貴的那些上猜錯。

---

## CCA 考試相關性

- **D1（Agentic Architecture）**：生命週期是所有 agentic 模式的基礎。常考「X 發生在 request flow 的哪一步？」
- **D5（Enterprise Deployment）**：安全架構、token 預算、stop-reason 處理是生產部署必備。
- 注意：「為什麼 client 和 Anthropic 之間要有 server？」→ API key 安全性，永遠是。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Claude request lifecycle 的五個步驟？ | Client 到 server → server 到 API → model 處理 → API 到 server → server 到 client。 |
| 為什麼 PM 必須要求 client 和 Anthropic API 之間有 server？ | 為了保護 API key —— client 的 key 可被挖出來做未授權請求。 |
| Server 角色的餐廳比喻？ | 服務生 —— 不可協商的中介，介於客人和廚房之間。 |
| 每個 API request 必備的四個欄位？ | API Key、Model、Messages、Max Tokens。 |
| Claude 內部處理的四個階段？ | Tokenization、embedding、contextualization、generation。 |
| 哪個 response 欄位告訴你答案是否被悄悄截斷？ | `stop_reason` —— 如果是 `max_tokens` 就是被截斷了。 |
| PM 在 request 層級擁有什麼成本槓桿？ | `max_tokens` —— 直接限制單次請求的成本和延遲。 |
| 為什麼 Claude 相同請求不總是 deterministic？ | Generation 步驟用機率和受控隨機性的混合。 |
| `usage` 欄位讓 PM 能做什麼？ | 計費、預算追蹤、per-user 額度。 |
| PRD 裡為什麼要區分 words 和 tokens？ | Token 可能是子字、空白或符號 —— 「200 words」不等於 `max_tokens=200`。 |
