# Extended Thinking — Engineering Deep Dive

| 項目 | 內容 |
|------|------|
| Exam Domain | D1 — Agentic Coding & Architecture (22%) — 主要；D5 — Enterprise Deployment (20%) — 次要 |
| Task Statements | 1.1（推理深度與 agent 決策品質）、1.2（agentic loop）、5.2（latency/cost 權衡） |
| Source | building-with-the-claude-api / 06-extended-features / Lesson 52 |

---

## One-Liner

Extended thinking 給 Claude 專屬的「草稿紙」token，讓模型在產出最終答案前先推理過一遍；用較高的成本和延遲換取單靠 prompt 無法穩定達成的準確度。

---

## 問題情境：當 prompt engineering 碰到天花板

每個嚴肅的 Claude 部署最終都會遇到一類 prompt——不論你怎麼調整指令、example、guardrail，準確率就是上不去。模型回答看起來合理，但對於難度較高的推理題，答案並不穩定正確。Extended thinking 就是為這個時刻設計的，它是你在**已經**優化過 prompt 與 eval 套件後，仍需要更多空間時才打開的功能。

把它當成 Claude 的草稿紙：模型會把推理過程寫在一塊內部工作區，做完草稿才產出最終回應。你用 token 付草稿紙的錢，等待更久，但最終答案是基於更長的內部思考而來。

---

## 回應結構：從一塊變兩塊

Extended thinking 關閉時，Claude 的回應就是一個簡單的 text block。打開之後，回應結構化成兩部分——一個 **thinking block**（推理軌跡）加一個 **text block**（最終答案）。

這會改變應用程式處理回應的方式。原本假設 `response.content[0].text` 的程式碼，現在必須迭代 content blocks 並區分 thinking 與使用者可見的 text。如果你把 Claude 的輸出直接渲染給使用者，必須決定要顯示推理過程、隱藏它、或收在「顯示推理」按鈕後面。

---

## 在程式碼裡啟用 thinking

課程教一個最小封裝，在 chat 函式上多開兩個參數：`thinking`（布林開關）與 `thinking_budget`（Claude 可花在推理的最大 token 數）。

```python
def chat(
    messages,
    system=None,
    temperature=1.0,
    stop_sequences=[],
    tools=None,
    thinking=False,
    thinking_budget=1024,
):
    ...
```

函式內部，當 `thinking` 打開時把 thinking 設定注入 API 參數：

```python
if thinking:
    params["thinking"] = {
        "type": "enabled",
        "budget": thinking_budget,
    }
```

呼叫方式：

```python
chat(messages, thinking=True)
```

兩條硬限制：

- **最小 budget 是 1024 tokens。** 不能再小。
- **`max_tokens` 必須大於 `thinking_budget`。** 因為 thinking 的預算是從 `max_tokens` 裡面扣的，`max_tokens` 必須容納推理軌跡與最終答案。

---

## 簽章系統

Extended thinking 的回應會帶上 thinking 內容的**加密簽章**。簽章是 Anthropic 偵測竄改的機制：如果開發者改動了 thinking 文字再把它送回下一輪，簽章就會驗證失敗，模型會拒絕這筆 history。

這是一個 safety 保證。Claude 的推理是 alignment training 的一部分——如果開發者能在 turn 之間改動推理文字，就能偽造一串合理化危險輸出的「chain of thought」，把模型誘導到不安全的區域。簽章就是為了堵住這個攻擊面。

實務意義：**絕對不要修改 thinking blocks**。把對話歷史送到下一輪時，連同簽章逐 byte 原樣送回。

---

## Redacted thinking blocks

有時候 Claude 的內部 safety 系統會對推理軌跡本身亮紅燈。這時候你拿到的不是可讀的推理文字，而是一個 **redacted thinking block**，裡面裝的是加密過的 payload。

兩件事很重要：

1. **遇到 redacted block 不能 crash。** 你的 content-block handler 必須把 redacted 當成一種合法的變體，和普通 thinking block、text block 一樣處理。
2. **原樣送回。** 雖然你的程式讀不出 redacted 的內容，Claude 在下一輪可以解密，所以把加密 payload 傳回去就能保留上下文。若你把它悄悄丟掉，等於截斷了 Claude 的記憶。

課程提到測試時可以送一個特殊的 trigger 字串強制 Claude 回傳 redacted 回應，拿來驗證你的 handler 不會在某些下游程式假設 thinking block 一定是可讀文字時掉鏈子。

---

## 成本與延遲的權衡

Extended thinking 不是免費的：

