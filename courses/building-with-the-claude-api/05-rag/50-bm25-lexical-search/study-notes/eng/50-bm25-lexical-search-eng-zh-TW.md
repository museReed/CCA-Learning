# BM25 Lexical Search — Engineering Deep Dive（工程深入）

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Architecture（22%）主領域；D5 — Enterprise Deployment（20%）次領域；D2 — Tool Design（18%）也相關（retrieval 作為 tool） |
| Task Statements | 1.3（context management）、5.2（production search infrastructure） |
| 來源 | building-with-the-claude-api / 05-rag / Lesson 50 |

---

## 一句話總結

BM25 是一個經典 lexical search 演算法，用來補語意搜尋的不足——穩定比對精確 term（ID、代號、罕見字），正是 embedding 悄悄失靈的那一半檢索品質。

---

## 問題：語意搜尋抓不到精確 term

想像你要在報告裡找 incident ID `INC-2023-Q4-011`。語意搜尋擅長概念相似——它知道「incident report」跟「cybersecurity event」相關——但它會回傳概念上接近卻**實際上沒有你要的 ID** 的段落。課程範例中，純語意搜尋查這個 incident ID 時，帶出了正確的 cybersecurity section，但也帶出了一個完全不相干的 financial analysis section。

為什麼？embedding 把文字壓縮成稠密 vector，罕見 token 會被平均掉。像 `INC-2023-Q4-011` 這種字面 string 幾乎沒有語意鄰居，所以包含它的問題的 embedding 被周圍的字主導——最後比對到的是那些字，不是那個 ID。

---

## Hybrid Search 策略

修正方式不是取代語意搜尋，而是**平行跑兩種**搜尋再合併：

- **Semantic search**——embedding、cosine similarity，擅長概念問題。
- **Lexical search**——經典 token 比對（BM25），擅長精確 term 命中。
- **Merged results**——合併兩者，回傳統一列表。

兩種方法互補，對方漏掉的我接住。合在一起就是更強韌的檢索層。

---

## BM25 怎麼運作

BM25（Best Match 25）對一個 query 用四步驟對 document 打分：

1. **Tokenize query**——把使用者問題斷成 term。`"a INC-2023-Q4-011"` 變 `["a", "INC-2023-Q4-011"]`。
2. **計算 term frequency**——每個 term 在所有 document 裡出現幾次。`"a"` 可能整份語料出現 5 次；`"INC-2023-Q4-011"` 可能只出現 1 次。
3. **用稀有度加權**——越稀有的 term 權重越高。常見字（`"a"`、`"the"`）幾乎不貢獻；罕見 term（`"INC-2023-Q4-011"`）主導整個分數。
4. **排序 document**——回傳累積加權 term frequency 最高的 document。

核心直覺：**到處都出現的 term 是 noise；只出現在一個地方的 term 是很強的 signal。** BM25 就是把這個直覺變成一個分數。

---

## 實作 BM25 搜尋

課程提供一個簡單包裝類別 `BM25Index`，API 和 `VectorIndex` 對齊：

```python
# 1. 用 section 切 chunk
chunks = chunk_by_section(text)

# 2. 建 BM25 store，加入 document
store = BM25Index()
for chunk in chunks:
    store.add_document({"content": chunk})

# 3. 搜尋
results = store.search("What happened with INC-2023-Q4-011?", 3)

# 印結果
for doc, distance in results:
    print(distance, "\n", doc["content"][:200], "\n----\n")
```

兩個 API 細節值得記住：

- `add_document({"content": chunk})`——document 用 dict payload 存，形狀跟 vector store 一樣，所以上層兩種 index 可互換。
- `store.search(query_text, k)`——吃 raw query text（BM25 自己做 tokenization，不需要 embedding 呼叫），回傳 top-k 的 (doc, distance) pair。

`INC-2023-Q4-011` 的查詢輸出現在正確地把字面提到 incident ID 的兩個 section——Software Engineering 跟 Cybersecurity——排在前面。

---

## 為什麼這對精確比對更好

