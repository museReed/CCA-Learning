# Fine-Grained Tool Calling — PM Perspective

| 項目 | 內容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%)、D5 — Enterprise Deployment (20%) |
| Task Statements | 2.1（tool schema 與選擇）、5.2（streaming 與反應速度） |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 41 |

---

## One-Liner

Fine-grained tool calling 讓產品可以讓使用者即時看到 AI「一個字一個字打出」tool 參數的過程——代價是工程端必須更謹慎處理可能暫時不合法的 JSON。

---

## Mental Model：現場即時字幕 vs. 完整字幕

| 模式 | 類比 | 使用者體驗 |
|------|------|-----------|
| 預設 streaming | 每次一整句才出現的電視字幕 | 停頓後整句浮出 |
| Fine-grained | 一個字一個字即時打出的現場聽打 | 平滑即時，但偶爾會閃過錯字 |

同樣的 trade-off 套用在 tool 參數 streaming：預設感覺像爆發、fine-grained 感覺像 live feed——但 live feed 可能瞬間出現稍後會被修正的亂碼。

---

## 為什麼對產品重要

Tool 參數生成可能很長。如果 tool 接收一篇 2,000 字的文章或一張詳細的 JSON 表單，Claude 要花好幾秒組裝。這段時間內使用者什麼都看不到——除非你 stream。

Fine-grained tool calling 是下列三者的差別：

- **「點擊 Generate、等 8 秒、內容出現」**（不 stream）
- **「點擊 Generate、內容隨主要欄位完成而分批出現」**（預設 streaming）
- **「點擊 Generate、看到游標在即時打出結果」**（fine-grained）

對內容生成型 UX（寫作、起草、表單填寫），第三種通常明顯更好。

---

## Product Use Cases

### 適合 Fine-Grained 的情境

| 情境 | 為什麼有價值 |
|------|-------------|
| 有預覽面板的 AI 寫作工具 | 使用者想看到草稿慢慢浮現 |
| 長文 email 生成器 | 顯著降低感知延遲 |
| 多欄位的即時表單 autofill | 每個欄位完成就立即渲染 |
| 帶可視編輯器的 code generation | 像人類協作者的即時打字感 |
| 長結構化報告（多段） | 使用者可以邊讀前段邊等後段生成 |

### 預設模式比較適合

| 情境 | 為什麼保留預設 |
|------|---------------|
| 短小的原子 tool call（< 1 秒） | Buffering 看不出來，fine-grained 的複雜度白花 |
| 沒人看的背景自動化 | 沒人看 stream，不用付延遲代價 |
| 合規關鍵流程 | 你想保留 server 驗證的安全網 |
| 單一錯值就讓下游壞掉的 tool | 部分/無效 JSON 風險太高 |

---

## PM Decision Framework

| 問題 | 如果 Yes | 行動 |
|------|---------|------|
| 有使用者正在看回應渲染嗎？ | Yes | 考慮 streaming |
| Tool 參數生成超過 3 秒嗎？ | Yes | Streaming 有價值 |
| 預設 streaming 明顯卡卡的嗎？ | Yes | 考慮 fine-grained |
| 工程端能加完整的 JSON 錯誤處理嗎？ | Yes | Fine-grained 可以安全使用 |
| 這個 tool 對畸形輸入零容忍嗎？ | Yes | 保留預設 |

---

## 隱藏成本：工程複雜度

Fine-grained tool calling 不是一個免費的「加速」開關，它把責任從 Anthropic 伺服器搬到你的程式碼：

- JSON 驗證 → 搬到 client
- 錯誤復原 → 搬到 client
- Schema 一致性檢查 → 搬到 client
- 邊緣案例（null、undefined、斷開的字串）處理 → 搬到 client

PM 提議啟用 fine-grained 時必須把這些工程工作算進預算。草率上線會帶來比預設模式更糟的 UX（使用者在 live feed 上看到 crash）。

---

## 應該追蹤的指標

上線後需要儀表化以下項目：

1. **首個可見 token 的時間** — 使用 fine-grained 的主要理由，應該顯著下降
2. **Tool 執行成功率** — 應該維持；如果下降，代表 JSON 處理有 bug
3. **Client 端 parse 錯誤率** — fine-grained 下會是非零，應隨處理成熟而下降
4. **端到端完成時間** — 可能不會變快；fine-grained 主要改善「感知延遲」
5. **生成期間的使用者參與度** — 是否更願意停留在頁面？真正的 UX 贏面

---

## Common PM Mistakes

1. **以為 fine-grained 就是全部變快** — 端到端時間通常一樣，改善的是感知延遲而不是吞吐量。
2. **沒寫 JSON 錯誤處理就上 fine-grained** — 使用者會看到 live feed 沒錯，也會看到 malformed chunk 造成的 crash。
3. **在短 tool call 上用 fine-grained** — 複雜度多了、UX 幾乎沒差。
4. **沒儀表化 parse 錯誤率** — 沒有這個指標，你根本不知道自己的處理有沒有效。
5. **把 fine-grained 跟「Claude 變快」混為一談** — 它只影響 streaming 中 tool 參數的遞送，不影響模型生成速度。

> **Key Insight**
>
> Fine-grained tool calling 是感知延遲的槓桿，不是吞吐量的槓桿。在使用者正在看長時間 tool 生成、且工程端能投入完整 JSON 處理時才啟用。CCA 考試要記得：trade-off 是「client 端 JSON 驗證責任」換「chunk 立即遞送」。

---

## CCA Exam Relevance

- **D2 (Tool Design)**：理解 fine-grained 會關閉 streaming 期間 server 的 JSON 驗證，client 必須處理錯誤。
- **D5 (Enterprise Deployment)**：Streaming 是核心 UX 槓桿，fine-grained 是其中最激進的設定。
- 題目可能描述一個 UX 問題（「tool streaming 感覺一陣一陣」）並問是哪個設定控制的。

---

## Flashcards

| Front | Back |
|-------|------|
| Fine-grained tool calling 的使用者可見效果是什麼？ | Tool 參數以逐 token 即時串流出現，而不是一陣一陣地 burst |
| 預設 tool-use streaming 感覺像什麼？ | 停頓後爆發——每個 burst 對應一個驗證過的最上層 key |
| Fine-grained 的主要工程成本是什麼？ | Client 必須在 streaming 中 graceful 處理無效 / 部分 JSON |
| PM 什麼時候應該選 fine-grained？ | 長時間 tool 生成、使用者正在看回應浮現、且工程端能投入 JSON 錯誤處理 |
| 哪一個指標在 fine-grained 之後最會改善？ | 首個可見 token 的時間——感知延遲 |
| 啟用 fine-grained 之後哪個指標不應該變差？ | Tool 執行成功率——parse bug 會在這裡浮現 |
| Fine-grained streaming 最好的類比？ | 一個字一個字的現場聽打，相對於整句才出現的電視字幕 |
| 什麼時候 fine-grained 是白花複雜度？ | 短 tool call、背景自動化，或不能容忍畸形輸入的關鍵 tool |
