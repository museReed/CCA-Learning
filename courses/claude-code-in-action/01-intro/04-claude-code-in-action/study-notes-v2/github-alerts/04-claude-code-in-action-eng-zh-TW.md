# Claude Code in Action — 工程師深度解析

| Item | Detail |
|------|--------|
| Exam Domain | D2: Tool Design & MCP Integration (18%), D3: Claude Code Configuration & Workflows (20%) |
| Task Statements | 2.4 (MCP integration), 2.5 (built-in tools), 3.6 (CI/CD integration), 1.1 (agentic loops) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> [!NOTE]
> 本節所有內容均直接來自官方課程教材。

## One-Liner / TL;DR

Claude Code 的威力來自智慧化串接內建工具、透過 MCP 伺服器擴展能力、以及整合 CI/CD 流水線——而非任何單一工具。

## Core Concepts

### Claude 是工具使用專家

課程強調 Claude 本質上是一個專業的工具使用者。Claude Code 設計為**可擴展**的——除了內建工具外，你可以透過 MCP 伺服器和自訂整合來新增功能。

### 內建工具

Claude Code 內建一組用於檔案 I/O、執行和搜尋的預設工具：

| 工具 | 用途 |
|------|------|
| Read | 讀取檔案內容（支援圖片、PDF、notebook） |
| Write | 建立或覆寫檔案 |
| Edit | 對現有檔案進行精準、局部的編輯 |
| Bash | 執行 shell 指令 |
| Grep | 使用 regex 搜尋檔案內容（基於 ripgrep） |
| Glob | 按檔名/模式尋找檔案 |
| NotebookEdit | 編輯 Jupyter notebook 儲存格 |
| WebFetch | 擷取並分析網頁內容 |
| WebSearch | 搜尋網路上的即時資訊 |

### 智慧工具組合

讓 Claude Code 真正強大的是它如何**組合**這些工具來處理複雜的多步驟問題。本課每個 demo 都展示了不同的串接模式——從 profiling 和 benchmarking 到執行 notebook 儲存格和控制瀏覽器。

---

## Demo 演練：效能最佳化 — chalk 函式庫

> [!NOTE]
> 講師實機示範的逐步演練。截圖取自實際課程影片。

**背景**：chalk 是 npm 第 5 大下載量套件，每週約 4.29 億次下載。即使是微小的效能改善都會對整個生態系產生巨大影響。

| 步驟 | 發生了什麼 | 截圖 |
|------|-----------|------|
| 1 | 講師介紹 chalk——npm 第 5 大下載量套件，用於終端機彩色文字 | ![chalk docs](../../visual-guide/frames/frame_016.jpg) |
| 2 | 展示下載統計：每週 4.29 億次下載 | ![429M downloads](../../visual-guide/frames/frame_022.jpg) |
| 3 | 要求 Claude 找出並最佳化效能問題。Claude 建立 todo 清單追蹤進度，然後執行 benchmark 找出最差的情況 | ![todo and benchmarks](../../visual-guide/frames/frame_027.jpg) |
| 4 | Claude 撰寫檔案聚焦在一個特定案例，然後使用 CPU profiler 了解為何緩慢 | ![CPU profiling](../../visual-guide/frames/frame_030.jpg) |
| 5 | Claude 實作最佳化並驗證結果 | ![3.9x improvement](../../visual-guide/frames/frame_032.jpg) |

**結果**：目標操作達到 **3.9 倍吞吐量提升**。

> [!TIP]
> Claude 自行建立 todo 清單並追蹤複雜任務的進度。這種自我管理行為是 agentic loop 在多步驟中維持連貫性的方式——計畫 → 執行 → 觀察 → 優化。

---

## Demo 演練：Jupyter Notebook CSV 流失分析

> [!NOTE]
> Claude 不只是寫程式——它會執行、讀取結果、然後調整。

**背景**：影音串流平台使用者的 CSV 資料集。目標：分析使用者流失模式。

