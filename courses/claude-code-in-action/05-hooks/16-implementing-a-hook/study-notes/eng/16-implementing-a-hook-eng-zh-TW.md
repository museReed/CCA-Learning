# 實作一個 Hook — 工程師深入解析

| 項目 | 細節 |
|------|--------|
| 考試領域 | D3 — Claude Code Configuration & Workflows (20%) |
| Task Statements | 3.2 (custom commands & hooks), 1.5 (Agent SDK hooks for tool call interception) |
| 來源 | claude-code-in-action / 05-hooks / Lesson 16 |

---

## 一句話摘要

實作一個 hook 就是在 `settings.local.json` 配置（matcher + command），然後撰寫腳本從 stdin 讀取 JSON、檢查 `tool_input`、以 exit code 0（允許）或 2（封鎖 + stderr 回饋）結束。

---

## 背景：從理論到實作

Lesson 15 教了你*定義* hook 的四步驟框架。這堂課完整走過一個可運作的實作 — 一個防止 Claude 讀取 `.env` 檔案的 PreToolUse hook。

> 💡 **iOS/Swift 類比**
>

![.env Guard Flow](../../visuals/env-guard-flow-zh-TW.svg)
*圖：.env 檔案守衛資料流 — PreToolUse 攔截 Read 呼叫，阻擋敏感檔案存取。*

> 這就像從概念上理解 `URLProtocol` 到實際繼承它、註冊它、然後在 Xcode debugger 中看到你的攔截器觸發。真正的學習發生在你看到各部分連結起來的時候。

---

## 逐步實作

### 1. 配置 `settings.local.json`

打開 `.claude/settings.local.json` 並加入 PreToolUse hook：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read|Grep",
        "hooks": [
          {
            "type": "command",
            "command": "node ./hooks/read_hook.js"
          }
        ]
      }
    ]
  }
}
```

關鍵配置細節：
- **`matcher: "Read|Grep"`** — 攔截兩個能存取檔案內容的工具
- **`command`** — 指向實作邏輯的 Node.js 腳本
- **`type: "command"`** — 告訴 Claude Code 這是要執行的 shell command

> 📝 **為什麼用 `settings.local.json`？**
>
> 這個檔案被 gitignore — 用於你的個人設定。用 `.claude/settings.json`（沒有 `.local`）放團隊共用的 hook，應 commit 到版本控制。

### 2. 撰寫 Hook 腳本

腳本從 stdin 讀取、解析 JSON、檢查檔案路徑、以適當的 code 結束：

```javascript
async function main() {
  // 第一步：從 stdin 讀取 tool call 資料
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }

  // 第二步：解析 JSON
  const toolArgs = JSON.parse(Buffer.concat(chunks).toString());

  // 第三步：提取檔案路徑
  const readPath =
    toolArgs.tool_input?.file_path || toolArgs.tool_input?.path || "";

  // 第四步：檢查並決定
  if (readPath.includes('.env')) {
    console.error("You cannot read the .env file");
    process.exit(2);  // 封鎖操作
  }

  // 若到這裡，隱含 exit code 0（允許）
}

