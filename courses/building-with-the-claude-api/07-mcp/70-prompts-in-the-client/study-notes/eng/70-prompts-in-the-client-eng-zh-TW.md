# Prompts in the Client — Engineering Deep Dive（繁體中文）

| 項目 | 說明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（MCP primitives：client 端 prompt 存取）、1.2（seed agent loop）、2.2（message content blocks） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 70 |

---

## One-Liner

從 client 使用 prompt 就是在 MCP client 加兩個方法：`list_prompts()` 做探索、`get_prompt(name, args)` 取得已插值的訊息 list，直接送給 Claude 當作新對話的開場。

---

## Client 端契約

Server 用 `@mcp.prompt()` 定義的 prompt，要 client 暴露兩個方法才真正可用：

1. **`list_prompts()`** — 回傳 server 知道的所有 prompt，含名字、描述、參數 metadata
2. **`get_prompt(prompt_name, args)`** — 用給定參數執行 server 的 prompt function，回傳結果訊息 list

兩個方法準備好後，應用就能做 slash menu UI、為每個 prompt 顯示描述、向使用者收參數、然後啟動一個組好的 Claude 對話。

---

## 實作 `list_prompts`

```python
async def list_prompts(self) -> list[types.Prompt]:
    result = await self.session().list_prompts()
    return result.prompts
```

這是對 session 的直通：

- `self.session().list_prompts()` 呼叫 MCP SDK，向 server 問目前註冊的 prompt
- SDK 回 `ListPromptsResult`，你把 `result.prompts` 當作 `types.Prompt` list 回出去

每個 `types.Prompt` 物件帶：

- `name` — 字串識別（例如 `"format"`）
- `description` — UI 顯示用的人類可讀說明
- 參數 metadata — 名字、描述、是否必填

應用用這些資訊組 picker、驗證輸入、或做權限控制。

---

## 實作 `get_prompt`

```python
async def get_prompt(self, prompt_name, args: dict[str, str]):
    result = await self.session().get_prompt(prompt_name, args)
    return result.messages
```

這個方法帶參數抓指定的 prompt：

- `prompt_name` — 從 `list_prompts()` 看到的名字
- `args` — dict，key 對應 server 端 function 的參數名
- session 的 `get_prompt` 發請求給 server，server 執行 prompt function 並回傳 `list[base.Message]`
- 你把 `result.messages` 回出去——就是可以直接送給 Claude 的對話

---

## Prompt 參數怎麼運作

Server 端 prompt function 會有參數。例如：

```python
def format_document(doc_id: str):
    # doc_id 會被插值進 prompt 模板
```

Client 呼叫 `get_prompt("format", {"doc_id": "report.pdf"})` 時，MCP SDK 會把 dict 當 keyword arguments 餵給 `format_document(doc_id="report.pdf")`。Function 執行、插值、回訊息 list。Client 看不到中間模板，只看到最終訊息。

這種參數化是 prompt 能重用的原因：一個 server 端模板服務無限的參數組合。

---

## 在 CLI 測試 Prompts

`list_prompts` 與 `get_prompt` 接好後，CLI 會把 prompts 暴露成 slash-command。打 `/` 會跳出 prompt 選單。選一個之後可能會再要你填一些參數（例如「要 format 哪份文件？」），接著完成的 prompt 送給 Claude。

典型 workflow：

1. **使用者選 prompt**（例如 `/format`）
2. **系統要求必要參數**（例如哪份文件）
3. **Client 呼叫 `get_prompt(name, args)`** — 收到插值後的訊息
4. **Client 把訊息送給 Claude** — Claude 用這個 seed 開始對話
5. **Claude 正常進行** — 可能呼叫 tool、讀 resource、產最終答案

---

## 完整 Prompt 驅動的 Agent Loop

從 server 作者角度看，prompt 是食譜；從 client 角度看，是預組好的對話開場。合起來：

