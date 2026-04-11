# Fine-Grained Tool Calling — Engineering Deep Dive

| 項目 | 內容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%)、D5 — Enterprise Deployment (20%) |
| Task Statements | 2.1（tool schema 與選擇）、2.4（多輪 tool loop）、5.2（streaming 與回應速度） |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 41 |

---

## One-Liner

Fine-grained tool calling 是一個可選的 streaming 模式，會關閉 server 端對 tool 參數的 JSON 驗證，讓你能即時收到 tool_use 的部分 JSON chunk，代價是你必須自己處理不合法的 JSON。

---

## 背景：Tool Use + Streaming

對帶有 tool 的 messages 請求啟用 streaming 時，Claude 會在生成過程中送出事件：

- `ContentBlockStart` / `ContentBlockStop`
- `ContentBlockDelta` — 一般文字生成
- `InputJsonEvent` — 專屬於 tool_use block，傳遞部分 JSON

每個 `InputJsonEvent` 都帶兩個關鍵屬性：

| 屬性 | 意義 |
|------|------|
| `partial_json` | 代表 tool 參數某一段的 JSON chunk |
| `snapshot` | 到目前為止所有 chunk 累積後的 JSON |

```python
for chunk in stream:
    if chunk.type == "input_json":
        print(chunk.partial_json)     # 增量片段
        current_args = chunk.snapshot # 目前累積結果
```

---

## 預設行為：Buffered Validation

預設情況下，Anthropic API **不會**把 Claude 生成的每個 token 立刻往 client 推，而是在 server 端將 chunk 先 buffer 起來、對照你的 tool schema 做驗證之後才 flush 出去。驗證的單位是**最上層的 key-value pair**。

假設 tool schema 預期的結構是：

```json
{
  "abstract": "This paper presents a novel...",
  "meta": {
    "word_count": 847,
    "review": "This paper introduces QuanNet..."
  }
}
```

API 的行為：

1. 等整段 `abstract` 的值生成完畢
2. 對該 key-value pair 做 schema 驗證
3. 一次送出 `abstract` 所有 buffer 住的 chunk
4. 接著處理 `meta` 物件

這就是為什麼 tool-use streaming 感覺起來是**延遲後的爆發**，而不是平滑的逐 token 串流。驗證是在保護你，避免把無效或無法使用的部分參數往下游程式碼送。

---

## 啟用 Fine-Grained Tool Calling

Fine-grained tool calling 會**關閉**上述的 server 驗證：

```python
run_conversation(
    messages,
    tools=[save_article_schema],
    fine_grained=True,
)
```

對照效果：

| 面向 | 預設 | Fine-Grained |
|------|-----|--------------|
| JSON 驗證 | 有（每個最上層 key-value） | 無 |
| Chunk 送出方式 | 每個有效 key 後的 buffered burst | 立即，逐 token |
| UX 反應速度 | 有延遲感 | 即時感 |
| 可能收到無效 JSON？ | 不會（server 端處理） | **會 — client 必須處理** |

啟用 fine-grained 後，你可能在整個 `meta` 物件還沒完成之前就先拿到 `word_count`，可以更早更新 UI 或預處理。

---

## 處理無效 JSON

驗證關閉之後，Claude 可能送出還不合法的 JSON，例如 `"word_count": undefined` 而不是一個數字。你的 snapshot parser 必須能容忍這種情況：

```python
import json

for chunk in stream:
    if chunk.type != "input_json":
        continue
    try:
        parsed_args = json.loads(chunk.snapshot)
    except json.JSONDecodeError:
        # 部分 / 無效 JSON — 繼續累積，不要 crash
        continue
    # 能 parse 成功後，才能安全地使用 parsed_args
```

常見的防禦模式：

1. **累積 + 重試** — 嘗試 parse snapshot，失敗就等下一批 chunk
2. **逐欄位抽取** — 用寬鬆的 regex 或增量 JSON parser 抽出已完成的 key
3. **最終驗證** — 當該 tool_use block 的 `ContentBlockStop` 到來時，做一次嚴格 parse 與 schema check

