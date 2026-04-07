# Hooks 的注意事項 — 工程師深入解析

| 項目 | 細節 |
|------|--------|
| 考試領域 | D3 — Claude Code Configuration & Workflows (20%) |
| Task Statements | 3.2 (custom commands & hooks), 1.5 (Agent SDK hooks for tool call interception) |
| 來源 | claude-code-in-action / 05-hooks / Lesson 17（純文字課） |

---

## 一句話摘要

Hook 腳本應使用**絕對路徑**以確保安全性（防止 path interception 和 binary planting 攻擊），但絕對路徑破壞可攜性 — 解法是 `settings.example.json` + init script 模式。

---

## 核心問題

### 為什麼要絕對路徑？

```json
// ❌ 相對路徑（安全風險）
"command": "node ./hooks/read_hook.js"

// ✅ 絕對路徑（安全）
"command": "node /Users/alice/projects/queries/hooks/read_hook.js"
```

| 攻擊 | 描述 | 絕對路徑如何幫助 |
|--------|-------------|------------------------|
| **Path interception** | 攻擊者在 `$PATH` 中放入惡意腳本 | 絕對路徑繞過 `$PATH` 解析 |
| **Binary planting** | 攻擊者在工作目錄放入同名惡意檔案 | 絕對路徑指向確切的檔案 |

> [!CAUTION]
> **安全性不可妥協**
>
> CCA 考試將安全最佳實踐視為正確答案。

---

## 解法：模板 + Init Script


![Template Init Pattern](../../visuals/template-init-pattern-zh-TW.svg)
*圖：Template → Init → Local 模式 — 提交含 $PWD 佔位符的 template，一次性 init 產生機器專屬設定。*

### 1. `settings.example.json`（commit 到 git）

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read|Grep",
        "hooks": [
          {
            "type": "command",
            "command": "node $PWD/hooks/read_hook.js"
          }
        ]
      }
    ]
  }
}
```

### 2. `scripts/init-claude.js`（commit 到 git）

讀取模板 → 替換 `$PWD` → 寫入 `settings.local.json`

### 3. `settings.local.json`（gitignored，自動生成）

> [!NOTE]
> **為何對團隊很重要**
>
> 此模式確保：安全（絕對路徑）+ 可攜（模板適用任何機器）+ 自動化 + 版本控制

---

## 兩個 Settings 檔案

| 檔案 | 用途 | 在 Git？ |
|------|---------|---------|
| `settings.json` | 團隊共用設定 | 是 |
| `settings.local.json` | 生成的機器特定檔 | 否 |

---

## 反模式（考試常考）

| ❌ 錯誤做法 | ✅ 正確做法 | 為什麼 |
|-------------------|---------------------|-----|
| Hook command 用相對路徑 | 用絕對路徑 | 安全風險 |
| Commit 帶絕對路徑的 `settings.local.json` | Commit 帶 `$PWD` 佔位符的模板 | 絕對路徑是機器特定的 |
| 手動編輯路徑 | 用 init script 自動生成 | 手動容易出錯 |

---

## 練習題

### Q1：開發者生產力情境（S4）

團隊想共享 PreToolUse hook 配置。推薦方法？

- A. Commit 帶相對路徑的 `settings.local.json`
- B. Commit 帶絕對路徑的 `settings.json`
- C. Commit 帶 `$PWD` 佔位符的 `settings.example.json` 和 init script
- D. 每個開發者手動建立

<details><summary>答案</summary>

**C** — 兼顧安全和可攜性。

> [!IMPORTANT]
> 關鍵原則：模板 + init script = 安全 + 可攜
</details>

### Q2：CI/CD 整合情境（S5）

CI pipeline 的 hook 用相對路徑被安全審計標記。修正？

- A. 將 hooks 目錄加到 `$PATH`
- B. CI 加 setup 步驟生成帶絕對路徑的 `settings.local.json`
- C. CI 停用 hook
- D. 寫死路徑

<details><summary>答案</summary>

**B** — Init script 模式在 CI 也適用。

> [!IMPORTANT]
> CI/CD 環境需要與開發者機器相同的安全態勢。
</details>

### Q3：程式碼生成情境（S2）

新開發者 clone 後 hook 不工作。有 `settings.example.json` 但沒有 `settings.local.json`。原因？

- A. Hook 預設停用
- B. 需執行 `npm run setup` 生成 `settings.local.json`
- C. 需手動複製模板
- D. OS 不支援

<details><summary>答案</summary>

**B** — `settings.local.json` 被 gitignore，必須由 script 生成。
</details>
