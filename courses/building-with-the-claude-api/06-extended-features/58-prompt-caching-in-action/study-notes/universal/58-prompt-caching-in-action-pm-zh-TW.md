# Prompt Caching in Action — PM Perspective（繁體中文）

| 項目 | 詳情 |
|------|------|
| 考試領域 | D5 — Enterprise Deployment (20%) |
| Task Statements | 5.1（成本／延遲優化）、5.2（production 效能） |
| 來源 | building-with-the-claude-api / 06-extended-features / Lesson 58 |

---

## One-Liner

在真實產品裡開 caching 的意思是：和團隊講好哪段 tool list 與 system prompt 保持凍結、接好 cache 標記，然後到 production 監看 usage 計數器，驗證 business case 裡承諾的節省是否真的出現。

---

## PM 為什麼要在意

Caching 是少數幾個「產品層級決策」能決定成敗的優化：我們承諾這段 context 在每次呼叫間保持一致。Engineering 把 tool list 和 system prompt 轉成可快取形式之後，這項功能要嘛省錢，要嘛靜默什麼都不做。結果完全取決於：

1. **產品保證哪些東西穩定** — 大型穩定 system prompt？穩定 tool schema？兩個都有？都沒有？
2. **有沒有人在看數字** — Cache 節省只有在有人盯著 dashboard 時才算數。

真的懂這堂課的 PM，走進 roadmap 會議可以說：「caching 開了，這三件事會把它打翻，這個指標我會盯著證明它有用。」

---

## Mental Model：會員杯折扣

想像星巴克的自帶杯折扣。第一次買咖啡沒什麼特別。第二次如果你帶著同一個杯子，就有折扣。忘記帶杯子？原價。杯子太小？不給折扣。太久沒用？優惠過期。

| 咖啡店比喻 | Caching 對應 |
|------------|----------------|
| 帶同一個杯子 | 送同樣的前綴 |
| 續杯折扣 | Cache read 便宜 |
| 第一次來付原價 | 第一次 `cache_creation_input_tokens` |
| 每次匹配都便宜 | 後續 `cache_read_input_tokens` |
| 杯子太小 → 沒折扣 | 前綴 < 1,024 tokens → 不 cache |
| 忘記帶一次 → 付原價 | 改一個字 → cache miss |

會員計畫只有在顧客（你的 app）一直帶同一個杯子（同樣的前綴）時才有用。

---

## Product Use Cases

### 三個最高價值的目標

| 目標 | 典型大小 | 為什麼是好候選 |
|------|----------|----------------|
| 大型 system prompt | ~6K tokens | 定義產品 persona；每次呼叫都穩定 |
| Tool schemas | ~1.7K tokens | Tool 定義不會在 session 中途改 |
| 重複的 message 內容 | 視情況 | 任何反覆送相同內容的 workflow（文件問答、滾動對話歷史） |

### 部分命中是產品勝利

因為 tools、system prompt、messages 各自獨立快取，產品團隊可以：

- **調整 system prompt**（可能是表現最差的一層）而不動 tools——tools 的 cache 節省不變。
- **新增一個 tool**——知道只有 tools 層被 cache write，system prompt 的 cache 保持熱。
- **在 system prompt 層做 A/B 測試**——清楚知道成本影響：一組付新 prompt 的 cache write，另一組繼續讀 cached 版。

這種細粒度意味著 caching 不必是「全有全無」的實驗閘門。

---

## PM Decision Framework

真實上線時 scope caching 的決策：

| 問題 | 為什麼重要 |
|------|------------|
| 哪一層（tools／system／messages）佔最大的穩定塊？ | 那是你第一個 breakpoint 要放的位置；也是最大的省 |
| 我們能承諾那一層至少凍結一週嗎？ | 不斷編輯會毀掉節省；穩定就是契約 |
| 誰擁有「cache 真的在用嗎」的 dashboard？ | 沒人看 `cache_read_input_tokens`，節省就只是空口宣稱 |
| 預期命中率是多少？ | 用來設目標（例：上線後 70% 的非首次呼叫要是 cache read） |
| 如何在 cache 失效前通知團隊？ | 改 system prompt 前在 Slack 講一聲，能省去成本圖表上的驚喜尖峰 |

