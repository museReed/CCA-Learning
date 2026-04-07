# Custom Commands — 工程師視角


![Custom Commands Scope Architecture](../../visuals/custom-commands-scope-architecture-zh-TW.svg)
*圖：自訂指令範圍 — 專案 vs 使用者層級。*


![Custom Command Mechanism](../../visuals/custom-command-mechanism-zh-TW.svg)
*圖：自訂指令 — Markdown 檔案變成 Slash Command。*

| 項目 | 內容 |
|------|------|
| 考試對應 | D3 — Claude Code Configuration & Workflows（佔 20%） |
| Task Statements | 3.2 ★★★（custom commands & skills）、3.1 ★★（CLAUDE.md config） |
| 課程來源 | claude-code-in-action / 03-context-and-commands / Lesson 11 |

---

## 一句話理解

Custom commands 就是把可重複使用的 prompt 模板存成 `.claude/commands/` 裡的 markdown 檔案。用 `$ARGUMENTS` 當動態輸入的注入點，讓你把常做的工作流程變成一行 slash command。

---

## Custom Commands 怎麼運作

Custom commands 用你自己的專案專用捷徑來擴充 Claude Code 內建的 `/` 指令。機制很簡單：

1. 在 `.claude/commands/` 裡建立一個 `.md` 檔案
2. 檔名就是指令名稱（例如 `audit.md` → `/audit`）
3. 檔案內容就是送給 Claude 的 prompt
4. 在檔案任何地方用 `$ARGUMENTS` 作為執行時輸入的 placeholder
5. 重啟 Claude Code 才能載入新指令

> [!TIP]
> **核心心智模型**
>
> Custom commands 是**有觸發器的存檔 prompt**，不是腳本。它們不會直接執行程式碼 — 它們指示 Claude 該做什麼。把它們想成 prompt 模板，不是 shell scripts。

---

## 建立你的第一個 Command

### 範例一：Dependency Audit

```
# 檔案：.claude/commands/audit.md


![Claude Code Configuration Hierarchy](../../visuals/claude-code-configuration-hierarchy-zh-TW.svg)
*圖：Claude Code 設定階層。*

Review all dependencies installed in this project.
Check for known vulnerabilities and outdated packages.
If any vulnerabilities are found, update the affected packages.
After updating, run the test suite to verify nothing broke.
```

使用方式：`/audit`

### 範例二：Write Tests（帶引數）

```
# 檔案：.claude/commands/write_tests.md

Write comprehensive tests for $ARGUMENTS.
Follow the existing test patterns in this project.
Run the tests after writing them to make sure they pass.
```

使用方式：`/write_tests src/auth.ts` 或 `/write_tests the validation utilities in src/utils/`

> [!NOTE]
> **影片補充**
>
> 講師特別強調，`$ARGUMENTS` 不限於檔案路徑。你可以傳入任何字串 — 描述、feature 名稱、甚至自然語言指示。Placeholder 就是純粹的文字替換。

---

## Command 的作用域：Project vs User

| 作用域 | 路徑 | 誰看得到 | 是否 commit 到 Git |
|-------|------|---------|-------------------|
| 專案 | `.claude/commands/` | 整個團隊 | **是**（committed） |
| 個人 | `~/.claude/commands/` | 只有你自己 | 否 |

> [!IMPORTANT]
> **考試重點**
>
> 專案範圍的 `.claude/commands/` 是考試關注的重點。它代表**把團隊慣例編碼為指令** — 這是 D3 的核心考試概念。這遵循 **Architecture > Prompt** 的考試哲學 — 與其告訴每個開發者如何 audit dependencies，不如建立一個編碼了流程的 command。

---

## 實用 Command 點子

| 指令 | 用途 | 有引數？ |
|------|------|---------|
| `/audit` | 檢查 dependencies 漏洞、更新、跑測試 | 否 |
| `/write_tests` | 為特定檔案或模組產生測試 | 是 — 檔案路徑或描述 |
| `/review` | 檢查程式碼變更的常見問題 | 是 — 檔案路徑或 PR 號碼 |
| `/doc` | 為一個模組產生文件 | 是 — 模組名稱 |
| `/migrate` | 為 schema 變更建立資料庫 migration | 是 — 變更描述 |
| `/refactor` | 按照專案慣例重構檔案 | 是 — 檔案路徑 |

---

## 工程師類比

| 概念 | 類比 |
|------|------|
| Custom commands | Shell aliases 或 Makefile targets — 常用工作流程的捷徑 |
| `.claude/commands/` 目錄 | `.github/workflows/` — 專案層級的自動化設定 |
| `$ARGUMENTS` | Bash 腳本裡的 `$1` — positional parameter 替換 |
| 專案範圍的 commands | 提交到 repo 的 ESLint config — 團隊共用的慣例 |
| 新增後重啟 Claude Code | `source ~/.zshrc` — 重新載入設定以套用變更 |

