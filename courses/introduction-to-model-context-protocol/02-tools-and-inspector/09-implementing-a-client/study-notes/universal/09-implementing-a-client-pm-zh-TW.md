# Implementing a Client — PM 策略概覽

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | T2.2 實作 MCP client-server 通訊; T2.4 處理 tool discovery 和執行流程 |
| Source | introduction-to-model-context-protocol / 02-tools-and-inspector / Lesson 09 |

---

## 一句話摘要

MCP client 是你產品中的協調層，在使用者、Claude 和外部服務之間協調——就像一位知道什麼時候該問誰什麼事的專案經理。

---

## Client 就是專案經理

把 MCP client 想像成協調複雜請求的專案經理：

1. **接收** — 利害關係人（使用者）提交請求
2. **資源調查** — PM 檢查哪些團隊（MCP server）可用及提供什麼服務
3. **專家諮詢** — PM 把請求和可用資源呈現給決策者（Claude）
4. **委派** — 決策者說「請數據團隊拉這份報告」— PM 路由請求
5. **交付** — PM 收集結果帶回給決策者做最終建議
6. **回應** — 決策者為利害關係人組成精鍊的答案

這六步模式是每個 MCP 驅動的產品互動的核心。

> **PM Takeaway**
> Client 是協調層，不是智慧層。Claude 提供智慧（決定做什麼）。MCP server 提供能力（做事）。Client 連接它們。這個關注點分離是理解架構的關鍵。

---

## 兩個核心操作

每個 MCP client 與 MCP server 只做兩件事：

### 「你能做什麼？」（Discovery）

在任何工作開始前，client 會問每個 MCP server 它提供什麼 tools。這就像 PM 與新供應商的第一次會議——「讓我看看你的服務目錄。」

回應是結構化的能力清單：tool 名稱、描述，以及每個 tool 需要什麼輸入。這份目錄傳給 Claude 讓它做出明智決策。

### 「請做這件事」（Execution）

當 Claude 決定使用 tool 時，client 接受 Claude 的具體請求並發送到正確的 MCP server。這就像 PM 發送詳細的工作訂單給供應商：「用參數 Z 對資料集 Y 執行分析 X。」

Server 做完工作回傳結果，client 把結果傳回 Claude 做解讀。

> **PM Takeaway**
> 這兩個操作——discovery 和 execution——是 client 與 MCP 做的唯一的事。如果團隊中有人描述更複雜的互動，他們可能是在描述多輪同樣的兩個操作。

---

## 五步產品流程

從產品角度，每次使用者與 MCP 驅動的 tools 互動都遵循五個步驟：

**步驟 1：探索能力** — 你的產品檢查有哪些 tools 可用。這自動且對使用者不可見地發生。

**步驟 2：向 Claude 呈現上下文** — 你的產品把使用者的問題連同 tool 目錄發送給 Claude。Claude 同時看到使用者要什麼和它有什麼 tools 可以用。

**步驟 3：Claude 做決定** — Claude 要麼直接回答（如果不需要 tools）或決定用特定輸入呼叫特定 tool。這是「AI 判斷」步驟。

**步驟 4：執行動作** — 你的產品把 Claude 的 tool 請求發送到適當的 MCP server。Server 做工作——查詢資料庫、取得檔案、跑計算。

**步驟 5：交付答案** — 你的產品把 tool 結果送回 Claude，它為使用者組成自然語言回應。

使用者看不到這些複雜性。他們問問題然後得到答案。五個步驟在毫秒到秒內完成。

> **PM Takeaway**
> 步驟 3 是產品品質勝負的關鍵。Claude 選擇正確 tool 的能力取決於 tool 描述的品質（來自 server）和使用者問題的清晰度。兩者都是產品設計關切。

---

## 雙呼叫模式

一個微妙但重要的面向：每次使用 tool 的互動中，產品會對 Claude 做兩次獨立呼叫。

**第一次呼叫**：「使用者問 X。這些是可用 tools。你想怎麼做？」
**Claude 回應**：「我想用輸入 Z 呼叫 tool Y。」

**第二次呼叫**：「Tool Y 回傳了這些結果。現在請回答使用者的原始問題。」
**Claude 回應**：「根據數據，答案是...」

這個雙呼叫模式有產品影響：

- **延遲**：涉及 tools 時兩次 API 呼叫意味著更長的回應時間
- **成本**：每次互動兩次 Claude API 呼叫（對定價模型很重要）
- **品質**：第二次呼叫受益於具體數據，常常產生比僅第一次呼叫更好的回應

> **PM Takeaway**
> 估算產品的回應時間和 API 成本時，記住使用 tool 的互動需要兩次 Claude API 呼叫。不使用 tool 的互動只需一次。你的產品中這兩種類型的混合比例決定整體效能和成本。

---

## 產品團隊應理解的錯誤場景

四種類型的失敗可能發生，每種對使用者端有不同影響：

1. **Tool 找不到** — Claude 請求的 tool 不存在。通常是配置問題。
2. **無效輸入** — Claude 發送了錯誤型別的資料給 tool。通常是 tool 描述清晰度問題。
3. **Server 錯誤** — MCP server 或外部服務失敗。基礎設施問題。
4. **傳輸錯誤** — Client 和 server 之間的連線中斷。網路問題。

每種需要不同的錯誤處理和不同的使用者訊息。

---

## CCA 考試關聯性

本課完成 **Domain 2 (18%)**：

- Client 使用兩個 SDK 類別：Client（連線）和 ClientSession（通訊）
- 兩個核心方法：`list_tools()` 和 `call_tool()`
- 從 discovery 到最終回應的五步 agentic 流程
- 雙呼叫模式（每次使用 tool 的互動兩次 Claude API 呼叫）
- 錯誤處理：檢查 `result.isError` 捕獲 tool 層級失敗

---

## Flashcards

| Front | Back |
|-------|------|
| 用商業語言描述 MCP client 的角色是什麼？ | 它是協調層——就像一位調查可用資源、向決策者（Claude）呈現選項、路由執行請求的專案經理。 |
| MCP client 與 MCP server 只做哪兩個操作？ | Discovery（問有哪些 tools 可用）和 Execution（用特定輸入呼叫特定 tool）。 |
| MCP 產品流程的五個步驟是什麼？ | 1) 探索能力, 2) 向 Claude 呈現上下文, 3) Claude 做決定, 4) 執行動作, 5) 交付答案。 |
| 為什麼使用 tool 的互動需要兩次 Claude API 呼叫？ | 第一次：Claude 收到查詢和 tools，決定做什麼。第二次：Claude 收到 tool 結果，組成最終回應。 |
| 雙呼叫模式的成本影響是什麼？ | 每次使用 tool 的互動花費兩次 Claude API 呼叫而非一次，影響定價模型和使用量預估。 |
| 五步流程中哪一步決定產品品質？ | 步驟 3（Claude 的決定）——取決於 tool 描述品質和使用者問題清晰度，兩者都是產品設計關切。 |
| MCP client 有哪四種錯誤類型？ | Tool 找不到（配置）、無效輸入（描述清晰度）、Server 錯誤（基礎設施）、傳輸錯誤（網路）。 |
| 使用者在五步 MCP 流程中體驗到什麼？ | 什麼也沒有。他們問問題然後得到答案。所有五步透明地在毫秒到秒內發生。 |