| 步驟 | 發生了什麼 | 截圖 |
|------|-----------|------|
| 1 | 講師提供影音串流平台使用者 CSV 資料，要求 Claude 在 Jupyter notebook 中分析流失原因 | ![CSV dataset](../../visual-guide/frames/frame_037.jpg) |
| 2 | Claude 將分析程式碼寫入 notebook 儲存格、執行並查看輸出結果 | ![notebook execution](../../visual-guide/frames/frame_041.jpg) |
| 3 | Claude 根據前一次的執行結果客製化後續儲存格——逐步深入分析 | ![iterative analysis](../../visual-guide/frames/frame_044.jpg) |

**結果**：Claude 透過執行、觀察和優化產生完整的流失分析——不只是產生程式碼。

> [!TIP]
> 關鍵差異在於「執行-觀察-優化」迴圈。Claude 執行儲存格、讀取實際輸出，然後決定下一步分析什麼。這比「只產生程式碼」的方法產生出明顯更好的分析結果。

---

## Demo 演練：使用 Playwright MCP 調整 UI 樣式

> [!NOTE]
> 展示 MCP 伺服器如何將 Claude Code 的能力擴展到內建工具之外。

**背景**：一個 UI 生成應用程式，其聊天介面和標題列需要樣式修正。

| 步驟 | 發生了什麼 | 截圖 |
|------|-----------|------|
| 1 | 講師展示 UI 應用程式——聊天介面和標題列看起來未經設計、很粗糙 | ![unstyled UI](../../visual-guide/frames/frame_049.jpg) |
| 2 | 給予 Claude Code Playwright MCP 伺服器的存取權——新增瀏覽器控制工具 | ![Playwright MCP](../../visual-guide/frames/frame_054.jpg) |
| 3 | Claude 開啟瀏覽器、導航到應用程式、截圖查看目前狀態 | ![browser screenshot](../../visual-guide/frames/frame_058.jpg) |
| 4 | Claude 更新樣式、再次截圖驗證，反覆迭代直到結果精緻 | ![improved styling](../../visual-guide/frames/frame_061.jpg) |

**結果**：透過視覺回饋迴圈達成精緻、專業的介面。

> [!TIP]
> MCP 工具透過設定檔加入——不需要重新訓練或修改程式碼。Claude 僅根據工具描述就能適應新工具。這就是擴展性的故事：當內建工具不夠用時，MCP 來補足。

---

## Demo 演練：GitHub PR Review——攔截 PII 洩露

> [!IMPORTANT]
> 本課最長的 demo。展示 Claude Code 在 CI/CD 中運行以攔截人工審查會遺漏的安全問題。

**背景**：Claude Code 在 GitHub Actions 內運行，由 PR 建立或在評論中 `@claude` 觸發。

**情境設置**：
- AWS 基礎架構：**DynamoDB** 資料表 → **Lambda** 函式 → **S3 bucket**
- 該 S3 bucket 與**外部行銷合作夥伴**共享
- 數月後，內部團隊要求將使用者 email 加入匯出資料
- 開發者在 Lambda 函式中新增一行——忘了這個 bucket 是對外共享的
- 這導致 **PII（使用者 email）** 洩露給外部合作夥伴——嚴重的安全/合規風險

| 步驟 | 發生了什麼 | 截圖 |
|------|-----------|------|
| 1 | 講師說明 Claude Code 可在 GitHub Actions 中運行——由 PR 或 `@claude` 提及觸發 | ![GitHub Actions integration](../../visual-guide/frames/frame_066.jpg) |
| 2 | 設置 AWS 情境：DynamoDB → Lambda → 與外部合作夥伴共享的 S3 bucket | ![AWS architecture](../../visual-guide/frames/frame_072.jpg) |
| 3 | 開發者新增一行——使用者 email 現在包含在 Lambda 匯出到共享 S3 bucket 的資料中 | ![one-line change](../../visual-guide/frames/frame_083.jpg) |
| 4 | 建立包含 email 新增變更的 Pull Request | ![PR created](../../visual-guide/frames/frame_094.jpg) |
| 5 | Claude Code 自動審查攔截 PII 洩露——顯示完整資料流並解釋外部合作夥伴風險 | ![PII review caught](../../visual-guide/frames/frame_098.jpg) |

