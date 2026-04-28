# 定義 Prompts — 工程深入解析

| 項目 | 細節 |
|------|--------|
| 考試範疇 | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server primitives), 2.6 (prompt template design), 1.3 (prompt engineering for tools) |
| 來源 | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 12 |

---

## 一句話摘要

MCP prompts 是 server 端定義的參數化訊息模板，回傳 `list[base.Message]`，為使用者提供預先建立且經過測試的指令，效果優於臨時撰寫的 prompt。

---

## 為什麼需要 Prompts

使用者已經可以直接向 Claude 提出任何要求。MCP prompts 的價值在於**專業知識封裝**：

| 方式 | 品質 | 一致性 | 維護 |
|----------|---------|-------------|-------------|
| 使用者自己寫 prompt | 不穩定 — 取決於使用者能力 | 低 — 每次不同 | 無 — 一次性 |
| MCP server 提供 prompt | 高 — 經開發者測試 | 高 — 每次用相同模板 | 集中化 — 更新一次，所有 client 受益 |

---

## `@mcp.prompt()` Decorator

Prompts 遵循與 tools 和 resources 相同的 decorator 模式：

```python
@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format."
)
def format_document(
    doc_id: str = Field(description="Id of the document to format")
) -> list[base.Message]:
    prompt = f"""
Your goal is to reformat a document to be written with markdown syntax.

The id of the document you need to reformat is:
<document_id>
{doc_id}
</document_id>

Add in headers, bullet points, tables, etc as necessary.
Feel free to add in structure.
Use the 'edit_document' tool to edit the document.
After the document has been reformatted...
"""
    return [
        base.UserMessage(prompt)
    ]
```

### 關鍵實作細節

1. **`name` 參數** — 成為 slash command 識別碼（如 `/format`）
2. **`description` 參數** — 在 prompt 列表中顯示給使用者
3. **`Field(description=...)`** — Pydantic Field 用於參數文件說明
4. **回傳類型 `list[base.Message]`** — 訊息列表（UserMessage、AssistantMessage）送給 Claude
5. **f-string 插值** — `{doc_id}` 在執行時替換為實際參數值

---

## Prompt 中的訊息類型

Prompts 回傳訊息列表，可以包含：

```python
# 單一使用者訊息（最常見）
return [base.UserMessage(prompt_text)]

# 多輪對話（用於複雜工作流程）
return [
    base.UserMessage("Here is the task..."),
    base.AssistantMessage("I understand. Let me..."),
    base.UserMessage("Now proceed with step 2...")
]
```

多輪 prompts 適用於：
- **Few-shot 範例** — 在實際任務前示範 Claude 如何回應
- **複雜工作流程** — 引導 Claude 完成多步驟流程
- **角色設定** — 在任務指令前建立 Claude 的角色

---

## Prompt vs. Tool vs. Resource：控制模型

| Primitive | 控制者 | 觸發方式 | 範例 |
|-----------|-----------|---------|---------|
| **Tool** | Claude（model-controlled） | Claude 在推理時決定 | `calculate_sqrt(3)` |
| **Resource** | 應用程式碼（app-controlled） | 你的程式碼呼叫 `read_resource()` | `@plan.md` 自動完成 |
| **Prompt** | 使用者（user-controlled） | 使用者輸入 `/format` 或點擊按鈕 | `/format doc_id=plan.md` |

---

## 使用 MCP Inspector 測試

```bash
uv run mcp dev mcp_server.py
```

在 Inspector 中：
1. 切換到 **Prompts** 分頁
2. 從列表中選擇 prompt
3. 填入參數值（如 `doc_id = "plan.md"`）
4. 點擊「Get Prompt」查看插值後的訊息
5. 驗證 f-string 變數正確替換

---

## 設計最佳實踐

1. **用 XML tag 標記變數邊界** — `<document_id>{doc_id}</document_id>` 防止 prompt injection
2. **在 prompt 中引用可用的 tools** — 告訴 Claude 該用哪些 tools
3. **明確指定輸出格式** — 如果要 markdown，就說「written with markdown syntax」
4. **用邊界案例測試** — 空字串、長文件、特殊字元
5. **保持 prompts 領域專屬** — 文件 server 有格式化 prompts，資料 server 有分析 prompts

---

## 常見錯誤

1. **回傳字串而非 `list[base.Message]`** — prompts 必須回傳 Message 物件列表
2. **忘記參數文件說明** — 用 `Field(description=...)` 讓使用者知道要提供什麼
3. **沒有引用 tools** — 如果 prompt 預期 Claude 使用特定 tools，要在 prompt 文字中明確提及
4. **過於泛用的 prompts** — prompts 應善用 server 的特定功能

> **Key Insight**
>
> Prompts 是 MCP 中的 **user-controlled** primitive。不同於 tools（Claude 決定何時行動）或 resources（你的 app 決定何時取得），prompts 透過 slash commands 或 UI 按鈕給使用者明確控制權。CCA 考試中，三方控制模型（model / app / user）是高頻考點。

---

## CCA 考試關聯

- **D2 (Tool Design & MCP Integration)**：要熟悉 `@mcp.prompt()` decorator 模式、回傳類型（`list[base.Message]`）、以及透過 Pydantic `Field` 的參數處理。
- **D1 (Agentic Architecture)**：Prompts 代表 MCP 控制模型的使用者控制層。
- 考試關鍵區分：「使用者觸發的預定義工作流程」= prompt。「Claude 決定行動」= tool。「App 取得資料」= resource。

---

## Flashcards

| 正面 | 背面 |
|-------|------|
| MCP prompt function 回傳什麼？ | `list[base.Message]` — UserMessage 和/或 AssistantMessage 物件的列表 |
| 誰控制 MCP prompts 的觸發時機？ | 使用者（user-controlled）— 透過 slash commands、按鈕或選單 |
| 定義 MCP prompt 的 decorator 是什麼？ | `@mcp.prompt(name="...", description="...")` |
| 如何為使用者說明 prompt 參數？ | 在 function 參數上使用 Pydantic `Field(description="...")` |
| 為什麼在 prompt 模板中使用 XML tag 如 `<document_id>`？ | 明確標記變數邊界、防止 prompt injection、幫助 Claude 識別結構化資料 |
| MCP 中 prompts 和 tools 的區別是什麼？ | Prompts 是 user-controlled（使用者明確觸發），tools 是 model-controlled（Claude 決定何時呼叫） |
| MCP prompts 可以包含多輪對話嗎？ | 可以 — 回傳多個 UserMessage 和 AssistantMessage 物件，用於 few-shot 範例或複雜工作流程 |
| 部署前如何測試 prompts？ | 使用 MCP Inspector — 切換到 Prompts 分頁，填入參數，驗證插值後的訊息 |
