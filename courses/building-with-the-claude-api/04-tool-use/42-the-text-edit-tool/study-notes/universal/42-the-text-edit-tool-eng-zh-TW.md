# Text Editor Tool — Engineering Deep Dive

| 項目 | 內容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%)、D1 — Agentic Architecture (22%) |
| Task Statements | 2.3（built-in / server tools）、2.1（tool schema 與選擇）、1.2（tool 編排） |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 42 |

---

## One-Liner

Text editor tool 是 Anthropic 內建的 tool：Claude 本身已經知道完整 schema，你只需要宣告一個很小的 stub（`type` + `name`），然後自己寫執行 Claude 指令用的檔案操作實作。

---

## 為什麼叫「內建」Tool

大部分 tool 需要你準備兩件事：

1. 描述每個參數的完整 JSON schema
2. 實際執行的 Python 函式

Text editor tool 不一樣。Anthropic 在模型內部**預先定義好完整 schema**，涵蓋所有支援的檔案操作。你：

- **不需要**定義 `path`、`command`、`old_str`、`new_str` 這些參數
- **不需要**寫完整 JSON schema
- **需要**宣告一個小 stub 告訴 Claude「啟用這個內建 tool」
- **需要**寫實際操作檔案的本地函式

Claude 那一側是黑箱；你這一側依然重要。

---

## 支援的操作

Text editor tool 讓 Claude 能像使用本地編輯器的軟體工程師一樣工作：

| Operation | 功能 |
|-----------|-----|
| **view** | 讀取檔案或列出目錄；可以看特定行範圍 |
| **create** | 建立新檔案並寫入初始內容 |
| **str_replace** | 將檔案中某個字串換成另一個（最常見的編輯） |
| **insert** | 在指定行號插入文字 |
| **undo_edit** | 復原最近一次的編輯 |

這些合起來涵蓋核心編輯能力——讀、寫、建立、修改、還原。

---

## 宣告 Stub

Stub 的內容依 Claude 模型系列而異。Lesson 提供的 helper：

```python
def get_text_edit_schema(model: str) -> dict:
    if model.startswith("claude-3-7-sonnet"):
        return {
            "type": "text_editor_20250124",
            "name": "str_replace_editor",
        }
    elif model.startswith("claude-3-5-sonnet"):
        return {
            "type": "text_editor_20241022",
            "name": "str_replace_editor",
        }
    # 最新的 version string 請查 Anthropic 官方文件
```

重點：

- `type` 是**依模型系列 versioned** 的，字串必須跟你使用的模型對得上。Anthropic 把對應表放在 `docs.anthropic.com/en/docs/agents-and-tools/tool-use/text-editor-tool`。
- `name` 對應每個 version 是固定的（例如上面兩個版本都是 `str_replace_editor`）。
- Claude 會在內部把 stub 展開成完整 schema，你看不到參數定義。

---

## 當成一般 Tool 傳進去

```python
import anthropic

client = anthropic.Anthropic()
model = "claude-3-5-sonnet-20241022"

response = client.messages.create(
    model=model,
    max_tokens=2048,
    tools=[get_text_edit_schema(model)],
    messages=[
        {"role": "user", "content": "Open ./main.py 並摘要內容"},
    ],
)
```

Claude 會回傳一個 `tool_use` block，`name` 是 `str_replace_editor`，`input` 包含 Claude 想執行的指令（例如 `{"command": "view", "path": "./main.py"}`）。你的程式碼要依 `input["command"]` dispatch 並執行動作。

---

## 提供實作

你負責真正操作檔案系統。最小版本的 dispatcher：

```python
def run_text_editor(tool_input: dict) -> str:
    command = tool_input["command"]
    path = tool_input["path"]

    if command == "view":
        with open(path) as f:
            return f.read()

    elif command == "create":
        with open(path, "w") as f:
            f.write(tool_input["file_text"])
        return f"已建立 {path}"

    elif command == "str_replace":
        with open(path) as f:
            content = f.read()
        new_content = content.replace(
            tool_input["old_str"],
            tool_input["new_str"],
            1,
        )
        with open(path, "w") as f:
            f.write(new_content)
        return "替換完成"

    elif command == "insert":
        # 在 tool_input["insert_line"] 插入文字
        ...

    elif command == "undo_edit":
        # 還原前一版本
        ...

    else:
        return f"未知 command: {command}"
```

