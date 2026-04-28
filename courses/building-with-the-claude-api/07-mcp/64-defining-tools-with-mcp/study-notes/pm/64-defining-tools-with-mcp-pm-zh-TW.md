# Defining Tools with MCP — PM 視角

| 項目 | 說明 |
|------|------|
| 考試領域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.1（tool schemas）、2.3（MCP primitives：tools）、1.2（agent loop 整合） |
| 來源 | building-with-the-claude-api / 07-mcp / Lesson 64 |

---

## 一句話總結

Lesson 64 是 tool 撰寫變**便宜**的時刻：Python MCP SDK 把手寫 JSON Schema 替換成 decorated function，把「寫出第一個 tool 的時間」從「一整天樣板」壓縮到「一段 Python」——這會改變 PM 該怎麼 scope AI 功能。

---

## 心智模型：從電路圖到名片

SDK 出現之前，加 tool 像在畫電路圖：

| SDK 之前（手寫 JSON） | 有 SDK（decorator + type hints） |
|--------------------|-----------------------------|
| 長長的 JSON Schema 文件 | Decorated Python function |
| 很容易漏 `required` key | SDK 從 function signature 自動填 |
| 非作者工程師難讀 | 讀起來像業務邏輯 |
| 文件離 code 很遠 | Description 就在參數旁邊 |

把 MCP tool（加上 SDK）想像成**名片**：小、標準化、易讀——新 tool 幾行就能寫完，直接遞給 Claude 用。

---

## 為什麼這節課對 PM 重要

SDK 的人體工學帶來三個產品層級的後果：

1. **Tool 數量變便宜。** 加一個新 tool 只要幾分鐘，PM 可以安全地要求更細緻的功能——每個 intent 一個 tool——而不是把行為塞在 mega-tool 裡。
2. **Description 變成產品文案。** `description` 是 Claude 的操作手冊；寫好它是 PM/writer 的工作，不只是工程的。它就是 tool 的 prompt engineering。
3. **錯誤處理是 UX 的一部分。** Tool 失敗時（`ValueError`），Claude 會把錯誤呈現給使用者。也就是說 tool 錯誤訊息是**使用者可見的文案**。PM 該 review。

---

## 兩個 Demo Tools 的走查

這節課針對記憶體文件集合實作了兩個 tools：

| Tool | 業務角色 |
|------|---------|
| `read_doc_contents` | 「讓 Claude 用 ID 查特定文件」 |
| `edit_document` | 「讓 Claude 提議並執行 find/replace 編輯」 |

Description 明確警告 Claude 注意細節陷阱——例如 `old_str` 指定「必須精確相符，包含空白」。PM 讀到這裡應該把 tool description 當成**Claude 和真實世界副作用之間的 guardrail**。

### Find/Replace 的警告（產品警示）

`edit_document` 用 Python 的 `str.replace`，會替換文件裡**所有**出現位置。Demo 這樣沒問題；真實產品裡這是槍自己的腳：

> 「把 'budget' 這個字換成 'expenditure'」可能默默把整份文件的每個 budget 都換掉，而不是使用者原本想改的那一處。

PM 該標記這一點。真實產品通常需要：

- 對 match 做唯一性檢查
- 套用前預覽
- 所有編輯的 audit log
- 破壞性動作的使用者確認

---

## 產品應用場景

### 輕量 tool 撰寫有回報的地方

| 情境 | 為什麼合適 |
|------|----------|
| 快速功能迭代 | 新 tool 只是約 10 行改動，PM 可以試驗 |
| Domain 專屬助理 | 一個 domain 動作一個 tool（讀政策、提議編輯、發摘要） |
| 內部平台團隊 | 透過共享 MCP server 標準化公司 tool 函式庫 |
| Tool 目錄 | 多個 tool 各司其職，Claude 在 runtime 選擇 |

### 低摩擦是風險的地方

| 情境 | 警告 |
|------|------|
| 變更 production 系統 | 低摩擦讓風險 tool 很容易就 ship——要強制 review |
| Tool 名字曖昧 | Claude 的選擇取決於 description 品質，草率的文案 = 選錯 tool |
| Tool 重疊 | 兩個 tool 做類似的事會讓 Claude 混淆；PM 該去重 |
| 沉默的 side effect | `edit_document` 替換所有符合項；真實產品需要明確確認 |

