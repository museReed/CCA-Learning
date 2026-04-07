# Useful Hooks — PM 視角

| 項目 | 內容 |
|------|------|
| 考試對應 | D3 — Claude Code Configuration & Workflows（佔 20%）、D1 — Agentic Architecture（佔 27%） |
| Task Statements | 1.5（Agent SDK hooks）、3.2（custom commands & hooks）、1.2（multi-agent coordinator-subagent patterns） |
| 課程來源 | claude-code-in-action / 05-hooks / Lesson 18 |

---

## TL;DR

本課介紹兩個解決實際 AI 開發問題的 hook：(1) **type-checking hook**，在 AI 修改程式碼後抓出連鎖錯誤；(2) **duplication prevention hook**，用第二個 AI instance 審查改動是否重複。對 PM 來說，關鍵洞察是：AI 工具有可預測的盲點，而 **hook 提供了 prompt 指示無法達成的確定性保障**。

---

## 為什麼 PM 需要知道這些

這兩個 hook 解決了 AI 輔助開發中的兩大常見失敗模式：

| 失敗模式 | 商業影響 | Hook 解決方案 |
|---------|---------|-------------|
| AI 改了函式但壞了其他檔案 | Bug 上了 production，開發者信任度下降 | Type-checking hook 自動抓錯 |
| AI 建了重複程式碼而非重用既有的 | 技術債累積，維護成本上升 | Duplication review hook 標記冗餘程式碼 |

**PM 重點**：撰寫 acceptance criteria 時，你需要明確指出哪些品質關卡是自動化的（hook）vs 哪些是 best-effort 的（prompt）。

---

## 心智模型：工廠品質管控

### Hook 1：生產線上的即時檢查員

想像工廠組裝線上，機器人修改了一個零件。生產線上的即時檢查員立刻確認這個修改有沒有導致下游組裝問題：

| 工廠 | AI 開發 |
|------|--------|
| 機器人修改零件 | Claude 修改 function signature |
| 檢查員確認下游零件是否還能組裝 | PostToolUse hook 跑 type checker |
| 零件不合？→ 送回返工 | 有 type errors？→ Claude 修正 |
| 不需要人工介入 | 不需要開發者介入 |

**重點**：檢查員在**每次修改後自動執行**——不是等有人想到才去檢查。

### Hook 2：獨立稽核員

再想像工廠有很多零件倉庫。當工人製作新零件時，獨立稽核員會檢查倉庫裡是否已經有類似的零件：

| 工廠 | AI 開發 |
|------|--------|
| 工人製作新零件 | Claude 寫新的 database query |
| 稽核員檢查現有庫存 | 第二個 Claude instance 審查既有 queries |
| 發現重複？→ 用現有零件 | 發現重複？→ 重用既有 query |
| 多花稽核時間，但減少浪費 | 多花 API 費用，但 codebase 更乾淨 |

> [!TIP]
> **PM 決策點**
>
> Duplication hook 每次編輯都要多花時間和錢。這是經典的 **品質 vs 速度 trade-off**，PM 必須評估。講師建議：只監控最關鍵的目錄——不要什麼都稽核。

---

## AI 失焦：PM 必須知道的現象

影片展示了一個關於 AI 能力限制的關鍵洞察：

| 任務類型 | AI 行為 | 結果 |
|---------|---------|------|
| 簡單聚焦：「印出 pending 訂單」 | Claude 找到並重用既有程式碼 | 正確 |
| 複雜多步驟：「建 Slack 整合，含訂單提醒」 | Claude 寫了全新的重複程式碼 | 錯誤 |

**為什麼 PM 要關心**：當你寫的 feature 需求涉及很多步驟，AI **更可能產生冗餘程式碼**。這不是 bug——這是 context 運作方式的可預測限制。Hook 補償了這個限制。

> [!IMPORTANT]
> **考試核心哲學**
>
> **Architecture > Prompt** — 結構性保障（hook）比指示性的（prompt）更可靠。
> **Independent review > Self-review** — 獨立審查者能抓到原始工作者遺漏的問題。

---

## 產品情境演練

### 情境：多團隊的電商平台

你是一個電商平台的 PM。後端有 50+ 個 SQL query 檔案橫跨多個領域（訂單、庫存、客戶、支付）。三個開發團隊每天都使用 Claude Code。

| 問題 | 沒有 Hook | 有 Hook |
|------|----------|--------|
| A 團隊新增「取得 pending 訂單」query | 跟 B 團隊的既有 query 重複 | 第二個 Claude instance 抓到 duplicate |
| 開發者修改 API response type | 其他 12 個檔案的 call site 靜默壞掉 | Type checker hook 立即抓到所有 12 個錯誤 |
| 複雜 feature 橫跨多個領域 | Claude 建立冗餘的工具函式 | Scoped review hook 標記既有替代方案 |

**PRD 影響**：你的 acceptance criteria 應該指明：
- 「所有 TypeScript 編輯必須觸發自動 type checking」（= PostToolUse hook）
- 「關鍵目錄的新 query 必須經過 duplicate 審查」（= duplication review hook）
- 這些**不是可選的開發者偏好**——它們是**必要的品質關卡**

> [!TIP]
> **PM 跟工程師溝通的框架**
>
> 不要說「Claude 應該檢查有沒有重複」（prompt-based，不可靠），而是說：「我們需要一個 PostToolUse hook，自動審查 queries 目錄的改動是否有 duplication。」這給工程師一個清晰的架構需求。

---

## PM 的 Trade-off 分析