---

## 反面模式

| 反面模式 | 問題 | 更好的做法 |
|---------|------|-----------|
| 在 commands 裡放複雜邏輯 | Commands 是 prompts 不是腳本 — Claude 可能理解有歧義 | 保持 commands 聚焦；用 hooks 處理 deterministic 邏輯 |
| 不把 commands commit 到 repo | 團隊成員無法受益於共享的工作流程 | 存在 `.claude/commands/` 並 commit |
| 在 commands 裡寫死檔案路徑 | 專案結構變了就壞了 | 用 `$ARGUMENTS` 處理動態路徑 |
| 為一次性任務建立 commands | 增加雜亂但沒有複用價值 | Commands 是給**可重複**的工作流程用的 |
| 忘記重啟 Claude Code | 新 commands 在重啟前不會被載入 | 新增/修改 commands 後一定要重啟 |

---

## 考試聚焦：Commands vs Hooks vs CLAUDE.md

這是 D3 常考的區分題：

| 機制 | 做什麼 | 什麼時候用 |
|------|-------|-----------|
| **Custom Commands** | 用 `/name` 觸發的可重複 prompt 模板 | 可重複的工作流程（audit、test、review） |
| **CLAUDE.md** | 永遠載入的專案指示 | 持久性慣例（coding style、專案結構） |
| **Hooks** | 工具執行的程式化 middleware | Deterministic 強制執行（阻擋寫入、自動格式化） |
| **Memories** | 個人的持久筆記 | 個人偏好和修正 |

> [!TIP]
> **判斷口訣**
>
> - 「每次做 X，我都打同樣的長 prompt」→ **Custom command**
> - 「Claude 應該永遠知道這個專案的 Y」→ **CLAUDE.md**
> - 「Z 絕對不能發生 / 必須永遠發生」→ **Hook**
> - 「Claude 一直對我個人搞錯 W」→ **Memory**

核心考試哲學：**Architecture > Prompt** — custom commands 把團隊工作流程編碼到專案結構中，讓它們可發現、可版本控制、一致。

---

## 模擬考題

### 第一題：Code Generation 情境

你的團隊經常要求 Claude Code 產生 API endpoint 的 boilerplate。每個開發者打的 prompt 略有不同，導致程式碼 patterns 不一致。標準化這個工作流程的最佳方式是什麼？

- A. 把 boilerplate 指示加到 CLAUDE.md
- B. 在 `.claude/commands/endpoint.md` 建立 custom command，用 `$ARGUMENTS` 帶入 endpoint 名稱
- C. 建立 PreToolUse hook 來強制 boilerplate 結構
- D. 分享一個文字檔，裡面放建議的 prompt 讓所有開發者複製貼上

<details><summary>答案與解析</summary>

**B** — Custom command 在團隊之間標準化了 prompt，同時允許透過 `$ARGUMENTS` 做動態輸入。因為它在 `.claude/commands/` 裡，它會被 commit 到 repo，團隊所有成員都能用。

- A 對永遠開啟的慣例可行，但對按需觸發的工作流程來說太重了
- C 是用來做 deterministic 強制執行的，不是 prompt 模板化
- D 是手動的而且容易出錯 — 開發者會隨時間修改它

> [!IMPORTANT]
> 考試哲學：**Architecture > Prompt** — 把工作流程編碼在專案結構裡，不要靠口耳相傳的知識。

</details>

### 第二題：Developer Productivity 情境

你建立了一個新的 custom command 檔案在 `.claude/commands/lint_fix.md`，但在 Claude Code 裡打 `/lint_fix` 時，指令沒有出現。最可能的原因是什麼？

- A. 檔案必須命名為 `lint-fix.md`，用連字號而不是底線
- B. 你需要重啟 Claude Code 才能載入新指令
- C. Custom commands 只有在用 `$ARGUMENTS` 時才能運作
- D. 檔案必須放在 `~/.claude/commands/` 而不是專案目錄

<details><summary>答案與解析</summary>

**B** — Custom commands 在啟動時載入。建立或修改 command 檔案後，你必須重啟 Claude Code 才會出現在指令清單裡。

- A 不正確 — 底線在 command 名稱中可以正常使用
- C 不正確 — `$ARGUMENTS` 是選用的
- D 不正確 — `.claude/commands/`（專案範圍）是有效的，而且是團隊共享 commands 的建議位置

> [!NOTE]
> 這是一個實務知識題 — 影片明確提到了重啟的需求。

</details>
