# Response Streaming — 工程深度解析

| 項目 | 細節 |
|------|------|
| 考試領域 | D5 — Enterprise Deployment (20%) |
| Task Statements | 5.2（streaming 與回應速度）、5.3（production 模式） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 13 |

---

## 一句話總結

Response streaming 把單次 blocking API 呼叫換成 server-sent 的漸進事件流，讓你的 client 在 Claude 生成時就能把文字顯示出來，把使用者感受到的延遲從「10-30 秒的轉圈」降到「第一個 token 不到一秒」。

---

## 延遲問題

一次完整的 Claude completion 對長回應可能花 10 到 30 秒。非 streaming 的流程中，你的伺服器呼叫 `messages.create(...)`，等整段回應，再轉給 client。這幾秒間，使用者盯著轉圈沒有任何回饋——經典的「是不是壞了？」時刻，直接擊垮感受品質。

根本原因是長文生成是 token by token。就算 Claude 立刻開始產 token，預設 API 呼叫會把它們全部留在 server 端，直到訊息完成才給出來。

Streaming 的解法是**邊生成邊轉送部分輸出**——Claude 正在寫的字會在幾百毫秒內出現在使用者 UI 上。

---

## 為什麼感受延遲 > 實際延遲

總生成時間在 streaming 下不會改變。改變的是使用者看到的**第一個位元組時間**（TTFB）。人類對回應速度的感受來自第一個可見的生命跡象，不是完成時間戳。15 秒的 streamed 回應感覺比 5 秒的 blocking 回應快，因為使用者看到文字持續出現。

這是基本 UX 原則：進度指示和漸進渲染勝過轉圈。Streaming 就是使用者現在從任何 LLM 產品期待的 ChatGPT 式體驗。

---

## Stream Event 類型

`stream=True` 時，API 會送出一連串有型別的 events，而不是單一回應。課程涵蓋六種 event 類型：

| Event | 意義 |
|-------|------|
| `MessageStart` | 新訊息開始 |
| `ContentBlockStart` | 新 content block 開始（text、tool_use 等）|
| `ContentBlockDelta` | 一塊生成文字（或其他 content delta）|
| `ContentBlockStop` | 當前 content block 完成 |
| `MessageDelta` | 頂層訊息 metadata 更新 |
| `MessageStop` | Stream 結束 |

`ContentBlockDelta` events 載著你要顯示的實際 token chunks。其他載結構性 metadata（你在哪個 block、訊息是否完成）。

純文字 UI 只需要 deltas。對更豐富的整合（tool use、多 content blocks），start/stop events 告訴你當前該把內容 append 進哪個 block。

---

## 用原始 Events 做基礎 Streaming

最直白的形式是直接 iterate events：

```python
from anthropic import Anthropic

client = Anthropic()

messages = [{"role": "user", "content": "Write a 1 sentence description of a fake database"}]

stream = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=messages,
    stream=True,
)

for event in stream:
    print(event)
```

這給你所有 event 類型的順序。適合 debug 或建立需要對 tool_use delta 和 text delta 分開處理的 custom dispatch 邏輯。

---

## 用 SDK 做簡化的 Text Streaming

對常見情況——「我只要 text chunks 一來就拿到」——SDK 提供更高層級的 helper：

```python
with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=messages,
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

和原始形式的關鍵差異：

- 用 `client.messages.stream(...)`（不是 `.create(..., stream=True)`）
- 用 `with` context 管理——確保底層 HTTP 連線被清掉
- `stream.text_stream` 只 yield text chunks。所有結構事件都幫你過濾掉
- `flush=True` 很重要——不加 buffering 會把 streaming 效果藏起來

這是你在 90% production chat UI 會用的形式。

---

## Streaming 後取得最終訊息

Streaming 對使用者很好，但你的 backend 通常還需要完整訊息給：

- 資料庫儲存（chat history）
- Analytics / logging
- 餵到下一輪對話
- 計算 token 用量 / 費用

Stream 結束後，你可以取得組好的訊息：

```python
with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=messages,
) as stream:
    for text in stream.text_stream:
        send_chunk_to_client(text)

    final_message = stream.get_final_message()
    store_in_database(final_message)