main();
```

> ⚠️ **關鍵實作細節**
>
> 1. **從 stdin 讀取，不是 argv** — Tool call 資料透過 standard input 傳入，不是命令列參數
> 2. **用 `console.error()`，不是 `console.log()`** — 回饋必須送到 stderr（exit code 2 只將 stderr 發給 Claude）
> 3. **同時檢查 `file_path` 和 `path`** — 不同工具在 `tool_input` 中可能用不同欄位名
> 4. **Exit code 2，不是 1** — Code 1 是一般錯誤；code 2 專門表示「封鎖此 tool call」

### 3. 重啟並測試

儲存兩個檔案後：

1. **重啟 Claude Code** — Hook 變更只在重啟後生效
2. **用 Read 測試**：請 Claude 讀取 `.env` — 應被封鎖
3. **用 Grep 測試**：請 Claude grep `.env` — 也應被封鎖
4. **用允許的檔案測試**：請 Claude 讀取其他檔案 — 應正常運作

> 🎬 **講師影片洞察**
>
> Claude 在回應中辨認出 hook 回饋：「I was prevented by a read hook from accessing that file.」這展示了回饋迴圈 — Claude 不只是失敗；它理解*原因*並將此傳達給使用者。

---

## 常見實作錯誤

| ❌ 錯誤 | ✅ 修正 | 為什麼 |
|-----------|--------|-----|
| 用 `console.log()` 做回饋 | 用 `console.error()` | exit code 2 時只有 stderr 會送給 Claude |
| 以 exit code 1 封鎖 | 以 exit code 2 封鎖 | Code 1 = 一般錯誤；Code 2 = 刻意封鎖 |
| 只讀 tool_input.file_path | 同時檢查 tool_input.path | Grep 用 `path`，Read 用 `file_path` |
| 忘記重啟 Claude Code | 改 hook 後一定要重啟 | Hook 在啟動時載入 |
| 用 `process.argv` 取輸入 | 用 `process.stdin` | Tool call 資料透過 stdin 傳入 |
| 精確比對 `.env` | 用 `.includes('.env')` | 檔案路徑可能是絕對路徑 |

---

## 反模式（考試常考）

| ❌ 錯誤做法 | ✅ 正確做法 | 為什麼 |
|-------------------|---------------------|-----|
| 在腳本中檢查 tool_name 來過濾工具 | 用 config 中的 matcher 做工具過濾；腳本做輸入驗證 | 關注點分離 — matcher 選工具，腳本處理邏輯 |
| 在 settings.json 中寫 inline hook 邏輯 | 用外部腳本檔案 | 可維護性、可測試性、可讀性 |
| 靜默封鎖不回饋 | 封鎖時一定要寫 stderr | Claude 需要知道*原因*才能調整行為 |
| 只防護 Read | 同時防護 Read 和 Grep | 兩個工具都能暴露檔案內容 |

---

## 練習題

### Q1：開發者生產力情境（S4）

你實作了一個 PreToolUse hook 來防止 Claude 讀取 `.env` 檔案。Hook 腳本用了 `console.log("Access denied")` 和 `process.exit(2)`。Claude 成功封鎖了讀取但沒顯示 "Access denied" 訊息。問題是什麼？

- A. Exit code 應該是 1，不是 2
- B. 回饋必須寫到 stderr（`console.error()`），不是 stdout（`console.log()`）
- C. Matcher 除了 `Read` 還應包含 `Write`
- D. Hook 需要回傳 JSON 回應而非純文字訊息

<details><summary>答案</summary>

**B** — Hook 以 exit code 2 結束時，只有 stderr 輸出會轉發給 Claude 作為回饋。`console.log()` 寫到 stdout，不會被捕獲。用 `console.error()` 寫到 stderr。

- A：Code 1 是一般錯誤，不是封鎖訊號
- C：Write 不相關 — 問題是關於讀取存取的回饋
- D：純文字寫到 stderr 是正確機制；不需要 JSON 包裝
</details>

### Q2：CI/CD 整合情境（S5）

你的團隊想實作一個 hook，檢查 Claude 是否在執行潛在危險的 Bash 命令（如 `rm -rf`）。Hook 應封鎖危險命令、允許安全命令。哪個實作方法正確？

- A. PostToolUse hook，在執行後還原危險命令的結果
- B. PreToolUse hook，matcher 為 `Bash`，讀取 stdin JSON，檢查 `tool_input.command`，若命令符合黑名單則以 exit code 2 結束
- C. PreToolUse hook，matcher 為 `.*`，封鎖所有包含 "rm" 的 tool call
- D. 在 system prompt 加入「永不執行 rm -rf」

<details><summary>答案</summary>

**B** — 需要 PreToolUse 在執行前封鎖。Matcher 專門指向 `Bash`。腳本檢查 `tool_input.command`（實際 shell 命令）並套用黑名單檢查。

- A：PostToolUse 太晚了 — 危險命令已經執行
- C：`.*` 太廣泛（攔截所有工具），且在任何工具中檢查 "rm" 不精確
- D：Prompt-based，有非零失敗率 — 安全需求不可接受

> 考試哲學：**Deterministic > Probabilistic**
</details>

### Q3：客戶支援代理情境（S1）

你正在為客服代理實作一個 PreToolUse hook。Hook 必須在退款金額超過 $500 時封鎖 `process_refund` 工具。你的腳本讀取 stdin JSON 並檢查 `tool_input.amount`。但測試中，hook 允許了 $600 的退款。最可能的原因是什麼？

- A. Exit code 應該是 1 而不是 2
- B. 腳本在檢查 `tool_input.refund_amount` 而不是工具實際使用的欄位名
- C. 應該用 PostToolUse hook 而不是 PreToolUse
- D. Matcher 應該是 `.*` 來攔截所有 tool call

<details><summary>答案</summary>

**B** — 最常見的實作 bug 是 `tool_input` 中的欄位名不匹配。每個工具定義自己的 input schema。腳本必須使用工具期望的確切欄位名（可能是 `amount`、`refund_amount`、`value` 等）。

- A：Exit code 2 對封鎖來說是正確的
- C：PostToolUse 無法封鎖 — 退款已被處理
- D：Matcher 應指向特定工具，不是所有工具
</details>
