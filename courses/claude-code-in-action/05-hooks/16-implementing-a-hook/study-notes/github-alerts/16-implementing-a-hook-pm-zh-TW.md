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

這堂課展示了完整可運作的 hook 實作。PM 不需要寫 hook，但理解實作流程幫助你撰寫更好的驗收標準。

---

## 實作流程

| 步驟 | 建築保全 | Hook 實作 |
|------|------------------|---------------------|
| 1. 登記攝影機 | 加到控制面板 | 在 `settings.local.json` 加入 hook |
| 2. 對準正確的門 | 設定角度 | 設定 `matcher` |
| 3. 設定警報規則 | 「10 點後有人就警報」 | 寫腳本邏輯 |
| 4. 測試 | 走過門口驗證 | 請 Claude 讀取 .env |
| 5. 啟用 | 啟動系統 | 重啟 Claude Code |

> [!TIP]
> **PM 洞察**
>
> Hook 需要**重啟**才會生效。向團隊部署新 hook 不是即時的 — 在推出計畫中考慮這一點。

---

## PM 驗收檢查清單

> [!IMPORTANT]
> **驗收標準**
>
> 1. **覆蓋**：Hook 涵蓋所有相關工具了嗎？
> 2. **回饋品質**：封鎖訊息有解釋政策嗎？
> 3. **測試**：正面（封鎖）和負面（允許）測試都通過
> 4. **設定層級**：合規 hook 在團隊共用設定中

---

## 自我修正回饋迴圈

1. Claude 嘗試讀取 `.env`
2. Hook 封鎖並發送回饋
3. Claude 確認並調整方法 — 不需人工介入

> [!WARNING]
> **PM 風險警示**
>
> 安全 hook 在 `settings.local.json` 的話，每個開發者必須個別配置。合規需求應堅持用 `settings.json`（團隊共用、版本控制）。

---

## 反模式（考試常考）

| ❌ 錯誤做法 | ✅ 正確做法 | 為什麼 |
|-------------------|---------------------|-----|
| 假設存檔後就生效 | 一定重啟 Claude Code | Hook 只在啟動時載入 |
| 接受靜默封鎖 | 要求清楚的錯誤訊息 | Claude 需要回饋 |
| 合規 hook 放個人設定 | 放團隊共用設定 | 個人設定無法跨團隊強制 |

---

## 練習題

### Q1：客戶支援情境（S1）

團隊實作了封鎖 > $500 退款的 hook。Hook 運作但代理回覆「I encountered an error」而非政策說明。你的建議？

- A. 在 system prompt 加退款政策
- B. 改善 hook 的 stderr 訊息，包含政策說明
- C. 改用 PostToolUse
- D. 移除 hook

<details><summary>答案</summary>

**B** — Hook 的 stderr 訊息直接轉發給 Claude。

> [!IMPORTANT]
> **PM 重點**：Hook 回饋品質直接影響客戶體驗。
</details>

### Q2：開發者生產力情境（S4）

PreToolUse hook 在一位工程師的機器上未啟用。Hook 只在 team lead 的 `settings.local.json`。修正方式？

- A. 寄信給所有工程師
- B. 移到 `.claude/settings.json` 並 commit
- C. 在 CLAUDE.md 加入限制
- D. 在所有機器全域設定

<details><summary>答案</summary>

**B** — 團隊共用 hook 屬於 `.claude/settings.json`。

> [!IMPORTANT]
> **PM 重點**：合規 hook 必須在版本控制的團隊設定中。
</details>

### Q3：多代理研究情境（S3）

PostToolUse hook 驗證資料但 Claude 沒使用驗證後的資料。問題？

- A. 應改為 PreToolUse
- B. 回饋寫到 stdout 而非 stderr
- C. Matcher 不對
- D. Context window 太小

<details><summary>答案</summary>

**B** — PostToolUse 回饋必須寫到 stderr 才會進入 Claude 的 context。

> [!IMPORTANT]
> **PM 重點**：確認 hook 輸出到 stderr 而非 stdout。
</details>
