# Configuration and multi-file skills — PM 觀點

| 項目 | 細節 |
|------|---------|
| 考試範圍 | D3 — Claude Code 設定與工作流程 (20%) |
| 任務陳述 | 3.1 (CLAUDE.md)、3.3 (自訂指令/skill)、3.5 (權限模型) |
| 課程來源 | introduction-to-agent-skills / 第 03 課 |

---

## 一句話摘要

本影片涵蓋讓 skill 更強大的進階技巧：完整的 metadata 欄位集、如何撰寫能可靠觸發的描述、為安全敏感的工作流程限制工具存取權限，以及使用漸進式揭露（progressive disclosure）跨多個檔案組織較大的 skill。你將學會如何在支援複雜使用情境的同時保持 skill 的效率。

---

## 為什麼 PM 需要知道

### 學完本課你將理解

- 設定進階 skill metadata 欄位，包括 allowed-tools 和 model
- 撰寫能在正確請求時可靠觸發的有效 skill 描述
- 使用 allowed-tools 來限制 skill 啟用時 Claude 可以使用的工具
- 使用漸進式揭露和多檔案結構來組織複雜的 skill

### 重點摘要（商業影響）

name 和 description 是必填欄位 — allowed-tools 和 model 是選填但功能強大的附加項目。
好的 description 要回答兩個問題：這個 skill 做什麼？Claude 應該在什麼時候使用它？
allowed-tools 限制 skill 啟用時 Claude 可以使用的工具 — 適用於唯讀或安全敏感的工作流程。

---

## PRD 檢查清單

- [ ] 團隊是否理解設定與多檔案 skill？
- [ ] 相關功能是否已記錄在文件中？
- [ ] 是否已考慮邊界情況？

---

*來源：introduction-to-agent-skills — Configuration and multi-file skills*
