# Making Changes — 工程深度筆記

| 項目 | 細節 |
|------|--------|
| 考試領域 | D1 — Agentic Coding Fundamentals (22%), D3 — Effective Claude Code Usage (30%) |
| Task Statements | 3.4 ★★★ (plan mode vs direct), 3.5 ★★★ (iterative refinement), 1.1 ★ (agentic loops) |
| 考試情境 | S2 (Code Gen), S4 (Developer Productivity) |
| 來源 | claude-code-in-action / 02-getting-started / Lesson 08（影片 + 文字） |

---

## 一句話總結

Claude Code 提供三種操作模式應對不同複雜度：直接執行用於簡單變更，Planning Mode 用於複雜的多檔案重構，Thinking Modes 用於模糊問題的深度推理。

---

## 截圖溝通

告訴 Claude 要改什麼最精確的方式是展示給它看：

1. **截取螢幕截圖** — 你想修改的 UI 元素
2. **用 Ctrl+V 貼上**（macOS 上不是 Cmd+V）到 Claude Code 聊天中
3. **描述你想要的變更** — 相對於截圖

> [!NOTE] **講師影片洞察**
>
> 講師示範貼上 uigen 應用的截圖並請 Claude 修改 UI。他特別強調用 Ctrl+V — 「是 Ctrl+V，不是 Cmd+V」— 因為這是 Claude Code 用於圖片貼上的快捷鍵。

這是**多模態輸入** — Claude 同時處理圖片和文字指令來理解變更。截圖消除了關於你指的是哪個元素的歧義。

---

## Planning Mode（Task 3.4 ★★★）


![Planning Mode Execution Flow](../../visuals/planning-mode-execution-flow-zh-TW.svg)
*圖：Plan Mode 執行流程 — 探索、規劃、審查、執行。*


![Plan Mode Flow](../../visuals/plan-mode-flow-zh-TW.svg)
*圖：三種模式對應不同複雜度。*

Planning Mode 是 Claude Code 處理複雜、多檔案變更的機制。它將**規劃**與**執行**分離。

### 如何啟用

按 `Shift+Tab` 兩次（如果已經自動接受編輯則按一次）：

```
一般模式：  提問 → Claude 立即執行
Plan Mode：提問 → Claude 規劃 → 你審核 → Claude 執行
```

### Planning Mode 做什麼

1. **讀取更多檔案** — Claude 更廣泛地探索你的程式碼庫
2. **建立詳細計畫** — 展示它打算做什麼
3. **等待核准** — 你在任何變更前審核並可以重新導向
4. **執行計畫** — 只在你確認後

```
┌──────────┐    ┌─────────────────┐    ┌──────────────┐
│ 你提問   │───→│ Claude 探索     │───→│ Claude 規劃  │
└──────────┘    │（讀取檔案、     │    │（逐步        │
                │  搜尋程式碼）   │    │  行動清單）   │
                └─────────────────┘    └──────┬───────┘
                                              │
                                              ▼
                                       ┌──────────────┐
                                       │ 你審核       │
                                       │ 計畫         │
                                       └──────┬───────┘
                                              │
                                    ┌─────────┴─────────┐
                                    ▼                   ▼
                              ┌──────────┐        ┌──────────┐
                              │ 核准     │        │ 重新導向 │
                              │ → 執行   │        │ → 重新規劃│
                              └──────────┘        └──────────┘
```

> [!TIP] **關鍵洞察**
>
> Planning Mode 不只是「較慢的執行」。它是根本不同的工作流，在行動前蒐集更多 context。規劃階段的額外檔案讀取通常能捕捉到直接執行會遺漏的相依性和邊界情況。

### 何時使用 Planning Mode

| 使用 Planning Mode | 使用直接執行 |
|-------------------|---------------------|
| 多檔案重構 | 單檔案編輯 |
| 架構變更 | 簡單 bug fix |
| 跨模組的新功能實作 | 新增一個 CSS class |
| 不確定範圍的任務 | 確切知道要改什麼 |
| 不熟悉的程式碼庫 | 充分理解的程式碼 |

---

## Thinking Modes（Extended Thinking）


![Thinking Modes Token Spectrum](../../visuals/thinking-modes-token-spectrum-zh-TW.svg)
*圖：Thinking Mode 頻譜 — 從 standard 到 ultrathink。*

Thinking modes 在回應前給 Claude 更多 token 進行內部推理。這與 Planning Mode 是正交的 — 它們解決不同的問題。

