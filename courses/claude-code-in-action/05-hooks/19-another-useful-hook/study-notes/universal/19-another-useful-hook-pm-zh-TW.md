# Another Useful Hook — PM 視角

| 項目 | 內容 |
|------|------|
| 考試對應 | D3 — Claude Code Configuration & Workflows（佔 20%）、D1 — Agentic Architecture（佔 27%） |
| Task Statements | 1.5（Agent SDK hooks）、3.2（custom commands & hooks）、1.7（session state & resumption） |
| 課程來源 | claude-code-in-action / 05-hooks / Lesson 19（純文字課程） |

---

## TL;DR


![Hook 分類總覽](../../visuals/hook-taxonomy-zh-TW.svg)
*圖：Hook 完整分類 — 全部 9 種 Hook 依生命週期、是否可攔截、用途分類。*

Claude Code 有 9 種 hook 類型——不只是 PreToolUse 和 PostToolUse。額外的 hook（`Stop`、`SubagentStop`、`Notification`、`PreCompact`、`UserPromptSubmit`、`SessionStart`、`SessionEnd`）覆蓋了完整的 AI session 生命週期。對 PM 來說，這代表你可以在 AI 工作流的**每個階段**指定自動化——從 session 開始到結束，而不只是工具執行期間。

---

## 為什麼 PM 需要知道所有 Hook 類型

理解完整的 hook 分類讓你能寫出更精確的需求：

| PM 的問題 | 對應 Hook | 需求範例 |
|----------|----------|---------|
| 「AI 完成任務後會發生什麼？」 | `Stop` | 「每次 review session 後生成摘要報告」 |
| 「環境如何設定？」 | `SessionStart` | 「Claude 啟動時載入專案設定」 |
| 「子任務完成後怎麼處理？」 | `SubagentStop` | 「coordinator 使用前驗證 subagent 輸出」 |
| 「如何保存 context？」 | `PreCompact` | 「自動壓縮前 extract 關鍵決策」 |
| 「能驗證用戶輸入嗎？」 | `UserPromptSubmit` | 「處理前根據 template 檢查 prompt」 |

不知道這些 hook 類型的話，PM 只能寫出模糊的需求如「系統應該記錄所有東西」——工程師無法精確實作。

---

## 心智模型：飯店住客生命週期

把 AI session 想成飯店住客的住宿過程：

| 飯店事件 | Hook 類型 | 發生什麼 |
|---------|----------|---------|
| 住客 check in | `SessionStart` | 房間準備好、載入偏好設定 |
| 住客提出要求（客房服務） | `PreToolUse` | 驗證要求是否允許、確認額度 |
| 要求完成 | `PostToolUse` | 品質檢查、更新帳單 |
| 住客找前台但沒人 | `Notification` | 通知經理（需要權限或閒置中） |
| 禮賓部完成委託的跑腿 | `SubagentStop` | 帶著結果回報給住客 |
| 房間變得凌亂 | `PreCompact` | 房務在打掃前保存重要物品 |
| 住客投意見箱 | `UserPromptSubmit` | 前台先審閱再轉交管理層 |
| 住客今天的要求都完成了 | `Stop` | 準備每日摘要 |
| 住客 check out | `SessionEnd` | 結帳、清理、累積會員點數 |

> 💡 **PM 重點**
>
> 你不需要理解每個 hook 的技術實作。你需要知道**哪些生命週期時刻可以自動化**，這樣你才能寫出工程師能對應到特定 hook 類型的需求。

---

## 可變資料問題（PM 簡化版）

工程師面臨的一個挑戰：每種 hook 類型收到不同的資料。這對 PM 很重要，因為它影響每個階段有什麼資訊可用：

| Hook 類型 | 可用資料 | PM 影響 |
|----------|---------|--------|
| `PreToolUse` / `PostToolUse` | 哪個工具、什麼輸入、什麼輸出 | 可以根據特定工具動作做決策 |
| `Stop` | Session ID、transcript 路徑 | 可以生成摘要但不知道最後一個具體動作 |
| `Notification` | Session ID、通知詳情 | 可以警報但 context 有限 |
| `SubagentStop` | Session ID、subagent 輸出 | 可以驗證子任務結果 |

> 🎯 **PM 為什麼要在意**
>
> 如果你寫的需求是「記錄 Claude 做的每個 database query」，工程師需要知道這代表 PostToolUse hook 掛在 database 工具上（有 `tool_input` 包含 query）。如果你寫「每次 session 結束後摘要 Claude 做了什麼」，那是 Stop hook（有 `transcript_path` 但沒有個別工具資料）。

---

## 產品情境演練

### 情境：AI 驅動的 Code Review Pipeline

你是 CI/CD 系統的 PM，使用 Claude Code 做自動化 code review。不同 hook 類型的應用方式：

| Pipeline 階段 | Hook 類型 | 自動化 |
|-------------|----------|--------|
| Pipeline 啟動 | `SessionStart` | 載入 repo 設定、設定 review 範圍 |
| Claude review 一個檔案 | `PostToolUse` | 讀完檔案後跑 linter |
| Claude 寫 review 評論 | `PostToolUse` | 驗證評論格式 |
| Research subagent 調查一個 pattern | `SubagentStop` | 驗證研究結果是結構化的 |
| Context 變大 | `PreCompact` | 裁剪前保存關鍵發現 |
| Claude 完成 review | `Stop` | 生成 review 摘要、寫到 PR |
| Pipeline 結束 | `SessionEnd` | 清理暫存檔、更新指標 |

**PRD 用語**：
- 不要寫：「系統應該自動生成 review 摘要」
- 要寫：「一個 `Stop` hook 在 Claude 完成回應後生成結構化 review 摘要並寫到 PR」

