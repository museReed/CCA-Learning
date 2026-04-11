# Prompt Caching in Action — Engineering Deep Dive（繁體中文）

| 項目 | 詳情 |
|------|------|
| 考試領域 | D5 — Enterprise Deployment (20%) 主要；D2 — Tool Design (18%) 次要 |
| Task Statements | 5.1（成本／延遲優化）、5.2（production 效能）、2.1（tool schema 設計） |
| 來源 | building-with-the-claude-api / 06-extended-features / Lesson 58 |

---

## One-Liner

實戰上的 prompt caching 就是：把 tools list 和 system prompt 轉成可快取的 longhand block 形式並加上 `cache_control`，然後看 response 裡的 `cache_creation_input_tokens` / `cache_read_input_tokens` 去驗證命中與寫入。

---

## 真實 app 中哪裡最能省

課程點出三個高價值目標：

- **大型 system prompt** — 例如約 6K token 的 coding assistant system prompt。
- **複雜 tool schema** — 例如約 1.7K tokens 的多個 tool 定義。
- **重複的 message 內容** — 持續重送同樣前綴的對話或 workflow。

原則：caching 只有在你重複送一模一樣的內容時才有用——而在許多真實 app，這種情況**極度頻繁**。

---

## Tool Schema Caching 的設定

要快取 tool schema，把 `cache_control` 加到 **list 的最後一個 tool**。這個 tool 之前（包括本身）的所有東西都會被快取。

```python
if tools:
    tools_clone = tools.copy()
    last_tool = tools_clone[-1].copy()
    last_tool["cache_control"] = {"type": "ephemeral"}
    tools_clone[-1] = last_tool
    params["tools"] = tools_clone
```

為什麼要先 copy 再改：

- `tools.copy()` 建立 tools list 的淺拷貝，不會影響呼叫端的原始 list。
- `tools_clone[-1].copy()` 建立最後一個 tool dict 的淺拷貝，原本那個保持乾淨。
- 只有 copy 會被加上 `cache_control`。

你**也可以**直接寫 `tools[-1]["cache_control"] = ...`，但 copy 的做法能避免之後重排 tool、跨呼叫共用 list、或 app 不同部分共享 tool 定義時出現的詭異 bug。

`cache_control` 值設為 `{"type": "ephemeral"}`——標準的 1 小時 cache type。

---

## System Prompt Caching 的設定

System prompt 要從純字串轉成 longhand 結構化 block 形式，才有地方放 `cache_control`：

```python
if system:
    params["system"] = [
        {
            "type": "text",
            "text": system,
            "cache_control": {"type": "ephemeral"},
        }
    ]
```

字串形式的 system prompt 沒有欄位能放 `cache_control`；block 形式有。一旦把 system prompt 這樣結構化，整個 system prompt 就會成為 cached prefix 的一部分。

---

## 從 Response 讀 Cache 行為

啟用 caching 後，API 的 `usage` block 會新增幾個 token 計數器，告訴你這一次是寫入還是讀取 cache：

| 欄位 | 含義 |
|------|------|
| `cache_creation_input_tokens` | 這次 request Claude **寫入** cache 的 token 數（第一次或 cache miss 被迫重寫）。 |
| `cache_read_input_tokens` | 這次 request Claude 從 cache **讀取** 的 token 數（命中——省錢事件）。 |

常見模式：

- **第一次 request**：`cache_creation_input_tokens=1772`、`cache_read_input_tokens=0`——正在寫入 cache。
- **後續 request，內容相同**：`cache_creation_input_tokens=0`、`cache_read_input_tokens=1772`——正在讀取 cache。
- **內容改變**：改過的段會產生新的 `cache_creation_input_tokens`，因為那段還不在 cache 裡。

Cache **極度敏感**：tools 或 system prompt 改一個字元就會讓那個組件的整份 cache 失效。

---

## Cache Ordering 與部分命中

你可以在單一 request 裡設多個 cache breakpoint。Claude 處理順序是固定的：

1. **Tools**（若有）
2. **System prompt**（若有）
3. **Messages**

這個順序讓**部分命中**變得可能。假設你改了 system prompt 但 tools 沒動：

- Tools 仍然逐 byte 一致 → tools 段 **cache read**。
- System prompt 不同 → 新的 system prompt **cache write**。
- Messages 正常處理。

你只為真的變了的部分付錢。這種細粒度快取是本功能最大的優點之一：它是漸進失效，不是全有全無。

