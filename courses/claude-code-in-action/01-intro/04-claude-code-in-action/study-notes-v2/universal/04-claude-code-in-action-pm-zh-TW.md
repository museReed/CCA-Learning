# Claude Code in Action — PM 策略總覽

| Item | Detail |
|------|--------|
| Exam Domain | D2: Tool Design & MCP Integration (18%), D3: Claude Code Configuration & Workflows (20%) |
| Task Statements | 2.4 (MCP integration), 2.5 (built-in tools), 3.6 (CI/CD integration), 1.1 (agentic loops) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> 📝 本節所有內容均直接來自官方課程教材。

## One-Liner / TL;DR

Claude Code 透過自主多步驟任務執行、MCP 可擴展工具、以及 CI/CD 自動化品質閘門來創造商業價值——減少效能、分析、設計和合規方面的工程瓶頸。

## Core Concepts

### Claude Code 天生就是可擴展的

Claude 本質上是一個專業的工具使用者。Claude Code 內建檔案 I/O、執行和搜尋工具——但更關鍵的是，它設計為**可擴展**的。新功能可以透過 MCP 伺服器新增，無需重新訓練或修改程式碼。

### 內建工具 — PM 需要知道的

大多數任務不需要特別配置工具。Claude 智慧地串接內建工具：

| 功能 | 商業影響 |
|------|---------|
| 檔案 I/O（Read、Write、Edit） | 自主修改程式碼，不需人工陪伴 |
| 執行（Bash） | 自動執行測試、benchmark、建置 |
| 搜尋（Grep、Glob） | 導航大型程式碼庫以理解上下文 |
| Notebook（NotebookEdit） | 帶執行的資料分析，不只是產生程式碼 |
| 網路（WebFetch、WebSearch） | 研究並驗證即時資訊 |

### 智慧工具組合

讓 Claude Code 真正強大的是它如何**組合**這些工具來處理複雜的多步驟問題。把它想成一個能自己規劃工作、執行、檢查結果、並反覆迭代的能幹團隊成員——全程不需要逐步指示。

---

## 🎬 Demo 演練：效能最佳化 — chalk 函式庫

> 即使是廣泛使用的基礎設施也可能有隱藏的效能提升空間——就像在你團隊每天使用的流程中找到 3.9 倍的效率改善。

**商業背景**：chalk 是 npm 第 5 大下載量套件（每週約 4.29 億次下載）。這個規模的效能最佳化通常需要資深工程師時間，而且經常被延後。

| 步驟 | 發生了什麼 | 截圖 |
|------|-----------|------|
| 1 | 講師介紹 chalk——npm 第 5 大下載量套件，整個生態系的基礎設施 | ![chalk docs](../../visual-guide/frames/frame_016.jpg) |
| 2 | 展示規模：每週 4.29 億次下載——這裡的改善會波及整個生態系 | ![429M downloads](../../visual-guide/frames/frame_022.jpg) |
| 3 | Claude 自主建立 todo 清單、執行 benchmark、找出效能最差的案例 | ![todo and benchmarks](../../visual-guide/frames/frame_027.jpg) |
| 4 | Claude 撰寫針對性測試檔案並使用 CPU profiling 精確定位瓶頸 | ![CPU profiling](../../visual-guide/frames/frame_030.jpg) |
| 5 | Claude 實作修正並用 benchmark 驗證改善結果 | ![3.9x improvement](../../visual-guide/frames/frame_032.jpg) |

**結果**：🏆 **3.9 倍吞吐量提升**——在步驟之間完全自主完成，無需人工介入。

**商業影響**：
- 資深工程師時間從例行最佳化工作中釋放
- 效能改善由被動變為主動
- 可量化的成果（3.9 倍）並有完整稽核紀錄

> 💡 **PM 為何關心**：Claude 自行建立任務清單並追蹤進度。這種自我管理能力意味著它能處理通常需要技術主管分解的複雜多步驟工作。

---

## 🎬 Demo 演練：Jupyter Notebook CSV 流失分析

> 「寫分析程式碼」和「寫、執行、讀結果、優化」的差別，就是範本和實際洞察的差別。

**商業背景**：從資料中獲取洞察需要分析師或資料科學家。當資料團隊滿載時，產品團隊只能等待。

