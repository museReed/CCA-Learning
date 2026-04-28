# Defining Prompts — Engineering Deep Dive（繁體中文）

| 項目 | 說明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（MCP primitives：tools、resources、prompts）、1.2（seed agent loop）、2.2（base.Message content blocks） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 69 |

---

## One-Liner

Prompts 是 MCP 的第三個原語——預先調校過、高品質的指令模板。Server 作者把「怎麼寫才會得到好結果」的 know-how 封裝起來，讓 client 可以用名字呼叫，而不是要求終端使用者自己學 prompt engineering。

---

## Prompts 解決的問題

使用者當然可以自己寫指令——「convert report.pdf to markdown」也會動。但結果的好壞完全取決於 prompt 寫得多好，而多數使用者不是 prompt 工程師。本課的核心觀點：

> 使用者雖然能自己完成任務，但使用 server 作者精心設計與測試過的 prompt，能得到更一致、更高品質的結果。

Prompts 把專家知識外部化。開發者知道怎麼寫一個能產出優質 markdown 的 prompt，就把它烘焙成 server 端可重用的模板。

---

## Prompts 在 MCP 原語中的位置

| 原語 | 目的 | 範例 |
|------|------|------|
| Tool | 執行動作 | `edit_document(doc_id, new_content)` |
| Resource | 暴露資料 | `docs://documents/{doc_id}` |
| Prompt | 預先調校的指令模板 | `format(doc_id)` 把文件改成 markdown |

Prompt 不是「Claude 要讀的文字」，而是一個 **可呼叫的模板**：client 帶參數呼叫，拿回一串可以直接送給 Claude 的訊息。

---

## Prompts 怎麼運作

- 用 `@mcp.prompt()` 裝飾器定義
- 每個 prompt 帶 `name` 與 `description`
- 回傳一個訊息 list（user / assistant），組成完整的對話開場
- Prompt 應該高品質、測試過、與 server 主要用途相關

Client 後續用名字呼叫時，server 會用 client 提供的參數執行裝飾過的 function，把回傳的訊息 list 轉交給 client，client 原封不動送給 Claude。

---

## 實作 Format 指令 — Imports

先從 MCP SDK import base message types：

```python
from mcp.server.fastmcp import base
```

`base` 提供 `UserMessage`、`AssistantMessage` 等型別化物件，用來組 prompt 的訊息 list。

---

## 實作 Format 指令 — 定義

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

{doc_id}