```
┌──────────┐                       ┌────────────┐    list_prompts()      ┌────────────┐
│  User    │                       │ Application│ ─────────────────────▶ │ MCP Server │
│          │                       │ (+ client) │                        │            │
│          │   選 "format"          │            │                        │            │
│          │ ─────────────────────▶ │            │                        │            │
│          │   doc_id="report.pdf"  │            │    get_prompt(...)     │            │
│          │ ─────────────────────▶ │            │ ─────────────────────▶ │            │
│          │                        │            │ ◀───────────────────── │            │
│          │                        │            │   messages=[...]       └────────────┘
│          │                        │            │                              │
│          │                        │            │   第一次呼叫 Claude          │
│          │                        │            │ ─────────────────────▶ ┌──────────┐
│          │                        │            │ ◀───────────────────── │  Claude  │
│          │                        │            │   tool_use(...)        │   API    │
│          │                        │            │                        └──────────┘
│          │                        │            │   loop 繼續...
└──────────┘                        └────────────┘
```

Prompt 只 seed 對話，之後 tool use、resource access、多輪推理都照常走。

---

## Prompt Best Practices（本課提到）

- 與 server 用途相關
- 上線前充分測試
- 清楚具體的指令
- 設計時考慮與現有 tool 的協作
- 仔細想使用者要提供什麼參數

對應 Lesson 69 的 server 端 best practices，client 是 prompt 的消費者。

---

## Common Mistakes

1. **把 `get_prompt` 結果當純文字** — 它是 **訊息 list**，要用 Anthropic API 的 messages 參數送，不是單一使用者字串
2. **傳錯參數名** — `args` 的 key 要跟 server prompt function 的參數名完全一致，不一致就噴錯
3. **沒先呼叫 `list_prompts` 就呼 `get_prompt`** — 技術上可以，但失去做 UI 與驗證的機會
4. **跨 session 快取 prompt 結果** — Prompt 輸出是新對話的模板，後續對話狀態是 per-session，快取訊息會誤導狀態模型
5. **忽略 description metadata** — prompts 的重點就是可發現性，把 description 傳進 UI

> **Key Insight**
>
> `list_prompts` 與 `get_prompt` 很小——兩個方法、幾行程式——卻是 MCP 產品表面的收尾。有了它們，你的 client 就多了「server 作者維護的預先工程化動作選單」。每次 server 作者改進一個 prompt，所有用它的 client 都自動升級。這種不對稱複利讓 prompts 變成三種 MCP 原語中對 PM 最友善的一個。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：知道 client 側兩個方法（`list_prompts`、`get_prompt`）、dict 傳參、回傳 `list[base.Message]`
- **D1（Agentic Architecture）**：Prompts 用策劃的對話開場 seed agent loop，後續照常
- 考題模式：「Client 如何帶參數抓 prompt？」→ `await self.session().get_prompt(prompt_name, args)` 並回傳 `result.messages`

---

## Flashcards

| Front | Back |
|-------|------|
| 使用 prompts 需要哪兩個 client 方法？ | `list_prompts()` 做探索、`get_prompt(prompt_name, args)` 取插值後的訊息 list |
| `list_prompts()` 回傳什麼？ | `result.prompts`——`types.Prompt` list，含 name、description、參數 metadata |
| `get_prompt` 回傳什麼？ | `result.messages`——`list[base.Message]`，可直接送給 Claude |
| Prompt 參數怎麼傳？ | 用 `dict[str, str]`，key 對應 server prompt function 的參數名 |
| Client 呼叫 `get_prompt` 時 server 做什麼？ | 用 args 當 keyword arguments 執行裝飾過的 prompt function，回結果訊息 list |
| Client 拿到訊息後怎麼用？ | 送給 Claude 當新對話的開場，agent loop 照常進行（tool、resource、多輪） |
| CLI 中 prompt 怎麼呈現給使用者？ | Slash-command（例如 `/format`），可選擇的參數 picker，然後送給 Claude |
| 為什麼跨 session 快取 `get_prompt` 結果有風險？ | Prompt 輸出是新對話的模板，後續狀態是 per-session，快取訊息會誤導應用的狀態模型 |
