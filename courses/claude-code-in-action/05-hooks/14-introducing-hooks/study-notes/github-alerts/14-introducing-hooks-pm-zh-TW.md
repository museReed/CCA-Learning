# Introducing Hooks — PM Perspective

| 項目 | 內容 |
|------|------|
| 考試對應 | D3 — Claude Code Configuration & Workflows（佔 20%） |
| Task Statements | 3.2（custom commands & hooks）、1.5（Agent SDK hooks） |
| 課程來源 | claude-code-in-action / 05-hooks / Lesson 14 |

---

## TL;DR


![Tool Execution Pipeline](../../visuals/tool-execution-pipeline-zh-TW.svg)
*圖：Claude Code 如何處理工具呼叫 — 模型提出請求，系統透過 Hook 攔截，再執行。*

Hooks 是 Claude Code 的「品管關卡」和「自動化觸發器」。把它想成產品裡的 business rule engine：在 AI 行動之前可以攔截審核（Pre），行動之後可以觸發品質檢查（Post）。PM 需要理解這個機制，因為它決定了「哪些 AI 行為是可以被保證的」vs「哪些只是盡力而為」。

---

## Why PMs Need to Understand Hooks

作為 PM，你不需要自己寫 hook，但你需要知道：

1. **什麼行為可以被 100% 保證** — Hook 能做到的事
2. **什麼行為只能盡力而為** — Prompt instruction 能做到的事
3. **怎麼跟工程師溝通需求** — 知道什麼時候該要求用 hook

這直接影響你寫 PRD 時的 acceptance criteria 和 risk assessment。

---

## Mental Model: 機場安檢 vs 機上廣播

| | PreToolUse Hook | PostToolUse Hook | Prompt Instruction |
|--|----------------|-----------------|-------------------|
| 類比 | 機場安檢 — 不符合就不能登機 | 落地後海關 — 已入境但可補驗 | 機上廣播「請繫安全帶」 |
| 保證程度 | **100% 確定**會執行 | **100% 確定**會執行 | 95-99%（AI 可能忽略） |
| 能阻止嗎？ | 可以阻止行動 | 不能（已發生），但可以善後 | 不能保證 |
| 適用場景 | 合規、安全、權限控制 | 品質檢查、格式化、通知 | 風格偏好、語氣建議 |

> [!IMPORTANT]
> **考試核心哲學（PM 必記）**
>
> - **Architecture > Prompt** — 能用結構解決的，不要靠提示
> - **Deterministic > Probabilistic** — 能用程式保證的，不要靠 AI 自覺

---

## Product Scenario Walkthrough

### Scenario: Customer Support Agent

你在規劃一個 AI 客服系統，需求如下：

| 需求 | 實現方式 | 為什麼 |
|------|----------|--------|
| 退款 > $500 必須人工審核 | **PreToolUse hook** — 攔截 `process_refund`，金額超標就 block 並轉人工 | 合規需求，不能有任何漏網之魚 |
| 回覆語氣要友善 | **Prompt instruction** | 偏好性需求，偶爾偏差可接受 |
| 每次回覆後記錄到 CRM | **PostToolUse hook** — 回覆完自動寫入 | 流程自動化，保證每次都執行 |
| 優先推薦自助方案 | **Prompt instruction** | 策略偏好，有彈性空間 |

> [!TIP]
> **PM 決策框架**
>
> 寫 PRD 時問自己——「如果 AI 在這個行為上 100 次有 1 次出錯，後果是什麼？」
> - 後果嚴重（財務損失、合規違規）→ **必須用 hook**
> - 後果輕微（語氣稍差、格式不一致）→ **prompt instruction 足夠**

---

## Configuration: 誰控制什麼

Hooks 有三層設定，這對 PM 來說很重要，因為它決定了**團隊治理**：

| 層級 | 誰管 | 典型用途 | PM 關心的 |
|------|------|----------|-----------|
| Global (`~/.claude/settings.json`) | 個人開發者 | 個人偏好（自動 format） | 不可控，每人不同 |
| Project shared (`.claude/settings.json`) | Tech Lead / 團隊 | 團隊標準（lint、測試） | **可以要求團隊統一** |
| Project local (`.claude/settings.local.json`) | 個人 | 個人覆寫 | 無法強制 |

> [!TIP]
> **PM Takeaway**
>
> 如果你的 acceptance criteria 需要某個 hook 生效，確保它在 **Project shared** 層級，不是靠個人設定。

---

## Hooks in the Bigger Picture

Hooks 在考試中跨多個 Domain 出現：

