# Controlling Context — PM 視角


![Context Window As Resource Analogy](../../visuals/context-window-as-resource-analogy-zh-TW.svg)
*圖：Context Window 是有限資源 — 類比。*


![Context Control Tools Decision Tree](../../visuals/context-control-tools-decision-tree-zh-TW.svg)
*圖：選擇上下文控制工具的決策樹。*

| 項目 | 內容 |
|------|------|
| 考試對應 | D5 — Reliability & Performance（15%）、D3 — Claude Code Configuration & Workflows（20%） |
| Task Statements | 5.1 ★★★（context preservation）、5.4 ★★（large codebase context）、3.5 ★★（iterative refinement） |
| 課程來源 | claude-code-in-action / 03-context-and-commands / Lesson 10 |

---

## TL;DR

Claude Code 有一個有限的「工作記憶」（context window）。就像開太久的會議一樣，對話累積噪音，Claude 會失去專注。四種工具管理這件事：**Escape**（中斷）、**雙擊 Escape**（倒帶）、**`/compact`**（摘要後繼續）、**`/clear`**（全新開始）。PM 需要了解這些，因為 context 管理直接影響開發者生產力和 AI 輸出品質 — 這影響衝刺速度和產品時程。

---

## 為什麼 PM 需要知道這些

你不需要自己管理 context，但你需要理解：

1. **「再問一次 Claude」不是免費的** — 每次互動都消耗 tokens 和 context 空間
2. **為什麼長 coding session 會產出更差的結果** — context pollution 是真實的工程限制
3. **如何設定合理的期望** — 2 小時的 Claude session 不是線性生產力

這些知識幫你規劃衝刺、估算工作量，以及和工程團隊溝通 AI 輔助開發的事。

---

## 心智模型：會議室白板

| 工具 | 白板類比 | 什麼時候用 |
|------|---------|-----------|
| **Escape** | 「等等，停下來 — 讓我釐清一下」 | 有人往錯誤方向走 |
| **雙擊 Escape** | 擦掉最後 3 個項目，從一個好的點重新開始 | 題外話帶偏了會議 |
| **`/compact`** | 拍一張白板照片，擦掉白板，把照片貼成小參考 | 白板滿了但洞察很寶貴 |
| **`/clear`** | 把白板完全擦乾淨換新主題 | 切換到完全不同的會議議程 |

> 💡 **PM 決策框架**
>
> 問自己：「AI 還需要它之前學到的東西嗎，還是要開始一個不相關的事？」
> - 需要先前知識 → **`/compact`**
> - 乾淨的開始更好 → **`/clear`**

---

## 產品情境演練

### 情境：AI 輔助開發的衝刺規劃

你的工程團隊每天用 Claude Code。一位資深工程師回報：「Claude 前 20 分鐘很好用，然後開始犯奇怪的錯。」以下是發生了什麼以及你可以建議什麼：

| 症狀 | 根本原因 | 建議 |
|------|---------|------|
| Claude 重複已修好的 bug | debug 噪音填滿了 context window | 子任務之間用 `/compact` |
| Claude 忘記專案慣例 | 早期的指令掉出了 context | 把慣例存為 memories 或放在 CLAUDE.md |
| Claude 修改錯誤的檔案 | 前一個任務的不相關 context | 切換 feature 時用 `/clear` |
| Claude 的輸出品質隨時間下降 | Context window 被低訊號內容塞滿 | 訓練團隊主動使用 Escape + 倒帶 |

> 🎯 **PM 重點**
>
> Context 管理是一項**開發者技能**，應該納入團隊的 AI 工具入職訓練。主動管理 context 的團隊，從 AI coding assistant 得到的結果明顯更好。

---

## 四種工具 — PM 需要知道的

### Escape — 「停下來重新導向」

當 Claude 往錯誤方向走時，開發者按 Escape 中途停止它。這節省 tokens 也防止壞的輸出污染 context。