---

## PM 決策框架：review 一個 Tool PR

團隊加新 MCP tool 時，PM 該檢查：

1. **Tool `name` 清楚且動詞化了嗎？**（`read_doc_contents`，不是 `docs_tool_3`）
2. **`description` 有告訴 Claude 它做什麼 AND 不做什麼嗎？**（例如「必須精確相符，包含空白」）
3. **每個參數都有 `Field(description=...)` 嗎？** 缺 description 會降低 tool 品質。
4. **失敗時會怎樣？** Tool 應該 raise 使用者可讀的錯誤，而不是默默失敗。
5. **Tool 是破壞性的嗎？** 如果是，產品流程有核准/確認嗎？
6. **和既有 tools 有重疊嗎？** 有的話合併或改名釐清。

---

## Description 就是文案撰寫

MCP tool description 大概是 Claude 產品裡最被低估的文案：

| 屬性 | 含義 |
|------|------|
| Claude 讀，不是使用者讀 | 沒有行銷包裝；簡明宣示性語言勝出 |
| 用於 tool 選擇 | 曖昧的 description → 叫錯 tool |
| 約束 agent 行為 | 你可以設定期待（「只有你有精確 doc ID 才用」） |
| 工程 reviewer 看不出來 | Code review 抓不到弱文案——PM 必須 review |

PM 的直覺法則：如果 tool description 過不了技術寫作的 review，它大概也過不了 Claude 的。

---

## 常見 PM 錯誤

1. **Review tool code 但不 review tool description** — description 是和 Claude 的 API contract。
2. **Scope mega-tools** — 一個「什麼文件操作都做」的 tool 比三個專注的 tool 更難讓 Claude 使用。
3. **忽略破壞性副作用** — `edit_document` 默默替換所有符合項；需要產品 UX 來圍住它。
4. **以為錯誤訊息只是內部的** — `ValueError` 文字會透過 Claude 到達終端使用者；要寫清楚。
5. **把 SDK 人體工學當成「只是工程問題」** — 生產力贏面改變了 PM 能試驗的速度。

> **Key Insight**
>
> 用 Python SDK 做的 MCP tool 定義是 PM 的 surface，不只是工程 surface。`name`、`description`、和參數 doc 是產品文案，會形塑 Claude 行為和使用者可見的輸出。當 tool 撰寫變這麼便宜，瓶頸從工程努力轉移到產品判斷——那就是 PM 賺飯錢的地方。

---

## CCA 考試重點

- **D2（Tool Design & MCP Integration）**：知道 SDK 模式是 `FastMCP` + `@mcp.tool(...)` + `Field(description=...)`。
- **D1（Agentic Architecture）**：理解 tool error（raised exception）會透過 agent loop 傳遞，Claude 能把它納入下一輪。
- 預期有情境題問 tool 命名、description 品質、錯誤呈現。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| 從 SDK-based tool 模式 PM 該帶走什麼？ | Tool 撰寫現在夠便宜，PM 可以要求更多、更窄的 tool，不是 mega-tool。 |
| 誰該 review tool 的 `description` 欄位？ | PM——它是形塑 Claude 行為的產品文案。 |
| 這節課 `edit_document` 的隱藏風險是什麼？ | 它叫 `str.replace`，會替換每個出現位置；真實產品需要唯一性或確認。 |
| Tool 錯誤為什麼在產品層級重要？ | Tool `raise ValueError` 時，Claude 會把訊息呈現給使用者——它是使用者可見文案。 |
| 參數沒有 `Field` description 會怎樣？ | Claude 只看到參數名，所以 tool 選擇和使用品質下降。 |
| Demo server 對外提供幾個 tools，各做什麼？ | 兩個：`read_doc_contents` 和 `edit_document`（find-and-replace）。 |
| PM 對 tool 重疊的規則是什麼？ | 兩個 tool 做類似的事會讓 Claude 混淆——去重或改名。 |
| 一句話框架 tool description 給 PM？ | 它們是 Claude 的操作手冊，因此是產品文案。 |