---

## 什麼時候用 Fine-Grained

以下任一情況可以考慮啟用：

- 需要**即時顯示 tool 參數生成進度**（例如把一篇草稿串流到預覽面板）
- 想**提早開始處理部分 tool 結果**以壓低端到端延遲
- 預設的 buffering 延遲明顯傷害 UX
- 團隊有能力投入**完整的 JSON 錯誤處理**

多數應用用預設（驗證）模式就夠好。只有當 buffering 造成使用者可感知的卡頓時才值得上 fine-grained。

---

## 與 Non-Streaming 的比較

| 模式 | 延遲特徵 | 驗證 | 複雜度 |
|------|---------|-----|--------|
| Non-streaming | 最後一次回應 | 完整 schema 驗證 | 最簡單 |
| Streaming（預設） | 最上層 key 之間的 burst | 逐 key 驗證 | 中等 |
| Streaming（fine-grained） | 平滑逐 token | 無（交由 client） | 最高 |

用最簡單、能滿足 UX 的模式。只有 buffering 延遲真的讓使用者感覺卡，才值得付 fine-grained 的複雜度代價。

---

## Common Mistakes

1. **啟用 fine-grained 卻沒寫 JSON 錯誤處理** — 串流 consumer 會在第一個無法 parse 的 snapshot 就 crash。
2. **把 `partial_json` 當成獨立 JSON 文件直接 parse** — `partial_json` 是片段，應該 parse `snapshot`。
3. **把第一個能 parse 的 snapshot 當成最終結果** — snapshot 還會繼續成長，要等 tool_use block 的 `ContentBlockStop` 才算結束。
4. **對不能容忍畸形參數的 tool 啟用 fine-grained** — 如果下游無法處理 malformed 輸入，就保留預設模式。
5. **結束後沒做最終 schema 驗證** — fine-grained 完全跳過 server 驗證，你必須在執行 tool 前自己驗一次。

> **Key Insight**
>
> Fine-grained tool calling 是延遲與正確性的 trade-off：用「server 端 JSON 驗證」換「更快、更平滑的 streaming」。預設模式更安全；fine-grained 是在「看得見的串流進度值得在 client 端實作完整 JSON 錯誤處理」時才用。

---

## CCA Exam Relevance

- **D2 (Tool Design)**：理解 tool 參數 streaming 預設是 buffered、逐 key 驗證，並知道如何 opt out。
- **D5 (Enterprise Deployment)**：生產環境 UX 的延遲優化——streaming tool_use 是一個具體槓桿。
- 題目若描述「tool 參數 streaming 有延遲後爆發的感覺」，答案就是 per-key 驗證造成的 buffering。

---

## Flashcards

| Front | Back |
|-------|------|
| 哪一種事件傳遞 streaming 中的部分 tool 參數？ | `InputJsonEvent`，附帶 `partial_json`（增量）與 `snapshot`（累積） |
| 預設 streaming 模式驗證什麼？ | Tool 參數每一個最上層 key-value pair 對照 schema 驗證 |
| `fine_grained=True` 會關掉什麼？ | Streaming 過程中 server 端對 tool 參數的 JSON 驗證 |
| 為什麼預設的 tool-use streaming 會有「爆發感」？ | API buffer chunk 直到一個完整、有效的最上層 key-value pair 完成 |
| Fine-grained tool calling 的主要風險？ | Claude 可能送出無效 JSON，client 必須 graceful 地處理 `json.JSONDecodeError` |
| 什麼時候該啟用 fine-grained tool calling？ | 當即時 streaming 進度對使用者重要，且團隊能投入完整 JSON 錯誤處理 |
| 哪一個屬性提供目前累積的 JSON？ | `InputJsonEvent` 的 `snapshot` |
| Fine-grained streaming 結束後還必須做什麼？ | 做最後一次嚴格 parse 與 schema check，再執行 tool |
