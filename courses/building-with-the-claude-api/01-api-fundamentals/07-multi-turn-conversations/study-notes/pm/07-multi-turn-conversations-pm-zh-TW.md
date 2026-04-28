# Multi-Turn Conversations — PM Perspective（繁體中文）

| 項目 | 內容 |
|------|------|
| Exam Domain | D1 — Agentic Architecture (22%) 主要；D5 — Enterprise Deployment (20%) 次要 |
| Task Statements | 1.2（agentic loop 基礎）、1.1（對話狀態管理）、5.3（生產 pattern） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 07 |

---

## One-Liner

Claude 在呼叫之間沒有記憶——每一輪你的產品都要提供對話歷史——這讓「使用者感覺 AI 記得什麼」變成 PM 沒辦法丟給工程師的產品決策。

---

## Mental Model：金魚顧問

想像你請了一位非常聰明但是同時是金魚的顧問：每次你走進會議室，他都對上次會議沒有記憶。要持續對話，你每次會議開始都要遞上所有過去會議的列印逐字稿。

| 金魚顧問 | Claude API |
|---------|-----------|
| 會議之間會忘記 | API 呼叫之間 stateless |
| 讀逐字稿追上進度 | 每次呼叫讀 `messages` list |
| 逐字稿每次變厚 | `messages` list 每輪變長 |
| 厚逐字稿讀起來久 | 歷史越長，input token 越貴 |

PM 的工作是決定：逐字稿要放什麼、保留多久、每次會議你願意付多少錢。

---

## 為什麼 PM 該關心 Statelessness

這一個技術細節對產品的影響超乎想像：

| 產品考量 | Statelessness 的影響 |
|---------|---------------------|
| 聊天感 | 記憶必須刻意設計，不會免費出現 |
| 成本曲線 | 長聊天很快變貴（線性 token 成長） |
| 隱私 | 你決定留什麼、丟什麼 |
| Session 逾時 | 對話什麼時候「結束」你決定，不是 API |
| 跨裝置延續 | 歷史必須放在持久儲存，不只是 in-memory |
| Per-user 隔離 | 絕不能把一個使用者的歷史混進另一個 |

這每一項都是產品決策。工程師可以實作任何一種，但需要 PM 指引產品該有哪種行為。

---

## Product Use Cases

### 需要多輪的時候

| Feature | 為什麼必須多輪 |
|---------|-------------|
| 客服聊天 | 使用者會指涉對話前面的東西 |
| 教學 / coaching agent | 學習進度依賴前幾輪的 context |
| 長期寫作助理 | 草稿會跨多個 prompt 迭代 |
| 研究 agent | 某一步的發現會餵到下一步 |

### 單輪就夠的時候

| Feature | 為什麼單輪可以 |
|---------|-------------|
| 「摘要這封信」按鈕 | 每次點擊獨立 |
| 文件分類 | 不需要對話 |
| 翻譯 | 無狀態轉換 |
| 自動完成建議 | 發射後不管 |

PM 經驗法則：如果使用者會期待 AI「記得之前」，那就是多輪情境，你必須明確為它設計。

---

## 成本曲線：PM 必須看得懂的一張圖

因為歷史每輪都重播，input token 線性成長：

```
   Input tokens
        │
20,000  │                                    ●
        │                               ●
        │                          ●
10,000  │                     ●
        │                ●
        │           ●
 5,000  │      ●
        │  ●
        └──────────────────────────────────────── Turns
          1    5    10   20   30    40    50
```

這有三個產品後果：

1. **單位經濟隨聊天長度變動。** 50 輪的 chat 大約是 10 輪的 25 倍 input token 成本。
2. **最終會撞 context window。** 每個 model 有歷史長度上限；長 chat 撞牆前需要策略（摘要、截斷、prompt cache）。
3. **沒有聊天長度分布就沒辦法預估成本。** 需要真實埋點資料，不是憑感覺。

---

## PM Decision Framework：記憶策略

Launch 前，每個 feature 挑一個記憶策略：

| 策略 | 做法 | 什麼時候用 |
|------|------|----------|
| **完整歷史** | messages list 永遠保留每一輪 | 短對話（< 20 輪）且 context 重要 |
| **Sliding window** | 只留最近 N 輪 | 長對話但最近 context 就夠 |
| **摘要** | 把舊輪壓成滾動摘要 | 長對話但早期 context 還是重要 |
| **Session reset** | 閒置或動作時明確結束並清空 | 以任務為單位、有明確完成的 chat |
| **Prompt caching** | 沒變的 prefix 便宜重用 | 長而穩定的 system prompt + 變動的尾巴 |

PRD 應該指定用哪個策略、使用者看起來會是怎樣。「使用者會記住幾輪」是 PM 能回答的問題，不是工程細節。

---

## Common PM Mistakes

1. **以為 Claude 預設會記得** —— 它不會；跳過這一課，你第一個 chat feature 會讓使用者覺得「笨笨的」。
2. **沒有聊天長度或預算上限** —— 一個 power user 200 輪的對話會花你真金白銀，要設限。
3. **混淆跨使用者 session** —— 後端 bug 讓兩個使用者共用 `messages` list 就是隱私事故；PM 的驗收條件必須要求隔離。
4. **忘記 reset 流程** —— 使用者需要「新對話」按鈕；沒有它，成本爬升 context 變陳舊。
5. **沒埋點聊天長度分布** —— 沒真實 chat 長度分布就沒辦法規劃預算或 eval prompt。

> **Key Insight**
>
> Statelessness 是偽裝起來的產品決策。API 給你一張白紙；你的產品定義「記憶」是什麼意思。感覺像魔法的 chat 產品都是刻意這麼做——他們決定哪些輪次重要、session 多久、成本怎麼 scale、chat「重置」時使用者看到什麼。忽略這件事的產品會做出慢、貴、健忘的 chat，然後怪 model。**在 PRD 裡擁有記憶策略，你就會出 feel smart 而且可預測的 feature。**

---

## CCA Exam Relevance

- **D1（Agentic Architecture）**：多輪就是 agent loop 的基礎。情境：「Claude 怎麼記住之前訊息？」→ client 每輪都重送。
- **D5（Enterprise Deployment）**：線性 token 成長對成本與 scale 的啟示。
- 情境觸發：「使用者反映 chatbot 會忘」→ 檢查 app 有沒有追加 assistant 回應並送完整歷史，不是改 prompt。

---

## Flashcards

| Front | Back |
|-------|------|
| Claude 在同一個 chat 裡會自動記得之前交流嗎？ | 不會——API 是 stateless；你的 app 每輪都要重播歷史 |
| 「金魚顧問」比喻是什麼？ | Claude 呼叫之間會忘，所以你每次新會議都要遞一份完整的過去會議逐字稿 |
| 為什麼長聊天成本比例失衡？ | Input token 隨歷史重播線性成長；50 輪 chat 大約是 10 輪的 25 倍 input token |
| PM 可以挑的記憶策略有哪些？ | 完整歷史、sliding window、摘要、session reset、prompt caching |
| Statelessness 對多使用者 app 引發什麼產品考量？ | Per-user 隔離——一個使用者的歷史絕不能洩漏到另一個 |
| 什麼時候單輪就夠？ | 每次互動獨立（摘要、翻譯、分類）、使用者不期待「記憶」 |
| Chatbot「會忘」時第一個該檢查什麼？ | App 有沒有追加 assistant 回應並每次呼叫送完整歷史 |
| PRD 該指定哪些記憶相關事項？ | 用哪個記憶策略、輪數/成本上限、「新對話」/session reset 怎麼運作 |
