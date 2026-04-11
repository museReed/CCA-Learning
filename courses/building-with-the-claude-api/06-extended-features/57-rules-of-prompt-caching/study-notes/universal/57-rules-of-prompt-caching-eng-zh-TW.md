# Rules of Prompt Caching — Engineering Deep Dive（繁體中文）

| 項目 | 詳情 |
|------|------|
| 考試領域 | D5 — Enterprise Deployment (20%) 主要；D2 — Tool Design (18%) 次要 |
| Task Statements | 5.1（成本／延遲優化）、5.2（production 效能）、2.1（tool schema 設計） |
| 來源 | building-with-the-claude-api / 06-extended-features / Lesson 57 |

---

## One-Liner

Prompt caching 只有在你照規則玩時才有用：你必須手動加上 cache breakpoint、cached 內容必須逐 byte 一致、breakpoint 之前至少要有 1024 tokens、每次 request 最多 4 個 breakpoint。

---

## Cache 不是自動的——要加 Breakpoint

Caching 預設**不**啟用。你必須在 request 裡的某個 block 上明確加入 **cache breakpoint** 才會觸發。

運作原則：

- Message 上的處理工作**不會被自動快取**。
- 你要手動在某個 block 上加 `cache_control` 欄位。
- 該 breakpoint **之前與包含本身** 的所有內容會被快取。
- 後續 request 只有在到 breakpoint 為止的內容**完全一致**時才能讀取 cache。

換句話說，breakpoint 就是一條「切線」：上面的是可快取的前綴，下面的每次都是新的、要重新 preprocess。

---

## 必須使用 Longhand Block 形式

Message 的簡短形式（純字串）沒地方塞 `cache_control`。你必須用 **longhand block 形式**：

```python
# Shorthand — 無法快取
messages = [{"role": "user", "content": "這是一份長文件..."}]

# Longhand — 可以快取
messages = [{
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": "這是一份長文件...",
            "cache_control": {"type": "ephemeral"},
        }
    ],
}]
```

`cache_control` 欄位值設為 `{"type": "ephemeral"}`。`ephemeral` 是目前支援的 cache 類型，對應 lesson 56 的 1 小時 TTL。

---

## 逐 Byte 精確比對

Cache 極度敏感。到 breakpoint 為止的內容必須在後續 request 中**完全一致**才能重用。

即使很小的改動都會讓 cache 失效：

- 多加一個「please」→ cache miss。
- 改一個空白字元 → cache miss。
- 把兩句話順序對調 → cache miss。

只要前綴一變，Claude 就得從分歧點重新 preprocess，你還要再付一次 cache write 的錢。

**設計啟示：** 穩定內容放前面，變動內容放後面。使用者當下的問題應該放在 breakpoint **之後**，絕對不要放進快取前綴裡。

---

## 跨訊息 Caching

Cache breakpoint 可以橫跨多則 message，也可以跨不同 message 型態。如果你把 breakpoint 放在較後面的 message 上，**所有前面的 message**（user、assistant 等）都會被納入 cached 內容。

這對對話型 agent 特別有用：你可以把到某個穩定點為止的整個對話歷史都快取起來，然後後面繼續 append 新回合。

---

## 可快取的 Block 類型

不限於 text block。Cache breakpoint 可以加在：

- System prompts
- Tool definitions
- Image blocks
- Tool use blocks
- Tool result blocks

System prompt 與 tool definition 是**最佳**候選，因為它們在不同 request 之間幾乎不變，通常也是快取收益最大的地方。

---

## Cache Ordering：Tools → System → Messages

Claude 在幕後是按固定順序處理 request 的組件：

1. **Tools**（若有）
2. **System prompt**（若有）
3. **Messages**

這個順序決定了什麼東西會被快取到哪。如果你第一個 breakpoint 放在 messages 區，Claude 仍會把 tools 跟 system prompt 視為 cached 前綴的一部分，因為它們在處理順序上排前面。

每個 request 最多可以放 **4 個 cache breakpoint**。常見的 production layout：