你決定：

- 什麼算 Claude 的檔案系統沙盒
- 是否允許寫入、只讀、或限制路徑
- 是否維護 undo stack 給 `undo_edit` 使用

---

## 範例 Workflow

Prompt：*「Open ./main.py，加入一個計算 pi 到小數第 5 位的函式，然後建立 ./test.py 並寫單元測試。」*

Claude 的 turn 序列：

1. `tool_use`：`view ./main.py`
2. 你的程式碼回傳檔案內容
3. `tool_use`：`str_replace` 注入新函式
4. 你的程式碼執行替換並回報
5. `tool_use`：`create ./test.py` 含單元測試內容
6. 你的程式碼建立檔案並回報
7. 最後 assistant text：「完成——已新增 `compute_pi` 並寫好測試。」

每個 `tool_use` 都是 agentic loop 中的一次來回。

---

## 為什麼需要 Text Editor Tool

既然現代編輯器已經內建 AI 助手，為什麼要透過 API 暴露這個？因為它可以：

- 為需要**以程式方式**編輯檔案的應用服務（如 codemod 服務、遷移 bot）
- 在**沒有完整編輯器**的 agent 環境中使用
- 讓 **Claude 驅動的應用**原生嵌入檔案編輯能力
- 在 CI pipeline 中做**無頭自動化**

簡言之，它讓你可以在自家產品中複製「AI code editor」的功能，並能對檔案系統介面做細緻控制。

---

## Common Mistakes

1. **模型與 version string 對不上** — `text_editor_20241022` 配 3.7 Sonnet 或反過來。請一律查 Anthropic 官方文件最新對應。
2. **試圖寫完整 JSON schema** — 只需要 stub，Claude 已經知道參數。
3. **沒實作 `undo_edit`** — Claude 嘗試還原時，你的 handler 若忽略，workflow 就壞了。
4. **沒做沙盒就執行** — Claude 可以寫任意檔案，必須限定目錄並驗證路徑。
5. **忘了 `view` 也能針對目錄** — 你必須支援列目錄，不只是讀檔。

> **Key Insight**
>
> 「內建」形容的是 **schema**，不是 **執行**。Anthropic 把 schema 知識放在模型裡，但你還是要自己寫真正操作檔案系統的 Python code。Text editor tool 是一種 hybrid：Anthropic 懂 API，你擁有 runtime。

---

## CCA Exam Relevance

- **D2 (Tool Design)**：Text editor tool 是 built-in（schema 內建）tool 的典型代表，由開發者提供執行邏輯。
- **D1 (Agentic Architecture)**：檔案操作鏈（view → edit → create → test）是典型的多輪 agentic 模式。
- 題目可能對比 built-in tool（如 text editor）與 server tool（如 web search），後者由 Anthropic 完全處理執行。

---

## Flashcards

| Front | Back |
|-------|------|
| 用 text editor tool 要宣告什麼？ | 一個小 stub，包含 `type`（versioned）與 `name`（例如 `str_replace_editor`） |
| Text editor tool 的 schema 由誰提供？ | Anthropic — Claude 已經知道參數，你不需要定義 |
| Text editor tool 的執行由誰提供？ | 開發者 — 你寫執行 Claude 指令的檔案操作函式 |
| Text editor tool 支援哪些操作？ | view、create、str_replace、insert、undo_edit |
| 為什麼 `type` 字串帶日期（如 `text_editor_20241022`）？ | 因為 schema 依 Claude 模型系列 versioned，version 必須對應你的模型 |
| Claude 能不能用這個 tool 看目錄？ | 可以——`view` 對檔案與目錄都有效 |
| 沒沙盒跑 text editor tool 有什麼風險？ | Claude 可以寫任意檔案，路徑驗證與沙盒目錄是必要的 |
| 既然編輯器已經有 AI，為什麼還需要這個 tool？ | 讓 Claude 驅動的應用嵌入程式化檔案編輯能力，適合 codemod、agent、無頭自動化 |
