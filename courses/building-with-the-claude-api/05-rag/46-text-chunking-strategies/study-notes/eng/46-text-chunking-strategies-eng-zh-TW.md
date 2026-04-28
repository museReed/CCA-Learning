# Text Chunking Strategies — 工程深度解析

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Architecture (22%) 主要；D4 — Safety & Alignment (20%) 次要 |
| Task Statements | 1.3（context management）、4.1（grounded responses） |
| 來源 | building-with-the-claude-api / 05-rag / Lesson 46 |

---

## 一句話總結

Chunking 是 RAG 裡決定「可檢索單位」長什麼樣子的步驟，爛的 chunking 策略會默默毒死所有下游 retrieval，把不相關內容塞進 prompt、產出很有信心的錯答案。

---

## 為什麼 chunking 是槓桿最大的一步

想像一份文件有兩個 section：醫療研究和軟體工程。使用者問「How many bugs did engineers fix this year?」。如果 chunking 爛，醫療 section 裡出現的「bug」（像是「XDR-47, a bug we have not seen before」）就會被抓進 context，結果 Claude 很開心地回答病毒的事，而不是軟體缺陷。

這就是核心失敗模式：**chunk 看起來相關只是因為共享關鍵字，但周圍語意是不一樣的**。chunking 決定語意相似度被評估的粒度。太粗，chunk 混主題；太細，chunk 失去 context。

---

## 策略 1：Size-Based Chunking

最簡單的做法 — 把文字切成等長字串。325 字元的文件可能變成三個 ~108 字元的 chunks。

**優點：**
- 實作超簡單
- 適用任何文件型態（文字、code、log 任意內容）
- chunk 數量與大小可預測

**缺點：**
- 字會被切在句子中間
- chunk 失去周邊文字的重要 context
- section header 可能被從內容中切開

### 解法：加上 Overlap

Overlap 代表每個 chunk 包含鄰近 chunk 的部分字元 — 形成滑動視窗保留邊界 context。

```python
def chunk_by_char(text, chunk_size=150, chunk_overlap=20):
    chunks = []
    start_idx = 0

    while start_idx < len(text):
        end_idx = min(start_idx + chunk_size, len(text))
        chunk_text = text[start_idx:end_idx]
        chunks.append(chunk_text)

        start_idx = (
            end_idx - chunk_overlap if end_idx < len(text) else len(text)
        )

    return chunks
```

兩個要注意的點：
1. loop 實際上前進 `chunk_size - chunk_overlap` — overlap 縮小淨步長。
2. 終點分支設 `start_idx = len(text)` 保證 loop 會結束，避免 off-by-one。

---

## 策略 2：Structure-Based Chunking

按文件自然結構切 — header、段落、section。最適合你控制格式的情況（Markdown、內部報告有保證的 heading 樣式）。

```python
def chunk_by_section(document_text):
    pattern = r"\n## "
    return re.split(pattern, document_text)
```

**優點：**
- 最乾淨、語意最完整的 chunk — 每塊都是完整語意單位
- 自然邊界符合人類對文件的理解
- 「關於 risk factors」的 chunk 真的包含 Risk Factors section

**缺點：**
- 只在結構有保證時才能用 — 純文字或掃描 PDF 沒有 header 可切
- section 大小差異很大；一個 50 字、另一個可能 5000 字
- 一個巨大的 section 還是可能爆掉 token 預算

Structure-based 在格式配合時是**理想**，在不配合時是**錯誤工具**。

---

## 策略 3：Semantic-Based Chunking

先切成句子，用 NLP 衡量相鄰句子之間的關聯度，把相關句子組合成 chunks。

**優點：**
- 產生語意上最連貫的 chunks
- 邊界依意義切，不依字元或 header

**缺點：**
- 運算成本高（前處理時要跑 semantic similarity 模型）
- 實作要做對很複雜
- 調參比 size 或 sentence 方法困難

chunk 品質很關鍵、而且你有 compute 預算支撐時才用 semantic chunking。

---

## 策略 4：Sentence-Based Chunking（實務中庸）

用 regex 切成句子，再把句子組成 chunk 並可選擇句子層級 overlap。

```python
def chunk_by_sentence(text, max_sentences_per_chunk=5, overlap_sentences=1):
    sentences = re.split(r"(?<=[.!?])\s+", text)

    chunks = []
    start_idx = 0

    while start_idx < len(sentences):
        end_idx = min(start_idx + max_sentences_per_chunk, len(sentences))
        current_chunk = sentences[start_idx:end_idx]
        chunks.append(" ".join(current_chunk))

        start_idx += max_sentences_per_chunk - overlap_sentences

        if start_idx < 0:
            start_idx = 0

    return chunks
```

