# Text Embeddings — 工程深度解析

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Architecture (22%) 主要；D4 — Safety & Alignment (20%) 次要 |
| Task Statements | 1.3（context management）、4.1（grounded responses） |
| 來源 | building-with-the-claude-api / 05-rag / Lesson 47 |

---

## 一句話總結

Text embedding 是一個捕捉文字意義的數值向量；RAG retrieval 的做法就是把 user query 和儲存的 chunks 都轉成 embedding，再找出向量與 query 最接近的 chunks。

---

## Retrieval 問題

切完 chunk 之後，你手上有一堆文字片段。使用者提問時，你要找出哪些 chunks 與問題相關。這本質上是**搜尋問題** — 「掃所有 chunks，找出與 query 相關的」。

兩種做法：

- **Keyword search** — 找完全匹配的字。快、簡單，但遇到同義字、改寫、共享概念但無共享字詞的情況會失敗。
- **Semantic search** — 找*意義*最接近 query 的 chunks，不管確切字詞。這是 RAG 預設，由 embeddings 支撐。

使用者用自然語言問問題、且不一定鸚鵡學舌文件用語時，semantic search 是對的工具。「這家公司賺了多少？」應該要能匹配到標題為「Revenue」的 chunk，即使沒有共享關鍵字。

---

## 什麼是 text embedding？

Text embedding 是某段文字**意義的數值表示**。想像成把字和句子轉換成電腦可以用數學比較的格式。

流程：

- 你把文字餵進 **embedding model**
- 模型輸出一個很長的**數字 list**（embedding 向量）
- 每個數字範圍 **-1 到 +1**
- 每個數字代表輸入文字的某種學到的特徵或品質

---

## 理解這些數字

embedding 裡每個數字本質上是某種輸入品質的「分數」。重點警告：**我們無法精確知道每個數字代表什麼**。

會很想說「第 42 維代表文字有多快樂」或「第 17 維代表文字多談海洋」，但這些只是概念示意。每個維度的實際語意是模型在訓練時學到的，人類無法直接解讀。

對 RAG 重要的不是每個維度*代表什麼*，而是意義相似的文字會產生相似的向量。模型保證**幾何**，我們不需要解讀軸。

---

## 用 VoyageAI 做 embeddings

Anthropic 目前不提供 embedding 生成。推薦 provider 是 **VoyageAI**。

設定步驟：

1. 申請 VoyageAI 帳號（與 Anthropic 分開）
2. 取得 API key（免費起步）
3. 把 key 加到環境變數

在 `.env` 加：

```
VOYAGE_API_KEY="your_key_here"
```

這是部署時要注意的 D5 相關重點：RAG pipeline 引入**第二個 vendor**到你的 stack，有自己的 key、rate limit、定價、SLO。

---

## 實作

安裝 library：

```
%pip install voyageai
```

設定 client 與 helper function：

```python
from dotenv import load_dotenv
import voyageai

load_dotenv()
client = voyageai.Client()

def generate_embedding(text, model="voyage-3-large", input_type="query"):
    result = client.embed([text], model=model, input_type=input_type)
    return result.embeddings[0]
```

要注意：

- `client.embed` 吃的是**文字 list**，不是單一字串 — API 是 batched。embedding 所有 chunks 時可以（也應該）一次傳多筆。
- `result.embeddings` 是跟輸入 list 對齊的 list；單筆情況取 `[0]`。
- `input_type` 有差：「query」vs.「document」。許多 embedding 模型有非對稱調校，即使同一段文字，query 和 document 產出的向量會略有不同。
- `model="voyage-3-large"` 是 lesson 的範例 — 依品質／成本／延遲目標挑模型大小。

對 chunk 跑這個 function 會回傳一個 floating-point 數字 list — 就是 embedding。流程本身簡單；真正挑戰在**有效率地**用 embedding 做 retrieval。

---

## Embeddings 在 RAG pipeline 的位置

