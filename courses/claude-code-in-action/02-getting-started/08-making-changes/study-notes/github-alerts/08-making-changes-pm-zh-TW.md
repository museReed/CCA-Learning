# Making Changes — PM 觀點

| 項目 | 細節 |
|------|---------|
| 考試涵蓋 | D1 — Agentic Coding Fundamentals (22%), D3 — Effective Claude Code Usage (30%) |
| Task Statements | 3.4 ★★★ (plan mode vs direct), 3.5 ★★★ (iterative refinement), 1.1 ★ (agentic loops) |
| 考試情境 | S2 (Code Gen), S4 (Developer Productivity) |
| 課程來源 | claude-code-in-action / 02-getting-started / Lesson 08（影片 + 文字） |

---


![Thinking Modes Token Spectrum](../../visuals/thinking-modes-token-spectrum-zh-TW.svg)
*圖：Thinking Mode 頻譜 — 從 standard 到 ultrathink。*


![Planning Mode Execution Flow](../../visuals/planning-mode-execution-flow-zh-TW.svg)
*圖：Plan Mode 執行流程 — 探索、規劃、審查、執行。*


![Plan Mode Flow](../../visuals/plan-mode-flow-zh-TW.svg)
*圖：三種模式對應不同複雜度。*

## TL;DR

Claude Code 有兩個超越基本聊天的強大功能：Planning Mode（用於複雜多檔案任務）和 Thinking Modes（用於困難問題的深度推理）。PM 應理解這些，因為它們影響開發者生產力、token 成本，以及可以可靠自動化的任務類型。迭代改進工作流 — 提問、實作、審核、回饋、改進 — 是團隊日常實際使用 Claude Code 的方式。

---

## 為什麼 PM 必須理解這個

1. **生產力估算** — 知道開發者何時該用 Planning Mode vs 直接執行，有助於估算任務完成時間
2. **成本管理** — Planning Mode 和 Thinking Modes 都增加 token 消耗；PM 需要理解品質與成本的取捨
3. **任務範圍界定** — 理解 Planning Mode 能處理什麼，有助於為 AI 輔助開發適當界定 ticket 範圍
4. **視覺溝通** — 基於截圖的工作流改變了設計師和 PM 如何向使用 Claude Code 的開發者溝通變更

---

## 商業類比

| 概念 | 商業類比 |
|---------|-----------------|
| 直接執行 | 在 Slack 上快速傳訊修一個 typo — 不需要開會 |
| Planning Mode | 多週 sprint 前的專案啟動會議 — 建造前先對齊範圍 |
| Thinking modes | 給策略團隊額外一週深入分析複雜的市場決策 |
| 迭代改進 | 設計衝刺 — 展示原型、獲取利害關係人回饋、迭代、上線 |
| 截圖輸入 | 設計師的標註 mockup — 「改這個特定按鈕」並用紅圈圈起來 |

---

## 決策框架：哪個模式用於哪種任務？

| 任務類型 | 建議模式 | Token 成本 | 開發者時間 |
|-----------|-----------------|------------|---------------|
| 修 typo、加 log 語句 | 直接執行 | 低 | 幾分鐘 |
| 實作新 API endpoint | 直接或 Planning | 中 | 10-30 分鐘 |
| 跨 10 個檔案重構驗證 | Planning Mode | 高 | 30-60 分鐘 |
| 設計最佳快取演算法 | Thinking Mode (ultrathink) | 高 | 15-30 分鐘 |
| 跨多模組的全端功能 | Planning + Thinking | 最高 | 1-2 小時 |

> [!NOTE] **講師影片洞察**
>
> 講師提到「兩個功能都消耗額外 token，所以有成本考量。」這是關鍵的 PM 洞察：更強大的模式在複雜任務上產生更好的結果，但成本更高。目標是適當使用 — 讓工具匹配任務。

---

## 情境演練：與 Claude Code 的 Sprint 規劃

你的團隊正在規劃包含不同複雜度任務的 sprint：

