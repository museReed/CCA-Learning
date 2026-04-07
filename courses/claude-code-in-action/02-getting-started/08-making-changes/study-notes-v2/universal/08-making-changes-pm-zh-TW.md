# Making Changes — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows |
| Task Statements | 3.4 (plan mode vs direct), 3.5 (iterative refinement) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> 本節所有內容均直接來自官方課程教材。

## One-Liner / TL;DR

Claude Code 在基本聊天之外有兩個強大功能——Planning Mode（行動前先研究和提案）和 Thinking Modes（針對更難的問題進行更深度的推理）——加上截圖視覺輸入，改變了設計到開發的交接方式。

## Core Concepts

### 截圖精確溝通

開發者可以直接將截圖貼到 Claude Code 中，用視覺方式溝通 UI 變更：

1. 截取要修改的元素的截圖
2. 用 **Ctrl+V** 貼上（macOS 上不是 Cmd+V）
3. 描述想要的變更

**PM 重點：** 這改變了設計到開發的交接方式。設計師和 PM 可以提供標注過的截圖——「改這個特定元素」——而不是撰寫詳細的規格書。視覺溝通現在是 AI 輔助開發的一等公民輸入方式。

### Planning Mode

Planning Mode 就像請你的助理在行動前先做研究和提案——類似於初階開發者在寫程式前先寫設計文件。

**啟用方式：** 按 **Shift+Tab 兩次**（若已在自動接受模式則按一次）。

在 Planning Mode 中，Claude 會：

1. **讀取更多檔案** — 廣泛研究程式碼庫，像開發者在修改前先熟悉新的 repo
2. **建立詳細的實作計畫** — 呈現逐步的提案
3. **展示預計的操作** — 在任何程式碼變更前完全透明
4. **等待核准** — 開發者審查並可調整方向，就像在 sprint 承諾前審查設計文件

這不只是「較慢的執行」。它是一個根本不同的工作流程，收集更多脈絡、捕捉依賴關係，並降低多檔案不完整變更的風險。

### Thinking Modes

Thinking Modes 給 Claude 漸進式更多的推理時間——像給顧問額外的天數進行更深入的分析，而不是快速給意見。

| 模式 | 推理深度 | 商業類比 |
|------|---------|---------|
| "Think" | 基礎延伸 | 快速 30 分鐘分析 |
| "Think more" | 延伸 | 半天深度研究 |
| "Think a lot" | 全面 | 一整天的策略會議 |
| "Think longer" | 延長時間 | 多天的研究專案 |
| "Ultrathink" | 最大化 | 一週的全面稽核 |

每個等級讓 Claude 有漸進式更多的 token 進行更深入的分析。開發者在提示中包含關鍵字來啟用。

### Planning vs Thinking — 廣度 vs 深度

這兩個功能處理不同類型的複雜度：

| 維度 | Planning Mode | Thinking Mode |
|------|--------------|---------------|
| **作用** | 廣泛研究程式碼庫 | 對問題進行更深入的推理 |
| **商業類比** | 專案啟動——在承諾前調查所有利害關係人和系統 | 策略深潛——對特定決策進行徹底分析 |
| **複雜度類型** | 廣度——多個檔案、多個元件 | 深度——複雜邏輯、模糊需求 |
| **啟動方式** | Shift+Tab 兩次（切換） | 提示中的關鍵字（"think"、"ultrathink"） |
| **成本驅動** | 更多檔案讀取（工具呼叫） | 更多推理 token |

**PM 決策框架：**
- **簡單任務**（修正錯字、改顏色）→ 直接執行。快速、便宜。
- **多檔案任務**（跨 15 個檔案重命名、新增觸及多個模組的功能）→ Planning Mode。更多 token 但能捕捉依賴關係。
- **複雜邏輯**（設計快取演算法、除錯 race condition）→ Thinking Mode。更多推理 token。
- **既廣又深**（從零建構新帳務模組）→ Planning Mode + Thinking。最高 token 成本但對複雜工作品質最好。

兩個功能都會消耗額外 token——這是 PM 應該監控的成本-品質取捨。

### Git 整合

Claude Code 也兼任 Git 助手——開發者可以請它暫存變更並建立附有描述性訊息的 commit，不需離開終端。這串接了開發到提交的工作流程，特別是在反覆修改之後。

## Demo Walkthrough: Screenshot Paste — 置中佔位文字