```
┌──────────────┐    chunk       ┌──────────────┐   每個 chunk 都 embed  ┌──────────────┐
│   Document   │ ─────────────▶ │    Chunks    │ ───────────────────▶ │   Vectors    │
└──────────────┘                └──────────────┘                      └──────────────┘
                                                                            │
                                                                            ▼
┌──────────────┐  embed query   ┌──────────────┐   比對向量              ┌──────────────┐
│  User query  │ ─────────────▶ │ Query vector │ ───────────────────▶ │  Top-k chunks│
└──────────────┘                └──────────────┘                      └──────────────┘
```

embedding 會被叫**兩次**：

1. **前處理時** — corpus 裡每個 chunk 都被 embed 並儲存。
2. **查詢時** — 每個進來的 user query 被 embed，那個向量拿去和儲存的 chunk 向量比對。

比對兩邊必須用同一個 embedding model。混用模型產生的是不同幾何空間的向量，similarity score 會變得毫無意義。

---

## Query vs. Document input type

VoyageAI 曝露 `input_type` 參數，有 `"query"` 和 `"document"` 這種值。lesson 的範例 function 用 `input_type="query"`。在完整 pipeline 裡：

- embed **要儲存的 chunks** 時傳 `input_type="document"`
- embed **查詢時的 user 問題**時傳 `input_type="query"`

模型被調校過，讓 query embedding 能和 document embedding 最好地對齊。這個小細節可以測得出 retrieval 品質差異。

---

## CCA Task 對應

- **Task 1.3（Context Management）** — embedding 是你挑選哪些 chunk 變成 context 的機制，是 context 挑選的「評分函數」。
- **Task 4.1（Grounded Responses）** — grounding 品質取決於 retrieve 到的 chunks 對不對；embedding 是第一個控制這件事的槓桿。

---

## 常見錯誤

1. **index 和 query 用不同 embedding model** — 向量在不同空間；相似度變胡說。
2. **`input_type` 沒用對** — provider 支援時，document 和 query 要用各自對應的 input type。
3. **每次 query 都 re-embed chunks** — chunks 前處理時 embed 一次、存好向量、反覆用。runtime 只 embed query。
4. **忘了預留 VoyageAI 的延遲與成本** — embedding API 呼叫是每次 query 的新 network hop；對 p99 延遲和每次查詢成本有影響。
5. **以為維度可解讀** — 你無法「看某個維度」來 debug retrieval 失敗；debug 永遠是比對整個向量。

> **關鍵洞察**
>
> Embedding 把「哪個 chunk 對這個 query 最相關」化約成「哪個向量對這個向量最接近」。這就是全部的 trick。你不需要理解個別維度代表什麼 — 只需要相信模型把語意相似的文字放在向量空間中靠近的位置。RAG retrieval 的全部藝術在於挑一個好的 embedding model、並正確地比對向量。

---

## CCA 考試關聯

- **D1（Agentic Architecture）**：embedding 是 RAG retrieval 的搜尋骨幹。熟悉它是什麼、怎麼產生、為什麼能做 semantic search。
- **D4（Safety & Alignment）**：更好 retrieval → 更好 grounding → 更少幻覺。embedding 是 retrieval 品質的起點。
- 預期考題像「Anthropic 不提供 embeddings — 推薦的 provider 是？」（VoyageAI）、「embedding 值範圍是？」（每個維度 -1 到 +1）。

---

## Flashcards

| Front | Back |
|-------|------|
| 什麼是 text embedding？ | 一段文字意義的數值向量表示，用於 semantic search。 |
| embedding 裡每個數字的範圍是？ | -1 到 +1。 |
| Anthropic 提供 embedding 嗎？ | 不 — lesson 推薦 VoyageAI 當 embedding provider。 |
| VoyageAI 用哪個環境變數？ | `.env` 裡的 `VOYAGE_API_KEY`。 |
| Semantic search 和 keyword search 有何不同？ | Semantic search 透過向量相似度比對意義；keyword search 只比對確切字。 |
| `input_type` 參數做什麼？ | 告訴 embedding model 輸入是 query 還是 document；模型用非對稱調校最佳化 retrieval 品質。 |
| RAG pipeline 裡 embedding model 會被叫幾次？ | 前處理時很多次（每個 chunk 一次），runtime 每個進來的 user query 一次。 |
| 為什麼 index 和 query 混用不同 embedding model 是錯的？ | 向量在不同空間，similarity 失去意義。 |
