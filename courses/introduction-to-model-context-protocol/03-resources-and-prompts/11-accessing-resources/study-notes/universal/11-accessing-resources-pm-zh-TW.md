# 存取 Resources — PM 視角

| 項目 | 細節 |
|------|--------|
| 考試範疇 | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP client implementation), 2.4 (resource consumption patterns), 2.5 (content type handling) |
| 來源 | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 11 |

---

## 一句話摘要

存取 resources 就像你的 app 從共享硬碟拉出檔案，在會議開始前放到桌上 — Claude 不需要開口詢問就能立即看到資料。

---

## 為什麼 PM 需要理解 Resource 存取

Resource 存取是驅動以下功能的 client 端模式：
- **文件提及**（聊天介面中的 `@plan.md`）
- **Context 面板**（側邊欄顯示相關資料）
- **自動完成下拉選單**（從可用項目中選擇）

理解這個模式能幫助 PM：
1. **規格正確的互動模型** — 使用者即時看到資料，而非等 Claude「查詢」
2. **設定合理的效能預期** — resource 注入比 tool 取得資料更快
3. **設計更好的 UX 流程** — `@mention` 模式是經過驗證的互動範式

---

## 心智模型：會議前簡報

想像你在組織一場會議：

| 方式 | 類比 | MCP 對應 | 使用者體驗 |
|----------|---------|----------------|-----------------|
| **會前簡報** | 助理列印相關報告，會議開始前放在桌上 | **Resource 存取** | 快速 — 所有人可以立即參考文件 |
| **會中查找** | 有人說「讓我去檔案室看看」然後離開去取文件 | **Tool call** | 較慢 — 會議暫停等待取得資料 |

Resources 就是會前簡報。你的應用程式預先收集資料，交給 Claude 作為 context。Claude 不需要「離開會議室」去找資訊。

---

## `@Mention` 使用者旅程

Resource 存取所驅動的逐步 UX 流程：

1. **使用者在聊天輸入框中輸入 `@`** — app 向 server 查詢可用 resources
2. **自動完成下拉選單出現** — 顯示可用的文件、資料來源或參考
3. **使用者選擇項目**（方向鍵 + 空白鍵）— app 取得該 resource 的完整內容
4. **內容靜默注入 prompt** — 使用者看不到原始內容；它成為隱藏的 context
5. **使用者按 Enter 發送** — Claude 同時收到使用者的問題和引用的文件
6. **Claude 帶著完整 context 回應** — 沒有「讓我查一下」的延遲，沒有額外的 tool call

這與 Claude 官方介面中的「Add from Google Drive」是相同的模式。

---

## 產品意涵

### 效能
Resource 注入在 Claude 開始推理前完成，這意味著：
- **沒有額外延遲** — 不需要 tool call
- **不浪費 token** — Claude 不需要描述它要查什麼
- **第一次回應就已充分了解** — 不需要後續往返

### 資料格式意識
Resources 帶有格式提示（MIME types），影響 app 處理方式：

| 資料格式 | App 行為 | PM 考量 |
|-------------|-------------------|------------------|
| 結構化資料（JSON） | 解析為物件用於豐富顯示 | 可在 UI 中驅動表格、圖表或篩選器 |
| 純文字 | 直接顯示或注入聊天 | 實作簡單但視覺呈現有限 |
| 二進位（PDF、圖片） | 需要特殊渲染 | 你的 UI 規格需要檢視器元件 |

### 錯誤處理
如果 resource 找不到或不可用，app 應優雅處理。在 PRD 中應指定：
- 引用的文件不可用時使用者看到什麼
- 是否顯示警告或靜默忽略
- 回退行為（例如 Claude 仍可在沒有 resource 的情況下回答）

---

## PM 常見錯誤

1. **該用 resource 的場景設計成 tool 型 UX** — 如果使用者明確選擇要包含什麼資料，用 resources（不是 tools）
2. **沒有規格化自動完成體驗** — resource 驅動的自動完成需要設計規格：搜尋行為、結果排序、顯示格式
3. **忽略資料大小** — 大型 resources（整個資料庫、巨大文件）在注入前應分頁或摘要
4. **以為 Claude 控制 resource 存取** — resources 是 app-controlled；Claude 不決定何時取得

> **Key Insight**
>
> 由 resources 驅動的 `@mention` 模式創造了一種使用者體驗：context 在 AI 開始思考**之前**就已收集完畢。這根本性地比 tool 取得資料更快且更可預測。撰寫 PRD 時，總是問：「這筆資料能作為 resource 預先載入，還是 Claude 需要決定何時取得？」

---

## CCA 考試關聯

- **D2 (Tool Design & MCP Integration)**：預期會有關於 client 端 resource 模式的題目。要知道 `read_resource()` 回傳 `contents` 列表，MIME types 決定解析行為。
- **D1 (Agentic Architecture)**：Resource 存取透過在模型推理前注入資料到 prompt 來降低延遲。這是一個關鍵的架構取捨。
- 注意描述「資料出現在介面中」或「context 被預先載入」的情境 — 這描述的是 resource 存取，不是 tool call。

---

## Flashcards

| 正面 | 背面 |
|-------|------|
| `@mention` 模式中什麼觸發自動完成下拉選單？ | 使用者輸入 `@` 時，client 向 server 查詢可用 resources |
| Resource 內容如何傳遞給 Claude？ | 直接注入 prompt context — 不需要 tool call |
| Resource 存取的會議室類比是什麼？ | 會前簡報：助理列印報告，會議開始前放在桌上 |
| 為什麼 resource 存取對使用者來說比 tool 取得資料更快？ | 資料在 Claude 開始推理前就在 prompt 中 — 沒有額外往返或「讓我查一下」的延遲 |
| 什麼決定 client 如何解析 resource 內容？ | Resource 上的 MIME type — `application/json` 解析為 JSON，`text/plain` 用作原始文字 |
| 誰控制 resources 的存取時機 — Claude、app 還是使用者？ | 應用程式碼（app-controlled），雖然使用者可能透過輸入 `@` 觸發 |
| PM 應在 PRD 中為 resource 錯誤處理指定什麼？ | 引用文件不可用時使用者看到什麼、警告行為、回退行為 |
| 什麼真實功能展示了 resource 存取模式？ | Claude 的「Add from Google Drive」— app 取得文件內容並注入為 prompt context |
