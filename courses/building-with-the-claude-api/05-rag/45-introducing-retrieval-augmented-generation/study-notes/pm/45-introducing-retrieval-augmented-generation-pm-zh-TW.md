# Introducing Retrieval Augmented Generation — PM 視角

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Architecture (22%) 主要；D4 — Safety & Alignment (20%) 次要 |
| Task Statements | 1.3（context management）、4.1（grounded responses） |
| 來源 | building-with-the-claude-api / 05-rag / Lesson 45 |

---

## 一句話總結

RAG 是讓「用 AI 問遍公司整個知識庫」變成可出貨產品功能的關鍵：它讓 Claude 能回答那些根本放不進一次對話的文件。

---

## 心智模型：研究助理與檔案櫃

想像兩種助理的差別：

| 助理類型 | 運作方式 | 限制 |
|----------|----------|------|
| **純記憶型** | 靠學校學的知識回答 | 訓練沒碰過的主題就沒輒 |
| **Prompt-stuffer** | 你把 800 頁報告整本交給他再問 | 他被資訊淹沒、失焦，而且影印帳單爆炸 |
| **RAG 研究員** | 你問問題；他走到檔案櫃、抽出最相關的一個資料夾、讀完、回答 | 可擴展到超大資料庫；每個答案都 grounded 在特定來源 |

RAG 就是 **檔案櫃 + 研究員** 的 pattern。前處理（chunking + indexing）等於整理檔案櫃；查詢（retrieval + prompt）等於研究員去抽對的資料夾。

---

## RAG 解決的商業問題

每個知識密集的產品都會撞上同一面牆：**「AI 讀得到我們的東西嗎？」**

- 客服：「能不能從我們 2,000 篇 help articles 回答？」
- 法務：「能不能搜尋合約封存庫？」
- 企業搜尋：「能不能看懂我們 10 年的 Confluence？」
- 財務分析：「能不能從這份 800 頁的 10-K 抽出 risk factors？」

沒有 RAG，答案是「只有放得進一次 prompt 才行」，而這幾乎永遠不夠。有了 RAG，你對任意大小的 corpus 都有故事可講。

---

## 產品用例

### 適合 RAG 的場景

| 場景 | 為什麼 RAG 贏 |
|------|----------------|
| 知識庫 Q&A | corpus 大、問題窄、答案要能引用來源 |
| 「Chat with your PDF」 | 單一文件太大塞不進 context |
| 企業內部搜尋 | 多文件、多來源、內容會演進 |
| 領域專家（醫療、法律） | 大量參考資料，答案需要 grounded |
| 客服 copilot | 上千篇 help articles，要找對的那一篇 |

### 不適合 RAG 的場景

| 場景 | 更好的替代 |
|------|------------|
| 可以塞進 prompt 的短 PDF | **直接 prompt** — RAG 是過度工程 |
| 「今天天氣如何？」 | **Tool use** — 你要的是即時資料，不是靜態文件 |
| 「幫我寄這封信」 | **Tool use** — 你要的是動作，不是 retrieval |
| 閒聊、不需要知識 grounding | **單純 Claude** — 不需要 corpus |

---

## RAG 的成本／複雜度取捨

RAG 不是免費的。作為 PM，你拿以下換到以下：

| 放棄 | 換到 |
|------|------|
| 工程簡潔 | 突破 context window 的 scale |
| 零 infra 起點 | 每次查詢更便宜、更快的 prompt |
| 「把文件丟進去就好」的 UX | 可稽核、可引用的答案 |
| 零搜尋品質 bug | 本來做不到的功能 |

陷阱是不需要 RAG 時就往 RAG 跳。如果你的知識庫舒服放得進 prompt，最簡單的架構就是最好的。等 corpus 體積逼你上去時才上。

---

## PM 決策框架

當 stakeholder 說「我們要 AI 讀我們的文件」時，問這些：