| 因素 | Type-Checking Hook | Duplication Review Hook |
|------|-------------------|------------------------|
| 每次觸發的成本 | 低（~2-5 秒） | 高（~10-30 秒 + API 費用） |
| 覆蓋範圍 | 所有 TypeScript 檔案 | Scope 到關鍵目錄 |
| 誤報率 | 接近零（compiler 是 deterministic） | 低但可能有（AI 判斷） |
| 設定複雜度 | 簡單（一個指令） | 中等（需要 TypeScript SDK 整合） |
| **建議** | 所有專案都啟用 | 只在高價值目錄啟用 |

---

## 講師影片洞察

1. **任務複雜度會降低 AI 發現既有程式碼的能力** — 任務簡單時，Claude 會找到既有程式碼。任務複雜時，Claude 失焦並寫出 duplicate。這是一個**可預測的模式**，不是隨機 bug。
2. **Hook 可以使用 TypeScript SDK** — 這意味著 hook 可以程式化地啟動獨立的 Claude Code instance。這開啟了 hook 系統裡的 multi-agent review pattern。
3. **「It really comes down to trade-offs」** — 講師明確把這定位成 cost-benefit 決策，而不是普適的 best practice。PM 應該逐目錄評估。

---

## Anti-Patterns（考試常考）

| ❌ 錯誤做法 | ✅ 正確做法 | 為什麼 |
|-----------|-----------|--------|
| PRD 寫「AI 應該總是檢查 type」 | 要求用 PostToolUse hook 做 type checking | Prompt-based 需求有非零失敗率 |
| 假設 AI 會找到既有程式碼 | 實作自動化 duplication review | 複雜任務中 AI 會失焦——影片已示範 |
| 用 review hook 監控所有目錄 | 只 scope 到關鍵目錄 | 低價值目錄的成本大於收益 |
| 依賴 code review 抓 duplicate | 用 hook 作為第一道防線 | 人工 reviewer 也會漏；hook 是一致的 |

---

## 模擬考題

### 第一題：Developer Productivity 情境

你的工程團隊回報 Claude Code 修改共用 TypeScript 工具函式時，經常引入 type errors。這些錯誤在 code review 時才被發現，但那時開發者已經去做其他任務了。身為 PM，你應該在團隊的開發流程裡加入什麼需求？

- A. 在團隊的 CLAUDE.md 加上指示：「修改共用工具函式後，必須跑 type checker」
- B. 要求工程師在每次 Claude Code session 結束後手動跑 `tsc --noEmit`
- C. 實作一個 PostToolUse hook，在每次檔案編輯後自動跑 type checker
- D. 排程每日 batch type-check 任務，把累積的錯誤用 email 通知工程師

<details><summary>答案與解析</summary>

**C** — PostToolUse hook 提供即時、自動的回饋，開發者零負擔。Type errors 在同一個 Claude Code session 裡就被抓到並修正，開發者還沒離開就解決了。

- A 是 prompt 指示——Claude 可能會忽略，複雜任務時尤其嚴重
- B 增加手動開銷，開發者會忘記
- D 延遲了錯誤偵測好幾個小時，增加修正成本

**PM 重點**：目標是**在錯誤產生的當下就抓住**，而不是在下游。Hook 做得到；prompt 和手動流程做不到。
</details>

### 第二題：電商平台情境

你的電商平台有一個 `queries/` 目錄，裡面有 200+ 個 SQL 函式。使用 Claude Code 的工程師回報定期出現 duplicate queries。Duplication 在 Claude 被分配多步驟任務時最嚴重。什麼做法最能平衡品質與成本？

- A. 設定 PostToolUse hook，啟動另一個 Claude instance 審查整個專案的所有檔案改動
- B. 設定 PostToolUse hook，啟動另一個 Claude instance 只審查 `queries/` 目錄的改動
- C. 在 system prompt 加 few-shot examples，展示如何搜尋既有 queries
- D. 把所有 queries 合併到更少的檔案裡，增加 Claude 看到既有 query 的機會

<details><summary>答案與解析</summary>

**B** — 把 review hook scope 到只有 `queries/` 目錄，在品質（抓 duplicate）和成本（不對每個檔案編輯增加開銷）之間取得平衡。講師明確建議這個做法。

- A 太貴了——審查整個專案的每個檔案改動會大幅拖慢開發
- C 是 prompt-based，影片已經示範了這個失敗模式
- D 是差勁的軟體架構，會造成維護問題

**PM 重點**：品質關卡應該**針對高風險區域**，而不是普遍適用。這是「proportionate response」原則。
</details>

### 第三題：Multi-Agent 架構情境

產品團隊正在討論是否實作 query duplication hook。工程 lead 說它每次 query 檔案編輯會多花 15-20 秒。身為 PM，你應該如何框架這個決策？

- A. 拒絕 hook，因為它拖慢開發者
- B. 對所有目錄都啟用 hook 以最大化程式碼品質
- C. 評估 trade-off：只在 duplication 有高商業影響的關鍵目錄實作 hook
- D. 用每週程式碼 duplication 審計取代 hook

<details><summary>答案與解析</summary>

**C** — 這是 proportionate response。Hook 每次編輯都有成本，所以應該針對 duplication 影響最大的目錄（如支付 queries、訂單 queries）。低風險目錄（如測試工具）可能不值得這個開銷。

- A 忽視了已被證實的品質問題
- B 過度套用解決方案，造成不必要的開銷
- D 延遲偵測並增加修正成本

**PM 重點**：考試考的是 proportionate response。「總是」和「從不」的答案通常是錯的——適合情境的解決方案才是正確的。
</details>
