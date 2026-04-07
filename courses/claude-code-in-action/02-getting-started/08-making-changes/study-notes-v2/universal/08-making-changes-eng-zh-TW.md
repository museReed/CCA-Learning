# Making Changes — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows |
| Task Statements | 3.4 (plan mode vs direct), 3.5 (iterative refinement) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> 本節所有內容均直接來自官方課程教材。

## One-Liner / TL;DR

Claude Code 提供三種操作模式應對不同複雜度：截圖視覺溝通實現精確 UI 修改、Planning Mode 進行廣泛的多檔案探索、Thinking Modes 進行深度推理——每種都會消耗更多 token。

## Core Concepts

### 截圖精確溝通

溝通 UI 變更最有效的方式是直接讓 Claude 看到你看到的畫面：

1. 截取你想修改的元素的截圖
2. 在 Claude Code 聊天中使用 **Ctrl+V** 貼上（macOS 上不是 Cmd+V）
3. 描述你想對截圖中元素做的修改

Claude 同時處理圖片和文字指令（多模態輸入），精確理解要修改哪個元素以及如何修改。這消除了純文字描述如「左側面板的佔位文字」的模糊性。

### Planning Mode

Planning Mode 將規劃與執行分離，讓 Claude 在行動前先探索你的程式碼庫。

**啟用方式：** 按 **Shift+Tab 兩次**（若已在自動接受模式則按一次）。

在 Planning Mode 中，Claude 會：

1. **讀取更多檔案** — 更廣泛地探索程式碼庫以理解全貌
2. **建立詳細的實作計畫** — 明確展示它打算做什麼
3. **展示預計的操作** — 呈現計畫供你審查
4. **等待你的核准** — 在執行任何變更前給你機會審查和調整方向

這與直接執行有根本性的不同。規劃階段的額外檔案讀取通常能捕捉到直接執行會遺漏的依賴關係和邊界情況。

### Thinking Modes

Thinking Modes 讓 Claude 在回應前有漸進式更多的 token 用於內部推理。在你的提示中包含關鍵字：

| 模式 | 推理深度 | 最適用場景 |
|------|---------|-----------|
| "Think" | 基礎延伸 | 中等複雜度 |
| "Think more" | 延伸 | 複雜邏輯 |
| "Think a lot" | 全面 | 多步驟演算法 |
| "Think longer" | 延長時間 | 深度分析 |
| "Ultrathink" | 最大化 | 最困難的問題、模糊的需求 |

每個等級讓 Claude 在回應前有漸進式更多的 token 進行更深入的分析。

### Planning vs Thinking — 廣度 vs 深度

這兩個功能解決不同的問題，且可以組合使用：

| 維度 | Planning Mode | Thinking Mode |
|------|--------------|---------------|
| **作用** | 讀取更多檔案，建立行動計畫 | 對問題進行更深入的推理 |
| **複雜度類型** | 廣度——多個檔案、多個元件 | 深度——複雜邏輯、模糊需求 |
| **啟動方式** | Shift+Tab 兩次（切換） | 提示中的關鍵字（"think"、"ultrathink"） |
| **使用者互動** | 審查-核准循環 | 不需要額外互動 |
| **成本驅動** | 更多檔案讀取（工具呼叫） | 更多推理 token |

**何時使用 Planning Mode：** 需要廣泛理解程式碼庫、多步驟實作、跨多個檔案的變更、不熟悉的程式碼庫。

**何時使用 Thinking Mode：** 複雜邏輯、困難的除錯、演算法挑戰、模糊的需求。

**組合使用：** 對於同時需要廣度（多檔案）和深度（複雜推理）的任務，啟用 Planning Mode 並在提示中加入 "ultrathink"。兩者都會消耗額外 token——按比例使用。

### Git 整合

Claude Code 也是一個優秀的 Git 助手。完成修改後，你可以請 Claude 暫存和提交，並附上描述性的訊息——在不離開終端的情況下串接開發到提交的工作流程。

## Demo Walkthrough: Screenshot Paste — 置中佔位文字

| 步驟 | 發生了什麼 | 畫面 |
|------|-----------|------|
| 1. 啟動開發伺服器 | 講師執行 `npm run dev` 並在 localhost:3000 開啟應用程式 | ![frame_003](../../visual-guide/frames/frame_003.jpg) |
| 2. 發現問題 | 佔位文字位於左側面板但未置中 | ![frame_006](../../visual-guide/frames/frame_006.jpg) |
| 3. 截圖 + 貼上 | 截取佔位文字的截圖，用 Ctrl+V 貼到 Claude Code | ![frame_009](../../visual-guide/frames/frame_009.jpg) |
| 4. 結果 | Claude 搜尋程式碼庫、更新樣式——佔位文字已置中 | ![frame_012](../../visual-guide/frames/frame_012.jpg) |