---

## 要監看的商業指標

| 指標 | 追蹤內容 |
|------|----------|
| **Cache 命中率** | `cache_read_input_tokens / (cache_read + cache_creation)`——越高越好 |
| **單次對話成本** | Caching 上線後應下降；與 baseline 期間比較 |
| **Time-to-first-token** | 命中時應下降；對任何延遲敏感 UX 很重要 |
| **Cache 失效事件** | 每週有幾次 system prompt／tool 改動；太多就永遠拿不到節省 |
| **TTL 過期 miss** | 如果閒置數小時後的首次呼叫大多顯示 `cache_creation_input_tokens`，你的使用模式可能低於 1 小時頻率門檻 |

---

## Common PM Mistakes

1. **上線 caching 卻沒 dashboard** — 看不到 `cache_read_input_tokens`，就無法向 finance 證明有省到錢。
2. **讓文案團隊每週編輯 system prompt 而不事先通知** — 每次改寫就是 1 小時 cache 歸零。要建變更流程。
3. **忽視部分命中** — 團隊常誤以為「改了 system prompt，caching 壞了」，其實 tools 那層還在命中。部分命中是正常且有價值的。
4. **為第一次呼叫節省慶祝** — 第一次永遠是 cache *write*，那比平常**更貴**，不是更便宜。節省只在 1 小時窗口內後續呼叫累積。
5. **沒告訴 ops／on-call 1 小時 TTL** — 夜間流量掉，早上第一批呼叫全是 cache write，成本圖表看起來會很怪。
6. **把 caching 和 memory 混為一談** — 有人聽到「cache」就以為 Claude 在記東西。它不是。要澄清：caching 是成本／延遲，不是產品記憶。

---

> **Key Insight**
>
> 實戰的 caching 重點不是「按開關」，而是**擁有一份穩定性契約**。產品團隊決定什麼凍結、平台寫入 `cache_control` 標記、可觀測層回報 `cache_read_input_tokens` 對 `cache_creation_input_tokens`。這三塊缺一不可，否則上線就只是口頭節省，沒有真的省錢。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）** — 考題會給「caching 開了卻沒看到節省」的情境，答案通常是產品層原因（system prompt 被改、前綴有變數、把部分命中誤判為全 miss）。
- 記住 `cache_read_input_tokens` 是證明命中的欄位，`cache_creation_input_tokens` 是寫入的欄位。
- 記住部分命中是預期行為，因為 tools、system prompt、messages 各自獨立快取。
- 記住 1 小時 TTL 以及它與低頻流量的互動。

---

## Flashcards

| Front | Back |
|-------|------|
| 開啟 caching 時 PM 實際承諾什麼？ | 某些 context 層（tool list、system prompt、穩定前綴）在呼叫間會保持逐 byte 相同。 |
| 哪個 usage 欄位證明這次呼叫讀取了 cache？ | `cache_read_input_tokens`——Claude 從 cache 重用的 tokens。 |
| 哪個 usage 欄位證明這次呼叫寫入了 cache？ | `cache_creation_input_tokens`——Claude 剛寫入 cache 的 tokens。 |
| 什麼是「部分命中」？為什麼對 PM 是好事？ | 某一層（如 tools）命中、另一層（如 system prompt）寫入。讓你能調一層而不失去另一層的節省。 |
| 為什麼 caching 上線後第一次呼叫更貴而不是更便宜？ | 因為那是 cache write（`cache_creation_input_tokens`），不是 read。節省從 1 小時窗口內的後續呼叫開始。 |
| 說出最受 caching 影響的三個產品層。 | 大型 system prompt（~6K tokens）、tool schema（~1.7K tokens）、重複的 message 內容。 |
| 團隊星期五下午改寫 system prompt 會發生什麼事？ | 所有 system prompt cache 都失效；接下來每次呼叫都付 cache write，直到新 prompt 穩定。 |
| 為什麼「cache 命中率」dashboard 是 PM checklist 的一部分？ | 沒有它 caching 的效益無法驗證——沒證據就沒辦法向 finance 回報節省。 |
