# Project Setup — PM 觀點

| 項目 | 細節 |
|------|---------|
| 考試涵蓋 | D2 — Tool Design & MCP Integration (18%), D3 — Effective Claude Code Usage (30%) |
| Task Statements | 2.5 (built-in tools — awareness), 3.5 (iterative refinement — intro) |
| 課程來源 | claude-code-in-action / 02-getting-started / Lesson 06（純文字課程） |

---


![Iterative Refinement Cycle](../../visuals/iterative-refinement-cycle-zh-TW.svg)
*圖：迭代精煉循環 — 請求、建構、檢視、回饋。*

## TL;DR

課程使用一個小型 Node.js 應用，透過 Claude API 生成 UI 元件。PM 應理解：(1) 該專案展示 Claude Code 如何與真實程式碼庫協作，(2) API key 是選用的 — 表示工具在沒有外部 API 存取時也能運作，(3) 它引入的迭代式 generate-review-refine 工作流，是團隊實際使用 Claude Code 的方式。

---

## 為什麼 PM 該關注

1. **產品 demo 素養** — 理解示範專案有助於跟上課程，並向利害關係人溝通 Claude Code 的功能
2. **迭代工作流介紹** — generate-review-refine 循環是工程團隊採用 Claude Code 的方式；這是你會推銷的生產力故事
3. **API key 可選性** — 展示優雅降級，一個值得注意的產品設計模式

---

## 商業類比

| 概念 | 商業類比 |
|---------|-----------------|
| 含可選 API 的示範專案 | 像 freemium SaaS — 核心功能無需付費即可使用，進階功能需要 key |
| `npm run setup` 一次性初始化 | 像企業工具的入職設定 — 執行一次，然後開始工作 |
| 迭代式 UI 生成 | 像設計衝刺 — 展示原型、獲取回饋、改進、重複 |

---

## 情境演練：向利害關係人解釋 Claude Code

你的工程副總問：「Claude Code 實際上對我們的程式碼做什麼？」

以示範專案為參考：

| 步驟 | 發生什麼 | 商業影響 |
|------|-------------|----------------|
| 1. 開發者請 Claude 建立功能 | Claude 讀取專案結構和相關檔案 | 無需預先索引；第一天就能在任何程式碼庫上工作 |
| 2. Claude 生成實作 | 程式碼直接寫入專案檔案 | 不需要從另一個聊天視窗複製貼上 |
| 3. 開發者在瀏覽器中查看 | 應用程式立即反映變更 | 回饋循環是秒級，不是小時級 |
| 4. 開發者提供改進回饋 | Claude 迭代改進實作 | 透過對話收斂到正確的解決方案 |

---

## 練習題

### 情境：ROI 評估

你的財務長問團隊是否需要為每個開發者準備 Anthropic API key 才能使用 Claude Code。根據本課內容，正確答案是什麼？

- A. 是 — Claude Code 需要 API key 才能運作
- B. 否 — Claude Code 本身不需要 Anthropic API key；示範專案選擇性使用一個來驅動自己的功能
- C. API key 只在首次設定時需要，之後可以移除
- D. 一個共用的 API key 對整個團隊就夠了

<details><summary>答案</summary>

**B** — Claude Code 透過自己的機制進行驗證（Lesson 05）。本課的 Anthropic API key 是給示範專案的 UI 生成功能用的，不是給 Claude Code 本身用的。示範專案在沒有它的情況下使用靜態備用資料正常運作。

**PM 重點**：不要將示範專案的 API key 與 Claude Code 的驗證混為一談。這是兩個不同的系統。Claude Code 的成本是透過自己的訂閱/使用模式，而不是專案 `.env` 檔案中的 API key。
</details>