**PM 相關性**：這就是為什麼「Claude 跑偏了 10 分鐘」是訓練問題，不是 Claude 的問題。開發者應該及早中斷。

### 雙擊 Escape — 「回到前幾步」

按兩次 Escape 讓開發者把對話倒帶到任何之前的訊息。那個點之後的一切都被丟棄。

**PM 相關性**：這等同於「讓我們回到可行的地方，試另一個方法」。保留有用的 context 同時移除失敗的嘗試。

### `/compact` — 「摘要後繼續」

把整個對話壓縮成摘要。Claude 保留它學到的東西，但以壓縮的形式。

**PM 相關性**：這是讓長 session 能保持生產力的工具。沒有它，session 在 20-30 分鐘後就會退化。有了它，開發者可以維持數小時的高效 AI session。

### `/clear` — 「全新開始」

清除所有東西。Claude 從零 context 開始。

**PM 相關性**：切換不相關任務時必備。使用一個 feature 的殘留 context 去做另一個 feature，會造成交叉污染。

---

## 影片洞察

影片示範中 PM 應注意的要點：

1. **Context 管理是主動的，不是被動的** — 講師在 Claude 出問題_之前_就用這些工具，不是之後。這是團隊應該採用的最佳實踐。
2. **Escape + Memory 組合** — 當 Claude 重複犯錯時，講師按 Escape 然後儲存 memory。這是永久修正，不是單次 session 的變通方案。鼓勵你的團隊隨時間累積 memories。
3. **「對話控制快捷鍵看起來只是方便，但它們真的能改善 Claude 有效工作的能力」** — 講師的原話。這些不是可有可無的；它們是必要的工作流程工具。

---

## 模擬考題

### 第一題：Developer Productivity 情境

你的團隊已經用 Claude Code 兩個月了。回顧會上，工程師們反映 Claude 做小任務很好，但在較長的 feature 實作 session（1 小時以上）中表現掙扎。幾位工程師提到 Claude 會「忘記」之前的決定並開始自相矛盾。什麼團隊層級的建議能改善這個情況？

- A. 切換到 context window 更大的模型
- B. 訓練團隊在子任務間用 `/compact`，切換 feature 時用 `/clear`
- C. 限制 Claude Code session 最多 15 分鐘
- D. 把所有專案文件加到 CLAUDE.md 讓 Claude 永遠不會忘

<details><summary>答案與解析</summary>

**B** — 根本原因是長 session 中的 context pollution。教會團隊正確的 context 管理工具才是解決實際問題的方法。這是 Task 5.1（context preservation）的考試重點概念。

- A 可能有幫助但沒有解決 context pollution 的根本問題 — 更大的 window 還是會被噪音填滿
- C 太限制了，降低生產力
- D 會讓 CLAUDE.md 太大，本身就消耗 context window 空間

**PM 重點**：Context 管理是可學習的技能。把它納入你團隊的 AI 工具入職訓練。
</details>

### 第二題：Code Generation 情境

一位開發者已經和 Claude 花了 25 分鐘建構一個複雜的資料 pipeline。Claude 現在理解了 schema、轉換規則和錯誤處理 patterns。開發者需要新增一個轉換步驟，但 context window 快滿了。他該怎麼做？

- A. 用 `/clear` 重新解釋整個 pipeline
- B. 用 `/compact` 壓縮 session，然後新增轉換步驟
- C. 開新的 Claude Code session 然後貼上 pipeline 程式碼
- D. 不做 context 管理繼續下去

<details><summary>答案與解析</summary>

**B** — `/compact` 保留 Claude 對 pipeline 架構的理解，同時釋放 context 空間。累積的知識（schema、轉換 patterns、錯誤處理）正是值得保留的那種 context。

- A 浪費了 25 分鐘的累積理解
- C 失去 context 而且需要手動重新解釋
- D 有 context 溢出的風險，Claude 會丟失關鍵的早期資訊

**PM 重點**：當開發者說「我必須重新跟 Claude 解釋所有事」，問他有沒有先試過 `/compact`。
</details>