Add in headers, bullet points, tables, etc as necessary. Feel free to add in extra formatting.
Use the 'edit_document' tool to edit the document. After the document has been reformatted...
"""

    return [
        base.UserMessage(prompt)
    ]
```

重點：

- `@mcp.prompt(name=..., description=...)` 把 prompt 註冊到 server，client 列清單時會看到這些字串
- `doc_id: str = Field(description="...")` 是帶 metadata 的參數，description 會傳給 client 讓使用者知道要填什麼
- Function body 用 f-string 組多行模板，回傳 **訊息 list**，這裡只有一則 `UserMessage`
- 注意 prompt 內文引用了 `edit_document` **tool**——prompt 可以跟 server 其他 tool / resource 一起合奏，是「用 server 能力組出工作流」的 recipe

---

## 為什麼回傳型別是 `list[base.Message]`

Prompts 可以編碼多輪對話。例如你也可以預先塞一則 assistant 訊息：

- `base.UserMessage(...)` — 使用者「說」的
- `base.AssistantMessage(...)` — 預先放的 assistant 回應（適合 few-shot conditioning）

回傳 list 讓 server 作者完全控制 prompt 啟動時 Claude 看到的對話狀態，client 只是播放訊息。

---

## 用 MCP Inspector 測試

Inspector 有專門的 Prompts 區。測試步驟：

1. 跑 `uv run mcp dev mcp_server.py`
2. 瀏覽器打開 Inspector
3. 進 Prompts、選 prompt、填參數
4. Inspector 會顯示產生的訊息（就是即將送給 Claude 的內容）

這讓你在接 client 之前就能確認變數有正確插值、訊息結構符合預期。

---

## Best Practices

本課提到：

1. **專注在 server 主要用途的任務** — 文件 server 該出 `format`、`summarize`、`outline` 這類 prompt
2. **寫詳細具體的指令** — 模糊 prompt 產出模糊結果
3. **用不同輸入徹底測試** — 用 Inspector
4. **描述要清楚** — 使用者依 description 選擇 prompt
5. **設計 prompt 與 tool / resource 合奏** — 範圍清楚的 prompt 會自然串到 server 的 tool（例如 format prompt 最後呼叫 `edit_document`）

核心觀點：**Prompt 是你身為 server 作者的專業**，以 client 可呼叫的形式封存。若使用者三十秒內能自己寫出來，大概不需要做成 prompt；若你花了一週才調出最佳措辭，那才是值得暴露的知識。

---

## Common Mistakes

1. **把 prompt 當 raw 字串** — prompt 是 callable，回傳 `base.Message` list，不是模板字串
2. **忘了 `Field(description=...)`** — 沒有它，client 側無法告訴使用者要填什麼
3. **把 prompt 該抓的資料寫死** — 若 prompt 要文件文字，應該引用對應的 tool / resource，不要把資料烘焙進 prompt
4. **寫低成本 prompt** — 比使用者自己打的還差的 prompt 是負價值，只上你真的證明比 ad-hoc 更好的 prompt
5. **混淆 prompt 與 resource** — Prompt 是指令模板，resource 是資料，不要用 prompt 回文件內容

> **Key Insight**
>
> Prompts 是大多數 MCP 討論忽略的原語。Tools 給 Claude 能力，resources 給 context，prompts 給 **方向**。三個原語都有的 server 組合起來就像個小產品：client 能發現「能做什麼」（tools）、「有什麼資料」（resources）、「有哪些精心策劃的起點」（prompts）。實務上，prompt 會變成使用者看到的 slash-command 或快捷動作。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：Prompts 是 tools、resources 之外的第三種 MCP 原語；知道 `@mcp.prompt()` 裝飾器、`name` / `description`、回傳型別 `list[base.Message]`、參數的 `Field(description=...)`
- **D1（Agentic Architecture）**：Prompts 用 server 作者預先工程化的高品質開場訊息 seed agent loop
- 考題模式：「Server 作者要上線一個可重用、帶參數的文件改寫 markdown 指令，該用哪個 MCP 原語？」→ prompt，用 `@mcp.prompt()` 定義

---

## Flashcards

| Front | Back |
|-------|------|
| MCP 的 prompts 是什麼？ | Server 定義的預先調校、帶參數的指令模板，client 可用名字呼叫，取得給 Claude 的高品質對話開場 |
| 定義 prompt 的裝飾器？ | `@mcp.prompt(name=..., description=...)` |
| Prompt function 回傳什麼？ | `list[base.Message]`——組成對話開場的 user/assistant 訊息 list |
| base message types 從哪裡 import？ | `from mcp.server.fastmcp import base`，提供 `base.UserMessage`、`base.AssistantMessage` 等 |
| 參數 description 怎麼到使用者？ | 透過 `Field(description="...")` 放在參數上，MCP SDK 會傳給 client |
| 為什麼要出 prompt 而不是讓使用者自己寫？ | Server 作者有測過的專業級 prompt，暴露出來可以在不要求使用者學 prompt engineering 的情況下提升結果品質 |
| 怎麼在接 client 之前測 prompt？ | 跑 `uv run mcp dev mcp_server.py`，用 MCP Inspector 的 Prompts 區看產生的訊息 |
| Format 範例怎麼與其他 MCP 原語連動？ | 它引用 `edit_document` tool，顯示 prompt 可以串接 tool 與 resource 完成任務 |
