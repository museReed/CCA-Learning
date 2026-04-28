# The Full RAG Flow — 工程深度解析

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Architecture (22%) 主要；D4 — Safety & Alignment (20%) 次要 |
| Task Statements | 1.3（context management）、4.1（grounded responses） |
| 來源 | building-with-the-claude-api / 05-rag / Lesson 48 |

---

## 一句話總結

完整 RAG flow 是一個六步 pipeline — chunk → embed → 存 → embed query → similarity search → 餵 prompt 給 Claude — 其中 cosine similarity 是把「找相關文字」轉換成「找最接近向量」的度量。

---

## 六個步驟

```
  [前處理 — 每份文件跑一次]
  1. 切 source text
  2. 為每個 chunk 產生 embedding
  3. 存進 vector database
                      │
                      ▼
  [查詢時 — 每次使用者請求跑]
  4. 把使用者 query 轉 embedding
  5. 找相似 embedding（cosine similarity）
  6. 用 retrieved chunks 組最後 prompt → Claude
```

步驟 1-3 是**前處理**，事先跑，每份文件一次。步驟 4-6 是**查詢時**，每次使用者請求都跑。這個切割就是 RAG 可擴展的原因：昂貴的工作做一次，便宜的工作每次 query 才做。

---

## Step 1：切 Source Text

把每份文件切成可管理的 chunks。lesson 用兩個 toy section：

- Section 1 — Medical Research：*"This year saw significant strides in our understanding of XDR-47, a 'bug' we have not seen before."*
- Section 2 — Software Engineering：*"This division dedicated significant effort to studying various infection vectors in our distributed systems."*

注意詞彙陷阱：醫療 section 用了「bug」，軟體 section 用了「infection vectors」。keyword search 會很開心地把兩者接錯線。RAG 必須做得比這好。

---

## Step 2：產生 Embeddings

每個 chunk 餵進 embedding model（本課程是 VoyageAI），拿回一個數值向量。

lesson 用**玩具二維模型**讓幾何看得見。在這個想像模型裡：

- 維度 1 = 「文字多談醫療領域」
- 維度 2 = 「文字多談軟體工程」

醫療 chunk 的 embedding 是 `[0.97, 0.34]` — 很醫療，但「bug」這個字造成一點軟體詞彙滲漏。軟體 chunk 是 `[0.30, 0.97]` — 偏重軟體，但「infection vectors」帶進一點醫療訊號。

真正的模型用數百或數千維度，無法按維度解讀。玩具模型存在只是為了說明 similarity 在幾何上長什麼樣子。

---

## Normalization（正規化）

大部分 embedding API 會把向量正規化成單位長度（magnitude 1.0）。數學自動處理，你通常不用自己做。正規化後：

- `[0.97, 0.34]` → `[0.944, 0.331]`
- `[0.30, 0.97]` → `[0.295, 0.955]`

你可以把正規化向量想成單位圓（或高維的單位超球面）上的點。正規化讓 **cosine similarity** 和 **dot product** 等價，也是 vector database 能最佳化 similarity search 的原因。

---

## Step 3：存進 Vector Database

Vector database 是最佳化過的專門儲存庫：

- **儲存**長長的 float list
- **搜尋**最接近 query 向量的向量（approximate nearest neighbor）
- **擴展**到百萬或十億級向量

這步完成後前處理就結束。pipeline 暫停，等使用者 query。到這裡為止的所有工作都會被未來所有 query 攤提。

---

## Step 4：處理 User Query

當使用者問*「I'm curious about the company. In particular, what did the software engineering dept do this year?」*，你把 query 餵進**同一個** embedding model（與 chunks 用同一個）。

玩具範例給的原始向量是 `[0.1, 0.89]` — 低醫療、高軟體工程。正規化後：`[0.112, 0.993]`。

重點：同一個模型。而且若 provider 支援，這裡用 `input_type="query"`（Step 2 的 chunks 則用 `input_type="document"`）。

---

## Step 5：用 Cosine Similarity 找相似 Embedding

把 query 向量送到 vector database，要求回傳最接近的儲存向量。

### Cosine Similarity 怎麼運作

Cosine similarity 衡量兩個向量之間夾角的餘弦：

- 範圍：**-1 到 +1**
- 接近 **+1** → 高相似度（向量幾乎同方向）
- 接近 **-1** → 非常不同（向量反方向）
- **0** → 垂直（沒有有意義的關聯）

玩具範例裡：

| 比對 | Cosine Similarity |
|------|-------------------|
| Query vs. 軟體 chunk | **0.983**（非常高） |
| Query vs. 醫療 chunk | 0.398（低很多） |

Vector database 回傳軟體 chunk — 正是使用者想要的，儘管兩個 chunks 有重疊詞彙（「bug」、「infection vectors」）。

### Cosine Distance

你也會在 vector database 文件看到 **cosine distance**，定義是 `1 - cosine_similarity`。用 cosine distance：