| 步驟 | 發生了什麼 | 截圖 |
|------|-----------|------|
| 1 | 講師提供影音串流平台使用者 CSV 資料，要求 Claude 分析流失模式 | ![CSV dataset](../../visual-guide/frames/frame_037.jpg) |
| 2 | Claude 寫分析程式碼、執行 notebook 儲存格、讀取實際輸出 | ![notebook execution](../../visual-guide/frames/frame_041.jpg) |
| 3 | 根據發現的結果，Claude 客製化下一步分析——逐步深入洞察 | ![iterative analysis](../../visual-guide/frames/frame_044.jpg) |

**結果**：透過反覆執行產生完整的流失分析——不只是產生程式碼。

**商業影響**：
- 產品團隊不用等資料團隊就能獲得初步資料洞察
- 分析品質更高，因為 Claude 根據實際結果迭代
- 縮短產品決策的洞察時間

> 💡 **PM 為何關心**：Claude 不只是產生程式碼就交出去。它執行、讀取結果、並調整。這就是「拿到範本」和「拿到實際答案」的差別。

---

## 🎬 Demo 演練：使用 Playwright MCP 調整 UI 樣式

> 當利害關係人問「Claude 能做 X 嗎？」答案通常是「可以，用對的 MCP 伺服器」。這是你可以納入規劃的能力。

**商業背景**：UI 樣式迭代會在開發者和設計師之間產生來回溝通。每個迴圈耗費數小時或數天。

| 步驟 | 發生了什麼 | 截圖 |
|------|-----------|------|
| 1 | 講師展示一個 UI 生成應用程式——聊天介面和標題列需要樣式調整 | ![unstyled UI](../../visual-guide/frames/frame_049.jpg) |
| 2 | Claude Code 獲得 Playwright MCP 伺服器存取權——透過設定新增瀏覽器控制工具 | ![Playwright MCP](../../visual-guide/frames/frame_054.jpg) |
| 3 | Claude 開啟瀏覽器、導航到應用程式、截圖評估目前狀態 | ![browser screenshot](../../visual-guide/frames/frame_058.jpg) |
| 4 | Claude 更新樣式、重新截圖驗證，反覆迭代直到精緻 | ![improved styling](../../visual-guide/frames/frame_061.jpg) |

**結果**：透過視覺回饋迴圈達成精緻、專業的介面——以分鐘計而非小時。

**商業影響**：
- 更快的設計迭代週期（分鐘而非小時）
- 開發者自主處理樣式調整
- MCP 擴展性意味著新功能無需重新訓練——可以納入規劃

> 💡 **PM 為何關心**：MCP 就是擴展性的故事。新功能透過設定新增，不是工程工作。這代表你可以將 Claude Code 的能力成長納入路線圖。

---

## 🎬 Demo 演練：GitHub PR Review——攔截 PII 洩露

> 合規風險在合併前攔截，而非在生產環境中。擴展審查能力不需要多聘資深工程師。

**商業背景**：人工程式碼審查會遺漏跨領域的問題，如 PII 洩露，尤其在 infrastructure-as-code 中，資料流跨越多個檔案和資源。

**情境**：AWS 基礎架構含 DynamoDB → Lambda → S3 bucket。S3 bucket 與外部行銷合作夥伴共享。數月後，開發者將使用者 email 加入 Lambda 匯出——忘了 bucket 是對外共享的。這導致 PII 洩露給外部合作夥伴。

| 步驟 | 發生了什麼 | 截圖 |
|------|-----------|------|
| 1 | Claude Code 在 GitHub Actions 中運行——由 PR 或 `@claude` 提及自動觸發 | ![GitHub Actions](../../visual-guide/frames/frame_066.jpg) |
| 2 | AWS 情境：DynamoDB → Lambda → 與外部合作夥伴共享的 S3 bucket | ![AWS architecture](../../visual-guide/frames/frame_072.jpg) |
| 3 | 開發者新增一行 Lambda 程式碼——使用者 email 現在流向共享 S3 bucket | ![one-line change](../../visual-guide/frames/frame_083.jpg) |
| 4 | 建立包含 email 新增的 Pull Request | ![PR created](../../visual-guide/frames/frame_094.jpg) |
| 5 | Claude Code 攔截 PII 洩露——追蹤完整資料流並解釋外部合作夥伴風險 | ![PII caught](../../visual-guide/frames/frame_098.jpg) |