| Ticket | 複雜度 | 建議 Claude Code 模式 | 理由 |
|--------|-----------|------------------------------|-----------|
| 修正設定頁面按鈕顏色 | 低 | 直接執行 | 單一檔案，明確的變更 |
| 為整個應用加入深色模式 | 高（廣度） | Planning Mode | 觸及 CSS、元件、多檔案的狀態管理 |
| 優化資料庫查詢效能 | 高（深度） | Thinking Mode (ultrathink) | 需要深入分析查詢模式和索引策略 |
| 從零開始建立新的帳務模組 | 高（兩者） | Planning Mode + Thinking | 新架構（廣度）配合複雜的商業邏輯（深度） |

> [!TIP] **PM 決策規則**
>
> 估算使用 Claude Code 的 sprint 速度時，簡單任務從直接執行獲得 2-3 倍加速。複雜任務從 Planning Mode 獲得 1.5-2 倍加速但消耗更多 token。將此納入成本預測。

---

## PM 的迭代改進循環

這是你會看到開發者每天使用的工作流：

```
PM 提供需求
        │
        ▼
開發者詢問 Claude ──→ Claude 實作 ──→ 開發者審核
        ▲                                    │
        │                                    ▼
        └─── 開發者提供回饋 ◄── 需要變更？
             （截圖 + 描述）           │
                                      ▼（否）
                                  提交 / PR
```

**這對 PM 意味著什麼：**
- 回饋循環更快（分鐘級，不是天級）
- 視覺回饋（截圖）現在是一等公民的溝通方式
- PM 可以透過提供期望 UI 狀態的截圖來參與
- 更多迭代 = 更好的結果，但每次迭代都有 token 成本

---

## 練習題

### Q1：Sprint 速度估算

你的工程團隊正在採用 Claude Code。CTO 要你估算對 sprint 速度的影響。根據本課內容，哪個答案最有見地？

- A. 所有任務都會快 3 倍完成
- B. 簡單任務透過直接執行獲得顯著加速；複雜多檔案任務透過 Planning Mode 獲得適度加速但 token 成本更高；淨效果取決於任務組合
- C. 不會有可衡量的影響因為開發者仍需審核程式碼
- D. Claude Code 只幫助新功能，不幫助 bug fix

<details><summary>答案</summary>

**B** — 適當的回應。不同模式有不同的速度/成本特性。簡單任務獲得最大的相對加速。複雜任務從 Planning Mode 獲得品質提升但消耗更多 token。Sprint 的淨影響取決於任務類型的組合。

**PM 重點**：不要承諾統一的加速。分析你的 sprint 任務組合，根據複雜度估算每個任務的影響。
</details>

### Q2：成本優化

你團隊這個月的 Claude Code token 使用量翻倍了。調查發現開發者對大多數任務都使用 "ultrathink"。適當的 PM 回應是什麼？

- A. 完全禁止 ultrathink 以降低成本
- B. 建立指南：將 ultrathink 保留給複雜推理任務，簡單變更用直接執行，多檔案工作用 Planning Mode
- C. 接受更高的成本作為更好品質的代價
- D. 要求開發者少用 Claude Code

<details><summary>答案</summary>

**B** — 這是適當的回應。問題不是 ultrathink 本身而是不加區分的使用。建立讓模式匹配任務複雜度的使用指南同時優化品質和成本。

**PM 重點**：Token 成本優化是關於讓正確的模式匹配正確的任務，而不是限制強大的功能。建立開發者可以參考的簡單決策矩陣。
</details>

### Q3：設計-開發工作流

你的設計團隊想用 Claude Code 加速 UI 實作。他們問：「我們可以直接發截圖給開發者讓 Claude 來實作嗎？」根據本課內容，正確答案是什麼？

- A. 不行，Claude Code 不支援圖片輸入
- B. 可以，開發者可以用 Ctrl+V 直接貼截圖到 Claude Code，Claude 可以用視覺 context 來實作或修改 UI 元素
- C. 只有先將截圖轉換成文字描述才行
- D. 截圖只能用來識別 bug，不能用來實作新設計

<details><summary>答案</summary>

**B** — 課程明確教授基於截圖的溝通作為主要輸入方式。設計師可以提供標註截圖，開發者貼到 Claude Code，Claude 用多模態理解來實作變更。

**PM 重點**：這改變了設計到開發的交接流程。設計師可以視覺化溝通變更，減少 UI 修改對詳細書面規格的需求。考慮更新團隊工作流來利用這一點。
</details>
