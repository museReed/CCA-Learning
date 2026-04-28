# Creating your first skill — 工程師深度解析

| 項目 | 細節 |
|------|--------|
| 考試領域 | D3 — Claude Code 設定與工作流程 (20%) |
| 任務陳述 | 3.1 (CLAUDE.md)、3.3 (自訂指令/skill)、3.5 (權限模型) |
| 來源 | introduction-to-agent-skills / 第 02 課 |

---

## 一句話摘要

本影片帶你從零開始建立一個 skill — 一個可跨所有專案使用的個人 PR 描述 skill。你將看到如何建構 SKILL.md 檔案的結構、測試它，並了解 Claude Code 如何發現並將 skill 與你的請求進行匹配。

---

## 核心概念

### 學習目標

- 從零開始建立一個具有正確 frontmatter 結構的 skill
- 測試並驗證 skill 在 Claude Code 中是否正確載入
- 說明 Claude Code 如何將傳入的請求與可用的 skill 進行匹配
- 描述 skill 的優先順序層級（Enterprise、個人、專案、plugin）

### 重點摘要

一個 skill 就是一個包含 SKILL.md 檔案的目錄，其中有 frontmatter 格式的 metadata（名稱、描述）和下方的指令內容。

### 關鍵要點

- 具體變更的要點列表
- 將相關變更分組
- 提及任何被刪除或重新命名的檔案

---

## 記憶卡

**Q1：** 一個 skill 就是一個包含 SKILL.md 的目錄…？
**A1：** 一個 skill 就是一個包含 SKILL.md 檔案的目錄，其中有 frontmatter 格式的 metadata（名稱、描述）和下方的指令內容。

---

*來源：introduction-to-agent-skills — Creating your first skill*