- 接近 **0** → 高相似度
- 較大值 → 較不相似

這通常比較好解讀，因為「距離」會隨東西越不相似而變大。同樣的底層數學，只是報告慣例不同。

---

## Step 6：組最後 Prompt

把使用者問題和 retrieved chunk(s) 組成 prompt 送給 Claude：

```
Answer the user's question about the financial document.

<user_question>
How many bugs did engineers fix this year?
</user_question>

<report>
## Section 2: Software Engineering
This division dedicated significant effort to studying various infection vectors in our distributed systems
</report>
```

Retrieved chunk 用 XML tag（`<report>`）包起來，讓 Claude 知道哪一部分是使用者問題、哪一部分是 grounding source。Claude 接著從組合後的 context 產出答案。

這是 retrieval-augmented generation 的「generation」那一半。注意 Claude 自己從未呼叫 vector database — 你的應用程式做的。從 Claude 角度看，它收到的是一個普通 prompt，只是有異常多的精心挑選 context。

---

## 為什麼詞彙陷阱是重點

「bug」例子特意構造來讓 keyword search 出糗。兩個 chunks 都含疾病類語言；基於關鍵字的 retriever 很可能對「how many bugs did engineers fix」回傳醫療 chunk。在 semantic embedding 上做 cosine similarity 能正確處理，因為 query 向量方向（軟體偏重）接近軟體 chunk 的方向。

這就是為什麼 embedding 重要：它測的是**語意**方向，不是**詞彙**重疊。

---

## CCA Task 對應

- **Task 1.3（Context Management）** — 整個 RAG flow 就是 context-management pipeline。前處理決定什麼可被檢索；retrieval 決定什麼進 context；prompt 組裝決定 Claude 怎麼看。
- **Task 4.1（Grounded Responses）** — 最終 prompt 把 Claude 的答案 grounded 在 retrieved chunks。用 XML tag 包 chunks 等於向模型表明「這是來源素材」。

---

## 常見錯誤

1. **忘了 query 要用和 chunks 同一個 embedding model** — 向量落在不相容空間，similarity score 變毫無意義。
2. **跳過 normalization** — provider 沒幫你正規化、且 database 用 dot product 時，非正規化向量會產生錯誤排序。
3. **回傳太多 chunks** — top-k 設太大會把低相關內容塞進 prompt，分散 Claude 注意力。
4. **最終 prompt 沒 XML／結構化標記** — Claude 分不出問題和來源素材，grounding 變弱。
5. **production 沒記錄 retrieval score** — 答案錯時需要 retrieved chunks 的 similarity score 來 debug 是 retrieval 問題還是 generation 問題。

> **關鍵洞察**
>
> 六步 RAG flow 其實是兩半黏在一起：**離線前處理 pipeline**（chunk → embed → 存），每份文件跑一次；**線上 query pipeline**（embed query → retrieve → prompt），每次請求跑。你未來會 debug 的每個 RAG bug 都住在這六步其中之一，所以要知道邊界在哪、哪一步擁有哪種失敗模式。

---

## CCA 考試關聯

- **D1（Agentic Architecture）**：端對端 RAG pipeline 是核心 agentic-pattern 題目。預期會看「RAG 步驟正確順序是什麼」或「cosine similarity 在 flow 裡的哪一步」這種題。
- **D4（Safety & Alignment）**：RAG grounding 降低幻覺。「bug」例子是好 retrieval 阻止自信錯答案的教科書案例。
- 要準備好定義 cosine similarity、它的範圍、和 cosine distance 的關係。

---

## Flashcards

| Front | Back |
|-------|------|
| 列出完整 RAG flow 的六個步驟。 | 1) 切文字、2) 產生 embedding、3) 存進 vector DB、4) Embed user query、5) 找相似 embedding（cosine similarity）、6) 組最終 prompt 呼叫 Claude。 |
| 哪幾步是前處理 vs. 查詢時？ | 1-3 是前處理（每份文件一次）；4-6 是查詢時（每次使用者請求一次）。 |
| Cosine similarity 的範圍？ | -1 到 +1。 |
| Cosine similarity 為 +1 代表什麼？ | 向量同方向 — 最高相似度。 |
| Cosine similarity 為 0 代表什麼？ | 向量垂直 — 沒有有意義的關聯。 |
| Cosine distance 怎麼定義？ | `1 - cosine_similarity`。小值 = 高相似度；大值 = 較不相似。 |
| 為什麼 query 和 chunks 必須用同一個 embedding model？ | 否則向量在不同幾何空間，similarity 失去意義。 |
| 什麼是 normalization、為什麼重要？ | 把向量縮到單位長度（magnitude 1.0）。讓 cosine similarity 和 dot product 等價，並支援有效率的 similarity search。 |
| 「bug」例子裡為什麼 cosine similarity 成功而 keyword search 失敗？ | 它比較語意方向不是詞彙重疊，所以 query 的軟體偏重方向匹配軟體 chunk，即使詞彙有重疊。 |
