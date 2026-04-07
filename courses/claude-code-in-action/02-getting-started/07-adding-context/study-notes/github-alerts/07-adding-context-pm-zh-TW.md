# Adding Context — PM 觀點

| 項目 | 細節 |
|------|---------|
| 考試涵蓋 | D3 — Effective Claude Code Usage (30%), D5 — Performance Optimization (12%) |
| Task Statements | 3.1 ★★★ (CLAUDE.md hierarchy), 5.1 ★★ (context preservation), 5.4 ★★ (large codebase context) |
| 考試情境 | S2 (Code Gen), S4 (Developer Productivity) |
| 課程來源 | claude-code-in-action / 02-getting-started / Lesson 07（影片 + 文字） |

---

## TL;DR

Claude Code 透過三層設定檔系統（CLAUDE.md）管理專案 context。`/init` 透過分析程式碼庫生成初始檔案。三個層級 — global（所有專案）、project（透過 repo 共享）和 local（個人覆寫）。`@` 語法讓開發者將 Claude 指向特定檔案。對 PM 來說：這是團隊如何在組織中標準化 AI 輔助開發，以及如何管理 context window 預算。

---

## 為什麼 PM 必須理解這個

1. **團隊標準化** — CLAUDE.md commit 到版本控制代表每個開發者得到相同的 AI 行為。這是你維持程式碼品質一致性的槓桿。
2. **加速入職** — `/init` + CLAUDE.md 代表新團隊成員的 AI 助手從第一天就了解專案架構。
3. **效能調校** — CLAUDE.md 中太多 context 會降低效能。當團隊回報「Claude 很慢」時，PM 應理解這個取捨。
4. **安全考量** — CLAUDE.local.md 不會 commit 到版本控制，適合放個人 API key 或實驗性指令。

---

## 商業類比

| 概念 | 商業類比 |
|---------|-----------------|
| CLAUDE.md hierarchy | 公司政策層級：企業政策（global）< 部門政策（project）< 個人例外（local）。越具體覆寫越一般。 |
| `/init` 指令 | 員工入職 — 閱讀所有文件、理解組織、總結關鍵流程 |
| CLAUDE.md 中的 `@` file mention | 例行會議議程項目 — 總是在桌上，總是被討論 |
| 互動式 `@` mention | 臨時會議主題 — 只在相關時提出 |
| `#` memory 指令 | 更新團隊 wiki — 跨人員變動持續存在的知識 |

---

## 情境演練：將 Claude Code 推廣到 20 人團隊


![Claude Md Hierarchy Priority Stack](../../visuals/claude-md-hierarchy-priority-stack-zh-TW.svg)
*圖：CLAUDE.md 階層 — local 覆蓋 project 覆蓋 global。*

| 階段 | 動作 | CLAUDE.md 槓桿 |
|-------|--------|-----------------|
| 1. 初始設定 | 技術主管在主 repo 上執行 `/init` | 生成包含專案架構的基線 CLAUDE.md |
| 2. 標準化 | 技術主管將編碼標準、PR 慣例、測試要求加入 CLAUDE.md | 所有開發者透過版本控制繼承相同規則 |
| 3. 個人化 | 個別開發者建立 CLAUDE.local.md 放個人偏好 | 個人風格不影響團隊標準 |
| 4. 優化 | 團隊在監控 context 使用後移除低價值的 `@` 引用 | 更好的效能，更低的 token 成本 |

> [!NOTE] **講師影片洞察**
>
> 講師展示 CLAUDE.md「被包含在每個請求中」— 使其本質上是持久化的 system prompt。對 PM 來說，這代表 CLAUDE.md 是控制團隊 AI 行為最具影響力的單一設定。

---

## 決策框架：什麼放哪裡？

| 內容類型 | 放在哪裡 | 原因 |
|-------------|----------------|-----|
| 專案架構、建置指令 | `./CLAUDE.md`（project） | 每個開發者都需要；版本控制 |
| 編碼標準、PR 慣例 | `./CLAUDE.md`（project） | 團隊一致性；變更在 git 中追蹤 |
| 個人編碼風格偏好 | `~/.claude/CLAUDE.md`（global） | 適用於你所有專案；不共享 |
| 實驗性指令、個人 API key | `./CLAUDE.local.md`（local） | 每專案覆寫；不 commit |
| Schema 檔案、API 契約 | `./CLAUDE.md` 中的 `@` 引用 | 大多數請求需要的橫切 context |
| 任務特定的檔案 | 聊天中的互動式 `@` | 一次性 context；不浪費 context window |