### 頻譜

| 模式 | 推理深度 | 最適合 |
|------|----------------|----------|
| （預設） | 標準 | 多數任務 |
| "Think" | 基本延伸 | 中等複雜度 |
| "Think more" | 延伸 | 複雜邏輯 |
| "Think a lot" | 全面 | 多步演算法 |
| "Think longer" | 延長時間 | 深度分析 |
| "Ultrathink" | 最大化 | 最困難的問題、模糊需求 |

每個級別逐步給 Claude 更多 token 進行內部推理。

> [!NOTE] **講師影片洞察**
>
> 講師解釋 thinking modes 給 Claude「更多 token 來推理問題」。他將 ultrathink 定位為最大推理能力，在 Claude 掙扎於特別複雜或模糊的任務時很有用。他也提到成本取捨：「兩個功能都消耗額外的 token。」

---

## Planning Mode vs Thinking Mode（關鍵考試區別）

這是考試最重要的區別之一：

| 維度 | Planning Mode | Thinking Mode |
|-----------|--------------|---------------|
| **做什麼** | 讀取更多檔案，建立行動計畫 | 更深度地推理問題 |
| **複雜度類型** | 廣度 — 多檔案、多元件 | 深度 — 複雜邏輯、模糊需求 |
| **輸出** | 你在執行前審核的計畫 | 更徹底推理的回應 |
| **啟動** | Shift+Tab（切換） | 在 prompt 中加關鍵字（"think"、"ultrathink"） |
| **使用者互動** | 審核-核准循環 | 不需要額外互動 |
| **成本驅動** | 更多檔案讀取（tool call） | 更多推理 token |

```
複雜度矩陣：
                        低推理            高推理
                        複雜度            複雜度
                    ┌─────────────────┬─────────────────┐
低程式碼庫           │   直接           │   Think /       │
複雜度              │   執行           │   Ultrathink    │
                    ├─────────────────┼─────────────────┤
高程式碼庫           │   Planning       │   Planning +    │
複雜度              │   Mode           │   Thinking Mode │
                    └─────────────────┴─────────────────┘
```

> [!TIP] **關鍵洞察**
>
> 你可以組合兩種模式。對於需要理解多個檔案（廣度）又要解決複雜演算法（深度）的任務，使用 Planning Mode 加上 "think" 或 "ultrathink" 關鍵字。這讓 Claude 同時獲得廣泛 context 和深度推理。

---

## 迭代改進工作流（Task 3.5 ★★★）

完整的迭代工作流結合所有三種技術：

1. **初始請求** — 描述你想要的（文字 + 選用截圖）
2. **Claude 實作** — 直接執行或透過 Planning Mode
3. **你審核** — 在瀏覽器/IDE 中檢查結果
4. **提供回饋** — 結果截圖 + 描述要改什麼
5. **Claude 改進** — 基於你的回饋迭代
6. **重複** 直到滿意

> [!WARNING] **成本考量**
>
> Planning Mode 和 Thinking Modes 都消耗額外 token。Planning Mode 讀取更多檔案（tool call token）。Thinking modes 使用更多推理 token。在任務複雜度足以證明成本合理時使用，不要作為每個請求的預設。

---

## 熟悉的類比

| 概念 | 類比 | 為何合適 |
|---------|---------|-------------|
| 直接執行 | 請資深工程師修一個 typo — 直接做 | 簡單任務，不需要規劃 |
| Planning Mode | Sprint 前的架構審核 — 先規劃再建造 | 複雜任務需要前期探索 |
| Thinking modes | 給考試題目額外時間 | 更多時間 = 困難問題更好的推理 |
| Ultrathink | 困難設計問題的白板 session | 最大推理資源應對最大複雜度 |
| 截圖輸入 | 指著特定按鈕說「改這個」 | 視覺溝通消除歧義 |

---

## 考試重點

| 考試概念 | 本課教了什麼 |
|-------------|-------------------------|
| **Plan mode vs direct (3.4) ★★★** | Planning Mode 用於多檔案/複雜任務；直接用於簡單編輯。Planning 讀取更多檔案並建立可審核的計畫。 |
| **Iterative refinement (3.5) ★★★** | 提問 → 實作 → 審核 → 回饋 → 改進循環。截圖加速溝通。 |
| **Agentic loops (1.1) ★** | 迭代改進就是實踐中的 agentic loop — 蒐集 context、規劃、行動、評估、重複。 |

關鍵考試區別：

