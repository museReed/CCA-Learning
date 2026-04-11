# Text Chunking Strategies — PM 視角

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Architecture (22%) 主要；D4 — Safety & Alignment (20%) 次要 |
| Task Statements | 1.3（context management）、4.1（grounded responses） |
| 來源 | building-with-the-claude-api / 05-rag / Lesson 46 |

---

## 一句話總結

Chunking 是每個 RAG 功能看不見的產品品質旋鈕 — 它決定「一個知識單位」長什麼樣子，做錯了 AI 就會很有信心地引用錯段落。

---

## 心智模型：在晚宴切蛋糕

想像一個多層蛋糕。客人點「巧克力那層」或「草莓那層」。怎麼切很重要：

| 切法 | 每個客人拿到 | Chunking 策略 |
|------|--------------|---------------|
| 隨機 5 公分立方塊 | 有時純巧克力，有時一半巧克力一半草莓 | Size-based、無 overlap |
| 同樣的立方塊，但沾到下一塊的邊 | 一樣，但看得到旁邊是什麼層 | Size-based + overlap |
| 乾淨的水平切片，一層一片 | 他們點的那層，剛剛好 | Structure-based |
| 廚師按風味挑選分組 | 最小份量的純風味 | Semantic |

切得隨便，就會吃到跨層的那一口。點草莓的客人咬到一大塊巧克力也不知道為什麼。**這就是使用者在 RAG 功能裡遇到爛 chunking 的感覺**。

---

## 為什麼這是 PM 問題（不只是工程問題）

Chunking 決策直接驅動使用者看得到的行為：

- **「AI 給我不相關的答案」** → 通常是 chunking 爛
- **「AI 在 citation 裡切在句子中間」** → 一定是 chunking 爛
- **「AI 用我沒問的 section 回答」** → 本 lesson 經典的「bug」例子
- **「文件更新後答案沒跟上」** → re-chunking pipeline 壞了

PM 如果覺得 chunking 是「工程搞定的事」，就會是 CEO demo 功能結果拿到錯答案時那個道歉的人。

---

## 四種策略的 PM 白話

| 策略 | PM 白話 | 何時用 |
|------|---------|--------|
| **Size-based** | 「每 500 字切一次，加 overlap」 | 混合內容的預設 — 便宜、可靠、可預期 |
| **Structure-based** | 「按 Markdown header 切」 | 你控制內容格式時（內部文件、範本化報告） |
| **Sentence-based** | 「每 5 個句子一組」 | 散文為主的內容，句子是有意義的單位 |
| **Semantic** | 「用 NLP 把相關想法留在一起」 | 高風險 retrieval（法律、醫療）值得花 compute 時 |

PM 要內化的一件事：**沒有哪個是通用「最佳」**。對的策略看內容型態、品質標準、工程預算。

---

## 「bug」例子 — 每個 PM 都該知道

Lesson 用一個很鮮明的例子：一份文件有醫療研究和軟體工程兩個 section。醫療 section 剛好寫「XDR-47, a bug we have not seen before」。使用者問「How many bugs did engineers fix this year?」。

爛的 chunker 可能因為有「bug」這個字就把醫療 chunk 撈出來。Claude 接著寫一段流暢的關於病毒的答案 — 錯的 section、錯的領域、錯的答案，但語氣很有信心。

這就是**默默失敗** pattern。沒有錯誤訊息。log 看起來健康。只有使用者自己 QA 答案時才會發現。對 PM 而言，這種 bug 到第十次就會毀掉使用者信任。

---

## 產品用例

### 何時用 Structure-Based

| 訊號 | 理由 |
|------|------|
| 內容是 Markdown | header 是可靠邊界 |
| 你擁有撰寫範本（內部 wiki、PRD 範本） | 可以強制結構 |
| 每個 section 語意大致一致 | 語意對齊免費附送 |

### 何時用 Size-Based + Overlap

| 訊號 | 理由 |
|------|------|
| 你無法保證文件結構 | fallback 必須什麼都能處理 |
| 內容混雜（docs + PDF + code + log） | 一個策略搞定全部 |
| 你在出 MVP 想要可預期的行為 | 最好推理 |

