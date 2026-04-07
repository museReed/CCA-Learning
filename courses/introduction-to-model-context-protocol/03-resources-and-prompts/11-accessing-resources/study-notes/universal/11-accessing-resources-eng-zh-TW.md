# 存取 Resources — 工程深入解析

| 項目 | 細節 |
|------|--------|
| 考試範疇 | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP client implementation), 2.4 (resource consumption patterns), 2.5 (content type handling) |
| 來源 | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 11 |

---

## 一句話摘要

Client 端透過 `read_resource()` 搭配 `AnyUrl` 存取資源，處理 `ReadResourceResult.contents` 列表，並根據 MIME type 分支解析 JSON 或回傳原始文字。

---

## Client 端 Resource 存取模式

Lesson 10 介紹了如何在 server 端定義 resources，本課聚焦在消費這些 resources 的 client 端程式碼。核心 function 是 `read_resource()`。

### 核心實作

```python
import json
from pydantic import AnyUrl

async def read_resource(self, uri: str) -> Any:
    result = await self.session().read_resource(AnyUrl(uri))
    resource = result.contents[0]

    if isinstance(resource, types.TextResourceContents):
        if resource.mimeType == "application/json":
            return json.loads(resource.text)

    return resource.text
```

### 逐行解析

1. **`AnyUrl(uri)`** — Pydantic 的 URL 驗證器。接受任何 URI scheme（`docs://`、`file://`、自訂 scheme），在解析時驗證格式。
2. **`result.contents[0]`** — 回應有 `contents` 列表。取第一個元素，因為單一 resource 請求通常回傳一個項目。
3. **`isinstance(resource, types.TextResourceContents)`** — 型別檢查，確認是文字內容（相對於二進位 `BlobResourceContents`）。
4. **MIME type 分支** — 如果是 `application/json`，用 `json.loads()` 解析。否則回傳原始 `.text` 字串。

---

## 回應結構深入解析

Server 回傳的 `ReadResourceResult` 結構如下：

```
ReadResourceResult
  └── contents: list[TextResourceContents | BlobResourceContents]
        └── [0]
              ├── uri: str
              ├── mimeType: str
              ├── text: str  (TextResourceContents)
              └── blob: bytes (BlobResourceContents)
```

關鍵設計決策：
- **`contents` 是一個列表** — 雖然通常只有一個項目，但協議支持回傳多個 content block
- **兩種 content 類型** — `TextResourceContents` 用於文字資料，`BlobResourceContents` 用於二進位
- **MIME type 在 content 物件上** — 不在 result 包裝器上，因為每個 content block 可以有不同類型

---

## MIME Type 處理策略

| MIME Type | 解析策略 | 回傳類型 |
|-----------|---------------|-------------|
| `application/json` | `json.loads(resource.text)` | `dict` 或 `list` |
| `text/plain` | `resource.text` | `str` |
| `text/markdown` | `resource.text` | `str` |
| 二進位類型 | `resource.blob` | `bytes` |

---

## `@` 自動完成 UX 模式

從使用者角度看，resource 存取驅動 `@mention` 工作流程：

1. **使用者輸入 `@`** — client 呼叫 `list_resources()` 填充自動完成下拉選單
2. **使用者用方向鍵瀏覽** — 從列表中選擇想要的 resource
3. **使用者按空白鍵確認** — client 呼叫 `read_resource(selected_uri)`
4. **內容注入 prompt** — resource 內容成為 prompt context 的一部分，不需要 tool call

這與 tool 根本不同：資料在 Claude **開始推理之前**就在 prompt 中，帶來更快更準確的回應。

---

## 測試 Resource 存取

在 MCP Inspector 中：
1. 切換到 **Resources** 分頁
2. 點擊 direct resource 立即讀取
3. 對 templated resources，填入參數值
4. 檢視回應結構：URI、MIME type、內容

在你的 CLI client 中：
1. 輸入 `@` 觸發自動完成
2. 選擇一個 resource
3. 驗證內容出現在 prompt context 中
4. 確認 Claude 可以在回應中引用該內容

---

## 常見錯誤

1. **忘記 `AnyUrl()` 包裝** — 傳入原始字串而非用 Pydantic 的 `AnyUrl` 包裝會導致型別錯誤
2. **沒有處理 `contents` 列表** — 直接存取 `result.text` 而非 `result.contents[0].text`
3. **漏掉 JSON 解析** — 將 `application/json` 內容當作原始文字處理，導致 prompt 中出現字串編碼的 JSON
4. **忽略二進位 resources** — 沒有處理非文字資料的 `BlobResourceContents`

> **Key Insight**
>
> Resource 內容直接進入 prompt — 不經過 tool call 處理。這意味著資料作為一級 context 提供給 Claude，降低延遲且避免模型需要「詢問」資訊。CCA 考試要記住：resources 是 **app-controlled**，在模型推理**開始前**注入 context。

---

## CCA 考試關聯

- **D2 (Tool Design & MCP Integration)**：要熟悉 `read_resource()` 模式 — `AnyUrl`、`contents[0]`、MIME type 分支。這是可考的實作細節。
- **D1 (Agentic Architecture)**：理解 resources 不需 tool call 就能將 context 注入 prompt，對已知資料需求更有效率。
- 情境題可能描述「資料出現在聊天中」或「不需 Claude 詢問就可用」— 這是 resource 存取，不是 tool 呼叫。

---

## Flashcards

| 正面 | 背面 |
|-------|------|
| `read_resource()` 中包裝 URI 的 Pydantic 類型是什麼？ | `AnyUrl` — 驗證 URI 格式並接受任何 scheme（docs://、file:// 等） |
| 如何從 `ReadResourceResult` 存取實際內容？ | `result.contents[0]` — contents 欄位是列表，取第一個元素 |
| Client 應如何處理 resource 的 `application/json` MIME type？ | 呼叫 `json.loads(resource.text)` 將 JSON 字串解析為 Python dict/list |
| 使用者選擇 `@mention` 時，resource 內容去哪裡？ | 直接注入 prompt context — 不觸發 tool call |
| MCP resource 回應中的兩種 content 類型是什麼？ | `TextResourceContents`（文字/JSON 資料）和 `BlobResourceContents`（二進位資料） |
| 為什麼 resource 存取比 tool 取得資料更快？ | Resource 資料在 Claude 開始推理前就在 prompt 中 — 不需要額外往返 |
| `@mention` 模式中什麼觸發自動完成列表？ | 使用者輸入 `@` 時，client 呼叫 `list_resources()` |
| MIME type 不是 `application/json` 時的預設回退是什麼？ | 回傳 `resource.text` 作為原始字串 |