這給工程師一個明確的實作目標。

---

## Debug Hook：PM 應該知道它存在

工程師用一個簡單的 debug 技巧來發現每個 hook 收到什麼資料：

```json
{
  "matcher": "*",
  "hooks": [{ "type": "command", "command": "jq . > log.json" }]
}
```

**PM 為什麼要在意**：如果工程師說「我們不知道這個生命週期階段有什麼資料可用」，答案是：用 debug hook 去發現。這防止需求因為「我們需要先調查」而被擋住。

---

## PM 的 Hook 類型決策框架

寫需求時，用這個決策樹：

1. **需要在 AI 動作之前發生？** → PreToolUse（可以阻止）
2. **需要在 AI 動作之後發生？** → PostToolUse（只能回饋）
3. **需要在 Claude 回應完成時發生？** → Stop
4. **需要在子任務完成時發生？** → SubagentStop
5. **需要在 SESSION 開始/結束時發生？** → SessionStart / SessionEnd
6. **需要在 CONTEXT 即將被裁剪時發生？** → PreCompact
7. **需要在用戶提交 PROMPT 時發生？** → UserPromptSubmit
8. **需要在 Claude 需要注意時發生？** → Notification

> 💡 **簡單規則**
>
> 把 hook 跟**生命週期時刻**配對，而不是動作。「Claude 完成後」是 Stop hook，不是在每個工具上掛 PostToolUse hook。

---

## Anti-Patterns（考試常考）

| ❌ 錯誤做法 | ✅ 正確做法 | 為什麼 |
|-----------|-----------|--------|
| 寫「系統應該記錄所有東西」 | 指定哪種 hook 類型記錄什麼資料 | 模糊需求導致 over-engineering 或 under-engineering |
| 假設所有 hook 提供相同資料 | 理解資料因 hook 類型而異 | 需求可能要求該生命週期階段沒有的資料 |
| 用 PostToolUse 做 session 結束動作 | 用 Stop hook 做 session 結束動作 | PostToolUse 每個工具都觸發，Stop 只在結束時觸發一次 |
| Multi-agent 設計忽略 SubagentStop | 用 SubagentStop 驗證子任務輸出 | 沒有驗證，coordinator 可能處理格式錯誤的 subagent 資料 |

---

## 模擬考題

### 第一題：CI/CD Pipeline 情境

你的團隊 CI pipeline 用 Claude Code 做自動化 PR review。Claude 完成 review 後，你需要把摘要寫到 log 檔做稽核。哪個做法正確？

- A. PostToolUse hook，`matcher: "*"`，每次 tool call 後追加到 log
- B. Stop hook，讀取 transcript 並生成結構化摘要
- C. SessionEnd hook，寫出所有資料的 raw dump
- D. Notification hook，Claude 閒置時發送摘要

<details><summary>答案與解析</summary>

**B** — Stop hook 正好在 Claude 完成回應時觸發。它可以透過 `transcript_path` 存取完整對話紀錄來生成有意義的摘要。這是「Claude 完成後」的正確 lifecycle moment。

- A 在每次 tool call 後都觸發，生成很多不完整的條目——不是乾淨的摘要
- C 在整個 session 結束時才觸發，可能太遲或太廣泛
- D 在閒置或需要權限時觸發，不是完成時

**PM 重點**：「Claude 完成後」對應的是 `Stop` hook，不是 PostToolUse。把 lifecycle moment 對對是寫出可實作需求的關鍵。
</details>

### 第二題：Multi-Agent Research 情境

一個 coordinator agent 把研究任務分派給 subagent。你需要確保每個 subagent 回傳結構化 JSON 資料後，coordinator 才能處理它。需求裡該怎麼寫？

- A. 在 coordinator 的 system prompt 加上驗證指示
- B. 實作 SubagentStop hook，驗證 subagent 的輸出結構
- C. 在 coordinator 的 tool calls 上掛 PostToolUse hook
- D. 加 PreCompact hook，在 context 裁剪前檢查資料

<details><summary>答案與解析</summary>

**B** — `SubagentStop` 在 subagent 完成時觸發，這正是應該做輸出驗證的時間點。它在 coordinator 處理可能格式錯誤的資料之前提供 deterministic 的驗證。

- A 是 prompt-based（probabilistic），把負擔加在 coordinator 上
- C 在 coordinator 自己的 tool calls 上觸發，不是 subagent 完成時
- D 是關於 context 管理，不是輸出驗證

**PM 重點**：在 multi-agent 架構中，驗證指定在 **agent 之間的邊界**——那就是 SubagentStop hook 的位置。
</details>

### 第三題：Developer Productivity 情境

你的開發團隊希望啟動 Claude Code session 時，自動載入專案特定的 context（coding standards、架構決策）。應該用哪種 hook？

- A. PreToolUse hook，在第一次 tool call 前載入 context
- B. UserPromptSubmit hook，在第一個 prompt 前注入 context
- C. SessionStart hook，session 開始時載入專案 context
- D. Notification hook，Claude 請求權限時載入 context

<details><summary>答案與解析</summary>

**C** — `SessionStart` 在 session 開始或恢復時觸發，是載入環境和專案 context 的自然位置。

- A 只在特定工具被呼叫時觸發，可能不是第一個動作
- B 在每次用戶 prompt 時都觸發，不只是 session 開始——會重複載入 context
- D 在通知時觸發，跟 session 初始化無關

**PM 重點**：環境設定屬於 `SessionStart`，不屬於 per-action hook。這確保 context 載入一次，整個 session 都可用。
</details>
