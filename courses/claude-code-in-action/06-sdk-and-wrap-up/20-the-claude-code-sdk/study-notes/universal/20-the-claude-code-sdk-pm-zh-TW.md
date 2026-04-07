# The Claude Code SDK — PM 視角

| 項目 | 內容 |
|------|------|
| 考試對應 | D2 — Tool Integration & MCP（佔 20%）、D3 — Claude Code Configuration & Workflows（佔 20%）、D1 — Agentic Architecture（佔 27%） |
| Task Statements | 2.4（MCP integration — SDK 以程式化方式擴展 Claude Code）、3.6（CI/CD integration — SDK 驅動自動化工作流）、1.1（agentic loops — SDK 以程式化方式執行完整 agentic loop） |
| 課程來源 | claude-code-in-action / 06-sdk-and-wrap-up / Lesson 20 |

---

## TL;DR

Claude Code SDK 讓其他程式可以在沒有人類操作鍵盤的情況下使用 Claude Code。它是相同的 Claude Code — 相同規則、相同能力 — 但由腳本和 pipeline 控制而非人類。預設只能讀取、不能寫入，這是刻意的安全設計。PM 需要理解這點，因為它決定了哪些自動化工作流是可行的，以及如何在需求中描述它們。

---

![Sdk Architecture](../../visuals/sdk-architecture-zh-TW.svg)
*圖：Claude Code SDK 架構 — 三個進入點、同一引擎、權限模型。*


## PM 為什麼需要了解 SDK

SDK 將 Claude Code 從開發者工具轉變為**自動化組件**。這對產品很重要：

| 沒有 SDK | 有 SDK |
|---------|--------|
| Claude Code 一次幫一位開發者 | Claude Code 在 CI/CD 中為每個 PR 運行 |
| 人類必須手動輸入每個 prompt | 腳本在事件（git push、build、排程）觸發時啟動 Claude Code |
| 權限由開發者即時批准 | 權限必須預先配置 — 沒有人類在迴圈中 |

> 💡 **PM 重點**
> SDK 是 Claude Code 從「一位開發者的助手」擴展到「團隊級自動化」的方式。任何涉及自動化 AI code review、程式碼生成或分析的需求，大概率需要 SDK。

---

## 心智模型：聘請承包商

把終端機裡的 Claude Code 想像成承包商在你身邊工作 — 你告訴他做什麼、看著他工作、逐步批准。

SDK 就像給承包商**書面工作指令**：

| 面向 | 終端機（當面） | SDK（書面工作指令） |
|------|--------------|-------------------|
| 溝通 | 即時對話 | 預先寫好的指令 |
| 監督 | 你看著每一步 | 你事後審查結果 |
| 權限 | 當下說「好，去做吧」 | 必須在工作指令中預先指定 |
| 安全 | 你可以隨時叫停 | 安全規則必須預先配置 |
| 規模 | 一次一個專案 | 同時處理多個專案 |

關鍵差異：**沒有人類監督時，你需要更嚴格的前期規則。**

---

## 三種使用 SDK 的方式

SDK 有三種介面。PM 不需要知道語法，但應了解取捨：

| 介面 | 最適合 | 團隊特徵 |
|------|-------|---------|
| TypeScript | 豐富的整合、即時訊息處理 | 有 Node.js/TypeScript 專長的團隊 |
| Python | 資料 pipeline、ML 工作流、腳本 | Python 為主的技術棧 |
| CLI（pipe 模式） | Shell 腳本、快速自動化、bash-based CI | DevOps 團隊、簡單整合 |

> 💡 **PM 重點**
> 規劃 SDK 整合時，問你的工程團隊哪個介面適合他們的技術棧。功能完全相同 — 只有程式語言不同。

---

## 預設唯讀：一個產品決策

SDK 預設為**唯讀**模式。Claude 可以分析程式碼、找出問題、報告發現 — 但無法修改任何東西，除非被明確授權。

這不是限制 — 這是刻意的產品安全決策。

### 場景分析：為什麼唯讀很重要

想像一個每晚的 CI 作業，用 Claude Code 審查所有未關閉的 PR：

| 場景 | 權限等級 | 會發生什麼 |
|------|---------|-----------|
| PR 分析 + 留言 | 唯讀（預設） | Claude 讀取程式碼、產生 review 留言。安全。 |
| 自動修正格式 | 讀取 + Edit | Claude 讀取程式碼並修改檔案。需要信任編輯邏輯。 |
| 自動修正 + commit + push | 讀取 + Edit + Bash | Claude 可以執行任意 shell 指令。沒有護欄時風險很高。 |

每往上一個權限階梯，都增加能力和風險。SDK 強制你明確做出這個取捨。

> 🎯 **考試重點**
> 最小權限原則：只授予特定任務所需的權限。Code review bot 應該唯讀。格式化 bot 需要 Edit。部署 bot 需要 Bash。絕不授予超過所需的權限。

