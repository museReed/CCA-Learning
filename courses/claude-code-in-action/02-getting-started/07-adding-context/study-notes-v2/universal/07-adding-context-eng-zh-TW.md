# Adding Context — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows, D5: Context Management |
| Task Statements | 3.1 (CLAUDE.md hierarchy), 5.1 (context preservation), 5.4 (large codebase context) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> 本節所有內容均直接來自官方課程教材。

## One-Liner / TL;DR

Context 管理是 Claude Code 中最具影響力的技能 — `/init` 產生 CLAUDE.md，三層 CLAUDE.md 階層提供持久指令，`#` memory mode 更新它們，`@` 檔案提及則按需注入特定檔案內容。

## Core Concepts

### Context 管理原則

太多不相關的 context 會降低 Claude Code 的效能。一般專案可能有數十甚至數百個檔案，每個都包含大量資訊。當你向 Claude 提問或交付任務時，存在一個理想的資訊量 — 剛好足以理解如何回答或完成任務。一旦開始加入不相關的資訊，效能就會下降。

引導 Claude 找到相關檔案和文件非常重要。Claude Code 不需要手把手也能運作，但給予適當指引會得到最佳結果。

### /init 指令

首次在新專案中開啟 Claude Code 時，執行 `/init`。Claude 將：

1. **分析整個 codebase** — 專案目的、整體架構、程式碼模式與結構
2. **識別關鍵元素** — 相關指令、重要檔案、專案結構
3. **產生 CLAUDE.md 檔案** — 將分析結果摘要寫入此檔案

當 Claude 嘗試建立檔案時，會詢問權限：
- **Enter** — 批准檔案寫入
- **Shift+Tab** — 允許 Claude Code 自由寫入專案中的檔案（自動接受模式）

### CLAUDE.md 檔案

CLAUDE.md 檔案有兩個用途：

1. **引導 Claude 理解 codebase** — 幫助 Claude 更快找到相關程式碼（指令、架構、風格）
2. **自訂指示** — 提供一般性指引給 Claude 的位置

此檔案的內容會包含在你對 Claude 的每個請求中 — 它的功能等同於持久的 system prompt。

### CLAUDE.md 檔案位置

Claude Code 在三個層級識別 CLAUDE.md 檔案：

| 層級 | 檔案 | 是否共享？ | 說明 |
|------|------|-----------|------|
| 專案 | `./CLAUDE.md` | 是 — 提交至版本控制 | 由 `/init` 產生。透過 Git 與其他工程師共享。包含專案特定的 Claude 指示。 |
| 本地 | `./CLAUDE.local.md` | 否 — 不提交 | 你希望 Claude 只為你遵循的個人指示。不與其他工程師共享。 |
| 全域 | `~/.claude/CLAUDE.md` | 否 — 機器專屬 | 適用於你在這台機器上執行的所有專案的指示。 |

> 講師鼓勵打開產生的 CLAUDE.md 檔案並檢視其內容。由於它包含在每個請求中，了解其內容有助於優化 context。

### 使用 # Memory Mode 新增自訂指令

要更新 CLAUDE.md 而不需手動編輯檔案，在 Claude Code 中使用 `#` 指令。這會進入「memory mode」，允許你智慧地編輯 CLAUDE.md 檔案。

**範例：**
```
> # Don't write comments so often
```

輸入指令後，指定要加入哪個 CLAUDE.md 檔案（專案、本地或全域）。Claude 會智慧地將指令合併至該檔案 — 不是盲目附加。

### 使用 @ 提及檔案

使用 `@` 加上檔案路徑，將檔案內容包含在請求中。這是將 Claude 指向特定方向的技巧。

**在聊天中（一次性 context）：**
```
> How does the auth system work? @auth
```
提及檔案時，它會自動包含在對 Claude 的請求中。Claude 會顯示認證相關檔案供你選擇。

**在 CLAUDE.md 中（持久 context）：**
```markdown
The database schema is defined in @prisma/schema.prisma.
Reference it when working with data models.
```
當 `@` 用在 CLAUDE.md 中，被引用檔案的內容會自動包含在每個請求中。這意味著 Claude 可以立即回答相關問題，無需先讀取檔案。

> **Context Window 警告** — CLAUDE.md 中每個 `@` 引用都會永久佔用 context window 空間。僅引用在大多數請求中真正需要的檔案。偶爾需要的檔案請改用聊天中的互動式 `@` 提及。

## Demo Walkthrough：執行 /init 產生 CLAUDE.md