**結果**：Claude 透過理解基礎架構流程攔截了 PII 洩露——不是因為被告知「檢查 PII」，而是因為它追蹤了從 DynamoDB 經過 Lambda 到共享 S3 bucket 的資料流。

> [!WARNING]
> 這直接對應 Task 3.6（CI/CD 整合）。Claude 以結構化方式理解 infrastructure-as-code，能攔截規則掃描器會遺漏的問題。這體現了 **Architecture > Prompt** 的理念。

---

## 講師提示

1. **透過 todo 清單自我管理** — Claude 為複雜工作建立結構化任務清單，不需要人要求就會追蹤進度
2. **從內建工具開始** — 大多數任務不需要 MCP 擴展；只在內建功能真的不夠時才新增
3. **執行，不只是產生** — 「寫程式碼」和「寫、執行、讀取輸出、調整」之間的品質差異很大
4. **MCP 是設定，不是程式碼** — 新增工具能力只需要修改設定檔，不需要重新訓練
5. **CI/CD 能攔截人工遺漏的問題** — 自動審查能理解跨檔案的資料流，這在人工審查中容易被忽略

## Key Takeaways

1. **內建工具很強大** — Read、Write、Edit、Bash、Grep、Glob 涵蓋大部分開發任務
2. **工具串接是乘數** — 順序和組合比單一工具更重要
3. **MCP 擴展而非取代** — MCP 伺服器新增內建工具無法涵蓋的功能（瀏覽器、API）
4. **CI/CD 整合是一級功能** — Claude Code 在 GitHub Actions 中進行自動審查是生產環境的用例
5. **架構理解 > 明確指令** — Claude 對程式碼結構、資料流和基礎架構進行推理

---

# PART 2: Study Aids

> [!NOTE]
> 補充學習資料，非官方課程內容。

## Familiar Analogies

- **工具串接 = Unix 管道** — 就像 `cat file | grep pattern | sort | uniq`，Claude 串接 Read → Bash（profiling）→ Edit（修正）→ Bash（驗證）。每個工具做好一件事；串接創造價值。
- **MCP = USB 接口** — 你的筆電有內建功能（螢幕、鍵盤）。USB 接口讓你插入新裝置（相機、外接硬碟）。MCP 伺服器就是 Claude Code 的 USB 接口——按需插入瀏覽器控制、API 存取、資料庫工具。
- **Claude 的 todo 清單 = 資深工程師的草稿紙** — 資深工程師處理複雜問題時會先寫下步驟。Claude 也一樣，但用結構化格式來追蹤和打勾。
- **CI/CD 審查 = 機場安檢 X 光** — 掃描所有通過的東西（每個 PR），攔截人類可能遺漏的東西（資料流中的 PII），而且不會疲倦或分心。

## CCA Exam Connection

> [!TIP]
> 本課涵蓋跨三個 domain 的**四個考試相關模式**：

| 模式 | Demo | Task Statement | 考試相關性 |
|------|------|----------------|-----------|
| 計畫 → 執行 → 驗證 | Demo 1（chalk） | 1.1: Agentic loops | Claude 如何自主管理多步驟任務 |
| 執行 → 觀察 → 優化 | Demo 2（Jupyter） | 3.5: Iterative refinement | 「只產生」vs「執行-迭代」的品質差異 |
| MCP 工具採用 | Demo 3（Playwright） | 2.4: MCP integration | 何時及如何擴展 Claude Code 的能力 |
| 自動化 CI/CD 審查 | Demo 4（GitHub Actions） | 3.6: CI/CD pipelines | 具備基礎架構感知的自動審查 |

> [!TIP]
> **考試理念：相稱回應** — 從內建工具開始。只在內建功能真的不夠時才新增 MCP 或自訂工具。考試測試的是你知道「何時」擴展，而不只是「如何」擴展。

## Anti-Patterns

