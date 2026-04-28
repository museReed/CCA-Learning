# Implementing the RAG Flow — Engineering Deep Dive（工程深入）

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Architecture（22%）主領域；D5 — Enterprise Deployment（20%）次領域 |
| Task Statements | 1.3（context management）、5.2（production search infrastructure） |
| 來源 | building-with-the-claude-api / 05-rag / Lesson 49 |

---

## 一句話總結

實作 RAG 是一條五步驟 pipeline：切 chunk、生 embedding、把 vector 和原文一起存、對 user query 生 embedding、用 cosine similarity 搜尋——把語意檢索變成具體、可重現的 code 流程。

---

## RAG 五步驟 Pipeline

```
┌──────────┐  1. chunk_by_section   ┌──────────┐
│ report   │ ─────────────────────▶ │  chunks  │
│  .md     │                         └────┬─────┘
└──────────┘                              │
                                          ▼
                               2. generate_embedding(chunks)
                                          │
                                          ▼
                               3. VectorIndex.add_vector(
                                      embedding,
                                      {"content": chunk})
                                          │
                   ┌──────────────────────┘
                   ▼
        4. user_embedding = generate_embedding(question)
                   │
                   ▼
        5. store.search(user_embedding, k=2)
                   │
                   ▼
         [(doc, distance), ...]
```

RAG 這個概念——「回答前先找出相關文字」——全部可以壓縮成這五個固定步驟。檢索端沒有魔法；魔法全部在把文字映射到有意義向量空間的 embedding 模型裡。

---

## 步驟 1：切 chunk

```python
with open("./report.md", "r") as f:
    text = f.read()

chunks = chunk_by_section(text)
chunks[2]  # 測試看是否正確切到目錄
```

先前課程介紹的 `chunk_by_section` function 會把文件切成邏輯上的段落。每個 chunk 變成可獨立檢索的單位。切法很關鍵：切太小會失去上下文；切太大 embedding 會稀釋掉鑑別度。

---

## 步驟 2：批次產生 embedding

```python
embeddings = generate_embedding(chunks)
```

embedding helper 同時支援單一 string 和 list of strings，所以整份語料可以一次呼叫產出。這點在 production 很重要，因為 embedding API 通常按次計費，批次呼叫遠比 N 次個別呼叫便宜又快。

---

## 步驟 3：存進 vector database

```python
store = VectorIndex()

for embedding, chunk in zip(embeddings, chunks):
    store.add_vector(embedding, {"content": chunk})
```

注意 payload 是 `{"content": chunk}`。vector 只是 record 的一半——另一半是原始文字（或指向原文的 reference）。沒有原文的話，nearest-neighbor 搜尋回來的只是無意義的浮點數，根本沒東西能塞回 Claude。

### 為什麼要存原文？

query 時必須回傳實際的內容塞進 prompt。embedding vector 只是 index 的 key；value 必須是人類可讀的文字。變化做法包括：

- 完整 chunk 文字（最單純）
- 一個 pointer（doc_id + offset）晚點才取回
- 文字再加上 metadata（section title、source URL、timestamp）

---

## 步驟 4：對 user query 生 embedding

```python
user_embedding = generate_embedding(
    "What did the software engineering dept do last year?"
)
```

關鍵是**語料與 query 必須用同一個 embedding model**。混用模型會產生不相容的向量空間，similarity 分數就變沒意義。

---

## 步驟 5：用 cosine distance 搜尋

```python
results = store.search(user_embedding, 2)

for doc, distance in results:
    print(distance, "\n", doc["content"][0:200], "\n")
```

`store.search(query_vector, k)` 回傳前 k 個最近的 document，連同 distance。distance 越小 = similarity 越高。課程範例中：

- Section 2（Software Engineering）→ distance 0.71（最接近）
- Methodology section → distance 0.72（第二接近）

這個排序就是你交回給 Claude 當 grounded context 的內容。

---

## 接下來：純語意搜尋的極限

這堂課結尾有個警告：這個基本流程對乾淨的語意問題可以，但碰到需要**精確 term 比對**（incident ID、product SKU、error code）就會失靈。這正是後面課程要導入 BM25 與 hybrid retrieval 的原因。

---

## 常見錯誤

1. **只存 embedding 不存原文**——失去把實際內容回傳給 Claude 的能力。
2. **語料與 query 用不同 embedding 模型**——向量空間不相容，similarity 就變垃圾。
3. **跳過 batch embedding**——每個 chunk 個別呼叫在 production 又慢又貴。
4. **忽略 chunk 大小**——過大稀釋相關度；過小喪失上下文。
5. **把 distance 回給使用者**——distance 是 debug 訊號，不是產品輸出。回傳 content，log distance。

> **核心洞見**
>
> RAG pipeline 本身是一個**確定性的前處理 + 查詢**工作，不是 AI feature。智慧完全來自 (a) 把語意映射到幾何的 embedding 模型 (b) 下游在 retrieved chunks 上推理的 LLM。讓 pipeline 保持無聊、可替換，品質就會從你能獨立升級的元件身上長出來。

---

## CCA 考試關聯

- **D1（Agentic Architecture）**：RAG 是 context management 的經典 pattern。題目常包裝成「我要怎麼讓 Claude 認識它原本不知道的東西？」
- **D5（Enterprise Deployment）**：vector store 選型、embedding 成本、batch 處理、pipeline 新鮮度都是 deployment/scale 題目會出現的 production 議題。
- 注意會有誤導選項建議「fine-tune」來解決「Claude 不認識我們內部文件」——RAG 幾乎都是正解。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| RAG 流程有哪五個步驟？ | 1) 切文字、2) 對每個 chunk 產 embedding、3) 把 embedding + 原文存進 vector index、4) 對 user query 產 embedding、5) 在 store 中搜 top-k 最近的 chunks。 |
| 為什麼必須把原文和 embedding 一起存？ | query 時要把實際內容餵給 Claude——只有 embedding 的話是一堆看不懂的浮點數。 |
| 語料與 query 必須用同一個 embedding 模型嗎？ | 是。不同模型產生不相容的向量空間，cosine similarity 就變沒意義。 |
| `store.search(user_embedding, 2)` 回傳什麼？ | 一個 (document, distance) tuple 的 list——最接近的兩個 chunks 和它們的 cosine distance。 |
| 課程範例中，「What did the software engineering dept do last year?」的最接近結果是？ | Section 2（Software Engineering），distance 0.71。 |
| distance 越低代表 similarity 越高還是越低？ | 越低 = similarity 越高（在向量空間中越接近）。 |
| 為什麼要批次 embed 而不是 loop 逐筆？ | embedding API 按次計費，批次處理便宜又低延遲。 |
| 下一課要解決純語意搜尋的哪個極限？ | 精確 term 比對，例如 incident ID——語意搜尋可能漏掉字面上的 token match。 |