注意 regex `(?<=[.!?])\s+` — 一個 lookbehind，把結尾標點留在前一句而不是丟掉。overlap 現在以**句子**為單位而不是字元，這更有意義。

Sentence-based 是你沒有結構保證但又想要人類可讀 chunk 邊界時的合理預設。

---

## 如何選擇策略

| 策略 | 最適合 | 避免 |
|------|--------|------|
| **Structure-based** | Markdown、有保證 header 的內部報告 | 純文字、PDF、格式混雜 |
| **Sentence-based** | 大部分散文文件 | code（句子概念不適用） |
| **Size-based + overlap** | 任何內容型態、code、log、fallback | 有更好結構訊號且想用的時候 |
| **Semantic** | retrieval 品質值得付出的高風險場景 | latency 或預算吃緊的前處理 |

**正式環境經驗**：size-based + overlap 常是首選，因為簡單可靠、適用任何東西。不會完美但不會壞你 pipeline。等有證據顯示 retrieval 品質在傷害產品時再升級 sentence／structure／semantic。

**沒有單一「最佳」策略**。對的選擇要看你的文件、用例、以及你能承擔的品質／複雜度取捨。

---

## CCA Task 對應

- **Task 1.3（Context Management）** — chunking 是你控制可檢索 context 粒度的手段；chunk 大小決定系統中「一個知識單位」是什麼。
- **Task 4.1（Grounded Responses）** — 好的 chunking 降低把離題文字抓進來、把錯答案 grounded 的機率。

---

## 常見錯誤

1. **以為 chunking 是已解決的問題** — chunking library 的預設參數會一直可以用，直到它不行了，而你不知道為什麼 retrieval 開始錯。
2. **size-based 沒有 overlap** — 字和句子被切在邊界，chunk 失去讓自己可被檢索的 context。
3. **對非結構化文字用 structure-based** — 沒有 header 時 regex 會回傳整份文件當一個 chunk。
4. **不同文件型態用同一個策略** — code、散文、table 需要不同策略；不要強迫同一個 chunker 處理全部。
5. **production 沒 log chunk ID** — retrieval 回傳錯 chunk 時，除非能追到是哪個 chunk 被挑，否則無法 debug。

> **關鍵洞察**
>
> Chunking 是 RAG pipeline 第一個會默默騙使用者的地方。下游每個步驟 — embedding、retrieval、prompt 組裝 — 都把 chunks 當成 given。chunk 若跨主題邊界或切掉定義，retrieval 系統會很有信心地回傳它，Claude 會很有信心地用它回答。投資在 chunking eval 要在投資 retrieval 調校之前。

---

## CCA 考試關聯

- **D1（Agentic Architecture）**：chunking 是 RAG context-management pipeline 的第一個決策。熟悉四種策略、取捨、和何時用哪個。
- **D4（Safety & Alignment）**：爛 chunking 是錯答案的默默來源 — lesson 裡「bug」的例子是經典考題情境。
- 預期會看到「Markdown 文件有保證 header → 哪個策略？」（structure）、「純文字 PDF → 哪個策略？」（size+overlap 或 sentence）。

---

## Flashcards

| Front | Back |
|-------|------|
| 列出課程涵蓋的四種 chunking 策略。 | Size-based、structure-based、sentence-based、semantic-based。 |
| chunk overlap 解決什麼問題？ | 邊界 context 流失 — 確保完整字／句，並保留鄰近 chunk 共享的 context。 |
| 何時選 structure-based chunking？ | 文件結構有保證時（Markdown header、範本化報告）。 |
| structure-based chunking 的缺點？ | 只在結構存在時有效；沒 header 的純文字或 PDF 無法使用。 |
| 為什麼 semantic chunking 昂貴？ | 前處理時要跑 NLP／相似度模型衡量句子關聯。 |
| production 的 chunking fallback 策略？ | Size-based + overlap — 適用任何內容型態。 |
| 為什麼「bug」的例子（醫療 vs. 工程）有啟發性？ | 示範爛 chunking 如何單因關鍵字重疊就把不相關 chunk 抓進 prompt。 |
| `chunk_by_char` 裡 `start_idx = end_idx - chunk_overlap` 做什麼？ | 讓視窗前進 `chunk_size - chunk_overlap`，保留相鄰 chunk 的 overlap。 |