| Anti-Pattern | 為何錯誤 | 正確做法 |
|-------------|---------|---------|
| 在嘗試內建工具前就新增 MCP 伺服器 | 過度工程化；內建工具能處理大多數任務 | 先用 Read/Write/Edit/Bash/Grep，需要時再擴展 |
| 寫程式碼但不執行 | 「只產生」的方法會遺漏執行時錯誤和資料相關問題 | 執行、觀察輸出、優化（Demo 2 模式） |
| 僅依賴人工 PR 審查處理安全問題 | 人工會遺漏跨檔案資料流問題，尤其在 infra-as-code | 用 Claude Code 在 CI/CD 中自動化初步審查（Demo 4） |
| 期望 Claude 透過關鍵字比對來攔截問題 | 規則掃描器會遺漏架構層面的問題 | Claude 以結構化方式理解基礎架構——Architecture > Prompt |
| 給 Claude 單一的大型 prompt 處理複雜任務 | 壓垮上下文、降低品質 | 讓 Claude 用自己的 todo 清單分解步驟（Demo 1） |

## Practice Questions

**Q1.** 你的團隊使用 Terraform 管理 AWS 基礎架構。有位開發者提交 PR，將 `user_phone` 新增到一個寫入與第三方分析夥伴共享的 S3 bucket 的 Lambda 函式中。Claude Code 應如何設定來攔截這個問題？

- A) 新增 regex 規則掃描 PR 中的 PII 欄位名稱
- B) 將 Claude Code 設定為 PR 建立時觸發的 GitHub Actions workflow
- C) 撰寫自訂 MCP 伺服器來掃描 PII 模式
- D) 在 CLAUDE.md 中列出所有要監控的 PII 欄位

> [!NOTE]
> **答案：B。** 在 GitHub Actions 中設定 Claude Code（Task 3.6）。Claude 讀取 Terraform 檔案、追蹤資料流（Lambda → 共享 S3 bucket），並標記對外部合作夥伴的 PII 洩露。不需要明確的「檢查 PII」提示——Claude 以結構化方式理解基礎架構。這就是 Architecture > Prompt 的實踐。

**Q2.** 你需要 Claude Code 最佳化一個 Python 函式的效能。哪個工具序列代表最佳方法？

- A) 直接用已知的最佳化模式 Edit 程式碼
- B) Read → Bash（執行 profiler）→ Read profiler 輸出 → Edit（套用修正）→ Bash（重新執行 benchmark）
- C) 從頭 Write 一個全新的實作
- D) Grep 搜尋程式碼庫中類似的最佳化然後複製

> [!NOTE]
> **答案：B。** 這遵循 Demo 1 的「計畫 → Profiling → 修正 → 驗證」模式。Claude 應該在最佳化前先測量，然後驗證改善結果。選項 A 跳過測量。選項 C 不成比例。選項 D 無法解決特定瓶頸。測試 Task 2.5（內建工具）和 1.1（agentic loops）。

**Q3.** 你想讓 Claude Code 在 CSS 變更後驗證 web 應用程式登入頁面的渲染是否正確。哪種方法最合適？

- A) 讓 Claude Read CSS 檔案並推理視覺呈現
- B) 新增 Playwright MCP 伺服器讓 Claude 能截圖並視覺驗證
- C) 為每個 CSS 屬性撰寫單元測試
- D) 用 Bash 執行 headless 瀏覽器並儲存截圖供人工檢視

> [!NOTE]
> **答案：B。** 與 Demo 3 完全相符。Playwright MCP 給予 Claude 瀏覽器控制能力來截圖和視覺驗證——建立緊密的回饋迴圈。選項 A 無法驗證視覺渲染。選項 C 太脆弱。選項 D 需要人工審查。測試 Task 2.4（MCP integration）。

**Q4.** Claude Code 的 Jupyter notebook 分析（Demo 2）與標準程式碼產生方法有何不同？

- A) Claude 使用專門的資料科學模型
- B) Claude 寫程式碼、執行儲存格、讀取實際輸出，並根據結果客製化下一步
- C) Claude 有存取預建分析範本的權限
- D) Claude 直接透過 API 連接資料來源

> [!NOTE]
> **答案：B。** 「執行-觀察-優化」迴圈是關鍵差異。Claude 不只是產生程式碼——它執行儲存格、讀取結果、並調整分析。這比「只產生」的方法產生明顯更好的洞察。測試 Task 3.5（iterative refinement）。