| 步驟 | 發生什麼 | 截圖 |
|------|---------|------|
| 1 | 講師在專案中開啟終端機，用 `claude` 指令啟動 Claude Code | |
| 2 | 執行 `/init` — Claude 開始分析整個 codebase | ![/init 指令](../../visual-guide/frames/frame_019.jpg) |
| 3 | Claude 識別專案目的、架構、相關指令、重要檔案 | ![Codebase 分析](../../visual-guide/frames/frame_022.jpg) |
| 4 | Claude 摘要結果並寫入 CLAUDE.md 檔案 | |
| 5 | 權限提示出現 — Enter 接受，或 Shift+Tab 自由寫入 | ![權限提示](../../visual-guide/frames/frame_025.jpg) |

## Demo Walkthrough：使用 # Memory Mode

| 步驟 | 發生什麼 | 截圖 |
|------|---------|------|
| 1 | 講師注意到 Claude 在產生的程式碼中使用過多註解 | |
| 2 | 輸入 `#` 進入 memory mode | ![進入 memory mode](../../visual-guide/frames/frame_044.jpg) |
| 3 | 輸入指示：「don't write comments so often」 | ![新增指示](../../visual-guide/frames/frame_048.jpg) |
| 4 | 指定加入專案 CLAUDE.md 檔案 | |
| 5 | Claude 智慧地將指示合併至現有 CLAUDE.md | ![指示已合併](../../visual-guide/frames/frame_050.jpg) |
| 6 | 開啟檔案並透過搜尋驗證指示已新增 | |

## Demo Walkthrough：使用 @ 檔案提及

| 步驟 | 發生什麼 | 截圖 |
|------|---------|------|
| 1 | 講師想了解認證系統如何運作 | |
| 2 | 使用 `@auth` 提及認證檔案 — 檔案內容包含在請求中 | ![@ 提及 auth](../../visual-guide/frames/frame_055.jpg) |
| 3 | 說明這是將 Claude 指向特定方向的優秀技巧 | |
| 4 | 展示 CLAUDE.md 中也能使用相同的 `@` 語法進行持久引用 | ![CLAUDE.md 中的 @](../../visual-guide/frames/frame_060.jpg) |
| 5 | 提及 `@prisma/schema.prisma` — 定義所有資料表和記錄類型的資料庫 schema | |
| 6 | 使用 `#` memory mode 將 schema 引用加入 CLAUDE.md | ![新增 schema 引用](../../visual-guide/frames/frame_064.jpg) |
| 7 | 詢問「user 有哪些屬性？」— Claude 立即回答，無需讀取 schema 檔案 | ![即時回答](../../visual-guide/frames/frame_068.jpg) |

## 講師提示

- 首次在新專案中使用 Claude Code 時執行 `/init`
- 開啟並檢視產生的 CLAUDE.md，了解 Claude 對你專案的認知
- `#` 捷徑比手動編輯 CLAUDE.md 更快 — Claude 會智慧合併指令
- 當你已知相關檔案時，使用 `@` 提及可節省時間
- 將關鍵的跨領域檔案（如資料庫 schema）用 `@` 放入 CLAUDE.md，讓 Claude 隨時具備該 context
- 要有選擇性 — CLAUDE.md 中過多 `@` 引用會浪費 context window 並降低效能

## Key Takeaways

1. 太多不相關的 context 會降低 Claude Code 效能 — 給予恰到好處的指引
2. `/init` 透過分析 codebase 啟動專案 context，產生 CLAUDE.md
3. CLAUDE.md 包含在每個請求中 — 它是持久的 system prompt
4. 三個 CLAUDE.md 層級：專案（共享）、本地（個人）、全域（所有專案）
5. `#` memory mode 讓你智慧更新 CLAUDE.md，無需手動編輯
6. 聊天中的 `@` 提供一次性 context；CLAUDE.md 中的 `@` 提供每次請求的持久 context
7. CLAUDE.md 中被引用的檔案會自動載入 — Claude 可以立即回答而不需搜尋

---

# PART 2: Study Aids

> 補充學習資料，非官方課程內容。

## Familiar Analogies

| 概念 | 類比 | 為何適合 |
|------|------|---------|
| CLAUDE.md | `.bashrc` / `.zshrc` — 每次 shell session 載入 | 影響所有行為的持久設定，自動載入 |
| CLAUDE.md 階層 | CSS specificity：inline > class > element | 更具體的（本地）覆寫更通用的（全域） |
| `/init` | `git init` + 自動產生的 README | 以 metadata 和結構摘要啟動專案 |
| CLAUDE.md 中的 `@` | 檔案頂部的 `import` 語句 | 始終載入，始終可用 |
| 聊天中的互動式 `@` | 動態 `import()` | 按需載入，僅在該請求需要時使用 |
| `#` memory 指令 | `git config --global` 設定 | 為所有未來 session 持久保存指示 |
| Context window 預算 | 執行中程式的 RAM | 有限資源 — 載入過多會減少處理空間 |

## CCA Exam Connection

本課涵蓋三個高價值考試主題：

