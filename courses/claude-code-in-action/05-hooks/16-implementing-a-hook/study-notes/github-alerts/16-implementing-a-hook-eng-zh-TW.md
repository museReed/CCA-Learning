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

## 逐步實作

### 1. 配置 `settings.local.json`

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

> [!NOTE]
> **為什麼用 `settings.local.json`？**
>
> 這個檔案被 gitignore — 用於你的個人設定。用 `.claude/settings.json`（沒有 `.local`）放團隊共用的 hook。

### 2. 撰寫 Hook 腳本

```javascript
async function main() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }

  const toolArgs = JSON.parse(Buffer.concat(chunks).toString());

  const readPath =
    toolArgs.tool_input?.file_path || toolArgs.tool_input?.path || "";

  if (readPath.includes('.env')) {
    console.error("You cannot read the .env file");
    process.exit(2);
  }
}

main();
```

> [!WARNING]
> **關鍵實作細節**
>
> 1. **從 stdin 讀取，不是 argv** — Tool call 資料透過 standard input 傳入
> 2. **用 `console.error()`，不是 `console.log()`** — 回饋必須送到 stderr
> 3. **同時檢查 `file_path` 和 `path`** — 不同工具可能用不同欄位名
> 4. **Exit code 2，不是 1** — Code 2 專門表示「封鎖此 tool call」

### 3. 重啟並測試

> [!NOTE]
> **講師影片洞察**
>
> Claude 在回應中辨認出 hook 回饋：「I was prevented by a read hook from accessing that file.」這展示了自我修正的回饋迴圈。

---

## 常見實作錯誤

| ❌ 錯誤 | ✅ 修正 | 為什麼 |
|-----------|--------|-----|
| 用 `console.log()` 做回饋 | 用 `console.error()` | exit code 2 時只有 stderr 會送給 Claude |
| 以 exit code 1 封鎖 | 以 exit code 2 封鎖 | Code 1 = 一般錯誤；Code 2 = 刻意封鎖 |
| 只讀 tool_input.file_path | 同時檢查 tool_input.path | Grep 用 `path`，Read 用 `file_path` |
| 忘記重啟 Claude Code | 改 hook 後一定要重啟 | Hook 在啟動時載入 |

---

## 反模式（考試常考）

| ❌ 錯誤做法 | ✅ 正確做法 | 為什麼 |
|-------------------|---------------------|-----|
| 在腳本中檢查 tool_name 來過濾工具 | 用 config 中的 matcher 做工具過濾 | 關注點分離 |
| 靜默封鎖不回饋 | 封鎖時一定要寫 stderr | Claude 需要知道*原因* |
| 只防護 Read | 同時防護 Read 和 Grep | 兩個工具都能暴露檔案內容 |

---

## 練習題

### Q1：開發者生產力情境（S4）

你實作了一個 PreToolUse hook。腳本用了 `console.log("Access denied")` 和 `process.exit(2)`。Claude 封鎖了讀取但沒顯示訊息。問題是什麼？

- A. Exit code 應該是 1
- B. 回饋必須寫到 stderr（`console.error()`），不是 stdout
- C. Matcher 還應包含 `Write`
- D. Hook 需要回傳 JSON 回應

<details><summary>答案</summary>

**B** — exit code 2 時只有 stderr 輸出會轉發給 Claude。

> [!IMPORTANT]
> 關鍵原則：stderr = Claude 回饋；stdout = exit code 2 時被忽略
</details>

### Q2：CI/CD 整合情境（S5）

團隊想實作 hook 檢查 Claude 是否執行危險 Bash 命令。哪個方法正確？

- A. PostToolUse hook，執行後還原
- B. PreToolUse hook，matcher 為 `Bash`，讀 stdin JSON，檢查 `tool_input.command`，符合黑名單則 exit code 2
- C. PreToolUse hook，matcher 為 `.*`，封鎖所有含 "rm" 的 tool call
- D. 在 system prompt 加入「永不執行 rm -rf」

<details><summary>答案</summary>

**B** — 需要 PreToolUse 在執行前封鎖。Matcher 專門指向 `Bash`。

> [!IMPORTANT]
> 考試哲學：**Deterministic > Probabilistic**
</details>

### Q3：客戶支援代理情境（S1）

你為客服代理實作 PreToolUse hook，封鎖超過 $500 的退款。測試中 hook 允許了 $600 退款。最可能的原因？

- A. Exit code 應該是 1
- B. 腳本在檢查錯誤的 `tool_input` 欄位名
- C. 應該用 PostToolUse
- D. Matcher 應該是 `.*`

<details><summary>答案</summary>

**B** — 最常見的 bug 是 `tool_input` 欄位名不匹配。每個工具定義自己的 input schema。

> [!IMPORTANT]
> 考試哲學：**Architecture > Prompt** — 實作正確性很重要
</details>