---

## SDK 如何融入 Pipeline

SDK 最有用的角色是更大自動化工作流中的**組件**：

### 場景 1：Git Pre-Commit Hook

**業務需求**：防止意外提交 secrets

**流程**：開發者提交程式碼 -> SDK 分析 staged 檔案（唯讀） -> 發現 secrets 時阻止提交

**權限**：唯讀（預設） — 只需分析，不需修改

### 場景 2：CI/CD Code Review

**業務需求**：每個 PR 都獲得自動化第一輪審查

**流程**：PR 開啟 -> CI 觸發 SDK -> SDK 讀取 diff 並產生 review -> 在 PR 上發布留言

**權限**：唯讀 — review 產生文字輸出，不修改程式碼

### 場景 3：自動化 Dependency 更新

**業務需求**：無需手動工作即可保持 dependency 最新

**流程**：每週排程 -> SDK 檢查過期套件 -> SDK 更新設定檔 -> 建立 PR

**權限**：讀取 + Edit — 必須修改設定檔

> 🎬 **講師影片重點**
> 講師展示兩步驟示範：先用唯讀模式找出 codebase 中的重複 query，再授予 Edit 權限更新 package.json。這種漸進式權限模式是推薦做法 — 先分析，只修改需要的部分。

---

## 安全性：設定繼承

SDK 繼承專案設定中的所有安全規則。這意味著：

1. **專案層級規則**（`.claude/settings.json`）適用於 SDK 呼叫
2. **Deny 規則無法被覆寫** — SDK 呼叫者無法繞過
3. **縱深防禦**：即使 SDK 授予權限，專案設定仍可阻止

### 場景分析：多層安全

一家公司在 `.claude/settings.json` 中設定了這些規則：
- 允許：Read、Grep、Glob
- 禁止：刪除檔案的 Bash 指令

工程師寫了一個 SDK 腳本，授予 `allowedTools: ["Bash"]`。

**結果**：Claude 可以執行 Bash 指令，但刪除指令除外。Settings 的 deny 規則是 SDK 無法繞過的護欄。

> 💡 **PM 重點**
> 撰寫 SDK 自動化需求時，同時指定 SDK 權限和專案設定。它們作為層級配合工作 — SDK 授予能力，settings 定義邊界。

---

## SDK 功能的 PM 需求清單

指定 SDK 功能時，應包含：

| 需求領域 | 該指定什麼 | 範例 |
|---------|-----------|------|
| 任務範圍 | AI 應分析或修改什麼 | 「審查 PR diff 中的所有 Python 檔案」 |
| 權限等級 | 唯讀、Edit、Write、Bash 或組合 | 「分析用唯讀；自動修正模式用 Edit」 |
| 觸發條件 | 什麼事件啟動 SDK 呼叫 | 「PR 建立時」或「每晚凌晨 2 點」 |
| 輸出 | 結果送到哪裡 | 「發布為 PR 留言」或「寫入稽核日誌」 |
| 護欄 | AI 不得做什麼 | 「不得修改測試檔案」或「最多 10 個 agentic turn」 |
| 失敗處理 | SDK 呼叫失敗時怎麼辦 | 「記錄錯誤並通知團隊頻道」 |

---

## 反模式（考試常考）

| 錯誤做法 | 正確做法 | 原因 |
|---------|---------|------|
| 授予完整權限「以策安全」 | 只授予最小所需權限 | 權限越多 = 風險越大。「安全」意味著更少權限，不是更多 |
| 把 SDK 當作不同於 Claude Code 的產品 | 理解 SDK 是相同引擎的程式化介面 | 相同設定、相同工具、相同能力 |
| 需求中略過權限等級 | 明確指定每個自動化的唯讀 vs. 寫入 | 工程師無法猜測預期的安全姿態 |
| 假設 SDK 自動化不需要人類監督 | 為高風險 SDK 操作設計審查檢查點 | 沒有人類在迴圈中意味著預配置的規則必須完善 |

---

## 總結表格

| 概念 | 重點 | 考試相關性 |
|------|------|-----------|
| SDK 用途 | 以程式化方式執行 Claude Code 作為 pipeline 組件 | D1 1.1 — 自動化中的 agentic loop |
| 三種介面 | TypeScript、Python、CLI — 相同能力 | D2 2.4 — 程式化工具整合 |
| 預設唯讀 | 安全優先：除非明確授權否則不能寫入 | D3 3.6 — 安全的 CI/CD 整合 |
| 設定繼承 | 專案設定是 SDK 無法繞過的護欄 | D3 3.6 — 縱深防禦 |
| Pipeline 整合 | Git hooks、CI/CD、build scripts、排程作業 | D3 3.6 — 工作流自動化 |
| 權限升級 | 先分析（唯讀），再修改（明確授權） | D3 3.6 — 漸進式權限模型 |

---

## 記憶卡

