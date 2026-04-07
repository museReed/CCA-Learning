# Hooks 的注意事項 — PM 觀點

| 項目 | 細節 |
|------|---------|
| 考試範圍 | D3 — Claude Code Configuration & Workflows（佔考試 20%） |
| Task Statements | 3.2 (custom commands & hooks), 1.5 (Agent SDK hooks) |
| 課程來源 | claude-code-in-action / 05-hooks / Lesson 17（純文字課） |

---

## 重點摘要

Hook 腳本應使用絕對檔案路徑以確保安全，但絕對路徑是機器特定的，跨團隊共享時會壞掉。解法是模板檔案（`settings.example.json`）搭配佔位符，由自動化 setup script 轉換為機器特定的絕對路徑。PM 需要理解這一點，因為它影響新人入職、CI/CD 配置和安全合規。

---

## PM 為何需要關注

1. **安全審計** — 若組織要求安全審查，相對路徑的 hook command 會被標記
2. **開發者入職** — 新團隊成員需要執行 setup 步驟才能讓 hook 運作
3. **CI/CD pipeline** — 自動化環境中的 hook 需要機器特定配置
4. **團隊一致性** — 沒有模板模式，hook 可能在某些機器上靜默失敗

---

## 心智模型：辦公大樓門禁卡

| 面向 | 門禁卡系統 | Hook 配置 |
|--------|----------------|-------------------|
| 安全需求 | 掃描器必須連到確切的安全伺服器 | Hook 必須指向確切的腳本檔（絕對路徑） |
| 可攜問題 | 每棟大樓安全伺服器在不同地址 | 每台開發機器檔案在不同路徑 |
| 解法 | 模板卡配置 + 大樓特定 setup | 模板設定檔 + 機器特定 init script |
| 入職 | 新員工在自己大樓啟用卡片 | 新開發者在機器上執行 `npm run setup` |

> 💡 **PM 重點**
>
> 絕對路徑 = 更高安全性，但需要自動化 setup 步驟。如果你的 PRD 要求 hook，在部署計畫中包含「新開發者入職需要 setup 步驟」。

---

## 工程師會看到的兩個檔案


![Security vs Portability](../../visuals/security-portability-tradeoff-zh-TW.svg)
*圖：安全性與可攜性的取捨 — 絕對路徑安全但綁定機器；Template + init script 可兩全其美。*

| 檔案 | 誰建立 | 在 Git？ | 包含 Hook？ |
|------|---------------|---------|----------------|
| `settings.json` | Team lead，commit | **是** | 一般設定（無機器特定路徑） |
| `settings.local.json` | Setup script 自動生成 | **否** | 帶絕對路徑的 Hook command |

> ⚠️ **PM 治理備註**
>
> 如果合規 hook 只在 `settings.local.json`，它取決於每個開發者是否執行了 setup script。將此包含在入職檢查清單中。

---

## PM 應知道的安全概念

| 攻擊 | 商業風險 | 預防 |
|--------|--------------|-----------|
| **Path interception** | 惡意程式碼取代了預期的 hook 腳本執行 | 絕對路徑繞過目錄搜尋 |
| **Binary planting** | 攻擊者在專案目錄放入假冒腳本 | 絕對路徑忽略同名本地檔案 |

---

## 入職影響

| 發生什麼 | 影響 | 修正 |
|-------------|--------|-----|
| `settings.local.json` 不存在 | 沒有 hook 啟用 | 執行 `npm run setup` |
| 直接複製 `settings.example.json` | `$PWD` 佔位符殘留 — hook 靜默失敗 | 正確執行 init script |

> 💡 **PM 行動項目**
>
> 在團隊入職文件中加入「執行專案 setup script」。透過請 Claude 讀取受保護檔案來驗證 hook 是否啟用。

---

## 反模式（考試常考）

| ❌ 錯誤做法 | ✅ 正確做法 | 為什麼 |
|-------------------|---------------------|-----|
| 為方便允許相對路徑 | 為安全要求絕對路徑 | 安全審計會標記相對路徑 |
| Commit 機器特定設定到 git | 用模板 + init script 模式 | 機器特定路徑在其他機器壞掉 |
| 略過 setup 步驟文件 | 在入職檢查清單中包含 setup | 新開發者會有不起作用的 hook |

---

## 練習題

### Q1：開發者生產力情境（S4）

團隊部署了 PreToolUse hook 防止 Claude 存取憑證檔。新開發者加入後 Claude 在他們機器上可以讀取憑證。最可能原因？

- A. Claude Code 在某些 OS 上有繞過 hook 的 bug
- B. 新開發者沒有執行 setup script，`settings.local.json` 從未生成
- C. Hook 配置在全域層級，不在專案中
- D. PreToolUse hook 只對 Read 有效，不對 Grep

<details><summary>答案</summary>

**B** — `settings.local.json` 被 gitignore，必須由 setup script 生成。沒執行 setup 就沒有 hook 啟用。

**PM 重點**：Hook 啟用是開發環境 setup 的一部分。像資料庫 migration 或依賴安裝一樣 — 必須在入職檢查清單中。
</details>

### Q2：CI/CD 整合情境（S5）

安全團隊要求所有 hook 腳本使用絕對路徑。CI pipeline 在動態配置的 runner 上運行，workspace 目錄每次不同。如何為 CI 配置 hook？

- A. CI 中用相對路徑，自動化環境安全性較不重要
- B. 加入 CI pipeline 步驟，執行 init script 生成帶當前 workspace 絕對路徑的 `settings.local.json`
- C. 在 `settings.json` 寫死最常見的 CI workspace 路徑
- D. 在 CI 停用 hook

<details><summary>答案</summary>

**B** — Init script 模式在 CI 也適用。Setup 步驟從模板生成機器特定的絕對路徑。

**PM 重點**：CI/CD 環境需要與開發者機器相同的安全態勢。
</details>

### Q3：客戶支援情境（S1）

安全審計發現 hook command 用相對路徑。工程團隊認為絕對路徑會讓設定檔難以共享。推薦解法？

- A. 接受安全風險
- B. 用帶 `$PWD` 佔位符的 `settings.example.json` 模板和自動化 init script
- C. 移除 hook，改用 system prompt
- D. 用相對路徑但加 CLAUDE.md 指令

<details><summary>答案</summary>

**B** — 模板 + init script 模式同時滿足安全（絕對路徑）和團隊共享（可攜性）。

**PM 重點**：當工程師提出安全-便利取捨時，尋找兩者兼顧的方案。
</details>
