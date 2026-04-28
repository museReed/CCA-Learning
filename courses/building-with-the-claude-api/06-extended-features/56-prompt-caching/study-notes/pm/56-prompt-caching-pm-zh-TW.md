# Prompt Caching — PM Perspective（繁體中文）

| 項目 | 詳情 |
|------|------|
| 考試領域 | D5 — Enterprise Deployment (20%) |
| Task Statements | 5.1（成本／延遲優化）、5.2（production 效能） |
| 來源 | building-with-the-claude-api / 06-extended-features / Lesson 56 |

---

## One-Liner

Prompt caching 是 Claude API 的「批發折扣」——只要你的產品一直在送一大段相同的 context，開啟之後每一次非首次呼叫都會更快、更便宜，而且使用者完全感覺不出任何差別。

---

## PM 為什麼要在意這件事？

你的 app 每次呼叫 Claude，model 都會先跑一堆昂貴的前置作業（tokenization、embeddings、context 分析）才吐出第一個字——然後把這些結果丟掉。如果你的產品每次呼叫都送同一份 6,000 token 的 system prompt 或同一份長 PDF，你就是**每次都在重付這筆設定費，還要重等一遍**。

Prompt caching 改變了這個經濟模型。這筆設定費只付一次，之後一小時內的後續呼叫就「免費」（更便宜、更快）地重用。對任何「在穩定 context 上做反覆互動」的產品，這是單位經濟學與體感速度上最大的一根槓桿。

---

## Mental Model：手沖咖啡店

想像一間每杯都現磨的手沖咖啡店：

| 步驟 | 沒有 caching | 有 caching |
|------|--------------|------------|
| 第一位客人點衣索比亞手沖 | 磨豆、燒水、沖煮 | 磨豆、燒水、沖煮（付全額） |
| 第二位客人點一樣的 | 再磨一次、再燒一次、再沖 | 重用磨好的豆和熱水（只付沖的錢） |

磨豆與燒水 = preprocessing。沖煮 = 真正的生成。Prompt caching 就是「別再為同樣的訂單重複磨豆」。客人還是拿到現沖的咖啡——只是出杯更快，店家毛利更高。

---

## Product Use Cases

### 適合開 caching 的場景

| 情境 | 為什麼有用 |
|------|------------|
| 帶長 persona／指南的聊天產品 | Persona 每輪都一樣——cache 一次就好 |
| 文件問答（對同一份 PDF 問很多問題） | 文件穩定，只有問題在變 |
| 帶大 repo context 的 coding assistant | 每次 request 都帶一樣的 codebase context |
| 帶固定 tool 的 agent loop | Tool schema 每輪一樣 |
| 反覆編輯同一份草稿 | Base content 固定，指令在變 |

### 不適合的場景

| 情境 | 為什麼沒用 |
|------|------------|
| 一次性 prompt（不會重複） | 白白付 cache-write 成本 |
| Prompt 每次都變 | Cache 永遠 miss |
| 呼叫頻率極低（間隔數小時） | Cache 一小時就過期 |
| Prompt 很短 | 省下來的微乎其微 |

---

## PM Decision Framework

判斷是否要為某個功能開啟 prompt caching：

| 問題 | 為什麼重要 |
|------|------------|
| 每次 request 是否都帶一段「大而穩定」的 context？ | Caching 就是靠大穩定前綴在省 |
| 使用者在一小時內是否頻繁互動？ | 1 小時 TTL 獎勵高頻重用 |
| Input token 成本是否是單位經濟學的顯著一塊？ | 是的話，caching 直接影響毛利 |
| 體感延遲是使用者主要抱怨點嗎？ | Caching 降低 time-to-first-token |
| Cached 內容真的每次一模一樣（逐字相同）？ | Cache 對任何改動都極度敏感 |

大多為是，就該排進 roadmap——通常該排在其他 model 端優化之前。

---

## 商業影響

| 指標 | Prompt caching 的典型影響 |
|------|---------------------------|
| **單次對話成本** | 下降——cached 前綴以顯著折扣計費 |
| **延遲／time-to-first-token** | 下降——命中時跳過 preprocessing |
| **AI 功能毛利率** | 上升——熱門 workflow 的單位成本下降 |
| **留存率（間接）** | 可能上升——更快的回應讓產品更「順手」 |

這些全部是 production 收益，完全不需要改產品、也不增加使用者摩擦。這種機會很稀少。

---

## Common PM Mistakes

1. **把 caching 當成「之後再做」的優化** — 等你注意到帳單時，已經多付了好幾個月。只要你的產品有任何重複 context 的模式，就該排進 v1。
2. **把 caching 跟 memory 或個人化搞混** — caching 是「重用計算」，不是「記住使用者」。它不會改變 Claude 知道什麼。
3. **算指標時忽略 1 小時 TTL** — 不看呼叫頻率就預估「x% 呼叫被 cache」，低流量功能會高估節省。
4. **沒投資 context 穩定性** — 如果團隊每個 sprint 都在改 system prompt，cache 會一直被打翻。穩定 context 是前提。
5. **沒告訴 finance／ops caching 上線** — 成本曲線會突然變形。確保 cost model 跟得上。

---

> **Key Insight**
>
> Prompt caching 是**無形的產品改善**：使用者看不到，但感受得到。更低的單次成本保護毛利，更低的延遲讓產品用起來更順。對任何建立在「大而穩定 context」之上的 AI 功能，caching 是 PM 能推動的槓桿最大的優化——純粹的上行，沒有 UX 代價。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）** — caching 穩穩落在 task 5.1（成本與延遲）之下。考題會問如何優化重複 context 的 workflow。
- 記住 caching **同時**降低成本與延遲，不是只降一個。
- 記住 1 小時 TTL，以及只有在這時間窗內重用才有用。
- 題目若出現「對同一份長文件問很多問題」或「每輪都送同樣 system prompt」的情境，答案通常是 prompt caching。

---

## Flashcards

| Front | Back |
|-------|------|
| 用最白話說，prompt caching 為產品做了什麼？ | 把 Claude 昂貴的 preprocessing 結果存起來重用，讓重複 context 的呼叫更快更便宜。 |
| PM 必記的 1 小時規則是什麼？ | Cache 內容只存活一小時，過後就過期必須重建。 |
| Caching 影響哪兩個商業指標？ | 每次呼叫成本（下降）以及延遲／time-to-first-token（下降）。 |
| 哪些產品模式最受益？ | 大型穩定 system prompt、文件問答、帶 repo context 的 coding assistant、帶固定 tool 的 agent loop、反覆編輯。 |
| 哪些產品不受益？ | 一次性 prompt、內容每次都變、低頻使用（間隔超過一小時）、極短 prompt。 |
| Caching 是自動的嗎？ | 不是——必須明確開啟；不 opt-in Claude 就照常丟掉 preprocessing。 |
| Caching 會改變 Claude 對使用者的「認識」嗎？ | 不會——它只重用計算，不是 memory 或個人化。 |
| 為什麼 caching 應該排進 v1 而不是「之後再說」？ | 因為沒有它的每一週都是在「重複 context 流量上重付兩次」，省下的錢不會回補過去。 |