**關鍵重點：** 一張截圖加上一句指令就足以讓 Claude 找到正確的檔案並修復樣式。不需要描述是哪個元件、哪個 CSS 檔案或哪個 class 名稱。

## Demo Walkthrough: Plan Mode + Thinking — 複雜功能實作

| 步驟 | 發生了什麼 | 畫面 |
|------|-----------|------|
| 1. 發現問題 | 生成 card 元件後，講師注意到 "String Replace Editor"——顯示給使用者的技術工具名稱 | ![frame_018](../../visual-guide/frames/frame_018.jpg) |
| 2. 截圖記錄問題 | 截取技術文字的截圖並貼到 Claude Code | ![frame_027](../../visual-guide/frames/frame_027.jpg) |
| 3. 啟用 Plan Mode | 按 Shift+Tab 兩次啟用 Planning Mode——Claude 會在行動前先研究和規劃 | ![frame_035](../../visual-guide/frames/frame_035.jpg) |
| 4. 加入 ultrathink | 加入 "ultrathink" 以獲得最大推理深度；說明廣度（規劃）vs 深度（思考） | ![frame_049](../../visual-guide/frames/frame_049.jpg) |
| 5. 組合執行 | Plan Mode + ultrathink 同時運作——Claude 廣泛探索程式碼庫同時進行深度推理 | ![frame_054](../../visual-guide/frames/frame_054.jpg) |
| 6. 功能完成 | 技術工具名稱被替換為使用者友善的訊息：「Creating file:」和「Editing file:」 | ![frame_069](../../visual-guide/frames/frame_069.jpg) |
| 7. 驗證 | 後續編輯確認功能正常——顯示「Editing app.jsx」而非工具名稱 | ![frame_075](../../visual-guide/frames/frame_075.jpg) |

**關鍵重點：** 這個複雜任務涉及多個檔案，需要理解渲染管道。Planning Mode 找到所有相關檔案；ultrathink 推理出映射邏輯。組合使用大約花了兩分鐘完成一個需要大量手動調查的功能。

## Instructor Tips

- 貼上截圖時專門使用 **Ctrl+V**——macOS 上的 Cmd+V 在 Claude Code 中不起作用
- Planning Mode 不只是「較慢的執行」——它是一個根本不同的工作流程，會收集更多脈絡
- 當你不確定範圍時，從 Planning Mode 開始；對於理解清楚的修改回到直接執行
- Ultrathink 是最高推理等級——在 Claude 處理複雜或模糊任務時使用
- Planning Mode 和 Thinking Modes 都會花費額外 token——依任務複雜度按比例使用
- Claude Code 也兼任 Git 助手——完成修改後用它來暫存和提交

## Key Takeaways

1. 截圖消除模糊性——用 Ctrl+V 讓 Claude 看到你看到的畫面
2. Planning Mode（Shift+Tab 兩次）= 廣度——Claude 讀取更多檔案並在行動前建立計畫
3. Thinking Modes（think / think more / think a lot / think longer / ultrathink）= 深度——更多推理 token 用於更困難的問題
4. Planning 和 Thinking 可以組合用於同時需要廣度和深度的任務
5. 兩個功能都會消耗額外 token——依任務複雜度按比例使用
6. Claude Code 也處理 Git 操作——暫存和提交並附描述性訊息

---

# PART 2: Study Aids

> 補充學習資料，非官方課程內容。

## Familiar Analogies

- **截圖貼上** — 像是指著螢幕上的特定按鈕說「改這個」。視覺溝通消除了用文字描述 UI 元素的模糊性。
- **Planning Mode** — 像建築師在畫藍圖前先做現場勘查。你不會在理解完整佈局前就開始施工。額外的探索能捕捉到快速修補會遺漏的依賴關係。
- **Thinking Modes** — 像給工程師更多白板時間處理困難的設計問題。更多推理時間不代表要讀更多檔案——而是對同一問題進行更深入的分析。
- **Ultrathink** — 像是為關鍵系統元件進行三小時的設計審查會議。最大推理資源用於最大複雜度。
- **Planning + Thinking 組合** — 像跨團隊衝刺規劃（廣度：誰負責什麼）之後接深度技術設計會議（深度：如何實作）。複雜功能兩者都需要。
- **五個思考等級** — 像調光器而非開關。你逐漸調高推理能力：think (25%)、think more (50%)、think a lot (75%)、think longer (90%)、ultrathink (100%)。

