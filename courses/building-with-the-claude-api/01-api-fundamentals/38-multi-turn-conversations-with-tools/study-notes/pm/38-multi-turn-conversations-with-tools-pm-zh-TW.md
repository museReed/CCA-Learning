# Multi-Turn Conversations with Tools — PM Perspective（繁中）

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture (22%) / D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 1.3（multi-turn conversation management）、1.2（agentic loop 實作）、2.4（multi-turn tool loops） |
| 來源 | building-with-the-claude-api / 01-api-fundamentals / Lesson 38 |

---

## 一句話總結

Multi-turn tool 對話解鎖了「Claude 可以幫我呼叫一支 API」和「Claude 可以規劃、執行、串接多個動作解決真實使用者問題」之間的差距——而工程成本是寫一個 loop，不是整個重寫。

---

## 心智模型：生產線上的工人

把 Claude 想成一個聰明的生產線工人，工作台上放著各種專門工具：

| 單回合 tool | Multi-turn tool |
|------------|-----------------|
| 工人拿一樣工具、用完、放回去 | 工人拿工具 A、看結果、拿工具 B、看結果、一直到完成 |
| 主管（你的程式）交還一個結果 | 主管交還每一個結果，工人決定下一步 |
| 任務：「量這個零件」 | 任務：「確認這個零件尺寸對——量它、對規格、必要時調整」 |

工人不會事先規劃每一次 tool 呼叫。他們看目前結果、決定下一步。你程式的工作就是每次工人要求新動作時，把正確的 tool 結果交回去——直到工人最後交出完成品。

---

## 為什麼產品要在乎

Multi-turn tool 對話是 **agent 類功能** 的棲息地。沒有它，Claude 基本上只是個裝了一個 function 的高級 autocomplete。有了它，Claude 變成能：

| 能力 | 範例 |
|------|------|
| 串接依賴操作 | 「訂機票然後加進行事曆」 |
| 先看再做 | 「查天氣，再決定要不要訂戶外餐廳」 |
| 迭代優化 | 「搜尋產品、按評分篩、買評分最高的那個」 |
| 錯誤恢復 | 「如果那個 API 掛了，試備援 API」 |

每一個都是高槓桿的產品能力，單次 tool 呼叫做不到。Multi-turn loop 是從「AI 功能」走向「AI agent」的門檻。

---

## 產品應用場景

### 非要 Multi-Turn 不可的時候

| 場景 | 為什麼要 Multi-Turn |
|------|---------------------|
| 「幫我規劃京都旅行」 | 需要序列決策（日期 → 飯店 → 機票 → 活動） |
| 「Debug 這段 code 的錯誤」 | 讀檔 → 找問題 → 改 → 驗證 |
| 「幫我總結最近 30 封信」 | 抓清單 → 抓每封信 → 綜合 |
| 「找 80 萬以下、學區好的房子」 | 搜尋物件 → 抓學校評分 → 篩選 → 排序 |

### 單回合就夠的時候

| 場景 | 為什麼單回合 |
|------|--------------|
| 「今天幾號？」 | 一次 tool 呼叫就結束 |
| 「翻譯這段」 | 純模型操作，根本不用 tool |
| 「給我一個優惠碼」 | 單次查詢 |

PM 的經驗法則：**如果答案需要「先做 X，再根據結果做 Y」，就需要 multi-turn。**

---

## PM 決策框架

規劃 multi-turn tool 功能之前，先回答這些：

| 問題 | 為什麼重要 |
|------|-----------|
| 最多允許跑幾次迭代？ | 延遲、成本、安全邊界——使用者不能無限等 |
| 迭代中間如何向使用者顯示進度？ | 好幾秒的空白畫面會毀掉感知品質 |
| 中途 tool 失敗怎麼辦？ | 需要優雅降級策略 |
| Token 成本預算怎麼抓？ | 每個回合都會讓歷史變長，長 loop 很貴 |
| Loop 的觀測性怎麼做？ | Production debug 需要看到每個回合 |
| 使用者可以打斷 loop 嗎？ | 沒有取消鈕的長 loop 是敵意 UX |

---

## 常見 PM 錯誤

1. **以為 shipping 了第一個 tool 之後「agent」就免費**——從單回合變多回合需要真正的 loop 實作、錯誤處理、成本控制
2. **Loop 期間沒有進度指示**——使用者看到 spinner 會以為產品壞了；要把每一步顯示出來
3. **沒有 max_iterations 上限**——搞混的 Claude 或壞掉的 tool 會無限 loop；跳過這個的 PM 會 ship 一張失控 token 帳單
4. **沒編更長的延遲預算**——multi-turn 一定比單回合慢，因為每次 tool 呼叫都是一趟 round trip
5. **忽略部分結果**——loop 撞到上限時，要顯示「不完整」結果還是裝沒事？這是產品決策不是工程決策

---

> **Key Insight**
>
> Multi-turn tool 對話是產品層級對 agent 的定義。技術成本很小——一個 `while` loop 加更好的 helper function——但產品影響很大：延遲預算、進度 UX、取消、token 成本、觀測性全部都變成一線議題。把「讓這個功能支援 multi-turn」當成產品里程碑，不是一個 tech spike。

---

## CCA Exam Relevance

- **D1（Agentic Architecture）**：Multi-turn tool 對話是典型的 agentic loop。考題會問什麼時候用、跟單回合呼叫怎麼差。
- **D2（Tool Design & MCP Integration）**：記住 tool schema 必須在每次迭代都帶上。
- 考題描述「依賴鏈的 tool 呼叫」的情境——答案幾乎永遠是「實作對話 loop」。

---

## Flashcards

| 題目 | 答案 |
|------|------|
| 用什麼生產線比喻來理解 multi-turn tool 對話？ | 一個聰明的工人一次拿一樣工具、看每個結果、決定下一步 |
| Agent 的產品層級定義是什麼？ | 支援 multi-turn tool 對話的功能——串接、依賴推理 |
| 什麼時候必須用 multi-turn 而不是單回合？ | 當答案需要「先做 X 再根據 X 的結果做 Y」——規劃、迭代、錯誤恢復 |
| Multi-turn tool 功能最大的隱藏成本是什麼？ | 延遲——每次 tool 呼叫多一趟 round trip，感覺比單回合慢 |
| Multi-turn 功能為什麼需要 max_iterations 上限？ | 防止失控 loop 燒光 token、永遠卡住 UI |
| Multi-turn loop 期間最重要的 UX 元素是什麼？ | 進度指示——把每個步驟顯示出來，否則使用者會以為產品壞了 |
| Multi-turn 引入了哪些產品決策？ | 迭代上限、進度 UX、取消、token 預算、觀測性 |
| 為什麼不能直接 reuse 單回合 tool 實作？ | 單回合 tooling 不保留歷史、不管理 stop_reason、不處理一個 response 多個 tool 呼叫 |
