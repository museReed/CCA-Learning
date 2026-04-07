# Hooks 的注意事項 — PM 觀點

| 項目 | 細節 |
|------|---------|
| 考試範圍 | D3 — Claude Code Configuration & Workflows（佔考試 20%） |
| Task Statements | 3.2 (custom commands & hooks), 1.5 (Agent SDK hooks) |
| 課程來源 | claude-code-in-action / 05-hooks / Lesson 17（純文字課） |

---

## 重點摘要

Hook 腳本應使用絕對路徑以確保安全，但絕對路徑是機器特定的。解法是模板檔案搭配自動化 setup script。PM 需要理解這一點因為它影響入職、CI/CD 和安全合規。

---

## PM 為何需要關注

1. **安全審計** — 相對路徑會被標記
2. **開發者入職** — 需要執行 setup 步驟
3. **CI/CD pipeline** — 需要機器特定配置
4. **團隊一致性** — 沒有模板模式 hook 可能靜默失敗

---

## 心智模型：辦公大樓門禁卡

| 面向 | 門禁卡系統 | Hook 配置 |
|--------|----------------|-------------------|
| 安全需求 | 掃描器必須連到確切伺服器 | Hook 必須指向確切腳本（絕對路徑） |
| 可攜問題 | 每棟大樓地址不同 | 每台機器路徑不同 |
| 解法 | 模板 + 大樓特定 setup | 模板設定 + 機器特定 init script |

> [!TIP]
> **PM 重點**
>
> 絕對路徑 = 更高安全性，但需要自動化 setup 步驟。PRD 要求 hook 時，在部署計畫中包含入職 setup。

---

## 兩個檔案

| 檔案 | 在 Git？ | 包含 Hook？ |
|------|---------|----------------|
| `settings.json` | **是** | 一般設定 |
| `settings.local.json` | **否** | 帶絕對路徑的 Hook |

> [!WARNING]
> **PM 治理備註**
>
> 合規 hook 只在 `settings.local.json` 的話取決於每人是否執行 setup。包含在入職清單中。

---

## 反模式（考試常考）

| ❌ 錯誤做法 | ✅ 正確做法 | 為什麼 |
|-------------------|---------------------|-----|
| 為方便允許相對路徑 | 要求絕對路徑 | 安全審計標記 |
| Commit 機器特定設定 | 用模板 + init script | 其他機器會壞 |
| 略過 setup 文件 | 入職清單包含 setup | 新人會有壞 hook |

---

## 練習題

### Q1：開發者生產力情境（S4）

新開發者加入後 Claude 可讀取憑證檔。團隊有 PreToolUse hook。原因？

- A. Claude Code bug
- B. 沒執行 setup script，`settings.local.json` 未生成
- C. Hook 在全域層級
- D. PreToolUse 只對 Read 有效

<details><summary>答案</summary>

**B** — `settings.local.json` 被 gitignore，必須由 setup script 生成。

> [!IMPORTANT]
> **PM 重點**：Hook 啟用是環境 setup 的一部分，必須在入職清單中。
</details>

### Q2：CI/CD 整合情境（S5）

安全團隊要求絕對路徑。CI 在動態 runner 上。如何配置？

- A. CI 中用相對路徑
- B. 加 CI 步驟執行 init script 生成 `settings.local.json`
- C. 寫死路徑
- D. 停用 hook

<details><summary>答案</summary>

**B** — Init script 模式在 CI 也適用。

> [!IMPORTANT]
> CI/CD 環境需要與開發者機器相同的安全態勢。
</details>

### Q3：客戶支援情境（S1）

安全審計標記 hook 用相對路徑。工程師說絕對路徑難共享。解法？

- A. 接受風險
- B. 用帶 `$PWD` 佔位符的模板和 init script
- C. 移除 hook 用 prompt
- D. 用相對路徑加 CLAUDE.md 警告

<details><summary>答案</summary>

**B** — 模板 + init script 同時滿足安全和可攜。

> [!IMPORTANT]
> **PM 重點**：安全-便利取捨時尋找兩者兼顧方案。
</details>
