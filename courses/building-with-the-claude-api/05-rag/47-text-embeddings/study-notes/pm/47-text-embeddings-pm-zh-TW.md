# Text Embeddings — PM 視角

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Architecture (22%) 主要；D4 — Safety & Alignment (20%) 次要 |
| Task Statements | 1.3（context management）、4.1（grounded responses） |
| 來源 | building-with-the-claude-api / 05-rag / Lesson 47 |

---

## 一句話總結

Embeddings 是「意義的 GPS 座標」，它讓你的 RAG 功能有能力把使用者問題對應到正確 chunk — 同時悄悄把第二個 vendor 引入你的 stack。

---

## 心智模型：想法的 GPS 座標

想像把你 corpus 的每一句話都放進一張巨大的高維地圖。關於「revenue」的句子落在一個社區；關於「risk factors」的落在另一個；關於「supply chain」的落在第三個。

使用者提問時，你把他們的*問題*放到同一張地圖上，找最近的鄰居。那些鄰居就是最可能回答問題的 chunks。

| 概念 | PM 白話 |
|------|---------|
| Embedding model | 製圖師 — 把文字變成座標 |
| Embedding 向量 | 地圖上的特定座標 |
| Semantic similarity | 兩個座標之間的距離 |
| Semantic search | 「找地圖上最近的鄰居」 |

優雅之處在於即使字詞不同也有效。「這家公司賺了多少？」會落在「Revenue: $X million」附近，因為製圖師懂意義，不只是關鍵字。

---

## 為什麼 PM 要關心 embeddings

Embeddings 看起來是工程實作細節，但驅動使用者看得到的結果：

- **retrieval 品質** — 更好的 embedding model 代表更高機率找到對的 chunk
- **每次查詢成本** — 每個使用者問題都觸發一次 embedding 呼叫；provider 定價直接影響單位經濟
- **延遲** — embedding 是每次查詢額外的 network hop；吃掉你的 p95 延遲預算
- **vendor 多樣性** — embeddings 把第二個 AI vendor（VoyageAI）引入，和 Anthropic 並存，有自己的 SLO 和 outage 風險
- **keyword vs. semantic 取捨** — embeddings 幫助用自然語言提問的使用者，但對輸入確切詞的使用者來說純 keyword search 還是更快

---

## 兩 vendor 的現實

PM 常漏掉這塊：RAG 功能不是「Anthropic 的 AI」，是「Anthropic **加** VoyageAI 的 AI」。因為 Anthropic 目前不提供 embedding，你需要第二個 AI provider，它的 API 對每次查詢都是 critical。

這代表功能可用性現在被以下約束：
- Anthropic 的 uptime（generation）
- VoyageAI 的 uptime（embeddings）
- 你的 vector database 的 uptime（retrieval）

三個 vendor、三個 SLO、三條事件管道。要事先規劃。

---

## 產品用例

### Embeddings 在以下情境發光

| 場景 | 理由 |
|------|------|
| 使用者用自然語言提問 | 比對意義不是關鍵字 |
| corpus 使用使用者不認識的術語 | 「Profit」能匹配「net income」 |
| 使用者改寫或問模糊問題 | semantic similarity 寬容字詞 |
| 多語言支援 | multilingual embedding 可跨語言匹配 |

### Embeddings 吃力在以下情境

| 場景 | 更好的替代 |
|------|------------|
| 使用者輸入確切產品代碼 | Keyword／lexical search |
| 查詢是短 token（「SKU-4821」） | 結構化搜尋，不是 embedding |
| 需要可解釋的匹配 | keyword search 匹配看得見；embedding 是黑盒 |
| 成本吃緊且 corpus 很小 | 小 corpus 可能不值得建 embedding pipeline |

這就是 Lessons 49-51 介紹 BM25 等混合方法的原因 — 純 semantic 或純 keyword 都不完美。

---

## Input type 有差

VoyageAI 的 API 有 `input_type` 參數，讓你告訴模型某段文字是 **query**（使用者問題）還是 **document**（corpus 裡的 chunk）。模型是非對稱調校過的 — 同一段文字依 input type 產出略不同的向量。

對 PM 而言這是你可以驗證工程有沒有用好的品質槓桿。「query 有標 query，document 有標 document 嗎？」是 RAG review 會議裡合理的問題。

