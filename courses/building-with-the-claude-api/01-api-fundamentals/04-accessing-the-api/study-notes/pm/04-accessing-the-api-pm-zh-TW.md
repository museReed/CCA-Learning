# Accessing the API — PM Perspective（繁體中文）

| 項目 | 內容 |
|------|------|
| Exam Domain | D5 — Enterprise Deployment (20%) 主要；D3 — Claude Code Configuration (20%) 次要；D1 — Agentic Architecture (22%) |
| Task Statements | 5.1（model selection）、5.3（production patterns）、3.1（API key 管理）、1.2（agentic loop 基礎） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 04 |

---

## One-Liner

產品裡每一個 Claude feature 其實都是一趟五跳旅程——client、server、API、model、回來。搞懂這五跳的 PM，才能在延遲、成本、安全、失敗 UX 之間做出聰明的取捨。

---

## Mental Model：機場轉機

把 Claude 請求想成乘客從手機飛到模型再飛回來：

| 跳點 | 機場比喻 | PM 該在意什麼 |
|------|---------|--------------|
| 1. Client → 你的 Server | 上國內線 | UX 延遲預算開始倒數 |
| 2. Server → Anthropic | 國際轉機（護照＝API key） | 安全、rate limit、logging |
| 3. Claude 內部 | 海關 / 行李處理 | 看不見內部，但花時間和錢 |
| 4. Anthropic → Server | 飛機降落、拿行李 | 拿到 `stop_reason` 與 `usage` metadata |
| 5. Server → Client | 乘客叫計程車回家 | 渲染 streaming、需要的話把成本顯示給使用者 |

每一跳都加延遲，每一跳都可能出錯。PM 的工作就是圍繞這個事實設計：這整段過程既不即時也不免費。

---

## 為什麼「必須有 server」是產品規格的硬需求

PM 常被問「我們能不能直接從 mobile app 呼叫 API？」答案永遠是不行，而且理由是商業的，不只是技術的：

| Client-side 呼叫的風險 | 商業影響 |
|---------------------|---------|
| API key 被從 app binary 挖出來 | Credits 一夜被抽乾，帳單爆表 |
| Key commit 到 public repo | 被自動 revoke，feature 壞掉，丟臉事件 |
| Client 沒有 rate limit | 濫用的使用者花你的錢比他付的還多 |
| 沒有 audit log | 無法滿足企業合規需求（SOC2、HIPAA） |

Server 是你未來要應付法務、財務、安全部門所有要求的地方。**Day 1 就要有，不是等出事才補。**

---

## Product Use Cases

### 五步驟流程最重要的場景

| 場景 | PM 為什麼該懂這條流程 |
|------|--------------------|
| 給企業客戶的 chatbot | Audit log 跟 PII 脫敏都要在 server 那跳做 |
| 有 AI feature 的 mobile app | Key 不能包進 binary，需要 BFF 層 |
| 成本敏感的免費方案 | `usage` 讓你不用再拉計費系統就能按使用者計費 |
| 法規產業（醫療、金融） | Server 是唯一可以控管資料落地的地方 |
| 長篇生成 feature | `stop_reason == max_tokens` 要有「繼續」的 UX pattern |

### 沒那麼關鍵的場景（但還是要注意）

| 場景 | 為什麼 |
|------|-------|
| 只給 10 個工程師用的內部工具 | 安全還是重要，但成本/延遲調校可以晚點做 |
| 一次性實驗 | 流程一樣，只是省略生產環境硬化 |

---

## PM Decision Framework

設計 Claude feature 時走一遍這些問題：

| 問題 | 為什麼重要 |
|------|----------|
| API key 放哪裡？ | 答案必須是 server。工程師講「client」就要舉紅旗。 |
| 這個 feature 的 `max_tokens` 預算是多少？ | 決定成本上限和截斷 UX。 |
| `stop_reason == max_tokens` 怎麼處理？ | 自動續寫？顯示「看更多」？默默截斷？ |
| 每個使用者的用量怎麼計？ | `response.usage` 是免費的，另開一個計費系統不是。 |
| Prompt log 寫在哪？ | 必須是 server，而且要做 PII 脫敏。 |
| 等待時給使用者看什麼？ | 五跳總共好幾秒，streaming UX 或 loader 必備。 |

---

## 成本透明化的優勢

Anthropic 每個 response 都會回 `usage.input_tokens` 與 `usage.output_tokens`。這是 PM 的隱藏超能力：

- 可以讓企業使用者看到每次互動的成本。
- 可以不用叫工程師埋點就做每使用者配額。
- 可以立即 A/B 測試 prompt 變更的成本差異。
- 可以建 dashboard 看哪個 feature 最貴。

在其他 SaaS 產品裡，這些都需要另開計費 pipeline。Anthropic 直接塞在每個 response 裡。

---

## Common PM Mistakes

1. **以為 AI feature 是即時的** —— 五跳是真的要花時間，loading state、streaming、optimistic UI 第一天就要設計。
2. **scope 的時候沒決定 `max_tokens`** —— 工程師會隨便給一個數字，悄悄蓋住 feature 品質上限。
3. **忘了截斷 UX** —— `stop_reason == max_tokens` 生產環境一定會遇到，PRD 必須說明使用者會看到什麼。
4. **V1 不做成本計量** —— 之後補比一開始就用 `usage` 困難十倍。
5. **以為 client 可以直接打 Anthropic** —— 會卡住 mobile 和 web launch，直到 security 審 BFF 為止。

> **Key Insight**
>
> PM 的角度看，五步驟流程就是你未來面對每個事故、成本審查、安全稽核的地圖。工程師講「AI 很慢」或「AI 壞了」，你第一個問題永遠該是「哪一跳？」這一句話能強迫團隊把 client、server、Anthropic、model 區分開，比任何其他 post-mortem framing 都更快解鎖問題。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）**：情境題會問 API key 放哪、`max_tokens` 怎麼設、生產程式碼怎麼處理 `stop_reason`。
- **D3（Claude Code Configuration）**：API key 管理模式——答案永遠是 server 儲存。
- **D1（Agentic Architecture）**：每個 agent loop 都是在這個五步驟 envelope 上跑 for-loop。
- 觸發條件：題目說「工程師把 key 放進 mobile app」→ 正確答案永遠是「搬到後端 service」。

---

## Flashcards

| Front | Back |
|-------|------|
| 用 PM 語言講五步驟 Claude 請求流程？ | Client → Server → Anthropic API → Model → 回 Server → Client |
| 為什麼 mobile app 不能直接打 Anthropic？ | API key 會被從 binary 抽走，誰都能抽乾你的 credits |
| PII 脫敏唯一能做的位置是哪一跳？ | Server 那一跳（在資料離開你的邊界之前） |
| 每個 response 都會給哪些 PM 相關的 metadata？ | `usage.input_tokens`、`usage.output_tokens`、`stop_reason` |
| `stop_reason == max_tokens` 對 UX 的意義？ | Claude 被中途截斷；PRD 要描述截斷 UI（例如「繼續」按鈕） |
| 為什麼 response 的 `usage` 是 PM 超能力？ | 不用另外加 infra 就能做每使用者計費和 prompt A/B 成本比較 |
| scope AI feature 時第一個該問的安全問題？ | 「API key 放哪？」——唯一正確答案是 server |
| 假設 AI 回應是即時的會失去什麼？ | 會省略 loading / streaming UX，使用者在 2–5 秒 round trip 裡覺得 feature 壞掉 |