## CCA Exam Connection

> 💡
> 本單元涵蓋兩個高權重的任務陳述。預期考題會測試：
> - **Planning Mode vs Thinking Mode** — 廣度 vs 深度的區分是最容易出題的概念。Planning = 讀取更多檔案；Thinking = 更多推理 token。
> - **何時使用哪種模式** — 給定情境（多檔案重構 vs 演算法挑戰），識別正確的模式。
> - **組合模式** — 知道兩者可以同時使用於同時具有廣度和深度複雜度的任務。
> - **啟動方式** — Shift+Tab 兩次啟用 Planning Mode；提示中的關鍵字啟用 Thinking Modes。
> - **成本意識** — 兩個功能都增加 token 用量；按比例使用是關鍵。
> - **截圖輸入** — Ctrl+V（非 Cmd+V）在 Claude Code 中貼上圖片。

## Anti-Patterns

| Anti-Pattern | 為何失敗 | 正確做法 |
|-------------|---------|---------|
| 每個任務都用 Planning Mode | 在簡單變更上浪費 token；不必要地變慢 | 簡單且範圍明確的變更使用直接執行 |
| 小任務也用 ultrathink | 浪費推理 token 卻沒有收益 | 保留 thinking modes 給真正複雜的問題 |
| 從不使用 Planning Mode | 在多檔案變更中遺漏依賴關係 | 當範圍不明確或跨多個檔案時啟用 Planning Mode |
| 只用文字描述 UI 變更 | 模糊——「左邊的按鈕」可能指很多東西 | 用 Ctrl+V 貼截圖並指出特定元素 |
| 在 macOS 上用 Cmd+V 貼截圖 | 圖片不會貼進 Claude Code | 專門使用 Ctrl+V |
| 跳過 Planning Mode 的審查步驟 | 違背目的；可能執行有缺陷的計畫 | 核准執行前一定要審查計畫 |

## Practice Questions

**Q1.** 一位開發者需要重新命名一個在 Node.js monorepo 中被 15 個檔案引用的資料庫欄位。哪種方式最適合？

- A) 直接執行——直接請 Claude 重新命名
- B) Planning Mode——讓 Claude 探索程式碼庫並在修改前建立計畫
- C) Ultrathink——請 Claude 深入推理重新命名
- D) 為每個需要修改的檔案開新的 Claude 工作階段

> 📝
> **答案：B。** 這是典型的 Planning Mode 場景：跨多個檔案的變更需要先廣泛探索程式碼庫。Planning Mode 讀取相關檔案、識別所有引用，並呈現全面的計畫。Ultrathink (C) 解決的是錯誤的問題——這需要廣度，不是深度。

**Q2.** 一位開發者正在設計新的快取策略，涉及修改資料存取層、API 路由和設定系統。最佳演算法取決於特定的存取模式。哪種方式最好？

- A) 帶有詳細提示的直接執行
- B) 只用 Planning Mode
- C) 只用 Ultrathink
- D) Planning Mode + ultrathink——Planning Mode 用於廣泛理解程式碼庫，ultrathink 用於推理最佳演算法

> 📝
> **答案：D。** 這個任務同時具有廣度複雜度（多個元件）和深度複雜度（選擇最佳演算法）。組合 Planning Mode 和 ultrathink 能同時處理兩個維度。

**Q3.** 如何在 Claude Code 中啟用 Planning Mode？

- A) 在提示中輸入 "plan"
- B) 按 Shift+Tab 兩次（若已在自動接受模式則按一次）
- C) 啟動 Claude 時使用 `--plan` 旗標
- D) 在設定檔中啟用

> 📝
> **答案：B。** Planning Mode 透過 Shift+Tab 鍵盤快捷鍵切換。從預設狀態按兩次（若已在自動接受模式則按一次）。它不是提示關鍵字——那是 Thinking Modes 的啟動方式。

**Q4.** 一位初階開發者每個請求都使用 "ultrathink"，包括加 console.log 語句。Token 用量增加了 5 倍。該給什麼建議？

- A) Ultrathink 是免費的，繼續使用
- B) 保留 thinking modes 給真正複雜的任務；簡單變更使用直接執行
- C) 所有任務都改用 Planning Mode
- D) 停止使用 Claude Code 以降低成本

> 📝
> **答案：B。** Thinking Modes 會消耗額外 token。簡單任務使用標準執行即可。Ultrathink 是給真正困難的問題使用的，在這些問題中更多推理時間確實能產生更好的結果。依任務複雜度選擇合適的工具。
