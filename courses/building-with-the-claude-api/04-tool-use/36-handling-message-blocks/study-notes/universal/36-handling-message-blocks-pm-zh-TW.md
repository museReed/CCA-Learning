# Handling Message Blocks — PM Perspective（繁中）

| 項目 | 內容 |
|------|------|
| 考試領域 | D2 — Tool Design & MCP Integration (18%) / D1 — Agentic Architecture (22%) |
| Task Statements | 2.2（content block 處理）、2.1（tool schema 整合）、1.2（agentic loop 基礎） |
| 來源 | building-with-the-claude-api / 04-tool-use / Lesson 36 |

---

## 一句話總結

一旦你的產品讓 Claude 可以呼叫 tool，每一則 assistant 回覆就會變成一個**結構化的封包**——一部分是對用戶講的說明，一部分是給機器讀的動作請求——系統的工作就是把每一塊路由到正確的地方（UI vs 後端執行器）。

---

## 心智模型：無線電調度通訊

把啟用 tool 後的 Claude 回應想成**警用無線電調度**：

| 部分 | 無線電通話 | Claude 回應 |
|------|------------|-------------|
| 開場說明 | 「12 號車注意…」 | Text block——人類可讀的脈絡 |
| 可執行指令 | 「請前往 5 街和 Main 街口」 | ToolUseBlock——機器可讀的 function 呼叫 |
| 呼號 | 12 號車 | `tool_use_id`——配對請求與回應 |

調度員（你的後端）必須聽完整段通訊、把說明轉述給用戶、並把動作派給正確的單位。掉任何一塊對話就斷。

---

## 為什麼產品要在乎這件事

啟用 tool 之前，Claude 回應「就是一句話」，可以直接丟進 UI。啟用 tool 後，回應是一個**混合 payload**，需要解析：

- 有些部分是給用戶看的文字（「我來幫你查時間…」）
- 有些部分是後端動作（「呼叫 `get_current_datetime` 並帶這些參數」）
- 有些部分是看不見的 ID，必須往返送回 Claude

不懂這件事的 PM 會嚴重低估工程成本：看起來很簡單的功能（例如「讓 Claude 抓股價」）實際上需要新建一整套 block iteration、ID 追蹤、state 保留的管線。

---

## 產品應用場景

### Multi-Block 處理很重要的時候

| 場景 | 為什麼 block 重要 |
|------|-------------------|
| 會查即時資料的助理（天氣、股價、行事曆） | Text block = 用戶看到的；ToolUseBlock = 後端呼叫 |
| 需要串接多個操作的 agentic workflow | 每一回合可能產生多個 ToolUseBlock，你得平行執行 |
| 會一邊講話一邊動作的語音/影像助理 | Text block 驅動 TTS，tool-use block 觸發實體動作 |
| Debug 或稽核功能 | 要給用戶看「Claude 正在做什麼」就必須把 tool-use intent 露出來 |

### 可以保持簡單的時候

| 場景 | 更簡單的做法 |
|------|--------------|
| 純靜態知識問答 | 不用 tool——單一 text block 就好 |
| 分類／情感分析 | 不用 tool——用結構化 JSON 輸出 |
| 創意寫作 | 不用 tool——只要 text block |

---

## PM 決策框架

在承諾做一個使用 tool 的功能之前，確認團隊能回答：

| 問題 | 為什麼重要 |
|------|------------|
| 誰負責把 text-block 的說明露給用戶？ | 跳過的話體感會是 Claude「沉默思考」 |
| 如何在回合之間保留完整的 block list？ | 掉 block 會在後續回合引發看不懂的 API 錯誤 |
| 誰負責 tool_use 和 tool_result 的 ID 配對？ | 必須有一個專職的 layer 來配對請求和回應 |
| 一次回應回來多個 tool call 怎麼辦？ | 可能要平行執行，不是依序 |
| tool 執行中間的載入/進度狀態如何呈現？ | 長時間工具會讓 UX 出現空窗期，沒有 progress event 很難收尾 |

---

## 常見 PM 錯誤

1. **把 tool-use 當成「另一支 API」規劃**——它其實是一套新協定：multi-block message、ID 配對、stop_reason dispatch
2. **設計稿忽略說明 block**——設計師常常只畫最終答案，漏掉「我正在查…」的前言
3. **假設一回合只會有一個 tool call**——一題可能產生 2、3 個 tool-use block，UI 和後端都要能處理平行執行
4. **把 tool-use ID 當成工程內部細節**——它們是與 Claude 的契約。掉了就會壞、會出 400，最後用戶會看到
5. **沒編預算改 helper function**——舊的「加訊息到歷史」code 通常假設字串，必須升級

---

> **Key Insight**
>
> 當你把 tool 加進一個由 Claude 驅動的功能，assistant 回覆就不再是「一則訊息」，而是「一個通訊封包」。產品現在需要一個調度員：能朗讀說明、能把動作送給執行器、還能記住呼號。低估這個轉變是 tool-use 專案最常見的 overrun 來源。Kickoff 就要跟工程講清楚：「一旦啟用 tool，每一則訊息都會變成 typed block list。」

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：知道啟用 tool 會把 response shape 從字串變 block list；記得 ToolUseBlock 的四個欄位。
- **D1（Agentic Architecture）**：`stop_reason == "tool_use"` 是 agentic 模式裡標準的 loop 繼續信號。
- 考題會給一段把 `response.content` 當字串的程式，問你下一回合為什麼會壞。

---

## Flashcards

| 題目 | 答案 |
|------|------|
| 啟用 tool 後 Claude 回應的形狀變成什麼？ | 一個 typed block 的 list（TextBlock、ToolUseBlock），而不是單一字串 |
| 用什麼無線電比喻來理解 multi-block 訊息？ | 警用調度通訊——開場說明 + 動作指令 + 呼號（ID） |
| PM 規劃 tool-use 功能時最大的風險是什麼？ | 低估協定轉變——multi-block 解析、ID 配對、歷史保留 |
| 為什麼一定要把說明 text block 顯示給用戶？ | 否則 Claude 推理時 UX 會沉默，前言脈絡也會被丟掉 |
| 哪個 stop_reason 告訴後端要執行 tool 並繼續 loop？ | `"tool_use"` |
| 一個 Claude 回應可以有多個 tool-use block 嗎？ | 可以——一個問題可能需要多個 tool，系統要全部處理 |
| tool_use_id 為什麼不只是工程細節？ | 它們跨 API 呼叫配對請求與回應，丟了會讓後續回合壞掉 |
| 不升級舊 helper function 的產品代價是什麼？ | 後續回合會出看不懂的 400，因為先前的 block 被攤平成字串 |
