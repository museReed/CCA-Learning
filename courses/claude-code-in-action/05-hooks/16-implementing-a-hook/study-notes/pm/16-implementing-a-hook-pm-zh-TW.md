# 實作一個 Hook — PM 觀點

| 項目 | 細節 |
|------|---------|
| 考試範圍 | D3 — Claude Code Configuration & Workflows（佔考試 20%） |
| Task Statements | 3.2 (custom commands & hooks), 1.5 (Agent SDK hooks) |
| 課程來源 | claude-code-in-action / 05-hooks / Lesson 16 |

---

## 重點摘要


![Implementation Flow](../../visuals/env-guard-flow-zh-TW.svg)
*圖：.env 檔案守衛資料流 — PreToolUse 攔截 Read 呼叫，阻擋敏感檔案存取。*

這堂課展示了完整可運作的 hook 實作 — 從配置到測試。PM 不需要寫 hook，但理解實作流程幫助你撰寫更好的驗收標準、估算工程量，並驗證安全需求是否正確執行。

---

## 實作流程（不需要寫 code）

把實作 hook 想像成在建築物裡安裝新的保全攝影機系統：

| 步驟 | 建築保全 | Hook 實作 |
|------|------------------|---------------------|
| 1. 登記攝影機 | 加到保全控制面板 | 在 `settings.local.json` 加入 hook 設定 |
| 2. 對準正確的門 | 設定攝影機角度 | 設定 `matcher` 指向特定工具 |
| 3. 設定警報規則 | 「晚上 10 點後有人進入就警報」 | 寫腳本：「檔案路徑包含 .env 就封鎖」 |
| 4. 測試系統 | 走過門口驗證 | 請 Claude 讀取 .env — 驗證被封鎖 |
| 5. 啟用 | 啟動系統 | 重啟 Claude Code |

> 💡 **PM 洞察**
>
> 最重要的細節：hook 需要**重啟**才會生效。這意味著向團隊部署新 hook 不是即時的 — 在你的推出計畫中考慮這一點。

---

## PM 應驗證的項目

當工程師實作 hook 時，以下是驗收標準的檢查清單：

### 1. 覆蓋檢查
- **Hook 涵蓋所有相關工具了嗎？** 檔案存取防護必須涵蓋 `Read` 和 `Grep`。問：「Claude 能透過其他工具存取這些資料嗎？」

### 2. 回饋品質
- **封鎖訊息有解釋原因嗎？** Claude 收到 stderr 訊息。好的訊息幫助 Claude 嘗試替代方案。差的訊息造成困惑。

### 3. 測試完整性
- **正面測試**：hook 封鎖了受限動作
- **負面測試**：hook 允許正常操作繼續
- **邊界案例**：絕對路徑、相對路徑、相似檔名

### 4. 設定層級

![自我修正迴路](../../visuals/self-correcting-loop-zh-TW.svg)
*圖：自我修正回饋迴路 — Claude 嘗試、Hook 攔截並說明原因、Claude 自動調整做法。*

- **個人 hook** → `settings.local.json`（不在 git 中）
- **團隊 hook** → `settings.json`（commit 到 git）
- 合規 hook 應該永遠在團隊層級

> ⚠️ **PM 風險警示**
>
> 如果安全 hook 在 `settings.local.json`，每個開發者必須個別配置。合規需求應堅持用 `settings.json`（團隊共用）。

---

## 自我修正回饋迴圈

PM 需要理解的最強大面向之一：

1. Claude 嘗試讀取 `.env`
2. Hook 封鎖並發送回饋：「You cannot read the .env file」
3. Claude 確認：「I was prevented by a read hook from accessing that file」
4. Claude 調整方法 — 不需人工介入

這意味著 hook 創造了**自主合規** — AI 代理自我修正，不需人工介入。這是相對於 prompt 方法的重大產品優勢。

---

## 工程量估算

PM 規劃 sprint 參考：

| Hook 複雜度 | 工時 | 範例 |
|----------------|--------|---------|
| 簡單檔案防護 | 1-2 小時 | 封鎖讀取 `.env`、`.credentials` |
| 模式比對封鎖 | 2-4 小時 | 封鎖符合黑名單的 Bash 命令 |
| 條件邏輯 | 4-8 小時 | 封鎖 > $500 退款，主管批准則允許 |
| 多工具協調 | 1-2 天 | 跨多個工具執行工作流程順序 |