### 何時用 Sentence-Based

| 訊號 | 理由 |
|------|------|
| 內容是散文、沒結構 | 句子是自然單位 |
| 你要人類可讀的 citation | citation 框裡切掉的字看起來很壞 |

### 何時用 Semantic

| 訊號 | 理由 |
|------|------|
| 領域高風險（法律、醫療、金融） | retrieval 錯有實際後果 |
| retrieval 是驗證過的產品瓶頸 | 有數據顯示 chunk 品質重要 |
| 你有 compute 預算 | 前處理比較重 |

---

## PM 決策框架

規劃 RAG 功能時，簽核前回答這些：

| 問題 | 為什麼重要 |
|------|------------|
| 我們的 canonical 內容格式是什麼？ | 決定 structure-based 是否可行 |
| chunk 大小預算是多少？ | 直接關聯 prompt 大小、成本、延遲 |
| 誰負責 chunk 品質 eval？ | 必須有具名 owner，不是「工程大家都負責」 |
| 使用者怎麼看到 citation？ | 如果 citation 可見，切掉的 chunk 看起來壞了 |
| 文件變更時怎麼 re-chunk？ | 每次內容更新都有前處理成本 |

---

## 常見 PM 錯誤

1. **把 chunking 當工程實作細節** — 它是產品槓桿；chunk 大小直接影響使用者看到的內容。
2. **沒有 chunk 品質 eval** — 沒 test set 就出貨，代表你從憤怒使用者那學到 chunking 爛。
3. **以為一個策略適合所有內容型態** — 有 docs、PDF、code 的平台需要不只一個 chunker。
4. **忽略 re-indexing 故事** — 每次內容更新都觸發前處理；pipeline 脆弱的話，你的「AI 回答」功能會默默 stale。
5. **citation 不可稽核** — 沒有可見的來源連結，使用者抓不到默默失敗，信任崩塌。

> **關鍵洞察**
>
> Chunking 是 retrieval 的默默兄弟。當有人說「我們 RAG 系統答錯了」，大約一半情況的 root cause 是 chunking — 好 chunk 根本沒被產生，所以好 retrieval 不可能發生。對 PM 而言這代表 chunk 品質 day one 就是 eval target，不是「之後再迭代」的東西。

---

## CCA 考試關聯

- **D1（Agentic Architecture）**：熟悉四種策略、取捨、情境題準備好（「Markdown 有保證 header → ？」、「PDF 混雜 → ？」）。
- **D4（Safety & Alignment）**：「bug」例子直接對應幻覺風險 — 錯 chunk 導致很有信心的錯答案。
- 注意考題環繞「overlap」的寫法 — 問「怎麼避免 chunk 被切在句子中間」答案永遠是 overlap。

---

## Flashcards

| Front | Back |
|-------|------|
| PM 為什麼要關心 chunking？ | 它是默默驅動產品品質的元素 — 爛 chunking 導致很有信心的錯答案，使用者無法 debug。 |
| 「bug」例子在教什麼？ | 同一個關鍵字可以出現在不相關領域（醫療 vs. 軟體），產生錯但流暢的答案。 |
| 切蛋糕的類比是什麼？ | 糟糕切法會跨層，讓客人咬到錯的口味 — 爛 chunking 跨主題邊界。 |
| PM 何時挑 structure-based chunking？ | 你控制內容格式時（Markdown、範本化報告），header 是可靠邊界。 |
| 預設 fallback chunking 策略？ | Size-based + overlap — 適用任何內容型態、行為可預期。 |
| 為什麼 chunk overlap 對使用者看到的 citation 很重要？ | 沒有 overlap，chunk 會切在句子中間，citation 看起來壞了。 |
| 誰該負責 chunk 品質 eval？ | 具名 PM／工程搭檔 — 不是「工程大家」；這是產品指標。 |
| 爛 chunking 的默默失敗模式是什麼？ | 沒錯誤、log 健康、使用者拿到根據不相關 chunk 產出的自信錯答案。 |
