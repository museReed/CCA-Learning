# Rules of Prompt Caching — PM Perspective（繁體中文）

| 項目 | 詳情 |
|------|------|
| 考試領域 | D5 — Enterprise Deployment (20%) |
| Task Statements | 5.1（成本／延遲優化）、5.2（production 效能） |
| 來源 | building-with-the-claude-api / 06-extended-features / Lesson 57 |

---

## One-Liner

Prompt caching 有一本規則書，必須照辦才能拿到折扣：明確 opt in、cached 內容保持逐 byte 一致、達到 1,024 token 門檻、把四個 breakpoint 額度當成稀有資源來規劃。

---

## PM 為什麼要在意這些規則？

Engineering 可以把 caching 開關打開，但真正讓 caching 發揮效果的，是產品層面的決策：**哪些內容要保持穩定不變**。如果你的產品每個 sprint 都在改 system prompt、讓使用者重排 tool definition、把使用者問題塞進「模板」中間——cache 就會失效，省下來的錢全部蒸發。

換句話說：caching 的規則其實是「**你的 context 有多穩定**」的規則——這是產品決策，不是工程決策。

---

## Mental Model：倉庫貼標生產線

想像一個物流倉庫，箱子在輸送帶上被蓋印刷上標籤。每個箱子前三面都蓋著一樣的大型公司 logo（穩定），只有第四面手寫客戶地址（變動）。

| 層 | 倉庫比喻 | Caching 對應 |
|----|----------|----------------|
| 預先蓋的 logo | 公司 logo 的橡皮章 | Tools + system prompt + 穩定 context |
| 客製標籤 | 手寫的客戶地址 | 使用者當下的問題 |
| 規則 | Logo 必須完全一致——糊一個字就整面重印 | Cached 前綴必須逐 byte 相同 |
| 批量規則 | 不能預先蓋微型出貨單——只有大箱子才行 | Breakpoint 前最少 1,024 tokens |
| 切線規則 | 生產線上只有四個印章站 | 每個 request 最多 4 個 cache breakpoint |

印章只有在「左邊的東西完全一樣」時才省事。印章一換，整片就要重印。

---

## Product Use Cases

### 能符合規則的產品模式

| 模式 | 為什麼符合 |
|------|------------|
| 帶鎖定 persona 的聊天產品 | 穩定前綴 → 每輪逐 byte 一致 |
| 帶版控 tool schema 的 coding assistant | Tool 只在 deploy 之間改，不會 session 中途變 |
| 有標準 PDF 的文件問答 | 文件穩定；只有使用者問題在變（且放在 breakpoint 之後） |
| 帶固定工具箱的 agent loop | Tools + system prompt 每輪都是穩定的可快取前綴 |

### 會打破規則的產品模式

| 模式 | 為什麼會破 |
|------|------------|
| 在 prompt 頂端注入「個人化問候」 | 使用者名字是變數 → 每輪 cache miss |
| A/B 測試為不同使用者改寫 system prompt | 前綴不同 → 沒人受益 |
| 短 prompt（< 1,024 tokens） | 低於門檻 → caching 是 no-op |
| 讓使用者重排 tool description | Byte order 改變 → cache 失效 |

---

## PM Decision Framework

在 scope caching 進某個功能之前，跑一遍這張檢查表：

| 問題 | 為什麼重要 |
|------|------------|
| 是否有一段至少 1,024 tokens 的穩定 context？ | 低於此，caching 什麼都不做 |
| 能保證那段穩定內容放在 request 的**開頭**嗎？ | Breakpoint 切的是前綴，變數必須放在**之後** |
| 使用的獨立 caching 層少於 4 層嗎？ | 4 是硬上限——預算要抓好 |
| 能承諾 release 之間保持那段前綴逐 byte 一致嗎？ | 一個空白的 rewrite 就會打翻 cache |
| 那段 context 一小時內會被重用嗎？ | TTL 是 1 小時——冷門功能浪費 cache write |
| 你知道什麼時候會變嗎——以便把 breakpoint 放在能最小化失效的位置？ | Cache 邊界要對齊變動頻率 |

前四題不能全答「是」，caching 就會表現不如預期——或靜默什麼都不做。

---

## Common PM Mistakes

1. **把 caching 當成工程開關** — 它其實是**context 穩定性契約**。產品決策決定 cache 會不會命中。
2. **把變數內容注入前綴** — 把使用者名字、時間戳、session ID 放在 system prompt 頂端，等於每次呼叫都毀掉 cache 命中。變數移到尾巴。
3. **隨手改 system prompt** — 每次小編輯都讓 cache 失效。把 cached system prompt 當成有版本、有 changelog 的 asset 對待。
4. **在小功能上忽略 1,024 token 門檻** — 「我們開了 caching 但成本沒降」通常是前綴太短不合格。
5. **太早把 4 個 breakpoint 用完** — 把 budget 用光就沒空間做後續優化。留一個保留位。
6. **沒通知 cache 失效事件** — 一次 system prompt 「潤飾」就可能讓整個艦隊一小時的 cache 節省歸零。大家要知道這件事何時發生。

---

> **Key Insight**
>
> Prompt caching 的規則其實是一份「**你的產品承諾保持什麼穩定**」的契約。好的 PM 讀完這堂課會問：「我的 prompt、tools、context 哪些部分能真的凍結？」那個答案——不是工程開關——才決定 caching 能不能拿到廣告上的節省。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）** — 考題會測這些機械規則：手動 opt in、逐 byte 比對、1,024 token 底線、4 個 breakpoint 上限、1 小時 TTL、tools → system → messages 順序。
- 題目若出現 PM 被告知「caching 開了但沒看到省」——答案幾乎總是某條規則被違反（前綴裡有變數、內容低於門檻、或 system prompt 被隨手改過）。
- 記住 system prompt 與 tool definition 是**最佳**快取目標，因為它們在處理順序上排最前面，而且很少變動。

---

## Flashcards

| Front | Back |
|-------|------|
| 從 PM 角度看 prompt caching 是自動的嗎？ | 不是——engineering 要逐 block 明確 opt in，產品要承諾內容穩定才會賺。 |
| 什麼長度門檻才能啟動 caching？ | Breakpoint 之前累積至少 1,024 tokens。 |
| 單一 request 最多可以用幾個 breakpoint？ | 最多 4 個。 |
| 為什麼使用者的問題應該放在 breakpoint **之後**？ | 因為 cached 前綴必須逐 byte 相同；把變數放進前綴等於保證 miss。 |
| 最好的 caching 目標是哪些層？ | System prompt 和 tool definition——體積大、穩定、處理順序最前。 |
| 什麼改動會打翻 cache 即使「沒實質變化」？ | 任何空白編輯、錯字修正、加「please」、或重排 tool——caching 是逐 byte 精確。 |
| PM 為什麼要在意 1 小時 TTL？ | 低頻功能的 cache entry 會在被重用前過期，等於什麼都沒省到。 |
| PM 在 prompt caching 上真正的任務是什麼？ | 保證 context 穩定性——規則只有在產品承諾把 cached 前綴凍結住時才會兌現。 |