- **成本更高。** Thinking tokens 要計費，每次呼叫都吃 1024-token 的 thinking budget，規模化後就是真金白銀。
- **延遲更高。** 模型在吐出第一個 text token 之前要花更多實際時間。
- **客戶端程式更複雜。** Content-block 迭代、簽章處理、redacted 的 fallback。

指導原則：把 thinking 當成**準確度的調節桿**，標準 prompt engineering 之後才拉。決策流程：

1. 寫好 prompt。
2. 建立 eval set。
3. 反覆優化 prompt 直到準確率停滯。
4. 如果還是低於門檻，開 thinking 再跑一次 eval。

Thinking 解掉了就出貨。若沒解掉，代表問題不是推理深度的問題，需要換別的解法（tools、RAG、更好的 prompt 結構）。

---

## 功能相容性注意事項

課程明確點名 extended thinking 與某些其他功能**不相容**，特別是 **assistant message pre-filling** 與自訂 **temperature**。這在 production 裡很重要：如果你現有的 prompt 策略靠 pre-fill 的 assistant 訊息來引導輸出格式，就不能直接把 thinking 疊上去，必須重新設計那部分的 prompt。

完整的不相容清單放在 Anthropic docs，課程指向那份文件而不在此列出，因為清單會隨新模型演進。

---

## Common Mistakes

1. **在優化 prompt 之前就開 thinking。** Thinking 花錢又花時間。如果你的 prompt 根本寫錯，thinking 不會把它變對，你只是花更多錢得到同樣錯的答案。
2. **`max_tokens` ≤ `thinking_budget`。** API 會拒絕呼叫。`max_tokens` 必須能同時容納推理軌跡與最終答案。
3. **在 turn 之間修改 thinking blocks。** 任何修改都會破壞簽章，Claude 會拒絕 history。
4. **遇到 redacted thinking 就 crash。** 把 redacted 當一等公民處理，不要假設 thinking 內容永遠是可讀文字。
5. **把原始 thinking 直接丟給使用者看卻沒給 toggle。** 推理軌跡又長又偏內部，要嘛刻意呈現，要嘛預設隱藏。
6. **沒檢查相容性就把 thinking 和 assistant 預填或自訂 temperature 混用。** 呼叫會失敗或行為異常。

---

> **Key Insight**
>
> Extended thinking 是準確度的調節桿，不是預設值。正確的流程是：先優化 prompt，再建 eval，最後當 eval gap 明顯是推理深度問題時才開 thinking。簽章系統和 redacted blocks 是 safety 機制——把 thinking blocks 當成不透明物件，原樣傳遞，不要假設它永遠是可讀文字。

---

## CCA Exam Relevance

- **D1 (Agentic Coding & Architecture)**：Extended thinking 是在 agentic loop 內加深 Claude 推理的標準做法。預期會考「什麼時候 thinking 有幫助（難推理題）vs 什麼時候是浪費（簡單轉換）」。
- **D5 (Enterprise Deployment)**：成本/延遲權衡、`thinking_budget` vs `max_tokens` 的限制、以及相容性警告都是可直接命題的事實。
- 可能的題型：「Prompt engineering 已經碰天花板——下一個手段是什麼？」答案是 extended thinking，且要 eval-driven 決策。
- 記住兩個 safety 機制：**signature**（竄改偵測）和 **redacted blocks**（內部安全標記），兩者都必須原樣傳回。

---

## Flashcards

| Front | Back |
|-------|------|
| Extended thinking 解決什麼問題？ | Prompt engineering 已碰天花板的難推理題——它給 Claude 草稿紙 token，讓它在回答前深思熟慮。 |
| `thinking_budget` 的最小值是？ | 1024 tokens。 |
| `max_tokens` 和 `thinking_budget` 的關係？ | `max_tokens` 必須嚴格大於 `thinking_budget`，因為 budget 是從 max 裡扣的。 |
| 啟用 thinking 後會拿回哪兩種 content block？ | 一個 thinking block（推理軌跡）和一個 text block（最終答案）。 |
| Thinking block 上的 signature 是什麼？為何存在？ | 加密 token，用來證明 thinking 內容未被修改；防止開發者偽造 reasoning 來把模型引導到危險區。 |
| 什麼是 redacted thinking block？ | 推理被內部 safety 系統標記、以加密形式回傳的 thinking block。程式碼必須能處理並原樣傳回。 |
| 何時應該啟用 extended thinking？ | 只在優化 prompt、建好 eval、確認準確度仍因推理深度不足而低於門檻時才開。 |
| 舉兩個 extended thinking **不**相容的功能。 | Assistant message pre-filling 與自訂 temperature。 |
| 啟用 extended thinking 的三個代價？ | 成本更高（thinking tokens 計費）、延遲更高、客戶端程式更複雜（block 迭代、簽章、redaction）。 |
