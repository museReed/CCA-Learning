# MCP 複習 — 工程深入解析

| 項目 | 細節 |
|------|--------|
| 考試範疇 | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP server primitives), 2.4-2.6 (resource/tool/prompt design), 1.1 (agentic architecture) |
| 來源 | introduction-to-model-context-protocol / 04-assessment / Lesson 15 |

---

## 一句話摘要

MCP 有三個核心 server primitives — Tools（model-controlled）、Resources（app-controlled）和 Prompts（user-controlled）— 選擇正確的那個取決於誰應該控制互動。

---

![Three Primitives](../../visuals/three-primitives-zh-TW.svg)


## 三大 Primitives：完整參考

### 1. Tools — Model-Controlled

Claude 在推理過程中決定何時、如何呼叫 tools。

```python
@mcp.tool()
def calculate_sqrt(number: float) -> float:
    """Calculate the square root of a number."""
    return math.sqrt(number)
```

**何時使用**：給 Claude 原生沒有的能力 — 資料庫查詢、API 呼叫、檔案操作、計算、程式碼執行。

**關鍵特性**：
- Claude 自主決定呼叫時機
- 結果回饋到 Claude 的推理中
- 可以有副作用（寫入、刪除、發送）

### 2. Resources — App-Controlled

你的應用程式碼決定何時取得 resource 資料。

```python
@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def fetch_doc(doc_id: str) -> str:
    return docs[doc_id]
```

**何時使用**：為 UI 顯示取得資料或將 context 注入 prompt — 自動完成列表、文件提及、側邊欄面板。

**關鍵特性**：
- 應用程式碼呼叫 `read_resource()`，不是 Claude
- 內容直接注入 prompt（無 tool call 開銷）
- 唯讀 — 無副作用

### 3. Prompts — User-Controlled

使用者透過 UI 互動明確觸發預定義工作流程。

```python
@mcp.prompt(name="format", description="Rewrite document in Markdown")
def format_document(doc_id: str = Field(...)) -> list[base.Message]:
    return [base.UserMessage(f"Reformat document {doc_id} to markdown...")]
```

**何時使用**：使用者按需觸發的預定義、可重複工作流程 — slash commands、工作流程按鈕。

**關鍵特性**：
- 使用者透過 `/command`、按鈕點擊或選單選擇觸發
- 回傳 `list[base.Message]` 發送給 Claude
- 常編排 tools（prompts 提供指令，tools 提供能力）

---

## 決策指南

這是 CCA 考試最重要的決策框架：

```
需要給 Claude 新能力？
  → TOOLS（model-controlled）

需要為 UI 顯示或 prompt context 取得資料？
  → RESOURCES（app-controlled）

想要使用者可觸發的預定義工作流程？
  → PROMPTS（user-controlled）
```

### 延伸決策矩陣

| 場景 | Primitive | 原因 |
|----------|-----------|-----|
| Claude 計算一個值 | Tool | Claude 決定何時計算 |
| 自動完成下拉顯示文件 | Resource | App 為 UI 取得列表 |
| 使用者輸入 `@plan.md` 注入 context | Resource | App 取得並注入內容 |
| 使用者輸入 `/format` 重新格式化文件 | Prompt | 使用者明確觸發工作流程 |
| Claude 在對話中查詢資料庫 | Tool | Claude 決定何時查詢 |
| 使用者點擊「摘要」按鈕 | Prompt | 使用者觸發預定義工作流程 |

---

## 控制模型總結表

| 面向 | Tools | Resources | Prompts |
|-----------|-------|-----------|---------|
| 控制者 | Claude（model） | App 程式碼 | 使用者 |
| 觸發 | Claude 的推理 | `read_resource()` 呼叫 | `/` 命令或按鈕 |
| 副作用 | 有（寫入、發送、刪除） | 無（唯讀） | 無（只有訊息） |
| 回傳類型 | Tool result | 含 MIME type 的內容 | `list[base.Message]` |
| Decorator | `@mcp.tool()` | `@mcp.resource()` | `@mcp.prompt()` |
| Client 方法 | `call_tool()` | `read_resource()` | `get_prompt()` |
| 發現 | `list_tools()` | `list_resources()` | `list_prompts()` |
| UX 模式 | 對使用者不可見 | `@mention` 自動完成 | `/` slash commands |

---

## 它們如何協作

在真實應用中，三個 primitives 協作：

1. **Resources** 用可用文件填充 UI（自動完成）
2. **Prompts** 讓使用者觸發工作流程（`/format plan.md`）
3. Prompt 告訴 Claude 重新格式化文件
4. Claude 使用 **Tools** 讀取和編輯文件
5. 結果出現在聊天中

這是完整的 MCP 堆疊：Resources 供給資料 → Prompts 編排工作流程 → Tools 執行動作。

---

## 常見錯誤

1. **該用 resource 的場景用了 tool** — 唯讀資料用於 UI/context 時，resource 更快（無 tool call 開銷）
2. **該用 prompt 的場景用了 tool** — 使用者明確觸發的工作流程，用 prompt（更好的 UX、更一致）
3. **混淆控制模型** — 最重要的區分是「誰」控制：model、app 還是 user
4. **忘記 prompts 編排 tools** — prompts 和 tools 是互補的，不是競爭的
5. **建立有副作用的 resources** — resources 必須唯讀；副作用屬於 tools

> **Key Insight**
>
> 三方控制模型（Tools = model-controlled、Resources = app-controlled、Prompts = user-controlled）是 MCP 架構的基礎概念。每個「該用哪個 primitive？」的考題都可以用一個問題回答：「誰應該控制這個互動？」這個問題解決了 CCA 考試中絕大多數 D2 情境題。

---

## CCA 考試關聯

- **D2 (Tool Design & MCP Integration)**：本課是總結。Lessons 5-13 的每個概念都匯入「哪個 primitive？」的決策。
- **D1 (Agentic Architecture)**：控制模型對應 agent 架構層 — 模型層（tools）、應用層（resources）、使用者層（prompts）。
- **考試策略**：看到情境題時，先辨識控制者（model/app/user），然後選對應的 primitive。

---

## Flashcards

| 正面 | 背面 |
|-------|------|
| MCP 的三個 server primitives 是什麼？ | Tools（model-controlled）、Resources（app-controlled）、Prompts（user-controlled） |
| 誰控制 MCP 中的 Tools？ | Claude（model-controlled）— Claude 在推理時決定何時、如何呼叫 tools |
| 誰控制 MCP 中的 Resources？ | 應用程式碼（app-controlled）— 你的程式碼呼叫 `read_resource()` 取得資料 |
| 誰控制 MCP 中的 Prompts？ | 使用者（user-controlled）— 透過 slash commands、按鈕或選單觸發 |
| 何時該用 Tool 而非 Resource？ | Tool：Claude 需要能力（動作、副作用）。Resource：app 需要唯讀資料用於 UI 或 context |
| 何時該用 Prompt 而非 Tool？ | Prompt：使用者明確觸發預定義工作流程。Tool：Claude 自主決定行動 |
| 選擇 MCP primitive 的決策問題是什麼？ | 「誰應該控制這個互動？」— Model = Tool、App = Resource、User = Prompt |
| 三個 primitives 如何協作？ | Resources 供給資料到 UI、Prompts 為使用者編排工作流程、Tools 為 Claude 執行動作 |