| 步驟 | 發生了什麼 | 畫面 |
|------|-----------|------|
| 1. 啟動開發伺服器 | 講師執行 `npm run dev` 並在 localhost:3000 開啟應用程式 | ![frame_003](../../visual-guide/frames/frame_003.jpg) |
| 2. 發現問題 | 佔位文字位於左側面板但未置中 | ![frame_006](../../visual-guide/frames/frame_006.jpg) |
| 3. 截圖 + 貼上 | 截取佔位文字的截圖，用 Ctrl+V 貼到 Claude Code | ![frame_009](../../visual-guide/frames/frame_009.jpg) |
| 4. 結果 | Claude 搜尋程式碼庫、更新樣式——佔位文字已置中 | ![frame_012](../../visual-guide/frames/frame_012.jpg) |

**PM 重點：** 從「我看到一個問題」到「問題解決」整個過程不到一分鐘。不需要 Jira ticket、不需要設計規格、不需要 CSS 檔名。開發者用截圖給 Claude 看問題，然後用一句話描述修改。

## Demo Walkthrough: Plan Mode + Thinking — 複雜功能實作

| 步驟 | 發生了什麼 | 畫面 |
|------|-----------|------|
| 1. 發現問題 | 生成 card 元件後，講師注意到 "String Replace Editor"——顯示給使用者的技術工具名稱 | ![frame_018](../../visual-guide/frames/frame_018.jpg) |
| 2. 截圖記錄問題 | 截取技術文字的截圖並貼到 Claude Code | ![frame_027](../../visual-guide/frames/frame_027.jpg) |
| 3. 啟用 Plan Mode | 按 Shift+Tab 兩次啟用 Planning Mode——Claude 會在行動前先研究和規劃 | ![frame_035](../../visual-guide/frames/frame_035.jpg) |
| 4. 加入 ultrathink | 加入 "ultrathink" 以獲得最大推理深度；說明廣度（規劃）vs 深度（思考） | ![frame_049](../../visual-guide/frames/frame_049.jpg) |
| 5. 組合執行 | Plan Mode + ultrathink 同時運作——廣泛的程式碼庫探索搭配深度推理 | ![frame_054](../../visual-guide/frames/frame_054.jpg) |
| 6. 功能完成 | 技術工具名稱被替換為使用者友善的訊息：「Creating file:」和「Editing file:」 | ![frame_069](../../visual-guide/frames/frame_069.jpg) |
| 7. 驗證 | 後續編輯確認功能正常——顯示「Editing app.jsx」而非工具名稱 | ![frame_075](../../visual-guide/frames/frame_075.jpg) |

**PM 重點：** 這是一個 UX 改善，涉及多個檔案且需要理解應用程式如何渲染工具互動。用 Planning Mode + ultrathink，開發者大約兩分鐘完成。沒有 AI 輔助的話，這需要：(1) 找出工具名稱在哪裡渲染、(2) 追蹤資料流、(3) 修改顯示邏輯、(4) 測試建立和編輯兩條路徑。輕鬆就是 1-2 小時的任務壓縮到幾分鐘。

## Instructor Tips

- **Ctrl+V** 貼截圖，不是 Cmd+V——這是 macOS 使用者常遇到的問題
- Planning Mode 適合開發者事前不知道完整範圍的任務
- Ultrathink 用於最困難的問題——它是最大推理能力
- 兩個功能都有 token 成本——團隊應該制定按比例使用的指引
- Claude Code 也處理 Git 暫存和提交——開發者少一次脈絡切換

## Key Takeaways

1. 截圖實現視覺溝通——PM 和設計師可以提供標注圖片而非撰寫書面規格
2. Planning Mode（Shift+Tab 兩次）= 請 Claude 在行動前先研究和提案——降低複雜任務的風險
3. Thinking Modes（think / think more / think a lot / think longer / ultrathink）= 給 Claude 更多推理時間處理更難的問題
4. Planning 和 Thinking 可以組合——廣度 + 深度用於最複雜的任務
5. 兩個功能都增加 token 成本——PM 應監控使用並制定按比例使用的指引
6. Claude Code 也處理 Git 操作——暫存和提交並附描述性訊息

---

# PART 2: Study Aids

> 補充學習資料，非官方課程內容。

## Familiar Analogies

- **截圖貼上** — 像設計師在 mockup 上圈選元素並寫「改這個」。視覺脈絡消除了關於討論哪個元素的來回溝通。
- **Planning Mode** — 像請初階開發者在寫程式前先寫設計文件。他們研究程式碼庫、找出所有需要改動的檔案，並在提交任何程式碼前呈現計畫供審查。
- **Thinking Modes** — 像給顧問額外的分析時間。快速意見需要 30 分鐘；徹底的分析需要一週。每個思考等級是不同的推理時間預算。
- **Ultrathink** — 像委託全面稽核而非抽樣檢查。最大分析資源帶來結果的最大信心。
- **Planning + Thinking 組合** — 像專案啟動（調查所有團隊和系統）之後接深度技術設計會議（解決最難的架構問題）。複雜專案兩者都需要。
- **簡單任務用直接執行** — 像一則快速的 Slack 訊息：「修正第 42 行的錯字。」不需要開會，不需要規劃文件，直接做。

