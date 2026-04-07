# Summary and Next Steps — PM 視角

| 項目 | 內容 |
|------|------|
| 考試對應 | 全部 5 個 Domain（D1-D5） |
| Task Statements | 複習：1.1、2.1、2.4、3.1、3.2、3.6 |
| 課程來源 | claude-code-in-action / 06-sdk-and-wrap-up / Lesson 22 |

---

## TL;DR

課程以三個建議收尾：保持更新、勇於實驗、善用自動化。對 PM 來說，這是綜合盤點的時刻 — 理解 Claude Code 在整個技術棧上的能力（agentic 執行、tool 整合、設定、CI/CD 自動化），並將其轉化為產品決策、團隊工作流和自動化策略。

---

![Course Review Map](../../visuals/course-review-map-zh-TW.svg)
*圖：課程章節對應 CCA 考試領域。*


## 我們學到了什麼：逐章節 PM 重點

| 章節 | 學到什麼 | PM 行動項目 |
|------|---------|------------|
| 01 — Intro | Claude Code 是 agentic coding assistant，能自主計畫、執行和迭代。與 autocomplete 本質不同。 | **撰寫定位文件**，在 build-vs-buy 評估時區分 agentic AI 和 autocomplete 工具。 |
| 02 — Getting Started | 透過 `CLAUDE.md` 進行 project setup，定義 Claude 如何理解你的 codebase。Context window 有限且需要管理。 | **定義專案標準**的 `CLAUDE.md` — 每個團隊專案應包含哪些慣例、約束和 context？ |
| 03 — Context & Commands | Custom commands 建立可重複使用的工作流。Context 可透過 `@file` 引用精確控制。 | **識別團隊重複性工作流**（code review、bug triage、release notes）可轉為 custom commands。 |
| 04 — Integrations | MCP servers 擴展 Claude 的能力。GitHub integration 自動化 PR review 和 issue 回應。 | **評估** 與你技術棧相關的 MCP servers。**建立自動 PR review** 作為品質閘門。 |
| 05 — Hooks | Hooks 在 tool 執行層級強制執行政策。9 種 hook 類型涵蓋完整生命週期。 | **定義治理政策**（如「禁止直接存取 production DB」）透過 hooks 強制執行。 |
| 06 — SDK & Wrap Up | SDK 提供 programmatic 整合。課程以三個前瞻性建議收尾。 | **規劃整合路線圖** — Claude Code 在你的 CI/CD pipeline 中的 programmatic 定位在哪？ |

---

## 三個建議的 PM 視角

### 1. Stay Updated — 追蹤平台路線圖

Claude Code 持續活躍演進。新能力會改變什麼是可行的。

**PM 行動：**
- 訂閱 Claude Code changelog 和 release notes
- 維護能力清單 — Claude Code 今天能做什麼 vs 三個月前不能做什麼
- 每季重新檢視「目前不可行」的決策，因為能力在演進

### 2. Experiment — 建立團隊肌肉記憶

客製化（CLAUDE.md、commands、MCP servers）是讓 Claude Code 從通用助手變成團隊專用工具的關鍵。

**PM 行動：**
- 在 sprint 中分配 Claude Code 實驗時間（custom commands、MCP server 試用）
- 為組織專案建立共享的 `CLAUDE.md` template
- 記錄團隊使用哪些 MCP servers 及原因

### 3. Automate — 設計事件驅動工作流

GitHub integration 將 Claude Code 從開發者工具轉變為團隊自動化層。

**PM 行動：**
- 將團隊的重複性任務映射到潛在自動化觸發條件（PR 建立、Issue 開啟、`@claude` mention）
- 定義自動回應的 SLA（如「PR 建立後 5 分鐘內完成 review」）
- 建立治理框架，定義 Claude 可以和不可以自主做什麼

---

## 課程 vs 考試 Domain 對照（PM 視角）

| Domain | 權重 | PM 應該知道什麼 | 對應章節 |
|--------|------|----------------|---------|
| D1 — Agentic Architecture | 27% | Claude 如何自主計畫和執行。為什麼有時會失敗（context 限制、tool 選擇）。 | 01、02、06 |
| D2 — Tool Use & MCP | 20% | MCP 作為擴展模型。如何評估和整合第三方工具。 | 04 |
| D3 — Configuration | 20% | `CLAUDE.md` 作為團隊標準。Commands 作為可重用工作流。Hooks 作為政策強制。CI/CD 作為自動化。 | 02、03、04、05 |
| D4 — Security & Trust | 15% | Permission model（3 層）。為什麼 CI 需要明確權限。基於 Hook 的存取控制。 | 02、04、05 |
| D5 — Developer Productivity | 18% | 何時使用 Claude Code。自動化如何減少苦力。衡量生產力提升。 | 01、04、06 |

---

## PM 決策框架：投資優先順序

根據完整課程內容，以下是優先投資框架：