**結果**：PII 洩露在合併前被攔截。Claude 追蹤從 DynamoDB 經 Lambda 到共享 S3 bucket 的資料——理解基礎架構，而非只是掃描關鍵字。

**商業影響**：
- 合規風險在合併前攔截，而非在生產環境
- 擴展審查能力不需要多聘資深工程師
- 理解基礎架構脈絡，而非只是程式碼語法
- 不論審查者是否可用，都有一致的審查品質

> 🎯 **PM 關鍵要點**：Claude 攔截到這個問題不是因為有人寫了規則說「檢查 PII」。它理解了 Terraform 基礎架構流程並辨識出風險。這就是 **Architecture > Prompt**——Claude 以結構化方式推理系統。

---

## 講師提示

1. **Claude 自我管理複雜任務** — 它建立 todo 清單並追蹤進度，處理通常需要技術主管分解的工作
2. **從內建工具開始** — 大多數任務不需要特別設定；只在真正需要時才新增 MCP
3. **執行，不只是產生** — 「執行-觀察-優化」迴圈產生明顯更好的結果
4. **MCP 是設定，不是工程** — 新增功能是設定變更，不是開發專案
5. **CI/CD 自動化攔截人工遺漏** — 對跨檔案資料流和合規特別有價值

## Key Takeaways

1. 🔧 **內建工具處理大部分任務** — 不需要特別配置就能開始獲得價值
2. 🤖 **自主多步驟執行** — Claude 規劃、執行、觀察和優化，不需要逐步指引
3. 🔌 **MCP = 計畫性擴展** — 透過設定新增功能，納入路線圖
4. 🏗️ **CI/CD 整合提供合規價值** — 自動審查攔截架構風險，不只是語法錯誤
5. 📊 **可量化的成果** — 3.9 倍效能提升、PII 在合併前攔截、更快的迭代週期

---

# PART 2: Study Aids

> 💡 補充學習資料，非官方課程內容。

## Familiar Analogies

- **工具串接 = 生產線** — 每個站點（工具）做好一件事；序列創造成品。Claude 是決定什麼去哪裡、順序如何的廠長。
- **MCP = Claude 的 App Store** — 內建工具是預裝 app。MCP 伺服器是你為特定需求安裝的額外 app（瀏覽器控制、API 存取）。不需要全裝——只裝需要的。
- **CI/CD 審查 = 自動化品質檢查** — 就像生產線上的品管檢查點。每個 PR 通過，問題在出貨前攔截，不需增加人力就能擴展。
- **執行-觀察-優化 = 科學方法** — 假設（寫程式碼）、實驗（執行）、觀察（讀結果）、優化（調整方法）。Claude 用資料科學家實際工作的方式做資料科學。

## CCA Exam Connection

> 🎯 本課示範四種商業相關模式：

| 模式 | Demo | 商業價值 | Task Statement |
|------|------|---------|----------------|
| 自主任務管理 | Demo 1（chalk，4.29 億次下載） | 減少資深工程師在效能工作上的瓶頸 | 1.1: Agentic loops |
| 執行-觀察-優化 | Demo 2（Jupyter 流失分析） | 不依賴資料團隊就能獲得資料洞察 | 3.5: Iterative refinement |
| 透過 MCP 計畫性擴展 | Demo 3（Playwright 瀏覽器） | 透過設定而非工程新增功能 | 2.4: MCP integration |
| 自動化合規審查 | Demo 4（GitHub Actions，PII） | 合併前風險偵測，不增加人力 | 3.6: CI/CD pipelines |

## PM 決策框架

| 問題 | 指引 |
|------|------|
| 「我們需要 MCP 伺服器嗎？」 | 先不用。只在內建工具無法覆蓋特定需求時才新增（如瀏覽器測試、API 整合） |
| 「Claude Code 適合放在哪裡？」 | CI/CD 用於自動審查（Demo 4），開發者生產力用於臨時任務（Demos 1-3） |
| 「如何衡量 ROI？」 | 每項任務節省的時間、合併前攔截的問題、專家瓶頸的減少 |
| 「採用風險是什麼？」 | 內建工具低風險（不需設定）。MCP 中風險（需要設定）。CI/CD 低風險（標準 GitHub Actions） |
| 「推行順序是什麼？」 | 第一階段：內建工具 → 第二階段：CI/CD 審查 → 第三階段：MCP 擴展 |