## CCA Exam Connection

> 💡
> 作為 PM，你需要知道：
> - **Planning Mode vs Thinking Mode** — 廣度 vs 深度。這是最容易出題的區分。Planning 讀取更多檔案；Thinking 推理更深入。
> - **成本影響** — 兩個功能都增加 token 消耗。預期會有關於何時成本合理 vs 浪費的考題。
> - **啟動方式** — Shift+Tab 兩次啟用 Planning Mode；提示中的關鍵字啟用 Thinking Modes。
> - **截圖輸入** — Ctrl+V（非 Cmd+V）貼圖片。改變了設計到開發的交接方式。
> - **組合模式** — 知道兩者可以同時使用，以及何時適合。
> - **按比例使用** — 考試會測試你是否理解將工具能力配對到任務複雜度。

## Anti-Patterns

| Anti-Pattern | 為何失敗 | 正確做法 |
|-------------|---------|---------|
| 要求所有任務都用 Planning Mode | 浪費 token 並減慢簡單變更的速度 | 制定指引：多檔案任務用 Planning Mode，簡單編輯用直接執行 |
| 忽視強大功能的 token 成本 | 整個團隊預設用 ultrathink 導致預算超支 | 制定團隊指引——依任務複雜度配對模式 |
| 截圖就夠的時候還寫詳細文字規格 | 比視覺溝通更慢且更模糊 | 鼓勵 UI 變更使用截圖溝通 |
| 為了降成本而禁止 ultrathink | 移除了真正複雜任務的有價值工具 | 保留給複雜任務；禁止濫用，不是禁止功能本身 |
| 不審查 Planning Mode 的輸出 | 違背了審查-核准循環的目的 | 確保開發者在核准前一定審查計畫 |
| 以為 Claude Code 只能寫程式 | 錯過了暫存和提交的 Git 整合 | 將 Git 工作流程納入團隊的 Claude Code 使用模式 |

## Practice Questions

**Q1.** 你的工程團隊這個月 Claude Code token 用量翻倍了。調查發現開發者大部分任務都用 "ultrathink"，包括簡單的任務。適當的 PM 回應是什麼？

- A) 完全禁止 ultrathink
- B) 制定指引：保留 ultrathink 給複雜推理任務，簡單變更用直接執行，多檔案工作用 Planning Mode
- C) 接受較高的成本作為更好品質的代價
- D) 要求開發者減少使用 Claude Code 的頻率

> 📝
> **答案：B。** 問題是濫用，不是功能本身。制定依任務複雜度配對模式的使用指引能同時優化品質和成本。這是按比例的回應。

**Q2.** 你的設計團隊問：「我們可以把截圖給開發者讓 Claude 實作嗎？」根據本課程，正確答案是什麼？

- A) 不行，Claude Code 不支援圖片輸入
- B) 可以，開發者可以用 Ctrl+V 直接將截圖貼到 Claude Code，Claude 用視覺脈絡來實作或修改 UI 元素
- C) 只有先把截圖轉換成文字描述才行
- D) 截圖只能用於錯誤回報，不能用於新設計

> 📝
> **答案：B。** 截圖溝通是主要的輸入方式。設計師提供截圖，開發者用 Ctrl+V 貼上，Claude 用多模態理解來實作變更。這改變了設計到開發的交接方式。

**Q3.** 你正在為一組混合任務估算 sprint velocity。哪個模式對應是正確的？

- A) 簡單 bug fix → Planning Mode；複雜重構 → 直接執行
- B) 簡單 bug fix → 直接執行；多檔案重構 → Planning Mode；複雜演算法 → Thinking Mode；複雜新模組 → Planning Mode + Thinking
- C) 所有任務 → Ultrathink 以獲得最佳品質
- D) 所有任務 → Planning Mode 以確保安全

> 📝
> **答案：B。** 依任務複雜度配對模式。簡單任務需要直接執行（快速、便宜）。多檔案任務需要 Planning Mode（廣度）。複雜推理需要 Thinking Mode（深度）。同時具備兩者的任務需要組合使用。每個任務都用最強模式會浪費 token 而沒有相應的收益。

**Q4.** Claude Code 中如何啟用 Planning Mode？

- A) 在提示中輸入 "plan"
- B) 按 Shift+Tab 兩次（若已在自動接受模式則按一次）
- C) 使用 `--plan` 命令列旗標
- D) 在專案設定中啟用

> 📝
> **答案：B。** Planning Mode 透過 Shift+Tab 鍵盤快捷鍵切換。這與 Thinking Modes 不同，Thinking Modes 是透過提示中的關鍵字啟用（think、ultrathink 等）。
