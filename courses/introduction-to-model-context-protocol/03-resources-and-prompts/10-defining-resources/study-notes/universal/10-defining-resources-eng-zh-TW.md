# 定義 Resources — 工程深入解析

| 項目 | 細節 |
|------|--------|
| 考試範疇 | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server primitives), 2.4 (resource URI design), 2.5 (MIME type handling) |
| 來源 | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 10 |

---

## 一句話摘要

Resources 是 MCP server 中用來透過 URI 對外暴露唯讀資料的 primitive，類似 HTTP server 中的 GET handler。

---

![Resources Types](../../visuals/resources-types-zh-TW.svg)


## Resources vs. Tools：何時該用哪個

在 MCP server 開發中，第一個架構決策就是選擇 resource 還是 tool：

| 面向 | Resource | Tool |
|-----------|----------|------|
| 用途 | 暴露資料（唯讀） | 執行動作（可有副作用） |
| 控制者 | 應用程式碼（app-controlled） | Claude（model-controlled） |
| 呼叫方式 | Client 程式碼呼叫 `read_resource()` | Claude 自主決定呼叫 |
| HTTP 類比 | GET endpoint | POST/PUT/DELETE endpoint |
| Context 注入 | 內容直接注入 prompt | 結果由 Claude 內部處理 |

當你需要填充 UI（如自動完成清單）或將 context 注入 prompt（如 `@` 文件提及）時，resource 是正確選擇。

---

## 兩種 Resource 類型

### 1. Direct Resources — 靜態 URI

Direct resource 的 URI 是固定的，沒有參數。每次回傳相同「形狀」的資料。

```python
@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    return list(docs.keys())
```

URI `docs://documents` 是靜態的，適合用於列出所有可用項目、回傳 server metadata 或提供設定值。

### 2. Templated Resources — 參數化 URI

Templated resource 在 URI 中使用 `{param}` 佔位符。Python SDK 會自動提取這些值並作為 keyword arguments 傳入。

```python
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]
```

當 client 請求 `docs://documents/plan.md` 時，SDK 將 `plan.md` 解析為 `doc_id` 並傳入 `fetch_doc(doc_id="plan.md")`。

---

## `mime_type` 參數

MIME type 告訴 client 如何解讀回傳的資料：

| MIME Type | 使用場景 | Client 行為 |
|-----------|----------|-----------------|
| `application/json` | 結構化資料（list、object） | Client 呼叫 `json.loads()` |
| `text/plain` | 文件、日誌、純文字 | Client 使用原始字串 |
| `application/pdf` | 二進位檔案 | Client 以 binary 處理 |

SDK 自動處理序列化 — 回傳 Python list 或 dict 就會變成有效 JSON，不需要手動 `json.dumps()`。

---

## Request-Response 流程

```
Client Code --> MCP Client --> MCP Server --> Resource Function
                                                    |
Client Code <-- MCP Client <-- ReadResourceResult <-+
```

1. 你的程式碼呼叫 `session.read_resource(AnyUrl(uri))`
2. MCP client 發送 `ReadResourceRequest` 到 server
3. Server 將 URI 配對到正確的 resource function
4. Function 執行並回傳資料
5. SDK 包裝成 `ReadResourceResult`（含 MIME type metadata）

---

## 使用 MCP Inspector 測試

啟動 inspector：

```bash
uv run mcp dev mcp_server.py
```

Inspector UI 顯示兩個分頁：
- **Resources** — 列出 direct/static resources（點擊即可讀取）
- **Resource Templates** — 列出 templated resources（需提供參數值來測試）

Inspector 顯示完整的回應結構，包括 MIME type 和序列化後的內容，是驗證 resource 實作的必備工具。

---

## 常見錯誤

1. **忘記設定 `mime_type`** — client 可能因缺少 MIME type 而錯誤解析回應
2. **用 resource 做有副作用的操作** — 如果 function 有 write、delete 等副作用，應該用 tool
3. **手動序列化** — 自己呼叫 `json.dumps()` 但 SDK 已經處理了，導致雙重序列化
4. **混淆 direct 和 templated** — URI 沒有 `{}` 參數就一定是 direct resource

> **Key Insight**
>
> Resources 是 **app-controlled** — 你的應用程式碼決定何時讀取它們。這與 tool（Claude 決定何時呼叫）有根本性差異。理解這個控制邊界對 CCA 考試中的 MCP 架構題至關重要。

---

## CCA 考試關聯

- **D2 (Tool Design & MCP Integration)**：預期會出現「何時用 resource vs. tool」的情境題。關鍵區分是控制模型 — app-controlled vs. model-controlled。
- **D1 (Agentic Architecture)**：Resources 將 context 注入 prompt 而不需要 tool call，降低延遲和 token 消耗。
- 注意情境題中「資料需要顯示在 UI」或「用作 context」的描述 — 這些指向 resource 而非 tool。

---

## Flashcards

| 正面 | 背面 |
|-------|------|
| MCP 中兩種 resource 類型是什麼？ | Direct resources（靜態 URI、無參數）和 Templated resources（含 `{param}` 佔位符的參數化 URI） |
| Resource decorator 中的 `mime_type` 參數有什麼作用？ | 告訴 client 如何解讀回傳的資料（如 `application/json` 用於結構化資料） |
| 誰控制 MCP resources 的存取時機？ | 應用程式碼（app-controlled），不是 Claude 也不是使用者 |
| Python SDK 如何處理 templated resource 的參數？ | 自動從 URI 解析 `{param}` 並將匹配值作為 keyword arguments 傳入 function |
| 啟動 MCP Inspector 的指令是什麼？ | `uv run mcp dev mcp_server.py` |
| MCP resources 的 HTTP 類比是什麼？ | GET request handler — 暴露唯讀資料，無副作用 |
| 從 resource 回傳 dict 時需要呼叫 `json.dumps()` 嗎？ | 不需要 — SDK 自動處理序列化 |
| 使用者提及 `@document` 時，resource 內容最終去哪裡？ | 直接注入到送給 Claude 的 prompt 中，不需要 tool call |