- **Planning Mode vs Thinking Mode** — 廣度 vs 深度。Planning 讀更多檔案；thinking 推理更深。它們是互補的，不是替代的。
- **Extended thinking 不是 prompt 技巧** — 它是分配更多推理 token 的架構功能。考試哲學「Architecture > Prompt」適用。

> [!IMPORTANT] **考試筆記**
>
> 當考試呈現「複雜多檔案重構」情境時，答案幾乎總是涉及 Planning Mode。當情境涉及「模糊需求」或「複雜演算法」時，答案涉及 Thinking Modes。兩者同時出現時，組合使用。

---

## 練習題

### Q1：模式選擇

一位開發者需要重新命名一個在 Node.js monorepo 中被 15 個檔案引用的資料庫欄位。哪種方法最合適？

- A. 直接執行 — 直接請 Claude 重新命名
- B. Planning Mode — 讓 Claude 探索程式碼庫、識別所有引用，並在變更前建立計畫
- C. Ultrathink — 請 Claude 深度推理這個重新命名
- D. 為每個需要變更的檔案開一個新的 Claude session

<details><summary>答案</summary>

**B** — 這是經典的 Planning Mode 情境：影響多個檔案的變更需要先廣泛探索程式碼庫。Planning Mode 會讀取相關檔案、識別所有引用，並呈現全面的計畫。

- A 有遺漏某些檔案引用的風險
- C 解決了錯誤的問題 — 這需要廣度（多檔案），不是深度（複雜推理）
- D 違背了 agentic coding 助手的目的

考試哲學：**Architecture > Prompt** — Planning Mode 是處理多檔案複雜度的結構方法。
</details>

### Q2：組合模式

一位開發者被指派設計新的快取策略，涉及修改資料存取層、API 路由和設定系統。最佳快取演算法取決於程式碼庫中的特定存取模式。哪種方法最好？

- A. 直接執行配上詳細的 prompt
- B. 只用 Planning Mode — 它會找出演算法
- C. 只用 Ultrathink — 它會找出檔案變更
- D. Planning Mode + ultrathink — Planning Mode 用於廣泛的程式碼庫理解，ultrathink 用於推理最佳快取演算法

<details><summary>答案</summary>

**D** — 此任務同時具有廣度複雜度（跨程式碼庫的多個元件）和深度複雜度（選擇最佳快取演算法）。組合 Planning Mode 和 thinking mode 同時處理兩個維度。

考試哲學：**Proportionate response** — 對特定的複雜度配置使用正確的工具組合。
</details>

### Q3：成本效益使用

一位初級開發者開始對每個請求都使用 "ultrathink"，包括簡單任務如「新增一個 console.log 語句」。他們的 token 使用量增加了 5 倍。你給什麼建議？

- A. Ultrathink 是免費的，讓他們繼續
- B. 將 thinking modes 保留給真正有複雜度的任務 — 模糊需求、複雜演算法或困難除錯。簡單任務不會從額外推理 token 中受益。
- C. 他們應該改用 Planning Mode 而不是 ultrathink
- D. 他們永遠不應該用 ultrathink — 它是實驗性的

<details><summary>答案</summary>

**B** — Thinking modes 消耗額外 token。對於加 log 語句這種簡單任務，標準執行就夠了。Ultrathink 是給真正困難的問題 — 更多推理時間能產生更好結果的場景。

考試哲學：**Proportionate response** — 讓工具的力量匹配任務的複雜度。不要用大砲打蚊子。
</details>

---

## 反模式

| 反模式 | 為何失敗 | 更好的方法 |
|-------------|-------------|-----------------|
| 每個任務都用 Planning Mode | 簡單變更浪費 token；不必要地更慢 | 簡單、範圍明確的變更用直接執行 |
| 瑣碎任務用 ultrathink | 燒推理 token 卻無益處 | 將 thinking modes 保留給真正複雜的問題 |
| 從不用 Planning Mode | 多檔案變更中遺漏相依性 | 範圍不明確或跨多檔案時啟用 Planning Mode |
| 只用文字描述 UI 變更 | 有歧義 — 「左邊的按鈕」可以指很多東西 | 貼截圖並指向特定元素 |
| 跳過 Planning Mode 的審核步驟 | 失去意義；可能執行有缺陷的計畫 | 核准執行前永遠審核計畫 |
| 用 Cmd+V 而不是 Ctrl+V 貼截圖 | 圖片不會貼入 Claude Code | 截圖貼上專用 Ctrl+V |