> [!TIP] **PM 決策規則**
>
> 如果影響整個團隊，放在專案 CLAUDE.md。如果是個人的，放在 local 或 global。不確定時問自己：「新團隊成員需要這個嗎？」如果是，放專案 CLAUDE.md。

---

## Context Window 預算問題


![Context Window Budget Allocation](../../visuals/context-window-budget-allocation-zh-TW.svg)
*圖：Context Window 預算分配。*

PM 應理解這個取捨，因為它影響效能和成本：

| CLAUDE.md 中更多 context | CLAUDE.md 中更少 context |
|--------------------------|--------------------------|
| Claude 始終知道專案細節 | Claude 可能每次需要重新發現檔案 |
| 每次請求更高的 token 消耗 | 每次請求更低的 token 消耗 |
| 回應品質降低的風險 | 聚焦 context 帶來更好的推理 |
| 對重複問題更快 | 首次探索略慢 |

甜蜜點：只將**橫切的、經常需要的**檔案放在 CLAUDE.md `@` 引用中。讓 Claude 透過工具發現其他一切。

---

## 練習題

### Q1：組織推廣

你的 CTO 問：「我們如何確保所有 50 名使用 Claude Code 的開發者遵循我們的編碼標準？」哪個方法正確？

- A. 發 email 請每個開發者設定他們的 Claude Code 設定
- B. 將編碼標準加入專案 CLAUDE.md 並 commit 到 repository
- C. 建立 CLAUDE.local.md 模板並請每個開發者複製
- D. 使用 Anthropic 儀表板設定組織級的 Claude Code 規則

<details><summary>答案</summary>

**B** — 專案 CLAUDE.md commit 到版本控制，自動套用到所有 clone repo 的開發者。這是架構解決方案 — 不需要每個開發者手動設定，不會隨時間產生偏差。

**PM 重點**：CLAUDE.md 是你的政策執行機制。把它當成團隊級設定檔，不是個人設定檔。
</details>

### Q2：效能抱怨

一位開發者回報：「Claude Code 以前很快但現在很慢，答案也變差了。」調查發現他們上週在 CLAUDE.md 中加了 12 個 `@` 檔案引用。你建議什麼？

- A. 請他們升級到更高的 API 層級以取得更多 context window
- B. 審核 `@` 引用，將非必要的移到互動式 `@` mention；只在 CLAUDE.md 中保留橫切檔案
- C. 叫他們完全刪除 CLAUDE.md 重新開始
- D. 建議他們改用更簡單的專案結構

<details><summary>答案</summary>

**B** — 課程明確教導太多 context 降低效能。適當的回應是審核和優化，而不是刪除所有東西或用錢砸問題。

**PM 重點**：Context window 是有限資源。把 CLAUDE.md 中的 `@` 引用當成資料庫索引 — 每個都有維護成本，所以只保留提供橫切價值的。
</details>

### Q3：新人入職

一位新開發者加入你的團隊。他們從未使用過 Claude Code。在你的專案上進行高效 AI 輔助開發的最快路徑是什麼？

- A. 給他們 2 小時的 Claude prompt engineering 培訓
- B. 讓他們安裝 Claude Code、pull repo（包含 CLAUDE.md），然後開始工作 — CLAUDE.md 自動提供專案 context
- C. 請他們執行 `/init` 生成全新的 CLAUDE.md
- D. 分享你的個人 CLAUDE.local.md 給他們

<details><summary>答案</summary>

**B** — 如果團隊已經 commit 維護良好的 CLAUDE.md 到 repo，新開發者自動繼承所有專案 context。基本使用不需要培訓。

**PM 重點**：維護良好的 CLAUDE.md 是入職加速器。就像從第一天就讓每位新人都能使用資深工程師的大腦。
</details>