| Domain | Hooks 怎麼考 |
|--------|-------------|
| **D1 Agentic Architecture (27%)** | Agent SDK 的 hook 機制 — PostToolUse 做 data normalization、PreToolUse 做 policy enforcement |
| **D3 Claude Code Config (20%)** | Settings hierarchy、`/hooks` command、matcher syntax |
| **D5 Reliability (15%)** | Hook 作為 validation gate，確保 pipeline step 之間的品質 |

---

## Instructor Insights（影片補充）

講師影片中有幾個 PM 該注意的 nuance：

1. **Hook 拿到完整的 tool call details** — 不只是 "Claude 想寫檔案"，而是 "Claude 想用 Write tool 寫 `/src/auth.ts`，內容是..."。這意味著 hook 可以做非常精細的判斷
2. **PostToolUse 的 feedback loop** — Claude 收到 hook 的回饋後會自動修正。這不需要人工介入，是 **self-healing** 的設計
3. **講師原話："Wrapping your head around hooks can be really challenging"** — 如果你的工程師需要時間理解這個概念，這是正常的

---

## Practice Questions

### 第一題：Customer Support 情境

你的 AI 客服 agent 處理退貨和退款。公司政策規定：任何財務操作前必須驗證身份。目前這個規則是透過 system prompt 指示來 enforce。有客戶回報收到退款時沒有被要求驗證身份。建議的修正方式是什麼？

- A. 加強 system prompt，用更強硬的語氣要求驗證
- B. 加入 few-shot examples 示範正確的驗證流程
- C. 實作 PreToolUse hook，在 `get_customer` 回傳已驗證狀態前，block `process_refund`
- D. 加入 PostToolUse hook，在退款處理後檢查是否有做身份驗證

<details><summary>答案與解析</summary>

**C** — 財務操作前的身份驗證是合規需求。Prompt-based 方案（A、B）有非零失敗率——客戶回報已經證明了這點。PostToolUse（D）太遲——退款已經處理完。PreToolUse hook 的 prerequisite gate 是 deterministic 的。

> [!IMPORTANT]
> 考試哲學：**Deterministic > Probabilistic**、**Validation > Trust**

**PM 重點**：這就是為什麼 PRD 裡寫 "must verify identity" 不夠——你需要指定 enforcement mechanism 是 hook 而非 prompt。
</details>

### 第二題：Code Review CI 情境

你的團隊把 Claude Code 整合到 CI pipeline 做自動化 PR review。工程師反映 Claude 有時候會修改 migration 檔案，導致部署問題。你會建議什麼？

- A. 在 CLAUDE.md 加上「不要修改 migration 檔案」
- B. 設定 PreToolUse hook，block 對 `migrations/` 目錄的 Write/Edit 操作
- C. 設定 PostToolUse hook，在 Claude 修改 migration 檔案後 revert 變更
- D. 建立一個獨立的 review pipeline，排除 migration 檔案不給 Claude 看

<details><summary>答案與解析</summary>

**B** — PreToolUse hook 在問題發生前 deterministic 地阻止。A 是 prompt-based（對嚴重後果的場景不可靠）。C 是事後補救，增加複雜度。D 移除了有價值的 context，Claude 可能需要這些來 review migration 相關的 code。

**PM 重點**：「有時候會」（sometimes）= 你需要 deterministic solution。語氣偶爾不夠友善 → prompt 就夠；會改到 migration 導致 deployment issue → 嚴重後果 → 用 hook。
</details>

### 第三題：Multi-Agent Research 情境

一個 coordinator agent 將研究任務分派給多個 subagent。不同的 backend API 回傳不同格式的日期（Unix timestamp、ISO 8601、locale-specific string）。synthesis subagent 經常誤解日期。最佳方案是什麼？

- A. 在 synthesis subagent 的 prompt 裡加入日期格式說明
- B. 在每個 backend tool 上實作 PostToolUse hook，在 agent 處理結果前把日期統一轉成 ISO 8601
- C. 讓 coordinator agent 在傳給 synthesis subagent 前先轉換日期
- D. 用 few-shot examples 示範不同的日期格式

<details><summary>答案與解析</summary>

**B** — PostToolUse hooks 在 tool boundary 做 data normalization，是最可靠且可維護的方案。A 和 D 是 probabilistic。C 增加了 coordinator 的複雜度，且要求它理解所有可能的日期格式。

> [!IMPORTANT]
> 考試哲學：**Architecture > Prompt**、**Deterministic > Probabilistic**

**PM 重點**：Data normalization 是 infra 層面的問題，不應該靠 AI 「理解」不同格式。就像你做 data pipeline 時不會靠前端自己轉日期格式一樣。
</details>
