# Claude Code in Action — PM Perspective（繁體中文）

| 項目 | 內容 |
|------|------|
| 考試 Domain | D3 — Claude Code Configuration (20%) |
| Task Statements | 3.1（Claude Code 指令）、3.3（CLAUDE.md memory）、1.2（agentic workflow patterns） |
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 75 |

---

## 一句話總結

Claude Code 的真實價值，只有在團隊採用「context → plan → implement」workflow 並共享 `CLAUDE.md` 後才能解鎖 —— 這是 PM 必須主導的產品/流程決策，不是留給開發者各自為政的工程選項。

---

## 心智模型：新夥伴的第一天

把 Claude Code 進專案當成新工程師入職：

| 入職步驟 | 人類工程師 | Claude Code |
|---------|-----------|-------------|
| Codebase 導覽 | 讀 README + 問問題 | `/init` 掃描並寫 `CLAUDE.md` |
| 團隊慣例小抄 | 寫在 wiki | `CLAUDE.md`（project scope） |
| 個人筆記偏好 | 寫在自己的筆記本 | `CLAUDE.md`（local scope） |
| 通用工作風格 | 靠職涯養成 | `CLAUDE.md`（user scope） |
| 我們怎麼幹活 | 「先規劃再寫 code」 | context → plan → implement workflow |

新工程師沒 context 會寫幾週 mediocre code，Claude Code 沒 `CLAUDE.md` 也一樣。Memory file 不是選配功能，它就是入職文件。

---

## 為什麼這 lesson 對 PM 重要

大多數團隊裝了 Claude Code 卻用錯 —— 把它當 autocomplete 而不是 agent。本 lesson 是這個產品的 workflow 契約：照做得到 10x 價值，略過則只是漂亮一點的 search-and-replace。

PM 的任務：

1. **把 `/init` + `CLAUDE.md` 立為團隊規範** —— 不是建議。
2. **把三步 workflow 寫進團隊文件** —— context → plan → implement。
3. **定義哪些東西放進 project-scope CLAUDE.md** —— 不是所有偏好，只放共享的。
4. **把 CLAUDE.md 當成產品產物** —— 像 spec 一樣 review、像 spec 一樣更新。

---

## 產品使用情境

### 配合正確 workflow 時 Claude Code 最發光

| 情境 | 為什麼合適 |
|------|-----------|
| 在既有 codebase 上加新功能 | Context-first 流程避免 agent 重新發明你的 pattern |
| 在有完整 test 的情況下重構 | TDD 變體大發神威 —— test 就是成功標準 |
| 新工程師 ramp up 老專案 | `CLAUDE.md` 把 tribal knowledge 裝好 |
| 跨團隊協作 | Project `CLAUDE.md` 把慣例帶給每一個貢獻者 |

### 單靠 Claude Code 不夠的情境

| 情境 | 要搭配什麼 |
|------|-----------|
| 需要生產環境即時資料 | 加 MCP server（lesson 76） |
| 需要 UI 設計決策 | 還是要 product spec |
| 需要合規核准 | 人類 review in the loop |
| 需要跨 repo 知識 | `CLAUDE.md` user scope + 紀律 |

---

## CLAUDE.md 的三種 Scope（PM 視角）

這是 lesson 中最與產品相關的概念：

| Scope | 擁有者 | 該放什麼 | 不該放什麼 |
|-------|-------|---------|-----------|
| **Project** | Team lead / PM | Build 指令、團隊慣例、架構規則 | 個人快捷鍵、機器特定設定 |
| **Local** | 個別工程師 | 個人快捷鍵、工作筆記、實驗 flag | 團隊共享慣例、別人要遵守的規則 |
| **User** | 個別工程師 | 通用工作風格（「先說明再改」） | 專案特定 pattern |

PM 應該把 project-scope `CLAUDE.md` 當一等公民 deliverable —— 在 code review 時 review、在重大架構變更時更新、在 PR 描述中引用。

---

## PM 決策框架

要把 Claude Code rollout 給團隊時，回答：