---

## PM 決策框架

簽核 RAG 功能前，要有這些的清楚答案：

| 問題 | 為什麼 |
|------|--------|
| 我們用哪個 embedding provider？ | 引入 vendor 依賴 |
| 每次查詢成本是多少？ | 和使用量相乘 |
| embedding 呼叫的 p95 延遲是多少？ | 累加到使用者感知的總延遲 |
| query 和 document 的 `input_type` 用對了嗎？ | 做對就是免費品質提升 |
| VoyageAI 掛掉怎麼辦？ | fallback 計畫 — cache、keyword search、降級模式 |
| 如何對我們特定內容評估 embedding 品質？ | 通用 benchmark 會騙人；要有領域 eval set |

---

## 「黑盒」UX 挑戰

Embedding 是黑盒。retrieval 失敗無法靠指某個關鍵字來解釋。當使用者問「為什麼挑*那個* chunk？」，誠實的答案只有「它的向量最接近你 query 的向量」。這很少令人滿意。

兩個產品回應：
1. **逐字顯示 chunk 作為 citation** — 讓使用者看到 retrieve 到什麼，即使不懂為什麼
2. **記錄 retrieval score** — 讓工程能在 score 可疑偏低時 debug
3. **提供 keyword fallback** — semantic retrieval 失敗時讓使用者強制 exact 搜尋

---

## 常見 PM 錯誤

1. **不知道有兩個 vendor** — 上 RAG 功能卻沒意識到 Anthropic 不提供 embedding。
2. **沒有每次查詢成本模型** — 忘了每個使用者問題都觸發 VoyageAI 呼叫，單位經濟變模糊。
3. **以為 keyword search 過時了** — 沒有；有些使用者查詢還是 exact matching 服務得更好。
4. **把 embedding 當「純工程」** — embedding 選擇影響 retrieval 品質，使用者看得到。
5. **embedding outage 沒 fallback** — VoyageAI 掛掉，整個 RAG 功能就掛，除非你事先規劃。

> **關鍵洞察**
>
> Embedding 是 RAG 從模型功能變成**多 vendor、多延遲、多失敗模式** pipeline 的地方。把 embedding 當實作細節的 PM，會被 production 成本、延遲、outage 嚇到。對的視角：embedding 是基礎 infrastructure 依賴，對你產品的重要性等同你的 database。

---

## CCA 考試關聯

- **D1（Agentic Architecture）**：embedding 是 RAG 的 retrieval 骨幹。記基本事實 — 它是什麼、誰提供（本課程是 VoyageAI）、-1 到 +1 的範圍。
- **D4（Safety & Alignment）**：更好 embedding → 更好 retrieval → 更好 grounding → 更少幻覺。embedding 是 retrieval 品質的起點。
- 注意 Anthropic／VoyageAI 分工的題目 — 「本課程用哪個 provider 做 embedding？」是合理考題。

---

## Flashcards

| Front | Back |
|-------|------|
| embeddings 的 PM 友好比喻？ | 意義的 GPS 座標 — 每個句子落在語意地圖，retrieval 找最近鄰居。 |
| 本課程推薦哪家做 embeddings？ | VoyageAI — Anthropic 目前不提供 embeddings。 |
| embeddings 引入什麼多 vendor 風險？ | RAG 功能現在同時依賴 Anthropic 和 VoyageAI；任一 outage 功能就壞。 |
| 何時 semantic search 比 keyword search 差？ | 使用者輸入確切代碼、短 token 或結構化識別碼時。 |
| `input_type` 為什麼對 PM 重要？ | 對問題用「query」、對 chunks 用「document」是免費 retrieval 品質提升。 |
| embedding 的「黑盒」UX 挑戰？ | 你無法靠關鍵字解釋 retrieval 匹配；使用者可能問「為什麼這個 chunk？」誠實答案是「向量距離」。 |
| 列出 embedding 增加的三個成本／延遲因素。 | 每次查詢 embedding 成本、embedding API 延遲、整個 corpus 的前處理成本。 |
| RAG 驗收 checklist 裡 PM 應該要求什麼？ | provider 確認、每次查詢成本理解、embedding outage fallback、retrieval 品質的領域 eval set。 |
