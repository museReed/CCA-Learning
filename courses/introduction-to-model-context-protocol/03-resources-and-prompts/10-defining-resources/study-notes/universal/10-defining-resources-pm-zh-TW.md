# 定義 Resources — PM 視角

| 項目 | 細節 |
|------|--------|
| 考試範疇 | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server primitives), 2.4 (resource URI design), 2.5 (MIME type handling) |
| 來源 | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 10 |

---

## 一句話摘要

Resources 是 MCP server 的「參考資料庫」— 讓你的應用程式拉取資料用於顯示或提供 context，就像圖書館員根據書名幫你取書。

---

![Resources Types](../../visuals/resources-types-zh-TW.svg)


## 為什麼 PM 需要理解 Resources

身為 PM，你的產品需求決定了功能該用 resource、tool 還是 prompt。判斷錯誤會導致：

1. **浪費工程資源** — 本來用 resource 就能解決的需求，卻做成了 tool
2. **糟糕的使用者體驗** — 讓使用者等 Claude「查資料」，但其實資料可以預先載入
3. **錯誤的驗收標準** — 在 PRD 中指定了錯誤的互動模式

---

## 心智模型：辦公室檔案系統

把 MCP server 想像成一棟辦公大樓，裡面有三個部門：

| 部門 | MCP Primitive | 誰決定使用 | 辦公室類比 |
|------------|---------------|----------------------|----------------|
| 檔案櫃 | **Resource** | 櫃台人員（你的 app） | 櫃台人員拿出檔案給訪客 |
| 執行桌 | **Tool** | 主管（Claude） | 主管決定打電話給會計處理退款 |
| 工作手冊 | **Prompt** | 員工（使用者） | 員工按照標準作業流程執行 |

Resources 就是檔案櫃。你的應用程式碼打開抽屜、取出檔案，然後顯示在 UI 上或交給 Claude 作為 context。Claude 自己不會去開檔案櫃 — 這個區別非常關鍵。

---

## 兩種 Resource 類型

### 1. Direct Resources — 「給我整本目錄」

就像問圖書館員：「給我看所有可用的書。」請求永遠相同，URI 是固定的。

- **產品範例**：自動完成下拉選單，顯示所有可用文件
- **URI 模式**：`docs://documents`（無變數）

### 2. Templated Resources — 「給我這本特定的書」

就像問：「給我看 ID 是 plan.md 的書。」請求包含一個參數。

- **產品範例**：使用者輸入 `@plan.md` 時，系統取得該特定文件
- **URI 模式**：`docs://documents/{doc_id}`（大括號中有變數）

---

## 文件提及功能 — 產品情境演練

想像你正在設計一個聊天介面，使用者可以引用文件：

1. **使用者輸入 `@`** — 你的 app 呼叫「列出所有文件」resource 來填充自動完成選單
2. **使用者選擇 `plan.md`** — 你的 app 呼叫「取得特定文件」resource，帶入 `doc_id=plan.md`
3. **文件內容注入 prompt** — Claude 立即看到文件內容，不需額外步驟
4. **Claude 回應** — 帶著完整文件 context，即時回覆

這比另一種方案（Claude 呼叫 tool 去取文件）更快更流暢，因為資料在 Claude 開始思考前就已經在 prompt 裡了。

---

## 產品決策框架

撰寫 AI 功能的 PRD 時，問自己：

| 問題 | 如果是... | 如果否... |
|----------|-----------|----------|
| 資料需要出現在 UI 中（下拉選單、側邊欄）？ | **Resource** | 可能是 tool |
| 資料需要在 Claude 回應前就預載為 context？ | **Resource** | 如果 Claude 需要自己決定就用 tool |
| 取得這筆資料是否有副作用（寫入、刪除、扣款）？ | **Tool**（絕不是 resource） | Resource 是安全的 |
| Claude 是否需要自主決定何時取得這筆資料？ | **Tool** | Resource |

---

## 資料格式提示（MIME Types）

Resources 包含「格式提示」告訴 client 如何顯示資料：

| 格式提示 | 含義 | 產品意涵 |
|-------------|---------------|---------------------|
| `application/json` | 結構化資料（列表、表格） | 可渲染為豐富的 UI 元件 |
| `text/plain` | 純文字 | 直接顯示或注入聊天 |
| `application/pdf` | 二進位文件 | 可能需要特殊檢視器 |

這對 UI 規格很重要 — 知道資料格式有助於設計正確的顯示元件。

---

## PM 常見錯誤

1. **該用 resource 的地方指定成 tool** — 如果資料是唯讀且需要顯示在 UI，resource 更簡單也更快
2. **以為 Claude 會去取 resource** — resources 是 app-controlled；你的 app 去取，不是 Claude
3. **忽略自動完成模式** — resources 天然支持使用者覺得直覺的 `@mention` UX 模式
4. **沒有考慮資料新鮮度** — resources 在請求時回傳資料；如需即時更新，需與工程討論快取策略

> **Key Insight**
>
> PM 最需要記住的一點：resources 是 **app-controlled**。你的應用程式碼決定何時取得資料。這意味著你可以保證在 Claude 開始推理前資料已經就緒，帶來更快的回應時間和更好的 UX。

---

## CCA 考試關聯

- **D2 (Tool Design & MCP Integration)**：情境題會描述一個功能，問該用哪個 primitive。如果情境涉及在 UI 中顯示資料或將 context 注入 prompt，答案就是 resources。
- **控制模型是關鍵區分**：Tools = model-controlled、Resources = app-controlled、Prompts = user-controlled。這個三分法經常出現。
- 小心陷阱答案：建議用 tool「為 UI 取得資料」— 這種場景正確的 primitive 是 resource。

---

## Flashcards

| 正面 | 背面 |
|-------|------|
| 誰控制 MCP resources 的存取時機 — Claude、app 還是使用者？ | 應用程式碼（app-controlled） |
| MCP 中兩種 resource 類型是什麼？ | Direct resources（固定 URI、無參數）和 Templated resources（URI 含變數佔位符） |
| Resources 天然支持什麼產品 UX 模式？ | `@mention` 自動完成模式 — 輸入 `@`、看到可用項目、選擇一個、內容注入 prompt |
| PM 何時該在 PRD 中指定 resource 而非 tool？ | 資料是唯讀、需要顯示在 UI 中、或需要在 Claude 回應前預載為 context 時 |
| MIME type 提示對 resources 有什麼作用？ | 告訴 client 應用如何解讀和顯示回傳的資料 |
| 為什麼 resources 提供 context 比 tools 更快？ | Resource 資料在 Claude 開始推理前就直接注入 prompt，避免額外的往返 |
| Resource 可以有副作用（寫入、刪除、扣款）嗎？ | 不可以 — resources 是唯讀的。如需副作用，請用 tool |
| 在辦公室類比中，resource 是什麼？ | 檔案櫃 — 櫃台人員（app）從中取出檔案給訪客或添加到會議簡報中 |