| 優先級 | 投資項目 | 成本 | 影響 | 理由 |
|--------|---------|------|------|------|
| 1 | `CLAUDE.md` 標準 | 低 | 高 | 每次互動都受益於清晰的專案 context。零持續成本。 |
| 2 | 自動 PR review（GitHub integration） | 中 | 高 | 100% review 覆蓋率。捕捉結構性問題。減少開發者 context switching。 |
| 3 | 團隊工作流 custom commands | 低 | 中 | 標準化團隊與 Claude 的互動方式。跨專案可重用。 |
| 4 | MCP server 評估 | 中 | 中 | 擴展 Claude 的能力以匹配你的技術棧。 |
| 5 | 基於 Hook 的治理 | 高 | 中 | Tool 層級的政策強制。對安全敏感團隊很重要。 |
| 6 | SDK 整合 | 高 | 視情況 | 用於自訂工具的 programmatic 存取。ROI 取決於使用案例。 |

---

## 商業影響總結

| 指標 | 導入 Claude Code 前 | 完整導入後 |
|------|-------------------|-----------|
| PR review 覆蓋率 | 不一致（取決於 reviewer 可用性） | 100% 自動化初步 review |
| Bug triage 時間 | 數小時（開發者調查） | 幾分鐘（Issue 中 `@claude` mention） |
| Onboarding 摩擦 | 高（手動學習專案慣例） | 較低（`CLAUDE.md` 編碼慣例） |
| 政策遵循 | 人工 review | 自動化（hooks 在 tool 層級強制） |
| 重複性任務成本 | 每次都消耗開發者時間 | 一次性 command/automation 設定 |

---

## Practice Questions

### Question 1：策略情境

你的團隊完成了 Claude Code in Action 課程。CTO 要求你提出分階段導入計畫。哪個順序最合理？

- A. SDK 整合 → hooks → CLAUDE.md → GitHub integration
- B. CLAUDE.md 標準 → GitHub integration（PR review）→ custom commands → hooks
- C. Custom commands → MCP servers → CLAUDE.md → SDK
- D. 先 Hooks（安全）→ 其他隨意

<details><summary>答案與解析</summary>

**B** — 從最低成本、最高影響開始。`CLAUDE.md` 是基礎（每次互動都受益）。GitHub PR review 提供即時自動化價值。Custom commands 標準化團隊工作流。Hooks 在治理需求成熟後導入。

- A 從最高成本項目（SDK）開始 — 優先順序不佳
- C 跳過基礎層（CLAUDE.md）
- D 安全優先但忽略了需要基本採用後才能做治理

**PM 重點**：基礎先行（CLAUDE.md）→ 自動化（GitHub）→ 客製化（commands）→ 治理（hooks）→ programmatic 存取（SDK）。
</details>

### Question 2：生產力情境

團隊中一位開發者說「Claude Code 就是個高級 autocomplete」。根據課程，你應該解釋什麼關鍵區別？

- A. Claude Code 使用更大的語言模型
- B. Claude Code 在 agentic loop 中運作 — 自主計畫、執行工具、觀察結果並迭代，不像 autocomplete 只預測下一個 token
- C. Claude Code 可以使用 MCP servers
- D. Claude Code 可以讀取 CLAUDE.md 檔案

<details><summary>答案與解析</summary>

**B** — 根本區別在於 agentic loop。Autocomplete 預測行內補全。Claude Code 自主規劃多步驟方案、執行工具（檔案讀寫、終端命令）、觀察結果並迭代。這是第一章的核心概念（D1 — Agentic Architecture）。

- A 是技術細節，不是架構層面的區分
- C 和 D 是 agentic 架構中的功能，不是核心差異

**PM 重點**：Agentic loop 是定義性能力。其他一切（MCP、hooks、SDK）都建立在這個自主的 plan-execute-observe 循環之上。
</details>

### Question 3：自動化情境

你的團隊想自動化三個任務：(1) PR code review、(2) 強制「production code 中禁止 console.log」政策、(3) 從 PR 描述生成 release notes。哪些 Claude Code 功能對應到每個？

- A. (1) GitHub PR Review Action、(2) PreToolUse hook、(3) Custom command
- B. (1) Custom command、(2) CLAUDE.md 指令、(3) GitHub mention
- C. (1) MCP server、(2) PostToolUse hook、(3) SDK integration
- D. (1) GitHub PR Review Action、(2) PostToolUse hook、(3) Custom command

<details><summary>答案與解析</summary>

**A** — (1) GitHub PR Review Action 專為自動 code review 設計。(2) PreToolUse hook 可攔截檔案寫入，偵測到 `console.log` 就 block — 這是 blocking 政策強制。(3) Custom command 可模板化 release notes 生成工作流。

- B 用 CLAUDE.md 做政策強制 — 這是指導而非強制（Claude 仍可繼續）
- C 用 PostToolUse 做政策 — PostToolUse 無法 block，只能在事後提供回饋
- D 用 PostToolUse — 同 C 的問題，無法防止違規

**PM 重點**：Blocking enforcement 需要 PreToolUse（唯一能阻止執行的 tool-level hook）。PostToolUse 是用來觀察和回饋的，不是強制的。
</details>
