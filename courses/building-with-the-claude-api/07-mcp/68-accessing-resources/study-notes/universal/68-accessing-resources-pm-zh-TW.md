# Accessing Resources — PM Perspective（繁體中文）

| 項目 | 說明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（client 端 MCP resource 使用）、1.2（context 注入） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 68 |

---

## One-Liner

Accessing resources 是讓「@mention」變成產品功能的那塊 MCP：應用向 server 要被引用的資料，直接塞進 prompt 交給 Claude——零 tool call、零猜測、可預測的延遲與成本。

---

## 心智模型：給 Claude 一個已開好的資料夾

- **Tool call** 是給 Claude 一張地圖，希望它走到正確的大樓。知道路就快，不知道就慢又容易錯
- **Resource access** 是直接把資料夾打開放在 Claude 面前，Claude 一開始就能讀，不繞路、不用決定

當使用者明確指名要用什麼（「用這份文件」、「看這筆紀錄」），resource access 幾乎都是對的 pattern。

---

## 為什麼 PM 要在意

「@mention」做成 tool 和做成 resource，實際表現差異非常大：

| 指標 | Tool call 路徑 | Resource access 路徑 |
|------|---------------|---------------------|
| 每則使用者訊息的 API round trip | 2+ | 1 |
| 延遲負擔 | 每多一輪 ~1.5–3 秒 | 幾乎 0（在 Claude 呼叫前完成） |
| Token 成本 | tool schema + tool_use + tool_result + 最終答案 | 只有注入的內容 |
| 可靠度 | 依賴 Claude 正確決策 | 確定性 |
| UX | 「thinking...」轉圈更久 | 回應更俐落 |

用 resource access 上線的功能，立即就比較快且便宜——不用再調 prompt。

---

## 產品場景

### 什麼時候用 Resource Access

| 使用者體驗 | 為什麼適合 |
|-----------|-----------|
| @mention 文件 / 紀錄 / ticket | 使用者明確指定要包什麼 |
| Always-on context（公司政策、詞彙表） | 每次都要帶 |
| 「摘要這一頁」帶頁 ID 選擇器 | 確定性查詢、不需 Claude 決策 |
| File picker → 注入 | 應用知道是哪個檔案，無歧義 |

### Resource Access 不夠時

| 使用者需求 | 更適合的 pattern |
|-----------|-----------------|
| 對話中途讓 Claude 決定要不要查更多 | Tool call |
| 跨多個項目搜尋 | Tool call 帶 query |
| 依推理決定是否 fetch | Tool call |
| 有副作用的動作 | Tool call（絕不是 resource） |

---

## PM 決策框架

對任何「抓取並顯示」的功能問自己：

| 問題 | 若是 Yes | 意義 |
|------|---------|------|
| 使用者指定要抓哪個項目？ | Yes | Resource access |
| 候選集合在 UI 建構時就已知？ | Yes | Resource access（可用 dropdown / autocomplete） |
| 希望這個意圖永遠觸發 fetch？ | Yes | Resource access |
| 希望 Claude 可以跳過 fetch？ | Yes | Tool call |
| fetch 需要搜尋或排序？ | Yes | Tool call（Claude 帶 query） |

---

## 需要設計的 UX 層面

因為 resource access 在 **Claude 呼叫之前** 發生，UX 負擔在你的應用本身：

- **Discovery** — 使用者怎麼知道有 resource 可用？（@ autocomplete、slash menu、file picker）
- **Selection affordance** — dropdown vs 模糊搜尋 vs 指令輸入
- **進度提示** — resource fetch 還是有延遲，要放低調 loader
- **錯誤狀態** — URI 失敗時顯示「該文件已不可用」
- **Preview** — 讓使用者在送出前看到即將注入什麼（可選但體驗佳）

這完全是產品設計，不是 prompt engineering，設計師負責。

---

## 成本與 Context Window

Resource access 單次 API 呼叫便宜，但 token 不是免費——注入內容會佔 prompt 空間。PM 要預算：

- **大文件** — 能不能放進 context window？要定 truncation 或 chunking 規則
- **多 resource 同時** — 使用者若能 @mention 多項，總量可能爆開，要設上限
- **資料陳舊** — 內容是某時點快照，要決定每輪是否重抓
- **log 中的敏感資料** — 注入內容會流經 telemetry，要決定 redaction

---

## PM 常見錯誤

1. **把 @mention 做成 tool call** — 能動但慢一倍、貴一倍，對使用者沒任何好處
2. **讓 resource 無上限成長** — 把 50 頁 PDF 每輪都注入會燒爆 context 與延遲，要訂上限
3. **沒設計 resource discovery UX** — 使用者找不到的 resource 等同不存在
4. **忘記錯誤狀態** — resource 可能失敗（不存在、無權限、太大），UI 必須處理
5. **跳過 preview affordance** — 讓使用者看見即將注入什麼能提升信任，減少「Claude 為什麼這樣說？」的客訴

> **Key Insight**
>
> Resource access 是讓「使用者驅動的 context」變得無感的 pattern。使用者視角：「我 mention 了一個檔案，Claude 讀了」。架構視角：一次 API 呼叫而不是兩次、確定性的內容、清楚切分「應用抓什麼」與「Claude 推理什麼」。對 PM 而言，這是設計 context 豐富的 Claude 功能時最高槓桿的 pattern。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：要知道 resource access 在 MCP client 內（如 `read_resource`），在 Claude 呼叫之前執行，不是 tool loop 的一部分
- **D1（Agentic Architecture）**：Resources 把 context 預先注入，縮短 agent loop
- 考題模式：「使用者 @mention 一份文件，文件內容怎麼到 Claude？」→ client 抓 resource 後 inline 進 prompt，不是 tool call

---

## Flashcards

| Front | Back |
|-------|------|
| 「資料夾 vs 地圖」比喻是什麼？ | Tool call 給 Claude 一張地圖希望它找到資料；resource access 直接把資料夾打開放在 Claude 面前 |
| 為什麼 resource access 比 tool call 做 @mention 便宜？ | 一次 API round trip 而非兩次、總 token 更少、不用等 Claude 決定是否抓 |
| 誰負責 resource discovery 的 UX？ | 你的產品 / 設計團隊——使用者看到的 @ autocomplete、file picker、slash menu |
| Resource access 仍有什麼成本？ | 注入內容會占 prompt token，可能逼近 context window |
| 什麼時候 tool call 比 resource 好？ | 需要 Claude 判斷是否抓、需要 search、或操作有副作用時 |
| @mention 功能的 PRD 要含什麼？ | mention 的數量與大小上限、resource 失敗的 fallback UX、preview 機制、延遲預算、注入內容的隱私規則 |
| 為什麼 resource access 比 tool call 更確定性？ | 應用保證 fetch 一定發生，Claude 不會決定、不會跳過 |
| Resource-based 流程中，Claude 被呼叫前發生什麼？ | 應用透過 MCP client 抓 resource 並 inline 進正在組的 prompt |
