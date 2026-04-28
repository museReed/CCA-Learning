# Making a Request — PM Perspective（繁體中文）

| 項目 | 內容 |
|------|------|
| Exam Domain | D5 — Enterprise Deployment (20%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 5.1（model selection）、5.3（production patterns）、1.2（agentic loop 基礎） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 06 |

---

## One-Liner

單一 Claude 請求是任何 AI feature 最小的產品價值單位——三個參數決定 feature 的品質、成本、失敗模式。所以 PM 要像 review UI 文案那樣 review `model`、`max_tokens`、`messages`。

---

## Mental Model：販賣機交易

把 `client.messages.create()` 想成販賣機：

| 販賣機 | Claude 請求 |
|-------|------------|
| 選機台（咖啡 vs 汽水） | 選 `model`（Sonnet、Haiku、Opus） |
| 投正確的錢 | 提供 API key |
| 按按鈕（哪個商品） | 送 `messages`（prompt） |
| 機台吐出最多一份商品 | Claude 回最多 `max_tokens` 的內容 |
| 收據含價格 | `response.usage` 含 input/output token 數 |

你產品裡每個 feature 都是幾千次這種交易組成的系統。品質、成本、延遲都是三個參數選擇的湧現結果。

---

## 三個參數就是產品決策

### Model

選 model 是偽裝成技術決策的產品決策。它在速度、能力、成本之間取捨。

| Model 檔次 | 適合 | PM 考量 |
|-----------|------|--------|
| Sonnet（平衡） | 大多數 feature 的 default | 好基準，從這裡開始 |
| Haiku（快、便宜） | 摘要、分類、高量 | 每次呼叫便宜，難題可能錯過細節 |
| Opus（最強） | 推理重的 feature、複雜草稿 | 每次呼叫貴，留給高價值流程 |

注：課程裡的 model 名稱是範例；實際用的時候永遠跟工程師確認當代 model（例如 `claude-sonnet-4-5`）。

### `max_tokens`

這是你每次呼叫的成本上限。對 `max_tokens` 沒意見的 PM，等於讓工程師默默決定 feature 品質。

| Feature 類型 | 建議 max_tokens | 理由 |
|-------------|----------------|------|
| 聊天回應 | 500–1000 | 短回應，留空間給細節 |
| 文件摘要 | 1000–2000 | 有界但需要喘息空間 |
| 長篇草稿（email、blog） | 2000–4000 | 除非要快，否則值得花錢 |
| 分類 / 路由 | 50–100 | 單 token 答案，浪費 token = 浪費錢 |

**關鍵釐清**：`max_tokens` 是上限，不是目標。想要更長的輸出，要在 prompt 裡要求，不是把上限調高。

### `messages`

Messages list 是你的「對話狀態」。單輪 feature（問答、摘要）只有一個 entry。多輪 feature（chat、agent）會長大。Lesson 07 會細講多輪。

---

## Product Use Cases

### 單次請求就夠的時候

| Feature | 為什麼單輪就夠 |
|---------|--------------|
| 「幫我摘要這份文件」 | 一問一答 |
| 「翻譯這段文字」 | 無狀態轉換 |
| 「分類這張 ticket」 | 路由決策，沒有後續 |
| 「把這封信改成更友善的語氣」 | 發射後不管的轉換 |

### 需要不只一次呼叫的時候

| Feature | 為什麼單輪不夠 |
|---------|--------------|
| 帶歷史的聊天 | 需要 `messages` 隨時間成長（Lesson 07） |
| 使用 tool 的 agent | 需要依 `stop_reason` 分支的 loop（Lesson 32+） |
| Streaming 輸出 | 同一個呼叫加 `stream=True` flag |

---

## PM Decision Framework：Pre-Launch 問卷

Claude feature 出貨前，PRD 要回答這些問題：

| 問題 | 預設 |
|------|------|
| 要呼叫哪個 model？ | 沒特別原因就 Sonnet 起跳 |
| `max_tokens` 設多少？ | 合理回應最長長度 × 1.5 |
| 單輪還是多輪？ | 預設單輪，除非使用者要追問 |
| 典型一次呼叫多少錢？ | 計算：（平均 input + output token）× 價格 |
| 呼叫中給使用者看什麼？ | Loading state、streaming、optimistic UI |
| `stop_reason == "max_tokens"` 怎麼辦？ | 定義截斷 UX |
| 怎麼測 prompt 品質？ | Eval harness 或人工 review loop |

---

## 成本經濟學白話版

每次呼叫有兩個成本部分：

- **Input tokens** —— 你送出去的所有東西長度（system prompt + messages）
- **Output tokens** —— Claude 回應的長度

你每方向每百萬 token 付錢。PM 的啟示：

| 槓桿 | 對成本的影響 |
|------|-------------|
| 較短的 prompt | 線性便宜 input |
| 較緊的 `max_tokens` | 蓋住最壞情況 output 成本 |
| 較小的 model | 顯著便宜但可能降品質 |
| 把多個問題 batch 成一次呼叫 | 省每呼叫 overhead 但失敗會綁一起 |
| 用 tool use 取代巨大 context window | 每呼叫 input token 變少（Lesson 32+） |

經驗法則：多數 feature 的帳單被 input token 主宰，因為你一直重送 context。Lesson 07（多輪）會讓這個效應戲劇化。

---

## Common PM Mistakes

1. **對 `max_tokens` 沒意見** —— 讓工程師默默決定 feature 品質上限，而你不知道被蓋住了。
2. **以為 model 越大越好** —— 分類和路由 Haiku 比 Sonnet 在成本上完勝，而且使用者察覺不到差別。
3. **PRD 跳過 prompt 迭代** —— Prompt 是產品文案，應該跟 UI 文字一樣 review。
4. **沒編 prompt eval infra 的預算** —— 沒辦法量品質就沒辦法安全做 A/B。
5. **以為單輪永遠比較便宜** —— 長期 chat 如果硬做單輪，重送 context 比多輪更浪費 token。

> **Key Insight**
>
> `messages.create()` 三個參數不是技術小常識——它們是任何 Claude feature 的三大產品決策：能力（model）、成本上限（max_tokens）、對話設計（messages）。PRD 裡三個都明確簽核的 PM，feature 會打中成本與品質目標。三個都丟給工程師的 PM，feature 會默默 miss 目標然後被怪「AI 不行」。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）**：情境題問 model selection、`max_tokens` 大小、成本取捨。
- **D1（Agentic Architecture）**：每個 agent 都是在這個單一呼叫上跑 loop；熟悉原子單位是前置。
- 情境觸發：「AI feature 太慢/太貴/太短」→ 答案通常都住在三個參數其中一個。

---

## Flashcards

| Front | Back |
|-------|------|
| `messages.create()` 三個跟產品有關的參數是什麼？ | `model`（能力）、`max_tokens`（成本上限）、`messages`（對話設計） |
| `max_tokens` 是設目標還是上限？ | 上限——想要更長的輸出要在 prompt 裡要求，不是調高上限 |
| 為什麼 PM 該對 model 選擇有意見？ | 它在成本、速度、能力之間取捨；沒 PM 介入工程師會預設一個 |
| 什麼時候該用較小的 model（Haiku）？ | 分類、路由、高量摘要——使用者察覺不到差別的地方 |
| 每次呼叫的兩個成本部分是什麼？ | Input tokens（送出去）與 output tokens（Claude 寫的） |
| Claude 呼叫符合什麼販賣機比喻？ | 選機台（model）、投錢（API key）、按鈕（messages）、拿商品上限一份（max_tokens）、收據（usage） |
| 為什麼 prompt 品質是 PM 的事？ | Prompt 是產品文案，決定輸出品質，值得 PRD 等級的關注 |
| A/B 測 prompt 前需要什麼？ | Prompt 評估 infra 來量品質變化 |