- Breakpoint 1 → tools 結尾（快取所有 tool schemas）
- Breakpoint 2 → system prompt 結尾（快取 system prompt）
- Breakpoint 3 → message history 某處（快取穩定的對話前綴）
- Breakpoint 4 → 保留給更細粒度的快取

細分 breakpoint 讓 request 不同段可以各自獨立快取——某段變了只失效那一段，不會整份 cache 打翻。

---

## 最小內容長度：1024 Tokens

有一條底線：**breakpoint 之前與含本身的內容加總至少要 1024 tokens** 才會被快取。

- 一句短短「Hi there!」跨不過這個門檻。
- 你需要真的大的內容——長 system prompt、完整文件、或詳盡的 tool schema——才能觸發 caching。
- 1024 token 是所有要 cache 的 block **總和**，不是單一 block。

不到門檻時 `cache_control` 等於 no-op：不會建 cache，也不會省錢。

---

## Common Mistakes

1. **用 shorthand 字串形式** — 沒地方放 `cache_control`，什麼都不會被快取。先改成 longhand block 形式。
2. **把變動內容放在 breakpoint 之前** — 使用者的新問題絕對不能放進 cached 前綴裡，否則每次都 miss。
3. **低於門檻就想快取** — 想快取少於 1024 tokens 的 prompt 卻期待省錢。它會靜默什麼都不做。
4. **超過 4 個 breakpoint** — Request 會被拒絕。設計時要抓住 4 個名額的預算。
5. **不懂處理順序** — 把 breakpoint 放在 messages 上卻心理假設 tools 區「沒被快取」。它有——tools 跟 system prompt 在處理順序上排前面，永遠是 message 層級前綴的一部分。
6. **依賴 fuzzy matching** — Caching 是逐 byte 精確。先正規化空白、標點、順序，再說前綴是穩定的。

---

> **Key Insight**
>
> 定義快取成敗的四條規則：(1) 用 breakpoint 明確 opt in、(2) 逐 byte 比對、(3) 達到 1024 token 底線、(4) 遵守 tools → system → messages 的順序與 4 breakpoint 上限。任一條沒達成，cache 就靜默沒用——更糟的是你還為永遠不會被重用的內容付了 cache write。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）** — 考題會測你是否知道 caching 是手動、逐 byte、1024 token 底線。
- **D2（Tool Design）** — tool definition 是 caching 的頭號目標，因為它跨 request 穩定；考題可能問「tool 量大的 workflow 要把 breakpoint 放哪？」
- 記住處理順序：tools、system prompt、messages。這順序直接對應「我該先快取什麼？」
- 4 個 breakpoint、`{"type": "ephemeral"}`、1024 token 底線——這些是常考數字。

---

## Flashcards

| Front | Back |
|-------|------|
| Prompt caching 是自動的嗎？ | 不是——必須手動在 request 的某個 block 上加 `cache_control` 欄位（cache breakpoint）。 |
| `cache_control` 該填什麼值？ | `{"type": "ephemeral"}`——目前支援的 cache 類型，對應 1 小時 TTL。 |
| 哪種 message 形式支援 cache breakpoint？ | Longhand block 形式（`content` 是 block 的 list）。Shorthand 字串形式無法攜帶 `cache_control`。 |
| 放了 breakpoint 後 Claude 會 cache 多少內容？ | Breakpoint 之前與包含本身的所有內容。 |
| Follow-up 呼叫時 cached 內容要完全一樣嗎？ | 要——逐 byte 相同。加一個「please」都會失效。 |
| 可 cache 前綴的最小 token 數是多少？ | 1024 tokens（breakpoint 之前與含本身的所有 block 總和）。 |
| 一個 request 最多可以放幾個 breakpoint？ | 最多 4 個。 |
| Claude 處理 request 組件的順序是什麼？ | 先 tools、再 system prompt、再 messages。 |
| 哪些是最佳 caching 候選？為什麼？ | System prompt 與 tool definition——它們跨 request 很少變動，通常是最大塊穩定輸入。 |
| 後面的 message 上放 breakpoint 可以 cache 之前的 message 嗎？ | 可以——跨訊息 caching 會把 breakpoint 之前所有 message（user、assistant 等）都納入。 |
