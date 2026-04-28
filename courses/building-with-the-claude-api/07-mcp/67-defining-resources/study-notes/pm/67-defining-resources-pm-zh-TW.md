# Defining Resources — PM Perspective（繁體中文）

| 項目 | 說明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（MCP primitives：tools vs resources vs prompts）、1.2（context 注入） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 67 |

---

## One-Liner

Resources 是 MCP 的「資料架」——一種結構化的方式讓 server 暴露唯讀資料（文件、紀錄、清單），應用可以直接拉取注入 Claude prompt，不需要 tool call，也不讓 Claude 自己猜要抓什麼。

---

## 心智模型：餐廳菜單 vs 廚房

- **Resources = 菜單**：一張可讀的清單，列出 server 能提供的東西。你（應用）從菜單挑，server 把東西端給你，你擺到 Claude 的盤子上。
- **Tools = 廚房**：Claude 下單「幫我做三明治」，廚房實際去做（動作、副作用）。

兩者都由同一家餐廳（MCP server）提供。選菜單還是選廚房，就是選 resource 還是 tool。

---

## 為什麼 PM 要在意

幾乎所有有 context 感的 AI 功能——「@mention 文件」、「拉這筆紀錄」、「給我這個客戶的最新 notes」——背後都是 resources。搞清楚兩者差別會影響：

- **誰驅動 fetch** — 使用者 / 應用（resource）vs Claude（tool）
- **成本** — 拉一次 resource vs 給 Claude 一個可能呼叫很多次的 tool
- **延遲** — Resources 進第一個 prompt；tools 多一次 API round trip
- **可預測性** — Resources 永遠注入相同資料；tools 由 Claude 決定，比較靈活但不確定

PM 若搞混，要嘛為本該是直接拉取的操作支付 tool call 費用，要嘛做出 Claude 明明有資料卻幻想的產品。

---

## 功能範例：`@document` mention

課程用具體功能切入：CLI 中使用者輸入 `@`，跳出文件 autocomplete；選好送出，文件全文注入 prompt。

兩個 resources：

| 操作 | Resource 類型 | 原因 |
|------|--------------|------|
| 列出所有文件給 autocomplete | Direct（靜態 URI） | 固定、無參數、每次呼叫一樣 |
| 用 ID 取單一文件 | Templated（帶 `{doc_id}`） | 帶參數、每次輸出不同 |

零 tool call，拉資料完全不經 Claude round trip。應用直接從 server 拿資料塞進 prompt。

---

## Resource vs Tool — PM 速查表

| 產品情境 | Resource 或 Tool？ | 原因 |
|---------|--------------------|------|
| 使用者輸入 @filename 時插入文件內容 | Resource | 純讀、應用驅動、無須 Claude 判斷 |
| Claude 回答時可自行搜尋知識庫 | Tool | Claude 決定何時搜 |
| 填充客戶清單 dropdown | Resource | 靜態清單拉取 |
| 更新客戶電話 | Tool | 寫入 / 副作用 |
| 顯示當前 KPI dashboard | Resource | Pull-and-render |
| 「如果我日曆有空就幫我訂會議」 | Tool（agentic） | Claude 推理、決定、行動 |

---

## 產品場景

### 什麼時候用 Resources

| 需求 | 為什麼適合 Resources |
|------|---------------------|
| 使用者引用特定項目（@mention、/command、file picker） | 應用依使用者選擇驅動 fetch |
| 永遠要注入的 context（公司 style guide、詞彙表、schema） | 拉一次，每次對話都帶上 |
| UI 元件清單（autocomplete、dropdown） | Direct resource 對應靜態集合 |
| 資料驅動 onboarding（「你的上一筆訂單」） | 每個使用者拉一次、注入 prompt |

### 什麼時候改用 Tools

| 需求 | 為什麼適合 Tools |
|------|-----------------|
| 是否要 fetch 應由 Claude 判斷 | 只有 tools 讓 Claude 有選擇 |
| 有副作用的操作 | Resources 是唯讀的 |
| 參數要靠推理決定 | Tool input 可在對話中動態合成 |

---

## PM 決策框架

規格「拉取類」功能前問自己：

| 問題 | 若是 Yes | 意義 |
|------|---------|------|
| 是由使用者（而非 Claude）決定拉哪個項目？ | Yes | Resource |
| 純讀、無副作用？ | Yes | Resource |
| 希望每次對話都一定把資料放進 prompt？ | Yes | Resource |
| 希望 Claude 覺得沒必要就可以跳過 fetch？ | Yes | Tool |
| 操作會修改資料？ | Yes | Tool |

---

## PM 常見錯誤

1. **把所有 MCP 能力都當 tool** — 最便宜、最可預測的原語經常是 resource。先問「誰決定？」再規格
2. **不思考 URI namespace** — URI 就是 API，爛 URI（`docs://d1`、`docs://d2`）後面會吃大虧，要像設計 REST API 一樣認真
3. **以為 resources 是免費的** — 注入的內容還是吃 token，大文件會炸 context window
4. **把讀寫混在同一個原語** — 讀用 resource、寫用 tool，security review 與 audit log 會簡單太多
5. **跳過 Inspector 驗證** — MCP Inspector 可以在 client 還沒寫之前證明 resource 能用，PM 應該把這當成交付要求

> **Key Insight**
>
> Resources 是讓產品對 Claude 說「這就是你需要的資料」而不是「這是你也許能用的工具」的原語。每次強迫 Claude 選擇，都要付 token 成本並增加變異。Resources 是 PM 保留「確定性」與「成本控制」的武器，同時還能給 Claude 新鮮、相關的 context。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：Resources 是 MCP 三個 primitives 之一（tools、resources、prompts），知道 direct vs templated 的差異
- **D1（Agentic Architecture）**：Resources 是不經 tool call 把 context 塞進 agent loop 的方式，由 client 拉取後注入 prompt
- 考題模式：「應用要依使用者選擇把文件內容放進 prompt，是 tool 還是 resource？」→ resource

---

## Flashcards

| Front | Back |
|-------|------|
| Resources 與 tools 的「菜單 vs 廚房」比喻？ | Resources 是菜單（應用挑出資料端給 Claude），tools 是廚房（Claude 選擇去做的動作） |
| Resources 有哪兩種？ | Direct（靜態 URI、固定呼叫）與 templated（帶參數的 URI、參數化呼叫） |
| 什麼時候該用 resource 而非 tool？ | 當應用（而非 Claude）決定 fetch、fetch 沒副作用、資料應一律出現在 prompt 裡 |
| 舉一個 direct vs templated resource 的產品範例。 | Direct：列出所有文件給 autocomplete。Templated：用 `{doc_id}` 取特定文件 |
| Resources 還是會有哪種成本？ | Token 成本——注入的內容會計入 context window |
| 為什麼 URI 設計要認真對待？ | URI 是 server 的 API 契約，爛 URI 跟爛 REST route 一樣難改 |
| 對 Claude 而言 resources 與 tools 有何不同？ | Claude 不會「決定」呼叫 resource；resource 由 client 拉取注入 prompt，Claude 只看到結果 |
| 上線前該要求使用哪個驗證工具？ | MCP Inspector，它列出 direct 與 templated resources，可以先端到端測 |
