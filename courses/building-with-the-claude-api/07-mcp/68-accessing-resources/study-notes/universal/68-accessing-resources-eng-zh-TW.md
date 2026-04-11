# Accessing Resources — Engineering Deep Dive（繁體中文）

| 項目 | 說明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（MCP primitives：client 端 resource 存取）、2.2（content block types）、1.2（context 注入 agent loop） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 68 |

---

## One-Liner

Accessing resources 是「定義 resources」的 client 對偶——你在 MCP client 上新增 `read_resource(uri)`，依 MIME type 解析回傳的 `contents` list，把結果交給應用，在 Claude 還沒看到之前注入 prompt。

---

## 為什麼 Resources 比 Tool Call 更適合注入 context

本課開頭的重點：resources 讓 server 暴露「可以直接塞進 prompt」的資料，不需要 tool call。優勢是效率：

- **不必第二次 round trip** — 沒有 `tool_use` / `tool_result` 迴圈
- **確定性** — 資料一定存在，不用等 Claude 決定
- **除錯簡單** — content block 更少，trace 容易讀

使用者輸入 `@report.pdf` 送出時，應用透過 MCP client 抓 resource，把文字 inline 到 prompt，Claude 在第一次 API 呼叫就收到整份文件。

---

## 實作 `read_resource`

在 MCP client 新增方法：

```python
async def read_resource(self, uri: str) -> Any:
    result = await self.session().read_resource(AnyUrl(uri))
    resource = result.contents[0]
    # ... 依 MIME type 解析（見下節）
```

重點：

- URI 要用 `AnyUrl`（pydantic）包一層再傳給 SDK，確保型別正確
- `session().read_resource(...)` 是底層 SDK 呼叫
- response 的 `contents` 是 **list**，通常取第一個元素——裡面含實際資料與 metadata（MIME type）

回傳型別標為 `Any`，因為不同 resource 會回不同 Python 型別（字串、dict、list、binary）依 MIME type 而定。

---

## 依 MIME Type 解析

Resource 可回傳不同資料型態，client 必須分支處理：

```python
if isinstance(resource, types.TextResourceContents):
    if resource.mimeType == "application/json":
        return json.loads(resource.text)

    return resource.text
```

本課涵蓋兩種情況：

1. **`application/json`** — server 回結構化資料，用 `json.loads(resource.text)` 轉成 Python 物件
2. **`text/plain`**（或其他文字）— 直接回 `resource.text`

MIME type 是 server 透過 `@mcp.resource(mime_type=...)` 告訴 client 的契約，讓 client 不用猜。

其他內容型態（binary、image）可以加分支，但本課專注在 text 與 JSON——足夠對應 document mention 的情境。

---

## 必要 Imports

兩個 import 缺一不可：

```python
import json
from pydantic import AnyUrl
```

- `json` — 解析 JSON body
- `AnyUrl` — pydantic 的 URL 型別；`read_resource` 要求型別化 URL，不吃純字串

少了任一個就會爆 type error 或 runtime exception。

---

## 用 CLI 測試 Resource 存取

End-to-end 測試走 CLI：使用者問「What's in the @report.pdf document?」時，系統會：

1. 用 autocomplete 列出可用 resources（`list_resources` 或類似）
2. 使用者選一個
3. 自動抓 resource 內容（透過 `read_resource`）
4. 把內容放進送給 Claude 的 prompt

Claude 收到時文件已經在 context 中——不需要 tool call。

---

## 與應用整合

重要設計點：MCP client 的 code 會被 **應用其他部分** 使用。`read_resource` 是一塊建築積木，上層元件呼叫它來：

- 抓文件內容注入 prompt
- 填 @mention autocomplete
- 把 resource 資料整合進 prompt

這種分層很關鍵：

| 層 | 責任 |
|----|------|
| MCP client | 跟 MCP server 溝通、解析回應 |
| 應用層 | 決定何時抓、注入哪裡 |
| Prompt builder | 組最終送給 Claude 的訊息 |

Client 故意做得「笨」——只負責讀。業務邏輯留在應用層。

---

## 為什麼比 Tool Call 更有效率

比較兩種做法對應同一使用者意圖（「讀 report.pdf」）：

| 做法 | Round trips | Content blocks | 確定性 |
|------|------------|----------------|--------|
| Tool call（`read_doc_contents`） | 2（tool_use + tool_result） | tool_use、tool_result、最終文字 | Claude 決定是否呼叫 |
| Resource fetch（`read_resource`） | 1 | 只有 prompt 文字 | 應用保證一定抓 |

對於使用者明確驅動的 context（「我在 @mention 這份文件」），resource 路徑嚴格較優：更少 API 呼叫、更少 token、更快回應。

---

## Common Mistakes

1. **把 raw 字串當 URI 傳** — `read_resource` 需要 `AnyUrl`，跳過 `AnyUrl(uri)` 會爆型別錯誤
2. **忘了分支 MIME type** — 無條件回 `resource.text` 會把 JSON 變純字串，下游解析就壞了
3. **假設 `contents` 一定只有一個元素** — SDK 回 list，通常取第一個但沒保證，這個假設要寫在註解
4. **雙重 parse JSON** — server 若已用 `mime_type="application/json"` 序列化，text 就是 JSON；用 `json.loads` 正確，不要 server 端再包一層
5. **在 `read_resource` 裡放業務邏輯** — Client 要薄，「何時抓」屬於應用層

> **Key Insight**
>
> `read_resource` 是 `@mcp.resource()` 的對稱鏡像——一邊序列化、另一邊反序列化，MIME type 是黏合劑。懂這個對稱性，用 resource 支援的功能會像乾淨的資料通道，而不是權宜 tool call。每個 MCP client 都會有這三行 pattern：呼叫 `read_resource`、取 `contents[0]`、分支 `mimeType`。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：`read_resource` 是 `@mcp.resource()` 的 client 對偶；知道 method signature、`AnyUrl` 的使用、MIME type 分支模式
- **D1（Agentic Architecture）**：Resources 把 context 注入 agent loop 而不需 tool call，縮短 loop 並提升確定性
- 考題模式：「要傳給 `session.read_resource()` 的型別是什麼？」→ `AnyUrl`（來自 pydantic），不是 raw string

---

## Flashcards

| Front | Back |
|-------|------|
| Client 讀 resource 的核心方法？ | `async def read_resource(self, uri: str)`，內部呼叫 `self.session().read_resource(AnyUrl(uri))` |
| 傳給 SDK 之前 URI 要用什麼包一層？ | pydantic 的 `AnyUrl` |
| Response 的 `contents` 是什麼？ | Resource content 物件 list，通常取 `result.contents[0]` |
| 如何解析 JSON 型 resource 回應？ | 檢查 `resource.mimeType == "application/json"`，回 `json.loads(resource.text)` |
| 如何解析純文字 resource 回應？ | 直接回 `resource.text` |
| Client 做 resource 存取需要哪兩個 import？ | `import json` 與 `from pydantic import AnyUrl` |
| 為什麼 resources 比 tool call 更有效率？ | 一次 round trip 就好，資料直接內嵌 prompt，跳過 tool_use / tool_result 迴圈 |
| 誰決定呼叫 `read_resource`？ | 應用（依使用者動作或策略），不是 Claude——Claude 不看 URI，只看到結果文字 |
