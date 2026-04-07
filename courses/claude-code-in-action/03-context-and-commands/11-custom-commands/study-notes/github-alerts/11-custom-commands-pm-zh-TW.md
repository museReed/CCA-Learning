# Custom Commands — PM 視角


![Custom Commands Scope Architecture](../../visuals/custom-commands-scope-architecture-zh-TW.svg)
*圖：自訂指令範圍 — 專案 vs 使用者層級。*


![Custom Command Mechanism](../../visuals/custom-command-mechanism-zh-TW.svg)
*圖：自訂指令 — Markdown 檔案變成 Slash Command。*

| 項目 | 內容 |
|------|------|
| 考試對應 | D3 — Claude Code Configuration & Workflows（佔 20%） |
| Task Statements | 3.2 ★★★（custom commands & skills）、3.1 ★★（CLAUDE.md config） |
| 課程來源 | claude-code-in-action / 03-context-and-commands / Lesson 11 |

---

## TL;DR

Custom commands 是你的工程團隊可以建立和共享的可重複工作流程模板。不讓每個開發者為常見任務各寫各的 prompt，團隊在 `.claude/commands/` 裡定義一次 command，所有人用同樣的方式使用。PM 應該關注這件事，因為這就是你在團隊中標準化 AI 輔助工作流程的方式 — 減少不一致和新人上手摩擦。

---

## 為什麼 PM 需要知道這些

1. **一致性** — 當每個開發者都用 `/audit` 而不是各自版本的「檢查我的 dependencies」，輸出是可預測的
2. **新人上手** — 新的團隊成員可以打 `/` 看到所有可用的工作流程，不用讀文件
3. **流程編碼化** — 你的團隊最佳實踐變成可執行的，不只是被文件記錄
4. **可發現性** — Commands commit 到 repo 後，整個團隊都看得到

---

## 心智模型：團隊劇本

把 custom commands 想成**團隊劇本** — 一套共享的標準作業程序。

| 沒有 Commands | 有 Commands |
|-------------|-----------|
| 「我們團隊怎麼 audit dependencies？」— 問資深開發者 | 打 `/audit` — 每個人走同一個流程 |
| 「我們寫測試的慣例是什麼？」— 讀文件 | 打 `/write_tests src/auth.ts` — 慣例已內建 |
| 每個開發者的輸出略有不同 | 團隊間標準化的輸出 |
| 知識在人的腦子裡 | 知識在 codebase 裡 |

> [!TIP]
> **PM 重點**
>
> Custom commands 就是把部落知識變成共享基礎設施的方式。如果你聽到「只有 Alice 知道怎麼做 X」，那個工作流程就應該變成一個 command。

---

## 它怎麼運作（非技術摘要）

1. 開發者在專案的 `.claude/commands/` 資料夾裡建立一個 markdown 檔案
2. 檔名變成一個 slash command（例如 `audit.md` → `/audit`）
3. 檔案包含給 Claude 的指示 — 檢查什麼、做什麼、怎麼回應
4. 特殊的 placeholder `$ARGUMENTS` 讓使用者在執行 command 時傳入特定細節
5. 檔案被 commit 到 repo，所以整個團隊都能用

**範例**：`/write_tests src/auth.ts` 告訴 Claude：「按照我們專案的測試 patterns 為 `src/auth.ts` 寫測試。」

---

## 產品情境演練

### 情境：在快速成長的團隊中標準化程式碼品質

你的團隊兩個月內從 3 人成長到 8 人。你注意到：
- Code review 的評論很重複（「你忘了加測試」、「import pattern 不對」）
- 新工程師要一週才能學會專案慣例
- AI 產出的程式碼品質在開發者之間差異很大

