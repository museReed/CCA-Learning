# What are skills? — 工程師深度解析

| 項目 | 細節 |
|------|--------|
| 考試領域 | D3 — Claude Code 設定與工作流程 (20%) |
| 任務陳述 | 3.1 (CLAUDE.md)、3.3 (自訂指令/skill)、3.5 (權限模型) |
| 來源 | introduction-to-agent-skills / 第 01 課 |

---

## 一句話摘要

本影片介紹 skill — 可重複使用的 markdown 檔案，用來教導 Claude Code 如何自動處理特定任務。你不需要每次請 Claude 審查 PR 或撰寫 commit 訊息時都重複給出指示，只要撰寫一次 skill，Claude 就會在該任務出現時自動套用。

---

## 核心概念

### 學習目標

- 定義 Claude Code skill 是什麼以及它們如何運作
- 說明 skill 存放的位置（個人目錄 vs. 專案目錄）
- 區分 skill、CLAUDE.md 和 slash command 之間的差異
- 辨識適合使用 skill 作為自訂工具的情境

### 重點摘要

skill 是一組指令資料夾，Claude Code 可以自動發現並使用它們來更準確地處理任務。每個 skill 都存放在一個 SKILL.md 檔案中，其 frontmatter 包含名稱和描述。

---

## 記憶卡

**Q1：** skill 是一組指令資料夾，Claude Code 可以自動發現並使用它們來…？
**A1：** skill 是一組指令資料夾，Claude Code 可以自動發現並使用它們來更準確地處理任務。每個 skill 都存放在一個 SKILL.md 檔案中，其 frontmatter 包含名稱和描述。

---

*來源：introduction-to-agent-skills — What are skills?*