---

## 反模式（考試常考）

| ❌ 錯誤做法 | ✅ 正確做法 | 為什麼 |
|-------------------|---------------------|-----|
| 假設存檔後 hook 就「自動生效」 | 改 hook 後一定重啟 Claude Code | Hook 只在啟動時載入 |
| 接受靜默封鎖（無回饋訊息） | 要求清楚、可行動的錯誤訊息 | 沒有回饋 Claude 無法自我修正 |
| 合規 hook 放在個人設定 | 合規 hook 放在團隊共用設定 | 個人設定無法跨團隊強制執行 |
| 只測試封鎖案例 | 同時測試封鎖和允許 | 過於激進的 hook 破壞正常工作流程 |

---

## 練習題

### Q1：客戶支援情境（S1）

你的團隊實作了 PreToolUse hook 來防止 AI 客服代理處理超過 $500 的退款。測試中 hook 正確封鎖了大額退款。但代理回覆客戶「I encountered an error」而非解釋政策。你應建議什麼？

- A. 在 system prompt 加入退款政策說明
- B. 改善 hook 的 stderr 訊息，包含政策說明（如「退款超過 $500 需主管批准 — 請升級處理」）
- C. 改用 PostToolUse hook 讓代理能看到退款被封鎖
- D. 移除 hook，依賴 prompt 指令以獲得更好的客戶體驗

<details><summary>答案</summary>

**B** — Hook 的 stderr 訊息直接轉發給 Claude 作為回饋。清楚的政策訊息幫助 Claude 準確向客戶解釋情況。

- A：Prompt 指令不解決根因（差的 hook 回饋）
- C：PostToolUse 無法封鎖
- D：為 UX 移除確定性執行造成合規風險

**PM 重點**：Hook 回饋品質直接影響客戶體驗。驗收標準應包含「hook 必須在錯誤訊息中提供清楚的政策說明」。
</details>

### Q2：開發者生產力情境（S4）

你的團隊部署了 PreToolUse hook 來封鎖 Claude 修改 migration 檔案。一位工程師回報 hook 在他機器上未啟用，Claude 修改了一個 migration 檔。調查發現 hook 只配置在 team lead 的 `settings.local.json`。正確的修正方式？

- A. 寄信給所有工程師，請他們加到個人設定
- B. 將 hook 配置移到 `.claude/settings.json` 並 commit 到版本控制
- C. 在 CLAUDE.md 加入「不要修改 migration 檔案」作為備援
- D. 在所有機器的全域設定（`~/.claude/settings.json`）配置 hook

<details><summary>答案</summary>

**B** — 團隊共用 hook 屬於 `.claude/settings.json`（commit 到 git），確保所有團隊成員自動取得配置。

- A：手動分發容易出錯且不可擴展
- C：CLAUDE.md 是 prompt-based — 不提供確定性執行
- D：全域設定需要在每台機器手動設定且不受版本控制

**PM 重點**：合規 hook 必須在版本控制的團隊共用設定中 — 不是個人配置。
</details>

### Q3：多代理研究情境（S3）

工程師實作了 PostToolUse hook，在每次 API tool call 後執行資料驗證。測試中 hook 正確驗證資料，但 Claude 沒有在回應中使用驗證後的資料。最可能的問題？

- A. Hook 應改為 PreToolUse
- B. Hook 的回饋（驗證後資料）被寫到 stdout 而不是 stderr
- C. Matcher 沒有指向正確的工具
- D. Claude 的 context window 太小無法包含 hook 回饋

<details><summary>答案</summary>

**B** — PostToolUse hook 回饋必須寫到 stderr 才會包含在 Claude 的 context 中。如果驗證後資料寫到 stdout，Claude 永遠看不到。

- A：PreToolUse 在資料存在前執行 — 無法驗證
- C：如果 hook 在運行（正確偵測資料），matcher 沒問題
- D：Hook 回饋很小，不會顯著影響 context window

**PM 重點**：與工程師確認 hook 輸出到 stderr 而非 stdout。這是常見的實作錯誤，會靜默破壞回饋迴圈。
</details>