| 問題 | Command 解決方案 | 影響 |
|------|----------------|------|
| 不一致的測試 patterns | `/write_tests $ARGUMENTS` — 編碼測試慣例 | 所有 AI 產出的測試走同一個結構 |
| 忘記做 dependency audit | `/audit` — 跑完整的 audit + fix + test 循環 | 一鍵合規檢查 |
| 品質不一的 code review | `/review $ARGUMENTS` — 標準化的 review checklist | 一致的 review 輸出 |
| 新人上手慢 | 新開發者打 `/` 就能看到所有團隊工作流程 | 自助式可發現性 |

> [!IMPORTANT]
> **PM 重點**
>
> 規劃 AI 輔助開發工作流程時，問工程團隊：「哪些重複性任務應該變成 custom commands？」這是低成本、高影響的改善。

---

## Commands vs 其他設定

PM 常搞混什麼時候用哪個工具。以下是實用的區分：

| 工具 | 類比 | PM 什麼時候該要求 |
|------|------|-----------------|
| **Custom Commands** | SOP 劇本 | 「每個開發者都應該用同一個流程做 X」 |
| **CLAUDE.md** | 給 Claude 的專案 README | 「Claude 應該永遠知道我們專案的 Y」 |
| **Hooks** | 自動合規檢查 | 「Z 絕對不能發生 — 我們需要保證」 |
| **Memories** | 個人便利貼 | 個人偏好 — PM 不管這個 |

---

## 影片洞察

1. **Commands 是 markdown 檔案** — 不需要寫程式。PM 可以起草 command 模板然後交給工程團隊審查。
2. **`$ARGUMENTS` 接受任何文字** — 不只是檔案路徑。你可以建立 `/estimate $ARGUMENTS`，其中引數是 feature 描述。
3. **需要重啟** — 新增 commands 後，Claude Code 必須重啟。在工作流程文件中要注意這點。

---

## 模擬考題

### 第一題：Developer Productivity 情境

你的工程團隊用 Claude Code，但每個開發者為常見任務寫自己的 prompt。這導致程式碼品質不一致。作為 PM，哪個建議對標準化最有影響？

- A. 寫詳細的 CLAUDE.md 指示涵蓋每個工作流程
- B. 在 `.claude/commands/` 裡為最常見的工作流程建立一組 custom commands，並 commit 到 repo
- C. 發一封團隊 email 附上每個工作流程的建議 prompt
- D. 設定 hooks 來強制程式碼品質標準

<details><summary>答案與解析</summary>

**B** — Custom commands 把團隊工作流程編碼到專案結構中，讓它們可發現、一致、可版本控制。它們特別針對「每個開發者寫自己的 prompt」這個問題。

- A 是用來放持久性專案知識的，不是按需觸發的工作流程
- C 是手動的，隨時間會偏離，因為人們會修改 prompts
- D 是用來做 deterministic 強制執行的，不是工作流程標準化

> [!IMPORTANT]
> **PM 重點**：當你想要每個人走同一個流程時，Commands 是對的工具。當你需要保證時，Hooks 是對的工具。

</details>

### 第二題：Code Generation 情境


![Claude Code Configuration Hierarchy](../../visuals/claude-code-configuration-hierarchy-zh-TW.svg)
*圖：Claude Code 設定階層。*

一位新工程師加入你的團隊，問「我怎麼知道有哪些 AI 工作流程可用？」Custom commands 的哪個特性解決了這個問題？

- A. Custom commands 會自動記錄在 CLAUDE.md 裡
- B. 在 Claude Code 裡打 `/` 會列出所有可用的 commands，包括團隊定義的 custom commands
- C. Custom commands 建立時會發通知
- D. Custom commands 只有建立它的開發者才能用

<details><summary>答案與解析</summary>

**B** — Custom commands 出現在 `/` 指令選單裡，跟內建指令並列。這讓團隊工作流程自動文件化，不用讀外部文件就能發現。

- A 不是自動的 — CLAUDE.md 是獨立的檔案
- C 不是 commands 的功能
- D 不正確 — `.claude/commands/` 裡的專案範圍 commands 所有團隊成員都能用

> [!IMPORTANT]
> **PM 重點**：可發現性是 custom commands 相較於共享文件或部落知識的關鍵優勢。

</details>