## Anti-Patterns

| Anti-Pattern | 為何錯誤 | 正確做法 |
|-------------|---------|---------|
| 一開始就過度配置 MCP 伺服器 | 在用內建工具證明價值前增加設定成本 | 先簡單開始，特定需求出現時再擴展 |
| 把 Claude 當成「只產生」的工具 | 錯過「執行-觀察-優化」的優勢（Demo 2） | 啟用執行環境（notebook、bash） |
| 合規只靠人工程式碼審查 | 人工會遺漏跨檔案資料流，無法擴展 | 在 CI/CD 中自動化初步審查（Demo 4） |
| 期望關鍵字式 PII 偵測 | 遺漏架構風險（資料流向共享資源） | 利用 Claude 的基礎架構理解能力 |
| 所有分析都等資料團隊 | 為產品決策製造瓶頸 | 用 Claude 做初步分析，資料團隊做驗證 |

## Practice Questions

**Q1.** 你的工程團隊要採用 Claude Code。CTO 要求分階段推行計畫。根據 demo，最有效的順序是什麼？

- A) 先 MCP 擴展，然後 CI/CD，然後內建工具
- B) 內建工具用於開發者生產力，然後 CI/CD 用於自動審查，然後 MCP 用於專門工作流
- C) 先 CI/CD 以獲得即時合規價值，然後其他
- D) 同時全面部署所有功能

> 📝 **答案：B。** 第一階段：內建工具（零設定、立即產生價值——Demos 1-2）。第二階段：CI/CD 整合（GitHub Actions 設定、全組織合規——Demo 4）。第三階段：MCP 擴展（只在特定需求出現時——Demo 3）。這遵循相稱回應原則。

**Q2.** 一位重視安全的 VP 問：「如何確保 Claude Code 能攔截我們基礎架構中的 PII 洩露？」最佳回應是什麼？

- A) 「我們會為每種 PII 欄位類型撰寫明確規則」
- B) 「CI/CD 中的 Claude Code 讀取 infrastructure-as-code 並追蹤資料流——在 demo 中它透過理解架構而非被告知要找什麼來攔截 PII 洩露」
- C) 「我們需要一個自訂 MCP 伺服器來掃描 PII」
- D) 「Claude Code 無法可靠地攔截 PII——我們需要專門工具」

> 📝 **答案：B。** Claude Code 理解 Terraform 基礎架構並追蹤資料流（DynamoDB → Lambda → 共享 S3 bucket）。它在未被明確告知檢查 PII 的情況下攔截了使用者 email 對外部合作夥伴的洩露。這就是 Architecture > Prompt——Claude 以結構化方式推理系統。

**Q3.** 你的團隊每週花 20 小時在程式碼審查上。如何定位 Claude Code 的 CI/CD 整合來證明設定投資的正當性？

- A) 「它會取代所有人工程式碼審查」
- B) 「它增強人工審查——自動化初步審查攔截結構和合規問題，人工聚焦在業務邏輯和架構決策」
- C) 「它只能攔截 PII 問題，價值有限」
- D) 「它需要大量工程投資來設定」

> 📝 **答案：B。** Claude Code 處理初步審查（結構問題、安全、合規）。人工審查者聚焦在業務邏輯和架構決策。預期：審查週期縮短 30-50%、合規遺漏趨近零、一致的品質。設定成本：標準 GitHub Actions workflow——幾小時的工程時間。

**Q4.** 另一個團隊的 PM 問：「Claude Code 能幫我們分析使用者流失資料而不用等資料團隊嗎？」你怎麼說？

- A) 「不行，Claude Code 只能寫程式碼」
- B) 「可以——Claude 能在 Jupyter notebook 中寫分析程式碼、執行、讀取實際結果並迭代。像是有一個初步資料分析師，不過關鍵發現應由資料團隊驗證」
- C) 「可以，但只有設定專門的資料分析 MCP 伺服器才行」
- D) 「不行，資料分析需要專門模型」

> 📝 **答案：B。** Demo 2 正是展示了這個：Claude 透過寫程式碼、執行儲存格、讀取輸出、優化分析來分析流失資料。「執行-觀察-優化」迴圈產生真正的洞察，不只是程式碼範本。用於初步分析；關鍵發現由資料團隊驗證。