| 問題 | 如果「是」 |
|------|------------|
| 整個 corpus 舒服放得進一次 prompt 嗎？ | 跳過 RAG — 直接塞 |
| 內容是穩定的（非即時）嗎？ | RAG 可行 |
| 使用者需要 AI 引用或連到來源嗎？ | RAG — retrieved chunks 讓 citation 很自然 |
| corpus 每天／每小時在變嗎？ | RAG 但要有清楚的 re-indexing 排程 |
| 這其實是即時資料（天氣、股價）嗎？ | **不是** RAG — 用 tool use |
| 使用者會在廣大 library 裡問窄問題嗎？ | RAG 理想 |

---

## 「retrieval 品質」這個產品風險

這是 PM 最常漏掉的一塊：**RAG 會默默失敗**。

一般 AI 功能給錯答案就是錯答案，有人會開 ticket。RAG 功能裡，不管 retrieval 層抓回什麼 chunk，Claude 都會很有信心地根據它回答，即使那 chunk 是錯的。使用者看到的是流暢、權威、錯的答案。

這代表：

- retrieval 品質是**產品品質**問題，不只是工程細節
- 你需要測試 retriever 的 eval，不只是測試模型的 eval
- citation 是使用者端的安全功能，讓他們能自我查核
- 「信心」要來自來源，不是來自 Claude 的語氣

PM 如果略過這塊，就是客服團隊被「AI 跟我講錯」淹沒的那個人。

---

## 常見 PM 錯誤

1. **太早上 RAG** — corpus 放得進 10K tokens 就硬上整套 vector database pipeline。
2. **UX 沒設計 citation** — Claude 不引用任何東西，使用者無法查核，信任崩盤。
3. **把 retriever 當「做完了」** — 沒 eval、沒監控、默默回傳錯 chunk。
4. **把 RAG 和 tool use 搞混** — 拿 RAG 去 pitch 一個其實需要即時資料的功能。
5. **忽略 re-indexing 成本** — 忘記每次文件更新都觸發一個工程要負責的前處理 pipeline。

> **關鍵洞察**
>
> RAG 把「懂東西的 AI」變成「讀你東西的 AI」。對產品而言，這就是新奇 chatbot 與可出貨功能的差別。陷阱是 retrieval 品質會變成產品品質指標：retrieval 爛，模型再怎麼調都救不了答案。要出 RAG 的 PM 必須自己擁有 retrieval 的 eval loop，不只是 generation。

---

## CCA 考試關聯

- **D1（Agentic Architecture）**：情境題若寫「大型文件 corpus ＋ 問問題」→ 答 RAG。熟悉形狀：chunk → index → retrieve → prompt。
- **D4（Safety & Alignment）**：RAG 把回答 grounded 在來源文字，這是標準的降幻覺 pattern。
- 注意與 tool use 的對照：即時／動態資料用 tool use，不是 RAG。靜態／文件 corpus 用 RAG。

---

## Flashcards

| Front | Back |
|-------|------|
| 用一句話說，RAG 讓產品能做什麼？ | 能對大到塞不進一次 prompt 的 corpus 提問。 |
| RAG 的「檔案櫃」類比是什麼？ | 前處理＝整理檔案櫃；查詢時＝研究員抽對的資料夾。 |
| PM 何時應該選 prompt stuffing 而不是 RAG？ | corpus 舒服放得進 context window 時，RAG 是不必要的複雜度。 |
| PM 何時應該選 tool use 而不是 RAG？ | 資料是即時／動態（天氣、價格、live 系統）而非靜態文件時。 |
| RAG 功能隱藏的產品風險是什麼？ | retrieval 默默失敗 — Claude 很有信心地根據錯 chunk 回答。 |
| 為什麼 RAG UX 的 citation 很重要？ | 讓使用者能驗證來源，在信任答案前抓到 retrieval 錯誤。 |
| 舉三個 RAG 明顯勝出的商業場景。 | 知識庫 Q&A、chat-with-your-PDF、企業內部搜尋。 |
| 選 RAG 要 PM 放棄什麼？ | 工程簡潔 — 換來 scale、成本效率、可引用性。 |