---

## 實務考量

Prompt caching 在以下情況最有效：

- **Tool schema 跨 request 一致** — 帶穩定工具箱的 production agent。
- **System prompt 穩定** — 鎖定的 persona 與指令。
- **App 會送出多個帶類似 context 的 request** — 聊天、反覆工作流、批次 eval。

記住：cache 只活一小時。這個設計是給**相對高頻的 API 使用**，不是長期儲存。如果你的產品每幾小時才呼叫一次，cache 會在呼叫間過期，你會不斷付 cache write 卻沒拿到 read 的好處。

---

## Common Mistakes

1. **原地改呼叫端的 tool list** — 直接寫 `tools[-1]["cache_control"] = ...` 可能悄悄影響 app 其他地方共用的同一份 list。用 copy-then-assign 模式。
2. **System prompt 繼續用純字串** — 字串沒地方放 `cache_control`。必須包進 `{"type": "text", "text": ..., "cache_control": ...}` block。
3. **以為整個 request 是一個 cache 單位** — 它不是。Tools、system prompt、messages 按處理順序各自獨立快取，你可以拿到部分命中。
4. **Production 沒檢查 `usage` 欄位** — 不監看 `cache_creation_input_tokens` 對 `cache_read_input_tokens`，你根本不知道 cache 有沒有真的在用。
5. **對 cached 段做瑣碎編輯** — tool description 或 system prompt 一個空白、一個標點，就強制 cache 重寫。把 cached 段當成有版本、不可變的 asset。
6. **對低頻 workload 開 caching** — Entry 在被重用前就過期，你只付寫入、拿不到讀取。

---

> **Key Insight**
>
> 實戰的 caching 只有三件事：(1) 把最後一個 tool 包上 `cache_control` 以快取整份 tool schema、(2) 把 system prompt 轉成 longhand block 形式好放 `cache_control`、(3) 檢查 response 的 `cache_creation_input_tokens` / `cache_read_input_tokens` 驗證命中確實發生。處理順序（tools → system → messages）自然送你部分命中。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）** — 考題會測哪個 API 欄位證明 cache 命中（`cache_read_input_tokens`）、哪個證明 cache 寫入（`cache_creation_input_tokens`）。
- **D2（Tool Design）** — 記得 `cache_control` 放在 list 的**最後一個** tool，由於處理順序的關係，它會把前面所有 tools 都納入 cache。
- 記得部分命中行為：只改 system prompt 時 tools 的 cache 會保留，usage 會呈現 split 模式（tools 讀、system 寫）。
- 「extremely sensitive」的逐 byte 比對是常考警語——任何編輯都會失效。

---

## Flashcards

| Front | Back |
|-------|------|
| 哪個 API response 欄位告訴你這次 request 寫入了 cache？ | `cache_creation_input_tokens`——Claude 剛剛寫入 cache 的 token 數。 |
| 哪個 API response 欄位告訴你這次 request 讀取了 cache？ | `cache_read_input_tokens`——Claude 從 cache 重用的 token 數。 |
| `cache_control` 要加在 tools list 的哪裡才能快取整份 tools？ | 放在 list 的**最後一個** tool 上。由於 tools 最先被處理，它前面（含本身）的所有東西都會成為 cached prefix。 |
| 為什麼要 copy tools list 和最後一個 tool 再加 `cache_control`？ | 避免改動到呼叫端原本的 list 或原本的 tool dict，防止重排 tool 或其他地方共享時出現 bug。 |
| System prompt 要怎麼變成可快取的？ | 把字串換成 longhand block 形式 `[{"type": "text", "text": ..., "cache_control": {"type": "ephemeral"}}]`。 |
| 1 小時快取用的 `cache_control` 值是什麼？ | `{"type": "ephemeral"}` |
| Tools、system prompt、messages 的 caching 處理順序是什麼？ | 先 tools、再 system prompt、再 messages。 |
| 只改 system prompt 時 cache 會發生什麼？ | 部分命中：tools 拿到 cache read（沒變），新的 system prompt 拿到 cache write。 |
| Caching context 下「extremely sensitive」是什麼意思？ | 任何 cached 段的改動——就算一個字元——都會讓 cache 失效，強迫重寫。 |
| 為什麼 caching 不適合長期、低頻 workload？ | 因為 cache 只存活一小時，呼叫之間就過期，你只付 cache write 卻永遠拿不到 read。 |
