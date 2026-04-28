# Client 端的 Prompts — 工程深入解析

| 項目 | 細節 |
|------|--------|
| 考試範疇 | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.3 (MCP client implementation), 2.6 (prompt consumption patterns), 1.3 (prompt orchestration) |
| 來源 | introduction-to-model-context-protocol / 03-resources-and-prompts / Lesson 13 |

---

## 一句話摘要

Client 實作 `list_prompts()` 來發現可用 prompts，以及 `get_prompt(name, args)` 來取得插值後的訊息，啟用 slash command（`/`）UX 模式，讓使用者觸發預定義工作流程。

---

## 兩個 Client 端方法

### 1. `list_prompts()` — 發現

```python
async def list_prompts(self) -> list[types.Prompt]:
    result = await self.session().list_prompts()
    return result.prompts
```

此方法向 server 查詢所有可用 prompts。每個 `types.Prompt` 物件包含：
- `name` — 識別碼（用於 slash commands）
- `description` — 人類可讀的說明
- `arguments` — 必要/可選參數列表

### 2. `get_prompt()` — 帶插值的取得

```python
async def get_prompt(self, prompt_name, args: dict[str, str]):
    result = await self.session().get_prompt(prompt_name, args)
    return result.messages
```

此方法取得特定 prompt 並進行變數插值：
- `prompt_name` — 要取得哪個 prompt（如 `"format"`）
- `args` — 字串對字串的 dict（如 `{"doc_id": "plan.md"}`）
- 回傳 `result.messages` — 準備好發送給 Claude 的 `base.Message` 物件列表

---

## 完整的 Prompt 工作流程

從使用者互動到 Claude 回應的端到端流程：

```
1. 使用者輸入 "/"
   └── Client 呼叫 list_prompts()
       └── Server 回傳可用 prompts

2. 使用者選擇 "/format"
   └── Client 顯示參數輸入
       └── 使用者提供 doc_id = "plan.md"

3. Client 呼叫 get_prompt("format", {"doc_id": "plan.md"})
   └── Server 執行 format_document(doc_id="plan.md")
       └── 回傳插值後的訊息

4. Client 將訊息發送給 Claude
   └── Claude 收到專家級指令
       └── Claude 使用 tools（如 edit_document）來完成

5. Claude 回應格式化後的文件
```

### 關鍵洞察：Prompts 編排 Tools

Claude 收到 prompt 訊息後，通常需要使用可用的 **tools** 來完成任務。Prompts 提供指令，tools 提供能力。

---

## 三方控制模型

這是 Lessons 10-13 中最重要的概念，也是 CCA 考試核心主題：

| Primitive | 控制者 | 觸發機制 | 類比 |
|-----------|-----------|-------------------|---------|
| **Tools** | Model-controlled | Claude 在推理時決定 | 主廚決定用什麼食材 |
| **Resources** | App-controlled | 你的程式碼呼叫 `read_resource()` | 服務生自動送水 |
| **Prompts** | User-controlled | 使用者輸入 `/` 或點擊按鈕 | 顧客從菜單點餐 |

對應 Claude 官方介面：
- **Tools** — Claude 在幕後執行程式碼或計算
- **Resources** — 「Add from Google Drive」功能注入文件 context
- **Prompts** — 聊天輸入下方的工作流程按鈕

---

## Slash Commands：UX 模式

| 步驟 | 使用者行為 | Client 行為 |
|------|-------------|-----------------|
| 1 | 輸入 `/` | 呼叫 `list_prompts()`，顯示命令選單 |
| 2 | 選擇命令 | 根據 prompt arguments 顯示參數表單 |
| 3 | 提供參數 | 驗證輸入，準備 args dict |
| 4 | 確認 | 呼叫 `get_prompt(name, args)`，取得訊息 |
| 5 | （自動） | 將訊息發送給 Claude，顯示回應 |

---

## Prompt Arguments：變數插值

`get_prompt()` 中的 `args` 參數始終是 `dict[str, str]` — 所有值都是字串：

```python
# Client 端
messages = await client.get_prompt("format", {"doc_id": "plan.md"})

# Server 端（內部發生的事）
def format_document(doc_id: str = Field(...)):
    # doc_id = "plan.md" — 從 args 插值而來
    prompt = f"...{doc_id}..."
    return [base.UserMessage(prompt)]
```

即使參數代表數字或布林值，也以字串傳遞。Server function 處理必要的類型轉換。

---

## 常見錯誤

1. **混淆 `list_prompts()` 和 `get_prompt()`** — `list_prompts()` 回傳 metadata（名稱、描述），`get_prompt()` 回傳實際插值後的訊息
2. **非字串的 args 值** — `args` dict 必須是 `dict[str, str]`，不是 `dict[str, Any]`
3. **錯誤發送 prompt 訊息** — `get_prompt()` 的訊息直接進入對話，就像使用者打的一樣
4. **忘記 prompts 使用 tools** — prompts 提供指令，但 Claude 通常需要 tools 來完成任務；兩者都必須可用

> **Key Insight**
>
> 三方控制模型（Tools = model-controlled、Resources = app-controlled、Prompts = user-controlled）是 CCA 考試中最重要的 MCP 架構概念。每個 primitive 服務不同的利害關係人：tools 服務 Claude，resources 服務你的應用，prompts 服務你的使用者。

---

## CCA 考試關聯

- **D2 (Tool Design & MCP Integration)**：要知道兩個 client 方法 — `list_prompts()` 用於發現，`get_prompt(name, args)` 用於取得。`args` dict 是 `dict[str, str]`。
- **D1 (Agentic Architecture)**：三方控制模型是基石概念。預期情境題會問根據控制者該用哪個 primitive。
- 考題中出現「slash command」、「workflow button」或「user triggers」幾乎都指向 prompts。

---

## Flashcards

| 正面 | 背面 |
|-------|------|
| 處理 MCP prompts 的兩個 client 方法是什麼？ | `list_prompts()` 用於發現可用 prompts，`get_prompt(name, args)` 用於取得插值後的訊息 |
| `get_prompt()` 中 `args` 參數的類型是什麼？ | `dict[str, str]` — 所有 key 和 value 都是字串 |
| `get_prompt()` 回傳什麼？ | `result.messages` — 準備好發送給 Claude 的 `base.Message` 物件列表 |
| MCP prompts 對應什麼 UI 模式？ | Slash commands（`/`）— 使用者輸入 `/`、看到可用命令、選擇一個、提供參數 |
| Prompts 和 tools 如何協作？ | Prompts 提供指令（做什麼），tools 提供能力（怎麼做）— Claude 使用 tools 來完成 prompt 指令 |
| 三種 MCP 控制模型是什麼？ | Tools = model-controlled（Claude 決定）、Resources = app-controlled（你的程式碼決定）、Prompts = user-controlled（使用者決定） |
| 典型 client 中什麼觸發 `list_prompts()`？ | 使用者在聊天輸入中輸入 `/` — client 向 server 查詢可用 prompts |
| Claude 官方介面中什麼展示了 prompt 模式？ | 聊天輸入下方的工作流程按鈕 — 預定義的、使用者觸發的工作流程 |