**CLAUDE.md 階層（Task 3.1）** — 三個層級：專案（透過版本控制共享）、本地（個人，gitignored）、全域（機器上所有專案）。越本地 = 優先級越高。

**Context 保存（Task 5.1）** — CLAUDE.md 跨 session 持久存在。CLAUDE.md 中的 `@` 引用始終載入。`#` 指令更新持久記憶。

**大型 codebase context（Task 5.4）** — 過多 context 損害效能。CLAUDE.md 中的 `@` 應謹慎使用於跨領域檔案。讓 Claude 透過工具自行探索其餘部分。

考試測試的關鍵區別：
- CLAUDE.md（共享）vs CLAUDE.local.md（個人）— 都是專案層級但共享範圍不同
- CLAUDE.md 中的 `@`（每次請求）vs 聊天中的 `@`（一次性）— 持久 vs 按需 context
- `/init`（產生初始 CLAUDE.md）vs `#`（新增指令至現有 CLAUDE.md）

## Anti-Patterns

| Anti-Pattern | 為何失敗 | 正確做法 |
|-------------|---------|---------|
| 在 CLAUDE.md 中加入 15+ 個 `@` 引用 | 消耗 context window，降低效能和準確度 | 僅保留跨領域檔案；其餘用互動式 `@` |
| 從不執行 `/init` | Claude 每次 session 從零開始 | 首次使用時執行 `/init`，之後逐步維護 |
| 使用 CLAUDE.local.md 存放團隊標準 | CLAUDE.local.md 被 gitignore — 隊友看不到 | 使用專案 CLAUDE.md 存放共享標準 |
| 每次手動編輯 CLAUDE.md | 繁瑣且容易出錯 | 使用 `#` memory mode 進行智慧合併 |
| 將個人偏好放入專案 CLAUDE.md | 透過版本控制將你的風格強加給整個團隊 | 使用 CLAUDE.local.md 或 ~/.claude/CLAUDE.md 存放個人偏好 |
| 忽略全域 ~/.claude/CLAUDE.md | 錯失跨專案個人偏好的機會 | 在全域檔案中設定個人程式碼風格 |

## Practice Questions

**Q1.** 你的專案 CLAUDE.md 說「使用 2 空格縮排」。你的 CLAUDE.local.md 說「使用 4 空格縮排」。你的全域 ~/.claude/CLAUDE.md 說「使用 tab」。Claude 遵循哪個？

- A) Tab（全域優先級最高）
- B) 2 空格縮排（專案 CLAUDE.md 是標準）
- C) 4 空格縮排（本地覆寫專案和全域）
- D) Claude 詢問你要用哪個

> **答案：C。** 在 CLAUDE.md 階層中，越本地 = 優先級越高。CLAUDE.local.md 覆寫專案 CLAUDE.md，後者覆寫全域 ~/.claude/CLAUDE.md。

**Q2.** 開發者在 CLAUDE.md 中加入 12 個 `@` 檔案引用。回應變慢且不準確。最可能的原因和修復方式？

- A) Claude Code 對多個 `@` 引用有 bug — 更新到最新版
- B) `@` 引用消耗過多 context window — 移除非必要引用，改用互動式 `@`
- C) 檔案太大 — 拆分成更小的檔案
- D) CLAUDE.md 有 10 個 `@` 引用的限制 — 移除多餘的

> **答案：B。** 課程明確指出過多不相關的 context 會降低效能。CLAUDE.md 中的每個 `@` 引用都在每次請求時載入。修復方式是僅保留關鍵的跨領域檔案，任務特定的檔案改用互動式 `@`。

**Q3.** 你的團隊希望所有使用 Claude Code 的開發者遵循相同的程式碼標準。哪種方式正確？

- A) 每位開發者在自己的 ~/.claude/CLAUDE.md 中加入標準
- B) 將標準加入專案 CLAUDE.md 並提交至版本控制
- C) 將標準加入專案中的 CLAUDE.local.md
- D) 使用 `#` 在每位開發者的 session 中設定標準

> **答案：B。** 專案 CLAUDE.md 提交至版本控制，與所有團隊成員共享。這是架構性方法 — 不需逐人手動設定，不會產生設定漂移。

**Q4.** 在聊天訊息中使用 `@schema.prisma` 與在 CLAUDE.md 中加入 `@schema.prisma` 有何不同？

- A) 沒有差別 — 兩者運作方式相同
- B) 在聊天中，檔案僅包含在該請求中；在 CLAUDE.md 中，包含在每個請求中
- C) 在 CLAUDE.md 中檔案被快取；在聊天中每次重新讀取
- D) `@` 語法僅在聊天中有效，不適用於 CLAUDE.md

> **答案：B。** 聊天中的互動式 `@` 為當前請求提供一次性 context。CLAUDE.md 中的 `@` 使檔案內容持久化 — 自動包含在每個請求中，以 context window 空間換取即時可用性。