BM25 擅長精確比對是因為它：

- **給罕見 term 高權重**——只出現一次的 incident ID 具有最大鑑別力。
- **忽略常見字**——類似 stop-word 的 term 貢獻幾乎為零。
- **按 term frequency 打分，不看意思**——沒有語意平滑化把字面 token 沖掉。
- **處理技術 token 很好**——ID、SKU、error code、function name、CVE 編號都受益。

反面：BM25 對概念相似度很弱。如果使用者問「上一季出了什麼事？」BM25 沒辦法把它配到標題叫「Cybersecurity Analysis」的段落。那正是語意搜尋的主場。

---

## API 一致性鋪陳下一課

注意 `BM25Index` 和 `VectorIndex` 共享幾乎相同的介面：

| 方法 | BM25Index | VectorIndex |
|------|-----------|-------------|
| `add_document(dict)` | 存 raw text | 存 vector + metadata |
| `search(query, k)` | 回 top-k BM25 分數 | 回 top-k cosine distance |

這不是巧合。一致 API 是下一課 multi-index Retriever 能成立的條件——單一 wrapper 把同一個 query 轉發到兩個 index，然後用 reciprocal rank fusion 合併結果。

---

## 常見錯誤

1. **以為語意搜尋能找到精確 ID**——經常找不到。任何 token literal 都該走 BM25。
2. **用 BM25 取代語意搜尋**——會失去概念理解能力。正確 pattern 是 hybrid，不是二擇一。
3. **BM25 前不切 chunk**——BM25 是對 document 打分；chunking 決定你的 document 粒度。
4. **BM25 payload 只存 text**——加上 metadata（section title、doc id）讓下游合併與 attribution 可以運作。
5. **跳過 normalization**——大小寫與標點差異會傷害 BM25。課程的基本 tokenizer 隱藏了這點，production 系統必須正視。

> **核心洞見**
>
> 語意搜尋處理意思；BM25 處理字面 token。Production RAG 系統幾乎都需要兩者，因為 user query 總是混著概念意圖和具體識別碼。Hybrid pattern 不是 optimization——它是預設選項。

---

## CCA 考試關聯

- **D1（Agentic Architecture）**：hybrid retrieval 是經典的進階 RAG pattern；要了解 semantic 與 lexical 的互補角色。
- **D5（Enterprise Deployment）**：BM25 跑起來很便宜（ingest 與 query 都不需要呼叫 embedding API），對成本與 latency 很重要。
- **D2（Tool Design）**：當你把 retrieval 包成 Claude 可以呼叫的 tool 時，知道這個 tool 是 BM25 / 語意 / hybrid 會影響你怎麼描述給模型。
- 題目 pattern：「語意搜尋對一個包含特定 ID 的 query 回傳不相關結果——要加什麼？」→ BM25 / hybrid search。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| BM25 是什麼縮寫？ | Best Match 25——一個經典 lexical search 演算法。 |
| BM25 解決語意搜尋的什麼問題？ | 漏掉精確 term 比對（ID、代號、罕見字），這些被 embedding 沖淡了。 |
| BM25 打分的四步驟是哪四個？ | 1) Tokenize query、2) 算 term frequency、3) 按稀有度加權、4) 按累積加權頻率排序 document。 |
| 為什麼罕見 term 在 BM25 權重較高？ | 因為鑑別力更高——只出現在一處的 term 是強 signal。 |
| BM25 query time 需要呼叫 embedding API 嗎？ | 不用——BM25 直接在 token 上運作，不需要 embedding。 |
| Hybrid search 是要用 BM25 取代語意搜尋嗎？ | 不是——hybrid 是平行跑兩種再合併，不是取代。 |
| `BM25Index` 跟 `VectorIndex` 共享哪些 API 方法？ | `add_document(dict)` 和 `search(query, k)`——一致的 API 讓統一的 Retriever 成立。 |
| BM25 什麼時候會失效？ | 當 query 是概念性的、和相關文件完全沒字面 token 重疊時。這時需要語意搜尋。 |
