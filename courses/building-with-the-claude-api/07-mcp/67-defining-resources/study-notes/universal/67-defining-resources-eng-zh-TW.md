# Defining Resources — Engineering Deep Dive（繁體中文）

| 項目 | 說明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（MCP primitives：tools vs resources vs prompts）、2.2（content block types）、1.2（把 context 注入 agent loop） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 67 |

---

## One-Liner

Resources 是 MCP 中「暴露資料」的原語，行為像 HTTP GET handler，用 URI 定位，用 MIME type 決定序列化方式，分為兩種：direct（靜態 URI）與 templated（帶參數的 URI）。

---

## Resource vs Tool：心智切分

MCP server 有三種原語：tools、resources、prompts。決定新能力屬於哪一種時，第一個要問的就是「它是 resource 還是 tool？」

| 面向 | Resource | Tool |
|------|----------|------|
| 用途 | 暴露資料（讀） | 執行動作（讀或寫） |
| 類比 | HTTP GET | HTTP POST / RPC |
| 識別方式 | URI（`docs://documents/{id}`） | Named function ＋ JSON schema |
| 典型用法 | 取文件、列清單 | 編輯、刪除、寄送 |
| 誰決定呼叫 | Client / 應用，直接塞進 prompt | Claude 在推論時自己決定 |

經驗法則：如果是 pure read、使用者或應用想直接在 prompt 中引用，就做成 resource；如果是動作（尤其希望 Claude 在 agent loop 自主呼叫），就做成 tool。

---

## 動機範例：`@document_name` mention

課程用一個具體功能切入 resources：使用者在 CLI 輸入 `@`，應用跳出文件 autocomplete；選好並送出後，應用把文件內容注入 prompt。

需要兩個操作：

1. **列出所有文件** → 給 autocomplete
2. **取特定文件內容** → 注入 prompt

兩個都是純讀，完美對應 resources。

---

## Request / Response 流程

Resources 走 request-response 模式：client 發 `ReadResourceRequest` 帶 URI，server 回資料。URI 就是 resource 的位址。

```
Client ── ReadResourceRequest(uri="docs://documents/report.pdf") ──▶ Server
Client ◀──────── TextResourceContents(text=..., mimeType=...) ────── Server
```

刻意做得很簡單：沒有 schema negotiation、沒有 tool loop、沒有第二次 Claude call。Resources 就是用 URI 拉資料。

---

## 兩種 Resource

### Direct Resources

固定 URI，不會變。用於靜態資料端點，例如「給我所有文件的清單」。

### Templated Resources

URI 嵌入大括號參數。Python SDK 會解析 URI、抽出參數，以 keyword argument 傳給你的 function。用於帶參數的取值，例如「給我文件 X」。

URI template 的參數名必須跟 function signature 完全一致——SDK 用名字配對。

---

## 用 `@mcp.resource()` 實作

### Direct Resource：列出文件

```python
@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    return list(docs.keys())
```

- URI `docs://documents` 是靜態的
- 回傳值是 Python list，SDK 看到 `application/json` 會自動序列化
- 沒有參數，就是純粹的目錄列表

### Templated Resource：取單一文件

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

- URI 中的 `{doc_id}` 變成 function keyword argument
- `mime_type="text/plain"` 因為回傳是純文字
- 錯誤丟 Python exception，SDK 會轉成正確的錯誤 response

---

## MIME Types

Resources 可以回任何資料型態：字串、JSON、binary。`mime_type` 告訴 client 怎麼解析：

- `application/json` — 結構化 JSON，SDK 自動序列化
- `text/plain` — 純文字
- 其他任何合法 MIME type

關鍵便利：**SDK 會幫你序列化**。你只要回 Python 值（list、dict、str），SDK 根據 MIME type 轉換，不用自己做 `json.dumps`。

---

## 用 MCP Inspector 測試

Dev mode 啟動 server：

```bash
uv run mcp dev mcp_server.py
```

瀏覽器打開 Inspector，會看到兩個相關區塊：

- **Resources** — 列出 direct / 靜態 resources
- **Resource Templates** — 列出 templated resources 與參數 schema

點任何一個都可以跑一次，看到 client 實際會收到的 response 結構。這是驗證 URI、MIME type、return shape 最快的方式，接 client 之前先測過。

---

## 關鍵規則

- Resources 暴露資料；tools 執行動作
- Direct = 靜態 URI；templated = 帶 `{params}` 的 URI
- Templated URI 的參數名必須與 function argument 名字一致
- MIME type 指引 client 解析，並啟用自動序列化
- Python SDK 自動序列化——不要自己轉 JSON

---

## Common Mistakes

1. **用 resource 做有副作用的操作** — 寫入、寄送、刪除屬於 tools，不是 resources
2. **URI 參數跟 function argument 名字不一致** — `{doc_id}` 必須對應 `doc_id: str`
3. **自己做 JSON 序列化** — 設了 `mime_type="application/json"` 後 SDK 會幫你做，重複序列化會產生嵌套 JSON 字串
4. **忘了設 `mime_type`** — client 用它決定怎麼 parse，設錯或預設會讓本該 JSON 的東西變成純文字
5. **不用 Inspector 先測** — 跳過 MCP Inspector 意味著第一次真的呼叫就是第一次測試

> **Key Insight**
>
> Resources 是 **以 URI 定位的資料端點**。URI 就是整個 API 契約——選好 URI（例如 `docs://documents/{doc_id}`）等同設計 REST API。好的 resource 設計：穩定的 URI、清楚的 MIME type、明確的 tool/resource 切分。Resource 由 client 決定要不要拉；tool 由 Claude 決定要不要呼叫。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：Resources 是 MCP 三個 primitives 之一（tools、resources、prompts）；認得 `@mcp.resource()` 裝飾器、URI 與 `mime_type`；知道 direct vs templated 的差異
- **D1（Agentic Architecture）**：Resources 是 MCP server 向 agent loop 提供 context 的方式，不需 tool call——由 client 拉取後注入
- 考題模式：「Server 要以 ID 暴露文件內容，讓 client 注入 prompt，該用 tool 還是 resource？」→ resource

---

## Flashcards

| Front | Back |
|-------|------|
| MCP 的 resources 是什麼？ | Server 端以 URI 定位的資料端點，類似 HTTP GET handler，用來暴露資料而非執行動作 |
| Resources 有哪兩種？ | Direct（靜態 URI 如 `docs://documents`）與 templated（帶參數如 `docs://documents/{doc_id}`） |
| 定義 resource 的裝飾器？ | `@mcp.resource(uri, mime_type=...)` |
| Templated URI 參數怎麼到你的 function？ | SDK 從 URI 解析後以 keyword argument 傳入，依名字配對 |
| 什麼時候用 resource、什麼時候用 tool？ | Resource 給 client 要拉的純讀；tool 給動作（特別是希望 Claude 自主呼叫的） |
| `mime_type` 參數做什麼？ | 告訴 client 怎麼解析 response，並啟用 SDK 自動序列化（如 `application/json`） |
| 怎麼本地測試 resources？ | `uv run mcp dev mcp_server.py`，用瀏覽器的 MCP Inspector，會看到 Resources 與 Resource Templates |
| 要不要自己 JSON 序列化回傳值？ | 不用，SDK 會根據 `mime_type` 自動處理 |