| # | 正面 | 背面 | 記憶錨點 |
|---|------|------|---------|
| 1 | Claude Code SDK 的預設權限等級是什麼？ | 唯讀。寫入需要明確的權限授予。 | 承包商拿到「只看不動」的工作指令 |
| 2 | SDK 提供哪三種介面？ | TypeScript、Python、CLI（pipe 模式）— 功能完全相同 | 打到同一間辦公室的三條電話線 |
| 3 | SDK 為什麼預設唯讀？ | 沒有人類在迴圈中批准危險操作 — 最小權限原則 | 無人監督的承包商要更嚴格的規定 |
| 4 | SDK 會遵守專案設定嗎？ | 會 — settings 中的 deny 規則無法被 SDK 權限授予覆寫 | 大樓保全優先於你的訪客證 |
| 5 | SDK 自動化需要修改程式碼時，推薦做法是什麼？ | 先用唯讀模式分析，再用明確權限授予修改 | 先驗屋再裝修 |
| 6 | 列舉三個 SDK 實際使用場景 | Git pre-commit hook（Secret 偵測）、CI/CD code review、自動化 dependency 更新 | 保全、品檢員、維修隊 |
| 7 | PM 為 SDK 功能撰寫需求時應指定什麼？ | 任務範圍、權限等級、觸發條件、輸出目的地、護欄、失敗處理 | 完整的工作指令清單 |
| 8 | SDK 權限和專案設定如何互動？ | 取交集 — SDK 授予能力，settings 定義邊界。Deny 規則永遠勝出。 | 同一扇門上的兩把鎖 |

---

## 練習題

### 問題 1：CI/CD Pipeline 場景

團隊希望 Claude Code 自動審查每個 PR 並發布留言。Review 應分析程式碼品質但絕不修改檔案。作為 PM，需求中哪個權限規格是正確的？

- A. 「授予完整存取權，讓 Claude 可以徹底審查程式碼」
- B. 「使用唯讀模式 — Claude 分析並產生 review 文字，不修改檔案」
- C. 「授予 Edit 權限，讓 Claude 可以修正 review 中發現的問題」
- D. 「授予 Bash 權限，讓 Claude 可以在 review 過程中執行測試套件」

<details><summary>答案與說明</summary>

**B** — 只發布留言的 code review 只需要讀取程式碼和產生文字。唯讀模式恰好提供此能力，且安全性最高。

- A 違反最小權限 — review 不需要寫入權限
- C 混淆了 review 和 auto-fix — 這應該是分開的功能，各有各的權限
- D 增加不必要的風險 — 跑測試和 code review 是不同的事

**PM 重點**：將「分析」功能（唯讀）和「修改」功能（寫入權限）分開。絕不將它們綁在同一個權限等級下。
</details>

### 問題 2：自動化安全場景

工程師提議一個 SDK 自動化，每週更新 dependency。腳本授予 `allowedTools: ["Edit", "Write", "Bash"]`。專案設定 deny `Bash(rm *)`。自動化會意外刪除檔案嗎？

- A. 會 — `allowedTools` 覆寫專案設定
- B. 不會 — 專案設定的 deny 規則始終優先於 SDK 授權
- C. 會 — 但只在 Claude 判斷刪除是必要的情況下
- D. 不會 — 有任何 deny 規則時 `Bash` 完全被停用

<details><summary>答案與說明</summary>

**B** — 專案設定作為 SDK 授權無法繞過的護欄。`Bash(rm *)` 的 deny 規則無論 `allowedTools` 指定什麼都會阻止檔案刪除。

- A 錯誤 — SDK 授權永遠無法覆寫 settings deny 規則
- C 錯誤 — Claude 無法透過推理繞過 deny 規則
- D 錯誤 — 只有特定 pattern 被封鎖，不是所有 Bash 用法

**PM 重點**：專案設定是你的安全網。撰寫需求時，同時指定 SDK 權限和專案設定的 deny 規則以實現縱深防禦。
</details>

### 問題 3：產品規劃場景

你正在規劃一個新功能：「AI 驅動的程式碼生成，從範本建立 boilerplate 檔案。」最小所需的 SDK 權限等級是什麼？

- A. 唯讀（預設）
- B. 僅 Edit
- C. Edit + Write
- D. Edit + Write + Bash

<details><summary>答案與說明</summary>

**C** — 建立新檔案的程式碼生成需要 Write 權限（建立新檔案）。如果生成也修改既有檔案（例如更新 index），還需要 Edit。檔案建立不需要 Bash。

- A 不足 — 唯讀模式無法建立檔案
- B 不足 — Edit 修改既有檔案但無法建立新檔案
- D 授予不必要的 Bash 存取權 — 檔案建立不需要 shell 指令

**PM 重點**：將每個功能動作對應到最小所需工具。「建立新檔案」= Write。「修改既有檔案」= Edit。「執行 shell 指令」= Bash。只授予所需的。
</details>