```

這是兩全其美的模式：client 看到 streamed tokens，伺服器最終拿到完全結構化的 `Message` 物件（content blocks、stop_reason、usage 等）。

---

## 架構：Streaming 的位置

典型 streaming chat stack 長這樣：

```
Browser ──HTTP/WebSocket/SSE──▶ 你的伺服器 ──Anthropic SDK stream──▶ Claude API
   ▲                              │  │
   │                              │  └──(在 MessageStop) 存 final_message 進 DB
   └─────────── chunks ───────────┘
```

你的伺服器實質上是一個 proxy：

1. 接受使用者請求
2. 對 Anthropic 開啟 streaming 呼叫
3. 把每個 text chunk 轉給瀏覽器（透過 SSE 或 WebSocket）
4. 完成時把最終訊息寫到資料庫

關鍵：**不要**把你的 Anthropic API key 暴露給瀏覽器。就算直接 streaming 在技術上做得到，為了安全也必須走 streaming proxy 模式。

---

## Streaming 和 Tool Use

Tools 開啟時 streaming 仍然有效，但 event 類型會更豐富——你會在 stream 裡看到 `tool_use` content blocks。你要嘛用原始 event loop 處理，要嘛靠 SDK helper 自動組裝。純文字 UI 用 `stream.text_stream` 會隱藏 tool_use 噪音；顯示「Claude 正在呼叫 tool X…」的 agentic UI 就要原始 events。

---

## 常見錯誤

1. **Chat UI 不用 `stream=True`**——預設 blocking 行為對長回應是糟糕 UX。Streaming 是 production 預設模式，不是優化
2. **忘了 context manager**——`client.messages.stream(...)` 必須用 `with`，否則 HTTP 連線會漏
3. **忽略非 delta events**——只看 `ContentBlockDelta` 會錯過 stop reason、tool_use blocks、usage metadata
4. **不呼叫 `get_final_message()`**——你會失去結構化訊息，必須自己從 chunks 重組
5. **從瀏覽器直接 stream 到 Anthropic**——這會洩漏你的 API key。永遠經過自己的伺服器 proxy

> **Key Insight**
>
> Streaming 不會讓 Claude 更快——它讓 Claude *感覺*快，把感受延遲從回應結束挪到第一個 token。這是原型 LLM 應用和 production 應用在 UX 上最重要的單一差別。任何面向使用者的 chat 體驗，streaming 是必要，不是可選。

---

## CCA 考試重點

- **D5.2（streaming 與回應速度）**：預期會直接考如何啟用 `stream=True`、區分 `messages.create(stream=True)` vs `messages.stream(...)`、以及知道 event 類型
- **D5.3（production 模式）**：streaming 是 production chat UI 的標準模式——注意圍繞使用者感受延遲的考題
- 記住 event 名稱（`MessageStart`、`ContentBlockStart`、`ContentBlockDelta`、`ContentBlockStop`、`MessageDelta`、`MessageStop`）——這些會考

---

## Flashcards

| 題目 | 答案 |
|------|------|
| 怎麼在原始 Anthropic API 呼叫啟用 streaming？ | 把 `stream=True` 傳給 `client.messages.create(...)` |
| Streaming text 的高層 SDK 方法是什麼？ | `client.messages.stream(...)`——搭配 `with` context manager 使用 |
| 哪個 event 類型含實際生成的 text chunks？ | `ContentBlockDelta`——載著漸進的 text（或其他 content）delta |
| 主要六個 stream event 類型是什麼？ | MessageStart、ContentBlockStart、ContentBlockDelta、ContentBlockStop、MessageDelta、MessageStop |
| Streaming 會降低總生成時間嗎？ | 不會——總時間一樣。它透過邊生成邊顯示文字來降低使用者感受延遲 |
| 怎麼在 streaming 結束後取得完整組好的訊息？ | 在 `with` block 內 iterate `stream.text_stream` 後呼叫 `stream.get_final_message()` |
| `stream.text_stream` 過濾掉什麼？ | 所有非 text 結構事件——只 yield 純 text chunks |
| 為什麼 streaming 要走自己的伺服器而不是瀏覽器？ | 為了不暴露你的 Anthropic API key。伺服器當 streaming proxy |
| 在 streaming 語境下「time to first byte」是什麼？ | 使用者看到第一塊生成文字前的延遲——對感受速度才是關鍵的數字 |