1. **誰擁有 project `CLAUDE.md`？** 必須有人 curate。通常是 tech lead 或 PM。
2. **裡面放什麼？** 從 build 指令、code style、測試要求、架構概覽開始。
3. **`CLAUDE.md` 的改動怎麼 review？** 跟引發改動的 code 放同一個 PR。
4. **如何強制「先計畫」workflow？** 團隊共識、PR template、或內部工具。
5. **量什麼指標？** 新工程師 time-to-first-working-PR；PR 中包含「Plan:」段落的比例。

---

## Workflow 作為產品標準

「context → plan → implement」pattern 不是 Claude Code 的特殊怪癖 —— 而是現代 agent UX pattern。其他 agent 工具（Cursor、Windsurf、自製產品）都收斂到同一形狀。PM 層級：

| Workflow 步驟 | 可要求的產品產物 |
|--------------|----------------|
| Context | 檔案清單、相關文件、過去的 PR |
| Plan | PR 裡在 code 之前貼出的書面計畫 |
| Implement | 實際的 PR |

標準化後，code review 更快、onboarding 更便宜、品質下限上升 —— 同時消耗的 senior engineering 時數變少。

---

## 常見 PM 錯誤

1. **把 `CLAUDE.md` 當選配** —— 沒它，每場新 session 都得重學專案。複利優勢全沒。
2. **讓工程師把所有東西塞 user-scope** —— 共享慣例必須放 project scope，否則團隊受惠不到。
3. **為了「省時間」跳過 plan 步驟** —— 省了分鐘卻浪費小時修方向錯誤的實作。
4. **沒把 `CLAUDE.md` 列入 code review checklist** —— 它是活文件，過時條目會產出壞結果。
5. **混淆 `/clear` 與 `/init`** —— 教學入門經典錯誤。文件裡要清楚告訴團隊何時用哪個。

> **關鍵洞察**
>
> Claude Code 是 **團隊協定**，不只是開發者工具。PM 真正的 deliverable 不是「我們裝好了」，而是「我們有共用的 `CLAUDE.md`、我們遵守 context → plan → implement、我們 review agent memory 的改動像 review code 一樣」。做到的團隊拿到 agent 優勢；沒做到的沒有。

---

## CCA 考試重點

- **D3（Claude Code Configuration）**：直接考 `/init`、`/clear`、`#`、`CLAUDE.md` scope 的題目機率很高。
- **D1（Agentic Coding & Architecture）**：context → plan → implement workflow 就是 agent 的標準 pattern。
- 預期會出情境題：「某團隊裝了 Claude Code 但產能沒提升 —— 缺了什麼？」答案通常是 `CLAUDE.md` + workflow。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| PM 應該強制的三步 Claude Code workflow 是什麼？ | 1) 讀相關檔案餵 context、2) 要求書面計畫不寫 code、3) 請 Claude 實作計畫 |
| `CLAUDE.md` 的三種 scope 與各自擁有者是什麼？ | Project（團隊/PM 擁有、進 git）、Local（個別工程師、不進 git）、User（個別工程師、跨所有專案） |
| 為什麼 PM 該把 project-scope `CLAUDE.md` 當一等 deliverable？ | 它是所有未來 Claude Code session 繼承的入職文件、風格指南、架構摘要 —— 過時內容會產出壞結果 |
| `/init` 做什麼？何時該跑？ | 掃描 codebase 並把總結寫入 `CLAUDE.md`；專案起始時跑一次，重大架構改動後重跑 |
| `#` 快捷鍵做什麼？ | 附加筆記到 `CLAUDE.md` 並詢問 project、local 或 user scope |
| Claude Code 的 TDD 變體 workflow 是什麼？ | 餵 context → 請 Claude 發想 test cases → 實作 test → 寫 code 直到全綠 |
| PM rollout Claude Code 的頭號錯誤？ | 把 `CLAUDE.md` 當選配 —— 這會消除持久專案記憶的複利優勢 |
| 怎麼量化團隊是否遵守「plan first」規則？ | PR 中在 code diff 前包含書面計畫的比例 |
